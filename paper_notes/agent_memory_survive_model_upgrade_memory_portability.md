# Does Your Agent's Memory Survive a Model Upgrade? A Controlled Study of Memory Portability

## Basic info

* Title: Does Your Agent's Memory Survive a Model Upgrade? A Controlled Study of Memory Portability
* Authors: Ankit Goyal, Jaideep Ray
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2609.05339
* Date surfaced: 2026-09-08
* Why selected in one sentence: It treats model upgrades as memory migrations and shows which memory formats survive the handoff.

## Quick verdict

* Must read

I inspected the full arXiv HTML text, especially the migration setup, the four memory formats, the embedding-index experiment, the repair experiment, and the compatibility recommendations. This is a preserved note because it gives agent memory the upgrade test it badly needs.

## One-paragraph overview

The paper asks whether an agent's external memory remains usable after one component changes. It compares four common persistence formats on 48 synthetic histories with exact answer codes: LC-RAW full histories, RAG chunks, model-written natural-language NOTES, and fixed-schema KG records. It then isolates writer-reader model swaps, embedding upgrades, and repair sources. The main result is not "memory transfer is hard" in the abstract. It is more specific: fixed-schema records are robust to writer swaps; model-written notes can be strongly direction-dependent; mixed embedding indexes silently lose most of the benefit of a full re-embedding; and compressed stores cannot be repaired if they threw away the evidence.

## Model definition

### Inputs
Synthetic agent histories with randomized answer codes, stored under four memory formats, plus writer-reader model assignments, embedding configurations, and repair-source conditions.

### Outputs
Exact-match answer accuracy, retained performance after swap, cost-to-recover, retrieval recall/ranking diagnostics, and repair success counts.

### Training objective (loss)
There is no new trained model as the main contribution. The paper is a controlled systems evaluation of memory formats and migration procedures.

### Architecture / parameterization
The evaluated memory architectures are LC-RAW, RAG, NOTES, and KG-fixed. The key parameterization choice is whether memory is preserved as raw evidence, retrieved chunks, free-form compression, or normalized subject-predicate-object facts under a stable schema.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to prevent a common agent-system failure: a model endpoint changes, the memory database still exists, and the system quietly forgets because the new reader cannot use the old store the same way.

### 2. What is the method?
The method is a controlled migration harness. The authors separate the actor, memory writer, memory reader, embedder, and repair source, then swap one component at a time while keeping histories, query scoring, and resource limits fixed.

### 3. What is the method motivation?
Memory outlives models. A durable store has to survive reader upgrades, embedding-model changes, and repair attempts after the original writing model is gone.

### 4. What data does it use?
It uses 48 synthetic histories with randomized answer codes and verifiable queries. That is narrow, but it lets the paper use exact scoring rather than fuzzy human judgment.

### 5. How is it evaluated?
The paper measures own-store versus inherited-store accuracy, partial versus full embedding migration, and repair from either the compressed store alone or retained raw history. It also decomposes failures into construction loss, retrieval loss, and reader residual.

### 6. What are the main results?
KG-fixed changes by only about +0.0004 plus or minus 0.0020 after a writer swap. NOTES is highly directional: Qwen reading Llama-written notes loses 13.28 percentage points, while Llama reading Qwen-written notes gains 9.91 points. A 50/50 mixed embedding index captures only a 4.96-point gain compared with 11.90 points for full re-embedding. Store-only NOTES repair never reaches the 90% recovery target, while raw-history repair succeeds for 34 of 48 histories in one direction. RAG re-embedding recovers all 96 cases for about $0.013 each, and KG-fixed rebuilding recovers 91-96 of 96 at near-zero additional cost.

### 7. What is actually novel?
The novelty is the migration framing and decomposition. The paper does not just report end-to-end memory accuracy; it asks where migration loss enters and whether it can be repaired.

### 8. What are the strengths?
The experiment is simple, auditable, and direction-aware. The embedding-migration result is especially useful because mixed vector spaces can have matching dimensions and still be semantically incompatible.

### 9. What are the weaknesses, limitations, or red flags?
The histories are synthetic, the models are two sub-10B open-weight models, and KG-fixed is helped by a schema designed for the task. The result should be treated as a stress-test pattern, not a universal ranking of all memory systems.

### 10. What challenges or open problems remain?
The obvious open question is how these findings scale to messy personal memory, project history, procedural skills, and high-privacy stores where retaining raw history may be unacceptable.

### 11. What future work naturally follows?
Run the same migration harness over real user/project memory, richer schemas, hybrid lexical-vector retrieval, rerankers, and privacy-preserving source retention.

### 12. Why does this matter for cabbageland?
Cabbageland cares about agents that survive handoffs. This paper gives a concrete rule: memory should have schema, provenance, isolated embedding spaces, and a tested migration path, not just a pile of model-written summaries.

### 13. What ideas are steal-worthy?
Use small migration probes before cutover. Test both directions of a writer-reader swap. Never mix embedding spaces in one index without routing. Keep protected source history when policy allows. Decompose memory failures before blaming the reader model.

### 14. Final decision
Keep as a preserved note. This is directly useful for any long-lived agent system with evolving models.

## 6. Mandatory critical angles

The mechanism is strong because it turns memory portability into a set of component tests. The evaluation is narrow but honest, and the caveats are exactly the right ones: schema design helps, raw retention has privacy costs, and migration direction matters.

## 7. Writing style

Tone should be approving and practical. This is an engineering paper with enough discipline to be immediately useful.

## 8. Repository output format

Saved as a preserved paper note because memory migration should become a standard agent-system reliability check.
