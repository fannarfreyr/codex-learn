# Repository Guidelines

## Project Structure & Module Organization

This repository is currently an empty Git project. No source code, tests, assets, or dependency manifests exist yet. When adding the initial implementation, group files by purpose: `src/` for application code, `tests/` for tests, and `assets/` for static resources where applicable. Document the actual layout and entry points in `README.md`; avoid creating unused directories.

## Build, Test, and Development Commands

No build system, development server, or test commands are configured. Do not assume commands such as `npm test` or `make build` are available.

- `git status --short`: review local changes before committing.
- `git diff --check`: detect whitespace errors in tracked changes.
- `git diff`: inspect changes to tracked files before opening a pull request.

When introducing tooling, add reproducible setup, build, test, and local run commands to `README.md`, and update this guide to match.

## Coding Style & Naming Conventions

No language-specific conventions, formatter, or linter have been established. Use consistent indentation within each file and descriptive names. Prefer lowercase, hyphen-separated documentation filenames, with standard exceptions such as `README.md` and `AGENTS.md`. When selecting a language, adopt its conventional formatter and commit the configuration alongside the initial code.

## Testing Guidelines

No testing framework or coverage threshold is configured. Add tests for new behavior and bug fixes once executable code exists. Use the chosen framework's discovery conventions, such as `test_*.py` or `*.test.ts`, and document the test command. Keep tests deterministic and independent of private credentials or external services.

## Commit & Pull Request Guidelines

There is no commit history from which to infer a message convention. Use concise, imperative subjects, for example, `Add initial project setup`. Keep commits focused on one logical change.

Pull requests should explain the change, its purpose, and validation performed. Link relevant issues and include screenshots for visible interface changes. Explicitly state when tests could not be run.

## Security & Configuration

Never commit credentials or secrets. If configuration is needed, provide placeholder examples and ignore local secret files and generated artifacts.
