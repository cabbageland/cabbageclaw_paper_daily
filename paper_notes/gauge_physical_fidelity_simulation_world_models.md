# GAUGE: A Measurement-Grounded Benchmark for Physical Fidelity in Simulation Engines and Video World Models

## Basic info

* Title: GAUGE: A Measurement-Grounded Benchmark for Physical Fidelity in Simulation Engines and Video World Models
* Authors: Shuai Wang, Yaxin Feng, Xuekun Jiang, Shihan Tian, Ningyu Yan, Xing Shen, Chaoyang Lyu, Hui Wang, Yunsong Zhou, Hanqing Wang, Jiangmiao Pang, Yang Xiang, Xing Gao, Chunhua Shen, Weinan Zhang
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.05948
* Date surfaced: 2026-08-08
* Why selected in one sentence: It measures simulators and video world models against the same real-world physical reference instead of letting each paper choose its own flattering notion of plausibility.

## Quick verdict

* Highly relevant

I inspected the arXiv HTML full text. This is one of the better embodied/world-model evaluation papers because it is not hypnotized by visual realism. The core contribution is measurement discipline: real trajectories, calibrated parameters, and separate checks for law-form agreement versus actual physical parameter fidelity.

## One-paragraph overview

GAUGE is a unified benchmark for physical fidelity across both traditional simulators and generative video world models. The paper builds 22 controlled task families spanning rigid bodies, flexible cables, textiles, and volumetric deformables, backed by about 1,560 real motion-capture trials, calibrated physical metadata, and uncertainty annotations. Numerical engines such as Isaac Sim, Genesis, and Newton are reconstructed against the same real tasks and scored with generalized trajectory errors. Video world models are given an initial frame and prompt, their generated motion is tracked, and the resulting trajectories are tested for both expected equation form and the correctness of inferred physical parameters. The punchline is blunt: no engine is uniformly faithful, and video world models can look structurally right while still getting accelerations, momentum transfer, or oscillation timing wrong.

## Model definition

### Inputs
The benchmark takes calibrated real-world task setups, physical metadata, repeated motion-capture trials, simulator configurations, and initial-frame-plus-prompt inputs for world-model evaluation.

### Outputs
It outputs tracked trajectories, task-specific observables, normalized sim-to-real discrepancies, and world-model physical-consistency metrics that separate law-form agreement from parameter accuracy and temporal stability.

### Training objective (loss)
The benchmark itself has no trainable model or loss. It evaluates external simulators and video generation models.

### Architecture / parameterization
A benchmark and evaluation pipeline with two branches: matched real-versus-sim trajectory comparison for numerical engines, and initial-frame-conditioned video rollout plus tracked-law analysis for world models.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to measure physical fidelity in a way that is comparable across simulators and video world models. Existing work often scores visual plausibility or human judgments, which tells you almost nothing about which physical mechanism broke.

### 2. What is the method?
The method is a benchmark design. It collects controlled real-world trajectories with calibrated parameters, then evaluates simulators by direct trajectory discrepancy and world models by tracked motion, law-form consistency, and parameter recovery.

### 3. What is the method motivation?
Real-to-sim and world-model training only make sense if the environment gets the dynamics right. A visually nice rollout that breaks contact, momentum transfer, or deformation physics is actively misleading.

### 4. What data does it use?
GAUGE contains 22 task families across rigid bodies, textiles, cables, and deformables, with roughly 1,560 motion-capture trials. Physics-engine evaluation covers 14 task families, while world-model evaluation focuses on 5 rigid-body settings.

### 5. How is it evaluated?
Simulators are compared to real trajectories using generalized trajectory errors and task-specific metrics such as RMSE, DTW, momentum-transfer efficiency, and period fidelity. World models are evaluated by tracking generated motion and checking both physical-law form and parameter accuracy.

### 6. What are the main results?
No engine dominates across regimes. Isaac Sim is strong on several rigid tasks, Genesis does better on some textile and deformable cases, and Newton is best only in selected deformation settings. Even then, hard cases remain bad: the best bouncing-ball simulator result is still 15.63 times the real baseline RMSE, and Newton’s-cradle momentum transfer is only 0.20 or 0.26 for the valid engines. On the generative side, world models can match the right equation family while still recovering wrong accelerations, momentum transfer, or oscillation timing.

### 7. What is actually novel?
The real novelty is not another physics benchmark in the abstract. It is using one real-world measurement base to evaluate both classical simulators and generative world models, while separating structural-law agreement from actual parameter correctness.

### 8. What are the strengths?
It is grounded, quantitative, and cross-regime. The task coverage is broad enough to expose solver specialization, and the world-model track is more diagnostic than "does this look plausible?" style evaluation.

### 9. What are the weaknesses, limitations, or red flags?
The world-model track is narrower than the simulator track and currently focuses on rigid-body settings. The benchmark still depends on tracking quality and chosen observables. It diagnoses fidelity, but it does not yet tell you how fidelity errors interact with downstream policy learning.

### 10. What challenges or open problems remain?
The obvious next challenge is extending world-model evaluation to richer contact-rich and deformable settings without collapsing into unreliable tracking. Another is tying these fidelity metrics to downstream control or planning errors.

### 11. What future work naturally follows?
More interactive embodied tasks, policy-level consequence studies, benchmark expansions for deformable world models, and training objectives that explicitly optimize the measured failure modes.

### 12. Why does this matter for cabbageland?
This is the right evaluation instinct for world models: do not trust rollouts because they look convincing. Measure which mechanism is wrong, and distinguish equation-shape mimicry from actually correct dynamics.

### 13. What ideas are steal-worthy?
Use the same ground-truth reference for both classical simulators and generative models. Separate law-form consistency from parameter accuracy. Attach uncertainty annotations and calibrated metadata to physical benchmark tasks instead of treating the real world as an aesthetic reference.

### 14. Final decision
Keep as a preserved note. The benchmark is strong enough to matter for embodied-model evaluation and for thinking about how to test explicit state against physical reality.

## 6. Mandatory critical angles

GAUGE is strong on motivation, evaluation fairness, and failure-mode visibility. It is not a modular algorithm paper, so controllability and interpretability show up through the benchmark design rather than a model architecture. The main limitation is scope imbalance: the simulator track is broader than the world-model track.

## 7. Writing style

The correct tone here is severe and practical. This paper is valuable because it refuses perceptual slop as evidence of physical correctness.

## 8. Repository output format

Saved as a preserved paper note because it is a solid reference point for how cabbageland should think about physically grounded evaluation of world models and simulators.
