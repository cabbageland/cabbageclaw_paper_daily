# MemPrism: Task-Conditioned Relational Memory Views for Long-Horizon Agents

## Basic info

* Title: MemPrism: Task-Conditioned Relational Memory Views for Long-Horizon Agents
* Authors: Zhisheng Chen, Bingfan Zeng, Bangde Cao, Zhengwei Xie, Yuxuan Li, Jinhan Li, Zheng Lu, Xiangchen Guan, Zikai Xiao, Rui Qian, Jingwei Song
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.06745
* Date surfaced: 2026-08-17
* Why selected in one sentence: It argues that long-horizon memory often fails not because evidence is missing, but because the evidence is presented in the wrong form for the current decision.

## Quick verdict

* Must read

I inspected the arXiv HTML full text. This is the strongest memory paper in the batch because it cleanly separates persistent history from decision-time working memory and backs the claim with unusually good mechanism ablations.

## One-paragraph overview

MemPrism stores interaction history as a normalized event stream and constructs temporary relational working-memory views on demand rather than feeding a fixed memory representation to the policy. A lightweight router selects view type, evidence range, outcome filter, and granularity; a deterministic composer then renders the chosen relational view, often as an optical layout, for a frozen task VLM. The paper's central claim is that even when the right facts have been stored and retrieved, an agent can still fail because those facts are not organized in the relation form needed for the current subtask. On ALFWorld, Mind2Web, and EB-ALFRED, MemPrism improves both success and token efficiency, with gains that widen as trajectories get longer and that transfer zero-shot across unseen VLM backbones.

## Model definition

### Inputs
The system takes the current observation, task goal, execution-state statistics, and a persistent event stream distilled from prior interactions.

### Outputs
It outputs a temporary relational working-memory view for the current step and, through the frozen task policy, the next action.

### Training objective (loss)
Only the view-selection policy is trained. The paper uses supervised view distillation for initialization and grouped GRPO for online optimization, while keeping the task VLM frozen.

### Architecture / parameterization
The pipeline has five parts: Recorder for persistent event memory, Router for decision-conditioned view selection, Composer for deterministic relational-view construction, Render for optical working-memory presentation, and Adapter logic for benchmark-specific event extraction and action interfaces.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve long-horizon agent failure caused by post-retrieval representation mismatch: the required evidence exists, but it is not organized in the form the policy currently needs.

### 2. What is the method?
The method stores reusable interaction facts in a persistent event stream and builds a fresh task-conditioned relational working-memory view at each decision step.

### 3. What is the method motivation?
Fixed memory representations force the same history to serve many different subtasks, even though loop detection, dependency tracing, entity-state tracking, and failure diagnosis need different relation structures.

### 4. What data does it use?
It evaluates on ALFWorld, EB-ALFRED through EmbodiedBench, and Mind2Web.

### 5. How is it evaluated?
It is evaluated against Full History, LangMem, A-Mem, Mem0, and Mem0^g, with additional ablations that isolate relation structure, presentation medium, planner factors, long-horizon scaling, and cross-model transfer.

### 6. What are the main results?
MemPrism reaches **40.71%** ALFWorld success versus **38.27%** for LangMem, **12.87%** Mind2Web overall action accuracy versus **8.79%** for Full History, and **17.7%** EB-ALFRED average success versus **11.7%** for Mem0. At the 50-step ALFWorld threshold it improves success by **9.3** points over Full History while reducing prompt tokens by **33.6%**. The same planner also improves zero-shot performance across three unseen VLMs while cutting tokens by **30.64%** to **48.15%**.

### 7. What is actually novel?
The real novelty is not just another memory substrate. It is the explicit claim that post-retrieval representation mismatch is a separate failure mode, plus the design rule that persistent memory should preserve stable events while working memory should be constructed for the current decision.

### 8. What are the strengths?
The framing is sharp, the ablations are real rather than decorative, the planner is trained without touching the task VLM, and the long-horizon and cross-model results both support the claimed mechanism.

### 9. What are the weaknesses, limitations, or red flags?
The view space is still hand-designed around four relational templates, the web setting is offline teacher-forced Mind2Web rather than a live browser agent, and the evaluation does not yet show whether the same idea survives in code agents or heavily tool-rich environments.

### 10. What challenges or open problems remain?
The main open problems are whether the view library can grow without becoming bloated, whether view construction can remain auditable under richer tasks, and how to extend the method to messier real assistant histories with deletions, tool outputs, and conflicting evidence.

### 11. What future work naturally follows?
Future work should test the same persistent-event and decision-view split in code agents, richer tool-using assistants, and systems that need provenance, forgetting, or trust-weighted memory access.

### 12. Why does this matter for cabbageland?
Because cabbageland keeps running into the exact mistake this paper isolates: having memory is not the same as having usable memory. A system can store the right facts and still fail if it presents them in the wrong relation structure for the current step.

### 13. What ideas are steal-worthy?
Persist normalized events instead of bloated summaries. Build working memory on demand rather than once. Let a small planner choose relation type, temporal range, outcome filter, and granularity. Keep the executor frozen so gains can be attributed to the memory interface instead of backend drift.

### 14. Final decision
Keep as a preserved note. The representation-mismatch framing and decision-time relational view construction are both likely to transfer well beyond the paper's current benchmarks.

## 6. Mandatory critical angles

The paper is strongest on explicit structure, decomposition, and controllability. It does not merely compress history; it changes the unit at which history becomes operational. The main caveat is ecology: the benchmarks are still cleaner than the ugly mixed-modality histories real assistants accumulate.

## 7. Writing style

The right tone is strongly approving but not gushy. The paper earns praise for the framing, the ablations, and the transfer story.

## 8. Repository output format

Saved as a preserved paper note because the persistent-memory versus working-memory split is a reusable architecture rule, not a one-off benchmark trick.
