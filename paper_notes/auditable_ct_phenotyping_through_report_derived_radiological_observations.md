# Auditable CT Phenotyping Through Report-derived Radiological Observations

## Basic info

* Title: Auditable CT Phenotyping Through Report-derived Radiological Observations
* Authors: Riga Wu, Walter R. Witschey, Yicheng Li, Felix Barajas Ordonez, Keno K. Bressem, Lisa C. Adams, Gary E. Weissman, Li Shen, Christos Davatzikos, Eduardo Mortani Barbosa Jr, Daniel Truhn, Tianyu Han
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.25948
* Date surfaced: 2026-08-27
* Why selected in one sentence: It is a rare medical foundation-model paper that turns "what evidence is this actually using?" into a reusable audit and intervention object.

## Quick verdict

* Useful

I inspected the full arXiv HTML text, especially the introduction, the native-model and observation-bank setup, the cross-cohort annotation results, and the phenotype probe-audit and restriction sections. This paper earns a preserved note because it does something better than report stronger AUROC. It builds an evidence vocabulary that can be reused for annotation, prediction, audit, and intervention in the same CT pipeline.

## One-paragraph overview

ACT combines a native 3D CT volume-report model with a report-derived bank of radiological observations. The native model encodes the volume, compares it against report text, and then uses those similarities to weight a large bank of named observation directions embedded by F2LLM, producing a concept-anchored CT representation. That representation is then used for zero-shot finding annotation, EHR-phenotype prediction, probe-observation auditing, and clinician-defined observation-bank restriction. The important result is not just that ACT outperforms several baselines. It is that the same observation bank exposes when good phenotype accuracy is being achieved through clinically weak evidence and allows those directions to be constrained.

## Model definition

### Inputs
CT volumes, paired radiology reports during native-model training, a bank of report-derived radiological observations, and linked EHR phenotype labels for downstream evaluation.

### Outputs
Volume embeddings, concept-anchored CT embeddings, zero-shot finding scores, phenotype scores, and ranked probe-to-observation alignments for audit.

### Training objective (loss)
The native model is trained with a contrastive objective aligning CT volume embeddings to paired reports. Downstream phenotype probes are linear multilabel sigmoid heads trained with mean binary cross-entropy on frozen representations.

### Architecture / parameterization
DINOv2 slice encoder plus lightweight Transformer aggregation for the native 3D volume-report model, combined with a 376,194-item report-derived observation bank embedded by F2LLM into a 5,120-dimensional semantic space. Phenotype prediction is done with frozen features plus linear probes.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the fact that CT foundation models can predict many clinical phenotypes well while still relying on shortcut-like findings or clinically invalid proxy evidence.

### 2. What is the method?
The method trains a native 3D image-text model over CT volumes and reports, mines a large bank of named radiological observations from those reports, uses image-text similarities to build a concept-anchored CT representation, then audits and restricts phenotype probes against that bank.

### 3. What is the method motivation?
If a model predicts an EHR phenotype from CT, we still need to know whether it is using evidence that is actually related to the coded condition or merely exploiting correlated radiological context. A shared observation vocabulary makes that question inspectable.

### 4. What data does it use?
Training uses 38,317 patients: 20,000 chest CT-RATE patients and 18,317 abdominal Merlin patients. The observation bank contains 376,194 distinct radiological observations. Evaluation spans 25,183 held-out patients across CT-RATE, PMBB, RSNA-2023, and INSPECT. The phenotype study keeps 221 INSPECT phenotypes with at least 50 positive test scans.

### 5. How is it evaluated?
It is evaluated on zero-shot finding annotation, concept-conditioned retrieval, anatomical and ontological organization of the observation bank, zero-shot and linear-probe phenotype prediction versus CT-CLIP, and a probe-observation audit plus clinician-defined bank restriction.

### 6. What are the main results?
For zero-shot finding annotation, ACT reaches mean AUROCs of `0.749` on CT-RATE, `0.689` on chest PMBB, `0.683` on abdominal PMBB, and `0.675` on RSNA-2023, beating both 3D and 2D baselines. In phenotype prediction on unseen CTPA data, ACT beats CT-CLIP at macro AUROC `0.651` versus `0.572` under zero-shot scoring and `0.709` versus `0.662` under matched linear probing. The audit result is the severe part: only `97` observations occupy the `221` top-ranked phenotype directions, and one calcification phrase ranks first for `20` phenotypes including clinically unrelated ones. Restricting the observation bank to clinician-specified direct or associated evidence keeps `86` non-empty phenotype rule sets and improves the mean held-out AUROC from `0.741` to `0.751`.

### 7. What is actually novel?
The useful novelty is using one report-derived observation bank as the common language for annotation, phenotyping, audit, and restriction, rather than treating interpretability as a separate afterthought.

### 8. What are the strengths?
The paper is unusually strong on auditability and intervention. It not only shows that the representation is useful, but also exposes which observation directions dominate phenotype probes and demonstrates that restricting those directions can redirect evidence without hurting performance.

### 9. What are the weaknesses, limitations, or red flags?
The phenotype labels are weak EHR-derived phecodes rather than adjudicated radiological truths. The set of 221 reported phenotypes is chosen post hoc based on test prevalence. Only 86 phenotypes end up with non-empty clinician-defined evidence sets, which limits how broad the restriction result really is. The observation bank is also only as good as the reports it comes from, so reporting bias is built into the representation.

### 10. What challenges or open problems remain?
Scaling the evidence bank to more anatomies and more precise phenotype definitions, replacing weak EHR labels with better clinical targets, and making the clinician-defined restriction process less manual while keeping it trustworthy.

### 11. What future work naturally follows?
Patient-level counterfactual audits, automatic proposal of suspect observation clusters, broader concept-bank restriction for multimodal medical foundation models, and better separation of causal findings from care-process artifacts.

### 12. Why does this matter for cabbageland?
Because cabbageland keeps preferring systems that expose the evidence carrying the claim instead of asking everyone to trust a strong downstream metric. This paper is useful mainly as an audit pattern.

### 13. What ideas are steal-worthy?
Use one named concept bank across prediction and audit. Inspect the alignment between downstream probes and concept directions. Restrict the bank to domain-approved evidence and test whether performance holds or even improves.

### 14. Final decision
Keep as a preserved note. The paper is not clean enough to treat as solved clinical truth, but it is unusually honest and useful about evidence.

## 6. Mandatory critical angles

The paper is strongest on explicit evidence, intervention, and cross-cohort evaluation. Its main weaknesses are weak labels, post hoc phenotype filtering, and reliance on clinician-written restriction rules.

## 7. Writing style

The right tone is respectful and hard-nosed. The paper is worth keeping because it makes clinical evidence auditable, not because medical AUROC numbers are automatically persuasive.

## 8. Repository output format

Saved as a preserved paper note because the audit-and-restrict pattern is more transferable than the specific CT application.
