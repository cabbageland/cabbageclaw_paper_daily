# Temperature Scaling Is Not Enough: Calibration Gaps Under Human Label Distributions

## Basic info

* Title: Temperature Scaling Is Not Enough: Calibration Gaps Under Human Label Distributions
* Authors: Wisdom Dogah
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.13423
* Date surfaced: 2026-07-16
* Why selected in one sentence: It isolates a basic calibration failure that many uncertainty claims quietly assume away: the target is often a human distribution, not a one-hot truth.

## Quick verdict

**Useful**

This is not a giant benchmark or a new model family, but it makes a neglected assumption visible and measures the size of the resulting error. That alone gives it more value than many louder calibration papers. I inspected the full arXiv HTML paper, including the problem formulation, calibration protocol, results across vision and language, implications, and limitations.

## One-paragraph overview

The paper asks a narrow but important question: if temperature scaling is fit on hard labels, how well does it calibrate models when the true target is a soft human label distribution instead of a one-hot class? To answer that, it compares hard-label temperature scaling against an oracle that is fit directly on soft labels, using CIFAR-10H and ChaosNLI. The difference between their Brier scores is defined as the soft-label calibration gap. Across all nine tested model-and-dataset configurations, that gap is positive, which means hard-label calibration systematically understates the smoothing required when human disagreement is real rather than annotation noise.

## Model definition

### Inputs
The calibration stage takes logits from pretrained or finetuned classifiers together with either hard one-hot labels or soft human label distributions.

### Outputs
It outputs calibrated class probabilities, either via a single temperature scalar or via multiclass one-vs-rest isotonic regression.

### Training objective (loss)
Temperature scaling fits a single scalar `T` by minimizing negative log-likelihood on a held-out validation split. The oracle condition fits calibration directly against soft labels. Isotonic regression is evaluated as a second post-hoc baseline under analogous hard-label and soft-label fitting conditions.

### Architecture / parameterization
The underlying models are ResNet-18, ResNet-50, and ResNet-101 for CIFAR-10H, plus DistilBERT, BERT-base, and BERT-large for ChaosNLI. The paper's contribution is the calibration analysis, not a new predictive architecture.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tests whether the standard hard-label calibration recipe remains valid when the target label is genuinely distributional because humans disagree.

### 2. What is the method?
The method is a controlled measurement study. For each model, the paper fits hard-label temperature scaling, fits a soft-label oracle calibration, evaluates both against soft targets with Brier score and ECE, and repeats the same qualitative test with multiclass isotonic regression.

### 3. What is the method motivation?
Most calibration work assumes there is a single correct class and that disagreement is noise. That assumption breaks in ambiguous language and perception tasks, where the meaningful target may be a probability distribution over plausible labels.

### 4. What data does it use?
It uses CIFAR-10H for vision and ChaosNLI for language, both of which provide soft human label distributions rather than only majority-vote labels.

### 5. How is it evaluated?
Evaluation compares hard-label temperature scaling, soft-label oracle temperature scaling, and isotonic regression using Brier score and ECE across three model scales in each modality, repeated over three seeds.

### 6. What are the main results?
The soft-label calibration gap is positive in all nine configurations, ranging from `0.002` to `0.134` in Brier score. In vision, the gap rises from `0.002` on ResNet-18 to `0.003` on ResNet-50 and ResNet-101. In the SNLI-derived ChaosNLI split, the gap rises from `0.045` on DistilBERT to `0.053` on BERT-large. The mean language gap is `0.079`, far larger than the mean vision gap of `0.003`. Isotonic regression shows the same qualitative failure.

### 7. What is actually novel?
The novelty is diagnostic rather than architectural. The paper turns a rarely stated assumption of temperature scaling into a measurable gap and shows that the failure survives a second post-hoc calibration baseline.

### 8. What are the strengths?
The study is clean, uses public datasets with real soft labels, and states clearly when one of its scale hypotheses becomes inconclusive. It also keeps the message small enough to stay believable.

### 9. What are the weaknesses, limitations, or red flags?
The scale range is modest, the language models are small by 2026 standards, and ChaosNLI-M remains near chance, which muddies the scale claim on that split. The study is also limited to English-language annotation contexts.

### 10. What challenges or open problems remain?
The practical problem is how to calibrate well when only a small number of repeated human annotations are available, which is exactly the case in many real deployments.

### 11. What future work naturally follows?
The obvious next steps are larger-scale replications, more calibration methods under soft-label evaluation, and low-annotation regimes where the target distribution must be estimated cheaply.

### 12. Why does this matter for cabbageland?
Cabbageland cares about uncertainty, verification, and what model confidence actually means. This paper is a direct warning that majority-vote calibration can misstate reliability when ambiguity is structural rather than accidental.

### 13. What ideas are steal-worthy?
Evaluate uncertainty against soft human targets when disagreement is meaningful. Keep a clean "oracle on soft labels" baseline to measure how much hard-label calibration leaves on the table. Do not confuse majority-vote confidence with calibrated uncertainty.

### 14. Final decision
**Keep it.** It is a compact paper, but the measurement is real and the lesson is broadly reusable.
