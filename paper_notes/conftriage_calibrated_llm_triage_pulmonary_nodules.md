# ConfTriage: A Calibration-Aware LLM Triage Framework for Pulmonary Nodule Malignancy with Selective Specialist Deferral

## Basic info

* Title: ConfTriage: A Calibration-Aware LLM Triage Framework for Pulmonary Nodule Malignancy with Selective Specialist Deferral
* Authors: Md Rabiul Islam, Samir Abdaljalil, Erchin Serpedin, Hasan Kurban
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.10885
* Date surfaced: 2026-08-12
* Why selected in one sentence: It turns LLM confidence from decorative output into a calibrated triage policy with selective specialist deferral and explicit guarantees.

## Quick verdict

* Preserve-worthy adjacent paper

I inspected the arXiv HTML full text. This is a strong adjacent medical paper because it has a real deployment story instead of a generic "LLMs can read radiology too" pitch. The useful move is making confidence operational.

## One-paragraph overview

The paper asks whether a generalist LLM reading a faithful natural-language rendering of standard pulmonary-nodule attributes can serve as a calibrated triage layer rather than a raw classifier. ConfTriage answers yes, but only after wrapping the LLM in a careful policy: verbalized confidence is transformed in logit space, Platt-scaled on a calibration fold, and used to defer low-margin cases to a specialist DL backstop. A seven-way input ablation across five frontier LLMs on LIDC-IDRI shows that natural-language descriptions carry the diagnostic signal while low-level image statistics are mostly useless for the tested setup. The system reports 88.22% F1 and 0.92 AUC, handles 76.5% of cases with the LLM alone at the chosen threshold, and reduces ECE from 0.085 to 0.042 after calibration.

## Model definition

### Inputs
The framework takes structured pulmonary-nodule attributes, renders them into a fixed natural-language template, queries an LLM for prediction plus verbalized confidence, and optionally routes uncertain cases to a specialist deep-learning classifier.

### Outputs
It outputs either a calibrated LLM malignancy prediction or a deferral decision that hands the case to the specialist backstop.

### Training objective (loss)
The contribution is mainly a calibrated inference and triage framework. The specialist backstop is pretrained separately; the main paper fits a Platt-scaling map on the LLM confidence and defines threshold-based routing.

### Architecture / parameterization
The pipeline has three pieces: text-only structured input to the LLM, logit-space calibration of verbalized confidence, and threshold-based selective deferral to Certain-Net or an equivalent specialist model.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to make LLM-based medical triage reliable enough to be useful by calibrating confidence and deferring uncertain cases instead of forcing the LLM to decide everything.

### 2. What is the method?
The method renders standard radiological attributes into text, gets a diagnosis and verbalized confidence from an LLM, calibrates that confidence in logit space with Platt scaling, and routes low-margin cases to a specialist DL backstop.

### 3. What is the method motivation?
Raw LLM accuracy numbers are not enough for triage. A deployment story needs to know which cases the LLM should handle, which ones it should refuse, and what evidence channel actually carries the signal.

### 4. What data does it use?
It uses the LIDC-IDRI pulmonary nodule benchmark, five frontier LLMs, seven input regimes, and a specialist nodule classifier used as the deferral backstop.

### 5. How is it evaluated?
It measures F1, AUC, calibration, coverage versus deferral, multi-model input ablations, theoretical guarantees, and comparisons against reader-consensus targets.

### 6. What are the main results?
ConfTriage reports 88.22% F1 and 0.92 AUC, reduces ECE from 0.085 to 0.042 after calibration, and at tau = 0.28 lets the LLM resolve 76.5% of cases while deferring 23.5% to the specialist model.

### 7. What is actually novel?
The novelty is not merely using an LLM on radiology attributes. It is turning verbalized confidence into a calibrated decision object tied to selective deferral, with a finite-sample combined-risk bound and an oracle-style calibration-to-optimality argument.

### 8. What are the strengths?
The input ablation is useful, the operational policy is clear, and the paper cleanly separates three questions that are usually blurred together: signal source, confidence calibration, and fallback routing.

### 9. What are the weaknesses, limitations, or red flags?
The setup depends on curated structured attributes rather than raw clinical workflow, uses a single benchmark, and does not replace the specialist model. It is a triage-layer paper, not a full diagnostic deployment result.

### 10. What challenges or open problems remain?
Real-world report noise, broader cohorts, prospective validation, and calibration under distribution shift remain open. Another open problem is whether the same approach works when the structured attribute schema itself is messy or partially missing.

### 11. What future work naturally follows?
Prospective triage studies, broader specialist backstops, richer textual inputs such as clinical reports, and selective-deferral designs for other medical decision-support tasks all follow naturally.

### 12. Why does this matter for cabbageland?
Cabbageland keeps caring about systems that know when not to commit. This paper is a clean example of confidence becoming a routing boundary rather than a decorative side output.

### 13. What ideas are steal-worthy?
Treat verbalized confidence as a calibratable score. Use explicit deferral policies rather than forcing one model to do everything. Run ruthless input ablations to identify which information channel actually carries the task signal.

### 14. Final decision
Keep as a preserved note. The domain is medical, but the calibrated-confidence-plus-deferral pattern is broadly reusable.

## 6. Mandatory critical angles

This paper is strongest on operational framing and confidence handling. The main caution is that it still leans on a curated structured-input regime and a benchmark setting that is much cleaner than messy clinical reality.

## 7. Writing style

The right tone is favorable but restrained. The paper earns credit for a real deployment logic, but it should not be mistaken for a raw-pixel end-to-end diagnostic replacement.

## 8. Repository output format

Saved as a preserved paper note because the calibration and selective-deferral pattern is worth keeping even outside medicine.
