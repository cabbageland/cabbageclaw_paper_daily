# RD-JEPA: Predictive latent pretraining for few-trajectory transfer across reaction-diffusion equations

## Basic info

* Title: RD-JEPA: Predictive latent pretraining for few-trajectory transfer across reaction-diffusion equations
* Authors: Chenhao Si, Ming Yan
* Year: 2026
* Venue / source: arXiv:2609.29403
* Link: https://arxiv.org/abs/2609.29403
* Date surfaced: 2026-09-26
* Why selected in one sentence: It tests whether future-state latent prediction can transfer across reaction-diffusion systems when the target reaction law was excluded from pretraining.

## Quick verdict

* Useful

This is a narrow but clean representation-transfer paper. The good part is the controlled design: source systems, held-out governing equations, a no-predictive-latent control, and an architecture-matched scratch control. The caveat is that all systems are still related reaction-diffusion equations at fixed resolution and direct short forecast horizons.

## One-paragraph overview

RD-JEPA applies joint-embedding predictive architecture ideas to reaction-diffusion surrogate modeling. During self-supervised pretraining, an online encoder maps four observed fields into a context representation, an EMA target encoder represents a future field, and a lead-time-conditioned predictor estimates the future representation without reconstructing the field. The predictor includes diffusion-inspired neighborhood interaction and reaction-inspired pointwise pathways. During adaptation, the target encoder is removed, the online encoder is frozen, and the predictor plus a new decoder are trained on a few trajectories from a target equation. The same pretrained checkpoint is tested on source equations and on Lambda-Omega, Barkley, and Oregonator, which were excluded from pretraining.

## Model definition

### Inputs

The pretraining model receives four consecutive reaction-diffusion fields and a requested future lead time. During adaptation, it receives a few complete trajectories from the target system and then four observed fields at test time.

### Outputs

During pretraining, it predicts the latent representation of a future target field. During downstream use, it directly predicts five future full-field states at horizons 1 through 5.

### Training objective (loss)

Pretraining uses a latent prediction loss against a stop-gradient EMA target encoder. Downstream adaptation uses a supervised objective combining pointwise, relative-field, spatial-gradient, and Fourier-magnitude errors over the five horizons.

### Architecture / parameterization

The model uses a context encoder, an EMA target encoder, a lead-time-conditioned predictor with diffusion-like neighborhood and reaction-like pointwise latent pathways, and a dense decoder for full-field forecasts.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It tries to reduce the amount of simulation data needed when the nonlinear reaction term changes. Ordinary surrogate models often require a new corpus for each equation family.

### 2. What is the method?

Pretrain a JEPA-style predictor on several reaction-diffusion systems, then adapt the representation to new systems with one, five, or ten target trajectories.

### 3. What is the method motivation?

Predicting future representations may capture reusable dynamical structure across related PDEs without forcing the pretraining model to reconstruct every field directly.

### 4. What data does it use?

The source systems are Gray-Scott, FitzHugh-Nagumo, Brusselator, complex Ginzburg-Landau, and Schnakenberg. Held-out target systems are Lambda-Omega, Barkley, and Oregonator. The paper also tests Barkley under non-periodic boundary conditions.

### 5. How is it evaluated?

It evaluates relative discrete L2 field error and mean absolute spatial first-difference error over 300 held-out test trajectories, multiple support-set selections, adaptation budgets, horizons, and supervised surrogate baselines.

### 6. What are the main results?

On source systems, RD-JEPA has the lowest mean relative L2 error across all evaluated budgets and horizons. On held-out Lambda-Omega, Barkley, and Oregonator, it has the lowest mean relative L2 error against FNO and the no-predictive-latent control for every equation, budget, and horizon. Against FNO, LNO, ReViT, RieszNO, and CNextU-Net, it has the lowest mean on both reported metrics in all nine equation-budget settings, except one Lambda-Omega K=10 case where it is essentially tied with RieszNO. It also beats the architecture-matched scratch control.

### 7. What is actually novel?

The novelty is the controlled demonstration that predictive latent pretraining can transfer across omitted reaction laws, not just across coefficients or initial conditions inside one equation family.

### 8. What are the strengths?

The controls are the strength. The paper compares against a no-predictive-latent variant and a same-architecture scratch model, making it harder to attribute gains to the decoder or architecture alone.

### 9. What are the weaknesses, limitations, or red flags?

The target systems are still related PDEs, predictions are direct and short-horizon rather than long autoregressive rollouts, and the reported variability mostly reflects adaptation-set selection rather than full pretraining or optimizer randomness. No formal hypothesis tests are claimed.

### 10. What challenges or open problems remain?

Open problems include longer autoregressive stability, transfer to less related physics, automatic representation diagnostics, and identifying what the latent predictor actually stores about diffusion and reaction structure.

### 11. What future work naturally follows?

The natural follow-up is to test predictive latent pretraining on broader multi-physics corpora and to combine it with rollout-stability objectives like the September 25 latent-surrogate paper.

### 12. Why does this matter for cabbageland?

Cabbageland cares about world-model representations that transfer. RD-JEPA is a small but concrete test of whether future-prediction latents carry reusable dynamical information.

### 13. What ideas are steal-worthy?

Use held-out governing laws, not just held-out parameters. Include a no-predictive-latent control. Separate representation pretraining from decoder adaptation. Report transfer at tiny trajectory counts.

### 14. Final decision

Preserve. It is narrower than the top papers, but the experimental framing is worth remembering.
