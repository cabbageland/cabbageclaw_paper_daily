# DriftLens: Measuring Memory-Induced Reasoning Drift in Personalized Language Models

## Basic info

* Title: DriftLens: Measuring Memory-Induced Reasoning Drift in Personalized Language Models
* Authors: Xi Fang, Weijie Xu, Yingqiang Ge, Yuhui Xu, Stephanie Eckman, Chandan K. Reddy
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.02374
* Date surfaced: 2026-07-05
* Why selected in one sentence: It gives personalized-memory systems a way to measure reasoning-trajectory drift when final-answer accuracy is not available.

## Quick verdict

* Highly relevant

This is a strong evaluation paper for long-lived assistants. I inspected the full arXiv HTML, including the framework, controls, memory-induced drift results, and mitigation section. The important contribution is not that personalization can bias answers; it is that irrelevant stored user attributes can move the expressed reasoning trajectory while the final response remains plausible.

## One-paragraph overview

DriftLens studies open-ended, persona-indifferent questions where there is no single correct answer, but where irrelevant user memories should not change the reasoning path. The framework generates a no-memory response and memory-perturbed responses, maps reasoning steps into a value ontology, and compares the resulting symbolic trajectories with metrics such as dynamic time warping and a sequence recurrence index. The authors validate the instrument with pragmatic-noise negative controls and major-life-event positive controls, then evaluate four models across ten user-attribute memory categories. They find that user memories induce statistically significant reasoning drift above each model's noise floor. Mitigation through GRPO and DPO helps but is not uniformly clean.

## Model definition

### Inputs
The framework takes open-ended reasoning questions, no-memory baseline prompts, and prompts perturbed with injected user-attribute memories such as age, occupation, disability, education, gender, or other persona categories. For mitigation experiments, it also uses training examples derived from stable versus drifted reasoning trajectories.

### Outputs
DriftLens outputs value-labeled reasoning trajectories and drift scores comparing no-memory and memory-conditioned trajectories. The mitigation models output ordinary language responses, but are evaluated for capability, instruction following, drift, lexical diversity, helpfulness, and non-distraction.

### Training objective (loss)
The metric itself is not a learned predictor in the main framework. The mitigation section trains models with GRPO rewards tied to trajectory stability metrics such as DTW / SRI and formatting, and with DPO preference losses over symbolic-stability preference pairs. The accessible text reports that these objectives reduce drift with model-dependent tradeoffs.

### Architecture / parameterization
A ground-truth-free evaluation pipeline using LLM-generated or LLM-labeled reasoning trajectories, a value ontology, DTW and SRI trajectory metrics, bootstrap / statistical tests, and optional post-training through GRPO or DPO on smaller open models such as Qwen3-4B, Phi-4-mini-instruct, and Gemma2-2B.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Persistent user memory can personalize an assistant, but it can also make irrelevant attributes shape the reasoning process. For value-laden questions with no ground-truth answer, ordinary accuracy metrics cannot detect this drift.

### 2. What is the method?
For each question, DriftLens builds a no-memory baseline trajectory and compares it to trajectories generated under controlled memory perturbations. It maps reasoning steps to value categories and computes trajectory divergence using DTW and SRI. It validates the metrics with negative and positive controls before running persona-memory experiments.

### 3. What is the method motivation?
If the question does not logically depend on the user's demographic or personal attribute, the model should not silently shift its tradeoffs or justification path because that attribute is stored in memory. The failure is especially dangerous because the final answer can still sound fluent and reasonable.

### 4. What data does it use?
The paper curates open-ended, reasoning-invoking, unverifiable, persona-indifferent questions from public sources. It uses controlled perturbation stimuli for pragmatic noise, user-attribute memories, and major life-event positive controls. The evaluated models include Claude Sonnet 4.6, GPT-OSS-120B, Qwen3-4B, and DeepSeek-R1.

### 5. How is it evaluated?
It evaluates whether perturbations produce drift above noise floors, whether DTW and SRI agree, which memory categories cause the strongest effects, and whether post-training with GRPO or DPO reduces drift without damaging capability, instruction following, diversity, helpfulness, or non-distraction.

### 6. What are the main results?
The paper reports that every persona category on every tested model lies significantly above its pragmatic-noise floor under both DTW and SRI. It reports larger SRI effect sizes for Qwen3-4B, roughly 0.75-0.98, and Claude Sonnet 4.6, roughly 0.77-0.90, with smaller but still separated effects on GPT-OSS-120B and DeepSeek-R1. The mitigation section reports reduced DTW under several GRPO and DPO variants, but with model-dependent tradeoffs.

### 7. What is actually novel?
The novelty is the ground-truth-free trajectory audit for memory-conditioned reasoning. It does not require a correct answer. It asks whether the model's stated decision process is stable under irrelevant stored memories.

### 8. What are the strengths?
The controls are good. Pragmatic noise and major-life-event perturbations give a sanity check that the metric is not merely measuring surface variation. The paper also avoids claiming that every drift is harm; it treats drift categories as auditable risk signals.

### 9. What are the weaknesses, limitations, or red flags?
The framework measures expressed reasoning, not hidden cognition. If a model's chain-of-thought-style text is post-hoc or policy-shaped, the trajectory may be an imperfect proxy. The ontology labeling is also model-mediated, so the audit instrument inherits labeling assumptions. Finally, persona-indifferent question filtering is hard and may not be perfect.

### 10. What challenges or open problems remain?
The biggest open problem is connecting trajectory drift to actual downstream harm or user trust degradation. Another is making memory systems that can distinguish relevant personalization from irrelevant attribute leakage, especially when the user's context is genuinely relevant in some cases.

### 11. What future work naturally follows?
Run DriftLens-style audits on production memory systems, tool-using assistants, therapeutic / coaching agents, educational tutors, and enterprise assistants. Extend the metric beyond expressed text into tool choices, retrieval choices, and refusal / escalation behavior.

### 12. Why does this matter for cabbageland?
OpenClaw has memory. Any long-lived assistant with memory needs this kind of test: does stored context help the task, or does it bend unrelated reasoning? DriftLens gives a concrete way to audit that without pretending every messy human question has a single ground truth.

### 13. What ideas are steal-worthy?
Use within-question no-memory baselines. Treat stored memories as controlled perturbations. Measure reasoning-state drift, not only final answers. Separate harmless wording noise from substantive value-trajectory changes. Evaluate memory mitigations against helpfulness and capability, not just reduced drift.

### 14. Final decision
Keep as a highly relevant evaluation reference. It is not a complete solution to memory safety, but it makes a hidden personalized-assistant failure measurable.
