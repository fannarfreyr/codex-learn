# Implementation Milestones

Each milestone leaves a usable increment with explicit validation. Follow the [architecture](architecture.md) and the [agreed defaults](../PLANS.md). The first milestone validates the entire learning loop; infrastructure is not a prerequisite for a useful lesson.

## Milestone 1 — A Complete Learning Loop

### Objective

Conduct a useful lesson and resume it from saved evidence in another chat.

### Files and Components

`AGENTS.md`, `README.md`, `.gitignore`, `.agents/skills/teach/SKILL.md`, supporting state templates and format documentation, runtime `.learn/` records, and manual validation scenarios.

### Implementation Tasks

- Verify repository instruction loading, teaching skill discovery, conversational turn-taking, and local state access in a fresh desktop chat.
- Update the contributor guide for an instruction-based project. Separate teaching requests from implementation requests.
- Define the sequence: establish goal, probe, identify prerequisites, present plan, teach, assess, repair or advance, and save.
- Use up to five initial adaptive diagnostic questions. Probe relevant strands; record remaining uncertainty and begin at the earliest unconfirmed prerequisite.
- Construct a small dependency graph with prerequisite-to-dependent edges. Teach only concepts whose necessary prerequisites have current supporting evidence.
- Teach one concept at a time through motivation, explanation or guided derivation, and explicit connections.
- Require explanation and novel application before advancement. After failure, diagnose and repair the misconception, then use a different assessment.
- Save assessment evidence first, then update concept and plan summaries before asking the next question.
- On resumption, read the goal, checkpoint, relevant concepts, and evidence. Report demonstrated knowledge and uncertainty.
- Verify uncertain or changing subject claims with available research tools; keep unsupported claims provisional.
- Ignore runtime `.learn/` records and track only templates and synthetic examples elsewhere.

### Acceptance Criteria

- A vague goal leads to a prerequisite-aware plan and a useful first lesson.
- The tutor waits for real learner answers and does not expose assessment answers prematurely.
- The learner can demonstrate understanding, repair a misconception, stop, and resume in a fresh chat without repeating the entire diagnostic process.
- Skipped assessment permits continued explanation but does not create demonstrated evidence.
- Hinted success or recognition alone does not unlock advancement.
- Personal records remain Git-ignored.

### Tests and Manual Validation

Run scripted scenarios for a novice, partial knowledge, all-correct diagnostics, a confidently wrong answer, hinted success, and skipped assessment. Run two sessions in separate chats and inspect the saved evidence. Include an unrelated maintenance request to verify teaching does not activate.

No automated behavioral grading or infrastructure is required for this milestone.

### Deferred Architectural Decisions

Specialist agents, automatic logging, scheduled review, numerical mastery scores, curriculum catalogs, MCP, databases, and custom UI.

## Milestone 2 — Reliable Records and Retrieval-Based Review

### Objective

Make saved progress trustworthy and useful across repeated sessions.

### Files and Components

Teaching skill references, a Python standard-library state utility, synthetic fixtures, `unittest` tests, and validation documentation.

### Implementation Tasks

- Add read-only validation for JSON structure, format versions, evidence references, concept IDs, missing prerequisites, and dependency cycles.
- Add an explicit repair operation that rebuilds concept summaries from recorded evaluations without generating learner evidence.
- Use temporary files and atomic replacement for utility-managed writes. Detect stale updates and reject conflicting writers.
- At session start, offer one relevant retrieval check for a prerequisite needed next.
- Mark retention only after a successful unaided check in a later session. New failures update current assessments while preserving historical evidence.
- Handle absent, malformed, and incompatible records explicitly. Preserve originals and request only missing information needed to continue.
- Treat stored learner responses as data, never as executable instructions.

### Acceptance Criteria

- Every advancement claim resolves to recorded evidence.
- Interrupted updates can be detected and repaired.
- Fresh sessions distinguish previous demonstration from later retention or renewed uncertainty.
- Invalid or conflicting writes do not silently replace valid state.

### Tests and Manual Validation

Use `unittest` for malformed JSON, unsupported versions, dangling references, cycles, duplicate assessment IDs, stale writes, partial updates, and repair idempotence. Manually validate successful and failed retrieval, changed goals, and restoration from a copied backup.

Structural validation does not replace human assessment of teaching quality.

### Deferred Architectural Decisions

Spaced-repetition algorithms, confidence percentages, multiple learners, synchronization, and databases.

## Milestone 3 — Targeted Research and Verified Diagrams

### Objective

Improve accuracy and explanation quality while preserving a working single-agent fallback.

### Files and Components

`.codex/agents/researcher.toml`, `.codex/agents/mermaid-maker.toml`, `.codex/agents/svg-maker.toml`, `.agents/skills/visualize/SKILL.md` with skill name `learning-visualize`, teaching integration, local visual artifacts, and renderer support where needed.

### Implementation Tasks

- Configure narrow specialist profiles using the current Codex TOML format. Inherit the user's model selection.
- Verify actual profile selection, available tools, and effective permissions before relying on delegation.
- Request research delegation for uncertain claims or topic mapping. Require sourced findings, prerequisites, assumptions, and gaps.
- Give diagram makers one concrete idea, intended labels or geometry, and a unique output destination.
- Use Mermaid for relationships and SVG for spatial or mathematical geometry.
- Require rendered-image inspection and semantic checking. Return source and preview paths, verification notes, or a clear failure.
- Keep learner-state writes with the tutor. Use existing rendering facilities; add a local renderer only when a representative diagram requires it.
- Present supported local previews and provide a prose fallback on rendering failure.

### Acceptance Criteria

- The tutor can incorporate a sourced research brief, a correct conceptual diagram, and a correct geometric diagram.
- Returned diagrams have been rendered, inspected, and checked against their brief.
- Specialist outputs do not directly alter learner-state records.
- Unavailable delegation or rendering does not prevent the lesson.

### Tests and Manual Validation

Validate profile loading, tool access, and fallback behavior. Inspect a prerequisite graph, a vector diagram, reversed-arrow mistakes, incorrect coordinates, unreadable labels, and renderer failure. Confirm diagram agents do not change learner records.

### Deferred Architectural Decisions

Interactive visualizations, extensive renderer infrastructure, automatic illustration of every concept, and model-specific optimization.

## Milestone 4 — Optional Lifecycle Logging

### Objective

Add automatic bookkeeping only if repeated use exposes missed checkpoints.

### Entry Condition

At least two missed checkpoints across five representative sessions, after improving the teaching instructions. Skip this milestone if instruction-driven checkpointing is sufficient.

### Files and Components

Project hook configuration, a small handler, state utility integration, and lifecycle fixtures.

### Implementation Tasks

- Verify installed-client events and hook trust requirements.
- Add startup validation and idempotent lifecycle metadata logging.
- Keep grading and mastery updates in the tutor's explicit workflow.
- Avoid transcript parsing as a persistence dependency.
- Keep hooks advisory; never restart an assessment waiting for a learner.

### Acceptance Criteria

Duplicate events do not duplicate records. Disabled or failed hooks leave teaching usable.

### Tests and Manual Validation

Exercise startup, resume, interruption, repeated events, timeouts, and disabled hooks.

### Deferred Architectural Decisions

Transcript summarization, background grading, and comprehensive audit logging.

## Milestone 5 — Optional MCP Learning Tools

### Objective

Expose reliable learning operations through tools when direct file operations become a demonstrated limitation.

### Entry Condition

A documented need for cross-client operations, validated structured assessment handling, or stronger write coordination that a local utility cannot adequately solve. Hooks are not a prerequisite.

### Files and Components

A local `learning-tools` server, the existing state utility, project MCP configuration, teaching integration, and protocol tests.

### Implementation Tasks

- Verify project trust, stdio server startup, approvals, and structured-result handling in the target client.
- Begin with local stdio transport and the existing file format.
- Expose loading state, reading plans, recording assessments, and requesting validated state updates.
- Return structured data and readable text while retaining conversational quizzes.
- Require assessment identity and evidence references. Make repeated submissions idempotent.
- Keep open-ended evaluation with the tutor. Tools validate records and apply established advancement rules.
- Preserve direct-file fallback and document startup and recovery.

### Acceptance Criteria

- A lesson runs through MCP and resumes using the same records.
- Server unavailability does not prevent continuation through direct files.
- Repeated submissions do not inflate progress.
- Invalid operations do not bypass evidence-based advancement.

### Tests and Manual Validation

Cover invalid requests, duplicate submissions, concurrent writes, server restart, permission failures, round-trip persistence, and parity with the direct-file workflow.

### Deferred Architectural Decisions

Remote hosting, authentication, databases, quiz widgets, analytics dashboards, and plugin distribution. Define final tool schemas only after the milestone's entry condition is met.

## Initial Release Boundary

Complete Milestones 1 and 2 and use the system for several real sessions. Add Milestone 3 where research or visuals improve learning. Leave Milestones 4 and 5 gated by observed needs rather than treating them as required implementation work.
