# Harness Continual Learning: Continual Adaptation Beyond Model Parameters

## Basic info

* Title: Harness Continual Learning: Continual Adaptation Beyond Model Parameters
* Authors: Borui Kang, Jinrui Gu, Junhan Lv, Wenbin Li, Lei Wang, Yang Gao
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.19013
* Date surfaced: 2026-08-23
* Why selected in one sentence: It is the clearest recent paper on treating the agent harness itself as the learned state that can improve, drift, and forget.

## Quick verdict

* Highly relevant

I inspected the arXiv HTML full text, especially the HCL formalization, the four harness components, the guarded-evolution mechanism, and the ALFWorld, Minecraft, textual-reasoning, and multimodal experiments. This paper earns a preserved note because it names a real agent problem cleanly: a frozen foundation model can still "learn" through prompts, memories, tools, skills, and routing rules, and those harness edits can forget earlier behavior just as brutally as weight updates do. The framework is not fully mature, but the object of learning is exactly right.

## One-paragraph overview

The paper argues that modern agents adapt through more than model parameters. They also adapt through the surrounding harness: input interfaces, persistent memory, executable capabilities, and routing policies. Because those artifacts persist and evolve across interactions, they can accumulate capability but also silently break earlier behavior. The paper formalizes this as Harness Continual Learning (HCL), where the evolving state is the joint harness around a frozen model. It instantiates that state with four components, then introduces guarded harness evolution: a Continual Optimizer proposes candidate harness updates from feedback, and a Continual Evaluator commits them only if they satisfy current-improvement, historical-retention, and validity checks.

## Model definition

### Inputs
Current interaction data, persistent harness state, post-execution feedback, historical anchor cases, retention budgets, and validity checks.

### Outputs
Updated harness state, agent answers or actions produced with that harness, and acceptance or rejection decisions for candidate harness revisions.

### Training objective (loss)
There is no single end-to-end learned model with one scalar loss. HCL is an update-and-commit framework that seeks current-task improvement while constraining historical retention and validity before adopting a new harness state.

### Architecture / parameterization
Hybrid agent framework around a frozen foundation model. The learned state is decomposed into Task Interface, Experience Memory, Capability Map, and Adaptive Router, with a Continual Optimizer generating candidate revisions and a Continual Evaluator acting as the retention-and-validity gate.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve continual adaptation for agents whose effective behavior changes through harness edits even when the underlying foundation model is frozen.

### 2. What is the method?
The method is HCL: define harness state as the joint object of continual learning, then update it through guarded harness evolution. Each candidate harness is proposed from feedback and committed only if it improves current performance while staying within historical-loss and validity constraints.

### 3. What is the method motivation?
Agent behavior depends on prompts, memory contents, tool and skill interfaces, and routing logic. Updating those artifacts can help current tasks but also destroy previously working behaviors, creating a retention problem that model-centric continual learning does not describe well.

### 4. What data does it use?
The paper evaluates HCL in two open-world interaction settings, ALFWorld and Minecraft, plus controlled task streams for textual reasoning and multimodal perception. The textual-reasoning stream uses DeepSeek-V4-Flash as the frozen model, while multimodal perception and Minecraft use Qwen3.6-27B and some ablations use Qwen3.5 variants.

### 5. How is it evaluated?
Evaluation separates open-world capability accumulation from controlled forgetting analysis. The paper measures current performance, historical retention, and validity across ALFWorld, Minecraft, textual-reasoning streams, and multimodal streams, then studies how different retention budgets change the stability-plasticity trade-off.

### 6. What are the main results?
Across multiple settings, HCL reports relative gains above 10% over corresponding baselines. In ALFWorld, the stability-oriented profile reaches 61.74% with lower average forgetting than the adaptive baselines it compares against. In the controlled textual-reasoning stream, relaxing the retention budget raises final average performance from 52.20% to 64.70% while introducing only 0.07 average forgetting. The multimodal results show a similar retention-plasticity trade-off, with stricter retention reducing forgetting and looser retention improving final average performance.

### 7. What is actually novel?
The real novelty is the shift in the learning object. Instead of treating prompts, memory, tools, and routing as incidental scaffolding around a frozen model, the paper treats them as the actual mutable state of continual learning and defines forgetting at that harness level.

### 8. What are the strengths?
The paper names a real systems phenomenon instead of forcing everything back into parameter updates. The four-component decomposition is concrete enough to think with, and the guarded commit logic is a useful design principle even if one never copies the full framework.

### 9. What are the weaknesses, limitations, or red flags?
This is still a framework paper with hand-designed boundaries between components. The update generator is not yet a polished or universal mechanism. And some reported gains depend on evaluation configurations and retention budgets that may need careful retuning in new domains.

### 10. What challenges or open problems remain?
The hard problem is making harness evolution robust in real multi-tool agents where feedback is noisy, capability maps are large, memory updates are lossy, and validity checks are expensive or incomplete.

### 11. What future work naturally follows?
Apply the same framework to coding agents and long-lived tool-use systems, study automatic harness-diff generation, and learn stronger retention tests that detect when a seemingly local harness edit damages a distant workflow.

### 12. Why does this matter for cabbageland?
Because cabbageland is exactly the kind of system where the harness is a real learned object: prompts, skills, memory, and routing all change behavior. This paper gives a vocabulary and a control principle for that reality instead of pretending the frozen base model is the only thing that matters.

### 13. What ideas are steal-worthy?
Treat prompts, memory, capabilities, and routing as jointly versioned state. Separate candidate generation from commitment. Make historical retention an explicit admissibility gate. Evaluate harness evolution on both open-world accumulation and controlled forgetting streams.

### 14. Final decision
Keep as a preserved note. The framework is not final, but the object it identifies is exactly the right one.

## 6. Mandatory critical angles

The paper is strongest on explicit state, decomposition, controllability, and long-horizon failure analysis. It earns the continual-learning label because it defines a real retention problem over mutable harness artifacts rather than only over weights. The main caution is maturity: the framework is ahead of the evidence in some places.

## 7. Writing style

The right tone is warm but skeptical. The paper deserves credit for naming the right thing, while still needing harder deployment evidence.

## 8. Repository output format

Saved as a preserved paper note because the harness-as-state framing is likely to matter across many future agent systems.
