# SplitJEPA: Learning Invariant and Variant Latent Worlds without Reconstruction

## Basic info

* Title: SplitJEPA: Learning Invariant and Variant Latent Worlds without Reconstruction
* Authors: Ruijin Hua, Zichuan Liu, Zhuokai Zhao, Yujia Zheng
* Year: 2026
* Venue / source: arXiv preprint
* Link: https://arxiv.org/abs/2610.12349
* Date surfaced: 2026-10-09
* Why selected in one sentence: It gives reconstruction-free latent world modeling a concrete mechanism for separating invariant task state from variant execution or visual nuisance.

## Quick verdict

* Must read

This is the sharpest paper in today's batch. The main contribution is not another JEPA wrapper; it is the claim that prediction can recover the full latent state while matched correspondences orient that latent into invariant and variant blocks. The proof rests on stationary Gaussian predictive dynamics and sufficient variation, and the robotics experiments are still relatively small, but the mechanism is exactly the sort of representation discipline cabbageland cares about.

## One-paragraph overview

SplitJEPA studies how to learn a latent world representation that separates what should remain fixed across matched observations from what is allowed to vary. A standard reconstruction-based model can hide many latent parameterizations behind the same pixels, and a JEPA-style predictive model can recover useful latent state without reconstructing pixels but still leave a global rotational ambiguity that mixes invariant and variant factors. SplitJEPA adds an invariant-block consistency loss on matched pairs, together with predictive alignment and variance preservation, so the learned representation is organized into an invariant block and a variant block. Synthetic experiments test the block-identifiability claim directly, and ManiSkill PickCube/PushCube experiments show that policies using the invariant block are much more robust to camera and lighting shifts.

## Model definition

### Inputs

The representation learner receives observations or observation pairs generated from a latent dynamical system. In the robotic experiments, observations are 128 x 128 RGB frames from ManiSkill PickCube and PushCube, organized into matched groups that share task content such as object identity, initial object pose, and goal pose while varying robot initialization, execution trajectory, approach direction, camera, timing, or lighting. The robotic predictor also receives actions when predicting the next representation.

### Outputs

The encoder outputs a partitioned representation `r = [r_H; r_L]`, where `r_H` is intended to encode invariant task content and `r_L` is intended to encode variant factors. In robotics, this representation feeds action prediction or closed-loop policy evaluation.

### Training objective (loss)

The core representation objective combines predictive alignment, invariant consistency, and variance preservation: `L_repr = L_pred + lambda_inv L_inv + lambda_var L_var`. `L_pred` aligns predicted representations across predictive pairs, `L_inv` forces the designated invariant block to agree across matched pairs, and `L_var` prevents collapse. In the robotic implementation, an action-conditioned predictor maps `(r_t, a_t)` to a stop-gradient target `r_{t+1}`.

### Architecture / parameterization

The theory is stated abstractly for a representation map. The robotic implementation uses an ImageNet-initialized ResNet-50 encoder over RGB observations and a partitioned representation with equal-size invariant and variant blocks: 64+64 dimensions for PickCube and 128+128 dimensions for PushCube. The method is decoder-free; no observation reconstruction objective is used.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It asks how a reconstruction-free latent world model can learn not only a predictive state, but also the organization of that state into invariant factors that should be stable for a task and variant factors that capture nuisance or execution differences.

### 2. What is the method?

First, use JEPA-style predictive alignment to recover the full latent state up to a global orthogonal transformation. Second, use matched pairs that share the invariant content while varying the variant factors to force the invariant block to agree across those pairs. Under sufficient variation, this removes cross-block mixing and identifies invariant and variant subspaces up to independent within-block rotations.

### 3. What is the method motivation?

Pixel reconstruction makes the latent explain every visual detail before it can become useful, which can entangle viewpoint, lighting, robot configuration, and task state. Prediction without reconstruction avoids that cost, but prediction alone still leaves a mixed latent. The paper's motivation is to recover useful structure directly in representation space.

### 4. What data does it use?

The paper uses controlled synthetic nonlinear dynamical systems and two ManiSkill3 manipulation tasks: PickCube-v11 and PushCube-v12. Each robotic task uses 800 successful trajectories organized into 100 matched groups of eight, with 20% held out for validation. Evaluation includes in-distribution settings and OOD camera, lighting, and combined visual shifts.

### 5. How is it evaluated?

Synthetic evaluation measures block recovery and latent identification. Robotic evaluation measures offline action prediction and closed-loop success under in-distribution and OOD visual conditions. The paper compares raw pixels, R3M, LeJEPA, the invariant block alone, and the invariant plus variant blocks. Ablations remove predictive learning, invariant consistency, or diversity.

### 6. What are the main results?

On PushCube, the invariant block reaches 99.3 SR@10cm in-distribution, 71.5 under camera shift, 99.7 under lighting shift, and 64.5 under combined visual shift. R3M gets 97.7, 48.0, 90.7, and 25.8; raw pixels get 98.0, 12.8, 98.3, and 12.7. Removing the invariance term drops PushCube camera-shift performance from 71.5 to 19.7. On PickCube, the invariant block improves over baselines but the task remains harder, with 45.0 SR@10cm in-distribution and 28.3 under combined visual shift.

### 7. What is actually novel?

The novelty is the separation between latent recovery and latent block organization in a decoder-free JEPA setting. The paper shows that prediction can recover the complete latent state, while matched-pair invariant consistency can identify the invariant-variant partition without reconstructing observations.

### 8. What are the strengths?

The paper is unusually explicit about what prediction alone does and does not identify. The theorem names the remaining orthogonal ambiguity, the sufficient-variation condition is intuitive, and the robotics experiments test the claimed operational benefit under visual nuisance shifts. The ablation showing invariance removal damaging OOD performance is especially useful.

### 9. What are the weaknesses, limitations, or red flags?

The theory depends on idealized predictive dynamics and population assumptions. The matched-pair construction is doing real work; if the correspondences are weak, biased, or fail to span variant directions, the guarantee does not apply. The robotics tasks are table-top simulations, and PickCube shows that separating visual nuisance does not solve contact-rich manipulation difficulty.

### 10. What challenges or open problems remain?

The big open problem is how to obtain matched correspondences automatically in messier data. The method also needs larger-scale tests where invariant factors are task-relative and may change across objectives. A useful next step would test whether the learned blocks stay stable across domains, cameras, objects, and longer-horizon policies.

### 11. What future work naturally follows?

Use stronger correspondence mining, extend the factorization beyond two blocks, make the downstream policy choose which blocks to route through, and evaluate the representation inside learned world-model planning rather than only policy/action prediction. It would also be worth combining this with causal or controllability-based factorization.

### 12. Why does this matter for cabbageland?

Cabbageland cares about representations that make downstream decisions more controllable and less brittle. SplitJEPA is a clean example of how to turn "invariant representation" from a slogan into a training condition, a theorem, an ablation, and an OOD behavior difference.

### 13. What ideas are steal-worthy?

Separate "recover the state" from "orient the state." Use matched pairs to define the task-relative invariant block. Test the representation by routing policies through only the invariant block and corrupting or shifting the variant factors. Treat sufficient variation as a data requirement, not a footnote.

### 14. Final decision

Preserve. This is a high-signal representation paper and the most relevant paper of the day.
