# Do Agent Optimizers Compound? A Continual-Learning Evaluation on Terminal-Bench 2.0

## Basic info

* Title: Do Agent Optimizers Compound? A Continual-Learning Evaluation on Terminal-Bench 2.0
* Authors: Wenxiao Wang, Priyatham Kattakinda, Soheil Feizi
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.14004
* Date surfaced: 2026-07-16
* Why selected in one sentence: It tests the only question that really matters for agent harness optimization loops: whether a strong first optimization round survives new tasks and a second round without regressing.

## Quick verdict

**Must read**

This is a strong evaluation paper because it attacks a real blind spot rather than inventing a new optimizer slogan. The paper separates static benchmark improvement, transfer to newly introduced tasks, and second-round improvement under repeated optimization. That split is more useful than yet another leaderboard delta. I inspected the full arXiv HTML paper, including the phased protocol, task split, baseline agent configuration, main results, limitations, and the appendices describing the optimizer edits.

## One-paragraph overview

The paper builds a two-phase continual-learning evaluation on hard Terminal-Bench 2.0 tasks. In Phase 1, three optimizers -- GEPA, Meta Harness, and RELAI-VCL -- each optimize the same baseline coding agent on an initial task set `T1`. The resulting agent is then tested both on `T1` and on the expanded union `T1 U T2`, where `T2` contains newly introduced hard tasks. In Phase 2, each optimizer gets a second optimization budget starting from its own Phase-1 result and optimizes on the combined task set. This design isolates whether an optimizer overfits the first task batch, transfers to unseen tasks, and keeps improving when the task set expands.

## Model definition

### Inputs
The baseline agent receives Terminal-Bench task instructions plus access to shell execution, task completion, and image-reading tools inside a terminal-based harness. The optimizers receive rollout traces, evaluation feedback, and their own optimizer-specific search space over prompts or harness code.

### Outputs
The baseline agent outputs tool calls and terminal actions to solve benchmark tasks. The optimizers output edited prompts, harness code, or full agent-package changes depending on the method.

### Training objective (loss)
There is no gradient-based training of model weights in this paper. Each optimizer searches over harness changes using a fixed rollout budget and accepts candidates based on benchmark pass-rate improvements under the phased evaluation protocol.

### Architecture / parameterization
All methods start from the same baseline agent, TerminusKira, which wraps a Harbor-compatible terminal agent around `openai/gpt-5.5` with three tools: `execute_commands`, `task_complete`, and `image_read`. GEPA edits the system prompt, Meta Harness edits harness code, and RELAI-VCL edits the broader agent package with regression-aware search constraints.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It asks whether agent harness optimizers actually compound under repeated use, or whether they merely score well on one fixed benchmark pass and then regress when new tasks appear.

### 2. What is the method?
The method is a phased continual-learning benchmark. `T1` contains 12 hard Terminal-Bench tasks with 900-second timeouts. `T2` adds 10 more hard tasks with 1800-second timeouts. Each optimizer gets equal budgets for Phase 1 on `T1` and Phase 2 on `T1 U T2`, and the paper compares static performance, transfer, re-optimization, and lifelong average pass rate.

### 3. What is the method motivation?
A single post-optimization benchmark score is too easy to game. Real deployment means new failures and new task types appear over time, so the right question is whether the optimizer's first-round "improvements" generalize and whether the next round can build on them without unwinding earlier gains.

### 4. What data does it use?
It uses 22 hard Terminal-Bench 2.0 tasks split across `T1` and `T2`, spanning areas like systems programming, cryptography, machine-learning infrastructure, graphics, and bioinformatics.

### 5. How is it evaluated?
The main metrics are Phase 1 pass rate on `T1`, transfer performance on `T1 U T2` before re-optimization, Phase 2 pass rate after re-optimization on `T1 U T2`, and lifelong average pass rate across the stages.

### 6. What are the main results?
All three methods improve over the baseline in the static Phase 1 setting, but only one survives the continual-learning test cleanly. RELAI-VCL reaches `79.2%` on Phase 1, transfers at `72.7%`, reaches `77.3%` after Phase 2 re-optimization, and finishes with a `76.4%` lifelong average. GEPA reaches `70.8%` in Phase 1 but transfers below the unoptimized baseline at `54.5%`, then recovers to `72.7%` after Phase 2. Meta Harness transfers well at `68.2%` but then stalls, falling to `59.1%` after second-round optimization.

### 7. What is actually novel?
The novelty is the evaluation framing, not just the winning method. The paper cleanly separates one-shot optimization strength, transfer to new tasks, and continued improvement under repeated optimization. Most agent-optimizer papers collapse those into one number.

### 8. What are the strengths?
The setup is easy to understand, uses the same baseline agent across methods, and surfaces a failure mode that static benchmarks miss. The appendices are also unusually useful because they describe what each optimizer actually changed rather than hiding behind method names.

### 9. What are the weaknesses, limitations, or red flags?
The winning method is author-affiliated, so independent replication matters. The benchmark still lives inside Terminal-Bench rather than genuine deployment drift. The tasks are only loosely related, which limits how much this says about richer real-world continual learning.

### 10. What challenges or open problems remain?
The big open problem is building more realistic continual-learning evaluations with stronger task relationships, noisier production-style failures, and longer optimization histories than two rounds on a benchmark task union.

### 11. What future work naturally follows?
Future work should evaluate optimizer loops on live trace distributions, regression-aware search under evolving memory and tool stacks, and longer multi-phase protocols where second-round gains themselves must survive a third or fourth wave.

### 12. Why does this matter for cabbageland?
Cabbageland cares about self-improving agents, harness design, and whether iterative optimization is actually safe to run in the wild. This paper gives a concrete warning: strong first-round benchmark gains can hide shortcuts that collapse as soon as the task set changes.

### 13. What ideas are steal-worthy?
Treat regression control as a first-class constraint inside the optimizer, not a post-hoc check. Evaluate transfer to new tasks before you celebrate first-round gains. Report repeated-optimization behavior explicitly instead of hiding behind a single optimized score.

### 14. Final decision
**Keep it.** Even if the specific winning method changes later, the evaluation question this paper sharpens is worth keeping around.
