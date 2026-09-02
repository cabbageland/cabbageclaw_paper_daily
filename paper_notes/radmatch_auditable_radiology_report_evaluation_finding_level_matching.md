# RadMatch: Auditable Radiology Report Evaluation via Finding-Level Matching

## Basic info

* Title: RadMatch: Auditable Radiology Report Evaluation via Finding-Level Matching
* Authors: Charles Corbiere, Leo Machado, Aubin Charley, Baptiste Callard, Pierre Manceron, Corentin Dancette
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2609.01470
* Date surfaced: 2026-09-02
* Why selected in one sentence: It turns radiology-report evaluation from an opaque scalar into a persisted finding-level error record.

## Quick verdict

* Useful

I inspected the full arXiv HTML text, especially the extraction-matching-scoring pipeline, the actionable-error metric, the benchmark comparisons, and the discussion / latency sections. This is worth keeping as adjacent inspiration because the key idea is broader than radiology: if a metric throws away the structure people need to inspect, it stops being operationally useful even when its correlation looks fine.

## One-paragraph overview

RadMatch evaluates radiology reports by decomposing them into atomic findings, matching candidate findings to reference findings, and then scoring each match with clinical significance across a fixed set of attribute dimensions. The main output is not one opaque LLM score but an actionable-error count backed by a persisted record of which findings were missed, hallucinated, or only partially matched and along which dimensions they failed. That lets the metric do something ordinary LLM judges cannot: show a clinician or model developer where the errors actually are. The paper's larger point is good even outside radiology. Once a strong judge saturates correlation, the right question is no longer "who has the highest tau?" but "which metric still leaves an audit trail?"

## Model definition

### Inputs
A reference radiology report, a candidate report, and optionally a study indication. The prompts also include modality-specific few-shot exemplars reviewed by radiologists.

### Outputs
Extracted findings for both reports, matched finding pairs, attribute-level error characterizations, safety-oriented views, and the final actionable-error count.

### Training objective (loss)
There is no model training in the paper's main method. RadMatch is an inference-time, few-shot, multi-call metric. The deterministic tail aggregates the LLM outputs into the actionable-error score and diagnostic views.

### Architecture / parameterization
Four LLM calls plus deterministic aggregation: finding extraction from the reference and candidate, finding-level matching, and batched attribute grading. The attribute schema covers status, location, severity, morphology, certainty, longitudinal comparison, and measurement.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
How do we evaluate AI-generated radiology reports in a way that is clinically aligned and still interpretable enough to audit?

### 2. What is the method?
Decompose report comparison into extracted findings, matched finding pairs, and significance-aware attribute scoring, then report an actionable-error count instead of a single opaque quality score.

### 3. What is the method motivation?
Existing LLM metrics correlate better with radiologists than lexical metrics, but they still collapse all reasoning into one score that neither clinicians nor developers can inspect meaningfully.

### 4. What data does it use?
Two expert-annotated chest X-ray benchmarks: ReXVal and RadEvalExpert. The prompts are designed to extend to other anatomies and modalities via few-shot examples, but the evaluated benchmarks are chest X-ray only.

### 5. How is it evaluated?
By agreement with radiologist error counts using `|tau_b|`, per-error and per-subset diagnostic views, safety-oriented recall / precision, disagreement audits, and cost / latency measurements across different judge models.

### 6. What are the main results?
With Opus 4.8, RadMatch reaches `|tau_b| = 0.79` on ReXVal, matching inter-radiologist agreement, and `|tau_b| = 0.58` on RadEvalExpert, more than doubling the best prior metric at `0.24`. The metric remains near-frontier even with open judges: Gemma 4 31B reaches strong agreement while removing API cost. The pipeline costs about `$0.06` per pair with a frontier API judge and about `10.7 s` serial latency with Opus 4.8, which drops to about `1.8 s` with eight workers.

### 7. What is actually novel?
The novelty is not "LLM as judge." It is the persisted finding-level decomposition and the choice to score clinically actionable errors instead of only optimizing raw correlation.

### 8. What are the strengths?
It produces auditable records, keeps clinical significance explicit, reports cost and latency, and is frank that interpretability and actionability are now the real value once raw agreement saturates.

### 9. What are the weaknesses, limitations, or red flags?
The evaluated scope is still chest X-ray only. Several stages are LLM calls and therefore stochastic. The multi-call pipeline is more complex than a trivial single-call judge, and on raw correlation alone that simpler baseline can already be competitive.

### 10. What challenges or open problems remain?
Broader benchmark coverage for CT / MRI, better matching on dense reports with many benign findings, and reducing stage-level stochasticity without losing auditability.

### 11. What future work naturally follows?
Adapting the same structured metric design to other clinical modalities, integrating it into report-generation training loops, and exporting similar decomposed evaluation objects in non-medical domains.

### 12. Why does this matter for cabbageland?
Because cabbageland keeps preferring structured objects over vibes. RadMatch is a good reminder that the right metric is often the one that leaves behind something inspectable, not the one that wins one leaderboard column.

### 13. What ideas are steal-worthy?
Persist intermediate evaluation objects. Count actionable errors, not only generic quality scores. Separate raw agreement from operational usefulness once a capable judge saturates correlation.

### 14. Final decision
Keep as a preserved note. It is adjacent rather than central, but the metric-design lesson travels well.
