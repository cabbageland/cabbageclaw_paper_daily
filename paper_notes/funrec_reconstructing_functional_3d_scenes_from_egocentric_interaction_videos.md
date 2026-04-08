# FunRec: Reconstructing Functional 3D Scenes from Egocentric Interaction Videos

## Basic info

* Title: FunRec: Reconstructing Functional 3D Scenes from Egocentric Interaction Videos
* Authors: Alexandros Delitzas, Chenyangguang Zhang, Alexey Gavryushin, Tommaso Di Mario, Boyang Sun, Rishabh Dabral, Leonidas Guibas, Christian Theobalt, Marc Pollefeys, Francis Engelmann, Daniel Barath
* Year: 2026
* Venue / source: CVPR 2026 / arXiv preprint (cs.CV)
* Link: https://arxiv.org/abs/2604.05621
* Date surfaced: 2026-04-08
* Why selected in one sentence: It uses ordinary egocentric interaction videos to recover articulated, simulation-ready scene structure, which is much closer to functional world modeling than static reconstruction is.

## Quick verdict

* Highly relevant

This is adjacent rather than central to the robotics-policy cluster, but it is exactly the sort of 3D paper that matters: not prettier geometry for its own sake, but reconstruction of articulated parts, kinematics, and canonicalized scene structure from real interaction. If the claims hold, it is a very useful bridge between perception, affordances, and simulation-ready world models.

## One-paragraph overview

FunRec aims to build functional 3D digital twins of indoor scenes directly from in-the-wild egocentric RGB-D videos of people interacting with objects. Instead of assuming controlled captures, multi-state scans, or CAD priors, it tries to discover articulated parts, estimate their motion parameters, track their 3D movement, and reconstruct both static and moving geometry in a canonical space. The end product is meant to be simulation-compatible, not just visually plausible.

## Model definition

### Inputs
Egocentric RGB-D interaction videos of indoor scenes, including human interactions that reveal object articulation and motion. The model appears to use temporal multi-view evidence and observed object motion induced by interaction.

### Outputs
Recovered articulated scene structure: segmented articulated parts, estimated kinematic parameters, tracked 3D motions, and canonical-space geometry that can be exported as simulation-compatible meshes such as URDF or USD assets.

### Training objective (loss)
The exact optimization losses are not available from the accessible abstract text. The paper likely combines reconstruction, segmentation, tracking, and motion/kinematic estimation objectives, but I cannot name them precisely without the full paper details.

### Architecture / parameterization
From the accessible text, this is a multi-stage articulated-scene reconstruction system rather than a single simple predictor. It appears to combine learned perception for part discovery and tracking with geometric/kinematic estimation components to produce canonicalized functional 3D assets.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Most 3D scene reconstruction methods recover what a scene looks like, not how it works. Articulated reconstruction methods often depend on controlled setups, separate state captures, or object priors. That makes them weak fits for real-world embodied data, where interaction happens in messy egocentric streams.

### 2. What is the method?
The method takes egocentric RGB-D interaction footage and uses those interactions as supervision for articulated scene reconstruction. It discovers moving parts, estimates their kinematic structure, tracks their motion in 3D, and reconstructs geometry in a canonical frame so the output can function as a digital twin rather than a static mesh.

### 3. What is the method motivation?
Interaction reveals function. A cabinet door, drawer, or appliance component is much easier to understand when you see it being used than when you only see static appearance. The paper exploits that fact directly instead of treating interaction as nuisance variation.

### 4. What data does it use?
The abstract refers to new real and simulated benchmarks built around egocentric interaction videos. The input modality is RGB-D. I do not have dataset size or scene-category details from the accessible text alone.

### 5. How is it evaluated?
The paper evaluates part segmentation, articulation estimation, pose errors, and reconstruction quality on both real and simulated benchmarks. It also demonstrates downstream utility through simulation export, affordance mapping, and robot-scene interaction.

### 6. What are the main results?
The accessible text claims very strong gains over prior work: up to +50 mIoU in part segmentation, 5 to 10 times lower articulation and pose errors, and better reconstruction accuracy. Those are big improvements, though I have only abstract-level access here and have not inspected the full benchmark setup.

### 7. What is actually novel?
The real novelty is using ordinary egocentric interaction videos to recover functional articulated scene structure without controlled captures or CAD priors. That shifts the task from “reconstruct visible geometry” to “reconstruct what can move and how.”

### 8. What are the strengths?
It targets a genuinely useful output, not decorative 3D. It treats interaction as signal rather than noise. It appears to connect reconstruction to simulation and affordances. And the claimed downstream outputs are exactly the sort of thing embodied systems need.

### 9. What are the weaknesses, limitations, or red flags?
The accessible text does not tell me how robust the system is to partial interaction coverage, sensor noise, ambiguous kinematics, or cluttered scenes with many movable parts. There is also a classic risk that benchmark interactions reveal exactly the motions the method needs, while real deployment may be much sparser and messier.

### 10. What challenges or open problems remain?
Open problems include scaling to larger scenes, handling multiple interacting articulated objects, separating human-hand motion from object motion more robustly, and inferring latent affordances when only a small subset of possible interactions is observed.

### 11. What future work naturally follows?
A natural next step is to fuse this kind of functional reconstruction with persistent scene memory, object-centric world models, or robot policy learning that can plan directly over recovered articulated structure. Another useful direction is combining human demonstrations and robot interactions in a shared functional scene model.

### 12. Why does this matter for cabbageland?
Cabbageland keeps caring about explicit state, reusable structure, and world models that know more than surface appearance. FunRec matters because it pushes 3D reconstruction toward functional state: parts, joints, motion, simulation assets, and affordances. That is a much better substrate for planning than a static pretty mesh.

### 13. What ideas are steal-worthy?
Treat interaction videos as supervision for function, not just view diversity. Canonicalize moving geometry into a simulation-ready scene model. Build reconstruction pipelines whose output is directly useful for affordance maps, planning, and control instead of stopping at photorealistic reconstruction.

### 14. Final decision
Keep. This is strong adjacent inspiration for functional scene modeling and a useful citation whenever we want to distinguish static reconstruction from interaction-grounded world modeling.
