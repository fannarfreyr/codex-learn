# Evidence-Based Codex Learning System Plan

## Execution Objective

Implement the six-milestone MVP for one learner and seven graph-theory concepts, then demonstrate conservative background bootstrapping, adaptive calibration, evidence-based teaching, and continuity across fresh Codex chats using the same local repository checkout.

This is the approved implementation plan, incorporating the three final clarifications. It replaces the earlier five-milestone plan. Saving these documents does not begin implementation or authorize additional scope.

## Planning Documents

- [Architecture](docs/architecture.md): learner model, schema, evidence rules, mutation controls, repository structure, competency graph, and Codex capability checks.
- [Milestones](docs/milestones.md): six usable increments, dependencies, acceptance criteria, validation procedures, and deferred extensions.

## Agreed Defaults

| Decision | MVP behavior |
| --- | --- |
| Learners | One learner; validate the MVP in graph theory |
| Primary surface | Codex desktop app; keep instructions portable |
| Active work | One learning goal and one state-writing tutor |
| Interaction | Conversational assessments; wait for actual learner responses |
| Progression | Present the learning plan and begin without repeated approval checkpoints |
| Advancement evidence | Unaided explanation or derivation plus novel application |
| Storage | JSON records in local, Git-ignored `.learn/`; Markdown instructions and documentation |
| Persistence | Fresh Codex chats using the same local repository checkout |
| Historical authority | Preserved evidence log, including corrections |
| Competency states | Provisional derived projections over evidence |
| Background mapping | Small explicit rules producing conservative exposure priors |

## Core Learning Loop

1. Determine what the learner wants to learn.
2. Probe relevant existing knowledge.
3. Identify prerequisite concepts.
4. Construct a dependency-aware learning path.
5. Teach one unresolved concept at a time.
6. Test understanding through actual learner responses.
7. Repair misunderstandings and reassess.
8. Persist evidence and update provisional projections and checkpoints.

Background declarations seed exposure priors. Explicit calibration gathers observations. Normal teaching contributes further evidence to the same learner model. No stage makes the profile permanently complete.

## Implementation Sequence

| Milestone | Usable result | Dependency |
| --- | --- | --- |
| 1. Minimum viable tutor | Teach, assess, repair, save, and resume using stable concept IDs | Verify essential local capabilities |
| 2. Stable learner-state representation | Controlled evidence-backed mutations and rebuildable projections | Milestone 1 |
| 3. Small competency ontology | Seven concepts and shared traversal for diagnostics and teaching | Milestone 2 |
| 4. Background-based profile bootstrapping | Inspectable exposure priors without credential-based mastery | Milestones 2–3 |
| 5. Adaptive competency calibration | Short response-dependent diagnostics | Milestones 2–4 |
| 6. Dependency-aware personalized lesson planning | Skip, refresh, verify, or teach from graph and evidence | Milestones 1–5 |

Milestone 1 is independently useful. The full MVP completes all six milestones and passes the background-to-calibration-to-teaching-to-resumption demonstration.

## Changes from the Previous Plan

Preserve the single-learner, desktop-first approach, local JSON storage, conversational assessments, bounded diagnostics, evidence requirements for advancement, checkpointing, and single-writer ownership.

Replace the previous four-state summary with the richer provisional learner model. Replace session records as primary historical authority with independent evidence records referenced by sessions. Replace plan-specific prerequisite definitions with a shared competency graph. Replace the five-milestone sequence and early release boundary with the six-milestone MVP.

Postpone researcher and visualization agents until learner-model validation. Keep hooks, MCP, databases, custom UI, structured quiz tools, larger competency libraries, packaging, and plugin distribution deferred.

Retain the reference project's emphasis on prerequisites, motivated explanations, and assessment without depending on its pi extensions. [Reference repository](https://github.com/amosblomqvist/learn)

## Final Clarifications and Scope Boundary

- The evidence log remains authoritative. States, confidence, exposure priors, and capability summaries are provisional projections. Defer deciding whether learning history, current readiness, and retrieval condition need separate dimensions until MVP evaluation supports that change.
- Milestone 1 uses final IDs such as `graph-theory.terminology` and `graph-theory.connectivity`. Do not introduce temporary identifiers or migrations merely because graph traversal arrives in Milestone 3.
- MVP persistence means continuity across fresh Codex chats on the same local repository checkout. `.learn/` remains Git-ignored. Cross-machine persistence, clean-clone persistence, cloud synchronization, backup, and multi-device learner profiles are out of scope.

## Recommended MVP Boundary

One learner, seven graph-theory concepts, a tiny explicit background mapping, one teaching skill, one calibration skill, a small Python standard-library state utility, JSON persistence, and human pedagogical evaluation supported by focused deterministic tests.

This plan defines the approved implementation scope; the progress notes below describe work already present in the checkout. Verify actual client behavior before depending on documented capabilities. Future scope changes must be justified by evidence from this MVP.

## Implementation Progress

- Milestone 1: teaching skill, stable-ID observation envelope, contributor guidance, ignored personal-state path, and synthetic fixture implemented. Fixture test and ignore check pass. Scripted explanation/application manually inspected; live skill loading and fresh-chat behavior were subsequently verified in final validation.
- Skill validation discovery: system Python lacks PyYAML required by the bundled validator; no application dependency was added.
- Milestone 2: deterministic validation passed with 20 total tests. Synthetic rusty-learner observations were manually inspected; authoritative responses and evaluations remain separate. State utility supports immutable IDs, explicit corrections, projection rebuild, and scoped activation. Live-chat gates were subsequently verified in final validation.
- Milestone 3: validation passed with 24 total tests. BFS-shortest-path prerequisite traversal and bank coverage were manually inspected; all seven early IDs are retained.
- Milestone 4: validation passed with 30 total tests. Manual degree-only initialization leaves all seven competence states unknown; three foundations receive medium exposure priors, and the other four remain exposure-unknown.
- Milestone 5: 40 deterministic tests passed at this stage. The calibration skill uses persisted, response-dependent selection. Manual synthetic credential overestimation redirects connectivity to terminology without promoting competence. Pending unanswered questions remain unchanged. Live conversational validation subsequently passed.
- Milestone 6: 51 deterministic tests passed at this stage. The manual synthetic trajectory skips demonstrated terminology/connectivity, refreshes rusty BFS, and then skips BFS after fresh unaided evidence. Actual fresh Codex chat validation subsequently passed.

## Final MVP Validation

All six milestones are implemented and validated. The final suite passes 56 standard-library tests, including early-ID compatibility, immutable corrections, adaptive selection, evidence-derived lesson actions, and checkpoint recovery. Two actual Codex chats demonstrated the background-to-calibration-to-teaching-to-fresh-chat loop, with all 17 live-test observations explicitly synthetic and personal `.learn/` untouched.

See [validation results](docs/validation.md) and [live behavior, evidence trace, and failures](docs/validation-live.md). The observed sentence-form background alias gap was corrected without expanding credential interpretation. The deferred architecture decisions and seven-concept boundary remain unchanged.

## Approved v0.1.1 Documentation Release

Document and improve discoverability of the implemented v0.1 system, without new learning behavior, revised state semantics, skill changes, or changes to calibration/teaching logic.

Deliver a concise README, one canonical user guide with a capability reference and ten required fields per workflow, learner-model/calibration/teaching/resumption guidance, troubleshooting, and AGENTS.md documentation links. Keep CLI/operator material secondary to natural-language examples and document only actual options. Preserve the six-milestone MVP history above.

Validation requires a fresh Codex chat whose sole initial prompt is “What can I do with codex-learn and how do I get started?”, followed by a guide workflow performed exactly as written in isolated synthetic state. Run existing tests, check links and whitespace, verify implementation files and personal state are unchanged, and record any runtime bugs separately rather than fixing them in this release.

Implementation discoveries: exact background aliases, terminal calibration stop semantics, finite assessed-question reuse, evaluation-only corrections, and the write effects of resume/rebuild are now explicit in the guide. No functionality was added to accommodate the documentation. See the [v0.1.1 release record](docs/releases/v0.1.1.md) for source inventory and validation status. Tagging/publishing is not part of implementation.

Validation completed on 2026-10-21: a fresh chat discovered README/user-guide documentation from the exact orientation question and accurately described v0.1 without creating state. The guide's six-message walkthrough then ran verbatim in that chat; declaration, calibration, skip, stop, and inspection behaved as documented. Its two evidence records are synthetic, all seven competence estimates remain unknown, and state validation passes. All 56 existing tests pass; implementation hashes and personal-state isolation are unchanged.

An additional documentation clarification distinguishes self-report skips consumed per run from assessment question IDs excluded across runs. No runtime defect was discovered in the exercised workflow and no learning implementation was changed. New live validation covers the documented walkthrough, not every historical v0.1 workflow; remaining interface limitations and the retained chat/evidence references are in the release record. The files are ready to commit before a v0.1.1 tag is created.

## v0.1.2 Broad Competency Calibration

The [v0.1.2 plan](docs/releases/v0.1.2-plan.md) defines broad survey calibration and target-specific focused calibration, an inspectable evidence-based coverage policy, bounded resumable sessions, backward-compatible checkpoints, acceptance scenarios, and required documentation changes.

Survey calibration is now the default for whole-area requests without letting a foundational gap terminate the survey. Existing evidence, conservative projections, stable concept IDs, and the seven-concept scope remain intact. Implementation, all 78 standard-library tests, scripted walkthroughs, and live fresh-chat acceptance pass. See the [v0.1.2 validation record](docs/releases/v0.1.2.md) for results and limitations.
