# Guidance as Variance Matching

## Basic info

* Title: Guidance as Variance Matching
* Authors: Ali Backour, Artem Lukoianov, Frank Permenter, Tommi Jaakkola, Justin Solomon, Vincent Sitzmann
* Year: 2026
* Venue / source: arXiv preprint, 2611.34801v1; not a peer-review claim
* Link: https://arxiv.org/abs/2611.34801
* Date surfaced: 2026-11-26
* Why selected in one sentence: It replaces guidance-scale sweeps with a closed-form variance calibration rule and makes the explanatory assumptions testable.

## Quick verdict

* Highly relevant

Preserve the calibration method and the separation between denoising accuracy and generation quality. The posterior-covariance explanation is a useful model, not an established universal account of classifier-free guidance. Multi-modal experiments are meaningful, but schedule improvements and human evidence have specific limits.

## One-paragraph overview

Guided diffusion combines two clean-data predictions as D0 + w(D1-D0). Instead of selecting w by repeatedly generating samples and optimizing a chosen metric, this paper fits w from paired model predictions on forward-noised clean calibration examples. It asks that the spread of guided predictions match the clean data's spread, globally or at each noise level. Its motivating model treats finite-training denoiser errors as a scaled copy of posterior uncertainty; amplifying the difference between two predictions then restores variability lost by posterior-mean denoising. The practical statistic is marginal total variance, not a measured full conditional posterior. Primary full-text inspection covered main method/results/limitations and selected appendix calibration, cost, and covariance/subset ablations; proofs and all qualitative images were not exhaustively audited. Models and code were not run.

## Model definition

### Inputs

A noisy clean example x_t, noise level, and the model's normal conditioning: text, class, a first frame, actions, or other released-model inputs. Calibration additionally needs clean examples x0, their corresponding conditioning, and both model branches/predictions on the same forward-noised inputs. Weak/strong predictions may be unconditional/conditional branches or separate models; their interpretation is not identical in every guidance regime.

### Outputs

Each pretrained model yields a clean-data prediction D0 or D1 after converting its native noise/velocity parameterization if necessary. VMG fits either one scalar guidance weight or a noise-dependent weight, and combines predictions into D_w = D0 + w(D1-D0). The unchanged released sampler turns these predictions into images, videos, audio, motion, or world-model rollouts. It is not a new learned generator or uncertainty head.

### Training objective (loss)

No additional generator training. The explanatory denoiser objective is squared clean-data prediction error, whose ideal optimum is E[x0 | x_t]; native noise/flow parameterizations are converted into this representation. Practical calibration solves Var[D_w] = Var[x0], where Var means total variance/trace. Let Δ = D1-D0, a = Var[Δ], b = Var[D0] - tr Cov(D0,D1), and c = Var[D0] - Var[x0]. Then a w² - 2 b w + c = 0, with roots (b ± sqrt(b²-ac))/a when defined. The usual rule uses the positive root. Averaging coefficients over noise levels gives the global fit. This is moment matching, not FID optimization or a full likelihood fit; degenerate/no-real-root cases require attention rather than assuming every per-step equation has a solution.

### Architecture / parameterization

An inference/calibration wrapper around released diffusion/flow generators, not a new backbone. Main experiments retain each released sampler and step count. The mechanistic derivation uses an idealized effective-sample-mean denoiser: across independent retrainings, prediction errors have covariance proportional to Cov(x0 | x_t). Real CFG branches share parameters and differ in conditioning, so this abstraction is imperfect.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Guidance scales strongly affect generation, yet common explanations do not quantitatively predict practical scales. Tuning by a single metric is expensive and produces incompatible optima: on SD 3.5 Medium, the paper's optima range from 1 for Inception recall to 11.5 for CLIP score.

### 2. What is the method?

Estimate variances/cross-covariances of paired predictions on a clean calibration set noised at the sampler's levels. Solve the quadratic moment condition, either per level or after coefficient averaging. Use the resulting weight with the existing sampler. No reward judge, learned schedule, or generation sweep is required to fit it.

### 3. What is the method motivation?

Posterior means have less marginal variance than clean data, by total covariance. The paper proposes that errors from finitely trained denoisers retain posterior-shaped scatter, and guidance expands it. Correct covariance shape matters: adding unrelated isotropic or data-covariance noise to restore only the total amount of variance does not reproduce the gain.

### 4. What data does it use?

Disjoint calibration/evaluation examples from COCO, MJHQ-30K, UCF-101, OpenVid-1M, Bridge, AudioCaps, Song Describer, and KIT-ML, matched to model modality. SD 1.5/3.5 use 5,705 COCO calibration images and 10,000 evaluation examples; SD 3.5 Medium uses 40 noise levels. A subset experiment tests calibration with fewer examples. Native resolution matters: the authors use native high-resolution MJHQ images for FLUX rather than upsampling low-resolution COCO and distorting the variance target.

### 5. How is it evaluated?

Eleven released CFG models across five modalities; released guidance defaults, metric-swept constants, and hand-designed schedules. Metrics include distribution distances, precision/recall, alignment, and modality-specific measures. Toy trained-model experiments and selected high-dimensional diagnostics probe the covariance explanation. An informal blind pairwise study uses matched SD 3.5 Medium prompts/noise, with bootstrap intervals over raters. Its published constant is omitted because it is very close to VMG's, not because it lost a human comparison.

### 6. What are the main results?

* SD 1.5's constant is 7.44 versus released 7.5; SD 3.5 Medium is 4.14 versus 4.5. Across eleven models the appendix's average-variance objective has 12% median relative distance to published scales: close, not exact recovery everywhere.
* On SD 3.5 Medium, 256-image subset fits have standard deviation 0.06. The full 5,705-image/40-level fit uses roughly 460,000 branch evaluations versus 800,000 for one 10,000-image generation setting and about 34 million for its 42-scale sweep.
* The 1,458-vote, 41-person study gives VMG constant Elo 1048 ± 36 versus 985 ± 40 for the FDDINOv2-tuned constant and 874 ± 44 for FID tuning; its schedule scores 1088 ± 43. These are fitted study ratings, not universal quality scores.
* Schedule results are mixed: SVD FVD improves 141.2 to 113.7 and Wan 261.0 to 220.0, while CogVideoX worsens 236.3 to 262.1. Distributional/alignment trade-offs remain, including audio.
* Selected independently trained model pairs improve when extrapolated in either direction; earlier-checkpoint guidance needs larger scale than independent-model guidance. Neither finding licenses negative CFG for arbitrary prompts/models.

### 7. What is actually novel?

The quantitative, closed-form guidance calibration criterion and the finite-training-error/posterior-covariance account connecting it to guidance. It does not invent covariance-aware sampling, guidance schedules, or the observation that denoising loss and final generation quality differ.

### 8. What are the strengths?

A legible statistic and inexpensive fit; explicit equations; broad modalities; disjoint calibration/evaluation; metric trade-offs rather than a single leaderboard; hypotheses beyond retrospective explanation; a project page linking public code. Matching the full latent-channel covariance is also compared with trace matching for a selected model.

### 9. What are the weaknesses, limitations, or red flags?

The derivation first averages over retrainings at fixed inputs, then practice averages over inputs for one fixed pair. Effective sample counts, independence, and posterior-aligned errors are assumptions, not general neural-network theorems. Fixed model errors correlate across inputs and time, which can collapse diversity. Channel-covariance agreement does not prove full spatial conditional-covariance agreement. CFG conditioning contributes effects omitted by the error-only explanation. The human study is one model and informal; it does not compare directly to the released constant. Calibration is not data-free, and published defaults themselves are imperfect ground truth.

### 10. What challenges or open problems remain?

How representative must calibration data be under prompt/domain shift? When does matching a trace hide the wrong covariance geometry? How should invalid per-step roots be handled? Can a single criterion retain rare modes and improve prompt fidelity without correlated-error collapse? How does the rule change for distilled or nonstandard model pairs?

### 11. What future work naturally follows?

Test cross-domain calibration transfer; estimate geometry rather than just total spread; compare independent versus shared-checkpoint pairs; report rare-mode coverage, conditional adherence, and human preference at matched budget. Add a direct blinded comparison against the released default and test sensitivity to resolution/preprocessing and calibration-prompt composition.

### 12. Why does this matter for cabbageland?

It offers an explicit control/calibration interface for generative systems and a mechanism-rich baseline. More importantly, it prevents a category error: a better point predictor need not be a better finite-step sampler. That distinction transfers to world-model prediction, proposal generation, and controllability evaluation.

### 13. What ideas are steal-worthy?

* Solve a tractable moment equation from existing predictions before adding a learned controller.
* Separate the statistic that sets a control knob from independent metrics that test its output.
* Test a mechanism with new predictions: sign reversal and error correlation, not only a benchmark increase.
* Audit the geometry and diversity lost by scalar calibration; matching total variance is an interface, not a certificate.

### 14. Final decision

Preserve; try VMG as a low-cost baseline when clean representative calibration examples and suitable paired predictions exist. Keep its practical rule separate from its stronger explanatory claims. [Project/code](https://ottogin.github.io/vmg/); [primary PDF](https://arxiv.org/pdf/2611.34801).
