# Naju: A Native Discrete State-Space Model with Independent Retention and Writing for Long-Sequence Memory

## Basic info

* Title: Naju: A Native Discrete State-Space Model with Independent Retention and Writing for Long-Sequence Memory
* Authors: Hyuk Lim, Seunghyun Yoon
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.21000
* Date surfaced: 2026-07-24
* Why selected in one sentence: It replaces mushy long-memory claims with a concrete retain/write decoupling argument and a native discrete SSM that actually survives both retention and overwriting tests.

## Quick verdict

**Must read**

This is a real mechanism paper. The useful move is not "better long context" but a specific claim that coupled parameterizations force a retain/write tradeoff that the recurrence should not have. I inspected the arXiv PDF sections covering the abstract, introduction, Naju method, memory-kernel analysis, experiments, and conclusion.

## One-paragraph overview

The paper studies long-sequence memory tracking under a fixed recurrent state budget and argues that common efficient recurrences entangle two functions that should be independent: keeping old information and writing new information. In zero-order-hold SSMs, the same discretization variable that moves the transition toward identity also affects write scale. In complementary single-gate designs, stronger retention means weaker writing by construction. Naju removes that coupling by directly parameterizing the recurrence in discrete time as a forget-gated retention pole plus an independent input gate and selective write/read maps. The result is a diagonal selective SSM that can preserve a binding across long gaps and decisively replace it when needed.

## Model definition

### Inputs
The model takes the current token or sequence input, the previous recurrent state, and short causal local context that parameterizes token-dependent forget gates and selective write/read maps.

### Outputs
It outputs an updated recurrent state and a readout used for downstream prediction, such as next-token language-model outputs or task-specific sequence representations.

### Training objective (loss)
The architecture is trained with standard task losses for the evaluated domains: autoregressive language-model cross-entropy on WikiText-103 and the corresponding supervised task losses for the diagnostic memory suite, Long Range Arena, and associative-recall evaluations.

### Architecture / parameterization
Naju is a native discrete selective state-space model. Its recurrence is `x_n = f_n * x_{n-1} + i_n * (B_n u_n)`, where `f_n` is the forget gate that directly serves as the discrete recurrent pole, `i_n` is an independent input gate, and `B_n` / `C_n` are input-dependent write/read maps. The state is diagonal and scan-compatible.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to build an efficient recurrent sequence model that can both preserve long-range bindings and overwrite stale ones under a fixed state budget.

### 2. What is the method?
The method is to parameterize the recurrence directly in discrete time and give retention and writing separate gates instead of tying them through a single control or a continuous-time discretization variable.

### 3. What is the method motivation?
The motivation is that long-sequence memory needs two conflicting behaviors at once. The state must hold information almost losslessly over long horizons, but it must also update aggressively when the content changes. Coupled gates make those behaviors fight each other.

### 4. What data does it use?
The evaluation uses a diagnostic memory suite, multi-query associative recall, Long Range Arena, and WikiText-103 language modeling under matched training budgets.

### 5. How is it evaluated?
It is evaluated on retention and overwriting diagnostics, matched recurrent-state comparisons against Mamba-family and other efficient baselines, Long Range Arena averages, and WikiText-103 perplexity.

### 6. What are the main results?
At `4x` the training length, Naju is the only tested model that stays strong on both axes, with about `0.99` retention and `0.89` overwrite accuracy. On WikiText-103 at a matched `1.2B`-token budget and `d_model = 256`, it reaches `26.20` test perplexity versus about `28.31` for Mamba-2. It also leads the fully evaluated models in the budget-matched Long Range Arena comparison and beats both Mamba baselines on multi-query associative recall at matched state budgets.

### 7. What is actually novel?
The novelty is the direct discrete-time retain/write decoupling. The paper does not just bolt an LSTM idea onto an SSM marketing wrapper; it makes the recurrent pole itself discrete and independent from the write gain while keeping selective state-space structure.

### 8. What are the strengths?
It gives a crisp structural diagnosis, a simple recurrence, stability analysis, and an evaluation that tests the claimed tradeoff instead of only showing generic long-context benchmarks.

### 9. What are the weaknesses, limitations, or red flags?
The strongest evidence still comes from diagnostic memory tasks, associative recall, and language modeling rather than long-lived deployed systems. The architecture remains diagonal-state and may still hit representational limits that these benchmarks do not expose.

### 10. What challenges or open problems remain?
The next challenge is testing whether the retain/write decoupling keeps paying off in more realistic agentic and multimodal settings where the memory object is less clean than token-bound sequence state.

### 11. What future work naturally follows?
Apply the same decoupling principle to richer selective recurrences, multimodal recurrent state, and planning or world-model settings where overwriting and retention must coexist under partial observability.

### 12. Why does this matter for cabbageland?
Cabbageland cares about explicit state that can both persist and update without becoming latent mush. Naju gives a clean architectural example of that principle.

### 13. What ideas are steal-worthy?
Treat the forget gate as the discrete pole itself. Decouple write gain from retention rather than hoping optimization will discover the right compromise. Evaluate memory systems on both retention and overwrite stress tests, not only on long-context averages.

### 14. Final decision
**Keep it.** This is one of the cleaner recent arguments that state quality depends on the exact control interface, not just on giving the model a longer recurrent horizon.
