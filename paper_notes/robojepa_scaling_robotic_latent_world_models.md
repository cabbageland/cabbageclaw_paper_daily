# RoboJEPA: Scaling Robotic Latent World Models

## Basic info

* Title: RoboJEPA: Scaling Robotic Latent World Models
* Authors: Artem Zholus, Nicolas Beltran-Velez, Jianhao Yuan, Sarath Chandar, Tushar Nagarajan, Daniel Severo, Koustuv Sinha, Michal Drozdzal, Adriana Romero Soriano, Jeannette Bohg, Nicolas Ballas, Mahmoud Assran
* Year: 2026
* Venue / source: arXiv preprint
* Link: https://arxiv.org/abs/2610.10515
* Date surfaced: 2026-10-08
* Why selected in one sentence: It gives robotic latent world models a concrete scaling-law and planning-evaluation story instead of just showing larger rollouts.

## Quick verdict

* Must read

This is one of the stronger world-model papers in the batch because it treats scale as something to measure and extrapolate. The paper is still bounded by a frozen representation encoder, fixed available interaction data, and image-goal CEM planning without a learned proposal policy. But the core contribution is real: offline latent imagination error follows a fitted compute law and correlates with downstream robot planning behavior.

## One-paragraph overview

RoboJEPA is a family of action-conditioned JEPA-style latent world models trained on a large multi-embodiment manipulation corpus. A frozen V-JEPA 2.1 encoder turns multi-view robot video into latent tokens, and a transformer predictor learns to predict future latent embeddings from past visual tokens, actions, proprioceptive states, robot id, and camera-view conditioning. The authors scale the predictor from 22M to 8B parameters and train on 23 public manipulation datasets spanning 12 embodiments, 26 action spaces, 15,022 video hours, and 6,692 action-synchronized hours. Their main claim is that nine-step latent imagination L1 error follows a second-order power law in training compute on both DROID and RoboCasa holdouts, and that this error is a useful proxy for downstream planning performance in simulation and on a real Franka robot.

## Model definition

### Inputs

RoboJEPA receives a history of latent visual features from a frozen V-JEPA 2.1 encoder, past and future actions for rollout, proprioceptive states, a robot-id embedding, and per-view camera conditioning. The training data includes multi-view frames when available and heterogeneous robot action spaces unified by robot-specific action/state encoders.

### Outputs

The predictor emits next-frame latent visual tokens in the frozen encoder feature space. During planning, it autoregressively rolls out latent futures under candidate action sequences and compares the final predicted latent state to a goal-image latent.

### Training objective (loss)

The objective is the average of two per-token L1 losses in latent space: a teacher-forced next-embedding prediction loss and an autoregressive rollout loss that predicts missing future embeddings from a shorter prefix. The rollout loss is meant to reduce exposure bias and error accumulation.

### Architecture / parameterization

The world model is a deterministic transformer predictor over a flat interleaved sequence of visual tokens, action tokens, and state tokens. It uses ViT-style residual blocks with pre-normalization, RoPE, RMSNorm, GELU feed-forward blocks, QK-normalization, a timestep-causal attention mask, local temporal attention over up to eight prior steps, factorized multi-axis RoPE for time, height, width, and view, and learnable view bias. Parameter counts range from 22M to 8B.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It asks whether robotic latent world models scale predictably with compute, and whether offline latent prediction error can forecast downstream planning capability before expensive real-robot evaluation.

### 2. What is the method?

Train a large family of action-conditioned latent JEPA predictors on a unified robot-data mixture, fit scaling laws to held-out latent imagination error as a function of training compute, and evaluate whether larger/lower-error models plan better toward image goals in RoboCasa and on a real Franka robot.

### 3. What is the method motivation?

Robotics data and robot evaluation are expensive. If a world model's latent rollout error obeys a predictable compute law and correlates with planning success, researchers can make scale/data decisions without treating every training run and deployment as a gamble.

### 4. What data does it use?

The training mixture contains 23 public manipulation datasets, summarized into groups including DROID, RoboSet, RoboMind, LeRobot, RoboCasa365, 1X, AgiBot World, and nine Open-X Embodiment datasets. The compiled set has 2.8713M episodes, 15,022 video hours, 6,692 action hours, 12 platforms, and 26 robot/action ids.

### 5. How is it evaluated?

Offline evaluation measures per-token L1 latent rollout error over nine future steps on unseen DROID and RoboCasa scenes. Online evaluation uses image-goal planning with CEM, in simulation on RoboCasa tasks and on a real DROID-style Franka setup for Grasp, Object Lift, and Pick and Place. The scaling-law fit trains on smaller models up to 2B and tests extrapolation to 4B and 8B.

### 6. What are the main results?

The second-order power law fits held-out extrapolation best, with 4B/8B extrapolation error of 0.6e-3 on DROID and 1.4e-3 on RoboCasa, lower than a standard power law's 2.0e-3 and 3.7e-3. RoboCasa planning success improves with compute, with object-interaction push tasks showing no positive success until around 1e22 FLOPs. On real Franka tasks, RoboJEPA-8B reaches 67% Grasp, 50% Object Lift, and 27% Pick and Place success; RoboJEPA-4B reaches 60%, 30%, and 21%.

### 7. What is actually novel?

The novelty is not JEPA itself. It is the large-scale, multi-embodiment robotic world-model scaling study, the second-order compute law for latent imagination error, and the explicit link from offline error to image-goal planning performance.

### 8. What are the strengths?

The dataset mixture is broad, the model family spans several orders of magnitude, the scaling-law extrapolation is checked on larger held-out models, and the evaluation includes both simulated and real robot planning. The release of checkpoints and deployment code also matters.

### 9. What are the weaknesses, limitations, or red flags?

The representation encoder is frozen, so the scaling law describes the predictor on top of a fixed latent space, not full world-model representation learning. The training corpus is close to saturation under the current fits, so further gains may require more interaction data rather than only more parameters. The planning policy samples actions from a uniform distribution and uses image goals only, which leaves open how much better a learned proposal policy or language-conditioned goal interface would be.

### 10. What challenges or open problems remain?

The obvious next questions are joint encoder-predictor scaling, better data scaling, learned action proposals, text/image hybrid goals, and testing whether the offline error proxy survives distribution shifts outside DROID/RoboCasa-style manipulation.

### 11. What future work naturally follows?

Scale the representation encoder and predictor jointly. Fit data/compute/frontier laws rather than compute-only curves. Add a learned proposal policy for CEM or a policy distilled from successful model-predictive rollouts. Evaluate harder contact-rich manipulation and long-horizon tasks with out-of-domain objects and camera setups.

### 12. Why does this matter for cabbageland?

Cabbageland cares about world models that can be evaluated through useful proxies, not just watched as videos. RoboJEPA gives a template: define a latent rollout error, fit the compute frontier, check capability thresholds, and validate whether the proxy predicts downstream planning.

### 13. What ideas are steal-worthy?

Use offline imagination error as a planning proxy only after validating the correlation. Treat capability emergence as thresholded by compute, not smoothly present at every scale. Keep the scaling recipe deliberately simple when the research question is the scaling behavior itself.

### 14. Final decision

Preserve. This is a high-signal world-model scaling paper and the most relevant item in today's batch.
