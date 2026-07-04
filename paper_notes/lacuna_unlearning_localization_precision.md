# LACUNA: A Testbed for Evaluating Localization Precision for LLM Unlearning

## Basic info

* Title: LACUNA: A Testbed for Evaluating Localization Precision for LLM Unlearning
* Authors: Matteo Boglioni, Thibault Rousset, Siva Reddy, Marius Mosbach, Verna Dankers
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.02513
* Date surfaced: 2026-07-04
* Why selected in one sentence: It gives LLM unlearning a ground-truth parameter-localization testbed instead of treating output suppression as evidence of actual erasure.

## Quick verdict

**Strong keep**

This is a valuable evaluation paper. I inspected the full arXiv / AlphaXiv text, including the masked continual pretraining setup, PII construction, localization precision metric, unlearning baselines, resurfacing attack, results, and conclusion. The caveat is that LACUNA engineers where knowledge is stored; naturally acquired memorization may be messier.

## One-paragraph overview

LACUNA asks whether unlearning methods edit the weights that actually store the information they claim to remove. Existing benchmarks mostly check behavior: does the model stop emitting the forgotten answer while preserving utility? LACUNA instead injects synthetic PII into predefined parameter masks of OLMo-based models using masked continual pretraining. This creates ground-truth storage locations. Unlearning methods can then be evaluated not only on forget / retain behavior but on localization precision: do their edits distinguish in-mask from out-of-mask parameters? The paper finds that current methods can look good behaviorally while barely localizing the target weights and remaining vulnerable to resurfacing.

## Model definition

### Inputs

Inputs include synthetic PII profiles from PANORAMA, general OLMo pretraining data, predefined parameter masks, forget and retain PII QA sets, and unlearning method outputs.

### Outputs

The testbed outputs memorization models with PII injected into known masks, forget / retain evaluation sets, localization precision scores, behavioral unlearning metrics, utility scores, and resurfacing-attack measurements.

### Training objective (loss)

The construction uses masked continual pretraining to inject PII into selected parameter subsets, followed by parameter-efficient instruction tuning to make the model answer PII QA prompts. Evaluated unlearning methods use their own objectives; OracleGrad uses gradient ascent on forget data plus gradient descent on retain data restricted to the known mask.

### Architecture / parameterization

The paper builds 1B and 7B OLMo-based models with six parameter masks. Each mask covers 5% of selected feedforward and attention parameters outside the final instruction-tuned layers. The masks exclude normalization layers and embeddings.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

LLM unlearning can appear successful if the model stops producing a target answer, but that does not prove the stored information is gone. It may be hidden, routed around, or easy to resurface through fine-tuning. Existing output-level benchmarks cannot tell whether an unlearning method targeted the weights responsible for the memorized information.

### 2. What is the method?

LACUNA creates a controlled unlearning testbed by injecting PII into known parameter masks. It mixes synthetic PII with OLMo pretraining data and applies masked continual pretraining so different PII groups update different parameter subsets. It then instruction-tunes the model for QA-style extraction, constructs forget and retain sets, and evaluates unlearning methods on both behavior and localization.

### 3. What is the method motivation?

The motivation is to break a circularity. If we do not know where the knowledge lives, then evaluating a localization-based unlearning method requires trusting another uncertain localization method. LACUNA fixes the storage location before training, so it has ground truth.

### 4. What data does it use?

The paper uses PANORAMA synthetic PII profiles and a 4.3B-token subset of the OLMo-2 pretraining corpus. PANORAMA profiles include multiple PII fields, with the experiments focusing on fields such as email address and numerical identifiers. The released testbed includes memorized PII profiles, forget and retain splits, masks, and trained 1B / 7B models.

### 5. How is it evaluated?

Behavioral evaluation measures forgetting, retain performance, extraction strength, exact memorization, and utility. Localization precision is measured as ROC AUC over per-parameter edit scores, asking whether modified weights are inside the ground-truth mask. Robustness is tested with a resurfacing attack: fine-tune the unlearned model on held-out PII and see whether forgotten profiles leak again.

### 6. What are the main results?

Current methods can perform well on output-level unlearning while failing localization. SimNPO is behaviorally strong but has only marginal localization precision, reported at 0.515 in the email-address OLMo2 1B setting. OracleGrad, which has oracle access to the target mask and uses a simple gradient-difference objective inside that mask, reaches much higher localization precision, reported at 0.915, while preserving retain behavior and showing better resistance to resurfacing.

### 7. What is actually novel?

The novel part is the ground-truth localization testbed. Instead of asking whether a model says the forgotten thing, LACUNA asks whether the unlearning update touched the weights where the information was deliberately placed.

### 8. What are the strengths?

The paper targets the right hidden failure. Output suppression is not erasure. The masked-training construction is clever, the localization metric is direct, and the resurfacing attack makes the privacy risk concrete. The OracleGrad comparison is also useful because it shows precise localization can make even a simple unlearning objective much more robust.

### 9. What are the weaknesses, limitations, or red flags?

The strongest limitation is ecological validity. LACUNA's storage locations are engineered with masks, while real memorized web data may be more distributed, entangled, and architecture-dependent. The PII is synthetic, and the target knowledge is simpler than broad conceptual knowledge or copyrighted corpora. The testbed should complement behavioral evaluations, not replace them.

### 10. What challenges or open problems remain?

The hard problem is finding true storage loci without oracle masks. LACUNA can evaluate whether a proposed localization method works under controlled conditions, but the field still needs methods that identify naturally stored memorized content, distinguish suppression from erasure, and remain robust after continued training or model editing.

### 11. What future work naturally follows?

Useful follow-ups include applying LACUNA-style masked injection to more model families, more knowledge types, and more naturalistic memorization settings. Another direction is evaluating whether interpretability methods, gradient methods, or causal tracing can recover the injected masks before unlearning.

### 12. Why does this matter for cabbageland?

Cabbageland cares about durable agents, memory, privacy, and mechanisms that are testable rather than performative. LACUNA is a reminder that behavior can lie. A system that stops saying a secret has not necessarily stopped storing it.

### 13. What ideas are steal-worthy?

* Evaluate memory edits against known storage masks when possible.
* Separate behavioral forgetting from localization precision.
* Stress-test unlearning with resurfacing after fine-tuning.
* Use ROC AUC over parameter-edit scores rather than arbitrary edit thresholds.
* Treat oracle-localized baselines as sanity checks for whether the unlearning objective is the bottleneck.

### 14. Final decision

**Keep it.** This is the right kind of evaluation infrastructure: it exposes a hidden failure mode instead of rewarding good-looking outputs.

