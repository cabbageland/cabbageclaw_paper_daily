# 4Director: Controlling Video World Models with Rigid 3D Geometry

## Basic info

* Title: 4Director: Controlling Video World Models with Rigid 3D Geometry
* Authors: Wei Cao, Hao Zhang, Vikram Voleti, Yuqun Wu, Mallikarjun B R, Shimon Vainer, Mark Boss, Yaoyao Liu
* Year: 2026
* Venue / source: arXiv:2610.02160
* Link: https://arxiv.org/abs/2610.02160
* Date surfaced: 2026-10-02
* Why selected in one sentence: It turns object and camera control for video generation into explicit rigid 3D geometry instead of ambiguous 2D tracks or incomplete lifted proxies.

## Quick verdict

* Highly relevant

4Director is strong because the control representation earns its name. Complete object meshes, rigid transforms, camera poses, and a shared coordinate frame are not decorative; they directly improve object orientation, occlusion, and identity-preserving placement. The limitation is that the control is rigid-body only, so articulated details still live in the generator's guesswork.

## One-paragraph overview

4Director generates controlled video from a single image by first lifting the scene into 3D. The background becomes a point cloud, each clicked object becomes a complete canonical mesh, and every object is moved by a prescribed rigid transformation per frame while the camera moves in the same coordinate frame. The controlled scene is rendered as a depth video. A trainable Motion Adapter injects that rigid rendering into a Wan2.1-VACE-14B video generator, which supplies appearance, illumination, non-rigid details, and inpainted background. The authors build RealCOD-Rigid, 20,774 automatically annotated clips, and introduce Identity-Gated IoU to score object placement only when identity is preserved. Quantitatively and in a user study, 4Director beats four prior control methods.

## Model definition

### Inputs

Inputs are a source image, text prompt, user-marked object masks/clicks, camera trajectory, and per-object rigid SE(3) trajectories. The pipeline estimates depth and intrinsics, reconstructs object meshes, and renders the controlled scene as a depth video.

### Outputs

The model outputs an RGB video that starts from the input image, follows the prescribed camera path and object rigid motion, preserves object identity, and fills in plausible appearance, lighting, non-rigid motion, and newly revealed background.

### Training objective (loss)

The Motion Adapter is trained as a conditional video diffusion branch using pairs of rigid depth-control videos and target real clips from RealCOD-Rigid. The paper uses the Wan2.1-VACE training recipe rather than proposing a separate new loss for rigid control.

### Architecture / parameterization

4Director uses MoGe-2 for depth/intrinsics, SAM 2 for object masks, Pixal3D for complete canonical object meshes, and a static background point cloud. The Motion Adapter is a 3.0B-parameter DiT-style branch initialized from the VACE branch and inserted into the frozen Wan2.1-VACE-14B generator through context blocks and cross-attention hints.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Existing video-control methods use 2D cues that are ambiguous in depth and rotation, or lifted 3D proxies that lack complete object geometry. They can place an object roughly correctly while failing to preserve orientation, unseen sides, occlusion, or identity.

### 2. What is the method?

Represent each controlled object as a complete canonical mesh, move it with one rigid transform per frame, render the full controlled scene as depth, and condition a pretrained video generator through a Motion Adapter.

### 3. What is the method motivation?

Directors specify object and camera motion in 3D, not as vague image-plane hints. A rigid mesh gives the generator a persistent extent and orientation even when the object turns or leaves the frame.

### 4. What data does it use?

The authors construct RealCOD-Rigid from RealCOD-25K using an automatic pipeline for camera/depth estimation, first-frame 3D reconstruction, robust rigid-body tracking, and depth rendering. The final training set contains 20,774 clips. Evaluation uses 100 RealCOD-25K clips excluded from training, plus user-study cases.

### 5. How is it evaluated?

Metrics include FID, FVD, CLIP-SIM, camera rotation/translation error, VBench-I2V dimensions, user ratings, and Identity-Gated IoU. IG-IoU uses a vision-language identity gate so a frame contributes mask IoU only if the generated object is still the same object.

### 6. What are the main results?

4Director achieves the best scores across the main quantitative table: FID 44.1, FVD 370.4, CLIP-SIM 31.8, rotation error 3.65 degrees, translation error 0.122, recognition 94.9, and IG-IoU 60.4. The next-best IG-IoU is 54.8 from VerseCrafter. In the user study, 4Director receives 4.62 visual quality, 4.82 control accuracy, and 4.69 consistency, while the next best control score is 2.39.

### 7. What is actually novel?

The novelty is the complete rigid 3D scene representation as the control interface, together with RealCOD-Rigid and IG-IoU. It is not merely adding another depth condition; it supplies complete object surfaces plus prescribed 3D motion.

### 8. What are the strengths?

The control representation directly addresses depth, orientation, occlusion, and identity. The ablation is convincing: removing complete surfaces, rotation, or 3D depth lowers IG-IoU. The object leaving/re-entering example is especially clear.

### 9. What are the weaknesses, limitations, or red flags?

The method controls objects as rigid bodies. Articulated or deforming motion, such as limbs, running, jumping, or flexible objects, is left to the generator and can remain wrong. The training data is automatically annotated, so annotation errors and domain limits matter.

### 10. What challenges or open problems remain?

Extending the representation to articulated parts, deformable objects, contact-rich interactions, and editable scene dynamics is the natural hard part. Another open problem is exposing the 3D authoring interface in a way users can actually control without fighting reconstruction errors.

### 11. What future work naturally follows?

Add articulated skeletons or part-level meshes, combine with physical constraints, and connect rigid 3D controls to programmable world-state records so generation can be both authorable and verifiable.

### 12. Why does this matter for cabbageland?

Cabbageland wants generative systems with state that survives rendering. 4Director shows a useful pattern: when motion matters, make motion a first-class geometric object.

### 13. What ideas are steal-worthy?

Use complete object geometry instead of 2D hints. Score control only when identity is preserved. Treat background, objects, and camera as one coordinate system before giving anything to the generator.

### 14. Final decision

Preserve. It is one of the better controllable-video papers because the representation actually carries the claim.
