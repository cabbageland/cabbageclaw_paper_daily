# OneWorld: Learning Consistent Physics Across Actions in World Models

## Basic info

* Title: OneWorld: Learning Consistent Physics Across Actions in World Models
* Authors: Ke He, Yichen Ding, and Bin Yang
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2609.30946
* Date surfaced: 2026-09-28
* Why selected in one sentence: It gives a concrete training and evaluation mechanism for checking whether multiple action-conditioned futures from one initial scene imply the same hidden physics.

## Quick verdict

**Must read**

This is directly relevant because it attacks a world-model failure that ordinary video metrics can hide. The main contribution is not prettier prediction; it is a shared-world consistency criterion and an independent simulator-based evaluation protocol.

## One-paragraph overview

OneWorld starts from the observation that action-conditioned video world models usually generate each candidate future independently. Each rollout can look plausible, while different actions from the same initial scene imply incompatible friction, mass, gravity, deformability, or fluidity. The paper introduces a physical mechanism interpreter that maps each action-outcome branch to a distribution over latent mechanisms, aggregates those branch distributions into a prior-corrected shared-world evidence score, and uses that score for both flow-training loss and sampling-time guidance. The evaluation then asks whether several predicted futures can be jointly explained by one simulator physical configuration, not just whether each branch fits some configuration independently.

## Model definition

### Inputs
Inputs are an initial visual observation, a group of action sequences from the same initial world, noisy or estimated future video latents for each branch, and flow time.

### Outputs
The video model outputs future video latents for each action branch. The mechanism interpreter outputs a distribution over latent physical mechanisms for each branch, and the shared-world evaluator computes a compatibility score across the group.

### Training objective (loss)
The action-conditioned video backbone uses flow matching for branch-specific future prediction. The mechanism interpreter is trained with group-level same-world versus mismatched-world binary supervision using a log shared-world evidence score. After the interpreter is frozen, the video model is trained with `L = Lflow + lambda_shared Lshared`, where `Lshared = -log(C_tau + epsilon)`.

### Architecture / parameterization
The backbone is an action-conditioned latent flow model initialized from ACWM-DiT and using a frozen Wan2.1 VAE. The mechanism interpreter parameterizes branch posteriors as additive evidence updates to an initial-scene prior in Gaussian natural-parameter space. Sampling-time guidance adds a gradient of log shared-world evidence to the branch velocity field.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It addresses shared-world inconsistency: several action-conditioned futures from one initial scene can each be plausible while requiring mutually incompatible hidden physical properties.

### 2. What is the method?
For a group of intervention branches, OneWorld estimates a clean future latent for each branch, infers a latent mechanism posterior from each action-outcome pair, computes a shared-world evidence score, and uses that score to train and guide the video generator toward branch futures with common physical support.

### 3. What is the method motivation?
Planning compares alternative interventions from the same world. If alternative predictions imply different underlying worlds, a planner is comparing artifacts rather than real alternatives.

### 4. What data does it use?
The controlled experiments use Push Cube, Push Rope, and Pour Water settings following ACWM-Phys interaction setups. The broader qualitative study includes RoboDesk-style action cases.

### 5. How is it evaluated?
The paper reports masked MSE for single-rollout prediction and a simulator-based shared-world evaluation. It computes individual best-fit physical error per branch, a shared best-fit error requiring one physical configuration for all branches, and the shared-world gap between them.

### 6. What are the main results?
Relative to ACWM-DiT, OneWorld reduces the mean shared-world gap from 0.02382 to 0.00374, an 84.3% reduction, while also slightly improving mean masked MSE. It beats Vid2World, CoCo, Twin Rollouts, Shared Noise, and direct Posterior Alignment on the shared-world consistency metric.

### 7. What is actually novel?
The novelty is coupling branches through compatibility of inferred physical explanations rather than matching videos, sharing noise, or forcing identical mechanism posteriors. The shared-world gap is also a useful evaluation primitive.

### 8. What are the strengths?
The paper separates individual physical fit from cross-intervention consistency. The evaluator is simulator-based and independent of the learned compatibility score, which reduces the risk of training and evaluation circularity.

### 9. What are the weaknesses, limitations, or red flags?
The experiments are controlled and simulator-heavy. The latent mechanism coordinates are not named physical variables, so interpretability is operational rather than semantic. Scaling this to open-world video may require better physical state extractors and richer intervention groups.

### 10. What challenges or open problems remain?
The hard next problem is applying shared-world consistency to messy real scenes where physical factors are partially observable, contact events are ambiguous, and the simulator family is unavailable or incomplete.

### 11. What future work naturally follows?
Use shared-world gaps as a planner reliability signal, extend the mechanism interpreter to real robot/video datasets, and test whether branch groups improve action selection rather than only video metrics.

### 12. Why does this matter for cabbageland?
Cabbageland wants world models that preserve the hidden variables a planner needs. OneWorld gives a compact way to ask whether imagined futures are compatible alternatives from one state.

### 13. What ideas are steal-worthy?
Evaluate multiple futures jointly. Penalize incompatible hidden explanations, not just bad pixels. Treat uninformative interventions as uncertain evidence rather than forcing every branch posterior to match.

### 14. Final decision

**Preserve.** This is the strongest paper of the day because it gives both a mechanism and a test for a failure that planning-facing world models cannot afford.
