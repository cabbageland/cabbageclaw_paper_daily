# Cross-Lingual Alignment Without Joint Training: Do Monolingual Language Models Converge on Universal Representations?

## Basic info

* Title: Cross-Lingual Alignment Without Joint Training: Do Monolingual Language Models Converge on Universal Representations?
* Authors: Ej Zhou, Suchir Salhan, Catherine Arnett, Anna Korhonen
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.27115
* Date surfaced: 2026-08-29
* Why selected in one sentence: It shows that independent monolingual models can converge to an alignable geometry, and that a rigid rotation is enough to transfer actual factual content.

## Quick verdict

* Highly relevant

I inspected the full arXiv HTML text, especially the correlation/construction/causation framing, the reconstruction tables, the activation-patching experiment, and the contamination audit. This paper earns a preserved note because it tests a big claim in the right order: first geometric similarity, then constructive mapping, then causal content transfer. The result is more interesting than another multilingual benchmark win because it weakens the assumption that shared multilingual training is the only route to shared semantic structure.

## One-paragraph overview

The paper asks whether independently trained monolingual language models learn a shared representational geometry even when they never share parameters or multilingual data. It answers with three increasingly strong tests. First, hidden-state alignment on parallel sentences improves with data scale, model scale, and language proximity. Second, one model's hidden states can be mapped into another's with a simple Procrustes rotation. Third, the same rotation is causally meaningful: when a rotated source-language residual is patched into a target-language model at the right concept position, the target model's factual prediction flips toward the source model's answer. The striking part is not just that alignment exists, but that a geometry-preserving map works better for retrieval than more flexible affine or MLP fits.

## Model definition

### Inputs
Hidden states from monolingual language models run on parallel sentences, plus source-language residual activations for factual cloze prompts in the activation-patching experiments.

### Outputs
Aligned hidden representations, retrieval scores between source and target hidden states, and changed target-language factual predictions after patching.

### Training objective (loss)
The fitted maps minimize representation mismatch between paired source and target hidden states. Procrustes minimizes Frobenius reconstruction error under an orthogonality constraint. Affine and MLP baselines use less constrained reconstruction objectives.

### Architecture / parameterization
The paper does not introduce a new language model. It studies fixed monolingual transformers and compares three post hoc alignment maps: orthogonal Procrustes, affine linear mapping, and a small MLP.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to determine whether cross-lingual representational alignment requires joint multilingual training or whether independent monolingual training can still converge to a shared semantic geometry.

### 2. What is the method?
The method has three parts: correlate representations on parallel sentences, construct explicit maps between models, and causally test those maps by activation patching on factual cloze tasks.

### 3. What is the method motivation?
If monolingual models already converge to compatible geometry, then multilingual capability may be more modular than people assume. That matters for model stitching, merging, and multilingual systems built from monolingual components.

### 4. What data does it use?
The main reconstruction results use 36 language pairs from the Goldfish model family, with additional analyses on independently developed monolingual models from other groups. Mapping is fit on parallel sentence activations, and causal tests use country-to-capital cloze prompts across multiple target languages.

### 5. How is it evaluated?
The reconstruction experiments report P@1 retrieval, MSE, and linear CKA. The causal experiments report directional success rate: how often patching a rotated source residual into the target model pushes the target toward the donor answer. The paper also audits training-corpus language contamination.

### 6. What are the main results?
Across 36 Goldfish language pairs, Procrustes reaches 88.7% P@1 on the standard pool and 77.5% on the harder pool, versus 0.2% and 0.0% for the identity baseline, while reducing MSE from 2.258 to 0.689. More flexible affine and MLP maps lower MSE further but lose on retrieval. In the causal test, within-model patching gives a 76-98% ceiling, while cross-lingual Procrustes transfer still reaches 66-85% directional success across English to French, German, Spanish, Japanese, and Chinese. The contamination audit finds at most 0.1% English content in the non-English corpora used in the main analysis.

### 7. What is actually novel?
The novelty is not just another alignment score. It is showing that a single geometry-preserving rotation both reconstructs cross-lingual hidden states and transfers factual content causally, without shared multilingual pretraining.

### 8. What are the strengths?
The evidence ladder is excellent: correlation, construction, then causation. The metric choice is also thoughtful. The paper shows why lower reconstruction error is not the same as better semantic alignment when the application depends on preserved angular structure and neighborhood relations.

### 9. What are the weaknesses, limitations, or red flags?
The strongest causal probe is still a narrow factual cloze setup rather than open-ended generation. The main model families are around the 1B scale rather than frontier size, and the alignment maps are fit using parallel sentences, so this is not a pure no-supervision result.

### 10. What challenges or open problems remain?
The next question is whether the same geometry survives at frontier scale, richer tasks, and more structurally distant languages. Another open problem is whether useful alignment can be learned with weaker supervision than parallel text.

### 11. What future work naturally follows?
Model stitching, modular multilingual systems, and cross-lingual component reuse are the obvious directions. It would also be useful to test whether aligned monolingual modules can share tools, planners, or retrieved memory without retraining.

### 12. Why does this matter for cabbageland?
Because cabbageland keeps caring about reusable structure across systems. This paper suggests that shared semantic geometry may emerge more often than we assume, and that preserving the right invariants can matter more than fitting every coordinate perfectly.

### 13. What ideas are steal-worthy?
Use a strict evidence ladder for representation claims. Prefer geometry-preserving maps when downstream behavior depends on neighborhood structure. Test representation alignment causally by patching transformed states into a separate model instead of stopping at similarity scores.

### 14. Final decision
Keep as a preserved note. This is a strong representation paper with a clear claim, a good causal test, and practical implications beyond multilingual NLP.

## 6. Mandatory critical angles

The paper is strongest on evaluation fairness and mechanistic clarity. It does not stop at CKA vibes or cherry-picked bilingual examples; it asks whether the aligned representation can actually do something causal in the target model. The main realism caveat is that parallel data still fits the maps and the causal task is narrow. Even so, the orthogonality-versus-expressivity result is a durable lesson: the better fit is not always the better mechanism.

## 7. Writing style

The tone should be impressed by the evidence ladder, not by multilingual mystique. The real story is the geometry and the causal transfer, not generic "universal representation" branding.

## 8. Repository output format

Saved as a preserved paper note because the geometry-preserving alignment lesson is likely to matter for modular multilingual systems and representation reuse more broadly.
