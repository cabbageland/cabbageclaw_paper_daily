# Tycho: Active Abstraction with Programmatic World Models for ARC-AGI-3

## Basic info

* Title: Tycho: Active Abstraction with Programmatic World Models for ARC-AGI-3
* Authors: Jens Lehmann, Andrei Aioanei, Sahar Vahdati
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.28287
* Date surfaced: 2026-08-02
* Why selected in one sentence: It treats explicit world-model construction as a metareasoning problem about when model building is worth scarce interaction, which is much more interesting than another paper that merely posts a stronger simulator.

## Quick verdict

**Highly relevant**

I inspected the arXiv HTML paper, especially the introduction, formal setting, Tycho architecture, and evaluation sections. The paper's best move is not the headline score but the distinction between transition replay quality and action usefulness. The main caveat is that the whole system is benchmark-specific, orchestration-heavy, and dependent on very strong frontier models, so this is a sharp design pattern rather than a cleanly isolated algorithmic primitive.

## One-paragraph overview

Tycho is a coding-agent system for ARC-AGI-3 that tries to build explicit executable hypotheses about a game's hidden mechanics while interacting under a tight action budget. The agent separates actionable frames from animation and terminal screens, accumulates evidence in persistent task memory, builds a free-form programmatic world model when useful, verifies that model against observed transitions, plans with it, and may also bypass it if the model is not worth consulting. The paper's real thesis is that explicit models are not enough on their own: good performance requires deciding when to construct, repair, use, or ignore them under costly interaction.

## Model definition

### Inputs
The system consumes rendered grid observations, action histories, score-relevant transition traces, and persistent task memory from ARC-AGI-3 environments.

### Outputs
It emits executable game hypotheses, verification reports, simulated plans, and next actions for the live environment.

### Training objective (loss)
There is no newly trained task-specific model at the center of the paper. Tycho is an orchestration system built on top of strong foundation models used for actor and model-builder roles.

### Architecture / parameterization
Tycho is a hybrid agent stack with an orchestrator, task memory, an evidence interface, an executable hypothesis language, verification/planning tools, and a policy over when to delegate model construction or bypass it.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve interaction-efficient skill acquisition in ARC-AGI-3, where the agent must infer hidden rules and goals while every action counts against the score.

### 2. What is the method?
The method is to let the agent build explicit executable world models during interaction, verify them against observed transitions, plan with them when useful, and treat model use itself as a metareasoning choice rather than a mandatory step.

### 3. What is the method motivation?
Interactive abstraction is expensive. A model that explains the observed dynamics may still fail to identify the objective or may cost more to build than it saves. The paper wants to make explicit-model use conditional rather than doctrinal.

### 4. What data does it use?
The evaluation uses the 25 public ARC-AGI-3 games covering 183 levels, with matched-budget comparisons across orchestration policies and frontier-model backbones. Human replay distributions are used as efficiency references.

### 5. How is it evaluated?
The authors compare direct reasoning, actor-authored modeling, actor-requested delegation to a builder, and automatic repair after verification failure. They report Relative Human Action Efficiency, completion rates, paired game effects, human replay comparisons, and cost/context diagnostics.

### 6. What are the main results?
Among orchestration policies under matched budgets, actor-requested delegation performs best with mean RHAE 88.49. With that policy, GPT-5.6 Sol and Opus 5 both reach 100.00 RHAE and complete all 183 levels, and Opus 5 uses 61% fewer scored actions than the aggregate official human baselines. Automatic repair after verification failures improves transition reproduction but still lands at 83.07 RHAE, which is the paper's key negative result.

### 7. What is actually novel?
The strongest novelty is the framing of active abstraction: useful explicit models are not just induced, they are acquired and consulted under a budget. The paper explicitly separates simulator fidelity from decision value.

### 8. What are the strengths?
It gives inspectable explicit hypotheses instead of hiding everything in latents, uses a clear operational decomposition, and surfaces a non-obvious lesson: better verification does not imply better control. That is exactly the kind of distinction most world-model papers blur.

### 9. What are the weaknesses, limitations, or red flags?
The setup is benchmark-specific, orchestration-heavy, and leans on strong proprietary models. Action efficiency also excludes inference cost, so the reported performance is not the same thing as deployment efficiency. There is no autonomous outer-loop learning beyond the episode-level orchestration.

### 10. What challenges or open problems remain?
The central open problem is how to make explicit model induction cheaper, more transferable, and less benchmark-shaped. Another is learning when not to model, especially in domains where partial heuristics beat elaborate simulation.

### 11. What future work naturally follows?
Stronger metareasoning over model acquisition, cheaper verifiers, better reuse of partial hypotheses across tasks, and explicit outer-loop adaptation from prior failures all follow naturally.

### 12. Why does this matter for cabbageland?
It matters because cabbageland cares about explicit state, reusable abstractions, and the difference between legible structure and decorative structure. Tycho makes that difference operational.

### 13. What ideas are steal-worthy?
Separate actionable observations from irrelevant transition frames. Treat model construction as an expensive action subject to budget. Use verification to decide whether a model is usable, but do not confuse that with proof that consulting it will improve the next move.

### 14. Final decision
**Keep it.** This is one of the better explicit-structure papers in the recent batch because it is honest about when world models help and when they do not.
