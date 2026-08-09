# CalibForge: Adversarial Solver Calibration for Scaling Learnable Terminal Tasks

## Basic info

* Title: CalibForge: Adversarial Solver Calibration for Scaling Learnable Terminal Tasks
* Authors: Fanzhe Meng, Guoxin Chen, Jiale Zhao, Shuang Sun, Zhiyu Lin, Wayne Xin Zhao, Ruihua Song, Ji-Rong Wen, Kai Jia
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.06352
* Date surfaced: 2026-08-09
* Why selected in one sentence: It turns synthetic terminal-task generation into a solver-relative calibration loop instead of a blind volume game.

## Quick verdict

* Highly relevant

I inspected the arXiv HTML full text. This is one of the better recent synthetic-supervision papers because it changes the quality criterion for generated tasks instead of just generating more of them. The author-solver loop is procedural, but the calibration logic is the real contribution.

## One-paragraph overview

CalibForge targets a familiar failure mode in agent training: synthetic terminal tasks are easy to mass-produce, but many are trivial, noisy, underspecified, or miscalibrated to the target solver. The paper treats task generation as an adversarial calibration problem. An authoring agent turns a terminal clue into a candidate task and verifier, then designated solver agents attempt it. Their outcomes drive deterministic revision: tasks are simplified if nobody can solve them for good reasons, stripped of leakage if everybody solves them too easily, and repaired if weaker-versus-stronger solver behavior exposes misleading specifications or verifier issues. The paper instantiates this with both multi-solver calibration and stronger/weaker contrastive calibration, producing 5,431 retained tasks across 16 categories. Models trained on these tasks outperform strong released synthetic-terminal baselines on Terminal-Bench 2.0 and transfer better to SWE-bench Pro and Doc2Repo.

## Model definition

### Inputs
The pipeline takes seed terminal clues, generated candidate tasks with verifiers, solver trajectories from multiple LLM agents, and calibration outcomes across revision rounds.

### Outputs
It outputs calibrated terminal-task instances, distilled training trajectories, and trained terminal-agent models evaluated on held-out benchmarks.

### Training objective (loss)
The task-construction loop itself is not optimized with a single explicit differentiable loss. Downstream agent models are trained by supervised fine-tuning on distilled successful trajectories from the calibrated task set.

### Architecture / parameterization
An author-solver synthetic-data pipeline with two calibration modes: multi-solver calibration over several designated solvers and contrastive calibration between stronger and weaker solvers, followed by trajectory distillation and supervised fine-tuning of terminal agents.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to produce synthetic terminal tasks that are learnable, nontrivial, and useful for training terminal agents, instead of flooding training with poorly calibrated or contaminated tasks.

### 2. What is the method?
An authoring agent drafts task instances and verifiers from terminal clues. Solver agents then attempt each task. Their success or failure patterns determine whether the task is retained, revised, simplified, or flagged for leakage or verification issues. This loop runs under either multi-solver or stronger/weaker contrastive calibration.

### 3. What is the method motivation?
Raw synthetic task volume is a bad proxy for supervision quality. If the tasks are too easy, too hard, leaky, or ambiguous, the agent learns the wrong thing or wastes training budget.

### 4. What data does it use?
The paper constructs 5,431 calibrated tasks across 16 terminal-task categories: 1,263 from multi-solver calibration and 4,168 from contrastive solver calibration. It evaluates trained models on Terminal-Bench 2.0, SWE-bench Pro, and Doc2Repo.

### 5. How is it evaluated?
It trains matched backbone models on CalibForge and prior released task sets under a shared protocol, then compares task accuracy on Terminal-Bench 2.0 plus out-of-distribution transfer on SWE-bench Pro and Doc2Repo.

### 6. What are the main results?
On Terminal-Bench 2.0, CalibForge-30B-A3B reaches 32.58% and CalibForge-35B-A3B reaches 47.57%, beating the strongest shared-protocol baselines by 6.36 and 6.75 percentage points. The gains hold across benchmark categories rather than a narrow slice, and the trained models also transfer better to repository-level generation and issue-resolution benchmarks.

### 7. What is actually novel?
The novelty is not synthetic task generation by itself. The contribution is solver-relative calibration: retaining or revising tasks according to structured solver outcome patterns rather than treating all generated tasks as equally useful supervision.

### 8. What are the strengths?
The paper is disciplined about training-protocol control, task decontamination, and calibration logic. The stronger/weaker contrastive setup is especially useful because it targets the learning frontier instead of only average solvability.

### 9. What are the weaknesses, limitations, or red flags?
The whole pipeline is still expensive and heuristic. Calibration depends on the chosen solver set, and there is still no deep theory for why a particular retention rule is the right frontier for future solvers. It is also mainly a data-generation contribution, not a new planning architecture.

### 10. What challenges or open problems remain?
The hard open problem is adaptive calibration over rapidly changing solver families, where today's "just-right" difficulty becomes tomorrow's triviality. Another challenge is extending the method from terminal tasks to richer multi-tool, multi-file, or long-horizon software environments.

### 11. What future work naturally follows?
Online curriculum updates with changing solver pools, calibration rules conditioned on capability subskills, and similar stronger/weaker calibration loops for browser, multimodal, or repository-grounded agent tasks.

### 12. Why does this matter for cabbageland?
Cabbageland cares about learnable structured tasks, agent training data quality, and capability shaping. This paper provides a concrete way to think about synthetic supervision as a calibrated frontier object instead of a static dataset dump.

### 13. What ideas are steal-worthy?
Use stronger/weaker solver disagreement as a supervision-quality signal. Treat universal success as possible leakage and universal failure as a possible specification problem. Keep a bounded author-solver revision loop. Evaluate synthetic corpora under a matched training recipe so the data source is the main changing variable.

### 14. Final decision
Keep as a preserved note. It is more procedural than conceptual, but the solver-calibration framing is strong enough to reuse in future synthetic-agent-data work.

## 6. Mandatory critical angles

CalibForge is strongest on motivation, data realism relative to training use, and evaluation discipline. Its mechanism really does alter which tasks survive. The main caution is transfer over time: calibration tied to current solver families can age quickly.

## 7. Writing style

The right reading stance is pragmatic. This is not a new theory of agency. It is a well-aimed intervention on the quality of synthetic supervision.

## 8. Repository output format

Saved as a preserved paper note because the solver-relative calibration logic is directly relevant to synthetic-task generation for future agent training pipelines.
