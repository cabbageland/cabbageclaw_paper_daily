# TrackEverything: Long Horizon Dense Tracking via De-Duplicating 3D Scene Representations

## Basic info

* Title: TrackEverything: Long Horizon Dense Tracking via De-Duplicating 3D Scene Representations
* Authors: Ayush Jain, Sreeharsha Paruchuri, Ishita Gupta, Fan Zhang, Tanner Schmidt, Jakob Engel, Katerina Fragkiadaki, Adam W. Harley
* Year: 2026
* Venue / source: arXiv:2609.30222
* Link: https://arxiv.org/abs/2609.30222
* Date surfaced: 2026-09-26
* Why selected in one sentence: It turns long-video dense tracking into a persistent 3D scene-memory problem whose cost scales with unique geometry rather than raw frame count.

## Quick verdict

* Must read

This is the strongest remaining paper in the Friday batch. The mechanism is crisp: merge repeated observations of the same 3D surface, predict endpoints before full trajectories, and spend dense trajectory decoding only on dynamic points. The caveat is that the method depends on input point maps, camera geometry, and voxel choices, but the representation idea is highly transferable.

## One-paragraph overview

TrackEverything builds a dense 3D point tracker for long videos by maintaining world-coordinate tracks rather than frame-local pixel tracks. Within each sliding window, RGB features are lifted into a 3D feature cloud using depth and camera pose. An endpoint refiner predicts where each point lands at the end of the window and whether it is static or dynamic. A trajectory refiner then decodes within-window paths only for dynamic points. At window boundaries, co-located points are voxelized and merged, so the persistent track set grows mostly when new physical scene content appears. This lets the method track all visible points in 1000+ frame videos while prior dense all-frame methods run out of memory.

## Model definition

### Inputs

The model receives RGB video, camera geometry, and depth or point maps from sensors or off-the-shelf estimators such as VGGT. It processes the video in sliding windows and carries forward a persistent 3D scene-track set from previous windows.

### Outputs

The system outputs dense 3D point tracks in world coordinates, visibility logits, and static-versus-dynamic labels. Static points keep their world-coordinate positions; dynamic points receive dense within-window trajectories.

### Training objective (loss)

The paper trains against 3D point-tracking supervision with trajectory losses plus cross-entropy losses for visibility and static/dynamic classification. The trajectory refiner is trained on dynamic points; ablations show that forcing all points through the dynamic decoder keeps accuracy similar but costs substantially more memory and latency.

### Architecture / parameterization

The model uses a 2D visual encoder, a lifted 3D feature cloud, an endpoint-refiner transformer with 3D WAFT feature sampling, a lightweight trajectory refiner for dynamic points, and sparse voxel hashing for cross-window de-duplication.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It tries to remove the tradeoff between sparse long-horizon tracking and dense short-clip tracking. Existing dense methods usually scale with frame count and run out of memory on long videos.

### 2. What is the method?

TrackEverything tracks in persistent 3D scene space. It de-duplicates co-located surfaces across window boundaries, predicts endpoints before full trajectories, and uses 3D WAFT sampling instead of memory-heavy 4D correlations.

### 3. What is the method motivation?

Videos repeatedly observe the same physical surfaces. A tracker that stores every frame-local point separately is paying for projection redundancy instead of new scene information.

### 4. What data does it use?

The paper trains and evaluates on 3D point-tracking settings including TAPVid-3D, PointOdyssey, Dynamic Replica, Kubric-style synthetic data, and related dynamic-scene datasets. It uses estimated or ground-truth geometry depending on the experiment.

### 5. How is it evaluated?

It reports TAPVid-3D APD metrics, long-video memory and latency scaling, static/dynamic classification quality, ablations for WAFT, trajectory refinement, voxel size, and window length, plus qualitative long-video tracks.

### 6. What are the main results?

On TAPVid-3D short clips, TrackEverything beats open-source all-frame dense 3D trackers by more than 20% APD-P on average. It is the only dense all-frame method in the comparison that scales to 1000+ frame videos within 40 GB of GPU memory. The static/dynamic decomposition keeps accuracy while reducing latency by 4.8x and peak memory by 2.5x in the reported ablation. Removing trajectory refinement drops APD-P from 31.2 to 26.4, and removing 3D WAFT drops it to 29.3.

### 7. What is actually novel?

The novelty is the computational state representation: long-video tracking as de-duplicated 3D scene memory. The endpoint-before-trajectory decomposition and 3D WAFT are useful supporting mechanisms.

### 8. What are the strengths?

The paper has a real scaling argument, direct memory measurements, and ablations tied to the claimed mechanism. It also makes explicit why static scene content should not pass through the same expensive path as moving content.

### 9. What are the weaknesses, limitations, or red flags?

The method still depends on the quality of the point maps and camera geometry. Active memory grows with new scene content, not zero. Voxelization can merge nearby but distinct surfaces if the resolution is poorly chosen. The evaluation is strongest in settings where 3D geometry is available or recoverable.

### 10. What challenges or open problems remain?

Open problems include robust operation under poor geometry, nonrigid and articulated objects, real-time deployment on very large scenes, and connecting the persistent tracks to downstream world models or policies.

### 11. What future work naturally follows?

The obvious follow-up is to use de-duplicated dense 3D tracks as memory for video world models, VLA policies, and dynamic scene generation. Another direction is learned merge/split policies instead of fixed voxelization.

### 12. Why does this matter for cabbageland?

Cabbageland cares about explicit state that makes long horizons tractable. This paper is a concrete example of a representation that stops paying repeatedly for the same observed world.

### 13. What ideas are steal-worthy?

Scale state with unique physical content, not observation length. Route static and dynamic content through different compute paths. Merge persistent memory at boundaries. Treat de-duplication as a first-class representation operation.

### 14. Final decision

Preserve. This is the most transferable mechanism paper of the day.
