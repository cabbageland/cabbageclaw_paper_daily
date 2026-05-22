# SceneCode: Executable World Programs for Editable Indoor Scenes with Articulated Objects

## Basic info

* Title: SceneCode: Executable World Programs for Editable Indoor Scenes with Articulated Objects
* Authors: Puyi Wang, Yuhao Wang, Linjie Li, Zhengyuan Yang, Kevin Qinghong Lin, Yangguang Li, and Yu Cheng
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2605.19587
* Date surfaced: 2026-05-22
* Why selected in one sentence: It turns indoor scene generation into editable, executable world construction with articulated object programs instead of opaque mesh retrieval.

## Quick verdict

* Useful adjacent inspiration

This is not the most directly actionable paper for cabbageland’s current world-model questions, but it is one of the more structurally honest recent scene-generation papers. The valuable part is the representation choice: object programs, articulation metadata, and persistent scene state are treated as first-class outputs. The main caveat is that much of the pipeline is still agentic scaffolding and validation glue around code generation, so the elegance is more systems-level than learning-theoretic.

## One-paragraph overview

SceneCode takes a natural-language indoor scene prompt and compiles it into a room layout plus per-object executable Blender Python programs, rather than populating the scene from a fixed asset library of static meshes. Each object request is turned into a structured plan, routed through one of several code-generation strategies, executed and repaired in Blender, then compiled into simulation-ready SDF assets with rigid or articulated structure. The paper’s most useful idea is that if you want generated environments to support embodied interaction, then explicit part decomposition, joint semantics, and editable scene state should be native outputs of the generation process rather than annotations stapled on afterward.

## Model definition

This paper is really a multi-stage generative systems pipeline.

### Inputs
The input is a natural-language indoor scene prompt. Internally the system also uses reference images, room-level object requirements, spatial constraints, and structured object specifications produced by upstream planning agents.

### Outputs
The system outputs a renderable indoor scene, a persistent house-state or scene-state record, part-wise executable object programs, generated geometry, and simulator-ready SDF assets. For articulated objects it also outputs inferred joint structure and motion metadata.

### Training objective (loss)
This is not primarily a single end-to-end learned model with one clean objective. It is a routed generation-and-validation pipeline using VLM and LLM components, execution-guided repair, and downstream compilation. Because of that, the paper should be read more as a representation-and-systems contribution than as a crisp optimization result.

### Architecture / parameterization
A room-level planner turns prompts into scene layout and object requests through a planner, designer, and critic loop. Each object request is converted into an ObjectPlan and routed to one of five code-generation strategies. The system then synthesizes part-wise Blender Python programs, executes them in headless Blender, repairs failures using tracebacks, refines successful outputs with image-based critique, and compiles the resulting meshes into rigid or articulated simulator assets. A persistent scene-state registry links layout, object requests, programs, geometry, transforms, and physics-ready metadata.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Most indoor scene generation systems still output static meshes, even when they are marketed for embodied AI or robotic simulation. That means object structure, articulation, and editability are either inherited from a fixed library or absent altogether. The paper is trying to make generated scenes more interaction-ready by having the representation itself expose parts, joints, and editable state.

### 2. What is the method?
Given a scene prompt, the system first produces a room-level plan and a set of object requests. Instead of satisfying those requests by retrieving opaque assets, it converts each request into a structured object plan and synthesizes Blender Python code part by part. Programs are executed and repaired in a bounded loop, then refined based on rendered outputs. The resulting object meshes remain semantically decomposed, so articulated parts can be compiled into joints and exported as simulation-ready SDF assets. Everything is registered into a persistent scene-state file that keeps the world locally editable.

### 3. What is the method motivation?
The motivation is good. If a world is supposed to support embodied reasoning, manipulation, or policy evaluation, then object interaction mechanisms should not be hidden inside a static mesh or limited to whatever happened to exist in a library. Code is attractive here because it naturally exposes part structure, dimensions, materials, and motion mechanisms in a form that can be regenerated and edited.

### 4. What data does it use?
The main evaluation uses 30 natural-language room prompts spanning six indoor scene categories, plus object-level evaluations against generated assets and interaction demos in MuJoCo. The paper also compares against existing scene-generation systems such as SceneSmith, HSM, and LayoutVLM, and against an object-generation baseline for asset quality.

### 5. How is it evaluated?
The paper evaluates room-level scene synthesis quality, prompt faithfulness, object-level mesh and UV usability, code-level editability, articulation support, and downstream robot interaction. It includes automatic scene metrics, human pairwise preference judgments, and demonstrations that the generated articulated objects can be loaded into simulation and manipulated through independent movable links.

### 6. What are the main results?
At the room level, SceneCode is reported as the strongest method on prompt-faithfulness-oriented metrics, with the best object-count and attribute scores in the comparison table and competitive or better navigability and collision behavior. Human raters also prefer it for prompt faithfulness relative to the matched baselines. At the object level, the paper claims cleaner mesh structure, more usable UVs, and more simulator-loadable articulated assets than the baseline it compares against. I buy the direction of the result more than I buy every metric as final proof, because the prompt set and routing logic are still somewhat curated.

### 7. What is actually novel?
The real novelty is not just “use code for 3D generation.” It is the combination of room-level planning, routed part-wise code synthesis, execution-guided repair, articulation-aware compilation, and persistent scene-state registration in service of interaction-ready indoor worlds. The persistent scene-state layer is especially important because it makes world editing and object regeneration part of the representation instead of external bookkeeping.

### 8. What are the strengths?
The representation is much more honest about what embodied systems need. SceneCode produces objects with explicit parts and interaction mechanisms rather than hoping static geometry is enough. The validation loop is also practical. If you are going to generate code, checking whether it actually executes and whether the object matches the requested structure is far better than blind decoding.

### 9. What are the weaknesses, limitations, or red flags?
This is a complex scaffolded pipeline, not a compact learned model. Performance likely depends heavily on prompt routing, repair heuristics, and the bounded execution-refinement loop. The articulation compiler mainly targets dominant indoor mechanisms like hinged or sliding parts, so the approach is not yet a general physical-structure generator. I also do not know, from this read alone, how gracefully the system handles much messier prompts or richer scene diversity outside the evaluated categories.

### 10. What challenges or open problems remain?
A harder version of this problem would require richer object mechanics, better consistency across large scenes, and tighter guarantees that object programs remain semantically correct after repeated edits or regeneration. Another open question is how to connect this kind of executable scene representation to learned world models or planners rather than leaving it as a separate content-generation stack.

### 11. What future work naturally follows?
The obvious next step is to connect executable object programs and persistent scene state to learning loops, such as policy training, world-model pretraining, or simulator editing. It would also be useful to push beyond indoor furniture-style articulations into more varied object mechanics and stronger program reuse.

### 12. Why does this matter for cabbageland?
Because it is a clean example of **world representation as explicit editable state instead of asset soup**. Even though this paper is more on the scene-generation side than the control side, its assumptions are aligned with cabbageland’s taste: if structure matters, the representation should expose it in a way that downstream systems can inspect, modify, and rely on.

### 13. What ideas are steal-worthy?
Treat generated worlds as programs plus state registries, not just geometry. Preserve part-level identity so articulation can be compiled later instead of lost during mesh fusion. Use execution and repair loops as first-class components when code is the representation. Keep a persistent world-state layer that links requests, generated artifacts, and downstream simulation assets.

### 14. Final decision
Worth keeping as adjacent inspiration. It is not a direct answer to memory or planning inside embodied agents, but it is a strong representation paper for anyone who cares about editable simulated worlds with explicit object structure.
