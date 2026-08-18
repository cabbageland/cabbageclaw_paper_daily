# CytoFormer: A Molecularly Supervised Cell Foundation Model for Histopathology Cell Classification

## Basic info

* Title: CytoFormer: A Molecularly Supervised Cell Foundation Model for Histopathology Cell Classification
* Authors: Jialu Yao, Songhao Li, Alina Yu, Zhi Huang
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.16718
* Date surfaced: 2026-08-18
* Why selected in one sentence: It replaces manual cell labeling with paired spatial transcriptomics and turns that paired supervision into a reusable histopathology representation.

## Quick verdict

* Useful

I inspected the arXiv HTML full text. This is a strong adjacent paper because it uses a paired modality to solve a real supervision bottleneck instead of treating multimodality as branding. The best part is not only the scale. It is that the molecular signal seems to buy a better representation, not just a bigger pretraining set.

## One-paragraph overview

CytoFormer is a cell-level histopathology model trained from paired H&E and spatial transcriptomics rather than from manual image annotations. The authors collect 81 Xenium sections across 16 organs, derive cell identities by clustering and marker-based transcriptomic annotation, transfer those labels onto matched H&E crops, and train a ViT-giant encoder with organ-specific cell-type heads on 15.4 million cells. The resulting representation classifies held-out cells across organs, transfers well to public cell-classification benchmarks, and is notably label-efficient in an active-learning setting where it has to separate normal epithelium from look-alike tumor. The main contribution is a supervision recipe: use molecules to supervise morphology directly at cell resolution.

## Model definition

### Inputs
For each cell, the model takes a 56-micrometer H&E crop centered on the nucleus, resized to 224 by 224 pixels, together with the organ identity that selects the appropriate output head.

### Outputs
It outputs a 1536-dimensional cell embedding and an organ-specific cell-type prediction over 23 total categories distributed across 16 per-organ heads.

### Training objective (loss)
The accessible text describes supervised per-organ cell-type training but does not write the main loss in formula form. It is clearly optimized as a multi-class classification problem, and the downstream linear probes use class-balanced cross-entropy.

### Architecture / parameterization
CytoFormer uses a ViT-giant encoder initialized from UNI2-h, fine-tuned end-to-end, followed by 16 linear per-organ classification heads whose combined output space has 103 logits.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve how to obtain scalable and reliable cell-type supervision from routine histology without relying on slow, costly, and often noisy manual pathologist annotations.

### 2. What is the method?
The method pairs Xenium spatial transcriptomics with matched H&E, derives transcriptome-based cell labels, maps them onto H&E crops of the same physical cells, and trains a cell foundation model on those paired examples.

### 3. What is the method motivation?
Spatial transcriptomics can identify the same cell that later appears in the H&E section, so molecular identity can supervise morphology directly and at scale, avoiding manual image labeling bottlenecks.

### 4. What data does it use?
It uses **15.4 million** paired cells from **81** sections across **16** organs, with a spatially careful split of **12,111,769** training cells and **2,944,356** test cells, plus four public cell-classification benchmarks and a VisiumHD active-learning benchmark.

### 5. How is it evaluated?
It is evaluated on spatially held-out tissue, crop-size ablations, linear and full fine-tuning on public expert-annotated benchmarks, and an interactive active-learning task for normal-epithelium detection.

### 6. What are the main results?
On spatially held-out tissue it reaches **0.846** accuracy and **0.779** macro-F1 across all 16 organs. A **56**-micrometer crop is the best field of view. Under linear fine-tuning and full fine-tuning it outperforms six existing pathology foundation models on four public benchmarks. In the label-efficiency setting it reaches **0.82** F1 for normal-epithelium detection, beating the strongest baseline by about **0.13** F1 and reaching most of its final performance within roughly the first 200 annotations.

### 7. What is actually novel?
The novelty is using paired spatial transcriptomics as the direct source of cell-level supervision for routine histology, then showing that this supervision produces a transferable and label-efficient representation.

### 8. What are the strengths?
The dataset curation is serious, the train-test split is spatially careful enough to avoid leakage through overlapping crops, and the active-learning result makes a convincing case that the representation itself improved rather than the paper merely aggregating more data. The organ-specific heads are also a sensible way to respect real cross-organ appearance differences.

### 9. What are the weaknesses, limitations, or red flags?
The label space is intentionally coarse, so many finer immune or stromal subtypes are merged away. The paper uses Xenium alone as the source of molecular labels, so the supervision pipeline is not yet modality-agnostic. It also stops at cell typing rather than showing strong downstream clinical outcome gains.

### 10. What challenges or open problems remain?
The main open problems are extending the supervision recipe to finer cell states, other paired modalities, and real downstream clinical tasks where the typed-cell map has to prove its utility beyond classification accuracy.

### 11. What future work naturally follows?
Extend the approach to spatial proteomics or Visium HD, resolve finer subtypes, and use the resulting typed-cell maps as inputs for diagnosis, prognosis, treatment-response prediction, and broader tissue-organization analysis.

### 12. Why does this matter for cabbageland?
Because it is a very clean example of a general trick cabbageland cares about: use a paired modality with stronger semantics to supervise a cheaper and more ubiquitous modality, then keep the cheaper modality at inference time.

### 13. What ideas are steal-worthy?
Pair a semantically strong but expensive modality with a cheap production modality, transfer labels at the level of identical physical entities, split data in a way that respects field-of-view leakage, and judge foundation-model quality by low-annotation downstream usefulness rather than only raw pretraining scale.

### 14. Final decision
Keep as a preserved note. The molecular-supervision recipe is the part worth remembering, and it looks more transferable than the specific pathology benchmark details.

## 6. Mandatory critical angles

The paper is strongest on representation learning, data realism, and transferability. It replaces a brittle annotation pipeline with a semantically stronger one and shows that the gain survives into low-label downstream use. The main caveat is granularity: the taxonomy remains clinically useful but biologically coarse, so some of the claimed cell understanding is really category-level regularization.

## 7. Writing style

The right tone is approving but measured. This is a strong data-and-representation paper, not a proof that pathology cell foundation models are solved.

## 8. Repository output format

Saved as a preserved paper note because the paired-modality supervision trick is broadly reusable and the evidence is strong enough to keep.
