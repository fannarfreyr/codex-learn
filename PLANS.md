# Codex-Native Learning System Plan

## Purpose

Build a Codex-native learning system inspired by [amosblomqvist/learn](https://github.com/amosblomqvist/learn). Start with repository instructions, one teaching skill, ordinary conversation, and local learner records. Validate the complete teaching loop before adding infrastructure.

This is an implementation plan. Saving these documents does not authorize implementing the milestones.

## Planning Documents

- [Architecture](docs/architecture.md): teaching behavior, component responsibilities, learner-state interface, recommended architectural changes, and Codex capability checks.
- [Milestones](docs/milestones.md): objectives, files/components, implementation tasks, acceptance criteria, validation, and deferred decisions for each usable increment.

## Agreed Defaults

| Decision | Initial behavior |
| --- | --- |
| Learners | One learner, any topic |
| Primary surface | Codex desktop app; keep instructions portable |
| Storage | Local `.learn/`, ignored by Git |
| Progression | Present the plan and begin without a separate approval checkpoint |
| Advancement evidence | Unaided explanation or derivation, plus a new application |
| Retention evidence | Successful unaided retrieval in a later session |
| Active work | One learning goal and one state-writing tutor per checkout |

## Core Learning Loop

1. Establish the learner's goal and probe their relevant knowledge boundary.
2. Identify prerequisites and distinguish demonstrated knowledge from uncertainty.
3. Construct and present a small dependency-aware plan.
4. Teach one concept at a time.
5. Assess understanding before progressing.
6. Repair misunderstandings and assess again with a different question.
7. Persist demonstrated evidence and the next checkpoint for future sessions.

## Implementation Order

| Milestone | Usable result | Entry condition |
| --- | --- | --- |
| 1. Complete learning loop | Teach, assess, repair, save, and resume in a fresh chat | Verify essential local capabilities |
| 2. Reliable records and retrieval | Validate evidence, recover partial updates, and distinguish demonstration from retention | Milestone 1 works |
| 3. Research and diagrams | Add targeted research and verified conceptual/geometric diagrams | Single-agent loop works; research or visuals improve representative lessons |
| 4. Optional lifecycle logging | Add advisory automatic bookkeeping | At least two missed checkpoints across five representative sessions after improving instructions |
| 5. Optional MCP learning tools | Expose validated learning operations through local tools | A documented limitation remains that a local utility cannot adequately solve |

Complete Milestones 1 and 2, then use the system for several real sessions. Add Milestone 3 where it improves learning. Milestones 4 and 5 are independent, conditional extensions; neither is required to declare the initial system usable.

## Planning Baseline

At planning time, the repository contained only the contributor `AGENTS.md`, with no application, build system, tests, or configured learning tools. The bundled CLI reported `0.160.0`; desktop capability behavior remains subject to the checks in the architecture document.

The reference and official documentation were reviewed on October 5, 2026. Recheck version-sensitive behavior before implementing the relevant milestone.
