# Tools Are Not Islands: Set-Level Tool Retrieval for LLM Agents via Query-Conditioned Hyperedge Prediction

## Basic info

* Title: Tools Are Not Islands: Set-Level Tool Retrieval for LLM Agents via Query-Conditioned Hyperedge Prediction
* Authors: Xinyi Hong, Pinjun Dong, Xinyang Yu, Binyan Jiang
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.25718
* Date surfaced: 2026-07-29
* Why selected in one sentence: It attacks the right retrieval object for tool-using agents by scoring tool sets as sets instead of pretending independent top-k ranking is enough.

## Quick verdict

**Highly relevant**

This is a solid direct paper because it fixes a genuine mismatch between what tool retrievers score and what downstream agents actually need. The central move is simple but important: retrieve the complete jointly useful set, not just a ranked pile of individually plausible APIs. I inspected the full arXiv HTML paper, especially the method, main results, ablations, and transfer analyses.

## One-paragraph overview

The paper argues that tool retrieval for LLM agents is fundamentally a set-level problem. Existing systems usually score tools independently or generate tool choices sequentially, so they never directly evaluate whether the candidate set as a whole covers the task. The proposed method, HYSET, reframes retrieval as query-conditioned hyperedge prediction over a tool co-invocation hypergraph. That lets the model represent both joint usefulness and cardinality-specific interactions. The important result is not just better recall. HYSET improves set completeness and downstream pass rate, which is the metric that actually tracks whether the agent got the right bundle of tools before it started acting.

## Model definition

### Inputs
The inputs are a user query and a large tool library with observed tool co-invocation structure.

### Outputs
The output is a pre-selected candidate tool set intended to cover the task before the downstream agent executes.

### Training objective (loss)
The model is trained as a query-conditioned hyperedge predictor, with the tool set as the unit of supervision rather than independent per-tool scores alone.

### Architecture / parameterization
HYSET builds a tool co-invocation hypergraph, scores candidate sets through set-level interactions, and uses cardinality-specific interaction modeling so that compatibility patterns can depend on how many tools a task requires.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to solve the mismatch between independent-tool retrieval and real agent tasks, where success often depends on recovering the right combination of tools rather than the best-looking single API.

### 2. What is the method?
The method is HYSET, a set-level retriever that formulates tool retrieval as query-conditioned hyperedge prediction. Instead of scoring each tool in isolation or assembling a set autoregressively, it scores the candidate set directly.

### 3. What is the method motivation?
Independent top-k retrieval breaks whenever tool utility is a joint property. A travel task may need flight, hotel, weather, and currency tools together, while a second flight API is redundant even if its individual similarity score is high. The paper is motivated by this structural failure.

### 4. What data does it use?
The main evaluation is on ToolBench, including held-out tools, held-out categories, and unseen domains. The paper also compares annotation-only and execution-feedback training regimes.

### 5. How is it evaluated?
It is evaluated with Recall@5, COMP@5 for complete set coverage, and end-to-end pass rate. The paper also includes ablations on set-level scoring, cardinality-specific interactions, alternative set architectures, and zero-shot or few-shot generalization.

### 6. What are the main results?
HYSET outperforms every baseline on retrieval and end-to-end metrics in the paper's main setting. Relative gains over the strongest baseline reach 15.3 percent for the BERT configuration and 17.8 percent for Qwen on retrieval measures, with the biggest gains on set completeness: COMP@5 improves by 10.8 percent and 11.6 percent relative over ToolGen. End-to-end pass rate improves by as much as 13.1 percent. Even in the annotation-only regime, HYSET reaches 77.02 percent COMP@5. The few-shot transfer result is also good: five examples per target category recover 93.2 percent of fully supervised performance.

### 7. What is actually novel?
The novelty is the formulation. Treating tool retrieval as hyperedge prediction over tool sets gives a clean conceptual object that lines up with the downstream task better than independent ranking or sequence generation.

### 8. What are the strengths?
The strongest part is that the paper measures the right metric and then proves its mechanism with ablations. When the set-level objective is removed, COMP@5 and pass rate fall noticeably, which makes the core claim much more believable than a generic leaderboard gain.

### 9. What are the weaknesses, limitations, or red flags?
The work is still tightly coupled to ToolBench-style tool ecosystems. Some end-to-end gains depend on execution-feedback training, so not every margin should be read as architecture alone. Also, the human pass-rate margin is weaker than the clean retrieval margins.

### 10. What challenges or open problems remain?
A big open question is how well set-level retrieval scales when tools are noisier, more hierarchical, or dynamically generated. Another open problem is combining set completeness with downstream planning cost, since not every complete set is equally usable by the agent.

### 11. What future work naturally follows?
Future work should test whether the same set-level framing helps in environments with compositional tool schemas, mutable APIs, or multimodal tools. It would also be useful to couple the retriever to stronger uncertainty estimates so the agent knows when retrieval itself is incomplete.

### 12. Why does this matter for cabbageland?
It matters because cabbageland keeps building agents that need the right bundle of capabilities, not just the shiniest individual option. This paper is a direct reminder that retrieval units should match execution units.

### 13. What ideas are steal-worthy?
Measure complete-set coverage explicitly instead of hiding behind recall. Score candidate sets directly when downstream success depends on complementarity. Use cardinality-specific interactions rather than assuming pairwise compatibility is invariant across task sizes.

### 14. Final decision
**Keep it.** It is a useful framing paper with enough ablation evidence to make the set-level claim feel real rather than rhetorical.
