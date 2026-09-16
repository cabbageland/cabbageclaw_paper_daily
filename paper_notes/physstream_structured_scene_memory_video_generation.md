# PhysStream: Streaming Physics-Grounded Video Generation with Structured Scene Memory and Fine-Grained Motion Control

## Basic info

* Title: PhysStream: Streaming Physics-Grounded Video Generation with Structured Scene Memory and Fine-Grained Motion Control
* Authors: Chuhao Chen, Peter Wonka, Chaoyang Wang, Chen Wang, Qiao Feng, Sergey Tulyakov, Lingjie Liu
* Year: 2026
* Venue / source: arXiv:2609.17521
* Link: https://arxiv.org/abs/2609.17521
* Date surfaced: 2026-09-16
* Why selected in one sentence: It turns controllable video generation into sparse physical control plus online structured scene memory, which is much closer to a usable world-model interface than trajectory painting.

## Quick verdict

* Must read

This is the strongest paper in today's batch. It is not a generic "physics for video" paper; the useful idea is that an autoregressive generator should carry explicit scene history and accept sparse physical increments that can be applied mid-generation. This note is based on the full arXiv HTML text.

## One-paragraph overview

PhysStream is an image-to-video model for controllable tabletop dynamics. A user can apply sparse velocity-increment controls to specific objects at chosen timesteps, and the model generates future video with a structured memory derived online from prior generated frames. The memory has two main channels: positional maps from monocular depth and object-tracking maps from segmentation/tracking. The model is trained in two stages, first as a bidirectional motion-control model, then as a causal autoregressive model with scene memory. The result is a system that handles interactive multi-object control better than baselines that require full schedules, pixel-space drags, or external simulators whose state can diverge from the rendered scene.

## Model definition

### Inputs

The model takes an initial image or generated frame history, text/scene conditioning, sparse per-object velocity-increment controls, and structured scene-memory conditions derived from previous generated frames. The memory includes positional maps and object-tracking maps updated online.

### Outputs

The model outputs autoregressive future video frames. Evaluation also tracks physical-motion metrics, trajectory errors, failure rates, human preference, and long-horizon response to later control events.

### Training objective (loss)

The system is trained as a diffusion-style video generator with a motion-control conditioning stage and a causal autoregressive stage. The paper describes a two-stage recipe rather than a single new loss: Stage 1 learns motion-control conditioning, and Stage 2 introduces causal autoregressive training with structured scene memory.

### Architecture / parameterization

PhysStream builds on a video diffusion/DiT-style image-to-video backbone. The distinctive parameterization is the control and memory interface: sparse velocity-increment signals represent physical interventions, while positional and tracking maps provide structured scene memory. Inference repeatedly generates a segment, extracts memory from the generated frames, and feeds that memory back into the next segment.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Most controllable video methods either need the full control schedule before generation starts or use pixel-level signals that specify positions rather than dynamics. That is awkward for interactive generation, where a user wants to intervene late and where object motion should remain physically plausible after collisions and depth changes.

### 2. What is the method?

PhysStream uses sparse velocity increments as the user control and maintains structured scene memory from previously generated frames. It updates object tracks and positional maps online, then conditions the next autoregressive generation window on those maps plus any new velocity controls.

### 3. What is the method motivation?

Physical control should operate on a quantity the model can use to infer dynamics, not on a complete target trajectory. The model also needs remembered scene state because future motion depends on what has already happened, especially in multi-object scenes with depth motion and collisions.

### 4. What data does it use?

The main training and evaluation data are curated synthetic tabletop rigid-body scenes from SAGE/PyBullet/Blender-style simulation. The paper also evaluates in-the-wild prompts, real-world captures from OCID and Physics-IQ subsets, and non-rigid transfer examples after finetuning.

### 5. How is it evaluated?

The paper reports FVD, FVMD, trajectory ADE, median trajectory ADE, failure rate, scene/object/photometric consistency, VideoPhy semantic adherence and physical commonsense, human preference, real-world capture scores, non-rigid transfer, and long-horizon control response rates.

### 6. What are the main results?

On the multi-object interactive synthetic test, PhysStream improves FVMD to 787.0 versus 1183 for RealWonder, 1463 for Tora, and 3751 for FlashMotion. It also improves trajectory ADE to 40.24 versus 45.67 for FlashMotion and 60.91 for RealWonder, with a lower failure rate than all listed baselines. In in-the-wild comparison, PhysStream gets SA 5.00 and PC 4.15 and is preferred by human evaluators 91.8% on physics, 88.4% on motion, and 91.2% on visual quality. Ablations show the full memory model is best or near-best on almost all metrics, and positional maps matter more as depth displacement grows.

### 7. What is actually novel?

The novelty is the combination of interactive sparse physical control and online structured scene memory inside an autoregressive video generator. The method does not just condition on external trajectories; it updates internal scene evidence from its own generated frames and lets later controls act on that state.

### 8. What are the strengths?

The controls are physically meaningful, sparse, and interactive. The ablations isolate the memory channels rather than treating memory as branding. The evaluation includes physics-specific metrics and human preference, and the long-horizon test checks whether late controls still work after accumulated rollout drift.

### 9. What are the weaknesses, limitations, or red flags?

The validated core is tabletop rigid-body dynamics. The paper says the model still struggles with extremely complex motion, especially tumbling. Richer materials and non-rigid dynamics are encouraging but rely on additional finetuning rather than being a fully solved general physics generator. Memory extraction also depends on external depth/segmentation/tracking components.

### 10. What challenges or open problems remain?

The key challenge is scaling the same interface to messy scenes where object identity, contacts, deformability, and camera motion are less clean. Another open problem is making the memory update more native to the generative model rather than dependent on a stack of trackers and depth estimators.

### 11. What future work naturally follows?

Test this memory-control interface on navigation, object permanence, tool use, deformable objects, and richer camera control. Replace brittle external memory extractors with learned state estimators. Measure when memory maps become stale, wrong, or self-confirming during long rollouts.

### 12. Why does this matter for cabbageland?

Cabbageland cares about world models that expose and preserve state that can actually steer the future. PhysStream is useful because it treats memory and control as operational interfaces, not as interpretability labels.

### 13. What ideas are steal-worthy?

Represent user intervention as a sparse physical delta instead of a full trajectory. Feed back structured state extracted from generated frames. Evaluate whether late controls still work after long autoregressive history. Use depth-motion-stratified ablations to show when a state channel actually matters.

### 14. Final decision

Preserve. This is a mechanism-rich video world-model paper with a real design pattern for controllable generation.
