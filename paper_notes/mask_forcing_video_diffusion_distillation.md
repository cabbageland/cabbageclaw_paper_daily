# Mask Forcing: Improving Autoregressive Video Diffusion Distillation via Dual-Noise Masking Rollout

## Basic info

* Title: Mask Forcing: Improving Autoregressive Video Diffusion Distillation via Dual-Noise Masking Rollout
* Authors: Zhuoran Zhao, Shengju Qian, Tongtong Liang, Xianghao Kong, Songchun Zhang, Junchao Huang, Guian Fang, Xin Wang, Pan Hui, Anyi Rao
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2609.09123
* Date surfaced: 2026-09-09
* Why selected in one sentence: It improves autoregressive video diffusion distillation by perturbing the student rollout distribution instead of merely polishing collapsed outputs.

## Quick verdict

* Highly relevant

I inspected the full arXiv HTML text, including the DMD preliminaries, dual-noise masking rollout, distributional analysis, quantitative comparisons, ablations, human evaluation, long-video appendix, and interactive video-world-model experiment. This earns a preserved note because the method targets the mechanism of mode collapse in self-rollout DMD.

## One-paragraph overview

Mask Forcing is a training strategy for distilling autoregressive video diffusion students from stronger bidirectional teachers. Self-rollout distribution matching distillation uses reverse KL, which tends to be mode-seeking and can produce over-saturated, over-smoothed, low-diversity videos. Mask Forcing changes the student rollout inputs during training: random spatial-temporal positions are replaced with lower-noise versions of the student prediction while other positions remain at the original noise level. The model still denoises at the original global timestep, so the mixed-noise input broadens the rollout trajectory and gives noisier tokens cleaner context.

## Model definition

### Inputs
Text prompts, historical video chunks in an autoregressive latent-video model, and noisy latent chunks during denoising. During training, the method constructs dual-noise rollout inputs with random masks across spatial and temporal axes.

### Outputs
Autoregressively generated video chunks from a causal diffusion student model.

### Training objective (loss)
The base distillation objective is distribution matching distillation, minimizing a reverse-KL-style objective between the student-induced distribution and the teacher distribution through score differences. Mask Forcing changes the rollout distribution by sampling random masks and lower-noise timesteps, then applying the same DMD training to the perturbed self-rollout samples.

### Architecture / parameterization
The method is not a new backbone. It plugs into autoregressive video diffusion distillation methods such as Self Forcing, Causal Forcing, and LongLive, using flow-matching latent diffusion chunks, causal AR rollout, a small number of denoising steps, and random dual-noise masks sampled per frame and per chunk in the preferred setting.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Distilled autoregressive video diffusion models can generate faster and stream longer, but self-rollout DMD can collapse into a narrow set of teacher modes, causing over-saturation, over-smoothing, weak detail, and error accumulation.

### 2. What is the method?
During self-rollout training, Mask Forcing samples a binary mask and a lower-noise timestep. Masked positions are re-noised to the cleaner timestep, unmasked positions remain at the original timestep, and the model denoises the resulting dual-noise input at the original global timestep.

### 3. What is the method motivation?
Reverse KL gives useful distillation pressure but is mode-seeking. Perturbing the rollout exposes DMD to student samples beyond the modes the student already covers, while lower-noise masked tokens act as denoising guidance for noisier tokens.

### 4. What data does it use?
The key claim is that the method improves AR video diffusion distillation without adding real video data or extra post-training stages. The camera-controlled appendix uses open-source data including SpatialVID, OmniWorld, RealCam-Vid, DL3DV, Sekai, and MiraData.

### 5. How is it evaluated?
It evaluates chunk-wise and frame-wise AR video generation on a 100-prompt set and VBench, long-video generation on MovieGen, pairwise human preferences, convergence speed, diversity metrics, and an initial camera-controlled interactive video setting.

### 6. What are the main results?
Mask Forcing improves Self Forcing, Causal Forcing, and LongLive across visual quality, semantic score, motion quality, dynamic degree, and VBench metrics. Human preference favors Mask Forcing over Self Forcing, Causal Forcing, and LongLive by 80%, 79%, and 83%, and favors it over LongLive by 72% for long videos. Against joint distillation baselines, it reports HPSv3 10.17, vision score 11.58, instruction score 46.30, MQ 21.54, and dynamic degree 82, beating DistillAlign and Causal-rCM on those reported metrics.

### 7. What is actually novel?
The novelty is perturbing the autoregressive self-rollout distribution with dual-noise masked inputs so the same DMD objective sees broader student trajectories and cleaner local denoising context.

### 8. What are the strengths?
The intervention is simple, compatible with multiple baselines, and supported by ablations over mask ratio, timestep window, and mask scheme. The training-speed and diversity results make the method look like more than a one-metric hack.

### 9. What are the weaknesses, limitations, or red flags?
The evaluation is still mostly visual-quality, preference, and proxy-metric based. Better detail and diversity do not automatically imply better semantic controllability, physical consistency, or long-horizon planning usefulness.

### 10. What challenges or open problems remain?
The hard part is connecting improved AR video quality to controllable world simulation, reliable action conditioning, and semantic state persistence over very long rollouts.

### 11. What future work naturally follows?
Test dual-noise rollout perturbations in action-conditioned video world models, combine them with uncertainty or consistency checks, and evaluate whether the generated future stays useful for downstream decisions.

### 12. Why does this matter for cabbageland?
Cabbageland cares about generative models that preserve structure over time. Mask Forcing is relevant because it changes training exposure at the rollout level, where temporal failures actually emerge.

### 13. What ideas are steal-worthy?
Perturb the model's own rollout distribution during distillation. Use cleaner partial tokens as local denoising anchors. Evaluate mode collapse with diversity and human preference, not only aggregate aesthetic scores.

### 14. Final decision
Keep as a preserved note. It is a practical diffusion-distillation mechanism with enough empirical support to matter.
