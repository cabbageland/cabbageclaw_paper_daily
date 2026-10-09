# Missing Modality-Aware Calibration for Trustworthy Brain Tumor Segmentation

## Basic info

* Title: Missing Modality-Aware Calibration for Trustworthy Brain Tumor Segmentation
* Authors: Sol Lee, Hyunji Kim, Sungrae Hong, Donghee Han, Mun Yi
* Year: 2026
* Venue / source: arXiv preprint; MICCAI 2026 poster
* Link: https://arxiv.org/abs/2610.11419
* Date surfaced: 2026-10-09
* Why selected in one sentence: It calibrates missing-modality MRI segmentation with a local, modality-aware temperature field rather than pretending one global confidence correction fits every evidence pattern.

## Quick verdict

* Highly relevant

This is a useful deployment-facing calibration paper. It is narrow, but the narrowness is a virtue: missing MRI modalities create combination-specific and spatially heterogeneous calibration errors, and the paper targets exactly that. The main caveat is that the evidence is still limited to ECE-style calibration on brain tumor segmentation benchmarks, with residual boundary overconfidence.

## One-paragraph overview

Multimodal brain tumor segmentation models often retain Dice performance when some MRI modalities are missing, but their confidence estimates can become badly miscalibrated. MMA-LTS is a post-hoc calibration module that keeps the segmentation backbone frozen and learns a voxel-wise temperature field. The temperature estimator uses spatial features and logits from the backbone, a voxel-wise difficulty score based on Mahalanobis feature distances, and a learnable token encoding which MRI modalities are available or missing. The calibrated probabilities are produced by applying local temperature scaling to the frozen model's logits, preserving class ordering and segmentation accuracy while reducing expected calibration error across missing-modality combinations.

## Model definition

### Inputs

The module receives a pretrained segmentation model's logits, its joint spatial feature representation, and the current modality availability pattern over FLAIR, T1, T1ce, and T2 MRI. It also uses class-conditional and class-agnostic feature statistics estimated from training voxels to compute voxel difficulty.

### Outputs

MMA-LTS outputs a voxel-wise temperature field over the 3D volume. Applying that field to the frozen logits yields calibrated voxel-wise class probabilities for tumor subregions.

### Training objective (loss)

The calibration module is trained on a validation split with voxel-wise negative log-likelihood after temperature-scaled softmax. The frozen segmentation backbone is not retrained. Modality dropout is used during calibration training.

### Architecture / parameterization

The method uses a 3D CNN spatial encoder over concatenated features and logits, a voxel-wise difficulty gate, learnable available/missing modality tokens, FiLM-style affine modulation from the modality token, and a 3D CNN predictor for the temperature field. Temperature values greater than one reduce overconfidence; values below one correct underconfidence.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It addresses confidence miscalibration in brain tumor segmentation when clinical MRI inputs are incomplete. Accuracy may remain high, but confidence can become unreliable depending on exactly which modality is absent and where the voxel lies.

### 2. What is the method?

Compute a voxel-wise difficulty score from Mahalanobis distances in backbone feature space, encode the availability or absence of each modality with learnable tokens, use those signals to predict a spatially adaptive temperature field, and post-hoc rescale the frozen model's logits.

### 3. What is the method motivation?

Missing-modality difficulty is not monotonic in the number of available modalities. Which modality is missing matters, and difficult regions are spatially localized. A global temperature or count-based missingness signal cannot express that.

### 4. What data does it use?

Experiments use BraTS 2020 and FeTS 2024, both with four MRI modalities and three tumor regions: whole tumor, tumor core, and enhancing tumor. BraTS 2020 has 369 cases split into 219 training, 50 validation, and 100 test cases; FeTS 2024 has 1,251 cases split into 1000, 125, and 126.

### 5. How is it evaluated?

The paper evaluates segmentation with Dice similarity coefficient and calibration with foreground-voxel ECE using 10 bins, averaged across test volumes. It tests three missing-modality segmentation backbones: RobustSeg, mmFormer, and DC-Seg. Baselines include mL1-ACE, SDC, MC Dropout, temperature scaling, Dirichlet scaling, local temperature scaling, and selective scaling.

### 6. What are the main results?

On DC-Seg with BraTS 2020, MMA-LTS reduces average WT/TC/ET ECE to 10.2/14.5/15.1, beating the strongest local temperature baseline at 13.1/16.8/16.5 while preserving DSC. On FeTS 2024, it reaches 9.5/12.0/11.6. The gains are consistent across RobustSeg and mmFormer as well. Ablations show that removing the voxel difficulty score or the modality availability token degrades ECE.

### 7. What is actually novel?

The novelty is the combination of modality-combination conditioning and voxel-wise difficulty gating for post-hoc local temperature scaling under missing MRI modalities. It is not a new segmentation backbone.

### 8. What are the strengths?

The paper targets a real clinical reliability gap, keeps the backbone frozen, preserves segmentation accuracy, and tests multiple backbones and missing-modality combinations. The component ablations support the core claim that both spatial difficulty and modality identity matter.

### 9. What are the weaknesses, limitations, or red flags?

The evaluation is centered on ECE, which is useful but not the whole story of clinical reliability. The paper reports residual overconfidence near tumor boundaries. It is also limited to brain tumor MRI datasets, so generalization to other anatomies, scanners, and modality sets remains unproven.

### 10. What challenges or open problems remain?

The method needs broader validation under real hospital acquisition patterns, out-of-site shift, and decision-relevant uncertainty metrics. It would also be useful to connect the calibration map to abstention, triage, or human review policies.

### 11. What future work naturally follows?

Extend the method to other anatomical domains, include reliability metrics beyond ECE, test under prospective missingness patterns, and integrate calibrated confidence into downstream clinical workflows such as review prioritization or uncertainty-aware segmentation editing.

### 12. Why does this matter for cabbageland?

Cabbageland cares about uncertainty that is tied to the actual source of uncertainty. MMA-LTS is a clean example: missing evidence is represented explicitly, local difficulty is measured, and confidence is corrected where those factors bite.

### 13. What ideas are steal-worthy?

Use modality identity, not just modality count. Gate calibration by local feature difficulty. Keep post-hoc calibration lightweight when the prediction backbone is already strong. Preserve class ordering when the goal is confidence correction rather than segmentation refinement.

### 14. Final decision

Preserve. It is a narrow paper, but the mechanism is practical and the calibration framing is useful.
