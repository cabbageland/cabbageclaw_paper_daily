# ConfidenceBench: Evaluating Confidence Calibration in Large Language Models

## Basic info

* Title: ConfidenceBench: Evaluating Confidence Calibration in Large Language Models
* Authors: Matthew ffrench-Constant, Daniel Yang, Xinmeng Huang, Sanyam Kapoor
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.20526
* Date surfaced: 2026-07-26
* Why selected in one sentence: It treats verbalized confidence as a first-class evaluation target and shows, with a proper scoring rule, that recent frontier models can still be badly miscalibrated even when their answer accuracy looks decent.

## Quick verdict

**Highly relevant**

This is a useful evaluation paper because it measures a reliability axis people keep handwaving around. The best result is not that one model wins. It is that accuracy and calibration diverge sharply enough that several models do worse than a calibrated-random baseline on Brier score despite reasonable answer accuracy. I inspected the arXiv abstract and PDF sections covering the benchmark design, scoring setup, category analysis, headline results, and stated limitations.

## One-paragraph overview

The paper introduces a private benchmark for testing whether LLMs can state calibrated confidence, not merely produce correct multiple-choice answers. Each question requires both an answer and a numeric confidence estimate, and models are scored primarily with the Brier score so overconfident mistakes are punished properly. The benchmark is intentionally narrow and adversarial in the right way: high-precision math, spatial reasoning, word lookup, and unknowable questions that cannot be answered from ordinary world knowledge. Across 15 frontier models, the paper shows that the best-calibrated model is not the most accurate model, newer releases are not automatically better calibrated, and some systems remain dramatically overconfident in failure-prone categories.

## Model definition

### Inputs
Each evaluated model receives a private four-choice multiple-choice question from one of four categories plus a prompt to output both an answer and a confidence value from `0` to `100`.

### Outputs
The model outputs a selected answer option and a verbalized probability-like confidence estimate.

### Training objective (loss)
The paper introduces no new trainable model. It evaluates existing frontier LLMs under prompted confidence elicitation and scores the resulting behavior with the Brier score and related calibration diagnostics.

### Architecture / parameterization
The contribution is a benchmark-and-metric protocol rather than a new model architecture. It uses a private `200`-question set, three independent runs per model, category-specific analysis, and a proper scoring-rule evaluation of verbalized confidence.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to measure whether LLMs know when they are likely to be wrong, rather than only whether they can produce the right answer string.

### 2. What is the method?
The method asks models to answer private four-choice questions and state explicit confidence, then evaluates those confidence reports with the Brier score, calibration-gap analyses, and per-category breakdowns.

### 3. What is the method motivation?
In many real settings, a wrong answer with unjustified confidence is more dangerous than a plain miss. Accuracy alone hides that failure mode.

### 4. What data does it use?
It uses `200` private multiple-choice questions split across spatial reasoning, high-precision mathematics, word lookup, and unknowable questions, with repeated evaluation across `15` frontier LLMs and a human baseline.

### 5. How is it evaluated?
It is evaluated with three independent runs per model, overall and per-category Brier scores, accuracy-versus-calibration comparisons, a calibrated-random baseline of `0.1875`, and analysis of confidence gaps and probability distributions.

### 6. What are the main results?
Claude Opus 4.6 and Gemini 3.1 Pro Preview achieve the best reported Brier scores at `0.103`, substantially better than the calibrated-random baseline of `0.1875`. Gemini 3.1 Pro Preview is the most accurate model at `82.7%`, but not the best-calibrated, which is the whole point. Five of the fifteen models perform worse than the calibrated-random baseline on mean Brier score, and Gemini 3.1 Flash-Lite is the worst in the study at `0.367`. The human tester reaches about `70.5%` accuracy and `0.105` Brier, which places the human near the very top calibration tier.

### 7. What is actually novel?
The novelty is mostly in the evaluation contract. The paper treats prompted verbalized confidence as a measurable object with a proper scoring rule, includes an unknowable-question slice, and makes calibration divergence from accuracy impossible to ignore.

### 8. What are the strengths?
It uses a proper scoring rule instead of vague confidence heuristics, evaluates closed and open models without needing logits, and includes adversarially useful categories rather than just generic knowledge questions. The calibrated-random baseline is also a clean sanity check that makes the worst failures legible.

### 9. What are the weaknesses, limitations, or red flags?
The benchmark is still small at `200` questions and private rather than fully inspectable. More importantly, the paper evaluates prompted verbalized confidence, which may partly reflect instruction-following behavior or prompt framing rather than pure epistemic uncertainty. It is a useful behavioral metric, not a final theory of model belief.

### 10. What challenges or open problems remain?
The big open problem is connecting verbalized confidence to deeper internal uncertainty signals, abstention policies, and task settings beyond four-choice questions.

### 11. What future work naturally follows?
Extend the benchmark to richer answer formats, compare prompted confidence with logit-based confidence when available, and test whether calibration-aware prompting or training actually improves deployment-relevant abstention behavior.

### 12. Why does this matter for cabbageland?
Cabbageland cares about systems that know when not to bluff. This paper gives a clean reminder that answer accuracy and self-knowledge are different capabilities and should be measured separately.

### 13. What ideas are steal-worthy?
Score verbalized confidence directly with a proper scoring rule. Include an unknowable slice instead of only answerable questions. Keep a calibrated-random baseline in the report so bad calibration remains embarrassing in an interpretable way.

### 14. Final decision
**Keep it as a calibration reference.** The benchmark is narrow, but the correction it makes to sloppy accuracy-only evaluation is real and useful.
