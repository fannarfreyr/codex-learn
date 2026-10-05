from helpers import StateCase, declaration, event, report
from scripts.calibration import advance, start
from scripts.learn_state import StateError


class CalibrationTests(StateCase):
    def test_unsafe_session_ids_are_rejected_before_file_access(self):
        for ident in ('../outside', '/absolute', ''):
            with self.assertRaises(StateError):
                advance(self.store, ident)
        with self.assertRaises(StateError):
            start(self.store, '../outside')

    def answer(self, step, outcome='correct', assistance='none'):
        q = step['question']
        value = event('answer-' + str(len(self.store.events())), q['concept_id'], q['capability'],
                      outcome, assistance, q['novel'], step['session']['id'])
        value['question'] = {k: v for k, v in q.items() if k not in {'concept_id', 'level', 'rubric'}}
        value['rubric'] = q['rubric']
        self.store.record(value)
        return advance(self.store, step['session']['id'])

    def test_prior_changes_start_without_creating_competence(self):
        first = start(self.store, 'no-prior')
        self.assertEqual(first['question']['concept_id'], 'graph-theory.terminology')
        self.store.record(declaration())
        second = start(self.store, 'with-prior')
        self.assertEqual(second['question']['concept_id'], 'graph-theory.connectivity')
        self.assertEqual(self.projection()['competency_state'], 'unknown')

    def test_waits_without_inventing_answers_or_advancing(self):
        first = start(self.store, 'waiting')
        again = advance(self.store, 'waiting')
        self.assertEqual(first['question'], again['question'])
        self.assertEqual(self.store.events(), [])

    def test_basic_failure_redirects_from_core_to_foundation(self):
        self.store.record(declaration())
        step = start(self.store, 'overestimate')
        step = self.answer(step, 'incorrect')
        self.assertEqual(step['question']['concept_id'], 'graph-theory.terminology')
        self.assertEqual(step['question']['level'], 'foundation')

    def test_success_confirms_application_then_moves_upward(self):
        step = start(self.store, 'strong')
        step = self.answer(step)
        self.assertEqual(step['question']['capability'], 'application')
        step = self.answer(step)
        self.assertEqual(step['question']['concept_id'], 'graph-theory.connectivity')
        self.assertEqual(step['question']['level'], 'core')

    def test_hint_does_not_unlock_prerequisite(self):
        step = start(self.store, 'hinted')
        step = self.answer(step)
        step = self.answer(step, assistance='hint')
        self.assertNotEqual(self.projection('graph-theory.terminology')['competency_state'], 'active')
        self.assertIsNone(step['question'])
        self.assertIn('boundary', step['reason'])

    def test_skip_is_recorded_and_another_strand_can_be_probed(self):
        step = start(self.store, 'skip')
        old = step['question']['id']
        step = self.answer(step, outcome='skip')
        self.assertNotEqual(step['question']['id'], old)
        self.assertEqual(self.projection('graph-theory.terminology')['competency_state'], 'unknown')

    def test_self_report_is_an_answer_without_fabricated_performance(self):
        step = start(self.store, 'self-report')
        value = report('never-seen', 'never_seen', step['question']['concept_id'])
        value['session_id'] = 'self-report'
        self.store.record(value)
        next_step = advance(self.store, 'self-report')
        self.assertNotEqual(next_step['question']['id'], step['question']['id'])
        self.assertEqual(len(self.store.events()), 1)
        self.assertEqual(self.store.events()[0]['kind'], 'self_report')

    def test_budget_and_learner_stop_are_explicit(self):
        step = start(self.store, 'short', budget=1)
        step = self.answer(step)
        self.assertIsNone(step['question'])
        self.assertIn('budget', step['reason'])
        other = start(self.store, 'stop')
        stopped = advance(self.store, 'stop', stop=True)
        self.assertEqual(stopped['reason'], 'learner_requested_stop')

    def test_self_report_and_performance_from_one_turn_count_once(self):
        step = start(self.store, 'one-turn', budget=2)
        q = step['question']
        value = event('attempt', q['concept_id'], outcome='partial', session='one-turn')
        value['question'] = {k: v for k, v in q.items() if k not in {'concept_id', 'level', 'rubric'}}
        value.update(turn_id='learner-turn-1', rubric=q['rubric'])
        self.store.record(value)
        history = report('remembered', 'studied_before', q['concept_id'])
        history.update(session_id='one-turn', turn_id='learner-turn-1')
        self.store.record(history)
        next_step = advance(self.store, 'one-turn')
        self.assertEqual(next_step['session']['response_count'], 1)
        self.assertIsNotNone(next_step['question'])
        self.assertEqual(self.projection(q['concept_id'])['competency_state'], 'rusty')

    def test_all_correct_can_stop_without_forcing_a_failure(self):
        step = start(self.store, 'all-correct')
        while step['question']:
            step = self.answer(step)
        self.assertEqual(step['session']['response_count'], 8)
        self.assertTrue(all(e['evaluation']['outcome'] == 'correct' for e in self.store.events()))
