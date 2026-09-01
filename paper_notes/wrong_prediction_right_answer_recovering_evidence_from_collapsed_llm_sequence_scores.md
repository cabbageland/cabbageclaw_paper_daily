# Wrong Prediction, Right Answer: Recovering Evidence from Collapsed LLM Sequence Scores

## Basic info

* Title: Wrong Prediction, Right Answer: Recovering Evidence from Collapsed LLM Sequence Scores
* Authors: Qiyao Yan, Chenpeng Wang, Liangming Pan
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.31068
* Date surfaced: 2026-09-01
* Why selected in one sentence: It cleanly tests whether reasoning failures are real capability failures or merely output-score collapse.

## Quick verdict

* Must read

I inspected the full arXiv HTML text, especially the readout-gap setup, the target-label-free additive correction, the TF-IDF-missed and permutation controls, the cross-family transfer, and the explicit boundary cases. This earns a preserved note because it does something stricter than most probe papers: it shows that a tiny constrained intervention can recover held-out answer selection without teaching a new reasoning rule.

## One-paragraph overview

The paper argues that a model can internally represent the right answer while still failing at the final answer-selection step. To test that claim, it compares hidden-state probes, native candidate-answer string scores, and a tiny post-hoc score correction that adds one learned offset per label but uses no target labels. If accuracy comes back after such a weak intervention, then the failure was not a missing reasoning path but a late-stage readout distortion. Across controlled logic, ProofWriter, ANLI, and FOLIO, that is exactly what the authors find for the stronger Qwen3.5 models, with transfer to OLMo and Llama and with controls designed to rule out lexical or label-count hacks.

## Model definition

### Inputs
Frozen LLM hidden states at prompt-end and answer-slot positions, candidate-answer strings for multiple-choice style evaluation, and unlabeled in-domain score rows for fitting the additive correction.

### Outputs
Linear-probe predictions of the gold label, corrected candidate-answer scores after label-specific offsets, and the final selected answer.

### Training objective (loss)
The probe is a supervised linear readout trained on frozen hidden states. The diagnostic correction is not a learned reasoning model; it fits only label offsets from unlabeled in-domain score distributions under a prior-conditioned constraint.

### Architecture / parameterization
A frozen generator is paired with simple hidden-state probes and a two-parameter additive score-correction rule for the three-way settings emphasized in the paper.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It asks whether a wrong final answer really means the model failed to reason, or whether the failure is sometimes only a bad output readout.

### 2. What is the method?
Measure the gap between internal decodability and native sequence scoring, then apply a tiny target-label-free additive offset to candidate scores and see whether held-out accuracy recovers.

### 3. What is the method motivation?
Probe success alone is too weak, because probes can decode information the native output path never uses. Aggregate calibration gains are also too weak, because they can hide label-distribution tricks. The paper wants evidence that example-specific answer information really survived inside the model's own scoring path.

### 4. What data does it use?
A controlled synthetic lexical-logic setting plus ProofWriter, ANLI R2, and FOLIO. The main model family is Qwen3.5 2B/4B/9B, with transfer checks on OLMo-2-1B, Llama-3.1-8B, and Pythia checkpoints.

### 5. How is it evaluated?
By comparing raw sequence accuracy, probe accuracy, corrected accuracy, macro-F1, TF-IDF-missed slices, count-preserving permutation nulls, sample efficiency, prior perturbations, surface/verbalizer variants, and cross-family transfer.

### 6. What are the main results?
The main Qwen3.5 rows recover large held-out gains: on the synthetic lexical split, 4B/9B rise from 0.333 to 0.570/0.602; on ProofWriter they rise to 0.653/0.678; on ANLI R2 the 4B model rises from 0.478 to 0.571; on FOLIO diagnostic rows the 9B model reaches 0.638. The 25-example fits already recover useful gains, and the TF-IDF-missed ProofWriter slice still reaches 0.622/0.643 for Qwen3.5-4B/9B. Pythia and near-ceiling rows mostly do not recover, which usefully limits the claim.

### 7. What is actually novel?
The novelty is not the existence of probes or calibration. It is the conjunctive diagnostic: show internal decodability, show native readout collapse, apply an intentionally weak correction, and require the rescued decisions to beat hard nulls on held-out examples.

### 8. What are the strengths?
The paper is unusually disciplined about controls and scope. It uses a deliberately weak intervention, reports failure modes, and avoids pretending that every wrong answer was secretly a hidden success.

### 9. What are the weaknesses, limitations, or red flags?
The diagnostic lives in balanced-label settings with explicit candidate answers and known priors. It is not a general-purpose deployment fix. The recovered accuracy is still below probe accuracy, so the correction exposes only part of the hidden evidence.

### 10. What challenges or open problems remain?
The next challenge is per-example readout distortion beyond a global label offset, especially in freer-form answer settings where candidate labels are not fixed.

### 11. What future work naturally follows?
Testing similar diagnostics on free-form reasoning, tool decisions, and multimodal outputs, plus searching for more localized readout repairs that still keep the "no new reasoning learned" constraint.

### 12. Why does this matter for cabbageland?
Because cabbageland keeps running into the problem of people over-reading a surface failure. This paper gives a sharper way to ask whether the hidden computation is absent or just badly exposed.

### 13. What ideas are steal-worthy?
Use deliberately weak interventions as evidence tests. Separate internal decodability from native readout. Always compare a rescue method against permutation-style nulls before treating it as real signal.

### 14. Final decision
Keep as a preserved note. This is one of the better recent papers on evaluation and model internals because it narrows the claim, stresses the controls, and still gets a real result.
