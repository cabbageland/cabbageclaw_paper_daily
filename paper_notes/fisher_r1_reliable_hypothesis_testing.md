# Fisher-R1: Training LLM Agents for Reliable Hypothesis Testing

## Basic info

* Title: Fisher-R1: Training LLM Agents for Reliable Hypothesis Testing
* Authors: Jiacheng Miao, Jin Mu, Guanhua Chen, James Zou
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.07437
* Date surfaced: 2026-08-10
* Why selected in one sentence: It evaluates and trains coding agents on inferential validity rather than mere executability, using real scientific tasks and verified statistical rewards.

## Quick verdict

* Preserve-worthy adjacent paper

I inspected the arXiv HTML full text. This is one of the better recent agent-reliability papers because it goes after a failure mode that ordinary coding benchmarks barely see: a model can write runnable analysis code, report a neat p-value, and still choose the wrong statistical procedure.

## One-paragraph overview

The paper argues that open-ended hypothesis testing is a better reliability stress test for coding agents than most existing data-analysis benchmarks. In this setting, the agent does not just answer a factoid or fit a predictive model; it must choose a statistical method, execute it, report a p-value, and decide whether to reject the null. The authors build P-Bench, a 425-task benchmark drawn from economics, biology, and medicine, where each answer key is grounded in executable reference analysis and checked by experts. They then train Fisher-R1, an open-weight coding agent on synthetic hypothesis-testing tasks with supervised fine-tuning followed by RL. The reward is not method-name matching alone, but verified outcome alignment: p-value closeness in z-space plus conclusion correctness.

## Model definition

### Inputs
The agent takes a scientific hypothesis-testing question, a dataset, and a data description, then interacts with an execution environment.

### Outputs
It outputs executable analysis steps, a chosen statistical procedure, a p-value, and a reject/fail-to-reject decision.

### Training objective (loss)
The training pipeline uses supervised fine-tuning on expert-style trajectories and reinforcement learning with verified statistical rewards. The reward checks p-value accuracy in z-space and conclusion correctness rather than only text quality.

### Architecture / parameterization
The paper uses Qwen2.5-Coder backbones with an agentic execution loop in R. The key contribution is not a new backbone architecture but a benchmark plus a reward design targeted at inferential validity.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to make coding agents reliable at open-ended hypothesis testing, where choosing the wrong statistical method can produce confident but invalid conclusions.

### 2. What is the method?
The method has two parts: P-Bench for evaluation, and Fisher-R1 for training. P-Bench packages real scientific hypothesis-testing tasks with verified answer keys. Fisher-R1 trains on synthetic executable tasks using SFT and RL with outcome-grounded rewards.

### 3. What is the method motivation?
Existing agent benchmarks mostly reward fluency, executability, or answer plausibility. They rarely verify whether the reported p-value is statistically valid for the data and assumptions at hand.

### 4. What data does it use?
P-Bench contains 425 real hypothesis-testing tasks from economics, biology, and medicine, stratified into Easy and Hard splits. Training uses synthetic tasks with executable data-generating processes and verified answer keys.

### 5. How is it evaluated?
The paper reports pass@1 and pass@3 over three rollouts under two criteria. Raw scoring checks conclusion direction. Strict scoring also requires the reported p-value to stay close to the canonical answer in z-space.

### 6. What are the main results?
Fisher-R1-14B substantially improves over its backbone and beats strong open and proprietary baselines. The paper reports a 21% average relative single-trial gain over DeepSeek-V4-Pro, with gains up to 26% on the hardest tasks. Fisher-R1-14B beats GPT-5.4 on three of four strict metrics, including P-Hard strict pass@1 and pass@3. The paper also shows that the gap between Raw and Strict scores is large for all baselines, exposing how much conclusion-only evaluation overstates reliability.

### 7. What is actually novel?
The novelty is the evaluation target and reward design: open-ended statistical inference with verified outcome checking, not just code execution or multiple-choice method selection.

### 8. What are the strengths?
The benchmark is grounded in real scientific tasks, the answer keys are executable and audited, and the strict-vs-raw distinction is exactly the right diagnostic. The reward design also feels much more defensible than vague "analysis quality" judgments.

### 9. What are the weaknesses, limitations, or red flags?
The benchmark still focuses on single hypothesis tests per task rather than full multi-test pipelines with multiple-comparison correction. Method correctness is only indirectly rewarded through outcome closeness, and the environment is anchored to R rather than a broader mixed-tool ecosystem.

### 10. What challenges or open problems remain?
Real scientific workflows often involve multiple tests, model diagnostics, robustness checks, and ambiguous method choices. Teaching agents to justify assumptions and know when no single test is adequate remains an open problem.

### 11. What future work naturally follows?
Multi-test scientific pipelines, explicit assumption-check rewards, uncertainty over method choice, and better oversight tools for agentic science all follow naturally.

### 12. Why does this matter for cabbageland?
Cabbageland cares about reliable tool use, evidence-grounded reasoning, and the difference between polished outputs and valid computation. This paper gives a strong example of how to benchmark that difference.

### 13. What ideas are steal-worthy?
Evaluate agent reasoning with executed answer keys, not only surface outputs. Split scoring into conclusion correctness and evidence-grounded numerical correctness. Use RL rewards that directly encode the failure mode you care about rather than proxying it with generic success.

### 14. Final decision
Keep as a preserved note. The work is adjacent rather than central, but the benchmark and reward-design ideas are too useful to ignore.

## 6. Mandatory critical angles

This paper is strongest on evaluation design and reliability framing. It forces the right embarrassment: many strong agents can sound statistically competent while getting the actual inference wrong. The main limitation is scope. P-Bench is a sharp slice of the problem, not the whole scientific-agent stack.

## 7. Writing style

The right tone is approving but unsentimental. The important point is not that Fisher-R1 beats a leaderboard rival. The important point is that the benchmark distinguishes real inferential competence from pretty code theater.

## 8. Repository output format

Saved as a preserved paper note because the benchmark design, strict-vs-raw scoring split, and verified statistical reward pattern are directly useful for future work on reliable coding and research agents.
