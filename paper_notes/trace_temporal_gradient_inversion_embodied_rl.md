# Temporal Gradient Inversion for Private Trajectory Reconstruction in Embodied Reinforcement Learning

## Basic info

* Title: Temporal Gradient Inversion for Private Trajectory Reconstruction in Embodied Reinforcement Learning
* Authors: Sudip Bhujel, Shanghao Shi, Ruiquan Huang, Ning Zhang, and Yang Xiao
* Year: 2026
* Venue / source: arXiv / NeurIPS 2026
* Link: https://arxiv.org/abs/2609.30258
* Date surfaced: 2026-09-27
* Why selected in one sentence: It shows that ordered policy-gradient streams in embodied RL can leak private observation-action trajectories, not just isolated training examples.

## Quick verdict

**Useful**

This is a sharp privacy paper with a broader representation lesson: temporal structure amplifies leakage. The threat model is strong, but it matches the standard white-box honest-but-curious setup used in gradient inversion work.

## One-paragraph overview

TRACE attacks distributed embodied RL setups where agents keep raw observations on device but send ordered per-step policy-learning gradients to a server. Instead of inverting each gradient independently, TRACE encodes gradient updates, passes them through a causal transformer, and autoregressively decodes RGB observations plus discrete actions. The paper argues that adjacent embodied gradients carry correlated physical scene information and that policy-head gradients can reveal actions almost exactly under ordinary actor-critic losses. On held-out embodied navigation scenes, TRACE reconstructs trajectories with about 18.8 dB PSNR and near-perfect action recovery in a few milliseconds per frame, outperforming optimization and single-frame learning baselines.

## Model definition

### Inputs
TRACE takes a contiguous sequence of per-step gradients from an embodied RL client, along with white-box knowledge of the victim architecture, current checkpoint, action space, and learning rule. Training uses auxiliary trajectories from the same task family.

### Outputs
The attacker reconstructs RGB observation frames and predicts the corresponding discrete actions for each timestep in the trajectory.

### Training objective (loss)
TRACE uses a combination of pixel MSE, pixel L1, action cross-entropy, LPIPS/perceptual loss, and rollout supervision to reduce teacher-forcing exposure bias. The victim gradients come from PPO or A2C actor-critic objectives with value and entropy terms.

### Architecture / parameterization
The attacker has a gradient encoder, a causal temporal transformer, and a decoder for observations/actions. The default transformer uses six causal self-attention layers with eight heads, according to the appendix.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Distributed embodied RL can hide raw sensor data locally while exposing gradients. The paper asks whether those gradients leak full trajectories rather than only single frames.

### 2. What is the method?
TRACE amortizes gradient inversion over sequences. It maps each gradient to a latent, uses causal temporal attention to exploit trajectory context, then autoregressively decodes the observation-action stream.

### 3. What is the method motivation?
Embodied trajectories are temporally coherent. Consecutive camera views share layout, objects, lighting, and viewpoint geometry, and actor-critic policy-head gradients contain action-specific structure.

### 4. What data does it use?
The experiments use victim policies trained for point-goal navigation in AI2-THOR-like embodied scenes, with PPO and A2C variants. Evaluation uses 100 held-out trajectories of length T=8 for the main comparison.

### 5. How is it evaluated?
The paper reports MSE, PSNR, SSIM, LPIPS, action accuracy, and inference time. It compares against DLG, Inverting Gradients, and Learning to Invert adapted to the RL setting. It also tests held-out scene adaptation, defenses, trajectory length, victim architectures, multimodal inputs, larger action spaces, and gradient averaging.

### 6. What are the main results?
On the main held-out T=8 setting, TRACE reports MSE 0.014, PSNR 18.771 dB, SSIM 0.627, LPIPS 0.362, and 100% action accuracy under PPO, with 4.5 ms inference per frame. Under A2C, it reports PSNR 18.873 dB and 100% action accuracy at 3.0 ms. It improves over Learning to Invert by roughly 2 dB PSNR under PPO and about 1 dB under A2C.

### 7. What is actually novel?
The novelty is treating gradient inversion in embodied RL as trajectory reconstruction. The theoretical pieces around A2C/PPO gradient equivalence and policy-head action recovery support the empirical attack.

### 8. What are the strengths?
The attack is fast, sequence-aware, and tested beyond one default victim. The ablations show longer temporal context matters: the paper reports a substantial PSNR gain from T=1 to T=8.

### 9. What are the weaknesses, limitations, or red flags?
The attacker has strong white-box access and auxiliary data from the same task family. The privacy evaluation does not fully measure utility loss under the strongest defenses. The reconstructions are useful but not photorealistic, so the real-world harm depends on deployment context.

### 10. What challenges or open problems remain?
The hardest practical question is defense under acceptable RL performance cost. Sequence-aware privacy, secure aggregation, gradient aggregation, or DP-SGD may help, but each changes training cost and learning dynamics.

### 11. What future work naturally follows?
Test the attack on richer robotic policies, continuous actions, real robot camera streams, and federated settings with partial aggregation. On defense, evaluate privacy-utility tradeoffs for ordered gradient streams rather than single updates.

### 12. Why does this matter for cabbageland?
It is a reminder that sequence structure is a source of information, not just a modeling convenience. Any system that logs or transmits ordered internal traces needs privacy thinking at the trajectory level.

### 13. What ideas are steal-worthy?
Model gradient streams as temporal data. Use policy-head structure to recover actions. Evaluate privacy defenses against sequence reconstruction, not only single-example inversion.

### 14. Final decision

**Worth keeping as a useful warning.** The paper is less central than the world-model papers, but its trajectory-level view of leakage is a durable design lesson.
