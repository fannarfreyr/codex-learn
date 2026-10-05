"""The deliberately small graph and diagnostic bank used by the tutor."""

import json
from pathlib import Path

try:
    from .learn_state import IDS, SCOPES, StateError, require
except ImportError:
    from learn_state import IDS, SCOPES, StateError, require


DOMAIN = Path(__file__).resolve().parents[1] / 'competencies/graph-theory'


class Graph:
    def __init__(self, data):
        require(data.get('schema_version') == 1 and data.get('version') == 1, 'Unsupported competency graph version')
        require(data.get('area_id') == 'graph-theory', 'Only the graph-theory MVP is supported')
        nodes = data.get('concepts')
        require(isinstance(nodes, list), 'Missing concepts')
        self.nodes = {node['id']: node for node in nodes}
        require(len(self.nodes) == len(nodes), 'Duplicate concept IDs')
        require(set(self.nodes) == set(IDS), 'Graph must contain the seven stable MVP concepts')
        self.version = data['version']
        for node in nodes:
            require(node.get('parent_area') == 'graph-theory', 'Grouping is not a prerequisite concept')
            require(node.get('scope') == SCOPES[node['id']] and node.get('scope_version') == 1, 'Concept scope mismatch')
            require(isinstance(node.get('prerequisites'), list), 'Missing prerequisites')
            require(len(node['prerequisites']) == len(set(node['prerequisites'])), 'Duplicate prerequisites')
            require(all(p in self.nodes for p in node['prerequisites']), 'Missing prerequisite node')
        for ident in self.nodes:
            self.ordered(ident)

    @classmethod
    def load(cls, path=DOMAIN / 'graph.json'):
        return cls(json.loads(Path(path).read_text()))

    def ordered(self, target):
        require(target in self.nodes, 'Unknown target concept')
        visiting, done, result = set(), set(), []

        def visit(ident):
            require(ident not in visiting, 'Prerequisite cycle')
            if ident in done:
                return
            visiting.add(ident)
            for parent in self.nodes[ident]['prerequisites']:
                visit(parent)
            visiting.remove(ident)
            done.add(ident)
            result.append(ident)

        visit(target)
        return result

    def dependents(self, ident):
        require(ident in self.nodes, 'Unknown concept')
        return [c for c in IDS if ident in self.nodes[c]['prerequisites']]


def questions(graph=None, path=DOMAIN / 'questions.json'):
    graph = graph or Graph.load()
    data = json.loads(Path(path).read_text())
    require(data.get('schema_version') == 1 and data.get('graph_version') == graph.version, 'Question/graph version mismatch')
    seen = set()
    for q in data.get('questions', []):
        require(q['id'] not in seen, 'Duplicate question ID')
        seen.add(q['id'])
        require(q.get('concept_id') in graph.nodes, 'Question has unknown concept')
        require(q.get('scope') == graph.nodes[q['concept_id']]['scope'], 'Question scope mismatch')
        require(q.get('scope_version') == 1, 'Question scope version mismatch')
        require(q.get('level') in {'foundation', 'core', 'stretch'}, 'Invalid difficulty level')
        require(q.get('capability') in {'explanation', 'application'}, 'Invalid bank capability')
        require(bool(q.get('text')) and bool(q.get('rubric', {}).get('criteria')), 'Missing prompt/rubric')
        require(q.get('novel') is (q['capability'] == 'application'), 'Transfer metadata mismatch')
    require(all({q['capability'] for q in data['questions'] if q['concept_id'] == c} == {'explanation', 'application'} for c in IDS), 'Every concept needs explanation and application prompts')
    return data['questions']
