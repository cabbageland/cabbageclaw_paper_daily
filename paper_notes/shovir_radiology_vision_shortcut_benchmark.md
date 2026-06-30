# SHOVIR: A Benchmark for Evaluating Vision Shortcut Learning in Radiology Report Generation

## Basic info

* Title: SHOVIR: A Benchmark for Evaluating Vision Shortcut Learning in Radiology Report Generation
* Authors: Filippo Ruffini, Marco Salme, Rosa Sicilia, Valerio Guarrasi, and Paolo Soda
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.30201
* Date surfaced: 2026-06-30
* Why selected in one sentence: It gives medical VLM evaluation a region-level shortcut test instead of letting fluent radiology prose masquerade as visual grounding.

## Quick verdict

**Highly relevant**

This is a strong evaluation paper. The contribution is not a new radiology VLM; it is a benchmark that asks whether diagnostic statements actually depend on the image regions where the pathology is visible. I inspected the full arXiv PDF's benchmark construction, metrics, model list, results, and conclusion; confidence is high on the protocol and main findings, with caution around occlusion as a causal instrument.

## One-paragraph overview

SHOVIR evaluates vision shortcut learning in radiology report generation. The benchmark extends MIMIC-CXR plus ChestImaGenome and PadChest-GR with per-box CheXpert labels, then tests radiology VLMs under full-image noise, random occlusion, target disease-region occlusion, and co-disease-region occlusion. This lets the authors distinguish global visual reliance, direct pathology grounding, and contextual shortcut use. Across eight evaluated VLMs, the paper finds that high report-level quality does not guarantee faithful spatial grounding: some models keep generating plausible diagnoses even when relevant visual evidence is removed, or they degrade when co-occurring disease regions are removed while the target pathology remains visible.

## Model definition

SHOVIR is a benchmark rather than a new trainable model. The evaluated systems are existing radiology report generation VLMs.

### Inputs
Inputs are frontal chest radiographs from MIMIC-CXR and PadChest-GR, with associated reports, image-level CheXpert labels, and pathology bounding boxes mapped to per-box CheXpert labels. Perturbed variants include full-image noise, random-box occlusion, object-class occlusion, and different-object-class occlusion.

### Outputs
Evaluated VLMs output free-text radiology reports. The benchmark extracts clinical labels and graph/semantic metrics from those reports, then measures performance changes under perturbation.

### Training objective (loss)
SHOVIR does not train a new model. It defines evaluation metrics, including report-level metrics and shortcut deltas: full-noise drop, object-class-occlusion drop, and different-object-class-occlusion drop.

### Architecture / parameterization
The benchmark evaluates eight VLMs under their default inference configurations: CheXagent-2, CXRMate, Libra-v1, LLaVA-Rad, MAIRA-2, MedGemma, RaDialog, and NV-Reason-CXR. The benchmark itself is an occlusion-based evaluation protocol grounded in spatial annotations.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Radiology report generation metrics usually score lexical overlap or aggregate clinical correctness. They do not test whether a generated diagnostic statement came from the visible image evidence for that pathology. A model can sound clinically fluent while relying on priors, co-occurrence patterns, or report templates.

### 2. What is the method?
SHOVIR builds spatially grounded evaluation sets by attaching CheXpert disease labels to pathology boxes. It then runs controlled perturbations: replace the whole image with noise, occlude random regions, occlude the target disease boxes, or occlude boxes for co-occurring diseases while leaving the target box visible. The model's report quality and disease-level F1 changes reveal whether predictions depend on the intended evidence.

### 3. What is the method motivation?
If a model genuinely uses the visual evidence for a diagnosis, removing that region should hurt that diagnosis. If removing unrelated co-disease regions hurts the target diagnosis, the model is probably leaning on contextual shortcuts. If full-image noise barely hurts, the model may be getting too much from priors or low-level dataset statistics.

### 4. What data does it use?
The benchmark uses MIMIC-CXR with ChestImaGenome spatial annotations and PadChest-GR. The authors map bounding-box labels into CheXpert classes and apply conservative filtering. The final sets include thousands of images with reports, image labels, and region-level labels; PadChest-GR has fewer usable regions after mapping and filtering.

### 5. How is it evaluated?
The evaluation uses NLP metrics such as BLEU/ROUGE, clinical metrics such as F1-CheXbert, F1-RadGraph, and GREEN, and shortcut metrics based on performance drops under full noise, object-class occlusion, and different-object-class occlusion. Disease-level evaluation uses weighted mu-F1 over classes.

### 6. What are the main results?
All models show some drop when the whole image is replaced with noise, so they use visual signal to some extent. But sensitivity varies widely. CheXagent-2, MedGemma, and MAIRA-2 show large full-noise drops on MIMIC-CXR, while LLaVA-Rad is comparatively insensitive. Disease-level occlusion reveals sharper differences: CheXagent-2 has strong spatial grounding in the reported deltas, while models with strong baseline report quality can rank poorly on object-class-occlusion sensitivity. Co-disease occlusion also exposes contextual shortcut use.

### 7. What is actually novel?
The novelty is the region-level shortcut protocol for free-text radiology reports. It does not merely ask whether the report is clinically correct; it asks whether the disease-specific text depends on the disease-specific image evidence.

### 8. What are the strengths?
The benchmark is pointed at a real deployment failure. It uses two datasets, multiple perturbation conditions, and multiple metric families. The random-occlusion control is important because it distinguishes "area was removed" from "diagnostic evidence was removed." The direct-versus-contextual shortcut split is especially useful.

### 9. What are the weaknesses, limitations, or red flags?
Occlusion is a blunt intervention. Noise may introduce artifacts, and removing boxes is not the same as generating a plausible counterfactual patient without the pathology. The box-label mapping and filtering are conservative but still rule-based. The benchmark tests frontal radiographs and selected localizable CheXpert conditions, not the full clinical report generation problem.

### 10. What challenges or open problems remain?
Stronger causal evaluation needs counterfactual image generation or clinically validated edits, not only occlusion. Another open problem is localizing where shortcut behavior arises inside the model: visual encoder, projector, language decoder, or decoding prior. Human radiologist auditing of the perturbation effects would also strengthen the benchmark.

### 11. What future work naturally follows?
Extend SHOVIR-style evaluation to other medical imaging modalities, use counterfactual generation for pathology removal, trace visual-token dependence inside VLMs, and train models with region-grounded objectives that optimize for target-region sensitivity and co-disease independence.

### 12. Why does this matter for cabbageland?
It is a clean example of evaluation that refuses to average away the relevant failure. For any multimodal agent, the question should be: did the output depend on the exact evidence it claims to use?

### 13. What ideas are steal-worthy?
* Measure output change under targeted removal of claimed evidence.
* Include random perturbation controls so "occlusion hurts" is not overread.
* Separate direct visual grounding from contextual shortcut reliance.
* Compare baseline quality against grounding quality; do not assume they track.
* Build metrics around the failure the deployment actually cares about.

### 14. Final decision
**Keep as a strong evaluation reference.** It is not a perfect causal instrument, but it makes the right demand: clinical language must be visually accountable.
