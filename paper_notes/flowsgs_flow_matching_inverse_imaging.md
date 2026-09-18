# FlowSGS: Improving Flow Matching Priors for Inverse Imaging with Stochastic Interpolants

## Basic info

* Title: FlowSGS: Improving Flow Matching Priors for Inverse Imaging with Stochastic Interpolants
* Authors: Tianao Li, Xinhui Qian, Emma Alexander
* Year: 2026
* Venue / source: arXiv:2609.20769
* Link: https://arxiv.org/abs/2609.20769
* Date surfaced: 2026-09-18
* Why selected in one sentence: It turns flow-matching priors into a posterior sampler for inverse imaging, including nonlinear phase retrieval, rather than using them only as guided reconstruction engines.

## Quick verdict

* Highly relevant

This is a strong generative inverse-problem paper with a real sampling mechanism. The strongest part is the split Gibbs formulation plus the connection to stochastic interpolants and PnP-DM. This note is based on the full arXiv PDF text.

## One-paragraph overview

FlowSGS adapts Split Gibbs Sampling to use pretrained flow-matching priors for inverse imaging. Each iteration alternates a likelihood step, sampled with Langevin dynamics under the measurement model, and a prior step, sampled with a reverse-time SDE defined through the stochastic-interpolants framework. The paper shows how PnP-DM appears as a special case under specific diffusion choices, then adds a timestep conversion/correction strategy that makes the flow prior step efficient. Experiments cover linear inverse problems and nonlinear Fourier phase retrieval.

## Model definition

### Inputs

The sampler receives measurements, a forward operator or likelihood model, and a pretrained flow or diffusion prior. Experiments include motion deblurring, Gaussian deblurring, 4x super-resolution, Cartesian and radial compressed-sensing MRI, and Fourier phase retrieval.

### Outputs

The method outputs posterior samples of the unknown image. For linear inverse problems the paper reports the mean of eight samples; for phase retrieval it reports the best sample among eight for reconstruction metrics and uses 512 samples for uncertainty/mode analysis.

### Training objective (loss)

The pretrained flow priors are trained with standard flow-matching or stochastic-interpolant objectives. FlowSGS itself is an inference-time sampler, not a new training loss. The likelihood step uses Langevin dynamics, and the prior step uses a reverse-time SDE guided by the pretrained velocity or score model.

### Architecture / parameterization

The paper uses NCSN++ priors for fair pixel-space comparisons and also briefly tests latent-space Stable Diffusion 3.5 priors. The core algorithm is architecture-agnostic as long as the prior can supply the required velocity or score information.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Flow priors are attractive for inverse problems, but existing flow-based inverse solvers often assume linear forward models or rely on approximate guidance that does not faithfully sample the posterior.

### 2. What is the method?

FlowSGS decomposes posterior sampling into alternating likelihood and prior updates. The likelihood update enforces measurements with Langevin dynamics. The prior update maps through stochastic-interpolant reverse-time dynamics using the pretrained flow prior.

### 3. What is the method motivation?

Separating likelihood and prior steps lets the method handle more general measurement models while preserving a generative prior. The stochastic-interpolant view also lets flow priors inherit useful sampling structure from diffusion-style methods without pretending guidance alone is posterior sampling.

### 4. What data does it use?

Experiments use FFHQ images and fastMRI knee images resized to 256x256, plus toy Gaussian compressed sensing and latent-space examples.

### 5. How is it evaluated?

The paper compares DPS, PnP-DM, DAPS, PnP-Flow, FlowChef, FlowDPS, and FlowSGS variants under PSNR, SSIM, LPIPS, data-fit metrics, posterior KL in a toy Gaussian problem, and bimodal posterior recovery in phase retrieval.

### 6. What are the main results?

FlowSGS Linear leads most Table 1 tasks. It reaches 29.22 PSNR / 0.836 SSIM / 0.154 LPIPS on motion deblurring, 30.09 / 0.847 / 0.141 on Gaussian deblurring, and 29.49 / 0.844 / 0.149 on 4x super-resolution. For Fourier phase retrieval, FlowSGS GVP reaches 38.45 PSNR / 0.950 SSIM / 0.056 LPIPS, while FlowSGS Linear reaches 37.52 / 0.940 / 0.076. The paper also shows a clearer bimodal posterior than guidance-heavy flow baselines.

### 7. What is actually novel?

The novelty is integrating flow-matching priors into a split Gibbs posterior sampler through stochastic interpolants, plus a timestep correction that reduces discretization error in the prior step.

### 8. What are the strengths?

The method is framed as posterior sampling, not just reconstruction. The connection to PnP-DM is mathematically useful. The nonlinear Fourier phase retrieval experiment is a good stress test because the posterior can be multi-modal.

### 9. What are the weaknesses, limitations, or red flags?

Sampling remains costly compared with faster approximate flow methods. The paper focuses on non-blind inverse problems. Latent-space use is awkward because Langevin gradients through the decoder are expensive.

### 10. What challenges or open problems remain?

The main open problem is making the sampler fast enough for practical large latent or high-resolution systems without throwing away posterior faithfulness. Blind and semi-blind inverse problems are also left open.

### 11. What future work naturally follows?

Combine FlowSGS with one-step flow priors, hybrid pixel/latent Langevin schedules, EM-style blind inverse solvers, and posterior benchmarks like PosteriorBench.

### 12. Why does this matter for cabbageland?

Cabbageland cares about generative models as uncertainty-carrying mechanisms, not just image enhancers. FlowSGS is useful because it keeps the posterior-sampling question alive inside flow-based inverse solvers.

### 13. What ideas are steal-worthy?

Split measurement consistency from prior sampling. Treat stochastic-interpolant schedules as sampler design levers. Stress-test posterior samplers on multi-modal inverse problems, not just PSNR.

### 14. Final decision

Preserve. This is the strongest method paper in the day's inverse-problem lane.
