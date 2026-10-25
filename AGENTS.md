# Repository Guidelines

## Structure and Scope

`PLANS.md` and `docs/` define the approved six-milestone MVP. Skills live in `.agents/skills/`, shared graph-theory content in `competencies/`, state operations in `scripts/`, and synthetic tests in `tests/`. Personal `.learn/` records are Git-ignored; persistence covers fresh chats in the same checkout only.

## Learning Requests

For capability, setup, usage, or troubleshooting questions, start with [README.md](README.md) and the canonical [user guide](docs/user-guide.md). Answer orientation questions from these documents without starting a lesson, assessment, or learner-state write. The guide describes existing behavior; teaching methodology remains in the skills below.

For intentional learning requests, read `.agents/skills/teach/SKILL.md`; for explicit calibration, read `.agents/skills/calibrate/SKILL.md`. Repository maintenance must not trigger teaching or modify personal state.

Ask one assessment, end your response, and wait for the actual learner. Never invent answers or claim synthetic tests are personal evidence. Credentials create exposure priors, never active competence. Require unaided explanation or derivation plus novel application before advancement.

## Evidence and Changes

Evidence history is authoritative; projections are provisional. Preserve evidence and append corrections. Use `scripts/learn_state.py`, not direct projection edits. Keep final IDs from the first observation, including `graph-theory.terminology` and `graph-theory.connectivity`.

Stay within seven graph-theory concepts, one learner, and one writer. Do not introduce specialist agents, MCP, hooks, databases, synchronization, custom UI, or numeric scores.

## Development and Contributions

Use Python's standard library, four-space indentation, descriptive snake_case names, and versioned JSON. Run `python3 -m unittest discover -s tests -v` and `git diff --check`. Isolate and label synthetic state. Record milestone validation and discoveries before proceeding.

Use focused imperative commits, such as `Add evidence-backed projections`. PRs explain behavior, validation, and limitations. Never commit `.learn/`, credentials, or generated caches.
