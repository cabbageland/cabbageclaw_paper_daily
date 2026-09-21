# Beyond Benchmark Scores: Auditing Medical Vision-Language Models for Chest X-Ray Tuberculosis Screening

## Basic info

* Title: Beyond Benchmark Scores: Auditing Medical Vision-Language Models for Chest X-Ray Tuberculosis Screening
* Authors: Mushir Akhtar, M. Tanveer, Mohd. Arshad
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2609.21763
* Date surfaced: 2026-09-21
* Why selected in one sentence: It shows that medical VLM screening claims only make sense relative to a complete evaluation specification.

## Quick verdict

* Highly relevant

This is not a new model paper; it is a serious audit of evaluation portability. The useful lesson is that prompt, cohort, negative spectrum, prevalence, threshold, and metric each carry a different claim. A checkpoint-level benchmark score is too coarse for clinical screening.

## One-paragraph overview

The paper audits OpenCLIP, BioMedCLIP, CheXficient, and MedSigLIP on chest X-ray tuberculosis screening across Montgomery, Shenzhen, TBX11K, and VinDr-CXR. It fixes five prompt families and evaluates 244,000 model-image-prompt scores over 12,200 records. The audit shows that model ranking, AUROC, score reliability, and threshold transport all change under evaluation-specification shifts. Healthy controls make the task look easier than sick non-TB controls; named VinDr diagnoses can invert medical VLM rankings; and thresholds chosen for 95% source sensitivity rarely retain that sensitivity elsewhere. A supervised TBX11K source model also fails to transfer cleanly to external cohorts.

## Model definition

### Inputs

The VLMs receive chest radiograph images and text prompts describing TB-positive and non-TB classes. The supervised transfer baseline receives chest radiographs with TB labels from TBX11K.

### Outputs

The VLMs output image-text similarity scores used as TB screening scores. The supervised ResNet outputs TB classification scores.

### Training objective (loss)

The audited VLM checkpoints are frozen and not retrained in the paper. The supervised baseline trains a ResNet-50 with weighted cross-entropy on TBX11K training data.

### Architecture / parameterization

The audited models are OpenCLIP, BioMedCLIP, CheXficient, and MedSigLIP. The supervised baseline is a ResNet-50 trained over five seeds with source validation checkpoint selection.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It asks whether medical VLM screening conclusions survive changes in prompt, cohort, negative class, prevalence, operating threshold, and reliability criterion.

### 2. What is the method?

The method is an audit framework that represents an evaluation as a tuple containing checkpoint, prompt, cohort, negative class definition, prevalence, threshold, and metric. It then changes one or more parts of that tuple and measures whether the claim survives.

### 3. What is the method motivation?

Medical VLMs make zero-shot reuse tempting, but a checkpoint does not define a classifier by itself. The prompt, controls, prevalence, and threshold all participate in the clinical claim.

### 4. What data does it use?

It uses 12,200 chest radiograph records from Montgomery, Shenzhen, TBX11K training/validation, and VinDr-CXR test. VinDr-CXR supplies named negative groups such as no finding, pneumonia, and lung tumor.

### 5. How is it evaluated?

The paper evaluates AUROC, AUPRC, Brier score, ECE15, AURC, within-cohort operating points, prevalence-standardized reliability, and threshold transport. It uses image-level bootstrap, paired comparisons, and correction procedures for prompt and negative-spectrum tests.

### 6. What are the main results?

Prompt-family changes alter AUROC in 21 of 48 primary controlled comparisons. Replacing healthy controls with sick non-TB controls reduces AUROC by 0.140 for CheXficient, 0.306 for MedSigLIP, 0.261 for BioMedCLIP, and 0.075 for OpenCLIP. TBX11K thresholds selected for 95% sensitivity retain that point-estimate sensitivity in only four of sixteen target transports. A five-seed supervised source model reaches 0.999 AUROC on TBX11K validation but only 0.629 on Shenzhen and 0.629 on Montgomery.

### 7. What is actually novel?

The novelty is the evaluation-specification framing and the systematic stress tests. The paper is valuable because it refuses to collapse discrimination, reliability, and threshold portability into one benchmark score.

### 8. What are the strengths?

The audit is concrete and well scoped. It uses multiple models, prompt families, cohorts, negative spectra, and threshold-transport tests, and it marks CheXficient's documented VinDr-CXR pretraining exposure.

### 9. What are the weaknesses, limitations, or red flags?

The study is retrospective and single-task. It relies on dataset labels rather than a harmonized microbiological reference standard. VinDr-CXR labels are radiographic disease impressions, not prospective diagnostic ground truth.

### 10. What challenges or open problems remain?

The larger problem is how to design prospective local validation for medical VLMs when prompt choice, negative spectrum, and prevalence are all part of the deployment contract.

### 11. What future work naturally follows?

A useful follow-up would evaluate calibration and threshold transport prospectively at a new site with fixed prompts and prespecified negative classes.

### 12. Why does this matter for cabbageland?

It is a clean warning against benchmark portability theater. Any system that claims medical, safety, or high-stakes reliability needs to state the whole evaluation specification.

### 13. What ideas are steal-worthy?

Steal the evaluation tuple: model, prompt, cohort, negative class, prevalence, threshold, metric. It is a good general template for refusing vague benchmark claims.

### 14. Final decision

Preserve. It is a strong evaluation paper and a useful antidote to checkpoint-level claims.
