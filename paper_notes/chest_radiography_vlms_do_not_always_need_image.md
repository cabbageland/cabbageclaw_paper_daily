# Vision-language models for chest radiography do not always need the image

## Basic info

* Title: Vision-language models for chest radiography do not always need the image
* Authors: Mahshad Lotfinia, Sebastian Ziegelmayer, Lisa Adams, Daniel Truhn, Andreas Maier, Soroosh Tayebi Arasteh
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.17710
* Date surfaced: 2026-06-17
* Why selected in one sentence: It replaces medical VLM accuracy theater with causal image-use audits that test whether correct answers actually depend on the radiograph.

## Quick verdict

* Highly relevant

This is a sharp healthcare/evaluation paper. It does not ask whether medical VLMs can answer chest X-ray questions with respectable accuracy; it asks whether those answers causally depend on the image. I inspected the full PDF, including the introduction, intervention design, metrics, model panel, main result tables, robustness checks, and methods.

## One-paragraph overview

The paper audits medical and general VLMs on chest radiograph yes/no probes by intervening on the image while holding the question fixed. It uses label-matched image swaps, target-region masks over radiologist-marked boxes, and irrelevant masks of the same size. The resulting metrics distinguish accuracy from causal grounding: a model can be correct on the original image but keep the same answer when the relevant region is removed or even when another patient's same-label image is swapped in. Across nine systems, the authors find that text-only baselines are surprisingly close to multimodal systems, several VLMs ignore the image entirely, and the models that do use the image do so selectively rather than reliably.

## Model definition

### Inputs
The evaluated systems receive a chest radiograph and a yes/no question such as whether a finding is present. Depending on condition, the image is original, swapped for a different patient's same-label image, masked over the radiologist-marked target region, or masked over an irrelevant same-size region. Text-only baselines receive the prompt without image input.

### Outputs
The systems output yes/no answers and, where available, first-token confidence estimates. The audit computes accuracy, causal grounding rate, unrelated-image answer rate, irrelevant-mask stability, and a grounding-specificity premium.

### Training objective (loss)
The paper does not introduce a new multimodal model training objective. It evaluates existing general-purpose, specialist medical, frontier multimodal, text-only, and vision-only systems. The RAD-DINO baseline uses frozen image features with an L2-regularized logistic-regression head trained per finding.

### Architecture / parameterization
The model panel includes four general multimodal systems, two specialist medical multimodal systems, a closed-source frontier multimodal model, two text-only baselines, and a frozen RAD-DINO vision-only probe. The key architecture is the audit pipeline, not a new model: every case is evaluated under controlled image interventions, then categorized as ignoring the image, unstable, or using the image.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Medical VLM benchmarks often treat answer accuracy as evidence that the model used the image. That inference is unsafe because text priors, label prevalence, report patterns, and finding co-occurrence can produce correct answers without visual grounding.

### 2. What is the method?
The method is an interventional audit. For each chest radiograph question, the authors compare the model's answer under original image, label-matched swap, target-region occlusion, and irrelevant-region occlusion. If a correct answer survives removal of the relevant region and survives patient-specific image swap, accuracy is not evidence of image use.

### 3. What is the method motivation?
Post hoc saliency and attention maps do not establish causal dependence. A direct behavioral test should alter the image evidence and observe whether the answer changes for the right reason. The target mask and irrelevant mask separate localized visual grounding from generic occlusion sensitivity.

### 4. What data does it use?
The main probe set has 2,575 yes/no decisions built from MS-CXR phrase-grounding boxes, MIMIC-CXR labels, and ReXErr report-error cases. A CheXpert-based probe set with 1,380 cases supports cross-dataset analysis. The target masks rely on radiologist-marked boxes in MS-CXR.

### 5. How is it evaluated?
The paper evaluates accuracy plus three behavioral metrics. Causal grounding rate measures how often correct original answers flip when the target region is masked. Unrelated-image answer rate measures how often correct original answers survive a same-label patient swap. Irrelevant-mask stability measures robustness to a same-size irrelevant occlusion. The combination assigns models to ignore-image, unstable, or use-image categories.

### 6. What are the main results?
A text-only model with no image access lands within 5.7 accuracy points of the best multimodal system, and a 119B multimodal model is statistically indistinguishable from a 7B text-only baseline. Three systems ignore the image under the audit, one is unstable, and five use the image selectively. In the table shown in the paper, MedGemma-1.5-4B has nonzero causal grounding but still high unrelated-image answer rate, while LLaVA-Med-7B has zero causal grounding and perfect answer stability under image changes. The qualitative message is severe: some benchmark-correct medical VLM behavior is language-prior behavior wearing a radiology costume.

### 7. What is actually novel?
The novelty is the combined causal triad: label-matched swap, target mask, and irrelevant mask, read together with text-only and vision-only baselines. The paper is not merely another medical VQA benchmark; it is a grounding audit that asks whether the visual modality did causal work.

### 8. What are the strengths?
The intervention design is clear and transferable. The inclusion of text-only baselines is essential and damaging in the useful way. The paper also checks robustness across dataset, resolution, prompt phrasing, demographic/view subgroups, confidence, and radiologist comparisons.

### 9. What are the weaknesses, limitations, or red flags?
The task is still mostly yes/no finding-level probing, not full clinical reporting or workflow assistance. The target mask assumes the marked box captures the decisive visual evidence, which is reasonable but not perfect for diffuse findings. Same-label swaps preserve the label by design, so UAR must be interpreted alongside target masking rather than alone. The results should not be stretched into a complete clinical safety evaluation.

### 10. What challenges or open problems remain?
Medical VLM evaluation needs grounding tests for open-ended reports, longitudinal comparisons, uncertainty handling, and real clinician workflows. The field also needs methods that train models to make visual dependence explicit rather than only auditing after the fact.

### 11. What future work naturally follows?
Extend the intervention suite to multi-finding report generation, region-specific rationales, and clinical decision support. Another useful follow-up would test whether training on counterfactual or masked radiograph tasks improves causal grounding without destroying performance.

### 12. Why does this matter for cabbageland?
The paper is a clean example of mechanism-first evaluation. Cabbageland agents should be tested the same way: if a system claims to use a memory, source, tool, or image, intervene on that channel and see whether the answer changes appropriately. Correctness without causal dependence is not the behavior we want.

### 13. What ideas are steal-worthy?
Always include a no-input or wrong-input baseline when evaluating multimodal or tool-grounded systems. Use targeted and irrelevant interventions as a pair. Separate accuracy from grounding, confidence from grounding, and stable answers from justified answers.

### 14. Final decision
Preserve. This is one of the better evaluation papers because it replaces surface performance with a direct test of whether the claimed evidence channel mattered.
