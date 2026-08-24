# The Exceedance Design Effect: Effective Sample Size for Thresholds under Clustering

## Basic info

* Title: The Exceedance Design Effect: Effective Sample Size for Thresholds under Clustering
* Authors: Adam Noonan
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.21262
* Date surfaced: 2026-08-24
* Why selected in one sentence: It is the sharpest paper in the batch on why threshold guarantees under clustered calibration data need a different effective sample size than averages do.

## Quick verdict

* Must read

I inspected the arXiv HTML full text, especially the setup, the coverage-law derivation, the critique of the naive design effect, the level-dependence section, and the measured calibration example. This paper earns a preserved note because it identifies the exact dependence object threshold guarantees care about and shows how badly row counts can lie under clustering. The key cut is simple and brutal: thresholds care about exceedance correlation at the operating level, not ordinary score correlation.

## One-paragraph overview

The paper studies thresholds set from sample quantiles under clustered calibration data, with conformal prediction, abstention, and safety filters as the motivating cases. Its core claim is that the classical design effect for averages is the wrong correction for order-statistic thresholds. The relevant quantity is the intra-cluster correlation of exceedance indicators at the operating level, which depends on where the threshold is set and can be very different from correlation in the raw scores themselves. The paper derives a closed-form coverage law, shows that effective sample size is level-dependent rather than global, and measures the effect on released calibration sets. On a released 25,028-row calibration set, the tie-broken realised dispersion behaves like about 1,300 effective points rather than 25,028.

## Model definition

### Inputs
Clustered calibration scores, a target quantile or coverage level, and an independent test score.

### Outputs
The calibration-conditional coverage law, the exceedance-based design effect, and the corresponding threshold-specific effective sample size.

### Training objective (loss)
There is no trainable model. This is a statistical analysis of threshold guarantees under clustered sampling.

### Architecture / parameterization
Closed-form threshold-dispersion framework built around the order statistic used as a threshold and the intra-cluster correlation of exceedance indicators at the operating level.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the fact that many thresholded guarantees assume i.i.d. calibration points even though calibration data often arrives in clusters such as shared prompts, documents, or reasoning traces.

### 2. What is the method?
The method is to derive the coverage law for thresholds under clustered calibration and express the corresponding effective sample size through exceedance correlation at the operating threshold.

### 3. What is the method motivation?
An average and a threshold are different objects. Thresholds only care whether points fall on the same side of the line, so raw score similarity is not the right dependence statistic.

### 4. What data does it use?
The paper uses analytical derivations plus measured examples including SQuAD 2.0 and a released MATH-500 / Llama-3.2-1B process-reward calibration set with 25,028 rows over 500 question families.

### 5. How is it evaluated?
Through theorem derivation, plug-in estimation, and cluster-resampling measurements of realised calibration dispersion against i.i.d. controls.

### 6. What are the main results?
The sharpest measured example is that a released 25,028-row calibration set behaves like roughly 1,300 effective points after tie-breaking, with a measured dispersion ratio of 4.46x. In a separate example, same-paragraph score correlation is effectively zero at -0.0026, while exceedance correlation at the operating level is +0.0640, producing a design effect of 1.60. The paper also shows that effective sample size is level-dependent, so a dataset has no single universally correct threshold correction.

### 7. What is actually novel?
The real novelty is not "clustering matters." Everyone already knows that. The novelty is that thresholds need their own design effect, based on exceedance correlation at the deployment level rather than raw-score correlation or average-style effective sample size.

### 8. What are the strengths?
The paper is severe, operational, and mathematically clean. It gives a closed-form law, shows exactly where common practice goes wrong, and backs the theory with measured calibration examples instead of only asymptotic talk.

### 9. What are the weaknesses, limitations, or red flags?
The cleanest theorem relies on continuous score assumptions, so atomic or tied scores complicate the practice. The current measured examples are persuasive but still concentrated in a small set of calibration settings.

### 10. What challenges or open problems remain?
Handling discrete scores, informative family sizes, stronger selection channels, and deployment settings where the clustering structure itself shifts between calibration and use.

### 11. What future work naturally follows?
Build threshold-specific effective sample-size reporting into conformal evaluation, abstention systems, safety filters, and agent harnesses that repeatedly reuse shared prompts or documents.

### 12. Why does this matter for cabbageland?
Because cabbageland cares about calibrated thresholds, abstention, risk controls, and honest evaluation under clustered traces. This paper says that if the data clusters, row count is theater unless you measured the threshold-side dependence that the deployed decision actually uses.

### 13. What ideas are steal-worthy?
Measure exceedance ICC at the operating level, not only raw-score correlation. Report threshold-specific effective sample size rather than one global n_eff. Resample by cluster families, not by rows, when checking realised coverage dispersion.

### 14. Final decision
Keep as a preserved note. This is the kind of paper that can immediately improve how calibration claims are audited.

## 6. Mandatory critical angles

The paper is strongest on evaluation fairness, uncertainty quantification, and decision-making under dependence. It earns the calibration label because it identifies the correct dependence object for thresholded guarantees. The main caution is that discrete scores still need careful handling.

## 7. Writing style

The right tone is grateful and unsentimental. The paper is good because it says the existing correction is the wrong quantity and then proves a better one.

## 8. Repository output format

Saved as a preserved paper note because the threshold-specific effective-sample-size idea is directly reusable in future evaluation and deployment work.
