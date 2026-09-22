# Lifted Bellman Linear Programming for Offline Reinforcement Learning

## Basic info

* Title: Lifted Bellman Linear Programming for Offline Reinforcement Learning
* Authors: Hyukjun Yang, Jongchan Park, Narim Jeong, Donghwan Lee
* Year: 2026
* Venue / source: arXiv:2609.24489
* Link: https://arxiv.org/abs/2609.24489
* Date surfaced: 2026-09-22
* Why selected in one sentence: It turns offline critic learning into in-sample Bellman inequality constraints rather than bootstrapped regression against moving targets.

## Quick verdict

Highly relevant. This is a strong RL/control note because it changes the critic objective instead of adding a larger actor family or heuristic rollout patch. The theory is tabular, but the empirical ALBUM implementation is simple enough to be worth remembering. Full arXiv text was inspected.

## One-paragraph overview

Offline RL usually trains a critic by regressing against bootstrapped value targets, often stabilized by target networks, critic ensembles, and policy constraints. This paper starts from the linear programming characterization of Bellman optimality and lifts it into a joint Q,V program whose constraints only involve state-action pairs present in the offline dataset. The relaxed neural implementation, ALBUM, uses hinge penalties with detached multi-step rollout targets. On OGBench, it matches strong flow-policy baselines with a much smaller Gaussian-policy setup and no target network.

## Model definition

### Inputs

Inputs are offline transition datasets of state, action, reward, next-state tuples. The neural implementation consumes sampled in-dataset transitions and K-step dataset trajectory segments for Bellman and rollout hinge constraints.

### Outputs

The method learns a Q critic, a V function, and a Gaussian actor policy. The critic estimates in-sample values for policy extraction and improvement.

### Training objective (loss)

LBLP defines Bellman optimality through linear inequality constraints in the joint Q,V space. ALBUM relaxes these constraints into hinge penalties, includes K-step rollout constraints, and detaches rollout targets with stop gradient. The actor is trained with a standard policy improvement objective built on the learned critic.

### Architecture / parameterization

The tabular theory is a linear program over Q,V. The approximate method parameterizes Q, V, and the Gaussian actor with neural networks. It deliberately avoids critic ensembles and target networks.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It addresses offline RL's critic problem: bootstrapped regression can amplify values for out-of-distribution actions and usually needs target networks, ensembles, or heavy policy restrictions to stay stable.

### 2. What is the method?

The method formulates Lifted Bellman Linear Programming over Q and V, with constraints involving only state-action pairs found in the dataset. It then relaxes the constrained program with hinge penalties and implements the result as ALBUM.

### 3. What is the method motivation?

The motivation is that the LP view makes Bellman optimality an inequality-feasible smallest-function problem rather than moving-target regression. Lifting to Q,V avoids querying all next actions outside the dataset while still supporting policy extraction.

### 4. What data does it use?

The empirical evaluation uses OGBench state-based offline RL tasks. The paper also includes tabular and appendix analyses to validate the theoretical behavior of the constraints.

### 5. How is it evaluated?

ALBUM is compared with Gaussian-policy methods, diffusion-policy methods, flow-policy methods, and horizon-reduction or action-chunking methods. Metrics are success rates on OGBench tasks, plus ablations for target networks, critic ensembles, rollout horizon, coefficient conditions, and compute cost.

### 6. What are the main results?

On OGBench state-based tasks, ALBUM averages 43.4 success, essentially matching FQL at 43.6 and beating ReBRAC at 31.0. It leads on antmaze-large-navigate, antmaze-giant-navigate, scene-play, and puzzle-3x3-play. It uses 2.43M parameters and 78 MiB peak GPU memory, the fewest among compared methods, and reduces time per step by 44% versus FQL.

### 7. What is actually novel?

The novelty is the lifted primal LP over joint Q,V with in-dataset constraints, plus the hinge relaxation that can be implemented as a practical neural critic objective. The K-step constraints accelerate propagation without changing the ideal minimizer.

### 8. What are the strengths?

The method has a clean conceptual story: impose in-sample Bellman optimality directly. It is also computationally lean: one critic, no target network, no critic ensemble, and a simple Gaussian actor.

### 9. What are the weaknesses, limitations, or red flags?

The formal guarantees are strongest in finite or tabular settings, with deterministic-dynamics results for the sandwich property. Neural convergence is not established. Performance is uneven: ALBUM is weak on humanoidmaze-large and lower than action-chunking methods on some manipulation categories.

### 10. What challenges or open problems remain?

The big open problem is extending the analysis to stochastic transitions and neural function approximation. Another is determining when ALBUM's simple one-step actor is enough versus when action-chunking genuinely gives needed temporal abstraction.

### 11. What future work naturally follows?

Hybridizing LBLP-style critic constraints with richer policy classes is natural. So is using the constraint geometry for uncertainty or conservative value intervals in offline control.

### 12. Why does this matter for cabbageland?

Cabbageland cares about long-horizon decision-making and explicit optimization structure. This paper is a reminder that better planning can come from the value-learning geometry, not just bigger policies.

### 13. What ideas are steal-worthy?

Steal the question "can this Bellman update be written as an in-sample constraint?" Also steal the audit practice of checking bounded-update coefficient conditions; when violated, the paper shows V values can drift to the order of -1e6 and performance collapses.

### 14. Final decision

Preserve. This belongs in the offline RL and long-horizon value-propagation pile.
