# ChronoStitch: Training-Free Composition of Visual KV Memories for Long-Horizon Temporal Reasoning

## Basic info

* Title: ChronoStitch: Training-Free Composition of Visual KV Memories for Long-Horizon Temporal Reasoning
* Authors: Santiram Tiwari, Nishant Sinha, Kunal Kislay
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.19547
* Date surfaced: 2026-07-26
* Why selected in one sentence: It turns cached video state from a broken concatenation trick into a structured memory-composition problem with an explicit positional repair and a limited content repair.

## Quick verdict

**Useful**

This is a narrower paper than the top memory or continual-learning pieces today, but the mechanism is real and the negative result is worth keeping. The useful claim is that long-video KV reuse fails for two distinct reasons, not one: local rotary positions collide, and later chunks were encoded without access to earlier ones. I inspected the arXiv abstract and PDF sections covering the method, controlled probes, TempCompass results, efficiency measurements, and limitations.

## One-paragraph overview

The paper studies a practical long-video question-answering setup where a VLM stores internal KV cache state for separate video chunks and later tries to answer temporal questions without reprocessing the whole video. The authors show why naive chunk concatenation is structurally wrong: every chunk was originally encoded with its own local rotary frame, so concatenation corrupts temporal geometry, and later chunks still lack the cross-chunk context they never attended to during original encoding. ChronoStitch addresses the first problem with a training-free three-axis re-basing of stored post-rotary keys over time, height, and width, and addresses the second with selective recomputation of a small fraction of later-chunk visual tokens. The result is not an oracle replacement, but it is a concrete step toward reusable visual memory that actually preserves long-range temporal reasoning.

## Model definition

### Inputs
The method takes independently cached visual KV memories for multiple video chunks, the query-time chunk ordering, and a reader VLM such as Qwen2.5-VL-3B.

### Outputs
It outputs a composed visual memory cache that can be used for downstream long-horizon temporal question answering, along with the resulting QA predictions.

### Training objective (loss)
There is no trainable model in the proposed contribution. ChronoStitch is a training-free memory-composition procedure applied to already computed KV caches.

### Architecture / parameterization
The method has two parts: a three-axis delta rotation that re-bases stored post-rotary keys into a global multimodal RoPE coordinate system, and a selective repair stage that recomputes only a chosen fraction of later-chunk visual tokens while allowing them to attend over the composed cache.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to make independently stored video-chunk KV caches reusable for long-horizon temporal reasoning without paying full joint re-prefill cost at every query.

### 2. What is the method?
The method first repairs positional inconsistency with three-axis key re-basing, then repairs a limited amount of missing cross-chunk content by selectively recomputing high-deviation later-chunk visual tokens.

### 3. What is the method motivation?
Chunk-level caching is attractive for efficiency, but naive cache concatenation breaks temporal order and cross-chunk dependency structure. If cached memory is going to be reused, it needs explicit composition logic.

### 4. What data does it use?
It uses controlled order-sensitivity probes plus the temporal split of TempCompass, with `590` multiple-choice questions, and query-time efficiency measurements over a sample of `12` videos.

### 5. How is it evaluated?
It is evaluated with exact key-reconstruction diagnostics, QA performance on TempCompass temporal reasoning, event-ordering and attribute-change breakdowns, and wall-clock query-time comparisons against full joint re-prefilling.

### 6. What are the main results?
On TempCompass temporal split, full joint prefill reaches `63.9%` overall accuracy, while ChronoStitch reaches `54.1%`, beating three-axis re-basing alone at `49.8%`, scalar one-dimensional re-basing at `49.5%`, and naive concatenation at `49.3%`. The gains are largest on event ordering, where ChronoStitch improves over naive concatenation by `7.0` points. The method also runs about `3.26x` mean and `3.31x` median faster than full joint re-prefilling in the reported efficiency test.

### 7. What is actually novel?
The novelty is the decomposition of the failure mode. The paper shows that positional repair alone is insufficient, then pairs a geometrically correct three-axis re-basing with a limited content repair instead of pretending one-dimensional reindexing solves the whole problem.

### 8. What are the strengths?
It has a crisp negative result, a training-free repair procedure, and honest diagnostics that separate representational correctness from downstream QA gains. The efficiency story is also concrete rather than hand-wavy.

### 9. What are the weaknesses, limitations, or red flags?
The study uses a relatively small `3B` reader model, and the joint ceiling on TempCompass is only `63.9%`, which compresses the visible margin. The repair fraction is chosen from a small control, and the paper itself admits that the scalar-versus-three-axis difference is not yet large at the downstream QA level without selective repair. Efficiency is reported on one hardware configuration rather than with a fuller hardware-independent cost analysis.

### 10. What challenges or open problems remain?
The main open problem is whether the same composition logic scales to larger VLMs, longer horizons, more video chunks, and richer temporal tasks where the missing-content problem becomes harsher.

### 11. What future work naturally follows?
Test the method on stronger readers and longer videos, learn better token-selection policies for repair, and connect the cache-composition logic to broader hierarchical or retrieval-based video-memory systems.

### 12. Why does this matter for cabbageland?
Cabbageland cares about memory that keeps its structure when reused. This paper is a clean reminder that storing state is cheap; storing it in a form that still composes correctly later is the hard part.

### 13. What ideas are steal-worthy?
Treat cache reuse as a memory-composition problem, not as naive concatenation. Separate positional repair from content repair. Use representation-level diagnostics to show why an efficiency trick fails before selling the downstream benchmark delta.

### 14. Final decision
**Keep it as a useful mechanism note.** It is not a grand theory paper, but it contains a real and reusable lesson about making cached multimodal state composable.
