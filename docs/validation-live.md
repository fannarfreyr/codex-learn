# Live Codex Validation — 2026-10-05

This is a synthetic validation profile, not an assessment of the repository owner. Both chats ran repository commands in `/Users/fannar/workspace/github.com/fannarfreyr/codex-learn`. State is retained for inspection in `/private/tmp/codex-learn-live-validation-20261005`; personal `.learn/` was never initialized.

## Chats and Procedure

- Chat 1: `01a10c76-329e-7350-9bba-350a21a65094` — background, calibration, prerequisite repair, BFS refresher, and session end.
- Chat 2: `01a10c89-b735-73e3-933e-adc0de13792d` — fresh context, state recovery, shortest-path teaching, assessment, and session end.

The second chat received only the state location, synthetic-isolation instructions, and a request to continue. It received no earlier answers, target concept, or intended plan. The app retains both transcripts. Some early learner replies were entered directly in Chat 1; later replies were supplied through the authorized scripted test. Every stored observation remains explicitly synthetic.

## Observed Behavior

1. A declared BSc produced no competence claim. The first run exposed a missing sentence-form alias: “I have a BSc…” initially failed the explicit mapping. Added that exact alias, preserved the original declaration, and verified the restarted diagnostic began at connectivity. Unmatched credentials remain unmapped.
2. A deliberately incorrect connectivity answer redirected questioning toward terminology. Correct foundational performance then returned questioning to connectivity application. Repeated wording was recorded as non-novel, without creating an additional independent transfer success.
3. Teaching skipped demonstrated terminology, repaired connectivity with a different graph, and used the reported BFS history for reconstruction rather than a full introductory lesson.
4. A partial BFS explanation and hinted success remained rusty. The tutor requested an unaided explanation and fresh application before making BFS active.
5. Chat 1 ended with the shortest-path target untested. Chat 2 recovered the saved plan, skipped the three demonstrated prerequisites, and taught the target without onboarding or full recalibration.
6. Chat 2 saved an unaided explanation, then required a different six-vertex application. Its final record established active scoped shortest-path competence with moderate confidence.
7. Both chats asked assessments and ended their responses to wait. No learner answers were invented. Untested trees, DFS, and spanning trees stayed unknown.

## Evidence Trace

The authoritative records are individual JSON files under the isolated state's `evidence/`. Each assessment preserves its full question, actual response, assistance, private rubric, tutor evaluation, and rationale. Recording sequence makes inspection deterministic.

| Sequence | Evidence ID | Kind | Concept | Observation/evaluation | Assistance |
| --- | --- | --- | --- | --- | --- |
| 1 | `205a0bb6-d350-4694-8353-0cf531bfaab6` | background_declaration | background | exposure prior | — |
| 2 | `bbde5a0a-9c1a-4c8e-af5e-6b5db8c91e51` | assessment | terminology | correct | none |
| 3 | `5161b958-8e69-4628-b58b-54d7aaa4429e` | assessment | connectivity | correct | none |
| 4 | `175556af-6a2c-464e-87cf-19f240bd9e43` | self_report | connectivity | recognize | — |
| 5 | `8125b4ea-7203-476b-ad58-3b4d67236462` | assessment | connectivity | incorrect | none |
| 6 | `5e871a0d-d65d-40a0-bbf0-51b281bf69ca` | assessment | terminology | correct | none |
| 7 | `22f29033-a0e1-49f8-aed2-0bac573d8951` | assessment | terminology | correct | none |
| 8 | `03ebeaf4-b607-4d71-9b4e-0d420725f482` | assessment | connectivity | correct | none |
| 9 | `545e411e-5949-48dd-aded-71385f223959` | self_report | bfs | forgotten | — |
| 10 | `f08fcc8f-52f6-4674-a37c-f72a6c2296bd` | assessment | connectivity | correct | none |
| 11 | `03a68402-7ccb-4620-87e7-d3070f0b4892` | assessment | bfs | partial | none |
| 12 | `17b52e7c-b113-4180-8031-c3f56198998c` | self_report | bfs | studied_before | — |
| 13 | `1d1e1fed-f392-402f-86e7-9cb64877ee8c` | assessment | bfs | correct | hint |
| 14 | `f0abbf08-c9d6-41f5-8dec-bac6d271cc7f` | assessment | bfs | correct | none |
| 15 | `e4ec4cb4-ec4f-4d0c-ba34-169130e2331f` | assessment | bfs | correct | none |
| 16 | `5bd8a732-6758-4cff-8a8f-f037b274f512` | assessment | bfs-shortest-paths | correct | none |
| 17 | `4032704d-8cf7-48c4-9d75-7d763da2e92b` | assessment | bfs-shortest-paths | correct | none |

## Final Projections

| Concept | Provisional state | Competence confidence | Expected exposure |
| --- | --- | --- | --- |
| `graph-theory.terminology` | active | moderate | medium |
| `graph-theory.connectivity` | active | high | high |
| `graph-theory.trees` | unknown | none | medium |
| `graph-theory.bfs` | active | moderate | high |
| `graph-theory.dfs` | unknown | none | unknown |
| `graph-theory.bfs-shortest-paths` | active | moderate | unknown |
| `graph-theory.spanning-trees` | unknown | none | unknown |

The target-only plan is `demonstrated_within_scope` with no unresolved checkpoint. This does not claim broader graph-theory mastery. All 17 evidence records, seven projections, and session/checkpoint references passed state validation.

## Fresh-Chat Transcript Excerpt

> Resumed the isolated synthetic profile. Its saved evidence supports skipping terminology, connectivity, and BFS instruction; we’ll continue with **BFS shortest paths**.
> 
> In an unweighted graph, a shortest path uses the fewest edges. Extend the BFS procedure with two records: a distance and a predecessor. Give the source distance 0. When exploring vertex \(u\) first discovers \(v\), assign \(d(v)=d(u)+1\) and save \(u\) as \(v\)’s predecessor.
> 
> For example, predecessor links \(T \leftarrow Q \leftarrow S\) reconstruct the path \(S \to Q \to T\). Follow the links backward, then reverse the order. Your existing understanding of FIFO exploration and distance layers provides the basis for explaining why this works.
> 
> The unanswered checkpoint is saved in the synthetic profile.
> 
> Why does BFS find shortest paths in number of edges? Would that guarantee hold for arbitrary edge weights?

## Failures, Corrections, and Limits

The sentence-form background mapping failure was fixed with one explicit alias and a regression test; it did not cause a false mastery claim. A test-editing error introduced during the final audit was corrected before the complete suite passed.

The bundled skill validator cannot import PyYAML in the available Python runtimes. Frontmatter and reference paths were checked manually, and both skills were exercised in actual Codex chats. The application retains its standard-library-only runtime.

Open-ended grading remains a tutor judgment subject to human inspection. These results validate this small MVP, not grading reliability over a broad curriculum. No specialist agents, hooks, MCP, databases, synchronization, backup, or extra domains were introduced.

## Inspecting or Removing Fixture State

Inspect with:

```sh
python3 scripts/learn_state.py --state-dir /private/tmp/codex-learn-live-validation-20261005 --synthetic resume
python3 scripts/learn_state.py --state-dir /private/tmp/codex-learn-live-validation-20261005 --synthetic validate
```

The separate scripted preparation fixture is in `/private/tmp/codex-learn-mvp-validation-20261005`. Both explicitly named directories contain only validation state and can be removed after inspection; they are not required for the installed tutor. The automated tests use temporary directories that clean themselves up.
