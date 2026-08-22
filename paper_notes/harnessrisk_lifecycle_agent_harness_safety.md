# HarnessRisk: A Lifecycle-Oriented Benchmark for Agent Harness Safety

## Basic info

* Title: HarnessRisk: A Lifecycle-Oriented Benchmark for Agent Harness Safety
* Authors: Yajing Bai, Jinhao Duan, Jie Peng, Xianfeng Wu, Sijia Liu, Song Wang, Tianlong Chen
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.17597
* Date surfaced: 2026-08-22
* Why selected in one sentence: It is one of the clearest recent papers on why agent safety is a property of the deployed harness configuration, not the base model alone.

## Quick verdict

* Must read

I inspected the arXiv HTML full text, especially the lifecycle taxonomy, benchmark design, evaluator validation, and results sections. This paper earns a preserved note because it targets the right unit of failure: not isolated prompt injection or tool misuse, but the full harness lifecycle through which permissions, state, plugins, and consequential actions actually flow. The negative result is sharp and useful: high utility coexists with substantial attack success, model safety rankings flip across harnesses, and even very high explicit risk detection often fails to trigger containment or remediation.

## One-paragraph overview

The paper argues that current agent-safety benchmarks are too narrow because they mostly test one attack class or one execution slice at a time, while real harnesses create risk during configuration, extension, runtime operation, persistent state updates, action control, and incident recovery. To fix that, the authors build HarnessRisk, a benchmark of sandboxed agent workflows that embed adversarial instructions inside otherwise normal artifacts and score not just whether the task was completed, but whether the attack succeeded, whether compromise persisted, and whether the agent explicitly detected the risk. The main finding is that safety depends heavily on the deployed harness and its surrounding controls: the same model can look much safer or much less safe depending on how tools, permissions, provenance, and state are mediated.

## Model definition

### Inputs
Three-turn owner workflows, case-specific files and mock-service state, available tools and permissions, untrusted artifacts carrying adversarial instructions, and full agent trajectories produced by deployed model-harness configurations.

### Outputs
Trajectory-level Utility, Attack Success Rate (ASR), Persistence, and Detection labels, plus aggregate comparisons across lifecycle phases, models, and harnesses.

### Training objective (loss)
The paper does not introduce a new trainable agent model. It uses deployed language models inside three harnesses and applies a GPT-5.4-based evaluator that is validated against deterministic predicates and human reference labels.

### Architecture / parameterization
Lifecycle benchmark plus unified trajectory evaluator over deployed model-harness configurations. The relevant structure is the six-phase harness taxonomy and the four-metric outcome scheme, not a new trainable backbone.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve a framing mistake in agent safety evaluation: treating safety as if it lived mostly inside the base model rather than in the deployed harness that manages tools, state, permissions, extensions, and external actions.

### 2. What is the method?
The method is HarnessRisk, a benchmark of 128 sandboxed cases organized across six lifecycle phases: Harness Configuration, Capability Extension, Runtime Operation, State Persistence, Action Control, and Incident Recovery. Each case embeds an adversarial objective inside an untrusted workflow artifact while asking the agent to complete a benign user task.

### 3. What is the method motivation?
Agent risk can emerge before runtime, after runtime, or through persistent state and recovery channels that single-attack benchmarks do not compare cleanly. The paper wants one protocol that can expose those differences and separate task success from genuine safety.

### 4. What data does it use?
It uses 128 constructed benchmark cases executed across three harnesses, OpenClaw, Hermes, and Nanobot, with six language models and 14 model-harness configurations. Each trajectory starts from a fresh environment with controlled mock services and no real external network access.

### 5. How is it evaluated?
The benchmark scores each trajectory on Utility, ASR, Persistence, and Detection. The evaluator is validated against deterministic predicates and human reference labels, achieving 92.5% agreement for Utility, 89.7% for ASR, 84.3% for Persistence, and 85.7% for Detection.

### 6. What are the main results?
Across the 14 evaluated configurations, attack success ranges from 12.6% to 80.9% while Utility stays between 75.0% and 97.6%. The same model can be over four times less safe under a different harness: GLM-5.2 records 54.7% ASR on OpenClaw but only 12.6% on Nanobot. Useful-but-unsafe outcomes account for 59% of trajectories on OpenClaw, 38% on Nanobot, and 43% on Hermes. Detection correlates with lower ASR, but still does not guarantee safety: MiniMax M3 on OpenClaw detects risks in 97.9% of runs while keeping a 31.2% ASR.

### 7. What is actually novel?
The novelty is the lifecycle organization and the insistence that safety be measured at the deployed model-harness level. The paper does not just add another attack set; it supplies a six-phase taxonomy and a unified scoring protocol that can compare failures across configuration, runtime, persistence, and recovery.

### 8. What are the strengths?
The benchmark targets the right operational unit. The six-phase organization is cleaner than attack-bucket sprawl. The evaluator validation is stronger than many benchmark papers manage. The harness-comparison result is especially important because it punctures simplistic model-only safety narratives.

### 9. What are the weaknesses, limitations, or red flags?
The cases are still authored benchmark workflows rather than arbitrary live deployments. Real external networking is disabled, so some attack surfaces are intentionally excluded. Only three harnesses are tested, and the workflows are fixed at three owner turns, which limits how much long-lived autonomous behavior is exercised.

### 10. What challenges or open problems remain?
The obvious next problems are scaling this evaluation to richer real-world integrations, longer-lived state, more harnesses, and harder recovery tasks where provenance, rollback, and credential rotation interact in messier ways.

### 11. What future work naturally follows?
Future work should benchmark harness-level safeguards directly: stronger provenance preservation, safer state-management schemes, tighter action authorization, plugin isolation, and verified recovery mechanisms. It would also be useful to test how the same policies behave under different memory and tool abstractions.

### 12. Why does this matter for cabbageland?
Because cabbageland cares about real agents, not model demos. This paper is a severe reminder that permissions, persistent state, tool context, and recovery workflow are first-class parts of the safety story. If the harness is weak, model-level alignment can be flatteringly irrelevant.

### 13. What ideas are steal-worthy?
Treat harness lifecycle phases as explicit evaluation axes. Separate useful-but-unsafe from safe-but-useless outcomes. Preserve provenance and authorization context as first-class state. Evaluate recovery as a real capability instead of assuming detection automatically implies remediation.

### 14. Final decision
Keep as a preserved note. The paper nails the right abstraction boundary and produces a result that should change how agent safety is discussed and tested.

## 6. Mandatory critical angles

The paper is strongest on explicit state, persistence, authorization, and evaluation fairness. It earns the harness label because the benchmark actually spans configuration, extension, runtime, memory, action, and recovery rather than just stapling the word onto a prompt-injection suite. The main realism caveat is that the workflows are still sandboxed and curated, but the benchmark is much closer to deployed failure structure than the average single-attack paper.

## 7. Writing style

The right tone is approving but unsentimental. The paper deserves credit for shifting the safety unit from the model to the deployed configuration, and the results are sharp enough that they should not be softened into generic "interesting benchmark" language.

## 8. Repository output format

Saved as a preserved paper note because the lifecycle framing, harness comparison, and persistence/recovery emphasis are likely to stay useful.
