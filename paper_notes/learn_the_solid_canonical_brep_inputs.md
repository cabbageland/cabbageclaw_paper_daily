# Learn the Solid, Not the File: Canonical Inputs for Neural Networks on CAD Boundary Representations

## Basic info

* Title: Learn the Solid, Not the File: Canonical Inputs for Neural Networks on CAD Boundary Representations
* Authors: Heinrich Jiang, Hager Yasser Mohamed, Alexander Hitt, Valeriia Lomakina, Henning Jiang, Jennifer Jang
* Year: 2026
* Venue / source: arXiv:2609.11573
* Link: https://arxiv.org/abs/2609.11573
* Date surfaced: 2026-09-13
* Why selected in one sentence: It replaces arbitrary B-rep file partitions with a canonical solid-derived graph and shows that common CAD encoders are brittle to equivalent redescriptions of the same object.

## Quick verdict

* Must read

I inspected the full arXiv HTML text, including the canonical region construction, invariance argument, automatic perturbation tests, retrieval benchmark, predictive-churn analysis, and limitations. This is preserve-worthy because it cleanly separates the represented object from the accidental file decomposition.

## One-paragraph overview

The paper argues that B-rep neural networks often learn the stored file partition rather than the CAD solid. The same solid can be split into different faces, re-expressed as NURBS, rotated, passed through another CAD kernel, or modeled differently by a human while remaining the same object. Existing B-rep encoders can collapse under these valid changes. The proposed canonical region graph merges connected pieces of the same underlying surface, computes a canonical solid frame from centroid and principal directions, expresses node and edge features in that frame, and uses a graph transformer on the resulting representation. The method matches strong baselines on clean benchmarks while remaining stable under perturbations that break the baselines.

## Model definition

### Inputs
The model consumes a CAD solid represented through its canonical region graph. Nodes are maximally connected surface regions after merging arbitrary file cuts; edge features describe shared boundary curves. Positions, directions, areas, and related geometry features are expressed in a canonical frame derived from the solid rather than the input file frame.

### Outputs
For segmentation tasks, the model outputs per-region logits that are inherited by the original B-rep faces contained in each region. For retrieval and stability analysis, the representation yields embeddings or predictions that should remain stable across equivalent B-rep descriptions.

### Training objective (loss)
The paper uses supervised training for downstream CAD tasks such as segmentation, with standard classification/segmentation losses over labels inherited by faces or regions. The canonical construction itself is deterministic and is not learned.

### Architecture / parameterization
The representation is fed to a graph transformer: standardized node and edge features pass through an MLP stem, then 8 rounds of edge-conditioned multi-head attention with residual feed-forward blocks, width 512, 8 heads, and about 17.5M parameters.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
CAD solids have many valid B-rep descriptions. Existing B-rep neural encoders often treat those descriptions as distinct inputs, so predictions can change when the file is repartitioned, rotated, re-expressed, or round-tripped through another kernel even though the solid is unchanged.

### 2. What is the method?
Build a canonical region graph. Merge file faces that are connected pieces of the same underlying surface, keep separate disconnected surfaces even when they share parameters, compute a canonical frame from the solid, express features in that frame, and run a graph transformer over the resulting object-level graph.

### 3. What is the method motivation?
The model should be invariant to changes that preserve the CAD solid. If the target property belongs to the solid, not to the file partition, the input representation should encode the equivalence class rather than one arbitrary member of it.

### 4. What data does it use?
The experiments use standard CAD segmentation benchmarks including MFInstSeg, MFCAD++, and CADSynth; a 3,000-part Fusion 360 retrieval benchmark; and a human FreeCAD dataset where multiple CAD experts model the same part in different ways.

### 5. How is it evaluated?
The paper applies automatic perturbations: axis and diagonal face splitting, random rigid rotation, analytic-surface-to-NURBS re-expression, commercial-kernel import/export, and composed perturbations. It evaluates segmentation macro mIoU, retrieval self-identification, predictive churn, region ablations, and human-modeled variations.

### 6. What are the main results?
Under automatic perturbations, popular B-rep baselines often degrade sharply. On MFInstSeg, AAGNet falls from 0.9851 clean mIoU to 0.0055 under composed perturbations, UV-Net from 0.9725 to 0.0026, and BRepNet from 0.9828 to 0.4428, while the canonical method remains about 0.9862. Similar stability holds on MFCAD++ and CADSynth. On 3,000 Fusion 360 retrieval queries, the method reaches 96.1% and 96.3% rank-1 accuracy under axis and diagonal splits and remains 76.1% under composed perturbations, much stronger than B-rep baselines.

### 7. What is actually novel?
The novelty is not the graph transformer; it is the solid-derived canonical input. The paper makes arbitrary B-rep cuts, coordinate frames, and analytic-vs-NURBS encodings explicit nuisance variables, then removes them before learning.

### 8. What are the strengths?
The representation matches the invariance claim, and the perturbations are well chosen. The paper tests both automatic and human sources of equivalent representations, reports predictive churn rather than only average accuracy, and shows that simple augmentation does not repair the underlying representational mismatch.

### 9. What are the weaknesses, limitations, or red flags?
The construction depends on robust geometric keys, tolerances, and CAD-kernel access to underlying surfaces. Symmetric or degenerate solids require averaging or special handling. The method addresses single solids more directly than assemblies, feature histories, sketches, and richer design intent.

### 10. What challenges or open problems remain?
Open problems include assemblies, 2D sketches, feature trees, construction histories, tolerance robustness across real kernels, and generative evaluation metrics that do not punish correct solids merely because they use a different B-rep partition than a reference.

### 11. What future work naturally follows?
Extend canonicalization to assemblies and construction histories, pair it with generative CAD models, and replace element-matching reconstruction scores with solid-equivalence-aware metrics.

### 12. Why does this matter for cabbageland?
Cabbageland cares about explicit state over format accidents. This paper is a crisp example: the useful state is the solid, while the file's face partition is lossy bookkeeping that can actively mislead a learner.

### 13. What ideas are steal-worthy?
Audit whether the model reads an arbitrary representation rather than the invariant object. Canonicalize nuisance choices before learning. Report predictive churn under equivalent redescriptions. Design metrics around equivalence classes, not storage artifacts.

### 14. Final decision
Preserve as a must-read representation paper. It is one of the better recent examples of replacing a brittle input convention with a state carrier that actually matches the claim.
