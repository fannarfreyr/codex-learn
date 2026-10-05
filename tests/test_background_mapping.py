from helpers import StateCase, declaration, event, report
from scripts.bootstrap import exposure


class BackgroundTests(StateCase):
    def test_degree_only_changes_exposure_not_competence(self):
        self.store.record(declaration())
        p = self.projection()
        self.assertEqual(p['expected_exposure'], 'medium')
        self.assertEqual(p['competency_state'], 'unknown')
        self.assertEqual(p['evidence_confidence'], 'none')
        self.assertEqual(p['exposure_prior']['confidence'], 'low')
        self.assertEqual(p['estimate_basis_refs'], [])
        self.assertEqual(self.projection('graph-theory.bfs')['expected_exposure'], 'unknown')

    def test_unmatched_declaration_remains_unknown(self):
        d = declaration()
        d['statement'] = 'MSc in AI at an unspecified university'
        self.store.record(d)
        self.assertEqual(self.projection()['expected_exposure'], 'unknown')

    def test_observed_sentence_form_maps_without_guessing_other_credentials(self):
        d = declaration()
        d['statement'] = 'I have a BSc in Discrete Mathematics and Computer Science.'
        self.store.record(d)
        self.assertEqual(self.projection()['expected_exposure'], 'medium')
        self.assertEqual(self.projection()['competency_state'], 'unknown')
        self.assertEqual(self.store.events()[0]['statement'], d['statement'])

    def test_repeated_background_does_not_erase_demonstration(self):
        self.active()
        self.store.record(declaration())
        self.assertEqual(self.projection()['competency_state'], 'active')
        self.assertEqual(len(self.projection()['estimate_basis_refs']), 2)

    def test_credential_overestimation_is_corrected_by_observation(self):
        self.store.record(declaration())
        self.store.record(event('basic-failure', outcome='incorrect'))
        p = self.projection()
        self.assertEqual(p['competency_state'], 'developing')
        self.assertEqual(p['expected_exposure'], 'medium')
        self.assertNotEqual(p['evidence_confidence'], 'high')

    def test_never_seen_report_revises_exposure_not_historical_declaration(self):
        self.store.record(declaration())
        self.store.record(report('never', 'never_seen'))
        p = self.projection()
        self.assertEqual(p['expected_exposure'], 'low')
        self.assertEqual(p['exposure_prior']['declaration_refs'], ['degree-1'])
        self.assertEqual(self.store.events()[0]['statement'], 'BSc in Discrete Mathematics and Computer Science')

    def test_specific_course_has_high_exposure_but_no_active_state(self):
        d = declaration()
        d['statement'] = 'Completed a graph theory course'
        self.store.record(d)
        self.assertEqual(self.projection()['expected_exposure'], 'high')
        self.assertEqual(self.projection()['competency_state'], 'unknown')
