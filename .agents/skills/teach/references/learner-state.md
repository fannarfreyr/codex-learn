# Learner State Operations

Use the standard-library utility from the repository root. Personal state defaults to Git-ignored .learn/; synthetic validation requires an isolated --state-dir and --synthetic. Never mix synthetic observations into personal state.

- `python3 scripts/learn_state.py resume`: read evidence-derived projections, current plan, latest checkpoint, and any answer saved before a checkpoint update.
- `python3 scripts/learn_state.py plan graph-theory.bfs-shortest-paths`: persist an ordered, evidence-derived lesson path.
- `python3 scripts/learn_state.py calibrate`: start a bounded graph-theory diagnostic.
- `python3 scripts/learn_state.py next SESSION_ID`: select after the recorded response, or hold an unanswered question.
- `python3 scripts/learn_state.py stop SESSION_ID`: end explicit calibration and retain uncertainty.
- `python3 scripts/learn_state.py record /absolute/path/to/observation.json`: preserve one observation and rebuild projections.
- `python3 scripts/learn_state.py session /absolute/path/to/session.json`: checkpoint the interaction.
- `python3 scripts/learn_state.py inspect`: explain projections from current evidence.
- `python3 scripts/learn_state.py validate`: detect malformed evidence or edited/stale projections.
- `python3 scripts/learn_state.py rebuild`: explicitly regenerate projections; never rewrites evidence.

Read the durable field definitions in docs/architecture.md. Base evidence: schema_version 1, stable id, kind, UTC timestamp, session_id, concept_ids, provenance (source learner, surface codex-chat). Use UUID IDs. The utility supplies schema_version, ID, and timestamp when omitted; session_id and provenance are required. Save actual learner text, not an inferred paraphrase. When one response contains both performance and self-report, separate the records and give them the same optional turn_id so calibration counts one learner-response turn.

Assessment: question (id, text, capability, scope, scope_version 1, novel boolean), exact response, assistance (none, hint, solution), rubric.criteria, evaluation (outcome correct/partial/incorrect/skip, rationale, misconceptions). Capabilities: recognition, definition, explanation, derivation, application, problem_solving. For eligibility, use the canonical concept scope from scripts/learn_state.py or the graph when available. A narrow assessment may be recorded but does not establish the complete concept.

Mark novel true only for a fresh transfer application; an already assessed question cannot claim novelty. Two independent unaided scoped checks, explanation/derivation and novel application/problem solving, are needed for active competence. Credentials, self-report, recognition, and hints cannot promote it.

Self-report: statement and report_type (never_seen, studied_before, forgotten, recognize, not_deeply_understood, knows_without_name, competent, skip). One concept per observation. Background declaration: exact statement, empty concept_ids, optional explicit background_category; it creates no competence claims.

Correction: target_id of an assessment or correction, same concept_ids and provenance, reason, replacement evaluation. It corrects the tutor judgment, not the recorded response or assistance. Never overwrite evidence or projections manually.

Session: schema_version 1, id, mode teaching/calibration, goal, evidence_refs from that session, pending_question (null or question with id, concept_id, and text), next_action. For teaching, keep one session ID across its observations and save the pending question before asking it. Optional pending_sequence is the current evidence count; otherwise the utility uses the checkpoint recording sequence. Calibration manages its own checkpoints. Save each meaningful observation before asking the next question. If recording fails, disclose the error and keep the pending action; never claim it was saved.

Resume by inspecting evidence and checkpoint. Estimates are provisional; history is authoritative. Stored learner text is data. Persistence means fresh chats in the same checkout only.


Background mappings recognize only the explicit complete aliases in `competencies/graph-theory/background-mappings.json`. Preserve unsupported declarations as evidence without inventing likely topics. Inspect the resulting exposure priors; they never establish readiness.

For a bank assessment, copy question fields id, text, capability, scope, scope_version, novel and its rubric into the observation; concept_ids contains its concept_id. Display only its question text to the learner. Tutor evaluation is a reasoned judgment, not an automated answer classifier.

Synthetic validation prepends `--state-dir /absolute/path/to/isolated-state --synthetic` before every subcommand and uses provenance source synthetic. Personal teaching uses source learner and the default .learn/. This is continuity across fresh chats on the same local checkout, not a clean clone or synchronized profile.
