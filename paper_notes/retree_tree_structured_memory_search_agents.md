# Self-Correcting Long-Horizon Search Agents via Tree-Structured Memory

## Basic info

* Title: Self-Correcting Long-Horizon Search Agents via Tree-Structured Memory
* Authors: Aijun Yang, Qianxue Guo, Ziyi Huang, Yuxuan Chen, Shiyou Qian, Jian Cao
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.10676
* Date surfaced: 2026-08-12
* Why selected in one sentence: It treats search memory as revisable evidence state with explicit introducers and descendants instead of a transcript or rolling summary.

## Quick verdict

* Must read direct paper

I inspected the arXiv HTML full text. This is a strong search-agent paper because it does not confuse bounded context with solved state management. The valuable move is structural revision at the point a false claim entered the state.

## One-paragraph overview

The paper introduces ReTree, a tree-structured working memory for search agents that stores bounded summaries, source-linked evidence items, and revision history per node. When newly retrieved evidence contradicts an earlier claim, ReTree finds the node that introduced the claim, replaces the outdated evidence, regenerates the local summary, prunes descendants that depended on the refuted state, and resumes search from the repaired branch. Across 2,149 questions from Bamboogle, 2Wiki, HotpotQA, and FRAMES, it reaches 44.0% overall judge accuracy and 28.0% EM, beating Full-Trajectory ReAct by 13.9 judge-accuracy points and the strongest aggregate bounded baseline by 3.0 points. On a 600-question FRAMES attribution diagnostic it also reaches the best citation precision, recall, and F1.

## Model definition

### Inputs
The system takes a question, live search results, retrieved passages, and the current evidence-tree state built from prior steps.

### Outputs
It outputs updated search state, cited intermediate claims, and a final answer grounded in retrieved passages.

### Training objective (loss)
There is no model-training objective in the contribution itself. This is a search-memory design and evaluation paper.

### Architecture / parameterization
ReTree keeps an external dependency tree over evolving search state. Each node stores a bounded task summary, local evidence with source pointers, and revision history. The policy sees only the current summary plus top-k relevant evidence items, while the external tree keeps the richer provenance and dependency structure.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to stop long-horizon search agents from accumulating noisy transcript state and from silently carrying forward reasoning built on refuted evidence.

### 2. What is the method?
The method represents search state as an evidence tree, detects contradictions against source-linked facts, backtracks to the introducing node of the contradicted claim, prunes dependent descendants, and resumes search from the repaired state.

### 3. What is the method motivation?
Rolling summaries and flat updates can keep context short, but they often obscure where a claim came from and which later reasoning depends on it. That makes contradictions hard to repair cleanly.

### 4. What data does it use?
It uses 125 Bamboogle questions, 600 2Wiki questions, 600 HotpotQA questions, and 824 FRAMES questions, for 2,149 total evaluations.

### 5. How is it evaluated?
It compares answer quality, attribution quality, context footprint, and compute against Full-Trajectory ReAct, FlatUpdate, and ReportMemory under matched search limits.

### 6. What are the main results?
ReTree reaches 44.0% overall judge accuracy and 28.0% EM, compared with 30.1% and 20.6% for Full-Trajectory ReAct. It also beats the strongest aggregate bounded baseline by 3.0 judge-accuracy points. On FRAMES attribution it reaches 42.8 CiteF1 with 14.8% uncited claims, versus 31.5 and 33.1% for Full-Trajectory ReAct.

### 7. What is actually novel?
The novelty is not "tree search" in the usual sense. It is a dependency tree over evolving evidence state, used to identify where a contradictory fact entered the state and which descendants should be regenerated.

### 8. What are the strengths?
The state design is sharp, the attribution metrics are useful, and the paper separates three things cleanly: bounded context construction, durable source provenance, and contradiction-triggered state repair.

### 9. What are the weaknesses, limitations, or red flags?
Overall accuracy is still modest, the search setting depends on live retrieval and judge-based evaluation, and hard subtree pruning may discard branches that are recoverable in softer ways.

### 10. What challenges or open problems remain?
Open problems include softer belief revision, richer retrieval policies, better contradiction detection under ambiguity, and extending the idea beyond search into tool-use and coding workflows.

### 11. What future work naturally follows?
Typed evidence-state representations for broader agents, hybrid revision policies that do more than prune, and tighter integration between retrieval, attribution, and state repair all follow naturally.

### 12. Why does this matter for cabbageland?
Cabbageland keeps caring about the difference between "the model saw it once" and "the system knows what currently holds." ReTree gives a concrete pattern for editable, source-addressable working memory.

### 13. What ideas are steal-worthy?
Record the introducing state of each fact. Keep compact policy context while preserving richer external evidence lineage. Repair contradictions by revising dependent state, not just by replacing the latest fact.

### 14. Final decision
Keep as a preserved note. It is one of the cleaner recent papers on editable agent state, and the dependency-tree framing is worth reusing outside search.

## 6. Mandatory critical angles

This paper is strongest on state representation and attribution discipline. The main caution is that its gains do not magically solve search quality by themselves; the paper improves a weak state abstraction, but the absolute success ceiling is still low.

## 7. Writing style

The right tone is clearly favorable, with a little skepticism about the remaining performance ceiling. This is a good memory paper, not proof that search agents are suddenly robust.

## 8. Repository output format

Saved as a preserved paper note because the dependency-tree memory design and source-aware contradiction repair are both reusable ideas.
