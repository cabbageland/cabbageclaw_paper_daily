# Phantom Gains: Auditing Self-Improvement Against a Measured Null

## Basic info

* Title: Phantom Gains: Auditing Self-Improvement Against a Measured Null
* Authors: Cheng Xu, Nan Yan, Liming Chen, M-Tahar Kechadi
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.20290
* Date surfaced: 2026-08-23
* Why selected in one sentence: It is the sharpest paper in the batch on forcing self-improvement claims to survive a measured transition-level null rather than an assumed one.

## Quick verdict

* Must read

I inspected the arXiv HTML full text, especially the audit construction, the seven failure modes, the benchmark design, and the matched positive-control comparison. This paper earns a preserved note because it does the severe thing the literature keeps dodging: it measures the null for the transition statistic itself and shows that several standard analyses confidently report improvement on a model that never trained. The result is less "self-improvement is impossible" than "your audit is probably lying unless you measured its floor."

## One-paragraph overview

The paper studies how people decide whether a language model has improved itself at the level of individual problems gained and lost. Its core claim is that many of those transition-level analyses are built on differencing noisy estimates without first measuring what the same statistic looks like when nothing changed. To expose that, the authors run three rounds of rank-32 LoRA self-training on Qwen3-8B, but they also push a frozen control through the same evaluation path and show that common ledger-style and expansion-style statistics manufacture fake capability changes. They replace the thresholded expansion statistic with a per-problem exact test against pooled baseline replicates under false-discovery-rate control, then compare self-training against a matched distillation positive control and a benchmark-specific corruption floor.

## Model definition

### Inputs
Qwen3-8B checkpoints, unlabeled problem streams, filtered rationales or teacher outputs for different training arms, repeated sampled evaluations, and per-problem outcomes on AIME and MATH-derived benchmark slices.

### Outputs
Transition ledgers, per-problem detections of gain or loss, corruption and sharpening counts, and matched comparisons between self-training and distillation arms.

### Training objective (loss)
The audit itself is not a new trainable model. The paper studies several existing training arms, including rank-32 LoRA self-training and external distillation, then audits their claimed gains under controlled repeated evaluation.

### Architecture / parameterization
Evaluation-and-audit framework around LoRA-trained Qwen3-8B checkpoints. The core machinery is a transition ledger, measured null estimation from frozen-model replicates, and a threshold-free exact-test detector under FDR control.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the fact that transition-level self-improvement claims are usually treated as if problem gains and losses were directly observable, when in reality they are noisy differences between noisy sampled evaluations.

### 2. What is the method?
The method is a controlled transition-level audit. The paper runs training arms and a frozen control through the same pipeline, measures the null behavior of the transition statistics, identifies seven failure modes, replaces thresholded expansion with a per-problem exact test against pooled baseline replicates under FDR control, and evaluates gain and corruption against matched positive controls.

### 3. What is the method motivation?
Mean accuracy hides whether a system gained new problems or merely reshuffled noisy solves, so transition-level auditing is the right direction. But transition-level auditing itself becomes misleading if the statistic's own floor is unmeasured.

### 4. What data does it use?
The paper evaluates on three problem regimes: a 200-problem stratified subsample of MATH-500 for corruption-heavy analysis, AIME 2025 and 2026 for low-contamination expansion analysis, and a 1,163-problem difficulty band profiled from 10,999 held-out MATH problems for benchmark-specific noise-floor analysis. On AIME, the base model reaches only about 0.175-0.180 of the problems, leaving 22 rarely reached problems and 10 never reached problems for the sharpening-versus-expansion analysis.

### 5. How is it evaluated?
It compares frozen-control replicates, three self-training variants, and an external distillation positive control under matched stream, retained volume, and evaluation settings. The paper evaluates transition statistics, held-out replicate behavior, corruption counts, and exact-test detections instead of relying only on headline accuracy.

### 6. What are the main results?
The most damning result is that a frozen Qwen3-8B evaluated twice still produces an apparent expansion rate of 7/25 = 0.280 on unreached AIME problems under the common thresholded statistic. Across 110 frozen comparisons, the null for the "repair" threshold remains 0.058 [0.038, 0.078], not zero. The exact-test replacement returns zero detections on all 11 held-out baseline replicates. Under the matched ladder, distillation improves 8-11 of 22 rarely reached AIME problems while three self-training arms improve only 0-2, with the asymmetry surviving regression control at p < 1e-8. Both method families also corrupt 88-106 of 1,163 band problems against a design-matched floor of 8.

### 7. What is actually novel?
The real novelty is not another self-improvement benchmark. It is the insistence that every transition statistic needs its own measured null, plus a nearly free way to estimate that null from baseline replicates already present in multi-arm studies.

### 8. What are the strengths?
The paper is unusually severe about controls. It measures what popular statistics do on a model that never trained, separates sharpening from true expansion, uses a matched positive control instead of only criticizing self-training, and quantifies corruption rather than letting gains monopolize the narrative.

### 9. What are the weaknesses, limitations, or red flags?
The analysis is concentrated on mathematical reasoning benchmarks and one Qwen3-8B LoRA regime, so the exact numbers should not be over-generalized. The paper is much stronger at falsifying weak transition claims than at proving a broad replacement story for every training method. And on truly never-reached AIME problems, the evidence remains inconclusive.

### 10. What challenges or open problems remain?
The next challenge is extending this style of audit to other domains, other training regimes, and especially agent settings where "problem solved" is itself more ambiguous and tool use adds more sources of noise.

### 11. What future work naturally follows?
Build measured-null transition auditing into standard self-improvement, self-training, and agent-learning studies. Apply the same discipline to software tasks, world-model updates, and tool-use agents where silent corruption could be even more operationally damaging.

### 12. Why does this matter for cabbageland?
Because cabbageland cares about measured improvement, not self-congratulatory trace statistics. This paper gives a brutal but useful rule: before claiming that a training loop discovered new capability, first show that your audit does not "discover" the same thing on a frozen model.

### 13. What ideas are steal-worthy?
Measure a null for every transition statistic. Use baseline replicates already present in multi-arm studies instead of pretending null estimation is too expensive. Report corruption floors and corruption-to-learning ratios, not only gains. Keep a matched positive control in the same stream and evaluation regime.

### 14. Final decision
Keep as a preserved note. The paper is one of the best recent examples of methodological severity paying off immediately.

## 6. Mandatory critical angles

The paper is strongest on evaluation fairness, failure-mode analysis, and novelty-versus-packaging discipline. It earns the audit label because it measures the floor of the audit statistic itself. The main caution is transferability: the exact magnitudes come from a specific reasoning setup, even if the auditing lesson travels well.

## 7. Writing style

The right tone is severe and approving. The paper deserves credit for saying that a flattering transition story is worthless if the same statistic flatters a frozen model.

## 8. Repository output format

Saved as a preserved paper note because the measured-null principle is broadly reusable and likely to age well.
