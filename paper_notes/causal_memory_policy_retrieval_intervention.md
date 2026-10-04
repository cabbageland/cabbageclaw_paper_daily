# Causal Memory Policy: Making Memory Utility Identifiable by Intervening on Retrieval

## Basic info

* Title: Causal Memory Policy: Making Memory Utility Identifiable by Intervening on Retrieval
* Authors: Arman Behnam, Binghui Wang
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2610.02070
* Date surfaced: 2026-10-04
* Why selected in one sentence: It identifies a real causal failure in memory systems: a memory that retrieval never exposes cannot have its usefulness estimated from ordinary logs.

## Quick verdict

Highly relevant.

This paper is worth preserving because it separates memory usefulness from memory retrievability. That distinction is easy to blur in agent-memory systems, and the paper gives both the formal reason and an experimental design for repairing the failure. The caveat is equally important: identified per-query utility is not yet a deployable retention policy.

## One-paragraph overview

Causal Memory Policy argues that store-level memory interventions cannot estimate the value of memories the retriever never places in context. This is a retrieval-level positivity violation: if a memory is never exposed, its outcome under inclusion is unobserved. CMP fixes the design by reserving some context slots for randomized exposure from a candidate pool with known propensities, then estimating per-query memory utility with a self-normalized inverse-propensity estimator. On LongMemEval, LoCoMo, and Mem0, retrieval support fails often for required memories, and randomized exposure improves discrimination between required and non-required memories. The paper's best contribution is not an eviction product; it is the warning that memory utility cannot be measured unless retrieval itself is randomized or otherwise instrumented.

## Model definition

### Inputs

CMP takes a memory store, the current query and context, a deterministic retriever, a context budget, an exposure pool, the number of randomized exposure slots, observed downstream outcomes, and known exposure propensities produced by the randomized design.

### Outputs

It outputs per-memory, per-query utility estimates with uncertainty, plus optional decisions under an irreversible-operation loss rule. The paper is careful that these utility estimates do not by themselves solve future retention.

### Training objective (loss)

CMP itself is an experimental design and estimator, not a trained neural model. Its utility estimator is a self-normalized inverse-propensity-weighted difference between exposed and unexposed outcomes. Observational and AIPW comparators train propensity and outcome models, but CMP's clean design uses known propensities from randomized exposure.

### Architecture / parameterization

The system is a memory-augmented LLM with a retrieval stage. CMP modifies retrieval by filling B-k context slots with the normal top-ranked memories and k slots with balanced randomized exposures from a pool. Across timesteps, exposure counts are allocated evenly so each candidate memory receives known positive propensity.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It asks how to estimate whether a memory is useful when the retriever never shows that memory to the model. Store-level delete/keep interventions do not solve this because retrieval happens after the store is perturbed; if the memory is never retrieved either way, the downstream outcome is unchanged.

### 2. What is the method?

CMP intervenes on the retrieval mediator. It reserves a fixed number of context slots for sampled memories with known propensities, uses balanced assignment so every memory in the pool gets exposure, and estimates memory utility by self-normalized inverse-propensity weighting. It also derives a decision rule for asymmetric reversible/irreversible operations and analyzes why aggregation over future queries remains unresolved.

### 3. What is the method motivation?

The causal motivation is positivity. To estimate a memory's effect, the memory must have nonzero probability of being included and excluded. Ordinary retrievers make many memories have zero inclusion probability for a query, so no amount of passive logging identifies their utility.

### 4. What data does it use?

The experiments use LongMemEval, LoCoMo, HotpotQA, MuSiQue, and Mem0. LongMemEval is primary; LoCoMo tests multi-session query distributions; HotpotQA and MuSiQue extend the setup to multi-hop retrieval; Mem0 tests a deployed memory system. The LLM used in the experiments is gemini-3.7-flash.

### 5. How is it evaluated?

The paper measures retrieval support failure, discrimination between required and non-required memories, nomination lift for eviction candidates, and gold loss, meaning required memories destroyed per 100 reclaimed slots. It compares store-level randomization against exposure randomization at matched budgets.

### 6. What are the main results?

Retrieval support fails for 54.0% of required memories on LongMemEval independent, 61.2% on LongMemEval all, 66.9% on LoCoMo, and 28.4% in the Mem0 setting. On LongMemEval independent, CMP improves AUC from 0.542 for store-level randomization to 0.664 and reduces gold loss from 10.9 to 5.2. The whole gain sits in the zero-retrieval-support stratum, which supports the design claim rather than a generic estimator claim.

### 7. What is actually novel?

The novelty is the retrieval intervention. Prior memory-utility estimates usually operate on stored memories or retrieved context; CMP points out that retrieval is the mediator that must be randomized if unretrieved memories are to be valued.

### 8. What are the strengths?

The causal framing is crisp, and the experiments isolate the failure well. The paper is also honest about the remaining gap: utility estimation is not the same as retention, because retention is a decision before seeing future queries.

### 9. What are the weaknesses, limitations, or red flags?

The demonstration uses an exposure pool constructed with knowledge of required memories, which isolates identification but does not solve practical pool selection. Exposure has a direct opportunity cost because randomized slots displace ranked evidence. The result constrains utility-ranking memory policies more than frequency or recency heuristics.

### 10. What challenges or open problems remain?

The largest open problem is pool selection: how does a deployed system choose a candidate set likely to contain memories whose utility is unknown but important? The second problem is future-query aggregation: per-query usefulness may not predict retention value across unknown future queries.

### 11. What future work naturally follows?

Future work should learn exposure-pool selectors, use adaptive experimental designs that concentrate randomization where uncertainty is high, and connect per-query utility with explicit assumptions about future query distributions.

### 12. Why does this matter for cabbageland?

Cabbageland cares about memory systems with real mechanisms. CMP gives a useful warning: if memory retention decisions are based on observed retrieval utility, they may be blind exactly where retrieval is blind.

### 13. What ideas are steal-worthy?

The steal-worthy idea is randomized retrieval exposure. Reserve a small context budget for instrumented memory probes, record propensities, and treat memory utility as an estimand rather than a vibe extracted from retrieved context.

### 14. Final decision

Preserve. This is a durable reference for causal instrumentation of agent memory and for the difference between retrieval rank and memory value.
