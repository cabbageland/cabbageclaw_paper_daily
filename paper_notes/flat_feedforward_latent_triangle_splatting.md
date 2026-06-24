# FLAT: Feedforward Latent Triangle Splatting for Geometrically Accurate Scene Generation

## Basic info

* Title: FLAT: Feedforward Latent Triangle Splatting for Geometrically Accurate Scene Generation
* Authors: Orest Kupyn, Goutam Bhat, Philipp Henzler, Fabian Manhardt, Christian Rupprecht, Federico Tombari
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.24876
* Date surfaced: 2026-06-24
* Why selected in one sentence: It tries to decode video-diffusion latents into explicit surface primitives instead of accepting volumetric 3D Gaussian blobs as the final scene representation.

## Quick verdict

* Highly relevant

This is the strongest 3D/generative-media paper in today's scan. I inspected the full arXiv PDF, especially the triangle parameterization, renderer/window function, losses, evaluation tables, ablations, mesh conversion, and limitations. The paper is not perfect, but it makes a real representation argument: if a generated scene is meant for simulation or graphics pipelines, the output representation should look more like a surface.

## One-paragraph overview

FLAT starts from the observation that modern video diffusion latents contain useful multiview scene information, but most feedforward latent scene decoders output 3D Gaussian-style volumetric blobs. Those blobs render well, but they do not define clean surfaces and are awkward for game engines, simulation, and mesh workflows. FLAT instead predicts triangle splats directly from video latents in one feedforward pass. Its core tricks are a ray-centered local triangle parameterization, a Cholesky-style shape transform that avoids degenerate triangles, residual rotations around a ray-aligned frame, and a product window function that improves gradient flow for differentiable triangle rendering. A lightweight post-processing pass converts the semi-opaque triangle soup into a more opaque mesh-like representation.

## Model definition

### Inputs

Inputs are a single source image, generated or real multiview video frames/latents, camera trajectories, Plucker ray embeddings, and training-time pseudo-ground-truth depth and surface normals. The scene decoder uses denoised Wan-2.1 / Uni3C-style video latents plus camera/ray conditioning.

### Outputs

The model outputs a set of triangle splats. Each triangle has geometry, color, opacity, and sharpness parameters. The system can render novel views and can optionally post-process the semi-opaque triangles into an opaque, game-engine-compatible triangle representation.

### Training objective (loss)

FLAT uses a weighted combination of photometric and geometry losses: pixel-wise L2, LPIPS perceptual loss, scale-invariant disparity depth loss, rendered-normal supervision against pseudo-ground-truth normals, and opacity regularization. The paper gives the full objective as a weighted sum with lambda_rgb = 1.0, lambda_perc = 0.5, lambda_D = 0.01, lambda_N = 0.01, and lambda_O = 0.001.

### Architecture / parameterization

The scene decoder reuses a Wan-2.1 VAE-style decoder backbone and adds heads that predict triangle parameters instead of RGB pixels. Each local image region predicts a ray-centered triangle. The triangle center is placed along the anchor ray by predicted depth; shape comes from a constrained lower-triangular transform applied to a canonical equilateral triangle; orientation is represented through residual rotations in a ray-tangent frame. Rendering uses a differentiable triangle splatting formulation with a product window function.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Single-image-to-3D scene generation wants both strong generative priors and usable geometry. Video diffusion models provide the prior, but a video is not a scene asset. 3D Gaussian decoders can turn latent views into renderable representations, but the result is volumetric and surface-ambiguous. FLAT asks whether compressed video latents can be decoded directly into explicit surface primitives.

### 2. What is the method?

The method generates or uses multiview video latents, fuses them with camera/ray embeddings, and decodes them into triangle splats. The decoder predicts triangle depth, local 2D shape parameters, residual orientation, color, opacity, and sharpness. A differentiable renderer supervises the predicted triangles against target views, depths, and normals. For downstream use, a short optimization and pruning stage makes the triangles more opaque and connected.

### 3. What is the method motivation?

The motivation is that representation choice matters. A Gaussian blob can hide geometry errors while scoring well on RGB rendering metrics. A triangle is harder to predict, but it forces the model toward a surface-like object that downstream graphics and simulation systems can actually consume.

### 4. What data does it use?

Training uses a mixture of real and synthetic videos. Real videos come from RealEstate10K and DL3DV, with RealCam-Vid camera annotations. Synthetic data includes 25,000 S3OD object-centric images converted into videos with Uni3C camera motions, plus regenerated videos from RealEstate10K and DL3DV first frames and trajectories. Metric camera poses and depths are predicted with MapAnything, and pseudo-ground-truth normals are predicted with NormalCrafter.

### 5. How is it evaluated?

The paper evaluates feedforward 3D scene generation on RealEstate10K and DL3DV. It compares FLAT variants using 3DGS, 2DGS, and triangles under matched training conditions, plus prior state-of-the-art systems. Metrics include PSNR, SSIM, LPIPS, normal L1, normal cosine similarity, and mesh-conversion quality. The ablation table isolates architecture, window function, triangle representation, and rotation parameterization.

### 6. What are the main results?

The triangle representation gets worse RGB rendering metrics than the best Gaussian variant but much better geometry. Averaged over RealEstate10K and DL3DV, FLAT triangles reach normal cosine similarity 0.853, compared with 0.587 for 2DGS and 0.116 for 3DGS. For opaque mesh conversion, triangle outputs reach 21.23 PSNR on RealEstate10K versus 15.89 for 2DGS TSDF and 14.18 for 3DGS GS2Mesh, with far fewer vertices. The ablations show the parameterization matters: global rotation collapses to near-empty/noisy renders, and reverting the triangle window function or representation weakens performance.

### 7. What is actually novel?

The novelty is not "use triangles" in isolation. The useful novelty is showing a viable feedforward path from video diffusion latents to explicit non-volumetric surface primitives, and identifying the parameterization and renderer changes needed to make triangle prediction trainable.

### 8. What are the strengths?

The representation argument is clean. The paper compares 3DGS, 2DGS, and triangles under the same pipeline, so the geometry difference is not just a product of unrelated training choices. The ablation table is also useful because it shows that stable triangle decoding depends on the combination of ray-centered parameterization, residual rotation, and the window function.

### 9. What are the weaknesses, limitations, or red flags?

Triangles are less forgiving than Gaussians. FLAT struggles with thin elongated structures, reflections, semi-transparent regions, and high-frequency details. The converted mesh is not a clean watertight mesh; local connectivity can be incomplete, oversharpened, or fragmented. The method also inherits sparse-view ambiguity from the single input image and generated trajectory, and the authors acknowledge the model is trained with much less data than modern video generators.

### 10. What challenges or open problems remain?

The open problem is turning generated latent scenes into dense, coherent, watertight geometry without giving up generative flexibility. Another challenge is evaluating geometry in a way that does not over-reward smooth blobs or punish explicit surfaces for being less photometrically forgiving.

### 11. What future work naturally follows?

A strong follow-up would combine FLAT-style explicit surface decoding with stronger view coverage and a repair stage that enforces topological consistency. Another useful direction is testing whether triangle outputs improve downstream robotics, simulation, planning, or interactive editing compared with Gaussian scene assets at matched visual quality.

### 12. Why does this matter for cabbageland?

Cabbageland cares about world models and scene generators that expose usable state. FLAT is a reminder that a pretty video or Gaussian render is not necessarily a world representation. If the downstream user needs collision, editing, simulation, or persistent geometry, the scene representation has to carry surface structure explicitly.

### 13. What ideas are steal-worthy?

Use video diffusion latents as a prior, but decode them into the representation the downstream system needs. Compare representations under matched training conditions. Penalize representation choices that hide geometry errors behind RGB metrics. Use local ray-centered parameterizations when direct world-space prediction is unstable. Treat mesh conversion as part of the evaluation, not a decorative demo.

### 14. Final decision

**Keep it.** FLAT is not the final answer to generated 3D scenes, but it is a strong representation paper. It earns the surface-geometry claim because the representation changes the object the model has to predict and the evaluation checks that geometry directly.
