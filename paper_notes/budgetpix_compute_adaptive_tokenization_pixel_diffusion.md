# BudgetPix: Compute-Adaptive Tokenization for Pixel-Space Image Diffusion

## Basic info

* Title: BudgetPix: Compute-Adaptive Tokenization for Pixel-Space Image Diffusion
* Authors: Ozgur Kara, Yujia Chen, Daniel Watson, David Forsyth, James Matthew Rehg, Wen-Sheng Chu, Du Tran
* Year: 2026
* Venue / source: arXiv preprint
* Link: https://arxiv.org/abs/2610.12307
* Date surfaced: 2026-10-10
* Why selected in one sentence: It makes pixel-space diffusion operate across variable, content-adaptive token budgets from one fine-tuned checkpoint.

## Quick verdict

* Highly relevant

BudgetPix is a strong diffusion-systems paper because it turns compute into a meaningful control surface. It is not just pruning or token merging bolted on after training; the model is adapted to non-uniform layouts and has a decoder/refiner that can reconstruct fixed-resolution images from multi-scale tokens. The limitation is real: inference layouts come from intermediate predictions, so early blind spots can still decide where compute is spent.

## One-paragraph overview

Pixel-space diffusion transformers avoid autoencoder reconstruction limits but pay heavily for uniform token grids. BudgetPix replaces uniform tokenization with an entropy-guided quadtree layout that assigns fine tokens to high-complexity regions and coarse tokens to low-complexity regions. A multi-scale encoder embeds non-uniform patches, a scale-aware decoder reconstructs full-resolution images, and the diffusion transformer is fine-tuned to handle variable token counts. At inference, a few warm-up denoising steps estimate a clean image, which determines the adaptive layout. The result is a single checkpoint that can trade quality for speed across a wide budget range.

## Model definition

### Inputs

The model receives noisy image states during denoising, optional class or text conditioning depending on the parent model, and a content-adaptive patch layout. During training the layout is derived from the ground-truth image; during inference it is derived from an intermediate predicted clean image after warm-up steps, or randomized for one-step MeanFlow settings.

### Outputs

The denoiser predicts the usual diffusion or flow denoising target over variable-length multi-scale token sequences. The decoder reconstructs a fixed-resolution image from those tokens.

### Training objective (loss)

BudgetPix retains the parent pixel-space diffusion or flow-matching objective while fine-tuning the model over variable layouts and token counts. The inspected text states that the method adapts pixel-space denoisers through flexible training and sampling schedules; it does not replace the parent objective with a new generative loss.

### Architecture / parameterization

BudgetPix adds an entropy-guided quadtree encoder, multi-scale patch embeddings, a scale-aware decoder/refiner, and layout-aware training/inference around existing pixel-space diffusion transformer backbones. It is tested with JiT, MiniT2I, PixelDiT, and pixel MeanFlow.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Pixel-space diffusion transformers have fixed uniform token grids, so cost is rigid and often wasted on low-detail image regions. The paper asks how to make one pixel-space model operate at multiple compute budgets without training separate checkpoints.

### 2. What is the method?

BudgetPix builds a non-uniform image layout using entropy-guided recursive quadtree splitting. High-entropy regions keep fine patches; low-entropy regions are represented by coarser patches. A multi-scale encoder converts those patches into tokens, the transformer denoises the variable-length sequence, and a decoder/refiner reconstructs the fixed-resolution image. Inference estimates the layout from the model's own intermediate clean prediction.

### 3. What is the method motivation?

Visual information density is not uniform. A flat sky and a detailed object should not receive identical token budgets. Prior token merging is brittle for generation because it adapts after features exist, while a denoiser has to create the image through the layout.

### 4. What data does it use?

Experiments cover ImageNet class-conditional generation for JiT and MeanFlow, plus text-to-image generation with MiniT2I at 512 squared and PixelDiT at 1024 squared. Metrics include FID-50k, Inception Score, GenEval, DPG-Bench, CLIP similarity, PickScore, ImageReward, paired faithfulness metrics, human studies, VLM-as-judge, and wall-clock speed.

### 5. How is it evaluated?

The key evaluation varies token budget from dense 100% down to 25%, comparing BudgetPix against the base model run at reduced budgets, ToMe, feature-similarity merging, and RTI where applicable. The paper measures both absolute generation quality and faithfulness to each method's own full-budget output.

### 6. What are the main results?

On PixelDiT-T2I at 1024 squared, BudgetPix gets GenEval 0.725 and DPG-Bench 83.7 at 25% budget, while the base model at 25% gets GenEval 0.323 and DPG-Bench 55.1; the dense base model is 0.721 and 84.8. On MiniT2I-L at 512 squared, BudgetPix keeps GenEval around 0.874 at 25%, while the base model collapses to 0.017. On JiT-L/32 ImageNet at 512 squared, BudgetPix FID rises from 2.71 at 100% to 4.41 at 60% and 11.54 at 25%, while the base model rises from 2.66 to 15.51 and 107.51. Human raters can cut 52% of BudgetPix compute before seeing a difference, versus at most 38% for baselines.

### 7. What is actually novel?

The novelty is making non-uniform, content-adaptive tokenization native to pixel-space generation across training and inference, rather than applying post-hoc merging to a model trained only on uniform grids.

### 8. What are the strengths?

The method is architecture-portable across several pixel-space backbones, works for class-conditional and text-to-image settings, and is complementary to few-step generation because it reduces cost per step. The evaluation includes both automatic metrics and faithfulness/user judgments, which helps avoid hiding artifacts behind aggregate scores.

### 9. What are the weaknesses, limitations, or red flags?

The layout is derived from intermediate predictions, so it can miss details that are not visible yet. The method requires fine-tuning the model, not just dropping in a test-time wrapper. Full-resolution stages in some parent systems can still dominate cost. The entropy layout is a blunt proxy for semantic importance; a low-entropy region can still be semantically critical.

### 10. What challenges or open problems remain?

A better layout policy would combine visual complexity with semantic or prompt relevance. Another challenge is making the layout adapt during the reverse process without destabilizing identity and composition.

### 11. What future work naturally follows?

Learn the layout policy, condition it on prompt semantics, update it dynamically over denoising time, and use the same compute-adaptive idea for video or 3D generation where token budgets are even more painful.

### 12. Why does this matter for cabbageland?

Cabbageland cares about controllable generative systems and efficient structure. BudgetPix gives a concrete mechanism for allocating generation compute according to spatial complexity rather than pretending every patch deserves equal attention.

### 13. What ideas are steal-worthy?

Make budget a first-class inference control. Use multi-scale layouts that tile the output exactly. Train the model on the layouts it will see at inference. Evaluate budget reduction with faithfulness to the dense output, not only standalone quality metrics.

### 14. Final decision

Preserve. This is a practical diffusion mechanism paper with a clean efficiency/control lesson.
