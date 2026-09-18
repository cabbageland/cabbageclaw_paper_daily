# Can 4D Foundation Models Remember?

## Basic info

* Title: Can 4D Foundation Models Remember?
* Authors: Guangzhao He, Hadar Averbuch-Elor, Wei-Chiu Ma
* Year: 2026
* Venue / source: arXiv:2609.20819
* Link: https://arxiv.org/abs/2609.20819
* Date surfaced: 2026-09-18
* Why selected in one sentence: It tests whether 4D models maintain object-centric state after objects leave view, rather than rewarding visible-frame reconstruction quality.

## Quick verdict

* Highly relevant

This is a strong world-model evaluation paper. It does not propose a new memory architecture, but it asks the right question and gives it a reference-based benchmark. This note is based on the full arXiv PDF text.

## One-paragraph overview

The paper introduces PersistBench, a benchmark for visual memory in 4D foundation models. The core move is using 360-degree videos as omniscient ground truth: a model receives perspective crops where objects can leave the field of view, while the benchmark retains reference observations of the hidden objects. The evaluation separates object permanence, motion continuity, and appearance preservation. Across 12 public 4D reconstruction, camera-controlled video, and video-to-360 models, performance drops substantially once the target object becomes invisible.

## Model definition

### Inputs

PersistBench gives evaluated models observed perspective video segments derived from 360-degree video. The hidden reference comes from the full 360-degree recording.

### Outputs

Depending on the evaluated model class, models output generated video, novel views, or dynamic view reconstructions. PersistBench scores target objects on visible and invisible segments.

### Training objective (loss)

PersistBench itself is an evaluation benchmark, not a trained model. The evaluated models use their original training objectives. The benchmark scoring pipeline measures object permanence, motion continuity, and appearance preservation through off-the-shelf tracking, matching, and perceptual components.

### Architecture / parameterization

The paper evaluates 12 public models across 4D reconstruction, camera-controlled video generation, and video-to-360 generation. It does not introduce a new learnable architecture.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Existing 4D benchmarks mostly measure reconstruction or perceptual quality where content remains visible. They cannot tell whether a model remembers the state of an object after it leaves view.

### 2. What is the method?

Use 360-degree videos to construct input-reference pairs. The model sees a limited field-of-view input, while the benchmark uses withheld 360-degree observations as reference ground truth for objects that become hidden.

### 3. What is the method motivation?

Persistent object-centric memory is different from interpolation. A model that only uses visible pixels can look good on standard view-synthesis metrics but fail when it must carry unseen object state.

### 4. What data does it use?

The dataset is built from YouTube 360-degree videos, curated into segments with target objects and camera trajectories. The paper includes static and dynamic object subsets.

### 5. How is it evaluated?

The benchmark evaluates object permanence, motion continuity, and appearance preservation on visible versus invisible segments. It also reports model-category analyses, metric correlations, temporal stability, human-study support, and longer-video experiments.

### 6. What are the main results?

All evaluated models suffer substantial drops on invisible segments. Explicit projection or geometric conditioning helps: models such as GEN3C, TrajectoryCrafter, and NeoVerse tend to perform better on invisible segments than less explicitly conditioned approaches. The paper also finds that motion continuity is less correlated with object permanence and appearance than those two are with each other.

### 7. What is actually novel?

The novelty is the reference-based visual-memory setup. By using omnidirectional video as ground truth, the benchmark can score out-of-view object state instead of relying on plausibility or internal consistency.

### 8. What are the strengths?

The benchmark asks a capability question that standard video metrics dodge. The metrics are decomposed enough to show distinct memory failures. The paper also names the likely data-bias problem: most video training data keeps target objects visible.

### 9. What are the weaknesses, limitations, or red flags?

The pipeline depends on off-the-shelf pose estimation, object matching, tracking, and scoring models. The dataset distribution reflects available 360-degree video. The benchmark does not itself prove how to build persistent memory; it mostly shows current models do not have enough of it.

### 10. What challenges or open problems remain?

The next step is training data and architectures that force occlusion, disappearance, and reappearance. Another open question is how to evaluate models that output non-renderable 4D state such as point clouds or implicit scene graphs.

### 11. What future work naturally follows?

Curate memory-aware 4D training data, add explicit object or geometric state carriers, and test whether improvements on static object memory transfer to dynamic memory as the correlations suggest.

### 12. Why does this matter for cabbageland?

Cabbageland cares about world models whose state survives outside the current pixels. PersistBench gives a clean way to catch models that reconstruct the visible scene but fail to remember the world.

### 13. What ideas are steal-worthy?

Use omniscient data sources to score hidden state. Separate object permanence, motion continuity, and appearance preservation. Do not confuse visible-frame quality with memory. Evaluate static and dynamic memory separately.

### 14. Final decision

Preserve. This is not a mechanism paper, but it is a valuable evaluation lens for world-model claims.
