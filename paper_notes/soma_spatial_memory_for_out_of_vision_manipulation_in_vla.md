# Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action

## Basic info

* Title: Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action
* Authors: Xinhao Li, Yuhao Lian, Yuhan Yang, Jialiang Zhang, Huijie Dong, Dale Schuurmans, Jian Yang, Jiwen Lu
* Year: 2026
* Venue / source: ICML 2026 / arXiv
* Link: https://arxiv.org/abs/2605.22283
* Date surfaced: 2026-05-23
* Why selected in one sentence: It tackles a real VLA failure mode, objects leaving the current camera frustum, with explicit persistent spatial memory rather than pure prompt-and-frame reactiveness.

## Quick verdict

**Highly relevant**

This is one of the better recent embodied systems papers because the memory claim cashes out into an actual computational contract. SOMA is not conceptually minimal, and it depends on a stack of borrowed perception modules, but the paper does make persistent multi-view scene memory operationally useful for search, grounding, and action when the target is not visible. I inspected the arXiv HTML full text, including the method and main evaluation sections, but not every appendix table and ablation detail.

## One-paragraph overview

SOMA starts from a simple criticism of current vision-language-action systems: most of them act as though the world only exists inside the current image. If the target object moves outside the field of view, the policy either searches clumsily or fails. SOMA gives the robot a movable head camera, runs a dedicated scan when needed, lifts multi-view detections and geometry into a global spatial-semantic memory, keeps refining that memory during interaction, and retrieves instruction-relevant memory regions back into the manipulation policy. The result is a system that can act on remembered scene structure rather than only whatever is currently visible.

## Model definition

### Inputs
The system takes language instructions, current multi-camera RGB observations from left arm, right arm, and head cameras, robot state, a noised action sequence for diffusion-style decoding, and the persistent spatial memory built from head-camera scans. During memory construction it also consumes sampled frames from a scanning video sequence.

### Outputs
It outputs spatial memory tokens representing fused object semantics and geometry, refined memory updates over time, memory-retrieved context features, and finally the next action chunk for manipulation.

### Training objective (loss)
From the accessible paper text, the action model is trained as a DiT-style action decoder over noised action sequences, but the full loss decomposition is not described as crisply as I would like in the inspected sections. The memory construction pieces rely mostly on pretrained geometry and semantic components rather than a single end-to-end learned memory objective. So the honest answer is that the exact total training loss for the whole stack is only partially clear from the text I inspected.

### Architecture / parameterization
This is a hybrid system. Memory construction uses pretrained YOLO for detection, DINOv3 for appearance features, and VGGT for camera pose plus coarse geometry. Object features and 3D box encodings are fused into memory tokens, then dynamically refined and retrieved. The downstream action model is a DiT-based vision-language-action decoder.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve out-of-vision manipulation in VLA systems. Standard setups often assume that task-relevant objects are visible when the action must be chosen. That assumption breaks as soon as the target is occluded or simply outside the camera view.

### 2. What is the method?
The method has three parts. First, **Spatial Memory Construction** scans the workspace with a movable head camera and fuses multi-view object detections and geometry into a global object-level memory. Second, **Dynamic Memory Refinement** updates that memory as new observations arrive. Third, **Contextual Memory Retrieval** queries the memory with instruction-aware representations and feeds the retrieved context into a DiT-based action decoder.

### 3. What is the method motivation?
The motivation is that purely reactive view-bound policies cannot manipulate what they cannot currently see. If the system wants to do grounded action in partially observed scenes, it needs some persistent world substrate that survives camera motion and temporary invisibility.

### 4. What data does it use?
The paper evaluates on five self-designed real-world out-of-vision manipulation tasks, plus RoboCasa Tabletop GR1 and SimplerEnv for additional validation under more conventional settings. The memory is built from head-camera scan videos over the workspace.

### 5. How is it evaluated?
It is evaluated with success rate on the real-world out-of-vision tasks and with additional benchmark results on RoboCasa GR1 and SimplerEnv. The paper also highlights behavior changes such as faster target fixation, less unnecessary search, and near one-shot grasping in some cases.

### 6. What are the main results?
The paper reports clear gains over the compared VLA baselines on its real-world out-of-vision tasks, and it claims that SOMA also helps under standard observable settings rather than only in the custom benchmark. The exact margins look encouraging, but I did not independently audit every table and protocol detail, so I trust the directional result more than the precise leaderboard spread.

### 7. What is actually novel?
The novelty is not “memory” in the abstract. The novelty is the specific operational loop in which active scanning builds a persistent spatial-semantic memory that is then queried during manipulation for out-of-view target grounding. The important point is that the memory is object-level and scene-level, not just a short temporal cache of frames.

### 8. What are the strengths?
- It attacks a real embodied failure mode instead of a benchmark toy problem dressed up as generality.
- Memory is tied to a concrete use case: recoverable manipulation beyond the current frustum.
- The system uses explicit object and geometry structure instead of hoping generic VLM reasoning will hallucinate missing world state.
- Real-world evaluation matters here more than another simulator-only claim would.

### 9. What are the weaknesses, limitations, or red flags?
- The system is fairly heavy and modular, with several pretrained subsystems doing important work.
- The paper’s learning story is weaker than its systems story. This is more engineered composition than a clean learned world model.
- It leans on short-horizon static-scene assumptions during scanning, which may make memory construction easier than messier dynamic settings.
- The custom benchmark is useful, but also makes it easier to optimize for the paper’s favored failure mode.

### 10. What challenges or open problems remain?
A major open problem is how to make this kind of memory cheaper, cleaner, and more adaptive in dynamic scenes where objects move, people interfere, or the robot cannot afford a neat scanning phase. Another is how to move from object boxes plus features toward richer persistent state with affordances and object state changes.

### 11. What future work naturally follows?
- Learn more of the memory stack end to end instead of relying so much on stitched pretrained modules.
- Replace periodic scanning with more opportunistic or uncertainty-aware exploration.
- Extend the memory representation to object state, articulation, and affordance rather than mostly identity plus location.
- Test whether similar memory contracts help mobile manipulation beyond tabletop settings.

### 12. Why does this matter for cabbageland?
Because it is a concrete example of explicit persistent state doing real work in an embodied pipeline. The paper is not pretending that “reasoning” alone can recover missing perception. It says that if the object is out of view, the system needs a remembered world, and then it actually builds one.

### 13. What ideas are steal-worthy?
- Give memory a real job contract: maintain targetable scene state when the current image is insufficient.
- Use active perception to initialize memory rather than waiting for accidental coverage.
- Keep memory retrieval instruction-conditioned so the representation does not become a dead archive.
- Treat out-of-view manipulation as a first-class evaluation axis for VLA systems.

### 14. Final decision
**Preserve.** Not because it is a clean final-form architecture, but because it makes an important point clearly: persistent spatial memory is valuable when the world keeps existing after the camera turns away.
