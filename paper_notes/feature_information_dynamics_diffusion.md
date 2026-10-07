# Feature Information Dynamics in Diffusion

## Basic info

* Title: Feature Information Dynamics in Diffusion
* Authors: Jia-Shu Pan, Tao Zhang, Yufei Huang, Yanjun Sheng, Tailin Wu
* Year: 2026
* Venue / source: arXiv; NeurIPS 2026 poster
* Link: https://arxiv.org/abs/2610.08626
* Date surfaced: 2026-10-07
* Why selected in one sentence: It gives a quantitative way to locate when semantic, spatial, and local features enter a diffusion trajectory.

## Quick verdict

* Must read

This is worth preserving because it turns "coarse-to-fine diffusion" from a folk story into a measurable information-density profile. The strongest part is the chained decomposition, which avoids double-counting shared information between feature levels. The caveat is that the diagnostic is descriptive and expensive: it needs trained conditional denoisers for the feature hierarchy.

## One-paragraph overview

The paper defines feature information density for diffusion and flow-matching models using the I-MMSE identity. For a feature such as class, mask, Canny edge, or frequency band, the information density is proportional to the gap between the optimal unconditional denoising loss and the optimal feature-conditional denoising loss at each SNR. For nested features, the paper introduces a chained decomposition that measures only each feature's incremental contribution beyond earlier features. Experiments confirm spectral autoregression in pixel diffusion, then show that representation choice changes the semantic-to-local ordering: pixel diffusion can put mask information before class identity, while RAE produces the cleanest class -> mask -> Canny order and the fastest matched-recipe convergence.

## Model definition

### Inputs

The framework uses clean data, noisy data at a chosen SNR, and optional feature conditions. In the main visual experiments, the feature hierarchy is class label, segmentation mask, and masked Canny edges over a SAM-validated ImageNet-256 subset.

### Outputs

The trained denoisers or flow models output clean-data predictions or velocity predictions. The analysis outputs MMSE curves, chained MMSE gaps, log-SNR feature information densities, peak locations, and cumulative information profiles.

### Training objective (loss)

The diagnostic relies on the usual denoising or flow-matching squared-error objective. The information density is computed from loss gaps: unconditional versus feature-conditioned for a single feature, or successive cumulative feature bundles for the chained decomposition.

### Architecture / parameterization

The theory is architecture-agnostic. The experiments compare pixel-space JiT-L/16, SDVAE with SiT-XL/2, VAVAE with LightningDiT-XL/1, and RAE with DiTDH-XL. The spectral experiments also use MNIST and CIFAR-10 frequency-band conditional models.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It tries to measure when different features are generated during diffusion. Existing accounts say diffusion is coarse-to-fine, but they usually do not quantify which information appears at which SNR or how representation choice changes that order.

### 2. What is the method?

Use the I-MMSE identity to relate the derivative of mutual information between a feature and a noisy sample to the difference between unconditional and feature-conditioned denoising errors. For nested features, condition cumulatively and subtract adjacent MMSE curves to isolate incremental information.

### 3. What is the method motivation?

If a representation organizes information well, semantic, spatial, and local details may enter the denoising process at separable SNR ranges. Measuring that structure could explain training speed, guide schedules, and expose entangled representations.

### 4. What data does it use?

The paper uses controlled MNIST and CIFAR-10 frequency decompositions, plus ImageNet-256 with 485 SAM-validated classes. Each ImageNet example is paired with a class, foreground mask, and masked Canny edge map.

### 5. How is it evaluated?

The authors estimate MMSE and chained MMSE gaps over sampled SNR grids, visualize density peaks, compare representation-specific feature orderings, and run matched-recipe unconditional FID trajectories across four representations.

### 6. What are the main results?

Forward-chained frequency decompositions recover a monotone low-to-high frequency progression, while independent single-band conditioning double-counts shared information. In the representation comparison, best FID over 200 epochs follows RAE 8.39, VAVAE 21.16, SDVAE 30.83, and pixel 78.51. Pixel diffusion places mask information earlier and stronger than class identity; VAVAE restores semantic-first behavior but still entangles mask and Canny; only RAE gives a strict class -> mask -> Canny ordering.

### 7. What is actually novel?

The novelty is the feature-localized information-density diagnostic and the chained decomposition. It lets researchers compare representation dynamics without reducing everything to FID.

### 8. What are the strengths?

The theory is clean, the estimator has a direct connection to standard denoising losses, and the chained setup addresses shared-information confounds. The cross-representation comparison is especially useful because it makes representation choice a temporal information-design problem.

### 9. What are the weaknesses, limitations, or red flags?

The analysis is distribution-level and does not necessarily describe every individual sample. The chained attribution depends on feature order. The reported association between cleaner information ordering and faster convergence is not a causal proof. The method can become expensive because each cumulative feature bundle needs its own conditional model.

### 10. What challenges or open problems remain?

The open question is whether these profiles can predict training efficiency or sample quality before a full run. Another challenge is extending the diagnostic to larger, messier hierarchies: object identity, layout, depth, dynamics, text conditions, and action.

### 11. What future work naturally follows?

Use feature information density to choose representations, design timestep schedules, set feature-dependent guidance strengths, and test whether action-conditioned video or world models resolve state variables in the right order.

### 12. Why does this matter for cabbageland?

Cabbageland cares about whether a representation carries the variables a model claims to use. This paper gives a tool for asking not only whether a feature is present, but where along the generative process it becomes available.

### 13. What ideas are steal-worthy?

Use loss-gap diagnostics to localize information in a generative process. Prefer chained decompositions over independent probes when features share content. Treat representation choice as control over the temporal order of information, not just reconstruction quality.

### 14. Final decision

Preserve. This is a strong mechanism paper for diffusion, representation learning, and interpretable generative dynamics.

