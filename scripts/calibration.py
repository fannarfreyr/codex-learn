"""Deterministic survey/focused diagnostics; the tutor evaluates actual answers."""

import copy
import json
import uuid

try:
    from .competency import Graph, questions
    from .learn_state import IDS, SCOPES, effective_assessments, identifier, require
except ImportError:
    from competency import Graph, questions
    from learn_state import IDS, SCOPES, effective_assessments, identifier, require


PRIMARY_CAPABILITIES = {'explanation', 'derivation', 'application', 'problem_solving'}


def ready(projection):
    return (projection['competency_state'] == 'active'
            and projection['evidence_confidence'] in {'moderate', 'high'}
            and not projection['conflict_refs'])


def response_budget(value):
    require(type(value) is int and 1 <= value <= 14,
            'Calibration budget must be 1–14 response turns')


def normalized_session(value):
    """Adapt legacy checkpoints in memory; only an explicit update persists v2."""
    session = copy.deepcopy(value)
    if session['schema_version'] == 1:
        session.update(schema_version=2, strategy='survey', target=None,
                       status='stopped' if session.get('stop_reason') else 'active',
                       pause_reason=None, response_limit=session['budget'])
        session.setdefault('area_id', 'graph-theory')
        session.setdefault('consumed_question_ids', [])
        session.setdefault('response_count', 0)
    return session


def scope(session, graph):
    return list(IDS) if session['strategy'] == 'survey' else graph.ordered(session['target'])


def pending_answers(session, events):
    pending = session.get('pending_question')
    sequence = session.get('pending_sequence', session.get('recording_sequence', 0))
    return [e for e in events if pending and e['session_id'] == session['id']
            and e['sequence'] > sequence
            and (e['kind'] == 'assessment' and e['question']['id'] == pending['id']
                 or e['kind'] == 'self_report' and e['concept_ids'] == [pending['concept_id']])]


def used_questions(session, events):
    used = {e['question']['id'] for e in events if e['kind'] == 'assessment'}
    used.update(session.get('consumed_question_ids', []))
    if pending_answers(session, events):
        used.add(session['pending_question']['id'])
    return used


def coverage(session, events, profiles, graph=None, bank=None):
    """Coverage is an evidence-derived report, never a mastery projection."""
    session = normalized_session(session)
    graph = graph or Graph.load()
    bank = questions(graph) if bank is None else bank
    assessments = effective_assessments(events)
    used = used_questions(session, events)
    concepts = {}
    for concept in scope(session, graph):
        direct = [e for e in assessments if e['concept_ids'] == [concept]
                  and e['evaluation']['outcome'] != 'skip']
        representative = [e for e in direct if e['question']['scope'] == SCOPES[concept]
                          and e['question'].get('scope_version', 1) == 1
                          and e['question']['capability'] in PRIMARY_CAPABILITIES]
        tested_capabilities = {('explanation' if e['question']['capability'] in {'explanation', 'derivation'}
                                else 'application') for e in representative}
        skipped = [e['id'] for e in events if e['session_id'] == session['id']
                   and e['concept_ids'] == [concept]
                   and (e['kind'] == 'assessment' and e['evaluation']['outcome'] == 'skip'
                        or e['kind'] == 'self_report' and e['report_type'] == 'skip')]
        remaining = [q['id'] for q in bank if q['concept_id'] == concept and q['id'] not in used]
        profile = profiles[concept]
        uncertainty = []
        if not representative:
            uncertainty.append('No current-scope representative assessment; self-report is not coverage.')
        if not ready(profile):
            uncertainty.append('Current unaided scoped explanation/application readiness is not established.')
        if profile['conflict_refs']:
            uncertainty.append('Conflicting evidence needs verification.')
        if not remaining and not ready(profile):
            uncertainty.append('No unused bank prompt remains; further assessment needs a separate fresh task.')
        concepts[concept] = {
            'sampled': bool(representative),
            'assessment_refs': [e['id'] for e in direct],
            'representative_refs': [e['id'] for e in representative],
            'evaluation_refs': [e['evaluation_ref'] for e in direct],
            'tested_now_refs': [e['id'] for e in direct if e['session_id'] == session['id']],
            'tested_previously_refs': [e['id'] for e in direct if e['session_id'] != session['id']],
            'skipped_refs': skipped, 'deferred': bool(skipped and not representative),
            'untested_capabilities': [c for c in ('explanation', 'application') if c not in tested_capabilities],
            'capabilities': profile['capabilities'], 'ready': ready(profile),
            'remaining_question_ids': remaining, 'uncertainty': uncertainty,
        }
    return {'strategy': session['strategy'], 'target': session.get('target'),
            'breadth_complete': all(c['sampled'] for c in concepts.values()),
            'concepts': concepts,
            'selection_rationale': session.get('selection_rationale'),
            'status': session['status'],
            'reason': session.get('pause_reason') or session.get('stop_reason')}


def start(store, session_id=None, budget=8, strategy='survey', target=None):
    response_budget(budget)
    require(strategy in {'survey', 'focused'}, 'Invalid calibration strategy')
    require(target in IDS if strategy == 'focused' else target is None,
            'Focused calibration requires a supported target; survey takes no target')
    value = {'schema_version': 2, 'id': session_id or str(uuid.uuid4()), 'mode': 'calibration',
             'goal': 'Calibrate graph-theory knowledge' if target is None else 'Check readiness for ' + target,
             'area_id': 'graph-theory', 'strategy': strategy, 'target': target,
             'status': 'active', 'pause_reason': None, 'stop_reason': None,
             'budget': budget, 'response_limit': budget, 'response_count': 0,
             'evidence_refs': [], 'consumed_question_ids': [], 'pending_question': None,
             'next_action': 'Choose an informative question'}
    identifier(value['id'])
    path = store.path / 'sessions' / (value['id'] + '.json')
    require(not path.exists(), 'Session ID already exists; resume it instead')
    store.session(value)
    return advance(store, value['id'])


def survey_question(session, events, profiles, graph, bank, report):
    available = [q for q in bank if q['id'] not in used_questions(session, events)]

    def pick(concept):
        reports = [e for e in events if e['kind'] == 'self_report' and e['concept_ids'] == [concept]
                   and e['report_type'] != 'skip']
        preferred = 'application' if reports and reports[-1]['report_type'] == 'knows_without_name' else 'explanation'
        missing = report['concepts'][concept]['untested_capabilities']
        if len(missing) == 1:
            preferred = missing[0]
        options = [q for q in available if q['concept_id'] == concept]
        return next((q for q in options if q['capability'] == preferred), options[0] if options else None)

    uncovered = [c for c in IDS if not report['concepts'][c]['sampled']]
    # Declined concepts stay uncertain but do not monopolize the breadth pass.
    for deferred in (False, True):
        candidates = [c for c in uncovered if report['concepts'][c]['deferred'] == deferred]
        core = 'graph-theory.connectivity'
        if not session['response_count'] and profiles[core]['expected_exposure'] in {'medium', 'high'}:
            candidates = sorted(candidates, key=lambda c: c != core)
        for concept in candidates:
            selected = pick(concept)
            if selected:
                return selected, 'Survey breadth: sample an uncovered concept independently of prerequisite readiness.'

    ranked = []
    for concept in IDS:
        profile = profiles[concept]
        if ready(profile):
            continue
        selected = pick(concept)
        if not selected:
            continue
        capabilities = profile['capabilities']
        explanation = next((capabilities[c]['status'] for c in ('explanation', 'derivation', 'definition') if c in capabilities), None)
        application = next((capabilities[c]['status'] for c in ('application', 'problem_solving') if c in capabilities), None)
        gap = {'partial', 'aided', 'not_demonstrated'}
        if profile['conflict_refs']:
            priority, reason = 0, 'Verify conflicting direct evidence.'
        elif (explanation in gap and application is None
              or application in gap and explanation is None
              or explanation and application and explanation != application):
            priority, reason = 1, 'Distinguish explanation/terminology retrieval from application.'
            if application is None:
                desired = 'application'
            elif explanation is None:
                desired = 'explanation'
            else:
                desired = 'explanation' if explanation in gap else 'application'
            selected = next((q for q in available if q['concept_id'] == concept and q['capability'] == desired), selected)
        elif 'demonstrated' in (explanation, application):
            priority, reason = 2, 'Check the missing independent capability before establishing a strength.'
        else:
            priority, reason = 3, 'Characterize an unresolved gap with remaining direct assessment.'
        ranked.append((priority, IDS.index(concept), selected, reason))
    if ranked:
        _, _, selected, reason = min(ranked, key=lambda item: item[:2])
        return selected, 'Survey follow-up: ' + reason
    return None, 'no_remaining_informative_prompt; untested capabilities remain uncertain'


def focused_question(session, events, profiles, graph, bank):
    relevant = scope(session, graph)
    available = [q for q in bank if q['concept_id'] in relevant
                 and q['id'] not in used_questions(session, events)]

    def pick(concept):
        return next((q for q in available if q['concept_id'] == concept), None)

    responses = [e for e in events if e['session_id'] == session['id']
                 and e['kind'] in {'assessment', 'self_report'} and e['concept_ids'][0] in relevant]
    last = responses[-1] if responses else None
    if last:
        same_turn = [e for e in responses if e.get('turn_id', e['id']) == last.get('turn_id', last['id'])]
        last = next((e for e in reversed(same_turn) if e['kind'] == 'assessment'), last)
        last = next((e for e in effective_assessments(events) if e['id'] == last['id']), last)
        concept = last['concept_ids'][0]
        skipped = (last['kind'] == 'assessment' and last['evaluation']['outcome'] == 'skip'
                   or last['kind'] == 'self_report' and last['report_type'] == 'skip')
        gap = not skipped and (last['kind'] == 'assessment' and (
            last['evaluation']['outcome'] in {'partial', 'incorrect'} or last['assistance'] != 'none')
            or last['kind'] == 'self_report' and last['report_type'] in {'never_seen', 'forgotten', 'not_deeply_understood'})
        if gap:
            for parent in reversed(graph.ordered(concept)[:-1]):
                selected = None if ready(profiles[parent]) else pick(parent)
                if selected:
                    return selected, 'Focused gap: inspect a necessary prerequisite.'
            turns = {e.get('turn_id', e['id']) for e in responses if e['concept_ids'] == [concept]}
            if len(turns) >= 2 and not ready(profiles[concept]):
                return None, 'useful_boundary_found; unresolved concept needs teaching or refresh'
        if not skipped and not ready(profiles[concept]) and pick(concept):
            return pick(concept), 'Focused confirmation: check another capability within the target path.'
    for concept in reversed(relevant):
        if not ready(profiles[concept]) and pick(concept):
            return pick(concept), 'Focused readiness: probe the deepest unresolved concept in the target path.'
    return None, 'no_remaining_informative_prompt; target readiness remains provisional'


def advance(store, session_id, stop=False, pause=False, budget=None):
    identifier(session_id)
    require(not (stop and pause), 'Cannot pause and stop together')
    if budget is not None:
        response_budget(budget)
        require(not stop and not pause, 'A continuation budget cannot accompany pause or stop')
    path = store.path / 'sessions' / (session_id + '.json')
    require(path.is_file(), 'Missing calibration session')
    original = json.loads(path.read_text())
    events = store.events()
    store.check_session(original, {e['id']: e for e in events})
    require(original['mode'] == 'calibration', 'Not a calibration session')
    session = normalized_session(original)
    graph, bank = Graph.load(), questions()
    profiles = store.projections()

    def result(question, reason, save=True):
        if save:
            session.update(store.session(session))
        return {'session': session, 'question': question, 'reason': reason,
                'concepts': profiles, 'coverage': coverage(session, events, profiles, graph, bank)}

    if session['status'] in {'stopped', 'completed'}:
        return result(None, session['stop_reason'], save=False)
    own = [e for e in events if e['session_id'] == session_id]
    responses = [e for e in own if e['kind'] in {'assessment', 'self_report'}]
    session['evidence_refs'] = [e['id'] for e in own]
    session['response_count'] = len({e.get('turn_id', e['id']) for e in responses})
    answered = pending_answers(session, events)
    if answered:
        consumed = set(session.get('consumed_question_ids', []))
        consumed.add(session['pending_question']['id'])
        session['consumed_question_ids'] = sorted(consumed)
        session['pending_question'] = None
    if stop:
        session.update(status='stopped', stop_reason='learner_requested_stop', pause_reason=None,
                       pending_question=None, next_action='Summarize tested scope and uncertainty')
        return result(None, session['stop_reason'])
    if pause:
        session.update(status='paused', pause_reason='learner_requested_pause',
                       next_action='Continue calibration with an additional bounded block')
        return result(None, session['pause_reason'])
    if session['status'] == 'paused':
        if budget is None:
            return result(None, session['pause_reason'])
        session.update(status='active', pause_reason=None, budget=budget,
                       response_limit=session['response_count'] + budget)
    if session['pending_question']:
        session['next_action'] = 'Wait for actual learner response'
        return result(session['pending_question'], 'Await the actual learner response; do not advance.')
    relevant = scope(session, graph)
    if all(ready(profiles[c]) for c in relevant):
        session.update(status='completed', stop_reason='scoped_readiness_supported',
                       next_action='Summarize direct evidence and its scope')
        return result(None, session['stop_reason'])
    report = coverage(session, events, profiles, graph, bank)
    if session['strategy'] == 'survey':
        selected, reason = survey_question(session, events, profiles, graph, bank, report)
    else:
        selected, reason = focused_question(session, events, profiles, graph, bank)
    if selected is None:
        session.update(status='completed', stop_reason=reason,
                       next_action='Summarize tested scope, remaining uncertainty, and related teaching options')
        return result(None, reason)
    if session['response_count'] >= session['response_limit']:
        session.update(status='paused', pause_reason='response_budget_reached; conclusions remain provisional',
                       next_action='Summarize partial coverage; continue with an additional bounded block')
        return result(None, session['pause_reason'])
    session.update(pending_question=selected, pending_sequence=len(events), selection_rationale=reason,
                   next_action='Wait for actual learner response')
    return result(selected, reason)
