# Optimal Skill Selection for LLM Agents with Provable Bicriteria Guarantees

## Basic info

* Title: Optimal Skill Selection for LLM Agents with Provable Bicriteria Guarantees
* Authors: Yu Chen, Ruishuo Chen, Xun Wang, Zhuoran Li, Longbo Huang
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.19993
* Date surfaced: 2026-08-23
* Why selected in one sentence: It is the most directly useful paper in the batch on turning skill routing from heuristic relevance ranking into a budgeted set-optimization problem.

## Quick verdict

* Must read

I inspected the arXiv HTML full text, especially the formulation, the BPS theorem, the contamination-controlled benchmark design, and the end-to-end execution results. This paper earns a preserved note because it gets the object of optimization exactly right: not "which individual skills look relevant," but "which set of skills gives the frozen executor the right capability coverage under a hard context budget." It is rare to get a direct agent-systems problem, a clean optimization formulation, and a real execution benchmark all aligned this tightly.

## One-paragraph overview

The paper starts from a practical observation that is embarrassingly obvious once stated: LLM agents do not benefit from skills independently. They benefit from the capability composition of the selected skill set, while irrelevant or redundant skills consume scarce context and can directly hurt execution. The authors formalize skill selection as choosing a feasible skill set under a hard token budget to maximize a monotone submodular capability benefit minus a linear context penalty. They then introduce Best Prefix Selection (BPS), a polynomial-time algorithm with a tight (1 - 1/e, 1) bicriteria guarantee, and evaluate it on a contamination-controlled BigCodeBench-style benchmark where tasks are purposely unsolvable unless the selected skills expose the required private modules and semantics.

## Model definition

### Inputs
Task query, installed skill library, skill token lengths, fitted capability representations or coverage estimates, and a hard residual context budget for injected skill documents.

### Outputs
A selected set of skill documents to inject into the frozen executor's context for downstream task execution.

### Training objective (loss)
The paper's core contribution is not a new trainable executor. The fitted objective learns a structured benefit model from pass/fail execution records, then optimizes a monotone submodular benefit minus a linear token-length penalty under a hard budget.

### Architecture / parameterization
Set-optimization framework plus frozen executor. The end-to-end setup uses a frozen Qwen3-32B executor, fitted capability representations for skills, and the BPS selection algorithm operating over a budgeted skill library.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the fact that current skill selectors treat each skill independently and then pack the top-ranked items, even though downstream success depends on coverage, complementarity, redundancy, and context damage at the level of the selected set.

### 2. What is the method?
The method is to cast skill selection as regularized submodular maximization under a hard token budget. The paper defines a monotone submodular capability benefit, subtracts a linear context penalty, and solves the resulting problem with Best Prefix Selection, a partial-enumeration density-greedy algorithm that records and scores every feasible prefix.

### 3. What is the method motivation?
Agents operate inside bounded context windows. A selector that optimizes only semantic similarity can waste tokens on redundant or irrelevant skills and degrade the frozen executor even when each chosen skill looked individually reasonable.

### 4. What data does it use?
The main evaluation uses a contamination-controlled BigCodeBench variant. Tasks are gated so they cannot be solved unless the selected skills provide the required private APIs and hidden semantics. The paper also uses a capability-composition sanity check where complementary skills can solve the task but individually relevant single-capability skills cannot.

### 5. How is it evaluated?
The paper evaluates objective validity, optimization quality, and end-to-end measured execution. It compares BPS with released skill routers, text retrievers, greedy or top-k style selectors, and the frozen executor's own selection behavior.

### 6. What are the main results?
BPS reaches 0.73 measured task success versus 0.20-0.52 for the deployed baselines, while using 28% fewer tokens than the strongest released router. In the capability-composition sanity check, single-capability skill sets have 0% success, complementary skills reach 93%, adding a redundant skill costs 225 extra tokens for only a one-point gain, and adding a semantically related but irrelevant skill drops success by 23 points. The paper also reports that BPS attains the exact optimum on every evaluated selection instance in the fitted benchmark setting.

### 7. What is actually novel?
The novelty is the combination of three things that usually stay separate: a set-level capability formulation, a tight bicriteria guarantee for the budgeted regularized objective, and a benchmark that makes execution genuinely dependent on the selected skills instead of on contamination or generic base-model competence.

### 8. What are the strengths?
The paper is unusually well-aligned with the real systems problem. The capability-composition examples are concrete, the optimization story is mathematically clean, and the benchmark is built to punish fake skill-selection success. It also directly measures token efficiency instead of pretending context cost is free.

### 9. What are the weaknesses, limitations, or red flags?
The fitted benefit model still depends on assumptions about capability structure and executor behavior. The evaluation is strongest in coding-agent settings with explicit private modules, so the exact benchmark may not transfer unchanged to every agent domain. And while the theoretical algorithm is polynomial-time, the O(dL^4) discussion suggests scaling could get uncomfortable for very large libraries without additional engineering.

### 10. What challenges or open problems remain?
The hard next step is online and session-aware skill selection, where the available budget depends on evolving conversation state and where some capabilities can be supplied by retrieval, memory, or tools rather than static skill docs alone.

### 11. What future work naturally follows?
Test the same formulation on non-coding agents, combine it with dynamic retrieval and memory state, and study whether the capability-benefit model can be updated online from deployment traces rather than only from offline fitted records.

### 12. Why does this matter for cabbageland?
Because cabbageland lives inside the exact failure mode this paper names: too many potentially useful skills, too little context, and selectors that often confuse relevance with the actual capability mix the executor needs. This paper gives a much better abstraction for that problem.

### 13. What ideas are steal-worthy?
Model skill routing as set selection, not per-item ranking. Optimize capability coverage minus context damage under a hard budget. Use contamination-controlled tasks with private modules so selector quality cannot hide behind pretrained knowledge. Record every greedy prefix and select the best feasible one instead of trusting the final greedy chain blindly.

### 14. Final decision
Keep as a preserved note. This is one of the few recent skill-routing papers that looks both principled and operationally useful.

## 6. Mandatory critical angles

The paper is strongest on mechanism, decomposition, controllability, and evaluation realism. It earns the skill-selection label because the selected set, not the individual skill score, is the thing being optimized. The main caution is that the fitted capability model may be cleaner than real multi-turn deployments.

## 7. Writing style

The right tone is enthusiastic but strict. The paper is satisfying precisely because it replaces a mushy heuristic problem statement with the correct combinatorial one.

## 8. Repository output format

Saved as a preserved paper note because the formulation is directly reusable for agent design and evaluation.
