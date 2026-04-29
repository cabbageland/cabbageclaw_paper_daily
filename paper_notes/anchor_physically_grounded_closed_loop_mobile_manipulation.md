# ANCHOR: A Physically Grounded Closed-Loop Framework for Robust Home-Service Mobile Manipulation

## Basic info

* Title: ANCHOR: A Physically Grounded Closed-Loop Framework for Robust Home-Service Mobile Manipulation
* Authors: Jinhao Jiang, Shengyu Fang, Sibo Zuo, Yujie Tang, and Yirui Li
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2604.25323
* Date surfaced: 2026-04-29
* Why selected in one sentence: It is a decent systems paper on forcing symbolic mobile-manipulation plans to stay tied to continuously revalidated physical state instead of stale semantic assumptions.

## Quick verdict

**Useful**

This is not a deep learned-model paper, but it is a fairly honest systems paper about a real failure mode. Its best move is to frame open-vocabulary mobile manipulation as a state-consistency problem between symbolic planning and the evolving physical world, then add structured recovery instead of global thrashing. I inspected the abstract and substantial method text from the arXiv HTML, so confidence is good on the pipeline and claims, but I did not audit every implementation detail or all appendices.

## One-paragraph overview

ANCHOR is a modular home-service mobile-manipulation stack designed for disturbed, previously unseen environments. Instead of trusting a prebuilt semantic scene representation, it continually rebuilds a physically anchored world state from current RGB-D observations, uses that state to populate symbolic predicates for PDDL planning, refines navigation endpoints based on downstream manipulation feasibility, and escalates recovery only at the minimum responsible layer. The core idea is simple and sensible: keep the plan grounded in geometric evidence, not just in the last symbolic story you told yourself.

## Model definition

### Inputs
The framework takes a natural-language task instruction, RGB-D observations, robot state, occupancy maps, segmented object evidence, and geometric relations that support predicates such as near, aligned, holding, and in.

### Outputs
The high-level stack outputs symbolic plans, navigation endpoint refinements, and low-level action invocations such as find, align, grasp, and place.

### Training objective (loss)
The accessible text does not present a central learnable model with a single training loss for the overall framework. The key contribution is systems integration around physical anchoring, PDDL planning, and reachability-aware execution constraints.

### Architecture / parameterization
A hybrid modular stack: online scene graph and occupancy maintenance, LLM-generated problem PDDL, classical planning with Fast Downward, operability-aware base alignment using a reachability-shell surrogate, and hierarchical recovery across perception, base-arm coordination, and execution layers.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Open-vocabulary mobile-manipulation systems often fail not because the language side misunderstood the task, but because symbolic plans drift away from the real physical state. Pre-scanned maps go stale, navigation stops at positions that are geometrically reachable but useless for manipulation, and failures trigger blunt global replanning rather than localized repair.

### 2. What is the method?
- Build a physically anchored world state from online RGB-D observations.
- Derive symbolic predicates only from observable geometric evidence.
- Use an LLM to generate a constrained problem PDDL and a classical planner to produce candidate action sequences.
- Re-plan in receding-horizon style after each executed step.
- Refine base poses with operability-aware alignment so the arm can actually work from the chosen endpoint.
- Handle failures with a minimum-responsible-layer hierarchy instead of immediately triggering full replanning.

### 3. What is the method motivation?
The motivation is that long-horizon mobile manipulation breaks when the symbolic interface lies. If the planner keeps reasoning over stale or weakly grounded predicates, the robot accumulates errors until it reaches an inoperable state. The paper wants a tighter contract between plan symbols and physical evidence.

### 4. What data does it use?
The visible text reports 60 real-robot trials in previously unseen environments, including perturbation scenarios. I did not inspect the appendices in full, so I am not claiming more granular dataset breakdowns than that.

### 5. How is it evaluated?
The system is evaluated on real-robot task success and perturbation recovery, with comparisons against a weaker baseline mobile-manipulation stack. The evaluation focuses on execution robustness rather than just one-shot semantic grounding.

### 6. What are the main results?
The visible text reports task success improving from 53.3 percent to 71.7 percent and a 71.4 percent recovery rate under perturbations. I trust the direction of the improvement more than I trust any uninspected edge-case accounting.

### 7. What is actually novel?
The novelty is not any one component alone. The interesting contribution is the combined contract: symbolic predicates must stay physically anchored, navigation endpoints must satisfy manipulation operability, and recovery should be localized by responsible layer. That is a more disciplined systems decomposition than a generic VLM planner loop.

### 8. What are the strengths?
- It targets real deployment failure modes rather than benchmark theater.
- The physical anchoring idea is conceptually clean.
- It treats navigation and manipulation consistency as a first-class issue.
- The layered recovery scheme is more realistic than blind retry or full replan everything.

### 9. What are the weaknesses, limitations, or red flags?
- The system is fairly hand-built and domain-structured.
- Predicate definitions and thresholds may be brittle under broader variation.
- The state is only as good as the underlying perception pipeline.
- It is more a robustness engineering paper than a new learning mechanism.
- There is some risk that the reported success comes partly from careful domain scoping rather than broad generality.

### 10. What challenges or open problems remain?
Scaling this style of physical anchoring to richer tasks will require more expressive relational state, uncertainty handling, and better ways to reason about partial observability. The framework also still depends on reliable geometric sensing and heuristic thresholds.

### 11. What future work naturally follows?
- Add explicit uncertainty estimates to predicate grounding.
- Learn better recovery policies while preserving the minimum-layer discipline.
- Replace some threshold heuristics with calibrated learned detectors.
- Extend the anchored state to more temporal and causal relations, not just current geometry.

### 12. Why does this matter for cabbageland?
Because it is a useful reminder that many “reasoning” failures are really interface failures. Cabbageland cares about explicit state, legible decomposition, and not letting symbolic plans float free from the world. This paper is rough but aligned with that taste.

### 13. What ideas are steal-worthy?
- Treat symbolic predicates as contracts backed by observable evidence.
- Re-plan only after re-anchoring world state, not by trusting predicted symbolic effects.
- Make base-pose selection answer to downstream manipulation feasibility.
- Localize recovery to the smallest failing layer instead of escalating immediately.

### 14. Final decision
**Keep it, but as a systems note rather than a core architecture paper.** The main value is the interface discipline between symbolic plans and physical execution, not some deep new model class.