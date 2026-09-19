# SplashSplat: Reconstructing Splashing Liquids from Real-World Multi-View Videos

## Basic info

* Title: SplashSplat: Reconstructing Splashing Liquids from Real-World Multi-View Videos
* Authors: Peiyu Liu, Dingxi Zhang, Federico Tombari, Marc Pollefeys, Christina Tsalicoglou, Daniel Barath
* Year: 2026
* Venue / source: arXiv:2609.20818
* Link: https://arxiv.org/abs/2609.20818
* Date surfaced: 2026-09-19
* Why selected in one sentence: It builds a real multi-view benchmark for splashing liquids and uses observed interface geometry plus kinematic transport instead of unconstrained dynamic Gaussians.

## Quick verdict

* Useful

This is a useful 3D/dynamic reconstruction paper. It is adjacent rather than central for cabbageland, but the method has good taste: it constrains the representation with observable physics and admits where full fluid state is not recoverable. This note is based on the full arXiv PDF text.

## One-paragraph overview

SplashSplat targets a difficult reconstruction regime: real splashing liquid, where surfaces are weakly textured, view-dependent, short-lived, and hard to track. The paper introduces a 20-scene real benchmark captured with seven synchronized calibrated 4K cameras at 60 fps. The method fuses per-view liquid masks into per-frame SDFs, estimates a coarse velocity field through level-set transport, advects Lagrangian carriers, corrects them against new observations, reseeds where coverage is lost, and decodes local Gaussians for differentiable rendering.

## Model definition

### Inputs

Inputs are synchronized multi-view RGB videos, calibrated cameras, per-view liquid and container masks, scanned container meshes, and per-frame mask-fused liquid SDFs.

### Outputs

The method outputs novel-view renderings of the dynamic liquid, an estimated velocity field, carrier trajectories, local Gaussian primitives, and derived outputs such as temporal interpolation and style transfer.

### Training objective (loss)

The paper optimizes differentiable rendering losses, including photometric reconstruction terms, a DSSIM term on mask bounding boxes, mask/silhouette consistency, opacity modulation by the observed SDF, and regularizers tied to the carrier/transport representation. The exact optimization is reconstruction-time fitting, not a general pretrained model.

### Architecture / parameterization

SplashSplat represents liquid through SDF-constrained Lagrangian carriers. Each carrier holds a feature decoded by linear heads for offset, scale, and opacity plus a small color MLP conditioned on viewing direction; in the reported implementation each carrier has a 32-dimensional feature and decodes K = 2 Gaussian children.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Existing dynamic Gaussian methods can reconstruct textured dynamic scenes, but splashing liquids have weak texture, rapid topology changes, view-dependent appearance, and unobserved boundary conditions. They often fit images without recovering plausible motion.

### 2. What is the method?

SplashSplat imposes only physically motivated constraints that the images can support: observed SDF geometry, approximate level-set transport, incompressibility-biased velocity fitting, Lagrangian carrier advection, correction, and resampling.

### 3. What is the method motivation?

A full fluid simulator would need hidden boundary conditions and volume information that images do not reveal. Pure dynamic Gaussians are too unconstrained. SplashSplat chooses a middle path: use observed interface geometry to constrain motion, then use rendering optimization for fine appearance.

### 4. What data does it use?

The new benchmark has 20 real scenes recorded by seven GoPro cameras at 3840 x 2160 and 60 fps, with synchronized calibrated views, refined liquid/container masks, and scanned container meshes. The paper also evaluates on NeuroFluid WaterSphere.

### 5. How is it evaluated?

It reports foreground novel-view synthesis metrics, temporal jitter error, physical-plausibility proxies, training time, and memory. Baselines include Deformable-3DGS, SpacetimeGaussians, and 4D-Scaffold-GS.

### 6. What are the main results?

On the real benchmark, SplashSplat reaches 20.13 PSNR, 0.9570 SSIM, 0.0806 LPIPS, 0.0276 jitter error, density-deviation proxy 219.9, energy-deviation proxy 0.373, 37.8 minutes training time, and 5.31 GiB memory. The closest photometric baseline, 4D-Scaffold-GS, reaches 18.92 PSNR, 0.9552 SSIM, 0.0898 LPIPS, 0.0428 jitter error, and worse physical proxies at higher memory.

### 7. What is actually novel?

The benchmark is a real contribution: synchronized multi-view splashing-liquid video is rare. The method's novelty is the observed-SDF plus velocity-transport plus carrier-correction loop, which constrains dynamic Gaussians with kinematics without pretending to solve full fluid simulation.

### 8. What are the strengths?

The paper has a good constraint philosophy, reports efficiency, compares against strong dynamic Gaussian baselines, and exposes a hard real-data regime where unconstrained visual fitting fails.

### 9. What are the weaknesses, limitations, or red flags?

The dynamics are kinematic and observation-bound, not complete physical state. Thin droplets can be missed by mask-derived SDFs. The benchmark requires a controlled multi-camera setup and masks, so the method is not a casual monocular reconstruction pipeline.

### 10. What challenges or open problems remain?

Recovering unobserved interior velocity, handling missed thin structures, relaxing mask dependence, and connecting the reconstruction to predictive simulation remain open.

### 11. What future work naturally follows?

Use the benchmark to test learned fluid priors, combine carrier transport with predictive world models, and explore uncertainty over hidden fluid state rather than a single fitted motion.

### 12. Why does this matter for cabbageland?

Cabbageland cares about models that use explicit structure where it actually does work. SplashSplat is a concrete example of matching the representation to the observable physics instead of letting a flexible neural renderer hallucinate motion.

### 13. What ideas are steal-worthy?

Constrain motion with observable geometry before fitting appearance. Correct and reseed state against new observations. Report physical plausibility and efficiency beside rendering metrics.

### 14. Final decision

Preserve as adjacent inspiration. The benchmark and constraint philosophy are worth remembering.
