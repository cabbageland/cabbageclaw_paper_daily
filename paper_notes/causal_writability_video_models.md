# A Chosen Future Can Still Be Rewritten: Causal Writability in Video Models

## Basic info

* Title: A Chosen Future Can Still Be Rewritten: Causal Writability in Video Models
* Authors: Xingyun Wang, Haomin Zheng, Man Yuan, Leqian Yang, Ziming Liu
* Year: 2026
* Venue / source: arXiv:2609.15980
* Link: https://arxiv.org/abs/2609.15980
* Date surfaced: 2026-09-15
* Why selected in one sentence: It gives a causal test for whether a video model's physically correct future is absent, merely unused, or still internally writable after the natural rollout chooses a shortcut.

## Quick verdict

* Must read

This is the strongest paper in today's batch. The useful claim is not just that video models can take shortcuts; it is that the alternative physical future can remain internally available and causally executable even when generation follows the wrong cue. This note is based on the full arXiv text.

## One-paragraph overview

The paper studies video models trained on correlated appearance and motion, especially red slow masses and blue fast masses, then tests conflicting examples such as a red mass with fast observed motion. When the natural rollout follows color and generates the wrong slow future, the authors intervene on internal activations with a compact edit predicted from boundary physical state and target motion. The edit restores the motion-consistent future, but only up to a depth boundary where the same intervention stops changing decoded motion. The paper calls this causal writability: the model has not lost the physical alternative, but the route by which that alternative can control future tokens closes during inference.

## Model definition

### Inputs

The controlled experiments use observed video frames, object color, boundary state at the final observed frame, and target motion direction. The main Spring setup uses 65 observed frames followed by 64 generated frames, with Long and Short variants controlling how much motion history is visible. The pretrained replication uses a Wan 1.3B video DiT adapted under different training orders.

### Outputs

The model outputs generated future video. The analysis outputs fitted generated frequency, physics-follow rate, normalized frequency recovery, writable-site counts, and layerwise causal writability profiles.

### Training objective (loss)

The synthetic Spring model is a 488M-parameter latent flow-matching Transformer with a frozen Wan2.1 VAE. It is trained for video generation under biased color-motion correlations. The intervention controller is fit separately to predict activation edits from target family and boundary phase; it is not the main video model objective.

### Architecture / parameterization

The main model is a bidirectional DiT-style latent flow-matching video Transformer. The key analytic parameterization is an activation edit: aligned-minus-conflict differences on observed-frame token states, projected into a low-dimensional PCA basis and then predicted from a first-harmonic boundary-state controller. The paper also localizes the controlling route to attention K/V writes from observed-frame tokens into future-frame tokens.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Video rollouts can fail under shortcut correlations, but the output alone cannot tell whether the model never learned the physical rule or learned it and then failed to use it. The paper tries to separate absence of a solution from failure of causal access to a solution.

### 2. What is the method?

The method builds matched aligned/conflict pairs that share observed motion, boundary state, and generation seed but differ in color. It takes an internal difference from the aligned run and applies it to the conflict run. It then measures whether the decoded future moves from the shortcut future toward the motion-consistent future. The authors compress these edits with PCA and fit donor-free controllers from boundary phase and target direction.

### 3. What is the method motivation?

Shortcut failures are usually treated as missing knowledge or insufficient data. This paper asks a sharper question: can the correct future be written into the model's computation after the natural path has chosen a different future? If yes, model failure is partly a control and commitment problem, not only a representation problem.

### 4. What data does it use?

The controlled data are synthetic spring-mass, pendulum, and free-fall videos with deliberately correlated appearance and dynamics. The pretrained replication adapts Wan 1.3B on biased and neutral-first variants of the same dynamics task.

### 5. How is it evaluated?

The paper evaluates decoded video behavior using fitted physical variables such as frequency or gravity. It reports physics-follow rates, normalized recovery after edits, how many network sites remain writable, and component interventions that restore or remove causal recovery.

### 6. What are the main results?

Four edit coordinates retain nearly the full effect: 87.8% of held-out top-four writes satisfy the .75 to 1.25 recovery window, compared with 92.4% for the full paired-difference edit. A donor-free controller synthesized from target family and boundary phase succeeds on 85.9% of held-out writes across six run-direction groups. Across 15 Short runs, physics-following behavior rises from .52 at 5K to .60 at 100K while remaining shortcut errors become less writable, falling from 10.88 to 9.55 writable sites. Future-rescued errors are already writable at 3.79 more sites at 5K than persistent shortcut errors. In Wan 1.3B, neutral-first adaptation raises conflict physics-following to 80.5% versus 9.4% for direct biased adaptation and delays closure.

### 7. What is actually novel?

The novelty is causal writability as an internal controllability test for video futures. The paper does not stop at shortcut diagnosis; it shows compact physical edits, a closure boundary, training-time movement of that boundary, and an attention-mediated route by which observed motion writes into future tokens.

### 8. What are the strengths?

The controlled design is unusually clean. The intervention is tied to decoded physical behavior, not just hidden-state separability. The paper distinguishes observability from controllability: a physical signal can remain detectable after it no longer controls generation. The pretrained Wan replication makes the mechanism less likely to be a toy-only artifact.

### 9. What are the weaknesses, limitations, or red flags?

The core experiments use synthetic dynamics where matched counterfactuals and physical variables are available. The interventions require internal access and careful matching, so they are more diagnostic than immediately deployable. The pretrained result is an adapted video DiT on a controlled task, not an audit of arbitrary real-world videos.

### 10. What challenges or open problems remain?

The major open problem is whether the same write/closure phenomenon can be measured in messy real scenes where the relevant state variables are not obvious. Another is how to train models so a correct physical alternative remains causally usable without relying on post-hoc activation edits.

### 11. What future work naturally follows?

Run causal writability scans on navigation, manipulation, object permanence, and long-video prediction. Add losses that preserve writable physical state deeper into generation. Use closure depth as an early warning for which shortcut failures training will or will not repair.

### 12. Why does this matter for cabbageland?

Cabbageland cares about world models whose internal state actually carries the causal variable the architecture claims to model. This paper gives a precise way to ask whether a world model's state is merely readable or actually controllable.

### 13. What ideas are steal-worthy?

Separate "can decode the variable" from "can make the variable control the rollout." Measure writable-site count as a training diagnostic. Use matched shortcut pairs to build causal edit directions. Treat attention K/V paths as the route by which observed evidence commits future state.

### 14. Final decision

Preserve. This is a mechanism-rich world-model diagnostic and the most reusable idea in the batch.
