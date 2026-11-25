# Linear Probes Can Guide: Training-Free Control of Representation Generators

## Basic info

* Title: Linear Probes Can Guide: Training-Free Control of Representation Generators
* Authors: Pengwei Wang, José Morano, Botond Fazekas, Hrvoje Bogunović
* Year: 2026
* Venue / source: arXiv preprint, 2611.33037v1, submitted November 24, 2026
* Link: https://arxiv.org/abs/2611.33037
* Date surfaced: 2026-11-25
* Why selected in one sentence: It turns a frozen representation generator's linearly readable coordinates into controllable requests while explicitly measuring when latent compliance fails to change the image.

## Quick verdict

* Highly relevant

Preserve the interface and the anti-hacking evaluation, not a claim of exact semantic posterior sampling. Fit-Path is a useful guidance baseline because it separates request uncertainty from how a denoiser propagates a correction. “Training-free” excludes generator retraining, not probe labels, covariance fitting, or development-set tuning.

**Access:** Full PDF acquired. Read main theory/method, main results and ablations, limitations, and selected appendix composition, implementation, and timing details. Not every solver derivation or qualitative image independently audited; code/checkpoints not executed. The [project](https://penway.cn/lism/) resolves and links a [repository](https://github.com/penway/LiSM) and [Hugging Face page](https://huggingface.co/penway47/LiSM); this is not executable-release verification.

## One-paragraph overview

An RAE generator operates directly on pretrained vision features rather than a purely reconstruction-oriented VAE code. Those features already admit useful linear readouts. LiSM applies such readouts to a flow denoiser's clean prediction, constructs semantic constraints on their logits, and changes the flow using inverse-problem-style conditioning. Its key warning is that moving only in the probe direction can satisfy the latent measurement while leaving decoded content wrong. Fit-Path therefore weights requests using fitted feature uncertainty and spreads the update through a finite displacement of the denoiser. The result is broader global/local control with less internal-versus-visible disagreement, at additional sampling cost and sometimes lower sample preservation.

## Model definition

### Inputs

At each step: noisy representation tokens z_t, time t, a frozen representation-flow denoiser, and a semantic request. Requests use an affine probe r(z) = Wz + b, transformed into margins/signs/thresholds y(z) = Az + c. Positive request scores mean constraints are satisfied. Global requests pool tokens; local ones act on patches. The main non-class tasks additionally supply the requested ImageNet class to the generator.

### Outputs

A corrected clean representation estimate and guided flow velocity, ultimately decoded into a 256×256 image. Supported evaluations request class, image attributes, foreground layout, or keypoints. The method does not output a certified satisfaction probability or guaranteed valid image.

### Training objective (loss)

The RAE encoder, decoder, and denoiser stay frozen. The theoretical identity assumes an ideal MSE-optimal clean denoiser f(z_t,t) = E[Z | z_t]. Probes are fitted using clean-feature supervision and covariance is estimated from clean features; this is not zero-training conditioning in the literal sense. This read did not reconstruct every task-specific probe-fitting loss, so no universal probe loss is asserted.

At inference, the target is p_L(z) proportional to p(z)L(Az+c). L combines hard or softened score-sign requirements. The true noisy conditioning weight is E[L(AZ+c) | z_t], not L evaluated at the mean. Gaussian variants approximate that expectation and differentiate with covariance held fixed. There is no new generator optimization objective in LiSM.

### Architecture / parameterization

Main generator: pretrained RAEv2, frozen DINOv3-L encoder, reconstruction decoder, and DiT-DH-XL denoiser. Sampling uses a 100-step shifted Euler grid. Linear probes and a fitted covariance supply a small semantic interface.

The flow path is z_t = (1−t)z + tε, with t=1 noise and t=0 data. Let z_hat=f(z_t,t). LiSM computes request weights λ, direction u=Aᵀλ, correction Δ=αR(u), and velocity (z_t−z_hat−Δ)/t. Fit-Path uses a Gaussian-prior posterior covariance approximation and

`R_Path(u) = (c_t / τ) [f(z_t + τu,t) − f(z_t,t)]`, with `c_t=t²/(1−t)`.

The query radius caps per-patch displacement; τ is deliberately finite rather than a numerical approximation to an infinitesimal Jacobian. This costs one extra denoiser forward call and no denoiser backpropagation. The singular endpoint is not guided; implementation skips early steps as specified in the appendix.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Add new semantic controls to a frozen generator without separately training noise-aware classifiers or repeatedly decoding and backpropagating through image-space predictors. More subtly: make a semantic update affect actual imagery rather than merely the coordinates read by its own probe.

### 2. What is the method?

Exploit affine expectation commutation: r(E[Z|z_t]) = E[r(Z)|z_t]. Build request operators from clean probes; separate the weighting of unmet requirements from the representation response. Fit-Path uses fitted Gaussian score uncertainty for weighting and a finite denoiser-response path for the correction. Compare identity, covariance, JVP/VJP, finite-difference, and path responses rather than conflating them.

### 3. What is the method motivation?

A pretrained feature space supplies useful linear semantic coordinates. But the measured subspace is small: unmeasured features can stay inconsistent with requested logits. Denoiser response captures dependencies between coordinates; uncertainty distinguishes a genuinely likely constraint from a large mean logit. Neither ingredient alone universally solves local and global control.

### 4. What data does it use?

ImageNet-based generation and class requests; task-specific clean-feature support for attributes, foreground, and pose. Foreground requests use PartImageNet masks; keypoint requests use overlapping ImageNet/AP-10K categories. Development has 384 request–seed pairs and test 3,840; a fixed 810-request subset supports ablations. The pretrained representation and generator carry substantial earlier training not counted as new conditioning work.

### 5. How is it evaluated?

Decode images and use external task predictors different from the guiding networks. Adherence is class accuracy, attribute-score pass rate, foreground IoU, or PCK@0.2. Preservation is distribution precision for class and class retention for the other tasks. “Hack” averages positive internal-minus-external adherence gaps. Guidance strengths are selected on disjoint development requests; non-class tuning requires at least 75% development class retention, which does not guarantee that rate on test.

Shared initial noise improves paired comparison. Still, predictors differ across guidance families and are not omniscient judges; results establish practical interfaces, not isolated mathematical superiority under identical readout quality.

### 6. What are the main results?

Main Table 1: Fit-Path geometric-mean adherence 87.2, preservation 72.8, hacking gap 4.7, 8.5 seconds/image. Noise-aware CG: 72.1/78.0/7.2 and 5.0 seconds. Unguided timing is 4.6 seconds. Fit-Id reaches adherence 79.5 and preservation 76.0 but hacking 19.1.

Among LiSM-adapted inverse solvers, DCPS reaches adherence 82.9 and preservation 76.1 at 48.8 seconds; those are a different comparison from pixel-space DCPS in Table 1. An isotropic covariance response achieves strong global adherence but very weak local adherence in the ablation, illustrating why aggregate numbers need decomposition. Encoder transfer refits only probes/covariance and reuses DINOv3 guidance strengths; effectiveness follows each encoder's readability.

### 7. What is actually novel?

The useful contribution is connecting clean affine semantic readouts to representation-flow conditioning, organizing solver choices into uncertainty weighting and representation response, and proposing the finite Path response. Conditional-expectation linearity itself is elementary; exact conditioning and exact semantic control do not follow from it.

### 8. What are the strengths?

An explicit interface, meaningful component ablations, independent decoded-image measurements, visible compute costs, and an acknowledged failure mode. Tests cover both spatial and global requests. The finite-response mechanism is simple enough to steal without adopting an entirely new generator.

### 9. What are the weaknesses, limitations, or red flags?

- Exact mean logits require an ideal denoiser; fitted neural flows are approximate.
- Nonlinear L does not commute with expectation. Gaussian weighting remains a coarse posterior model of clustered features.
- Unreadable attributes cannot be requested, and probe/covariance estimation still needs suitable data.
- Three main tasks preserve class conditioning; they do not show unrestricted compositional text generation.
- Higher adherence can reduce preservation. No solver is best everywhere.
- Heterogeneous metric geometric means conceal task-specific compromises. A small measured hacking gap is not proof that hacking is absent.
- Runtime is a specific 100-step, 256px, hardware-dependent comparison, not a universal latency claim.

### 10. What challenges or open problems remain?

Calibrate semantic uncertainty beyond a Gaussian approximation, handle correlated simultaneous requests, measure decoder consistency without relying solely on pretrained judges, and characterize when guidance leaves the learned image manifold. Robustness under unusual requests or distribution shift remains more important than another average adherence point.

### 11. What future work naturally follows?

Evaluate equal-compute and equal-probe-quality controls; plot adherence/preservation/hacking curves rather than a single tuned point. Compare class-conditioned and null-conditioned composition at matched label budgets. Add human or task-grounded validity checks and out-of-distribution requests. Test whether training representations for controlled decoding improves the interface rather than merely its linear accuracy.

### 12. Why does this matter for cabbageland?

It joins representation learning, generative control, uncertainty, and verification through a legible mechanism. It suggests a concrete alternative to continually enlarging conditioning networks: choose a representation whose meaningful quantities can be measured, then test whether controlling those measurements controls the output.

### 13. What ideas are steal-worthy?

1. Separate request weighting from response propagation in both code and ablations.
2. Use internal–external disagreement as a first-class diagnostic, not only the guiding score.
3. Compare finite denoiser displacements with local gradients; locality can be the wrong approximation.
4. Report visible adherence, preservation, and total compute together.
5. Refit probes/covariance while holding guidance strengths fixed to reveal representation dependence.

### 14. Final decision

Preserve as a controllable-generation baseline and evaluation pattern. Reproduce the Fit-Id versus Fit-Path hacking difference before extending it. Do not describe LiSM as exact posterior semantic sampling, label-free guidance, or universal compositional generation.
