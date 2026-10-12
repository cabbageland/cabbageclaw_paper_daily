# Prediction Is Not a Sufficient Memory State

## Basic info

* Title: Prediction Is Not a Sufficient Memory State
* Authors: Robert Jenkinson Alvarez
* Year: 2026
* Venue / source: arXiv preprint
* Link: https://arxiv.org/abs/2610.13881
* Date surfaced: 2026-10-12
* Why selected in one sentence: It proves that a learner can preserve every current prediction while losing evidence required for future updates.

## Quick verdict

* Highly relevant

This is a clean theory paper with direct implications for memory and continual learning. It makes precise why "the current predictor" is not the same object as "a state that can continue learning." The caveat is that it is mathematical characterization, not a new practical memory architecture.

## One-paragraph overview

The paper studies what an exact cumulative learner must remember if it is supposed to keep learning after new observations arrive. Its central point is that histories with identical current predictions can require different future updates. In ridge regression, zero-label histories can all predict zero while still hiding different design matrices; when a nonzero label arrives, those hidden matrices change the update. The paper generalizes this distinction: fixed-dimensional exact recurrent state exists for smooth convex residual losses exactly when the loss is polynomial, while nonpolynomial losses can need unbounded evidence even after fixing the current predictor. It also analyzes attention, where unnormalized kernel evidence and normalization mass play the same role.

## Model definition

### Inputs

The paper considers cumulative histories of feature-label observations for regression and histories of keys/values for attention. New observations or queries arrive after the current state has been compressed.

### Outputs

The computations output current predictions and future updated predictors or attention responses after continuation observations are appended.

### Training objective (loss)

There is no learned neural training objective in the usual experimental sense. The paper analyzes exact cumulative learning under smooth convex residual losses, ridge regression objectives, and kernel attention closure conditions.

### Architecture / parameterization

The objects are mathematical recurrent states for exact learners. For ridge regression, the exact state includes predictor parameters plus the design matrix information. For polynomial residual losses, the state is a finite set of additive moments. For attention, the exact state depends on kernel feature structure and unnormalized evidence.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It asks what information a memory state must preserve so that a learner can continue updating correctly, rather than merely reproduce its current predictions.

### 2. What is the method?

The paper proves closure and lower-bound results for exact recurrent states under residual-loss learning and attention. It constructs equal-prediction histories that become distinguishable only after future observations.

### 3. What is the method motivation?

Current-output compression can look perfect until the next observation arrives. A memory for continual learning must preserve evidence that changes future response, even when that evidence has no effect on the present readout.

### 4. What data does it use?

It uses mathematical constructions rather than empirical datasets.

### 5. How is it evaluated?

The paper is evaluated by theorems: exact state dimension, hidden evidence dimension, closure classifications, and finite-bit lower bounds for future-update error.

### 6. What are the main results?

For degree-D polynomial residual losses in d dimensions, exact unweighted state requires r = binomial(d + D, D) - 1 coordinates, and r - d coordinates can remain hidden even among histories with the same current predictor. For nonpolynomial smooth convex residual losses, fixed-dimensional exact closure fails. In ridge regression with p outputs, the predictor costs dp coordinates, but the exact state costs dp + d(d+1)/2 because the design matrix matters. The finite-bit compression result gives average one-update error scaling with the hidden design-matrix dimension.

### 7. What is actually novel?

The paper separates prediction-equivalence from continuation-equivalence and quantifies the evidence hidden at fixed predictions.

### 8. What are the strengths?

The examples are simple but sharp. The ridge regression case makes the point impossible to hand-wave away, and the attention analysis connects the result to modern sequence models.

### 9. What are the weaknesses, limitations, or red flags?

The results are exact and assumption-specific. Approximate learners, finite vocabularies, task-average error, and bounded domains may change the practical scale. The paper does not provide a tested neural memory mechanism.

### 10. What challenges or open problems remain?

The open engineering question is how to preserve continuation-identifiable evidence approximately, under finite compute, without storing everything.

### 11. What future work naturally follows?

Design memory audits that test whether a model's compressed state supports future updates, not only current predictions. Apply the same distinction to learned optimizers, recurrent agents, and world-model state.

### 12. Why does this matter for cabbageland?

Cabbageland's memory and world-state questions often collapse "what the model currently says" into "what the model knows." This paper gives the formal counterexample.

### 13. What ideas are steal-worthy?

Use continuation tests, not only reconstruction tests. Preserve update-critical evidence. Treat zero current prediction as a dangerous case, because hidden structure can still determine future learning.

### 14. Final decision

Preserve. It is theory, but the conceptual lesson is durable.
