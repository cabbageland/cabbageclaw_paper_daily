# ConflictScore: Identifying and Measuring How Language Models Handle Conflicting Evidence

## Basic info

* Title: ConflictScore: Identifying and Measuring How Language Models Handle Conflicting Evidence
* Authors: Siyi Liu, Aaron Halfaker, Dan Roth, Patrick Xia
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.26437
* Date surfaced: 2026-06-26
* Why selected in one sentence: It makes conflicting evidence inside retrieved context visible instead of letting one supporting source launder an overconfident answer.

## Quick verdict

* Highly relevant

This is the best RAG/factuality-evaluation paper in today's scan. I inspected the full arXiv PDF, including the metric definition, ConflictBench construction, frontier-model benchmarking, TruthfulQA regeneration case study, conclusion, and limitations. I did not run the released code or audit the ConflictBench labels, so exact calibration and cost numbers remain paper claims.

## One-paragraph overview

ConflictScore extends atomic-claim factuality evaluation to the case where the grounding documents disagree with each other. Instead of asking whether a claim is supported somewhere in the retrieved corpus, it decomposes a response into claims, labels each claim against each grounding document as support, contradiction, or irrelevant, and computes measures of how much conflicted evidence surrounds the response. This matters because normal factuality metrics can mark an answer as supported when one document agrees with it, even if another retrieved document contradicts it. The paper also shows that conflict feedback can improve TruthfulQA multiple-choice answers, while prompt-only instructions to hedge or balance evidence produce only modest gains.

## Model definition

### Inputs

ConflictScore takes a model response and a set of grounding documents. For benchmarking, the paper uses ConflictBench, built from datasets covering counterfactual conflicts, ambiguous conflicts, and divergent opinions. The TruthfulQA case study uses retrieved Google Search documents plus the model's initial RAG response.

### Outputs

The pipeline outputs atomic claims, claim-document relation labels, ConflictScore-Count, ConflictScore-Ratio, conflict-detection labels, benchmark statistics, and regenerated answers when conflict feedback is supplied to the model.

### Training objective (loss)

The paper does not train a new neural model with a loss. It uses prompted LLM components for claim decomposition, evidence labeling, response generation, and regeneration. The metric itself is deterministic after upstream labels: aggregate support and contradiction labels per claim, then compute conflict count and ratio scores.

### Architecture / parameterization

The method is a modular evaluation pipeline. It uses an LLM to decompose responses into atomic claims, an LLM-based verifier to label each claim-document pair, and aggregation rules for CS-C and CS-R. In the reported experiments, models include Gemini, GPT, Qwen, and other proprietary/open-weight systems, depending on the task.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It targets a blind spot in factuality and faithfulness metrics. Retrieved evidence is often not a single coherent authority; it may contain support, contradiction, ambiguity, or incompatible perspectives. Existing metrics often collapse the grounding set and count a claim as supported if any document supports it. That misses overconfident answers that ignore contrary evidence.

### 2. What is the method?

The method has three stages. First, decompose the model response into atomic factual claims. Second, evaluate every claim against every grounding document and label the relation as support, contradiction, or irrelevant. Third, aggregate those labels. ConflictScore-Count measures the fraction of claims with both support and contradiction. ConflictScore-Ratio measures the balance of contradiction against support among claims.

### 3. What is the method motivation?

Good answers under conflicting evidence should often qualify, attribute, hedge, or explain the disagreement. A response can be locally supported but globally misleading if it asserts one side as settled while retrieved evidence contains credible exceptions or opposing claims. The metric is designed to reward awareness of source conflict rather than mere retrieval support.

### 4. What data does it use?

ConflictBench has 2,293 examples across ContraQA, MacNoise-NQ, MacNoise-TQA, AmbigDocs, and ConflictingQA, with 1,280 conflicting and 1,013 non-conflicting examples. The model benchmarking slice uses 100 ConflictingQA items with conflicting passages. The TruthfulQA case study uses multiple-choice TruthfulQA with top-10 Google Search documents under RAG, Control-RAG, and ConflictScore-based regenerated RAG.

### 5. How is it evaluated?

The paper evaluates the conflict-detection subroutine on ConflictBench, benchmarks frontier models on a conflicting-evidence report-writing slice, and tests whether feeding conflict signals back to models improves TruthfulQA multiple-choice accuracy. It also analyzes improvement and harm rates on the subset of questions where ConflictScore detects conflicts in the initial response.

### 6. What are the main results?

On the 100-item ConflictingQA slice, prompt-based balancing produces only modest gains; models still often commit to a single stance despite contradictory evidence. On TruthfulQA, conflict-aware regeneration improves accuracy across all reported models: for example, gemini-3.1-flash-lite rises from 84.85 to 88.96, gpt-4.1-mini from 84.21 to 85.24, gpt-oss-20b from 82.60 to 85.03, and qwen3-30b-a3b from 80.87 to 83.16. On conflict-detected subsets, regeneration corrects many originally wrong answers while harming few originally correct ones; the reported improve rates range from 37.21% to 74.00%, while harm rates stay around 1.63% to 3.86%.

### 7. What is actually novel?

The novelty is the explicit inter-document conflict accounting. Atomic factuality pipelines already exist, and LLM-as-verifier pipelines already exist, but this paper changes the aggregation target: a claim is not simply supported or unsupported by a corpus. It can be supported by one document and contradicted by another, and that conflict should be visible to the evaluator and possibly fed back to the generator.

### 8. What are the strengths?

The metric is conceptually clean and directly useful for retrieval systems. It distinguishes "some source agrees" from "the retrieved evidence is internally divided." The TruthfulQA regeneration case is also useful because it tests ConflictScore as a corrective signal, not only as an offline diagnostic.

### 9. What are the weaknesses, limitations, or red flags?

The pipeline can be expensive because it may evaluate every claim against every document. It depends on upstream claim decomposition and evidence-labeling quality; errors there propagate into the score. Claim granularity is a real issue: a nuanced qualified statement may be scored differently depending on whether it is extracted as one integrated claim or several simpler claims. The current version also treats grounding documents as equally reliable, so a conflict between an authoritative source and a junk source is not distinguished from a conflict between two credible sources.

### 10. What challenges or open problems remain?

The main challenge is combining conflict awareness with source reliability and salience. A deployed RAG system needs to know not only that evidence conflicts, but whether the contradiction comes from stale information, unreliable sources, ambiguous definitions, or genuinely unsettled facts. Efficient approximations are also needed for long reports and large retrieval sets.

### 11. What future work naturally follows?

Add source-quality weighting, temporal validity, and discourse-aware claim extraction. Use ConflictScore-like signals during training or decoding so models learn to qualify answers when evidence is split. Build lower-cost variants that evaluate only high-impact claims or representative claim-document pairs. Combine this with stale-fact memory systems so conflicts caused by time can be handled differently from conflicts caused by disagreement.

### 12. Why does this matter for cabbageland?

Cabbageland agents will often retrieve messy evidence. A memory or retrieval system that lets one supporting note drown out contradictory evidence will produce confident nonsense with receipts. ConflictScore gives a reusable test: did the answer preserve the disagreement structure of the evidence, or did it flatten the context into a single convenient claim?

### 13. What ideas are steal-worthy?

Score claim-document relations independently before aggregating. Track support and contradiction separately instead of reducing evidence to one support bit. Feed conflict signals back into generation, but also monitor harm cases where the model is swayed by misleading majority evidence. Add source reliability as a separate axis rather than pretending conflict alone settles the question.

### 14. Final decision

Keep and cite. This is not a complete factuality solution, but it identifies a failure mode every serious RAG and agent-memory system needs to test.
