# SafeImpute: Reliable Clinical Data Imputation via Conformal Selection

## Basic info

* Title: SafeImpute: Reliable Clinical Data Imputation via Conformal Selection
* Authors: Xinrui He, Mengting Ai, Junting Wang, Curtiss B. Cook, Jingrui He
* Year: 2026
* Venue / source: KDD 2026 author accepted manuscript / arXiv
* Link: https://arxiv.org/abs/2607.05613
* Date surfaced: 2026-07-08
* Why selected in one sentence: It treats clinical imputation as selective release under a stated error budget, not merely as an average-error prediction problem.

## Quick verdict

* Highly relevant

This is the strongest healthcare reliability paper I inspected today. I read the full PDF sections on the event-graph imputer, conformal selection, main results, ablations, FDR analysis, and conclusion. The caveats are real: the guarantee depends on exchangeability / dependence assumptions and on the proxy risk score being useful, but the deployment framing is exactly right.

## One-paragraph overview

SafeImpute tackles missing lab values in irregular, sparse clinical records, focusing on HbA1c imputation for diabetes-related settings. The model builds an event graph where nodes are patient visits, temporal edges connect consecutive visits for the same patient, and trend-aware value edges connect clinically similar events across patients. A two-relation GNN learns imputed values from these two edge types with adaptive fusion and auxiliary masked reconstruction. The key extra layer is not the imputer itself but the release rule: SafeImpute computes a label-free proxy risk score for each imputed value, converts it into conformal p-values, and applies Benjamini-Hochberg selection to control the false discovery rate of clinically unacceptable errors among released imputations.

## Model definition

### Inputs
Inputs are irregular longitudinal clinical event records. Each event node includes observed lab values, missingness indicators, basic patient attributes, timestamp information, temporal links to the same patient's neighboring visits, and trend-aware value links to similar events from other patients.

### Outputs
The model predicts imputed target lab values for missing entries, with the paper focusing on HbA1c. The selection module also outputs a deployed subset of imputations whose unacceptable-error false discovery rate is controlled at a user-specified level.

### Training objective (loss)
The imputer minimizes a target prediction loss, described as squared error over observed target labels, plus an auxiliary masked reconstruction loss over non-target labs using a Huber loss. The final objective is `Ltarget + lambda * Laux`. The conformal/BH release layer is a post-training selection procedure, not a gradient-trained loss.

### Architecture / parameterization
The learned imputer is a two-relation graph neural network. It applies separate GCN-style message passing over temporal edges and trend-aware value edges, then fuses relation-specific messages with a learned node-level gate. A multi-output linear head predicts laboratory variables. The risk-selection layer uses perturbation-induced prediction instability and an evidence-support penalty to form a proxy risk score, then performs conformal selection with Benjamini-Hochberg FDR control.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Clinical labs are often missing because tests are ordered irregularly. Standard imputation methods can reduce average error but do not tell clinicians which individual imputed values are reliable enough to use. SafeImpute asks for accurate imputation plus statistical control over the error rate among released values.

### 2. What is the method?
SafeImpute constructs an event graph from patient visits, learns missing lab values with a two-relation GNN, then selectively releases imputations. At release time, it estimates a proxy risk score from graph-perturbation instability and relational evidence scarcity, computes conformal p-values against calibration data, and uses BH to select values while controlling FDR.

### 3. What is the method motivation?
In clinical settings, an unreliable imputed value can mislead diagnosis or treatment. A useful system should sometimes withhold an estimate. The FDR framing is good because a hospital often releases many imputations, so the error burden among accepted values matters more than a single confidence score.

### 4. What data does it use?
The paper evaluates HbA1c imputation on a Mayo Clinic dataset and public MIMIC-III / MIMIC-IV datasets. The Mayo data covers diabetes-related clinical visits, while the MIMIC datasets provide ICU electronic health record benchmarks.

### 5. How is it evaluated?
It reports standard imputation accuracy metrics such as MAE and RMSE, plus precision / FDR-controlled selective-release metrics. It compares against statistical, deep learning, and sequential baselines; studies the pure event-graph imputer without selection; ablates temporal edges, value edges, adaptive fusion, auxiliary reconstruction, and proxy-risk components; and examines FDR-power tradeoffs.

### 6. What are the main results?
In the main table, SafeImpute reports MAE / RMSE / precision of 0.2464 / 0.3125 / 1.0000 on Mayo Clinic, 0.9662 / 1.2351 / 0.6333 on MIMIC-III, and 0.9715 / 1.3820 / 0.6555 on MIMIC-IV. It is best or near-best across these settings while adding selective-release control. The proxy-risk ablation is important: prediction instability alone causes much higher empirical FDR than the combined proxy score, including a Mayo increase from 0.0000 to 0.3575 in the reported ablation.

### 7. What is actually novel?
The novelty is the coupling of an irregular clinical event-graph imputer with conformal selective release. The two-relation graph model is useful, but the real contribution is treating imputation reliability as a deployment-level selection problem with an explicit tolerated error rate.

### 8. What are the strengths?
The paper evaluates on both private and public clinical data, includes diverse baselines, and makes the reliability layer explicit. The event graph also matches the clinical structure: within-patient temporal continuity and cross-patient analogy are different information sources and should not be forced through one relation.

### 9. What are the weaknesses, limitations, or red flags?
The FDR control relies on exchangeability / dependence assumptions and on the proxy score ranking risky imputations well enough. The primary task is HbA1c imputation, so the clinical breadth is still limited. Selective release necessarily trades coverage for reliability, and the right alpha / tolerance choice is a clinical governance decision, not just a modeling choice.

### 10. What challenges or open problems remain?
The obvious challenge is validating the selection rule prospectively under site shift, changing test-ordering policies, and different clinical variables. Another challenge is making the withheld-value behavior understandable enough for clinicians to trust the system without treating the proxy score as a calibrated probability.

### 11. What future work naturally follows?
Extend the framework to multiple target labs, multi-site prospective validation, clinical utility studies, subgroup reliability audits, and release policies that incorporate downstream decision cost rather than a fixed unacceptable-error threshold.

### 12. Why does this matter for cabbageland?
Cabbageland cares about uncertainty, calibration, and systems that know when not to act. SafeImpute is a concrete pattern: prediction is only half the artifact; the controlled release rule is the deployable interface.

### 13. What ideas are steal-worthy?
Separate predictive accuracy from release eligibility. Use perturbation instability plus evidence scarcity as a proxy risk signal. Calibrate a batch of decisions with FDR control when many outputs will be consumed downstream. Model temporal and similarity relations separately before fusion.

### 14. Final decision
Keep as a highly relevant healthcare reliability note. The mechanism is not magic, and the assumptions need respect, but the release-policy framing is the right shape for high-stakes ML.
