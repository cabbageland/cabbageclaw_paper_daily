# TRAJDEBUG: Tracing Error Lifecycle to Identify Critical Failures in Long-Horizon Agent Trajectories

## Basic info

* Title: TRAJDEBUG: Tracing Error Lifecycle to Identify Critical Failures in Long-Horizon Agent Trajectories
* Authors: Yunjia Qi, Zehua Yin, Xintong Shi, Hao Peng, Songyuanyi Lu, Yixian Liu, Richeng Xuan, Yuhong Liu, Zhichao Hu, Xiaozhi Wang, Lei Hou, Bin Xu, Juanzi Li
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.06346
* Date surfaced: 2026-08-08
* Why selected in one sentence: It gives long-horizon agent debugging an explicit error object, lifecycle state, and terminal-footprint test instead of one mushy postmortem judgment.

## Quick verdict

* Highly relevant

I inspected the arXiv HTML full text. This is one of the better recent agent-diagnostics papers because it does not confuse "a wrong-looking step happened somewhere" with "this is the earliest failure-responsible error." The core decomposition is sharp and directly reusable even if the benchmark details change.

## One-paragraph overview

TrajDebug targets a real agent-systems problem: failed trajectories are long, messy, and often contain several local mistakes, but only some of those mistakes actually matter for the terminal failure. The paper addresses this with a staged LLM-based diagnosis pipeline. It compresses trajectory history at multiple resolutions, extracts evidence-grounded error triggers that must cite an explicit wrong commitment and violated reference, clusters repeated manifestations into error instances, classifies whether each instance was resolved and whether it left a terminal footprint, and only then asks an attribution head to pick the critical step. The authors also build TrajErrBench, a benchmark of 486 manually annotated failed trajectories from Tau2Bench and SWE-Bench Pro, and show the pipeline beats prompt-only baselines while producing diagnoses that help rerun or transfer agent behavior.

## Model definition

### Inputs
The system takes a failed agent trajectory with task instruction, reasoning, actions, observations, and compressed multi-resolution history views.

### Outputs
It outputs per-step evidence-grounded error triggers, clustered error instances with lifecycle state labels, and a predicted critical error step for the failed trajectory.

### Training objective (loss)
There is no new trainable predictive model in the core method. The paper uses an inference-time LLM diagnosis pipeline rather than optimizing a learned loss for critical-error detection.

### Architecture / parameterization
A staged LLM-based diagnostic stack: multi-granularity compression, error-trigger extraction, error-state classification, candidate filtering, and final LLM attribution over terminal-relevant candidates.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to identify the earliest failure-responsible error in a long failed agent trajectory, not merely any local mistake. That is hard because evidence can be far away in the history, and many local errors are later repaired or turn out harmless.

### 2. What is the method?
The method has three main stages. First, it extracts atomic error triggers with explicit wrong commitments and violated references. Second, it groups triggers by shared violated reference object and classifies the instance state using resolution status plus terminal footprint. Third, it runs an attribution head only over terminal-relevant candidates to select the critical error step.

### 3. What is the method motivation?
Holistic prompting over full trajectories is brittle. If you do not separate local evidence discovery from downstream causal relevance, you either miss early errors in long context or over-credit the first wrong-looking step.

### 4. What data does it use?
It uses TrajErrBench, a benchmark of 486 manually annotated failed trajectories: 400 from Tau2Bench and 86 from SWE-Bench Pro. The SWE-Bench Pro subset averages about 119.7 steps and brings in long-horizon coding failures.

### 5. How is it evaluated?
The paper compares TrajDebug against advanced LLM prompting baselines and prior diagnostic systems on existing agent benchmarks plus TrajErrBench. It also studies robustness over trajectory length and runs two application scenarios: same-task reruns with targeted guidance and held-out transfer using aggregated failure memory.

### 6. What are the main results?
TrajDebug reports the best overall performance on the evaluated critical-error-detection benchmarks. The more practically important result is that converting diagnoses into rerun guidance improves task success by 10.80% on average, while aggregated failure memory transferred to held-out tasks adds another 5.70%.

### 7. What is actually novel?
The novelty is not simply "use an LLM to debug agents." The real contribution is treating agent errors as lifecycle-tracked instances: explicit violated references, clustered repeated manifestations, and state labels that separate repaired errors from terminally relevant ones.

### 8. What are the strengths?
The method is auditable relative to most agent-debugging papers. The verbatim-evidence rule is good. Grouping by violated reference object is better than counting raw bad steps. The terminal-footprint taxonomy is also practically useful for memory building and rerun guidance.

### 9. What are the weaknesses, limitations, or red flags?
The final attribution is still LLM judgment, not environment-level causal intervention. The budget-debt threshold is heuristic. The benchmark covers two domains and only failed trajectories, so we should not confuse this with a complete theory of agent-process diagnosis.

### 10. What challenges or open problems remain?
The hard problem is still causal validity under richer environments. It remains unclear how well the lifecycle labels hold for agents with parallel tools, partial observability, or environment stochasticity.

### 11. What future work naturally follows?
Counterfactual replay with environment execution, automatic repair generation, online failure memory updates, and direct training on lifecycle-aware supervision are the obvious next steps.

### 12. Why does this matter for cabbageland?
This is unusually aligned with cabbageland’s taste for explicit state over transcript vibes. A reusable agent memory should store violated references, repair status, and terminal footprint, not just "the model messed up around step 43."

### 13. What ideas are steal-worthy?
Require verbatim evidence for every diagnosed error. Cluster repeated local mistakes by violated reference object. Distinguish clean resolution, costly resolution, manifest active, and latent active. Convert diagnoses into reusable failure memory instead of one-off postmortems.

### 14. Final decision
Keep as a preserved note. The benchmark is narrower than the idea, but the error-object decomposition is strong enough to reuse in future agent debugging and memory systems.

## 6. Mandatory critical angles

TrajDebug is good on motivation, mechanism, and explicit state. Its decomposition actually changes the computation rather than renaming a monolithic prompt. Interpretability is better than average because the trigger and reference objects are citable. The weak spot is causal validity: the last step still relies on LLM attribution rather than mechanical intervention or replay.

## 7. Writing style

This paper earns direct language because it solves a real pain point. The right caution is not "maybe useful someday." The right caution is "good decomposition, still partly verbal causality."

## 8. Repository output format

Saved as a preserved paper note because the method is directly relevant to long-horizon agent debugging, failure memory, and reliability analysis.
