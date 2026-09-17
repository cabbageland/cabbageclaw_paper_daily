# PointZero: 3D Point Track Completion for Learning Transferable 3D Dynamics

## Basic info

* Title: PointZero: 3D Point Track Completion for Learning Transferable 3D Dynamics
* Authors: Bardienus P. Duisterhof, Kaifeng Zhang, Adam Hung, Bowen Wen, Stan Birchfield, Yunzhu Li, Deva Ramanan, Jeffrey Ichnowski
* Year: 2026
* Venue / source: arXiv:2609.19142
* Link: https://arxiv.org/abs/2609.19142
* Date surfaced: 2026-09-17
* Why selected in one sentence: It proposes dense 3D point-track completion as a robot-free dynamics pretraining objective, then shows transfer to action-conditioned dynamics and manipulation policies.

## Quick verdict

* Must read

This is the strongest cabbageland paper in the batch. The contribution is not just another robot world model; it isolates a transferable state variable, dense future 3D point tracks, and tests whether it improves downstream dynamics and imitation learning. This note is based on the full arXiv PDF text.

## One-paragraph overview

PointZero trains a diffusion transformer to predict dense future 3D trajectories for all observed points from a single RGB-D frame, sparse partial point tracks, and visual features. The pretraining data is a 2.9 million-frame synthetic dataset spanning deformable, articulated, and rigid objects, with randomized interactions. The trained model can be post-trained to condition on robot end-effector poses for scene-specific 3D dynamics, or to predict robot actions for imitation learning. The paper argues that 3D point-track completion is a scalable bridge between robot-free dynamics data and downstream embodied control.

## Model definition

### Inputs

The pretraining model receives an observed point cloud from one RGB-D frame, sparse partial 3D point trajectories over a 10-frame horizon, and DINOv2 visual tokens compressed through a Perceiver-IO module.

### Outputs

The model predicts dense future 3D tracks for all observed points. In downstream variants, it predicts robot-conditioned 3D dynamics or robot action chunks plus auxiliary point tracks.

### Training objective (loss)

The paper compares direct trajectory regression, flow matching velocity prediction, and a JiT-style x-prediction objective in point-trajectory space. The flow-matching objective samples Gaussian source point trajectories, linearly interpolates to target tracks, and trains the model to predict velocity. The JiT-style objective predicts the clean trajectory and supervises the implied velocity.

### Architecture / parameterization

PointZero is a diffusion transformer with point tokens, partial-track/action tokens, and visual tokens. Query tokens represent noisy future point trajectories plus initial positions. Cross-attention keys and values concatenate embedded observed points, action or track tokens, and compressed visual features. The base model uses a ViT-Base-sized transformer with 768-token dimension, 12 heads, and 12 layers.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

3D dynamics models are useful for planning and manipulation, but robot-action-conditioned dynamics data is expensive and narrow. Existing scene-specific models often need many interactions with the target scene. PointZero asks whether a generic 3D dynamics prior can be learned without robot action labels by completing partial 3D point tracks.

### 2. What is the method?

The method pretrains a transformer on 3D point-track completion. Given one RGB-D observation and sparse partial tracks, the model predicts dense future point trajectories for all observed points. For robot-conditioned dynamics, action tokens are replaced with end-effector pose tokens and the pretrained model is fine-tuned. For imitation learning, the model is post-trained to predict actions and optionally auxiliary point tracks.

### 3. What is the method motivation?

Point tracks are a useful middle representation. They are metric, object-agnostic, and can describe rigid, articulated, and deformable motion. Unlike robot actions, they can in principle be extracted from ordinary video. Unlike pixel video, they expose a 3D state variable that downstream control can use.

### 4. What data does it use?

The main pretraining data is a synthetic dataset of 2.9 million image frames with dense per-point trajectories over deformable cloth-like objects, articulated PartNet-Mobility objects, and rigid-body interactions. The paper also collects a real-world zero-shot evaluation set with 14 objects and 124 interactions. Downstream evaluations use PGND dynamics tasks plus simulated and real robot manipulation tasks from the 3PoinTr protocol.

### 5. How is it evaluated?

Evaluation covers held-out synthetic point-track completion, zero-shot real-world point-track completion, scene-specific robot-conditioned dynamics on the PGND benchmark, zero-shot PGND dynamics, and imitation learning on three simulation tasks plus four real-world manipulation tasks. Metrics include MDE, MSE, Chamfer Distance, Earth Mover's Distance, and task success.

### 6. What are the main results?

On the held-out synthetic dataset, every PointZero variant outperforms all adapted baselines on every metric and object category. On the real-world zero-shot dataset, PointZero-FM and PointZero-JiT outperform all baselines on 11 of 12 metrics. On PGND scene-specific dynamics, PointZero-FT beats PGND on 4/6 scenes and shows pretraining is critical compared with scratch training. For manipulation, PointZero has the highest or tied-highest success on 6/7 tasks. With 20 demos and auxiliary track supervision, pretraining improves average simulated success from 80.5% to 88.2%.

### 7. What is actually novel?

The novelty is the objective and representation choice: use 3D point-track completion as a scalable dynamics pretraining task, then post-train the same carrier for robot-conditioned dynamics and policies. The model architecture is less novel than the decision to make dense 3D tracks the transferable state.

### 8. What are the strengths?

The paper evaluates the representation across multiple transfer modes rather than only a native benchmark. The synthetic-to-real zero-shot test is a useful sanity check. The ablations separate architecture from pretraining and show that the pretrained prior matters. The output is explicit enough to inspect and measure in physical units.

### 9. What are the weaknesses, limitations, or red flags?

The pretraining set is still synthetic and does not cover broad real-world clutter, hand-object interaction, full material diversity, or long horizons. Robot transfer remains evaluated on relatively contained manipulation tasks. Several generative metrics use best-of-10 oracle reporting, which is useful for multimodal prediction but optimistic for deployment.

### 10. What challenges or open problems remain?

The obvious next challenge is extracting reliable 3D tracks from in-the-wild videos and using them for real pretraining. Another challenge is richer conditioning: contact locations, force cues, tool state, and object identity could matter more than sparse tracks alone. Long-horizon rollout stability remains open.

### 11. What future work naturally follows?

Train the same objective on pseudo-labeled real video. Add contact and force carriers. Evaluate planning with the predicted tracks directly rather than only post-training for policies. Test whether point-track uncertainty improves downstream decision-making.

### 12. Why does this matter for cabbageland?

Cabbageland cares about world models with explicit state that actually supports control. PointZero is a clean example: it chooses a state carrier, trains it at scale, and tests whether it improves later dynamics and action prediction.

### 13. What ideas are steal-worthy?

Use sparse observed interventions to supervise dense future state. Make the representation metric and object-agnostic. Test a world-model pretraining objective by freezing or post-training it into different downstream interfaces. Prefer physical-unit errors over only video scores.

### 14. Final decision

Preserve. This is a direct, mechanism-rich world-model paper and the most relevant paper today.
