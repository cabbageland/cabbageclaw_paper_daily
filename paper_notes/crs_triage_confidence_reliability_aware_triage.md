# CRS-Triage: Confidence- and Reliability-Aware Selective Triage under Incomplete Clinical Evidence

## Basic info

* Title: CRS-Triage: Confidence- and Reliability-Aware Selective Triage under Incomplete Clinical Evidence
* Authors: Guan Qiang, Yushen Chen, Tianlong Liu, David Rotenberg, Ethan H. Kim, Fang Fang
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.03862
* Date surfaced: 2026-08-06
* Why selected in one sentence: It is a good adjacent paper because it treats deferral as a structured risk problem under missing and conflicting multimodal evidence instead of as a generic confidence threshold.

## Quick verdict

**Useful**

I inspected the arXiv HTML paper, especially the modality-specific encoding, reliability-aware evidential fusion, training objective, selective-prediction tables, and the discussion of incomplete and conflicting evidence. The paper is useful because it makes three correct moves at once: it models structured-data missingness explicitly, it raises fused uncertainty when text and structured evidence disagree, and it penalizes under-triage more heavily than over-triage. The main limitation is scope. This is one dataset and one emergency-triage setting, so the exact penalty weights and coverage tradeoffs should not be treated as universal.

## One-paragraph overview

CRS-Triage is a multimodal triage model for emergency settings where structured clinical variables and clinical text are often incomplete, unreliable, or inconsistent. The model encodes structured data together with missingness masks, encodes text separately, predicts modality-specific Dirichlet evidence, and then fuses the modalities using reliability estimates plus a disagreement-aware uncertainty term. The output is not only a class probability distribution but also a confidence score used for selective prediction: the model can defer when the evidence is too unreliable or too contradictory. The training objective is explicitly risk-shaped so that under-triage costs more than over-triage.

## Model definition

### Inputs
The model takes structured emergency-department features, a binary missingness mask over those features, and clinical text for each encounter.

### Outputs
It outputs a class-probability vector over triage levels, a confidence score, and a final predict-or-defer decision at a chosen coverage threshold.

### Training objective (loss)
The paper jointly optimizes a KL-regularized evidential loss for fused and modality-specific Dirichlet outputs, an expected triage-penalty loss that weights under-triage more heavily than over-triage, a disagreement loss that raises fused uncertainty when modalities conflict, and a confidence-based selective objective.

### Architecture / parameterization
The system has separate structured and text encoders, modality-specific evidential predictors, reliability-aware fusion, disagreement-aware uncertainty adjustment, and a selective prediction layer that decides whether to emit a triage label or defer.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve selective clinical triage when the available evidence is incomplete, unreliable, and cross-modally inconsistent, which is exactly where naive confidence thresholds tend to fail.

### 2. What is the method?
The method separately models structured and text evidence, tracks structured missingness, estimates modality reliability, increases fused uncertainty when modalities disagree, and learns a confidence score that can drive defer decisions under asymmetric under-triage risk.

### 3. What is the method motivation?
In triage, uncertainty is not just "the softmax was flat." Missing lab values, weak documentation, and disagreement between modalities should all change whether the model is trusted to make the call.

### 4. What data does it use?
The experiments use the MIMIC-IV-ED dataset with structured emergency-department data and clinical text.

### 5. How is it evaluated?
The paper evaluates full-coverage classification and calibration, then compares selection methods at fixed 80% and 90% coverage using error rate, under-triage rate, and expected triage penalty over accepted predictions.

### 6. What are the main results?
At 80% coverage, using the CRS confidence score reduces expected triage penalty from 0.267 with evidential certainty to 0.208, and reduces under-triage from 5.9% to 4.7%. At 90% coverage, it reduces triage penalty from 0.331 to 0.291 and under-triage from 7.7% to 6.7%. The point is not just that the model can defer. It is that its own score is better than generic uncertainty surrogates at selecting the safer cases to keep.

### 7. What is actually novel?
The novelty is not multimodal fusion by itself. The useful contribution is confidence that depends on modality reliability, missingness, and cross-modal disagreement, together with a training objective that explicitly respects asymmetric under-triage harm.

### 8. What are the strengths?
It uses the right asymmetry for clinical risk. It does not average disagreement away. It also keeps the deferral mechanism inside the learning problem instead of bolting it on afterward.

### 9. What are the weaknesses, limitations, or red flags?
The evidence is limited to one benchmark setting. The exact penalty schedule is domain-specific. The paper assumes deferral capacity downstream, which is sensible in hospital workflows but not free in practice.

### 10. What challenges or open problems remain?
Generalization across institutions, better handling of distribution shift, and integration with actual downstream clinical workflows remain open. So does the question of how to calibrate deferral policies under changing data quality.

### 11. What future work naturally follows?
Cross-site validation, prospective workflow studies, and stronger shift-aware reliability estimation would all be natural next steps.

### 12. Why does this matter for cabbageland?
It matters because it is a good example of how to do uncertainty and selective action properly: missingness, disagreement, and asymmetric harm should all shape whether the system speaks or defers.

### 13. What ideas are steal-worthy?
Treat missingness as input state, not preprocessing noise. Raise uncertainty when modalities conflict. Optimize deferral against the real asymmetric error cost, not generic accuracy. Compare learned defer scores against simple uncertainty baselines at matched coverage.

### 14. Final decision
**Keep it as adjacent inspiration.** The domain is specific, but the uncertainty-design lesson is solid and transferable.
