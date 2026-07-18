# Proof-or-Stop: Don't Trust the Agent, Trust the Evidence -- Loop Engineering for Verifiable Evidence-Gated Lifecycle Control

## Basic info

* Title: Proof-or-Stop: Don't Trust the Agent, Trust the Evidence -- Loop Engineering for Verifiable Evidence-Gated Lifecycle Control
* Authors: Jek Huang, Jeffery Hsia, Jiayi Sun, Freddie Shi, Wei Huang, Ian H. White
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.14890
* Date surfaced: 2026-07-18
* Why selected in one sentence: It turns coding-agent lifecycle state into an evidence-admission problem instead of trusting the agent's own narration of completion.

## Quick verdict

**Must read**

This is one of the cleaner recent agent-control papers because it is explicit about what it does and does not prove. The contribution is not a better coding model; it is a host-neutral control layer that blocks lifecycle advancement unless fresh, code-bound evidence satisfies the gate. I inspected the full arXiv HTML paper, including the abstract, lifecycle mechanism, powered ablation, recovery section, self-application audit, and threats-to-validity discussion.

## One-paragraph overview

The paper proposes Proof-or-Stop Lifecycle Control, a discipline for autonomous coding systems where outputs like "reviewed," "tested," and "done" are treated as claims that need admissible evidence rather than as trustworthy state transitions. The system binds receipts to tracked source state, checks freshness and integrity, and either advances, repairs, escalates, or stops. The evidence-gated loop is then evaluated through mechanism tests, a pre-registered ablation over weaker control regimes, injected-failure recovery tests, and a self-application corpus from the system's own development.

## Model definition

### Inputs
The system takes lifecycle claims, tracked source state, review outputs, test receipts, hashes, metadata, and other machine-checkable evidence artifacts produced during coding-agent execution.

### Outputs
It outputs lifecycle admission decisions such as advance, repair, escalate, block, or stop, plus structured evidence records and receipts bound to the relevant code state.

### Training objective (loss)
The paper does not introduce a learned training objective. Proof-or-Stop is a control framework and execution discipline around coding agents rather than a new trainable model.

### Architecture / parameterization
The architecture is a host-neutral evidence-gated lifecycle loop: plan, execute, review, bounded reflection, gate, and done. The load-bearing pieces are tracked-source-state binding, freshness checks, authenticated receipts, and lifecycle gates that decide whether claims are admissible.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to stop autonomous coding systems from converting unsupported self-reports into lifecycle truth, especially when "done" can be claimed before evidence is fresh, complete, or actually bound to the code about to ship.

### 2. What is the method?
The method is evidence-gated lifecycle control: agent outputs are treated as claims, and lifecycle transitions are admitted only when fresh, tracked-source-state-bound evidence satisfies the gate predicate.

### 3. What is the method motivation?
In agentic software work, a passing-looking log or an agent saying "tests passed" is not enough. The paper argues that the missing control is claim admissibility, not another model.

### 4. What data does it use?
The evaluation uses a mechanism-test suite, a pre-registered powered ablation with `9,240` cells over `24` tasks and multiple control arms, injected-failure recovery scenarios, and a self-application corpus of `565` development stories and `1007` review findings.

### 5. How is it evaluated?
It is evaluated with engine-contract tests, tamper-resistance checks for receipt bundles, a multi-arm control-policy ablation against weaker loops, injected-failure recovery comparisons, and a self-hosted audit corpus.

### 6. What are the main results?
The unattended-loop engine passes `10/10` contract scenarios with zero false-done, and local-key receipt bundles reject `18` tamper classes with zero false accepts in the tested suite. In the powered ablation, visible-pass/hidden-fail amplification drops from `31/1800` under the compute-budgeted naive loop to `2/1800` under the evidence-gated loop. The self-application corpus contains `565` stories, `1007` review findings, and a `94.8%` resolution rate.

### 7. What is actually novel?
The novelty is the semantic shift: agent output may propose lifecycle state, but it is not itself lifecycle state. The system forces downstream automation to decide based on admissible evidence instead of trusting the producing agent.

### 8. What are the strengths?
The claim boundary is honest, the control mechanism is concrete, and the paper actually runs comparative ablations instead of stopping at conceptual rhetoric. The self-application audit is also more useful than the average "we use our own system" anecdote because it is tied to evidence and review findings.

### 9. What are the weaknesses, limitations, or red flags?
The paper is still evaluating one self-hosted system, one model family, and a self-built corpus. Cross-vendor review is selectively invoked rather than unbiased, and some labels in the audit corpus rely on reviewer judgement rather than external ground truth.

### 10. What challenges or open problems remain?
The open problem is generalization: how much of the gain survives different model families, different hosts, noisier software tasks, and less curated development loops.

### 11. What future work naturally follows?
The obvious next steps are larger powered recovery studies, unbiased cross-vendor review-rate estimation, and broader real-work measurements of how often visible-pass/hidden-fail states occur outside injected scenarios.

### 12. Why does this matter for cabbageland?
Cabbageland cares about coding agents, workflow integrity, and explicit state over vibe-based continuity. This paper offers a reusable discipline for deciding when an agent claim is safe for the rest of the system to act on.

### 13. What ideas are steal-worthy?
Treat agent outputs as proposals, not state. Bind every consequential receipt to concrete source state. Fail closed on stale or unsupported evidence. Separate "review exists" from "review is admissible for this code snapshot."

### 14. Final decision
**Keep it.** The mechanism is worth remembering, and the paper is disciplined enough not to oversell what it proved.
