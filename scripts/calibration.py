"""Small deterministic diagnostic heuristics; the tutor evaluates actual answers."""

import uuid

try:
    from .competency import Graph, questions
    from .learn_state import IDS, effective_assessments, identifier, require
except ImportError:
    from competency import Graph, questions
    from learn_state import IDS, effective_assessments, identifier, require


def ready(projection):
    return (projection['competency_state'] == 'active'
            and projection['evidence_confidence'] in {'moderate', 'high'}
            and not projection['conflict_refs'])


def start(store, session_id=None, budget=8):
    require(type(budget) is int and 1 <= budget <= 8, 'Calibration budget must be 1–8 response turns')
    value = {'schema_version': 1, 'id': session_id or str(uuid.uuid4()), 'mode': 'calibration',
             'goal': 'Calibrate graph-theory knowledge', 'area_id': 'graph-theory',
             'budget': budget, 'evidence_refs': [], 'pending_question': None,
             'next_action': 'Choose an informative question', 'stop_reason': None}
    identifier(value['id'])
    path = store.path / 'sessions' / (value['id'] + '.json')
    require(not path.exists(), 'Session ID already exists; resume it instead')
    store.session(value)
    return advance(store, value['id'])


def advance(store, session_id, stop=False):
    import json
    identifier(session_id)
    path = store.path / 'sessions' / (session_id + '.json')
    require(path.is_file(), 'Missing calibration session')
    session = json.loads(path.read_text())
    require(session.get('mode') == 'calibration', 'Not a calibration session')
    graph, bank = Graph.load(), questions()
    events = store.events()
    profiles = store.projections()
    own = [e for e in events if e['session_id'] == session_id]
    responses = [e for e in own if e['kind'] in {'assessment', 'self_report'}]
    assessments = [e for e in effective_assessments(events) if e['session_id'] == session_id]
    session['evidence_refs'] = [e['id'] for e in own]
    turns = {e.get('turn_id', e['id']) for e in responses}
    session['response_count'] = len(turns)
    pending = session.get('pending_question')
    answered = [e for e in responses if e['sequence'] > session.get('pending_sequence', 0)
                and (e['kind'] == 'assessment' and pending and e['question']['id'] == pending['id']
                     or e['kind'] == 'self_report' and pending and e['concept_ids'] == [pending['concept_id']])]
    if pending and not answered and not stop:
        return {'session': session, 'question': pending, 'reason': 'Await the actual learner response; do not advance.'}
    session['pending_question'] = None

    def finish(reason):
        session['stop_reason'] = reason
        session['next_action'] = 'Summarize tested scope and uncertainty; offer a related lesson'
        store.session(session)
        return {'session': session, 'question': None, 'reason': reason, 'concepts': profiles}

    if stop:
        return finish('learner_requested_stop')
    if session.get('stop_reason'):
        return finish(session['stop_reason'])
    if len(turns) >= session['budget']:
        return finish('response_budget_reached; conclusions remain provisional')
    used = {e['question']['id'] for e in events if e['kind'] == 'assessment'}
    # A self-report answering a pending question also consumes that prompt.
    used.update(session.get('consumed_question_ids', []))
    if pending and answered:
        used.add(pending['id'])
        session['consumed_question_ids'] = sorted(used)
    available = [q for q in bank if q['id'] not in used]

    def pick(concept, capability=None):
        options = [q for q in available if q['concept_id'] == concept and (capability is None or q['capability'] == capability)]
        return options[0] if options else None

    last = responses[-1] if responses else None
    if last:
        same_turn = [e for e in responses if e.get('turn_id', e['id']) == last.get('turn_id', last['id'])]
        last = next((e for e in reversed(same_turn) if e['kind'] == 'assessment'), last)
    selected, reason = None, None
    if last:
        concept = last['concept_ids'][0]
        actual = next((e for e in assessments if e['id'] == last['id']), last)
        gap = (actual['kind'] == 'assessment' and (actual['evaluation']['outcome'] in {'incorrect', 'partial'}
               or actual['assistance'] != 'none')) or (actual['kind'] == 'self_report' and actual['report_type'] in {'never_seen', 'forgotten', 'not_deeply_understood'})
        skipped = actual['kind'] == 'assessment' and actual['evaluation']['outcome'] == 'skip' or actual['kind'] == 'self_report' and actual['report_type'] == 'skip'
        if gap:
            for parent in reversed(graph.ordered(concept)[:-1]):
                if not ready(profiles[parent]):
                    selected = pick(parent)
                    if selected:
                        reason = 'Observed gap: inspect a necessary prerequisite at lower difficulty.'
                        break
            if not selected:
                count = len({e.get('turn_id', e['id']) for e in responses if e['concept_ids'] == [concept]})
                if count >= 2 and not ready(profiles[concept]):
                    return finish('useful_boundary_found; unresolved concept needs teaching or refresh')
                selected = pick(concept)
                reason = 'Characterize the gap with a different capability.'
        elif not skipped and not ready(profiles[concept]):
            selected = pick(concept, 'explanation') or pick(concept, 'application')
            reason = 'Confirm explanation and novel application rather than credit recognition alone.'
        if not selected:
            for candidate in graph.ordered(concept)[:-1] + graph.dependents(concept):
                if not ready(profiles[candidate]):
                    selected = pick(candidate)
                    if selected:
                        reason = 'Move to an unverified prerequisite or a harder dependent concept.'
                        break
    elif not any(ready(p) for p in profiles.values()) and profiles['graph-theory.connectivity']['expected_exposure'] in {'medium', 'high'}:
        selected = pick('graph-theory.connectivity', 'explanation')
        reason = 'Exposure prior starts questioning at core difficulty; it does not skip instruction.'
    if not selected:
        for concept in IDS:
            if not ready(profiles[concept]):
                selected = pick(concept)
                if selected:
                    reason = 'Probe an unresolved strand; no competence is inferred from background.'
                    break
    if not selected:
        return finish('no_remaining_informative_prompt; untested concepts remain uncertain')
    session.update(pending_question=selected, pending_sequence=len(events),
                   selection_rationale=reason, next_action='Wait for actual learner response')
    store.session(session)
    return {'session': session, 'question': selected, 'reason': reason}
