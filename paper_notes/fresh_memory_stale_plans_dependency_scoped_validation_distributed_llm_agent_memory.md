# Fresh Memory, Stale Plans: Dependency-Scoped Validation for Distributed LLM-Agent Memory

## Basic info

* Title: Fresh Memory, Stale Plans: Dependency-Scoped Validation for Distributed LLM-Agent Memory
* Authors: Evan Chen, Shiqiang Wang, Christopher G. Brinton
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2609.03340
* Date surfaced: 2026-09-04
* Why selected in one sentence: It isolates stale-plan execution as a distinct failure mode and fixes it with explicit lineage checks at the action boundary.

## Quick verdict

* Must read

I inspected the full arXiv HTML text, especially the motivation and formulation sections, the PlanFence protocol, and the RQ1-RQ3 experiment results. This earns a preserved note because it identifies a concrete systems bug that a lot of agent-memory work hides under vaguer "freshness" language. The proposed fix is also refreshingly specific: bind plans to exact public inputs, validate only the dependencies that matter for the pending external action, replan once, then fail closed.

## One-paragraph overview

The paper studies distributed LLM-agent teams where planning and execution are separated across agents that share public state. The central failure is not that the executor has stale state. It is that the executor can hold fresh state while still issuing a tool call authorized by an older plan derived from superseded records. The paper calls this stale-plan execution and formalizes the needed invariant as lineage validity: the plan used at the tool boundary must still descend from the current public records that matter for that action. PlanFence implements this by recording exact parent records for a plan, declaring the action-relevant dependency set in the tool wrapper, checking those records with their owners just before the external call, and forcing one replan or a block if the lineage no longer matches.

## Model definition

### Inputs
The runtime consumes public record versions, a generated plan with exact cited parents, the dependency declaration for the pending protected action, and owner responses for the declared dependencies.

### Outputs
It outputs one of three outcomes at the action boundary: authorize the external action, trigger one replan and recheck, or block the action.

### Training objective (loss)
There is no new trainable model as the main contribution. The paper introduces a coordination and validation protocol around existing LLM agents rather than a learned predictor.

### Architecture / parameterization
PlanFence is a distributed action-validation protocol. The learned pieces remain ordinary LLM agents; the novelty is the explicit lineage record plus dependency-scoped authorization gate placed at the tool boundary.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
How do you prevent a distributed agent team from executing a tool action that was derived from superseded public inputs even when the executor already sees the newest shared state?

### 2. What is the method?
Record the exact public records a plan used, declare which of those records can affect a pending external action, validate those records with their owners just before execution, then either replan once or block if the lineage is invalid or incomplete.

### 3. What is the method motivation?
Fresh state is not the same as fresh authorization. Updating the executor's local copy does not rewrite the derivation that produced cached plan arguments, so an action can still be justified by obsolete evidence unless lineage is checked explicitly.

### 4. What data does it use?
The study uses five-agent Qwen3.5 workflows for reservation, fulfillment, and deployment tasks, 30 controlled live workflows with a post-plan revision, and controlled replay stress tests across different update rates, key counts, dependency widths, and network settings including an AT&T trace.

### 5. How is it evaluated?
The paper evaluates safety by counting invalid issued actions, plus availability, task completion, coordination stall, and distributed traffic. The evaluation is organized around RQ1-RQ3: stale-plan exposure, low-vs-high churn coordination choice, and dependency-scoped vs all-key validation.

### 6. What are the main results?
The safety result is the main punch. In 30 controlled live workflows, freshness-only execution issues an obsolete action in every task, while PlanFence completes all tasks without an invalid action. In replay, owner-head freshness still issues 330/330 invalid actions in the staged setting, while PlanFence issues 0/330. In the aligned larger audit, any method enforcing exact lineage records zero invalid actions across 32,700 scheduled actions. On systems cost, proactive synchronization has lower stall at low churn, but PlanFence has lower stall than the safe proactive alternatives once the update rate reaches rho >= 4 and also beats equally safe all-key validation as the shared keyspace grows.

### 7. What is actually novel?
The novelty is the stale-plan execution diagnosis itself, the lineage-validity formulation, and the action-boundary protocol that checks only the dependencies relevant to the pending external action rather than treating generic freshness as sufficient.

### 8. What are the strengths?
It separates the safety invariant from the coordination policy, uses a concrete protected-action boundary, and reports systems tradeoffs instead of pretending the safe method is free. The dependency-scoped design is especially strong because it avoids validating unrelated state.

### 9. What are the weaknesses, limitations, or red flags?
The experiments are controlled and relatively narrow in workflow type. Dependency declarations are explicit and therefore assume the wrapper authors know what matters for the action. The results say more about authorization safety and coordination cost than about broad downstream task capability.

### 10. What challenges or open problems remain?
The hard open problem is recovering the same safety invariant when dependency declarations are noisy, tool wrappers are incomplete, or the plan depends on more complex latent transformations than straightforward public-record ancestry.

### 11. What future work naturally follows?
Broader evaluation on coding, browser, and embodied agents; partial or learned dependency recovery; and tighter integration with memory systems that persist authorization lineage automatically.

### 12. Why does this matter for cabbageland?
Because cabbageland keeps caring about long-running tool-using agents that mutate state. This paper gives a clean answer to the question "how do we know the action is still authorized after the world changed?"

### 13. What ideas are steal-worthy?
Persist the public-input lineage of plans. Put a dependency-scoped validator at the external action boundary. Distinguish one replan from unbounded retry. Treat unrelated shared state as noise rather than something that must always sit on the critical path.

### 14. Final decision
Keep as a preserved note. This is one of the better recent agent-systems papers because it identifies a real failure mode, states the invariant precisely, and gives a practical protocol with meaningful cost tradeoffs.
