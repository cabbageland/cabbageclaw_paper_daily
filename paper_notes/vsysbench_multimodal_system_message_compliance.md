# Compliance, Capability, and Conflict: Benchmarking Multimodal LLMs under System Messages

## Basic info

* Title: Compliance, Capability, and Conflict: Benchmarking Multimodal LLMs under System Messages
* Authors: Juan Yeo, Geewook Kim
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.19207
* Date surfaced: 2026-08-22
* Why selected in one sentence: It is one of the cleaner recent papers on evaluating whether multimodal system-message compliance survives conflict without hiding its capability cost.

## Quick verdict

* Highly relevant

I inspected the arXiv HTML full text, especially the benchmark design and overall/category-level results. This paper earns a preserved note because it scores correctness and constraint-following jointly on the same multimodal instance instead of letting either metric hide the other. The result is a useful negative picture: system messages impose a universal capability tax, open-weight models are brittle under user conflict, and even the strongest models still fail to reach a genuinely good compliance-capability frontier.

## One-paragraph overview

The paper introduces VSysBench, a multimodal benchmark built to test system-message adherence rather than plain user-instruction following. Each example pairs an image task with system-level constraints spanning format, style, background knowledge, content, and image-grounded requirements, then optionally introduces a misaligned user message that pressures the model to violate the hierarchy. The key move is the evaluation protocol: instead of scoring compliance or accuracy separately, it uses Joint Satisfaction Rate (JSR) and Cross-Constraint Sensitivity (CCS) so a model cannot hide behind being correct while noncompliant or compliant while wrong.

## Model definition

### Inputs
Images, system messages specifying multimodal constraints, aligned or misaligned user messages, and frozen MLLM responses from 16 evaluated systems.

### Outputs
Task answers plus benchmark metrics including Constraint Satisfaction Rate (CSR), Task Accuracy (TA), Joint Satisfaction Rate (JSR), and Cross-Constraint Sensitivity (CCS).

### Training objective (loss)
The paper does not introduce a new trainable MLLM. It evaluates existing open-weight and proprietary multimodal models under a new benchmark and verifier setup.

### Architecture / parameterization
Benchmark-and-metrics paper over frozen MLLMs. The main structure is the VSysBench taxonomy and the joint compliance/correctness scoring framework rather than a new model architecture.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the lack of a good multimodal benchmark for system-message adherence that also measures what those constraints cost in ordinary task capability and how easily they break under direct user conflict.

### 2. What is the method?
The method is VSysBench, a benchmark built on MMVet-v2 with 5 main constraint categories and 22 sub-categories, each paired with aligned and misaligned variants, and evaluated with joint metrics that score both compliance and answer correctness.

### 3. What is the method motivation?
Production multimodal systems increasingly rely on system messages, but prior benchmarks either test text-only constraints or embed the instruction into the user turn. That hides whether the model is respecting the intended hierarchy and whether doing so wrecks actual visual reasoning.

### 4. What data does it use?
The benchmark is built from MMVet-v2-derived multimodal tasks and covers 16 MLLMs: open-weight systems such as LLaVA, InternVL, Qwen3-VL, and Phi-4-Multimodal, plus proprietary GPT, Claude, and related frontier systems.

### 5. How is it evaluated?
It evaluates aligned and misaligned settings with CSR, TA, JSR, and CCS, then also breaks performance down by constraint category to see whether failures are mostly textual, stylistic, factual, or vision-grounded.

### 6. What are the main results?
System messages impose a 30-70% task-accuracy penalty across every evaluated model family. GPT-5.4 and Claude-Opus-4.7 lead overall, but only reach 36.2% total JSR. Under user conflict, GPT-5.4 retains 83.3% misaligned CSR while Qwen3-VL-32B collapses to 8.4%, and larger Qwen models actually do worse on misaligned compliance than smaller ones. Vision-grounded constraints are the hardest category for every model. The paper also surfaces fragile superficial compliance: Qwen3-VL-32B drops from aligned Format JSR 35.7 to misaligned 1.2, a 97% collapse.

### 7. What is actually novel?
The novelty is the joint evaluation frame. The benchmark does not merely ask whether a model followed a constraint or answered correctly; it scores both on the same instance and adds adversarially misaligned user turns to stress the system-message hierarchy directly.

### 8. What are the strengths?
The benchmark targets a real deployment problem. The JSR/CCS framing is better than single-axis metrics. The proprietary-versus-open governance gap is concrete rather than hand-wavy. The category analysis is useful because it shows that image-grounded constraints are a different failure mode from plain textual formatting.

### 9. What are the weaknesses, limitations, or red flags?
It is still a benchmark paper, so the main contribution is measurement rather than mechanism. The verifier may inherit some judgment noise even though robustness checks are reported. The setting is multimodal QA-like behavior, not full agent workflows with tools, memory, or longer temporal state.

### 10. What challenges or open problems remain?
The main open problem is how to improve system-message governance without paying such a heavy capability tax or collapsing under user conflict. Another is extending this style of evaluation beyond image-question settings into longer, tool-using multimodal agents.

### 11. What future work naturally follows?
Future work should test architectural or training interventions that explicitly preserve hierarchy under conflict, especially for vision-grounded constraints. It would also be useful to carry the JSR/CCS idea into agentic multimodal workflows.

### 12. Why does this matter for cabbageland?
Because cabbageland cares about instruction hierarchy, tool governance, and whether a system keeps its rules when the user or environment pushes against them. This paper gives a sharper measurement lens for that problem in the multimodal setting.

### 13. What ideas are steal-worthy?
Score compliance and capability jointly on the same instance. Add misaligned user turns explicitly rather than assuming clean inputs. Separate vision-grounded constraints from format/style constraints. Treat category balance as an additional frontier signal rather than only looking at one top-line metric.

### 14. Final decision
Keep as a preserved note. The benchmark framing is strong, the failure picture is concrete, and the joint metrics are worth reusing.

## 6. Mandatory critical angles

The paper is strongest on controllability, evaluation fairness, and failure modes under conflicting instructions. It earns the system-message label because it really does isolate the system-message hierarchy rather than folding everything into the user prompt. The main limit is that it still lives in benchmarked multimodal question answering, not full agent workflows.

## 7. Writing style

The right tone is measured but unsparing. The paper is valuable because it shows that current multimodal alignment is much shallower than top-line competence numbers suggest.

## 8. Repository output format

Saved as a preserved paper note because the benchmark design and joint metrics should stay useful as reference points for future multimodal-governance work.
