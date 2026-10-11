# Just Weather Scoring: Efficient End-to-end Nowcasting with Distributional Diffusion

## Basic info

* Title: Just Weather Scoring: Efficient End-to-end Nowcasting with Distributional Diffusion
* Authors: Jannik Wiese, Johannes Schusterbauer, Tommaso Martorella, Bjoern Ommer
* Year: 2026
* Venue / source: arXiv preprint
* Link: https://arxiv.org/abs/2610.12189
* Date surfaced: 2026-10-11
* Why selected in one sentence: It strips probabilistic precipitation nowcasting down to one radar-space diffusion model with a scoring-rule objective for few-step sampling.

## Quick verdict

* Highly relevant

JWS is a useful applied generative-model paper because it removes the usual multi-stage compression and deterministic-prior stack rather than adding another wrapper. The core move is clean: train directly in radar space with masked asynchronous diffusion and a simple distributional objective that blends CRPS with squared error. The caveat is that nowcasting metrics are domain-specific and the model still trades some CSI/HSS behavior against probabilistic calibration, but the paper is unusually clear about that tradeoff.

## One-paragraph overview

Diffusion nowcasting often uses latent compression, deterministic forecast priors, or separate generative decoders, which complicates training and can add uncertainty where radar intensity errors matter. Just Weather Scoring trains a single transformer directly on radar sequences. Masked Asynchronous Diffusion keeps observed context frames clean while sampling framewise noise levels for future frames, better matching forecasting conditions. Simple Distributional Diffusion Models replace a tuned distributional objective with a hyperparameter-free interpolation between CRPS and MSE, enabling strong few-step sampling. The result is a much simpler nowcasting pipeline that is competitive or state-of-the-art on SEVIR and MeteoNet with far lower training and inference cost.

## Model definition

### Inputs

The model receives radar observation sequences, clean context-frame masks, framewise diffusion times for future frames, and noise-corrupted radar frames. It conditions on past radar observations and predicts future precipitation frames.

### Outputs

The model samples ensembles of future radar maps for precipitation nowcasting. Internally it predicts denoising updates or clean radar maps in pixel/radar space, depending on the flow/diffusion parameterization.

### Training objective (loss)

JWS uses a simple distributional diffusion objective: `(1 - tau) * CRPS + tau * MSE` at each frame/timestep. CRPS aligns training with probabilistic forecasting, while MSE preserves high-noise denoising stability. The model is trained end-to-end without a separate autoencoder or deterministic forecast stage.

### Architecture / parameterization

The paper uses transformer-based pixel-space nowcasting models, including hierarchical/factorized variants. Its main method combines radar-space sequence diffusion, Masked Asynchronous Diffusion for conditioning/noise scheduling, and simple Distributional Diffusion Models for few-step inference.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Precipitation nowcasting needs sharp, probabilistic, fast forecasts. Multi-stage latent or deterministic-prior diffusion pipelines are expensive and can lose information through compression or impose biased priors.

### 2. What is the method?

JWS trains directly on radar fields. Masked Asynchronous Diffusion samples clean context frames and corrupted future frames with framewise noise levels. The sDDM objective blends CRPS and MSE so the model can produce calibrated forecast ensembles in few denoising steps.

### 3. What is the method motivation?

Weather users care about calibrated distributions over future precipitation, not just visually plausible frames. Radar-space modeling avoids compression artifacts, and scoring-rule supervision aligns the generative model with probabilistic forecast quality.

### 4. What data does it use?

The main benchmarks are SEVIR and MeteoNet. The paper reports SEVIR training with 402,500 sequences from 16,100 events and MeteoNet training with 259,656 sequences. It evaluates 6-hour nowcasting-style metrics over forecast ensembles.

### 5. How is it evaluated?

Metrics include CRPS, SSIM, HSS, CSI, reliability index, training/inference compute, parameter count, and wall-clock scaling over different numbers of function evaluations. Ablations isolate timestep sampling, MAD vs forcing/diffusion paradigms, architecture, and training objective.

### 6. What are the main results?

On SEVIR, JWS-B/32 reports CRPS 0.0176, SSIM 0.8092, HSS 0.5408, CSI 0.4180, and RI 0.0956, while JWS-L reaches CRPS 0.0175 and guidance raises HSS/CSI to 0.5894/0.4581. On MeteoNet, JWS-S/32 reaches CRPS 0.0141 and SSIM 0.7917 with only 24M parameters; JWS-B/32 reaches SSIM 0.7967. The paper reports comparable CRPS to FREUD with about 44x less training compute and notes that the smallest model can be more than 17x faster at inference than prior heavy systems.

### 7. What is actually novel?

The novelty is the combination of direct radar-space diffusion, clean-context asynchronous corruption, and a simple CRPS/MSE distributional objective that makes few-step probabilistic generation practical.

### 8. What are the strengths?

The system is dramatically simpler than multi-stage baselines. The ablations are useful, especially showing that clean-context MAD and sDDM matter. The metrics include reliability, not only sharpness or threshold-hit scores.

### 9. What are the weaknesses, limitations, or red flags?

The strongest CSI/HSS numbers may still require guidance or deterministic-prior conditioning, which can hurt calibration. CRPS is a marginal scoring rule, so spatial joint structure can be under-tested. Weather-specific wins may not automatically transfer to generic video generation.

### 10. What challenges or open problems remain?

The open challenge is joint spatiotemporal calibration: not just per-pixel marginal CRPS, but coherent uncertainty over storm shape, motion, and extremes. Another is operational robustness under sensor gaps and distribution shift.

### 11. What future work naturally follows?

Add structure-aware scoring rules, evaluate rare extreme events separately, couple radar-space diffusion with physical constraints, and test whether MAD-style context corruption helps other scientific sequence generators.

### 12. Why does this matter for cabbageland?

This is a good example of matching a generative objective to the real downstream uncertainty question. The paper says: do not hide uncertainty in latent compression if the domain cares about exact spatial intensity.

### 13. What ideas are steal-worthy?

Keep observed context clean during diffusion training. Use proper scoring rules when the product is a forecast distribution. Prefer single-stage data-space modeling when compression uncertainty is task-relevant.

### 14. Final decision

Preserve. It is domain-specific, but the training-design lesson is broadly useful.
