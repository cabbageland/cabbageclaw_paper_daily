# Thinking in Boxes: 3D Editing in Real Images Made Easy

## Basic info

* Title: Thinking in Boxes: 3D Editing in Real Images Made Easy
* Authors: Pradhaan S Bhat, Naveen Chandra R, Rishubh Parihar, Vaibhav Vavilala, R. Venkatesh Babu, D. A. Forsyth, Anand Bhattad
* Year: 2026
* Venue / source: ECCV 2026 / arXiv
* Link: https://arxiv.org/abs/2606.20556
* Date surfaced: 2026-06-21
* Why selected in one sentence: It turns 3D image editing control into an explicit source-to-target box specification instead of relying on vague text prompts, 2D boxes, or depth-only warps.

## Quick verdict

**Highly relevant**

This is a strong explicit-control generative media paper. The representation is deliberately simple: 3D object boxes plus a depth-aligned floor, projected into conditioning images for a fine-tuned image editor. I inspected the full arXiv PDF, especially the method, dataset construction, experiments, ablations, conclusion, and limitation. The main caveat is that the method depends on usable fitted boxes and can become ambiguous when box identities are not distinguishable.

## One-paragraph overview

Thinking in Boxes lets a user place a 3D box around an object in a source image and specify a target box for where that object should be after the edit. The boxes encode translation, rotation, scale, and visibility change. A depth-aligned floor acts as a shared scene reference frame, disambiguating object motion from camera motion and providing contact/shadow cues. The system projects the source and target layouts into conditioning images and fine-tunes a FLUX-Kontext image editor with LoRA layers so the generator can map source image plus source/target box layouts into the edited image. It is trained mostly on synthetic multi-object scenes and then finetuned on Objectron videos, but evaluated on real images and large 3D edits.

## Model definition

### Inputs
The model consumes a real source image, a projected source 3D layout, and a projected target 3D layout. The layouts contain color-coded 3D object boxes and a depth-aligned planar floor. The user fits or refines object boxes; the paper says the floor is estimated automatically, and off-the-shelf 3D box detectors can initialize boxes.

### Outputs
The model outputs an edited image that should preserve scene identity and object appearance while following the target 3D transformation. It handles object translation, rotation, scaling, disocclusion, and camera viewpoint changes through the same conditioning language.

### Training objective (loss)
The paper fine-tunes FLUX-Kontext with LoRA layers on paired source and target views. The accessible text describes source image, noisy target image, source layout, and target layout being encoded and concatenated, with the model trained to generate the edited target image. It does not spell out a new custom loss beyond the standard diffusion/image-editing training objective of the base editor.

### Architecture / parameterization
The architecture builds on FLUX-Kontext. The source image, source layout, and target layout are encoded by the VAE into latent tokens and concatenated spatially. Joint attention inside the MMDiT backbone allows image tokens to attend to source and target layout tokens. LoRA layers are injected into attention matrices while the rest of the model remains frozen.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to make large 3D spatial edits in real images controllable. Text prompts cannot specify precise 3D movement, and 2D boxes cannot distinguish translation, rotation, scaling, and camera movement. Depth-only or per-image optimization methods often fail under large transformations and disocclusion.

### 2. What is the method?
Represent each object as a 3D box with position, orientation, and scale. Render each box with fixed face colors so orientation is visible in a 2D conditioning image. Anchor the scene with a depth-aligned checkered floor, which moves with the camera but stays fixed under object motion. Feed the source image, source layout, and target layout to a LoRA-finetuned FLUX-Kontext editor, which generates the edited image.

### 3. What is the method motivation?
The motivation is that coarse geometry can be enough if it is the right geometry. A box does not reconstruct the object, but it specifies the transformation the generator needs to honor. The floor gives global reference, while face colors give local orientation. Together they make the edit a geometric contract rather than a prompt interpretation problem.

### 4. What data does it use?
The synthetic training set contains 110,000 scenes and 220,000 views drawn from 10,143 Objaverse-XL objects, with HDRIs and floor materials. The system is then finetuned with 10,000 image pairs from Objectron plus 10,000 synthetic pairs. Evaluation uses synthetic held-out data, WildDet-3D for real object edits, held-out Objectron samples for camera edits, and a 49-participant user study.

### 5. How is it evaluated?
It uses qualitative real-image comparisons, a user preference study, and quantitative metrics for image quality, region-localized consistency, and edit fidelity. Metrics include PSNR, SSIM, LPIPS, DreamSim, DINO feature consistency, warp error, mean distance, IoU, and angular error. Baselines include SAM3D, 3D-Fixer, SpatialEdit, Diffusion Handles, GeoDiffuser, FreeFine, SEVA, and Qwen-Camera-Control.

### 6. What are the main results?
On real object editing with WildDet-3D, the method ranks first or second on every reported metric and leads clearly on mean distance error and angular error. On synthetic object editing, it outperforms the baselines across all reported metrics. The user study shows high preference rates for the method across object preservation, background preservation, and layout following. The ablations support the representation choice: removing the floor hurts position preservation, and using uniform box colors hurts orientation accuracy.

### 7. What is actually novel?
The novelty is the specific control representation and how directly it is used. Prior work has used 3D primitives as loose conditioning, meshes, depth maps, or generated-image scaffolds. This paper treats source and target boxes as the edit specification itself and uses the floor to disambiguate object motion from camera motion.

### 8. What are the strengths?
The representation is compact, editable, and aligned with the user's actual intent. The method handles multiple transformation types through one conditioning language instead of separate special cases. The synthetic-to-real transfer is also practical: most training data is rendered, with a comparatively small real finetuning set.

### 9. What are the weaknesses, limitations, or red flags?
The interface still needs good 3D boxes. If the boxes are wrong, ambiguous, or hard to fit, the edit contract degrades. The paper explicitly notes failure when objects share similar scales and bounding boxes become indistinguishable; the model can then produce the identity transformation. The method also inherits the generative prior's ability or inability to hallucinate unseen object regions correctly. Quantitative 3D edit metrics remain imperfect proxies for semantic correctness.

### 10. What challenges or open problems remain?
Better automatic box fitting, identity tracking across multiple similar objects, and robust handling of non-box-like or articulated objects remain open. The method also invites a deeper question: what other simple explicit state objects can expose controllable directions inside foundation image editors?

### 11. What future work naturally follows?
Future work should pair the interface with stronger 3D detectors or interactive box refinement, test articulated and deformable objects more thoroughly, and extend the same source-to-target primitive idea to video editing where temporal consistency becomes load-bearing.

### 12. Why does this matter for cabbageland?
Cabbageland likes explicit structure that changes computation. This paper is a good example: the generator is not asked to infer "move it over there" from vibes. It receives a source state, a target state, and a shared coordinate reference. That is the kind of state-carrying interface worth stealing for controllable generation and world-model editing.

### 13. What ideas are steal-worthy?
Use simple primitives as edit contracts, not just conditions. Color-code geometric orientation when a 3D signal must survive projection to 2D. Add a global reference object when local object coordinates alone create ambiguity. Train on paired synthetic transformations, then use a small real set to bridge appearance.

### 14. Final decision
**Keep it.** This is not a general world model, but it is a strong controllability paper. The core lesson is broadly useful: when text and 2D hints under-specify a generative operation, give the model a small explicit state object that actually encodes the transformation.
