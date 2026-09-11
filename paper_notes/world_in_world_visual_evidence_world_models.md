# World in World: Explore the World with World Models

## Basic info

* Title: World in World: Explore the World with World Models
* Authors: Chenxi Song, Yanming Yang, Chi Zhang
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2609.11548
* Date surfaced: 2026-09-11
* Why selected in one sentence: It shows how to control a frozen causal video world model by converting heterogeneous visual evidence into native attention-readable state.

## Quick verdict

* Must read

I inspected the full arXiv HTML text, including the visual-evidence representation, target-view scene evidence, rendered geometry evidence, retrieved generated history, correspondence-guided attention routing, evidence-wise attention CFG, quantitative comparisons, and ablations. This is worth preserving because the mechanism is an interface design for frozen world models, not just a camera-control benchmark result.

## One-paragraph overview

World in World is a training-free inference interface for frozen causal video world models. It takes heterogeneous control evidence, such as a source video, a target camera view, rendered geometry, and previously generated states, and converts it into camera- and time-labelled clean visual states. These states are inserted as key/value evidence that the frozen model can read through native self-attention. Correspondence-guided attention routing uses persistent point identities and geometry to tell the model where to read from, while evidence-wise attention CFG regulates how strongly each auxiliary evidence source should push the denoising response. The result is a single interface for camera-controlled rerendering, long-horizon revisiting, stabilization, editing, K/V sharing, and motion transfer without fine-tuning the backbone.

## Model definition

### Inputs
The system takes a source video, target camera trajectory or target view request, optional target-view projections, rendered geometry for newly exposed regions, and retrieved generated states from a history bank. Each evidence item is represented as visual content plus camera, time, spatial support, and availability metadata.

### Outputs
The frozen causal video model outputs generated video frames under the requested camera and control conditions. For rerendering, the output should stay synchronized with the source event while presenting it from the target camera trajectory.

### Training objective (loss)
World in World introduces no new training objective. It keeps the LingBot-World 2.0 causal-fast checkpoint frozen and operates as an inference-time visual-evidence and attention-routing interface.

### Architecture / parameterization
The backbone is a frozen causal video world model. Evidence is encoded by running the frozen denoising network with the diffusion timestep set to zero to cache clean key/value states. Native source-anchor slots store source-video evidence; other evidence enters as temporary auxiliary attention blocks. Correspondence-guided attention routing adds geometry-derived correspondence weights to attention scores, and evidence-wise attention CFG modifies attention responses for each evidence source inside the same denoising forward pass.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Frozen video world models can roll forward visual states, but flexible control is hard when the evidence comes in different forms: source observations, target camera views, geometry hints, old generated frames, and edit conditions. The paper wants a unified way to make those evidence types usable without retraining the model for each control mode.

### 2. What is the method?
The method converts each evidence source into a clean visual state with camera, time, spatial support, and availability labels. These states are read through native self-attention. CGAR routes attention toward geometrically corresponding source-video tokens, and EWA separately adjusts each evidence channel's contribution relative to the native attention response.

### 3. What is the method motivation?
The useful premise is that a causal video model already knows how to read recent clean visual states. If control information can be expressed in that same internal language, then model extension becomes evidence construction and attention regulation rather than fine-tuning or bolting on a new controller.

### 4. What data does it use?
The paper evaluates on camera-controlled video rerendering over DAVIS and OpenVid-1M source videos. The method itself is training-free and uses a frozen LingBot-World 2.0 causal-fast checkpoint.

### 5. How is it evaluated?
Evaluation covers VBench dimensions, camera trajectory errors, and image fidelity metrics. The baselines include ReCamMaster, TrajectoryCrafter, WorldForge, InSpatio-World, UniWorld-View, and CameraAnything. Ablations remove EWA, CGAR, target-view warping, and source-camera Pluecker conditioning.

### 6. What are the main results?
On the main rerendering table, World in World reports the best overall VBench score at 85.192, lowest rotation error at 2.8326 degrees, best PSNR at 23.1511, best SSIM at 0.787205, and near-best LPIPS at 0.121664. The ablation table shows that removing target-view warping is the largest failure: rotation error rises from 1.7823 to 6.1158 and translation error from 0.053291 to 0.581847 on DAVIS.

### 7. What is actually novel?
The novelty is the clean-state evidence interface plus attention-level routing and guidance. The paper does not just condition on camera rays. It makes several visual evidence sources look like the model's own state, then decides where and how strongly to read each one.

### 8. What are the strengths?
The mechanism is compact, reusable, and aligned with how causal video models already operate. The ablations are also informative: they show that spatially aligned target-view evidence is not optional, and that correspondence routing and evidence-wise guidance help preserve appearance and structure.

### 9. What are the weaknesses, limitations, or red flags?
This is not a full physical world model. It can rerender and complete videos using a strong frozen prior, but the representation is still visual and attention-mediated. The evidence can be wrong or incomplete, and the paper does not solve global scene state, physical consistency, or long-horizon planning uncertainty.

### 10. What challenges or open problems remain?
Open problems include reliable uncertainty over evidence sources, persistent explicit scene state, handling large topological changes, making generated history auditable, and connecting visual evidence routing to action-conditioned planning rather than camera/view control alone.

### 11. What future work naturally follows?
Future work should add confidence estimates for each evidence source, explicit memory compaction for generated history, multi-camera or 3D scene-state integration, and downstream planning tests where wrong evidence can hurt decisions.

### 12. Why does this matter for cabbageland?
Cabbageland cares about world models that can carry state across boundaries. This paper is a concrete pattern for doing that: label the state carrier, align it spatially and temporally, route attention through correspondences, and avoid pretending one generic prompt can carry all control semantics.

### 13. What ideas are steal-worthy?
Use native model state as the interface for new controls. Attach source, target, geometry, and history evidence as separately scheduled channels. Route attention using explicit correspondences. Regulate auxiliary evidence by subtracting the native response direction before amplifying the useful correction.

### 14. Final decision
Keep as a must-read preserved note. The paper is not a complete world-model solution, but the evidence-interface design is exactly the kind of transferable mechanism worth remembering.
