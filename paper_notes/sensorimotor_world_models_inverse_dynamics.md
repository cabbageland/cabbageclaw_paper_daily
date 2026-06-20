# Sensorimotor World Models: Perception for Action via Inverse Dynamics

## Basic info

* Title: Sensorimotor World Models: Perception for Action via Inverse Dynamics
* Authors: Petr Ivashkov, Randall Balestriero, Bernhard Schoelkopf
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.20104
* Date surfaced: 2026-06-20
* Why selected in one sentence: It gives latent world models a simple action-recoverability constraint that prevents collapse while biasing representations toward controllable state.

## Quick verdict

* Highly relevant

This is a strong latent world-model paper. I inspected the full arXiv PDF, including the method, toy controllability analysis, planning experiments, physical-state probes, geometry visualizations, and limitations. The mechanism is simple enough to steal: if the latent before/after pair cannot recover the action, the representation probably has not earned the name sensorimotor state.

## One-paragraph overview

The paper trains a JEPA-style latent world model from offline pixel-action transitions using a forward latent prediction loss plus one inverse-dynamics regularizer. The encoder maps observations into embeddings, the forward model predicts the next embedding from the current embedding and action, and the inverse head predicts the action from the current and next embeddings. The inverse loss prevents the trivial constant-embedding solution and pushes the representation toward controllable degrees of freedom, while ignoring visual variation that is not action-linked. In toy worlds this recovers the right effective latent dimension and filters random distractors; in four control tasks it supports latent MPC planning that matches or beats a SIGReg baseline.

## Model definition

### Inputs
Inputs are offline transitions `(o_t, a_t, o_{t+1})` from video frames or image observations with continuous actions. The setup does not require rewards, task labels, or knowledge of the behavior policy. Planning later uses a current observation, a goal observation, and candidate action sequences.

### Outputs
The encoder outputs latent embeddings `z_t` and `z_{t+1}`. The forward dynamics model outputs a predicted next embedding. The inverse dynamics head outputs a predicted action. During planning, the learned forward model scores candidate action sequences by terminal distance between predicted latent state and goal latent state.

### Training objective (loss)
The joint objective is a forward mean-squared error between predicted next latent and encoded next latent plus `lambda` times an inverse mean-squared error between predicted and true action. The inverse loss backpropagates into the encoder and is the sole anti-collapse regularizer.

### Architecture / parameterization
The main architecture is an encoder, a latent forward model, and a small inverse MLP over concatenated latent pairs. In the control experiments the encoder follows the LeWM setup with a ViT-Tiny encoder projected to a 192-dimensional latent, a small transformer forward model with action conditioning, and a two-layer width-256 inverse model. Planning uses latent MPC with CEM over action sequences.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
JEPA-style latent world models trained end-to-end from pixels can collapse because the encoder and forward predictor can minimize latent prediction loss with constant embeddings. More broadly, pixel-preserving representations may keep visually salient but action-irrelevant details while missing the controllable structure needed for planning.

### 2. What is the method?
SMWM adds a single-step inverse dynamics head to a latent forward model. Given consecutive embeddings, the inverse head predicts the action that caused the transition. A collapsed representation cannot support action recovery, so the inverse objective makes collapse costly and encourages the encoder to preserve action-relevant state.

### 3. What is the method motivation?
The paper's motivation is "perception for action": useful state should be shaped by the actions an agent can take and the sensory changes those actions cause. Inverse dynamics gives that idea a concrete training signal without imposing a distributional prior on the latent space.

### 4. What data does it use?
The method uses offline, reward-free trajectory data with frames and continuous actions. Experiments include controlled 2D dot and triangular-sprite environments plus TwoRoom, Reacher, Push-T, and OGBench-Cube planning tasks.

### 5. How is it evaluated?
The paper evaluates latent dimension and geometry in toy settings, tests whether uncontrollable distractors are filtered, visualizes decoded control-relevant pose variables, performs goal-conditioned latent MPC planning, and probes frozen embeddings for physical state variables with linear and MLP probes.

### 6. What are the main results?
In toy dot settings, the number of significant principal components matches the controllable dimension and ignores random distractors. In planning, SMWM reaches 99 percent success on TwoRoom, 66 percent on Reacher, 83 percent on Push-T, and 84 percent on OGBench-Cube under the reported 50-step budget and 25-step goal offset. It roughly matches SIGReg on the 2D tasks and outperforms it on OGBench-Cube, where SIGReg reports 59 percent. Physical-state probes recover most ground-truth quantities well under regularized models, with SMWM especially strong on Cube quantities.

### 7. What is actually novel?
Inverse dynamics for representation learning is not new. The useful novelty is using it as the standalone anti-collapse mechanism for a JEPA-style latent world model and showing that this pressure recovers compact, controllable latent geometry without a Gaussian-matching prior, frozen encoder, EMA target, or reconstruction decoder.

### 8. What are the strengths?
The mechanism is clean and cheap. It targets controllability rather than visual fidelity. The toy analyses are unusually legible: when an uncontrollable dot moves randomly, the encoder drops it because it is neither action-recoverable nor forward-predictable. The planning comparisons also keep the architecture close to the SIGReg baseline, making the regularizer comparison meaningful.

### 9. What are the weaknesses, limitations, or red flags?
The method assumes the action is recoverable from consecutive observations. That fails when distinct actions produce identical visible changes or when necessary state, such as velocity, is not identifiable from a single frame. A behavior policy with action-correlated but uncontrollable distractors could also fool the representation. The experiments are moderate-scale simulated control, not long-horizon open-world robotics or real deployment.

### 10. What challenges or open problems remain?
Open problems include multi-frame encoders, multi-step inverse objectives, biased behavior-policy confounds, long-horizon rollout error, partial observability, and settings where downstream tasks require information that was not action-relevant in the training data.

### 11. What future work naturally follows?
The obvious follow-up is to combine inverse dynamics with history-based state, test on harder partially observed environments, and use the inverse model inside planners rather than only as a regularizer. Another useful direction is to audit whether learned latents stay action-sufficient under dataset shifts where distractors become action-correlated.

### 12. Why does this matter for cabbageland?
Cabbageland cares about world models where latent state actually carries structure. This paper gives a compact test: can the before/after latent pair recover the intervention? If not, the state may be predictive mush rather than a controllable world representation.

### 13. What ideas are steal-worthy?
Use inverse dynamics as a state-validity pressure. Prefer action-sufficient latents over visually exhaustive latents. Measure effective latent dimension against controllable degrees of freedom. Add distractors that vary visually but are not controlled by action, and check whether the model wastes state on them.

### 14. Final decision
Keep as a strong latent world-model reference. It is not a giant system paper, but the mechanism is clean, inspectable, and directly useful for designing better representation tests.
