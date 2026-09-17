# Dose-Aware Cold Diffusion with Physics Consistency for Generalizable Low-Dose CT Reconstruction

## Basic info

* Title: Dose-Aware Cold Diffusion with Physics Consistency for Generalizable Low-Dose CT Reconstruction
* Authors: Md Imam Ahasan, Guangchao Yang, A F M Abdun Noor, S M Hasan Mahmud, Md Mahfuzur Rahman
* Year: 2026
* Venue / source: arXiv:2609.18943; accepted at IJCNN 2026
* Link: https://arxiv.org/abs/2609.18943
* Date surfaced: 2026-09-17
* Why selected in one sentence: It couples continuous degradation conditioning with in-loop measurement-domain correction in a diffusion inverse-problem setting.

## Quick verdict

* Useful

This is an adjacent medical imaging paper, not a core world-model paper. It is still worth preserving because the mechanism is transferable: model the degradation continuously, allocate computation by severity, and enforce physics consistency inside each generative refinement step. This note is based on the full arXiv PDF text.

## One-paragraph overview

Dose-Aware Cold Diffusion treats low-dose CT reconstruction as a dose-conditioned cold diffusion inverse problem. Instead of adding synthetic Gaussian noise, the forward process uses dose-dependent Poisson thinning and filtered backprojection to create physically meaningful degradation states. The reverse process alternates learned denoising with forward-backprojection correction so the image remains consistent with measured projections. A dose-aware perception module estimates degradation severity, a structural prior module fuses edge/texture/CNN features, and a dose-calibrated step allocator gives lower-dose inputs more refinement steps.

## Model definition

### Inputs

The system receives a measured low-dose sinogram, its filtered-backprojection reconstruction, and a dose level represented continuously in (0, 1]. During training it uses full-dose CT images and simulated low-dose measurements.

### Outputs

The model outputs a reconstructed CT image intended to match the full-dose target while remaining consistent with the low-dose measurements.

### Training objective (loss)

The total loss combines image fidelity, projection-domain consistency, a dose-ranking loss, and a contrastive representation loss for dose-aware features. The image term includes L1 image error and a projection-domain squared error. The reverse update also includes an explicit forward-backprojection correction after each denoising step.

### Architecture / parameterization

The denoiser is a U-Net conditioned on time and dose embeddings. The Dose-Aware Perception module estimates severity and dose embeddings. PEM++ fuses gradient, Laplacian, non-local means, and CNN priors with attention and dose/time modulation. DCSA maps dose severity to the number of reverse refinement steps.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Low-dose CT lowers radiation but increases noise and artifacts. Many reconstruction methods are tuned to discrete dose levels or fail on unseen dose settings. The paper tries to reconstruct across a continuous range of dose levels while preserving projection-domain data consistency.

### 2. What is the method?

The forward process simulates low-dose acquisition from clean projections via dose-dependent Poisson thinning, then reconstructs degraded images with filtered backprojection. The reverse process uses a dose-conditioned denoiser, dose-calibrated step allocation, structural priors, and in-loop projection correction after every denoising step.

### 3. What is the method motivation?

Dose is not a categorical nuisance variable. It controls the noise statistics and degradation severity. A reconstruction model should condition continuously on dose and should not rely purely on learned image priors when measured projection data is available.

### 4. What data does it use?

Experiments use Mayo-2020, Mayo-2016, and LoDoPaB-CT. Mayo-2020 includes head, chest, and abdomen scans with simulated low-dose measurements at 50%, 25%, 12.5%, and 5%. Additional unseen-dose tests use 30% abdomen, 10% chest, and 15% head.

### 5. How is it evaluated?

The paper reports PSNR, SSIM, and RMSE per slice, with paired Wilcoxon signed-rank tests and FDR correction. It compares against diffusion and physics-guided baselines including PrideDiff, CoreDiff, Cold Diffusion, RDDM, DDPM-1000, RED-diff, and Noise2Sim. It includes cross-dataset and ablation tests.

### 6. What are the main results?

On Mayo-2020, DACD leads across all reported anatomies and dose levels. For abdomen at 5% dose, it reports 36.23 dB PSNR versus 35.45 for PrideDiff. For chest at 5%, it reports 33.53 versus 32.72. For head at 5%, it reports 39.42 versus 38.23. On LoDoPaB-CT, DACD reports 38.74 dB PSNR / 0.8951 SSIM versus 37.92 / 0.891 for PrideDiff. On Mayo-2016, it reports 44.36 / 0.9724 versus 43.72 / 0.9693. In the 12.5% Mayo-2020 ablation, the full model reaches 39.80 dB / 0.972 versus 37.10 / 0.961 for the cold diffusion baseline.

### 7. What is actually novel?

The novelty is the combination of continuous dose conditioning, adaptive reverse-step allocation, and projection-domain correction embedded inside the cold diffusion reverse process. Each component alone is unsurprising; the in-loop coupling is the useful part.

### 8. What are the strengths?

The design respects the measurement physics instead of treating reconstruction as pure image translation. The continuous dose representation is more realistic than discrete dose classes. The ablations are monotonic and support the claimed component contributions.

### 9. What are the weaknesses, limitations, or red flags?

The task remains evaluated mainly by PSNR/SSIM/RMSE. Simulated low-dose settings and public benchmarks do not prove clinical deployment utility. Future work is explicitly needed for anatomy-aware representations, cross-scanner generalization, and inference efficiency.

### 10. What challenges or open problems remain?

The important open question is whether the same gains hold across scanner vendors, reconstruction kernels, patient distributions, and prospective clinical workflows. Another question is how to quantify diagnostic risk, not just pixel fidelity.

### 11. What future work naturally follows?

Add anatomy-aware conditioning, scanner-domain adaptation, uncertainty maps, and task-level evaluation for lesion detection or radiologist performance. Test the physics-correction loop under real measured low-dose sinograms rather than only simulated degradation.

### 12. Why does this matter for cabbageland?

Cabbageland can steal the general pattern: treat degradation severity as continuous state, allocate computation adaptively, and project the generative refinement back into measurement consistency after every step.

### 13. What ideas are steal-worthy?

Use monotone degradation-to-step mappings. Put physics correction inside the denoising loop rather than after it. Train dose embeddings with ordinal and contrastive constraints. Evaluate unseen continuous degradation levels explicitly.

### 14. Final decision

Preserve as adjacent inspiration. The medical domain is not central, but the inverse-problem design pattern is useful.
