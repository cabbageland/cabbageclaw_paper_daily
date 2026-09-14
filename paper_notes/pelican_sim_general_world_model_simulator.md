# Pelican-Sim 1.0: A General World Model Simulator for Embodied Intelligence

## Basic info

* Title: Pelican-Sim 1.0: A General World Model Simulator for Embodied Intelligence
* Authors: Shilong Zou, Shilin Zhang, Yingji Zhang, Yuhang Huang, Yi Zhang, Zeyuan Ding, Han Dong, Junwei Liao, Yong Dai, Jian Tang, Xiaozhu Ju
* Year: 2026
* Venue / source: arXiv:2609.12036
* Link: https://arxiv.org/abs/2609.12036
* Date surfaced: 2026-09-14
* Why selected in one sentence: It is a robot world-model simulator report with a concrete dual action representation and downstream policy evaluations, not just video metrics.

## Quick verdict

* Highly relevant

This is the one robotics paper in the digest because it earns the world-model label better than most VLA reports. The dual action representation is the main transferable mechanism: keep precise numerical joint state and also render action as camera-aligned image-space motion. The downstream results are broad, though still bounded by simulator-heavy evaluation and a VLM evaluator that deserves independent scrutiny.

## One-paragraph overview

Pelican-Sim 1.0 is an action-conditioned latent video model built on a Cosmos-Predict-style Video DiT. Given the first RGB observation, optional task instruction, and a frame-aligned robot action trajectory, it predicts future visual observations. It conditions on actions in two complementary ways: a fixed 28-dimensional bilateral joint/action vector and a URDF-rendered skeleton action video projected into the paired camera. Sparse MoE layers support heterogeneous dynamics, and causal few-step distillation accelerates rollout generation. The paper evaluates video prediction quality and downstream uses: generated data for policy learning, policy evaluation/ranking, test-time action selection, policy improvement, and distribution-shift robustness.

## Model definition

### Inputs

Inputs include an initial RGB frame, an optional task instruction, robot URDF and camera calibration metadata, and a frame-aligned trajectory of robot configurations encoded into a 28-dimensional action layout. The same trajectory is also rendered as a synchronized action video using URDF forward kinematics and camera projection.

### Outputs

The model outputs predicted future RGB observations as a video rollout. Downstream, a fine-tuned VLM evaluator turns generated videos into terminal-success, progress, and visual-validity scores for policy evaluation, action selection, and policy improvement.

### Training objective (loss)

The world model uses a target-only flow-matching objective in latent video space. The clean conditioning frame remains fixed; target future latents are noised along a linear path, and the model predicts the velocity from noised target latents toward clean future latents. The VLM evaluator is separately adapted with LoRA and heads for success, progress, and visual validity.

### Architecture / parameterization

The base is a 28-layer latent Video DiT derived from Cosmos-Predict 2.5. Action values modulate odd-indexed blocks, action-video features enter even-indexed blocks through auxiliary context blocks, and sparse MoE layers combine shared and routed experts. The action vector packs left and right sides into 14 dimensions each: arm joints, gripper opening, and hand joints, with zero-filled missing slots.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Robot policies need cheap, controllable future prediction for data generation, policy evaluation, action selection, and policy improvement across heterogeneous embodiments. A world model must understand both numeric robot control and what that control means in the camera view.

### 2. What is the method?

Train an action-conditioned latent video model with dual action conditioning: a 28D unified action value and a URDF-rendered action video. Use sparse MoE for heterogeneous dynamics and distill the model into a four-step causal rollout generator. Pair generated videos with a VLM evaluator for downstream policy uses.

### 3. What is the method motivation?

Numeric joint actions preserve exact configuration but hide image-space motion. Rendered action videos expose whole-arm geometry, viewpoint, and gripper state but can lose precise configuration detail. Using both gives the simulator a better state-action carrier.

### 4. What data does it use?

Training combines real-world demonstrations from AgiBotWorld Beta, RealSource World, and RoboMIND with simulated trajectories from LIBERO, ManiSkill2, RoboTwin, and RoboCasa. After curation, the corpus contains about 1.0 million trajectories and roughly 8,000 hours of robot interaction data.

### 5. How is it evaluated?

The paper evaluates held-out video generation on AgiBotWorld Beta, RoboMIND, and RoboTwin using PSNR, SSIM, LPIPS, FID, FVD, and adapted EWMBench metrics. It also tests generated data for policy learning, policy evaluation/ranking against RoboTwin outcomes, VLM-guided action selection, and policy improvement through generated rollouts.

### 6. What are the main results?

Pelican-Sim beats evaluated baselines on all five main video-quality metrics across the three held-out splits. PSNR improves over the strongest baseline by 4.636 dB on AgiBotWorld Beta, 2.080 dB on RoboMIND, and 10.343 dB on RoboTwin. In limited-demo policy learning, adding 500 generated trajectories to 50 originals raises success from 70% to 93%. Policy evaluation reaches Pearson correlation 0.994 and 2.4 percentage-point MAE with 1,000 adaptation rollouts. For test-time action selection, Pelican-Sim plus the VLM evaluator reaches 63.8% success versus 43.2% for a single sample and 52.3% for Ctrl-World selection.

### 7. What is actually novel?

The dual action carrier is the most novel and useful part: a fixed cross-embodiment action vector plus rendered action-video conditioning from URDF and camera calibration. The breadth of downstream evaluation also raises the bar over pure video-metric world-model reports.

### 8. What are the strengths?

The action representation is concrete. The data curation is serious enough to matter. The downstream experiments test utility rather than only visual similarity. Ablations support the interleaved action-injection design and the combination of action video, action value, and sparse MoE.

### 9. What are the weaknesses, limitations, or red flags?

The downstream evidence leans heavily on RoboTwin-style simulated tasks and generated-video evaluation by a fine-tuned VLM. Some metrics remain mixed: certain adapted EWMBench submetrics are below the best baseline. The model may learn dataset-specific embodiment and camera priors despite the unified representation. Real closed-loop deployment is still not proved.

### 10. What challenges or open problems remain?

Generalization to genuinely unseen robots, cameras, task distributions, and real closed-loop policy execution remains the central test. Another challenge is separating world-model prediction error from VLM-evaluator bias in policy selection and improvement.

### 11. What future work naturally follows?

Run held-out real-robot evaluations, add uncertainty or abstention to world-model rollouts, test cross-embodiment zero-shot transfer, and audit whether the action-video branch carries real causal action information or mostly dataset priors.

### 12. Why does this matter for cabbageland?

It is a useful blueprint for action-conditioned world models: make the action state explicit, render what can be rendered, and prove downstream utility. The dual carrier idea generalizes beyond robotics.

### 13. What ideas are steal-worthy?

Represent actions twice: once in control space, once in observation space. Use URDF/camera metadata to create an explicit action video. Evaluate simulators by whether they improve policies, ranking, and action selection, not only by FVD.

### 14. Final decision

Preserve, with caution. The mechanism is strong and the evaluation is broad, but the claimed generality still needs harder real-world proof.
