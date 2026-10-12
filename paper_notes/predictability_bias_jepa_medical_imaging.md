# The Predictability Bias of Joint-Embedding Predictive Learning in Medical Imaging

## Basic info

* Title: The Predictability Bias of Joint-Embedding Predictive Learning in Medical Imaging
* Authors: Fabian Drexel, Bernhard Kainz, Jakob N. Kather, Daniel Rueckert, Lisa C. Adams, Keno K. Bressem, Cosmin I. Bercea
* Year: 2026
* Venue / source: arXiv preprint
* Link: https://arxiv.org/abs/2610.13237
* Date surfaced: 2026-10-12
* Why selected in one sentence: It shows that JEPA-style predictive pretraining can preserve predictable anatomy while attenuating unpredictable but clinically decisive pathology.

## Quick verdict

* Highly relevant

This is a strong adjacent paper because it audits the pretraining computation itself rather than only reporting downstream accuracy. TAP-JEPA is competitive as a CT encoder, but the exact hidden-target prediction pathway preferentially preserves anatomy over sporadic pathology. The caveat is that this is one large 3D CT JEPA, so the broader claim should be tested across objectives and modalities.

## One-paragraph overview

Joint-embedding predictive architectures learn by predicting teacher representations of hidden regions from visible context. In CT, surrounding anatomy is often predictable, but pathology can be localized, rare, and not inferable from neighboring tissue. This paper trains TAP-JEPA, a ViT-B/3D encoder on 113,611 CT volumes, and then replays the exact masking, teacher, predictor, and loss computations to ask what information survives prediction. The result is a clear predictability bias: anatomy remains much more recoverable than pathology, predicted pathology shifts toward matched normal controls, and several downstream classifiers barely change when final-layer pathology tokens are removed.

## Model definition

### Inputs

TAP-JEPA receives 3D CT volumes with masked target regions and visible context regions. The audit uses annotated pathology regions, matched control regions, mask exposure statistics, teacher features, predicted target features, and downstream scan-level labels.

### Outputs

The JEPA predictor outputs hidden-target representations from visible context. Downstream probes output scan-level pathology predictions from frozen encoder features.

### Training objective (loss)

TAP-JEPA is trained with a joint-embedding predictive objective: predict normalized teacher representations for masked 3D target regions from visible context. The audit replays this exact teacher/predictor computation to compare teacher-accessible information against predicted representations.

### Architecture / parameterization

The model is a ViT-B/3D joint-embedding predictive architecture trained for 240 epochs on thoraco-abdomino-pelvic CT volumes. Downstream analysis uses frozen features and scan-level probes.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It asks whether predictive self-supervision in medical imaging preserves clinically important local pathology, or whether it overlearns the more predictable anatomical structure around it.

### 2. What is the method?

The authors train TAP-JEPA, evaluate frozen features, then replay the exact mask sampler, teacher, predictor, and loss path on annotated pathology. They compare teacher targets, predicted targets, and geometry-only baselines for anatomy and pathology.

### 3. What is the method motivation?

Prediction rewards what can be inferred from context. In medical imaging, the clinically decisive signal is often the residual that context cannot predict.

### 4. What data does it use?

The model is trained on 113,611 CT volumes from four public cohorts. Evaluation includes RAD-ChestCT, Merlin, ATLAS, ReX, CT-RATE-derived thoracic probes, and annotated pathology categories across thoracic and abdominal settings.

### 5. How is it evaluated?

The paper reports frozen scan-level classification, mask exposure of pathology, Skill for anatomy/pathology discrimination in teacher versus predicted target representations, pathology-control displacement, context replacement interventions, and deletion effects on downstream decision margins.

### 6. What are the main results?

TAP-JEPA is competitive: on RAD-ChestCT it reports AUROC 0.7590 and AUPRC 0.5268, and on Merlin AUROC 0.8714 and AUPRC 0.6965. But pathology is often hidden and targeted: 61.5% to 81.4% of annotated pathology events are fully hidden and targeted. Prediction reduces pathology Skill more than anatomy Skill. In ATLAS, pathology Skill falls from 0.434 to 0.298 while anatomy falls from 0.886 to 0.820; in ReX, pathology falls from 0.341 to 0.243 while anatomy falls from 0.956 to 0.925. For liver, kidney, scarring/fibrosis, and nodules/masses, deleting final-layer pathology-overlapping tokens changes the decision margin by at most 0.45%.

### 7. What is actually novel?

The novelty is the causal audit of the JEPA prediction pathway: the paper traces what the actual pretraining target preserves and attenuates, rather than inferring everything from downstream transfer.

### 8. What are the strengths?

The paper uses a serious model and dataset scale, evaluates frozen transfer, and then digs into the mechanism with annotated pathology and exact replay of the training computation.

### 9. What are the weaknesses, limitations, or red flags?

The analysis is centered on one JEPA variant in CT. The downstream deletion test is final-layer and does not fully prove where pathology information may be redistributed. Some findings may change with masking policy, objective, representation depth, or modality.

### 10. What challenges or open problems remain?

The key challenge is building self-supervised objectives that keep the value of contextual anatomy while explicitly preserving context-unresolved pathology.

### 11. What future work naturally follows?

Test pathology-preserving losses, residual prediction objectives, masking schemes biased toward rare findings, and audits across radiographs, MRI, ultrasound, and video-like medical sequences.

### 12. Why does this matter for cabbageland?

It is a clean reminder that a representation can be excellent at predictable structure and still fail to preserve the rare residual events that matter. That applies beyond medicine.

### 13. What ideas are steal-worthy?

Audit the objective pathway, not only downstream scores. Compare teacher-accessible signal with predicted signal. Treat unpredictability as a feature to preserve, not noise to average away.

### 14. Final decision

Preserve. This is the strongest medical/non-agent paper in the batch and a useful warning about predictive representation learning.
