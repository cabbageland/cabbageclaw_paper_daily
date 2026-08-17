# Silent Updates: Measuring and Closing the Post-Deployment Disclosure Gap

## Basic info

* Title: Silent Updates: Measuring and Closing the Post-Deployment Disclosure Gap
* Authors: Sophia Abraham, Ben Bucknall
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.11803
* Date surfaced: 2026-08-17
* Why selected in one sentence: It turns post-deployment drift from a vague complaint into a concrete chain-of-custody audit with measurable disclosure failures.

## Quick verdict

* Highly relevant

I inspected the arXiv HTML full text. This is one of the better field-deployment papers in the current batch because it replaces hand-wavy "models change over time" talk with a public scorecard and a concrete binding problem.

## One-paragraph overview

Silent Updates studies whether public model documentation can actually be tied to the systems users interact with after deployment. The paper audits disclosure practices across **9** first-party API providers and **7** third-party inference hosts, using a scorecard plus a chain-of-custody protocol to test whether an external party can verify that the served artifact matches the artifact described in safety evaluations or system cards. The main result is ugly and useful: providers often publish substantial documentation, but none in the sample exposes a verifiable API-to-evaluation round trip, and the paper argues that current governance frameworks assume a binding primitive that does not exist in practice. It then proposes a three-part behavioral trigger system for when post-deployment changes should force disclosure or re-evaluation.

## Model definition

### Inputs
The study takes public provider documentation, model cards, changelogs, API interfaces, host metadata, and terms-of-service language for the sampled providers and hosts.

### Outputs
It outputs scorecard measurements, a chain-of-custody analysis, failure-mode taxonomy, and a proposed disclosure-trigger framework.

### Training objective (loss)
There is no trained model. This is an audit and governance-method paper.

### Architecture / parameterization
The paper's core machinery is a disclosure scorecard, a chain-of-custody verification protocol, a taxonomy of silent-update failure modes, and a proposed three-part trigger system based on capability, behavioral drift, and component changes.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the verification gap between published evaluations and the behavior of the systems actually being served after deployment updates.

### 2. What is the method?
The method is to operationalize post-deployment transparency as an auditable scorecard and chain-of-custody test, then analyze where existing provider practices fail.

### 3. What is the method motivation?
Current governance and safety reporting assume that an evaluated model can be externally linked to the deployed one. If that link is missing, a lot of safety documentation becomes much weaker evidence than it appears.

### 4. What data does it use?
It uses public documentation and interfaces from first-party API providers and third-party inference hosts, including system cards, changelogs, model identifiers, and terms of service.

### 5. How is it evaluated?
It evaluates providers against the scorecard criteria, analyzes chain-of-custody failure modes, and studies whether an external auditor can establish a verifiable round trip from served system to evaluation artifact.

### 6. What are the main results?
The paper finds that no provider in the sample exposes a verifiable API-to-evaluation round trip. It reports that no provider published enough information for an external party to verify that the served artifact is the same one documented in published safety materials. It also finds that **6 of 9** providers include terms that may discourage independent evaluation. On the scorecard's first-party sample, only **1 of 9** providers names a pinned evaluated snapshot, and several disclosure dimensions score **0 of 9**.

### 7. What is actually novel?
The novelty is not the observation that models drift. It is the decision to treat post-deployment disclosure as a measurable chain-of-custody problem with concrete provider-facing criteria.

### 8. What are the strengths?
The paper is concrete, auditable, and timely. It studies real provider practices, makes the failure modes legible, and offers a usable public instrument instead of a vibes-only governance complaint.

### 9. What are the weaknesses, limitations, or red flags?
The sample is limited, the scorecard necessarily embeds normative choices, and the analysis can only measure what is externally visible. A provider could have internal controls stronger than its public interface reveals.

### 10. What challenges or open problems remain?
The hard open problem is binding: how to expose verifiable links among evaluated artifacts, served deployments, and post-deployment updates without requiring providers to disclose every operational detail.

### 11. What future work naturally follows?
Future work should refine the scorecard, test it against more providers and open-weight hosts, design machine-checkable binding primitives, and build public-interest drift monitoring that survives provider policy changes.

### 12. Why does this matter for cabbageland?
Because cabbageland cares about field-deployment reality, not just benchmark theater. If a system card cannot be bound to the served artifact, then claims about reliability, safety, or capability need to be read with much more suspicion.

### 13. What ideas are steal-worthy?
Treat deployment transparency as a verifiable chain, not a PDF. Separate pinned identifiers from behavioral guarantees. Add explicit disclosure triggers for capability shifts, behavioral drift, and component substitutions. Check cross-surface divergence instead of assuming the API and chatbot surfaces are behaviorally identical.

### 14. Final decision
Keep as a preserved note. The binding problem is real, and this paper gives it a concrete operational shape.

## 6. Mandatory critical angles

The paper is strongest on auditability, governance clarity, and real-world relevance. It is weaker where all public-doc audits are weak: hidden internal controls remain invisible, and the scorecard cannot prove the absence of internal discipline.

## 7. Writing style

The right tone is crisp and approving with a little steel. The paper is valuable because it punctures false reassurance without collapsing into melodrama.

## 8. Repository output format

Saved as a preserved paper note because the chain-of-custody framing is likely to matter across future model-card, deployment, and evaluation work.
