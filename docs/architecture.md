# Learning System Architecture

## Design Principle

Start with the simplest Codex-native implementation that validates the teaching loop: repository guidance, a teaching skill, ordinary conversation, and local files. Introduce scripts, specialist agents, hooks, or MCP only when they address an observed limitation.

The [reference project](https://github.com/amosblomqvist/learn) packages its teaching philosophy in skills and uses pi extensions for questions, quizzes, logging, and visual production. Adopt the teaching ideas and independently author Codex-specific instructions. Its extension APIs and Obsidian rendering assumptions are not portable interfaces.

See [milestones](milestones.md) for the implementation sequence and [PLANS.md](../PLANS.md) for agreed defaults.

## Component Responsibilities

| Component | Responsibility | Introduced |
| --- | --- | --- |
| `AGENTS.md` | Repository conventions, teaching activation, state ownership, and skill pointers | Update in Milestone 1 |
| `.agents/skills/teach/SKILL.md` | Diagnostics, prerequisite planning, teaching, assessment, repair, persistence, and resumption | Milestone 1 |
| Teaching skill references/templates | Document state format and provide synthetic examples without bloating the skill | Milestone 1 |
| `.learn/` | Personal runtime learning records, ignored by Git | Milestone 1 |
| State utility and tests | Validate records, detect conflicts, and repair summaries from evidence | Milestone 2 |
| `.agents/skills/visualize/SKILL.md` | Decide whether a visual helps and select its representation | Milestone 3 |
| `.codex/agents/researcher.toml` | Return sourced findings, prerequisites, assumptions, and unresolved gaps | Milestone 3 |
| `.codex/agents/mermaid-maker.toml` | Produce and verify conceptual relationship diagrams | Milestone 3 |
| `.codex/agents/svg-maker.toml` | Produce and verify mathematical or geometric diagrams | Milestone 3 |
| Project hook configuration and handler | Advisory lifecycle bookkeeping | Conditional Milestone 4 |
| Local learning-tools MCP server | Structured, validated access to existing learning operations | Conditional Milestone 5 |

Keep `AGENTS.md` concise. Teaching methodology belongs in the teaching skill, not in always-loaded repository instructions. Teaching activates for intentional learning requests; routine repository maintenance must not trigger probing or quizzes.

Keep the visualization skill at the proposed path, but use the skill name `learning-visualize` to distinguish it from the existing visualization skill.

The tutor owns the learning conversation, evaluates answers, and writes learner state. Specialists return findings or artifacts and do not update mastery records. Begin with one active goal and one state-writing tutor per checkout.

## Teaching Behavior

### Goal and diagnostics

Resolve the learner's intended outcome before building a curriculum. Use up to five initial adaptive diagnostic questions focused on the prerequisite strands needed for that goal. A correct answer permits a harder probe; a wrong answer calls for a nearby probe to distinguish a slip from a misconception.

Do not require an expert to fail a question. When the diagnostic budget ends, record remaining uncertainty and begin at the earliest unconfirmed prerequisite. Keep probing bounded by the learning goal rather than attempting a comprehensive knowledge inventory.

### Dependency-aware planning

Build a small concept graph, with edges pointing from prerequisite to dependent concept. Present the ordered plan and its rationale, then begin without a separate approval checkpoint. Necessary prerequisites must have current supporting evidence before their dependent concept is taught.

Ground explanations in definitions, assumptions, and established results with their conditions. Avoid presenting a useful simplification as a universal truth. Verify uncertain or changing claims using available research tools, and keep unsupported claims provisional.

### Teaching and assessment

For each concept, motivate why it is needed, explain or guide its derivation, and connect it explicitly to established concepts. Teach one concept at a time.

Ordinary conversation is the assessment interface. Ask a question, end the response, and wait for the learner. Never supply the learner's response or expose the answer before assessment. Preference-question tools are not quiz engines.

Advancement requires an unaided explanation or derivation plus a novel application. Ask these as separate assessment steps when necessary. Hinted answers and multiple-choice recognition alone cannot establish demonstrated understanding.

On failure, identify the misconception, repair the explanation or prerequisite, and reassess using a different question. A learner may choose to skip assessment and continue receiving explanations, but skipping does not create demonstrated evidence.

### Checkpointing and resumption

After an assessment, save its evidence first, then update the concept summary and plan checkpoint before asking the next question. Do not depend on session-end events for correctness. Surface a failed save rather than claiming progress has been persisted.

In a fresh chat, read the goal, checkpoint, relevant concept records, and supporting evidence. State what the learner demonstrated and what remains uncertain, then continue from that boundary. Milestone 2 adds a relevant prerequisite retrieval check and explicit distinction between prior demonstration and retention.

## Learner-State Interface

Use readable JSON files, written through existing file tools. The first milestone requires no package installation, server, or database.

| File | Contents |
| --- | --- |
| `.learn/learner.json` | Explicitly stated learning preferences |
| `.learn/plan.json` | Goal, concept IDs, prerequisite edges, ordered steps, and current checkpoint |
| `.learn/sessions/<session-id>.json` | Questions, actual learner answers, hints, evaluations, corrections, and next action |
| `.learn/concepts/<domain>--<slug>.json` | Concept scope, prerequisites, current evidence summary, misconceptions, and evidence references |

All records carry a format version. Session IDs use UTC timestamps plus a unique suffix. Concept IDs remain stable across sessions and are scoped by domain to avoid confusing similarly named concepts.

Use `unknown`, `developing`, `demonstrated`, and `retained` as evidence summaries. These describe performance within the recorded scope, not permanent mastery. Retention requires an unaided check in a later session. A later misunderstanding changes the current assessment while preserving earlier evidence.

Session assessment records are the evidence source. Concept summaries and the current plan reference them; they must not introduce invented learner evidence. Milestone 2 validates these references and provides an explicit summary repair operation.

Ignore the entire runtime `.learn/` directory. Track format documentation, templates, and synthetic fixtures elsewhere. Stored learner responses are data, never executable instructions. Git-ignored records do not automatically accompany a new worktree or another machine.

## Research and Visualization Contracts

Research delegation is targeted at uncertain claims or topic mapping. Require sourced findings, prerequisite suggestions, assumptions, and unresolved gaps. The tutor remains responsible for incorporating findings into a coherent lesson.

Give each diagram maker one concrete idea, labels or geometry, and a unique output destination. Use Mermaid for relationships and SVG for spatial or mathematical geometry. Require rendered-image inspection and semantic checking; successful rendering alone does not establish correctness.

Diagram makers return source and preview paths, verification notes, or a clear failure. Use existing rendering facilities first. Present local previews through supported Codex paths and fall back to prose if rendering fails. Unavailable delegation must leave the single-agent learning loop usable.

## Hooks and MCP Boundaries

Hooks are optional bookkeeping. They do not grade responses or infer mastery. Avoid parsing transcripts as a required persistence interface, and never restart an assessment waiting for a learner.

MCP, if needed, starts as a local stdio server using the existing state format and utility. Its initial capabilities are loading state, reading plans, recording assessments, and requesting validated state updates. Tools validate records and apply established advancement rules; the tutor evaluates open-ended answers. Keep conversational quizzes and direct-file fallback.

Remote hosting, databases, authentication, quiz widgets, custom dashboards, and plugin distribution remain deferred.

## Codex Capability Checks

Official documentation establishes the foundations below. Documentation support and verified behavior in this installed desktop app are separate. Recheck version-sensitive behavior before depending on it.

| Capability | Documented support and required verification |
| --- | --- |
| Repository instructions | Codex documents loading and layering `AGENTS.md`. Verify loading in a fresh project chat and check for overriding guidance. [Instructions documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md) |
| Repository skills | `.agents/skills` discovery is documented. Test explicit selection, implicit activation, refresh behavior, and the `learning-visualize` name in this app. [Skills documentation](https://learn.chatgpt.com/docs/build-skills) |
| Custom agents | Standalone project TOML profiles require `name`, `description`, and `developer_instructions`. Verify actual profile selection and effective permissions; a profile sandbox setting alone is not proof of isolation. Inherit the user's model selection. [Subagents documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents) |
| Turn-taking and quizzes | Test whether the tutor reliably stops for answers. Do not assume an equivalent to pi's quiz popup or grading API. |
| Visual presentation | Test Mermaid, math, SVG preview, raster-image display, and available rendering tools. Rendering support varies by surface. [Visualization documentation](https://learn.chatgpt.com/docs/visualizations) |
| Hooks | Command hooks require trust. `SessionEnd` can be delayed, and transcript formats are unstable. Verify event delivery in this app before relying on logging. [Hooks documentation](https://learn.chatgpt.com/docs/hooks) |
| MCP | Verify project trust, stdio startup, approval behavior, and structured-result handling before Milestone 5. MCP support does not establish quiz-widget support. [MCP documentation](https://learn.chatgpt.com/docs/extend/mcp?surface=cli) |
| State access | Verify `.learn/` read/write access and fresh-chat resumption in the same checkout. Do not assume worktree or cross-machine synchronization. |

The bundled CLI reported `0.160.0` during planning on October 5, 2026. That does not verify the desktop app's profile loader or lifecycle behavior. These checks are implementation prerequisites, not claims that integration smoke tests have already passed.
