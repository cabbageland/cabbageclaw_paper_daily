# PosteriorBench: From Point Estimates to Posterior Matching in Evaluating Generative Inverse Solvers

## Basic info

* Title: PosteriorBench: From Point Estimates to Posterior Matching in Evaluating Generative Inverse Solvers
* Authors: Jiachen Yao, Zi-Siang Hsu, Xi Deng, Aditi Gupta, Xin Ju, Sally M Benson, Gege Wen, Anima Anandkumar
* Year: 2026
* Venue / source: arXiv:2609.20794
* Link: https://arxiv.org/abs/2609.20794
* Date surfaced: 2026-09-18
* Why selected in one sentence: It evaluates generative inverse solvers as posterior samplers rather than as single-reconstruction machines.

## Quick verdict

* Must read

This is a strong benchmark paper because it makes posterior recovery the object of evaluation. It is directly useful for anyone building generative solvers for underdetermined scientific problems. This note is based on the full arXiv PDF text.

## One-paragraph overview

PosteriorBench argues that many scientific inverse problems are intrinsically ambiguous, so evaluating only the best or mean reconstruction rewards models that collapse posterior structure. The benchmark defines four physics-based inverse tasks, constructs high-fidelity reference posterior ensembles with slow but reliable procedures such as rejection sampling and MCMC-style workflows, and compares solver ensembles against those references with metrics for mean, marginal uncertainty, distributional alignment, and spectral structure. The result is a benchmark that can show when a method matches observations but still misrepresents uncertainty.

## Model definition

### Inputs

The benchmark inputs are sparse, noisy, or low-resolution observations from four inverse problems: Darcy flow pressure observations, Poisson potential observations, carbon-storage well or column measurements, and light-transport reflectance/transmittance observations.

### Outputs

Evaluated solvers output ensembles of candidate latent fields or material fields. The benchmark compares those generated samples to weighted reference posterior samples.

### Training objective (loss)

PosteriorBench itself is an evaluation suite, not a newly trained model. The evaluated baselines use their native objectives, including guided diffusion or function-space diffusion objectives, ensemble data assimilation, and MC-dropout uncertainty. The benchmark metrics are posterior-mean error, posterior-standard-deviation error, maximum mean discrepancy, sliced Wasserstein distance, and radially averaged power-spectrum error.

### Architecture / parameterization

The benchmark is model-agnostic. It evaluates ECI sampling, DiffusionPDE, FunDPS, Fun-DDPS, DDIS, FunDiff, ES-MDA, and FNO with MC Dropout across the four tasks.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Generative inverse solvers are often evaluated by whether they produce one plausible reconstruction, even when many physically plausible latents explain the same observations. That lets a solver average modes, collapse uncertainty, or look accurate pointwise while failing the posterior.

### 2. What is the method?

PosteriorBench defines four inverse problems with controllable physics and high-fidelity reference posterior construction. For each case, it stores a reference weighted ensemble and evaluates generated ensembles with a five-metric posterior suite.

### 3. What is the method motivation?

Scientific inverse problems often feed downstream decisions. A solver that hides posterior spread or mode structure can be worse than one with a slightly less pretty mean reconstruction but better calibrated uncertainty.

### 4. What data does it use?

The tasks are Darcy flow inversion, Poisson source recovery, carbon capture and storage, and light transport material inference. The priors include binary permeability fields, smooth Gaussian random fields, geostatistical multimodal reservoir models, and layered scattering media.

### 5. How is it evaluated?

Eight solvers are evaluated with posterior-mean error, posterior-standard-deviation error, MMD, sliced Wasserstein distance, spectral error, and runtime. The paper also includes case-level visualizations and metric relationship plots.

### 6. What are the main results?

The main result is that pointwise accuracy and posterior quality can disagree. In LTMI, MC Dropout has lower posterior-mean error than FunDPS in Table 2, but much worse posterior-std error, MMD, and SWD, with visibly over-smoothed samples. Function-space diffusion samplers are generally strong but task-dependent; ES-MDA remains competitive or better in some settings. No method closes the posterior-matching problem across all tasks.

### 7. What is actually novel?

The novelty is not a new solver. It is the benchmark construction: pairing each inverse case with a reference posterior and explicitly scoring distributional recovery rather than single reconstructions.

### 8. What are the strengths?

The task design is conceptually clean. The metrics cover different posterior failures rather than collapsing everything into one score. The paper is honest that reference posterior construction is costly, which is precisely why most benchmarks avoid it.

### 9. What are the weaknesses, limitations, or red flags?

The benchmark is limited by the number of tasks, the cost and assumptions of constructing reference posteriors, and the solver set evaluated so far. The reference ensembles are not magic ground truth; they are high-fidelity approximations under the chosen priors and noise assumptions.

### 10. What challenges or open problems remain?

The hard next step is expanding to more domains while keeping reference posterior quality. Another open problem is connecting posterior metrics to downstream decision quality rather than treating distributional match as the final endpoint.

### 11. What future work naturally follows?

Add more inverse problems, include newer flow and diffusion posterior samplers, test calibration under misspecified priors/noise, and report task-level decision loss for scientific workflows.

### 12. Why does this matter for cabbageland?

Cabbageland cares about uncertainty, verification, and models that preserve usable state. PosteriorBench is a template for not letting generative systems launder ambiguity into a single confident output.

### 13. What ideas are steal-worthy?

Evaluate the ensemble, not the best sample. Include spectral or structural metrics when pixel/field means can lie. Build reference distributions even if they are expensive. Treat uncertainty as a represented object, not a plot after the fact.

### 14. Final decision

Preserve. This is the strongest paper in the batch for evaluation taste and uncertainty discipline.
