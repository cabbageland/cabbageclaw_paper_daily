# Benchmarking World Models for Continual Learning on Compositional Tasks

## Basic info

* Title: Benchmarking World Models for Continual Learning on Compositional Tasks
* Authors: Haoyu Zhou, Joe Watson, Anson Lei, Ingmar Posner
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2609.22055
* Date surfaced: 2026-09-21
* Why selected in one sentence: It builds a benchmark that tests whether world models reuse previous mechanisms, not merely whether they adapt quickly to a new task.

## Quick verdict

* Must read

This is directly relevant because it turns compositional continual world modeling into a measurable problem. The paper's strongest contribution is not a new state-of-the-art robot result; it is the benchmark design that separates reuse from raw learning speed. The modular model result is useful but deliberately caveated by its dependence on a frozen privileged encoder.

## One-paragraph overview

The paper proposes a robot-manipulation benchmark where each curriculum trains primitive tasks first and then ends with a composition task built by recombining those primitives. The composition is factorized along action, perception, and full action-plus-perception axes, so the benchmark can ask where reuse fails. The authors evaluate DreamerV3, TD-MPC2, conventional continual-learning methods, and a progressive modular world model based on PWM. Conventional methods trade forgetting against transfer. Explicit modular dynamics nearly eliminate forgetting under a frozen encoder, but without that representation privilege they do not clearly beat the monolithic counterpart.

## Model definition

The paper is primarily a benchmark, but it evaluates trainable world models.

### Inputs

The models receive multi-camera observations, proprioception, action history, and current continuous actions. Observations use three camera views plus a 7-D proprioceptive vector; actions are 3-D relative end-effector displacement plus a scalar gripper command.

### Outputs

The shared world-model backbone encodes observations into latents and predicts action-conditioned latent transitions. Task-specific heads consume the latent state to produce reward, termination, value, and policy quantities needed for control.

### Training objective (loss)

DreamerV3 uses its generative reconstruction and latent dynamics objectives plus actor-critic training. TD-MPC2 uses decoder-free latent consistency, reward prediction, temporal-difference learning, and policy/planning objectives. The modular PWM variant trains a mixture of dynamics experts with routing while task-specific heads are reinitialized per task. The exact loss decomposition is inherited from the baseline models rather than invented as a new loss.

### Architecture / parameterization

DreamerV3 is a recurrent stochastic latent world model with an observation decoder. TD-MPC2 is a deterministic decoder-free latent dynamics model that uses policy-guided planning. PWM is a modular mixture-of-experts variant of TD-MPC2: each incoming task adds three trainable dynamics experts, previous experts are frozen, and a router combines all active experts.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It asks whether world models can continually learn a sequence of related robot tasks and then reuse previously learned primitives in a later compositional task without forgetting the earlier tasks.

### 2. What is the method?

The method is a benchmark and evaluation protocol. Six Meta-World-derived suites present primitive tasks followed by a composition task. The suites are grouped by action composition, perception composition, and full composition.

### 3. What is the method motivation?

Existing continual robot benchmarks often conflate two things: learning an unseen task quickly and reusing prior mechanisms. A composition task built from earlier primitives is a cleaner reuse test.

### 4. What data does it use?

It uses simulated robot-manipulation curricula built from Meta-World assets and environments, with dense rewards, scripted oracle reference returns, automatic resets, and online MBRL interaction.

### 5. How is it evaluated?

The paper reports backward transfer (BWT) for forgetting and forward transfer (FWT) for how efficiently the final composition task is learned relative to scratch. Returns are normalized between a failure floor and a scripted oracle reference.

### 6. What are the main results?

DreamerV3 generally beats TD-MPC2 across continual-learning methods. Conventional methods trade FWT against BWT: fine-tuning transfers but forgets, ER transfers best but only slows drift, EWC underperforms, and PackNet reduces forgetting at the cost of capacity. Under a frozen encoder, PWM reaches average BWT 3.85 and FWT 36.18 versus TD-MPC2's BWT 34.97 and FWT 38.11, nearly eliminating forgetting while matching forward transfer.

### 7. What is actually novel?

The novel part is the compositional continual benchmark and its action/perception/full factorization. The modular result is less novel architecturally, but it is useful as a diagnostic of what explicit expert reuse can and cannot buy.

### 8. What are the strengths?

The benchmark design is crisp. It tests reuse by construction, exposes perception shifts as a distinct bottleneck, and uses ablations to ask whether old experts actually contribute to composition-task performance.

### 9. What are the weaknesses, limitations, or red flags?

The strongest modular result depends on an encoder pretrained on demonstrations from all tasks and then frozen. That is a diagnostic privilege, not a deployable continual-learning solution. The evaluation is simulated, online, and tied to dense rewards and automatic resets.

### 10. What challenges or open problems remain?

The paper leaves open how to learn a stable task-agnostic representation without seeing all tasks in advance. It also flags task-conditioned routing as a limitation for temporally composed tasks, where the reusable primitive may change across stages.

### 11. What future work naturally follows?

A natural next step is a world model with a stronger pretrained visual backbone and state-conditioned expert routing, evaluated under the same compositional protocol without frozen privileged encoders.

### 12. Why does this matter for cabbageland?

Cabbageland keeps asking when structure actually supports reuse. This paper gives a clean answer format: build tasks where the only good shortcut is reusing prior mechanisms, then measure where that reuse fails.

### 13. What ideas are steal-worthy?

The action/perception/full composition split is worth stealing. So is the evaluation distinction between a reusable task-agnostic backbone and task-specific heads.

### 14. Final decision

Preserve. This is the most relevant paper of the day because it gives a better test for reusable world-model structure.
