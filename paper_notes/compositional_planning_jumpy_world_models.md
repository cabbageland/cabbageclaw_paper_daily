# Compositional Planning with Jumpy World Models

## Basic info

* Title: Compositional Planning with Jumpy World Models
* Authors: Jesse Farebrother, Matteo Pirotta, Andrea Tirinzoni, Marc G. Bellemare, Alessandro Lazaric, Ahmed Touati
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2602.19634
* Date surfaced: 2026-03-24
* Why selected in one sentence: It makes temporal abstraction operational by learning multi-timescale predictive models over reusable policies, not just over primitive actions.

## Quick verdict

**Highly relevant**

This is one of the better recent planning papers because the abstraction is real and mathematically grounded. The paper does not merely say “hierarchical” and then smuggle everything back into end-to-end mush; it explicitly models successor-style future occupancies for pre-trained policies across different timescales, then plans over sequences of those policies. I inspected the abstract and substantial method text, but not the full appendix or every experiment table, so I trust the conceptual mechanism more than the exact size of the reported gains.

## One-paragraph overview

The paper asks a sensible question: if we already have a repertoire of competent pre-trained behaviors, why keep planning at the raw action level for long-horizon tasks? Its answer is to learn jumpy world models that predict the state occupancy induced by executing a given policy over geometrically distributed timescales. Those predictive models are then combined to estimate the value of switching among policies in sequence, allowing planning over temporally extended actions instead of primitive action tokens. The important contribution is not just better long-horizon prediction; it is a cleaner planning interface for compositional behavior.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Long-horizon decision-making is hard when planning directly over primitive actions because errors compound and search blows up. If a library of useful policies already exists, the problem becomes how to predict and evaluate what happens when those policies are composed over varying durations.

### 2. What is the method?
- Learn policy-conditioned jumpy world models that predict discounted successor-state occupancies rather than one-step transitions.
- Represent different execution durations through geometrically decaying horizons.
- Extend Temporal Difference Flows with a horizon-consistency objective so predictions at different timescales agree with each other.
- Define geometric switching policies that execute one policy for a random duration, then switch to the next.
- Estimate the value of arbitrary policy sequences from the learned occupancies and optimize plans via random shooting.

### 3. What is the method motivation?
Planning over reusable behaviors should be easier than planning over raw actions, but only if the predictive model can say what those behaviors do over meaningful horizons. One-step world models are a bad fit for that because the long horizon gets rebuilt from too many fragile local predictions.

### 4. What data does it use?
From the accessible text, the experiments use OGBench navigation and manipulation tasks and evaluate multiple classes of base policies. I did not fully audit the appendix-level dataset and policy details.

### 5. How is it evaluated?
The paper compares zero-shot base policies, compositional planning with the jumpy world model, action-level planning with one-step world models, and hierarchical / policy-composition baselines. It also includes ablations on planning frequency, objective, proposal distribution, and the horizon-consistency objective.

### 6. What are the main results?
From the accessible text, planning with jumpy world models substantially improves zero-shot performance across manipulation and navigation tasks and reports roughly a 200% relative improvement over primitive-action planning on long-horizon tasks. I have not independently verified every reported number.

### 7. What is actually novel?
The core novelty is the combination of three things: policy-conditioned jumpy predictive models, consistency across timescales, and a value estimator for arbitrary sequences of temporally extended policies. Any one part alone would be less interesting; together they make behavior-level planning concrete.

### 8. What are the strengths?
- The abstraction target is correct: reusable policies, not just primitive actions.
- The predictive object is more appropriate for long-horizon composition than one-step dynamics.
- Timescale consistency is an actual mechanism rather than a vague regularizer.
- It offers a serious alternative to retraining task-specific hierarchies.
- It is useful for thinking about world models as occupancy predictors rather than image generators.

### 9. What are the weaknesses, limitations, or red flags?
- It depends on already having a useful repertoire of base policies.
- Random-shooting plan search is simple and may become a bottleneck as the policy library grows.
- Successor-style occupancy prediction is powerful, but it does not by itself give explicit object-centric or causal state.
- The approach seems best suited to settings where downstream rewards or goals can be evaluated from predicted state visitation.

### 10. What challenges or open problems remain?
How to build or adapt the policy library, how to make the predictive state more structured and intervention-aware, and how to scale search over large behavior repertoires remain open. So does the question of how well occupancy-style planning transfers to messy real-world robotics.

### 11. What future work naturally follows?
- Learn better proposal/search methods over policy sequences.
- Combine behavior-level occupancy models with explicit symbolic or object-level state.
- Add uncertainty estimation for when policy compositions leave the support of training data.
- Test whether this interface works with real robot foundation policies, not just benchmark repertoires.

### 12. Why does this matter for cabbageland?
Because it is a good example of explicit temporal abstraction that actually changes planning. It is much closer to reusable compositional control than papers that just rename latent rollout tokens as “hierarchical reasoning.”

### 13. What ideas are steal-worthy?
- Predict occupancy induced by reusable behaviors, not just one-step transitions.
- Model horizons explicitly instead of hoping long-horizon composition emerges from local rollouts.
- Enforce consistency across timescales in predictive world models.
- Treat policy sequencing as a first-class planning object.

### 14. Final decision
**Worth preserving and likely worth a deeper read.** This is real compositional planning machinery, not decorative hierarchy.