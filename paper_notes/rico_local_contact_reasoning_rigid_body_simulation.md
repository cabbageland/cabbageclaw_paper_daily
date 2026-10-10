# RiCo: Neural Simulation of Rigid-Body Interactions via Local Contact Reasoning

## Basic info

* Title: RiCo: Neural Simulation of Rigid-Body Interactions via Local Contact Reasoning
* Authors: Ruixiang Ouyang, Guanren Qiao, Fansen Meng, Yueci Deng, Ruixing Jin, Kui Jia, Guiliang Liu
* Year: 2026
* Venue / source: arXiv preprint
* Link: https://arxiv.org/abs/2610.12333
* Date surfaced: 2026-10-10
* Why selected in one sentence: It models rigid-body dynamics through sparse local surface contacts rather than diffuse object-level interaction attention.

## Quick verdict

* Highly relevant

RiCo is a good physical-world-model paper because it pushes representation down to the interaction scale that matters. Contact is local, signed, and geometry-dependent; the method encodes exactly that instead of asking a global object token to infer it later. The sim-to-real section is preliminary and the domain is passive rigid bodies, but the mechanism is pointed in the right direction.

## One-paragraph overview

RiCo is a neural simulator for multi-object rigid-body dynamics. Each object is represented by tracked surface points, normals, center of mass, and physical properties such as inverse mass, friction, and restitution. For each surface point, RiCo builds a sparse neighborhood of nearby external surface points or static environment candidates, encodes relative direction, signed offset, normals, relative motion, and physical properties, then uses a point transformer to reason within the rigid body. An anchor decoder predicts displacements at a few surface anchors and recovers one rigid transform for the whole object. This yields better long-horizon rollouts and much cleaner contact fidelity than object-level baselines.

## Model definition

### Inputs

RiCo receives two consecutive scene states for multiple rigid objects, plus static environment geometry and per-object physical properties. Each object state includes surface sample positions, normals, center of mass, finite-difference motion, and physical parameters. Contact neighborhoods include nearby points from other objects or analytic static surfaces.

### Outputs

The model predicts the next scene state by outputting rigid-body motion updates. It decodes displacements at selected anchor points, fits a single rigid transformation per object, applies that transform to the object's surface points, and rolls the predicted state forward autoregressively.

### Training objective (loss)

The paper trains RiCo as a supervised dynamics model on simulated trajectories. The accessible text describes offline supervised training and trajectory targets; the exact scalar loss is not summarized in the main text beyond predicting rigid transformations from anchor displacements and evaluating position/orientation rollout errors. The likely objective is regression on next-step motion/state, but the note should not pretend a more specific formula than the paper states in the inspected sections.

### Architecture / parameterization

The architecture has three main stages: sparse contact-neighborhood construction, contact-conditioned point encoding with intra-object transformer reasoning, and anchor-query decoding for rigid motion prediction. The contact descriptor is 14-dimensional and includes relative direction, signed offset, candidate normal, relative displacement, candidate physical properties, and static/dynamic indicator. The point state is 15-dimensional and includes point position relative to center, motion, normal, physical properties, and displacement from the initial surface point.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It tries to learn accurate multi-object rigid-body dynamics, especially collisions and contact interactions where small local surface relationships create abrupt changes in object translation and rotation.

### 2. What is the method?

For each object surface point, RiCo queries nearby candidate contact points from other objects and the environment. It encodes local geometry, signed penetration-like offsets, relative motion, normals, and physical properties. A shared point transformer propagates these contact-conditioned features across the rigid body, and an anchor decoder converts them into a whole-object rigid transform.

### 3. What is the method motivation?

Rigid-body contact is local: only nearby surfaces exchange contact forces. Dense all-pairs scene reasoning is wasteful, while whole-object attention can blur the exact surface geometry that determines collisions. RiCo keeps the local contact signal explicit, then lets the rigid body integrate those local effects.

### 4. What data does it use?

The main experiments use MOVi-A, MOVi-B, and MOVi-Sphere rigid-body simulation benchmarks. Generalization tests train on one geometry distribution and test on another. Large-scale tests train on small MOVi-B scenes with 3 to 10 objects and evaluate zero-shot on 270-object scenarios. A real-world billiards experiment uses simulated training and five real-world multi-ball collision sessions for zero-shot transfer.

### 5. How is it evaluated?

The paper reports position RMSE and orientation RMSE over autoregressive horizons of 50, 75, and 100 frames for MOVi benchmarks, 75 and 100 frames for cross-geometry generalization, and 120 to 360 steps for large-scale scenes. It also introduces ground-truth-relative penetration-time ratio and mean penetration depth to measure contact fidelity while accounting for overlap already present in ground-truth trajectories.

### 6. What are the main results?

On MOVi-A at 100 frames, RiCo reaches 0.115 m position RMSE and 11.40 deg orientation RMSE, compared with RigidFormer at 0.177 m and 18.32 deg. On MOVi-B at 100 frames, RiCo reaches 0.111 m and 9.54 deg, compared with RigidFormer at 0.161 m and 15.33 deg. For contact fidelity on MOVi-B, RiCo gets 11.0% ground-truth-relative penetration-time ratio and 2.22 mm mean penetration depth, versus 44.8% and 267.70 mm for the RigidFormer reimplementation. Replacing signed offset with absolute distance raises penetration time from 11.0% to 23.6% and mean depth from 2.22 mm to 7.86 mm. Increasing point resolution from 512 to 1024 barely changes trajectory RMSE but improves contact fidelity from 23.4% to 11.0% and 6.21 mm to 2.22 mm. In real billiards, RiCo is worse than the physics engine but shows preliminary transfer.

### 7. What is actually novel?

The novelty is the sparse local contact representation plus intra-object reasoning pipeline for rigid-body neural simulation. The signed local geometry is especially important because the ablation shows it matters more for physical consistency than for raw trajectory RMSE.

### 8. What are the strengths?

The paper evaluates contact fidelity directly, not just position error. It demonstrates cross-geometry transfer, scaling to much larger scenes than training, and an initial sim-to-real check. The method also exploits high-resolution geometry in the metric that matters: penetration behavior.

### 9. What are the weaknesses, limitations, or red flags?

The framework is limited to passive rigid-body dynamics. It does not address deformable objects, actuated systems, tactile feedback, or policy-conditioned manipulation. The real-world evidence is small and still worse than the corresponding physics engine. The exact supervised loss details are less prominent than the architecture and evaluation, so implementation replication would require reading the appendix carefully.

### 10. What challenges or open problems remain?

The obvious challenge is extending local contact reasoning to deformable objects, articulated bodies, and action-conditioned environments. Another open problem is integrating this kind of contact module into visual world models where surface state is inferred, uncertain, and partially occluded.

### 11. What future work naturally follows?

Combine local contact reasoning with learned 3D reconstruction or object state estimators, add action-conditioned control inputs, and use contact-fidelity metrics as training signals rather than only evaluation metrics. A hybrid model could use video to infer object state and RiCo-like contact reasoning to predict dynamics.

### 12. Why does this matter for cabbageland?

Cabbageland cares about world models whose state supports action consequences. RiCo is a concrete reminder that contact should be represented at the surface scale, not dissolved into a global latent and hoped back into existence.

### 13. What ideas are steal-worthy?

Use sparse local contact neighborhoods. Encode signed contact geometry. Measure penetration relative to ground truth, not only rollout RMSE. Let local contacts influence a whole-object rigid transform through intra-object reasoning.

### 14. Final decision

Preserve. This is a strong physical-mechanism paper with a useful contact-fidelity lesson.
