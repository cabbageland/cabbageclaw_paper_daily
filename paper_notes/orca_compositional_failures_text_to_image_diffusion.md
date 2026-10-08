# ORCA: Hunting Compositional Failures in Text-to-Image Diffusion

## Basic info

* Title: ORCA: Hunting Compositional Failures in Text-to-Image Diffusion
* Authors: Arshia Hemmat, Amirhossein Vahidi, Amitis Shidani, Mohammad Vali Sanian, Hesam Asadollahzadeh, Aryan Yazdan Parast, Mo Lotfollahi
* Year: 2026
* Venue / source: arXiv preprint
* Link: https://arxiv.org/abs/2610.09841
* Date surfaced: 2026-10-08
* Why selected in one sentence: It treats text-to-image binding failures as a train-time cross-modal alignment problem and supplies a low-rank visual grounding signal.

## Quick verdict

* Highly relevant

ORCA is a strong diffusion paper because it names the failure mechanism precisely: the model has access to compositional text structure, but the diffusion objective does not directly ground that structure in visual composition. The auxiliary loss is training-only, so there is no inference tax. The caveat is that the reported regime is still MS-COCO 256 and GenEval-scale compositional evaluation, not a full proof that the approach handles arbitrary scene graphs.

## One-paragraph overview

Text-to-image diffusion models often fail on binding: colors attach to the wrong objects, spatial relations invert, and object counts drift. ORCA argues that this is not simply because text encoders lack information; modern architectures already add T5 because CLIP drops compositional structure. The problem is that the diffusion latent is not trained to align T5's extra structure with visual composition. ORCA adds an auxiliary loss at an intermediate diffusion block. It builds a low-rank PCA target from frozen DINOv2 features, uses the residual between T5 and CLIP embeddings to parameterize an orthogonal projection, and aligns the diffusion latent to that visual subspace. On DiT-L/2, ORCA reaches FID 16.65 and GenEval 0.291 at 200K steps, outperforming REG at the same budget and vanilla/REPA 400K baselines.

## Model definition

### Inputs

The diffusion model trains on MS-COCO image-caption pairs at 256x256. Conditioning includes frozen CLIP and T5 text embeddings. ORCA also uses clean-image DINOv2 features to build the auxiliary target during training.

### Outputs

The base model outputs the usual diffusion or rectified-flow velocity/noise prediction in latent image space. ORCA's auxiliary head outputs a projected representation of an intermediate diffusion hidden state that should match the low-rank DINOv2 target.

### Training objective (loss)

The base loss is the standard velocity-matching objective for rectified-flow diffusion in a frozen autoencoder latent space. ORCA adds a mean-squared auxiliary alignment loss between the projected intermediate hidden state and the PCA-compressed frozen DINOv2 visual target. Inference is unchanged.

### Architecture / parameterization

The main experiments use diffusion transformer backbones DiT-B/2, DiT-L/2, and U-ViT-L. ORCA adds a learned linear T5-to-CLIP projection, computes the residual between projected T5 and CLIP embeddings, feeds that residual into a small MLP, orthonormalizes the resulting matrix with QR, and uses it as a text-conditioned low-rank readout from the diffusion latent. The default rank is 64 and the best auxiliary block is intermediate depth.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It targets compositional text-to-image failures: wrong attribute binding, inverted spatial relations, inaccurate counts, and multi-object confusion.

### 2. What is the method?

Add a training-time auxiliary loss that aligns an intermediate diffusion latent with a low-rank target from frozen self-supervised visual features. The readout subspace is prompt-dependent, parameterized by the residual between T5 and CLIP text embeddings.

### 3. What is the method motivation?

CLIP's contrastive objective keeps shared content but discards some syntax and binding. T5 retains more compositional structure, but that structure lives in a language-modeling space. ORCA tries to ground the T5-only residual into visual feature directions that matter for image composition.

### 4. What data does it use?

The main training/evaluation protocol uses MS-COCO at 256x256. The DINOv2 PCA target is estimated from a fixed subset of 5,000 training images, with about 1.28M patch embeddings sub-sampled to 100K for SVD.

### 5. How is it evaluated?

The main metrics are FID-30K for image quality and GenEval for compositional fidelity. The paper reports comparisons across DiT-B/2, DiT-L/2, and U-ViT-L, plus per-category GenEval breakdowns, rank ablations, block-placement ablations, auxiliary-loss weight sweeps, and auxiliary CLIP/PickScore analyses.

### 6. What are the main results?

On DiT-L/2, ORCA reaches FID 16.65 and GenEval 0.291 at 200K steps. REG at 200K reaches FID 18.57 and GenEval 0.258; REPA at 400K reaches FID 20.05 and GenEval 0.275; vanilla at 400K reaches FID 24.01 and GenEval 0.247. At 150K, ORCA's gains concentrate on compositional categories: Position, Color attribution, Two objects, and Counting. Rank 64 is the FID-optimal default, while rank 128 gives slightly higher GenEval but worse FID.

### 7. What is actually novel?

The novelty is using the T5-minus-CLIP residual to parameterize a prompt-dependent orthogonal visual readout, and aligning diffusion latents to a low-rank DINOv2 target specifically to address compositional binding.

### 8. What are the strengths?

The method has zero inference overhead, strong baseline comparisons, clear category-level improvements, and ablations showing the rank, block placement, and loss weight matter. The theory around spectral mass gives a useful reason to expect low-rank saturation.

### 9. What are the weaknesses, limitations, or red flags?

The gains are meaningful but GenEval scores are still low in absolute terms, especially for hard compositional categories. The setup is MS-COCO 256, not a broad real-world generation suite. The paper does not fully establish whether the T5-CLIP residual is always the right carrier of compositional information across larger modern T2I stacks.

### 10. What challenges or open problems remain?

The next challenge is testing richer scene-graph, spatial, and counting benchmarks, plus higher-resolution production backbones. It also needs comparisons to methods that use explicit layout, attention supervision, or synthetic compositional data.

### 11. What future work naturally follows?

Apply the auxiliary target to larger multimodal diffusion transformers. Replace or augment DINOv2 PCA targets with object-centric or relation-centric visual features. Use the residual-subspace diagnostic to measure whether a prompt's compositional content is grounded before sampling.

### 12. Why does this matter for cabbageland?

Cabbageland cares about the difference between adding a module and making the module's information usable. ORCA is a good pattern: find the representation that has the missing structure, then add an explicit alignment objective at the point where the generator can use it.

### 13. What ideas are steal-worthy?

Use residuals between representation systems as diagnostic signals. Keep inference unchanged when possible and pay the alignment cost during training. Ablate the rank and layer placement because "more representation" is not automatically better.

### 14. Final decision

Preserve. This is a strong compositional diffusion note with a mechanism worth remembering.
