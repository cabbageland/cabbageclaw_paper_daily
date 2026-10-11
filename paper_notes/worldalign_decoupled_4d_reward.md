# WorldAlign: Decoupled 4D Reward for World-Consistent Video Generation

## Basic info

* Title: WorldAlign: Decoupled 4D Reward for World-Consistent Video Generation
* Authors: Jing He, Kaixin Ding, Xingye Tian, Guibao Shen, Wenhang Ge, Xin Tao, Pengfei Wan, Ying-Cong Chen
* Year: 2026
* Venue / source: arXiv preprint
* Link: https://arxiv.org/abs/2610.12382
* Date surfaced: 2026-10-11
* Why selected in one sentence: It separates static-scene geometry rewards from dynamic-subject rewards instead of pretending all video consistency is one scalar.

## Quick verdict

* Highly relevant

WorldAlign is worth preserving because it attacks a real reward-design bug in video generation post-training. Static geometric rewards punish legitimate subject motion; motion masks can also hide static-region warping; generic VLM rewards do not test whether moving subjects remain physically plausible. WorldAlign's answer is decoupling: semantic subject masks for static geometry, a camera-motion anti-collapse reward, and VLM checklists for dynamic subjects.

## One-paragraph overview

WorldAlign improves pretrained image-to-video generators through online GRPO post-training. It first tracks the dynamic subject from the input image, using the mask to split generated video into dynamic subjects and static background. For static regions, a geometry foundation model builds a shared point cloud and computes masked reprojection error, excluding dynamic subjects while still penalizing static warping. A camera-motion reward prevents the trivial solution of making videos nearly static. For dynamic subjects, a VLM-as-judge checklist evaluates dynamicity, physical plausibility, shape consistency, and texture consistency. The resulting reward components jointly improve world consistency without freezing subject or camera motion.

## Model definition

### Inputs

The post-training loop receives an image prompt, text prompt, generated video samples, propagated subject masks, geometry foundation model outputs for point maps and cameras, and VLM checklist judgments for dynamic subjects.

### Outputs

The pretrained image-to-video generator outputs videos. WorldAlign outputs reward components for static consistency, camera motion, and dynamic-subject consistency, then uses those rewards to update the generator through GRPO with LoRA adaptation.

### Training objective (loss)

WorldAlign uses online GRPO. For each prompt group, it computes normalized reward components `Rstatic`, `Rcam`, and `Rdyn`, aggregates them into an advantage, and applies the clipped GRPO objective. The tracker, geometry foundation model, and VLM judge remain frozen.

### Architecture / parameterization

The method leaves the base video generator architecture unchanged. It uses semantic tracking/masking, a geometry foundation model such as VGGT-1B for static/camera rewards, and a strong VLM judge such as Qwen3.6-style judging for dynamic-subject checklists. Experiments post-train Wan2.2-TI2V-5B and Wan2.1-I2V-14B-480P.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Generated videos can look realistic frame by frame while violating 4D world consistency: static structures warp across viewpoints, and dynamic subjects change shape, texture, direction, or plausible motion. Existing geometry rewards often assume static scenes and suppress motion.

### 2. What is the method?

WorldAlign decouples static and dynamic regions. It uses masked reprojection against a geometric world prior for static background, a camera-motion reward to avoid static collapse, and a VLM checklist reward for dynamic subject behavior and appearance.

### 3. What is the method motivation?

Static backgrounds and moving subjects obey different consistency rules. A single geometry reward over the whole frame confuses legitimate motion with inconsistency; a single perceptual or VLM score misses precise static geometry failures.

### 4. What data does it use?

The paper post-trains and evaluates on image-to-video prompts with motion-capable subjects such as people, animals, and vehicles. It uses held-out test prompts with subject masks and camera-motion instructions. Evaluation is performed on Wan2.2-TI2V-5B and Wan2.1-I2V-14B-480P.

### 5. How is it evaluated?

Static consistency is measured with Masked Epipolar Error and Masked Reprojection Error. Dynamic consistency is measured with tracked-subject DINOv3 similarity and checklist yes rate, including dynamicity. General quality/motion is measured with VBench Dynamic Degree, Motion Smoothness, and Aesthetic Quality. The appendix adds pairwise human evaluation.

### 6. What are the main results?

On Wan2.2-TI2V-5B, WorldAlign improves checklist yes rate from 0.697 for the base model to 0.781 and dynamicity from 0.63 to 0.85, while Dynamic Degree rises from 0.63 to 0.72. It reduces Masked Epipolar Error from 0.463 to 0.321 and Masked Reprojection Error from 0.040 to 0.026. On Wan2.1-I2V-14B-480P, it improves checklist yes rate from 0.760 to 0.856, dynamicity from 0.81 to 0.92, and Dynamic Degree from 0.62 to 0.74, with Masked Epipolar Error down from 0.469 to 0.264. Human evaluation over 300 judgments favors WorldAlign on static consistency 71.3%, dynamic consistency 75.0%, and overall quality 70.3%.

### 7. What is actually novel?

The novelty is reward factorization: use a geometry prior only where its assumptions hold, use camera motion as an anti-degenerate constraint, and use explicit dynamic-subject checklists for the moving parts.

### 8. What are the strengths?

The paper directly diagnoses reward hacking by motion suppression and evaluates metrics jointly with Dynamic Degree. The ablation shows masked reprojection alone improves geometry but suppresses motion; adding camera and dynamic rewards recovers the intended behavior.

### 9. What are the weaknesses, limitations, or red flags?

The method inherits errors from the tracker, geometry model, and VLM judge. Checklist rewards are only as good as the questions and judge reliability. It is post-training-heavy and tested on image-to-video generators rather than as a core world-model architecture.

### 10. What challenges or open problems remain?

The main open problem is moving from judged consistency to predictive physical state: forces, contacts, occlusions, and object permanence are not fully captured by DINO similarity or checklist yes rates.

### 11. What future work naturally follows?

Replace checklist judging with more grounded dynamic-state metrics, add object-level physical constraints, and use the static/dynamic decoupling idea in action-conditioned video world models.

### 12. Why does this matter for cabbageland?

Cabbageland cares about rewards that test the claimed structure instead of rewarding shortcuts. WorldAlign is a good example of refusing one scalar mush for a mixed static/dynamic world.

### 13. What ideas are steal-worthy?

Never apply a static-scene reward to the whole video when moving objects exist. Always pair geometry rewards with anti-collapse motion checks. Turn world-consistency evaluation into separate static and dynamic contracts.

### 14. Final decision

Preserve. The reward design is imperfect but pointed at the right failure mode.
