# Why Are GUI Agents Correct but Late? Decode on the Decision-Time Critical Path, Tested with Pre-Compiled Policy Trees

## Basic info

* Title: Why Are GUI Agents Correct but Late? Decode on the Decision-Time Critical Path, Tested with Pre-Compiled Policy Trees
* Authors: Zihan Dong, Rui Qian, Qishi Zhan, Dongshen Peng, Kaixin Li, Yu Li
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.28399
* Date surfaced: 2026-08-02
* Why selected in one sentence: It isolates a real computer-use-agent failure mode, decode latency on the decision-time critical path, and fixes it with a clean precompile-and-route systems trick instead of pretending better prompting will solve timing.

## Quick verdict

**Must read**

I inspected the arXiv HTML paper, especially the introduction, AAPT method, main results, oracle-routing analysis, and transfer discussion. This is one of the better agent systems papers in the recent batch because it asks a falsifiable causal question instead of just reporting another benchmark delta. The main limitation is clear in the paper's own results: the method shines when the right action family can be enumerated in advance and weakens when the interaction is late-bound or open-ended.

## One-paragraph overview

The paper argues that many GUI agents fail not because they misunderstand the interface, but because they spend too long decoding after the decisive event has already appeared. Its proposed fix, Adaptive Anticipatory Policy Trees (AAPT), uses idle time to precompile a bounded conditional action tree with observable guards, pre-authorized actions, and deadlines sized to the model's own latency. At event time, a lightweight observer routes the current screen to a prepared branch and executes immediately instead of generating a fresh long response. The result is not a new foundation model but a controlled systems intervention that shows timing on the critical path is itself a major failure source.

## Model definition

### Inputs
The system takes a task instruction, current GUI screenshots, change-gated runtime observations, and recent interaction context from a computer-use environment.

### Outputs
During preparation it emits a bounded conditional policy tree with branch guards, actions, and deadlines. During execution it emits a routed branch choice and the corresponding action.

### Training objective (loss)
There is no new model training objective at the core of the paper. AAPT wraps frozen multimodal models and changes when computation happens rather than retraining the base model.

### Architecture / parameterization
This is a systems wrapper around frozen multimodal GUI agents: a planner that precompiles a policy tree during idle time plus a lightweight observer/router that matches live frames to prepared branches.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the case where a GUI agent knows the right move but produces it too late for transient interface events such as short-lived dialogs, prompts, or reaction-time states.

### 2. What is the method?
The method is AAPT. During quiet periods, the same frozen model compiles a small conditional policy tree whose branches correspond to plausible future events. At runtime, a cheap observer routes incoming frames to a branch and fires the pre-authorized action without a fresh long decode.

### 3. What is the method motivation?
If expensive decoding remains on the decision-time critical path, better reasoning does not matter because the action lands after the window closes. The paper wants to separate "insufficient anticipation" from "computation placed in the wrong part of the pipeline."

### 4. What data does it use?
The main evaluation uses a contested-window GUI benchmark with paired trials, pre-registered seeds, and windowed transient events. It also includes replication on an independent multimodal model and transfer tests on DynaCU-Bench deadline-focused tasks.

### 5. How is it evaluated?
The evaluation is unusually disciplined for this kind of paper. It uses paired trials, pre-registered endpoints, exact McNemar tests, ablations on planning/routing/observer speed, an oracle-routing probe, and an external transfer benchmark.

### 6. What are the main results?
In the declared primary contested-window comparison, AAPT improves success from 0.50 to 0.79 with no incorrect actions. Baselines that still decode during execution fail to recover the window. The oracle-routing probe shows that perfect routing turns a tie into a significant win, which localizes branch routing as a real remaining bottleneck. On DynaCU-Bench transfer, AAPT matches a reactive baseline overall rather than dominating it, which cleanly marks the boundary of the method.

### 7. What is actually novel?
The novelty is not merely "do some planning ahead of time." The stronger move is using precompiled policy trees as a controlled intervention to isolate decode latency as a causal systems failure rather than blaming generic model weakness.

### 8. What are the strengths?
The paper asks a real causal question, uses pre-registered paired tests, gives a mechanism with clear failure boundaries, and resists the common temptation to overclaim transfer. The oracle-routing experiment is especially good because it identifies where the remaining gap actually lives.

### 9. What are the weaknesses, limitations, or red flags?
The method depends on pre-enumerable action branches and available idle time. It is less natural for late-bound interaction where the right action family is not known in advance. The benchmark is also deliberately deadline-heavy, so the measured effect size should not be read as a blanket statement about all GUI tasks.

### 10. What challenges or open problems remain?
The main open problem is handling richer branching without exploding tree size or routing error. More generally, the field still lacks a unified way to blend anticipatory execution with reactive replanning when the event space cannot be enumerated cheaply.

### 11. What future work naturally follows?
Distilled branch routers, learned guard matchers, hybrid anticipatory-reactive controllers, and broader task families where deadlines matter but branches are not easily enumerable would all be natural next steps.

### 12. Why does this matter for cabbageland?
It matters because cabbageland keeps touching computer-use agents and agent runtime design. The paper gives a reusable lesson: move expensive cognition off the critical path when the environment clock is the real enemy.

### 13. What ideas are steal-worthy?
Use idle periods to precompile bounded action contingencies. Size the preparation object against measured model latency instead of intuition. Use oracle-style ablations to distinguish a planning bottleneck from a routing bottleneck before rewriting the whole stack.

### 14. Final decision
**Keep it.** This is a direct and useful systems paper with a clear mechanism, a real causal claim, and failure boundaries explicit enough to reuse.
