# Interpretable AI with Local Distillation

## Basic info

* Title: Interpretable AI with Local Distillation
* Authors: Erin Craig, Yiling Huang, Snigdha Panigrahi
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.23538
* Date surfaced: 2026-08-25
* Why selected in one sentence: It is one of the better explicit-structure papers in the batch because it turns a black-box teacher into a locally interpretable model rather than another attribution wrapper.

## Quick verdict

* Highly relevant

I inspected the full arXiv HTML text, especially the introduction, the local-distillation setup, the randomized-stability sections, the BRCA1 example, and the benchmark comparison section. This paper earns a preserved note because it is trying to make the interpretable object be the predictor itself. That is much more interesting than adding explanations after the fact.

## One-paragraph overview

The paper proposes local distillation, a framework in which a black-box teacher guides a sparse local linear student at each query point. The teacher does two things: it defines locality by upweighting training examples with similar predicted outcomes, and it anchors the student with the teacher's prediction at the query point as a pseudo-observation whose weight is estimated from the data. To turn these local fits into something trustworthy, the method adds small Gaussian randomization to the local objective and repeatedly refits, using selection frequencies and clustering over randomized fits to identify stable local features and stable subgroups. Across 17 tabular regression datasets, the local students usually approach teacher-level predictive performance while staying sparse, and the gene-expression example shows the payoff: subgroup-specific signals appear in local models that a global lasso washes out.

## Model definition

### Inputs
A query point, a training set of tabular features and responses, teacher predictions on the query and training data, and a chosen student regularizer such as lasso or ridge.

### Outputs
A sparse local linear model for the query point, including prediction, coefficients, feature-selection frequencies under randomized refits, and cluster structure across local models.

### Training objective (loss)
Weighted local linear regression with regularization, where weights are determined by similarity in the teacher's predicted response. The teacher prediction at the query point is inserted as a pseudo-observation, and its weight is estimated from the data through the student-to-teacher loss ratio. The interpretability layer adds small Gaussian randomization to the local objective and studies the distribution of refit solutions.

### Architecture / parameterization
Teacher can be a tabular foundation model or another black-box predictor such as TabPFN, TabFM, or XGBoost. Student is a local linear model with lasso or ridge regularization, fit separately at each query point.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the gap between highly predictive but opaque tabular models and classical interpretable models that are easy to reason about but often too weak.

### 2. What is the method?
Fit a local sparse linear model around each query point, but define locality in teacher-prediction space and anchor the local fit to the teacher's output. Then use randomized refits to measure which coefficients are stable and which subgroups of local models recur.

### 3. What is the method motivation?
If a strong teacher already captures complex nonlinear structure, a local linear student should not need to rediscover the whole function. It only needs to explain the teacher's behavior in the relevant neighborhood. Using teacher-prediction similarity collapses the localization problem onto a supervised axis rather than an arbitrary distance in raw feature space.

### 4. What data does it use?
Seventeen regression datasets from the UCI Machine Learning Repository and the OpenML-CTR23 benchmark, spanning sample sizes from 159 to 4177 and feature counts from 5 to 51. It also includes a high-dimensional BRCA1 gene-expression example with 215 test patients shown in the cluster figure.

### 5. How is it evaluated?
By comparing predictive performance against global linear students, teacher models, and other local methods such as LOESS and local linear forests, and by examining whether randomized local models surface stable single-point and subgroup-level feature structure.

### 6. What are the main results?
On the Auto MPG example, local distillation improves the global lasso's prediction squared error by 48%, moving from 10.81 to 5.59 and nearly matching the TabPFN teacher at 5.25. Across 17 regression datasets, the paper reports that local distillation usually approaches teacher-level test R^2 when the teacher clearly outperforms a global linear model. In the BRCA1 example, stable local models keep a median of 15 genes with selection frequency above 0.9 across 100 randomized refits, and the resulting clusters surface subgroup-specific genes such as FAM107A and KLF14 that receive zero weight in the global lasso.

### 7. What is actually novel?
The novelty is not just "train a local surrogate." It is teacher-defined locality, the pseudo-observation anchor at the query point, and the move from one brittle local fit to a randomized stability object that supports both feature reliability and subgroup discovery.

### 8. What are the strengths?
The paper keeps the interpretable object explicit and sparse. It also does not pretend that a single fit is self-justifying; the stability analysis is a real step beyond ordinary local surrogate methods. The examples are concrete and better than the usual toy explanations.

### 9. What are the weaknesses, limitations, or red flags?
The method depends on the teacher being genuinely better than the student. If the teacher is weak or weird, the locality notion inherits that weakness. The paper is also mostly about tabular regression, so one should not assume the same setup transfers cleanly to sequence models or multimodal systems. Per-query fitting plus randomized refits is also more computationally expensive than a single global model.

### 10. What challenges or open problems remain?
Extending the framework to classification, structured outputs, sequential data, and higher-dimensional input spaces where a one-dimensional teacher-prediction axis may not capture all relevant local geometry.

### 11. What future work naturally follows?
Teacher-guided local models for multimodal predictors, local controllers or planners extracted from stronger black-box policies, and stability-aware local distillation methods that operate on temporal or relational data rather than only tabular responses.

### 12. Why does this matter for cabbageland?
Because cabbageland prefers explicit structure that still does real predictive work. This paper is a good example of using a strong black box to define a legible local object rather than settling for attribution noise.

### 13. What ideas are steal-worthy?
Define local neighborhoods in model-output space, not only raw feature space. Use pseudo-observation anchoring to keep local fits tied to a strong teacher. Treat explanation stability as a first-class object and cluster local models to expose subgroup structure.

### 14. Final decision
Keep as a preserved note. It is an adjacent paper, but it has the right taste: interpretable mechanism first, then performance.

## 6. Mandatory critical angles

The paper is strongest on explicit representation, interpretability, and local controllability of reasoning. It is less about raw scale and more about preserving useful heterogeneity. The main red flag is domain scope: the method is persuasive for tabular regression, not yet for broader model classes.

## 7. Writing style

The tone should be pleased and slightly relieved. This is one of the few interpretability papers in the batch that does not feel like decorative attribution.

## 8. Repository output format

Saved as a preserved paper note because the teacher-defined local-model pattern feels reusable well beyond the tabular benchmarks in the paper.
