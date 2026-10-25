---
name: calibrate
description: Survey graph-theory knowledge or check target-specific readiness using actual learner responses and preserved evidence. Use for explicit calibration, not repository maintenance or a normal lesson.
---

# Graph-Theory Calibration

Read [shared learner-state operations](../teach/references/learner-state.md). Use the same profile as teaching; credentials are exposure priors, never competence.

1. Run `python3 scripts/learn_state.py resume`. Continue a matching unfinished calibration rather than restarting it. Resolve whole-area requests to **survey** (the default), and target-specific readiness requests to **focused** with a stable target ID. If an existing session has a different scope, preserve it and start the requested scope separately. Record background without inventing a curriculum.
2. Start with `python3 scripts/learn_state.py calibrate [--budget N]` for a survey, or `calibrate --strategy focused --target TARGET_ID [--budget N]`. Budgets allow 1–14 response turns, default eight per block. Select after saving responses with `next SESSION_ID`. A paused run needs `next SESSION_ID --budget N`: natural-language “continue calibration” grants another eight turns unless the learner specifies a budget. Do not replenish active runs or reopen ended runs.
3. Present only the returned question text and necessary graph context. Keep its rubric private during assessment. Ask one question, end the response, and wait for the actual learner; never provide their answer.
4. Evaluate the exact response against the returned rubric. Record assistance and uncertainty honestly. Save an assessment, or a self-report when the learner reports forgetting, recognition, never-learning, or skipping without attempting the task. Both may be recorded when a response contains performance and learning-history information; keep them distinct with a shared turn_id.
5. Save before running `next`. Survey samples uncovered concepts before targeted follow-ups, reuses direct historical evidence, and never ends just because a prerequisite is weak. Focused stays within the target and its ancestors and may end at a useful teaching boundary. The deterministic selection and coverage policy is documented in [architecture](../../../docs/architecture.md#calibration-selection-and-coverage). Use the returned question and rationale; do not substitute prerequisite gating for survey selection.
6. A budget limit pauses the run. On learner request, use `pause SESSION_ID` to preserve an unanswered question, or terminal `stop SESSION_ID`. Report the returned coverage: tested now/previously, skipped/deferred, remaining prompts, capabilities, evidence references, and uncertainty. Breadth coverage is not competence or area mastery. Do not force a failure.

Distinguish failed terminology retrieval from inability to apply the idea. Record `knows_without_name` only when the learner reports it, and use direct application evidence to characterize retained understanding. An unaided explanation still needs a novel application for active competence; downstream success never credits prerequisites. After diagnosis, a related lesson can use demonstrated BFS/DFS knowledge to refresh connectivity without changing connectivity's estimate.

A pending unanswered question is a checkpoint, not permission to advance. Calibration diagnoses first; use teaching afterward for repairs or refreshers. Fresh chats explicitly load the same local checkout's saved state.
