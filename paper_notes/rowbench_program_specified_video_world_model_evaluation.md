# ROWBench: Do Video Models Render What the Program Specifies?

## Basic info

* Title: ROWBench: Do Video Models Render What the Program Specifies?
* Authors: Zheng-Hui Huang, Guixu Lin, Yu-Ju Tsai, Jian-Kai Zhu, Fengbo Lan, Yu-Lun Liu, Yung-Yu Chuang, Kaipeng Zhang, Zhixiang Wang
* Year: 2026
* Venue / source: arXiv:2610.02205
* Link: https://arxiv.org/abs/2610.02205
* Date surfaced: 2026-10-02
* Why selected in one sentence: It evaluates whether video world models faithfully render executable world-state records and timestamped program events.

## Quick verdict

* Must read

This is the strongest evaluation paper in the batch. Its value is the contract: a generated video is checked against a replayable world record, not against generic plausibility. The paper name says ROWBench, while the body uses PROWBench; the mechanism and contribution are still clear.

## One-paragraph overview

ROWBench/PROWBench builds programmatic world episodes with explicit entity identities, transforms, camera trajectories, action phases, and timestamped events. The same execution record can be rendered into synchronized proxy videos such as coarse 3D, semantic proxies, or colored oriented bounding boxes, and generated videos are then scored against the program's observable consequences. The benchmark includes 170 dynamic episodes and 600 proxy videos, covering first-person and third-person views, some synchronized multi-view scenes, and a long-horizon track where entities leave and re-enter view. The useful move is that it separates "the program ran" from "the video rendered what the program specified."

## Model definition

### Inputs

The benchmark provides recorded world states, entity definitions, camera trajectories, scene descriptions, action timelines, timestamped event logs, and visual proxy videos. Evaluated models receive whatever control inputs their native interface supports: camera paths, depth, segmentation, CWM proxies, coarse 3D proxies, colored-OBB proxies, first frames, and text prompts.

### Outputs

The evaluated video models output RGB videos that should follow prescribed camera motion, entity trajectories, identities, action phases, event outcomes, and multi-view consistency.

### Training objective (loss)

ROWBench does not introduce a new trainable generator. Its metrics use off-the-shelf components, including SAM 3 for localization and Qwen3.6-27B for event/timeline judging. The paper is an evaluation framework rather than a model trained with a new loss.

### Architecture / parameterization

The core system is a programmatic world-generation and evaluation pipeline. It has a world synthesis stage, a control-compilation stage that renders synchronized proxy representations from shared records, and an evaluation suite for controllability, logic/state alignment, long-horizon memory, multi-view consistency, and video quality.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Programmable world models can maintain explicit state and executable rules, but the learned video renderer may fail to visualize the actual state transitions, interactions, or object identities. Existing benchmarks often reward visual quality or broad controllability without checking against fine-grained program-specified events.

### 2. What is the method?

Generate episodes from executable world records, render multiple synchronized proxy representations, feed these controls to video models, and evaluate generated videos against recorded entity states and timestamped events.

### 3. What is the method motivation?

If world models are going to act like game engines or simulators, then plausibility is not enough. The video must show the consequences of the executed program.

### 4. What data does it use?

The benchmark contains 170 dynamic programmatically constructed episodes and 600 proxy videos. It includes coarse 3D, semantic proxy, and colored-OBB representations, with first-person and third-person perspectives and a multi-view subset.

### 5. How is it evaluated?

It reports entity control with bounding-box IoU and center error, camera control, video quality, temporal/text metrics, Logic-Render Alignment, Interaction Success Rate, IoU-weighted versions of the logic metrics, long-horizon reappearance IoU and state persistence, and multi-view appearance consistency.

### 6. What are the main results?

Proxy-conditioned models tend to beat camera-conditioned world models on entity trajectories and event timelines. In the main track, LynnReal-Omni and MiniMax-H3 are strong on entity control and logic alignment. In the long-horizon setting, all methods remain weak: 30-second BBox IoU is only 0.175 to 0.280 and reappearance IoU is only 0.053 to 0.131. In multi-view generation, methods whose inputs explicitly distinguish participants reach about 82-94% appearance compliance and 81-90% cross-view consistency on judgeable observations, while C2R has much worse identity compliance despite a lower MEt3R point estimate.

### 7. What is actually novel?

The novelty is not a new video generator. It is the replayable program-state record plus metrics that connect generated pixels back to explicit events and entity states.

### 8. What are the strengths?

The benchmark tests whether structure is rendered, not merely whether a video looks good. It separates entity placement from event success, short-horizon control from long-horizon memory, and single-view quality from multi-view consistency.

### 9. What are the weaknesses, limitations, or red flags?

Some metrics rely on VLM judges and detectors, so the benchmark inherits judge reliability issues. MiniMax-H3 influenced curation for the Unverified-FF setting, so results involving it need that caveat. The benchmark is still programmatically generated, so real-world visual and interaction complexity is not fully represented.

### 10. What challenges or open problems remain?

The key open problem is renderer accountability over longer horizons and multi-agent/multi-view worlds. The paper shows that current models still forget returning entities and can render plausible but wrong interactions.

### 11. What future work naturally follows?

Extend the executable-record idea to richer physics, object affordances, deformable or articulated bodies, embodied tasks, and agent-world feedback loops where decisions depend on rendered state fidelity.

### 12. Why does this matter for cabbageland?

Cabbageland cares about explicit state that actually constrains downstream generation and action. ROWBench gives a concrete evaluation pattern: when a state machine says an event happened, the pixels must prove it.

### 13. What ideas are steal-worthy?

Keep a replayable event log. Evaluate rendered consequences, not just prompts. Weight interaction success by entity placement. Test long-horizon reappearance explicitly after objects leave the field of view.

### 14. Final decision

Preserve. This is a clean benchmark for a failure mode that will matter for any programmable or interactive world model.
