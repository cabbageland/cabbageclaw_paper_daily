# What Do Compliance Detectors Read? An Audit of Activation Probes and Guard Models

## Basic info

* Title: What Do Compliance Detectors Read? An Audit of Activation Probes and Guard Models
* Authors: Saisab Sadhu, Aadit Sengupta, Vinay Kumar Sankarapu, Pratinav Seth
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.16852
* Date surfaced: 2026-08-18
* Why selected in one sentence: It asks whether compliance detectors actually read the governing rule or merely recognize violation-flavored scenarios.

## Quick verdict

* Must read

I inspected the arXiv HTML full text. This is one of the sharpest papers in the batch because it refuses to stop at detector accuracy and instead audits construct validity, benchmark quality, and adversarial scope. The most useful result is not that ICS works cheaply. It is that the whole detector setup is more rule-blind than the field likes to admit.

## One-paragraph overview

The paper introduces the Internal Compliance Score (ICS), a training-free activation readout built from the monitored model's own residual activations, then uses it as an audit instrument rather than merely a new leaderboard entry. ICS is calibrated from ten labeled adherent/violating pairs, scored with one dot product, and compared against deployed guard models, an MLP probe, a zero-shot judge, and lexical floors across regulatory and safety settings. The central result is uncomfortable: efficient detectors mostly capture whether a scenario sounds broadly violative, not whether the supplied rule makes it a violation. The authors call this rule blindness. They also show that several public compliance benchmarks are too lexically degenerate to measure rule-conditioned reasoning at all. ICS still has practical value as a cheap reranking signal, but the paper is strongest where it limits its own claims.

## Model definition

### Inputs
ICS takes a text case passed through a monitored decoder transformer, typically a rule plus scenario pair or a generated response to be ranked for compliance, and reads the residual-stream activation at a selected layer.

### Outputs
It outputs a scalar compliance score that can be thresholded as a detector or used to rank candidate responses.

### Training objective (loss)
There is no gradient-based training objective. The readout direction is the normalized difference of class means from ten labeled adherent/violating pairs, with layer and threshold chosen on held-out calibration slices.

### Architecture / parameterization
The method is a nearest-centroid / Fisher-LDA-style activation probe over a decoder model's residual activations. It uses zero trained parameters beyond the chosen direction, layer, and threshold.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve two linked problems: cheap compliance detection without retraining a separate guard, and honest measurement of whether such detectors actually compose the governing rule with the scenario.

### 2. What is the method?
The method builds a training-free activation score, ICS, from ten labeled pairs, compares it against deployed guards and other probes, and then stress-tests every detector with rule ablations, counterfactual rule-scenario crossings, lexical floors, budget-matched nulls, and adversarial attacks.

### 3. What is the method motivation?
Guard models are expensive, frozen, and often evaluated on benchmarks that may reward scenario recognition rather than true rule-conditioned reasoning. If the task is "does this case violate this rule," then the rule has to matter.

### 4. What data does it use?
It uses 20 regulatory domains, 13 external benchmarks, 7 public compliance benchmarks, a crossed benchmark over 8 regulatory domains, fixed-scenario counterfactual pairs, safety benchmarks, and an IFEval-based response-selection study.

### 5. How is it evaluated?
It is evaluated with AUROC, F1, threshold metrics, lexical floors, budget-matched random-direction nulls, rule-ablation tests, crossed rule-scenario counterfactuals, leave-one-distribution-out comparisons, and content-selection experiments on generated responses.

### 6. What are the main results?
ICS reaches AUROC **0.952** on OmniCompliance in-domain and still compares well against deployed guards on matched-budget metrics. But the deeper result is that deleting, permuting, or swapping the governing rule causes **0/20** significant drops across their robustness checks, showing rule blindness. The paper also finds that **4 of 7** public compliance benchmarks are lexically degenerate. As a practical selector, ICS improves mechanically verified IFEval pass rate by **5.2** percentage points, but a white-box attack drives ICS-guided verified pass from **0.70** to **0.00**.

### 7. What is actually novel?
The real novelty is the audit frame. ICS itself is a useful low-cost probe, but the bigger contribution is showing how to test what a detector is reading, how to correct for selection-induced probe floors, and how to separate deployable utility from fake claims of rule understanding.

### 8. What are the strengths?
The paper is unusually honest about baselines and failure modes. It uses matched nulls instead of chance theater, audits the benchmarks themselves, includes positive controls that show the tests have power, and still extracts a practical reranking use case from a negative construct-validity finding.

### 9. What are the weaknesses, limitations, or red flags?
ICS itself remains rule-blind, so the paper diagnoses a problem more than it solves it. Several of its strongest regulatory-generation results still rely on LLM-judge scoring rather than a mechanical verifier. The method is also brittle to serialization choices and collapses under an adaptive white-box attack, so it is not a standalone enforcement mechanism.

### 10. What challenges or open problems remain?
The open problem is building detectors that genuinely bind rule text to scenario details instead of riding a broad harmfulness or violation prior. The field also needs cleaner rule-conditioned benchmarks that are not shortcut-solvable from surface text alone.

### 11. What future work naturally follows?
Future work should combine explicit rule execution or structured policy representations with learned detectors, create harder crossed rule-scenario datasets, and treat low-cost internal scores as one signal inside a broader audited control loop rather than a complete solution.

### 12. Why does this matter for cabbageland?
Because this is exactly the kind of evaluation mistake cabbageland tries to avoid. A monitor that looks sharp on a benchmark but ignores the governing object is not control. It is cosmetically aligned correlation.

### 13. What ideas are steal-worthy?
Use budget-matched nulls instead of pretending chance is the right baseline for selected probes. Build fixed-scenario counterfactual tests where only the rule flips the label. Keep cheap internal scores for candidate reranking, but never let them masquerade as proof of grounded policy reasoning.

### 14. Final decision
Keep as a preserved note. The paper is valuable both as a detector audit and as a general lesson in how not to fool yourself with high scores on the wrong construct.

## 6. Mandatory critical angles

This paper is strongest on motivation, evaluation fairness, and novelty-versus-packaging. It explicitly tests whether the claimed rule conditioning is real, shows where lexical shortcuts and layer-selection artifacts inflate confidence, and refuses to hide the fact that its own method is bounded. The main limitation is that the positive practical story, cheap selection, is much narrower than the field's larger hope for rule-aware compliance monitoring.

## 7. Writing style

The right tone is severe and exact. The paper earns praise for honesty and for stabbing directly at detector theater.

## 8. Repository output format

Saved as a preserved paper note because the rule-blindness diagnosis, the benchmark audit discipline, and the selection-null methodology all look reusable beyond compliance.
