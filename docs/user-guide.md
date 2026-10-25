# codex-learn User Guide

This is the canonical learner guide for the implemented v0.1 MVP, documented in v0.1.1. See the [README](../README.md) for setup, the [architecture](architecture.md) for technical formats, and the [v0.1.1 record](releases/v0.1.1.md) for validation.

## Getting started

Open the local checkout in Codex with Python 3.10+ available as `python3`. No Python packages or server setup are needed. Codex uses repository instructions and local file/command tools; permit those operations when needed. The utility validates and stores observations; Codex evaluates open-ended answers.

The following are canonical natural-language examples, not slash commands or a rigid parser. Ordinary wording is acceptable, but Codex must resolve the intended concept or session. You can declare background, request optional calibration, or ask for teaching immediately; full calibration is not an onboarding requirement.

## What can I do?

| Capability | Canonical request |
| --- | --- |
| [Declare background](#declare-background) | “Record my declared background: BSc in Discrete Mathematics and Computer Science.” |
| [Start calibration](#start-calibration) | “Calibrate my graph-theory knowledge.” |
| [Continue calibration](#continue-calibration) | “Continue my graph-theory calibration from its saved checkpoint.” |
| [Stop calibration](#stop-calibration) | “Stop calibration here and summarize what remains uncertain.” |
| [Request teaching](#request-teaching) | “Help me learn BFS shortest paths using my saved profile.” |
| [Respond or request help](#respond-and-request-help) | “Give me a hint.” / “Skip.” / “I studied this before but have forgotten it.” |
| [Inspect the profile](#inspect-the-learner-profile) | “Show my saved learner profile.” |
| [Explain an estimate](#explain-an-estimate) | “Explain my current estimate for BFS and show the supporting evidence.” |
| [Correct an evaluation](#correct-an-evaluation) | “Review the evaluation of my last connectivity answer. If it was misgraded, append a correction while preserving the original evidence.” |
| [Reassess a concept](#reassess-a-concept) | “Reassess my understanding of BFS with fresh explanation and application questions.” |
| [End teaching](#end-a-teaching-session) | “End this learning session and save the next step.” |
| [Continue learning](#continue-a-previous-session) | “Continue my learning from saved state in this checkout.” |
| [Locate state](#locate-learner-state) | “Where is my learner state stored, and what persists between chats?” |
| [Validate or recover state](#check-and-recover-saved-state) | “Check whether my saved learner state is valid and explain any errors before changing anything.” |

Each capability below states its purpose, invocation, inputs, supported options, state effects, expected behavior, inspection, recovery, limitations, and a concrete example.

## Declare background

- **What it does:** Saves declared education, courses, professional experience, or claimed competency. Supported mappings suggest exposure, not mastery.
- **How to invoke:** Ask to record the declaration, or include it when requesting calibration or teaching.
- **Required inputs:** Your background statement; a recognized complete declaration for an automatic mapping.
- **Supported options:** Recognized degrees/courses, unmatched free text, or separate concept-specific self-report. No transcript import or curriculum lookup.
- **State read or changed:** Appends background evidence, updates declaration references, and rebuilds exposure priors/projections. Direct concept reports use a separate evidence kind.
- **Expected behavior:** A credential alone leaves competence unknown with confidence none. Exposure may influence diagnostic starting level; it never justifies skipping prerequisites.
- **Inspect the result:** Ask for exposure priors and their declaration/rule references.
- **Correct or recover:** Clarify an unmatched declaration or add direct self-report; preserve the earlier statement. Evaluation corrections cannot amend background records.
- **Current limitations:** Automatic mapping is small; arbitrary degrees/experience may be stored without mapping. Background cannot erase demonstrated performance.
- **Example:** “Record my declared background: BSc in Discrete Mathematics and Computer Science.”

Matching ignores case/punctuation but compares complete declarations against explicit aliases:

- “BSc in Discrete Mathematics and Computer Science”
- “I have a BSc in Discrete Mathematics and Computer Science”
- “BSc Discrete Mathematics and CS”
- “BSc: Discrete Mathematics + Computer Science”

These imply **medium expected exposure** to terminology, connectivity, and trees. “Completed a graph theory course” and “Completion of a graph theory course” imply **high exposure** to those same foundations. Prior confidence is low in both cases. The other four concepts remain exposure-unknown without additional information. Unmatched declarations must not be turned into guessed curricula.

## Calibration

Calibration seeks a useful knowledge boundary, not exhaustive examination. The bank has fourteen prompts across seven concepts. Actual responses, assistance, self-report, prerequisites, and available unused prompts guide selection.

Question history has one implementation detail worth knowing: assessment question IDs are excluded across runs. A self-report-only skip consumes the pending prompt through that run's session metadata, so a new run may ask that skipped prompt again. Neither representation gives competence credit for skipping.

### Start calibration

- **What it does:** Starts a bounded graph-theory diagnostic, or identifies an unfinished one to continue.
- **How to invoke:** Ask to calibrate graph-theory knowledge.
- **Required inputs:** A request for this area; background is optional. Codex creates the session ID.
- **Supported options:** Declare background first, request hints, self-report, skip, or stop early. No learner-facing difficulty, custom budget, or alternate-domain setting.
- **State read or changed:** Reads profile/question history and writes a checkpoint; subsequent responses add evidence to the shared profile.
- **Expected behavior:** One question, then a wait. Questioning moves upward/sideways after success or toward prerequisites after gaps. The default maximum is eight response turns, with earlier stopping at a useful boundary or prompt exhaustion.
- **Inspect the result:** Request the selection rationale, tested scope, evidence references, and uncertainty.
- **Correct or recover:** Review a grade or resume an unanswered checkpoint. Start a new run if the previous one ended.
- **Current limitations:** Assessed question IDs remain excluded across runs; there is no unlimited replacement bank. All-correct runs need not force a failure or establish the whole domain.
- **Example:** “Calibrate my graph-theory knowledge.”

### Continue calibration

- **What it does:** Resumes an unfinished diagnostic using its saved evidence/question.
- **How to invoke:** Answer in the current chat or ask a fresh chat on this checkout to continue calibration.
- **Required inputs:** An unfinished checkpoint; identify the intended session if it is not the latest.
- **Supported options:** Answer, request help, self-report, skip, stop, or identify an existing session ID.
- **State read or changed:** Reads the checkpoint and evidence; saves actual responses and subsequent selections.
- **Expected behavior:** An unanswered question stays pending. A saved answer is recovered even if checkpoint updating was interrupted.
- **Inspect the result:** Ask what question/answer references were recovered and why the next question was selected.
- **Correct or recover:** Specify the correct session or inspect save errors. If no checkpoint exists, start a run using the existing profile.
- **Current limitations:** Generic resumption selects the latest saved session. A stopped/completed run does not reopen; a new run retains evidence and assessed-question history.
- **Example:** “Continue my graph-theory calibration from its saved checkpoint.”

### Stop calibration

- **What it does:** Ends calibration without claiming untested concepts are known.
- **How to invoke:** Explicitly ask to stop calibration.
- **Required inputs:** The current run, or its identifier if ambiguous.
- **Supported options:** Stop at any point; request a summary or related teaching afterward.
- **State read or changed:** Saves a stop reason/summary next action and clears the pending question; stopping itself is not a scored answer.
- **Expected behavior:** The tutor summarizes tested scope and uncertainty; the run remains ended.
- **Inspect the result:** Ask for the stop reason and current profile.
- **Correct or recover:** To return to an unanswered question, leave it pending instead. After stopping, request a new run or teaching using preserved evidence.
- **Current limitations:** There is no pause command. Restarting does not reset the profile or replenish the bank.
- **Example:** “Stop calibration here and summarize what remains uncertain.”

## Request teaching

- **What it does:** Plans relevant prerequisites and teaches one unresolved concept at a time.
- **How to invoke:** Name a supported target and ask to learn it using saved state.
- **Required inputs:** A target concept; Codex resolves natural names to IDs. Prior calibration is unnecessary.
- **Supported options:** Any target below, background declarations, hints, skips, or fresh reassessment. Ordinary teaching uses up to five initial relevant probes.
- **State read or changed:** Reads evidence/graph; writes the current plan, teaching checkpoint, and observations. Calibration and teaching share the profile.
- **Expected behavior:** The tutor presents a short path and skips, verifies, refreshes, reconstructs, bridges, or introduces concepts according to evidence. Partial answers need bridges; incorrect answers need repair and a different check. Assessments wait for your response.
- **Inspect the result:** Ask for ordered actions, reasons/evidence, and the current checkpoint.
- **Correct or recover:** Identify a questionable prerequisite assumption, request fresh checks, challenge a grade, or inspect a failed save.
- **Current limitations:** One learner/goal/writer; no broad curriculum, programming exercises, weighted-path algorithms, specialist agents, or custom quiz UI.
- **Example:** “Help me learn BFS shortest paths using my saved profile.”

| Target | Stable ID | Prerequisite |
| --- | --- | --- |
| Graph terminology | `graph-theory.terminology` | None |
| Connectivity | `graph-theory.connectivity` | Terminology |
| Trees | `graph-theory.trees` | Connectivity |
| BFS | `graph-theory.bfs` | Connectivity |
| DFS | `graph-theory.dfs` | Connectivity |
| BFS shortest paths | `graph-theory.bfs-shortest-paths` | BFS |
| Spanning trees | `graph-theory.spanning-trees` | Trees |

Scope is explanation and tracing on finite, simple, undirected graphs; shortest paths are unweighted. These are lesson prerequisites, not a universal curriculum. Success on a dependent concept does not automatically establish its prerequisites.

## Respond and request help

- **What it does:** Supplies performance or metacognitive evidence and controls assessment participation.
- **How to invoke:** Answer in chat, ask for a hint, say “Skip,” or describe what you remember.
- **Required inputs:** Your actual response or self-report; no quiz form exists.
- **Supported options:** Never seen, previously studied, forgotten, recognition without understanding, knowing an idea without its name, or claimed competency; assistance and declining an assessment.
- **State read or changed:** Saves an assessment, self-report, or separate records for both. A shared turn ID can prevent double-counting one combined response in calibration.
- **Expected behavior:** Assistance is recorded. A skip gives no competence gain or failure claim. Hinted success/recognition cannot establish active competence.
- **Inspect the result:** Request the stored text, assistance, report type, rubric outcome, and rationale.
- **Correct or recover:** Report overlooked assistance or captured-text errors. Review grading or supply fresh evidence; evaluation corrections cannot rewrite response/assistance fields.
- **Current limitations:** Self-report need not override performance. An answer following a hint is not unaided; tutor-authored tasks are not independently certified.
- **Example:** “I studied this before but have forgotten it. Give me a hint.”

## Inspect the learner profile

- **What it does:** Shows estimates derived from preserved evidence.
- **How to invoke:** Ask for the profile, optionally naming a concept.
- **Required inputs:** None for this checkout's default profile; a concept for focused inspection.
- **Supported options:** All seven concepts, or a conversational focus on states, confidence, exposure, capabilities, misconceptions, conflicts, or timestamps.
- **State read or changed:** Reads projections derived from evidence. The utility's `inspect` does not create observations or rewrite state.
- **Expected behavior:** Unobserved concepts remain unknown despite credential priors; references/rationale accompany estimates.
- **Inspect the result:** Ask for underlying evidence files or use the operator reference. Conversational focus is not a CLI filter flag.
- **Correct or recover:** Use explanation, correction, reassessment, or state validation according to the problem.
- **Current limitations:** This is a local graph-theory profile, not a global knowledge inventory or memory of all chats.
- **Example:** “Show my saved learner profile, focusing on BFS and its evidence confidence.”

## Explain an estimate

- **What it does:** Explains an estimate's basis, separating assumptions and observed performance.
- **How to invoke:** Ask why a concept has its current estimate and request evidence.
- **Required inputs:** A concept/estimate to investigate.
- **Supported options:** Explain exposure, confidence, assistance, capabilities, misconceptions, conflicts, or a planning action.
- **State read or changed:** Reads projections, original observations, and effective evaluations/corrections; explanation adds no learning evidence.
- **Expected behavior:** Identifiable records and assessed scope support the explanation. A false premise about your state should be clarified.
- **Inspect the result:** Compare referenced JSON answers, rubrics, evaluations, and corrections.
- **Correct or recover:** Challenge a particular judgment, report uncertainty, reassess, or validate stale caches.
- **Current limitations:** Inspectable reasoning does not prove grading is correct. Confidence is a heuristic category, not a probability.
- **Example:** “Explain my current estimate for BFS and show the supporting evidence.”

## Correct an evaluation

- **What it does:** Revises a mistaken tutor evaluation while retaining the original observation and grade.
- **How to invoke:** Identify the disputed answer and request a review/correction if warranted.
- **Required inputs:** A concept/question/recent answer or evidence ID sufficient to locate the record, plus the reason for dispute. Ambiguity needs clarification.
- **Supported options:** Revise outcome, evaluation rationale, or misconceptions; corrections can target assessments or earlier corrections.
- **State read or changed:** Appends a correction and rebuilds projections/any existing plan, preserving original evidence.
- **Expected behavior:** Effective evaluations change when a justified correction is saved. Active competence still requires sufficient supporting evidence.
- **Inspect the result:** Compare original grade, correction target/reason, and updated estimate basis.
- **Correct or recover:** Review a mistaken correction or obtain fresh evidence; preserve malformed records and report capture problems separately.
- **Current limitations:** No direct mastery assignment. Corrections cannot rewrite original response, question, rubric, assistance, concept scope, or provenance; declarations/self-reports are not correction targets.
- **Example:** “Review the evaluation of my last connectivity answer. If it was misgraded, append a correction while preserving the original evidence.”

## Reassess a concept

- **What it does:** Tests current competence with new evidence rather than revising history.
- **How to invoke:** Request fresh explanation and application checks for a supported concept.
- **Required inputs:** The concept; mention uncertainty or prior assistance.
- **Supported options:** Targeted teaching checks, a fresh transfer task, or a new bounded calibration where unused prompts remain.
- **State read or changed:** Reads existing evidence and appends new performance; updates the shared profile and plan.
- **Expected behavior:** New evidence can strengthen readiness or lower confidence and prompt refresh, while preserving history.
- **Inspect the result:** Ask what changed, which observations support it, and whether the plan skips, verifies, or refreshes.
- **Correct or recover:** Flag aided, narrow, reused, or misgraded tasks; review the evaluation or use a different task.
- **Current limitations:** No profile reset or direct state assignment. Calibration has finite prompts; teaching can author different checks. One success may be insufficient.
- **Example:** “Reassess my understanding of BFS with fresh explanation and application questions.”

## Session continuity

### End a teaching session

- **What it does:** Saves the current learning boundary and next action.
- **How to invoke:** Ask to end the lesson and save the next step.
- **Required inputs:** The current interaction; identify it if ambiguous.
- **Supported options:** End before answering, after an answer, or after demonstrating a concept. Stopping calibration is a different workflow.
- **State read or changed:** Saves actual observations, teaching checkpoint, and current plan as appropriate.
- **Expected behavior:** Reports what was saved and what remains pending; no invented answer or unrelated new goal.
- **Inspect the result:** Request the checkpoint, pending question, and next action.
- **Correct or recover:** Retain any unsaved answer and error; inspect/recover state rather than trusting an unconfirmed save.
- **Current limitations:** Closing a window does not trigger automatic session-end logging. Explicitly request a save.
- **Example:** “End this learning session and save the next step.”

### Continue a previous session

- **What it does:** Recovers the relevant profile, goal, latest checkpoint, and pending-answer information from files.
- **How to invoke:** Ask a fresh chat on this checkout to continue from saved state.
- **Required inputs:** Saved state here; identify another intended session if the latest is not yours.
- **Supported options:** Resume teaching or unfinished calibration, request a summary, or choose a new supported goal after completion.
- **State read or changed:** Reads evidence/sessions; `resume` also rebuilds an existing plan. Subsequent learning can add evidence.
- **Expected behavior:** Demonstrated prerequisites need not be retaught; unresolved concepts stay unresolved. A saved answer should not be requested again because checkpoint updating was interrupted.
- **Inspect the result:** Ask which session, target, pending question/answer references, and next action were recovered.
- **Correct or recover:** Check checkout/state location, identify the intended session, or validate bad records. If files are absent, establish a goal without inventing history.
- **Current limitations:** Generic resume selects the latest session. Prior chat context is not automatically injected; stopped calibration stays stopped; different machines/clean clones do not carry the profile.
- **Example:** “Continue my learning from saved state in this checkout.”

## Locate learner state

- **What it does:** Explains local storage and the continuity boundary.
- **How to invoke:** Ask where state is stored and what persists.
- **Required inputs:** None for an explanation; use the intended checkout for actual inspection.
- **Supported options:** Explain evidence, projections, sessions, learner metadata, or the plan. Isolated synthetic storage is an operator/test variation, not a multi-user service.
- **State read or changed:** A documentation-only explanation need not read personal records or write anything; actual file inspection reads them.
- **Expected behavior:** Default state is `.learn/` under the repository containing the utility, regardless of terminal working directory. The whole directory is Git-ignored.
- **Inspect the result:** See the layout below or ask Codex for the actual path without changing it.
- **Correct or recover:** Check for another checkout or explicit state-directory override. Do not manufacture missing evidence.
- **Current limitations:** No cross-machine, clean-clone, cloud-sync, backup, or multi-device persistence. Losing these files loses the profile.
- **Example:** “Where is my learner state stored, and what persists between chats?”

```text
.learn/
    learner.json                # Preferences metadata and declaration references
    plan.json                   # Current target and derived prerequisite actions
    evidence/<evidence-id>.json  # Preserved observations and corrections
    concepts/<concept-id>.json   # Rebuildable competency projections
    sessions/<session-id>.json   # Checkpoints, pending question, next action
```

Files are created as needed; there is no mandatory initialization command. `plan.json` exists once a target plan has been requested. Retained preferences metadata is not a user-facing settings system.

## Understand the learner model

Evidence history is authoritative. States, confidence, exposure priors, and capability summaries are provisional projections, not permanent mastery certificates.

| State | Interpretation in v0.1 |
| --- | --- |
| `unknown` | Insufficient performance or relevant learning-history information |
| `never_learned` | Learner reports no prior encounter, without stronger contrary evidence |
| `exposed` | Self-reported familiarity without the required performance pair |
| `forgotten` | Prior study/forgetting is reported but usable current retrieval is absent |
| `rusty` | Prior study plus partial/aided competence, or repeated gaps after earlier demonstration |
| `developing` | Performance is insufficient for active competence, without qualifying learning history |
| `active` | Scoped unaided explanation/derivation and a novel application/problem-solving task are supported |

Failure alone does not establish never-learning or forgetting. Credentials alone create no competence claim. An active estimate with low confidence after conflict needs verification before prerequisites are skipped.

**Competence confidence** is `none`, `low`, `moderate`, or `high`. Rules use low confidence for self-report/narrow or conflicting evidence and moderate confidence for corroboration. For active estimates, high confidence requires four independent eligible question IDs, or three across at least two sessions. These are heuristics, not measured probabilities or numerical knowledge scores.

**Expected exposure** is separately `unknown`, `low`, `medium`, or `high`; background-prior confidence is low. Direct self-report can revise exposure assumptions without establishing competence. **Capability summaries** cover recognition, definition, explanation, derivation, application, and problem solving. They retain the latest relevant outcome and evidence references; omitted dimensions are untested. A narrow success does not establish the entire concept scope.

Evidence kinds distinguish background declarations, self-report, assessments, and corrections. Assessments retain the exact response, assistance (`none`, `hint`, `solution`), scoped rubric, outcome, and tutor rationale. New observations preserve history; corrections change effective evaluations. A skip does not change competence. One later gap can lower confidence; repeated gaps can produce rusty knowledge; fresh unaided evidence can restore readiness. Dependent success gives no automatic prerequisite credit.

Misconceptions can reflect historical assessments even after improvement. Inspect their evidence and current rationale rather than assuming every listed misconception remains unresolved. Timestamps aid inspection; elapsed time alone does not downgrade knowledge. Separating learning history, current readiness, and retrieval condition into independent dimensions remains deferred.

## Troubleshooting

| Symptom | Inspect first | Supported next step |
| --- | --- | --- |
| “My degree should mean I know this” | Exposure versus competence; exact declaration alias | Clarify background and demonstrate the concept |
| “I answered correctly but am not active” | Scope, assistance, novelty, performance pair, grading | Ask why; challenge a grade or take fresh unaided checks |
| “The estimate is too confident” | Conflicts, actual answers, rubrics, confidence rationale | Report uncertainty and reassess; do not edit projected states |
| “I remember this but cannot explain it” | Learning history and aided/partial performance | Record self-report and request reconstruction/refresher |
| “The tutor recorded something incorrectly” | Actual response versus evaluation | Review grading; response/assistance capture cannot be amended by the correction tool |
| “Calibration has no new question” | Stop reason, tested scope, used question IDs | Use the summary or request targeted teaching/reassessment; new calibration only helps where eligible prompts remain |
| “Continuing calibration gives a summary” | Whether the run was stopped/completed | Request a new run or teaching; `next` does not reopen it |
| “A fresh chat started from zero” | Checkout, state path, saved session, save errors | Request an explicit state read; do not invent absent records |
| “Saved estimates look edited or stale” | Validation and preserved evidence | Explicitly rebuild derived records |
| “A record is malformed or unsupported” | Exact error and affected file/version | Preserve it and report the problem; rebuild does not fix arbitrary evidence/checkpoints |

### Check and recover saved state

- **What it does:** Validates integrity, identifies stale caches, and can explicitly rebuild derived records from valid evidence.
- **How to invoke:** Request validation first; separately request rebuilding when the problem concerns derived records.
- **Required inputs:** Intended state location and any observed error; default personal state is this checkout's `.learn/`.
- **Supported options:** Read-only validation, error explanation, or explicit rebuild. No general automatic repair/rollback command.
- **State read or changed:** Validation reads records. Rebuild writes projections, learner metadata, and any existing plan; it preserves evidence and does not repair session files.
- **Expected behavior:** Errors are surfaced. Rebuilding relies on preserved, structurally valid evidence.
- **Inspect the result:** Re-run validation and inspect estimates/evidence references.
- **Correct or recover:** Preserve malformed originals and errors. Report genuine implementation defects separately rather than manually assigning mastery.
- **Current limitations:** Rebuild is not backup restoration, a raw-evidence editor, or universal save recovery. Unsupported versions need investigation.
- **Example:** “Check whether my saved learner state is valid and explain any errors before changing anything.” For stale caches: “Rebuild my derived records from the preserved evidence without rewriting observations.”

## Operator reference

Learners can use the requests above. These are existing utility operations, run from the repository root; they do not grade answers or conduct a lesson by themselves.

| Command after `python3 scripts/learn_state.py` | Effect |
| --- | --- |
| `inspect` | Reads evidence-derived projections for all seven concepts |
| `validate` | Reads/checks evidence, projections, sessions, and any plan |
| `resume` | Returns latest checkpoint/projections; rebuilds an existing plan |
| `plan TARGET_ID` | Writes the target's ordered, evidence-derived plan |
| `calibrate [--session-id NEW_ID]` | Starts diagnostic and saves pending prompt; optional ID must be unused |
| `next SESSION_ID` | Selects after saved evidence or holds unanswered prompt; may update checkpoint |
| `stop SESSION_ID` | Ends calibration and saves stop reason |
| `record FILE` | Appends validated observation/correction and rebuilds derived records; identical IDs are idempotent, conflicting reuse is rejected |
| `session FILE` | Writes a validated checkpoint |
| `rebuild` | Rebuilds derived records, preserving evidence |

Global options precede the subcommand: `--state-dir PATH` selects a local directory; `--synthetic` permits explicitly synthetic evidence in an isolated directory. Synthetic mode is rejected with the default personal `.learn/` location. Observations also need synthetic provenance; the flag alone does not label them. These are operator/test options, not a profile-switching UI.

Check `python3 scripts/learn_state.py --help` and `python3 scripts/learn_state.py calibrate --help`. The CLI has no `--budget`, `--difficulty`, `--concept` filter, `reset`, `set-mastery`, or reopen-stopped-run operation. The Python calibration helper's internal budget argument is not a CLI option.

JSON details are in the [schema/evidence reference](architecture.md#learner-state-schema) and [shared state-operation instructions](../.agents/skills/teach/references/learner-state.md). Use the utility instead of editing projection JSON.

## Synthetic walkthrough for documentation validation

This optional walkthrough uses existing isolation options to test the guide without assessing the repository owner. **Its records are not personal learning evidence.**

Precondition: `/private/tmp/codex-learn-v0.1.1-docs-validation` must not already exist. Check before starting; preserve an existing directory and document a new run instead of deleting or silently reusing it. Personal `.learn/` must remain untouched.

Send these messages **one at a time**, waiting for each response. The first selects the existing utility options; it is an instruction to Codex, not a new application setting.

1. “For this walkthrough, keep all learner state in /private/tmp/codex-learn-v0.1.1-docs-validation using --state-dir and --synthetic, with provenance source synthetic. Do not access or modify my personal .learn/ profile. These are synthetic learner statements, not evidence about me. Do not change implementation files or invent answers. Confirm the isolated location and wait.”
2. “Record my declared background: BSc in Discrete Mathematics and Computer Science.”
3. “Calibrate my graph-theory knowledge.”
4. “Skip.”
5. “Stop calibration here and summarize what remains uncertain.”
6. “Show my saved learner profile.”

Expected result: the declaration stays identifiable; terminology/connectivity/trees get medium exposure with low prior confidence. A credential or skip creates no competence. Without other observations, all seven states remain unknown with confidence none. Calibration asks a question, accepts the actual skip, selects a different available prompt, and ends with an explicit stop reason. Evidence is labeled synthetic. Inspect records and validate using the same override:

```sh
python3 scripts/learn_state.py --state-dir /private/tmp/codex-learn-v0.1.1-docs-validation --synthetic validate
```

Preserve the transcript, evidence/session references, and failures in the release record. The named fixture directory can be removed after inspection and is not required for normal learning. Do not remove personal state during cleanup.
