import json
from pathlib import Path
import unittest

from helpers import StateCase


class EarlyRecordCompatibilityTests(StateCase):
    def test_early_records_resolve_in_the_final_graph_without_renaming(self):
        fixture = Path(__file__).parent / 'fixtures/milestone1-session.json'
        session = json.loads(fixture.read_text())
        for observation in session['observations']:
            recorded = self.store.record(observation)
            self.assertEqual(recorded['id'], observation['id'])
            self.assertEqual(recorded['concept_ids'], observation['concept_ids'])
            self.assertEqual(recorded['response'], observation['response'])
        projection = self.projection()
        self.assertEqual(projection['graph_version'], 1)
        self.assertTrue(projection['graph_ref'].endswith('#graph-theory.connectivity'))
        self.assertEqual(projection['evidence_refs'], session['evidence_refs'])
        # Historical applications without explicit novelty remain useful evidence,
        # but are not retroactively relabeled to establish active competence.
        self.assertNotEqual(projection['competency_state'], 'active')


class InitialEvidenceTests(unittest.TestCase):
    def test_distinct_explanation_and_transfer_observations(self):
        session = json.loads((Path(__file__).parent / "fixtures/milestone1-session.json").read_text())
        records = session["observations"]
        self.assertEqual(session["evidence_refs"], [r["id"] for r in records])
        self.assertEqual(len({r["question"]["id"] for r in records}), 2)
        self.assertEqual({r["question"]["capability"] for r in records}, {"explanation", "application"})
        for r in records:
            self.assertEqual(r["concept_ids"], ["graph-theory.connectivity"])
            self.assertEqual(r["schema_version"], 1)
            self.assertEqual(r["provenance"]["source"], "synthetic")
            self.assertTrue(r["response"])
            self.assertTrue(r["rubric"]["criteria"])
            self.assertTrue(r["evaluation"]["rationale"])
            self.assertEqual(r["assistance"], "none")


if __name__ == "__main__":
    unittest.main()
