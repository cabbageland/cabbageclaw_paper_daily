# EA-Graph: Artifact-Anchored Verification Memory for Coding Agents under Upstream Drift

## Basic info

* Title: EA-Graph: Artifact-Anchored Verification Memory for Coding Agents under Upstream Drift
* Authors: Hwai-Jung Hsu, Cheng-Jan Chi, Hanna Everett
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.04278
* Date surfaced: 2026-08-06
* Why selected in one sentence: It is the cleanest direct paper in the batch on multi-session coding-agent memory because it stores verification claims against exact artifact content instead of trusting prose summaries to stay true after upstream drift.

## Quick verdict

**Must read**

I inspected the arXiv HTML paper, especially the artifact-identity model, the evidence-versus-freshness split, the unprovable state, the generated drift testbed, and the main Haiku and Sonnet results. The paper gets the real problem right: a previous session can preserve the conclusion of a verification step while losing the exact artifact state that made the conclusion valid. The best part is the refusal instinct. When replacement content is missing, EA-Graph returns **unprovable** instead of bluffing. The main caveat is scope. The evaluation is in carefully generated repositories rather than messy real codebases, so the claim is about provability judgment under drift, not general software-engineering competence.

## One-paragraph overview

EA-Graph is a structured memory for coding agents that need to revisit earlier verification claims after an upstream has changed. Instead of storing "this was checked," it stores claims anchored to first-class artifact identities at sub-path granularity and attaches content digests for the exact support that justified each claim. Each stored fact also carries two independent states: evidence strength and freshness. When the upstream changes, the system re-checks whether the anchored support is still current and classifies the earlier claim as unaffected, affected, or unprovable. The key design choice is that missing replacement content is not treated as low confidence. It is a terminal state that forces the agent to say the claim cannot currently be re-established.

## Model definition

### Inputs
The system takes a repository representation with code nodes, artifact nodes, read/write/kill relations, previously recorded verification claims, artifact-content anchors, and a new upstream drop that may include value drift, logic drift, or withheld content.

### Outputs
It outputs refreshed claim judgments such as unaffected, affected, or unprovable, along with updated freshness/evidence metadata and a separate retain-or-withdraw disposition for the maintained artifact.

### Training objective (loss)
There is no central learned model with a training loss. The contribution is a structured memory and query scheme, not a trained predictor.

### Architecture / parameterization
The memory state is written as a graph-plus-claim structure: code nodes, artifact nodes, read/write/kill edges, verification claims, anchors to canonical artifact identities plus content digests, metadata that separates evidence from freshness, and a separate disposition record so unverifiable content need not be destroyed.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the fact that coding agents often resume work from earlier sessions using prose summaries that record what was concluded but not the exact artifact state that made the conclusion true. After an upstream change, the project may still build while the earlier verification claim has silently gone stale.

### 2. What is the method?
The method stores verification claims over first-class artifacts with sub-path identity, resolves aliases to their leaf definitions, anchors each claim to the exact content used to verify it, separates evidence strength from freshness, and returns unaffected, affected, or unprovable when the upstream changes.

### 3. What is the method motivation?
File-level and prose-level memory are too coarse. A changed table entry can invalidate one behavior without invalidating every other reader of the file, and a missing upstream replacement should not force the agent into a fake binary guess.

### 4. What data does it use?
The evaluation uses generated repositories whose behavior-to-artifact ground truth is known by construction. Each clean world contains 96 behaviors across 12 modules, a readable but non-executable reference, and an unversioned upstream drop. The paper analyzes 42 sessions across seven clean worlds, 14 model-world instances, three memory conditions, and two model tiers.

### 5. How is it evaluated?
The task is to classify earlier claims as unaffected, affected, or unprovable after value drift, logic drift, and deliberately withheld content. The main metric is per-world F1 over the not-OK set, with exact paired signed-rank comparisons across worlds.

### 6. What are the main results?
In the Haiku round, the anchored condition beats both prose notes and no persistent memory in all seven worlds, with exact paired p = 0.0156 against each control. Its per-world median F1 is 1.000 versus 0.270 for prose and 0.286 for no memory. In the Sonnet round, the anchored condition is perfect in all seven worlds, but the controls also hit frequent ceilings, so the preregistered contrasts become non-significant through lack of non-tied pairs rather than through reversals. The introduction also gives a useful framing number: file-level invalidation can mark about 88 of 96 behaviors as suspect when only about 17 are actually affected.

### 7. What is actually novel?
The novelty is not "agents with memory." The paper's real contribution is artifact-level verification memory with sub-path identity, explicit content anchors, a strict separation between evidence and freshness, and an explicit unprovable state when replacement content is missing.

### 8. What are the strengths?
It uses the right unit of invalidation. It gives missing replacement content a principled status instead of hiding it inside a soft confidence score. It also avoids the usual benchmark leakage problem by building a world where the exact drift ground truth is known and version-control shortcuts are intentionally blocked.

### 9. What are the weaknesses, limitations, or red flags?
The world is generated, not organic. The exact test form for some Haiku comparisons is selected post hoc. The study does not measure repair quality, efficiency, or how difficult anchor extraction would be in large, mixed-language, dependency-heavy real repositories.

### 10. What challenges or open problems remain?
The hardest open problems are extracting complete anchors from real repositories, handling dynamic artifacts and runtime configuration, surviving partial observability outside a clean generated world, and integrating this memory with actual repair and re-verification loops.

### 11. What future work naturally follows?
Real-repository evaluation, automatic anchor extraction, integration with test and build graphs, and using anchor breakage to drive targeted re-checking or repair planning would all be natural follow-ons.

### 12. Why does this matter for cabbageland?
It matters because cabbageland repeatedly deals with multi-session coding work, upstream drift, and handoffs between agents. This paper offers a much better continuation primitive than "left a note in the repo and hoped it stayed true."

### 13. What ideas are steal-worthy?
Store claims against sub-path artifact identities, not just files. Keep evidence and freshness as separate state. Treat unprovable as a first-class terminal outcome. Keep artifact disposition separate from claim validity so uncertainty does not automatically destroy the last working state.

### 14. Final decision
**Keep it.** This is a real mechanism paper with a disciplined refusal mode and a design lesson that transfers cleanly to coding-agent memory.
