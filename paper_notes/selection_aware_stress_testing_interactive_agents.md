# Selection-Aware Stress Testing for Interactive Agents

## Basic info

* Title: Selection-Aware Stress Testing for Interactive Agents
* Authors: Yang Xu, Chenang Li, Jiefu Zhang, Haixiang Sun, Zhou Li, Vaneet Aggarwal
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.30916
* Date surfaced: 2026-09-01
* Why selected in one sentence: It attacks the common habit of discovering a weak subgroup on the same benchmark data and then talking as if the subgroup effect were confirmed.

## Quick verdict

* Useful

I inspected the full arXiv HTML text, especially the discovery/confirmation protocol, the small-cluster audit, the tau-bench studies, and the paper's own decision-status logic. This earns a preserved note because the empirical result is not triumphant, but the evaluation discipline is worth keeping.

## One-paragraph overview

Selection-Aware Semantic Stress Testing (SASST) tries to make subgroup stress tests in agent evaluation less sloppy. Instead of using one benchmark both to choose a winning workflow and to discover the task slice where that winner looks weak, SASST splits tasks into discovery and confirmation sets. It learns a bounded task-reweighting rule from pre-execution features on the discovery set, freezes that rule, and then re-runs the same workflow comparison on held-out confirmation tasks. It also checks support and stability and can explicitly abstain. The main empirical point is sobering by design: a discovery-time effect can vanish on confirmation, and the right conclusion is often "no supported claim."

## Model definition

### Inputs
Pre-execution task features, clustered task-level workflow outcomes, and a fixed workflow-comparison target such as Plan+Verifier versus ReAct.

### Outputs
A frozen task-reweighting rule, a weighted workflow comparison on held-out tasks, and a final status such as confirmed, not confirmed, failed feasibility, or abstained.

### Training objective (loss)
There is no learned neural model. The method selects a bounded nonnegative reweighting rule on discovery tasks subject to support and stability constraints, then evaluates that frozen rule on confirmation tasks with uncertainty control.

### Architecture / parameterization
A discovery-confirmation statistical protocol with task-level clustering, predeclared reporting slots, and a conservative small-cluster safeguard based on Bonferroni `t` bounds.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to stop same-data subgroup fishing in interactive-agent benchmarking.

### 2. What is the method?
Split tasks into discovery and confirmation sets, learn a stress rule from discovery-task features only, freeze it, and then confirm or reject the subgroup comparison on held-out tasks.

### 3. What is the method motivation?
A subgroup reversal found after looking at benchmark outcomes may just be noise. If it is real and reusable, it should survive on new tasks.

### 4. What data does it use?
Controlled validation studies plus tau-bench agent experiments with 80 tasks, two simulator seeds, and three workflows over 480 episodes.

### 5. How is it evaluated?
Through coverage audits, positive controls, support/stability checks, and held-out confirmation of discovery-selected stress rules in agent studies.

### 6. What are the main results?
The paper finds that Gaussian bounds undercover while Bonferroni `t` bounds are conservative in the audited small-cluster setting. In the Qwen3-8B tau-bench study, a +3.75 point discovery gain for Plan+Verifier over ReAct becomes 0.0 on confirmation, with final counts 0 confirmed / 2 not confirmed / 8 abstained / 0 failed feasibility. In the Qwen2.5-7B study, neither the workflow benefit nor a stable rule confirms, with maximum rule stability only 0.27.

### 7. What is actually novel?
The novelty is protecting both the winner selection and the subgroup search in the same protocol, rather than treating subgroup discovery as free once the benchmark has been run.

### 8. What are the strengths?
It has good epistemic hygiene. The method can say "no claim," and the paper actually uses that option instead of force-spinning the outcome.

### 9. What are the weaknesses, limitations, or red flags?
Power is limited with only 40 confirmation clusters, and the second study is a model replication rather than an independent benchmark replication. The method is more useful as evaluation discipline than as evidence of a strong domain finding today.

### 10. What challenges or open problems remain?
Getting enough independent task clusters for meaningful confirmation while still keeping agent evaluations affordable.

### 11. What future work naturally follows?
Applying similar protected subgroup logic to coding-agent benchmarks, multimodal agent studies, and deployment audits where subgroup claims are otherwise easy to overstate.

### 12. Why does this matter for cabbageland?
Because agent-eval discourse is full of weak subgroup stories. This paper gives a cleaner protocol for deciding when a discovered slice is real enough to matter.

### 13. What ideas are steal-worthy?
Protect subgroup search with held-out confirmation. Use explicit abstention when support or stability is weak. Report why a claim failed, not just that it failed.

### 14. Final decision
Keep as a preserved note. The paper is not a grand empirical victory, but it is a valuable guardrail against evaluation theater.
