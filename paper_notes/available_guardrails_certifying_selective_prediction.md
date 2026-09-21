# Available Guardrails: Certifying Selective Prediction across ML Systems

## Basic info

* Title: Available Guardrails: Certifying Selective Prediction across ML Systems
* Authors: Parivesh Priye, Yufeng Wang, Haibin Ling, Michael Chaykowsky
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2609.22048
* Date surfaced: 2026-09-21
* Why selected in one sentence: It separates whether a selective-prediction certificate is valid from whether finite calibration data can make it available at the desired granularity.

## Quick verdict

* Highly relevant

This is a strong uncertainty and deployment paper. Its main value is conceptual and operational: availability is a finite-data resource, not a footnote to validity. The planner results are mixed, but the framing is worth keeping.

## One-paragraph overview

The paper studies selective predictors that act only when a prediction is trustworthy enough, such as tool-call gates, moderation filters, clinical classifiers, or recommenders. It argues that deployments often need certified reliability for multiple reporting units, and finite calibration data may be too thin to certify useful coverage at that granularity. Using exact binomial inversion, the paper computes the probability that a unit can be certified, then optimizes reporting partitions to maximize certified traffic. It finds a real safety-granularity-coverage frontier across synthetic studies, intent routing, tool calling, content moderation, lesion classification, and recommendation, while showing that no single planner dominates all regimes.

## Model definition

This paper mostly defines a certification and planning framework around existing predictors.

### Inputs

Inputs are prediction scores, correctness labels on calibration data, reporting group labels or candidate partitions, safety targets, familywise error budgets, and desired reporting granularity.

### Outputs

The framework outputs selective thresholds, certified reporting units, expected certified coverage, and availability-aware partition choices.

### Training objective (loss)

There is no new learned model loss. The core objective maximizes traffic-weighted expected certified coverage, using exact binomial availability for candidate reporting units.

### Architecture / parameterization

The method uses frozen predictors and score functions. Planning is done with exact-binomial calculations, held-out partition selection, dynamic programming over contiguous group cuts, and optional familywise error-budget reallocation.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It asks when finite calibration data can certify a selective predictor at a target safety level and reporting granularity, not merely whether the certificate would be valid if it passed.

### 2. What is the method?

The method uses Clopper-Pearson exact binomial inversion to compute certificate availability, then plans reporting partitions and thresholds to maximize expected certified traffic.

### 3. What is the method motivation?

A gate may be safe on average but uncertifiable for small subgroups, tools, labels, or patient categories. Finer reporting creates support starvation.

### 4. What data does it use?

The paper uses synthetic settings, intent classification datasets, and four application gates: BFCL tool calling with Qwen2.5-14B, Civil Comments moderation, DermaMNIST lesion classification, and MovieLens recommendation.

### 5. How is it evaluated?

It compares expected and realized certified coverage under different partition planners, reporting granularities, score qualities, target precision levels, and distribution shifts.

### 6. What are the main results?

The arithmetic is verified across 432 binomial cells with mean absolute error 0.00067 between predicted and simulated certification frequency. At target precision 0.90, true error 0.05, and 80% availability, one group needs 179 served calibration examples; fifty groups need 450 each. At true error 0.09 with fifty groups, the requirement jumps to 13,407. Held-out selection improves coverage over support balancing by 0.0601 on average in synthetic configurations, but much of the practical gain comes from independent selection and error-budget allocation rather than structured partition search.

### 7. What is actually novel?

The novelty is treating certificate availability as a design objective distinct from validity. That distinction clarifies why a formally valid guardrail can still be practically unavailable.

### 8. What are the strengths?

The paper is honest about limitations. It shows the frontier across many domains and repeatedly notes that planner dominance depends on comparator and regime.

### 9. What are the weaknesses, limitations, or red flags?

The dynamic program optimizes an approximate objective over a restricted partition family. Semantic constraints can reduce coverage sharply, and the planner can lose to strong random-order controls.

### 10. What challenges or open problems remain?

The hard problem is planning under semantic, legal, fairness, or operational constraints where arbitrary group merges are not acceptable. Distribution shift also breaks the IID certification assumption.

### 11. What future work naturally follows?

Availability-aware certification should be combined with explicit admissible hierarchies and shift diagnostics, so coverage gains do not come from operationally meaningless group merges.

### 12. Why does this matter for cabbageland?

Any autonomous tool system will need abstention and delegation gates. This paper explains why "we certified the gate" is incomplete unless the finite-data availability and reporting units are specified.

### 13. What ideas are steal-worthy?

Use availability as a planning resource. Also steal the habit of separating validity, coverage, granularity, and semantic acceptability instead of treating them as one safety number.

### 14. Final decision

Preserve. It is a clean deployment-statistics paper with useful language for future agent and tool-use systems.
