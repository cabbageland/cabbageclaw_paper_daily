# WikiSkill: Compiling Agent Experience into Persistent Knowledge for Skill Evolution

## Basic info

* Title: WikiSkill: Compiling Agent Experience into Persistent Knowledge for Skill Evolution
* Authors: Liyan Tang, Cyrus Rashtchian, Chun-Sung Ferng, Andrew Tomkins, Da-Cheng Juan, Tu Vu
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.27454
* Date surfaced: 2026-08-28
* Why selected in one sentence: It cleanly separates raw agent traces, persistent knowledge, and executable skills, then shows that the middle layer materially improves skill evolution.

## Quick verdict

* Highly relevant

I inspected the full arXiv HTML text, especially the three-layer workspace design, the orchestration loop, the transfer results, and the ablations about the persistent wiki. This paper earns a preserved note because it takes a vague "agent memory helps skill evolution" idea and turns it into an explicit intermediate object that persists, compounds, and transfers.

## One-paragraph overview

WikiSkill is a framework for evolving filesystem-style agent skills using a persistent wiki layer that sits between raw execution traces and active skills. Each iteration runs an inference agent on tasks using the current skills, a Wiki Maintainer consolidates what happened into structured knowledge, a Skill Proposer uses that wiki plus the new traces to propose skill updates, and a validation gate keeps or rolls back skill edits. The important asymmetry is that skills can be rolled back while the wiki persists, so later updates can build on accumulated knowledge rather than relearning the same lesson from scratch.

## Model definition

### Inputs
Execution traces from agent rollouts, the current persistent wiki, the active skill set, benchmark tasks, and validation outcomes.

### Outputs
Updated wiki pages, updated skill modules, and validation-selected skill states for the next iteration.

### Training objective (loss)
There is no model-weight training claim in the main method. The loop optimizes skill evolution through iterative rollouts, wiki updates, and validation-gated skill edits.

### Architecture / parameterization
A three-layer workspace: immutable raw traces, a persistent wiki layer for accumulated knowledge, and a skill layer with executable modules. The loop uses an inference agent, a wiki maintainer, a skill proposer, and a gating/rollback mechanism.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to make agent skill evolution compound over time instead of repeatedly mining isolated optimization artifacts.

### 2. What is the method?
The method introduces a persistent knowledge base that continuously consolidates agent experience and then informs later skill proposals.

### 3. What is the method motivation?
If useful lessons remain scattered across trajectories, rejected proposals, and old edits, later skill updates cannot systematically reuse them. A dedicated wiki layer should support compounding.

### 4. What data does it use?
The paper evaluates across LiveMathematicanBench, SealQA, SpreadSheetBench, OfficeQA, and ALFWorld, using Qwen, Gemma, and Gemini-family models.

### 5. How is it evaluated?
It compares against no-skill and several skill-evolution baselines, studies scaling interaction inside the Qwen family, and tests cross-model skill transfer.

### 6. What are the main results?
WikiSkill outperforms existing skill-evolution baselines across models and tasks. Within the Qwen family, average gains are 12.3%, 17.5%, and 23.9% for the 4B, 9B, and 27B models. Qwen-3.5-9B with WikiSkill reaches 47.4% average accuracy, beating Qwen-3.6-27B without skills at 39.4%. Transfer can beat self-evolution: for example, Qwen-3.5-9B reaches 70.2% on ALFWorld with a Qwen-3.6-27B-evolved skill versus 63.4% with its own.

### 7. What is actually novel?
The novelty is the explicit three-layer separation and the persistence asymmetry: traces are immutable, skills are revisable, but the wiki keeps compounding across iterations.

### 8. What are the strengths?
The representation choice is clear, the results are broad rather than single-benchmark, and the transfer findings suggest that knowledge discovery and knowledge execution are distinct agent capabilities.

### 9. What are the weaknesses, limitations, or red flags?
The setting is still benchmark-centered and mostly about skill modules rather than fully open-ended long-horizon deployment. The paper also does not prove that every wiki page is high quality; it shows usefulness through downstream validation.

### 10. What challenges or open problems remain?
It remains unclear how wiki curation scales when tasks, tools, and environments become much noisier, or when multiple agents write conflicting lessons into shared memory.

### 11. What future work naturally follows?
Structured memory conflict resolution, better skill provenance, and more explicit policies for promoting wiki knowledge into reusable tools or contracts all follow naturally.

### 12. Why does this matter for cabbageland?
Because cabbageland keeps caring about explicit memory and reusable structure. This paper makes a persuasive case that the thing between raw traces and executable skills should itself be a maintained object.

### 13. What ideas are steal-worthy?
Separate raw traces from accumulated knowledge and from executable skills. Let skills roll back while knowledge persists. Treat cross-model transfer as a way to distinguish skill discovery from skill execution.

### 14. Final decision
Keep as a preserved note. This is one of the better recent papers on agent skill evolution because it gives persistent knowledge a concrete role instead of using "memory" as a fog word.

## 6. Mandatory critical angles

The paper is strongest on explicit structure and compounding knowledge. It is not a full theory of agent memory, but it does show that a maintained intermediate object can materially improve iterative skill development. That is enough to keep.

## 7. Writing style

The tone should be approving but selective. Emphasize the structural separation and the transfer result rather than turning it into a general triumphalist memory paper.

## 8. Repository output format

Saved as a preserved paper note because the trace/wiki/skill split is a durable idea for agent memory and skill pipelines.
