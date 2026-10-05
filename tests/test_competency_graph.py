import copy
import json
from pathlib import Path
import tempfile
import unittest

from scripts.competency import DOMAIN, Graph, questions
from scripts.learn_state import IDS, StateError


class GraphTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((DOMAIN / 'graph.json').read_text())

    def test_shortest_paths_have_only_relevant_prerequisites(self):
        graph = Graph(self.data)
        self.assertEqual(graph.ordered('graph-theory.bfs-shortest-paths'), [
            'graph-theory.terminology', 'graph-theory.connectivity',
            'graph-theory.bfs', 'graph-theory.bfs-shortest-paths'])
        self.assertNotIn('graph-theory', graph.nodes)
        self.assertNotIn('graph-theory.trees', graph.ordered('graph-theory.bfs-shortest-paths'))

    def test_invalid_references_duplicates_and_cycles_fail(self):
        cases = []
        duplicate = copy.deepcopy(self.data)
        duplicate['concepts'].append(duplicate['concepts'][0])
        cases.append(duplicate)
        missing = copy.deepcopy(self.data)
        missing['concepts'][1]['prerequisites'] = ['graph-theory']
        cases.append(missing)
        cycle = copy.deepcopy(self.data)
        cycle['concepts'][0]['prerequisites'] = ['graph-theory.connectivity']
        cases.append(cycle)
        version = copy.deepcopy(self.data)
        version['version'] = 2
        cases.append(version)
        for data in cases:
            with self.subTest(data=data), self.assertRaises(StateError):
                Graph(data)

    def test_all_final_ids_and_both_capabilities_are_available(self):
        graph = Graph.load()
        bank = questions(graph)
        self.assertEqual(set(graph.nodes), set(IDS))
        self.assertEqual(len(bank), 14)
        for c in IDS:
            self.assertEqual({q['capability'] for q in bank if q['concept_id'] == c}, {'explanation', 'application'})

    def test_invalid_bank_versions_and_ids_fail(self):
        bank = json.loads((DOMAIN / 'questions.json').read_text())
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / 'questions.json'
            bank['graph_version'] = 2
            path.write_text(json.dumps(bank))
            with self.assertRaises(StateError):
                questions(path=path)
            bank['graph_version'] = 1
            bank['questions'][0]['concept_id'] = 'probability.expectation'
            path.write_text(json.dumps(bank))
            with self.assertRaises(StateError):
                questions(path=path)
