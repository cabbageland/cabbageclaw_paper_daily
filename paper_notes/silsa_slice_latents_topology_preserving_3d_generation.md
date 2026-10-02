# SILSA: Sliding-Window Slice Latents for Topology-Preserving High-Resolution 3D Generation

## Basic info

* Title: SILSA: Sliding-Window Slice Latents for Topology-Preserving High-Resolution 3D Generation
* Authors: Tianjiao Yu, Xinzhuo Li, Yifan Shen, Ying Shen, Kiet A. Nguyen, Adheesh Sunil Juvekar, Ismini Lourentzou
* Year: 2026
* Venue / source: arXiv:2610.02201
* Link: https://arxiv.org/abs/2610.02201
* Date surfaced: 2026-10-02
* Why selected in one sentence: It gives high-resolution 3D generation compact slice latents that preserve topology more directly than sparse voxel tokenizers.

## Quick verdict

* Highly relevant

SILSA is a strong representation paper. The key move is to make cross-sectional topology visible to the latent sequence instead of scattering continuous surfaces across many voxel tokens. The claims are bounded to image-to-3D generation and training-distribution coverage, but the representation idea is worth keeping.

## One-paragraph overview

SILSA replaces large sparse voxel token sets with overlapping slice latents along the three canonical axes. With 128 slice positions per axis, the model uses 384 fixed tokens. A SliceVAE encodes oriented surface samples into these slice latents and decodes them through a sparse volumetric decoder; a Volumetric Anchor Lattice lets x-, y-, and z-axis streams exchange evidence through a shared 3D workspace during rectified-flow generation. A slice-wise topology loss matches persistent-homology structure inside cross-sections and aligns Betti transitions across adjacent slices. The result is a cheaper one-stage image-to-3D generator that better preserves thin structures, holes, repeated parts, and long-range connectivity.

## Model definition

### Inputs

Training uses 3D meshes or sampled oriented surface points for the SliceVAE, and images for image-conditioned generation. The slice encoder receives point positions, normals, and depth-relative offsets inside overlapping bins along x, y, and z.

### Outputs

The generator outputs slice latents, which the decoder turns into high-resolution meshes. The VAE decoder predicts geometry through a sparse volumetric feature grid, upsampling to a 256-cubed grid and extracting a mesh with differentiable Dual Marching Cubes.

### Training objective (loss)

The SliceVAE objective combines differentiable rendering losses on depth, normals, and silhouettes, KL regularization, and a slice-wise topology-preserving loss. The topology loss combines persistent-homology supervision within slices and Betti-transition alignment across neighboring slices. The generative model is an image-conditioned rectified-flow transformer trained to generate the slice-latent representation.

### Architecture / parameterization

The representation uses 3N slice latents with N=128 by default, for 384 tokens. The encoder uses sliding-window pooling over surface points with window width 8. The decoder scatters axis-wise slice latents into a shared coarse 3D grid and uses sparse transformer decoding plus self-pruning upsampling. The rectified-flow transformer uses a Volumetric Anchor Lattice as cross-axis shared memory.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

High-resolution 3D generation needs compact latents, but compact global latents can miss topology and sparse voxel tokens can be expensive and fragmented. Thin supports, holes, spokes, and repeated parts often break even when surface error looks acceptable.

### 2. What is the method?

Encode shapes as overlapping slice latents along three axes, coordinate the slice streams through a shared volumetric lattice, and train with topology-aware slice supervision.

### 3. What is the method motivation?

A slice captures the structure of an entire cross-section, including components and holes. Neighboring slices expose how topology changes through depth, which is more directly aligned with structural correctness than independent local voxel tokens.

### 4. What data does it use?

Training uses Trellis-500K. Evaluation uses 200 sampled Toys4K assets, 50 in-the-wild images, and an open-surface DeepFashion3D test. The paper compares against Dora, XCube, Trellis, SparseFlex, Shape-E, LN3Diff, Direct3D, 3DTopia-XL, InstantMesh, GaussianAnything, SAR3D, and others.

### 5. How is it evaluated?

Image-to-3D metrics include CLIP, FD, KD, PSNR, LPIPS, coverage, and MMD. VAE reconstruction metrics include Chamfer distance, F-score at 0.01 and 0.005, IoU, and Betti error for topology. Efficiency is measured by token count, parameter count, memory, training time, and inference time.

### 6. What are the main results?

SILSA improves PSNR from 30.12 to 32.74 over SparseFlex, increases coverage from 73.12% to 79.08%, and reduces Betti error from 1.743 to 1.582. It uses 384 tokens, over 98% fewer than Trellis, XCube, and SparseFlex, and reduces training memory from 14.6GB for Dora to 8.7GB, with inference time 0.34 seconds per shape.

### 7. What is actually novel?

The novelty is the fixed multi-axis sliding-window slice latent representation, the Volumetric Anchor Lattice for cross-axis coordination, and tractable per-slice topology supervision for 3D generation.

### 8. What are the strengths?

The paper ties representation, objective, and failure mode together. The ablations show that topology loss, three-axis slicing, overlap, and gated VAL updates matter. The efficiency gains are large enough to be more than cosmetic.

### 9. What are the weaknesses, limitations, or red flags?

It is still image-to-3D under a training distribution. Ambiguous or low-information views remain underdetermined. Betti-style topology metrics are useful but do not cover semantics, physical usability, articulation, or editability.

### 10. What challenges or open problems remain?

Scaling to more diverse object distributions, articulated/deformable objects, scene-level generation, and downstream simulation usefulness remain open. Another issue is whether topology-preserving latents help text-to-3D and multi-object composition.

### 11. What future work naturally follows?

Use slice-like latents for editable 3D assets, physics-aware shape generation, and scene reconstruction where topology and connectivity have downstream consequences.

### 12. Why does this matter for cabbageland?

Cabbageland cares about representations that preserve structure the next computation needs. SILSA is a clean example: topology is not a visual nicety, it is part of the latent contract.

### 13. What ideas are steal-worthy?

Represent high-dimensional objects through structured cross-sections. Use topology losses where local reconstruction losses miss structural errors. Coordinate directional views through a shared workspace instead of unconstrained token mixing.

### 14. Final decision

Preserve. It is a useful 3D-generation representation paper with both mechanism and evidence.
