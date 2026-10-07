# DepthWorld: 3D World Model for Robot Manipulation

## Basic info

* Title: DepthWorld: 3D World Model for Robot Manipulation
* Authors: Jai Bardhan, Josef Sivic, Vladimir Petrik
* Year: 2026
* Venue / source: arXiv; accepted at CoRL 2026
* Link: https://arxiv.org/abs/2610.08780
* Date surfaced: 2026-10-07
* Why selected in one sentence: It shows that robot video world models improve when dense metric depth is part of the predicted state rather than an afterthought.

## Quick verdict

* Highly relevant

This is the one robotics paper worth preserving today. It clears the higher bar because the contribution is not just another VLA wrapper; it builds a calibrated 3D supervision source and changes the world-model output so RGB rollouts compose with metric depth. The limitation is that the model is still autoregressive and evaluated as a predictive world model, not as a complete closed-loop robot policy.

## One-paragraph overview

DepthWorld has two pieces. First, DROID-3D recalibrates the DROID robot teleoperation dataset into a dense RGB-D corpus with robot-grounded multi-view extrinsics by combining learned stereo depth, dense matching, URDF rendering, and a joint factor graph over each robot's episodes. Second, DepthWorld trains a Stable Video Diffusion-based action-conditioned world model to predict multi-view RGB and depth together. The architectural trick is spatial latent tiling: RGB and depth are VAE-encoded separately and placed side by side in a wider latent grid, preserving the pretrained VAE and U-Net priors. Joint RGB-depth training improves RGB prediction by +1.48 dB PSNR on external views and +1.02 dB on wrist views over an RGB-only baseline, while producing metric depth for geometric reasoning.

## Model definition

### Inputs

DepthWorld consumes multi-view robot history with RGB and metric depth for two external cameras and one wrist camera, plus per-frame end-effector pose / action conditioning. The training data comes from DROID-3D, which supplies dense metric depth and calibrated camera extrinsics in the robot base frame.

### Outputs

The model predicts future multi-view RGB and metric depth rollouts. The PM-DPT variant also predicts robot-frame 3D point maps and confidence logits for future frames and views.

### Training objective (loss)

The base objective is the Stable Video Diffusion denoising loss on the joint spatially tiled RGB-depth latent. The PM-DPT variant adds a confidence-weighted robust point-map loss in robot base coordinates, using ground-truth point maps from depth backprojection through calibrated intrinsics and extrinsics. Training is staged: 40,000 steps for joint RGB-depth denoising, then 50,000 additional steps with the point-map head.

### Architecture / parameterization

The model starts from the Stable Video Diffusion checkpoint used by Ctrl-World, with identical action conditioning. RGB and depth tiles for three cameras are encoded by the unmodified SVD VAE and tiled into a 72 by 80 latent grid per timestep. The SVD U-Net denoises an 11-frame temporal window. A lightweight DPT head initialized from VGGT can read predicted RGB-depth latents and emit point maps.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

RGB-only robot world models can produce plausible frames that do not compose into a consistent 3D scene. That makes their rollouts weak for occlusion, contact, planning, and policy evaluation.

### 2. What is the method?

First, recalibrate DROID into DROID-3D with dense metric depth and robot-grounded extrinsics. Second, train a depth-aware action-conditioned video world model using spatial latent tiling and optional robot-frame point-map supervision.

### 3. What is the method motivation?

Downstream robot use needs geometry. If depth is not supervised, the video model can satisfy RGB losses while losing object shape, cross-view agreement, and robot-scene spatial relationships.

### 4. What data does it use?

The paper processes DROID's raw 71k-trajectory release from 13 institutions, covering 28 robots and 13 labs after filtering. Calibration is evaluated on about 1,000 scenes from five labs. World-model evaluation uses 256 held-out DROID trajectories with 10 consecutive autoregressive rollouts.

### 5. How is it evaluated?

Calibration is evaluated with external-external and wrist-external reprojection error, robot depth error, and robot mask IoU. World-model quality is evaluated with RGB PSNR, SSIM, LPIPS, depth AbsRel, RMSE, delta-1, cross-view reprojection, generated-depth agreement, and comparisons with PointWorld and an adapted TesserAct.

### 6. What are the main results?

DROID-3D improves calibration strongly over a PointWorld-style per-scene baseline: external-external median reprojection error drops from 5.84 px to 0.25 px, wrist-external from 13.19 px to 1.03 px, robot depth error from 111.3 mm to 14.0 mm, and mask IoU from 0.440 to 0.810. For world modeling, joint RGB-depth prediction raises external PSNR from 22.63 to 24.09 and wrist PSNR from 16.98 to 17.96. PM-DPT maintains RGB quality while improving wrist depth metrics slightly, reaching wrist AbsRel 0.2182 and delta-1 0.8210.

### 7. What is actually novel?

The novelty is the combination of dataset-level robot-grounded recalibration and a minimal depth integration path that preserves pretrained video priors. Spatial latent tiling is a practical way to add geometry without destructive channel expansion or a separate depth U-Net.

### 8. What are the strengths?

The calibration pipeline solves a real bottleneck for geometric supervision in robot data. The ablations show that bad depth targets can actively hurt RGB prediction, which is an important warning. The model predicts depth natively, so geometry is available during rollout rather than estimated afterward.

### 9. What are the weaknesses, limitations, or red flags?

DepthWorld is still an autoregressive rollout model and inherits exposure bias and quality degradation. Wrist-view depth remains much harder than external-view depth because of motion, proximity, and occlusion. The paper shows predictive improvements, not closed-loop robot policy improvements.

### 10. What challenges or open problems remain?

The next challenge is using the 3D outputs for planning, policy improvement, and geometric rewards. Another is enforcing stricter spatiotemporal 4D consistency instead of improving per-rollout RGB-depth quality.

### 11. What future work naturally follows?

Use DROID-3D to train world models with explicit object permanence, contact, and uncertainty. Add geometric consistency losses across time, and test whether native depth rollouts improve model-predictive control or policy reranking.

### 12. Why does this matter for cabbageland?

This is exactly the difference between pretty prediction and usable state. DepthWorld makes geometry part of the generated state, which is the kind of explicit structure a downstream planner can actually inspect.

### 13. What ideas are steal-worthy?

Add missing state through supervision, not post-hoc interpretation. Preserve pretrained priors by tiling modalities in latent space when possible. Treat calibration as part of the model pipeline, not as boring dataset plumbing.

### 14. Final decision

Preserve. This is a strong robotics/world-model paper because the mechanism is geometric state, not agent branding.

