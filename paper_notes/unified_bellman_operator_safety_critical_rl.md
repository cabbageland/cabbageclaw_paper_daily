# A Unified Bellman Operator for Safety-Critical Reinforcement Learning

## Basic info

* Title: A Unified Bellman Operator for Safety-Critical Reinforcement Learning
* Authors: Nishanth Arun Rao, Royina Karegoudra Jayanth, Benjamin Eysenbach, Jaime Fernandez Fisac
* Year: 2026
* Venue / source: arXiv preprint
* Link: https://arxiv.org/abs/2610.12420
* Date surfaced: 2026-10-10
* Why selected in one sentence: It puts safety and task return into one Bellman recursion instead of relying on separate safety filters or average-cost CMDP constraints.

## Quick verdict

* Useful

This is a theory-heavy safe RL paper with a genuinely useful framing move. The best part is the value-level coupling: a policy should optimize return only inside a safety-certified recursion, not learn task behavior first and get clipped by a filter later. The caveats are serious: the proof depends on idealized assumptions and scaled safety margins, while the neural JointSAC implementation no longer inherits strict forward invariance.

## One-paragraph overview

The paper proposes a robust joint Bellman operator that combines task reward with a safety action-value function. A fast timescale estimates the safety value of the current joint policy, while a slow timescale estimates the joint value whose greedy policy must optimize return under adversarial disturbances without leaving the safe set. The authors prove contraction-style properties, forward invariance of the safe configuration set, and convergence to optimal safety-constrained task values under their assumptions. They then approximate the operator with JointSAC and evaluate it against safety filters and CMDP baselines on adversarial continuous-control tasks.

## Model definition

### Inputs

The learning setup receives states, controller actions, adversarial disturbances, rewards, and a continuous safety margin. In experiments, the environments are Gymnasium locomotion and SafetyGymnasium SafeVelocity tasks augmented with adversarial disturbances.

### Outputs

The learned system outputs a controller policy and a disturbance policy through a joint action-value function. It also learns a safety action-value function used to evaluate whether the joint policy remains safe.

### Training objective (loss)

The theoretical objective is fixed-point learning under a joint Bellman operator where task reward is truncated by the safety action-value. The algorithm uses two-timescale stochastic approximation: the safety critic tracks the safety value of the current joint policy on a fast timescale, while the joint critic updates on a slow timescale. The continuous-control implementation, JointSAC, follows a SAC-like actor-critic approximation with controller/disturbance gradient descent-ascent and finite timescale separation.

### Architecture / parameterization

The theory is operator-level and not architecture-specific. JointSAC is a deep RL approximation based on ISAACS and SAC, with separate controller and disturbance policies and critics for safety and joint values.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Safe RL methods often either enforce safety through external filters that can fight the task policy, or optimize expected constraint costs that do not guarantee safety at every time. The paper tries to learn a policy that maximizes task return while keeping strict safety as part of the value recursion.

### 2. What is the method?

It defines a safety action-value for the current joint policy and a joint action-value whose Bellman target is truncated by that safety value. The controller maximizes the joint value while the disturbance minimizes it. Learning proceeds on two timescales so the safety critic can evaluate the policy before the joint critic moves too far.

### 3. What is the method motivation?

Safety filters intervene at the boundary and can produce jittery or aliased actions when a reward policy keeps trying unsafe moves. Lagrangian CMDP methods usually bound expected cost, not worst-case forward invariance. The motivation is to make safety endogenous to the value target.

### 4. What data does it use?

The main experiments use three Gymnasium locomotion environments and eight SafetyGymnasium SafeVelocity environments, all with adversarial disturbances. Evaluation uses five training seeds and 300 rollouts per seed, totaling 1,500 evaluation rollouts per environment setup.

### 5. How is it evaluated?

The paper reports episodic rewards and costs during training and final rollout evaluations. It compares JointSAC against least-restrictive safety filters, PCPO, PPO-Lag, and SAC-Lag.

### 6. What are the main results?

JointSAC shows stable convergence with near-zero episode costs on the plotted SafeVelocity tasks. Across all 11 environments, the paper reports near-zero evaluation violations, with maximum cost 0.03 plus/minus 0.08 on Hopper-v4. On Hopper-v4, JointSAC gets reward 3266.89 plus/minus 103.80 with cost 0.03 plus/minus 0.08, while PPO-Lag and SAC-Lag show nonzero costs and lower rewards in the excerpted table. On InvertedPendulum-v4, JointSAC gets 999.43 plus/minus 1.28 reward and zero cost.

### 7. What is actually novel?

The novelty is the unified safety-constrained Bellman operator and its two-timescale learning analysis, not a new neural network architecture. The operator couples safety evaluation and task optimization at the value-function level.

### 8. What are the strengths?

The paper directly targets the mismatch between safety filters and reward policies. It gives a formal convergence and forward-invariance story under assumptions, and then tests a neural approximation in adversarial continuous-control settings rather than only tabular examples.

### 9. What are the weaknesses, limitations, or red flags?

The strict safety proof does not transfer cleanly to high-dimensional neural approximations. The convergence analysis relies on sufficiently scaled safety margins, which can create numerical issues and require heuristic tuning. The method assumes well-defined continuous safety margins and full state observability, which are exactly the hard parts in messy real-world settings.

### 10. What challenges or open problems remain?

The main challenge is preserving guarantees when function approximation, partial observability, perception error, and learned safety margins enter the loop. Another is making the safety margin specification itself robust and auditable.

### 11. What future work naturally follows?

Pair the operator with certified or interval-valued critics, learn conservative safety margins from perception with uncertainty, and test it in domains where safety constraints are not perfectly known. It would also be useful to compare action smoothness and intervention behavior against safety filters in more detail.

### 12. Why does this matter for cabbageland?

Cabbageland cares about decision-making under uncertainty and systems that do not bolt safety on after the fact. This paper gives a clean value-level pattern: safety should shape the recursion that defines good action, not merely post-process actions.

### 13. What ideas are steal-worthy?

Use separate timescales for "is this policy safe?" and "how should this policy improve?" Truncate task value with safety value. Compare safe RL methods under adversarial disturbances, not only average-cost training curves. Be explicit about where theory stops and neural approximation begins.

### 14. Final decision

Preserve as a useful RL/control note. It is less directly plug-and-play than the top four papers, but the operator-level framing is worth keeping.
