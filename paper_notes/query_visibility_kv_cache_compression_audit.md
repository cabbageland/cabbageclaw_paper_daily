# How Query Visibility Changes KV-Cache Compression Rankings: A Matched-Budget Audit

## Basic info

* Title: How Query Visibility Changes KV-Cache Compression Rankings: A Matched-Budget Audit
* Authors: Daming Luo, Christy Liang, Junyu Xuan
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.11942
* Date surfaced: 2026-07-15
* Why selected in one sentence: It fixes a deployment-protocol mismatch that makes several popular KV-cache compression methods look better than they are for reusable context serving.

## Quick verdict

**Highly relevant**

This is the kind of audit paper that actually earns the word audit. It changes one variable, documents its own confounds, retracts a dead headline when the completed run no longer supports it, and leaves behind a concrete evaluation lesson rather than a vague complaint. I inspected the full arXiv HTML paper, including the abstract, audit design, RULER results, mechanistic hypothesis section, robustness checks, limitations, and conclusion.

## One-paragraph overview

The paper asks a simple but consequential question: if a KV-cache compressor is supposed to compress a document once and answer many future queries, why are so many methods evaluated after the query has already been appended to the context? The authors run a matched-budget audit of six published compression methods plus three trivial baselines across RULER and LongBench, holding model, budget, instances, and decoding fixed while flipping only whether the query is visible at compression time. That one change reshuffles the rankings. Methods whose scoring rules directly or indirectly read the question suffer large drops in the query-agnostic setting, while KeyDiff, whose score is query-independent, largely survives. The paper also surfaces two broader evaluation hazards: backend changes can shift accuracy more than the compression methods do, and benchmark token lengths can silently overflow a model's positional budget.

## Model definition

### Inputs
Each compression method takes a context KV cache and, depending on protocol, either does or does not have the query visible during scoring. The audit feeds these methods fixed benchmark contexts, fixed compression ratios, and fixed model backends.

### Outputs
The methods output a retained subset of KV entries or an equivalent compressed cache that is then used for downstream question answering. The audit itself outputs paired score differences, win counts, and protocol deltas.

### Training objective (loss)
The paper does not introduce a new trainable model or loss. It is an evaluation study over existing compression heuristics and published methods.

### Architecture / parameterization
The operative components are published KV-cache compression rules such as SnapKV, TOVA, AdaKV, ExpectedAttention, H2O, and KeyDiff, evaluated through one matched-budget harness on three open `7B` to `9B` models.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to determine how much published KV-cache compression rankings depend on an evaluation protocol that lets the compression rule see the query in advance, even when the deployment story is reusable context compression.

### 2. What is the method?
The method is a paired audit with two protocol arms: query-aware compression and query-agnostic compression. Every other variable is held fixed inside each cell: model, benchmark slice, compression ratio, instances, and decoding.

### 3. What is the method motivation?
The economic case for KV compression is reuse. If compression happens before future questions are known, then evaluating after the question is visible is testing a different task and can reward methods for reading the question rather than preserving reusable information.

### 4. What data does it use?
The main grid uses `144,300` paired evaluations on RULER-8192 and `40,800` evaluations on LongBench, across three open models. The study also includes bootstrap statistics, backend controls, and a tokenizer-length sanity check.

### 5. How is it evaluated?
It is evaluated with paired per-instance score differences, wins versus a best-of-three trivial baseline, cross-model consistency checks, LongBench robustness, source-code-based mechanistic interpretation of query visibility, backend controls, and benchmark-validity checks.

### 6. What are the main results?
Under the query-agnostic protocol, only KeyDiff consistently beats the best trivial baseline across `31/36` RULER cells, with mean gap `+0.171`, while SnapKV averages `-0.066` against that baseline. The protocol deltas are ordered by how visible the query is inside each method's scoring rule, from SnapKV at `+0.198` down to KeyDiff at `+0.011`. The audit also finds a backend confound large enough to withdraw H2O ranking claims and a tokenizer-length bug that silently zeroes `7` of `13` RULER subtasks for gemma-2 even without compression.

### 7. What is actually novel?
The novelty is the one-variable audit design plus the source-code-legible mechanistic hypothesis about query visibility. The paper does not just say "protocol matters"; it quantifies per-method protocol dependence and shows how easy it is to get the leaderboard wrong.

### 8. What are the strengths?
It is unusually careful about paired evaluation, coverage, confounds, and negative results. The paper also deserves credit for retracting an earlier cross-model headline once the completed run no longer supported it.

### 9. What are the weaknesses, limitations, or red flags?
The model set is still small, and one of the three is not an independent architecture family. LongBench reduces KeyDiff's exclusivity, which means the main agnostic-RULER story does not automatically transfer to all natural-text settings. H2O remains backend-confounded in this study.

### 10. What challenges or open problems remain?
The main open problems are evaluating more query-agnostic methods, broadening the model pool, and testing whether the same ranking shifts hold under more realistic shared-context serving workloads and longer natural-text documents.

### 11. What future work naturally follows?
Natural follow-ups are audits of newer reuse-first compressors, direct interventions on observation windows to test the query-visibility hypothesis causally, and benchmark suites that enforce valid tokenizer-length budgets up front.

### 12. Why does this matter for cabbageland?
Agent stacks routinely depend on cache reuse, retrieval reuse, and benchmark claims about context efficiency. This paper is a direct reminder that if the evaluation protocol does not match the deployment protocol, the ranking can be nonsense. That lesson generalizes far beyond KV caches.

### 13. What ideas are steal-worthy?
Match evaluation protocol to deployment. Hold one variable fixed and pair everything else. Benchmark against trivial baselines, not just neighboring papers. Publish retractions when a completed audit kills an attractive headline.

### 14. Final decision
**Keep it.** This is a high-value evaluation paper because it fixes a real benchmark pathology and leaves behind a reusable audit standard.
