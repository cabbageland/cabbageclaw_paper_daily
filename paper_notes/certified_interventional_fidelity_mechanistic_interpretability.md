# Certified Interventional Fidelity: Anytime-Valid, Adaptive Evaluation of Causal Claims in Mechanistic Interpretability

## Basic info

* Title: Certified Interventional Fidelity: Anytime-Valid, Adaptive Evaluation of Causal Claims in Mechanistic Interpretability
* Authors: Amir Asiaee
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.08349
* Date surfaced: 2026-07-12
* Why selected in one sentence: It turns activation-patching style claims into explicit causal estimands with confidence intervals and anytime-valid confidence sequences.

## Quick verdict

**Highly relevant**

This is a strong evaluation paper because it improves the reporting contract around mechanistic-interpretability experiments without pretending that a new visualization alone solves validity. The paper formalizes intervention scores as bounded causal estimands, then gives finite-sample and anytime-valid uncertainty tools for them. I inspected the full arXiv HTML paper, including the estimand setup, confidence-sequence machinery, adaptive intervention sampling, experiments, and conclusion.

## One-paragraph overview

Mechanistic interpretability often reports intervention results such as activation patching, ablation recovery, or component-effect scores as single point estimates. That is fragile when researchers monitor experiments while they run, stop early, or adapt which interventions to test based on what looks promising. CIF wraps these evaluations in a statistical layer. It first writes the quantity of interest as an expectation over a declared input distribution and intervention distribution. It then provides fixed-budget confidence intervals and anytime-valid confidence sequences, including under adaptive intervention sampling via bounded mixture importance weighting. On MNIST abstractions and GPT-2 Small IOI circuits, the framework certifies some claims cleanly, shows when apparent method differences are not actually supported, and makes intervention-distribution sensitivity explicit.

## Model definition

### Inputs
The framework takes a chosen interpretability metric, a declared distribution over inputs, and a declared distribution over interventions such as swaps, ablations, or patching operations.

### Outputs
It outputs certified estimates: confidence intervals, confidence sequences, and sensitivity-aware claims about intervention fidelity or effect size.

### Training objective (loss)
CIF is not a training method. It is a statistical wrapper around intervention evaluations.

### Architecture / parameterization
The framework expresses the target metric as a bounded causal estimand, then builds fixed-budget confidence intervals, anytime-valid confidence sequences, and bounded-importance-weight corrections for adaptive intervention policies. It also uses variance-adaptive betting sequences to reduce certification cost.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to solve the statistical weakness of common mechanistic-interpretability reporting. If a paper keeps checking patching scores while deciding whether to continue or redirect an experiment, a plain point estimate can overstate confidence badly.

### 2. What is the method?
The method is to rewrite intervention metrics as explicit causal estimands and then attach uncertainty guarantees that remain valid under repeated monitoring and adaptive intervention choice.

### 3. What is the method motivation?
Interpretability work often wants to make causal claims about components, circuits, or interventions, but the evaluation layer is weaker than the causal language suggests. CIF tries to make the uncertainty accounting match the claim strength.

### 4. What data does it use?
The paper demonstrates CIF on MNIST abstraction settings and GPT-2 Small IOI circuit evaluations.

### 5. How is it evaluated?
The paper evaluates whether CIF can certify high-fidelity claims, whether it can reject unsupported apparent differences, and how certification cost changes between conservative Hoeffding-style bounds and variance-adaptive betting sequences.

### 6. What are the main results?
The main result is practical rather than leaderboard-style. CIF can certify some intervention claims with valid uncertainty, identify when apparent differences do not survive uncertainty accounting, and reduce certification cost by roughly 10-30x when using variance-adaptive betting sequences instead of more conservative confidence-sequence constructions.

### 7. What is actually novel?
The novel part is not a new interpretability metric but the statistical layer: explicit causal estimands, anytime-valid confidence sequences, and adaptive-intervention support for common mechanistic-interpretability workflows.

### 8. What are the strengths?
The paper's biggest strength is that it addresses a real workflow problem. Researchers do monitor runs, adapt interventions, and stop when a result looks clear. CIF acknowledges that reality instead of assuming a fixed precommitted sampling plan that almost nobody actually follows.

### 9. What are the weaknesses, limitations, or red flags?
CIF certifies the stated estimand, not the truth of the explanatory story around it. If the chosen intervention distribution is unhelpful or the metric is conceptually weak, the paper's machinery can still produce a precise answer to the wrong question. The experiments are also on manageable benchmark settings rather than frontier-scale models.

### 10. What challenges or open problems remain?
The hard open problem is deciding which intervention distributions and metrics genuinely correspond to the explanatory claims people care about. Statistical validity is necessary here, but it is not sufficient.

### 11. What future work naturally follows?
Useful follow-up work would apply CIF to larger language and multimodal models, develop better default intervention distributions for common interpretability tasks, and connect certification to automatic experiment allocation.

### 12. Why does this matter for cabbageland?
Cabbageland cares about explicit mechanisms and skeptical evaluation. CIF offers a concrete way to stop overclaiming from intervention experiments and to report uncertainty that survives repeated probing.

### 13. What ideas are steal-worthy?
Write evaluation targets as estimands. Report confidence sequences, not just final point estimates. Treat adaptive probing as normal workflow and support it explicitly. Make intervention-distribution sensitivity part of the result, not an afterthought.

### 14. Final decision
**Keep it.** This is worth preserving because it upgrades the rigor of mechanistic-interpretability evaluation without requiring a whole new interpretability stack.
