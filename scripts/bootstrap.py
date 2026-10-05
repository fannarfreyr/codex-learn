"""Small explicit exposure mappings. These never establish competence."""

import json
from pathlib import Path
import re

try:
    from .learn_state import IDS, require
except ImportError:
    from learn_state import IDS, require


PATH = Path(__file__).resolve().parents[1] / 'competencies/graph-theory/background-mappings.json'


def normalize(text):
    return re.sub(r'[^a-z0-9]+', ' ', text.casefold()).strip()


def mappings(path=PATH):
    data = json.loads(Path(path).read_text())
    require(data.get('schema_version') == 1, 'Unsupported background mapping version')
    aliases = set()
    rule_ids = set()
    for rule in data['rules']:
        require(rule['id'] not in rule_ids, 'Duplicate background rule')
        rule_ids.add(rule['id'])
        require(all(c in IDS and v in {'low', 'medium', 'high'} for c, v in rule['exposure'].items()), 'Invalid exposure mapping')
        for alias in rule['aliases']:
            key = normalize(alias)
            require(key not in aliases, 'Ambiguous declaration alias')
            aliases.add(key)
    return data['rules']


def exposure(concept, events, rules=None):
    rules = mappings() if rules is None else rules
    candidates = []
    rank = {'low': 1, 'medium': 2, 'high': 3}
    for e in events:
        if e['kind'] == 'background_declaration':
            for rule in rules:
                if normalize(e['statement']) in {normalize(a) for a in rule['aliases']} and concept in rule['exposure']:
                    candidates.append((rule['exposure'][concept], e['id'], rule['id']))
    reports = [e for e in events if e['kind'] == 'self_report' and concept in e['concept_ids'] and e['report_type'] != 'skip']
    if reports:
        latest = reports[-1]
        direct = 'low' if latest['report_type'] == 'never_seen' else 'high'
        return direct, {'confidence': 'low', 'declaration_refs': [c[1] for c in candidates],
                        'self_report_refs': [latest['id']], 'mapping_rule_ids': [c[2] for c in candidates],
                        'rationale': 'Direct concept self-report updates exposure assumptions, not competence.'}
    if not candidates:
        return 'unknown', None
    return max(candidates, key=lambda c: rank[c[0]])[0], {
        'confidence': 'low', 'declaration_refs': list(dict.fromkeys(c[1] for c in candidates)),
        'mapping_rule_ids': list(dict.fromkeys(c[2] for c in candidates)),
        'rationale': 'Explicit background mapping suggests exposure only; it provides no competence evidence.'}
