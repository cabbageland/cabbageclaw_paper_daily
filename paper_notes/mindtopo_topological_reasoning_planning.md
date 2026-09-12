# MindTopo: Can Foundation Models Reason in Topological Space?

## Basic info

* Title: MindTopo: Can Foundation Models Reason in Topological Space?
* Authors: Yunfei Ge, Anbang Liu, Qineng Wang, Johnalbert Garnica, Jianwen Lyu, Zihan Wang, Reuben Tan, Jianfeng Gao, Ruohan Zhang, Yining Hong, Jiajun Wu, Manling Li
* Year: 2026
* Venue / source: arXiv:2609.11900
* Link: https://arxiv.org/abs/2609.11900
* Date surfaced: 2026-09-12
* Why selected in one sentence: It tests whether models can preserve topological invariants through both static reasoning and interactive planning, which is a better probe for world-model claims than ordinary metric spatial QA.

## Quick verdict

* Must read

MindTopo is a benchmark rather than a method paper, but it is a good benchmark in the way this repo cares about: it asks whether the state variable that matters survives across action. The reasoning/planning split is especially useful because it shows that naming a topological relation and acting under it are not the same capability. Full arXiv HTML inspected.

## One-paragraph overview

The paper introduces MindTopo, a benchmark for topological intuition across continuity, separation, order, enclosure, and knots. Each property is tested at two cognitive levels: reasoning tasks ask models to identify or predict topological relations from rendered scenes, while planning tasks instantiate an environment where actions must preserve or exploit the relation. The dataset has 11,030 instances across 13 procedurally generated task types. Experiments on 14 MLLMs show a consistent reasoning-to-planning drop, training probes on Qwen3-VL-2B improve reasoning much more than planning, and video-generation rollouts can look locally plausible without preserving topology through dynamics.

## Model definition

The paper is primarily a benchmark. The learned systems are evaluated foundation models and training probes, not a new model architecture.

### Inputs

Rendered scenes, task instructions, and for planning tasks an interactive environment state plus history of previous actions. Some probes use generated visual observations or explicit state representations.

### Outputs

For reasoning, scalar or structured answers about topological relations. For planning, action sequences executed in the environment. For training probes, the output is the same answer or action format after SFT, GRPO-style RL, or SFT plus RL.

### Training objective (loss)

The benchmark itself has no training objective. The paper's Qwen3-VL-2B experiments use answer-only supervised fine-tuning and reinforcement learning; the exact optimization details are in the appendix, and the note does not need them to understand the main result.

### Architecture / parameterization

The evaluated systems are multimodal LLMs, video generative models used as imagined observation sources, and Qwen3-VL-2B-Instruct in SFT/RL variants. The benchmark environments and ground truth are programmatic.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It argues that spatial reasoning benchmarks overemphasize metric or viewpoint-dependent relations and under-test topology: relations that remain invariant under continuous deformation and matter for physical action.

### 2. What is the method?

MindTopo builds 13 procedural task types over five topological primitives. Each primitive has reasoning tasks and at least one matched planning environment, allowing separate measurement of static topological recognition and action-conditioned topological control.

### 3. What is the method motivation?

Real spatial intelligence often depends on continuity, enclosure, connectivity, order, separation, and knots, not just Euclidean distance. A world model that cannot preserve these invariants through action is weaker than its static scene answers suggest.

### 4. What data does it use?

It uses programmatically generated scenes and environments: 8,030 reasoning questions and 3,000 planning episodes, for 11,030 instances total. Human performance is also measured for comparison.

### 5. How is it evaluated?

Reasoning tasks are scored by exact answer accuracy. Planning tasks are scored by executing model actions in the environment and measuring episode success. The paper also audits error categories and tests training interventions on Qwen3-VL-2B.

### 6. What are the main results?

Every MLLM performs better on reasoning than planning. GPT-5.6-Sol, for example, is reported at 66.83% reasoning versus 52.75% planning, while several other strong models drop much more sharply. Human performance is reported at 97.87%. On Qwen3-VL-2B, SFT plus GRPO raises selected reasoning average from 14.24% to 51.53%, but planning success rises only from 0.20% to 6.33%.

### 7. What is actually novel?

The useful novelty is the coupled reasoning/planning topology design. Existing benchmarks may include spatial puzzles or topology fragments, but this one explicitly organizes five topological primitives across static and interactive settings.

### 8. What are the strengths?

The primitive taxonomy is clean. The programmatic generation gives ground truth. The error analysis separates visual grounding failures from downstream state-prediction, dynamic, and planning failures. The benchmark directly attacks inflated "spatial reasoning" claims.

### 9. What are the weaknesses, limitations, or red flags?

Benchmarks can become overfit targets. The procedural environments may still be toy worlds. High performance on MindTopo would not certify broad physical grounding, and poor performance may sometimes reflect prompt/action-format friction rather than topology alone.

### 10. What challenges or open problems remain?

The main challenge is building systems that maintain topological state through action, not just recognize it in a still image. The gap between generated plausible endpoints and valid topological rollouts is especially important.

### 11. What future work naturally follows?

Use MindTopo-like tasks as a diagnostic suite for video world models, embodied planners, and simulator-grounded training. Add richer physical manipulation tasks where topology changes through contact, occlusion, cutting, tying, and containment.

### 12. Why does this matter for cabbageland?

Cabbageland cares about explicit state and compositional world models. Topological relations are compact state variables that should govern planning, memory, and generation. This paper gives a concrete way to punish models that only look spatially competent.

### 13. What ideas are steal-worthy?

Split every "the model understands X" claim into static identification and action-preserving control. Build benchmarks around invariants, not labels. Audit whether generative rollouts preserve the invariant, not whether endpoints look plausible.

### 14. Final decision

Preserve. This is a direct reference for evaluating spatial world models and embodied reasoning claims.
