# PMMC: Prospective Multimodal Memory Compilation for Long-Term LVLM Agents

## Basic info

* Title: PMMC: Prospective Multimodal Memory Compilation for Long-Term LVLM Agents
* Authors: Jingyu Sun, Yan Lin, Yuyang Xue, Yifan Wang, Zhengtao Yao, Rui Qian, Zefeng Xu, Jiachen Li, Xianyang Liu, Jiancheng Pan, Jingyuan Sun, Syed Murtuza Baker, Hongpeng Zhou
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.00962
* Date surfaced: 2026-08-04
* Why selected in one sentence: It is the strongest memory paper in today's batch because it moves query-conditioned multimodal access planning into write time and verifies the programs before they ever get used.

## Quick verdict

**Highly relevant**

I inspected the arXiv HTML paper, especially the compiler setup, prospective question generation, execution-grounded verification, online routing, ablations, and Question Bank coverage analysis. The paper is structurally interesting because it stops treating memory as a passive store and instead compiles likely future access programs during consolidation. The biggest caveats are the extra write-time cost, incomplete Question Bank coverage, and the fact that online behavior still falls back to multimodal RAG when routing confidence or readiness checks fail.

## One-paragraph overview

PMMC treats long-term multimodal memory as something that can be prepared in advance rather than queried from scratch every time. During memory consolidation, a Questioner predicts plausible future questions, a Planner turns each one into a typed multimodal access program, and a Doubter verifies whether the program can actually recover enough evidence from the visible memory. Accepted question-program pairs enter a Question Bank that stores access strategies rather than answers. At query time, the system routes the incoming question to a compiled program, re-executes it over the currently visible memory, materializes the retrieved evidence, and answers from that evidence. If routing or readiness is weak, it falls back to multimodal RAG.

## Model definition

### Inputs
The system takes a multimodal interaction history with dialogue text, source images, optional captions, temporal and session metadata, and then a real incoming user query with optional query images.

### Outputs
It outputs a Question Bank of prospective questions and verified memory-access programs, then at inference time outputs retrieved source evidence and a grounded answer.

### Training objective (loss)
There is no single new end-to-end training loss that defines PMMC. The contribution is a compiler-like memory framework built from prompted components, typed contracts, and execution-backed verification rather than newly trained model weights.

### Architecture / parameterization
PMMC uses a Questioner-Planner-Doubter pipeline over bounded compilation units, a typed requirement contract for each prospective question, execution-grounded readiness checks, a frozen runtime Question Bank, and multimodal RAG fallback for low-confidence or insufficiently supported queries.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the inefficiency and brittleness of multimodal long-term memory systems that wait until query time to figure out how evidence should be retrieved and combined.

### 2. What is the method?
The method is prospective multimodal memory compilation: predict likely future questions during consolidation, compile them into typed evidence-access programs, verify those programs by actual execution, and reuse them later as runtime routes.

### 3. What is the method motivation?
Different future questions need different memory interfaces. Some need text, some need image-text binding, some need raw-image evidence, and some need temporal or multi-hop evidence. A fixed retrieval policy is too blunt for that variety.

### 4. What data does it use?
The main evaluation uses MEMLENS and Mem-Gallery across four answer backbones: GPT-5-mini, Claude Haiku 4.5, Qwen3.5-9B, and Qwen3.5-27B.

### 5. How is it evaluated?
It is evaluated with Harmonized Judge score, F1, evidence recall, raw-image evidence hit, program success, fallback rate, and query-time versus write-time token costs, plus ablations over the Doubter, dynamic planning, raw-image access, and refinement depth.

### 6. What are the main results?
PMMC ranks first in six of eight backbone-benchmark settings and reaches a 49.9 macro overall Harmonized Judge average versus 46.7 for the strongest baseline. In the Qwen3.5-9B ablations, full PMMC reaches 92.1 program success. Removing the Doubter drops quality and program success, replacing the dynamic planner with a fixed plan hurts most sharply, and removing raw-image access hurts Mem-Gallery especially hard. Question Bank coverage reaches 82.1% at top-5 candidates, and an oracle selector suggests about 8.4 points of remaining headroom.

### 7. What is actually novel?
The novelty is not just adding another memory store. The more interesting move is compiling and execution-validating question-conditioned access programs before the query arrives, then using the resulting Question Bank as a routing index rather than an answer cache.

### 8. What are the strengths?
The paper keeps original text and images as canonical evidence, uses explicit readiness checks, shows real ablation-based dependence on its components, and exposes the write-time versus query-time trade-off instead of hand-waving it away.

### 9. What are the weaknesses, limitations, or red flags?
The write-time cost is substantial. Coverage is incomplete, routing still leaves meaningful headroom, and the system does not replan online beyond falling back to multimodal RAG. The whole design also assumes future information needs are predictable enough to compile in advance.

### 10. What challenges or open problems remain?
Better Question Bank coverage, stronger candidate ranking, uncertainty-aware routing, and lower write-time cost remain open. The paper also leaves open how self-evolving the compiled tool inventory should become.

### 11. What future work naturally follows?
More adaptive routing, uncertainty-aware compilation, more compact program representations, and learned criteria for when prospective compilation is worth the write-time cost would all follow naturally.

### 12. Why does this matter for cabbageland?
It matters because cabbageland keeps touching long-horizon multimodal agents and persistent memory. PMMC gives a clean architectural idea: move some of the hard memory reasoning into consolidation time, verify it there, and keep the runtime interface small and explicit.

### 13. What ideas are steal-worthy?
Treat prospective questions as a memory-compilation target. Store access programs instead of only summaries or embeddings. Keep provisional answers private to the compiler and strip them from the runtime memory bank. Use execution-backed readiness checks before accepting a memory route.

### 14. Final decision
**Keep it.** This is a direct memory paper with a real mechanism, clear trade-offs, and a reusable design lesson.
