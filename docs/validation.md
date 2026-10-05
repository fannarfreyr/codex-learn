# Validation Record

Scripted learners are synthetic examples, not statements about the repository owner. Deterministic tests alone do not establish Codex behavior. The required live checks have now passed in two actual chats; see [live results, evidence trace, and failures](validation-live.md). Earlier milestone entries below record validation at that stage.

## Milestone 1

Implemented teaching skill, stable-ID observation envelope, repository guidance, and ignored personal-state location. Python 3.13.3 is available. Official docs confirm discovery locations; installed-app skill loading was subsequently verified in the live check.

Manually inspected the scripted explanation of adjacency versus connectivity and application to another graph. Partial answers need a bridge; misconceptions need repair before another assessment. Fixture: tests/fixtures/milestone1-session.json.

Live learner and fresh-chat validation were pending at this stage and subsequently passed. No personal learner evidence was created.


Milestone 2: 20 tests pass. Manually executed a synthetic rusty-learner sequence in an isolated temporary directory and inspected its three evidence records. Result: rusty/moderate, with aided application and no active promotion. System and bundled Python lack PyYAML; the bundled skill validator cannot run without optional tooling. Frontmatter and reference paths inspected manually; application remains standard-library-only.


Milestone 3: graph traversal and 14 prompts inspected manually. BFS layers, deterministic alphabetical DFS order, and spanning-tree examples checked against the concrete edge sets. 24 tests pass; no learner evidence migrated.


Milestone 4: manually initialized a synthetic degree-only profile in temporary state. Three medium exposure priors, four unknown exposure priors, seven unknown competence projections with confidence none. All 30 tests pass.

## Milestone 5

40 tests pass. In an isolated synthetic state, declared the example BSc, started at core connectivity, and recorded: “Connected means every vertex has an edge directly to every other vertex.” Evaluation identified the adjacency/connectivity misconception. Selection redirected to foundation terminology, with zero active concepts. Running selection again without answering returned the same pending question. Evidence integrity passed.

The calibration skill is present. Its frontmatter and shared reference were inspected; the bundled validator still cannot import PyYAML. Live question presentation, actual learner turn-taking, and fresh-chat recovery subsequently passed.

## Milestone 6

51 tests pass. `python3 tests/manual_mvp.py --state-dir /private/tmp/codex-learn-mvp-validation-20261005` created ten explicitly synthetic observations, without personal learner state. Original answers and private rubrics were manually reviewed against the concrete graphs.

The diagnostic moved from core connectivity to application, then checked the unverified terminology prerequisite. Before a BFS refresher, the shortest-path plan skipped terminology/connectivity, refreshed BFS, and introduced the target. Fresh unaided explanation and a different six-vertex application changed BFS to skip. The target remains unknown with its explanation question saved as pending. The state integrity check passed.

The runner is a reproducible fixture preparation tool, not a simulated Codex conversation. Automated subprocess resumption and plan-rebuild tests pass; live chat turn-taking and fresh-chat continuation subsequently passed. The four manual procedures are in `tests/scenarios/`.

## Completion Audit

56 deterministic tests pass, and `git diff --check` is clean. Both live chats completed and ended with saved checkpoints. All 17 observations are synthetic; personal `.learn/` remains absent.

| Required behavior | Current evidence |
| --- | --- |
| Background is a prior, never mastery | Mapping tests; live declaration and corrected sentence-form alias |
| Adaptive questioning | Selection tests; live misconception redirected to foundation, success returned to application |
| Inspectable, evidence-backed estimates | Immutable JSON observations, scoped rubrics, correction/rebuild tests, live evidence trace |
| Different gaps produce different teaching | Planning tests; live connectivity repair and concise rusty-BFS reconstruction |
| Ordinary teaching refines the calibration model | Live records 10–17 update the shared profile and persisted plan |
| Fresh-chat continuity | Second actual chat recovered the target and skipped supported prerequisites with no prior answers in its prompt |
| Conservative uncertainty | Hinted success stayed rusty; untested trees, DFS, and spanning trees stayed unknown |
| Stable IDs and controlled writes | Early-record compatibility, immutable-correction, conflicting-ID, novelty, and checkpoint-integrity tests |
| Scope and isolation | Seven graph nodes; standard-library utility; no personal state or deferred infrastructure created |

The open-ended evaluations and concrete graph answers were inspected manually. The [live record](validation-live.md) preserves chat IDs, observed behavior, evidence IDs, the mapping failure and correction, and fixture locations for inspection or removal.
