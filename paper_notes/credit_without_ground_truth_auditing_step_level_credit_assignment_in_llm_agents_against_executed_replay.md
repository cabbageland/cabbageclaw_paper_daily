# Credit Without Ground Truth: Auditing Step-Level Credit Assignment in LLM Agents Against Executed Replay

## Basic info

* Title: Credit Without Ground Truth: Auditing Step-Level Credit Assignment in LLM Agents Against Executed Replay
* Authors: Haiyue Zhang
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.19760
* Date surfaced: 2026-08-21
* Why selected in one sentence: It is the most severe paper in the batch on whether the step-level credit signals used in agent training correspond to anything causally real.

## Quick verdict

* Must read

I inspected the arXiv HTML full text, especially the executed-replay setup, audit criteria, and training-analysis sections. This paper is unusually good because it refuses the standard cheat where a credit signal gets evaluated against annotated step correctness instead of causal contribution. The result is brutal and useful: the usual signals largely fail once you ask the right question.

## One-paragraph overview

The paper audits step-level credit assignment signals for LLM agents against causal ground truth produced by executed replay in ALFWorld. At each decision point, the authors resample policy-supported alternative actions, roll the environment forward, and measure how much the outcome distribution changes. That becomes the target for causal contribution. Against that target, common signals such as LLM-judge scores, outcome-conditioned logprob ratios, and the policy's own confidence do not identify which steps actually matter better than chance. The paper then pushes further and shows that apparent downstream differences between sparse-credit training variants mostly collapse into a much dumber confound: different rules retain different numbers of examples, so they change optimization dose as much as or more than they change credit quality.

## Model definition

### Inputs
Collected agent trajectories, replayable environment states, policy-supported alternative actions at each decision point, and the compared credit signals.

### Outputs
Executed-replay causal-contribution measurements, fidelity statistics for the compared credit signals, and downstream training comparisons across credit rules.

### Training objective (loss)
The paper is primarily an audit rather than a new model proposal. It studies credit signals used in existing agent-training setups and runs a seven-arm training experiment, but the accessible paper text does not frame the contribution as one new standalone loss.

### Architecture / parameterization
Hybrid evaluation stack around existing LLM policies in a replayable single-agent tool environment. The key machinery is the executed-replay instrument and the statistical audit, not a new network architecture.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve a methodological failure in agent training: we often act as though a step-level credit signal identifies causally important steps even when we never test it against actual causal contribution.

### 2. What is the method?
The method is executed replay. For each step in a collected trajectory, the paper resamples the policy's own alternatives, re-executes the environment, and uses the induced change in outcomes as ground truth for that step's causal contribution. It then audits existing credit signals against that target.

### 3. What is the method motivation?
Annotated step correctness is not the same thing as whether a step mattered for the final outcome. If those are conflated, we can end up training agents on signals that look sensible but are causally empty.

### 4. What data does it use?
The audit uses ALFWorld trajectories from two model families. The paper reports 50 trajectories collected with Qwen2.5-7B-Instruct on a frozen task list and 28 trajectories in the Llama-3.1-8B-Instruct transfer arm, with exclusions and coverage rules handled explicitly in the paper.

### 5. How is it evaluated?
The paper compares credit signals using multiple independent tests: rank fidelity against replay ground truth, sign agreement, partial correlation after conditioning out fluency, and a seven-arm pre-registered training experiment that controls for downstream dose confounds.

### 6. What are the main results?
Causal contribution is sparse: only 30.5% of defined decision points carry measurable effect. Measurability itself is policy-dependent, with no policy-supported counterfactual at 13.1% of points for one family versus 26.8% for another. Implicit credit tracks fluency strongly, with median rank correlation +0.75 and a +0.70 replication in the second family, while outcome conditioning adds essentially no causal information, with partial correlation -0.004 on the registered Qwen set. In the seven-arm training experiment, no arm reliably beats the untrained policy once effective sample size is taken seriously.

### 7. What is actually novel?
The novelty is auditing credit against executed causal contribution rather than correctness labels, and then forcing the training comparison to separate credit content from training dose.

### 8. What are the strengths?
The paper is pre-registered, methodologically severe, and unusually careful about not letting one statistic do all the work. It also produces a useful negative result instead of inflating a weak positive one.

### 9. What are the weaknesses, limitations, or red flags?
The environment is still ALFWorld, so the audit lives in one replayable single-agent tool domain rather than richer multi-agent or messier real software settings. Some replay coverage is model-dependent because the policy may not support enough plausible counterfactual actions at every step.

### 10. What challenges or open problems remain?
The main open problem is extending this kind of audit to harder environments where action spaces are larger, trajectories are longer, tool effects are less deterministic, and executed replay becomes more expensive.

### 11. What future work naturally follows?
Run executed-replay credit audits in coding agents, browser agents, and richer tool-use environments; compare different causal estimators; and design training rules that keep effective sample size genuinely matched across credit variants.

### 12. Why does this matter for cabbageland?
Because agent papers constantly smuggle proxy targets past evaluation. This paper gives a severe reminder that if your credit signal is not grounded against actual contribution, you may just be rewarding fluency and then confusing optimizer dose for insight.

### 13. What ideas are steal-worthy?
Audit step credit against replayed counterfactual outcomes, not correctness labels. Treat measurability as part of the object instead of sweeping it away. Match effective sample size across training conditions before claiming a better credit rule.

### 14. Final decision
Keep as a preserved note. This is the kind of negative methodological paper that saves future work from fake learning signals.

## 6. Mandatory critical angles

The paper is strongest on evaluation fairness, failure-mode analysis, and truthfulness about what is actually being measured. It earns the "agent credit" framing because it really tests contribution rather than just relabeling correctness. The distribution-shift caveat is obvious: the audit should be repeated in much harsher environments.

## 7. Writing style

The right tone is severe and slightly delighted. The paper is valuable precisely because it is willing to break a flattering story.

## 8. Repository output format

Saved as a preserved paper note because the executed-replay audit principle is broadly reusable for agent evaluation and training analysis.
