# UGG: Unified Generative Geometry Model

## Basic info

* Title: UGG: Unified Generative Geometry Model
* Authors: Amani Kiruga, Zhiyi Li, Ruojin Cai, Hansen Lillemark, Xiaoshan Wu, Ayush Tewari, Yilun Du
* Year: 2026
* Venue / source: arXiv:2611.14440v1; arXiv lists NeurIPS 2026
* Link: https://arxiv.org/abs/2611.14440
* Date surfaced: 2026-11-11
* Why selected in one sentence: A concrete joint RGB-depth-camera model makes generation and geometric prediction different conditional queries, with explicit outputs that can be checked against observed images.

## Quick verdict

* Highly relevant

Preserve the conditional-completion interface and the incomplete-supervision recipe. The strongest results are sparse geometric inference and evidence that appearance generation helps geometry. Do not promote this into a metric, causal, action-conditioned world model: aligned geometry, heuristic search, and independently selected depth/pose are narrower achievements.

**Read basis:** Full-text HTML main paper and selected appendices covering datasets, representation, training, inference, alignment, and verifier rules; official repository README. No training run, checkpoint evaluation, code audit, or independent reproduction. [Project](https://ugg-model.github.io/); [official repository](https://github.com/amanikiruga/UGG). The repository exposes training/inference code and documents release weights; the weights were not downloaded or tested.

## One-paragraph overview

UGG fine-tunes a pretrained video generator into a joint model of appearance, depth, and camera geometry. RGB and depth use VAE latents; cameras become spatially aligned Plucker ray direction/moment maps. Modality-specific transformer branches communicate through shared self-attention. Different noise patterns designate observations and unknowns, so the same model can generate a video given camera motion or infer geometry given a video. Loss masks let real RGB-camera data and synthetic RGB-depth-camera data share training without fabricated missing labels. Multiple stochastic completions can be checked against optical-flow-derived geometric evidence. The important caveat is that depth and pose are ranked independently: the selected outputs need not be one coherent sampled scene.

## Model definition

### Inputs

A sequence with any supported observed subset of RGB frames, depth maps, and camera-ray maps, plus optional text and per-modality/per-time noise levels. Final training uses 50-frame clips at 288 by 384 pixels, sampled at dataset-dependent rates of 8–30 FPS. The implemented training distribution uses five task patterns, not exhaustive training of every conceivable missing-data pattern. Context groups may be clean or noisy during training; observed tokens are clamped clean during inference.

### Outputs

Flow velocities for RGB, depth, ray-direction, and ray-moment tokens. Iterative denoising yields missing RGB/depth sequences and dense ray maps, from which camera rotation, translation, and intrinsics are recovered. Outputs are image-aligned fields and cameras, not object graphs, physical parameters, action policies, or an explicit persistent simulator state.

### Training objective (loss)

For each available modality, interpolate clean latent `z0` and Gaussian noise: `zt = (1-t) z0 + t epsilon`. Regress the flow target `epsilon - z0` with mean-squared error. The main objective weights available modality losses; the implementation appendix averages the four RGB/depth/ray-direction/ray-moment losses and masks those lacking supervision. A shifted diffusion-time schedule uses shift 3.0. Context is exactly clean with probability 0.5; otherwise context and targets receive separately sampled group noise levels.

There is no stated physical-conservation or exact multi-view-consistency constraint in this flow objective. Geometry is supervised and statistically coupled through the network; consistency is not guaranteed by the parameterization.

### Architecture / parameterization

Wan2.2-TI2V-5B initialization, with frozen VAE and text encoder. A mixture-of-transformers arrangement has modality-specific projections, feed-forward processing, and output heads, with shared multimodal self-attention and optional text cross-attention. This is not sparse token routing. The appendix describes 30 transformer layers, hidden size 3072, and 24 attention heads. RGB/depth are VAE encoded; ray fields are packed/projected directly into aligned latent-resolution tokens. New branches copy relevant pretrained weights, with new ray-specific interfaces separately initialized.

Default inference uses 40-step UniPC with history guidance. The paper reports about 20 seconds for one 50-frame denoising loop on an H100/H200; that is not the total cost of generating and scoring 16 hypotheses.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Geometric prediction and visual generation usually expose different architectures and fixed input/output directions. Sparse observations are ambiguous, deterministic predictions discard alternatives, and complete RGB-depth-pose supervision is scarce. UGG asks whether a common scene representation can support both tasks and learn from incomplete datasets.

### 2. What is the method?

Represent every frame by RGB, depth, and camera rays in a shared scene scale. Encode camera pose as per-pixel Plucker direction and moment, which aligns the camera signal with image locations. Train a multimodal flow model with noise acting as a task/missingness interface. At inference, fix observations and denoise the rest.

For search, draw 16 candidates. Use RAFT forward/backward-consistent correspondences, select useful frame pairs, and derive geometric evidence from observed RGB. Depth candidates are aligned to observed parallax and checked through reprojection, with photometric/DINOv2 terms in the dense protocol. Pose candidates are checked against image-estimated relative translation direction using candidate intrinsics. Choose depth and pose separately. If no usable pair survives, the verifier abstains and evaluation scores a uniformly random candidate from the pool.

### 3. What is the method motivation?

RGB, depth, and cameras are complementary observations of the same scene, so conditioning on one should help infer another. A generative representation can retain multiple possible explanations, while explicit geometric fields provide a handle for image-based checking. The useful decomposition is observations, completion, and evidence—not an implicit claim that joint generation automatically enforces physics.

### 4. What data does it use?

A heterogeneous mixture of 14 real/synthetic datasets, including RealEstate10K, DL3DV-10K, TartanAir/V2, Spring, BEDLAM variants, Virtual KITTI 2, Aria Synthetic Environments, OmniWorld-Game, SceneNet RGB-D, MVS-Synth, Mid-Air, and MatrixCity. RealEstate10K and DL3DV contribute RGB and cameras but not depth; many synthetic sources supply richer annotations. Missing labels are masked. Language descriptions or null prompts supply text conditioning.

The paper reports roughly 100K optimizer steps, global batch 1024, and two weeks on 128 H200 GPUs. Large pretrained video priors and substantial additional compute are central dependencies, not incidental implementation details.

### 5. How is it evaluated?

- Camera-controlled generation on RealEstate10K, SpatialVID, and DL3DV with one-frame or first/last-frame RGB context: PSNR, SSIM, LPIPS.
- Dense/sparse camera prediction on RealEstate10K, Sintel, TUM, ScanNetV2, and ScanNet++: ATE, relative translation/rotation errors, and sparse translation angular error.
- Depth on ScanNet++, 7-Scenes, KITTI, Sintel, and Bonn: Abs Rel and threshold accuracy.
- Single-sample prediction, 16-candidate image-based selection, and an explicitly labeled ground-truth oracle over that same pool.
- Smaller Wan2.1-1.3B ablations on task removal, extra partially annotated data, shared versus modality-specific processing, and camera representation.

Depth evaluation uses video-level scale/shift alignment; dense poses use Sim(3) alignment. The verifier's rule sets and motion thresholds are selected leave-one-benchmark-out. It uses no per-instance ground-truth geometry at deployment, but rule development still uses benchmark performance.

### 6. What are the main results?

- Sparse RealEstate10K tAE: UGG 8.260 degrees; Aether 39.834; UGG with search 3.475; same-pool oracle 1.550.
- Dense ScanNet++ ATE: UGG 0.087 versus Geo4D 0.190; search 0.082.
- Sparse ScanNet++ depth Abs Rel: UGG 0.101, search 0.082, oracle 0.055. The remaining oracle gap makes verifier quality a meaningful bottleneck.
- One-view generation leads the listed Aether/SEVA comparisons on all three datasets. Two-view DL3DV is a counterexample: SEVA PSNR 17.61 versus UGG 16.61.
- In the separate small-model ablation, removing RGB generation worsens KITTI depth Abs Rel from 0.152 to 0.322. Adding RGB-camera-only RealEstate10K data improves Bonn depth from 0.239 to 0.135.

Search is not uniformly beneficial: dense 7-Scenes depth Abs Rel changes from 0.083 to 0.084, and some rotation metrics worsen. Main-model results and smaller ablation numbers are different experimental regimes and must not be mixed.

### 7. What is actually novel?

The specific integration of aligned RGB/depth/camera modalities, diffusion-forcing-style conditional completion, incomplete heterogeneous supervision, and evidence-ranked geometric hypotheses. Flow matching, mixture-of-transformers, video pretraining, and diffusion forcing are inherited ingredients. Compare against Aether, Geo4D, Gen3R, camera-conditioned synthesis, and unified 4D generation—not merely generic video models without camera inputs.

### 8. What are the strengths?

A concrete representation and training objective; explicit modality availability rather than invented labels; useful bidirectional transfer between appearance and geometry; multiple datasets and task families; informative task-removal ablations; distinction between deployable selection and oracle selection. Spatially aligned camera conditioning is more legible than hiding all geometry in a global token.

### 9. What are the weaknesses, limitations, or red flags?

- Independent depth/pose selection undermines a strong “one coherent scene” interpretation of searched outputs.
- Alignment can hide absolute scale and affine depth errors that matter downstream.
- Cross-modal attention is learned coupling, not a hard consistency constraint.
- Optical flow, RANSAC, dynamic objects, occlusion, poor parallax, and textureless scenes can corrupt verification. Forward/backward flow checks are not a complete rigidity test.
- Search increases compute substantially; compare quality at matched wall-clock, not only against one-sample feedforward predictions.
- Capacity, pretraining, data mixture, and extra tasks complicate causal attribution. The architectural ablations use a smaller model and limited training.
- Fifty-frame, low-resolution training does not establish persistent long-horizon spatial memory or compositional object dynamics.
- No action-conditioned transitions, planning benchmark, physical transfer, or calibrated uncertainty coverage is established.

### 10. What challenges or open problems remain?

Jointly consistent depth and pose; reliable hypothesis ranking under dynamic scenes and degenerate camera motion; metric scale; calibrated multimodal uncertainty; longer-horizon continuity; distinguishing better scene understanding from better pretrained completion. The oracle gap shows useful alternatives exist but does not prove that their sampling probabilities are meaningful uncertainty estimates.

### 11. What future work naturally follows?

Evaluate a joint geometry verifier against independent selection. Report metric and aligned errors separately. Compare one, four, and sixteen candidates against compute-matched deterministic/iterative baselines. Stress-test moving objects, low texture, occlusion, and out-of-domain cameras. Add persistent scene state or action inputs only with tests that isolate whether they improve physical prediction and downstream decisions.

### 12. Why does this matter for cabbageland?

This is a strong baseline/design reference for generative scene models with an explicit geometric interface. The reusable idea is to make perception and synthesis query the same representation while retaining outputs that independent evidence can challenge. It earns structured generative geometry—not a sweeping world-understanding claim.

### 13. What ideas are steal-worthy?

- Use noise/missingness patterns as an input-output interface across modalities.
- Preserve annotation-availability masks in the objective instead of forcing every dataset through fabricated supervision.
- Spatially align global-looking controls, such as cameras, with the signals they constrain.
- Measure candidate diversity and verifier headroom separately using a same-pool oracle.
- Make abstention and joint-output consistency explicit when a verifier cannot establish a reliable choice.

### 14. Final decision

Preserve as a highly relevant joint geometry/generation baseline. Prioritize the conditional-query mechanism and incomplete-data training recipe; the first follow-up should test joint depth-pose selection at a matched inference budget. Do not cite its aligned geometry or best-of-16 gains as evidence of metric reconstruction, physical simulation, uncertainty calibration, or planning success.
