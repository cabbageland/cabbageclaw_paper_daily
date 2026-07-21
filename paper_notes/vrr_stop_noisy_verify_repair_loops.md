# Verify, Repair, Repeat, or Stop? Robust Stopping for Noisy Verify-Repair Loops in LLM Agents

## Basic info

* Title: Verify, Repair, Repeat, or Stop? Robust Stopping for Noisy Verify-Repair Loops in LLM Agents
* Authors: Yitao Wu, Si Shen, Rui Yang, Hong Peng, Bin Hu
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.17641
* Date surfaced: 2026-07-21
* Why selected in one sentence: It treats repair loops as noisy state transitions and gives an explicit stopping rule for when another repair round is expected to make the plan worse.

## Quick verdict

**Highly relevant**

This paper is worth keeping because it asks the right systems question: not whether verify-repair loops can help, but when they should stop before they corrupt a good candidate. The framework is pleasantly explicit about where the damage comes from and when calibration becomes too weak to trust. I inspected the arXiv PDF sections covering the noise model, belief recursion, calibration, experiments, guarded fallback, and conclusion.

## One-paragraph overview

The paper models a verify-repair loop as a repeated decision over a single candidate plan. A verifier produces noisy accept / reject votes, a repairer can either fix a bad plan or damage a good one, and the system has to decide whether to commit or repair again. `VRR-Stop` estimates the posterior validity of the current plan from verification votes, then computes the expected marginal gain of one more repair round using calibrated repair-success and repair-damage rates. If the gain is negative, it stops. If calibration itself becomes unreliable, the paper falls back to `VRR-Guard`, a conservative incumbent-preserving rule. The point is that rising verifier acceptance does not imply rising true validity, and fixed-round repair can be catastrophically wrong.

## Model definition

### Inputs
The framework takes the current plan, the history of repair rounds, `M` binary verification votes for the current round, and calibrated estimates of verifier false-accept / false-reject rates plus repair success / damage rates.

### Outputs
It outputs a posterior belief that the current plan is truly valid, the expected marginal gain of one more repair round, and a `Commit` versus `Repair` decision. In the guarded mode it may also preserve the incumbent best candidate instead of accepting the latest one.

### Training objective (loss)
There is no new end-to-end neural model here. The method estimates verifier noise with a binomial-mixture EM procedure and estimates repair success / damage rates from weakly supervised labeled repair transitions. The stopping rule itself is analytic.

### Architecture / parameterization
The system is a belief filter plus a one-step stopping policy. `VRR-Stop` uses a four-parameter noise model with verifier false acceptance `rho0`, verifier false rejection `rho1`, repair success `alpha`, and repair damage `beta`. `VRR-Guard` is a conservative fallback for low-identifiability regimes.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to decide when iterative verify-repair loops should stop, especially when both the verifier and the repairer are noisy.

### 2. What is the method?
The method uses Bayesian belief filtering over plan validity plus a marginal-gain stopping rule. One more repair round is issued only when the expected gain from fixing an invalid plan outweighs the expected damage to a valid one.

### 3. What is the method motivation?
The motivation is that multi-round repair is not monotone. A good plan can be damaged, verifier pass rates can drift upward even while true validity falls, and fixed repair budgets have no principled stopping logic.

### 4. What data does it use?
The end-to-end experiments cover `GSM8K`, `MATH-500`, `MBPP`, and `BFCL`, with generators and verifiers from the `Qwen2.5`, `Mistral`, and `Llama` families. Several stress settings deliberately inject prompt mismatch or weak verification regimes.

### 5. How is it evaluated?
It is evaluated against no-repair, fixed-budget repair, majority-stopping and confidence-threshold heuristics, plus diagnostic references such as a true-parameter myopic policy. Metrics include final true validity, repair rounds used, and sign-flip risk under different verifier discrimination levels.

### 6. What are the main results?
On the GSM8K / `Qwen2.5-3B` stress setting, fixed `K=5` repair collapses final validity from `0.700` to `0.116`, while `VRR-Stop` reaches `0.722` with only `0.72` repair rounds on average, a `+60.6` point gain over fixed repair. In a near-zero-discrimination regime where calibrated stopping fails, `VRR-Guard` lifts validity from `0.223` back to `0.793`.

### 7. What is actually novel?
The novelty is the stopping formulation, not a new repair model. The paper makes stopping a sign-identification problem over a calibrated marginal gain instead of a fixed loop count or verifier-threshold heuristic.

### 8. What are the strengths?
It cleanly separates verifier noise from repair noise, explains why pass-rate metrics can lie, and includes a conservative fallback instead of assuming calibration always works.

### 9. What are the weaknesses, limitations, or red flags?
The model assumes local stationarity and a binary validity state, which are simplifications. Several headline results come from stress regimes rather than ordinary production loops, and the calibration machinery can fail when verifier discrimination is very low.

### 10. What challenges or open problems remain?
The next hard problem is modeling round-varying or state-dependent repair dynamics rather than fixed `alpha` / `beta` within a local window.

### 11. What future work naturally follows?
This framework should be extended to richer validity states, non-binary verifiers, and online mode switching that detects when to use the calibrated rule versus the guarded fallback.

### 12. Why does this matter for cabbageland?
Cabbageland cares about long-running agent loops, repair policies, and systems that fail honestly instead of polishing themselves into nonsense. This paper gives a real control law for that.

### 13. What ideas are steal-worthy?
Model repair as both gain and damage. Stop based on expected marginal gain, not round count. Separate calibration trust from action selection. Preserve an incumbent candidate when verifier discrimination collapses.

### 14. Final decision
**Keep it.** This is a strong systems-control paper for anyone building iterative agent loops.
