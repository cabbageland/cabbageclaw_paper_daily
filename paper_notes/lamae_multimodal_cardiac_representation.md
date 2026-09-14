# Reading the Whole Heart: Latent-Attention Masked Autoencoders for Multimodal Cardiac Representation Learning

## Basic info

* Title: Reading the Whole Heart: Latent-Attention Masked Autoencoders for Multimodal Cardiac Representation Learning
* Authors: Andrea Agostini, Simon Bohi, Moritz Vandenhirtz, Samuel Ruiperez-Campillo, Max Krahenmann, Silke Muhlstedt, Irene Cannistraci, Ece Ozkan Elsen, Julia E. Vogt, Thomas M. Sutter
* Year: 2026
* Venue / source: arXiv:2609.12035
* Link: https://arxiv.org/abs/2609.12035
* Date surfaced: 2026-09-14
* Why selected in one sentence: It treats multimodal clinical data as a structured patient-level hierarchy during self-supervised pretraining instead of fusing modality encoders only at finetuning time.

## Quick verdict

* Highly relevant

This is a useful medical representation-learning paper because it takes data structure seriously. The latent-attention module gives the model a patient-level workspace where ECG, echo, chest X-ray, and clinical variables can exchange information despite missingness and irregular study/view/entity structure. The single-source MIMIC setting limits the deployment claim, but the modeling move is worth preserving.

## One-paragraph overview

LAMAE is a multimodal masked autoencoder for cardiovascular representation learning. Each modality has its own encoder and decoder, but visible tokens from all available modalities are passed through a shared latent-attention module with a multimodal CLS token. The method models healthcare data as a study-view-entity hierarchy: echo studies have multiple videos/frames, ECGs have leads, and CXR studies may have multiple views. During pretraining, patch masking and entity masking force reconstruction not only from local signal context but also from cross-entity and cross-modal evidence. Pretrained on over 1.2 million MIMIC-IV hospital stays, LAMAE improves on independent MAE and strong medical baselines on hospital-stay tasks.

## Model definition

### Inputs

Inputs are multimodal hospital stays containing any available subset of ECG, echocardiography, chest X-ray, and clinical variables. Each modality is represented through a hierarchy of studies, views, and base entities such as echo frames, ECG leads, or CXR images. The model also receives masks indicating missing modalities and masked patches/entities.

### Outputs

During pretraining, the model reconstructs masked parts of each available modality. For downstream tasks, it outputs patient-level representations through the multimodal CLS token, then task heads predict mortality, ICD-10 chapter labels, DRG code/severity/mortality risk, length of stay, LVEF, CXR labels, or ECG interval measurements.

### Training objective (loss)

The pretraining loss is a masked reconstruction objective over unavailable-to-the-encoder patches of available modalities, weighted by modality-specific mask ratio. Entity masking also drops whole leads, frames, or views. Downstream tasks use task-specific supervised finetuning losses.

### Architecture / parameterization

LAMAE uses modality-specific transformer encoders and decoders plus a shared multi-head, multi-layer latent-attention module. The latent-attention module processes concatenated latent embeddings from all observed modalities and produces a multimodal CLS token and cross-modal output tokens.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Most medical foundation models are modality-specific or fuse modalities late. Cardiovascular diagnosis, however, naturally integrates ECG, echo, chest radiographs, and clinical variables, and real hospital data is irregular and missing. The paper tries to pretrain on that structured multimodal reality directly.

### 2. What is the method?

Encode visible modality-specific tokens separately, merge their latent embeddings with a shared latent-attention block, and reconstruct masked patches/entities through modality-specific decoders. Use a multimodal CLS token for downstream hospital-stay tasks.

### 3. What is the method motivation?

Late fusion discards cross-modal evidence during representation learning. A shared latent workspace can learn both intra-modality structure and inter-modality relationships while still handling missing modalities cleanly.

### 4. What data does it use?

The paper builds a MIMIC-IV multimodal hospital-stay dataset using MIMIC-IV-CXR, MIMIC-IV-ECG, MIMIC-IV-Echo, and MIMIC-IV-ED. It contains 1,267,017 unique hospital stays, 227,835 CXR studies with 377,110 images, 7,243 echo studies with 525,328 videos, and 800,035 12-lead ECG measurements.

### 5. How is it evaluated?

The main evaluation is hospital-stay-level prediction: in-hospital mortality, ICD-10 chapter IX, DRG code, DRG severity, DRG mortality risk, and length of stay. It also evaluates unimodal CXR CheXpert labels, echo LVEF regression, and ECG interval regression.

### 6. What are the main results?

On hospital-stay tasks, LAMAE beats the independent MAE on all six tasks and beats strong ProbMED/MedSigLip-style baselines on five of six. In-hospital mortality AUROC reaches 91.59, ICD-10 chapter IX reaches 83.02, DRG severity 70.29, DRG mortality risk 72.21, and length of stay 81.70. The 1500-epoch checkpoint nudges mortality to 91.71 and ICD-10 to 83.10. On unimodal tasks, LAMAE is competitive on CXR, improves echo LVEF MAE from 8.97 to 8.29, and improves five of six ECG interval targets.

### 7. What is actually novel?

The novelty is the structured latent-attention pretraining setup: modality-specific encoders/decoders with a shared latent multimodal integration block, plus entity masking over clinically meaningful entities like leads, frames, and views.

### 8. What are the strengths?

The paper is aligned with the structure of the domain. It has a large pretraining corpus. It isolates the latent-attention contribution by comparing against an independent MAE trained on the same data and time. It evaluates both patient-level multimodal tasks and unimodal probes.

### 9. What are the weaknesses, limitations, or red flags?

Everything is still MIMIC-derived, so cross-institution transfer is not established. Restricted-modality tests partly measure modality coverage because echo and CXR are missing for many hospital stays. The CXR gains are within seed variance. Clinical utility requires external validation and robustness checks beyond benchmark AUROC.

### 10. What challenges or open problems remain?

The main open problem is whether the learned patient-level representation transfers across hospitals, scanners, care patterns, and patient populations. Another is integrating notes, labs, medications, and time-series vitals without turning the latent workspace into an unstructured dump.

### 11. What future work naturally follows?

Validate on external cohorts, add laboratory time series and clinical notes, study missingness mechanisms explicitly, and test whether entity masking improves robustness to missing leads/views under clinical acquisition shifts.

### 12. Why does this matter for cabbageland?

It is a good example of preserving the right hierarchy in a foundation model: patient, study, view, entity, modality, and missingness. That is relevant well beyond medicine.

### 13. What ideas are steal-worthy?

Use a latent workspace after modality-specific encoders. Mask whole semantic entities, not only patches. Treat missing modalities as first-class structure. Evaluate full multimodal tasks and unimodal probes to see whether integration helps or merely averages.

### 14. Final decision

Preserve as adjacent inspiration. The domain is medical, but the structure-aware pretraining pattern is directly reusable.
