# Encoding Memory in World Models with Test-Time Model-Based Reinforcement Learning

## Basic info

* Title: Encoding Memory in World Models with Test-Time Model-Based Reinforcement Learning
* Authors: Maxime Burchi, Fayaz Ali Dharejo, Radu Timofte
* Year: 2026
* Venue / source: arXiv:2611.09625v1; submitted November 6, 2026
* Link: https://arxiv.org/abs/2611.09625
* Date surfaced: 2026-11-09
* Why selected in one sentence: Episode-local parameter updates offer a concrete memory baseline beyond changing recurrent architectures, with replay regularization and explicit runtime costs.

## Quick verdict

* Highly relevant

Preserve the mechanism, but call it interactive adaptation rather than cheap inference. The useful separation freezes generic visual features while adapting dynamics and behavior to one episode; the strongest caveat is that this uses rewards, original training replay, and substantial evaluation compute. It does not provide an explicit map, permanent cross-episode memory, or a real-time deployment result.

**Read basis:** Full-text arXiv HTML main methods/results, replay and freezing ablations, Appendix A update-frequency study, actor/critic losses, pseudocode, and compute details. The PDF transfer timed out, but HTML provided the inspected text. The [official repository](https://github.com/burchim/TT-MBRL) README was reachable on November 9 and said code would be released soon; no runnable implementation was inspected or reproduced.

## One-paragraph overview

Rather than demand that one fixed recurrent state remember every new maze layout, TT-MBRL lets the model's weights change during evaluation. Each episode begins from the trained world-model, actor, and critic checkpoint and creates a fresh replay buffer. Gradient updates mix current-episode trajectories with old training data to prevent early overfitting. Visual encoder/decoder weights stay fixed, while dynamics and reward/continuation prediction adapt; the actor and critic then improve through imagined trajectories from that adapted model. The approach improves memory-heavy maze performance across recurrent, transformer, and structured-state-space backbones, but pays for the improvement with online learning and discards the adapted weights at the next episode.

## Model definition

### Inputs

Observation/action/reward/continuation sequences sampled from training replay and current-episode replay, normally in a 50/50 mixture. Memory Maze observations are 64×64 RGB images. The 2D variant sees a local 3×3 neighborhood with a target-color border, flattened to 75 values, and has five discrete actions. The policy receives deterministic/stochastic latent state; it is not fed a privileged full maze map.

### Outputs

The world model predicts latent-state distributions, rewards, and continuation flags; its pretrained decoder can reconstruct observations. The actor emits actions and the critic estimates imagined returns. At test time, model parameters themselves become episode-specific storage in addition to ordinary contextual state and a replay buffer.

### Training objective (loss)

The baseline Dreamer-style world model uses observation reconstruction plus reward and continuation negative log-likelihoods, with separately weighted dynamics and representation KL terms and stop-gradient targets. **Test-time updates remove reconstruction and freeze visual encoder/decoder parameters**, retaining reward/continuation prediction and latent KL objectives.

The actor uses REINFORCE with normalized imagined advantages plus entropy regularization. The critic learns discretized symlog-transformed lambda-returns using cross-entropy with an EMA-prediction regularizer. Imagined rollouts use a 15-step horizon in the background formulation. This is reward-informed model-based RL during evaluation, not label-free visual test-time adaptation alone.

### Architecture / parameterization

The framework is tested on DreamerV3's recurrent world model, TWISTER's transformer world model, and R2I's structured-state-space model. Learned pieces include visual representation modules, sequential dynamics and latent prediction, reward/continuation heads, and MLP actor/critic networks. The contribution is a reset/replay/update protocol, not a newly structured world-state representation.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

A world model shared across many randomized episodes can learn common visual and dynamical patterns but lose the layout peculiar to the current episode. Context-only memory can therefore generate an inconsistent future when the agent revisits a place. Architecture improvements do not eliminate this problem.

### 2. What is the method?

At episode start, copy pretrained world-model, actor, and critic parameters and initialize empty episode replay. Act, store the interaction, update the dynamics from mixed old/new replay, then update actor/critic using the adapted model. Reset these adaptations before the next evaluation episode. If early episode data are shorter than a required training sequence, training trajectories provide the missing context. Visual freezing reduces compute and stabilizes the coordinate system in which dynamics adapt.

### 3. What is the method motivation?

Generic knowledge and episode-specific facts need not share one memory mechanism. Keeping visual representations stable while adjusting transition predictions can encode repeated local structure in weights. Old replay provides a regularizer when the first few current observations are insufficient; delaying all adaptation until a large buffer fills instead sacrifices early benefits.

### 4. What data does it use?

Training interactions from Memory Maze 2D and the 3D Memory Maze benchmark at four sizes, then observations/rewards from each evaluation episode. The main maze budget is 100M training environment steps; R2I also receives a 400M-step setting. Twenty visual DeepMind Control tasks and 26 Atari games provide non-memory-focused checks. Atari's table reports 400K environment steps under the 100K-action benchmark accounting; these units should not be silently equated.

### 5. How is it evaluated?

Episode returns on randomized mazes; latent KL and video-prediction metrics over 100 unseen 64-frame trajectories; replay-mixture, prefill, freezing, and update-frequency ablations; and aggregate DMC/Atari scores. Primary 100M maze results average three runs with 100 evaluation episodes. The 400M R2I comparison uses six runs. The paper also tests extra optimization with **training data only** to distinguish new episode information from extra compute.

### 6. What are the main results?

- On 3D Memory Maze 15×15 at 400M training steps, R2I rises from **42.0 ± 5.8 to 54.1 ± 3.5**, versus the reported human score 67.7. On 13×13, 60.1 ± 1.6 becomes 63.0 ± 1.5.
- At 100M on 3D 15×15, R2I rises from 20.3 ± 1.1 to 29.3 ± 4.7; TWISTER from 23.1 ± 0.5 to 31.5 ± 1.8. Do not confuse these with the 400M numbers.
- In 2D 15×15, R2I scores 171.6 without adaptation, 171.7 with extra training-data-only updates, and 244.3 with mixed train/test replay. DreamerV3's corresponding values are 46.2, 47.0, and 185.0.
- DMC's aggregate mean improves from 776.2 to 788.2; Atari IQM from 0.502 to 0.514. These modest changes do not establish universal improvement on every task.

The quoted 53.7% improvement after 4,000 environment steps concerns the per-step reward improvement curve late in an episode, not a 53.7% improvement in aggregate episode return.

### 7. What is actually novel?

Applying episode-reset, replay-regularized test-time learning to Dreamer-style world models **and their behavior policies**, with evidence across several backbone families. Test-time training, parameter-based memory, replay regularization, and model-based policy learning already exist. The contribution is a useful protocol and empirical decomposition, not the discovery that gradient updates can store information.

### 8. What are the strengths?

It is architecture-agnostic enough to test across three different temporal model families. Training-only extra-compute controls address a common confound. Replay, visual freezing, and prefill experiments expose practical failure modes instead of leaving adaptation as a black box. Latent/pixel prediction improvements provide evidence beyond a return leaderboard.

### 9. What are the weaknesses, limitations, or red flags?

- **Runtime:** Table 6 reports **0.65 hours per 3D R2I episode** with visual modules frozen and 1.04 hours unfrozen. These compare two adapting variants; neither is a no-adaptation baseline time. The result is not a real-time controller claim.
- **Access assumptions:** Evaluation retains original training replay and receives environment rewards and continuation signals. A deployment without those resources is a different problem.
- **Memory semantics:** Weights are not an addressable, inspectable layout store. The replay buffer also stores episode information; this is not buffer-free memory compression.
- **Attribution:** Model, actor, and critic all change. The combined result should not be attributed solely to improved world-model memory without further isolation.
- **Lifetime:** Adaptation is reset between episodes, so the experiment does not demonstrate lifelong accumulation or controlled consolidation.
- **Evidence scope:** Most central gains are from maze-like environments; explicit mapping/retrieval alternatives and equal-latency deployment comparisons remain important baselines. Public implementation was still pending when checked.

The paper earns “test-time model-based adaptation,” not “explicit-state simulator,” “neurosymbolic memory,” or general deployment-ready continual learning.

### 10. What challenges or open problems remain?

Compressing adaptation into a usable latency budget; robust updates under nonstationary rewards or corrupted observations; separating layout learning from policy improvement; and deciding which facts should persist across episodes. Catastrophic within-episode overfitting is mitigated, not guaranteed absent.

### 11. What future work naturally follows?

Compare against an explicit maze map, retrieval memory, longer context, and lightweight low-rank adaptation under matched wall-clock and interaction budgets. Hold actor/critic fixed while adapting the model, and vice versa. Test removal or compression of original training replay. Add controlled layout changes mid-episode to measure stale-memory recovery, not just eventual return.

### 12. Why does this matter for cabbageland?

Any claim that a new recurrent architecture solves world-model memory should now answer a simpler alternative: why not adapt the transition model within the episode? The visual/dynamical split is especially reusable. But whether parameter memory is preferable to explicit state depends on editability, retrieval, latency, and supervision—not only a maze score.

### 13. What ideas are steal-worthy?

- Reset episode adaptation to a stable checkpoint rather than silently leaking evaluation knowledge across episodes.
- Keep the representational coordinate system fixed while adapting dynamics.
- Mix generic replay with immediate observations to control early-update overfitting.
- Measure adaptation quality against both elapsed compute and observations accumulated.
- Report world-model-only, policy-only, and joint adaptation before assigning causal credit.

### 14. Final decision

**Preserve as a required memory/adaptation baseline, with a runtime warning attached.** A useful small follow-up is model-only versus joint adaptation against an explicit map under a fixed latency budget. Do not describe the current evidence as cheap inference, permanent memory, or a reproduced public implementation.
