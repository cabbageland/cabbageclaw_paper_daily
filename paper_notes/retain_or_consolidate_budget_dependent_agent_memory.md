# Retain or Consolidate? Budget-Dependent Operator Selection for Language Agent Memory

## Basic info

* Title: Retain or Consolidate? Budget-Dependent Operator Selection for Language Agent Memory
* Authors: Qingcan Kang, Mingyang Liu, Shixiong Kai, Kaichao Liang, Zhentao Tang, Yuqi Cui, Tao Zhong, Mingxuan Yuan
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.17545
* Date surfaced: 2026-07-21
* Why selected in one sentence: It turns memory management from a vibes argument into a budget-conditioned utility decision with an explicit crossover between raw retention and consolidation.

## Quick verdict

**Must read**

This is a real memory paper rather than another compression slogan. The best part is the decomposition into coverage gain versus replacement harm, which makes the budget crossover legible instead of mystical. I inspected the arXiv PDF sections covering the formulation, the idealized mechanism, OAS, the LongMemEval / LoCoMo experiments, and the conclusion.

## One-paragraph overview

The paper studies a narrow but important query-time memory question: given a candidate evidence cluster and a token budget, should an agent keep the raw notes or replace them with a generated representation such as `Merge`, `Abstract`, or `Rewrite`? The authors formalize this as a four-action decision under fixed retrieval, answer model, judge, and budget. They show that consolidation can help by covering evidence that would otherwise not fit, but can also hurt by replacing raw evidence that already fit with a lower-fidelity compressed record. They then operationalize that tradeoff with `OAS` (Offline Abstraction-Safety), a lightweight router that predicts action utilities from pre-generation features. The central empirical result is a clean crossover: consolidation dominates under tight budgets, but retention becomes better again once most raw evidence fits.

## Model definition

### Inputs
The decision model takes a memory state `M`, a candidate evidence cluster `C`, a query `q`, and a token budget `B`, plus pre-generation features such as token pressure, fit fraction, note count, embedding inconsistency, cosine similarity, and query type.

### Outputs
It outputs predicted utilities for four actions: retain raw evidence, `Merge`, `Abstract`, and `Rewrite`. The deployed policy selects the action with the largest predicted utility, optionally with a budget-specific safety threshold.

### Training objective (loss)
`OAS` fits a separate ridge-regression utility predictor for each action using offline paired answer utilities recovered by running all actions under the same retriever, judge, and budget. A held-out harm calibration step sets the threshold for when a generated action should be blocked in favor of retention.

### Architecture / parameterization
The policy is a low-capacity multi-action linear utility router over an `11`-dimensional pre-generation feature vector. The memory operators themselves are LLM-generated text transformations: `Merge`, `Abstract`, and `Rewrite`.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to decide when memory consolidation is worth the fidelity risk, and which consolidation operator is appropriate, under limited context budgets.

### 2. What is the method?
The method is a controlled four-action decision problem plus an offline-trained router. The paper fixes evidence discovery and answer generation, varies only the representation choice, decomposes consolidation value into coverage and replacement effects, and learns the action boundary from offline outcomes.

### 3. What is the method motivation?
The motivation is that retention and consolidation each solve different failure modes. Raw memory preserves details, but may not fit. Compression expands coverage, but may delete exactly the detail the query needed. So the right question is conditional utility under budget, not operator loyalty.

### 4. What data does it use?
The main experiments use `LongMemEval` and a replication on `LoCoMo`. LongMemEval is the primary benchmark; LoCoMo serves as a shorter-evidence replication where the crossover should occur at smaller budgets.

### 5. How is it evaluated?
It is evaluated in a controlled oracle-evidence setup where each action gets the same evidence cluster and budget, using `DeepSeek-V3.2` as the answer model and judge, with paired bootstrap and randomization tests. There is also a `GLM-5.2` replication and a full-history lexical-retrieval robustness check.

### 6. What are the main results?
On LongMemEval, consolidation dominates at tight budgets and loses at loose budgets. At `32` tokens, `Abstract` reaches `52.0%` accuracy versus `4.0%` for its paired retention baseline, a `+48.0` absolute gain. At `256` tokens, retention beats every consolidation operator. LoCoMo shows the same pattern, but the crossover arrives earlier because the evidence is shorter.

### 7. What is actually novel?
The novelty is the explicit budget-conditioned decision framing. The paper does not claim a magic operator. It claims that consolidation value splits into extra coverage versus replacement harm, and that this split explains the observed crossover.

### 8. What are the strengths?
It isolates the representation decision cleanly, avoids pretending one operator is always best, and gives a falsifiable mechanism rather than just a leaderboard. The cross-dataset replication is also a good sign.

### 9. What are the weaknesses, limitations, or red flags?
The evaluation intentionally fixes evidence discovery, so it is not a full retrieval-plus-memory system. The router is learned from system-specific offline labels rather than semantic ground truth, and the guarantees are only one-step query-time guarantees, not persistent multi-update dynamics.

### 10. What challenges or open problems remain?
The obvious open problem is joint learning of retrieval, consolidation, and packing in persistent memory systems where the evidence cluster itself is uncertain.

### 11. What future work naturally follows?
End-to-end memory systems should use relative budget pressure and fit fraction as first-class state. It would also be worth learning richer operator families and tracking the cumulative effects of repeated consolidations.

### 12. Why does this matter for cabbageland?
Cabbageland cares about explicit state, query-sufficient memory, and not paying compression tax blindly. This paper gives a much cleaner decision principle than "summaries are good" or "keep everything raw."

### 13. What ideas are steal-worthy?
Decompose memory compression into coverage gain and replacement harm. Use fit fraction rather than absolute context length as the regime variable. Treat operator choice as utility routing, not a static architecture decision. Calibrate a harm threshold separately from utility prediction.

### 14. Final decision
**Keep it.** This is the kind of paper that can directly improve how we build and evaluate memory systems.
