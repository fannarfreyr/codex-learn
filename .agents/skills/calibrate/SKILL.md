---
name: calibrate
description: Adaptively diagnose graph-theory knowledge from actual learner responses and preserve evidence. Use when a learner requests calibration, not for repository maintenance or a normal lesson.
---

# Graph-Theory Calibration

Read [shared learner-state operations](../teach/references/learner-state.md). Use the same profile as teaching; credentials are exposure priors, never competence.

1. Run `python3 scripts/learn_state.py resume`. Resume a pending calibration rather than restarting it. Record any new background declaration without inventing a curriculum.
2. Start with `python3 scripts/learn_state.py calibrate`, or resume selection with `python3 scripts/learn_state.py next SESSION_ID`. The utility chooses among the seven-concept bank using evidence and a maximum of eight response turns.
3. Present only the returned question text and necessary graph context. Keep its rubric private during assessment. Ask one question, end the response, and wait for the actual learner; never provide their answer.
4. Evaluate the exact response against the returned rubric. Record assistance and uncertainty honestly. Save an assessment, or a self-report when the learner reports forgetting, recognition, never-learning, or skipping without attempting the task. Both may be recorded when a response contains performance and learning-history information; keep them distinct with a shared turn_id.
5. Save before running `next`. Let successes, gaps, and prerequisite checks change the next question. Do not mark an unaided explanation active without a novel application, or credit prerequisites from dependent success.
6. On learner request, run `stop SESSION_ID`. When selection returns no question, summarize tested capabilities, uncertainty, evidence, and the useful boundary; offer a related lesson. Do not force a failure or claim untested areas are mastered.

A pending unanswered question is a checkpoint, not permission to advance. Calibration diagnoses first; use teaching afterward for repairs or refreshers. Fresh chats explicitly load the same local checkout's saved state.
