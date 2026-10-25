import copy
import json
import subprocess
import sys

from helpers import StateCase, declaration, event, report
from scripts.calibration import advance, start
from scripts.learn_state import IDS, REPO, StateError, Store


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
        step = start(self.store, 'overestimate', strategy='focused', target='graph-theory.connectivity')
        step = self.answer(step, 'incorrect')
        self.assertEqual(step['question']['concept_id'], 'graph-theory.terminology')
        self.assertEqual(step['question']['level'], 'foundation')

    def test_focused_success_confirms_application_then_checks_prerequisite(self):
        step = start(self.store, 'strong', strategy='focused', target='graph-theory.connectivity')
        step = self.answer(step)
        self.assertEqual(step['question']['capability'], 'application')
        step = self.answer(step)
        self.assertEqual(step['question']['concept_id'], 'graph-theory.terminology')
        self.assertEqual(step['question']['level'], 'foundation')

    def test_hint_does_not_unlock_prerequisite(self):
        step = start(self.store, 'hinted', strategy='focused', target='graph-theory.terminology')
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
        self.assertEqual(step['session']['status'], 'paused')
        self.assertTrue(step['coverage']['breadth_complete'])
        self.assertTrue(all(e['evaluation']['outcome'] == 'correct' for e in self.store.events()))

    def test_survey_samples_all_concepts_before_repeating_even_after_gaps(self):
        self.store.record(declaration())
        step = start(self.store, 'broad', budget=14)
        sampled = []
        for _ in IDS:
            sampled.append(step['question']['concept_id'])
            step = self.answer(step, 'incorrect')
        self.assertEqual(set(sampled), set(IDS))
        self.assertEqual(len(sampled), len(set(sampled)))
        self.assertTrue(step['coverage']['breadth_complete'])
        self.assertIsNotNone(step['question'])

    def test_weak_connectivity_and_strong_downstream_evidence_survive(self):
        self.store.record(declaration())
        step = start(self.store, 'mixed', budget=14)
        while step['question']:
            outcome = 'incorrect' if step['question']['concept_id'] == 'graph-theory.connectivity' else 'correct'
            step = self.answer(step, outcome)
        self.assertEqual(step['session']['status'], 'completed')
        for concept in ('bfs', 'dfs', 'bfs-shortest-paths'):
            self.assertEqual(self.projection('graph-theory.' + concept)['competency_state'], 'active')
        self.assertNotEqual(self.projection()['competency_state'], 'active')
        self.assertEqual(self.projection()['capabilities']['application']['status'], 'not_demonstrated')
        actions = {s['concept_id']: s['action'] for s in self.store.plan('graph-theory.bfs-shortest-paths')['steps']}
        self.assertEqual(actions['graph-theory.bfs'], 'skip')
        self.assertNotEqual(actions['graph-theory.connectivity'], 'skip')
        self.assertTrue(step['coverage']['breadth_complete'])
        self.assertTrue(step['coverage']['concepts']['graph-theory.connectivity']['uncertainty'])
        self.assertTrue(self.store.validate()['valid'])

    def test_terminology_gap_and_application_are_distinct_capabilities(self):
        for concept in IDS[1:]:
            self.active(concept, concept)
        step = start(self.store, 'retrieval')
        step = self.answer(step, 'incorrect')
        self.assertEqual(step['question']['capability'], 'application')
        step = self.answer(step)
        profile = self.projection(IDS[0])
        self.assertEqual(profile['capabilities']['explanation']['status'], 'not_demonstrated')
        self.assertEqual(profile['capabilities']['application']['status'], 'demonstrated')
        self.assertNotEqual(profile['competency_state'], 'active')

    def test_knows_without_name_prefers_application_without_claiming_coverage(self):
        self.store.record(report('name', 'knows_without_name', IDS[0]))
        step = start(self.store, 'names')
        self.assertEqual(step['question']['capability'], 'application')
        self.assertFalse(step['coverage']['concepts'][IDS[0]]['sampled'])

    def test_prior_direct_evidence_is_reused_but_not_narrow_or_skip(self):
        self.store.record(event('old-term', IDS[0]))
        self.store.record(event('narrow', IDS[1], scope='Recall a word'))
        self.store.record(event('declined', IDS[2], outcome='skip'))
        step = start(self.store, 'reuse')
        self.assertEqual(step['question']['concept_id'], IDS[1])
        records = step['coverage']['concepts']
        self.assertEqual(records[IDS[0]]['tested_previously_refs'], ['old-term'])
        self.assertTrue(records[IDS[0]]['sampled'])
        self.assertFalse(records[IDS[1]]['sampled'])
        self.assertFalse(records[IDS[2]]['sampled'])

    def test_conflicting_evidence_gets_first_follow_up_and_corrections_apply(self):
        for concept in IDS:
            self.store.record(event('old-' + concept, concept))
        self.active(IDS[4], 'dfs-pair')
        self.store.record(event('dfs-conflict', IDS[4], outcome='incorrect'))
        step = start(self.store, 'conflicted')
        self.assertEqual(step['question']['concept_id'], IDS[4])
        self.assertIn('conflicting', step['reason'])
        original = next(e for e in self.store.events() if e['id'] == 'dfs-conflict')
        correction = {'id': 'fixed', 'kind': 'correction', 'session_id': 'review',
                      'concept_ids': [IDS[4]], 'provenance': original['provenance'],
                      'target_id': original['id'], 'reason': 'Synthetic review of tutor evaluation',
                      'evaluation': dict(original['evaluation'], outcome='correct')}
        self.store.record(correction)
        fresh = start(self.store, 'corrected')
        self.assertNotEqual(fresh['question']['concept_id'], IDS[4])
        self.assertIn('fixed', fresh['coverage']['concepts'][IDS[4]]['evaluation_refs'])

    def test_budget_pause_and_bounded_resume_keep_same_survey(self):
        step = start(self.store, 'blocks', budget=2)
        step = self.answer(step)
        step = self.answer(step)
        self.assertEqual(step['session']['status'], 'paused')
        self.assertFalse(step['coverage']['breadth_complete'])
        self.assertIsNone(advance(self.store, 'blocks')['question'])
        step = advance(self.store, 'blocks', budget=3)
        self.assertEqual(step['session']['response_limit'], 5)
        self.assertEqual(step['question']['concept_id'], IDS[2])
        again = advance(self.store, 'blocks', budget=14)
        self.assertEqual(again['session']['response_limit'], 5)
        self.assertEqual(step['question'], again['question'])
        for _ in range(3):
            step = self.answer(step)
        self.assertEqual(step['session']['response_count'], 5)
        self.assertEqual(step['session']['status'], 'paused')

    def test_pause_keeps_unanswered_question_and_stop_is_terminal(self):
        step = start(self.store, 'pause')
        paused = advance(self.store, 'pause', pause=True)
        self.assertEqual(paused['session']['pending_question'], step['question'])
        self.assertIsNone(advance(self.store, 'pause')['question'])
        continued = advance(self.store, 'pause', budget=2)
        self.assertEqual(continued['question'], step['question'])
        stopped = advance(self.store, 'pause', stop=True)
        self.assertIsNone(stopped['session']['pending_question'])
        path = self.root / 'sessions/pause.json'
        saved = path.read_bytes()
        self.assertIsNone(advance(self.store, 'pause', budget=8)['question'])
        self.assertEqual(path.read_bytes(), saved)

    def test_final_turn_self_report_skip_is_consumed_before_pause(self):
        step = start(self.store, 'last-skip', budget=1)
        question = step['question']
        skipped = report('skip-final', 'skip', question['concept_id'])
        skipped['session_id'] = 'last-skip'
        self.store.record(skipped)
        paused = advance(self.store, 'last-skip')
        self.assertIn(question['id'], paused['session']['consumed_question_ids'])
        continued = advance(self.store, 'last-skip', budget=14)
        self.assertNotEqual(continued['question']['concept_id'], question['concept_id'])
        self.assertTrue(continued['coverage']['concepts'][question['concept_id']]['deferred'])
        self.assertFalse(continued['coverage']['concepts'][question['concept_id']]['sampled'])

    def test_focused_stays_within_target_path_and_can_stop_at_boundary(self):
        step = start(self.store, 'target', budget=14, strategy='focused', target=IDS[5])
        asked = []
        while step['question']:
            asked.append(step['question']['concept_id'])
            step = self.answer(step, 'incorrect')
        self.assertEqual(asked[0], IDS[5])
        self.assertTrue(set(asked) <= {IDS[0], IDS[1], IDS[3], IDS[5]})
        self.assertIn('useful_boundary', step['reason'])
        self.assertEqual(set(step['coverage']['concepts']), {IDS[0], IDS[1], IDS[3], IDS[5]})

    def test_complete_focused_profile_asks_nothing_unrelated(self):
        for concept in (IDS[0], IDS[1], IDS[3], IDS[5]):
            self.active(concept, concept)
        step = start(self.store, 'ready', strategy='focused', target=IDS[5])
        self.assertIsNone(step['question'])
        self.assertEqual(step['reason'], 'scoped_readiness_supported')
        self.assertEqual(self.projection(IDS[4])['competency_state'], 'unknown')

    def test_bank_exhaustion_does_not_claim_readiness(self):
        step = start(self.store, 'exhaust', budget=14)
        while step['question']:
            step = self.answer(step, 'incorrect')
        if step['session']['status'] == 'paused':
            step = advance(self.store, 'exhaust', budget=1)
        self.assertIn('no_remaining_informative', step['reason'])
        self.assertTrue(step['coverage']['breadth_complete'])
        self.assertTrue(all(not c['ready'] and c['uncertainty'] for c in step['coverage']['concepts'].values()))
        second = start(self.store, 'exhaust-again')
        self.assertIsNone(second['question'])
        self.assertEqual(len(self.store.events()), 14)

    def test_legacy_checkpoint_is_upgraded_only_on_update(self):
        step = start(self.store, 'legacy')
        legacy = {k: v for k, v in step['session'].items()
                  if k not in {'strategy', 'target', 'status', 'pause_reason', 'response_limit', 'response_count', 'consumed_question_ids'}}
        legacy['schema_version'] = 1
        self.store.session(legacy)
        path = self.root / 'sessions/legacy.json'
        saved = path.read_bytes()
        resumed = Store(self.root, allow_synthetic=True).resume()
        self.assertEqual(path.read_bytes(), saved)
        self.assertEqual(resumed['latest_session']['strategy'], 'survey')
        continued = advance(self.store, 'legacy')
        self.assertEqual(continued['question'], step['question'])
        self.assertEqual(json.loads(path.read_text())['schema_version'], 2)
        legacy.update(stop_reason='useful_boundary_found', pending_question=None)
        self.store.session(legacy)
        saved = path.read_bytes()
        self.assertIsNone(advance(self.store, 'legacy', budget=8)['question'])
        self.assertEqual(path.read_bytes(), saved)

    def test_invalid_configuration_does_not_create_session(self):
        for options in ({'budget': 0}, {'budget': 15}, {'budget': True}, {'strategy': 'other'},
                        {'strategy': 'focused'}, {'strategy': 'focused', 'target': 'missing'}, {'target': IDS[0]}):
            with self.subTest(options=options), self.assertRaises(StateError):
                start(self.store, 'bad', **options)
            self.assertFalse((self.root / 'sessions/bad.json').exists())

    def test_invalid_v2_checkpoint_is_rejected_before_replacing_it(self):
        step = start(self.store, 'valid')
        for changes in ({'status': 'wrong'}, {'strategy': 'focused'}, {'budget': 15},
                        {'response_limit': 0}, {'consumed_question_ids': ['../outside']},
                        {'schema_version': 3}, {'mode': 'teaching'}):
            value = copy.deepcopy(step['session'])
            value.update(changes)
            path = self.root / 'sessions/valid.json'
            saved = path.read_bytes()
            with self.subTest(changes=changes), self.assertRaises(StateError):
                self.store.session(value)
            self.assertEqual(path.read_bytes(), saved)

    def test_fresh_process_recovers_saved_answer_and_live_coverage(self):
        step = start(self.store, 'process', budget=1)
        q = step['question']
        value = event('saved-before-crash', q['concept_id'], q['capability'], session='process')
        value.update(question={k: v for k, v in q.items() if k not in {'concept_id', 'level', 'rubric'}}, rubric=q['rubric'])
        self.store.record(value)
        evidence = {p.name: p.read_bytes() for p in (self.root / 'evidence').glob('*.json')}
        resumed = self.cli('resume')
        self.assertEqual(resumed['latest_session']['pending_answer_refs'], ['saved-before-crash'])
        self.assertTrue(resumed['latest_session']['coverage']['concepts'][q['concept_id']]['sampled'])
        paused = self.cli('next', 'process')
        self.assertEqual(paused['session']['status'], 'paused')
        continued = self.cli('next', 'process', '--budget', '8')
        self.assertNotEqual(continued['question']['id'], q['id'])
        self.assertEqual(continued['session']['response_count'], 1)
        self.assertEqual(evidence, {p.name: p.read_bytes() for p in (self.root / 'evidence').glob('*.json')})

    def cli(self, *args):
        result = subprocess.run([sys.executable, str(REPO / 'scripts/learn_state.py'),
                                 '--state-dir', str(self.root), '--synthetic', *args],
                                capture_output=True, text=True, check=True)
        return json.loads(result.stdout)

    def test_cli_exposes_strategies_pause_and_block_budgets(self):
        step = self.cli('calibrate', '--session-id', 'cli', '--strategy', 'focused', '--target', IDS[3], '--budget', '3')
        self.assertEqual(step['question']['concept_id'], IDS[3])
        self.assertEqual(self.cli('pause', 'cli')['session']['status'], 'paused')
        self.assertEqual(self.cli('next', 'cli', '--budget', '2')['session']['response_limit'], 2)
        self.assertEqual(self.cli('stop', 'cli')['session']['status'], 'stopped')

    def test_survey_depth_varies_with_prior_evidence(self):
        self.active(IDS[0], 'old-active')
        self.store.record(event('old-connectivity', IDS[1]))
        step = start(self.store, 'uneven', budget=14)
        asked = []
        while step['question']:
            asked.append(step['question']['concept_id'])
            step = self.answer(step)
        self.assertNotIn(IDS[0], asked)
        self.assertEqual(asked.count(IDS[1]), 1)
        self.assertEqual(asked.count(IDS[3]), 2)
        self.assertTrue(step['coverage']['breadth_complete'])

    def test_aided_survey_samples_other_branches_without_promoting(self):
        step = start(self.store, 'aided-survey')
        for _ in IDS:
            step = self.answer(step, assistance='hint')
        self.assertTrue(step['coverage']['breadth_complete'])
        self.assertIsNotNone(step['question'])
        self.assertTrue(all(p['competency_state'] != 'active' for p in self.store.projections().values()))

    def test_correction_is_not_an_extra_response_turn(self):
        step = start(self.store, 'correct-turn', budget=2)
        step = self.answer(step, 'incorrect')
        original = self.store.events()[0]
        self.store.record({'id': 'amend', 'kind': 'correction', 'session_id': 'correct-turn',
                           'target_id': original['id'], 'concept_ids': original['concept_ids'],
                           'provenance': original['provenance'], 'reason': 'Synthetic grading review',
                           'evaluation': dict(original['evaluation'], outcome='correct')})
        step = advance(self.store, 'correct-turn')
        self.assertEqual(step['session']['response_count'], 1)
        self.assertIn('amend', step['coverage']['concepts'][IDS[0]]['evaluation_refs'])
        self.assertEqual(step['coverage']['concepts'][IDS[0]]['capabilities']['explanation']['status'], 'demonstrated')
        self.assertEqual(step['coverage']['concepts'][IDS[0]]['untested_capabilities'], ['application'])

    def test_paused_saved_answer_is_recovered_before_new_block(self):
        step = start(self.store, 'paused-answer')
        advance(self.store, 'paused-answer', pause=True)
        q = step['question']
        value = event('late-answer', q['concept_id'], q['capability'], session='paused-answer')
        value.update(question={k: v for k, v in q.items() if k not in {'concept_id', 'level', 'rubric'}}, rubric=q['rubric'])
        self.store.record(value)
        step = advance(self.store, 'paused-answer', budget=2)
        self.assertEqual(step['session']['response_limit'], 3)
        self.assertEqual(step['session']['response_count'], 1)
        self.assertNotEqual(step['question']['id'], q['id'])

    def test_cli_rejects_invalid_configuration_without_creating_state(self):
        for args in (('calibrate', '--budget', '15'), ('calibrate', '--strategy', 'focused'),
                     ('calibrate', '--target', IDS[0]), ('calibrate', '--strategy', 'bad')):
            result = subprocess.run([sys.executable, str(REPO / 'scripts/learn_state.py'),
                                     '--state-dir', str(self.root), '--synthetic', *args],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertFalse((self.root / 'sessions').exists())
