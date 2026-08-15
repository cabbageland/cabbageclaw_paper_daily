# Agent Behavioral Contracts II: Certifying Compositional Reliability Without Assuming Independence

## Basic info

* Title: Agent Behavioral Contracts II: Certifying Compositional Reliability Without Assuming Independence
* Authors: Varun Pratap Bhardwaj, Garima Singh, Arun Pratap Bhardwaj
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.12895
* Date surfaced: 2026-08-15
* Why selected in one sentence: It tests the independence assumption behind multi-agent reliability multiplication and replaces it with a dependence-aware finite-sample certificate.

## Quick verdict

* Highly relevant

I inspected the arXiv HTML full text. This paper is worth keeping because it attacks a sloppy systems assumption with preregistered evidence and then supplies a concrete replacement instead of stopping at critique.

## One-paragraph overview

The paper studies compositional reliability for multi-agent pipelines and asks whether multiplying component reliabilities makes sense when the components share a model. In a preregistered confirmatory evaluation of **18,000** two-agent handoff missions, same-model agents co-fail on **90.0%** of the missions on which either fails, with log OR **6.66** and phi **0.916**. Different-model substitution reduces that dependence, while different-vendor substitution does not once the model already differs. The authors then build a dependence-free finite-sample certificate: a linear program over the joint failure law constrained by measured co-execution moments inside a Bonferroni-Clopper-Pearson box. On four-stage data, enriching the moment family from **10** to **14** functionals narrows the identified interval by **85.7%** and lifts the certified reliability floor from **0.2455** to **0.4116**.

## Model definition

### Inputs
The analysis takes mission-level contract outcomes, co-execution moments, agent-topology structure, and measured component reliabilities from multi-agent pipelines.

### Outputs
It outputs dependence statistics, certified lower bounds on graph reliability, and an anytime-valid sequential certificate under optional stopping.

### Training objective (loss)
There is no learned model. The core method is a finite-sample linear program over admissible joint distributions together with a sequential e-process certificate.

### Architecture / parameterization
The framework is a contract-based multi-agent reliability analysis: deterministic scoring code, preregistered mission campaign, moment-constrained LP certification, and an optional-stopping-valid sequential test.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the mismatch between real correlated failures in multi-agent systems and the common practice of multiplying component reliabilities as if the components failed independently.

### 2. What is the method?
First it measures dependence directly in a preregistered same-model versus different-model substitution study. Then it certifies graph reliability without assuming dependence structure by optimizing over all joint laws consistent with measured co-execution moments.

### 3. What is the method motivation?
Shared-model agents are likely to share blind spots, so a compositional bound that multiplies reliabilities can look reassuring while being wrong in exactly the direction that matters operationally.

### 4. What data does it use?
It uses a **30,820**-mission campaign, with **18,000** missions in the confirmatory two-agent handoff evaluation, across retail and financial workflow generators scored by deterministic gold code.

### 5. How is it evaluated?
It is evaluated with preregistered contrasts over model sharing, multiple dependence statistics, LP-certified reliability floors under different moment families, and an anytime-valid sequential test with empirical type-I control.

### 6. What are the main results?
Same-model agents co-fail on **90.0%** of missions where either fails, with log OR **6.66**. Switching to a different model reduces association across all confirmatory and secondary contrasts. The dependence-free certificate materially tightens when moment information increases, lifting the floor from **0.2455** to **0.4116** from **10** to **14** moments.

### 7. What is actually novel?
The novelty is not merely pointing out correlated failure. The paper both measures the signed operational cost of the independence assumption and offers a finite-sample replacement that does not require fitting a fragile dependence model.

### 8. What are the strengths?
The confirmatory design is serious, the scoring is deterministic, the paper reports a failed vendor-level hypothesis instead of massaging it away, and the replacement certificate is operationally concrete.

### 9. What are the weaknesses, limitations, or red flags?
The LP scales exponentially with the number of pipeline stages, the experiments cover only small motifs and two task domains, and model identity is still confounded with model capability in the substitution design.

### 10. What challenges or open problems remain?
The main open problems are scaling certification to larger compositions, handling LLM-based aggregator nodes, and understanding certificate decay as models or task distributions drift.

### 11. What future work naturally follows?
Future work should match substituted models on marginal failure rate, develop scalable certification for larger graphs, and study continuous recertification under deployment drift.

### 12. Why does this matter for cabbageland?
Because cabbageland routinely reasons about composed agents, critics, verifiers, and redundant reviews. This paper says clearly that same-model redundancy can be fake safety unless dependence is measured.

### 13. What ideas are steal-worthy?
Never report a multi-agent reliability product without checking dependence. Treat model identity as a systems variable, not just a procurement variable. Use moment-constrained bounds when the dependence structure is unknown rather than pretending a fitted copula solved the problem.

### 14. Final decision
Keep as a preserved note. Even where the exact certificate does not transfer, the measurement lesson about same-model redundancy is too useful to lose.

## 6. Mandatory critical angles

The paper is strongest on evaluation fairness, explicit failure modeling, and operational honesty. Its key contribution is not philosophical uncertainty about dependence but a measurable anti-conservative error in real composed systems.

## 7. Writing style

The right tone is respectful but unsentimental. The paper earns attention by testing a bad assumption directly and by reporting the null when the cleaner vendor story fails.

## 8. Repository output format

Saved as a preserved paper note because the dependence lesson and the certification construction both feel reusable for future agent-systems work.
