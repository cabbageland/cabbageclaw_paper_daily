# Optimal Sequential Annotations for Off-Policy Evaluation

## Basic info

* Title: Optimal Sequential Annotations for Off-Policy Evaluation
* Authors: Woojin Chae, Ezinne Nwankwo, Haitong Qin, Angela Zhou
* Year: 2026
* Venue / source: arXiv:2609.26707
* Link: https://arxiv.org/abs/2609.26707
* Date surfaced: 2026-09-23
* Why selected in one sentence: It treats expert annotation as part of the off-policy estimator and optimizes label allocation for value-estimation variance rather than generic prediction accuracy.

## Quick verdict

Highly relevant. This is a sober RL/evaluation paper with a useful statistical mechanism for settings where rewards or states live inside text, images, or judge labels. Full arXiv text was inspected.

## One-paragraph overview

Offline RL and off-policy evaluation increasingly rely on messy observations: case notes, clinical text, screenshots, preference logs, or LLM-judge labels. Cheap labels may be biased, while expert annotation is expensive. This paper formulates the problem as doubly robust off-policy evaluation with missing rewards or reward-derived states. It then chooses forward-monotone sequential annotation probabilities to minimize the variance of the policy-value estimator under a budget. The practical result is a batch-adaptive annotation scheme that can stop after early-stage annotation for some trajectories and spend more label budget where it most improves the target value estimate.

## Model definition

### Inputs

Inputs are offline trajectories, behavior and evaluation policies, observed rich measurements or silver labels, optional current states, and sequential annotation decisions that reveal rewards and sometimes next-state components.

### Outputs

The method outputs a doubly robust estimate of a target policy value and an annotation design: stagewise probabilities for which trajectory prefixes should receive gold annotation under a budget.

### Training objective (loss)

There is no learned policy objective. The design objective minimizes the asymptotic variance of the doubly robust off-policy value estimator under annotation budget and forward-monotonicity constraints. Nuisance functions are estimated from observed and annotated data.

### Architecture / parameterization

This is a statistical estimation framework, not a neural architecture. The feasible implementation uses batch-adaptive, cross-fitted nuisance estimation and realized annotation probabilities.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It addresses how to do trustworthy off-policy evaluation when the reward or relevant state is only available through costly expert annotation, while cheap automatic labels are available but imperfect.

### 2. What is the method?

The method projects the full-data off-policy score onto annotation filtrations, derives variance contributions for sequential annotation stages, and allocates annotation probability in proportion to the conditional standard deviation of each stage's contribution under the budget.

### 3. What is the method motivation?

The motivation is that active learning for prediction is the wrong target. If the goal is a policy-value functional, annotation should reduce that estimator's variance, even if that differs from labeling examples that are hard to predict.

### 4. What data does it use?

The paper uses simulations, social-services casenotes from a homelessness-services collaboration, and LMArena human-preference vote logs.

### 5. How is it evaluated?

It compares adaptive annotation to random annotation at matched label budgets, measuring RMSE against full-annotation or simulator truth, interval width, and policy-value estimation quality.

### 6. What are the main results?

On casenote data, adaptive annotation reduces DRL RMSE by about 23% at 30-40% budgets and 34-65% at budgets of 50% and above for housing placement. For progress rewards, it reduces DRL RMSE by 17-32% at 40-60% budgets and 45-68% at 70-80%. In simulator-grounded validation, adaptive annotation reduces RMSE to truth by 12-38% for placement and 33-51% for progress. On LMArena, adaptive annotation reduces RMSE by 55-62% at every budget.

### 7. What is actually novel?

The novelty is the sequential annotation design for off-policy evaluation: label allocation is optimized for the doubly robust value estimator and respects prefix-style annotation constraints.

### 8. What are the strengths?

The paper connects theory to real messy data instead of stopping at an oracle design. The LMArena example also makes it directly relevant to AI evaluation and post-training pipelines.

### 9. What are the weaknesses, limitations, or red flags?

The guarantees rely on annotation ignorability, overlap, nuisance quality, and correctly recorded annotation probabilities. The casenote ground truth is partly unknown, so some real-data results are relative to full-annotation or fitted simulators rather than an external truth.

### 10. What challenges or open problems remain?

A major challenge is robust nuisance estimation when silver labels are biased in structured ways. Another is extending the design to richer annotation actions where experts can annotate different fields, not just prefixes.

### 11. What future work naturally follows?

Future work should connect this to LLM-as-judge auditing, reward-model validation, selective expert review, and offline policy evaluation for deployed agents where logs contain unstructured evidence.

### 12. Why does this matter for cabbageland?

Cabbageland cares about trustworthy evaluation under uncertainty. This paper gives a concrete way to spend scarce human review where it improves the decision estimate rather than the scoreboard.

### 13. What ideas are steal-worthy?

Steal the principle "optimize annotation for the estimand." For agent evaluations, that means review examples that reduce uncertainty in the policy or product decision, not merely examples that a classifier finds confusing.

### 14. Final decision

Preserve. This is useful for offline RL, evaluation, and human-in-the-loop measurement.
