# World Models' Last Exam in Physics

## Basic info

* Title: World Models' Last Exam in Physics
* Authors: Mingju Gao, Qingle Liu, Yuzhao Peng, Xinjie Lin, Ziming Qin, Zheng Jiang, Wenyi Li, Calvin Xiao, Youjie Zheng, Kaisen Yang, Qinhuai Na
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2610.08791
* Date surfaced: 2026-10-07
* Why selected in one sentence: It evaluates video world models with explicit physical measurements instead of trusting visual plausibility or VLM judgment.

## Quick verdict

* Must read

This is the strongest paper in today's batch because it turns physical consistency into measured evidence. The benchmark still depends on visibility, task design, and extraction tools, but it cleanly separates "the video is observable" from "the physics is right." That distinction is exactly what video world-model evaluation needs.

## One-paragraph overview

The paper introduces a 40-task benchmark for image-to-video models used as world models. Tasks span mechanics, optics, hydrostatics, phase changes, electromagnetism, granular media, surface tension, and viscous flow. Each task pairs a generated first frame with a prompt, then scores the resulting video through a two-stage evaluator: a VLM screens temporal consistency and observability, while task-specific tools measure quantities such as trajectories, periods, angles, liquid levels, and event timing. Across eight video generation models and 1,280 generated videos, the best model reaches only 57.76 out of 100, exposing a large gap between plausible motion and quantitatively correct physical behavior.

## Model definition

### Inputs

The benchmark evaluator receives a generated video, the task's first frame and prompt, and the task's predefined physical assumptions and measurement criteria. The evaluated video models receive task-specific image prompts, generated first frames, and video prompts.

### Outputs

The evaluator outputs a temporal consistency / observability score, task-specific physical measurements, a physical score, and a gated composite score. The generation models output videos; the benchmark does not train a new world model.

### Training objective (loss)

There is no training loss for a new model in this paper. The scoring rule combines a VLM consistency gate with programmatic physical measurements. If the consistency score is below 80, the physical score is retained diagnostically but does not contribute to the composite score.

### Architecture / parameterization

The evaluator uses Qwen3.6-27B for temporal consistency and observability screening, plus task-specific measurement pipelines using tracking, segmentation, geometric fitting, photometry, and temporal analysis. CoTracker3 and SAM 2 are used as building blocks for extracting measurable evidence.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It targets the evaluation gap for video world models. A model can produce a coherent-looking video while violating the physical relationship that would matter for prediction, planning, or simulation.

### 2. What is the method?

Build controlled physical tasks with observable, scale-canceling criteria; generate videos from a shared first-frame and prompt protocol; screen whether the video is measurable; then compute explicit physical residuals from extracted quantities.

### 3. What is the method motivation?

Reference videos and VLM judgments do not isolate physical law violations. A measurement-based benchmark can say which relationship failed and whether the necessary evidence was even visible.

### 4. What data does it use?

The benchmark contains 40 controlled tasks across nine physical families. The authors generate first frames with GPT-Image-2.5, evaluate eight image-to-video models, and collect four samples per task-model pair, totaling 1,280 generated videos. They also render 480 synthetic reference videos to validate the measurement module.

### 5. How is it evaluated?

The paper reports composite scores over task families and difficulty levels, validates measurement on synthetic videos with known relationships, and compares the evaluator against human judgments and a direct VLM scoring baseline on 320 videos.

### 6. What are the main results?

The best model averages 57.76 out of 100. Some tasks are nearly solved, but others fail badly: a stone-in-liquid buoyancy task has an all-model mean of 3.45, and all eight models receive zero physical scores under the protocol. Synthetic reference videos score 97.53 on average when the consistency gate is bypassed. Against human judgments, the evaluator gets 51.58% within-task ranking agreement versus 43.40% for direct VLM scoring, and 53.12% confirmed pairwise agreement versus 45.62% for direct VLM scoring.

### 7. What is actually novel?

The novelty is not another broad video benchmark. It is the measurement contract: each task specifies what observable relationship is being tested, what evidence must be extracted, and how a physical residual maps to a score.

### 8. What are the strengths?

The task catalog is broad, the scores are interpretable, and the evaluator preserves intermediate measurements for debugging. The paper refuses to treat temporal coherence as physical correctness. The synthetic-video validation is a useful sanity check that the measurement code can score correct relationships when the visual evidence is present.

### 9. What are the weaknesses, limitations, or red flags?

The benchmark is constrained by observability and extraction reliability. A low score can mean the model failed physics, failed to instantiate the scene, or made measurement impossible. The VLM consistency gate can still shape what counts as scorable evidence, even though physical correctness is measured separately.

### 10. What challenges or open problems remain?

The next challenge is making measurement robust in messier, less controlled scenes and connecting these metrics to downstream planning failures. Another open problem is turning measured physical residuals into training or post-training signals without overfitting to benchmark-specific scenes.

### 11. What future work naturally follows?

Add more contact-rich manipulation, multi-object causality, material parameters, and action-conditioned tasks. Use the measurement residuals as rewards or diagnostics during video-world-model post-training, then test whether improvements transfer to planning.

### 12. Why does this matter for cabbageland?

Cabbageland cares about world models whose state can support action. This benchmark asks the right question: not "does the video look plausible?" but "does it preserve the measured relationship the downstream system would rely on?"

### 13. What ideas are steal-worthy?

Separate observability from correctness. Score physical claims through explicit extracted variables, not generic visual quality. Retain intermediate measurements so failures can be audited instead of collapsed into one benchmark number.

### 14. Final decision

Preserve. This is a direct hit for world-model evaluation, physical consistency, and measurable state.

