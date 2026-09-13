# ActMap: Single-Pass Uncertainty Quantification from Generation-Time Activation Maps

## Basic info

* Title: ActMap: Single-Pass Uncertainty Quantification from Generation-Time Activation Maps
* Authors: Jacopo Dardini, Roberta Calegari
* Year: 2026
* Venue / source: arXiv:2609.11498
* Link: https://arxiv.org/abs/2609.11498
* Date surfaced: 2026-09-13
* Why selected in one sentence: It turns a full LLM generation trajectory into a compact fixed-size uncertainty artifact that supports single-pass answer-level reliability scoring.

## Quick verdict

* Highly relevant

I inspected the full arXiv HTML text, including the activation-map construction, supervised classifier setup, baseline taxonomy, main in-domain results, compression comparison to ACT-ViT, transfer failures, ablations, calibration, and limitations. The note is worth keeping because the paper is unusually honest about the boundary between in-domain usefulness and cross-domain failure.

## One-paragraph overview

ActMap addresses answer-level uncertainty quantification for LLM generations. Sampling-based methods need multiple generations, token-probability methods only see the final output distribution, and many white-box methods collapse internal computation to one hidden vector. ActMap records hidden states from every layer at every generated token, adaptively pools the hidden dimension, summarizes time with 12 statistic channels, and maps the result into a fixed 12 x 32 x 128 tensor. A lightweight classifier, usually a compact Vision Transformer, predicts whether the generated answer is correct. In-domain, this single-pass artifact beats common black-box, grey-box, and compact white-box baselines while using far less storage than dense activation tensors. Out of domain, the detector often falls near chance.

## Model definition

### Inputs
Inputs are generation-time hidden states from a decoder-only transformer: every layer, every generated token, and the hidden coordinates pooled online to 128 dimensions. The classifier sees only the compressed activation map, not the generated text or output token probabilities.

### Outputs
The ActMap classifier outputs an estimated probability that a specific generated answer is correct. The score can drive abstention, routing, escalation, or selective verification.

### Training objective (loss)
The classifier is trained supervised on labeled generations with correctness or factuality labels, using a binary classification objective. The base LLM is not changed; hooks collect activations during ordinary decoding.

### Architecture / parameterization
ActMap compresses an L x T x D hidden trajectory into a 12 x 32 x 128 tensor of temporal-statistic channels over pooled layer and hidden-coordinate axes. The main classifier is a compact 2.4M-parameter Vision Transformer, though capacity-matched MLPs perform comparably in ablations.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Deployments need a per-answer reliability signal from one generation. Existing methods either require many samples, read only token probabilities, or discard most of the model's internal trajectory.

### 2. What is the method?
Capture hidden states during normal decoding, compress the layer-token-hidden trajectory into a fixed activation map, and train a small classifier to predict correctness from that map.

### 3. What is the method motivation?
The full generation trajectory contains information about how the model arrived at the answer. A compact structured summary may preserve more uncertainty signal than a final-token probe without the cost of storing dense activation tensors or sampling many answers.

### 4. What data does it use?
The paper evaluates TriviaQA, NQ-Open, GSM8K, and CNN/DailyMail factuality across Qwen3-8B, Llama-3.1-8B, and Mistral-7B, with additional Qwen3-32B scale checks. It reports a 476,372-map dataset for release.

### 5. How is it evaluated?
The paper reports AUROC, AUPRC, ECE, selective-prediction behavior, storage/computation cost, occlusion analysis, ablations, and transfer across datasets, tasks, generators, and model scales. Baselines include semantic entropy, perplexity, mean token entropy, P(True), TAD, RAUQ, EigenScore, and dense ACT-ViT.

### 6. What are the main results?
ActMap leads every non-tensor baseline on all twelve 7-8B model/dataset pairs. Its mean AUROC is 0.825 versus 0.790 for TAD and 0.741 for the best training-free baseline. It nearly matches dense ACT-ViT, 0.825 versus 0.823 mean AUROC, while using 49,152 values instead of about 3.3M values and lower ECE on ten of twelve pairs.

### 7. What is actually novel?
The novelty is the fixed-size activation-map representation: it keeps layer structure, pooled hidden-coordinate structure, and temporal generation statistics in a small artifact that can be scored cheaply after one generation.

### 8. What are the strengths?
The representation is practical, compact, and empirically strong in-domain. The paper compares against multiple UQ families, includes calibration, analyzes where signal appears in the map, and tests classifier swaps to show the representation matters.

### 9. What are the weaknesses, limitations, or red flags?
Transfer is poor. Cross-generator, cross-task, and cross-scale detectors can fall near chance. That means ActMap is not a universal truth detector; it requires target-domain labels and deployment-specific calibration. The evaluation is also limited to open-weight 7-8B models plus a scale check, not frontier closed systems.

### 10. What challenges or open problems remain?
Open problems include transfer-stable activation geometry, label-efficient recalibration, long-form factuality, model-family shifts, adversarial robustness, and combining ActMap with external verification instead of treating it as final authority.

### 11. What future work naturally follows?
Use ActMap as a routing signal for selective verification, retrieval fallback, abstention, or human review. Pair it with deployment-shift monitors so stale detectors cannot silently keep making confident decisions.

### 12. Why does this matter for cabbageland?
Cabbageland cares about uncertainty signals that are cheap enough to run at scale but honest about their scope. ActMap is interesting because it keeps more internal state than token scores while exposing the danger of uncalibrated transfer.

### 13. What ideas are steal-worthy?
Store a compact audit artifact per important generation. Preserve trajectory statistics rather than only final states. Treat uncertainty detectors as deployment-local instruments, and verify transfer before trusting them outside their calibration slice.

### 14. Final decision
Preserve as a highly relevant uncertainty and oversight primitive. It is useful exactly because the paper shows where it breaks.
