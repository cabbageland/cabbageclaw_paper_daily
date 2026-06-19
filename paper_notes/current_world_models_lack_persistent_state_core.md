# Current World Models Lack a Persistent State Core

## Basic info

* Title: Current World Models Lack a Persistent State Core
* Authors: Jinpeng Lu, Dexu Zhu, Haoyuan Shi, Linghan Cai, Guo Tang, Yinda Chen, Jie Cao, Duyu Tang, Yi Zhang, Yong Dai, Xiaozhu Ju
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.20545
* Date surfaced: 2026-06-19
* Why selected in one sentence: It turns world-state persistence into a viewpoint-intervention benchmark instead of accepting realistic video as evidence of a world model.

## Quick verdict

* Highly relevant

This is the most relevant paper today. I inspected the full arXiv PDF, including the benchmark design, diagnostic dimensions, model table, event-factor analysis, human calibration section, and conclusion. The paper is valuable because it asks the right hard question: does a generated world keep evolving while the camera is not watching?

## One-paragraph overview

The paper introduces WRBench, a diagnostic benchmark for video world models. Each test specifies a scene, an event, and a camera intervention that moves observation away from the target and later returns. The benchmark then separates several failure modes: maybe the camera never executed the requested move, maybe the target never re-entered view, maybe the visible sequence looked fine but the returned object froze, reset, drifted, vanished, or duplicated. Across 9,600 videos from 23 generators, the central result is that current models can produce plausible visible continuity without reliably preserving the event endpoint when it was unobserved.

## Model definition

### Inputs
WRBench inputs are Natural-25 event-view records: an initial scene family, an object/event specification, a viewpoint intervention, and the model-specific conditioning form needed to drive a given video generator. For evaluated generators, inputs vary by paradigm: prompt-only camera requests, model-inferred controls, source-video conditions, or geometry-cache conditions.

### Outputs
The evaluated generators output videos. WRBench outputs diagnostic scores for requested-camera precision, prompt-camera alignment, visual integrity, visible spatial consistency, visible state consistency, re-observation support, re-observed spatial consistency, and re-observed state consistency.

### Training objective (loss)
The paper does not introduce a new trained world model or a new training loss. It introduces a benchmark and evaluation pipeline. The authors argue that future world models need objectives that explicitly supervise endpoint persistence under viewpoint intervention, but that is a design direction, not an implemented loss in this paper.

### Architecture / parameterization
WRBench is a benchmark stack rather than a learned architecture. Its pieces are the Natural-25 prompt/event suite, WRBenchLib for translating records into model-specific conditions and provenance, a hierarchical diagnostic evaluator, and 2,547 deduplicated human annotator verdicts used to calibrate automatic judgments.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
The paper targets a blind spot in video world-model evaluation. Existing metrics reward fidelity, motion, camera control, and plausible physics while not testing whether an internal world state continues to evolve when the relevant object is out of view.

### 2. What is the method?
The method is to use viewpoint change as an observability intervention. WRBench asks the camera to move away from an event target and later return, then scores whether the returned evidence supports the same event endpoint. Its diagnostic chain separates control execution, visible quality, re-observation access, and returned-state correctness.

### 3. What is the method motivation?
A real world model should model how the world unfolds, not just how the next visible frame should look. If a cat jumps onto a bed while the camera turns away, the cat should be on the bed when the camera returns. The benchmark is motivated by this gap between view-conditioned rendering and persistent world-state evolution.

### 4. What data does it use?
WRBench uses Natural-25, a balanced suite of 25 scene families across 19 venues crossed with a four-level event design that factors spatial displacement against in-place state change. The experiments evaluate 23 video generators and 9,600 generated videos. Human calibration uses 2,547 deduplicated annotator verdicts.

### 5. How is it evaluated?
The paper evaluates generated videos through a six-dimension diagnostic chain: requested-camera precision, prompt-camera alignment, visual integrity, visible spatial/state consistency, re-observation support, and re-observed spatial/state consistency. Re-observed consistency is computed only on the subset where hidden-and-returned evidence is judgeable, which keeps "failed to return" separate from "returned in the wrong state."

### 6. What are the main results?
The central result is a preservation-access-re-observed-consistency gap. Models can preserve visible quality or expose the target again, but returned-state correctness remains a distinct and weak capability. Re-observed spatial and state consistency form their own block, while re-observation support can move almost independently. Scaling Wan variants from smaller to larger settings increases access or visible quality but does not reliably improve re-observed state. Geometry caches and source-video conditions help ask the return question more often, but they do not solve hidden event evolution.

### 7. What is actually novel?
The novelty is the attribution structure of the benchmark. WRBench does not merely ask whether a video is realistic or whether a camera trajectory was followed. It treats camera motion as an intervention on observability and separately measures whether the returned object preserves the event-induced endpoint.

### 8. What are the strengths?
The benchmark decomposes failure instead of hiding it behind a holistic score. It handles heterogeneous control paradigms by recording what condition each model actually received. It also distinguishes relocation from in-place state change, which exposes the more revealing failure: object transformations that move nowhere are especially hard to preserve out of view.

### 9. What are the weaknesses, limitations, or red flags?
This is a benchmark and diagnosis, not a fix. The evaluation depends on automatic judgments calibrated by humans, so it is bounded by the evaluator design and judgeability criteria. The model roster is also a snapshot of current video generators, and some API models have sparse re-observation support, making their returned-state scores less stable.

### 10. What challenges or open problems remain?
The open problem is writing hidden event endpoints into persistent state. The paper argues that current systems mostly cache where to look back, not what changed while hidden. Future work needs architectures and objectives that supervise state evolution under temporary non-observation.

### 11. What future work naturally follows?
Natural follow-ups include training losses for endpoint persistence, reward models that separately score camera access and returned-state correctness, world models with explicit what-memory rather than only geometry or appearance caches, and broader benchmarks for multi-object hidden dynamics.

### 12. Why does this matter for cabbageland?
This is close to cabbageland's core taste: explicit state must do work. The benchmark provides a concrete test shape for memory, world models, and agent state: hide the evidence, let the state evolve, then return and check whether the mechanism preserved the right endpoint.

### 13. What ideas are steal-worthy?
Use observability interventions rather than passive evaluation. Report access separately from correctness. Treat a missing returned object as a different failure from a wrong returned state. For any claimed world model or memory module, test in-place state changes, not only relocations that can be tracked by spatial anchors.

### 14. Final decision
Keep as a high-value reference and likely recurring baseline for world-model discussions. The paper does not solve persistent state, but it names the failure with the right experimental knife.
