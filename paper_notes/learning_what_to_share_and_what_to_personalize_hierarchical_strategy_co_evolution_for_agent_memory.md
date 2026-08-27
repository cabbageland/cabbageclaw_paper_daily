# Learning What to Share and What to Personalize: Hierarchical Strategy Co-Evolution for Agent Memory

## Basic info

* Title: Learning What to Share and What to Personalize: Hierarchical Strategy Co-Evolution for Agent Memory
* Authors: Yupeng Han, Shuochen Liu, Kai Zhang, Ze Liu, Zhihong Pan, Xianquan Wang
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.25329
* Date surfaced: 2026-08-27
* Why selected in one sentence: It is the strongest memory-specific paper in the batch on separating shared memory rules from user-specific ones and letting that boundary evolve with evidence.

## Quick verdict

* Highly relevant

I inspected the full arXiv HTML text, especially the method sections on universal strategy distillation, persona delta distillation, and cross-level rule flow, plus the benchmark table, ablations, and cross-model transfer results. This paper earns a preserved note because it makes memory policy explicit instead of burying it in vague retrieval or generic RL updates. The central question is real: what should every user share, what should stay personalized, and how do you keep that split from fossilizing?

## One-paragraph overview

HiPS treats memory management as a hierarchical strategy problem rather than a fixed retrieval heuristic. It maintains a universal strategy `S_u` for cross-user rules and a persona-specific delta `Delta_p` for users whose behavior diverges from the population norm. Universal Strategy Distillation updates the shared rules by contrasting high- and low-reward traces, Persona Delta Distillation writes behavior-level exceptions for divergent users, and Cross-Level Rule Flow can promote a local rule upward or specialize a universal rule downward. The policy then injects a budgeted subset of those rules into the prompt and is optimized with a combined answer-plus-adherence reward. The attractive part is not just better scores. It is that the boundary between shared and personalized memory is treated as a first-class object.

## Model definition

### Inputs
Long dialogue histories, retrieved memory candidates, a user identity or persona context, and the currently active universal plus persona-specific memory-management rules.

### Outputs
Updated memory trajectories, selected strategy rules injected into the prompt, and final task responses on personalized dialogue benchmarks.

### Training objective (loss)
The policy is optimized with GRPO using a combined reward `R_ans + lambda * R_follow`, where `R_follow` measures compliance with the active strategy rules. Strategy refinement itself is done through LLM-based distillation over trajectories rather than through a direct gradient loss on a rule model.

### Architecture / parameterization
An external-memory personalized agent built around a backbone LLM with four main components: Universal Strategy Distillation, Persona Delta Distillation, divergence-gated personalization, and Cross-Level Rule Flow, plus budgeted submodular rule selection at inference.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the fact that most memory agents use either one global memory policy for everyone or fully ad hoc personalization, even though some rules are universally good and others are clearly user-specific.

### 2. What is the method?
The method learns a shared rule set for cross-user memory behavior, learns persona-specific deltas for users whose behavior deviates from those rules, and migrates rules between the two levels based on accumulated evidence. A policy then consumes a budgeted set of these rules during rollout.

### 3. What is the method motivation?
Population-averaged memory policies wash out minority behaviors, but fully individualized policies redundantly rediscover universal rules and struggle on cold-start users. The paper's motivation is to discover the split empirically instead of hard-coding it.

### 4. What data does it use?
It trains on 423 samples drawn from 70% of the PersonaMem 32K split. It evaluates on four personalized-memory benchmarks: PersonaMem, PrefEval, PersonaBench, and PERMA, covering in-domain preference evolution and out-of-domain noisy or cross-domain settings.

### 5. How is it evaluated?
It is evaluated across twelve settings against long-context, retrieval, memory-bank, and RL-based baselines, then with ablations on USD, PDD, gating, flow, and predictive gain, plus cross-model transfer to GPT-4o-mini, Gemini 2.5 Flash, and GPT-5.

### 6. What are the main results?
HiPS is best in all twelve reported settings. On PersonaMem it reaches `73.49` at 32K and `62.01` at 128K, compared with `64.45` and `55.37` for MemSkill and `42.17` and `20.74` for raw long context. On PrefEval Explicit it scores `89.20`, ahead of `82.60` for MemSkill. The out-of-domain story is where the architecture earns its keep: on PERMA C-S, ablating cross-level flow drops performance from `66.95` to `45.39`, and removing the divergence gate drops it to `51.63`. Persona deltas add about `+6.0` points on PersonaMem 128K on average, with some personas gaining up to `+18.6`.

### 7. What is actually novel?
The real novelty is treating the universal-versus-personalized boundary as something to be discovered and updated online, not fixed in advance. The rule-promotion and specialization loop is the part that matters most.

### 8. What are the strengths?
The paper exposes memory policy as an explicit artifact, gives a plausible reason to separate global and persona-local rules, and validates that the separation matters most when distribution shifts or user diversity stress the system. The cross-model transfer result is also useful because it suggests the strategy text is not just overfitted to one backbone.

### 9. What are the weaknesses, limitations, or red flags?
This is still benchmark-heavy personalized chat memory, not a general memory architecture for open-ended agents. The strategy objects are natural-language rules distilled by another LLM, which can be brittle or verbose. The system is also not cheap: the reported memory evolution time scales from roughly 140 to 1,700 seconds as context grows.

### 10. What challenges or open problems remain?
The main open question is whether explicit rule layers still help once memory becomes richer than persona management: tool histories, contradictory external facts, long-horizon plans, or multi-user shared state. Another challenge is replacing prompt-level rule text with something more structured without losing interpretability.

### 11. What future work naturally follows?
Structured rule schemas instead of free text, tighter coupling between rule evolution and retrieval indexing, and memory systems that separate user preferences, factual state, and task state rather than treating them as one bank.

### 12. Why does this matter for cabbageland?
Because cabbageland cares about memory as policy, explicit state, and bounded context management. HiPS is useful mainly as a design pattern: not all memory rules should be global, and not all personalization should stay siloed.

### 13. What ideas are steal-worthy?
Make the shared versus personalized split explicit. Gate personalization by measurable divergence instead of applying it everywhere. Allow rules to migrate upward or downward based on evidence. Use budgeted rule selection so the prompt does not become another garbage dump.

### 14. Final decision
Keep as a preserved note. It is not the final answer to agent memory, but it is better than most recent work at naming the actual policy question.

## 6. Mandatory critical angles

The paper is strongest on explicit memory policy, decomposition, and out-of-domain behavior. It is weaker on deployment realism and on proving that natural-language rules are the right long-term representation rather than just a convenient current one.

## 7. Writing style

The right tone is interested but unsentimental. The paper is valuable because it clarifies a real design axis, not because benchmark scores alone are exciting.

## 8. Repository output format

Saved as a preserved paper note because the universal-versus-personalized split is a reusable memory-design pattern.
