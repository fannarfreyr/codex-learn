"""Inspectable file-backed learner evidence. No grading model or external dependencies."""

import argparse
import copy
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import tempfile
import uuid


REPO = Path(__file__).resolve().parents[1]
IDS = tuple('graph-theory.' + name for name in (
    'terminology', 'connectivity', 'trees', 'bfs', 'dfs',
    'bfs-shortest-paths', 'spanning-trees'))
SCOPES = dict(zip(IDS, (
    'Vertices, edges, adjacency, degree',
    'Paths and reachability in finite simple undirected graphs',
    'Connected acyclic graphs; identify and explain examples',
    'Explain and trace breadth-first exploration',
    'Explain and trace depth-first exploration',
    'Explain and apply BFS to unweighted shortest paths',
    'Identify and construct a spanning tree')))
CAPABILITIES = {'recognition', 'definition', 'explanation', 'derivation', 'application', 'problem_solving'}
REPORTS = {'never_seen', 'studied_before', 'forgotten', 'recognize',
           'not_deeply_understood', 'knows_without_name', 'competent', 'skip'}
OUTCOMES = {'correct', 'partial', 'incorrect', 'skip'}
KINDS = {'assessment', 'self_report', 'background_declaration', 'correction'}


class StateError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise StateError(message)


def now():
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def identifier(value):
    require(isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', value), 'Unsafe or missing ID')
    return value


def nonempty(value, label):
    require(isinstance(value, str) and bool(value.strip()), f'Missing {label}')


def evaluation(value):
    require(isinstance(value, dict), 'Missing evaluation')
    require(value.get('outcome') in OUTCOMES, 'Invalid evaluation outcome')
    nonempty(value.get('rationale'), 'evaluation rationale')
    require(isinstance(value.get('misconceptions', []), list), 'Misconceptions must be a list')
    for item in value.get('misconceptions', []):
        nonempty(item, 'misconception')


def validate_event(event, existing, allow_synthetic=False):
    require(isinstance(event, dict), 'Evidence must be an object')
    require(event.get('schema_version') == 1, 'Unsupported evidence schema version')
    identifier(event.get('id'))
    identifier(event.get('session_id'))
    try:
        stamp = datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00'))
        require(stamp.tzinfo is not None, 'Timestamp needs timezone')
    except (KeyError, TypeError, ValueError, AttributeError) as error:
        raise StateError('Invalid timestamp') from error
    concepts = event.get('concept_ids')
    require(isinstance(concepts, list) and len(concepts) == len(set(concepts)), 'Invalid concept list')
    require(all(c in IDS for c in concepts), 'Unknown concept ID')
    provenance = event.get('provenance', {})
    require(provenance.get('source') in {'learner', 'synthetic'}, 'Invalid provenance source')
    nonempty(provenance.get('surface'), 'provenance surface')
    require(allow_synthetic or provenance['source'] == 'learner', 'Synthetic evidence requires isolated validation state')
    kind = event.get('kind')
    require(kind in KINDS, 'Invalid evidence kind')
    if 'turn_id' in event:
        require(kind in {'assessment', 'self_report'}, 'Only learner responses have turn IDs')
        identifier(event['turn_id'])
    if kind == 'assessment':
        require(len(concepts) == 1, 'Assess each credited concept separately')
        question = event.get('question', {})
        identifier(question.get('id'))
        nonempty(question.get('text'), 'question')
        nonempty(question.get('scope'), 'question scope')
        require(question.get('capability') in CAPABILITIES, 'Invalid capability')
        require(type(question.get('scope_version', 1)) is int and question.get('scope_version', 1) >= 1, 'Invalid scope version')
        require(type(question.get('novel', False)) is bool, 'Novel must be boolean')
        nonempty(event.get('response'), 'actual response')
        require(event.get('assistance') in {'none', 'hint', 'solution'}, 'Invalid assistance')
        rubric = event.get('rubric', {}).get('criteria')
        require(isinstance(rubric, list) and bool(rubric), 'Missing rubric criteria')
        for criterion in rubric:
            nonempty(criterion, 'rubric criterion')
        evaluation(event.get('evaluation'))
        if question.get('novel', False):
            require(not any(e['kind'] == 'assessment' and e['id'] != event['id']
                            and e['question']['id'] == question['id'] for e in existing.values()),
                    'Previously assessed question cannot be a novel application')
    elif kind == 'self_report':
        require(len(concepts) == 1, 'Self-report needs one scoped concept')
        require(event.get('report_type') in REPORTS, 'Invalid report type')
        nonempty(event.get('statement'), 'self-report statement')
    elif kind == 'background_declaration':
        require(not concepts, 'Background does not directly assert concept competence')
        nonempty(event.get('statement'), 'background declaration')
        category = event.get('background_category')
        require(category is None or isinstance(category, str), 'Invalid background category')
    else:
        require(not any(k in event for k in ('response', 'assistance', 'question', 'rubric')),
                'Corrections change evaluation only; preserve the original observation')
        target = existing.get(event.get('target_id'))
        require(target is not None, 'Correction target does not exist')
        require(target['kind'] in {'assessment', 'correction'}, 'Only assessment evaluations can be corrected')
        require(concepts == target['concept_ids'], 'Correction cannot change concept scope')
        require(provenance['source'] == target['provenance']['source'], 'Correction cannot change provenance')
        nonempty(event.get('reason'), 'correction reason')
        evaluation(event.get('evaluation'))


def effective_assessments(events):
    """Apply explicit evaluation corrections without changing recorded responses."""
    result = {}
    roots = {}
    for event in events:
        if event['kind'] == 'assessment':
            result[event['id']] = copy.deepcopy(event)
            result[event['id']]['evaluation_ref'] = event['id']
            roots[event['id']] = event['id']
        elif event['kind'] == 'correction':
            root = roots[event['target_id']]
            result[root]['evaluation'] = copy.deepcopy(event['evaluation'])
            result[root]['evaluation_ref'] = event['id']
            roots[event['id']] = root
    return list(result.values())


def eligible(event, concept):
    q = event['question']
    return (event['evaluation']['outcome'] == 'correct'
            and event['assistance'] == 'none'
            and q['scope'] == SCOPES[concept]
            and q.get('scope_version', 1) == 1
            and (q['capability'] not in {'application', 'problem_solving'} or q.get('novel', False)))


def has_pair(events, concept):
    explanations = [e for e in events if eligible(e, concept) and e['question']['capability'] in {'explanation', 'derivation'}]
    applications = [e for e in events if eligible(e, concept) and e['question']['capability'] in {'application', 'problem_solving'}]
    return any(a['question']['id'] != b['question']['id'] for a in explanations for b in applications)


def project(concept, events):
    relevant = [e for e in events if concept in e['concept_ids']]
    assessments = [e for e in effective_assessments(events) if concept in e['concept_ids'] and e['evaluation']['outcome'] != 'skip']
    reports = [e for e in relevant if e['kind'] == 'self_report' and e['report_type'] != 'skip']
    history = any(e['report_type'] in {'studied_before', 'forgotten'} for e in reports)
    state, confidence = 'unknown', 'none'
    rationale = 'No performance evidence or relevant learning-history report.'
    conflicts = []
    pair_at = None
    for index in range(len(assessments)):
        # A complete unaided pair after the last gap establishes current readiness.
        prefix = assessments[:index + 1]
        last_gap = max((i for i, e in enumerate(prefix) if e['evaluation']['outcome'] in {'partial', 'incorrect'}), default=-1)
        if has_pair(prefix[last_gap + 1:], concept):
            pair_at = index
    if pair_at is not None:
        gaps = [e for e in assessments[pair_at + 1:] if e['evaluation']['outcome'] in {'partial', 'incorrect'}]
        state, confidence = 'active', 'moderate'
        rationale = 'Unaided scoped explanation/derivation and novel application are recorded.'
        successful = [e for e in assessments if eligible(e, concept)]
        independent = {e['question']['id'] for e in successful}
        if len(independent) >= 4 or (len(independent) >= 3 and len({e['session_id'] for e in successful}) >= 2):
            confidence = 'high'
        if gaps:
            conflicts = [e['evaluation_ref'] for e in gaps]
            confidence = 'low'
            rationale = 'Earlier unaided competence conflicts with later performance; verify before skipping.'
            if len(gaps) >= 2:
                state, confidence = 'rusty', 'moderate'
                rationale = 'Previously demonstrated competence now has repeated gaps; refresh and reassess.'
    elif assessments:
        supported = any(e['evaluation']['outcome'] == 'correct' or e['evaluation']['outcome'] == 'partial' for e in assessments)
        state = 'rusty' if history and supported else 'forgotten' if history else 'developing'
        confidence = 'moderate' if len(assessments) >= 2 else 'low'
        rationale = 'Observed performance is insufficient for an unaided scoped explanation/application pair.'
        if history:
            rationale += ' Prior learning is reported; it is not itself demonstrated competence.'
        elif reports and reports[-1]['report_type'] == 'never_seen' and not supported:
            state, confidence = 'never_learned', 'low'
            rationale += ' Never-learning is a learner report, not inferred from failure.'
    elif reports:
        last = reports[-1]['report_type']
        state = 'never_learned' if last == 'never_seen' else 'forgotten' if last == 'forgotten' else 'exposed'
        confidence = 'low'
        rationale = 'Learning-history self-report only; competence has not been demonstrated.'
    if state == 'active' and reports and reports[-1]['report_type'] in {'never_seen', 'forgotten'}:
        last_report = reports[-1]
        if last_report['sequence'] > assessments[pair_at]['sequence']:
            conflicts.append(last_report['id'])
            confidence = 'low'
            rationale = 'Performance and later self-report conflict; inspect before skipping.'
    capabilities = {}
    for e in assessments:
        outcome = e['evaluation']['outcome']
        result = 'aided' if outcome == 'correct' and e['assistance'] != 'none' else {
            'correct': 'demonstrated', 'partial': 'partial', 'incorrect': 'not_demonstrated'}[outcome]
        capabilities[e['question']['capability']] = {'status': result, 'evidence_refs': [e['id'], e['evaluation_ref']] if e['id'] != e['evaluation_ref'] else [e['id']]}
    successes = [e for e in assessments if eligible(e, concept)]
    return {
        'schema_version': 1, 'concept_id': concept, 'graph_version': None,
        'competency_state': state, 'evidence_confidence': confidence,
        'expected_exposure': 'unknown', 'exposure_prior': None,
        'capabilities': capabilities, 'evidence_refs': [e['id'] for e in relevant],
        'estimate_basis_refs': list(dict.fromkeys([e['id'] for e in reports] + [r for e in assessments for r in (e['id'], e['evaluation_ref'])])),
        'rationale': rationale,
        'misconceptions': [{'description': m, 'evidence_ref': e['evaluation_ref']} for e in assessments for m in e['evaluation'].get('misconceptions', [])],
        'conflict_refs': conflicts,
        'last_interaction_at': relevant[-1]['timestamp'] if relevant else None,
        'last_reviewed_at': assessments[-1]['timestamp'] if assessments else None,
        'last_unaided_success_at': successes[-1]['timestamp'] if successes else None,
    }


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(dir=path.parent, prefix='.pending-')
    try:
        with os.fdopen(fd, 'w') as stream:
            json.dump(value, stream, indent=2, ensure_ascii=False)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


class Store:
    def __init__(self, path, allow_synthetic=False):
        self.path = Path(path).resolve()
        self.allow_synthetic = allow_synthetic
        require(not allow_synthetic or self.path != (REPO / '.learn').resolve(), 'Synthetic state cannot use the personal .learn directory')

    def events(self):
        result = []
        for path in sorted((self.path / 'evidence').glob('*.json')):
            try:
                event = json.loads(path.read_text())
            except (OSError, ValueError) as error:
                raise StateError(f'Cannot read evidence {path.name}: {error}') from error
            require(path.stem == event.get('id'), 'Evidence filename/ID mismatch')
            result.append(event)
        result.sort(key=lambda e: e.get('sequence', 0))
        existing = {}
        for sequence, event in enumerate(result, 1):
            require(event.get('sequence') == sequence, 'Invalid or duplicate recording sequence')
            validate_event(event, existing, self.allow_synthetic)
            existing[event['id']] = event
        return result

    def projections(self):
        events = self.events()
        projections = {concept: project(concept, events) for concept in IDS}
        graph_path = REPO / 'competencies/graph-theory/graph.json'
        if graph_path.exists():
            try:
                from .competency import Graph
            except ImportError:
                from competency import Graph
            graph = Graph.load()
            for concept, value in projections.items():
                value['graph_version'] = graph.version
                value['graph_ref'] = 'competencies/graph-theory/graph.json#' + concept
        mapping_path = REPO / 'competencies/graph-theory/background-mappings.json'
        if mapping_path.exists():
            try:
                from .bootstrap import exposure
            except ImportError:
                from bootstrap import exposure
            for concept, value in projections.items():
                value['expected_exposure'], value['exposure_prior'] = exposure(concept, events)
                prior = value['exposure_prior']
                if prior:
                    value['evidence_refs'] = list(dict.fromkeys(prior['declaration_refs'] + value['evidence_refs']))
        return projections

    def sync(self):
        projections = self.projections()
        for concept, projection in projections.items():
            atomic_json(self.path / 'concepts' / f'{concept}.json', projection)
        events = self.events()
        learner_path = self.path / 'learner.json'
        learner = json.loads(learner_path.read_text()) if learner_path.exists() else {}
        require(learner.get('schema_version', 1) == 1, 'Unsupported learner version')
        require(isinstance(learner.get('preferences', {}), dict), 'Invalid preferences')
        atomic_json(learner_path, {
            'schema_version': 1, 'preferences': learner.get('preferences', {}),
            'declaration_refs': [e['id'] for e in events if e['kind'] == 'background_declaration']})
        if (self.path / 'plan.json').exists():
            self.plan()
        return projections

    def record(self, event):
        events = self.events()
        existing = {e['id']: e for e in events}
        value = copy.deepcopy(event)
        value.setdefault('schema_version', 1)
        value.setdefault('id', str(uuid.uuid4()))
        value.setdefault('timestamp', existing.get(value['id'], {}).get('timestamp', now()))
        validate_event(value, existing, self.allow_synthetic)
        if value['id'] in existing:
            candidate = copy.deepcopy(existing[value['id']])
            candidate.pop('sequence')
            value.pop('sequence', None)
            require(candidate == value, 'Conflicting evidence ID; append a correction instead')
            self.sync()
            return existing[value['id']]
        value.pop('sequence', None)
        value['sequence'] = len(events) + 1
        path = self.path / 'evidence' / f"{value['id']}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive creation is the history-preservation boundary. One writer per checkout.
        try:
            with path.open('x') as stream:
                json.dump(value, stream, indent=2, ensure_ascii=False)
                stream.write('\n')
                stream.flush()
                os.fsync(stream.fileno())
        except FileExistsError as error:
            raise StateError('Concurrent or conflicting evidence write') from error
        self.sync()
        return value

    def validate(self):
        projections = self.projections()
        for concept, expected in projections.items():
            path = self.path / 'concepts' / f'{concept}.json'
            require(path.exists() or not self.events(), f'Missing projection: {concept}; rebuild explicitly')
            if path.exists():
                try:
                    require(json.loads(path.read_text()) == expected, f'Stale or edited projection: {concept}; rebuild explicitly')
                except ValueError as error:
                    raise StateError(f'Invalid projection {concept}: {error}') from error
        self.sessions()
        plan_path = self.path / 'plan.json'
        if plan_path.exists():
            saved = json.loads(plan_path.read_text())
            require(saved.get('schema_version') == 1, 'Unsupported plan version')
            try:
                from .planning import build
            except ImportError:
                from planning import build
            require(saved == build(saved.get('target'), projections, len(self.events())),
                    'Stale or edited plan; rebuild explicitly')
        return {'valid': True, 'evidence_count': len(self.events()), 'concept_count': len(projections)}

    def check_session(self, value, events):
        require(isinstance(value, dict), 'Session must be an object')
        require(value.get('schema_version') == 1, 'Unsupported session version')
        identifier(value.get('id'))
        require(value.get('mode') in {'teaching', 'calibration'}, 'Invalid session mode')
        nonempty(value.get('goal'), 'session goal')
        refs = value.get('evidence_refs', [])
        require(isinstance(refs, list) and all(r in events and events[r]['session_id'] == value['id'] for r in refs), 'Invalid session evidence references')
        pending = value.get('pending_question')
        require(pending is None or isinstance(pending, dict), 'Invalid pending question')
        if pending:
            identifier(pending.get('id'))
            require(pending.get('concept_id') in IDS, 'Pending question needs a stable concept ID')
            nonempty(pending.get('text'), 'pending question text')
        if value.get('mode') == 'calibration':
            require(type(value.get('budget')) is int and 1 <= value['budget'] <= 8,
                    'Invalid calibration response budget')
        sequence = value.get('pending_sequence', value.get('recording_sequence', len(events)))
        require(type(sequence) is int and 0 <= sequence <= len(events), 'Invalid checkpoint sequence')

    def sessions(self):
        events = {e['id']: e for e in self.events()}
        sessions = []
        for path in (self.path / 'sessions').glob('*.json'):
            value = json.loads(path.read_text())
            self.check_session(value, events)
            require(value['id'] == path.stem, 'Session filename/ID mismatch')
            nonempty(value.get('updated_at'), 'checkpoint update time')
            sessions.append(value)
        return sessions

    def session(self, value):
        events = {e['id']: e for e in self.events()}
        self.check_session(value, events)
        value = copy.deepcopy(value)
        value['updated_at'] = now()
        value['recording_sequence'] = len(events)
        atomic_json(self.path / 'sessions' / f"{value['id']}.json", value)
        return value

    def plan(self, target=None):
        path = self.path / 'plan.json'
        if target is None:
            if not path.exists():
                return None
            saved = json.loads(path.read_text())
            require(saved.get('schema_version') == 1, 'Unsupported plan version')
            target = saved.get('target')
        try:
            from .planning import build
        except ImportError:
            from planning import build
        value = build(target, self.projections(), len(self.events()))
        atomic_json(path, value)
        return value

    def resume(self):
        events = self.events()
        sessions = self.sessions()
        latest = max(sessions, key=lambda s: s['updated_at'], default=None)
        if latest:
            require(latest.get('schema_version') == 1, 'Unsupported session version')
            identifier(latest.get('id'))
            own = [e for e in events if e['session_id'] == latest['id']]
            latest['evidence_refs'] = [e['id'] for e in own]
            pending = latest.get('pending_question')
            answers = [e['id'] for e in own if pending and e['sequence'] > latest.get('pending_sequence', latest.get('recording_sequence', 0))
                       and (e['kind'] == 'assessment' and e['question']['id'] == pending['id']
                            or e['kind'] == 'self_report' and e['concept_ids'] == [pending['concept_id']])]
            latest['pending_answer_refs'] = answers
            if answers:
                latest['next_action'] = ('Run next for this calibration session; the pending response is already saved'
                                         if latest['mode'] == 'calibration' else
                                         'Use the saved response and current plan; do not ask the answered question again')
        return {'evidence_count': len(events), 'latest_session': latest,
                'concepts': self.projections(), 'plan': self.plan(), 'continuity': 'same-local-checkout'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state-dir', type=Path, default=REPO / '.learn')
    parser.add_argument('--synthetic', action='store_true', help='Permit explicitly synthetic validation evidence in isolated state')
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('record', 'session'):
        sub.add_parser(name).add_argument('file', type=Path)
    for name in ('inspect', 'validate', 'rebuild', 'resume'):
        sub.add_parser(name)
    sub.add_parser('calibrate').add_argument('--session-id')
    sub.add_parser('plan').add_argument('target')
    for name in ('next', 'stop'):
        sub.add_parser(name).add_argument('session_id')
    args = parser.parse_args()
    try:
        store = Store(args.state_dir, args.synthetic)
        if args.command in {'calibrate', 'next', 'stop'}:
            try:
                from .calibration import advance, start
            except ImportError:
                from calibration import advance, start
            result = start(store, args.session_id) if args.command == 'calibrate' else advance(store, args.session_id, stop=args.command == 'stop')
        elif args.command in {'record', 'session'}:
            result = getattr(store, args.command)(json.loads(args.file.read_text()))
        elif args.command == 'inspect':
            result = store.projections()
        elif args.command == 'rebuild':
            result = store.sync()
        elif args.command == 'plan':
            result = store.plan(args.target)
        else:
            result = getattr(store, args.command)()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except (StateError, OSError, ValueError, TypeError, KeyError) as error:
        parser.exit(2, f'learn-state: {error}\n')


if __name__ == '__main__':
    main()
