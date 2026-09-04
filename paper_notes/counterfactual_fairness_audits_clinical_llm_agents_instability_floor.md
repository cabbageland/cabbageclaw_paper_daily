# Counterfactual Fairness Audits of Multi-Step Clinical LLM Agents Require a Measured Per-Action Instability Floor

## Basic info

* Title: Counterfactual Fairness Audits of Multi-Step Clinical LLM Agents Require a Measured Per-Action Instability Floor
* Authors: Rohith Reddy Bellibaltu, Manpreet Singh, Deepak Parashar, Rahul Joshi
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2609.03221
* Date surfaced: 2026-09-04
* Why selected in one sentence: It shows that demographic flip-rate audits for clinical agents are unreadable unless they are anchored to the agent's own same-condition instability floor.

## Quick verdict

* Highly relevant

I inspected the full arXiv HTML text, especially the benchmark design, acceptable-action-band formulation, instability-floor results, and discussion sections. This note is worth keeping because the paper fixes a measurement problem rather than merely adding another fairness benchmark. It is also unusually honest about what it does not yet prove: the paper measures the floor and releases the audit harness, but it does not overclaim disparity findings before the estimand is ready.

## One-paragraph overview

The paper introduces **FairMedAgent**, an evaluation harness for demographic fairness in multi-step clinical LLM agents. The key point is that a counterfactual action flip rate, by itself, cannot be interpreted as evidence of disparity unless you first know how often the same agent flips under the exact same condition with nothing changed. The harness therefore measures a **per-action instability floor** and also defines a more careful fairness estimand, the **within-range counterfactual flip rate**, which counts only flips between actions that a published clinical rule admits and a blinded clinician has adjudicated as acceptable. The paper's central result is not a disparity score. It is that the instability floor is large enough to dominate the observed demographic contrasts, so fairness audits that omit it are structurally misleading.

## Model definition

### Inputs
The evaluated agent receives a synthetic clinical vignette, a fixed-form demographic condition, and deterministic tool-result fixtures inside a six-stage trajectory with five model-facing decisions around one environment step.

### Outputs
The agent outputs sequential clinical actions such as acuity, ordering, medication-related flags, documentation, or disposition choices, which the harness then scores.

### Training objective (loss)
There is no new trainable model introduced by the paper. The contribution is an evaluation harness, a fairness estimand, and an instability-floor protocol around existing clinical LLM agents.

### Architecture / parameterization
The system is a fixed-form multi-step clinical-agent evaluation loop with clinician-defined acceptable-action bands, counterfactual demographic condition swaps, and repeated-run measurement of action instability.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
How do you audit demographic fairness in sequential clinical LLM agents without confusing true disparity with the agent's own stochastic action instability?

### 2. What is the method?
Run repeated identical-condition trajectories to estimate a per-action instability floor, define within-range counterfactual flips using clinician-adjudicated acceptable-action bands, and compare demographic contrasts only against that measured floor.

### 3. What is the method motivation?
If the same agent flips often under no demographic change at all, then a raw demographic flip count cannot be interpreted as disparity evidence. The floor has to be measured, not assumed away.

### 4. What data does it use?
The reported measurements use 16 synthetic vignettes, six-stage trajectories, repeated identical-condition reruns, and fixed-form demographic contrasts spanning race, sex, age, insurance, English proficiency, and intersections. A second model is used to test whether the floor pattern is system-specific.

### 5. How is it evaluated?
The harness reports counterfactual flip rate, mean absolute score difference, signed action-rate disparity, and the within-range counterfactual flip rate. The main evaluation in this paper focuses on instability-floor measurement, majority-vote mitigation, and whether observed contrasts rise above that floor.

### 6. What are the main results?
The headline result is that the floor is substantial. Re-running an identical condition ten times over 16 vignettes moves the primary agent's action in 8.7% of outcome-vignette cells across 4,320 comparisons. The action-specific rates vary sharply, from 2.2% for ICU escalation to 17.9% for controlled-substance caution. A second model shows a 6.7% pooled floor and ranks the six actions almost identically, with Spearman 0.94 and exact p = 0.017. Majority voting over five draws removes only 39% of the floor before flattening. No demographic contrast in the current data clears the measured floor, and the paper explicitly states that no disparity result is claimed yet because band adjudication is still under way.

### 7. What is actually novel?
The novelty is the insistence that a fairness audit needs a same-action instability floor plus an acceptable-action-band-aware estimand, not just another raw flip metric.

### 8. What are the strengths?
It makes the measurement target much cleaner, separates demographic sensitivity from outright clinical error, and is careful not to inflate provisional instrumentation results into fairness claims.

### 9. What are the weaknesses, limitations, or red flags?
The study is still based on synthetic vignettes, the acceptable-action bands are not fully adjudicated yet, and the reported results are floor measurements rather than finished clinical disparity estimates. The fixed phase order is useful for attribution but less realistic than a fully adaptive agent loop.

### 10. What challenges or open problems remain?
The big open problems are finishing band adjudication, extending the protocol to richer clinical trajectories and more models, and deciding how to combine instability-aware auditing with real clinical outcome considerations.

### 11. What future work naturally follows?
Apply the same floor protocol to broader clinical-agent stacks, test stronger stabilization methods than simple majority vote, and extend the estimand to real-world or semi-simulated deployments where adaptive planning matters.

### 12. Why does this matter for cabbageland?
Because cabbageland keeps caring about measurement honesty in safety-critical agents. This paper is a good reminder that if your audit metric is noisier than the effect you want to claim, the right conclusion is not "maybe biased" but "your measurement object is not ready."

### 13. What ideas are steal-worthy?
Measure an instability floor before interpreting a flip rate. Use acceptable-action bands to separate sensitivity from plain error. Treat residual variance as part of the estimand boundary, not as an embarrassing detail to hide in appendices.

### 14. Final decision
Keep as a preserved note. This is a useful paper because it corrects the measurement logic of sequential fairness audits instead of decorating the old logic with more plots.
