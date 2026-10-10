# What 30,000 Hours of Ego-centric Video Does Not Teach

## Basic info

* Title: What 30,000 Hours of Ego-centric Video Does Not Teach
* Authors: Jiahua Dong, Anurag Bagchi, Yash Jangir, Muhammad Zubair Irshad, Sergey Zakharov, Martial Hebert, Homanga Bharadhwaj, Yu-Xiong Wang, Vitor Campagnolo Guizilini, Pavel Tokmakov
* Year: 2026
* Venue / source: arXiv preprint
* Link: https://arxiv.org/abs/2610.12464
* Date surfaced: 2026-10-10
* Why selected in one sentence: It gives a direct scaling study showing that ego-centric video teaches world models agent appearance much more readily than object interaction dynamics.

## Quick verdict

* Must read

This is a sharp world-model evaluation paper, not because it has the flashiest method, but because it measures the exact gap that planning and simulation care about. Scaling 30,000 hours of ego-centric video helps, but the paper separates the agent from the agent's effect on objects and shows the latter saturating much lower. The dynamic-region supervision is a partial fix; the deeper contribution is the evidence that pixels and scale alone do not buy contact-faithful world models.

## One-paragraph overview

The paper trains Cosmos 3 video world models on nested ego-centric human-manipulation datasets from 300 to 30,000 hours, then evaluates generated rollouts with separate structural consistency scores for the agent's hands/body and the manipulated objects. Plain scaling improves both, but skeleton conditioning quickly saturates agent fidelity and exposes a lower object-interaction ceiling. The authors then add object-centric adaptive noise scheduling and loss reweighting over dynamic regions near interactions, which improves object fidelity more than previous interaction-focused auxiliary objectives but still leaves a large gap. A humanoid transfer experiment shows the same pattern: agent fidelity improves more than object consequence fidelity.

## Model definition

### Inputs

The world model receives an initial RGB observation and an action or motion conditioning sequence. Some variants additionally receive a projected skeleton sequence aligned to the video-token grid. For humanoid transfer, the model receives a start frame and a 138-dimensional humanoid state trajectory.

### Outputs

The model predicts the following 16 video frames, producing a 17-frame window including the observed first frame. The evaluation extracts generated hand/agent masks and manipulated-object masks to compute structural consistency.

### Training objective (loss)

The base model is a diffusion or flow-style video generation model trained to predict denoising targets over video latents. The proposed object-centric supervision modifies the training target in dynamic regions by raising the effective noise level while preserving the same clean latent target, and optionally reweights the loss inside the same dynamic regions. The paper also reimplements prior PhysisForcing-style auxiliary objectives and finds they do not improve this ego-centric setting.

### Architecture / parameterization

The experiments use Cosmos 3 video world models at multiple sizes. Skeleton conditioning projects 3D body configuration into image coordinates and adds learned skeleton tokens to corresponding video embeddings. Dynamic-region supervision uses D4RT point tracks, 3D displacement, reliability, and a soft hand-proximity prior to localize likely interaction regions.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It asks whether scaling ego-centric human video is enough to learn world models that faithfully predict both the agent and the objects the agent changes.

### 2. What is the method?

The paper first performs a controlled scaling study over nested 300 to 30,000 hour datasets. It then adds skeleton conditioning to saturate agent fidelity cheaply, so object fidelity can be measured without being confounded by better agent prediction. Finally, it proposes dynamic-region supervision that shifts denoising pressure toward manipulated objects and contact-adjacent regions.

### 3. What is the method motivation?

Pixel-level video losses spend most capacity on visible, predictable, high-area content. The parts most relevant for interaction, such as occluded contacts, object deformation, friction, stiffness, and hidden geometry, can be underweighted or unobservable. The authors want to test whether scale alone overcomes this or whether the objective has to change.

### 4. What data does it use?

The training corpus contains 30,000 hours of ego-centric human manipulation, spanning roughly 32,000 tasks, 116 environment types, and 14,000 contributors. Evaluation uses an out-of-distribution benchmark with different capture hardware, sites, and participants, with 17-frame windows and 11,328 instance masks. The humanoid transfer experiment uses 11 simulated bimanual tasks and evaluates on EgoVLA policy rollouts.

### 5. How is it evaluated?

The central metric is Structural Consistency Score, computed separately for hands/agent and manipulated objects using segmentation and tracking. LPIPS is used as a perceptual control. Humanoid transfer also reports success-agreement with simulator verdicts on critical windows.

### 6. What are the main results?

For the standard scaling run, agent fidelity gains 0.12 SCS from 300 to 3,000 hours and only 0.06 from 3,000 to 30,000 hours, with a fitted asymptote of 0.811. Skeleton conditioning lets a 300-hour Nano model reach the agent fidelity that the baseline reaches around 15,000 hours, and the skeleton and baseline curves converge to about 0.800 to 0.811. With the agent saturated, object fidelity improves only 0.09 SCS over two orders of magnitude and fits a ceiling of 0.565, with 93% already realized at 30,000 hours. Dynamic-region supervision improves object SCS at 30,000 hours from 0.527 to 0.546. In humanoid transfer, Ours reaches hand SCS 0.88, object SCS 0.79, and success agreement 0.81, but object SCS still drops faster over the rollout horizon.

### 7. What is actually novel?

The novelty is the controlled decomposition of world-model scaling into agent fidelity and object-interaction fidelity, plus the use of skeleton conditioning as an instrument to expose the object ceiling. The dynamic-region objective is useful, but the measurement design is the most important contribution.

### 8. What are the strengths?

The paper measures the right thing instead of hiding behind visual quality. It separates perception of the agent from consequences in the world, uses out-of-distribution evaluation, includes perceptual controls, and tests whether previously proposed interaction objectives transfer. The finding is actionable: supervision must be shifted toward dynamic, contact-relevant regions.

### 9. What are the weaknesses, limitations, or red flags?

The proposed dynamic-region supervision only raises the ceiling modestly. The method still relies on RGB video where key physical variables are hidden or occluded. The analysis is anchored to Cosmos 3 and this particular ego-centric corpus, so the exact ceiling may not transfer to every architecture or data mix. SCS also depends on segmentation and tracking, though the authors estimate metric ceilings to show the observed gap is below tracker limits.

### 10. What challenges or open problems remain?

The hard problem is learning object response when mass, friction, stiffness, hidden geometry, and forces are not directly visible. Future systems likely need better object state, explicit contact supervision, multimodal sensing, simulator-derived labels, or architectures that represent persistent hidden state rather than relying on video pixels alone.

### 11. What future work naturally follows?

Combine ego-centric video with explicit physical state, depth, tactile/contact information, object-centric latents, or simulation supervision. Test whether latent-predictive objectives or geometry-aware world models improve object SCS more than dynamic noise. Extend the evaluation to longer horizons and more deformable or occluded objects.

### 12. Why does this matter for cabbageland?

Cabbageland cares about world models as instruments for planning and counterfactual action evaluation. This paper shows that visual plausibility of the acting body is not enough: a planning-useful world model must predict what the action does to the world.

### 13. What ideas are steal-worthy?

Report agent fidelity and object-effect fidelity separately. Use conditioning to saturate an easy axis, then measure the remaining bottleneck. Shift supervision toward dynamic regions, but treat that as a partial patch, not a solution. Build world-model evaluations around consequences, not just appearance.

### 14. Final decision

Preserve. This is the most useful paper of the day because it cuts through the scaling story and names the missing state.
