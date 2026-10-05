# Uncertainty as a Proxy for Semantic Correctness in Diffusion-Based Medical Image Synthesis

## Basic info

* Title: Uncertainty as a Proxy for Semantic Correctness in Diffusion-Based Medical Image Synthesis
* Authors: Yuxuan Ou, Konstantinos Kamnitsas, OxAAA Study, AICT Consortium, Regent Lee, Vicente Grau
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2610.03224
* Date surfaced: 2026-10-05
* Why selected in one sentence: It tests diffusion uncertainty against anatomical semantic error rather than visual similarity metrics.

## Quick verdict

* Highly relevant

This is a useful medical generation reliability paper because it refuses to equate plausible pixels with correct anatomy. Its main contribution is an evaluation scaffold: compare uncertainty maps against lumen-mask semantic error at pixel, region, image, external, and OOD levels. The task is narrow, but the structure is exactly right.

## One-paragraph overview

The paper studies non-contrast CT to contrast-enhanced CT synthesis for abdominal aorta imaging using AortaDiff, a multitask diffusion system that jointly produces a synthetic CECT image and a lumen segmentation. The segmentation branch gives an explicit anatomical proxy for semantic correctness: if the generated image's lumen segmentation disagrees with the ground truth lumen, the generation is anatomically wrong even if it looks realistic. Six uncertainty methods are compared: deep ensembles, HyperDiff, BayesDiff, Monte Carlo dropout, repeated diffusion sampling, and test-time augmentation. MCDropout is the practical winner because it performs strongly across scales and external shift without extra training when dropout already exists.

## Model definition

### Inputs

The core model takes an NCCT abdominal aorta slice as input. Uncertainty methods add variability through weights, architecture perturbation, repeated diffusion sampling, or input perturbations.

### Outputs

The multitask diffusion model outputs a synthetic CECT image and a lumen segmentation mask. Each uncertainty method outputs a pixel-wise uncertainty map over the generated CECT image, later aggregated at pixel, region, and image levels.

### Training objective (loss)

The inspected text states that AortaDiff jointly optimizes CECT generation and lumen segmentation with shared image representation. The exact loss weighting is inherited from the previous AortaDiff work and is not fully rederived in the accessible sections. The uncertainty comparison itself is mostly an evaluation layer; MCDropout, repeated sampling, and TTA require no retraining, while ensemble and HyperDiff require additional training.

### Architecture / parameterization

AortaDiff is a multitask diffusion framework for NCCT-to-CECT synthesis with an added segmentation output. The uncertainty methods span different sources: whole-network disagreement from ensembles, hypernetwork weight sampling from HyperDiff, last-layer Laplace approximation from BayesDiff, stochastic subnetworks from MCDropout, repeated DDIM sampling, and transformed inputs under TTA.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It addresses a key failure of medical image generation: a synthetic image can look plausible while placing anatomy incorrectly. Standard metrics such as PSNR, SSIM, LPIPS, and MSE do not directly measure whether clinically relevant structure is correct.

### 2. What is the method?

Use the model's jointly predicted lumen segmentation as a semantic representation of the generated anatomy. Compare uncertainty maps against semantic error between predicted and ground-truth lumen masks at pixel, superpixel-region, and image levels. Also test external distribution shift and vascular-stent OOD detection.

### 3. What is the method motivation?

If uncertainty is going to be used for clinical filtering, it should flag semantic failure, not just visual deviation. The lumen segmentation gives a concrete anatomical target.

### 4. What data does it use?

The paper uses the Oxford abdominal aortic aneurysm data for internal testing and the AICT multi-centre dataset for external validation. OOD detection uses vascular stents as clinically relevant unseen structures absent from training.

### 5. How is it evaluated?

Pixel-level evaluation uses disagreement between predicted and ground-truth lumen masks, pixel-wise AUROC, and uncertainty-guided sparsification. Region-level evaluation groups aortic pixels into SLIC superpixels and measures correlation/sparsification against regional error. Image-level evaluation labels generated slices as failures based on lumen Dice thresholds and computes AUROC. OOD detection aggregates uncertainty maps into image-level scores for stent detection.

### 6. What are the main results?

The segmentation proxy is validated by applying three independent lumen segmenters to the generated CECT images; the multitask segmentation agrees with them at mean Dice 0.95. At pixel level, MCDropout is best overall with AUSE 0.028, AUSC 0.911, and AUROC 0.830, while BayesDiff is near random at AUROC 0.493. At region level, MCDropout and HyperDiff are effectively tied, with Spearman correlations around 0.65 and 0.64. At image level, MCDropout, TTA, repeated diffusion sampling, and ensembles exceed AUROC 0.9 for severe failures and remain useful up to moderate Dice thresholds. On external AICT data, MCDropout stays above 0.8 across most aggregation strategies and thresholds. For stent OOD detection, MCDropout reports AUROC 0.77 to 0.83 depending on aggregation, comparable to TTA and repeated sampling.

### 7. What is actually novel?

The novelty is using semantic anatomical correctness as the target for uncertainty evaluation in diffusion-based medical synthesis, rather than treating uncertainty as a proxy for pixel similarity or distributional realism.

### 8. What are the strengths?

The evaluation is multi-scale, includes external validation, and compares uncertainty sources rather than one preferred trick. The practical conclusion is valuable: training-free uncertainty methods can match or beat retraining-heavy methods for deployment filtering.

### 9. What are the weaknesses, limitations, or red flags?

The whole study is one application: NCCT-to-CECT synthesis of the abdominal aorta. Semantic correctness is measured through segmentation, so the framework depends on having a reliable task-specific structural proxy. It flags severe failures better than it ranks already-good images. It does not prove downstream clinical decision improvement.

### 10. What challenges or open problems remain?

Generalizing this framework to other organs, modalities, and structures will require appropriate semantic targets. Another open problem is combining multiple uncertainty sources into a calibrated clinical action policy rather than only ranking/filtering.

### 11. What future work naturally follows?

Apply the same evaluation pattern to contrast MRI synthesis, lesion-preserving generation, surgical planning structures, and generative augmentation pipelines. A strong next step would couple uncertainty maps to human review policy and measure whether they reduce harmful synthetic-image use.

### 12. Why does this matter for cabbageland?

It is a crisp example of evaluation that measures the thing that matters. The paper does not ask "does the image look similar"; it asks whether the generated anatomy is semantically right and whether uncertainty knows when it is wrong.

### 13. What ideas are steal-worthy?

When a generative model claims structure, attach a structural head or external structural probe and evaluate uncertainty against that structure. Report pixel, region, and image behavior separately because uncertainty can be useful at one scale and weak at another.

### 14. Final decision

Preserve. This is directly useful for uncertainty, generative-model evaluation, and clinical reliability framing.
