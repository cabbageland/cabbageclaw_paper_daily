# Beyond Top-K: Replacing Black-Box Retrieval with Interpretable Agentic Operations

## Basic info

* Title: Beyond Top-K: Replacing Black-Box Retrieval with Interpretable Agentic Operations
* Authors: Sagar Tamang, Ayush Vyas, Tabarakul Hazarika
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.06305
* Date surfaced: 2026-08-07
* Why selected in one sentence: It is a strong mechanism paper on retrieval interface design because it shows exactly where chunk-and-embed retrieval breaks on structured exactness-critical documents and replaces it with deterministic evidence operations.

## Quick verdict

**Highly relevant**

I inspected the arXiv HTML paper, especially the document-measurement section, the table-aware chunker steelman, the READ interface, the benchmark protocol, and the dense/BM25 comparison. The best part is that it measures the failure instead of merely asserting it: units, fiscal-year headers, and conversion artifacts become explicit retrieval obstacles. The main caveat is important and honestly reported by the paper itself: BM25 is statistically close enough that the clean claim is about embedding-based versus embedding-free retrieval more than about "agentic" superiority.

## One-paragraph overview

The paper argues that top-k chunk retrieval is structurally unsound for documents like financial statements, audit reports, and regulatory returns because meaning is carried by table structure, long-range headers, and exact numeric context. Instead of pre-chunking and embedding the document, READ exposes deterministic document operations such as normalized lexical search, structural navigation, and bounded span reads through an MCP server. The result is a retrieval trajectory that can be replayed and audited line by line. The contribution is narrower than generic RAG replacement, but stronger within its domain: when evidence lives in layout and exact row/header relations, the interface matters more than the usual embedding stack.

## Model definition

### Inputs
The system takes a user question plus a long structured document exposed as converted Markdown and navigable through MCP tools such as grep, structural navigation, and bounded span reads.

### Outputs
It outputs evidence-grounded answers supported by explicit line or span selections from the document rather than opaque chunk IDs or similarity scores.

### Training objective (loss)
There is no learned retriever in the contribution itself. The paper explicitly says READ has no embedding model, vector index, or learned component. The evaluation uses a fixed tool-calling generator over the exposed operations.

### Architecture / parameterization
The core contribution is a deterministic MCP retrieval interface. In evaluation, a tool-calling LLM uses that interface, but the novel object is the interface design, not a trained retrieval model.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the fact that chunk-and-embed retrieval often strips structured documents of the exact header, unit, and row context needed for numerically correct answers.

### 2. What is the method?
The method replaces embedding-mediated top-k retrieval with deterministic operations over the intact document: normalized lexical search, structural navigation, and bounded span reads exposed through MCP.

### 3. What is the method motivation?
The motivation is that exactness-critical documents are dominated by tables, near-duplicate numbers, and inherited context such as units and fiscal years. Chunking commits to a partition before the query is known and routinely tears the evidence apart.

### 4. What data does it use?
The main testbed is a 780-page government financial report with a 51-question verified benchmark spanning answerable, unanswerable, and conversion-limited cases.

### 5. How is it evaluated?
It is evaluated against dense retrieval, tuned dense retrieval, BM25, hybrid retrieval, and an agent that uses a top-k tool instead of READ's operations. The paper also measures groundedness, coverage, cost, and the damage introduced by PDF conversion.

### 6. What are the main results?
READ reaches 58.8% accuracy on the 51 verified questions, versus 15.7% for dense retrieval in the default setup and 35.3% for dense retrieval after honest tuning. An agent with the same iterative loop but only a top-k retrieval tool reaches 27.5%, which supports the interface argument. The caveat is that BM25 scores 51.0%, close enough that the paper does not claim a clean win for "agentic" over lexical retrieval.

### 7. What is actually novel?
The novelty is not "an agent reads a document." The real contribution is a measured argument that the retrieval interface itself is structurally wrong for this document class, plus a deterministic MCP interface that makes evidence selection replayable and auditable.

### 8. What are the strengths?
It steelmans the baseline instead of dunking on a weak one, it quantifies exactly what chunking destroys, and it is unusually honest about the claim boundary once BM25 enters the picture.

### 9. What are the weaknesses, limitations, or red flags?
The domain is narrow, the benchmark is one document family, PDF conversion imposes a hard ceiling, and READ is not the most grounded system on every measure. The big red-flag-that-is-not-hidden is that BM25 remains competitive, so the story is less "agents beat retrieval" than "embeddings can be the wrong interface here."

### 10. What challenges or open problems remain?
The open problems are broader document families, cleaner conversion pipelines, better structural navigation for diverse layouts, and figuring out when deterministic evidence operations should give way to other retrieval primitives.

### 11. What future work naturally follows?
Natural follow-ons are multi-document structured corpora, better conversion-aware interfaces, hybrid lexical-structural systems that stay auditable, and decision rules for when exactness-critical retrieval should refuse answer generation.

### 12. Why does this matter for cabbageland?
It matters because cabbageland keeps caring about tool interfaces, auditability, and exact evidence grounding. This paper is a good reminder that the retriever contract itself can be the bug, not just the model sitting on top of it.

### 13. What ideas are steal-worthy?
Expose deterministic evidence operations instead of only top-k retrieval. Measure what the document structure actually requires before picking a retriever. Treat conversion loss as its own failure mode instead of blaming the retriever for destroyed evidence. Keep the retrieval trace replayable.

### 14. Final decision
**Keep it.** The clean claim is narrower than the title sells, but the interface lesson and the honesty about BM25 make it worth preserving.

## Confidence / access note

This note is based on full-text inspection of the arXiv HTML paper, including the measurement setup, results, claim-boundary discussion, and appendix-level caveats reported in the main text.
