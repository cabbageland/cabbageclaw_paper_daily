# Beyond Myopic World Models: Long-Horizon End-to-End Training for Direct Future Prediction

## Basic info

* Title: Beyond Myopic World Models: Long-Horizon End-to-End Training for Direct Future Prediction
* Authors: Xinyi Li, Zaishuo Xia, Chenjie Hao, Yubei Chen
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.07420
* Date surfaced: 2026-08-16
* Why selected in one sentence: It cleanly argues that long-horizon world-model failure is often a supervision-horizon problem before it is an architecture problem.

## Quick verdict

* Highly relevant

I inspected the arXiv HTML full text. This is the most useful world-model paper in the set because it does not hide behind a new backbone name; it directly asks whether one-step supervision is structurally misaligned with long-horizon use.

## One-paragraph overview

The paper proposes Direct Prediction World Model (DPWM), a non-recursive model that predicts the endpoint observation from the initial observation and the whole action sequence in a single forward pass. Instead of fitting only one-step transitions and then recursively rolling them forward, DPWM trains end-to-end on K-step endpoint prediction across a range of horizons. The main claim is that long-horizon accuracy depends heavily on aligning the loss with the actual prediction horizon, because one-step training both creates train-inference mismatch and assigns gradient without regard to downstream endpoint sensitivity. On continuous-control and pixel-based benchmarks, DPWM substantially improves endpoint accuracy, with especially large gains at long horizons.

## Model definition

### Inputs
The model takes the initial observation and an action sequence of length K, where K is sampled from a predefined horizon distribution during training.

### Outputs
It outputs the endpoint observation at time t+K in a single pass, without generating intermediate states.

### Training objective (loss)
The model minimizes squared error between the predicted endpoint observation and the true endpoint observation over sampled horizons K. This is a direct K-step endpoint loss rather than a one-step transition loss.

### Architecture / parameterization
The pipeline uses an observation encoder, a Transformer action-sequence encoder, a FiLM-conditioned residual MLP dynamics module, and an observation decoder. The important structural property is that the dynamics module is non-recursive with respect to horizon.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the mismatch between long-horizon use of world models and the short-horizon objectives that most of them are trained on.

### 2. What is the method?
The method is to train a single model to predict endpoint observations directly across many horizons, compressing the full action sequence and avoiding recursive rollout during both forward prediction and gradient propagation.

### 3. What is the method motivation?
Recursive rollout amplifies small errors and trains the model on the wrong objective. If the downstream task cares about the endpoint, then the loss should land on the endpoint rather than hoping short-horizon fidelity composes well.

### 4. What data does it use?
The paper evaluates on four DeepMind Control Suite tasks in raw state space, namely cheetah-run, humanoid-walk, hopper-hop, and walker-run, and also reports pixel-based benchmark results.

### 5. How is it evaluated?
It compares DPWM against recursive and any-step world-model baselines such as ADM and MoSim. The main metric is endpoint prediction error at multiple horizons under both random and policy-generated trajectory datasets, with additional comparisons to recurrent baselines retrained under the same long-horizon objective.

### 6. What are the main results?
The gains explode with horizon. On the policy-trained Cheetah setting at horizon **100**, endpoint MSE is **0.4452** for DPWM versus **25.6086** for ADM and **11.0004** for MoSim. On the random-data Cheetah setting at horizon **100**, DPWM reaches **0.1854** versus **1.7240** for ADM and **0.3215** for MoSim. The paper also shows that recurrent baselines improve when retrained with the same endpoint objective, supporting the claim that the loss is the main story.

### 7. What is actually novel?
The most important novelty is the framing: supervision horizon is treated as a primary design variable for world models. DPWM is useful, but the deeper contribution is the argument that long-horizon endpoint loss is the right training target.

### 8. What are the strengths?
The paper makes a clean causal argument, backs it with controlled comparisons, and refuses to over-claim that a new architecture alone solved the problem. The theory and experiments point in the same direction.

### 9. What are the weaknesses, limitations, or red flags?
The evaluation is about endpoint prediction rather than downstream planning or control. Independently queried endpoints are not forced to form a temporally consistent trajectory, and the paper focuses mainly on deterministic settings.

### 10. What challenges or open problems remain?
The open problems are how to turn endpoint gains into planning gains, how to impose trajectory consistency across queried horizons, and how to extend the approach cleanly to stochastic environments.

### 11. What future work naturally follows?
Future work should plug direct endpoint objectives into planning loops, compare against stronger recurrent baselines under identical long-horizon training, and test hybrid schemes that preserve consistency while still avoiding recursive error amplification.

### 12. Why does this matter for cabbageland?
Because it sharpens a reusable principle: if a system will be judged at long horizon, the supervision should usually know that too. This is the same taste cabbageland keeps needing in agents, memory, and planning.

### 13. What ideas are steal-worthy?
Treat supervision horizon as a first-class design choice. Separate architectural contribution from objective contribution. Use direct endpoint loss when the downstream task only really cares about where the process lands.

### 14. Final decision
Keep as a preserved note. Even if the final architecture is not the last word, the objective critique is strong and likely to transfer.

## 6. Mandatory critical angles

The paper is strongest on mechanism, evaluation framing, and transferability of the underlying lesson. It is weaker on downstream control evidence and on explicit state beyond the latent prediction interface.

## 7. Writing style

The right tone is approving but precise. The paper earns credit mainly for the objective argument, not for the glamour of a new acronym.

## 8. Repository output format

Saved as a preserved paper note because the supervision-horizon argument is more reusable than the specific model instantiation.
