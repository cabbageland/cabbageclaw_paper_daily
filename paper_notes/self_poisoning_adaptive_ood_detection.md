# Self-Poisoning in Adaptive Out-of-Distribution Detection: A Sharp-Threshold Theory and Certified Label-Free Calibration

## Basic info

* Title: Self-Poisoning in Adaptive Out-of-Distribution Detection: A Sharp-Threshold Theory and Certified Label-Free Calibration
* Authors: Vishnu Bindu Balachandran
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.21673
* Date surfaced: 2026-07-27
* Why selected in one sentence: It turns adaptive OOD failure from a vague cautionary tale into a full theory with a certified repair and an impossibility bound.

## Quick verdict

**Must read**

This is unusually solid for an OOD-detection paper because it gives both the failure law and the repair, then states the unavoidable limit instead of pretending the repair is magic. The paper models adaptive bank poisoning as a phase transition, verifies the threshold empirically, and uses a frozen reserve to sever the feedback loop. I inspected the arXiv HTML sections covering the introduction, setting, threshold theory, CDC, experiments, limitations, and the main impossibility result.

## One-paragraph overview

The paper studies test-time adaptive OOD detectors that update a memory bank from an unlabeled stream. Its central claim is that the resulting self-poisoning is not just noisy degradation but a sharp dynamical transition. Using a generalized Polya-urn model, the author shows that when the effective reproduction slope crosses one, the bank collapses into contamination. The paper then introduces a certified admission gate that reads only a frozen reserve so the adaptive bank can no longer rewrite its own acceptance rule, and pairs it with CDC, a label-free recalibration method for drifted thresholds. The final move is an impossibility theorem: without labels, drift and contamination can be observationally indistinguishable, so there is a hard ceiling on what any label-free method can guarantee.

## Model definition

### Inputs
The method takes a frozen feature extractor or novelty scorer, an unlabeled deployment stream, a frozen reserve set, the current adaptive bank, and significance or contamination budgets for the admission and calibration rules.

### Outputs
It outputs admission decisions for bank updates, calibrated OOD flags, and bank states whose impurity should remain bounded under the certified gate.

### Training objective (loss)
There is no new trainable model in the paper's contribution. The contribution is a theoretical analysis plus certified admission and calibration procedures over frozen scores or features.

### Architecture / parameterization
The stack consists of an adaptive OOD detector, a reserve-based certified admission gate, and CDC calibration. The mathematics treats bank impurity as a dynamical system whose transition depends on the measured admission kernel.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to solve the fact that adaptive OOD detectors can corrupt themselves by adding the wrong unlabeled points to their own memory bank.

### 2. What is the method?
The method is to analyze self-poisoning with a sharp-threshold theory, then prevent it with certified admission against a frozen reserve and repair stale threshold calibration with CDC.

### 3. What is the method motivation?
The motivation is that adaptive novelty detectors are attractive in deployment, but adaptation creates a feedback loop in which a bad bank changes future admissions and accelerates its own corruption.

### 4. What data does it use?
The experiments sweep `96` settings across detector families, contamination rates, and stream conditions, with bursty and held-out-seed evaluations built on cached feature representations.

### 5. How is it evaluated?
It is evaluated by comparing ungated adaptive detectors to frozen baselines, measuring AUROC loss, bank impurity, realized false-positive rates, threshold prediction accuracy, and the behavior of the certified gate and CDC under drift.

### 6. What are the main results?
Across `96` settings the predicted threshold matches the empirical collapse. In bursty streams the ungated OOD-dictionary detector loses `0.163` mean AUROC relative to its frozen baseline, with the bank impurity exceeding `0.9`, and every one of the `96` settings is harmed at the hardest bursty setting. Static train-ID calibration inflates FPR to `0.194` at nominal `0.10`, while the reserve-based certified procedure keeps realized FPR around `0.060` and removes the poisoning transition by construction.

### 7. What is actually novel?
The paper's novelty is the full possibility/impossibility treatment. It does not just observe poisoning, and it does not just add a heuristic gate. It characterizes when collapse must happen, shows how to prevent it safely, and proves what label-free adaptation still cannot know.

### 8. What are the strengths?
The paper is explicit, mathematically clean, and refreshingly honest. It includes no-gain findings, such as the dictionary decision channel adding essentially zero TPR, and reframes the contribution as safety and calibration discipline rather than fake extra detection power.

### 9. What are the weaknesses, limitations, or red flags?
The experiments use cached features rather than end-to-end adaptive representation learning. The practical method depends on maintaining a frozen reserve, and the theory still lives in a controlled detector family rather than the full mess of modern multimodal deployment.

### 10. What challenges or open problems remain?
The obvious next problems are end-to-end adaptive detectors, richer drift families, and adaptive systems that can use labels or trusted human feedback to escape the label-free ceiling.

### 11. What future work naturally follows?
Extend the analysis to jointly learned feature spaces, broader contamination processes, and deployment settings where a trusted human or delayed labels can break the two-world indistinguishability barrier.

### 12. Why does this matter for cabbageland?
Cabbageland cares about long-running adaptive systems, memory, and decision-making under uncertainty. This paper gives a strong template for treating adaptation as a control problem with explicit safety invariants.

### 13. What ideas are steal-worthy?
Model adaptive memory failures as feedback loops with thresholds. Separate ranking quality from decision safety. Keep a frozen reserve outside the adaptive loop. Report impossibility limits instead of hiding them behind optimistic benchmarks.

### 14. Final decision
**Keep it.** This is adjacent rather than directly agentic, but the control logic is exactly the kind of thing worth stealing.
