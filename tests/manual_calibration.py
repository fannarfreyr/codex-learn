"""Scripted synthetic survey acceptance; fresh processes are not fresh Codex chats."""

import argparse
import json
from pathlib import Path
import subprocess
import sys


REPO = Path(__file__).resolve().parents[1]
PROVENANCE = {'source': 'synthetic', 'surface': 'v0.1.2-scripted-validation'}
REPLIES = {
    'terminology.explanation': 'Vertices are objects; edges join pairs. Adjacent vertices share an edge. Degree counts incident edges, equal to the number of neighbors in a simple undirected graph.',
    'terminology.application': 'A has neighbors B and C. C has degree two, from edges AC and CD.',
    'connectivity.explanation': 'Connected means every vertex has a direct edge to every other vertex.',
    'connectivity.application': 'P reaches only Q; P, Q, and R cannot be one component because PR is missing.',
    'trees.explanation': 'A tree is a connected acyclic undirected graph. A cycle violates acyclicity; two separate paths are acyclic but disconnected, so both conditions matter.',
    'trees.application': 'The first graph is the path A-B-C-D, connected and acyclic, hence a tree. The second contains the cycle A-B-C-A and an isolated D, so it is not a tree.',
    'bfs.explanation': 'BFS starts at the source and explores distance layers with a FIFO queue. Mark a vertex visited when enqueuing it so multiple incoming discoveries do not queue it repeatedly.',
    'bfs.application': 'Layers from A are {A}, {B,C}, {D}, {E}. E first appears at distance three through D; D is queued once despite having two previous-layer neighbors.',
    'dfs.explanation': 'DFS follows one unvisited neighbor down a branch until no unvisited neighbor remains, then backtracks to continue another branch. A visited set prevents cycles from causing repeated exploration.',
    'dfs.application': 'With alphabetical neighbors, discover A, then B, then D, then C. C has no unvisited neighbors, so return through D and B to A; all remaining neighbors are already visited.',
    'bfs-shortest-paths.explanation': 'FIFO completes each distance layer before the next, so a vertex first discovered from distance k has minimum edge distance k+1. Arbitrary weights break the guarantee because fewer edges can have greater total weight.',
    'bfs-shortest-paths.application': 'Layers are {A}, {B,C}, {D,E}. A-B-D uses two edges; A-C-E-D uses three and is longer. First discovery of D through B supplies a shortest path.',
    'spanning-trees.explanation': 'A spanning tree is a connected acyclic subgraph using every original vertex and only original edges. Including every vertex makes it spanning, and connectivity without cycles makes it a tree.',
    'spanning-trees.application': 'Choose AB, BC, and CD. These reach all four vertices without a cycle. Omit CA to remove the triangle cycle while keeping all vertices connected.',
}


def run(path):
    path = path.resolve()
    if path.exists():
        raise ValueError('Use a nonexistent isolated directory; preserve previous validation records')
    if path == (REPO / '.learn').resolve():
        raise ValueError('Synthetic validation cannot use personal state')
    path.mkdir(parents=True)
    transcript = []

    def command(*args):
        result = subprocess.run([sys.executable, str(REPO / 'scripts/learn_state.py'),
                                 '--state-dir', str(path), '--synthetic', *args],
                                cwd=REPO, capture_output=True, text=True, check=True)
        value = json.loads(result.stdout)
        transcript.append({'command': list(args), 'result': value})
        return value

    step = command('calibrate', '--session-id', 'mixed-survey', '--budget', '8')
    asked = []
    while step['question']:
        question = step['question']
        asked.append(question['id'])
        short_id = question['id'].removeprefix('graph-theory.')
        gap = question['concept_id'] == 'graph-theory.connectivity'
        observation = {'id': 'synthetic-answer-' + str(len(asked)), 'kind': 'assessment',
                       'session_id': 'mixed-survey', 'concept_ids': [question['concept_id']],
                       'provenance': PROVENANCE,
                       'question': {k: v for k, v in question.items() if k not in {'concept_id', 'level', 'rubric'}},
                       'response': REPLIES[short_id], 'assistance': 'none', 'rubric': question['rubric'],
                       'evaluation': {'outcome': 'incorrect' if gap else 'correct',
                                      'rationale': ('Confuses direct adjacency with path reachability.' if gap
                                                    else 'Synthetic response meets the saved scoped rubric.'),
                                      'misconceptions': ['Connectivity requires direct adjacency'] if gap else []}}
        input_path = path / (observation['id'] + '-input.json')
        input_path.write_text(json.dumps(observation, indent=2) + '\n')
        command('record', str(input_path))
        step = command('next', 'mixed-survey')
        if step['session']['status'] == 'paused':
            # No prior transcript or Python Store is supplied to the new process.
            resumed = command('resume')
            assert resumed['latest_session']['id'] == 'mixed-survey'
            assert resumed['latest_session']['response_count'] == 8
            step = command('next', 'mixed-survey', '--budget', '8')
    final = command('inspect')
    assert step['session']['status'] == 'completed'
    assert step['coverage']['breadth_complete']
    assert len(asked) == len(set(asked)) == 14
    for concept in ('bfs', 'dfs', 'bfs-shortest-paths'):
        assert final['graph-theory.' + concept]['competency_state'] == 'active'
    assert final['graph-theory.connectivity']['competency_state'] != 'active'
    plan = command('plan', 'graph-theory.bfs-shortest-paths')
    actions = {item['concept_id']: item['action'] for item in plan['steps']}
    assert actions['graph-theory.bfs'] == 'skip'
    assert actions['graph-theory.connectivity'] != 'skip'
    command('validate')
    (path / 'transcript.json').write_text(json.dumps(transcript, indent=2) + '\n')
    return {'synthetic_state_dir': str(path), 'questions': asked,
            'response_count': step['session']['response_count'], 'coverage': step['coverage'],
            'states': {c: p['competency_state'] for c, p in final.items()},
            'fresh_process_recovery': 'passed',
            'fresh_codex_chat_validation': 'not performed by this script'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state-dir', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.state_dir), indent=2))
