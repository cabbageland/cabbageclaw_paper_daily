# What Makes a Good Medical Image Tokenizer? Rethinking Reconstruction and Generation in Medical Image Tokenization

## Basic info

* Title: What Makes a Good Medical Image Tokenizer? Rethinking Reconstruction and Generation in Medical Image Tokenization
* Authors: Niklas Bubeck, Yundi Zhang, Vasiliki Sideri-Lampretsa, Julian McGinnis, Jiancheng Yang, Daniel Rueckert, Jiazhen Pan
* Year: 2026
* Venue / source: arXiv:2609.24691
* Link: https://arxiv.org/abs/2609.24691
* Date surfaced: 2026-09-22
* Why selected in one sentence: It audits medical image tokenizers as state carriers for generation, privacy, and downstream utility instead of assuming natural-image tokenizer behavior transfers.

## Quick verdict

Useful. This is adjacent rather than core, but it is a good domain-specific representation audit. The paper's strongest contribution is not a new tokenizer; it is a controlled benchmark showing that medical image tokenization obeys different tradeoffs than natural-image tokenization. Full arXiv text was inspected.

## One-paragraph overview

Latent diffusion in medical imaging depends on a tokenizer that compresses images into the space where the generator operates. This paper benchmarks 30 tokenizer configurations from 10 model families across 12 medical datasets and three compression factors. It measures reconstruction, generation, codebook behavior, latent geometry, downstream classification, and memorization. The key message is that medical data changes the usual assumptions: reconstruction strongly predicts generation, codebook usage does not guarantee good latent geometry, memorization is generally mild and decreases with compression, and most discrete tokenizers preserve downstream-useful information.

## Model definition

### Inputs

Inputs are 2D medical images from 12 datasets. Tokenizers encode images into continuous or discrete latent grids at compression factors 4, 8, and 16, with matched latent shapes across methods.

### Outputs

Each tokenizer outputs latent codes and reconstructed images. A frozen tokenizer then provides latents for a conditional DiT generator. Downstream probes use frozen latent representations for classification.

### Training objective (loss)

All tokenizers share a fixed autoencoding setup and reconstruction-centered training objective, with quantizer-specific commitment or codebook mechanisms where applicable. The generator is a DiT-B/2-style latent diffusion model trained over frozen tokenizer latents with class and dataset conditioning.

### Architecture / parameterization

The benchmark includes VQGAN, SimVQ, SimQINCo, RQVAE, DiVeQ, SF-DiVeQ, LFQ, BSQ, continuous AEKL, and SoftVQ. The encoder and decoder follow a convolutional VQ-GAN backbone, while the generator uses a shared DiT with AdaLN-Zero conditioning.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It addresses the lack of evidence for tokenizer choice in medical latent generative models. Medical pipelines often inherit natural-image tokenizers even though medical datasets are smaller, less diverse, and more privacy-sensitive.

### 2. What is the method?

The method is a controlled benchmark: train many tokenizer families under a shared backbone and protocol, freeze them, train matched generators, and evaluate reconstruction, generation, latent geometry, codebook statistics, memorization, and downstream linear probes.

### 3. What is the method motivation?

A tokenizer bounds what the generator can model and what downstream systems can reuse. In medicine, it also affects whether synthetic generation leaks patient identity and whether diagnostic features survive compression.

### 4. What data does it use?

The paper uses 12 medical imaging datasets spanning several modalities and tasks. It evaluates each tokenizer at three compression factors and conditions the generator on class and source-dataset embeddings.

### 5. How is it evaluated?

It reports reconstruction metrics such as PSNR, SSIM, LPIPS, rFID, and reconstruction Frechet Medical Distance; generation metrics such as gFID and generation Frechet Medical Distance; codebook utilization and latent geometry; memorization via nearest-neighbor/copy-rate style measures; and downstream utility via linear classifiers on frozen latents.

### 6. What are the main results?

Reconstruction and generation strongly correlate in this benchmark: rFID and gFID have Pearson r = 0.82 with 95% bootstrap CI [0.77, 0.86], and Spearman rho = 0.81 with CI [0.77, 0.85]. Modern tokenizers often use nearly all codebook entries, but explicit-codebook methods can still compress latents into thin anisotropic subspaces. Memorization is mild overall and decreases under stronger compression. Most discrete tokenizers preserve downstream classification information, while lookup-free binarization shows a consistent probe gap around 0.02 to 0.05.

### 7. What is actually novel?

The novelty is the multi-axis medical tokenizer benchmark and the finding that medical reconstruction is a useful predictor of generation quality, contrary to reports from natural-image tokenizer studies.

### 8. What are the strengths?

The evaluation is broad and asks the right operational questions: not just "does the image reconstruct," but "does the latent generate, memorize, preserve downstream signal, and use its codebook sensibly?"

### 9. What are the weaknesses, limitations, or red flags?

The study is limited to 2D medical data. It uses a single fixed DiT-B/2 generator, so results measure latent fidelity under that generator rather than all possible discrete-code modeling regimes. The downstream task is linear probing, not full clinical use.

### 10. What challenges or open problems remain?

Volumetric data, high-resolution clinical settings, report-conditioned generation, and autoregressive modeling over discrete medical tokens all remain open. A matched natural-image control under the exact same codebase would also sharpen the domain contrast.

### 11. What future work naturally follows?

Future work should test tokenizer behavior in 3D MRI/CT, multimodal report-image generation, and foundation-model pretraining. It should also treat privacy and diagnostic preservation as first-class tokenizer objectives.

### 12. Why does this matter for cabbageland?

It is a good reminder that latent compression is a modeling decision, not infrastructure. The same state bottleneck carries generation quality, privacy risk, and task information.

### 13. What ideas are steal-worthy?

Steal the multi-axis tokenizer audit: reconstruction, generation, code usage, latent rank, memorization, and downstream probe utility. Also steal the domain-specific humility: do not assume a representation lesson transfers unchanged from natural images to medical images.

### 14. Final decision

Preserve as adjacent inspiration. It is useful for thinking about representation bottlenecks and evaluation design.
