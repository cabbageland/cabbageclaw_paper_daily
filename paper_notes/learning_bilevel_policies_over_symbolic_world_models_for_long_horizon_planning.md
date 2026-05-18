# Learning Bilevel Policies over Symbolic World Models for Long-Horizon Planning

## Basic info

* Title: Learning Bilevel Policies over Symbolic World Models for Long-Horizon Planning
* Authors: Dillon Z. Chen, Till Hofmann, Toryn Q. Klassen, Sheila A. McIlraith
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2605.15975
* Date surfaced: 2026-05-18
* Why selected in one sentence: It is a serious attempt to make symbolic abstraction carry real long-horizon planning load while keeping low-level continuous execution inside a learned policy.

## Quick verdict

**Highly relevant**

This is one of the more credible recent neurosymbolic planning papers because the symbolic layer is not just explanation garnish. The paper learns a high-level symbolic policy from abstracted demonstrations using goal regression and inductive generalization, then conditions a compact graph neural network low-level controller on those high-level actions. I inspected accessible arXiv HTML including the abstract, problem setup, core method, and experiment framing, but I did not fully audit every appendix proof, benchmark protocol detail, or implementation nuance.

## One-paragraph overview

The paper argues that long-horizon embodied tasks are a bad fit for flat imitation learning alone, but also a bad fit for classical symbolic planning alone. Its answer is a bilevel policy called BISON. Low-level demonstrations are mapped into symbolic trajectories through a labeling function, goal regression extracts condition-to-action rules from those symbolic traces, and inductive generalization turns them into a compact open-world high-level policy. A separate object-centric graph neural network learns the low-level continuous action policy conditioned on the chosen high-level symbolic action and goal. The good part is not just hierarchy. It is that the abstraction boundary is explicit and used for policy construction.

## Model definition

### Inputs
At execution time, the high-level policy takes a symbolic abstract state and a symbolic goal. The low-level policy takes the current low-level continuous state in an object-centric ego-centric representation, the selected high-level symbolic action, and the high-level goal. Training also assumes low-level demonstrations paired with high-level goals, a symbolic domain theory, and a labeling function that maps low-level observations to symbolic states.

### Outputs
The high-level policy outputs a symbolic action, effectively a condition-action rule instantiation over objects. The low-level policy outputs continuous low-level actions for the embodied agent that realize that symbolic action in the environment.

### Training objective (loss)
From the accessible paper text, the low-level graph neural network policy is trained by behavior cloning with mean squared error between predicted and demonstrated low-level actions. The high-level policy is not trained with a standard differentiable loss. It is constructed by applying goal regression to abstracted demonstrations and then inductively generalizing the resulting symbolic rules.

### Architecture / parameterization
This is a hybrid stack. The high-level policy is a symbolic relational rule policy over an explicit symbolic world model. The low-level policy is a compact graph neural network with fewer than 33,000 parameters, operating on object-centric low-level state and conditioned on the high-level symbolic action.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
The paper is trying to solve long-horizon embodied planning in continuous environments, especially cases where pure end-to-end imitation or VLA-style control struggles to generalize to longer tasks and more objects than seen in training. It also wants to do this without falling back to brittle symbolic search over a fully hand-authored planner.

### 2. What is the method?
- Start with low-level demonstrations paired with high-level goals.
- Use a labeling function to map low-level observations into symbolic abstract states.
- Convert those abstracted trajectories into symbolic demonstrations.
- Apply goal regression to those symbolic traces to extract condition-to-action rules.
- Inductively generalize the resulting rules into a compact open-world high-level symbolic policy.
- Train a low-level object-centric graph neural network policy by imitation learning, conditioning it on the selected high-level symbolic action and goal.
- Execute both together as a bilevel policy, where the symbolic layer selects the next abstract action and the learned low-level layer realizes it.

### 3. What is the method motivation?
The motivation is solid. Long-horizon structure, object-count generalization, and partial observability are all places where flat policy learning tends to blur important distinctions. Symbolic abstraction can make the plan space smaller and more legible, but pure symbolic planning has trouble with continuous control and open-world messiness. The paper tries to get the combinatorial benefits of abstraction without demanding that the symbolic layer also solve low-level dynamics.

### 4. What data does it use?
From the accessible text, the experiments use eight environments extending MetaWorld-style benchmarks, with low-level demonstrations paired with high-level goals. The paper also reports large-scale evaluation across 21,600 episodes. I did not fully audit the demonstration collection pipeline or every environment variation from the appendices.

### 5. How is it evaluated?
It is evaluated against eight baselines spanning VLA-style methods, end-to-end learned methods, and symbolic planning approaches. The key questions are whether the method outperforms these baselines on long-horizon tasks, whether it generalizes to longer horizons than those seen in training, whether it handles uncertainty and open-world settings, whether it is more efficient than planning or replanning baselines, and whether the learned high-level policy scales to very large numbers of relevant objects.

### 6. What are the main results?
From the accessible text, the headline result is that BISON generalizes to longer-horizon problems and to larger object counts than the VLA and end-to-end baselines on the extended MetaWorld benchmarks, while being more time- and memory-efficient in training and inference. The most striking claim is that, when low-level execution cost is ignored, the learned high-level symbolic policy can solve problems with 10,000 relevant objects in under a minute. I trust that result as a statement about symbolic policy scaling much more than as a statement about full embodied deployment, because the hard physical execution piece is factored out in that specific comparison.

### 7. What is actually novel?
The real novelty is not “symbols plus neural policy.” That story is old. The stronger contribution is to derive a learned high-level symbolic *policy* from abstracted demonstrations using goal regression and inductive generalization, rather than relying on classical search over a hand-authored planner. The other useful move is conditioning the low-level learned controller on explicit symbolic actions, which gives the interface between abstraction and execution a concrete computational role.

### 8. What are the strengths?
- The abstraction boundary is explicit instead of being implied by prompting rhetoric.
- The high-level policy is legible, inspectable, and combinatorially scalable in a way end-to-end policies usually are not.
- The low-level controller is compact rather than brute-force scaled.
- The design directly targets long-horizon and many-object generalization, which is where symbolic structure should help if it is doing real work.
- The paper is refreshingly honest that low-level imitation and high-level abstraction solve different problems.

### 9. What are the weaknesses, limitations, or red flags?
- The paper assumes a symbolic domain theory and a labeling function from low-level observations to symbolic states. That is a major part of the problem, and it is not solved here.
- The approach is less impressive if the abstraction interface has to be heavily hand-designed for every domain.
- The low-level policy is still behavior cloning, so robustness to serious off-demonstration dynamics may remain limited.
- The most dramatic scaling claim, 10,000 objects in under a minute, concerns the high-level symbolic policy in isolation rather than end-to-end embodied execution.
- Open-world and partial-observability claims depend heavily on how good the symbolic abstraction and observation labeling are in practice.

### 10. What challenges or open problems remain?
The hardest open problem is how to learn or maintain the labeling function and symbolic state abstraction from raw sensory input without hand engineering away the hard part. Another is how to keep the symbolic layer editable and trustworthy when the environment is partially observed, noisy, or semantically ambiguous. There is also the question of how to represent uncertainty at the symbolic layer instead of assuming clean abstract state transitions.

### 11. What future work naturally follows?
- Learn the abstraction and labeling function from perception rather than assuming them.
- Add explicit uncertainty and belief tracking at the symbolic layer.
- Replace pure behavior cloning at the low level with more robust closed-loop or generative action policies.
- Test whether the learned symbolic policy can coordinate richer memory, tool use, or multi-agent interaction.
- Explore how much of the symbolic domain theory can be induced rather than supplied.

### 12. Why does this matter for cabbageland?
Because it is a real example of using explicit symbolic state to carry long-horizon structure without pretending symbolic planning can do everything alone. It supports a design instinct cabbageland keeps returning to: typed interfaces between perception, memory, planning, and action are often more promising than stuffing all burdens into one latent policy and calling the residue “reasoning.”

### 13. What ideas are steal-worthy?
- Learn a high-level *policy* over symbolic state, not just a symbolic planner or verifier.
- Use goal regression over abstracted demonstrations to derive reusable condition-action structure.
- Condition low-level control explicitly on the chosen high-level symbolic action.
- Treat object-count generalization as a first-class reason to prefer symbolic or relational structure.
- Keep the low-level controller small when the symbolic layer already removes combinatorial burden.

### 14. Final decision
**Worth preserving.** This paper does not solve abstraction learning, which is the biggest catch, but it does give a cleaner and more serious blueprint for mixing symbolic long-horizon structure with learned low-level execution than most recent neurosymbolic branding exercises.
