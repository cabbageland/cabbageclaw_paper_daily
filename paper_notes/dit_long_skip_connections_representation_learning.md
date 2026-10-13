# Why DiT Models Underperform as Representation Learners without Long Skip Connections

## Basic info

* Title: Why DiT Models Underperform as Representation Learners without Long Skip Connections
* Authors: Benyuan Meng, Yiliang Zhang, Jin-Wen Wu, Qianqian Xu, Qingming Huang, Longtao Huang
* Year: 2026
* Venue / source: NeurIPS 2026 / arXiv
* Link: https://arxiv.org/abs/2610.13344
* Date surfaced: 2026-10-13
* Why selected in one sentence: It gives a concrete mechanism for why DiT features degrade and why long skip connections can separate denoising noise from reusable image representation.

## Quick verdict

* Must read

This is a mechanism-rich diffusion architecture paper. Its value is not merely that LSCs help DiTs; the useful part is the claim that skip paths route diffusion noise around the target-reconstruction section. The empirical evidence is controlled enough to be useful, though the mechanism is still partly inferential and tested on conventional DiT rather than every modern MMDiT-style backbone.

## One-paragraph overview

The paper studies why DiT backbones can generate well while producing weaker intermediate features for perception tasks than U-Net diffusion backbones. The authors train controlled DiT variants with and without long skip connections, evaluate their features on semantic correspondence, segmentation, and depth tasks, then probe the internal flow of target information and diffusion noise. They argue that a diffusion backbone internally reconstructs a clean target representation before predicting noise or velocity. Without LSCs, diffusion-noise information has to pass through this target-reconstruction stream, polluting reusable features. With LSCs, that noise can bypass the middle stream and re-enter near the prediction section.

## Model definition

### Inputs

The diffusion backbone receives latent image variables, diffusion timestep, conditioning text/class information when relevant, and diffusion noise through the noisy latent. Feature extraction receives images and selected timesteps.

### Outputs

The diffusion model predicts the diffusion target, usually noise or velocity. For representation evaluation, intermediate activations are extracted as dense visual features and fed to downstream tasks such as semantic correspondence, semantic segmentation, and depth estimation.

### Training objective (loss)

The controlled models use a diffusion/flow-matching-style mean-squared error objective for predicting the velocity/noise target. Downstream heads use task-specific losses, while the training-free correspondence setting directly evaluates features. Mutual-information probes estimate how much target information and diffusion-noise information appears in activations.

### Architecture / parameterization

The base model is DiT-XL/2. The LSC variant folds the DiT chain conceptually in half and concatenates a skip activation into later layers, followed by normalization and a linear projection. The paper compares DiTs with and without these long skip paths.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It asks why Diffusion Transformers can be strong generators but weak representation learners when intermediate activations are reused as vision features.

### 2. What is the method?

The authors run controlled from-scratch training on ImageNet-256 with and without LSCs, evaluate feature quality across six settings, measure correlation decay, use mutual-information probing, and run causal intervention experiments that replace skip-carried signals with high-frequency image content and/or diffusion noise.

### 3. What is the method motivation?

The standard "DiT features are bad because of massive activations" explanation is incomplete. LSCs are known to improve DiT generation, but the paper wants a representation-level mechanism, not just an engineering recipe.

### 4. What data does it use?

Training uses ImageNet-256. Feature evaluation uses SPair-71k for semantic correspondence, Horse-21 and CityScapes for segmentation, and NYU Depth v2 for depth estimation.

### 5. How is it evaluated?

Generation is evaluated with FID under CFG 1.5. Representation quality is evaluated with PCK@0.1 on SPair, mIoU on segmentation, and d1 on depth estimation. The paper also uses correlation decay slope, mutual-information estimates, and controlled signal-injection experiments.

### 6. What are the main results?

With LSCs, FID improves from 20.87 to 14.39. SPair(a) improves from 34.68 to 41.10, SPair(b) from 52.62 to 60.68, Horse-21 mIoU from 30.35 to 36.32, CityScapes from 50.22 to 51.55, and depth d1 from 0.70 to 0.74. A shorter LSC run with roughly aligned FID still beats the no-LSC model on most representation metrics, suggesting the feature improvement is not just better generation. Mutual-information probing shows LSCs reduce diffusion-noise content and increase target information in the middle layers. The intervention experiments suggest both high-frequency semantics and diffusion-noise routing matter.

### 7. What is actually novel?

The novel contribution is the diffusion-noise bypass hypothesis: LSCs are not merely shortcutting image edges; they route denoising-trajectory information around the target-reconstruction section, keeping the middle representation cleaner.

### 8. What are the strengths?

The paper is unusually useful because it connects an architectural choice to the diffusion objective. It also tests feature quality across multiple tasks instead of only reporting generation metrics. The controlled FID-aligned comparison makes the representation claim more credible.

### 9. What are the weaknesses, limitations, or red flags?

The causal mechanism is supported but not fully proven. The authors could not effectively retrofit existing pretrained DiTs with LSCs. The controlled experiments use conventional DiT, leaving MMDiT and many modern production backbones underexplored. The intervention experiment can cause collapse, which makes interpretation somewhat messy.

### 10. What challenges or open problems remain?

The main open problem is how to adapt pretrained DiTs without full retraining. Another is whether modern multimodal diffusion transformers have analogous noise-routing failure modes or already solve them through other paths.

### 11. What future work naturally follows?

Test LSC-like routing in MMDiT, video DiT, and 3D/4D diffusion backbones. Develop retrofit adapters that give pretrained models a noise bypass. Evaluate whether cleaner middle representations improve controllability, editing, and world-model state reuse.

### 12. Why does this matter for cabbageland?

Cabbageland cares about reusable representations inside generative models. This paper says the architecture must keep denoising bookkeeping from contaminating the representation stream, which is exactly the kind of mechanism that matters for compositional world models.

### 13. What ideas are steal-worthy?

Separate target reconstruction from trajectory/noise bookkeeping. When using generative backbones as perception backbones, inspect what information each stream is forced to carry. Treat skip connections as routing constraints, not cosmetic residual plumbing.

### 14. Final decision

Preserve. It is a strong architectural mechanism note and useful framing for future diffusion-world-model design.
