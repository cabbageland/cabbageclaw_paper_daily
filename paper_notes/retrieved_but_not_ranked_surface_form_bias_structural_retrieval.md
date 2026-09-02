# Retrieved but not ranked: surface-form bias in structural retrieval, from mathematics to agent trajectories

## Basic info

* Title: Retrieved but not ranked: surface-form bias in structural retrieval, from mathematics to agent trajectories
* Authors: Nabira Rashid, Manolis Kellis
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2609.01556
* Date surfaced: 2026-09-02
* Why selected in one sentence: It tests semantic retrieval where wording and structure are intentionally pulled apart instead of letting lexical overlap fake success.

## Quick verdict

* Must read

I inspected the full arXiv HTML text, especially the shared two-domain protocol, the retrieval and reranking stages, the lexical-control sign flip, the judge-dependence analysis, and the downstream null. This is a preserved note because it does something many retrieval papers avoid: it defines a hard semantic target, measures where the failure sits, and refuses to inflate a downstream pipeline that had no headroom anyway.

## One-paragraph overview

The paper studies retrieval when the relevant item is structurally similar but lexically disguised. It uses two domains under one protocol: competition-math problems where the correct source problem shares reasoning structure but not wording with the query, and ALFWorld trajectories where the relevant procedure should generalize across different objects and receptacles. Embedding retrieval looks much less semantic in that regime. In math, the correct item is usually somewhere in the top 10 but almost never ranked first under heavy disguise. In trajectories, retrieval falls to chance or below once literal object tokens are no longer allowed to anchor relevance. The authors then show that a naive lexical reranker flips sign across domains, which is the paper's nicest diagnostic, while LLM rerankers help but remain domain- and judge-dependent.

## Model definition

### Inputs
Queries and full candidate corpora in two domains: disguised competition-math problems and ALFWorld-derived task trajectories. For reranking, the top-10 retrieved candidates plus the query text are passed to lexical or LLM judges.

### Outputs
A ranked retrieval list, reranked top-1 predictions, and downstream retrieved context for the paired solver study.

### Training objective (loss)
The paper does not train a new retrieval model. It evaluates existing embedders and rerankers. The LLM judges are used only as inference-time rerankers.

### Architecture / parameterization
Production embedding models (`gemini-embedding-001`, Qwen3-Embedding-8B, and MiniLM in the trajectory domain) plus lexical rerankers and LLM rerankers such as Gemini 3.1 Flash-Lite, GLM-5.2, and Claude Haiku 4.5.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Whether modern embedding retrieval actually retrieves by structure rather than by lexical resemblance when the two are deliberately separated.

### 2. What is the method?
Run one retrieval-and-reranking protocol across two unrelated domains with tiered disguise requirements, exact chance baselines, lexical controls, LLM judges, and a paired downstream utility test.

### 3. What is the method motivation?
Single-domain topical benchmarks let wording and meaning move together, so good scores can hide a ranker that is mostly following surface overlap.

### 4. What data does it use?
MathNet-Retrieve with 500 disguised queries against a 117,088-item competition-math corpus, and an ALFWorld-derived benchmark with 118 trajectory queries against 336 trajectories labeled by task type with increasing disguise requirements.

### 5. How is it evaluated?
By strict and lenient Hit@k, chance baselines, lexical-versus-structural error analysis, judge comparisons, contamination checks, and a paired downstream solver test.

### 6. What are the main results?
In mathematics, strict Hit@1 at the hardest disguise tier is `0.0%` for both production embedders even though the correct item is nearly always in the top 10. In `95.2%` to `99.8%` of misses, the winner is more lexically similar than the gold. In trajectories, retrieval drops to hypergeometric chance or below once the gold must differ in object and receptacle. The lexical reranker hurts mathematics but helps trajectories, closing `26%` to `36%` of the gap there, so the sign itself becomes a useful benchmark diagnostic. LLM rerankers recover part of the gap in both domains, but the effect size and best judge do not transfer cleanly.

### 7. What is actually novel?
The novelty is the cross-domain structural-retrieval evaluation protocol and the lexical-control sign-flip result, not a new ranker architecture.

### 8. What are the strengths?
It tests the right failure mode, uses two very different domains, defines exact chance on the trajectory side, and includes a downstream null rather than pretending retrieval gains always matter to the solver.

### 9. What are the weaknesses, limitations, or red flags?
The LLM reranking gains partly concentrate on well-known competition problems, so memorization is a real contamination risk. The paired downstream study also shows that solver truncation can erase retrieval headroom, which means the full pipeline result is less general than the retrieval audit itself.

### 10. What challenges or open problems remain?
The open problem is building retrievers whose top rank is genuinely structure-sensitive rather than merely able to place the gold somewhere in a shallow candidate set for a stronger reranker to rescue.

### 11. What future work naturally follows?
Train structure-aware retrievers, extend the benchmark style to more agentic domains, and measure when reranking gains survive contact with a downstream solver that still has enough headroom to use them.

### 12. Why does this matter for cabbageland?
Because cabbageland keeps caring about retrieval, memory, and task abstraction. This paper is a good reminder that "in the top 10" is not the same thing as "retrieved in the way your downstream system actually needs."

### 13. What ideas are steal-worthy?
Use adversarial structural disguise, report a lexical control whose sign is itself diagnostic, and include a deliberately bad retrieval condition when testing downstream utility.

### 14. Final decision
Keep as a preserved note. The paper is evaluation-heavy, but the protocol is sharp and transferable.
