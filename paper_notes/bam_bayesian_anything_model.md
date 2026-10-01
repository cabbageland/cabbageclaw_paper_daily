# BAM! Bayesian Anything Model: a foundation model for generative computational imaging

## Basic info

* Title: BAM! Bayesian Anything Model: a foundation model for generative computational imaging
* Authors: Alessio Spagnoletti, Charlesquin Kemajou Mbakam, Jonathan Spence, Andres Almansa, Marcelo Pereyra
* Year: 2026
* Venue / source: arXiv:2609.39660
* Link: https://arxiv.org/abs/2609.39660
* Date surfaced: 2026-10-01
* Why selected in one sentence: It turns operator-conditioned reconstruction into a lightweight flow-map posterior sampler for many imaging inverse problems.

## Quick verdict

* Highly relevant

BAM is a strong applied generative-model paper because it treats the forward operator as part of the model interface, not as a hidden dataset-specific assumption. The paper is careful about its limits: known operators, additive Gaussian noise, and no automatic model-mismatch detection. Within that scope, the mechanism is useful.

## One-paragraph overview

BAM addresses Bayesian computational imaging, where the goal is not just to reconstruct one image from a measurement but to sample from the posterior distribution implied by a forward operator and noise model. Large zero-shot image priors can be used with approximate likelihood guidance, but that is expensive and biased. Specialized physics-aware models avoid some of that bias but are tied to specific instruments or tasks. BAM upgrades the operator-conditioned Reconstruct Anything Model backbone into a conditional flow map. The forward operator and noise level are provided at inference time, and a 36M-parameter network produces posterior samples in a few steps, usually three. The experiments cover super-resolution, deblurring, inpainting, compressed sensing, JPEG restoration, sparse-view CT, and blind motion deblurring, with BAM often beating specialized and zero-shot baselines in perceptual quality at much lower cost.

## Model definition

### Inputs

Inputs include a measurement, a known forward operator, an adjoint/operator representation, a noise level, a starting latent or image state, and flow times. For the main setup, the observation model is additive Gaussian noise around a linear forward operator.

### Outputs

The model outputs posterior image samples. Multiple independent samples can be averaged to estimate a posterior mean, and their variation can be used for posterior uncertainty summaries.

### Training objective (loss)

BAM is trained as a conditional flow map. It combines a diagonal flow-matching drift loss with a Lagrangian self-distillation loss that propagates the drift to finite jumps. Auxiliary terms target reconstruction/posterior behavior. The paper frames this as learning an integrated flow map from noisy states to posterior samples.

### Architecture / parameterization

BAM uses a lightweight RAM-style operator-conditioned backbone with unrolled physics-aware updates. It is modified from reconstruction into posterior sampling by learning a conditional flow map across operators, datasets, and noise levels. The reported model has 36M parameters.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Computational imaging needs posterior sampling for inverse problems, but current choices are awkward: large generic priors need approximate likelihood guidance, while physics-aware generative models usually specialize to a narrow dataset, task, or instrument.

### 2. What is the method?

Train a single operator-conditioned conditional flow map that receives the measurement model at inference time and maps reference noise to posterior samples in a few steps. The model amortizes over many forward operators and noise levels.

### 3. What is the method motivation?

If the physics of the instrument is known at inference time, the generative model should condition on that operator directly. This avoids both retraining a new posterior sampler for each instrument and relying on approximate external guidance from a generic image model.

### 4. What data does it use?

The model is pretrained on 4KLSDB downsampled to image resolutions used in the experiments, together with libraries of forward operators. Evaluation uses FFHQ, AFHQ, LSUN, DIV2K, the Kohler camera-shake benchmark, and appendix extensions including sparse-view CT on LIDC-IDRI chest slices.

### 5. How is it evaluated?

The paper compares BAM with zero-shot methods such as LATINO, LATINO-PRO, and TReg, with RAM before and after finetuning, and with training-based or task-specialized methods. Metrics include PSNR, SSIM, LPIPS, runtime, and qualitative posterior samples.

### 6. What are the main results?

The main claim is that BAM produces high-quality posterior samples in three steps and often wins LPIPS/sample-quality comparisons across FFHQ, AFHQ, LSUN, DIV2K, and Kohler. It also remains competitive with specialized methods while using far fewer steps and a small 36M-parameter model.

### 7. What is actually novel?

The novelty is not just another inverse-problem network. BAM makes the forward operator an inference-time condition of a learned posterior flow map, moving from deterministic operator-conditioned reconstruction to generative posterior sampling.

### 8. What are the strengths?

The interface is crisp, the model is small, and posterior samples are more useful than a single reconstruction for downstream decisions. The paper also explores transfer to unseen operators and tasks rather than reporting only one benchmark.

### 9. What are the weaknesses, limitations, or red flags?

BAM assumes additive Gaussian noise and linear or mildly nonlinear known operators. It is non-blind unless an external operator estimate is provided. It does not detect model mismatch, so a wrong operator or noise model can produce unreliable posteriors without warning. Posterior calibration remains open.

### 10. What challenges or open problems remain?

The big open problems are calibrated uncertainty, unknown or partially known forward models, nonlinear measurement processes, and domain shift in scientific or medical settings. Sample diversity also needs stronger calibration evidence, not just perceptual quality.

### 11. What future work naturally follows?

Extend the operator-conditioned flow-map idea to MRI, CT, microscopy, astronomy, and robotics perception where forward operators are known but ground truth is scarce. Add mismatch detection and calibration diagnostics.

### 12. Why does this matter for cabbageland?

BAM is a good model of how to expose physics to a generator: the forward operator is an input, not a footnote. That interface is relevant to any generative system meant to reason under measurement constraints.

### 13. What ideas are steal-worthy?

Condition generation on the actual operator. Treat posterior sampling as the product, not a deterministic reconstruction plus vibes. Keep the model small enough that finetuning for a domain is plausible.

### 14. Final decision

Preserve. It is one of the best non-robotics papers today and a useful template for physics-aware generative inference.

