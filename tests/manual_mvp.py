"""Prepare an inspectable synthetic trajectory; this does not simulate a Codex chat."""

import argparse
import copy
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.calibration import advance, start
from scripts.competency import questions
from scripts.learn_state import Store, require


TARGET = 'graph-theory.bfs-shortest-paths'
BFS = 'graph-theory.bfs'
PROVENANCE = {'source': 'synthetic', 'surface': 'scripted-manual-validation'}


def observe(store, question, response, rationale, session, outcome='correct', assistance='none'):
    value = {'id': 'observation-' + str(len(store.events()) + 1), 'kind': 'assessment',
             'session_id': session, 'concept_ids': [question['concept_id']],
             'provenance': PROVENANCE,
             'question': {k: v for k, v in question.items() if k not in {'concept_id', 'level', 'rubric'}},
             'response': response, 'assistance': assistance, 'rubric': question['rubric'],
             'evaluation': {'outcome': outcome, 'rationale': rationale, 'misconceptions': []}}
    return store.record(value)


def run(path):
    store = Store(path, allow_synthetic=True)
    require(not store.events(), 'Use a fresh isolated directory; existing evidence will not be replaced')
    store.record({'id': 'degree', 'kind': 'background_declaration', 'session_id': 'onboarding',
                  'concept_ids': [], 'provenance': PROVENANCE,
                  'statement': 'BSc in Discrete Mathematics and Computer Science'})
    initial = store.projections()
    require(all(p['competency_state'] == 'unknown' for p in initial.values()), 'Credential created competence')
    step = start(store, 'diagnostic', strategy='focused', target='graph-theory.connectivity')
    trajectory = []
    replies = {
        'graph-theory.connectivity.explanation': (
            'A path is a sequence of vertices with an edge between successive vertices. Two vertices are connected if a path joins them. Components are maximal groups mutually reachable by paths; direct adjacency is unnecessary.',
            'Defines paths, reachability, and components and distinguishes adjacency.'),
        'graph-theory.connectivity.application': (
            'P, Q, and R form one component because PQ and QR connect them by paths. S and T form the other component. P cannot reach T because there is no edge or path linking the groups.',
            'Correctly identifies both components and justifies the lack of reachability.'),
        'graph-theory.terminology.explanation': (
            'Vertices are the objects and edges join pairs of vertices. Adjacent vertices share an edge. Degree counts incident edges, or neighbors in a simple undirected graph.',
            'Correct definitions within the finite simple undirected scope.'),
        'graph-theory.terminology.application': (
            'A has neighbors B and C. C has degree 2 because AC and CD are its two incident edges.',
            'Correctly applies adjacency and degree to a fresh graph.'),
    }
    for _ in range(4):
        q = step['question']
        require(q['id'] in replies, 'Unexpected diagnostic branch; inspect before continuing')
        trajectory.append(q['id'])
        response, rationale = replies[q['id']]
        observe(store, q, response, rationale, 'diagnostic')
        step = advance(store, 'diagnostic')
    advance(store, 'diagnostic', stop=True)
    store.plan(TARGET)
    store.record({'id': 'bfs-history', 'kind': 'self_report', 'session_id': 'lesson',
                  'concept_ids': [BFS], 'provenance': PROVENANCE, 'report_type': 'studied_before',
                  'statement': 'I studied BFS before. I recognize it but cannot explain the queue unaided.'})
    bank = {q['id']: q for q in questions()}
    observe(store, bank[BFS + '.explanation'],
            'It visits nearby vertices before far ones, but I cannot explain which waiting vertex it chooses next.',
            'Recognizes layers but omits the FIFO frontier mechanism.', 'lesson', outcome='partial')
    observe(store, bank[BFS + '.application'],
            'After the distance-layer hint: A, then B and C, then D, then E.',
            'Correct distance layers after an explicit hint; not unaided evidence.', 'lesson', assistance='hint')
    before = store.plan(TARGET)
    explanation = copy.deepcopy(bank[BFS + '.explanation'])
    explanation.update(id='bfs-refresh-explanation', text='Explain how a FIFO frontier gives BFS its distance-layer order, including discovery of a neighbor.')
    observe(store, explanation,
            'Start with the source in a FIFO queue and mark it discovered. Remove the front vertex, add each undiscovered neighbor at the back, and mark each when adding it. Vertices discovered at one distance wait before the next layer, so exploration proceeds by increasing edge distance.',
            'Explains discovery, FIFO frontier, and distance-layer order without assistance.', 'lesson')
    transfer = copy.deepcopy(bank[BFS + '.application'])
    transfer.update(id='bfs-refresh-transfer', text='Vertices 1–6 have edges 12, 13, 24, 35, 46, 56. Give BFS distance layers from 1 and explain when 6 is discovered.',
                    rubric={'criteria': ['Layers are {1}, {2,3}, {4,5}, {6}.',
                                         '6 is discovered through 4 or 5 and queued once; FIFO completes earlier layers first.']})
    observe(store, transfer,
            'The layers are {1}, {2,3}, {4,5}, {6}. Processing 4 or 5 first discovers 6 at distance 3; marking it at discovery prevents adding it twice. FIFO processes the earlier layers before that layer.',
            'Correctly traces a new graph and explains unique discovery and FIFO ordering.', 'lesson')
    after = store.plan(TARGET)
    pending = bank[TARGET + '.explanation']
    store.session({'schema_version': 1, 'id': 'lesson', 'mode': 'teaching', 'goal': TARGET,
                   'evidence_refs': [e['id'] for e in store.events() if e['session_id'] == 'lesson'],
                   'pending_question': pending, 'next_action': 'Wait for the learner to answer the BFS shortest-path explanation'})
    return {'synthetic_state_dir': str(store.path), 'diagnostic_questions': trajectory,
            'before_refresher': [(s['concept_id'], s['action']) for s in before['steps']],
            'after_refresher': [(s['concept_id'], s['action']) for s in after['steps']],
            'pending_question': pending['text'], 'integrity': store.validate(),
            'fresh_codex_chat_check': 'pending; a new Python process is insufficient'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state-dir', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.state_dir), indent=2))
