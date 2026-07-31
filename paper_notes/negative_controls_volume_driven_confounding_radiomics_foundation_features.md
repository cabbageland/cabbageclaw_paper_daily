# Negative controls reveal volume-driven confounding in radiomics and imaging foundation model features

## Basic info

* Title: Negative controls reveal volume-driven confounding in radiomics and imaging foundation model features
* Authors: Katy L. Scott, Sejin Kim, Joshua Siraj, Caryn Geady, Matthew Boccalon, Mattea Welch, Mogtaba Alim, Andrew J. Hope, Benjamin Haibe-Kains
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.28423
* Date surfaced: 2026-07-31
* Why selected in one sentence: It uses volume-preserving negative controls to test whether predictive imaging features still work after the supposed spatial signal is destroyed, which is exactly the right embarrassment test.

## Quick verdict

**Highly relevant**

This is a strong evaluation-and-quality-control paper rather than a new model paper, and that is exactly why it matters. I inspected the full arXiv PDF, especially the introduction, negative-control design, multi-cohort results, reproduced survival and HPV signatures, discussion, and methods around READII-2-ROQC. The main caveat is that the paper diagnoses confounding but does not solve the entire upstream reproducibility stack, especially acquisition, reconstruction, and segmentation variability.

## One-paragraph overview

The paper introduces READII-2-ROQC, a modular pipeline for stress-testing radiomic and imaging-foundation-model features with volume-preserving negative controls. For each image-mask pair, the pipeline generates voxel-perturbed controls that selectively destroy spatial structure in the ROI, the whole image, or background regions while preserving geometry. It then compares extracted features and downstream signature behavior between original and perturbed images. Across three public cancer imaging cohorts and 3,552 tumor volumes, the paper shows that several published radiomic signatures retain predictive performance after meaningful spatial structure is destroyed, implying that they are largely volume-driven or context-driven rather than capturing true biological texture. The analysis also suggests that FMCIB deep features often draw signal from tumor boundary or surrounding background rather than the tumor interior.

## Model definition

### Inputs
The pipeline takes medical images, segmentation masks, clinical labels, and a set of negative-control perturbation configurations that target ROI, whole-image, background, and related regions.

### Outputs
The outputs are radiomic and deep feature sets, perturbation-sensitivity analyses, reproduced signature scores, and comparisons against volume-only baselines for survival or classification tasks.

### Training objective (loss)
The paper does not introduce a new trainable model. The main contribution is the READII-2-ROQC quality-control pipeline. Existing feature extractors such as PyRadiomics and the external FMCIB foundation model are used as components, and reproduced radiomic signatures are evaluated rather than newly trained as the paper's core contribution.

### Architecture / parameterization
This is a modular analysis pipeline: negative-control generation, feature extraction with PyRadiomics and FMCIB, correlation and perturbation analysis, and downstream evaluation of published survival and HPV-status signatures against volume baselines.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to determine whether radiomic and deep imaging signatures are actually capturing biologically meaningful spatial signal, or whether they are mostly riding on easier confounds such as tumor volume or background context.

### 2. What is the method?
The method is to generate structured volume-preserving negative controls by perturbing voxel values while keeping geometry fixed, then compare features and downstream predictive performance between original and perturbed images.

### 3. What is the method motivation?
A predictive signature is easy to overinterpret. If destroying texture while preserving volume leaves the prediction mostly intact, the feature may be a proxy for geometry or context rather than a real biomarker.

### 4. What data does it use?
The pipeline is applied across three public cancer imaging cohorts, processing 3,552 tumor volumes. It extracts PyRadiomics features and 4,096 FMCIB deep features, and reproduces previously published survival and HPV-status radiomic signatures.

### 5. How is it evaluated?
It is evaluated through feature-correlation analyses across original and perturbed images, volume-dependence analysis, reproduction of published radiomic signatures on both original and control images, and comparison against volume-only baselines for survival and HPV prediction.

### 6. What are the main results?
Multiple radiomic survival signatures retain performance after spatial structure is destroyed, revealing volume-driven or contextual confounding. The Aerts survival signature performs comparably to a volume-only model and stays robust to all perturbations, which is exactly the wrong kind of robustness. The Choi survival signature underperforms the volume baseline in this reproduction. The Choi HPV signature does better than volume on original images but degrades under certain full-image and background perturbations, suggesting a more meaningful but still not purely intratumoral signal. FMCIB features often appear to derive signal from tumor boundaries or surrounding background rather than the tumor interior.

### 7. What is actually novel?
The novelty is not just voxel shuffling. The paper extends the negative-control idea into a reusable quality-control framework with multiple region-specific perturbations, applies it across radiomics and imaging foundation features, and treats perturbation sensitivity as a criterion for biological plausibility.

### 8. What are the strengths?
The paper asks the right falsification question. It is open-source, multi-cohort, and concrete about what breaks. It also goes beyond correlation filtering, showing that conventional feature-screening shortcuts are not enough to remove volume confounding.

### 9. What are the weaknesses, limitations, or red flags?
The framework diagnoses a major confound but does not address all upstream sources of instability, including acquisition, reconstruction, and segmentation variability. The perturbation family is strong but still limited, and the paper does not establish clinical validity directly.

### 10. What challenges or open problems remain?
The main open problem is extending this kind of quality control to more modalities, more realistic perturbations, peritumoral analyses, and settings where radiogenomic interpretation matters. Another is integrating these checks earlier in pipeline design rather than only as a retrospective audit.

### 11. What future work naturally follows?
Future work should incorporate peritumoral region analysis, radiogenomic datasets, modality-specific perturbations, and broader reporting standards for perturbation-sensitive biomarker validation.

### 12. Why does this matter for cabbageland?
It matters because cabbageland cares about mechanism over proxy theater. This paper is a reminder that if a model or feature claims to capture structure, you should try to destroy that structure while preserving the confound and see what survives.

### 13. What ideas are steal-worthy?
Use negative controls that preserve the suspected confound while damaging the claimed signal. Treat perturbation sensitivity as a validity test, not just a nice-to-have explainability add-on. Compare sophisticated features against brutally simple baselines like volume before narrating biology.

### 14. Final decision
**Keep it.** This is exactly the kind of anti-self-deception paper that improves research taste, even outside medical imaging.
