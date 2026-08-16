# LongHorizon-Harness: Advancing Long-Horizon Agents for Real-World Tasks

## Basic info

* Title: LongHorizon-Harness: Advancing Long-Horizon Agents for Real-World Tasks
* Authors: Ziyu Ma, Hailang Huang, Shun Zou, Yong Wang, Shidong Yang, Yiming Hu, Fei Wei, Xiangxiang Chu
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.01964
* Date surfaced: 2026-08-16
* Why selected in one sentence: It makes long-horizon execution an explicit audited-state problem instead of pretending a growing execution transcript is good enough.

## Quick verdict

* Must read

I inspected the arXiv HTML full text. This is the most relevant paper in the batch because it externalizes task state, separates acting from judging, and gets large gains on real long-horizon benchmarks without needing a new foundation model.

## One-paragraph overview

The paper argues that long-horizon agents fail less because they lack a clever next action and more because they lose track of what is already true. LongHorizon-Harness fixes that by storing progress as structured task state outside the executor transcript and only letting that state change through independent audit reports. Each round follows a Manage-Execute-Audit loop: a manager writes a bounded subtask contract from the current audited state, a fresh-context executor performs the subtask, and a read-only auditor inspects the environment to decide what actually completed. On matched backbones, this lifts Qwen 3.7-Plus from **51.8%** to **80.7%** on WeaveBench, from **69.7%** to **77.2%** on Terminal-Bench 2.1, and from **2.8%** to **8.3%** binary completion on OSWorld 2.0.

## Model definition

### Inputs
The framework takes the original task, the current structured task state, prior audit reports referenced by the manager, and the live environment exposed through either GUI or CLI tools.

### Outputs
It outputs a bounded subtask contract, an executor report, an audit report grounded in read-only environment inspection, and an updated persistent task state whose records are marked completed, pending, blocked, or untrusted.

### Training objective (loss)
There is no new trained agent model in the paper. The contribution is a harness and state-management protocol layered over existing model-and-tool backends.

### Architecture / parameterization
The system is a three-role harness. A manager owns the persistent state, an executor performs one subtask in a fresh bounded context, and an auditor independently verifies the resulting environment. A lightweight adapter lets the same loop run over backends such as Claude Code, Codex CLI, and OpenClaw.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve long-horizon execution failure caused by context rot, task-state loss, and self-assessment errors that propagate through later decisions.

### 2. What is the method?
The method is the Manage-Execute-Audit loop. The manager writes the next contract from explicit state, the executor performs only that contract in a fresh context, and the auditor uses read-only inspection to decide what changed before any persistent state is updated.

### 3. What is the method motivation?
Execution, state maintenance, and completion judgment should not all share the same growing transcript. When the acting agent is also the historian and the verifier, it can record false progress and then build later plans on that fiction.

### 4. What data does it use?
It evaluates on WeaveBench, OSWorld 2.0, and Terminal-Bench 2.1, covering hybrid GUI or CLI workflows, desktop computer-use tasks, and pure command-line tasks.

### 5. How is it evaluated?
It is evaluated by comparing matched backbones with and without the harness on task-level metrics such as WeaveBench PassRate and overall score, OSWorld binary completion and partial score, and Terminal-Bench success rate. The paper also analyzes cost, token usage by role, and performance by task type.

### 6. What are the main results?
With Qwen 3.7-Plus, the harness raises WeaveBench PassRate from **51.8%** to **80.7%**, Terminal-Bench 2.1 success from **69.7%** to **77.2%**, and OSWorld 2.0 binary completion from **2.8%** to **8.3%**. On a 34-task OSWorld 2.0 subset, Claude Opus 4.7 rises from **20.6%** to **35.3%** binary completion. With Codex as executor, the harness reaches **83.1%** on Terminal-Bench 2.1 using GPT-5.6 Luna.

### 7. What is actually novel?
The novelty is not generic planning or subtasking. It is the decision to make audited task state the only persistent cross-round memory, with explicit separation between the role that acts and the role that certifies what became true.

### 8. What are the strengths?
The mechanism is sharp, legible, and transferable. It generalizes across GUI and CLI settings, works with multiple backends, and gives a concrete operational rule for when progress is allowed to persist.

### 9. What are the weaknesses, limitations, or red flags?
Some headline comparisons use official baselines with different privilege settings, so not every row is perfectly matched. The framework also increases token cost in some settings, especially when the auditor has to do expensive recovery work, and it still depends on the underlying model to execute each bounded round competently.

### 10. What challenges or open problems remain?
The open problems are how to make auditing cheaper, how to make task-state schemas richer without becoming bloated, and how to handle ambiguous or partially observed completion conditions in a principled way.

### 11. What future work naturally follows?
Future work should test stronger and cheaper auditors, richer contract construction, multi-agent role specialization, and broader long-horizon settings where user approvals, policy constraints, or external service state become part of the persistent record.

### 12. Why does this matter for cabbageland?
Because it enforces a discipline cabbageland keeps wanting anyway: execution traces are not trustworthy state. Audited facts, bounded contracts, and fresh-context rounds are better primitives for real long tasks.

### 13. What ideas are steal-worthy?
Persist audit reports rather than raw execution history. Keep completion authority read-only. Write explicit task-state records with evidence references. Use fresh-context executors so the actor never drags a whole fossil bed of earlier confusion into the next round.

### 14. Final decision
Keep as a preserved note. This is a real systems paper with a reusable architecture rule, not just another benchmark climb.

## 6. Mandatory critical angles

The paper is strongest on decomposition, controllability, and explicit state. It is also unusually good on interpretability for an agent-harness paper because the persistent state and audit reports are human-readable artifacts. The main caveat is evaluation fairness around unmatched privilege settings and the extra token cost of auditing.

## 7. Writing style

The right tone is strongly approving. The paper earns it by replacing transcript mysticism with explicit verified state transitions.

## 8. Repository output format

Saved as a preserved paper note because the audited-state framing and MEA loop are both likely to remain useful.
