# The World Model Remembers, the Actor Forgets: Dream Rehearsal for Continual Model-Based RL

## Basic info

* Title: The World Model Remembers, the Actor Forgets: Dream Rehearsal for Continual Model-Based RL
* Authors: Gurp Nijjer
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.19749
* Date surfaced: 2026-07-23
* Why selected in one sentence: It cleanly localizes continual-learning failure in Dreamer-style agents to the actor channel and then uses the retained world model itself as a rehearsal source.

## Quick verdict

**Must read**

This is the best kind of continual-learning paper: it first checks the field's implicit premise instead of building another fix on top of it. The useful surprise is that replay preserves the world model far better than behavior, so the actor is the thing that forgets. I inspected the arXiv HTML sections covering the abstract, introduction, experimental setup, component-localization section, recovery-from-imagination section, dream rehearsal section, grading section, and conclusion.

## One-paragraph overview

The paper studies DreamerV3-style model-based RL agents trained sequentially on multiple tasks with an unbounded replay buffer. The standard intuition says replay should preserve old-task competence by keeping the world model accurate. The paper measures that assumption directly and finds a split result: reward prediction, value estimates, and termination structure for old tasks survive almost intact, while the actor's behavior still collapses. From there the paper introduces dream rehearsal, a supervised self-imitation procedure on world-model-generated trajectories that are graded before being used for actor updates. The core claim is that in this replay-maintained regime, continual forgetting is mostly a policy-learning channel problem rather than a world-memory problem.

## Model definition

### Inputs
The agent consumes MiniGrid RGB observations, replayed past experience, and imagined rollouts produced by its own world model during rehearsal.

### Outputs
The world model predicts latent dynamics, reward, continuation, and decoded observations, while the actor outputs actions for both real-environment interaction and imagination-based training.

### Training objective (loss)
The base agent uses standard DreamerV3-style world-model, critic, and actor training. Dream rehearsal adds supervised self-imitation updates on graded imagined trajectories, using a realized-first grading rule to decide which dream segments are worth cloning.

### Architecture / parameterization
The setup uses a `17M`-parameter DreamerV3 world model with a CNN encoder, RSSM, and reward/continuation/decoder heads, plus a `1.8M`-parameter actor with imagination horizon `H=15`.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to explain and fix catastrophic forgetting in sequential model-based RL when the agent already keeps all past experience in replay.

### 2. What is the method?
The method first probes the final agent checkpoint to see which component actually forgets, then rehearses the actor with supervised cloning on world-model-generated trajectories that pass a grading rule.

### 3. What is the method motivation?
If the world model already preserves the old-task signal, then adding more replay or more world-model protection is attacking the wrong object. The actor needs a more reliable learning channel.

### 4. What data does it use?
It uses sequential MiniGrid task chains. The core four-task chain is DoorKey-5x5 -> SimpleCrossingS9N1 -> LavaGapS5 -> MultiRoom-N2-S4, with an eight-task extension for scale-up checks.

### 5. How is it evaluated?
It is evaluated by sequential retention across tasks, component-level probes of reward/value/termination knowledge, recovery experiments inside imagination, and comparisons against plain replay, frozen-policy references, and matched real-episode cloning.

### 6. What are the main results?
Under never-clear replay, reward discrimination retains at roughly `1.0`, but plain replay still passes `0/3` four-task chains. RL-in-imagination fails to recover lost skills on `0/3` seeds, while supervised self-imitation from graded dreams succeeds on `3/3` with zero new environment interaction. Interleaved dream rehearsal yields `3/3` four-task chains, `3/3` eight-task chains, and a paired gain of about `+0.13` over matched real-episode cloning.

### 7. What is actually novel?
The novelty is the decomposition. The paper does not just propose another rehearsal trick; it first shows that the world model is already the remembered component, so the actor-learning channel is the real failure mode.

### 8. What are the strengths?
It asks the right causal question, uses component-level probes instead of behavior-only metrics, reports pre-registered refuted hypotheses, and turns the localization result into a rehearsal mechanism that actually matches the diagnosis.

### 9. What are the weaknesses, limitations, or red flags?
Everything is demonstrated on MiniGrid chains with `n=3` seeds and a `17M`-parameter agent. That is enough to make the phenomenon interesting, but not enough to settle how far it scales.

### 10. What challenges or open problems remain?
The main open problem is whether this actor-channel failure still dominates in larger environments, continuous-control settings, or richer world models where imagination quality itself may become the bottleneck.

### 11. What future work naturally follows?
Test dream rehearsal on larger domains, stabilize the policy-gradient channel more directly, and learn better dream-grading criteria that do not depend on careful hand-audited failure analysis.

### 12. Why does this matter for cabbageland?
Cabbageland cares about explicit state, world models, and continual competence. This paper gives a sharper ontology: remembered latent structure and retained behavior are not the same thing, so interventions should be attached to the failing channel.

### 13. What ideas are steal-worthy?
Measure component retention separately before designing the fix. Treat the world model as a rehearsal generator rather than just a prediction module. Use realized-first grading so imagined successes do not outrank genuinely useful trajectories.

### 14. Final decision
**Keep it.** The localization result alone is worth preserving, and the repair is aligned with the diagnosis instead of being another decorative continual-learning patch.
