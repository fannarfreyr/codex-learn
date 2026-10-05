import copy
import json
from unittest.mock import patch

from helpers import CONNECTIVITY, StateCase, declaration, event, report
from scripts.learn_state import IDS, REPO, StateError, Store


class EvidenceTests(StateCase):
    def test_only_unaided_scoped_explanation_and_novel_application_activate(self):
        self.store.record(event('recognize', capability='recognition'))
        self.assertNotEqual(self.projection()['competency_state'], 'active')
        self.store.record(event('explain'))
        self.store.record(event('aided', capability='application', assistance='hint', novel=True))
        self.assertNotEqual(self.projection()['competency_state'], 'active')
        self.store.record(event('transfer', capability='application', novel=True))
        self.assertEqual(self.projection()['competency_state'], 'active')
        self.assertEqual(self.projection()['evidence_confidence'], 'moderate')

    def test_narrow_scope_does_not_support_skipping_broad_scope(self):
        self.store.record(event('narrow', scope='One direct edge only'))
        self.store.record(event('apply', capability='application', novel=True))
        self.assertNotEqual(self.projection()['competency_state'], 'active')

    def test_background_and_self_report_never_activate(self):
        self.store.record(declaration())
        self.assertEqual(self.projection()['competency_state'], 'unknown')
        self.assertEqual(self.projection()['evidence_confidence'], 'none')
        self.store.record(report('claimed', 'competent'))
        self.assertEqual(self.projection()['competency_state'], 'exposed')

    def test_rusty_and_forgotten_need_history_not_failure_alone(self):
        self.store.record(event('failure', outcome='incorrect'))
        self.assertEqual(self.projection()['competency_state'], 'developing')
        self.store.record(report('history', 'studied_before'))
        self.assertEqual(self.projection()['competency_state'], 'forgotten')
        self.store.record(event('hinted', capability='application', assistance='hint', novel=True))
        self.assertEqual(self.projection()['competency_state'], 'rusty')

    def test_never_seen_is_a_qualified_self_report(self):
        self.store.record(report('never', 'never_seen'))
        p = self.projection()
        self.assertEqual((p['competency_state'], p['evidence_confidence']), ('never_learned', 'low'))

    def test_skip_does_not_change_competence(self):
        self.active()
        before = self.projection()
        self.store.record(event('skip', outcome='skip'))
        after = self.projection()
        for field in ('competency_state', 'evidence_confidence', 'capabilities'):
            self.assertEqual(before[field], after[field])

    def test_conflicting_observation_requires_verification_then_refresh(self):
        self.active()
        self.store.record(event('later-fail', outcome='incorrect'))
        p = self.projection()
        self.assertEqual((p['competency_state'], p['evidence_confidence']), ('active', 'low'))
        self.assertEqual(p['conflict_refs'], ['later-fail'])
        self.store.record(event('confirm-gap', capability='application', outcome='partial', novel=True))
        self.assertEqual(self.projection()['competency_state'], 'rusty')
        self.active(prefix='repaired')
        self.assertEqual(self.projection()['competency_state'], 'active')
        self.assertEqual(self.projection()['conflict_refs'], [])

    def test_corrections_preserve_response_and_original_evaluation(self):
        original = event('mistake', outcome='incorrect')
        self.store.record(original)
        correction = report('correction', 'skip')
        correction.pop('statement')
        correction.pop('report_type')
        correction.update(kind='correction', target_id='mistake', reason='Tutor misread the answer', evaluation=event('x')['evaluation'])
        self.store.record(correction)
        self.store.record(event('apply', capability='application', novel=True))
        self.assertEqual(self.projection()['competency_state'], 'active')
        recorded = self.store.events()[0]
        self.assertEqual(recorded['response'], original['response'])
        self.assertEqual(recorded['evaluation']['outcome'], 'incorrect')
        self.assertIn('correction', self.projection()['estimate_basis_refs'])
        correction2 = copy.deepcopy(correction)
        correction2.update(id='second-correction', target_id='correction', evaluation=event('x', outcome='partial')['evaluation'])
        self.store.record(correction2)
        self.assertNotEqual(self.projection()['competency_state'], 'active')

    def test_idempotence_and_conflicting_ids(self):
        original = event('same')
        original.pop('timestamp')
        self.store.record(original)
        self.store.record(original)
        self.assertEqual(len(self.store.events()), 1)
        changed = copy.deepcopy(original)
        changed['response'] = 'Different response'
        with self.assertRaises(StateError):
            self.store.record(changed)
        self.assertEqual(len(self.store.events()), 1)

    def test_correction_cannot_rewrite_the_original_observation(self):
        self.store.record(event('original', outcome='incorrect'))
        correction = report('bad-correction', 'skip')
        correction.pop('statement')
        correction.pop('report_type')
        correction.update(kind='correction', target_id='original', reason='Incorrect grading',
                          evaluation=event('x')['evaluation'], response='A rewritten learner answer')
        with self.assertRaises(StateError):
            self.store.record(correction)
        self.assertEqual(len(self.store.events()), 1)
        self.assertEqual(self.store.events()[0]['response'], 'Synthetic learner response')

    def test_repeated_application_cannot_claim_novelty(self):
        self.store.record(event('app', capability='application', novel=True))
        again = event('again', capability='application', novel=True)
        again['question']['id'] = 'app'
        with self.assertRaises(StateError):
            self.store.record(again)

    def test_invalid_evidence_rejected_without_writing(self):
        for change in ({'schema_version': 9}, {'id': '../escape'},
                       {'concept_ids': ['probability.expectation']}, {'response': ''},
                       {'timestamp': 'yesterday'}, {'concept_ids': [IDS[0], IDS[1]]}):
            value = event('invalid')
            value.update(change)
            with self.subTest(change=change), self.assertRaises(StateError):
                self.store.record(value)
        self.assertEqual(self.store.events(), [])

    def test_unrelated_concepts_never_inherit_competence(self):
        self.active('graph-theory.bfs')
        self.assertEqual(self.projection()['competency_state'], 'unknown')

    def test_synthetic_evidence_cannot_enter_personal_state(self):
        with self.assertRaises(StateError):
            Store(REPO / '.learn', allow_synthetic=True)
        ordinary = Store(self.root)
        with self.assertRaises(StateError):
            ordinary.record(event('synthetic'))

    def test_interrupted_projection_update_rebuilds_without_losing_evidence(self):
        with patch('scripts.learn_state.atomic_json', side_effect=OSError('simulated interruption')):
            with self.assertRaises(OSError):
                self.store.record(event('durable'))
        self.assertEqual(len(self.store.events()), 1)
        with self.assertRaises(StateError):
            self.store.validate()
        self.store.sync()
        self.assertTrue(self.store.validate()['valid'])

    def test_edited_projection_is_detected_and_repair_is_idempotent(self):
        self.store.record(event('record'))
        path = self.root / 'concepts' / (CONNECTIVITY + '.json')
        data = json.loads(path.read_text())
        data['competency_state'] = 'active'
        path.write_text(json.dumps(data))
        with self.assertRaises(StateError):
            self.store.validate()
        first = self.store.sync()
        self.assertEqual(first, self.store.sync())
        self.assertNotEqual(first[CONNECTIVITY]['competency_state'], 'active')

    def test_malformed_or_future_evidence_is_not_silently_replaced(self):
        self.store.record(event('record'))
        path = self.root / 'evidence/record.json'
        path.write_text('{broken')
        with self.assertRaises(StateError):
            self.store.sync()
        self.assertEqual(path.read_text(), '{broken')

    def test_session_resume_preserves_checkpoint_and_evidence(self):
        self.store.record(event('answer'))
        self.store.session({'schema_version': 1, 'id': 'session-1', 'mode': 'teaching',
                            'goal': 'Learn connectivity', 'evidence_refs': ['answer'],
                            'pending_question': None, 'next_action': 'Ask novel application'})
        fresh = Store(self.root, allow_synthetic=True)
        resumed = fresh.resume()
        self.assertEqual(resumed['evidence_count'], 1)
        self.assertEqual(resumed['latest_session']['next_action'], 'Ask novel application')
        self.assertEqual(resumed['concepts'], self.store.projections())

    def test_confidence_and_review_follow_repeated_independent_evidence(self):
        self.active()
        self.store.record(event('retrieval', session='session-2'))
        self.assertEqual(self.projection()['evidence_confidence'], 'high')
        self.assertIsNotNone(self.projection()['last_unaided_success_at'])

    def test_preferences_survive_projection_rebuild(self):
        self.store.sync()
        path = self.root / 'learner.json'
        data = json.loads(path.read_text())
        data['preferences'] = {'pace': 'slow'}
        path.write_text(json.dumps(data))
        self.store.sync()
        self.assertEqual(json.loads(path.read_text())['preferences'], {'pace': 'slow'})
