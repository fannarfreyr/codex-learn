# codex-learn

A Codex-native evidence-based tutor. See [PLANS.md](PLANS.md), [architecture](docs/architecture.md), and [milestones](docs/milestones.md).

Open this checkout in Codex. For example:

- “I have a BSc in Discrete Mathematics and Computer Science. Calibrate my graph-theory knowledge.”
- “Help me learn BFS shortest paths using my saved profile.”
- In a fresh chat on this same checkout: “Continue my learning from saved state.”

The tutor asks one question at a time and waits for your answer. Background creates exposure priors; actual responses support competence. Teaching and calibration update the same profile, and lesson plans distinguish skipping, checking, refreshing, and introducing prerequisites.

Personal `.learn/` is Git-ignored. Evidence is preserved; estimates are provisional. Persistence covers this local checkout, without synchronization, backup, or clean-clone continuity.

## Inspecting Local State

Python 3.10 or newer, standard library only:

```sh
python3 scripts/learn_state.py resume
python3 scripts/learn_state.py inspect
python3 scripts/learn_state.py plan graph-theory.bfs-shortest-paths
python3 scripts/learn_state.py validate
```

Each concept explains its evidence, confidence, misconceptions, and conflicts. The plan lists prerequisite actions and reasons. The tutor records observations with `record`, checkpoints with `session`, and selects diagnostics with `calibrate` and `next SESSION_ID`. These commands do not grade learner answers.

If derived records are stale after an interrupted save, `rebuild` restores them from evidence. Preserve malformed evidence for inspection; never edit projections to claim competence. See the [architecture](docs/architecture.md) for formats and correction rules.

## Development

Run the deterministic tests and whitespace check:

```sh
python3 -m unittest discover -s tests -v
git diff --check
```

Synthetic tests are not personal evidence. The MVP passes 56 deterministic tests and live validation across two Codex chats, including fresh-chat continuation. See [validation](docs/validation.md) and the [live evidence trace and corrected failure](docs/validation-live.md).
