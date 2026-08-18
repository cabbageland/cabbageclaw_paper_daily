# Quipu: A Governed Bitemporal Knowledge Graph Store

## Basic info

* Title: Quipu: A Governed Bitemporal Knowledge Graph Store
* Authors: Steve Brown
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.16813
* Date surfaced: 2026-08-18
* Why selected in one sentence: It moves governance inside the write path of agent-written knowledge instead of leaving it to after-the-fact dashboards and middleware.

## Quick verdict

* Highly relevant

I inspected the arXiv HTML full text. This is the most directly reusable paper in the batch because it encodes several strong design rules for agent-written memory: gate against the post-state, keep refusal verdicts, make rules bitemporal, and never let composition widen trust. The evidence is still somewhat self-contained, so I am not treating it as a solved substrate, but the architecture taste is very good.

## One-paragraph overview

Quipu is an embeddable knowledge-graph store built for agent-written facts rather than human-curated cleanup. It inverts four defaults the paper argues are jointly bad under agent workloads: accept-now-clean-later writes, single or missing time axes, flat trust, and governance that lives outside the data store. In Quipu, every governed write is staged against the pending post-state, accepted or denied by explicit predicates, and followed by a signed verdict fact that survives even if the write is rolled back. Data, trust labels, verdicts, and rules are bitemporal. Named graphs are the unit of authority, and graph composition follows a non-widening lattice. The evaluation uses a deterministic multi-writer lifecycle called Census plus an external evidence-sufficiency benchmark to argue that the store ends cleaner, replays decisions honestly as of their instant, and exports evidence that can be read without overclaim.

## Model definition

### Inputs
The system takes proposed fact deltas, graph and dataset membership, trust and authority labels, policy specifications, and audit queries over committed history.

### Outputs
It outputs either committed facts or refused writes, plus signed, time-indexed verdict facts and queryable audit records over the resulting store state.

### Training objective (loss)
There is no trainable model and no learning objective. Quipu is a governed data substrate with deterministic enforcement and audit logic.

### Architecture / parameterization
The architecture is a gated bitemporal graph store with named-graph authority, non-widening lattice composition, signed verdict permanence, and in-store governance facts whose audit reduces to a query over the same substrate.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve how to store agent-written knowledge without inheriting curation-era defaults that tolerate invalid writes, lose historical policy context, flatten trust, and externalize governance.

### 2. What is the method?
The method is a governed store design with post-state write gating, verdict permanence, bitemporal data and rules, partitioned authority at the graph level, and non-widening composition of graph views.

### 3. What is the method motivation?
If agents can write quickly and repeatedly, strictness becomes affordable precisely because the writer can absorb structured refusals and retry. That changes the tradeoff that made loose stores convenient for human workflows.

### 4. What data does it use?
It uses a deterministic seeded multi-writer lifecycle called Census, a small replay of five real Pre-Action Gate decisions from the Yupana stack, and a DEMM-style external evidence-sufficiency evaluation over exported decision records.

### 5. How is it evaluated?
It is evaluated against five research questions: enforcement cost, defect prevention versus an ungated control, audit decidability against an external checker, non-widening composition probes, and historical re-derivation of past decisions. It is also evaluated on exported evidence with overclaim and property sufficiency metrics.

### 6. What are the main results?
On the seeded Census run, the gated store ends with **0 of 6** planted defects versus **6 of 6** in the ungated control. All **7 of 7** composition probes uphold the lattice contract. It re-derives **50 of 50** satisfied verdicts as of their decision instant, while a latest-only rule set would misreport them. On the exported DEMM-style evidence, a property-level reader achieves **PSA 1.0** with zero overclaim and zero underclaim, while simple presence baselines overclaim on **75%** to **87.5%** of cases.

### 7. What is actually novel?
The novelty is not "AI-native graph store" branding. It is the combined architecture rule: governed post-state writes, verdict facts that survive rollback, bitemporal rules and evidence, graph-level authority that only narrows under composition, and an audit that is decidable from the store's own contents.

### 8. What are the strengths?
The design principles are crisp and taste-driven rather than decorative. The evaluation is deterministic, artifact-backed, and directly tied to the paper's research questions. The DEMM-style evidence analysis is especially useful because it attacks the common container fallacy: mistaking the presence of a trace or ledger for sufficient evidence.

### 9. What are the weaknesses, limitations, or red flags?
The main weakness is external validity. Census is synthetic by construction, and the real-world replay is only five decisions from the author's own stack. The benchmark regime added to DEMM is self-administered, so while the within-regime comparisons are informative, this is not the same as broad third-party validation. The paper also makes no throughput or query-performance claims.

### 10. What challenges or open problems remain?
The open problems are scaling the governed-store contract to more writers, more tasks, and more heterogeneous substrates, and testing whether the same strictness logic remains affordable outside the paper's own agent ecology.

### 11. What future work naturally follows?
Future work should run controlled multi-task agent experiments over several models and stacks, formalize the design principles as a portable governed-store specification, and benchmark other substrates against the same research questions.

### 12. Why does this matter for cabbageland?
Because cabbageland keeps running into exactly this boundary: if agents can write memory, then trust, time, and refusal evidence cannot stay implicit. Quipu gives a concrete substrate-level answer instead of another middleware sermon.

### 13. What ideas are steal-worthy?
Gate writes against the post-state, not the request alone. Keep signed verdict facts even when a write is denied. Make rules and verdicts bitemporal so historical audits are honest. Compose trust by a non-widening lattice so overlays cannot silently launder authority.

### 14. Final decision
Keep as a preserved note. Even if the specific implementation does not win, the architecture rules look durable and directly useful.

## 6. Mandatory critical angles

The paper is strongest on explicit state, decomposition, and controllability. It replaces "we logged it somewhere" with concrete governance primitives whose behavior can be queried. The main red flag is evaluation ecology: the strongest results come from a deterministic synthetic lifecycle and the author's own governed writer stack, so portability is still a live question.

## 7. Writing style

The right tone is sharply approving but not credulous. This is a serious design paper, not a settled standard.

## 8. Repository output format

Saved as a preserved paper note because the governed-memory substrate is directly relevant to agent-written knowledge, durable memory, and trustworthy audit trails.
