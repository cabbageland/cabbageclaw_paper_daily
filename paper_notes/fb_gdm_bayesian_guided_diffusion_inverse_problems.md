# FB-GDM: Fully-Bayesian Guided Diffusion Models for High-Dimensional Linear Inverse Problems via Unsupervised Variational Inference

## Basic info

* Title: FB-GDM: Fully-Bayesian Guided Diffusion Models for High-Dimensional Linear Inverse Problems via Unsupervised Variational Inference
* Authors: Gatien Seguy, Thomas Rodet
* Year: 2026
* Venue / source: arXiv:2609.29216
* Link: https://arxiv.org/abs/2609.29216
* Date surfaced: 2026-09-26
* Why selected in one sentence: It removes ground-truth-tuned diffusion guidance knobs by inferring the prior/data precision balance during sampling.

## Quick verdict

* Highly relevant

This is a good calibration paper for diffusion inverse problems. The useful move is to turn PiGDM's guidance hyperparameters into latent precision variables and infer them from the observation at each reverse step. The paper is still limited to linear inverse problems with a fixed pretrained image prior, but the deployment lesson is strong.

## One-paragraph overview

Diffusion priors can solve image inverse problems, but common guidance methods such as DPS and PiGDM depend on scalar hyperparameters that are often tuned with ground truth. FB-GDM starts from PiGDM's Gaussian approximation and derives a conditional score controlled by two precisions: one for the denoising approximation and one for the observation likelihood. Instead of choosing these by hand, it treats them as unknown random variables and estimates them with fast variational inference during each reverse diffusion step. The method needs only the observation and forward operator. On CelebA-HQ inverse problems, it approaches ground-truth-tuned PiGDM oracles and is more robust when the operator, noise level, or image distribution changes.

## Model definition

### Inputs

The sampler receives a degraded observation `y`, a known linear forward operator `A`, the current noisy diffusion state, and a pretrained unconditional DDPM prior. It does not receive the true image, true noise level, or task-specific tuning values.

### Outputs

It outputs reconstructed images by following a reverse diffusion process guided by an inferred conditional score. Internally it estimates two precision parameters at each reverse step.

### Training objective (loss)

FB-GDM does not train a new image model in the paper. It reuses a pretrained unconditional DDPM and performs unsupervised variational inference over precision parameters during sampling. The underlying DDPM was trained with the usual denoising objective.

### Architecture / parameterization

The method is a Bayesian guidance layer around an unconditional diffusion model. It uses PiGDM-style Gaussian denoising and observation approximations, a closed-form conditional score, and a separable variational factorization so updates scale linearly with the number of pixels.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It solves the calibration problem in diffusion-guided linear inverse problems. Existing guidance methods can work well only after operator-, noise-, or image-specific hyperparameter tuning, often against ground truth.

### 2. What is the method?

FB-GDM treats the denoising variance and observation-noise variance as latent precisions. At each reverse step, it estimates them by variational inference and plugs them into a closed-form conditional score.

### 3. What is the method motivation?

A reconstruction method should know when to trust the learned image prior and when to trust the measurement. Fixed guidance scales can hallucinate prior-consistent structure or amplify measurement noise.

### 4. What data does it use?

The experiments use an unconditional DDPM pretrained on CelebA-HQ at 256x256. Evaluation covers CelebA-HQ inverse problems and out-of-distribution ImageNet images with the same face prior.

### 5. How is it evaluated?

The paper evaluates deblurring, uniform blur, super-resolution, noise-level shifts, out-of-distribution image reconstructions, runtime, PSNR, SSIM, and visual artifacts. Baselines include DPS and several PiGDM settings, including ground-truth-tuned oracles.

### 6. What are the main results?

For 9x9 Gaussian blur at 20 dB, FB-GDM reaches 28.86 dB PSNR and 0.822 SSIM without tuning, essentially matching the 28.85 dB PiGDM oracle and beating nominal PiGDM at 15.28 dB. Across operator changes it stays close to tuned PiGDM oracles. Across noise levels from 1 to 30 dB it remains near the best frozen oracle without knowing the true noise. On ImageNet images reconstructed with a CelebA-HQ face prior, it avoids the face-like hallucinations seen with DPS.

### 7. What is actually novel?

The novelty is not the diffusion prior. It is the fully Bayesian treatment of guidance precision inside a scalable reverse sampler.

### 8. What are the strengths?

The paper addresses a real deployment footgun: tuning against unavailable ground truth. It tests operator shift, noise shift, and image-distribution shift, and it compares against both nominal and oracle-tuned baselines.

### 9. What are the weaknesses, limitations, or red flags?

The setting is still linear inverse problems, and the prior is a domain-specific image prior. Matching PSNR or SSIM does not guarantee scientific validity in medical or astronomical domains. Runtime is higher than one nominal PiGDM or DPS pass, though much cheaper than repeated tuning sweeps.

### 10. What challenges or open problems remain?

Open problems include nonlinear forward models, more realistic measurement corruption, domain-specific uncertainty reporting, and whether the inferred precisions are calibrated enough to support downstream decisions.

### 11. What future work naturally follows?

Useful follow-ups include applying the same precision-inference idea to video diffusion, 3D reconstruction, medical imaging, and samplers with learned measurement models.

### 12. Why does this matter for cabbageland?

Cabbageland cares about uncertainty and controllability. FB-GDM is a concrete example of replacing manual confidence knobs with inferred local trust in prior versus evidence.

### 13. What ideas are steal-worthy?

Promote guidance scales to latent variables. Infer prior/data balance from the current observation. Compare to oracle-tuned baselines rather than only nominal defaults. Treat hallucination as a calibration failure, not just an aesthetic defect.

### 14. Final decision

Preserve. This is a strong mechanism paper for calibrated generative inference.
