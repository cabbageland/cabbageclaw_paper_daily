# MIRTO: a registration-gated, multiverse-tested evaluation protocol for unsupervised anomaly segmentation in brain MRI

## Basic info

* Title: MIRTO: a registration-gated, multiverse-tested evaluation protocol for unsupervised anomaly segmentation in brain MRI
* Authors: Negin Kafee Hernashki, Soumick Chatterjee
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2610.02136
* Date surfaced: 2026-10-04
* Why selected in one sentence: It shows how medical anomaly-segmentation conclusions can be artifacts of registration, threshold transfer, lesion definition, and metric choice rather than model quality.

## Quick verdict

Highly relevant.

This is a strong evaluation paper, not because it introduces a new segmenter, but because it makes hidden leaderboard choices explicit and quantifies their consequences. The paper is especially useful for cabbageland because it treats evaluation as a structured system with failure modes, not as a neutral scoreboard.

## One-paragraph overview

MIRTO evaluates unsupervised anomaly detection for brain MRI by freezing model outputs and varying the evaluation pipeline rather than the models. It maps anomaly maps to a canonical grid, checks registration with label-free diagnostics, chooses thresholds on validation data or conformal calibration rather than the test set, reports realised false-positive burden, and runs conclusions through a multiverse of defensible choices. Applied to four UAD methods on 312 BraTS 2020 subjects, it finds that a mapping error can drop voxel AUROC from 0.873 to 0.583 while slice-level AUROC barely moves; Dice advantages at validation thresholds can disappear at equal realised false-positive burden; and lesion sensitivity can be driven more by lesion definition and hit criteria than by method. The limitation is that the evidence is exploratory on one cohort, but the protocol is a valuable template.

## Model definition

### Inputs

MIRTO takes stored anomaly maps from UAD methods, subject brain masks, binary tumour references, validation subjects, test subjects, registration transforms, threshold grids, post-processing choices, lesion definitions, hit criteria, aggregation choices, and metric choices. The four evaluated methods were trained separately on healthy MRI data.

### Outputs

The protocol outputs metric tables, registration-gate decisions, realised false-positive burden distributions, threshold-transfer decompositions, multiverse ranking curves, paired bootstrap intervals, and hypothesis verdicts. It does not output a new segmentation model.

### Training objective (loss)

MIRTO itself has no trainable objective. It evaluates existing UAD methods and leaves their architectures and losses unchanged. The paper briefly describes evaluated models such as REFLECT, cDDPM, UCCD, and AnomalyDINO, but the contribution is the evaluation protocol.

### Architecture / parameterization

The method is an evaluation pipeline: canonical voxel mapping, registration gating, validation/conformal/test-matched thresholding, post-processing variants, multiverse axes, paired subject-bootstrap intervals, and multiplicity control.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It asks why UAD brain MRI papers can report clean single-number rankings when the score depends on unreported evaluation choices: spatial alignment, threshold selection, false-positive budget, metric aggregation, lesion definition, and hit criterion.

### 2. What is the method?

MIRTO gates the geometry of each comparison with registration diagnostics, normalizes and thresholds anomaly maps on a grid, selects thresholds on validation data or via conformal calibration, reports realised false-positive burden on test, decomposes threshold-transfer effects, and evaluates conclusions across 15,552 defensible pipeline choices.

### 3. What is the method motivation?

Medical segmentation evaluation is brittle because small spatial or threshold choices can change the clinical meaning of a result. MIRTO makes those choices explicit so a model ranking cannot silently depend on a favorable threshold, a broken registration, or a convenient lesion definition.

### 4. What data does it use?

The main test cohort is 312 BraTS 2020 subjects, with a disjoint validation set of 24 subjects. Methods are trained on healthy data, including IXI-HH+Guys as the main common training setup. The labels are whole-tumour references on T2 MRI.

### 5. How is it evaluated?

It evaluates voxel AUROC, voxel AUPRC, Dice, lesion sensitivity, slice-level AUROC, and related metrics under a multiverse of choices. The full factorial has 155,520 universes per method; the defensible subset fixes canonical reference and true voxel volume and uses 15,552 universes. Intervals are paired subject-bootstrap intervals with multiplicity correction.

### 6. What are the main results?

A wrong axis/crop mapping for cDDPM gives voxel AUROC 0.583; correcting it raises voxel AUROC to 0.873, AUPRC by 0.535, and Dice by 0.520, while slice-max AUROC moves far less. A similar REFLECT export error leaves 26% of test subjects anti-located and drops voxel AUROC from 0.936 to 0.616 while slice AUROC stays 0.915. Within metrics, the method explains at least 0.95 of variance for voxel AUROC and AUPRC and 0.77 for Dice, but only 0.14 for lesion sensitivity. Some Dice advantages at validation thresholds vanish at equal realised false-positive burden, exposing threshold-transfer artifacts.

### 7. What is actually novel?

The novelty is the combination of registration gating, threshold-transfer identities, conformal burden control, and multiverse evaluation for UAD segmentation. The paper's contribution is a disciplined evaluation contract, not a model.

### 8. What are the strengths?

The strongest part is that MIRTO catches errors that common reported metrics can miss. It also gives exact identities for why contrasts change between validation thresholds and matched burden. The recommendations are practical: one reference grid, registration checks, non-test thresholds, realised burden distributions, subject mean/median/pooled Dice, full lesion definitions, paired intervals, and multiplicity correction.

### 9. What are the weaknesses, limitations, or red flags?

The study uses one cohort and one broad pathology type with large visible lesions. The 312 test subjects helped develop the protocol, so inference is exploratory. It has one trained model per method/training set, so seed variance is unknown. Validation-threshold intervals do not include threshold-fitting uncertainty from the 24-subject validation set.

### 10. What challenges or open problems remain?

The main next step is a preregistered confirmatory evaluation on an untouched cohort, with fixed training sets, fixed threshold rules, multiple seeds, and pathologies with smaller subtler lesions.

### 11. What future work naturally follows?

This protocol should be wrapped around other medical imaging benchmarks, especially those where thresholding, calibration, and registration choices are underreported. A broader version could include nested resampling of threshold fitting and multiple independent cohorts.

### 12. Why does this matter for cabbageland?

Cabbageland cares about evaluation that actually tests mechanisms. MIRTO is a good example of turning "leaderboard uncertainty" into explicit axes that can be measured, stress-tested, and reported.

### 13. What ideas are steal-worthy?

The steal-worthy idea is the multiverse evaluation: define the defensible axes, run the conclusion across them, and report both how often rankings flip and how large the differences are. The registration-gate pattern is also broadly useful for any spatial benchmark.

### 14. Final decision

Preserve. This is a high-value reference for evaluation design, medical AI benchmarking, and the difference between model performance and evaluation artifacts.
