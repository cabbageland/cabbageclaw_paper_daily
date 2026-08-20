# ReWEIGH the Evidence: Calibrating Token-Level Ordinal Visual Evidence to Mitigate Hallucinations in Large Vision-Language Models

## Basic info

* Title: ReWEIGH the Evidence: Calibrating Token-Level Ordinal Visual Evidence to Mitigate Hallucinations in Large Vision-Language Models
* Authors: Jihae Jeong, Junha Choi, Hwanjo Yu
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.19075
* Date surfaced: 2026-08-20
* Why selected in one sentence: It introduces a clean training-free decoding intervention that measures candidate-specific visual support instead of leaning on generic confidence or attention heuristics.

## Quick verdict

* Highly relevant

I inspected the arXiv HTML full text. This is one of the strongest hallucination-mitigation papers in the batch because it intervenes at the right level: the current candidate token, judged against the actual visual evidence available inside the model. The method is lightweight, legible, and backed by sensible ablations rather than just a single benchmark win.

## One-paragraph overview

ReWEIGH uses the internal visual-token states of a large vision-language model as a source of token-level evidence during decoding. For each candidate token, it projects each visual position through the output head, converts position-wise support into an ordinal statistic that is comparable across positions, aggregates that evidence with dense mean reciprocal rank, and compares the result against a token-specific reference learned from unlabeled images. If the candidate falls below that reference, ReWEIGH applies a bounded suppression penalty. The whole intervention is training-free, uses cached prefill evidence, and tries to reduce hallucinations without simply making the model speak less.

## Model definition

### Inputs
The method takes an image, the text prompt, the LVLM's visual-token hidden states, the current candidate token set during decoding, and a token-specific calibration reference estimated from unlabeled images.

### Outputs
It outputs adjusted decoding scores for candidate next tokens and therefore a modified generated response with reduced unsupported content.

### Training objective (loss)
There is no new training objective for the main method. ReWEIGH is a training-free decoding intervention applied to pretrained LVLMs.

### Architecture / parameterization
The method uses logit-lens-style readouts over visual-token states, dense mean reciprocal rank for scale-invariant evidence aggregation, and a token-specific reference table that determines when to apply a bounded suppression penalty.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to reduce LVLM hallucinations by measuring whether the image actually supports the token the model is about to emit.

### 2. What is the method?
The method aggregates rank-based internal visual evidence across positions, calibrates that evidence per token using unlabeled images, and suppresses only those candidate tokens whose evidence falls below their token-specific reference.

### 3. What is the method motivation?
Attention and output confidence are not candidate-specific evidence measures. A model can be confident or visually engaged while still proposing an unsupported token. The paper wants a direct signal of visual support for the actual next-token candidate.

### 4. What data does it use?
The main experiments use four 7B LVLM backbones on CHAIR, AMBER, MMHal-Bench, and MM-Vet, plus broader evaluation across **11** models from **6** architecture families up to **32B**. Calibration is built from **500** unlabeled MS COCO training images.

### 5. How is it evaluated?
It is evaluated on object-hallucination metrics, generative and discriminative multimodal benchmarks, general multimodal utility, and a series of ablations on ordinal readout choice, token-specific calibration, calibration size, and image-specific evidence mismatch.

### 6. What are the main results?
Across the four main backbones, ReWEIGH reduces CHAIR[I] by **10.3% to 21.3%** while largely preserving or improving F1. The intervention extends to **11** models up to **32B**. With cached evidence, the average added latency is only **1.33%** per token. In ablations, replacing the ordinal readout with probability pooling worsens CHAIR[S] from **44.8** to **50.0**, and shuffling token references degrades performance, which is exactly the evidence the paper needed.

### 7. What is actually novel?
The novelty is combining position-invariant ordinal evidence pooling with token-specific calibration so the model can decide whether a particular candidate token is unusually weakly supported by the image.

### 8. What are the strengths?
It is light, explicit, and easy to reason about. The method does not need retraining, the calibration table is cheap, and the ablations actually isolate the role of the ordinal readout and token-token reference matching.

### 9. What are the weaknesses, limitations, or red flags?
The intervention is still heuristic rather than probabilistically grounded in a full generative model of image evidence. It relies on a chosen readout layer and a calibration set. The strongest results are on hallucinated object mentions, so broader reasoning failures may not yield as neatly.

### 10. What challenges or open problems remain?
The main open problem is extending this kind of candidate-specific evidence control beyond object hallucination toward longer reasoning chains, relational errors, and multi-token unsupported claims.

### 11. What future work naturally follows?
Future work should learn or adapt the calibration table online, combine token-level evidence with answer-level abstention policies, and test whether similar ordinal readouts help multimodal chain-of-thought generation.

### 12. Why does this matter for cabbageland?
Because it is a concrete reminder that "confidence" and "evidence" are not the same thing. The paper offers a steal-worthy pattern for grounding generation in the model's own internal evidence without retraining the whole system.

### 13. What ideas are steal-worthy?
Use rank-based rather than probability-based pooling when cross-position scales are incomparable. Calibrate evidence per candidate token instead of globally. Cache evidence during prefill so grounding interventions stay cheap at decode time.

### 14. Final decision
Keep as a preserved note. The method is clean, the intervention point is right, and the paper is more useful than most hallucination-mitigation work.

## 6. Mandatory critical angles

This paper is strongest on grounding, controllability, and failure-mode specificity. Its core strength is that it measures a real candidate-level quantity instead of waving at generic attention maps. The main caution is that the evidence signal is still a derived heuristic over internal states.

## 7. Writing style

The right tone is sharp and approving. This is a rare hallucination paper that actually improves the measurement target instead of decorating the same old one.

## 8. Repository output format

Saved as a preserved paper note because the token-specific evidence-calibration idea is both reusable and unusually legible.
