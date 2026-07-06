# WorldDirector: Building Controllable World Simulators with Persistent Dynamic Memory

## Basic info

* Title: WorldDirector: Building Controllable World Simulators with Persistent Dynamic Memory
* Authors: Hanlin Wang, Hao Ouyang, Qiuyu Wang, Wen Wang, Qingyan Bai, Ka Leong Cheng, Yue Yu, Yixuan Li, Yihao Meng, Zichen Liu, Yanhong Zeng, Yujun Shen, Qifeng Chen
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.02517
* Date surfaced: 2026-07-06
* Why selected in one sentence: It separates 3D semantic motion planning from video synthesis so dynamic objects keep persistent identity and trajectory while off-screen.

## Quick verdict

* Preserve-worthy with caveats

This is the most useful generative world-model paper in today's scan. I inspected the full PDF, including the method overview, experiments, ablations, conclusion, and stated limitation. The caveat is real: the visual domain is still synthetic / game-like, and the examples depend on the underlying video model. The design pattern is nevertheless good.

## One-paragraph overview

WorldDirector targets a specific failure in video world models: dynamic objects often stop, drift, or change identity when they leave the camera view and later re-enter. The paper argues that object permanence should not be left inside entangled pixel generation. Its framework uses an LLM as a central orchestrator that translates user instructions into 3D object and camera trajectories. Those trajectories are projected into 2D location conditions for a causal chunk-based video generator. Appearance Binding injects visual anchors from prior context, and spatial-aware cross-attention routes entity-specific prompts to the right regions. The result is a controllable video simulator where off-screen objects can continue moving and reappear with more stable identity.

## Model definition

### Inputs
The system takes an initial frame, user instructions describing camera and object behavior, context from prior generated chunks, and LLM-generated 3D trajectories for camera and dynamic entities.

### Outputs
It outputs long-horizon generated video chunks with controlled camera motion, object trajectories, and persistent appearance of dynamic entities.

### Training objective (loss)
The paper builds on LingBot-World-Base and trains with video-generation objectives under location, appearance, and context conditioning. The details in the inspected text emphasize reconstruction and consistency rather than a new standalone loss.

### Architecture / parameterization
WorldDirector combines an LLM planner, 3D-to-2D projection of object/camera trajectories, location conditioning, appearance conditioning, sequence-concatenated historical context, causal chunk generation, and spatial-aware cross-attention for entity-specific control.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Video world models can preserve static backgrounds for a while, but they often fail object permanence for dynamic entities. If an object leaves the view, the model may freeze it, forget its trajectory, or recreate it with a different identity when it returns.

### 2. What is the method?
WorldDirector decouples motion planning from rendering. An LLM plans 3D trajectories and events; the video model receives projected location controls, appearance anchors, and context memory while generating causal chunks.

### 3. What is the method motivation?
Object permanence requires a state variable outside the current pixels. If the renderer alone is responsible for invisible motion, it has to infer dynamics from priors and often collapses. Explicit trajectory orchestration gives the renderer a state contract.

### 4. What data does it use?
The paper uses a data pipeline to build training and test videos with dynamic entities, camera motion, and trajectory annotations. The inspected text states a 100-video test set of novel scenes and subjects, and notes the synthetic game-data domain gap.

### 5. How is it evaluated?
It compares against causal interactive world-model baselines including Yume 1.5, HY-World, Infinite-World, LingBot-World-Fast, and HyDRA. Metrics include PSNR, SSIM, LPIPS, VBench subject/background consistency, and dynamic subject consistency using DINO and CLIP similarities on detected object crops.

### 6. What are the main results?
WorldDirector reports the best reconstruction metrics in the table: PSNR 18.127, SSIM 0.502, LPIPS 0.359, and best dynamic subject consistency by CLIP. The ablation removing Appearance Condition lowers all listed metrics, including dynamic subject consistency, and qualitative examples show identity loss when the explicit appearance channel is removed.

### 7. What is actually novel?
The novelty is not simply "LLM controls video." It is the separation of semantic 3D orchestration, location control, and appearance binding as explicit memory for dynamic entities.

### 8. What are the strengths?
The paper names a real world-model failure, designs directly against it, and includes ablations showing that appearance binding is not cosmetic. It also supports promptable new events, not only extrapolation of objects visible in the first frame.

### 9. What are the weaknesses, limitations, or red flags?
The authors note a domain gap from synthetic game data, producing unnatural locomotion or blurry faces. The method also depends on the quality of the LLM planner and the base video generator. The evidence is not yet a general physical-simulation benchmark.

### 10. What challenges or open problems remain?
The major challenge is real-world fidelity under complex interactions, occlusion, and multi-object physical contact. Another challenge is verifying whether planned 3D trajectories are physically plausible rather than merely consistent enough for video metrics.

### 11. What future work naturally follows?
Train and evaluate on real-world dynamic scenes, add physical constraints or simulators to the LLM trajectory planner, and test whether object permanence survives longer horizons and denser interactions.

### 12. Why does this matter for cabbageland?
The transferable idea is to keep persistent dynamics outside the renderer. For world models, agents, and long-horizon visual planning, the state that matters should be explicit enough to update and inspect.

### 13. What ideas are steal-worthy?
Use an explicit trajectory layer for invisible dynamics. Bind appearance separately from location. Generate in causal chunks but carry structured memory forward. Treat off-screen object motion as state evolution, not as a hallucination task.

### 14. Final decision
Keep as a useful generative-world-model note. The current evidence is not a production-grade simulator, but the architecture points in the right direction: persistent state first, rendering second.
