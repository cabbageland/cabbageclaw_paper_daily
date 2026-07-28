# Beyond Aggregate Risk: Role-Stratified Conformal Risk Control for LLM Tool Calls

## Basic info

* Title: Beyond Aggregate Risk: Role-Stratified Conformal Risk Control for LLM Tool Calls
* Authors: Md Ashikur Rahman, Md Arifur Rahman, Niamul Hassan Samin, Khandaker Rifah Tasnia, Sifat Rahman Ahona, Juena Ahmed Noshin
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.24343
* Date surfaced: 2026-07-28
* Why selected in one sentence: It puts the calibration budget on the semantic field that can actually cause harm instead of averaging risk over a whole action.

## Quick verdict

**Useful**

This is a good paper because it chooses the right unit of certification. A tool call is not one homogeneous object: the body of an email and the recipient field do not carry the same failure cost, and aggregate control hides that. I inspected the arXiv HTML abstract, introduction, contribution summary, threat model and problem setup, and the argument showing the price of aggregate coarseness.

## One-paragraph overview

The paper studies prompt-injection and tool-call safety for LLM agents. Instead of calibrating risk over a whole action, it calibrates each semantic argument role separately, such as target, credential, command, or content. The core claim is that aggregate certification dilutes rare but high-risk roles: a system can look safe on average while repeatedly failing on the fields that matter most. The proposed role-stratified conformal risk control layer wraps any per-field detector, assigns role-specific budgets and thresholds, and uses pooled handling only when a role is too rare to certify directly.

## Model definition

### Inputs
The method takes structured tool calls, a semantic role label for each argument, per-field detector scores estimating influence from untrusted context, calibration data, and role-specific risk budgets.

### Outputs
It outputs allow or block decisions for fields or actions under thresholds chosen to satisfy role-specific conformal risk targets.

### Training objective (loss)
The contribution does not introduce a new base detector loss. It is a calibration wrapper around any per-field detector, with thresholds chosen by conformal risk control rather than by end-to-end training.

### Architecture / parameterization
The architecture is a per-field detector plus a role-stratified conformal calibration layer. Roles like target, credential, command, and content each get their own budget, threshold, and certification logic.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to prevent high-risk tool-call fields from being underprotected by action-level average-risk certification.

### 2. What is the method?
The method is role-stratified per-field conformal risk control: calibrate risk separately for semantic roles rather than over the whole action.

### 3. What is the method motivation?
Rare high-risk fields can be drowned out by many benign fields in an aggregate metric, which makes the certified object mismatch the harmful object.

### 4. What data does it use?
It evaluates on AgentDojo and InjecAgent across six language models, with transfer, unseen-suite, detector-noise, drift, and adaptive-attack conditions.

### 5. How is it evaluated?
It is evaluated through theoretical analysis of the coarseness penalty, finite-sample certification claims, and empirical compliance and utility comparisons under several shifted conditions.

### 6. What are the main results?
The method tracks the predicted price of coarseness, achieves much more consistent role-specific budget compliance than aggregate-style baselines, and stays comparatively robust under transfer and shift when recalibration assumptions are respected.

### 7. What is actually novel?
The novelty is not conformal prediction itself. It is applying calibration at the semantic argument-role level and explicitly quantifying why action-level aggregation is the wrong unit.

### 8. What are the strengths?
The paper chooses the right failure unit, is detector-agnostic, and combines a simple theoretical argument with practical prompt-injection benchmarks.

### 9. What are the weaknesses, limitations, or red flags?
The clean guarantees still depend on exchangeability or recalibration. Rare roles may need pooled treatment, and the whole method inherits the weaknesses of the underlying per-field detector.

### 10. What challenges or open problems remain?
Real systems still need stronger role labeling, better detectors, and more evidence on how the method behaves under heavy semantic drift and richer tool schemas.

### 11. What future work naturally follows?
Combine role-stratified calibration with provenance-tracking or noninterference-style defenses, and test it on real production tool traces instead of benchmark-only injections.

### 12. Why does this matter for cabbageland?
Cabbageland cares about structured tool use, prompt injection, and uncertainty control that cashes out at the place harm occurs. This paper is directly useful because it certifies the field that actually matters.

### 13. What ideas are steal-worthy?
Calibrate by semantic role, not by whole action. Give stricter budgets to target and credential fields. Treat aggregate risk as a potentially deceptive summary rather than a sufficient safety certificate.

### 14. Final decision
**Keep as a useful control-layer paper.** It is not the whole safety stack, but it improves the unit of certification in a way that is both principled and practical.
