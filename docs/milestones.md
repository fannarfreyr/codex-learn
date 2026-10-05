# Implementation Milestones

## Scope and Execution Order

Follow [PLANS.md](../PLANS.md) and the [architecture](architecture.md). The six-milestone MVP covers one learner and seven graph-theory concepts. Milestone 1 is independently usable; the full MVP validates background bootstrapping, calibration, personalized teaching, and resumption.

Evidence is authoritative. Categorical states remain provisional derived projections. Stable final concept IDs are used from Milestone 1. Persistence is limited to fresh Codex chats on the same local checkout, with `.learn/` Git-ignored.

## Milestone 1 — Minimum Viable Tutor

### Objective

Validate one concept's teaching, assessment, repair, persistence, and resumption.

### Files and Components

Repository guidance, README, teaching skill, ignore rules, session/evidence records, and manual scenarios.

### Data Structures or Formats

Versioned observations with question, response, assistance, outcome, checkpoint, and final stable concept IDs, including `graph-theory.terminology` and `graph-theory.connectivity`.

### Implementation Tasks

Accept a goal; ask up to five relevant probes; present a short prerequisite chain; teach one unresolved concept; distinguish correct, partial, and incorrect responses; repair and reassess; save meaningful observations. Use final IDs without introducing full graph traversal or temporary identifiers.

### Acceptance Criteria

Actual answers change tutor behavior. Advancement requires explanation and novel application. Saved evidence survives a fresh chat in the same checkout. Introducing the later graph requires no concept-ID migration.

### Automated Tests

Fixture validity and record-format checks. No automated teaching grader is required.

### Manual Validation Scenario

Teach connectivity using terminology as a prerequisite. Exercise partial and incorrect answers, repair, stop, and resume in the same checkout.

### Dependencies

Verify instruction loading, skill selection, turn-taking, and local file access.

### Deferred Decisions

Credential interpretation, complete projections, shared graph traversal, explicit calibration, agents, hooks, MCP, UI, and databases.

### Risks or Uncertainties

Subjective evaluation and instruction-following errors. Keep evidence visible and treat this as an experimental tutor increment.

## Milestone 2 — Stable Learner-State Representation

### Objective

Establish shared provisional projections and controlled evidence-backed updates.

### Files and Components

State utility, format reference, teaching integration, fixtures, and state tests.

### Data Structures or Formats

The approved schema: authoritative evidence records, provisional states/confidence, capability summaries, misconceptions, conflicts, and interaction/review timestamps.

### Implementation Tasks

Implement record creation, validation, idempotency, projection updates, correction handling, and rebuild. Prevent credential/self-report-only promotion to active. Record incidental demonstrated knowledge through the same path.

### Acceptance Criteria

Every projection explains its basis. Evidence survives updates. Aided answers cannot establish active competence. Weak or conflicting evidence remains uncertain. Projections can be rebuilt from the evidence log.

### Automated Tests

Missing references, unsupported transitions, conflicting IDs, unsupported versions, correction chains, interrupted updates, and deterministic rebuild.

### Manual Validation Scenario

Record prior study, hinted success, and failed unaided explanation. Inspect the rusty projection and its supporting records.

### Dependencies

Milestone 1 and its stable observation identities.

### Deferred Decisions

Separate learning-history/readiness/retrieval dimensions, numerical scores, decay formulas, scheduled review, multi-user storage, synchronization, and extensive migration machinery.

### Risks or Uncertainties

Categories may oversimplify competence. Preserve scope, confidence, and rationale; do not silently promote ambiguous records.

## Milestone 3 — Small Competency Ontology

### Objective

Reuse one tiny graph for diagnostics and teaching.

### Files and Components

Graph-theory graph, prompt/rubric bank, graph validation/traversal, and tests.

### Data Structures or Formats

Stable IDs already used in Milestone 1, parent area, scoped objectives, prerequisite edges, graph version, and prompt metadata.

### Implementation Tasks

Author the seven approved concepts. Validate references and cycles. Support ancestor traversal and ordering. Associate prompts with concepts and capabilities.

### Acceptance Criteria

BFS shortest paths resolves to the correct chain. Hierarchy membership is distinct from prerequisites. Untested neighbors remain unknown. Earlier learner records resolve without renaming.

### Automated Tests

Duplicate IDs, missing nodes, cycles, deterministic traversal, grouping separation, version mismatches, and compatibility with Milestone 1 evidence.

### Manual Validation Scenario

Select BFS shortest paths and inspect its prerequisite chain and diagnostic prompts.

### Dependencies

Milestone 2.

### Deferred Decisions

Other domains, universal deduplication, graph editors, ontology databases, and broad curriculum coverage.

### Risks or Uncertainties

Poor edges create unnecessary lessons. Review prerequisites against scoped objectives and avoid hidden programming requirements.

## Milestone 4 — Background-Based Profile Bootstrapping

### Objective

Turn declared background into conservative exposure priors.

### Files and Components

Background mappings, onboarding instructions, state integration, and mapping tests.

### Data Structures or Formats

Background declarations and explicit mappings to concept IDs and exposure categories.

### Implementation Tasks

Preserve original wording. Recognize only supported mappings. Show assumptions. Merge priors without replacing assessments. Record unmatched declarations without inventing concepts.

### Acceptance Criteria

Credentials never create active competence. Exposure influences diagnostic starting level. Observed gaps override presumed readiness. Unmapped concepts remain unknown.

### Automated Tests

Credential-only profiles, unmatched backgrounds, repeated onboarding, conflicting declarations, and preservation of demonstrated competence.

### Manual Validation Scenario

Declare a BSc in Discrete Mathematics and CS, inspect priors, then fail terminology and confirm diagnostic difficulty drops.

### Dependencies

Milestones 2–3.

### Deferred Decisions

Curriculum scraping, broad credential interpretation, institutional equivalence, transcript ingestion, and research agents.

### Risks or Uncertainties

Degree content varies. Map the example degree only to medium expected exposure in terminology, connectivity, and trees. Leave the remaining concepts unmapped without more specific support.

Explicit graph-theory course completion may create high expected exposure to those foundations, with low prior confidence. It still provides no competence evidence. Failed diagnostics revise current competence and questioning difficulty; they do not prove absence of historical exposure.

## Milestone 5 — Adaptive Competency Calibration

### Objective

Locate a useful competence boundary through short explicit calibration.

### Files and Components

Calibration skill, prompt-selection heuristics, checkpoints, and policy tests.

### Data Structures or Formats

Calibration scope, pending prompt, tested capabilities, selection rationale, and stop reason.

### Implementation Tasks

Start at foundation without usable priors or at core with medium/high mapped exposure. Move upward after unaided success. Inspect prerequisites after gaps. Check explanation after recognition-only success. Persist meaningful observations.

### Acceptance Criteria

Responses change question order. Hinted and unaided success differ. Forgetting reports remain visible. All-correct runs may finish without requiring failure.

### Automated Tests

Synthetic sequences for upward movement, prerequisite redirection, aided answers, skips, repetition, and stopping. Test selection policy rather than LLM grading.

### Manual Validation Scenario

Run credential-overestimation, rusty-learner, and strong-knowledge scenarios. Compare questions and provisional projections.

### Dependencies

Milestones 2–4.

### Deferred Decisions

Bayesian tracing, IRT, information-gain optimization, probabilities, and exhaustive examination.

### Risks or Uncertainties

Fatigue and ambiguous questions. Default to eight learner-response turns, stopping earlier when a useful next action is clear, on learner request, or when no informative prompt remains. Budget-limited conclusions remain provisional.

Choose deterministically among untested eligible prompts. Require direct evidence before crediting each concept. Explicit calibration diagnoses first and offers teaching afterward.

## Milestone 6 — Dependency-Aware Personalized Lesson Planning

### Objective

Combine the graph and profile to decide what to skip, refresh, verify, or teach.

### Files and Components

Teaching skill, planning utility, persisted plan, planning tests, and end-to-end scenarios.

### Data Structures or Formats

Prerequisite action, evidence references, rationale, target, graph version, and checkpoint.

### Implementation Tasks

Traverse target-relevant prerequisites. Order them. Choose actions from current projections and their evidence. Teach unresolved concepts. Update the same learner model after new observations.

### Acceptance Criteria

Supported active prerequisites are skipped. Rusty concepts receive refreshers. Unknown/never-learned concepts receive introductory teaching. Conflicted projections receive targeted checks.

### Automated Tests

Action selection, ordering, scope mismatch, conflicts, unrelated concepts, and checkpoint reconstruction.

### Manual Validation Scenario

After calibration, request BFS shortest paths. Inspect personalized actions, complete a repair, and resume in another chat on the same checkout.

### Dependencies

Milestones 1–5.

### Deferred Decisions

Global curriculum optimization, multiple goals, broad ontology expansion, agents, hooks, MCP, and packaging.

### Risks or Uncertainties

Skipping an essential prerequisite incorrectly. Exposure priors never justify prerequisite skipping. Require supported active competence with moderate/high confidence and no unresolved relevant conflict.

| Projection | Default teaching action |
| --- | --- |
| Active with sufficient scoped evidence | Skip instruction |
| Active but conflicted or insufficiently scoped | Verify briefly |
| Rusty | Concise refresher, then unaided check |
| Forgotten | Short reconstruction attempt; expand if needed |
| Exposed/developing | Bridge from demonstrated capabilities |
| Unknown/never learned | Introductory teaching at the relevant foundation |

## MVP Boundary

Complete all six milestones for one learner in Codex desktop, seven graph-theory concepts, a tiny explicit background mapping, one teaching skill, one calibration skill, a small Python standard-library state utility, JSON persistence in one local checkout, and human pedagogical evaluation.

Milestone 1 remains independently usable. The full MVP requires the background-to-calibration-to-teaching-to-resumption demonstration.

## End-to-End Validation Procedure

1. Start with empty `.learn/` in the normal local checkout.
2. Declare the example BSc background.
3. Inspect exposure priors; competence must remain unknown.
4. Request graph-theory calibration.
5. Supply unaided successes, partial answers, hinted success, and self-report.
6. Confirm selection adapts instead of following a fixed question sequence.
7. Inspect preserved evidence and provisional projections; each estimate must explain its basis.
8. Request BFS shortest paths.
9. Inspect a plan that skips demonstrated foundations, refreshes a rusty prerequisite, and teaches an unresolved concept.
10. Demonstrate understanding through explanation and novel application.
11. End the chat and start a fresh Codex chat on the same repository checkout.
12. Recover evidence, relevant projections, and checkpoint without repeating onboarding or full calibration.

## Required Evaluation Scenarios

| Scenario | Required result |
| --- | --- |
| A: Credential overestimation | No active concepts from credentials; failed basics lower current readiness; diagnostics and teaching return to foundations |
| B: Rusty learner | Prior study plus hinted success and failed unaided explanation yields a qualified rusty/forgotten projection; concise refresh; no unsupported active promotion |
| C: Strong prior knowledge | Relevant unaided explanations/applications skip elementary instruction and move diagnostics toward harder or neighboring unresolved concepts |
| D: Persistence | A fresh chat on the same checkout recovers evidence; supported active prerequisites remain usable; unresolved concepts remain unresolved |

Also validate skips, unmatched backgrounds, mistaken prerequisite inference, contradictions, evaluation corrections, interrupted saves, and unrelated maintenance requests.

Automated tests validate deterministic behavior and record integrity. Human inspection assesses question quality, grading, explanations, and whether categories help learning.

Do not add clean-clone, cross-machine, synchronization, backup, or multi-device acceptance tests.

## Deferred Extensions

Researcher and visualization agents, automated hooks/session logging, structured quiz tools, MCP learning-tools server, larger competency libraries, broader evaluation infrastructure, packaging, distribution, and plugin architecture remain deferred until MVP evidence justifies them.

Retain the previous hook entry condition: repeated missed checkpoints after improving instructions. Require a demonstrated limitation before MCP. Neither is part of the six-milestone MVP.

## Implementation Discoveries

- Milestone 1 uses final concept IDs and schema version 1 from the first observation. Deterministic fixture validation passed; live behavioral gates subsequently passed and are tracked in [validation notes](validation.md). The sandbox protects `.agents/`, so creating skills required its explicit write approval.
- Milestone 2: 20 deterministic tests passed. Manual synthetic prior-study + unaided failure + hinted application yields rusty, not active. Novelty and exact scope must be explicit to prevent recognition or narrow checks from unlocking prerequisites.
- Milestone 3: 24 tests passed. Manually traced terminology → connectivity → BFS → BFS shortest paths. The 14-prompt bank covers explanation and application for each concept. Grouping is separate from prerequisite edges.
- Milestone 4: manually inspected BSc priors and confirmed no competence promotion. 30 tests passed, including later contradiction, unmatched degree, course exposure, and preservation of existing evidence.
- Milestone 5: 40 tests passed at this stage, including upward movement, prerequisite redirection, skips, aided answers, bounded stopping, and holding an unanswered question. Manually recorded a connectivity misconception after the example degree and observed a foundation terminology question next. Codex conversational behavior subsequently passed live validation.
- Milestone 6: 51 tests passed at this stage. Scripted manual validation preserves ten identifiable observations in isolated state. Its plan changes from skip/skip/refresh/teach to skip/skip/skip/teach after new BFS evidence. A separate Python process recovers state and answered checkpoints; actual fresh Codex chat validation subsequently passed.

## Final Validation Status

All six increments pass their deterministic checks and required manual scenarios. The final suite contains 56 passing tests. Live validation across two Codex chats preserved 17 synthetic evidence records, differentiated partial/rusty/active/unknown knowledge, repaired a prerequisite, and resumed the target from files without onboarding. The fresh chat added new evidence to the same model and left untested concepts unknown.

See [live results and the corrected background-alias failure](validation-live.md). Deferred decisions remain deferred; this validation does not establish broad grading reliability or curriculum coverage.
