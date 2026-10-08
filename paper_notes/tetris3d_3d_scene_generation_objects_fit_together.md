# Tetris3D: 3D Scene Generation With Objects That Fit Together

## Basic info

* Title: Tetris3D: 3D Scene Generation With Objects That Fit Together
* Authors: Jaeyeong Kim, Jinhyuk Jang, Jongmin Lee, Kyehong Park, Seungryong Kim
* Year: 2026
* Venue / source: arXiv preprint
* Link: https://arxiv.org/abs/2610.10539
* Date surfaced: 2026-10-08
* Why selected in one sentence: It makes physical relation and neighboring geometry explicit conditioning variables for compositional 3D scene generation.

## Quick verdict

* Must read

This is a strong compositional 3D generation paper because the structure is doing actual work. The model does not merely hope independently generated objects will align after placement; it conditions object generation on surrounding surfaces and physical relation labels. The weakness is dependence on segmentation, depth, and VLM-inferred relation graphs, so errors in those front-end modules can still poison the generation order and conditions.

## One-paragraph overview

Tetris3D reconstructs a 3D scene from a single image by generating each object in a physical dependency order and conditioning each generation step on already-generated neighboring geometry. It builds on a voxel-based TRELLIS.2 shape generator and injects per-voxel interaction conditions: nearby surface distance, relative vectors, surface normals, and a relation embedding for stack, lean, contain, touch, or none. To train this, the paper introduces ComOb, a 1.2M-scene simulation dataset with physically stable object arrangements, per-object meshes, and relation annotations. Experiments on Toys4K and real contact-rich scenes from MessyKitchens and Picasso show better reconstruction quality and much lower penetration and post-simulation instability than scene-generation or amodal-object baselines.

## Model definition

### Inputs

The system takes a single RGB scene image, object masks, depth information or depth estimates, and physical relation/dependency predictions. For each target object, it also receives interaction context from previously generated neighboring objects.

### Outputs

It outputs per-object 3D shapes and poses in a shared scene, including sparse structure and structured latent tokens that decode into object meshes/textured geometry.

### Training objective (loss)

The paper builds on the TRELLIS.2 sparse-structure and structured-latent generation objectives. The exact full loss is inherited from the diffusion/generative backbone, with additional interaction-conditioning inputs rather than a new physical-simulation loss. Evaluation, not the training objective alone, measures physical penetration, displacement, and kinetic instability.

### Architecture / parameterization

Tetris3D uses a voxel-grid generative backbone from TRELLIS.2. Interaction conditions are encoded on the same 3D grid and injected per token. The spatial context includes distance to neighboring surfaces, relative position vectors, and nearest-surface normals; relation type is a learned embedding. A VLM infers directed physical dependencies and relation labels, then topological sorting determines object generation order.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Single-image 3D scene reconstruction often generates plausible objects that do not fit together physically. Occluded contact regions make it especially hard to infer shapes and poses that support, contain, lean on, or touch neighboring objects without penetration or floating.

### 2. What is the method?

Generate the scene autoregressively. Infer a physical dependency graph, generate support objects first, then condition each dependent object's shape and pose on the geometry and physical relations of its neighbors. Train with a new physics-simulated dataset of stable interacting object scenes.

### 3. What is the method motivation?

Humans infer hidden shape partly from contact and support. If a cup sits on a table or inside a container, the neighboring geometry constrains the invisible object surface. Making that constraint an explicit generation condition is more direct than letting an implicit scene feature carry all contact information.

### 4. What data does it use?

The key training contribution is ComOb, a 1.2M-scene simulated dataset of composite object scenes with stable physical arrangements, object meshes, RGB/depth/masks, and relation labels. Evaluation uses Toys4K, MessyKitchens, and Picasso.

### 5. How is it evaluated?

The paper reports scene-level and object-level reconstruction metrics such as Chamfer distance, F-score, box IoU, and residual rotation error. It also reports generative quality with MMD, COV, P-FID, Uni3D, and ULIP, plus physical stability metrics: penetration depth, mean displacement after simulation, and peak kinetic energy.

### 6. What are the main results?

On Toys4K, Tetris3D improves scene Chamfer distance to 3.68 versus 5.72 for ShapeR and 8.68 for WorldSculpt, raises F1-S to 0.8407, and cuts penetration depth to 0.0036 versus 0.1177 for WorldSculpt and 0.8862 for ShapeR. On MessyKitchens and Picasso, it keeps lower reconstruction error and physical instability than scene generation and amodal-generation-plus-pose baselines. The ablation without interaction conditioning increases penetration depth from 0.0192 to 0.4980 on Toys4K.

### 7. What is actually novel?

The novelty is explicitly conditioning each object's 3D generation on neighboring surface geometry and physical relation type, then ordering generation through a physical dependency graph. ComOb is also a useful dataset contribution because it directly supplies relation-annotated, physically settled composite scenes.

### 8. What are the strengths?

The physical stability metrics are exactly the right kind of evaluation for the claim. The ablations isolate interaction conditioning and visible-to-invisible attention. The method also generalizes beyond the synthetic ComOb source to real contact-rich scenes.

### 9. What are the weaknesses, limitations, or red flags?

The physical relation graph is inferred by a VLM at inference time, and the method depends on object masks and depth estimates. The interaction conditions are guidance, not hard constraints, so the model still cannot guarantee physical validity. The relation vocabulary is useful but coarse.

### 10. What challenges or open problems remain?

The next step is tighter integration with differentiable physics or constraint solving so relation satisfaction is enforced, not just encouraged. Another open issue is robust relation inference under clutter, occlusion, and ambiguous support.

### 11. What future work naturally follows?

Use relation-conditioned generation inside interactive scene editing or robot simulation. Add explicit constraint repair after generation. Expand relation types to include articulated, deformable, and multi-object support. Test with downstream physical simulation tasks, not only reconstruction metrics.

### 12. Why does this matter for cabbageland?

It is a clean example of structure at the right interface. The model does not ask a latent to vaguely learn "physical coherence"; it gives the generator local geometry and relation variables at the point where they can constrain the hidden shape.

### 13. What ideas are steal-worthy?

Topologically sort generation by physical dependency. Represent relation context per voxel rather than as a global tag. Evaluate generative 3D scenes with penetration and post-simulation stability, not just visual similarity.

### 14. Final decision

Preserve. This is a useful compositional 3D paper with a real mechanism and good evaluation alignment.
