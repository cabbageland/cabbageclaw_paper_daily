# From Faulty Memories to Corrected Actions: Dependency-Guided Rollback Repair for Memory-Augmented Agents

## Basic info

* Title: From Faulty Memories to Corrected Actions: Dependency-Guided Rollback Repair for Memory-Augmented Agents
* Authors: Caili Yu, Yiqi Wang, Jiaqi Zhang, Yiqun Duan, Mingkai Zheng, Zhangkai Wu, Kaize Shi, Taotao Cai
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.10502
* Date surfaced: 2026-08-12
* Why selected in one sentence: It treats persistent-memory failure as a downstream state-repair problem instead of pretending that deleting a bad memory or rewriting the last answer is enough.

## Quick verdict

* Must read direct paper

I inspected the arXiv HTML full text. This is one of the better recent agent-memory papers because it attacks the right boundary. The main insight is blunt and correct: fault removal is not state recovery.

## One-paragraph overview

The paper studies what should happen after a memory-augmented agent has already consumed a bad memory and produced a failed execution. Instead of deleting the source or restarting from scratch, it builds a typed memory-to-action graph from runtime provenance, traces downstream dependencies, checks which affected nodes still have independent trusted support, plans a rollback over the unsupported state, and selectively replays only the answer-relevant affected computation. On a 150-case controlled benchmark across shopping, travel, and customer-support tools, the method reaches 85.3% recovery versus 77.3% for the strongest competing repair baseline while preserving all benign memories and removing all diagnosed faulty ones. On an adapted 50-case LongMemEval-V2 subset it reaches 68.0% recovery versus 54.0% for the next best method.

## Model definition

### Inputs
The framework takes a failed user session, an active memory store, the failed execution trace, runtime provenance linking memory reads to claims, plans, actions, and writes, plus diagnosed faulty memory identifiers from an upstream detector.

### Outputs
It outputs a corrected answer, a repaired execution trace, and a repaired active memory state.

### Training objective (loss)
There is no model-training objective in the main contribution. This is a runtime repair and evaluation framework.

### Architecture / parameterization
The method has four main pieces: a typed memory-to-action dependency graph, downstream tracing from diagnosed faults, independent-support checking to avoid over-invalidation, and a rollback planner plus selective replay executor.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to recover both answer quality and persistent state after faulty memories have already propagated through an agent's reasoning and actions.

### 2. What is the method?
The method constructs a typed provenance graph, traces the affected downstream subgraph of a diagnosed memory fault, preserves nodes with independent trusted support, invalidates unsupported descendants, and selectively replays only the answer-relevant affected computation.

### 3. What is the method motivation?
Persistent memory failures are not local. Once a bad record has changed claims, tool calls, answers, or later memory writes, deleting the original record or revising only the final answer leaves contaminated state behind.

### 4. What data does it use?
It uses a 150-case controlled benchmark spanning shopping, travel, and customer-support tool-use domains with four fault types, plus a 50-case adapted subset of LongMemEval-V2 for external stress testing.

### 5. How is it evaluated?
It measures recovery, recurrence, faulty-memory removal, benign-memory preservation, claim invalidation F1, replay ratio, and LLM-call cost against memory-centric and trace-centric repair baselines.

### 6. What are the main results?
On the controlled benchmark the method reaches 85.3% recovery versus 77.3% for LLM-judge repair and 60.7% for AgentTrace-style repair, while removing all faulty memories and preserving all benign memories. On the adapted subset it reaches 68.0% recovery versus 54.0% for the next best method and the highest claim invalidation F1, 0.669.

### 7. What is actually novel?
The novelty is the formulation of post-failure memory recovery as joint answer repair plus persistent-state repair, with explicit dependency tracing, independent-support checks, and answer-relevant replay.

### 8. What are the strengths?
The paper has the right failure boundary, a clear typed provenance contract, sensible cost-aware evaluation, and a real distinction between preserving benign state and merely repairing the final output.

### 9. What are the weaknesses, limitations, or red flags?
The method assumes an upstream fault diagnosis, so it does not solve detection. The benchmark is still controlled and synthetic, recurrence is not the best among all baselines, and the results depend on sufficiently complete runtime provenance.

### 10. What challenges or open problems remain?
The biggest open problems are realistic fault diagnosis, more natural long-horizon benchmarks, partial or noisy provenance, and deciding how much replay is worth paying for under real latency constraints.

### 11. What future work naturally follows?
Joint detection-and-repair systems, typed memory schemas designed for rollback, provenance-aware runtime logging, and broader evaluation on real assistants or coding agents all follow naturally.

### 12. Why does this matter for cabbageland?
Cabbageland keeps building and thinking about systems with persistent memory. This paper says the important thing cleanly: once memory writes become durable, repair has to reason over state lineage, not just over the last answer text.

### 13. What ideas are steal-worthy?
Treat memory faults as typed dependency contamination. Preserve nodes with independent support instead of deleting everything downstream. Use answer-relevant selective replay instead of full recomputation.

### 14. Final decision
Keep as a preserved note. The framing is directly reusable for memory-equipped assistants, and the recovery-versus-cost evaluation is better than the usual vague "self-correcting agent" story.

## 6. Mandatory critical angles

This paper is strongest on problem framing and repair boundary choice. The main caution is that it assumes fault diagnosis and structured provenance, so the contribution is most immediately valuable as a design target for agent runtimes rather than a drop-in end-to-end cure.

## 7. Writing style

The right tone is strongly favorable and exact. The paper deserves credit for naming the real problem, but it should not be exaggerated into a complete memory-safety solution.

## 8. Repository output format

Saved as a preserved paper note because post-failure memory recovery is a reusable systems concept, and the selective rollback pattern is worth keeping nearby.
