# The Calibration Floor: Format Repair Can Masquerade as Self-Correction at Small-to-Mid Scale

## Basic info

* Title: The Calibration Floor: Format Repair Can Masquerade as Self-Correction at Small-to-Mid Scale
* Authors: Mingguang Chen, Bo Qu, Licheng Wang
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.04355
* Date surfaced: 2026-08-06
* Why selected in one sentence: It is one of the cleanest recent audits of self-correction claims because it isolates answer-content change from answer-extraction repair and then tests the difference causally.

## Quick verdict

**Must read**

I inspected the arXiv HTML paper, especially the margin decomposition, the floor criterion, the admission gates, the forced-continuation probe, the constrained-decoding control, and the main results. The paper is strong because it does not merely complain that self-correction metrics are messy. It gives an exact decomposition and then actively intervenes on the extraction boundary. The central conclusion is severe: much of what gets measured as self-correction is format repair, not answer-content change. The main caveat is that the content-margin interpretation still lives on a post-treatment-selected both-parseable subset, and the frontier check is lower powered than the main open-weight grid.

## One-paragraph overview

The paper studies language-model self-revision under a strict no-external-feedback setting and asks whether measured accuracy gains reflect genuine answer changes or merely better answer extraction. It decomposes the total self-revision delta into three exact pieces: a content margin where both initial and revised answers are parseable, a format-recover margin where only the revised answer becomes parseable, and a format-loss margin where the revision destroys an otherwise parseable answer. It then adds stronger controls, including forced continuation with zero new reasoning and grammar-constrained decoding that makes answers parseable by construction, to test whether the observed gains survive once the extractor is no longer doing the hidden work.

## Model definition

### Inputs
The framework takes initial and revised model outputs, answer-extractor outcomes, correctness labels, confidence signals, and gating thresholds across multiple model-task cells.

### Outputs
It outputs an exact decomposition of the total revision delta into content and format margins, plus calibration-floor analyses, gating estimates, and causal-control comparisons.

### Training objective (loss)
There is no new learned model. The paper is an evaluation instrument built around offline measurement, decomposition, and causal controls.

### Architecture / parameterization
The instrument combines frozen-trajectory evaluation, a per-sample delta identity, a content-versus-format decomposition, a floor criterion computed on the content margin, a forced-continuation probe, and a constrained-decoding control that forces answer parseability.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the fact that many self-correction claims collapse accuracy changes, answer-content changes, and answer-extraction changes into one number, then call the result "reasoning improvement."

### 2. What is the method?
The method exactly decomposes total self-revision delta into content, format-recover, and format-loss margins, then tests the decomposition with forced continuation and constrained-decoding controls while analyzing calibration on the content margin rather than on the total effect.

### 3. What is the method motivation?
If the revised answer becomes easier to parse, an evaluation pipeline can record an accuracy gain even when the model did not become more correct in any meaningful sense. The paper wants to separate that formatting artifact from actual answer change.

### 4. What data does it use?
The main grid covers Qwen3.5 models from 0.8B to 9B, Gemma-4-12B, multiple benchmark tasks, 29 primary cells, a literature-protocol replication arm, and a smaller frontier API check that includes Tencent Hy3 and Nvidia Nemotron-3-Ultra-550B.

### 5. How is it evaluated?
It evaluates the exact decomposition, scale effects, the content-margin calibration floor, leave-one-out prediction, cross-family replication, a literature protocol replication, a forced-continuation probe, and a constrained-decoding causal control.

### 6. What are the main results?
Across the 12 admitted cells with meaningful extraction failures, format effects exceed content effects with one-sided Wilcoxon p = 1.7e-3. The constrained-decoding control closes a median 71% of the gap between the naive total effect and the content-margin estimate. In the frontier arm, the content margin is exactly zero in all five cells even when total effects reach +0.275. One particularly brutal result is 4B GSM8K: a zero-reasoning forced continuation recovers correct answers on 63.5% of the probed rows, while the full two-round revision protocol recovers only 19.2%, which is almost impossible to read as a reasoning story.

### 7. What is actually novel?
The novelty is the exact additive decomposition plus the insistence on validating it causally rather than only descriptively. The floor criterion is also applied to the content margin itself, which is the right object if the question is genuine correction.

### 8. What are the strengths?
The paper attacks the right failure boundary. It gives a better object to optimize and report. It also includes honest counterexamples where the full revision outperforms the zero-reasoning probe, instead of overclaiming a universal verdict.

### 9. What are the weaknesses, limitations, or red flags?
The content margin is still measured on a post-treatment-selected both-parseable subset. The frontier arm is lower powered than the main grid. The study is about no-feedback self-correction, not the broader world of tool-using or externally verified revision.

### 10. What challenges or open problems remain?
A stronger causal story for content change under selection, better extractors that reduce the need for this cleanup, and extensions to tool-augmented or externally verified revision settings all remain open.

### 11. What future work naturally follows?
Any self-correction benchmark should adopt a similar decomposition or at least report it. Tool-based correction settings should repeat the same controls. Answer extractors themselves should be stress-tested as part of evaluation, not treated as invisible plumbing.

### 12. Why does this matter for cabbageland?
It matters because cabbageland cares about honest evaluation of reasoning and agent repair. This paper is a good antidote to accidentally rewarding formatting or extraction artifacts while thinking you measured better thinking.

### 13. What ideas are steal-worthy?
Decompose total gains into content and format margins. Run a zero-reasoning continuation control. Compute gating floors on the content margin, not on the total delta. Treat extractors as part of the evaluated system, not as neutral observers.

### 14. Final decision
**Keep it.** This is a harsh but useful measurement paper with lessons that transfer well beyond its specific self-correction setup.
