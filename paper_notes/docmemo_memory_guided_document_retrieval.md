# DocMemo: Dynamic Evidence Discovery via Probabilistic Memory-Guided Retrieval for Multi-Modal Document Understanding

## Basic info

* Title: DocMemo: Dynamic Evidence Discovery via Probabilistic Memory-Guided Retrieval for Multi-Modal Document Understanding
* Authors: Hanshu Yao, Janfeng Zhong, Niu Lian, Jinpeng Wang
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.07067
* Date surfaced: 2026-08-10
* Why selected in one sentence: It turns long-document evidence search into an explicit evolving memory state with Bayesian page-belief updates instead of pretending repeated retrieval passes are already stateful.

## Quick verdict

* Highly relevant

I inspected the arXiv HTML full text. This is a good memory-and-retrieval paper because it has an actual state update mechanism rather than generic "agentic retrieval" branding. The tri-level memory is concrete, the Bayesian update loop is specific, and the efficiency gains are strong enough to matter.

## One-paragraph overview

DocMemo addresses long-document visual question answering where the real bottleneck is not raw reading, but finding and revising evidence across many pages under a limited budget. The authors argue that both static top-k retrieval and many iterative baselines are effectively stateless: once the first page pool is chosen, later rounds mostly rebuild context rather than maintaining a structured exploration state. Their solution is a tri-level document memory. Document Schema Memory holds reusable structural priors about the document, Page Belief Memory tracks evolving page relevance as Beta-distributed uncertainty, and Question Episodic Memory stores query-local reasoning traces and missing-information notes. Retrieval then becomes a feedback loop: Thompson sampling proposes pages, the reasoner marks useful and irrelevant pages, Bayesian belief updates revise page posteriors, spatial propagation nudges nearby pages, and adaptive-granularity evidence access adds fine-grained crops for locally dense regions such as tables.

## Model definition

### Inputs
The framework takes a long multimodal document, a user query, precomputed page embeddings and summaries, and the current retrieval-reasoning state.

### Outputs
It outputs an answer, a multi-round evidence trajectory, updated memory states, and improved page selection over time.

### Training objective (loss)
The paper does not introduce a new end-to-end training loss for the backbone model. The contribution is an inference-time retrieval-reasoning-memory update framework around a VLM and retriever.

### Architecture / parameterization
The core architecture is tri-level memory: document schema memory for structural priors, page belief memory modeled with Beta distributions, and question episodic memory for trajectory notes and refined queries. Retrieval uses Thompson sampling over evolving page posteriors, plus locality-aware spatial propagation and adaptive-granularity visual evidence access.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to improve long-document multimodal reasoning when the necessary evidence is sparse, heterogeneous, and spread across many pages.

### 2. What is the method?
The method maintains explicit memory over the document structure, current page relevance beliefs, and the question's evolving search trajectory. After each reasoning round, useful and irrelevant pages update the page-belief posterior, which then guides the next retrieval step.

### 3. What is the method motivation?
Static retrieval commits too early, and many iterative methods only simulate iteration while rebuilding the retrieval state from scratch. The authors want retrieval to become an actual evolving belief process.

### 4. What data does it use?
The paper evaluates on MMLongBench-Doc, LongDocURL, and PaperTab. The system uses Qwen3.5-VL-9B as the backbone VLM and ColQwen2.5 for visual retrieval.

### 5. How is it evaluated?
It reports accuracy as the primary metric, along with Evidence Recall and All-Hit Rate for evidence acquisition. It also runs ablations on memory removal, Bayesian updating removal, and adaptive-granularity evidence access.

### 6. What are the main results?
DocMemo outperforms the strongest agentic baselines by 3.7 points on MMLongBench-Doc, 8.8 points on LongDocURL, and 15.0 points on PaperTab. On MMLongBench-Doc it reaches 71.3% overall accuracy. Removing the full memory or Bayesian updating drops accuracy to 68.5% and 68.8%, respectively. During multi-round retrieval, cumulative Evidence Recall rises from 28.32% to 69.56% and All-Hit Rate from 12.90% to 58.05%. The method also averages only 1.24 rounds per question and is about 2.4x more efficient than the fixed-three-round SimpleDoc baseline under the paper's call-count proxy.

### 7. What is actually novel?
The novelty is not just using multiple retrieval rounds. The contribution is explicit cross-round state propagation with a probabilistic page-belief memory and question-trajectory memory that actually influence subsequent retrieval.

### 8. What are the strengths?
The memory design is concrete and interpretable. The process metrics are strong, not just the final score. The method also earns points for efficiency rather than only accuracy inflation.

### 9. What are the weaknesses, limitations, or red flags?
Evaluation still relies on GPT-4.1 as an automatic judge, though the paper reports 96.7% agreement with human review on a sampled subset. The system also depends on nontrivial offline preprocessing, page embeddings, and document-specific structure extraction.

### 10. What challenges or open problems remain?
The harder open problem is scaling this kind of stateful retrieval to interactive agents that mix documents with tools, web evidence, or long-term cross-session memory instead of only one document at a time.

### 11. What future work naturally follows?
Better uncertainty-aware stopping rules, richer memory update signals than page usefulness labels, and cross-document or cross-session versions of page-belief memory all follow naturally.

### 12. Why does this matter for cabbageland?
This is exactly cabbageland taste: if a system says it has memory, ask what the memory object is, how it updates, and how it changes future computation. DocMemo passes that test better than most retrieval-agent papers.

### 13. What ideas are steal-worthy?
Separate structural priors, evolving beliefs, and episodic query traces into different memory objects. Treat retrieval as posterior updating rather than repeated top-k search. Use process metrics such as evidence recall growth and all-hit rate, not only final answer accuracy.

### 14. Final decision
Keep as a preserved note. The memory design is explicit, the gains are substantial, and the retrieval-state framing is directly reusable for broader evidence-grounded agents.

## 6. Mandatory critical angles

This paper is strongest on mechanism clarity and process-level evaluation. It does a good job showing that the gains come from state updates rather than simply spending more rounds. The main caution is that the deployment stack is somewhat heavy and document-specific, so the idea matters more than the exact implementation choices.

## 7. Writing style

The right tone is approving and slightly severe. This is a retrieval paper that earns the word "memory" instead of using it as branding glitter.

## 8. Repository output format

Saved as a preserved paper note because the tri-level memory and Bayesian page-belief update pattern are directly useful for future work on document reasoning, retrieval agents, and evidence-grounded planning.
