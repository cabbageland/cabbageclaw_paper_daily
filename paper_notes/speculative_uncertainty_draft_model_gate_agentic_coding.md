# How to Speculate about Uncertainty in Agentic Coding? A Draft-Model Gate Method

## Basic info

* Title: How to Speculate about Uncertainty in Agentic Coding? A Draft-Model Gate Method
* Authors: Konstantin Grotov, Valentin Malykh
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2609.05274
* Date surfaced: 2026-09-08
* Why selected in one sentence: It recovers a pre-execution failure signal for black-box coding agents from output tokens alone.

## Quick verdict

* Must read

I inspected the full arXiv HTML text, especially the phase-aware feature extraction, the veto-gate policy, deployment tables, calibration caveat, and cross-agent transfer results. This paper is worth preserving because it gives a practical black-box route to catching bad agent actions before execution.

## One-paragraph overview

Speculative Uncertainty inverts the idea of speculative decoding. Instead of using a small draft model to propose tokens for a large model, it uses the draft to teacher-force score a black-box agent's already-generated trajectory. The method extracts separate features from reasoning spans and action spans, then trains a lightweight calibrator to predict whether the next code action will execute without error. A downstream veto gate blocks likely failures and triggers a cheaper replan before the environment pays for an execute-fail-retry loop.

## Model definition

### Inputs
Generated coding-agent trajectories with reasoning and action spans, plus labels indicating whether the next execution step succeeds.

### Outputs
A scalar failure-likelihood score and, in the evaluated policy, an accept-versus-replan decision before execution.

### Training objective (loss)
The draft model is aligned to agent trajectories through SFT or teacher-forcing distillation, and a linear calibrator is trained against a verifiable execution-success label.

### Architecture / parameterization
The system pairs a black-box target agent with a small open-weight draft model, Qwen3-4B in the main experiments. The draft scores output tokens, features are aggregated separately for reasoning and action phases, and the calibrator feeds a thresholded veto gate.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Coding agents often fail only after they act. That is expensive because the failed execution, error output, and retry all consume tokens and time.

### 2. What is the method?
Run a small draft model over the agent's completed trajectory, compute speculative cross-likelihood features, split features by phase, and predict whether the next action is likely to fail before executing it.

### 3. What is the method motivation?
White-box uncertainty is unavailable for many deployed agents, and repeated sampling is too costly. Output-token scoring by a separate draft model is a deployable compromise.

### 4. What data does it use?
The main experiments use SWE-rebench OpenHands trajectories for training and held-out evaluation, then test on SWE-Bench Verified and DA-Code. The paper also studies transfer to Claude 3.5 Sonnet as a black-box target.

### 5. How is it evaluated?
It reports AUROC and precision at 80% recall for failure prediction, calibration metrics, and deployment outcomes: execution error rate, token cost, task success, true-veto recall, and false-veto rate.

### 6. What are the main results?
Phase-aware SU with teacher-forcing reaches AUROC 0.77 on SWE-Bench Verified and 0.78 on DA-Code, compared with 0.57-0.59 for verbalized confidence and 0.82-0.83 for white-box HTC. The veto gate cuts error rate from 21% to 15% on SWE-Bench Verified and from 14% to 6% on DA-Code, saving 14-19% tokens per task. Cross-agent transfer is promising: a Qwen-distilled draft reaches 0.69 AUROC on Claude, above the untrained 0.60 baseline.

### 7. What is actually novel?
The novelty is using a separate draft model as a black-box uncertainty sensor for an already-generated agent trajectory, plus showing that reasoning and action phases need separate treatment.

### 8. What are the strengths?
It targets a real deployment constraint, uses verifiable execution labels, and reports the awkward result that lower execution error does not automatically increase task success.

### 9. What are the weaknesses, limitations, or red flags?
The gate is not well calibrated enough to treat the score as a reliable probability without extra post-hoc calibration. The downstream policy is simple, and on SWE-Bench Verified it reduces task success from 49% to 44%, so the benefit is cost and risk reduction rather than benchmark improvement.

### 10. What challenges or open problems remain?
The next step is turning the failure signal into better recovery policies rather than merely cheaper replans. The method also needs testing outside software engineering.

### 11. What future work naturally follows?
Use the score for routing, human escalation, stronger repair loops, streaming mid-generation interruption, and tool-specific risk budgets.

### 12. Why does this matter for cabbageland?
Cabbageland cares about agents that know when to stop before acting. This paper gives a concrete pre-action gate that works even when the main agent is closed-box.

### 13. What ideas are steal-worthy?
Score output tokens with a small aligned draft. Split reasoning and action phases. Put the uncertainty gate at the tool boundary. Evaluate against actual execution labels, not self-reported confidence.

### 14. Final decision
Keep as a preserved note. The method is not a competence fix, but it is a useful runtime-control primitive.

## 6. Mandatory critical angles

The representation claim is credible because the draft signal is compared with verbalized confidence and white-box baselines. The evaluation is honest about the tradeoff: fewer bad executions and lower token spend, not better final solve rate.

## 7. Writing style

Tone should be practical and sharp. Praise the deployability, but keep the success-rate caveat visible.

## 8. Repository output format

Saved as a preserved paper note because pre-execution uncertainty gating is a reusable pattern for tool-using agents.
