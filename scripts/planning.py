"""Dependency-aware lesson actions, derived from the shared evidence projections."""

try:
    from .calibration import ready
    from .competency import Graph
except ImportError:
    from calibration import ready
    from competency import Graph


def action(projection):
    state = projection['competency_state']
    if ready(projection):
        return 'skip', 'Scoped unaided explanation and novel application support skipping instruction.'
    if state == 'active':
        return 'verify', 'Earlier competence is uncertain or conflicted; verify before relying on it.'
    if state == 'rusty':
        return 'refresh', 'Use a concise refresher, then check unaided explanation and fresh application.'
    if state == 'forgotten':
        return 'reconstruct', 'Attempt a short reconstruction of prior learning; expand if retrieval fails.'
    if state in {'exposed', 'developing'}:
        return 'bridge', 'Start from recorded capabilities and repair the unresolved gap.'
    return 'teach', 'Introduce this foundation; exposure alone does not establish current readiness.'


def build(target, projections, evidence_sequence):
    graph = Graph.load()
    steps = []
    for concept in graph.ordered(target):
        projection = projections[concept]
        selected, reason = action(projection)
        steps.append({
            'concept_id': concept, 'label': graph.nodes[concept]['label'],
            'scope': graph.nodes[concept]['scope'], 'action': selected,
            'evidence_refs': projection['evidence_refs'],
            'estimate_basis_refs': projection['estimate_basis_refs'],
            'rationale': reason + ' ' + projection['rationale'],
        })
    unresolved = next((s for s in steps if s['action'] != 'skip'), None)
    return {
        'schema_version': 1, 'target': target, 'graph_version': graph.version,
        'evidence_sequence': evidence_sequence, 'steps': steps,
        'current_checkpoint': ({'concept_id': unresolved['concept_id'], 'action': unresolved['action']}
                               if unresolved else None),
        'status': 'in_progress' if unresolved else 'demonstrated_within_scope',
    }
