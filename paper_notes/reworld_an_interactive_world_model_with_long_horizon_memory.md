# ReWorld: An Interactive World Model with Long-Horizon Memory

## Basic info

* Title: ReWorld: An Interactive World Model with Long-Horizon Memory
* Authors: Zhifei Chen, Luozhou Wang, Guibao Shen, Dongyu Yan, Shuai Yang, Tianshuo Xu, Yihua Du, Wei Wang, Tianyi Gui, Lianghua Huang, Yingcong Chen
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.23565
* Date surfaced: 2026-08-25
* Why selected in one sentence: It is the strongest systems paper in the batch on separating short-horizon control from long-horizon revisit memory and on making that separation deployable under a fixed KV budget.

## Quick verdict

* Must read

I inspected the full arXiv HTML text, especially the introduction, method sections on mixed attention windows and memory consolidation, the data-pipeline description, and the experiment setup and claims. This paper earns a preserved note because it names a real conflict instead of pretending more context solves everything: control wants a short attention window, memory wants a long one, and deployment still needs bounded inference. ReWorld's value is that it resolves all three pressures with a coherent package rather than a slogan.

## One-paragraph overview

ReWorld is an interactive video world model designed to follow user actions, preserve revisit consistency over long horizons, and still stream in real time. The core move is to split control and memory by training window rather than by separate models. Most attention heads are trained on short local windows, a small subset is trained on full-history access, and random head routing keeps either capability from binding to a fixed subset of heads. At inference, the full history is not kept in memory. Instead, the model runs with a fixed 12-chunk cache backed by a pose-indexed landmark bank that stores sparse, full-resolution snapshots of earlier views and retrieves the landmarks nearest the current camera pose. Chunk-drop training makes these sparse non-contiguous caches in-distribution, and a rank-128 LoRA distillation path compresses inference to four denoising steps for real-time use.

## Model definition

### Inputs
Text prompts or captions, recent video chunks, per-chunk 6-DoF action commands, relative SE(3) camera trajectories for pose-indexed attention, and at inference a retrieved set of pose-near landmark chunks plus recent chunks under a fixed KV budget.

### Outputs
Streaming future video chunks that follow the commanded camera motion while preserving revisit consistency over long rollouts.

### Training objective (loss)
The paper clearly specifies distribution-matching distillation with self-forcing rollouts for the real-time four-step LoRA path. The exact base generative loss for the underlying streaming video model is not made explicit in the method excerpts I inspected, so I would not bluff a more specific objective than next-chunk generative world-model training plus the DMD-style distillation stage.

### Architecture / parameterization
Streaming video world model with pose-indexed attention (MRoPE), direct action injection, mixed per-head attention windows, random head routing, a pose-retrieved landmark memory bank under a fixed 12-chunk cache, chunk-drop training, and a rank-128 LoRA for four-step real-time distillation.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the fact that interactive world models need three things at once - action following, revisit memory, and real-time streaming - and the naive way to push one of those usually harms the others.

### 2. What is the method?
The method trains control and memory under different attention windows inside one backbone, rotates which heads get global access so the capability does not attach to specific heads, then deploys with a bounded landmark bank that stores and retrieves old chunks by camera pose. A four-step LoRA distillation path makes the same backbone usable in real time.

### 3. What is the method motivation?
Control only needs the recent scene and the current command, so it should not depend on long history. Memory is the opposite: it can only be learned if the model sometimes sees the far past. Deployment then introduces a third constraint, because full-history attention is too expensive to keep online.

### 4. What data does it use?
An eight-source joint corpus combining Unreal-rendered fly-throughs, game roaming footage, and real-world video. The training mixture is reported as 63% UE, 26% real, and 11% game at the clip level. Each sample is a 189-frame window at 24 fps, about 8 seconds long, with RGB frames, captions, actions, and trajectories. Palindrome trajectories are injected on two UE sources with probability 0.2 to provide revisit evidence.

### 5. How is it evaluated?
On three axes: camera controllability, long-horizon memory, and generation quality, against six recent interactive world-model baselines. The memory test uses minute-long out-and-back rollouts where the model must reconstruct the starting view after a long absence.

### 6. What are the main results?
The paper reports the best control fidelity among compared systems at 11.95 degrees rotation error, the best camera-motion consistency, and the best generation quality. On 64-second out-and-back rollouts covering 384 latents, the model's fixed 12-chunk cache can still regenerate the starting view at rollout lengths where sliding-window memory has already discarded the needed evidence.

### 7. What is actually novel?
The real novelty is not "memory for world models" in the generic sense. It is the combination of mixed per-head window training, random head routing so all heads experience both local and global regimes, a pose-retrieved landmark cache under a hard inference budget, and chunk-drop training that matches training-time attention to the sparse memory pattern used at deployment.

### 8. What are the strengths?
The paper has a real systems thesis. It names the control-memory conflict clearly, makes an explicit design choice about it, and follows through all the way to deployment constraints. The landmark bank is also better than generic compression talk because it preserves whole chunks and sparsifies by spatial redundancy instead of degrading everything uniformly.

### 9. What are the weaknesses, limitations, or red flags?
This is still camera-trajectory memory, not full semantic world-state memory. The memory retrieval key is pose, so the system is strongest on revisiting views rather than on tracking object identity, causal dynamics, or open-ended agent-environment interaction. The revisit evidence is also partially injected by palindrome trajectories, which is a useful curriculum but not the same as naturally arising revisit structure.

### 10. What challenges or open problems remain?
Extending this from egocentric visual revisit memory to object-level or event-level memory in dynamic scenes. Another open problem is whether the same separation still works when actions are not simple camera motions but embodied manipulations with irreversible scene change.

### 11. What future work naturally follows?
Pose-plus-object retrieval, learned memory admission policies, memory keyed by causal state rather than only spatial proximity, and hybrid interactive world models that can preserve both viewpoint consistency and object-state consistency over long horizons.

### 12. Why does this matter for cabbageland?
Because cabbageland keeps caring about explicit memory, fixed-budget inference, and world models that do not confuse longer context with actual state management. This paper is unusually useful because it turns that concern into a clean design pattern.

### 13. What ideas are steal-worthy?
Train the same backbone under both short and long windows, but randomize which heads get which regime. Preserve old evidence as sparse full-resolution landmarks instead of compressing everything equally. Make sparse deployment memory in-distribution with chunk-drop training. Distill only the fast path with a plug-in LoRA so the main model and control channels stay intact.

### 14. Final decision
Keep as a preserved note. This is one of the better recent world-model systems papers because it has a real bottleneck, a real mechanism, and a real deployment story.

## 6. Mandatory critical angles

The paper is strongest on mechanism, explicit memory, deployment realism, and controllability. It earns the world-model label because it is about future video under action with persistent revisit state, not just a branded video generator. The main limitation is representational scope: the memory is spatial and camera-indexed, not yet a broader explicit scene model.

## 7. Writing style

The right tone is admiring but not breathless. The paper deserves praise because it actually resolves a structural conflict instead of smearing it across more tokens.

## 8. Repository output format

Saved as a preserved paper note because the control-memory separation and fixed-budget landmark-retrieval design are likely to transfer to future cabbageland work.
