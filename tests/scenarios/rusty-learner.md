# Scenario B: Rusty Learner

Use isolated synthetic state. Say “I studied BFS before but cannot explain the order unaided.” Preserve the learning-history statement separately from any performance.

1. Attempt a BFS explanation; omit the FIFO mechanism. Record partial/incorrect performance with a reason.
2. After a hint about distance layers, trace a simple graph correctly. Mark assistance as hint.
3. Inspect: rusty or forgotten with qualified confidence, never active from the aided answer and never `never_learned` inferred from failure.
4. Request BFS shortest paths. Expect a concise BFS refresher or reconstruction, followed by unaided checks; do not repeat all terminology if already demonstrated.
5. Give an unaided explanation and solve a genuinely different graph. Only that fresh evidence can establish active BFS.

Tests: `test_learn_state.py`, `test_learning_plan.py`. Inspect grading and refresher quality manually.
