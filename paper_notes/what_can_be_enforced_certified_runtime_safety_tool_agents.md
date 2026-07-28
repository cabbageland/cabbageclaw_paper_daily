# What Can Be Enforced? A Theory of Certified Runtime Safety for Tool-Using Agents

## Basic info

* Title: What Can Be Enforced? A Theory of Certified Runtime Safety for Tool-Using Agents
* Authors: Shawn Ray
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.22868
* Date surfaced: 2026-07-28
* Why selected in one sentence: It is a useful standards paper because it separates three things that guardrail discussions keep collapsing into one blob.

## Quick verdict

**Highly relevant**

This paper is more valuable as a framework than as a deployment recipe, but the framework is badly needed. Its main contribution is not another guardrail stack. It is a clean separation between symbolic enforceability, exogenous judge calibration, and endogenous closed-loop intervention effects. I inspected the arXiv HTML abstract, introduction, results summary, related-work framing, and the enforcement-model sections that define the paper's regimes.

## One-paragraph overview

The paper studies runtime guardrails for tool-using agents and asks what such systems can actually guarantee. It argues that three distinct questions are usually mixed together. First, given oracle predicates and a bounded policy-state representation, what safety policies are even enforceable? Second, if a judge is fallible but the environment is exogenous, what false-block versus miss frontier can calibration achieve? Third, if blocking changes the agent's future proposals, what matters is a closed-loop controlled model rather than a static ROC curve. The result is a regime map: some claims are symbolic, some are statistical, and some require modeling the intervention feedback loop explicitly.

## Model definition

### Inputs
The framework takes structured tool actions, safety predicates or judge scores, the gate's internal state representation, and in the controlled case a model of how intervention changes future proposals.

### Outputs
It outputs allow or block decisions, symbolic enforceability characterizations, calibrated risk frontiers, and closed-loop occupancy-based safety tradeoffs under explicit assumptions.

### Training objective (loss)
There is no new trainable model in the core contribution. The paper contributes theoretical characterizations, calibration analysis, and controlled-model optimization.

### Architecture / parameterization
The method is a hybrid symbolic and probabilistic analysis of runtime gates: register-like state for enforceability, Neyman-Pearson and conformal calibration for exogenous judging, and occupancy-program analysis for closed-loop intervention.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to clarify what runtime guardrails for tool-using agents can actually guarantee and where those guarantees break.

### 2. What is the method?
The method is to split the problem into enforceability, calibration, and feedback-control regimes, then characterize each regime with the appropriate mathematics rather than a single catch-all story.

### 3. What is the method motivation?
Most guardrail claims quietly jump between symbolic rules, empirical judge scores, and behavior under intervention without admitting that those are different objects.

### 4. What data does it use?
The paper is primarily theoretical, but it supports the theory with static diagnostics, finite controlled examples, representation rewrites, and paired closed-loop reruns.

### 5. How is it evaluated?
It is evaluated by proving characterization results, analyzing decidability boundaries, deriving calibrated frontiers, and running targeted experiments that isolate the claimed distinctions.

### 6. What are the main results?
The paper shows which nonempty safety policies deterministic gates can enforce relative to their register model, shows a separable monotone fragment that stays in PSPACE while richer counter systems become undecidable, and shows that exogenous calibration does not identify the closed-loop frontier once blocking changes future behavior.

### 7. What is actually novel?
The novelty is the regime-correct composition. The paper's main contribution is the line it draws between symbolic enforcement, statistical calibration, and endogenous control.

### 8. What are the strengths?
It is conceptually clean, names common category errors directly, and should improve how future guardrail papers state their guarantees.

### 9. What are the weaknesses, limitations, or red flags?
The guarantees are assumption-heavy. Some results can degenerate to block-all, and the closed-loop analysis depends on an explicit finite controlled model that many practical systems will not have.

### 10. What challenges or open problems remain?
The big open problem is how to get useful closed-loop guarantees without requiring an unrealistically neat model of the intervention dynamics.

### 11. What future work naturally follows?
Build guardrail evaluations that report which regime they inhabit, study richer but still tractable policy representations, and connect occupancy-style analysis to more realistic agent workflows.

### 12. Why does this matter for cabbageland?
Cabbageland cares about tool use, verification, and not lying to itself about safety. This paper is useful because it helps separate real guarantees from statistical cosmetics.

### 13. What ideas are steal-worthy?
State guarantees by regime. Do not use static judge calibration as a proxy for closed-loop safety. Treat the gate's representational power as part of the safety claim, not an implementation detail.

### 14. Final decision
**Keep as a standards and framing paper.** It is not the whole answer, but it gives a much better checklist for what future guardrail claims should have to specify.

