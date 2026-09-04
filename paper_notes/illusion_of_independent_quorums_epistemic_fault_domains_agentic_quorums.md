# The Illusion of Independent Quorums: Epistemic Fault Domains and Correlated Cognitive Failures in Agentic Quorums

## Basic info

* Title: The Illusion of Independent Quorums: Epistemic Fault Domains and Correlated Cognitive Failures in Agentic Quorums
* Authors: Jun He, Deying Yu
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2609.02925
* Date surfaced: 2026-09-04
* Why selected in one sentence: It formalizes shared-evidence failure in multi-agent authorization and replaces reviewer count with a structural epistemic cut.

## Quick verdict

* Must read

I inspected the full arXiv HTML text, especially the system model, the structural-cut theorems, the DAQC controller section, and the Monte Carlo validation material. This note is worth preserving because the paper does not merely complain that agents may share evidence paths; it turns that complaint into an explicit object with operational consequences. The result is a much cleaner way to talk about multi-agent authorization safety than the usual reviewer-count theater.

## One-paragraph overview

The paper studies high-stakes mutations authorized by multiple agents, such as rollbacks, privilege grants, or deprovisioning actions. Its core claim is that nominally distinct reviewers often inherit the same upstream telemetry, document, retrieval path, or tool backend, so multiple votes may reflect one corrupted cause rather than independent evidence. To make that precise, the paper introduces **Epistemic Fault Domains** and the structural epistemic cut **kappa_E**, the minimum number of modeled root faults whose exposure covers an authorizing coalition. Under explicit assumptions, kappa_E lower-bounds the number of root faults needed for actual semantic compromise. The paper then proposes **Dependency-Aware Quorum Admission (DAQC)**, which separates prospective quorum selection from commit-time admission and requires provenance-aware cut checks before a mutation is allowed to commit.

## Model definition

### Inputs
The framework takes a participant set, quorum rule, explicit fault basis, planned and realized provenance graphs, and the modeled exposure relations from root faults to reviewers and evidence paths.

### Outputs
It outputs structural cut values, admission or denial decisions for candidate quorums, and reconfiguration requirements when the realized provenance does not satisfy the minimum cut.

### Training objective (loss)
There is no trainable model here. The contribution is a structural theory plus a runtime controller for provenance-aware quorum selection and admission.

### Architecture / parameterization
The paper uses graph- and hypergraph-style structural objects to represent evidence ancestry and a runtime controller, DAQC, that checks prospective and realized provenance against a cut threshold before admitting a commit.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
How do you tell whether a multi-agent authorization quorum actually has independent epistemic support rather than several agents echoing one shared upstream fault?

### 2. What is the method?
Define common-cause evidence ancestry as Epistemic Fault Domains, measure quorum resilience with the structural cut kappa_E, and enforce a minimum acceptable cut at runtime with DAQC.

### 3. What is the method motivation?
Counting reviewers or even model families does not tell you how many distinct root causes would have to fail to corrupt the authorizing coalition. Shared telemetry, documents, or tools can collapse many votes onto one evidence path.

### 4. What data does it use?
The paper uses analytical constructions, seeded Monte Carlo mechanism checks across controlled topologies, and a frozen 120-task benchmark suite with an endpoint execution protocol for external evaluation.

### 5. How is it evaluated?
It evaluates the theory by proving structural properties of kappa_E, validating fault-propagation behavior via closed-form baselines and Monte Carlo simulation, and packaging the operational setting into a benchmark suite for external endpoint testing.

### 6. What are the main results?
The central theorem-level result is that arbitrarily large quorums can still have kappa_E = 1 if one root fault reaches a decisive coalition, so nominal size alone is not resilience. The paper also proves that discovering shared ancestry can never increase credited resilience, and that adding voters at a fixed threshold cannot increase the structural cut under compatible exposure extensions. On the mechanism side, the Monte Carlo simulations match analytical expectations within roughly 1.1 percentage points across the reported conditions. The paper then freezes a 120-task benchmark so the controller logic can be exercised against concrete mutation scenarios rather than only toy theorems.

### 7. What is actually novel?
The main novelty is not just "correlated failures matter." It is the explicit structural object kappa_E, the lower-bound relation to semantic compromise, and the selection-versus-admission split in DAQC.

### 8. What are the strengths?
It gives a concrete language for shared evidence ancestry, proves uncomfortable but useful monotonicity facts, and turns the theory into a runtime admission policy instead of leaving it as a static analysis story.

### 9. What are the weaknesses, limitations, or red flags?
The guarantee depends on the explicit fault basis and conservative provenance reconstruction. If important shared causes are missing from the modeled basis, the computed cut can still flatter the system. The paper is also much stronger as a structural framework than as a broad empirical study of frontier agent deployments.

### 10. What challenges or open problems remain?
Open problems include richer provenance capture in messy real systems, combining human and machine reviewers in one fault basis, and deciding how conservative the exposure model must be without making the controller unusably pessimistic.

### 11. What future work naturally follows?
Live deployment studies, tighter provenance instrumentation, integration with approval workflows in coding and operations agents, and adaptive quorum construction under cost or latency constraints.

### 12. Why does this matter for cabbageland?
Because cabbageland keeps bumping into ensemble and multi-agent safety questions where "just add another reviewer" is not a serious answer. This paper gives a better object to optimize.

### 13. What ideas are steal-worthy?
Count fault-separated evidence paths, not reviewer instances. Separate plan-time quorum selection from commit-time admission. Fail closed and reconfigure instead of pretending more votes repair a structurally weak quorum.

### 14. Final decision
Keep as a preserved note. This is a strong structural paper because it takes a hand-waved safety intuition, makes it explicit, and then proves where the popular proxy fails.
