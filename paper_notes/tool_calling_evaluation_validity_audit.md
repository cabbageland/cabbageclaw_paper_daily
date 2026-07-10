# Benchmarking the Benchmarks: A Validity Audit of Tool-Calling Evaluation

## Basic info

* Title: Benchmarking the Benchmarks: A Validity Audit of Tool-Calling Evaluation
* Authors: Vishvesh Bhat, Jay Vaghasiya, Muhammad Ahmed Mohsin, Asad Aali
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.02577
* Date surfaced: 2026-07-10
* Why selected in one sentence: It audits the evaluator layer of tool-agent benchmarks and shows that official scores often disagree with expert trace-level task judgments.

## Quick verdict

* Must read

This is the most important paper in today's scan. It is not another leaderboard wrapper; it asks whether the benchmark verdicts used to rank tool-calling agents are themselves valid and reproducible. I inspected the full PDF, including the audit method, benchmark panel, disagreement tables, LiveMCPBench rerun analysis, Tool-Veritas section, conclusion, and representative failure cases.

## One-paragraph overview

The paper audits four tool-calling benchmark families: BFCL v4, tau2-Bench Retail, LiveMCPBench, and MCP-Atlas. For each audited task, it preserves execution traces, tool calls, outputs, official labels, evaluator diagnostics, and available state, then compares the benchmark label against expert trace-level judgment of whether the user objective was actually achieved. The result is ugly in the useful way: 92 disagreements across 496 reviewed tasks, or an 18.5% aggregate misalignment rate. The failures come from both deterministic and LLM-judge evaluators, including brittle state matching, trajectory lock-in, incorrect ground truth, substring checks, reward-basis mismatch, rubric drift, hallucinated completion, answer-only scoring, and judge variance. The paper also proposes Tool-Veritas and Harness Lab as more auditable evaluation infrastructure.

## Model definition

### Inputs
The audited evaluation stack receives user prompts, tool schemas, initial environment states, agent trajectories, tool calls, tool outputs, final responses, official benchmark verdicts, evaluator logs, and benchmark-specific metadata. Tool-Veritas tasks additionally encode deterministic outcome checks, optional qualitative criteria, and bounded repair windows.

### Outputs
The official benchmarks output binary or scalar task scores. The audit outputs expert pass/fail labels, disagreement direction, failure categories, benchmark-level misalignment rates, repeated-run score variance, and Tool-Veritas agreement statistics.

### Training objective (loss)
The paper does not train a new learned agent. LLM judges inside some benchmark families are evaluated as components, but no new judge training objective is introduced. Tool-Veritas is a deterministic-first evaluator with optional restricted qualitative judging rather than a learned scoring model.

### Architecture / parameterization
The core architecture is an audit and harness stack. Harness Lab preserves raw artifacts, exposes case- and turn-level diagnostics, supports repeated-run comparison and selective retry, and stores human adjudications separately from official labels. Tool-Veritas separates deterministic outcome gates from optional qualitative checks, records whether success occurs initially or after repair, and avoids treating the final natural-language answer as the only evidence of task completion.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Tool-calling benchmarks are being used as proxies for agent capability, but their evaluators are rarely validated. If the scoring code or LLM judge disagrees with what a human trace reviewer would call success, benchmark scores can reward evaluator artifacts rather than actual tool-use ability.

### 2. What is the method?
The method is a trace-level validity audit. The authors reproduce benchmark runs, collect raw traces and evaluator artifacts, have three independent expert annotators judge whether each user objective was achieved, and classify disagreements between official labels and human labels. They also rerun LiveMCPBench 23 times under the same 95-task configuration to measure reproducibility, then evaluate Tool-Veritas against expert judgment on 70 tasks across six models.

### 3. What is the method motivation?
Agent evaluation is only as trustworthy as the evaluator. Deterministic exact-match checks can reject semantically valid alternate solutions, while LLM judges can hallucinate success, drift rubrics, or vary across runs. The paper's premise is that benchmark validity needs evidence, not vibes.

### 4. What data does it use?
The audit covers 496 expert-reviewed tasks: 112 from tau2-Bench Retail, 200 from BFCL v4, 89 from MCP-Atlas, and 95 from LiveMCPBench. It evaluates Kimi-K2.6 on tau2-Bench Retail and MiniMax-M2.7 on BFCL v4, LiveMCPBench, and MCP-Atlas. Tool-Veritas is evaluated on 70 tasks with six models, producing 420 model-task evaluations.

### 5. How is it evaluated?
The main metric is evaluator-human disagreement: official benchmark label versus expert trace-level task success. The paper reports false positives, false negatives, benchmark-specific failure categories, repeated-run score spread for LiveMCPBench, and Tool-Veritas agreement against expert review.

### 6. What are the main results?
Across 496 audited tasks, 92 official labels disagree with expert judgments, for an 18.5% misalignment rate. LiveMCPBench has 30.5% disagreement, BFCL v4 has 20.0%, MCP-Atlas has 13.5%, and tau2-Bench Retail has 9.8%. Across 23 LiveMCPBench reruns, scores range from 57.9% to 76.8%, with mean 69.4%, standard deviation 5.4 percentage points, and spread 18.9 percentage points. Tool-Veritas reaches 95.5% agreement over 420 model-task evaluations, and all 19 disagreements are false negatives rather than false positives.

### 7. What is actually novel?
The novelty is treating tool-agent evaluators as auditable systems with their own validity and reproducibility metrics. The failure taxonomy is also useful because it unifies deterministic benchmark failures and LLM-judge failures under one trace-level lens.

### 8. What are the strengths?
The paper inspects raw traces instead of only aggregate scores. It compares deterministic and LLM-judge paradigms, quantifies repeated-run variance, gives concrete failure categories, and proposes evaluation infrastructure that preserves artifacts instead of hiding scoring behind a final number. The LiveMCPBench rerun result is especially persuasive because a 18.9 point score spread is too large to dismiss as noise.

### 9. What are the weaknesses, limitations, or red flags?
The audit covers a limited number of agents and benchmark configurations. Expert adjudication is itself a human process, and the release status of trace-level artifacts matters for trust. Tool-Veritas is promising but still preliminary, evaluated on 70 tasks rather than at the scale of the audited benchmark ecosystem. The paper reports a lot of infrastructure claims whose usefulness depends on code and artifact release.

### 10. What challenges or open problems remain?
The field needs benchmark packages that make evaluator behavior inspectable by default: raw traces, versioned scorers, deterministic state evidence, repeated-run variance, human-audit hooks, and component metrics. It also needs better standards for when LLM judges are allowed to score qualitative dimensions and when deterministic outcome gates are mandatory.

### 11. What future work naturally follows?
Reaudit more benchmark families, more agents, and frontier-model tool stacks. Build CI-style evaluator regression tests for agent benchmarks. Add score confidence intervals and repeated-run protocols to leaderboards. For production agents, use trace-level task adjudication rather than final-answer scoring.

### 12. Why does this matter for cabbageland?
OpenClaw-style agents live and die by tool traces, delegated sessions, and side effects. This paper says the evaluation layer should look like a serious observability layer: preserve raw traces, distinguish tool invocation from outcome success, track evaluator variance, and audit whether scoring agrees with human intent. That is directly reusable for local agent harnesses.

### 13. What ideas are steal-worthy?
Separate tool invocation correctness, task completion correctness, and outcome verification. Store evaluator labels separately from raw traces. Treat repeated-run spread as a first-class benchmark statistic. Make all scoring disagreements inspectable at the turn level. Prefer deterministic outcome gates for factual side effects and reserve LLM judging for genuinely qualitative criteria.

### 14. Final decision
Preserve. This is a benchmark-validity paper with immediate engineering consequences for agent evaluation.
