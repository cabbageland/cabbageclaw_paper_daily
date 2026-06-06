# What Should Agents Say? Action-state Communication for Efficient Multi-Agent Systems

## Basic info

* Title: What Should Agents Say? Action-state Communication for Efficient Multi-Agent Systems
* Authors: Chen Huang, Yuhao Wu, and Wenxuan Zhang
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.05304
* Date surfaced: 2026-06-06
* Why selected in one sentence: It gives a compact public-state contract for multi-agent systems: pass action, grounded state, and result instead of dumping private reasoning into shared history.

## Quick verdict

**Highly relevant**

This is a small paper with an unusually stealable systems idea. I inspected the arXiv PDF, including the diagnostic communication strategies, PACT definition, benchmark tables, ablation, coding-harness port, and limitations. Confidence is high on the mechanism and practical relevance, though the method is intentionally narrow: it targets systems where repeated shared history is a major source of cost and confusion.

## One-paragraph overview

PACT argues that multi-agent systems have over-focused on roles, schedules, and topologies while leaving the inter-agent message itself as unconstrained natural language. The paper compares common strategies such as full content, concise generation, conclusion only, brief summary, and artifact only. The diagnostic result is that no fixed compression strategy is universally best, but useful messages tend to preserve action-centered information. PACT turns that into a protocol: before a sender's output enters shared history, it is projected into an action-state record with ACTION, STATE, and RESULT fields. The agent can still reason privately; only the public handoff is disciplined.

## Model definition

### Inputs

At each turn, an agent receives its local observation, role or action, and shared history. It produces a raw output, which PACT then projects before appending to shared history.

### Outputs

PACT outputs a compact public message containing the action taken or requested, the grounding state or evidence, and the result that downstream agents need.

### Training objective (loss)

PACT is training-free. It is a communication protocol or proxy hook over the public history, not a learned compressor.

### Architecture / parameterization

The protocol defines a sender-side projection into three fields: ACTION, STATE, and RESULT. In production coding harnesses, the authors implement it as a proxy hook that keeps summary blocks, tool calls, and tool results while removing intermediate free-form assistant content from prior turns.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Multi-agent LLM systems often let full natural-language outputs accumulate in shared history. Downstream agents repeatedly process redundant reasoning traces, restatements, and noisy deliberation, which inflates token cost and can degrade performance.

### 2. What is the method?

- Let agents reason and act normally.
- Before a non-terminal agent output becomes public shared history, project it into an action-state message.
- Preserve only ACTION, STATE, and RESULT.
- Drop private deliberation, redundant explanation, and process-level content.
- Apply the same principle to controlled multi-agent benchmarks and to coding agents through a proxy hook.

### 3. What is the method motivation?

The paper's real insight is that communication length is not the only issue. The public trace should say what changed in the task state and what downstream agents should use, not expose all private computation that produced the change.

### 4. What data does it use?

The controlled experiments use HotpotQA and 2WikiMultiHopQA for split-evidence interaction, plus AIME2024, AIME2025, GPQA-Diamond, and OpenBookQA for a sequential pipeline. The coding-harness experiments use SWE-bench Verified with OpenHands and SWE-agent.

### 5. How is it evaluated?

The paper reports F1 for split-evidence QA, exact-match accuracy for pipeline tasks, average total tokens per problem, ablations over the ACTION/STATE/RESULT fields, and SWE-bench Verified resolve rates plus token cost for coding harnesses.

### 6. What are the main results?

In controlled multi-agent settings, PACT generally improves or preserves task performance while using fewer tokens. In the four-agent pipeline, it uses only about 19% to 23% of Multi-Agent Debate's tokens while matching or beating mean accuracy. In coding harnesses, PACT improves OpenHands SWE-bench Verified resolved instances from 97 to 115 out of 500 while reducing tokens per resolved by 10.3%. In SWE-agent, it reduces input tokens from 314.6M to 156.0M and tokens per resolved by about 47%, with a small resolve-rate drop from 25.6% to 24.2%.

### 7. What is actually novel?

The novelty is the communication invariant. PACT defines what is allowed into public shared history, rather than changing agent roles, adding debate rounds, or training a summarizer.

### 8. What are the strengths?

- Extremely simple and portable.
- Separates private computation from public state.
- The ablation supports the three-field design: removing ACTION or STATE hurts, and RESULT-only messages become ambiguous.
- The coding-harness port shows the idea is not limited to toy multi-agent scaffolds.

### 9. What are the weaknesses, limitations, or red flags?

- It assumes shared conversational history is a major cost source; systems with short interactions or different state stores may benefit less.
- The experiments do not cover all forms of open-ended debate, tool-heavy planning, or dynamically routed multi-agent systems.
- A bad projection can drop information that later agents actually need.
- The paper does not solve deeper questions of belief conflict, uncertainty, or provenance beyond the compact state field.

### 10. What challenges or open problems remain?

The open problem is adaptive public-state design. ACTION/STATE/RESULT is a good minimum, but complex agent systems may need uncertainty, dependencies, invalidated assumptions, or explicit branch/revision markers.

### 11. What future work naturally follows?

- Combine PACT-style public messages with MAGE-style execution-state trees.
- Add provenance and confidence fields for tool-heavy workflows.
- Learn or verify projection quality without exposing private reasoning.
- Test the protocol in dynamic agent networks where receivers are not fixed in advance.

### 12. Why does this matter for cabbageland?

Because it gives an immediate design rule for agent systems: public traces should be state updates, not diaries. That is directly relevant to long-horizon tool agents, coding agents, memory systems, and OpenClaw-style orchestration.

### 13. What ideas are steal-worthy?

- Keep private reasoning private; expose only public action-state updates.
- Make handoff records grounded: action, state/evidence, result.
- Treat shared history as a constrained state channel, not a transcript dump.
- Use projection hooks around existing agents instead of rewriting the agent loop.

### 14. Final decision

**Worth keeping.** PACT is not a grand theory of multi-agent intelligence, and that is a virtue. It is a clean state-interface rule that will probably save real systems from a lot of self-inflicted context sludge.
