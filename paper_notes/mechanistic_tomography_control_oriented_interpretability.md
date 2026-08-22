# Mechanistic Tomography: Designed Measurement for Control-Oriented Interpretability

## Basic info

* Title: Mechanistic Tomography: Designed Measurement for Control-Oriented Interpretability
* Authors: Vijay Erramilli
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.19338
* Date surfaced: 2026-08-22
* Why selected in one sentence: It is the sharpest paper in the batch on turning interpretability from a bag of probes into a held-out measurement-design problem.

## Quick verdict

* Must read

I inspected the arXiv HTML full text, especially the framing, planted-map experiments, GPT-2 IOI study, and Qwen-2.5-7B refusal-surface evaluation. This paper earns a preserved note because it imposes a much better discipline on interpretability work: choose a measurement family, test it on held-out interventions at the scale where you plan to use it, and only escalate to richer interaction terms when the residual structure demands it. The paper is unusually strong at separating when extra mechanistic complexity is necessary from when it is just decorative overfitting.

## One-paragraph overview

The paper argues that many interpretability methods are doing versions of the same underlying job: trying to recover an unobserved internal effect map from designed interventions and measurements. It expresses this shared structure as a simple inverse-problem view, $\tilde{y} = Ax + w$, where the intervention design matrix determines what can be identified, the target map captures the mechanism you hope to recover, and the residual captures nonlinearity, sampling error, and basis mismatch. The useful contribution is not one new interpretability trick. It is a workflow for deciding which measurement family is warranted: start with the cheapest access mode that could plausibly recover the target, validate on held-out interventions, calibrate finite mismatches if that is enough, and only move to lifted interactions or Hessian-based terms when the held-out failures force you there.

## Model definition

### Inputs
Chosen intervention bases, model activations or response readouts, forward measurements, gradients, designed Hessian-vector products, held-out interventions, and response surfaces from synthetic control problems, Tracr programs, GPT-2-small IOI, and Qwen-2.5-7B.

### Outputs
Recovered effect maps, calibrated response maps, interaction maps, held-out intervention predictions, and control-facing diagnostics relating observer quality to downstream intervention quality.

### Training objective (loss)
There is no single new trainable model. Different recovery steps use sparse recovery or ridge-style fitting to estimate linear or lifted response maps from designed interventions, then evaluate them on held-out actions.

### Architecture / parameterization
Interpretability-as-measurement framework. The paper treats patching, attribution maps, lifted interaction features, and Hessian-vector products as different measurement families for recovering internal effect maps under different access assumptions.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the fact that interpretability methods often report recovered effects without a principled account of what quantity they are measuring, when a simpler measurement family is sufficient, or whether the estimate survives the interventions it is supposed to support.

### 2. What is the method?
The method is mechanistic tomography: formulate mechanistic recovery as a designed measurement problem, choose a basis and intervention family, fit an effect map from measurements, then validate or reject that map using held-out interventions at the intended operating scale.

### 3. What is the method motivation?
If an interpretability estimate will later guide control or intervention, then it functions as an observer. A bad observer can still produce flattering local stories while failing at the held-out actions where you actually want it to generalize.

### 4. What data does it use?
The paper uses several levels of testbed: a two-HMM belief-state control problem, planted finite-effect maps, Tracr programs with known structure, GPT-2-small on indirect-object identification, and Qwen-2.5-7B on a refusal-margin response surface built from HarmBench and XSTest prompts.

### 5. How is it evaluated?
Evaluation is done through held-out intervention prediction, control error, known-ground-truth recovery in planted or compiled settings, documented circuit behavior in GPT-2 IOI, and predictive adequacy on held-out Qwen intervention-response pairs.

### 6. What are the main results?
In the two-HMM control study, observer error and control error track tightly with Spearman 0.95. In the forward-only planted setting, 12 aggregate measurements recover a 32-coordinate finite-effect map with held-out Pearson r = 0.989 and held-out R² = 0.935, while ridge needs 32 measurements to match exhaustive coordinate count. In GPT-2-small IOI, the primary Name Mover–Negative Name Mover interaction is the largest held-out predictive cross-group term. On Qwen-2.5-7B, a 20-parameter calibrated additive map reaches held-out R² = 0.9829 and MAE 0.003790, while a 48-parameter lifted pairwise map gives no meaningful MAE improvement.

### 7. What is actually novel?
The novelty is the measurement-design lens itself and the corresponding decision procedure. The paper unifies several interpretability tools under one inverse-problem language and gives a practical rule for when to stop at calibration versus when to add richer interaction terms.

### 8. What are the strengths?
The paper is concrete, severe, and disciplined. It uses synthetic, semi-synthetic, and pretrained-model settings rather than staying in one comfort zone. It avoids the common interpretability sin of assuming that more elaborate explanations are automatically better.

### 9. What are the weaknesses, limitations, or red flags?
It is a framework paper more than a drop-in method, so some readers may want a more standardized recipe than it provides. Its conclusions depend on basis choice. The Qwen study validates finite behavioral response prediction, not true internal mechanism recovery. Some settings still rely on carefully chosen intervention families rather than arbitrary open-ended interventions.

### 10. What challenges or open problems remain?
The biggest open problem is scaling this discipline to larger, messier models where good intervention bases are unclear, sparse recovery assumptions break, and behavioral endpoints are only weakly tied to the latent mechanism one claims to measure.

### 11. What future work naturally follows?
Future work should apply the same workflow to tool-use agents, multimodal circuits, and long-horizon control policies, where held-out intervention validity matters more than local linear narratives. It would also be useful to automate basis proposal and residual-triggered escalation.

### 12. Why does this matter for cabbageland?
Because cabbageland wants mechanisms that survive contact with control, not flattering interpretability theater. This paper offers a very usable research taste: do the cheapest valid measurement first, test it honestly, and only buy more complexity when the residual makes that complexity necessary.

### 13. What ideas are steal-worthy?
Treat interpretability as observer design. Use held-out interventions as the gate for adding pairwise or higher-order structure. Distinguish local gradient stories from finite intervention behavior. Let calibration compete with interaction expansion instead of assuming both are always needed.

### 14. Final decision
Keep as a preserved note. The framing is sharp, the results are concrete, and the measurement-discipline is broadly reusable.

## 6. Mandatory critical angles

The paper is strongest on mechanism, controllability, evaluation fairness, and transferability of interpretability claims. It earns the control-oriented label because it keeps asking whether an estimate predicts held-out interventions at use scale. The main caution is basis dependence: a measurement family can look adequate or inadequate partly because the chosen coordinates were helpful or unhelpful.

## 7. Writing style

The right tone is enthusiastic but exact. The paper is conceptually ambitious, but it earns that ambition by repeatedly reducing the idea to held-out tests and concrete recovery numbers.

## 8. Repository output format

Saved as a preserved paper note because the measurement-design framing is strong enough to matter beyond this specific batch.
