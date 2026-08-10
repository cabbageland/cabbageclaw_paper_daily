# Addressable Memory for Video World Models

## Basic info

* Title: Addressable Memory for Video World Models
* Authors: Xindi Wu, Sven Elflein, James Lucas, Olga Russakovsky, Laura Leal-Taixe, Despoina Paschalidou, Jonathan Lorraine, Aljosa Osep
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.07408
* Date surfaced: 2026-08-10
* Why selected in one sentence: It identifies addressability rather than mere capacity as the long-horizon video-memory bottleneck and fixes it with a training-free memory design that is unusually explicit and testable.

## Quick verdict

* Must read

I inspected the arXiv HTML full text. This is one of the cleaner recent memory papers because it does not wave at "long context" as if that were an explanation. It isolates a concrete failure mode in RoPE-based video world models, shows why naive compression corrupts memory, and proposes a training-free fix with a purpose-built benchmark.

## One-paragraph overview

The paper studies visual persistence in autoregressive video world models that carry long-range history through a growing KV cache. Its claim is that these models fail over long rollouts for two distinct reasons. First, once temporal RoPE offsets leave the range seen in training, old cache entries become hard to address even if they are still stored. Second, naive compression in the RoPE-rotated key space corrupts memory because incompatible phases partially cancel. The proposed fix, WorldTrace, is a training-free memory framework that stores compressed history in fixed summary slots with distinct in-distribution virtual positions. It uses two complementary writers: WorldTrace-Field for temporally coherent history compression, and WorldTrace-Landmark for sparse episodic recall at scene transitions. The paper also introduces LoopBench, a controlled revisit benchmark for testing whether a compressed cache can reconstruct a previously visited scene after a long detour.

## Model definition

### Inputs
The method takes the video world model's autoregressive KV cache, long rollout history, and the current generation query under temporal RoPE.

### Outputs
It outputs an addressable compressed memory cache and the resulting long-horizon generations, together with coherence and revisit-recall metrics.

### Training objective (loss)
There is no new training objective in the core contribution. WorldTrace is a training-free inference-time memory mechanism layered on top of an existing world model.

### Architecture / parameterization
The core design has three pieces: slot-rank virtual position assignment so compressed memory remains in-distribution and distinguishable, canonical-space key storage that unrotates keys before compression and re-rotates them at the target slot position, and two writers matched to different query families. WorldTrace-Field averages contiguous temporal groups in canonical key space for coherence. WorldTrace-Landmark stores frozen canonical keys for detected scene-entry landmarks to support episodic recall.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to preserve long-horizon visual consistency in autoregressive video world models, especially when a rollout leaves a scene and later revisits it.

### 2. What is the method?
The method compresses distant history into a fixed set of summary slots, assigns each slot a distinct virtual position tied only to slot rank, and stores keys canonically so they can be re-encoded at the correct slot position later. It uses field-style averaging for smooth continuation and landmark-style verbatim traces for revisit recall.

### 3. What is the method motivation?
Long-horizon failure is not just "the cache is too small." Stored content becomes unreadable once RoPE offsets move out of distribution, and naive compression destroys content before it can even be retrieved. The method explicitly separates addressability from stored content quality.

### 4. What data does it use?
The main experiments use the Matrix-Game-2 1.3B autoregressive world model, with additional results in the appendix on LingBot-World. The paper also introduces LoopBench, a controlled revisit benchmark with loop topologies such as ABA, ABCA, and ABCDA.

### 5. How is it evaluated?
It evaluates open-ended rollout coherence using metrics such as TempSSIM and scene drift, and evaluates revisit memory using PAC and TempSSIM on LoopBench. It also compares against sliding-window caches, Block-relative positioning, Centroid-linear positioning, and naive compression variants.

### 6. What are the main results?
WorldTrace-Field achieves the best temporal coherence at long horizons, including a reported relative TempSSIM gain of about 15.5% on long rollouts. WorldTrace-Landmark improves episodic recall by about 19.5% on LoopBench ABA revisits. At N=48, WorldTrace-Field is best on both TempSSIM and drift among the compared compression-positioning schemes. The paper also reports that WorldTrace outperforms Block-relative positioning by 5.9% and 2.8% TempSSIM at shorter horizons N=8 and N=16, respectively.

### 7. What is actually novel?
The novelty is the explicit decomposition of long-horizon memory into addressability and informativeness, followed by a concrete inference-time design that fixes both. The slot-rank virtual-position scheme is especially important because it keeps summary slots distinct at arbitrary horizons instead of collapsing them onto shared capped positions.

### 8. What are the strengths?
The mechanism is clear, training-free, and genuinely reusable. The benchmark is good because it directly tests revisit recall rather than only generic rollout smoothness. The canonical-space key storage story is also conceptually sharp and easy to steal.

### 9. What are the weaknesses, limitations, or red flags?
The work is still scoped to autoregressive video world models with temporal RoPE. The two memory writers are hand-designed rather than learned, and the main evaluation is concentrated on a specific distilled world model family rather than a broad suite of architectures.

### 10. What challenges or open problems remain?
A larger open problem is learning when to use field-style memory versus landmark-style memory automatically, or extending the addressability idea to multimodal and action-conditioned world models with more complex memory objects.

### 11. What future work naturally follows?
Learned memory-writer selection, object-centric canonical memory traces, integration with action planning, and explicit addressability benchmarks for other long-horizon agent memories all follow naturally.

### 12. Why does this matter for cabbageland?
Cabbageland cares about world models, persistent memory, and explicit state. This paper gives a concrete design pattern: do not just store more state; make the addressing scheme itself explicit and stable under long horizons.

### 13. What ideas are steal-worthy?
Use slot-rank virtual positions rather than original timestamps for compressed memory. Unrotate keys into canonical space before summarizing them. Separate coherence memory from episodic landmark memory. Benchmark revisit recall directly instead of relying only on generic rollout quality.

### 14. Final decision
Keep as a preserved note. The mechanism is crisp, the benchmark is useful, and the core idea transfers beyond video generation into any RoPE-based long-horizon memory system.

## 6. Mandatory critical angles

This paper is strongest on mechanism, failure analysis, and transferability of the core idea. It earns trust because the authors find the exact place the computation breaks, then repair that place directly. The main caution is scope: this is not yet a general memory theory for all world models, only a strong design for a specific but important class.

## 7. Writing style

The right tone is favorable and exact. This is not "yet another memory paper." It is a paper about why long-horizon memory stops being addressable and how to keep it readable.

## 8. Repository output format

Saved as a preserved paper note because the slot-rank addressing idea and canonical-key storage pattern are directly reusable for future work on world-model memory and long-horizon agent state.
