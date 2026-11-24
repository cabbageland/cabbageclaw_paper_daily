# Scalable Beckmann Maps Improve One-step Generation

## Basic info

* Title: Scalable Beckmann Maps Improve One-step Generation
* Authors: Ulrik Unneberg, Shiyi Wang, Lee Cheuk-Kit, Felix Berg, Boris Kozinsky, Yilun Du, Michael S. Albergo, Eric Vanden-Eijnden
* Year: 2026
* Venue / source: arXiv preprint, submitted November 20, 2026
* Link: https://arxiv.org/abs/2611.28286
* Date surfaced: 2026-11-24
* Why selected in one sentence: Makes direct endpoint-map learning competitive through a concrete training-time guidance mechanism, with explicit limits on its theory and compute claims.

## Quick verdict

Highly relevant

A real mechanism-rich alternative to teacher distillation and repeated flow integration. Preserve the direct-map objective, conditional/null correction, and matched-representation ablations. Do not translate “no auxiliary feature loss” into “no pretrained representations,” or eight-frame-reset video metrics into long-horizon control.

## One-paragraph overview

Beckmann Transport Models construct an autonomous probability current from noise–data interpolations and learn a map that is constant along its flow lines, with identity behavior at data endpoints. SBM makes that map train effectively at scale. It interprets the current as pointing toward a weighted denoising mean, derives an implicit classifier-free-guidance correction, and replaces the unavailable conditional/null denoisers with predictions from the map itself. The practical recipe adds boundary-level conditioning, normalized transport updates and gradient balancing. Training requires directional derivatives and additional predictions; inference needs one map call and a decoder. Evidence spans class-conditional images, text-to-image, and unguided action-conditioned video prediction.

**Inspection basis:** Primary full PDF: main equations, theorem assumptions, principal experiments, ablations and limitations; selected appendix references, not an independent proof audit. [PDF](https://arxiv.org/pdf/2611.28286). [Project page](https://tullebulle.github.io/projects/sbm/) resolved; checkpoints were not executed.

## Model definition

### Inputs

A latent noise or interpolated noise–data sample, condition c (class, text, or frame/action history), and boundary level gamma. Training draws independent noise x0 and data x1 with interpolation Is = (1-s)x0 + sx1. World models condition on four previous frames and their actions.

### Outputs

An endpoint latent T_theta(x,c,gamma), decoded to an image or next frame. At inference the input is pure noise and gamma is a fixed read level. Longer videos autoregressively feed generated frames back into the context. There is no separate learned symbolic state or planner.

### Training objective (loss)

The base transport loss is squared error between T(Is) and a stopped target T(Is) + JVP(T, Is, direction). A boundary squared-error loss anchors predictions to clean data. For guidance strength omega, the practical correction to direction x1-x0 is proportional to

`(1 - 1/omega) / (1-s) * [T(Is,c,s) - T(Is,null,s)]`.

The boundary target gets the corresponding implicit conditional/null correction. The entire target, including the JVP and correction, is stopped. Omega = 1 recovers unguided conditional BTM. The implemented recipe conditions on boundary level, uses noisy boundary inputs, restricts guidance, normalizes transport updates and balances gradients; the ideal clean-boundary theorem does not prove convergence of that whole recipe.

### Architecture / parameterization

Conditional/null branches of one generator with condition dropout, not an additional denoising teacher. ImageNet uses DiT-B/2 in SD-VAE comparisons and DiTDH base/XL transformers in RAE latents. Strongest images use a frozen DINOv2 representation encoder and trained decoder. Text-to-image additionally uses a frozen FLAN-T5-Large text encoder. Video models use a conditional U-Net in SD3 autoencoder latents.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Direct one-step maps avoid a multistep teacher but previously generated poor conditional images. Ordinary CFG combines scores/velocities that an endpoint-only map does not expose. The problem is making guidance and scalable training work without abandoning one-call generation.

### 2. What is the method?

Express the time-averaged current through an autonomous denoising field; apply implicit CFG there; substitute the map's conditional/null contrast for the denoiser contrast. Train endpoint conservation plus boundary anchoring with the resulting direction. This changes the current and potentially the basin boundaries assigning source noise to data modes.

### 3. What is the method motivation?

A terminal map should not change along a trajectory that reaches the same endpoint. Making this invariance explicit provides supervision for the map directly. Implicit guidance also preserves the conditional covariance of the base transport target at fixed input/time, unlike a naive explicit target whose covariance scales with omega squared.

### 4. What data does it use?

ImageNet at 256x256, MiniT2I training data, and BridgeData V2/RT-1 robot videos. No new clinical or real-robot-control study. The generator is trained from scratch; latent/text encoders are not.

### 5. How is it evaluated?

FID-50k, Inception Score, multi-encoder FDr6, precision/recall and class-feature geometry for images; GenEval for text-to-image; SSIM, PSNR, LPIPS, FID and FVD for video. Native BTM comparisons fix architecture, SD-VAE, data and single-call sampling. Other system comparisons differ in latents/architecture; an iMF-in-matched-RAE control helps isolate this. Compute is estimated in FLOPs, with feature-network training usage counted but not all pretraining investments.

Video scoring resets history to ground truth every eight generated frames. Baseline rows largely come from DriftWorld. Qualitative uninterrupted rollouts are not a quantitative long-horizon test.

### 6. What are the main results?

- Matched DiT-B/2/SD-VAE at 100 epochs: SBM FID 9.3 versus native BTM 51. Each SBM update costs about 1.6 times as much.
- ImageNet SBM-XL: FID 1.61 at 840 EFLOP versus iMF 1.72 at an estimated 2,700 EFLOP. Drifting/W-Flow can obtain lower FID at greater reported compute with auxiliary feature losses.
- FDr6 is 6.2 versus iMF's 8.4; semantic-feature distances still exceed validation-reference distances substantially. Low FID is not distributional completion.
- Text-to-image: GenEval 0.856, one map call at 256px; MiniT2I-L/16 reaches 0.883 with 200 NFEs at 512px. Resolution and representation confound a simple speed/quality headline.
- Unguided Bridge-V2: FVD 18.1 versus 46.05, 15.6 versus at least 30.4 EFLOP. RT-1 short run reaches 28.3 versus 62.8 at 5.7 versus at least 16.1 EFLOP. These are prediction results, not policy success rates.

### 7. What is actually novel?

Training-time guidance for a direct Beckmann endpoint map using its own prediction contrast, plus a credible scaling recipe. BTM, autonomous currents, CFG and one-step generation predate this work. The map-for-denoiser substitution has an explicitly characterized contrast error rather than being exact by definition.

### 8. What are the strengths?

Matched native-model experiments; useful ablations and compute accounting; a multi-feature evaluation beyond FID; clear separation between ideal equations and implementation. The unguided world-model result shows that the recipe has value beyond the guidance claim.

### 9. What are the weaknesses, limitations, or red flags?

Pretrained RAE features underlie the strongest models. Headline ImageNet metrics and recipe ablations use limited seeds; selected native-BTM visual comparisons choose the best of 50 images and are explicitly not rigorous evidence. Training-time guidance costs additional forwards/JVP work. One NFE excludes decoding: RT-1's measured 21 ms/frame includes roughly 14.2 ms map and 6.6 ms decoder.

Population stationary-update consistency and local weak-guidance existence do not establish global arrival, unique output-law selection, or optimization convergence. A two-mode construction even permits the unchanged ordinary map at the same guidance strength. Video quality does not certify action causality, physical validity, calibration, or control usefulness.

### 10. What challenges or open problems remain?

Which self-consistent solution does training select? Does the endpoint objective preserve rare-mode coverage under shift? How well do uninterrupted video rollouts remain action-correct? Can representation and decoder costs erase gains at another resolution or batch size?

### 11. What future work naturally follows?

Matched-latent multi-seed iMF/BTM/SBM comparisons; learned versus exact denoiser-contrast controls; mode-coverage and calibration tests; other interpolants/couplings; quantitative long-horizon rollouts and downstream MPC. Reward/physical-constraint guidance is a proposal here, not a demonstrated capability.

### 12. Why does this matter for cabbageland?

It makes an explicit structural constraint do useful work in generation without claiming that larger implicit modeling solves everything. It is a serious fast-generator baseline and a reminder to separate representational advantages from objective advantages. “World model” here earns the narrow next-frame predictive label, not a reusable physical-state or planning claim.

### 13. What ideas are steal-worthy?

- Directly supervise invariance along a known probability current plus an explicit endpoint condition.
- Use a model's conditional/null contrast to guide its training, while measuring substitution error.
- Keep identity, transport and guidance constraints separately ablatable.
- Report generator NFE, decoder-inclusive latency, total training FLOPs and semantic coverage separately.

### 14. Final decision

Preserve. Read alongside native BTM and iMF before choosing a one-step generation baseline. Do not cite it as teacher-free pixel-space learning or proven long-horizon robotics modeling.
