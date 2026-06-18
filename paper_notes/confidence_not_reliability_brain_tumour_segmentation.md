# Confidence is Not Reliability: Rethinking MC Dropout in Brain Tumour Segmentation

## Basic info

* Title: Confidence is Not Reliability: Rethinking MC Dropout in Brain Tumour Segmentation
* Authors: Xin Ci Wong, Duygu Sarikaya, Kieran Zucker, Marc de Kamps, Nishant Ravikumar
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.19300
* Date surfaced: 2026-06-18
* Why selected in one sentence: It shows that high uncertainty-error AUROC can hide clinically unsafe sub-region calibration failures in brain-tumour segmentation.

## Quick verdict

* Highly relevant

This is a compact but useful medical reliability paper. Its value is not that MC Dropout works or fails globally; it shows exactly how a reassuring aggregate uncertainty metric can mask overconfident errors in the treatment-critical enhancing-tumour region. I inspected the full PDF, including the data split, model setup, uncertainty metrics, segmentation results, calibration analysis, triage analysis, discussion, and limitations.

## One-paragraph overview

The paper evaluates MC Dropout uncertainty for glioma segmentation on BraTS21 using a pretrained SegResNet and a locally trained UNet-Res. Both models achieve strong voxel-level uncertainty-error AUROC, meaning uncertain voxels tend to rank above correct voxels. But this ranking success does not guarantee usable reliability. UNet-Res is badly miscalibrated on enhancing tumour: it has near-zero entropy, high expected calibration error, and low Dice on the sub-region most tied to treatment response and biopsy targeting. The paper's main message is that clinical uncertainty evaluation must include sub-region calibration and patient-level triage behavior, not just Dice and global AUROC.

## Model definition

### Inputs
Inputs are multiparametric brain MRI volumes from BraTS21, including T1, T1ce, T2, and FLAIR modalities after standard preprocessing. The models receive cropped 3D volumes. MC Dropout inference uses 20 stochastic forward passes per patient, with dropout active and normalization layers kept in evaluation mode.

### Outputs
The segmentation models output tumour sub-region predictions for whole tumour, tumour core, and enhancing tumour. The uncertainty pipeline outputs predictive entropy, expected entropy, mutual information, AUROC for uncertainty-error ranking, expected calibration error, reliability diagrams, and patient-level entropy strata for triage.

### Training objective (loss)
The paper does not introduce a new training objective. It evaluates a pretrained MONAI SegResNet and a locally trained residual UNet baseline. The exact UNet-Res training loss is not specified in the accessible main text I inspected, so I am not inferring it. The key evaluated procedure is inference-time MC Dropout plus uncertainty and calibration measurement.

### Architecture / parameterization
The evaluated architectures are a pretrained 3D SegResNet from the MONAI model zoo and a custom 3D UNet with residual units. SegResNet uses post-hoc dropout injection at inference, while UNet-Res uses dropout present during training. Both are evaluated on the same 126-patient BraTS21 test split.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Brain-tumour segmentation metrics such as Dice can look strong while missing clinically critical failure modes. Uncertainty metrics are supposed to flag risky predictions, but global uncertainty-error alignment may still miss sub-region-specific overconfidence. The paper asks whether MC Dropout uncertainty is reliable enough for clinically meaningful review and triage.

### 2. What is the method?
The authors run deterministic and MC Dropout inference for SegResNet and UNet-Res on BraTS21. They compute segmentation Dice, voxel-level uncertainty via entropy and mutual information, AUROC for uncertainty-error alignment, expected calibration error on foreground-relevant voxels, reliability diagrams by tumour sub-region, and patient-level entropy quartiles.

### 3. What is the method motivation?
AUROC answers a ranking question: do erroneous voxels tend to have higher uncertainty than correct voxels? Clinical deployment also needs a calibration question: does the predicted confidence mean anything for the specific region where a mistake changes care? Those are not the same question, especially under class imbalance and small critical sub-regions.

### 4. What data does it use?
The paper uses BraTS21 with 1,251 labelled pre-operative multiparametric MRI cases, split into 1,000 training, 125 validation, and 126 test patients with patient-level disjoint splits. The images are skull-stripped, atlas-registered, resampled to 1 mm isotropic resolution, normalized per modality over non-zero brain voxels, and center-cropped to 128 cubed voxels.

### 5. How is it evaluated?
Segmentation is evaluated with Dice for whole tumour, tumour core, and enhancing tumour. Uncertainty quality is evaluated with entropy and mutual information AUROC against voxel-level errors. Calibration is evaluated with expected calibration error and reliability diagrams over foreground-relevant voxels. Triage utility is evaluated by stratifying patients into entropy quartiles and comparing segmentation performance.

### 6. What are the main results?
MC Dropout changes Dice by less than 0.01 relative to deterministic inference, so stochastic inference does not materially harm segmentation accuracy. Both models achieve high uncertainty-error AUROC: roughly 0.977 for SegResNet entropy and 0.975 for UNet-Res entropy. But UNet-Res has a severe enhancing-tumour calibration failure: ET entropy is about 0.054, ECE is 0.915, and ET Dice is only about 0.714. Patients with greater than 40% ET Dice error are not meaningfully more uncertain than good cases under UNet-Res. For SegResNet, high-entropy patients have worse whole-tumour Dice, with median WT Dice about 0.835 in the highest-uncertainty quartile versus 0.925 in the lowest, making entropy more useful as a triage signal.

### 7. What is actually novel?
The novelty is the sub-region calibration argument. The paper is not merely "MC Dropout for segmentation." It shows that a strong global ranking metric can coexist with a clinically invalid confidence signal in a specific tumour compartment. That distinction is the useful contribution.

### 8. What are the strengths?
The evaluation targets a deployment-relevant failure. It separates Dice, AUROC ranking, calibration, entropy magnitude, and patient-level triage. It also compares a strong pretrained architecture with a weaker locally trained model, making clear that uncertainty behavior depends on architecture and training regime, not just on the MC Dropout wrapper.

### 9. What are the weaknesses, limitations, or red flags?
The study uses a single public dataset with consensus labels, so the exact numbers should not be treated as deployment-general. SegResNet uses post-hoc dropout injection while UNet-Res has embedded dropout, which makes the architectures not perfectly comparable. The paper does not test sensitivity to the number of MC passes. It also does not include prospective reader studies, subgroup calibration, or multi-site clinical validation.

### 10. What challenges or open problems remain?
The field still needs uncertainty methods that are calibrated at the region and patient level, not just rank-correlated with errors. Another open problem is turning uncertainty overlays into measurable improvements in clinician workflow without increasing false reassurance or alert fatigue.

### 11. What future work naturally follows?
A strong follow-up would repeat the analysis across multiple sites, additional segmentation backbones, deep ensembles, test-time augmentation, conformal methods, and calibrated post-processing. Prospective reader studies should measure whether uncertainty-guided review improves surgical or treatment-planning decisions.

### 12. Why does this matter for cabbageland?
The paper is a clean warning against metric comfort. If a system claims uncertainty, memory, grounding, or source reliability, the evaluation must ask whether the signal works in the slice where failure matters. A strong average score can still be the wrong safety property.

### 13. What ideas are steal-worthy?
Always separate ranking from calibration. Report behavior by critical sub-region, not only globally. Convert voxel-level or token-level uncertainty into patient-level or task-level triage signals. Treat a high AUROC as necessary but not sufficient for trust.

### 14. Final decision
Preserve. This is a useful medical AI reliability paper and a reusable evaluation lesson for any system where confidence is supposed to guide human review.
