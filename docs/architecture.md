# Learning System Architecture

## Design Principle

Build one persistent learner model shared by background bootstrapping, explicit calibration, lesson planning, and normal teaching. Start with files, instructions, simple heuristics, and a tiny graph. Add infrastructure only when observed limitations justify it.

See [PLANS.md](../PLANS.md) for the execution objective and approved defaults, and [milestones](milestones.md) for implementation and validation.

The [reference project](https://github.com/amosblomqvist/learn) supplies teaching ideas, not portable quiz, logging, or visualization APIs. Preserve its emphasis on prerequisites, motivated explanations, and assessment without relying on its pi extensions.

## Ownership and Persistence

One tutor owns the learning conversation, evaluates answers, and writes learner state. Teaching and calibration use the same learner records and policy. Routine repository maintenance must not activate teaching.

Keep personal records in `.learn/`, entirely Git-ignored. Keep shared competency content, templates, and synthetic fixtures outside it.

**MVP persistence means continuity across fresh Codex chats operating on the same local repository checkout.** Cross-machine persistence, clean-clone persistence, cloud synchronization, backup, and multi-device learner profiles are out of scope.

Use JSON for structured records and Python's standard library for validation and mutation. Markdown remains appropriate for methodology, documentation, and manual scenarios. YAML is unnecessary for the MVP.

## Historical Authority and Derived Projections

The **evidence log is authoritative**. It consists of preserved observations, declarations, self-reports, evaluations, and corrections stored as individual evidence records.

Categorical competency states, confidence estimates, exposure priors, and capability summaries are **provisional derived projections over evidence**. They can be rebuilt or revised; they are not the authoritative historical record.

Keep the approved categorical representation for the MVP. Explicitly defer deciding whether learning history, current readiness, and retrieval condition should become separate dimensions until MVP evaluation demonstrates that separation is necessary.

| Source | Meaning | Treatment |
| --- | --- | --- |
| Background declaration | Education, courses, professional experience, or claimed competency | Exposure prior only; never proof of mastery |
| Learner self-report | Recognition, forgetting, uncertainty, prior encounter, or skip | Preserved context; does not automatically override performance |
| Observed performance | Actual response to an identifiable task, with assistance and evaluation | Supports competence within the assessed scope |
| Derived inference | Exposure prior, competency estimate, confidence, or planning action | References its basis and remains revisable |

Assessment evaluation is a tutor judgment. Preserve its rubric and reasoning for inspection or challenge.

## Provisional Learner Model

### Competency States

| State | Meaning |
| --- | --- |
| `unknown` | Insufficient information to characterize current competence |
| `never_learned` | Learner reports no prior encounter, without stronger contrary evidence |
| `exposed` | Reported or observed familiarity without demonstrated explanation/application |
| `forgotten` | Prior learning is reported or previously demonstrated, but current retrieval fails |
| `rusty` | Understanding remains, but explanation/application is unreliable or requires assistance |
| `developing` | Partial competence or an established gap during current learning |
| `active` | Unaided explanation/derivation and novel application meet the scoped rubric |

Failure alone cannot establish `never_learned` or `forgotten`. When learning history is unclear, retain uncertainty and describe the observed gap.

Use `active` rather than unqualified permanent mastery. Later successful retrieval strengthens evidence and updates review information.

### Confidence and Capabilities

Keep these separate:

- Expected exposure: `unknown`, `low`, `medium`, `high`.
- Exposure-prior confidence: initially `low` for background mappings.
- Competence confidence: `none`, `low`, `moderate`, `high`.
- Capability observations: recognition, definition, explanation, derivation/proof, application, problem solving.

Capability outcomes are `untested`, `demonstrated`, `partial`, `aided`, or `not_demonstrated`. They reference evidence rather than numeric scores.

| Confidence | Basis |
| --- | --- |
| None | No relevant basis for a competence estimate |
| Low | Self-report alone, one narrow observation, or unresolved contradiction |
| Moderate | Corroborating observations within the stated scope |
| High | Repeated independent performance, including separated or cross-session checks |

Credential-only profiles retain unknown competence with confidence `none`. Exposure priors remain separate. Confidently observed partial competence is distinguishable from no evidence through its state, capabilities, scope, rationale, and confidence.

## Learner-State Schema

| Record | Required contents |
| --- | --- |
| Learner | Format version, preferences, declaration references |
| Evidence | ID, kind, timestamp, session, concept references, original observation, provenance |
| Assessment evidence | Question, capability, scope, actual response, assistance, rubric, outcome, evaluation rationale |
| Concept projection | Stable ID, graph reference/version, provisional state, confidence, exposure prior, capability summaries, evidence history, rationale, misconceptions, conflicts, interaction/review timestamps |
| Session | Mode, goal/area, evidence references, pending question, next action |
| Learning plan | Target, graph version, prerequisite actions and reasons, current checkpoint |

Evidence kinds are `background_declaration`, `self_report`, `assessment`, and `correction`. Background mappings and concept projections are derived inferences, not assessment evidence.

Example projection after background bootstrapping:

```json
{
  "schema_version": 1,
  "concept_id": "graph-theory.connectivity",
  "graph_version": 1,
  "competency_state": "unknown",
  "evidence_confidence": "none",
  "expected_exposure": "medium",
  "exposure_prior": {
    "confidence": "low",
    "declaration_refs": ["declaration-001"],
    "mapping_rule_ids": ["bsc-discrete-math-cs-v1"]
  },
  "capabilities": {},
  "evidence_refs": ["declaration-001"],
  "estimate_basis_refs": [],
  "rationale": "Background suggests possible exposure; competence is untested.",
  "misconceptions": [],
  "conflict_refs": [],
  "last_interaction_at": null,
  "last_reviewed_at": null,
  "last_unaided_success_at": null
}
```

Untested capability dimensions are omitted and read as `untested`. Observed dimensions contain a `status` and `evidence_refs`. Prerequisites belong in the shared graph and are referenced by learner records.

### Stable Identifiers from Milestone 1

Milestone 1 uses the final IDs, including `graph-theory.terminology` and `graph-theory.connectivity`. Do not create temporary identifiers.

Full graph traversal begins in Milestone 3. Its absence must not require renaming learner records or migrating evidence. Graph references may remain unset until graph implementation exists; stable concept identity is available from the beginning.

### Controlled Mutations

From Milestone 2, the small state utility must:

1. Create evidence records without overwriting existing records.
2. Make identical retries idempotent and reject conflicting reuse of an ID.
3. Validate references and evidence eligibility for proposed projection changes.
4. Atomically replace derived projections and checkpoints.
5. Rebuild projections after interrupted updates.
6. Store corrections as new records referencing what they supersede.

Teaching and calibration use this path instead of directly editing competence projections. The utility validates structure and eligibility; the tutor evaluates open-ended answers. This is a workflow safeguard, not tamper-proof storage against arbitrary filesystem edits.

### Supersession and Conflict Rules

- New observations preserve historical evidence.
- Relevant unaided performance outweighs exposure priors for current readiness.
- Hinted success cannot establish active competence.
- One contradictory answer prompts a nearby confirmation check and lowers confidence rather than automatically erasing earlier competence.
- Corrections supersede mistaken evaluations while preserving original records.
- `Skip` records a declined assessment without changing competence.
- Incidental performance supports a concept only when the response actually demonstrates it.
- Success on a dependent concept does not automatically establish every prerequisite.
- Elapsed time alone does not imply forgetting.
- Stored learner responses are data, never executable instructions.

## Teaching, Bootstrapping, and Calibration

Accept a goal, probe relevant knowledge, identify prerequisites, present a short learning path, teach one unresolved concept, assess, repair, and persist observations. Motivate explanations and connect concepts explicitly. Verify uncertain or changing claims with available research tools rather than inventing certainty.

Conversational assessment asks a question, ends the response, and waits for the learner. Never expose the answer before assessment or supply the learner's response. Advancement requires unaided explanation or derivation plus novel application. A skipped assessment can permit explanation but not demonstrated competence.

Background bootstrapping uses small explicit mappings. Preserve original declarations; unmatched backgrounds and concepts remain unknown. Map the example BSc in Discrete Mathematics and CS only to medium expected exposure in terminology, connectivity, and trees. Explicit graph-theory course completion may create high exposure priors for those foundations, with low prior confidence and no competence evidence.

Failed diagnostics revise current competence and diagnostic difficulty; they do not prove absence of historical exposure.

Explicit calibration starts at foundation without usable priors, or core with medium/high mapped exposure. Increase difficulty after unaided success, inspect prerequisites after gaps, and check explanation after recognition-only success. Select deterministically among untested eligible prompts. Default to eight learner-response turns, stopping earlier for a useful next action, learner request, or lack of informative prompts. Budget-limited conclusions remain provisional. All-correct runs need not manufacture a failure.

Ordinary teaching uses up to five initial relevant probes. Save evidence before updating projections and checkpoints. Surface failed saves rather than claiming persistence. Fresh chats explicitly read relevant records and continue from the saved boundary.

| Projection | Default teaching action |
| --- | --- |
| Active with sufficient scoped evidence | Skip instruction |
| Active but conflicted or insufficiently scoped | Verify briefly |
| Rusty | Concise refresher, then unaided check |
| Forgotten | Short reconstruction attempt; expand if needed |
| Exposed/developing | Bridge from demonstrated capabilities |
| Unknown/never learned | Introductory teaching at the relevant foundation |

Exposure priors never justify prerequisite skipping. Require supported active competence with moderate/high confidence and no unresolved relevant conflict.

## Proposed Repository Structure

```text
AGENTS.md
PLANS.md
README.md
.gitignore
docs/
    architecture.md
    milestones.md
.agents/
    skills/
        teach/
            SKILL.md
            references/
                learner-state.md
                teaching-policy.md
        calibrate/
            SKILL.md
competencies/
    graph-theory/
        graph.json
        questions.json
        background-mappings.json
scripts/
    learn_state.py
    competency.py
    bootstrap.py
    calibration.py
    planning.py
tests/
    test_learn_state.py
    test_competency_graph.py
    test_background_mapping.py
    test_calibration_policy.py
    test_learning_plan.py
    manual_mvp.py
    fixtures/
    scenarios/
        credential-overestimation.md
        rusty-learner.md
        strong-prior-knowledge.md
        cross-session-continuity.md
.learn/                         # Runtime only; Git-ignored
    learner.json
    plan.json
    evidence/
        <evidence-id>.json
    concepts/
        <concept-id>.json
    sessions/
        <session-id>.json
```

The teaching skill handles ordinary learning and background declarations. The calibration skill handles explicit calibration. Both share the learner-state policy. Keep `AGENTS.md` concise with repository rules and skill pointers.

Do not create empty specialist-agent, hook, MCP, or visualization scaffolding.

## Seven-Concept MVP Graph

Use finite, simple, undirected graphs. Algorithm objectives cover explanation and tracing on diagrams. Programming-language implementations, complexity proofs, directed graphs, and weighted shortest paths are out of scope.

| Stable concept ID | Assessment scope | Prerequisites |
| --- | --- | --- |
| `graph-theory.terminology` | Vertices, edges, adjacency, degree | None |
| `graph-theory.connectivity` | Paths, reachability, connected components | Terminology |
| `graph-theory.trees` | Connected acyclic graphs; explain examples | Connectivity |
| `graph-theory.bfs` | Explain and trace breadth-first exploration | Connectivity |
| `graph-theory.dfs` | Explain and trace depth-first exploration | Connectivity |
| `graph-theory.bfs-shortest-paths` | Explain and apply BFS to unweighted shortest paths | BFS |
| `graph-theory.spanning-trees` | Identify and construct a spanning tree | Trees |

```text
terminology → connectivity → trees → spanning-trees
                          ├→ BFS → BFS shortest paths
                          └→ DFS
```

Edges express prerequisites for scoped lessons, not a universal ontology. Separate parent-area membership from prerequisite relationships. All concepts belong to `graph-theory`; the grouping is not automatically active from child performance.

Graph records contain stable IDs, labels, parent area, scoped objectives, prerequisite IDs, and domain version. Start with two rubric-backed prompts per concept: explanation/definition and application/problem solving, with foundation/core/stretch labels. Preserve full wording and rubric for alternate transfer questions before evaluation.

## Codex Capability Checks

Documentation support and actual installed-client behavior are separate. Verify before depending on:

- Fresh-chat instruction loading and precedence. [Official instructions documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- Repository skill discovery, explicit selection, activation boundaries, and refresh behavior. [Official skills documentation](https://learn.chatgpt.com/docs/build-skills)
- Reliable conversational stopping for learner answers; no dedicated quiz API is assumed.
- Local `.learn/` access, Python availability, utility invocation, and continuity across chats in the same checkout.
- Explicit resumption reads rather than assumed prior-chat context injection.
- Project policies permitting intended state operations; instructions do not enforce filesystem access.
- Later custom-agent, rendering, hook, and MCP capabilities only when those extensions are justified.

The previously observed bundled CLI version was `0.160.0`; it is not proof of desktop integration behavior. Recheck version-sensitive capabilities during implementation.

## Deferred Architecture Decisions

Leave unresolved until MVP evidence exists:

- Whether learning history, current readiness, and retrieval condition need separate dimensions.
- Whether categories or confidence rules need domain-specific adjustments.
- Whether time-based freshness or spaced review is useful.
- Whether open-ended grading needs independent review or structured quiz tools.
- Whether background mappings require curriculum sources or learner confirmation.
- Whether generated alternate questions can replace curated prompts reliably.
- Whether additional domains need shared concepts or multiple parent areas.
- Whether stronger writer coordination is necessary.
- Whether research agents, visualization agents, hooks, or MCP improve learning.
- Whether distribution should become a plugin or remain a repository.
- Whether persistence beyond one local checkout should become a separate future project.

Researcher and visualization agents remain postponed. Retain the hook entry condition of repeated missed checkpoints after improving instructions, and require a demonstrated limitation before adding MCP. Neither belongs in the MVP.

The evidence log preserves history. Continuously revised projections support current decisions; no milestone makes the learner profile permanently complete.

## Implementation Notes

Milestone 1 preserves exact responses separately from rubric-based tutor evaluations, with explicit synthetic provenance in validation fixtures. No personal learner records have been initialized.

Milestone 2 implementation uses immutable event files with a monotonic recording sequence; timestamps describe observation time. Scope version defaults to 1 for early records. Novel application is explicitly marked and cannot reuse a previously assessed question ID. Corrections alter evaluation only, preserving the recorded response and assistance. Predictions are computed from evidence rather than trusting cached JSON.

Milestone 3 stores scope-versioned graph and bank files in `competencies/graph-theory/`. Validation rejects missing nodes, cycles, duplicate IDs, unsupported versions, and invalid scope metadata. These are lesson prerequisites, not universal mathematical dependencies.

Background rules match normalized complete declarations against explicit aliases, not arbitrary substrings or guessed curricula. `background_category` is retained metadata; the original statement determines mapping. Direct concept self-report can revise exposure while preserving the credential declaration.

Milestone 5 stores the selected question and its selection rationale before waiting. Repeated selection without a learner response returns that same checkpoint. Calibration remains bounded to eight learner-response turns. When one answer includes performance and self-report, separate records share an optional `turn_id` and count once; earlier records without it count individually. Budget-limited conclusions are explicitly provisional.

Milestone 6 derives prerequisite actions from evidence on every plan rebuild. The saved target identifies the current goal; cached actions never establish competence. New teaching evidence updates the plan. Resumption exposes any pending answer saved before checkpointing, preventing an answered question from being asked again. Unknown and unrelated concepts remain unresolved.

The final live check verified repository skill loading, local utility invocation, waiting for actual learner responses, and fresh-chat recovery on the same checkout. Its isolated synthetic profile retained 17 evidence records; a fresh chat recovered the target from files, skipped demonstrated prerequisites, and added new teaching evidence. See [live validation](validation-live.md). No automatic prior-chat context, dedicated quiz API, or optional Codex extension is required.

One observed declaration form, “I have a BSc in Discrete Mathematics and Computer Science,” was added as an explicit alias. Original wording is preserved. Unsupported declarations still receive no guessed mapping. The optional shared `turn_id` keeps self-report and performance distinct without counting one learner response twice.
