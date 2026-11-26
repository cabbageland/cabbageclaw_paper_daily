# Not all world models can doubt: how training objective and architecture shape epistemic uncertainty in JEPA and RSSM world models

## Basic info

* Title: Not all world models can doubt: how training objective and architecture shape epistemic uncertainty in JEPA and RSSM world models
* Authors: Simon Baur, Wojciech Samek, Jackie Ma
* Year: 2026
* Venue / source: arXiv preprint, 2611.34830v1; not a peer-review claim
* Link: https://arxiv.org/abs/2611.34830
* Date surfaced: 2026-11-26
* Why selected in one sentence: It traces uncertainty failures upstream through representation and recurrence instead of treating the uncertainty estimator as an isolated module.

## Quick verdict

* Highly relevant

Preserve the stage-wise intervention protocol and the posterior-versus-prior readout ablation. The study supports a concrete failure mode of these Dreamer-type features; it does not establish that JEPAs universally have better uncertainty or that reconstruction is intrinsically wrong. Native-resolution, checkpoint, and planning-selection differences matter.

## One-paragraph overview

The authors freeze a JEPA world model, LeWorldModel, and a DreamerV3 RSSM trained on the same recorded data, then fit post-hoc uncertainty heads. Using simulator state access, they displace a body or object coordinate, re-render, and follow the perturbation through successive internal stages to the final uncertainty score. Both encoders initially see changes; Dreamer's recurrent update attenuates brief ones, while smaller entities attract less reconstruction gradient and can end up weakly represented. Testing a head on the posterior before recurrence restores much of the lost signal. Detection, error ranking, and planning show consequences, with meaningful exceptions. This note is based on main full text and selected appendix architecture/readout/planning protocols; not all tables, code, or simulator behavior were independently audited.

## Model definition

### Inputs

RGB observation histories and action histories from ten simulators. LeWM uses the last three 224x224 frames, with actions embedded into the same feature width. Dreamer uses native 64x64 observations and recurrent history, trained in sequences of sixteen model steps. Simulator state is available to the evaluation intervention machinery, not a direct model input. Goal-conditioned planning additionally receives a goal image.

### Outputs

LeWM predicts the next 192-dimensional image embedding. Dreamer's categorical latent-state prior predicts 32 groups of 32 classes, with a decoder reconstructing observations. The post-hoc head produces a scalar epistemic-variance score from predictor features. A CEM planner emits candidate action sequences optimized against a goal cost with or without uncertainty penalty. The method is a diagnostic/readout study, not a newly trained robot policy.

### Training objective (loss)

LeWM minimizes squared next-embedding prediction error against a stop-gradient target plus SIGReg anti-collapse regularization (weight 0.09). The appendix specifies a sketched isotropic-Gaussian regularizer rather than generic contrastive training. Dreamer minimizes pixel reconstruction error plus balanced posterior/prior KL terms, with free bits and weights 0.8/0.2. Reward and continuation heads are inert here because recorded rewards are zero and continuation constant: this is not a reproduction of a full reward-learning Dreamer agent.

The last-layer Laplace fit accumulates training-feature Gram matrix G = sum ψψᵀ and uses precision Λ = G/σ² + I/τ², giving u(ψ) = ψᵀΛ⁻¹ψ. It is a Gaussian last-layer approximation; on categorical Dreamer predictors it should not be mistaken for a fully Bayesian categorical world model. A five-head bootstrapped MLP ensemble uses the original one-step prediction loss while keeping the backbone frozen.

### Architecture / parameterization

LeWM: ViT-Tiny with patch size 14, a 192-dimensional frame embedding, causal transformer over three frames/actions (depth six), and prediction MLP; uncertainty reads its 2048-dimensional penultimate predictor feature. Dreamer-small: CNN encoder, 512-dimensional layer-normalized GRU, 1024-dimensional categorical stochastic state, prior/posterior MLPs, and transposed-CNN decoder; main uncertainty reads the 512-dimensional prior-head feature. A posterior-head ablation reads the state before recurrent attenuation. Architecture, input resolution, temporal structure, and objective all differ.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Uncertainty is routinely used to avoid unfamiliar model states or penalize unreliable imagined plans. But a head can only react to information retained by its features. The paper asks which stages lose physically meaningful changes before an uncertainty estimate can see them.

### 2. What is the method?

Set one simulator coordinate to x' = x + εσ_i e_i, render it, and compute normalized feature displacement at encoder, posterior/recurrent state, predictor, and uncertainty. Repeat for body/object changes and different persistence durations. Relate uncertainty sensitivity to entity reconstruction-gradient share. Then test unfamiliar-state detection, prediction-error ranking, impossible-event detection, consistent distribution shifts, and uncertainty-penalized CEM planning. Swap uncertainty estimators and attach a Dreamer head before the recurrent stage as checks.

### 3. What is the method motivation?

The architecture/objective determine which distinctions survive. Recurrence can correctly smooth noisy isolated changes yet also hide a real discontinuity. Reconstruction can favor large visual regions rather than small task-critical objects. An uncertainty head cannot undo these choices by changing its output formula.

### 4. What data does it use?

The same recorded data per simulator for both model families: TwoRoom, PointMaze, Reacher, PushT, Cube, Ball-in-cup, Finger, Fetch push, Scene, and Cube double. Backbones are frozen single checkpoints per environment. Held-out windows/episodes support perturbation and downstream tests. Importantly, unfamiliar quadrants are removed from the uncertainty-head Gram-matrix fitting data, not from backbone training; this measures head support recognition rather than a clean backbone-unseen-state experiment.

### 5. How is it evaluated?

Normalized stage displacement and uncertainty sensitivity; body/object AUROC; Spearman correlation with each family's own prediction error; paired clean/violated windows; visual/physics shifts; CEM goal success. Laplace is compared with five bootstrap heads and a posterior-feature readout. Planning uses 200 episodes per seed across three seeds; backbone-training replication is absent. The reported penalty gain chooses the best λ in {0.1, 0.3, 1} versus zero on the same episodes, and goal costs differ by family.

### 6. What are the main results?

* At single-frame perturbations, Dreamer's posterior registers changes before the GRU but the recurrent representation transmits roughly one fifth of the relative displacement; longer persistence partly restores sensitivity. LeWM's predictor features retain much more of the perturbation.
* For Dreamer, object/body reconstruction-gradient ratios track uncertainty-sensitivity ratios across seven object environments (reported Spearman 0.93). This is a correlation, not a causal objective ablation.
* LeWM wins 13 of 17 body/object unfamiliar-quadrant AUROC cells and ranks its own next-step errors better in eight of ten environments. The errors are different quantities: embedding residual versus posterior/prior KL.
* Single-object violation and visual-shift tests favor LeWM; invisible contacts and multi-object settings weaken it. Physics-shift AUROC spans 0.48–0.99 with no consistent leader.
* Uncertainty-penalized planning improves LeWM in six of nine rare-region-start settings and five long-horizon settings; selected gains are 17–28 percentage points. Several environments gain nothing. These are best-of-three penalty results, not a universally beneficial fixed penalty.
* Moving Dreamer's readout to the pre-GRU posterior restores much violation/dynamics-shift detection. That is the key counterexample to blaming the uncertainty-head family alone.

### 7. What is actually novel?

A stage-wise physical-perturbation diagnosis connecting post-hoc uncertainty to representation loss, paired with persistence/entity-size analyses and downstream checks across these two paradigms. Last-layer Laplace, ensembles, JEPA, RSSM, and uncertainty-aware planning are not new components.

### 8. What are the strengths?

The same-state interventions locate failures rather than merely correlating final scores. Persistence tests, object/body decomposition, estimator replacement, and the posterior readout give complementary evidence. The paper includes exceptions and explicitly limits its paradigm claim to the instances tested. A simulator lets it distinguish physically altered observations from arbitrary image noise.

### 9. What are the weaknesses, limitations, or red flags?

One architecture instance per paradigm and one trained checkpoint per environment cannot support a universal ranking. Resolution differs 224x224 versus 64x64, alongside capacity/context/objective differences. Feature/episode bootstrap intervals do not replace backbone seeds. Single-frame teleports are artificial and smoothing them is not always undesirable. A larger response to background/color change is not automatically useful epistemic uncertainty. Reported reconstruction associations lack matched causal retraining. The unfamiliar-state protocol excludes head-fitting support, not backbone exposure. Family-specific error targets and planning costs complicate comparisons; choosing the best penalty on evaluated episodes can overstate deployable gains.

### 10. What challenges or open problems remain?

Which changes should uncertainty ignore as harmless and which must it retain? Can sensitivity be calibrated to actual task risk, not just deviation magnitude? Does the failure persist at equal resolution and with transformer RSSMs, object-centric reconstruction, different recurrence, or large pretrained JEPAs? Can long imagined trajectories remain reliable when one-step uncertainty seems sensible?

### 11. What future work naturally follows?

Retrain matched models after changing the recurrent gate, removing reconstruction, or balancing object-region losses. Match input resolution/context/capacity and repeat backbone seeds. Separate invariant nuisance shifts from decision-relevant shifts. Select uncertainty penalties on validation environments, report all weights, and evaluate failures over long-horizon closed-loop control. Test posterior/prior/hybrid readouts without simulator privilege at deployment.

### 12. Why does this matter for cabbageland?

It gives a practical world-model evaluation checklist: explicit state intervention, stage trace, alternate readout, independent downstream test. An inspectable uncertainty interface is only as good as the distinctions its representation keeps. This is a stronger design lesson than a broad JEPA-versus-reconstruction slogan.

### 13. What ideas are steal-worthy?

* Trace a controlled input change through every interface before redesigning the last module.
* Put uncertainty heads both before and after recurrence to expose filtering losses.
* Measure sensitivity separately for small critical objects and visually dominant context.
* Vary perturbation duration to distinguish temporal smoothing from information absence.
* Publish support-exclusion scope, readout location, penalty-selection protocol, and backbone-seed limitations alongside AUROC.

### 14. Final decision

Preserve as an evaluation and architecture-debugging reference. Try alternate readout placement before adding a more elaborate uncertainty estimator, but do not infer safety or world-model superiority from these results alone. [Primary PDF](https://arxiv.org/pdf/2611.34830).
