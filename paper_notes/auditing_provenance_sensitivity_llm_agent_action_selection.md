# Auditing Provenance Sensitivity in LLM Agent Action Selection

## Basic info

* Title: Auditing Provenance Sensitivity in LLM Agent Action Selection
* Authors: Junchi Liao
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.20827
* Date surfaced: 2026-07-24
* Why selected in one sentence: It turns "did the agent act correctly?" into the harder question "was the evidence that determined the action actually authorized to determine it?"

## Quick verdict

**Highly relevant**

This is a better agent-evaluation paper than the average tool benchmark because it fixes task, proposition, and policy, then changes only source authority. That makes the failure mode legible instead of hand-wavy. I inspected the arXiv PDF sections covering the abstract, introduction, target-specific audit method, matched source interventions, controlled degradation setup, experiments, limitations, and conclusion.

## One-paragraph overview

The paper studies tool-using agents that act on a mix of user instructions, trusted tool outputs, memory, retrieved records, and untrusted text. A final action can be correct while still being influenced by evidence that was not authorized to determine that tool choice or argument. The proposed audit decomposes the context into semantic factors and labels each factor separately for each target as valid, invalid, or neutral under an explicit application policy. It then runs matched interventions where only the source authority of a proposition changes, controlled degradations where valid evidence is removed while invalid competition remains, and coalition-based interaction diagnostics over partial evidence. The goal is not merely to find wrong actions, but to locate where provenance controls fail even when outcomes still look acceptable.

## Model definition

### Inputs
The audit takes a fixed action interface, a task prompt, decomposed context factors, an application-level authorization policy, and a specific target such as a tool name or argument value.

### Outputs
It outputs target-score changes, paired action discordance rates, degradation patterns, and interaction summaries that indicate whether unauthorized evidence influenced the audited decision target.

### Training objective (loss)
There is no new trainable model. The paper audits existing open-weight LLM agents with deterministic prompt interventions and score comparisons.

### Architecture / parameterization
The contribution is an evaluation protocol: target-specific authorization labeling, matched trusted/untrusted source swaps, mixed/full/clean degradation comparisons, and Harsanyi/Shapley-style partial-evidence interaction analysis.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to detect whether an agent's action selection is improperly influenced by unauthorized evidence sources even when the resulting action may still be correct.

### 2. What is the method?
The method labels each context factor per action target, runs matched source-authority interventions, removes valid evidence while keeping invalid competitors, and uses partial-evidence interactions as a secondary localization diagnostic.

### 3. What is the method motivation?
Standard outcome evaluation cannot tell whether the action was grounded in the right evidence. Correctness can mask brittle dependence on stale memory, neighboring records, or untrusted text.

### 4. What data does it use?
The evaluation uses `450` controlled next-action tasks drawn from authored workflow tasks, Tau2-style tasks, and BFCL examples.

### 5. How is it evaluated?
It is evaluated by comparing target scores and parsed actions under source-matched prompts, by degradation tests over full/mixed/clean evidence settings, and by coalition interaction summaries over controlled context subsets.

### 6. What are the main results?
Across multiple open-weight model families, changing only source authority alters generated actions in `5.4%` of competing cases versus `1.7%` of supporting cases. In the controlled degradation test, the strict full-correct / mixed-error / clean-correct pattern appears in `2.4%` of comparisons with a `95%` confidence interval of about `[2.1, 3.0]`. The models clearly respond to source-authority cues, but not enough to isolate their actions from unauthorized evidence.

### 7. What is actually novel?
The novelty is the target-specific authorization framing. The audit does not treat provenance as a generic prompt-injection story. It asks which sources are permitted to determine each exact tool or argument target.

### 8. What are the strengths?
It cleanly separates tool choice from argument choice, changes only source authority in its primary intervention, and is unusually explicit about what its degradation pattern can and cannot prove.

### 9. What are the weaknesses, limitations, or red flags?
The trusted versus untrusted source distinction is still conveyed through textual prompt framing rather than a full operational provenance stack. The task family is next-action centric, and the interaction analysis is a stress diagnostic rather than a causal proof.

### 10. What challenges or open problems remain?
A big open problem is moving from prompt-level authority markers to end-to-end provenance channels enforced through actual tool, memory, and retrieval infrastructure.

### 11. What future work naturally follows?
Use the audit on real agent runtimes with structured provenance, extend it to multi-step trajectories, and couple it with runtime guards that can block action components whose determining evidence is unauthorized.

### 12. Why does this matter for cabbageland?
Cabbageland cares about tool use that is not only effective but governable. This paper gives a practical audit for whether the action channel is being steered by the right evidence.

### 13. What ideas are steal-worthy?
Label evidence per target, not per prompt. Run source-matched interventions that keep proposition content fixed. Use full/mixed/clean degradation to expose retained unauthorized competition. Treat partial-evidence interactions as diagnostics, not automatic guilt.

### 14. Final decision
**Keep it.** This is one of the better recent papers on turning evidence authorization into a concrete agent-audit problem.
