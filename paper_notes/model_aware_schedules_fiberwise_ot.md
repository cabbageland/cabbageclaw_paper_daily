# Model-Aware Schedules Improve Generation via Fiberwise Optimal Transport

## Basic info

* Title: Model-Aware Schedules Improve Generation via Fiberwise Optimal Transport
* Authors: Luyi Jia, Boyan Zhang, Yilun Liu, Steffen Rulands
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2609.11842
* Date surfaced: 2026-09-11
* Why selected in one sentence: It makes diffusion and flow-matching schedule time depend on predictor-specific decomposition risk rather than only model-agnostic path geometry.

## Quick verdict

* Highly relevant

I inspected the full arXiv HTML text, including the fiberwise optimal-transport formulation, closed-form schedule allocation, DDPM and flow-matching experiments, robustness checks, and shared risk-profile diagnostics. This is worth preserving because it gives a concrete mechanism for schedule design and tests it across several model/dataset/sampler settings.

## One-paragraph overview

This paper studies the signal/noise schedules used by diffusion and flow-matching models. Standard schedules can be explained through coefficient-path kinetic action, but that view is model-agnostic: it ignores where a particular trained predictor makes larger decomposition errors. The paper defines a fiberwise prediction risk. At a fixed state on the affine probability path, many signal/noise decompositions are compatible with the same mixed state; these decompositions form a fiber. The cost between the true and predictor-induced decompositions inside the fiber gives a model-aware risk profile along the schedule. Estimating this profile from an early baseline checkpoint and combining it with kinetic action yields a closed-form traversal-time allocation. The resulting schedules improve FID for both DDPM and flow matching, and normalized risk profiles appear to align across multiple independently trained settings.

## Model definition

### Inputs
For the generative models, inputs are data samples, noise samples, time or schedule coordinates, and the mixed state along an affine probability path. For schedule construction, the input is a baseline checkpoint used to estimate prediction-error-derived fiberwise risk along the baseline coefficient curve.

### Outputs
The schedule-construction procedure outputs a modified time allocation along a fixed coefficient curve. The trained DDPM or flow-matching model outputs generated samples from noise under the model-aware schedule.

### Training objective (loss)
The underlying models use standard DDPM or flow-matching training objectives. The schedule objective combines coefficient-path kinetic action with a schedule-time-integrated fiberwise prediction risk constraint. In the fixed-curve specialization, this gives a closed-form allocation density rather than a new neural loss.

### Architecture / parameterization
The experiments use DDPM and flow-matching generative models, mainly U-Net-style backbones on CIFAR-10 and ImageNet-64, plus a U-ViT control and diagnostics on larger pretrained DiT-XL/2 and InstaFlow 2-RF checkpoints. The schedule is a deformation of the traversal of a baseline coefficient curve, not a new network architecture.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Schedule design is central to diffusion and flow models, but many schedules are model-agnostic. They do not ask where the trained predictor is less reliable along the path. The paper wants a principled way to allocate schedule time using model-specific prediction risk.

### 2. What is the method?
At each point on an affine probability path, the method considers the fiber of compatible signal/noise decompositions. It defines prediction risk by optimal-transport cost between the true and predicted decompositions in that fiber. It estimates this risk profile from an early baseline checkpoint, then combines it with kinetic action to compute a modified traversal-time allocation.

### 3. What is the method motivation?
The motivation is that a schedule should not only move smoothly through signal/noise space; it should also spend time according to what the model can predict. If a predictor is unreliable in a region, that risk should affect how the path is traversed.

### 4. What data does it use?
The main experiments use unconditional generation on CIFAR-10 and ImageNet-64. The diagnostics also inspect larger conditional latent diffusion and 2-Rectified Flow checkpoints without necessarily retraining those larger systems under the modified schedule.

### 5. How is it evaluated?
The paper reports 50,000-sample FID at matched numbers of function evaluations, across DDPM and flow-matching settings, multiple samplers/integrators, CIFAR-10 and ImageNet-64, paired seeds where applicable, and robustness/ablation variations.

### 6. What are the main results?
For CIFAR-10 DDPM at epoch 400, DPM++3M at 16 NFE improves FID from 9.64 to 8.06, a 16.4% relative reduction. For ImageNet-64 DDPM, DPM++3M at 16 NFE improves FID from 25.01 to 23.26. For CIFAR-10 flow matching, midpoint 16 NFE improves FID from 7.62 to 4.68, a 38.6% relative reduction. The paper says all four CIFAR-10 flow-matching configurations and all seven ImageNet-64 flow configurations improve.

### 7. What is actually novel?
The novelty is the fiberwise decomposition-risk view and its conversion into a closed-form schedule-time allocation. The normalized-risk alignment across independent settings is also interesting because it suggests there may be reusable schedule templates rather than fully bespoke tuning every time.

### 8. What are the strengths?
The method is mechanistic, mathematically explicit, and empirically tested across both diffusion and flow matching. It also uses paired comparisons and looks at robustness across sampler budgets, prediction targets, architectures, and risk-estimation checkpoints.

### 9. What are the weaknesses, limitations, or red flags?
The approach still deforms traversal along fixed curves; it does not discover arbitrary probability paths. The strongest claims are image-generation FID improvements, so semantic controllability, diversity, downstream utility, and larger-scale training economics remain less settled. The risk-profile universality claim is promising but should not be overgeneralized beyond the evaluated settings.

### 10. What challenges or open problems remain?
Open problems include schedule design for conditional generation with stronger semantic constraints, online adaptation during training, interaction with solver grids, scaling laws for risk estimation cost, and whether the shared risk template holds for video, 3D, audio, and multimodal diffusion systems.

### 11. What future work naturally follows?
Apply fiberwise-risk schedules to video diffusion, rectified flow video models, text-to-3D, and diffusion policies. Combine the method with uncertainty diagnostics, semantic guidance, or adaptive sampler grids. Test whether frozen analytic allocation templates survive across model families and datasets.

### 12. Why does this matter for cabbageland?
Cabbageland cares about generative mechanisms that expose where the model is weak. This paper gives a concrete state-dependent risk object and uses it to reshape generation instead of relying on aesthetic schedule folklore.

### 13. What ideas are steal-worthy?
Estimate a model's risk along an interface before redesigning the interface. Separate coefficient-path geometry from predictor-specific error. Look for normalized profiles that transfer across systems. Treat schedule time as an allocation resource.

### 14. Final decision
Keep as a highly relevant preserved note. The paper is math-heavy, but the mechanism and empirical coverage are strong enough to matter.
