# HorizonStream: Long-Horizon Attention for Streaming 3D Reconstruction

## Basic info

* Title: HorizonStream: Long-Horizon Attention for Streaming 3D Reconstruction
* Authors: Chong Cheng, Peilin Tao, Nanjie Yao, Guanzhi Ding, Xianda Chen, Yuansen Du, Xiaoyang Guo, Wei Yin, Weiqiang Ren, Qian Zhang, Zhengqing Chen, Hao Wang
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2605.23889
* Date surfaced: 2026-05-25
* Why selected in one sentence: It gives a crisp explanation for long-horizon streaming 3D failure and replaces refresh-or-drift memory hacks with a learned recurrent geometric retention state.

## Quick verdict

* Useful

This is adjacent rather than central, but it is one of the better long-sequence systems papers in recent 3D work. I inspected the full text through arXiv HTML and PDF text extraction, including the method, main benchmark tables, and ablations around retention behavior. The mechanism is more interesting than the headline benchmark chase because it makes memory shape explicit.

## One-paragraph overview

HorizonStream treats streaming 3D reconstruction as a memory-kernel problem. Existing methods either keep growing opaque state that gets contaminated over time or periodically refresh that state and lose continuity. The paper proposes Geometric Linear Attention, which compresses cross-window reconstruction evidence into an O(1) recurrent state with learned channel-wise retention so old information can decay smoothly rather than being abruptly forgotten or indefinitely preserved. The result is a constant-memory streaming system that reportedly stays stable on sequences far longer than the clips it was trained on.

## Model definition

### Inputs
The system takes sequential image frames in a streaming multi-view reconstruction setting, processed in short causal windows with calibration-free pose and geometry cues carried across windows through recurrent state.

### Outputs
It outputs online camera pose and 3D reconstruction estimates, with the recurrent state carrying compressed geometric evidence across time.

### Training objective (loss)
The accessible core text makes the training schedule and datasets clear, but I did not fully audit every objective term in the appendices. The safe summary is that the model is trained for streaming 3D reconstruction and pose estimation with learned recurrent attention state, optimized over multi-dataset geometric supervision.

### Architecture / parameterization
A streaming 3D reconstruction model with Geometric Linear Attention, meaning a causal windowed transformer-like stack whose cross-window memory is a learned recurrent geometric state with channel-wise retention parameters.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Long streaming sequences break many reconstruction systems because their memory either drifts, gets contaminated, or has to be periodically reset. That makes nominal long-horizon support much weaker than advertised.

### 2. What is the method?
The method replaces naive cache carryover with Geometric Linear Attention. Cross-window geometric evidence is summarized into a bounded recurrent state, and learned retention controls how different channels preserve or discount old evidence over time.

### 3. What is the method motivation?
The motivation is that long-horizon online reconstruction needs selective persistence, not just more tokens. A useful memory should retain stable structure, forget stale evidence, and avoid hard discontinuities from refresh-based tricks.

### 4. What data does it use?
The paper trains on 24 datasets spanning indoor, outdoor, and driving scenes. Reported evaluations include VKITTI2, KITTI, Oxford, ScanNet++, TUM, Waymo, VBR, ETH3D, Oxford Spires, and 7Scenes.

### 5. How is it evaluated?
The paper reports absolute trajectory error on multiple streaming datasets, long-sequence VBR results, reconstruction metrics such as chamfer distance and F1, and KITTI depth estimation comparisons. It also includes ablations around retention bands and no-refresh versus refresh behavior.

### 6. What are the main results?
The paper claims stable generalization to sequences beyond 10,000 frames with constant memory and linear time. In the cross-dataset comparison table, HorizonStream reports better average KITTI ATE than most streaming methods and strong results on Oxford, TUM, and Waymo, while an added loop-closure variant improves some numbers further. On VBR, the plain model reports 37.42 average ATE and the loop-closure variant 12.76, beating other streaming baselines listed there.

### 7. What is actually novel?
The useful novelty is the explicit retention-kernel story. The paper does not just say “we made streaming longer.” It argues that different evidence channels need different decay timescales and builds that idea directly into recurrent geometric attention.

### 8. What are the strengths?
The mechanism is conceptually clean, the paper diagnoses why refresh/no-refresh baselines fail, and the evaluations include genuinely long sequences rather than only short in-domain clips. I also like that the memory remains bounded instead of quietly scaling with horizon.

### 9. What are the weaknesses, limitations, or red flags?
This is still a specialized geometric reconstruction system, so transfer to broader world-model or embodied-memory problems is indirect. Some of the table formatting is messy enough that exact comparison reading takes care, and I would want more adversarial stress tests around moving objects or stronger non-rigid scenes. The loop-closure variant also means not every headline number comes from the same pure online regime.

### 10. What challenges or open problems remain?
Handling harder dynamic scenes, integrating stronger semantic structure into the retained geometric state, and understanding how to set or learn retention policies when the environment’s timescales shift sharply.

### 11. What future work naturally follows?
Use similar retention-state ideas in other long-horizon perception or world-model settings, combine geometric memory with explicit object memory, and study whether retention spectra can become controllable rather than only learned.

### 12. Why does this matter for cabbageland?
Because it makes a recurring point very clearly: long-horizon competence is often a memory-policy problem, not just a context-window problem. If a system keeps failing after a few hundred steps, the right fix may be a better retention kernel rather than a bigger latent bucket.

### 13. What ideas are steal-worthy?
Treat retention shape as a first-class design object. Use bounded recurrent evidence state instead of opaque ever-growing caches. Diagnose long-horizon failure by asking what the memory is forgetting too early and what stale evidence it is preserving too long.

### 14. Final decision
Keep as adjacent inspiration. It is not directly about agents or control, but it is a strong reference for explicit long-horizon memory design and for explaining why naive streaming state tends to rot.