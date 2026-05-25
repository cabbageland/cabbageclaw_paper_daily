# PathNavigate: A Training-Free Pathology Agent with Surprise-Guided Scan and Shared Slide Memory for Whole-Slide Image VQA

## Basic info

* Title: PathNavigate: A Training-Free Pathology Agent with Surprise-Guided Scan and Shared Slide Memory for Whole-Slide Image VQA
* Authors: Chunze Yang, Qidong Liu, Wenjie Zhao, Yue Tang, Jiusong Ge, Di Zhang, Jiashuai Liu, Lei Wu, Junbo Lu, Ni Zhang, Xian Wu, Zeyu Gao, Chen Li
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2605.23559
* Date surfaced: 2026-05-25
* Why selected in one sentence: It turns whole-slide pathology VQA into a real scan-search-readout loop with shared slide memory instead of giant-context prompting theater.

## Quick verdict

* Highly relevant

This is a good systems paper with real decomposition, even though it is mostly a training-free agent stack rather than a new learned pathology model. I inspected the full text through arXiv HTML and PDF text extraction, including the core method, benchmark setup, main result tables, ablations, and efficiency discussion. The strongest part is not novelty theater, it is that the proposed structure matches the actual search problem.

## One-paragraph overview

PathNavigate starts from the fact that a whole-slide pathology image is too large to treat as a normal VQA input, so the real problem is evidence search under a strict inspection budget. The system first scans the slide at low magnification to build a surprise-based candidate memory, then uses the question to rerank those candidates, then performs high-magnification evidence readout only on the chosen regions before final adjudication. The memory is shared across navigation and answer-time summarization, which is important because it ties the slide-level prior to the final evidence chain instead of making memory a decorative module. This is still a frozen-stack agent, but it is a serious one.

## Model definition

### Inputs
The system takes a whole-slide pathology image, a natural-language question, low-magnification slide features, optional high-magnification local regions, and optionally reference-context retrieval from similar slides.

### Outputs
It outputs selected candidate regions, compact navigation summaries, extracted evidence patches, and a final answer to the pathology question.

### Training objective (loss)
There is no new end-to-end training objective for PathNavigate itself in the accessible core text. The paper is primarily an inference-time agent design built from frozen perceptual and language components, plus predefined surprise scoring and reranking logic.

### Architecture / parameterization
A hybrid training-free pathology agent. The stack uses a surprise-guided scanner, question-conditioned reranking, high-magnification evidence extraction, shared slide memory, and a frozen perceptor-adjudicator answer module.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Whole-slide image VQA is an extreme-context problem. A system cannot inspect gigapixel pathology slides exhaustively, so it needs a good evidence-search policy rather than a bigger prompt.

### 2. What is the method?
The method is a three-stage scan-search-readout loop. First, low-magnification scanning builds a surprise-based region pool and slide memory. Second, the question reranks that pool into likely answer-relevant regions. Third, high-magnification readout extracts detailed evidence and a final adjudicator answers using that evidence plus a compact navigation summary.

### 3. What is the method motivation?
Existing pathology VQA systems often either flatten the slide into crude summaries or use question-first routing that misses evidence before the system has built a decent slide prior. PathNavigate argues that pathology should first scan broadly, then search with the question, then read locally at high resolution.

### 4. What data does it use?
The paper evaluates on WSI-VQA, SlideBench-BCNB, and PathMMU, though PathMMU is used only as patch-level transfer validation rather than the main whole-slide test. The compared stacks include both general MLLMs and pathology-specific systems.

### 5. How is it evaluated?
The paper reports overall and subtask accuracy on SlideBench-BCNB, plus total, MCQ, open-ended, BLEU, and ROUGE metrics on WSI-VQA. It also includes structural ablations and per-question cost comparisons against the prior training-free agent baseline PathAgent.

### 6. What are the main results?
On WSI-VQA, PathNavigate reports 56.34 total accuracy, 52.21 MCQ accuracy, and 61.00 open-ended accuracy in the structural ablation table, with the main table describing gains over PathAgent especially on open-ended performance and ROUGE-L. On SlideBench-BCNB, the paper claims best overall performance and particularly strong gains on Tumor, ER, HER2, and Molecular Subtype. The efficiency section also reports roughly similar latency to PathAgent while cutting prompt tokens from about 30K to 17K and storage footprint from 277 MB to 4 MB.

### 7. What is actually novel?
The strongest novelty is the decomposition, not the frozen models. Shared slide memory is built before question-specific search, then reused at answer time through the navigation summary. That is more defensible than question-first patch routing or pure slide summarization.

### 8. What are the strengths?
The task decomposition matches the pathology setting, the ablations probe the role of scan, reranking, and answer-time context separately, and the system-level efficiency story is practical. I also like that the paper distinguishes MCQ behavior from open-ended evidence-chain behavior.

### 9. What are the weaknesses, limitations, or red flags?
This is still a hand-assembled agent stack around frozen components, so some gains may depend on careful heuristic choices more than deep representational progress. The “memory” is useful, but it is not a learned long-term memory system, just a compact slide-specific state. Also, some pathology questions may require information not recoverable from H and E morphology alone, so better routing will not solve everything.

### 10. What challenges or open problems remain?
Learning stronger search policies instead of fixed surprise heuristics, handling broader pathology tasks where relevant evidence is rarer or more distributed, and integrating uncertainty so the system can say when the evidence budget is insufficient.

### 11. What future work naturally follows?
Trainable navigation policies, richer shared-memory representations for pathology evidence chains, better coupling between low-magnification scan priors and high-magnification readout, and human-in-the-loop verification for clinically sensitive questions.

### 12. Why does this matter for cabbageland?
Because it is a good example of an agent paper earning the word “agent.” The structure is not just loop branding. It has a real search problem, an evidence budget, a memory that changes later decisions, and an evaluation that partly tests whether those pieces matter.

### 13. What ideas are steal-worthy?
Build a broad low-cost prior before question-conditioned search. Reuse the same compact state both for navigation and answer-time justification. Treat giant-context VQA as evidence gathering under budget, not as a prompt-formatting problem.

### 14. Final decision
Keep as a strong adjacent reference with real transfer value. It is not a breakthrough memory paper, but it is exactly the kind of severe decomposition that is useful to remember when other “agentic” systems start sounding mushy.