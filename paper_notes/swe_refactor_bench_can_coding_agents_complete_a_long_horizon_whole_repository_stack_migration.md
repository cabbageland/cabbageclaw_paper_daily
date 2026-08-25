# SWE Refactor Bench: Can Coding Agents Complete a Long-Horizon, Whole-Repository Stack Migration?

## Basic info

* Title: SWE Refactor Bench: Can Coding Agents Complete a Long-Horizon, Whole-Repository Stack Migration?
* Authors: Deyao Hong, Yizhe Chi, Wenyi Li, Xiaoqiu Wang, Mingju Gao, Kaisen Yang, Bingxiang He, Youjie Zheng, Calvin Xiao, Qinhuai Na
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.23564
* Date surfaced: 2026-08-25
* Why selected in one sentence: It is the sharpest evaluation paper in the batch on separating objective completion from superficial behavioral success in coding-agent benchmarks.

## Quick verdict

* Useful

I inspected the full arXiv HTML text, especially the benchmark framing, the three-stage protocol, the overall results, and the validity analysis. This paper earns a preserved note because it names a benchmark pathology that is both obvious and frequently ignored: an agent can preserve behavior by not performing the migration at all. The paper does the needed boring work of operationalizing that failure instead of hand-waving it away.

## One-paragraph overview

SWE Refactor Bench is a benchmark for coding agents performing whole-repository stack migrations rather than ordinary bug fixes. The key idea is that behavior-only evaluation is blind to whether the requested transformation actually happened. The benchmark therefore uses a three-stage funnel: Migration Audit checks whether the migration was performed, Behavioral Tests check whether the repository still works, and Agentic Verification uses six independent coding agents to generate additional targeted tests for hidden behavioral differences between the original and migrated systems. Across 20 migration tasks and 520 runs, the paper shows that the field is much worse at real migrations than behavior-only success rates would imply.

## Model definition

### Inputs
An untouched code repository plus a specified migration target, such as a framework, toolchain, or language rewrite.

### Outputs
A migrated repository that is supposed to complete the requested transformation while preserving correct behavior.

### Training objective (loss)
There is no trainable model in the paper. It is a benchmark and evaluation protocol for existing coding-agent systems.

### Architecture / parameterization
Three-stage evaluator: Migration Audit, fixed Behavioral Tests, and Agentic Verification using six independent coding-agent verifiers.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the fact that existing coding-agent benchmarks often check only behavioral correctness, which allows agents to pass without performing the requested repository-wide migration.

### 2. What is the method?
Construct 20 whole-repository migration tasks and evaluate solutions with a three-stage protocol that separately checks migration completion, fixed behavioral correctness, and hidden behavioral differences.

### 3. What is the method motivation?
If a benchmark does not verify that the migration happened, an agent can copy or preserve the old implementation and still be rewarded. That is not migration ability. It is evaluation blindness.

### 4. What data does it use?
Twenty migration tasks spanning four kinds of technical debt. The benchmark reports 130,118 fixed behavioral checks and evaluates 520 runs from eight frontier models across 26 effort configurations.

### 5. How is it evaluated?
First by Migration Audit, then by fixed Behavioral Tests, then by Agentic Verification where six independent coding agents each get one hour to probe for hidden differences.

### 6. What are the main results?
Only 28 of 520 runs, or 5.4%, pass all three stages. Thirteen of the 20 tasks receive no accepted solution. The best model scores only 47.0 out of 100. The failure modes split cleanly: 30 runs preserve behavior by skipping the migration and get stopped by Migration Audit, while 252 runs attempt the migration and then fail the fixed tests. Among the 340 runs that pass Migration Audit, 58% reach 99% of fixed checks but only 26% reach 100%. Capability also varies sharply by migration type: agents score 31.4 on build-toolchain rewrites but only 5.6 on language rewrites.

### 7. What is actually novel?
The real novelty is making migration completion a first-class evaluation object and then adding agent-generated hidden tests as a third stage rather than assuming the fixed suite is enough.

### 8. What are the strengths?
The benchmark is structurally right. It does not collapse "objective completed" into "tests passed," and it treats the final 1% of behavioral correctness as a meaningful separate challenge rather than a rounding error. The validity analysis also matters because the paper checks agreement with humans and studies what the verifier stage adds.

### 9. What are the weaknesses, limitations, or red flags?
Twenty tasks is still a small benchmark, and the verifier stage is only as strong as the verifying agents plus the one-hour budget. The task distribution may also overrepresent the kinds of migrations that are easiest to formalize. One should not read this as the final word on repository migration, only as a much better starting point.

### 10. What challenges or open problems remain?
Scaling the task set, broadening migration types, and building stronger verification methods that combine structural diff checks, semantic traces, and independent test synthesis without exploding evaluation cost.

### 11. What future work naturally follows?
Benchmarks for partial migrations, long-lived multi-PR migrations, and migration tasks that require documentation updates, infrastructure changes, and developer ergonomics rather than only code-level transformations.

### 12. Why does this matter for cabbageland?
Because cabbageland cares about coding agents, real objective completion, and evaluation that does not quietly reward the wrong thing. This paper gives a clean pattern for separating "looked good under the current tests" from "actually did the requested work."

### 13. What ideas are steal-worthy?
Always audit the requested transformation directly. Keep behavioral testing, but make it the second gate rather than the only one. Use independent agentic verification to search for hidden differences after the apparent success case.

### 14. Final decision
Keep as a preserved note. Even if the benchmark grows later, the blindness framing is already useful.

## 6. Mandatory critical angles

The paper is strongest on evaluation fairness, failure-mode exposure, and operational honesty. It is less about architecture and more about forcing the benchmark to score the right object. The main limitation is benchmark scale and verifier dependence.

## 7. Writing style

The right tone is approving and unsentimental. The paper is valuable because it does not let benchmark theater masquerade as progress.

## 8. Repository output format

Saved as a preserved paper note because the migration-audit framing is a durable evaluation idea for future coding-agent work.
