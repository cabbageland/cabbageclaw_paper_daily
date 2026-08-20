# FACET: Preserving Source Intent and Executable State in Terminal Task Synthesis

## Basic info

* Title: FACET: Preserving Source Intent and Executable State in Terminal Task Synthesis
* Authors: Kou Shi, Zun Wang, Qisheng Su, Shiting Huang, Ziao Zhang, Zhen Fang, Qingnan Ren, Jin Liu, Yu Zeng, Yiming Zhao, Lin Chen, Zehui Chen, Feng Zhao
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.18580
* Date surfaced: 2026-08-20
* Why selected in one sentence: It is the cleanest paper in the batch on executable-state discipline for terminal agents and synthetic terminal-task construction.

## Quick verdict

* Must read

I inspected the arXiv HTML full text. This is the sharpest terminal-task synthesis paper in the batch because it does not pretend that an instruction, a container, a solution, and a verifier will stay aligned if they are generated from drifting intermediate artifacts. The paper makes shared executable state the actual design object and gets real data-efficiency gains out of that choice.

## One-paragraph overview

FACET is a synthetic terminal-task construction pipeline that starts from related agent skills or source materials, reconstructs them into coherent scenarios, realizes and repairs the execution environment, and only then generates the task artifacts. The key move is to let the realized container state serve as shared grounding for the instruction, reference solution, and verifier. That sounds obvious, but most synthetic pipelines do not really do it. FACET then validates and selectively repairs artifact-specific failures without throwing away the rest of the bundle. The output is a set of denser, harder, more executable tasks whose successful trajectories are good enough to fine-tune smaller terminal agents meaningfully.

## Model definition

### Inputs
The system takes related agent skills or source materials, LLM-based generation stages, and a realizable terminal environment that can be built, executed, and checked.

### Outputs
It outputs a task bundle consisting of an instruction, an initialized environment, a reference solution, an executable verifier, and runtime metadata. It also produces successful agent trajectories on validated tasks for downstream supervised fine-tuning.

### Training objective (loss)
FACET itself is a synthesis pipeline, not a new trainable model with a single end-to-end loss. The downstream training signal is supervised fine-tuning on approximately 1.2K successful terminal-agent trajectories.

### Architecture / parameterization
The architecture is a multi-stage LLM-guided pipeline with scenario reconstruction, environment realization and repair, shared-state artifact generation, execution-based validation, and targeted artifact repair. The downstream agent fine-tuning is evaluated on Qwen3.5 models at 4B, 9B, and 27B.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve a quality bottleneck in synthetic terminal supervision: the instruction, environment, solution, and verifier are often generated from inconsistent assumptions, which quietly makes tasks invalid or badly graded.

### 2. What is the method?
The method is to reconstruct related skills into a coherent scenario, instantiate the environment first, use the realized state as shared grounding for all task artifacts, then validate and selectively repair failures.

### 3. What is the method motivation?
Terminal tasks are not text-only prompts. They are executable bundles whose validity depends on cross-artifact consistency. If the artifacts do not point to the same executable state, the whole task can become unsolvable or incorrectly judged.

### 4. What data does it use?
The paper reports **6,078** validated tasks with an average of **22.77** executable checks per task, and collects about **1.2K** successful agent trajectories for fine-tuning. It evaluates on Terminal-Bench 2.1 and compares against existing terminal datasets.

### 5. How is it evaluated?
It is evaluated by comparing the resulting dataset against existing terminal-agent datasets at both task and trajectory levels, then fine-tuning Qwen3.5 models and measuring Terminal-Bench 2.1 performance under a shared evaluation scaffold.

### 6. What are the main results?
FACET produces longer-horizon trajectories and the densest verifier structure among the compared datasets. Fine-tuning on only **1.2K** successful trajectories yields consistent Terminal-Bench 2.1 gains: **17.60 -> 24.72** for 4B, **27.34 -> 35.58** for 9B, and **40.82 -> 47.57** for 27B. The 27B FACET-tuned model lands only **1.49** points below a **397B** Qwen row evaluated under the same setting.

### 7. What is actually novel?
The novelty is not just "more synthetic terminal data." It is forcing instruction, solution, and verifier generation to share one realized executable state and repairing artifact-specific failures without regenerating the entire task from scratch.

### 8. What are the strengths?
The design rule is simple, concrete, and correct. The dataset ends up genuinely stricter, with far more executable checks than typical terminal sets. The downstream gains are also impressively data-efficient instead of just reflecting brute-force scale.

### 9. What are the weaknesses, limitations, or red flags?
The paper is still tied to one particular synthesis ecology and one benchmark family. A dense verifier can make tasks harsher without necessarily making them more semantically representative. And the downstream success still depends on the base agent scaffold rather than on FACET alone.

### 10. What challenges or open problems remain?
The main open problem is how to generalize the shared-state discipline to broader, messier, and more heterogeneous terminal tasks without overfitting to one environment-construction pipeline.

### 11. What future work naturally follows?
Future work should test the same principle in other tool-use environments, vary the source-material types more aggressively, and benchmark how much each synthesis stage contributes to final task validity.

### 12. Why does this matter for cabbageland?
Because it names a failure mode that bites mixed-format agent work constantly: if the search surface, executable surface, and grading surface drift apart, capability claims become partly fake. This paper gives a direct rule for designing around that.

### 13. What ideas are steal-worthy?
Use realized executable state as shared grounding. Repair artifact-specific failures instead of regenerating everything. Prefer denser executable checks over vague success conditions. Treat cross-artifact consistency as a first-class data-quality constraint.

### 14. Final decision
Keep as a preserved note. The paper is concrete, severe, and likely to stay useful.

## 6. Mandatory critical angles

This paper is strongest on explicit state, controllability, and evaluation fairness. It replaces fuzzy synthetic-data optimism with a real executable-state discipline. The main caution is that it still lives inside one benchmark and scaffold ecology.

## 7. Writing style

The right tone is severe and approving. The paper earns respect by being less magical than the average synthetic-data paper.

## 8. Repository output format

Saved as a preserved paper note because the executable-state rule is broadly reusable for terminal-agent data construction and evaluation.
