import copy
from pathlib import Path
import tempfile
import unittest

from scripts.learn_state import SCOPES, Store


CONNECTIVITY = 'graph-theory.connectivity'


def event(ident, concept=CONNECTIVITY, capability='explanation', outcome='correct',
          assistance='none', novel=False, session='session-1', scope=None):
    return {
        'schema_version': 1, 'id': ident, 'kind': 'assessment',
        'timestamp': '2026-10-05T13:00:00Z', 'session_id': session,
        'concept_ids': [concept], 'provenance': {'source': 'synthetic', 'surface': 'test-fixture'},
        'question': {'id': ident, 'text': 'Synthetic diagnostic question',
                     'capability': capability, 'scope': scope or SCOPES[concept], 'novel': novel},
        'response': 'Synthetic learner response', 'assistance': assistance,
        'rubric': {'criteria': ['Scoped explanation or application criterion']},
        'evaluation': {'outcome': outcome, 'rationale': 'Synthetic tutor evaluation against the criterion.', 'misconceptions': []},
    }


def report(ident, report_type, concept=CONNECTIVITY):
    value = event(ident, concept)
    for key in ('question', 'response', 'assistance', 'rubric', 'evaluation'):
        value.pop(key)
    value.update(kind='self_report', report_type=report_type, statement='Synthetic learning-history report')
    return value


def declaration(ident='degree-1', category='bsc-discrete-math-cs'):
    value = report(ident, 'studied_before')
    value.pop('report_type')
    value.update(kind='background_declaration', concept_ids=[],
                 statement='BSc in Discrete Mathematics and Computer Science', background_category=category)
    return value


class StateCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.store = Store(self.root, allow_synthetic=True)

    def active(self, concept=CONNECTIVITY, prefix='pass'):
        self.store.record(event(prefix + '-explain', concept))
        self.store.record(event(prefix + '-apply', concept, 'application', novel=True))

    def projection(self, concept=CONNECTIVITY):
        return self.store.projections()[concept]
