# Beyond Retrieval: Query-Conditioned Reuse of Long-Horizon Agent Trajectories

## Basic info

* Title: Beyond Retrieval: Query-Conditioned Reuse of Long-Horizon Agent Trajectories
* Authors: Yifei Li, Heng Wang, Lingling Zhang, Muye Huang, Xinyu Zhang, Jiashuai Liu, Hang Yan, Rongman Xu
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.12847
* Date surfaced: 2026-08-15
* Why selected in one sentence: It cleanly separates memory retrieval from memory usefulness and shows that long-horizon experience needs target-bound reuse rather than raw replay.

## Quick verdict

* Must read

I inspected the arXiv HTML full text. This is the most useful paper in the batch because it defines the right evaluation boundary for agent memory instead of hiding retrieval, selection, and reuse inside one blended score.

## One-paragraph overview

The paper studies what happens after a memory system has already found a relevant long-horizon trajectory. It builds a frozen bank of **623** verified historical trajectories and creates **2,391** target tasks across WebArena, WorkArena, and AppWorld whose workflows remain reusable while bindings like entity, file, date, or state change. The key method is Query-Conditioned Reuse (QCR): instead of injecting the raw selected trajectory, it writes a small target-bound support object with four fields, namely the workflow invariant, bindings to re-obtain, applicability conditions, and a verification guardrail. On the shared selected-memory setup, QCR reaches **62.3%** average success, beating Full Trajectory by **10.7** points while using **48.9%** fewer online tokens.

## Model definition

### Inputs
The reuse pipeline takes a target natural-language query, the target's initial observation, and one ranker-selected historical trajectory from a frozen memory bank.

### Outputs
It outputs a target-bound support object for the acting agent and then a new target trajectory whose final state is checked by the target environment's verifier.

### Training objective (loss)
There is no new trained memory model in the paper. The contribution is an evaluation framework and a support-writing procedure over a fixed retriever, fixed selector, and fixed acting model.

### Architecture / parameterization
The system is a frozen agent-memory pipeline: a unified bank of verified source trajectories, an embedding retriever that returns top-5 candidates, a lightweight ranker that selects one record, and one of three delivery modes to the actor: Generic Summary, Full Trajectory, or the four-field QCR support object.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the gap between retrieving a relevant long-horizon trajectory and actually using that trajectory safely on a new task whose bindings and state have changed.

### 2. What is the method?
The method freezes candidate retrieval and single-memory selection, then compares how the same selected experience is used at execution time. QCR rewrites the selected trajectory into four compact target-bound fields rather than handing the actor the raw trace.

### 3. What is the method motivation?
Long-horizon trajectories can encode a valuable workflow, but they also carry stale users, file paths, parameters, observations, and failed branches. Retrieval alone does not tell the actor what still transfers.

### 4. What data does it use?
It uses a unified memory bank of **623** verifier-approved historical trajectories and a benchmark of **2,391** binding-shifted target tasks derived from WebArena, WorkArena, and AppWorld.

### 5. How is it evaluated?
It is evaluated with a frozen-retrieval protocol that keeps candidate retrieval, selected trajectory, acting model, decoding, tool budget, and verifier fixed across methods. Metrics are verified Success, Milestone completion, API calls, and non-overlapping online token cost, plus analyses by selected-memory length and source-target binding shift.

### 6. What are the main results?
QCR reaches **62.3%** average Success, which is **10.7** points above Full Trajectory, while cutting online tokens by **48.9%** and using fewer API calls. The reranker selects a reusable memory for **94.8%** of targets, and end-task success lands only **1.8** points below an oracle reusable selector.

### 7. What is actually novel?
The novelty is the framing. The paper isolates post-retrieval reuse as its own measurable bottleneck and defines a sharp accounting boundary where different support objects can be compared fairly.

### 8. What are the strengths?
The design is disciplined. Retrieval and selection are held fixed, the benchmark uses executable verifiers, and the main improvement is both stronger and cheaper than raw trajectory injection.

### 9. What are the weaknesses, limitations, or red flags?
The setup uses verified successful source trajectories, a single selected memory, and controlled binding shifts. It does not yet cover naturally accumulated memory stores, partial failures, multi-memory composition, or open-ended memory acquisition.

### 10. What challenges or open problems remain?
The open problems are how to learn reuse policies, how to compose multiple memories safely, and how to keep provenance-rich storage without polluting the actor with stale source state.

### 11. What future work naturally follows?
Future work should test learned support writers, stronger retrievers under the same accounting boundary, multi-memory composition, and broader task histories with naturally recurring failures and retries.

### 12. Why does this matter for cabbageland?
Because cabbageland keeps running into the exact distinction this paper names: what should be preserved in storage is not the same as what should be injected into the acting context. This is a reusable design rule for memory systems.

### 13. What ideas are steal-worthy?
Separate retrieval quality from reuse quality. Preserve rich trajectories offline, but give the actor a compact target-bound procedure plus explicit bindings-to-recover and verification obligations. Evaluate memory after retrieval, not only at retrieval.

### 14. Final decision
Keep as a preserved note. This is a real baseline-setting paper for long-horizon agent memory rather than a decorative memory prompt tweak.

## 6. Mandatory critical angles

The paper is strongest on decomposition, controllability, and evaluation fairness. Its key move is not a larger memory bank but a cleaner operational boundary. The main missing piece is broader ecological realism around how memory stores and failures accumulate over time.

## 7. Writing style

The right tone is sharply approving. The paper earns credit by refusing to pretend that a retrieved trajectory is automatically useful just because it looks relevant.

## 8. Repository output format

Saved as a preserved paper note because the reuse framing, benchmark boundary, and support-schema idea are all likely to be useful later.
