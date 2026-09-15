# ModaLens: Measuring Image Sensitivity in Report-Conditioned Medical VLMs

## Basic info

* Title: ModaLens: Measuring Image Sensitivity in Report-Conditioned Medical VLMs
* Authors: Sebastian Andres Cajas Ordonez, Maximin Lange, Quang Bui, Anqi Peter Li, Felipe Ocampo Osorio, Rafi Al Attrach, Kushul Reddy Palakala, Sahil Kapadia, Zakaria Laouabdia Sellami, Xinyue Zhang, Ashley Zhang, Leo Anthony Celi
* Year: 2026
* Venue / source: arXiv:2609.15635
* Link: https://arxiv.org/abs/2609.15635
* Date surfaced: 2026-09-15
* Why selected in one sentence: It cleanly audits whether a report-conditioned medical VLM's answer actually moves when the image changes and the report stays fixed.

## Quick verdict

* Highly relevant

This is a strong diagnostic paper, not because it builds a new model, but because it measures a failure mode clinical multimodal systems can hide: answering from report text while barely using the image. It is careful about what it can and cannot claim because labels are report-derived. This note is based on the full arXiv text.

## One-paragraph overview

ModaLens performs paired image-swap audits on report-conditioned medical VLM prompts. For each MIMIC-CXR case, it holds the question and report fixed while replacing the image with another study image, usually from the same patient. If the answer changes, the model is sensitive to the image under that prompt; if not, it may be anchored by the report, response bias, or nonvisual priors. On 3,199 cases and 44,786 trials, report availability sharply reduces image-swap sensitivity in MedGemma-27B, and the direction replicates across additional model families.

## Model definition

### Inputs

Inputs are chest radiograph images, free-text radiology reports, and yes/no clinical questions. The primary design asks all 14 questions per case: 13 finding-specific CheXpert-style questions plus one composite question. The intervention swaps only the image; report and question are fixed.

### Outputs

The audited model outputs yes/no answers or answer-token scores. The audit outputs flip rates, margin changes, accuracy against report-derived labels, per-finding sensitivity, and layer/intervention analyses.

### Training objective (loss)

ModaLens does not train a new VLM. It evaluates existing instruction-tuned medical and general VLMs, primarily MedGemma-27B, with additional checks on MedGemma-4B, Qwen3.5, and LLaVA-NeXT variants.

### Architecture / parameterization

The main experiment uses MedGemma-27B, a 62-layer decoder model with image and text inputs. The audit is model-agnostic: paired concordant/discordant inputs, readout validation across lowercase first-token, token-family, and generated-answer scoring, and attention/report-token knockout analyses.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

When a medical VLM gets a radiology report plus an image, a correct answer may come entirely from the report. Standard accuracy cannot tell whether the image mattered. ModaLens measures image sensitivity under report-conditioned prompts.

### 2. What is the method?

For each case, run the model with the original image and with a substituted image while holding report and question fixed. Compare generated answers and continuous yes/no margins. Then repeat with the report absent to estimate how much report availability suppresses image sensitivity.

### 3. What is the method motivation?

Clinical multimodal systems can fail silently if a strong text source overrides image evidence. A model can look competent against report-derived labels while ignoring the visual input, which is dangerous when the report is historical, wrong, or mismatched to the image.

### 4. What data does it use?

The headline data are MIMIC-CXR test cases: 3,199 frontal-image cases from 293 patients, 3,180 within-patient substitutions, and 44,786 paired trials across 14 questions. VQA-RAD, SLAKE, OmniMedVQA, and ProbMed are used for supplementary controls, but MIMIC-CXR is the only report-paired dataset.

### 5. How is it evaluated?

The primary metric is answer flip rate under image substitution, with patient-clustered bootstrap intervals. The paper also reports continuous margin shifts, label-changed versus label-unchanged subsets, generated-answer validation, modality ablations, per-finding breakdowns, prompt/order controls, model-family replication, and attention/report-token interventions.

### 6. What are the main results?

Under an explicit answer instruction, MedGemma-27B's generated answer changes on 4.26% of trials with the report and 20.94% without it, a paired difference of 16.7 points with 95% CI [15.6, 17.7]. The original prompt with lowercase first-token readout gives 4.70% with the report and 17.07% without it. Continuous margins also move more without the report: mean absolute paired margin change is 0.690 with the report and 2.307 without it, larger without the report on 82.9% of trials. The report effect persists across Qwen3.5-9B, Qwen3.5-27B, and LLaVA-NeXT on Mistral-7B under the answer instruction.

### 7. What is actually novel?

The novelty is the paired report-conditioned image-swap audit and its careful readout validation. The paper measures sensitivity rather than pretending report-derived label accuracy is visual correctness.

### 8. What are the strengths?

The paired design is clean and easy to reuse. The paper validates the readout, reports continuous changes beyond binary flips, includes prompt/order and substitute-seed checks, and is unusually explicit about limitations. The distinction between "report anchoring" and "image competence" is handled well.

### 9. What are the weaknesses, limitations, or red flags?

The labels are derived from reports, not independent image annotations, so the audit measures image sensitivity rather than visual correctness. MIMIC-CXR is a single-institution chest X-ray setting, and no other dataset in the paper pairs images with reports. Whole-image substitution does not isolate the queried finding, view, position, or acquisition differences. Prompt order changes the magnitude, so the flip rate is not an order-independent model property.

### 10. What challenges or open problems remain?

The next step is independent image-ground-truth evaluation for cases where image and report disagree. The field also needs modality-sensitivity audits for other medical modalities, longitudinal reports, and workflows where historical context is useful but must not dominate current image evidence.

### 11. What future work naturally follows?

Build report-conditioned VLM benchmarks with independently annotated visual changes, add automatic modality-sensitivity checks to medical VLM evaluation, and train systems to surface when the answer is text-driven, image-driven, or conflicted.

### 12. Why does this matter for cabbageland?

This is a reusable causal audit for multimodal models. It asks whether the claimed modality actually carries decision weight, which is the same structural question cabbageland cares about in memory, world models, and tool-using systems.

### 13. What ideas are steal-worthy?

Hold all non-target inputs fixed and intervene only on the modality being audited. Report flip rates and continuous margins. Validate the readout instead of trusting a single token proxy. Treat "uses image" and "is visually correct" as separate claims.

### 14. Final decision

Preserve. This is an excellent evaluation primitive for multimodal grounding and silent-modality failure.
