# codex-learn

A Codex-native tutor that uses demonstrated understanding to decide what to teach next. **v0.1.1 documents the existing v0.1 MVP; it adds no learning features.**

## Setup and current scope

Open this repository checkout as your project in Codex. Have Python 3.10+ available as `python3` and permit the local file/command operations needed to save learning progress. The Python utility uses only the standard library: no package installation, server, database, or separate quiz UI is required.

The MVP covers seven concepts in finite, simple, undirected graphs: terminology, connectivity, trees, BFS, DFS, BFS shortest paths in unweighted graphs, and spanning trees. It supports one learner, one current goal, and one state-writing tutor at a time.

## Quick start

For a short diagnostic, say:

> I have a BSc in Discrete Mathematics and Computer Science. Calibrate my graph-theory knowledge.

Background is optional and never proves mastery. Answer one question at a time; you can ask for a hint, report uncertainty, or say “Skip.”

You can also start teaching directly, without calibration:

> Help me learn BFS shortest paths using my saved profile.

When leaving a lesson, ask to save the next step. In a fresh chat on this **same local checkout**, say:

> Continue my learning from saved state in this checkout.

## What can I do?

The [user guide](docs/user-guide.md) gives canonical prompts, inputs, options, state effects, inspection, recovery, and limitations for each workflow.

| I want to… | Guide |
| --- | --- |
| Declare education, courses, experience, or claimed competency | [Background](docs/user-guide.md#declare-background) |
| Start, continue, or stop a diagnostic | [Calibration](docs/user-guide.md#calibration) |
| Learn a concept or get a prerequisite-aware path | [Teaching](docs/user-guide.md#request-teaching) |
| Ask for hints, skip, or report forgotten knowledge | [Respond and request help](docs/user-guide.md#respond-and-request-help) |
| Inspect my learner profile | [Profile inspection](docs/user-guide.md#inspect-the-learner-profile) |
| Ask why a competency estimate exists | [Estimate explanations](docs/user-guide.md#explain-an-estimate) |
| Challenge a grade or reassess my knowledge | [Corrections](docs/user-guide.md#correct-an-evaluation) / [reassessment](docs/user-guide.md#reassess-a-concept) |
| End a lesson or continue a previous session | [Session continuity](docs/user-guide.md#session-continuity) |
| Find my state files and understand persistence | [Storage](docs/user-guide.md#locate-learner-state) |
| Investigate uncertain estimates or save errors | [Troubleshooting](docs/user-guide.md#troubleshooting) |

Personal state is JSON under Git-ignored `.learn/`. Evidence is preserved; estimates are provisional. There is no cross-machine synchronization, backup service, or clean-clone continuity. [Understand the learner model](docs/user-guide.md#understand-the-learner-model) before interpreting “active” as permanent mastery.

## Development and release evidence

Run `python3 -m unittest discover -s tests -v` and `git diff --check`. See [v0.1.1 release validation](docs/releases/v0.1.1.md), [technical architecture](docs/architecture.md), and the [original MVP plan](PLANS.md).
