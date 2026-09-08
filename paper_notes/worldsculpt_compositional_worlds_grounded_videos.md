# WorldSculpt: Generating Compositional Worlds from Grounded Videos

## Basic info

* Title: WorldSculpt: Generating Compositional Worlds from Grounded Videos
* Authors: Muyao Niu, Jixuan He, Ruihan Yu, Lian Fu, Yonghao Yu, Zheng-Hui Huang, Yifan Zhan, Fengbo Lan, Yongtao Ge, Yinqiang Zheng, Kaipeng Zhang, Zhixiang Wang
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2609.05416
* Date surfaced: 2026-09-08
* Why selected in one sentence: It turns generated 3D worlds into collections of addressable object meshes rather than one fused scene representation.

## Quick verdict

* Highly relevant

I inspected the full arXiv HTML text, especially the anchor-aligned canonicalization, multi-view feature lifting, Pixal3D adaptation, UE-MeshyScene benchmark, scene-generation results, and limitations. This earns a preserved note because the compositional representation is the point, not a decorative wrapper around generation.

## One-paragraph overview

WorldSculpt generates a compositional 3D scene from grounded videos. Given RGB images, instance masks, camera poses, and coarse 3D boxes, it processes each object independently, maps that object's visible evidence into an anchor-aligned canonical frame, conditions a strong object-level 3D generative prior on multi-view features, and places the resulting mesh back into a shared world frame. The output is a set of individual object meshes, so downstream systems can select, move, edit, or simulate objects without disentangling them from a fused surface.

## Model definition

### Inputs
Multi-view RGB observations with instance-level 2D masks, camera parameters, and coarse 3D object localizations.

### Outputs
A collection of individual object meshes, each generated in canonical object space and transformed into a shared world frame.

### Training objective (loss)
The sparse-structure and shape stages are trained against ground-truth latent targets while the pretrained Pixal3D parameters stay frozen. The trainable parts are LoRA adapters, conditioning projections, and the multi-view aggregator.

### Architecture / parameterization
The method adapts Pixal3D with anchor-aligned object canonicalization, crop-aware projection, DINOv3 feature lifting into canonical voxel volumes, permutation-invariant IBR-style view aggregation, zero-initialized conditioning injection, and LoRA adapters on the generative prior.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Current generated worlds are often visually plausible but structurally awkward: they produce one fused mesh or Gaussian soup instead of separate, usable objects.

### 2. What is the method?
For each object, WorldSculpt chooses an anchor view, defines an object-centered canonical cube, projects multi-view visual features into that frame, aggregates evidence across views, runs an adapted object-level 3D prior, and transforms the generated mesh back to world coordinates.

### 3. What is the method motivation?
Object-level priors can complete hidden geometry, but they usually assume a single centered object. Scene reconstruction methods can align observed geometry, but often leave occluded parts incomplete and fused. WorldSculpt combines the two.

### 4. What data does it use?
It trains on single objects in canonical space and evaluates on Toys4k, Toys4k-Scene, HouseCat6D, and the new UE-MeshyScene benchmark.

### 5. How is it evaluated?
It reports Chamfer distance, EMD, and F-Score under canonical single-object evaluation and world-frame scene evaluation without per-object ICP alignment.

### 6. What are the main results?
On HouseCat6D, WorldSculpt reports CD-l2 0.28 and F-Score 0.995 versus ShapeR at 1.26 and 0.973. On Toys4k-Scene, it reports CD-l2 0.61 and F-Score 0.981 versus ShapeR at 8.38 and 0.746. On UE-MeshyScene, it beats ShapeR across all metrics, including CD-l2 2.48 versus 7.42 and F-Score 0.951 versus 0.813. The benchmark itself contains six Unreal Engine scenes, 2,299 objects, and 5,964 views.

### 7. What is actually novel?
The novelty is scaling object-level generative priors to dense multi-object scenes by conditioning each object on aligned multi-view evidence while preserving separate mesh identity.

### 8. What are the strengths?
The output representation is genuinely more useful than a fused scene. The no-scene-level-training result is also notable: the adapted object prior generalizes to scenes with hundreds of occluded objects.

### 9. What are the weaknesses, limitations, or red flags?
The system assumes reasonably good masks, camera poses, and coarse 3D boxes. It also generates objects independently, so object-object contact, support, physics, and global scene consistency are not the main solved problem.

### 10. What challenges or open problems remain?
The next challenge is coupling addressable object generation with relational constraints, physical plausibility, temporal updates, and downstream interaction.

### 11. What future work naturally follows?
Add relational layout constraints, physics-aware post-processing, interactive editing loops, and uncertainty over hidden object geometry.

### 12. Why does this matter for cabbageland?
Cabbageland keeps wanting world models with reusable state. WorldSculpt is a good example of representation structure doing real work: the object boundary survives into the generated artifact.

### 13. What ideas are steal-worthy?
Keep objects addressable. Use an object prior for completion but anchor it in world coordinates. Evaluate generated scenes without alignment shortcuts. Build benchmarks with per-object ground truth, not just pretty renderings.

### 14. Final decision
Keep as a preserved note. The paper is not a complete physical world model, but it is a strong compositional 3D-generation step.

## 6. Mandatory critical angles

The explicit structure does real work because downstream editability depends on object identity. The main caution is that the pipeline inherits the quality of upstream segmentation, camera recovery, and object localization.

## 7. Writing style

Tone should be approving but precise. This is useful because it changes the output object, not because it has a grandiose world-model label.

## 8. Repository output format

Saved as a preserved paper note because addressable generated worlds are a durable cabbageland interest.
