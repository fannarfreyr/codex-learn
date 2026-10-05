import json
import subprocess
import sys

from helpers import StateCase, declaration, event, report
from scripts.calibration import start
from scripts.learn_state import REPO, StateError, Store


TARGET = 'graph-theory.bfs-shortest-paths'
TERM = 'graph-theory.terminology'
CONN = 'graph-theory.connectivity'
BFS = 'graph-theory.bfs'


class PlanningTests(StateCase):
    def actions(self):
        return {s['concept_id']: s['action'] for s in self.store.plan(TARGET)['steps']}

    def test_plan_uses_only_target_ancestors_and_priors_never_skip(self):
        self.store.record(declaration())
        plan = self.store.plan(TARGET)
        self.assertEqual([s['concept_id'] for s in plan['steps']], [TERM, CONN, BFS, TARGET])
        self.assertEqual(set(self.actions().values()), {'teach'})

    def test_active_rusty_and_unknown_have_different_actions(self):
        self.active(TERM, 'terms')
        self.store.record(report('old-bfs', 'studied_before', BFS))
        self.store.record(event('failed-bfs', BFS, outcome='incorrect'))
        self.store.record(event('hinted-bfs', BFS, 'application', assistance='hint', novel=True))
        actions = self.actions()
        self.assertEqual(actions[TERM], 'skip')
        self.assertEqual(actions[CONN], 'teach')
        self.assertEqual(actions[BFS], 'refresh')
        self.assertEqual(actions[TARGET], 'teach')

    def test_forgotten_exposed_and_never_learned_remain_distinct(self):
        self.store.record(report('forgot', 'forgotten', TERM))
        self.store.record(report('exposure', 'recognize', CONN))
        self.store.record(report('new', 'never_seen', BFS))
        self.assertEqual(self.actions(), {TERM: 'reconstruct', CONN: 'bridge', BFS: 'teach', TARGET: 'teach'})

    def test_later_conflict_replaces_skip_with_verification(self):
        self.active(TERM, 'terms')
        self.store.plan(TARGET)
        self.store.record(event('conflict', TERM, outcome='incorrect'))
        saved = json.loads((self.root / 'plan.json').read_text())
        self.assertEqual(saved['steps'][0]['action'], 'verify')
        self.assertIn('conflict', saved['steps'][0]['evidence_refs'])

    def test_wrong_scope_and_dependent_success_do_not_unlock_foundations(self):
        self.store.record(event('narrow', TERM, scope='Recognize a vertex'))
        self.store.record(event('apply', TERM, 'application', novel=True))
        self.active(BFS, 'bfs')
        self.assertNotEqual(self.actions()[TERM], 'skip')
        self.assertEqual(self.actions()[CONN], 'teach')

    def test_teaching_updates_existing_plan_and_checkpoint(self):
        self.store.plan(TARGET)
        self.active(TERM, 'taught-terms')
        fresh = Store(self.root, allow_synthetic=True).resume()
        self.assertEqual(fresh['plan']['steps'][0]['action'], 'skip')
        self.assertEqual(fresh['plan']['current_checkpoint']['concept_id'], CONN)
        self.assertEqual(fresh['plan']['evidence_sequence'], 2)

    def test_answer_recorded_before_checkpoint_save_is_recovered(self):
        step = start(self.store, 'interrupted')
        q = step['question']
        value = event('answer', q['concept_id'], session='interrupted')
        value['question'] = {k: v for k, v in q.items() if k not in {'concept_id', 'level', 'rubric'}}
        value['rubric'] = q['rubric']
        self.store.record(value)
        # A fresh process has no Python object or prior conversational context.
        result = subprocess.run([sys.executable, str(REPO / 'scripts/learn_state.py'),
                                 '--state-dir', str(self.root), '--synthetic', 'resume'],
                                capture_output=True, text=True, check=True)
        resumed = json.loads(result.stdout)
        self.assertEqual(resumed['latest_session']['pending_answer_refs'], ['answer'])
        self.assertIn('already saved', resumed['latest_session']['next_action'])

    def test_unanswered_teaching_question_is_preserved(self):
        self.store.plan(TARGET)
        question = {'id': 'pending-lesson', 'concept_id': TERM, 'text': 'Explain degree.'}
        self.store.session({'schema_version': 1, 'id': 'lesson', 'mode': 'teaching',
                            'goal': TARGET, 'evidence_refs': [], 'pending_question': question,
                            'next_action': 'Wait for learner response'})
        resumed = Store(self.root, allow_synthetic=True).resume()
        self.assertEqual(resumed['latest_session']['pending_question'], question)
        self.assertEqual(resumed['latest_session']['pending_answer_refs'], [])

    def test_edited_plan_actions_are_rebuilt_from_evidence(self):
        plan = self.store.plan(TARGET)
        plan['steps'][0]['action'] = 'skip'
        (self.root / 'plan.json').write_text(json.dumps(plan))
        with self.assertRaises(StateError):
            self.store.validate()
        self.assertEqual(self.store.resume()['plan']['steps'][0]['action'], 'teach')

    def test_invalid_checkpoint_is_reported_without_replacing_it(self):
        self.store.session({'schema_version': 1, 'id': 'lesson', 'mode': 'teaching',
                            'goal': TARGET, 'evidence_refs': [], 'pending_question': None})
        path = self.root / 'sessions/lesson.json'
        value = json.loads(path.read_text())
        value['evidence_refs'] = ['missing-answer']
        path.write_text(json.dumps(value))
        with self.assertRaises(StateError):
            self.store.resume()
        with self.assertRaises(StateError):
            self.store.validate()
        self.assertEqual(json.loads(path.read_text())['evidence_refs'], ['missing-answer'])

    def test_demonstrated_target_finishes_only_its_scoped_path(self):
        for index, concept in enumerate((TERM, CONN, BFS, TARGET)):
            self.active(concept, 'ready-' + str(index))
        plan = self.store.plan(TARGET)
        self.assertEqual(plan['status'], 'demonstrated_within_scope')
        self.assertIsNone(plan['current_checkpoint'])
        self.assertEqual(self.projection('graph-theory.dfs')['competency_state'], 'unknown')

    def test_unknown_target_rejected_without_plan_write(self):
        with self.assertRaises(StateError):
            self.store.plan('probability.expectation')
        self.assertFalse((self.root / 'plan.json').exists())
