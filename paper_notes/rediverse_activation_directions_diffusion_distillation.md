# Restoring Diversity in Distilled Image and Video Generators by Probing Activations

## Basic info

* Title: Restoring Diversity in Distilled Image and Video Generators by Probing Activations
* Authors: Furkan Horoz, Ozgur Kara, Kaan Oktay, Adil Kaan Akan, Atakan Kara, Anand Bhattad, James Matthew Rehg
* Year: 2026
* Venue / source: arXiv:2611.18550v1, November 13, 2026; preprint
* Link: https://arxiv.org/abs/2611.18550
* Date surfaced: 2026-11-16
* Why selected in one sentence: It diagnoses a concrete spectral bottleneck in few-step diffusion students and tests targeted repairs against meaningful equal-energy controls.

## Quick verdict

* Highly relevant

Preserve the diagnostic and intervention design. The useful finding is that diversity loss can coexist with increased total activation variance, and teacher-derived directions can restore variation the student still knows how to render. Do not preserve the stronger claims that one block universally explains distillation collapse or that diversity recovery has no cost.

**Read basis:** Full-text main paper, plus selected measurement, implementation, ablation, and human-study passages in Appendices A, D, E.1/E.7, and J. No model/code execution, independent reproduction, or exhaustive appendix audit.

## One-paragraph overview

The authors compare a diffusion teacher and its four-step student on the same prompts and noise seeds. At an intermediate block, the student's activation distribution retains or increases total variance but loses effective dimensionality. Steering along teacher principal directions changes composition and pose, whereas the student's own leading direction tends to change appearance. ReDiverse turns that observation into two repairs: regress a prefix adapter's first-step activation toward a paired later-step teacher target, or inject stochastic perturbations along prompt-specific teacher directions at inference. Both leave the downstream student intact; combining them recovers much of the teacher's measured diversity across two image and two video model families, sometimes sacrificing reward scores or realism.

## Model definition

### Inputs

The base student consumes the usual noisy image/video latent, denoising timestep, and text conditioning. Diagnostic runs use the same initial noises and conditional branch for teacher and student at their first denoising step. FT training pairs each caption/noise with a teacher activation at block `ell` after advancing to a chosen teacher step `tau`. TF additionally uses a per-prompt cache of teacher principal directions and empirical spreads, estimated from 25 teacher trajectories independent of evaluation seeds.

### Outputs

The adapted prefix produces a hidden activation at the diagnosed block; the frozen suffix and remaining four-step sampling procedure produce an image or video. TF adds a hidden-state perturbation, not a new pixel-space guidance target. Neither variant directly emits a covariance matrix or guarantees a semantic mode label.

### Training objective (loss)

Only FT learns parameters. With the teacher and base student frozen, minimize elementwise MSE between paired activations:

`L = E[c, epsilon] ||h_student(ell, first_step; c, epsilon) - stopgrad(h_teacher(ell, tau; c, epsilon))||^2 / D`.

The teacher first advances `tau - 1` steps from the same initial noise. This is paired feature regression, not direct covariance matching, a new adversarial loss, or re-distillation of the entire model. Image/video token positions supply the loss; text positions in joint transformers do not. The recipe uses 100 DiffusionDB captions times 16 noises, 200 AdamW updates, batch 32, learning rate `1e-4`, and final-checkpoint selection.

TF has no learned objective. Center teacher activations into rows of `X`, diagonalize the small Gram matrix `X X^T`, recover unit directions `u_k`, and set their spread to `s_k = sqrt(lambda_k / N)`. At the student's first step only, add `sum_k alpha_k s_k u_k`, with independent `alpha_k ~ Uniform[-2, 2]`, default `K=8`, `N=25`. FT and TF may be combined.

### Architecture / parameterization

The method reuses matching teacher/student architectures: SDXL's U-Net, SD3's multimodal DiT, Wan 2.1's DiT, and MiniMax-H3's DiT. FT adds rank-32 LoRA to attention and feed-forward modules through the diagnosed block and enables it only at the first sampling step. Later layers and later steps retain the original student. Compressed or structurally different students would need an alignment/projection not demonstrated here.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Few-step image/video generators repeatedly produce similar compositions from different seeds. Output diversity scores detect that failure but do not say where useful variation stopped propagating or whether the decoder can still express it.

### 2. What is the method?

Measure seed-conditioned activation covariance across depth. Track total variance, `TV = sum(lambda)`, participation ratio, `PR = sum(lambda)^2 / sum(lambda^2)`, and `TV/PR`. Diagnose a block where effective dimensionality falls while total variance remains high. Then repair that interface using paired teacher-feature regression, teacher-principal-direction steering, or both. Keep the suffix fixed to test whether the existing downstream model can render the restored variation.

### 3. What is the method motivation?

Increasing noise indiscriminately can add texture changes or defects without recovering structural modes. If the suffix can decode teacher directions, a targeted prefix/activation intervention may restore composition without retraining the rendering stack. That is an experimentally supported hypothesis for the studied students, not a theorem about every generator.

### 4. What data does it use?

FT uses 1,600 caption/noise pairs from the first 100 DiffusionDB captions, disjoint from evaluation prompts. Automatic image evaluation uses 553 GenEval prompts and 100 seeds per prompt; video uses 300 VBench prompts and ten seeds each. The diagnostic covariance study uses 1,000 noises per prompt, with 100 image prompts and 20 video prompts per backbone. TF needs a separate 25-run teacher bank for each evaluation prompt.

### 5. How is it evaluated?

Four public four-step teacher/student pairs: SDXL/DMD2, SD3/TDM, Wan 2.1/lightx2v, and MiniMax-H3/Turbo. Arms share evaluation noise banks. Diversity uses multiple perceptual/embedding distances, Vendi, and camera-trajectory variation; quality/alignment uses CLIPScore, preference rewards, VBench consistency, and text-video similarity. Compare FT, TF, combined, original student, teacher, image noise optimization/DP-DMD, and video DFD. SD3 ablations test block placement, step gating, direction count, and teacher/student/random direction sources. Human evaluation is narrower: ten selected prompts per evaluated model, 59 distinct raters overall, randomized A/B order, and ties counted as half.

### 6. What are the main results?

- The reported student/teacher PR ratios at the diagnosed blocks are 0.37-0.60, while TV ratios are 1.03-2.92: more variance does not mean broader effective variation.
- On SD3, combined DINO diversity rises from 48.4 to 60.1, near teacher 61.6. ImageReward falls from 1.026 to 0.872; the teacher is 1.017. Do not hide that trade-off.
- On Wan 2.1, combined DINO rises from 31.6 to 52.2 versus teacher 51.6; V-JEPA diversity remains below the teacher, 18.7 versus 20.9. ViCLIP text-video similarity falls from 21.5 to 20.5.
- On MiniMax-H3, combined DINO rises from 36.5 to 50.9 versus teacher 52.5. These are diversity scores, not recognition accuracies or recovered-mode percentages.
- On the smaller SD3 ablation set, teacher-direction TF gives DINO 53.0 / ImageReward 0.878; equal-energy random directions give higher DINO 57.8 but much worse reward 0.719. Student directions give only DINO 49.5 but preserve reward 0.954. This directly exposes why a single diversity metric is inadequate.

### 7. What is actually novel?

The combination of blockwise spectral diagnosis, an intervention showing the suffix can decode teacher variation, and a targeted first-step repair across image/video pairs. LoRA, feature regression, PCA steering, and early-step layout sensitivity are existing ingredients. The strongest novelty is a testable failure localization and repair recipe, not the invention of structured generation or a universal theory of distillation.

### 8. What are the strengths?

The diagnosis separates variance magnitude from spectral spread. Paired seeds and an unchanged suffix make the intervention legible. Teacher/student/random-direction controls test specificity, while FT-only/TF-only arms separate learning from injected variability. Multiple backbones/modalities and human judgments reduce dependence on a single proxy. The paper reports quality failures rather than only the best diversity number.

### 9. What are the weaknesses, limitations, or red flags?

- **Cost:** Training-free is not teacher-free. Twenty-five partial teacher trajectories per new prompt, cached high-dimensional directions, and teacher access must be amortized; a four-step student label alone does not describe end-to-end latency.
- **Representation inference:** PR is an eigenvalue-concentration statistic, not exact rank or a count of semantic modes. A nonlinear suffix can change spectral geometry, so the paper's broad dimensional-bottleneck language is stronger than a general proof supplied by these probes.
- **Quality trade-off:** Random directions can score even higher on diversity while harming alignment. Teacher directions help, but combined recovery still lowers some reward scores and video realism.
- **Scope:** Matching architectures are assumed. A limited set of distilled checkpoints does not establish an intrinsic single-block hallmark of all distillation recipes.
- **Selection:** Detailed one-factor ablations are on SD3 and a smaller prompt set; their teacher/student values must not be mixed numerically with the main table.
- **Evaluation:** Hundreds of prompts support the automatic study, but the human study uses only ten selected prompts per model. Rater count is not independent prompt coverage; no general content-quality or deployment guarantee follows.

### 10. What challenges or open problems remain?

Automatically selecting block, teacher target step, perturbation scale, and directions without quality-driven tuning; keeping prompt-specific teacher preparation affordable; handling nonmatching architectures; and testing whether the intervention helps rare compositional modes rather than familiar variants. Longer video horizons and distribution-shifted prompts may change the relevant block or direction structure.

### 11. What future work naturally follows?

Distill with an explicit activation-direction preservation objective from the start. Compare prompt-specific teacher bases with reusable low-cost bases and learned projections for compressed students. Run equal-wall-clock evaluations including teacher preparation/cache memory. Test held-out compositions, rare attributes, longer horizons, and several distillation recipes while reporting a quality-diversity frontier rather than a single best point.

### 12. Why does this matter for cabbageland?

It supplies a concrete alternative to vague claims that a representation is more expressive or controllable. Measure the distribution at a chosen interface, intervene there, and test what the fixed downstream system can actually do. The same experimental logic could inform video/world-model bottlenecks and compositional state, but those transfers are proposals, not results in this paper.

### 13. What ideas are steal-worthy?

- Track activation energy and effective dimensionality separately; a healthy norm can hide a collapsed spectrum.
- Keep a decoder fixed while restoring a candidate missing direction to distinguish inaccessible variation from destroyed capacity.
- Match perturbation energy across teacher, student, and random bases; report quality beside diversity.
- Gate structure-level interventions to the earliest useful step and test whether extending them corrupts later rendering.
- Treat teacher setup, direction storage, and reuse count as part of the method's compute budget.

### 14. Final decision

**Preserve as highly relevant.** Reuse the measurement-and-control experiment before adopting the complete repair pipeline. Require teacher-preparation-inclusive timing and a quality-diversity comparison before claiming a practical improvement. The durable lesson is that variation's direction matters, not merely its magnitude.
