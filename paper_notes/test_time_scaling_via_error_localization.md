# Test-Time Scaling via Error Localization

## Basic info

* Title: Test-Time Scaling via Error Localization
* Authors: Rajiv Shailesh Chitale, Rahul Madhavan, Taneesh Gupta, Deepanway Ghosal, Aravindan Raghuveer
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.21453
* Date surfaced: 2026-07-24
* Why selected in one sentence: It turns failure feedback into a token-level branching signal so inference-time compute can repair the bad suffix instead of paying to rerun the good prefix.

## Quick verdict

**Highly relevant**

This is a solid inference-time control paper because the mechanism is specific and the ablations actually test it. The idea is simple enough to steal and the compute savings are real. I inspected the arXiv PDF sections covering the abstract, introduction, TTEL method, scaling experiments, context ablations, spike-filter ablations, and conclusion.

## One-paragraph overview

The paper tackles a common inefficiency in test-time scaling: when a long reasoning or coding trace fails, most methods either sample from scratch again or append more global feedback without identifying where the trace first went wrong. TTEL uses the same model as both generator and evaluator. After a failure, it rescoring the original trajectory under feedback-conditioned context and compares those token probabilities against a null-feedback baseline. Large filtered divergences indicate likely error locations. The algorithm then truncates the trajectory at the most suspicious point, preserves the prefix, and regenerates only the suffix. That turns test-time search into prefix-sharing branch repair rather than full-solution rerolling.

## Model definition

### Inputs
The method takes a problem prompt, a generated trajectory, and failure feedback from either a generic message or a task environment, plus a null-feedback baseline for filtering context-only probability shifts.

### Outputs
It outputs token-level spike locations, truncated branch points, a prefix-sharing search tree, and final candidate solutions selected under a rollout budget.

### Training objective (loss)
There is no training or gradient update in the method itself. TTEL is an inference-time algorithm applied to a fixed pretrained autoregressive language model.

### Architecture / parameterization
The architecture is a search procedure around one model acting in two roles: student generator and teacher-style feedback-conditioned evaluator. The key signal is the contrast between informed and null-context token probabilities.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to make inference-time scaling more token-efficient by preserving valid reasoning prefixes instead of discarding them after a failed attempt.

### 2. What is the method?
The method computes token-level divergence under failure feedback, filters it against a null-feedback baseline, cuts the trace at the most confident error point, and branches new generations from there.

### 3. What is the method motivation?
Failure feedback is usually trajectory-specific. If you throw away the exact path that produced the failure, the feedback loses most of its local value. TTEL tries to keep the path and repair only the broken segment.

### 4. What data does it use?
The experiments use LiveCodeBench V6 for coding plus AIME-25 and HMMT-25 for math reasoning.

### 5. How is it evaluated?
It is evaluated as a pass-at-k versus generated-token-cost tradeoff against independent sampling, multi-turn refinement, and RSA-style baselines, with ablations on full-trace availability and null-baseline filtering.

### 6. What are the main results?
On LiveCodeBench with Qwen3-8B, TTEL reaches `71.0%` `pass@64` while using about `360.4k` average generated tokens versus `735.0k` for independent sampling. On AIME-25 it reaches about `0.820` `pass@16`. Removing full-trace context lowers accuracy and increases token cost. Removing spike filtering explodes the average detected spikes in turn one from about `19.3` to `486.0` and drops pass@k to about `0.592`, showing that the filtering step is not optional decoration.

### 7. What is actually novel?
The novelty is repurposing a feedback-conditioned token-probability contrast as an online branch-localization signal rather than using similar signals only for offline distillation or policy updates.

### 8. What are the strengths?
The algorithm is conceptually clean, testable, and ablated properly. It establishes a real Pareto improvement instead of just a one-point benchmark win.

### 9. What are the weaknesses, limitations, or red flags?
It still depends on additional rescoring passes and on some form of useful feedback, even if generic. The experiments are concentrated on Qwen-based models and a limited set of reasoning domains.

### 10. What challenges or open problems remain?
The next challenge is making the localization robust when feedback is noisier, more ambiguous, or delayed, and when traces branch semantically rather than token-locally.

### 11. What future work naturally follows?
Combine TTEL with stronger verifiers, richer environment feedback, learned spike calibration, or structured program-state checkpoints instead of pure token-prefix retention.

### 12. Why does this matter for cabbageland?
Cabbageland cares about systems that spend compute where the error lives. TTEL is a good example of making the repair boundary explicit instead of hoping extra samples magically fix the right step.

### 13. What ideas are steal-worthy?
Keep the valid prefix. Contrast informed feedback against a null baseline to suppress context-only probability drift. Treat token-level rescoring as a branch-selection signal, not just as a train-time distillation trick.

### 14. Final decision
**Keep it.** This is one of the better recent papers on making inference-time scaling behave like a repair system rather than a reroll lottery.
