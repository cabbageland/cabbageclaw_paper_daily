# When May a Bandit Leave Its Anchor? E-Process-Authorized Thompson Sampling under Non-stationarity

## Basic info

* Title: When May a Bandit Leave Its Anchor? E-Process-Authorized Thompson Sampling under Non-stationarity
* Authors: Mayand Gulati, Kerong Wang, WeiChen Au
* Year: 2026
* Venue / source: arXiv; listed as NeurIPS 2026 E-Values Workshop
* Link: https://arxiv.org/abs/2610.03646
* Date surfaced: 2026-10-05
* Why selected in one sentence: It gives an anytime-valid gate for when an adaptive bandit may depart from a trusted stationary Thompson-sampling anchor.

## Quick verdict

* Useful

This is not a universal non-stationary bandit winner, and the authors are refreshingly explicit about that. Its value is conceptual: adaptation should be authorized by evidence when there is a trusted anchor, and the guarantee should control departure from that anchor. The empirical story is mixed, which makes the mechanism more credible rather than less.

## One-paragraph overview

The paper proposes e-process-authorized Thompson sampling, or e-ATS. Each arm keeps both a full-history Beta posterior and a discounted short-memory Beta state. Under a prior-predictive stationary Beta-Bernoulli model, an anytime-valid e-process monitors evidence for a change. Before authorization, the short-memory state has zero influence and the policy exactly matches optimistic Thompson sampling. After authorization, a reversible relevance score controls how much the discounted state influences action choice. The key guarantee is not regret optimality; it is that under the declared stationary model, the probability of ever departing from the trusted anchor is at most the chosen alpha threshold.

## Model definition

### Inputs

The algorithm observes a multi-armed Bernoulli bandit stream. At each round it receives rewards for the selected arm. Each arm has its own full reward history, discounted short-memory history, and e-process evidence state.

### Outputs

The policy outputs an arm choice each round. Internally it outputs authorization gates, full-history Beta posteriors, discounted Beta pseudo-posteriors, relevance scores, and a decision weight controlling how much short-memory evidence can affect Thompson sampling.

### Training objective (loss)

There is no learned neural model and no gradient loss. The method uses Bayesian Beta-Bernoulli updates, discounted pseudo-count updates, likelihood-ratio e-processes over candidate change points, and Thompson-style posterior sampling.

### Architecture / parameterization

This is an algorithmic controller. It couples an optimistic Thompson sampling anchor with a short-memory posterior. The e-process decides whether short memory is allowed to affect actions; the relevance score decides whether recent rewards still disagree with the long-history model; the decision weight mixes the resulting samples.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

In non-stationary bandits, long history helps under stationarity but hurts after change. The paper asks when a policy should be allowed to stop trusting its full-history anchor.

### 2. What is the method?

Maintain full-history and discounted states per arm. Use an anytime-valid e-process to test evidence against the stationary prior-predictive model. Before authorization, behave exactly like optimistic Thompson sampling. After authorization, let a recent-disagreement relevance score allow short-memory posterior samples to influence decisions.

### 3. What is the method motivation?

Uncontrolled adaptation can leave a good stationary policy because of noise. Instead of choosing a forgetting rate by hand or always discounting, the policy should require statistical permission before departing from a trusted anchor.

### 4. What data does it use?

The method is evaluated on synthetic and literature-derived non-stationary Bernoulli bandit environments. The registered suite contains 16,380 non-stationary environments across nine mechanisms plus 1,820 stationary environments. The replay suite uses 4,500 matched runs on 606 trajectories from nine environment families.

### 5. How is it evaluated?

The paper reports mean normalized dynamic pseudo-regret and compares e-ATS with optimistic Thompson sampling, an open-ramp version without authorization, certified and practical GLR alternatives, and a broader replay set of baselines. It also measures whether the policy departs in stationary environments.

### 6. What are the main results?

Under the declared stationary model, departure from the anchor is bounded by alpha_E because a departure can occur only after e-process authorization. In 1,820 stationary registered environments, only one arm was authorized in total, and e-ATS matched the anchor's mean regret. On the registered non-stationary suite, e-ATS has lower regret than OTS and open ramp: 0.0390 versus 0.0494 and 0.0540. On the replay suite, open ramp is better than e-ATS: 0.1414 versus 0.1530. The authors summarize the lesson cleanly: evidence controls when adaptation begins, not whether it always helps.

### 7. What is actually novel?

The novelty is translating an anytime-valid e-process into a policy-level departure gate, then coupling the policy so that before authorization it exactly follows the anchor. That makes the statistical guarantee directly control behavior.

### 8. What are the strengths?

The guarantee is precise and behavior-facing. The method does not pretend adaptation is free. The experiments include a stationary sanity check where uncontrolled adaptation hurts badly.

### 9. What are the weaknesses, limitations, or red flags?

The guarantee is prior-predictive under a Beta(1,1) stationary model, not valid separately for every fixed arm mean. It authorizes departure but does not guarantee non-stationary regret. The algorithm does not force exploration, so a changed arm may not be sampled enough to produce evidence. The replay-suite result is mixed, with mean rank 9.72 among 17 methods.

### 10. What challenges or open problems remain?

The paper itself names the next needs: restartable authorization, validity for fixed means, and actual non-stationary regret guarantees. Another open issue is how to make authorization robust when action selection starves changed arms of evidence.

### 11. What future work naturally follows?

Use e-process-style authorization as a gate for memory eviction, model adaptation, tool-policy updates, or online calibration, where departures from a trusted baseline should be rare under a declared null. In RL, pair the gate with exploration mechanisms that ensure evidence can arrive.

### 12. Why does this matter for cabbageland?

Cabbageland cares about systems that adapt without thrashing. e-ATS is a clean pattern: keep a conservative anchor, require evidence before leaving it, and separate permission to adapt from proof that adaptation will help.

### 13. What ideas are steal-worthy?

Couple the adaptive system to a baseline so you can prove no behavioral divergence before authorization. Use evidence gates to control when a short-memory model may override long memory. Report where adaptation hurts instead of hiding it.

### 14. Final decision

Preserve as a useful control/adaptation pattern. It is not today's most important paper, but the evidence-gated departure idea is worth keeping.
