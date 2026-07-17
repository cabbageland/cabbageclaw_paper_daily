# SearchOS-V1: Towards Robust Open-Domain Information-Seeking Agent Collaboration

## Basic info

* Title: SearchOS-V1: Towards Robust Open-Domain Information-Seeking Agent Collaboration
* Authors: Yuyao Zhang, Junjie Gao, Zhengxian Wu, Jiaming Fan, Jin Zhang, Shihan Ma, Yao Yao, Weiran Qi, Chuyan Jin, Guiyu Ma, Xingzhong Xu, Kai Yang, Ji-Rong Wen, Zhicheng Dou
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.15257
* Date surfaced: 2026-07-17
* Why selected in one sentence: It turns long-horizon search progress into explicit shared state with measurable gains on completeness-sensitive benchmarks.

## Quick verdict

**Must read**

This is one of the better recent agent systems papers because the mechanism is not decorative. SearchOS externalizes what search agents usually keep as fragile prompt residue: what remains to do, which evidence supports which claim, where coverage gaps still exist, and which search paths already failed. I inspected the full arXiv HTML paper, including the problem formulation, SOCM design, middleware details, main results, ablations, and case studies.

## One-paragraph overview

The paper reformulates open-domain information seeking as relational schema completion with grounded citations, then builds a multi-agent system around that framing. Instead of letting agents infer progress from long chat histories, SearchOS maintains explicit shared state through four objects: a Frontier Task list, an Evidence Graph, a Coverage Map, and a Failure Memory. A central orchestrator decomposes unresolved gaps, dispatches worker agents in a pipeline-parallel way, and uses middleware to inject state, extract evidence, enforce budgets, and detect stalled trajectories. The result is a search stack that treats provenance, coverage, and failure recovery as system invariants rather than prompt conventions.

## Model definition

### Inputs
The system takes an open-domain information-seeking query, the evolving relational schema, current SOCM state, retrieved web pages, and tool outputs from browser and search actions.

### Outputs
It produces populated tables or lists with grounded citations, plus intermediate artifacts such as task decompositions, evidence nodes, coverage updates, and failure-memory entries.

### Training objective (loss)
The paper does not introduce a new learned objective. SearchOS is a system-level prompting and orchestration framework built on top of existing LLM agents and tools.

### Architecture / parameterization
SearchOS uses a planner-orchestrator plus specialized explore, search, and writer agents. The load-bearing design pieces are Search-Oriented Context Management (Frontier Task, Evidence Graph, Coverage Map, Failure Memory), a Search Tool Middleware Harness, and a hierarchical skill system separating strategy skills from source-specific access skills.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to stop long-horizon search agents from losing track of progress, repeating dead ends, and leaving coverage holes when the search process gets too long for implicit conversational memory.

### 2. What is the method?
The method is to cast the task as relational schema completion with grounded citations, maintain explicit shared search state through SOCM, schedule worker agents with continuous pipeline dispatch, and enforce execution invariants through middleware rather than agent self-discipline.

### 3. What is the method motivation?
Search state is too important to leave inside transient chat context. If provenance, coverage, and failures matter, they should be represented directly and updated atomically.

### 4. What data does it use?
The main evaluations are on WideSearch and GISA, both structured information-seeking benchmarks where answers can be graded for item-level and row-level completeness.

### 5. How is it evaluated?
The paper compares SearchOS against ReAct, Plan-and-Solve, Table-as-Search, A-MapReduce, and Web2BigTable. Metrics are item-level and row-level precision, recall, and F1 on WideSearch, plus F1 and exact-match variants across question types on GISA. The paper also runs schema-planning and scheduling ablations.

### 6. What are the main results?
On WideSearch, SearchOS reaches `80.3` item-level F1 versus `76.0` for the strongest baseline, and `56.5` row-level F1 versus `54.5`. On GISA set questions it reaches `76.5` F1 versus `63.1`, a `+13.4` gain. The scheduling ablation is also real rather than cosmetic: continuous dispatch reduces average end-to-end time from `629.13s` to `476.34s`, improves slot utilization from `34.6%` to `41.7%`, uses fewer LLM calls, and raises item F1 from `79.66` to `86.75` on the paired WideSearch study.

### 7. What is actually novel?
The novelty is not "many agents search the web." The novelty is making search progress itself explicit and shareable through Frontier Tasks, Evidence Graphs, Coverage Maps, and Failure Memory, then letting middleware govern those objects as part of execution.

### 8. What are the strengths?
The mechanism is concrete, the recall-heavy gains match the claimed design benefit, and the ablations support the story. It also has better taste than many search-agent papers because provenance and coverage are first-class objects instead of post hoc traces.

### 9. What are the weaknesses, limitations, or red flags?
The task framing is still structured table completion with grounded citations, which is cleaner than messy open-ended research synthesis. Some of the gains may depend on how naturally the benchmark matches the schema-completion formulation. It is also a fairly heavy harness-engineering solution rather than a minimal model change.

### 10. What challenges or open problems remain?
The hard question is whether the same explicit-state design scales to noisier research tasks where the right schema is unstable, evidence is conflicting, and the final product is not a table but a synthesis or argument.

### 11. What future work naturally follows?
Natural next steps are broader open-ended tasks, lighter-weight versions of the same state machinery, and systems that learn when to revise schema structure instead of only filling it.

### 12. Why does this matter for cabbageland?
Cabbageland cares about long-horizon agents that track state instead of faking continuity through prompt length. SearchOS offers a clean architecture pattern for evidence-grounded search, explicit coverage accounting, and persistent failure memory.

### 13. What ideas are steal-worthy?
Use an explicit frontier task queue for unresolved coverage gaps. Keep provenance in an evidence graph instead of burying it in chat turns. Track failure memory so dead-end access patterns are not rediscovered every run. Put state injection and stall detection in middleware rather than relying on the model to remember its own operating rules.

### 14. Final decision
**Keep it.** This is a strong systems paper with a mechanism worth reusing.
