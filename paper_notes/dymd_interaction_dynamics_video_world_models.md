# DyMD: Preserving Interaction Dynamics through Distribution Matching Distillation in Few-Step Video World Models

## Basic info

* Title: DyMD: Preserving Interaction Dynamics through Distribution Matching Distillation in Few-Step Video World Models
* Authors: Haojun Xu, Jie Huang, Xin Lu, Mingchen Zhong, Zihao Fan, Linjiang Huang, and Si Liu
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2609.31349
* Date surfaced: 2026-09-28
* Why selected in one sentence: It diagnoses why DMD-style few-step video distillation keeps image quality but loses robot-object interaction dynamics.

## Quick verdict

**Highly relevant**

DyMD is useful because the failure mode is concrete and easy to miss: static or weak-motion outputs can score well visually while becoming useless as embodied futures. The paper's fixes are training-time only, so the inference budget stays at four denoiser evaluations.

## One-paragraph overview

Distribution Matching Distillation can compress a large video diffusion teacher into a few-step student, but in robotic videos the student may suppress the very motion needed for planning. DyMD analyzes the teacher and critic sides of the DMD update. Weak re-noising keeps the teacher posterior near motion-deficient student rollouts; stronger re-noising can restore motion but risks artifacts. Separately, stronger-motion rollouts have higher fake-score flow-matching loss, meaning the critic tracks them worse. DyMD adapts timestep sampling with temporal affinity-conditioned re-noising and allocates critic fitting effort with dynamics-guided fake-score tracking.

## Model definition

### Inputs
Inputs are first frames, text/action prompts, student-generated rollouts, paired target/reference videos for affinity computation, VAE latent dynamics for critic difficulty prediction, and noise levels/timesteps for DMD training.

### Outputs
The trained output is a four-step 1.3B image-to-video student. During training, auxiliary components produce per-rollout timestep sampling densities and critic loss weights.

### Training objective (loss)
The generator follows the DMD teacher-critic score-difference update. The critic is trained with a weighted flow-matching loss, where weights are predicted from noise-relative fitting difficulty. The difficulty predictor is trained online with a Huber loss against log flow-matching loss centered by a noise-bin baseline.

### Architecture / parameterization
The teacher is PF-Wan 14B, the student and fake-score model are initialized from Wan2.1-Fun 1.3B, temporal affinity uses frozen V-JEPA features, and critic difficulty uses VAE latent temporal descriptors passed through a lightweight MLP.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Few-step video distillation can preserve visual fidelity while erasing interaction dynamics, which makes the distilled model weak as a world-model backbone for embodied prediction and planning.

### 2. What is the method?
DyMD mixes a base timestep schedule with a teacher-velocity-turning prior according to each rollout's temporal affinity to target dynamics, then upweights critic fitting on predicted-hard motion-rich rollouts.

### 3. What is the method motivation?
Teacher guidance should spend more effort where motion can be recovered, and the fake-score critic should not underfit the stronger-motion samples that matter most for embodied use.

### 4. What data does it use?
The student is distilled from PF-Wan, a robotic-manipulation-focused video teacher. The paper evaluates on R-Bench, the robot subset of PAI-Bench-G, EZS-Bench, and two WorldArena/RoboTwin planning tasks.

### 5. How is it evaluated?
It reports R-Bench task-adherence consistency, PAI-Bench-G and EZS-Bench Domain/Space/Physics/Time/Quality scores, ablations for sampling and tracking, representation probes, and downstream action-planner success using frozen video backbones.

### 6. What are the main results?
At four denoiser evaluations, DyMD raises R-Bench TAC from 34.6 to 44.2, PAI-Bench-G Domain from 74.4 to 79.5, and EZS-Bench Domain from 73.3 to 76.2 versus Base DMD, while keeping PAI Quality at 78.1. In WorldArena, mean planning success rises from 16% to 34%.

### 7. What is actually novel?
The novelty is connecting motion loss to teacher posterior behavior and critic fitting difficulty, then using rollout-specific dynamics signals to allocate re-noising and critic weight.

### 8. What are the strengths?
The ablations separate adaptive sampling from critic tracking. The downstream planning test is important because it checks whether better videos actually help an embodied policy head.

### 9. What are the weaknesses, limitations, or red flags?
The teacher-velocity turning profile is teacher- and schedule-specific. Some quality/physics metrics can prefer near-static outputs, so the paper has to lean on task adherence and planning success to show the right gain.

### 10. What challenges or open problems remain?
The next step is making the re-noise prior less teacher-specific and testing whether the same dynamics preservation works in non-robot video, multi-object physical prediction, and longer horizons.

### 11. What future work naturally follows?
Use motion/dynamics-aware distillation objectives for video world models, track planning-relevant dynamics during compression, and evaluate distilled models with intervention or policy success instead of only visual metrics.

### 12. Why does this matter for cabbageland?
It is a warning about compression: a model can keep perceptual polish while dropping operational variables. That is exactly the kind of failure a downstream planner will expose.

### 13. What ideas are steal-worthy?
Look for score-fitting difficulty correlated with the behavior you care about. Route teacher correction based on rollout-specific fidelity. Treat static but pretty videos as a failure for embodied world models.

### 14. Final decision

**Preserve.** This is a strong video-world-model distillation note with a clear planning-facing failure mode.
