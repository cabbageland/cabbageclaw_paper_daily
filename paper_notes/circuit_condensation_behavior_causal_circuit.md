# Circuit Condensation: Post-Training that Concentrates a Behavior's Causal Circuit

## Basic info

* Title: Circuit Condensation: Post-Training that Concentrates a Behavior's Causal Circuit
* Authors: Sai Adith Senthil Kumar
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.27254
* Date surfaced: 2026-08-30
* Why selected in one sentence: It treats circuit legibility as a trainable property and makes exhaustive circuit verification feasible instead of aspirational.

## Quick verdict

* Must read

I inspected the full arXiv HTML text, especially the method loop, the cross-model reduction results, the IOI anchor analysis, and the limitations. This earns a preserved note because it does not merely search harder for a smaller explanation of behavior in a frozen model. It changes the model so the causal graph carrying that behavior becomes smaller, then checks whether that payoff still describes the original model well enough to matter.

## One-paragraph overview

The paper proposes Circuit Condensation, a post-training procedure for concentrating a target behavior into a smaller causal circuit. Each round ranks surviving edges by causal importance, prunes the weakest ones, trains only a low-rank adapter to reproduce the original model through the retained graph, and keeps the cut only if both the target behavior and general capability survive on held-out data. The payoff is practical rather than aesthetic: once the circuit gets small enough, exhaustive subset tests, pairwise interaction checks, and stronger necessity claims become computationally tractable. Across four behaviors and eight models, the method usually beats frozen circuit discovery by a large margin and often preserves much closer agreement with the original model than a size-matched frozen baseline.

## Model definition

### Inputs
Prompt tokens for the target behavior, clean and corrupted examples for causal attribution, and the current circuit graph over model components and edges.

### Outputs
The model still emits ordinary next-token predictions, but the procedure additionally returns a reduced circuit graph intended to carry the target behavior with minimal retained structure.

### Training objective (loss)
The paper trains a low-rank adapter to match the original model's outputs while preserving the target behavior through the retained circuit. Cuts are accepted only if held-out task performance and a general-capability gate both survive; otherwise the prior state is restored.

### Architecture / parameterization
A pretrained language model is paired with an iterative controller that ranks causal edges, prunes them, and heals the surviving graph using a low-rank adapter. The core architecture is therefore a frozen base model plus adapter-based post-training under repeated causal pruning.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Frozen circuit discovery often returns circuits so large that they are hard to inspect, compare, or verify exhaustively. The paper wants circuits small enough that stronger claims about necessity and interaction become testable.

### 2. What is the method?
The method alternates four steps: rank edges by causal importance, prune the weakest edges, train an adapter to recover the original behavior through what remains, and accept or reject the cut based on held-out behavior and capability checks.

### 3. What is the method motivation?
Searching a fixed model better may still leave the behavior distributed across a large graph. If interpretability payoff depends on tractable verification, then moving the behavior into a smaller circuit can be more useful than freezing the model and hoping search quality improves.

### 4. What data does it use?
The paper evaluates four behaviors across eight models from four families, plus a detailed indirect-object-identification anchor where prior circuit roles are already documented. It also uses held-out data for acceptance decisions and for checks against the original model.

### 5. How is it evaluated?
It compares retained circuit size against frozen baselines, measures whether the target behavior survives, checks general-capability retention, tests agreement with the original model's outputs, and uses exhaustive subset and pairwise ablations when the resulting circuit is small enough.

### 6. What are the main results?
Condensed circuits are smaller than the strongest frozen baseline in 30 of 32 settings, by 8.1x on average and up to 316x. Repeating the same search without weight updates loses in 29 of 32 settings, which shows the payoff comes from reshaping the model rather than from a better search alone. On the IOI anchor, the condensed circuit keeps 24 heads, 17 with documented roles, versus 61 heads and 36 undocumented ones for the matched frozen circuit. Agreement with the original model remains fairly strong, with median choice agreement of 96.5% and median token-level KL of 0.215 across the full grid.

### 7. What is actually novel?
The real novelty is the stance that circuit findability is trainable. That is stronger than another pruning heuristic on a frozen model.

### 8. What are the strengths?
The method is conceptually clean, the empirical comparison against frozen and frozen-weight controls is strong, and the paper cashes out interpretability with harder tests rather than with nicer pictures. The IOI anchor analysis is especially persuasive because it connects the reduced circuit to an already studied mechanism.

### 9. What are the weaknesses, limitations, or red flags?
The reduced circuit first explains the adapted network, not automatically the original model. The behaviors studied are still a limited set, and the capability gate is not equally strict across model families. The paper also notes cases where a simpler baseline can return smaller circuits and cases where the payoff does not extend cleanly.

### 10. What challenges or open problems remain?
The big open question is whether this scales to richer behaviors and larger models without collapsing the capability gate or introducing new distortions. Another challenge is deciding which behaviors are stable enough targets for condensation in the first place.

### 11. What future work naturally follows?
Apply the procedure to more realistic multi-step behaviors, strengthen the capability-preservation criteria, and test whether condensed circuits remain legible under distribution shift or across languages and domains.

### 12. Why does this matter for cabbageland?
Because cabbageland keeps preferring explicit mechanisms that can actually be checked. This paper turns that preference into a method: if the circuit is too big to verify, train until the behavior fits somewhere smaller.

### 13. What ideas are steal-worthy?
Treat legibility as an optimization target. Use accept-or-restore control instead of monotone pruning. Judge an interpretability method partly by whether it makes exhaustive verification newly affordable.

### 14. Final decision
Keep as a preserved note. This is a real mechanism paper with durable ideas for interpretable structure rather than another giant-circuit description exercise.

## 6. Mandatory critical angles

The paper is strongest on mechanism, decomposition, and transferability of the core idea. It explicitly distinguishes search quality from representational reshaping and provides controls that make that distinction believable. Interpretability here is not just descriptive; it is operationalized as whether the graph is small enough to run stronger tests. The main fragility is that condensation modifies the model, so the explanation relation to the original network has to be re-earned rather than assumed.

## 7. Writing style

The note should stay blunt and anti-mystical. The good part of this paper is that it refuses to romanticize giant circuits.

## 8. Repository output format

Saved as a preserved paper note because the trainable-findability idea is exactly the kind of reusable research move the repo should keep.
