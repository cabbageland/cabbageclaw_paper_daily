# VideoPhysEdit: Physical Counterfactual Video Editing via Rigid-Body Physical Scene Reconstruction

## Basic info

* Title: VideoPhysEdit: Physical Counterfactual Video Editing via Rigid-Body Physical Scene Reconstruction
* Authors: Conghan Yue, Yuanjie Chen, Yue Han, Ya Gao, Yunyan Xiao, WeiYao Zhang, Zhineng Chen
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2609.35134
* Date surfaced: 2026-09-29
* Why selected in one sentence: It treats video editing as physical intervention on an executable reconstructed scene rather than as prompt-conditioned pixel repair.

## Quick verdict

**Highly relevant**

This is a useful physical-world-model paper even though it is framed as video editing. The method is pipeline-heavy and limited to rigid-body scenes, but the central move is correct: infer state and parameters, intervene in that state, simulate the downstream consequences, then guide generation. I read the full arXiv HTML text, including method, benchmark, evaluation protocol, ablations, and limitations.

## One-paragraph overview

VideoPhysEdit defines physical counterfactual video editing: given a source video, a physical edit, and an execution frame, generate the video that should result after the edit changes scene dynamics. Instead of asking a video model to hallucinate the consequences, the pipeline identifies objects, tracks motion, reconstructs geometry and support relations, performs physical inversion to find a rigid-body simulation that reproduces observed motion, applies the requested intervention, and rolls the counterfactual simulation forward. The resulting trajectories and edited reference image guide video generation. The paper also builds PCVE-RigidBench, a benchmark with paired factual and counterfactual videos and physical ground truth, plus Physical Edit Score for trajectory-level evaluation.

## Model definition

### Inputs

Inputs are a source video, a physical edit instruction or benchmark operation, an execution frame, object/motion observations from tracking, reconstructed scene geometry, and candidate physical parameters for rigid-body simulation.

### Outputs

The system outputs a counterfactual edited video. Internally it outputs reconstructed scene state, simulated counterfactual trajectories, motion/appearance controls, and an edited reference image used by the video generator.

### Training objective (loss)

The pipeline is training-free with respect to the main method. Physical inversion searches for simulation parameters and initial states that reproduce observed motion and contacts, and video generation uses pretrained released components. The paper does not introduce a new end-to-end learned loss for the full system.

### Architecture / parameterization

This is a hybrid pipeline: object identification and tracking, geometry reconstruction, support and contact analysis, rigid-body physical inversion in simulation, intervention rollout, and conditional video generation. The core "model" is the explicit reconstructed physical scene plus a pretrained generator guided by simulated trajectories.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Existing video editing methods can alter pixels while failing to model the downstream physical consequences of an intervention. If an object is inserted, removed, or changed, later motion and contacts should change too.

### 2. What is the method?

The method reconstructs a simulation-ready rigid-body scene from the source video, searches for physical parameters that reproduce observed motion, applies the requested edit as a physical intervention, simulates the counterfactual, and uses that simulated trajectory to guide video generation.

### 3. What is the method motivation?

Counterfactual motion is not directly visible in the source video. A physical edit changes causal state, so the system needs an executable state transition model rather than only a visual edit model.

### 4. What data does it use?

The benchmark uses 20 synthetic rigid-body scenes with 129 source-counterfactual pairs rendered in Blender with PyBullet physical ground truth. The paper also shows qualitative real-video examples.

### 5. How is it evaluated?

The paper evaluates on PCVE-RigidBench with Physical Edit Score, mask IoU, and visual fidelity metrics. Physical Edit Score measures trajectory-error improvement toward the counterfactual target relative to leaving the source unchanged.

### 6. What are the main results?

VideoPhysEdit reports the best physical edit accuracy among compared methods and a Physical Edit Score of 0.376, the only positive score in the comparison. The paper also reports that reconstructing a physical scene and simulating the intervention improves downstream trajectory accuracy relative to methods that directly infer the counterfactual visually.

### 7. What is actually novel?

The novelty is the combination of PCVE as a task, explicit physical scene reconstruction from video, simulation-backed intervention rollout, and a benchmark/metric that evaluates downstream physical consequences instead of visual plausibility alone.

### 8. What are the strengths?

* The causal intervention framing is strong.
* The benchmark includes paired counterfactual targets and physical ground truth.
* The method separates factual reconstruction, physical inversion, intervention, and generation.
* The metric penalizes edits that look plausible but do not move toward the counterfactual target.

### 9. What are the weaknesses, limitations, or red flags?

The scope is rigid-body scenes with relatively constrained interactions. Pipeline errors compound: tracking, geometry, physical inversion, and video generation can each fail. Real-world generalization is shown qualitatively rather than as a broad measured claim.

### 10. What challenges or open problems remain?

Handling deformable objects, fluids, articulated bodies, ambiguous observations, occlusions, and richer natural videos remains open. The system also needs stronger uncertainty over reconstructed physical parameters.

### 11. What future work naturally follows?

* Add uncertainty-aware physical inversion and multiple plausible counterfactual rollouts.
* Extend PCVE to articulated or deformable scenes.
* Use differentiable or learned simulators where explicit PyBullet-style reconstruction is too brittle.

### 12. Why does this matter for cabbageland?

It is a good example of explicit state doing useful work. The video generator is not trusted to invent physics from vibes; an executable scene supplies the state transition.

### 13. What ideas are steal-worthy?

* Evaluate physical edits by trajectory improvement against counterfactual ground truth.
* Use physical inversion as a bridge between perception and generative editing.
* Treat interventions as operations on state, not just operations on pixels.

### 14. Final decision

**Keep.** The method is bounded, but the task and evaluation frame are exactly the right kind of pressure on video world models.
