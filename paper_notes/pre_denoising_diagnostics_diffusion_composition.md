# Where to Look Is Not How to Fix: Pre-Denoising Diagnostics and Modality-Dependent Control in Diffusion Composition

## Basic info

* Title: Where to Look Is Not How to Fix: Pre-Denoising Diagnostics and Modality-Dependent Control in Diffusion Composition
* Authors: Fangzheng Wu, Brian Summa
* Year: 2026
* Venue / source: arXiv; listed as NeurIPS 2026
* Link: https://arxiv.org/abs/2610.03068
* Date surfaced: 2026-10-05
* Why selected in one sentence: It separates where compositional stress is diagnosable from where intervention actually improves a text-to-image diffusion output.

## Quick verdict

* Highly relevant

This is a careful diffusion-control paper, not a magic prompt-fixing paper. Its useful point is that diagnosis and control are different empirical questions: the layer or representation where a defect is most visible may not be the place where intervention helps. The effect sizes are small and narrow, but the experimental framing is unusually transferable.

## One-paragraph overview

The paper studies rare attribute-object compositions such as unusual color-object pairs in Stable Diffusion-style systems. It introduces a pre-denoising Compositional Stress Index, or CSI, that measures how poorly a full prompt embedding can be reconstructed from attribute, object, and context components. CSI detects controlled stress prompts, but repairing the embedding residual does not improve generated color agreement. Inside the denoiser, the deep encoder has the strongest diagnostic accessibility signal, while decoder cross-attention boost gives the strongest output response. The conclusion is not that decoder boost is a universal fix; it is that diagnostics, representation repair, and output control need to be mapped separately.

## Model definition

### Inputs

The experiments use matched anchor-stress prompt pairs, text-encoder embeddings, and cross-attention maps from SD1.5 and SDXL. SD3 is used for text-path diagnostic extension. The controlled prompt set contains 432 prompts organized as 216 anchor-stress pairs.

### Outputs

The paper outputs diagnostic scores and intervention measurements: CSI for text-side compositional stress, diagnostic accessibility for block-level cross-attention separation, color hit rate for object-local chromatic correctness, and effect estimates for embedding repair, selective boost, selective attribute zeroing, and broad cross-attention ablation.

### Training objective (loss)

The base diffusion models are frozen. The learned components are low-rank embedding adapters trained to reduce the CSI-diagnosed representation residual by moving stress embeddings toward anchor-like structure. Denoiser interventions are inference-time edits rather than trained losses.

### Architecture / parameterization

The study treats Stable Diffusion UNets as block-structured control surfaces: down/encoder blocks, middle block, and up/decoder blocks. CSI is computed from text-encoder representations through low-capacity composition models. Diagnostic accessibility is computed from attribute-binding behavior in cross-attention maps. Interventions alter either embeddings or cross-attention at selected sites.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It asks why text-to-image diffusion models fail at semantically rare compositions, and whether the place where a failure is detectable is also the place where fixing should happen.

### 2. What is the method?

Use a controlled anchor-stress protocol. First, compute CSI from text embeddings to detect non-factorized prompt representations. Second, test whether embedding-level repair changes output correctness. Third, sweep denoiser block groups and intervention modalities to compare diagnostic accessibility with output response.

### 3. What is the method motivation?

A lot of composition-control work assumes that if attention or representation geometry reveals a problem, intervening there should improve the image. The paper tests that assumption directly.

### 4. What data does it use?

The main controlled set has 432 prompts, 216 paired groups, and attributes/objects drawn from T2I-CompBench, CLEVR, and ARO lexicons. Full per-block color-hit analyses use 52 stress prompts per seed for which the color scorer is applicable. A smaller six-prompt localization subset is used for the matched embedding-versus-downstream comparison.

### 5. How is it evaluated?

CSI is evaluated as a separator between anchor and stress prompts and as a predictor of output-side failures. Denoiser blocks are evaluated with diagnostic accessibility. Intervention effects are evaluated with object-local color hit rate, using fixed attention-derived object masks and sign-flip/bootstrap analyses.

### 6. What are the main results?

CSI separates controlled anchor and stress prompts with reported ROC-AUC 1.0 across SD1.5, SDXL, and SD3 text path, though the authors explicitly note that the protocol helps create that separation. Embedding adapters reduce representation residuals but do not improve color hit rate; token-level repair can reduce it. A downstream intervention on a six-prompt localization subset improves color hit rate by 0.0272, while token embedding repair decreases it by 0.0680. Inside the denoiser, the largest positive diagnostic-accessibility mean appears at D2, but selective boost has its largest positive response at decoder blocks. Decoder boost effects are small and not universally FDR-robust.

### 7. What is actually novel?

The novelty is the diagnosis-control dissociation. The paper does not merely introduce a new metric; it shows that a metric can identify stress without giving you the right control coordinate.

### 8. What are the strengths?

The experimental design is clean, the claims are narrow, and the limitations are unusually explicit. It distinguishes representation fit, diagnostic readout, and output behavior instead of conflating them.

### 9. What are the weaknesses, limitations, or red flags?

The evaluated endpoint is color-only and applies to a limited subset of prompts. The intervention effects are small. SD3 is only tested through the text path, and the main control study is limited to UNet-style diffusion models rather than DiT backbones. Fixed intervention hyperparameters leave open whether better-tuned interventions would change the site map.

### 10. What challenges or open problems remain?

The large open problem is how to build interventions whose objectives match the denoiser's binding behavior. CSI-based routing and decoder repair remain unvalidated. Generality beyond chromatic binding is also not established.

### 11. What future work naturally follows?

Extend the site-modality map to DiT backbones, non-color composition, object count, spatial relations, material binding, and text/image-conditioned editing. A stronger next step would learn interventions with denoising-aligned objectives while keeping the diagnosis-control distinction.

### 12. Why does this matter for cabbageland?

It is a reusable warning for controllable generation and agent repair loops: the place where an error is legible is not automatically the place where action should be applied. Good systems need separate instrumentation for diagnosis and intervention.

### 13. What ideas are steal-worthy?

Use matched anchor-stress pairs to isolate a compositional defect. Build a diagnostic coordinate, then explicitly test whether optimizing that coordinate changes the output. Map interventions by both site and modality instead of treating an architecture as one homogeneous control surface.

### 14. Final decision

Preserve. This is directly useful for diffusion control, representation auditing, and the broader principle that observability is not controllability.
