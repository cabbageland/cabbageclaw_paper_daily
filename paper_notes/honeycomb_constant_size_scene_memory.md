# Honeycomb: Constant-Size Scene Memory Representation for Video World Models

## Basic info

* Title: Honeycomb: Constant-Size Scene Memory Representation for Video World Models
* Authors: Jack Wei Lun Shi, Kaichen Zhou, Haoyu Chen, Yufeng Weng, Keane Ong, Ruojin Cai, Hang Hua, Justin K. W. Yeoh, Mengyu Wang
* Year: 2026
* Venue / source: arXiv:2609.37690
* Link: https://arxiv.org/abs/2609.37690
* Date surfaced: 2026-09-30
* Why selected in one sentence: It gives video world models a bounded persistent memory instead of a cache that grows with every generated observation.

## Quick verdict

* Highly relevant

Honeycomb is useful because it treats long-horizon video consistency as a memory-representation problem, not only a larger-context problem. The six-plane HexMemory design is compact, explicit, and integrated into a video diffusion generator through read and write operations. The main caveat is that the system depends on estimated depth, poses, and camera geometry, so its memory can inherit errors from the reconstruction stack.

## One-paragraph overview

The paper introduces Honeycomb, a camera-controlled video world model with a fixed-size scene memory called HexMemory. Instead of storing an ever-growing set of RGB observations, 3D points, or diffusion latents, HexMemory stores features in three spatial and three spatiotemporal planes. A feed-forward writer maps each new generated chunk into plane features, the previous planes are warped when spatial or temporal bounds expand, and old and new memory are fused with confidence-weighted pooling plus a learned residual correction. A reader projects target camera views into memory and reconstructs latent maps that condition a video diffusion transformer. The result is better revisit consistency and novel-view quality while keeping feature storage and write cost bounded.

## Model definition

### Inputs

The system starts from an input frame, camera trajectory, estimated camera parameters, estimated depth, and generated video chunks. During writing, it uses latent tokens, depth-derived 3D positions, camera centers, ray directions, and write time. During reading, it uses target camera geometry to query the memory.

### Outputs

It outputs generated video chunks along the target camera trajectory. Internally, the memory reader outputs reconstructed latent maps and visibility masks that condition the diffusion transformer.

### Training objective (loss)

The writer, fusion networks, and reader are trained with a latent reconstruction objective. Training clips provide latents, estimated depth, and camera poses; the model writes input and generated chunks to memory, queries the memory from camera views, and minimizes MSE between reconstructed latents and original visible latent tokens. The video generator branch is trained on top of a pretrained camera-controllable video diffusion backbone.

### Architecture / parameterization

HexMemory consists of six fixed-size 2D feature planes: three spatial planes and three spatiotemporal planes arranged as pairs over the coordinate axes. A point feature is read by sampling paired planes and combining their features. The feed-forward writer splats per-point learned contributions into the planes. Recurrent updates warp previous planes into expanded bounds, pool old and new features with confidence maps, and apply a learned residual correction. Generation uses a Wan2.2 5B video backbone with a ControlNet-style memory branch.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Long video world models lose consistency when the camera revisits old regions because earlier observations fall outside the temporal context. Existing explicit memories help but grow as generation proceeds.

### 2. What is the method?

Honeycomb keeps a fixed-size low-rank memory in six feature planes. It reads from memory to condition future generation and writes each new chunk back into the same tensors, using coordinate warping, confidence pooling, and residual correction.

### 3. What is the method motivation?

If a world model is meant to support long rollouts, memory cannot scale linearly with every observation. A constant-size memory forces the model to consolidate scene information rather than append history forever.

### 4. What data does it use?

The model is trained on RealEstate10K with estimated poses and depth from ViPE configured with Depth Anything 3. It is evaluated on RealEstate10K and WorldScore.

### 5. How is it evaluated?

The paper evaluates generation quality on WorldScore, novel-view synthesis on RealEstate10K, and closed-loop revisit consistency by generating trajectories that leave and return to the initial viewpoint. Metrics include PSNR, SSIM, LPIPS, WorldScore metrics, and RAFT optical-flow error between input and revisit frames.

### 6. What are the main results?

Honeycomb reaches the best WorldScore average among compared methods at 65.52. On RealEstate10K novel-view synthesis, it achieves 18.45 PSNR, 0.674 SSIM, and 0.274 LPIPS, beating Spatia and LSM-World. On closed-loop WorldScore revisit evaluation, it improves PSNR to 17.22 and reduces flow error to 3.00 pixels versus 6.64 for Spatia and 27.05 for LSM-World. A compact memory setting uses 19.8 MB of feature storage with only a 0.12 dB PSNR drop.

### 7. What is actually novel?

The novelty is a recurrent fixed-size scene memory for video generation that can be written feed-forward without per-scene optimization or full-history reprocessing. The low-rank plane structure makes memory bounded, and the recurrent writer makes updates cheap.

### 8. What are the strengths?

The mechanism is clean and directly attacks a bottleneck. The paper also compares against growing-cache methods and reports revisit metrics, not just pretty forward samples.

### 9. What are the weaknesses, limitations, or red flags?

The memory depends on estimated depth and camera poses, so geometry errors can corrupt writes and reads. Expanding bounds while preserving plane resolution means older memory becomes coarser over longer rollouts. Dynamic objects are not excluded during writes, which is bold but could also cause contamination in more complex scenes.

### 10. What challenges or open problems remain?

Handling dynamic scenes, uncertain depth, loop closures, and very large spaces remains open. The memory also needs ways to decide what to preserve or forget when fixed capacity becomes insufficient.

### 11. What future work naturally follows?

Add uncertainty-aware writing, explicit dynamic-object channels, adaptive plane allocation, and planning-oriented memory queries. Test beyond real-estate flythroughs on interactive environments where objects move and actions change state.

### 12. Why does this matter for cabbageland?

Persistent memory is a core world-model requirement. Honeycomb offers a concrete design pattern: recurrently compress observations into a bounded spatial-temporal state that future generation can query.

### 13. What ideas are steal-worthy?

Use fixed-size spatial/spatiotemporal planes as memory, fuse writes by confidence plus residual correction, and evaluate memory by revisit consistency rather than only next-frame quality.

### 14. Final decision

Preserve. The method is not a complete world model, but its memory interface is exactly the kind of reusable mechanism worth remembering.
