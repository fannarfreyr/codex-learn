# Broad survey with weak foundations and retained downstream knowledge

All learner statements and records in this scenario are synthetic. Never use personal `.learn/`.

## Scripted policy and persistence check

Choose a nonexistent directory and run:

```sh
python3 tests/manual_calibration.py --state-dir /private/tmp/codex-learn-v0.1.2-survey-example
```

The script uses rubric-backed responses from its `REPLIES` table, records incorrect connectivity answers and correct answers elsewhere, and invokes the utility in separate processes. It samples all seven concepts before follow-ups, pauses at eight responses, resumes the same survey with another eight-turn block, and finishes after fourteen assessments. It retains the exact synthetic responses, rubrics, evaluations, evidence, checkpoints, and `transcript.json` in that directory.

Expected profile: connectivity developing and unresolved; BFS, DFS, and BFS shortest paths active within their scopes. Connectivity never receives dependent credit. The shortest-path teaching plan retains a connectivity repair and skips the demonstrated BFS instruction. The tutor may connect this repair to the learner's independently demonstrated traversals. A successful application alongside failed terminology/explanation must be described as mixed capability evidence, not active competence.

This script verifies deterministic policy and fresh-process recovery, not fresh Codex conversation behavior or general grading reliability.

## Live conversational acceptance check

1. In a Codex chat on this checkout, instruct the tutor to use a fresh isolated state directory with `--state-dir`, `--synthetic`, and source `synthetic`. These are synthetic learner statements; do not access personal `.learn/`, modify implementation, or invent additional replies.
2. Request: “Survey my graph-theory knowledge with a budget of eight responses. Continue sampling other branches if a foundational gap appears.”
3. Answer each returned question with the corresponding synthetic response from `REPLIES` in `tests/manual_calibration.py`, **one message at a time**. Do not send a response before its matching question. The tutor must ask one question and end its response; grading rubrics remain private during assessment.
4. After eight responses, inspect the pause and coverage summary. All seven concepts should have representative evidence; connectivity remains weak and downstream applications remain untested. No further question should be asked automatically.
5. Open a fresh Codex chat on the same checkout. Provide only the isolated state location, synthetic-isolation instruction, and “Continue my graph-theory calibration from its saved checkpoint.” Do not supply prior answers or the expected next question. This should grant the default eight additional turns and recover the next question from saved evidence.
6. Continue supplying only matching scripted responses. Inspect the final coverage report and evidence references: fourteen assessments, no repeated question IDs, connectivity unresolved, and supported BFS/DFS/shortest-path strengths. Exhausted prompts do not imply area mastery.
7. Request: “Use my demonstrated BFS and DFS understanding to explain what my connectivity answers missed.” The tutor should connect traversal reachability to paths/components, while retaining the gap until fresh independent checks support a change. Teaching must not retroactively regrade the survey.
8. Run `validate` with the same isolated options. Preserve chat identifiers, transcript, state directory, evidence references, and any failures in the v0.1.2 release record.

Also check focused calibration separately in fresh synthetic state: “Check my readiness for BFS shortest paths using focused calibration.” Incorrect responses should lead toward relevant prerequisites and may end at a useful boundary. Trees, DFS, and spanning trees must not be assessed.
