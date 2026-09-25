# Beyond Compression: Training Latent Representations for Stable Long-Horizon Rollout in Neural Surrogate Solvers

## Basic info

* Title: Beyond Compression: Training Latent Representations for Stable Long-Horizon Rollout in Neural Surrogate Solvers
* Authors: Andreas E. Robertson, Ashley T. Lenau, John D. Shimanek, Benjamin A. Jasperson, Vivek Oommen, David L. Damm, Krishna Garikipati, Remi Dingreville
* Year: 2026
* Venue / source: arXiv:2609.30198
* Link: https://arxiv.org/abs/2609.30198
* Date surfaced: 2026-09-25
* Why selected in one sentence: It shows that latent surrogate solvers need representations trained for stable long rollout, not merely compact reconstruction.

## Quick verdict

* Must read

This is the strongest paper in the batch because it targets the representation/consumer mismatch directly. The paper shows that reconstruction quality and one-step prediction can improve while long-horizon rollout gets worse, then tests a concrete set of training interventions that make the latent space less sensitive and more rollout-suitable. The caveat is that the recipe is empirical and domain-specific, but the framing is broadly useful.

## One-paragraph overview

Latent dynamics models accelerate scientific simulation by encoding high-dimensional physical fields, rolling out dynamics in latent space, and decoding the result. The usual justification is compression, but this paper argues that compression is the easy part. The hard part is making the latent representation stable under repeated autoregressive use. The authors evaluate Koopman-inspired autoencoder training, latent Hamming noise injection, dynamics-side noise injection, and multi-step rollout fine-tuning across spinodal decomposition, active matter, and crystal-plasticity fatigue simulations. The headline result is that training interventions aligned with long rollout reduce accumulated error even when they degrade familiar short-horizon metrics.

## Model definition

### Inputs

The model receives sequences of physical simulation fields. Depending on the dataset, these are concentration fields for spinodal decomposition, active-matter state variables, or crystal-plasticity fatigue fields. The dynamics model receives latent encodings of recent states as rollout context.

### Outputs

The system predicts future physical fields autoregressively. Internally, an autoencoder maps fields to latent representations, a latent dynamics model predicts future latent states, and the decoder maps those states back to physical fields.

### Training objective (loss)

The autoencoder uses reconstruction losses augmented by Koopman-inspired latent-dynamics constraints, KL regularization in some ablations, and Hamming latent-noise injection. The dynamics model is trained with direct prediction losses, with additional input-noise injection and multi-step rollout fine-tuning. The paper emphasizes that losses optimized for reconstruction or one-step prediction can diverge from the deployed long-rollout objective.

### Architecture / parameterization

The system uses a latent dynamics model built from an autoencoder plus an autoregressive dynamics predictor. The paper modernizes the latent representation with a spatial autoencoder and uses an AViT-style dynamics model. Koopman-inspired training adds a learned convolutional Koopman operator in latent space.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It tries to make latent neural surrogate solvers stable enough for long autoregressive rollout. The failure mode is that a latent representation trained only for reconstruction can be a poor state space for long-horizon dynamics.

### 2. What is the method?

The paper studies training-level interventions rather than a single new architecture. It adds Koopman-inspired constraints during autoencoder training, injects Gaussian noise into latent codes before the Koopman transformation, injects noise into dynamics-model inputs, and fine-tunes the dynamics model over multiple rollout steps.

### 3. What is the method motivation?

Autoregressive rollout compounds small errors. If the decoder is highly sensitive to small latent perturbations, ordinary latent prediction errors can explode in output space. Koopman-style constraints and Hamming noise are meant to shape a latent space where errors are less damaging and latent points are more robustly separated.

### 4. What data does it use?

The paper evaluates on spinodal decomposition, active matter evolution, and mesoscale crystal-plasticity simulations for high-cycle fatigue. The fatigue task is especially useful because the target event emerges over horizons far beyond the training observations.

### 5. How is it evaluated?

It reports rollout errors such as RelMSE and VRMSE at multiple horizons, decoder sensitivity diagnostics, latent linearity tests, compute and memory comparisons, and qualitative physical-field rollouts. It also tests extrapolation in high-cycle fatigue by rolling beyond the training horizon.

### 6. What are the main results?

The cumulative interventions reduce long-rollout error by about 40% in the reported active-matter setting. Koopman training reduces decoder sensitivity even when it does not make the dynamics more linear in the simple sense. Hamming noise further improves 15-step rollout error by roughly 20% relative to the KL-regularized Koopman model, and dynamics-side noise adds another roughly 20% at long horizon while hurting one-step accuracy. The proposed latent model matches or beats full-resolution performance in the tested settings while using around two orders of magnitude fewer FLOPs and half the GPU memory in the reported 40-step comparison.

### 7. What is actually novel?

The novelty is the systematic demonstration that representation training for latent scientific surrogates should be judged by long-rollout stability, not reconstruction or one-step prediction. The individual ingredients are familiar, but the paper ties them to decoder sensitivity and rollout-aligned representation shaping.

### 8. What are the strengths?

The paper has the right diagnostics. It shows metric conflict rather than hiding it, tests interventions cumulatively and individually, and includes a fatigue case where the surrogate must extrapolate over long physical horizons. The compute and memory argument is also concrete.

### 9. What are the weaknesses, limitations, or red flags?

The method is still an empirical recipe, and the best intervention mix may not transfer cleanly to other PDE families or surrogate architectures. Koopman language should not be overread: the constraint improves sensitivity more than it proves genuinely linear latent dynamics. The paper also leaves open how to choose the intervention strength without substantial validation.

### 10. What challenges or open problems remain?

Open problems include automatic selection of rollout-aligned representation objectives, robustness under simulator mismatch, stability over even longer horizons, and whether similar ideas help learned world models outside scientific fields.

### 11. What future work naturally follows?

Useful follow-ups include decoder-sensitivity regularizers, latent robustness metrics during training, adaptive multi-step curriculum schedules, and applying the same representation diagnostics to video world models or model-based RL.

### 12. Why does this matter for cabbageland?

Cabbageland cares about state representations that can support future prediction and action. This paper is a clean reminder that a state can reconstruct beautifully and still be a bad substrate for the computation that consumes it.

### 13. What ideas are steal-worthy?

Evaluate representations by downstream rollout, not just reconstruction. Track decoder sensitivity as a first-class diagnostic. Add noise where deployment errors will appear, not just where the loss is easiest. Treat multi-step stability as a representation property.

### 14. Final decision

Preserve. This is the most transferable mechanism paper of the day.
