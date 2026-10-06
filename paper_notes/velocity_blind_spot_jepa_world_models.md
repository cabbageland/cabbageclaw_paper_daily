# Frozen in a Frame: The Velocity Blind Spot in JEPA World Models

## Basic info

* Title: Frozen in a Frame: The Velocity Blind Spot in JEPA World Models
* Authors: Tinghe Zhang, Chunyu Liu, Yu Leon Liu, Zerui Zhao, Jiaheng Chen, Yucheng Xiao, Jiaxing Li, Yunlong Wang, Alex Lamb
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2610.04585
* Date surfaced: 2026-10-06
* Why selected in one sentence: It proves that next-frame JEPA targets built from single rendered frames cannot identify velocity, then tests and repairs the failure with an explicit pose/motion split.

## Quick verdict

* Must read

This is the sharpest paper in today's batch because it does not merely report a world-model failure; it explains why the representation target cannot contain the variable the task needs. The TI-JEPA fix is intentionally small, but the diagnostic package is the real value. The downstream wins are still scoped, especially outside controlled environments, but the representational critique is clean enough to keep.

## One-paragraph overview

The paper studies action-conditioned JEPA world models whose encoder maps each frame to a latent and whose predictor learns the next frame's latent from recent latents and actions. The authors show that if a renderer maps instantaneous configuration to a frame, then any single-frame embedding is a function of configuration only and cannot identify instantaneous velocity unless velocity is already determined by position. They confirm this on released LeWM checkpoints, where position is linearly decodable but velocity is at chance, and introduce TI-JEPA, which encodes pose from frames and an explicit finite-difference motion code from a short pose window. The paper then tests the fix with velocity probes, opposite-velocity rollout experiments, and stop-at-goal planning tasks.

## Model definition

### Inputs

The baseline JEPA consumes image observations and actions. Official LeWM-style predictors may receive a short history window, but the target remains a single-frame embedding. TI-JEPA consumes a short frame window for encoding, derives pose codes per frame, derives a motion code from finite differences of pose codes, and feeds the current pose code, motion code, and action into a memoryless predictor.

### Outputs

The baseline emits a predicted next-frame latent. TI-JEPA emits predicted next pose and motion codes. The evaluation reads these codes through velocity probes, branch-separation rollouts, and planning objectives.

### Training objective (loss)

The baseline follows the LeWM JEPA objective: squared prediction error between the predicted next latent and the target next-frame latent, plus SIGReg regularization on the latent distribution. TI-JEPA supervises both predicted pose and predicted motion codes with squared latent prediction losses, applies SIGReg to the pose code, and uses a separate variance floor for the motion code.

### Architecture / parameterization

The baseline is an action-conditioned JEPA with an image encoder and an AdaLN-conditioned autoregressive transformer predictor. TI-JEPA uses a shared pose encoder, a bias-free MLP over finite pose differences to produce a motion code, and a memoryless predictor over pose, motion, and action. The paper tests small CNN variants, official-scale ViT-Tiny plus AdaLN-transformer variants, recurrent-aggregator controls, and real dm_control Reacher photographs.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It targets a missing-state problem in JEPA world models. If the predicted representation is a single-frame embedding, the model may be forced to predict dynamics without an identifiable representation of velocity.

### 2. What is the method?

The paper first proves the identifiability issue, then introduces RateIdent diagnostics and TI-JEPA. TI-JEPA splits the latent into a pose code and a finite-difference motion code, then predicts both forward under action.

### 3. What is the method motivation?

Second-order physical systems require velocity. A single rendered frame without motion blur contains configuration but not velocity. Putting recent frames into the predictor can help rollout prediction, but it does not make the target representation itself carry velocity.

### 4. What data does it use?

The diagnostic suite uses official LeWM checkpoints and benchmarks including PushT, Reacher, Cube, and TwoRoom. The paper also builds controlled InertiaBall, Pendulum, and CartPole settings, runs official-scale CartPole and Pendulum experiments, and trains on real dm_control Reacher photographs.

### 5. How is it evaluated?

RateIdent has three main protocols: probe ladders for velocity recoverability, kill experiments comparing rollouts from identical frames with opposite velocity, and stop-at-goal planning tasks that require velocity-aware behavior. The paper also compares against matched-memory baselines and a recurrent-aggregator alternative.

### 6. What are the main results?

On official LeWM checkpoints, every embedding-based velocity probe sits at or below chance while position probes reach roughly 0.94 to 0.98 R-squared. In controlled environments, TI-JEPA's explicit motion code has the only consistently useful probe signal and improves stop-at-goal planning; closed-loop final-distance improvements include 55% on Pendulum and 64% on CartPole versus the matched memoryless baseline. On real Reacher photographs, TI-JEPA produces the largest branch-separation margin over the history baseline, though velocity-sign accuracy remains near chance.

### 7. What is actually novel?

The novelty is the target-level critique. The paper is not just adding a memory window; it says the prediction target itself is wrong when velocity matters, then provides a minimal structured target that restores identifiability.

### 8. What are the strengths?

The formal argument is simple and checkable. The evaluation probes the specific hidden variable rather than treating downstream success as a proxy. The authors document several self-caught confounds, including frame-level leakage and oversized action budgets.

### 9. What are the weaknesses, limitations, or red flags?

The positive planning results are strongest in controlled synthetic environments. Real PushT downstream planning is a null result at the reported scale, and real Reacher shows strong branch separation but not clean velocity-sign readout. TI-JEPA is a structural fix for one missing variable, not a complete world-model recipe.

### 10. What challenges or open problems remain?

The open question is whether explicit motion channels improve closed-loop physical control at scale, with real robot data, contact, occlusion, and multimodal goals. Another question is how this interacts with recurrent belief-state models that never expose single-frame embeddings as the planning state.

### 11. What future work naturally follows?

Use RateIdent-style diagnostics on other self-supervised video world models. Extend the pose/motion split to richer physical variables: contact, mass, friction, object permanence, and uncertainty. Test whether explicit motion latents help policies, not just latent planners.

### 12. Why does this matter for cabbageland?

Cabbageland cares about state that carries the claim. This paper is exactly that: it shows the representation cannot carry velocity, then changes the interface so velocity becomes a named, auditable object.

### 13. What ideas are steal-worthy?

Before scaling a world model, prove whether the target representation can identify the variables needed by the downstream task. Use opposite-state counterfactuals that are visually identical at time zero but dynamically different afterward. Separate "predictor has history" from "state contains the variable."

### 14. Final decision

Preserve. This is a direct hit for world models, explicit state, temporal representation, and planning diagnostics.
