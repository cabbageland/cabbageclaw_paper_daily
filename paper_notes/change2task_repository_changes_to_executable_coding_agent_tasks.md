# Change2Task: From Repository Changes to Executable Coding Agent Tasks and Environments

## Basic info

* Title: Change2Task: From Repository Changes to Executable Coding Agent Tasks and Environments
* Authors: Haomin Qi, Xingliang Wang, Xuanqi Gao, Baihui Sang, Xin Zhang, Minghua Ma, Pengfei Gao, Yu Kang, Qingwei Lin, Saravan Rajmohan, Dongmei Zhang, Qi Zhang
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.28591
* Date surfaced: 2026-07-31
* Why selected in one sentence: It treats merged PR history as raw material for modern executable coding-agent tasks instead of leaving useful developer-grounded changes stranded in old snapshots.

## Quick verdict

**Highly relevant**

This is a strong infrastructure paper because it attacks the right bottleneck: task supply with runnable environments. I inspected the full arXiv PDF, especially the framework overview, Patch Reversal / Code Mapping / Agent Reconstruction pipeline, lifecycle and fidelity gates, comparative evaluation, cost accounting, and limitations. The main caveat is scope: the method depends on traceable PR evidence, a healthy descendant revision, and executable checks, so it does not magically recover every maintenance obligation.

## One-paragraph overview

Change2Task turns merged pull requests into executable coding-agent tasks on healthy modern revisions of the same repository. Instead of binding each task forever to its original historical snapshot, the system uses a three-level construction ladder. It first tries Patch Reversal when the historical change can be reversed directly on a modern base. If direct replay fails but source blocks still correspond, it uses Code Mapping. If the behavior still exists but structure has drifted too much, it uses Agent Reconstruction, where Claude Code with Opus 4.8 proposes scoped modern task variants under lifecycle, restoration, and fidelity checks. The result is a larger pool of developer-grounded tasks extracted from maintained environments, with lower storage and setup overhead than task-per-snapshot approaches.

## Model definition

### Inputs
The system takes source PR evidence, the implementation patch, tests or behavioral checks, a healthy descendant revision in the same repository, task-family adapters, and in Level 3 the modern repository context plus feedback to the reconstruction agent.

### Outputs
The output is a finalized executable task package containing a healthy base, a task-inducing patch, target and regression checks, restoration information, provenance, and metadata for coding-agent evaluation.

### Training objective (loss)
The paper does not train a new model. Agent Reconstruction uses Claude Code with Opus 4.8 in a bounded construction loop, but the contribution is the task-construction framework and validation pipeline rather than task-specific model optimization.

### Architecture / parameterization
This is a hybrid systems pipeline with three escalating construction routes: deterministic Patch Reversal, deterministic Code Mapping, and agent-assisted Reconstruction. A fidelity gate compares modern reconstructed changes to the historical source change profile, and lifecycle / scope / restoration checks decide acceptance.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the shortage of executable coding-agent data. Historical PRs contain real maintenance intent, but they are tied to old repository states, while building fresh environments for every task is expensive.

### 2. What is the method?
The method is to reconstruct developer-grounded historical changes on healthy modern descendants using a three-level escalation path, then qualify the result with lifecycle, scope, restoration, and fidelity checks before releasing it as an executable task.

### 3. What is the method motivation?
Coding agents need realistic tasks with working environments, tools, and verifiers. Old benchmark snapshots age badly, while synthetic tasks can lose real maintenance intent. Repository lineage gives a way to refresh grounded tasks on maintained code.

### 4. What data does it use?
The evaluation starts from 1,130 construction-eligible source changes and finalizes 900 paired tasks across five task families: Bug Fix, Feature Addition, Test Generation, API Migration, and Security Repair. The corpora are public Python and Java software repositories, and agent evaluation covers four coding-agent configurations.

### 5. How is it evaluated?
It is evaluated by task-construction success, source change profile fidelity, comparison against a PR-based construction baseline, matched agent outcome agreement between historical and reconstructed tasks, and accounting for environment time, storage, and end-to-end expenditure.

### 6. What are the main results?
Across the 1,130 eligible changes, Change2Task achieves 79.6 percent verified task construction success, yielding 900 paired tasks. On a matched Bug Fix candidate set it reconstructs 500 tasks versus 387 for the baseline, a 29.2 percent gain. Finalized tasks have 0.894 weighted source change profile fidelity and up to 98.0 percent matched outcome agreement under agent evaluation. Reusing 388 healthy modern bases reduces amortized environment time by 58.4 percent, storage by 71.2 percent, and overall expenditure by 10.8 percent.

### 7. What is actually novel?
The novelty is not just "use PR history." The new piece is the maintained-base reconstruction framework with escalating construction routes, restoration-aware lifecycle checks, and an explicit fidelity gate that measures how closely the modern task still matches the source maintenance change.

### 8. What are the strengths?
The framework is practical and grounded in real developer evidence. The three-level escalation path is sensible. The lifecycle and restoration checks prevent fake tasks from slipping through. The cost analysis is also useful because it shows why modern-base reuse matters operationally.

### 9. What are the weaknesses, limitations, or red flags?
Eligibility is narrower than the headline might suggest. The method needs a traceable PR, executable checks, an identifiable behavior that still exists in the descendant code, and a stable modern execution path. It is also only evaluated on five task families, two main language families, and a limited set of agent interfaces.

### 10. What challenges or open problems remain?
The biggest remaining challenge is extending this approach to tasks whose behavior is not well captured by ordinary tests, such as UI changes, distributed-service behavior, hardware interaction, or performance obligations. Another is broadening language and repository coverage.

### 11. What future work naturally follows?
Future work should add more task families, richer project-specific oracles, broader language support, and better support for obligations expressed through interfaces or system behavior rather than unit tests alone.

### 12. Why does this matter for cabbageland?
It matters because cabbageland repeatedly needs more high-quality coding-agent tasks without paying the full environment-construction tax every time. This paper offers a strong recipe for turning repository lineage into modern, runnable, developer-grounded evaluation and training data.

### 13. What ideas are steal-worthy?
Reuse healthy modern bases. Escalate from deterministic patch replay to correspondence mapping to agentic reconstruction instead of forcing one method to handle every case. Measure modern reconstructions against the source change profile rather than only asking whether tests pass.

### 14. Final decision
**Keep it.** This is a direct infrastructure contribution with immediate value for coding-agent dataset construction and benchmark maintenance.
