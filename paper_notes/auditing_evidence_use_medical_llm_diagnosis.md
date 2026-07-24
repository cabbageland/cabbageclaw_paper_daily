# Auditing Evidence Use in Medical LLM Diagnosis

## Basic info

* Title: Auditing Evidence Use in Medical LLM Diagnosis
* Authors: Junchi Liao, Jiawen Deng, Fuji Ren
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.20848
* Date surfaced: 2026-07-24
* Why selected in one sentence: It replaces medical-LLM answer accuracy theater with a role-aware audit of how diagnostic margins change when evidence units are added, removed, or clinically neutralized.

## Quick verdict

**Useful**

This is a good diagnostic paper because it does not confuse large interactions with failures. It first mines evidence interactions, then forces clinical review and stability checks before making stronger claims. I inspected the arXiv PDF sections covering the abstract, introduction, audit method, experiments, clinical validation, targeted counterfactual validation, robustness checks, discussion, and limitations.

## One-paragraph overview

The paper asks whether medical LLMs use case evidence appropriately rather than merely whether they guess the right diagnosis. For each case, it decomposes the evidence into units, scores candidate diagnoses under controlled subsets of those units, and computes low-order interactions in diagnostic margins. Crucially, it treats evidence as diagnosis-relative: a finding can support the target, support a competitor, or act as an excluding or clinically local cue. That lets the audit separate plausible differential-diagnosis structure from suspicious evidence-use patterns. On three diagnostic datasets and five open-weight models, most high-strength interactions are legitimate support or conflict, but a smaller stable subset of invalid cases clusters around negated or absent findings and clinically local cues.

## Model definition

### Inputs
The audited system receives a clinical case decomposed into evidence units, a fixed candidate diagnosis list, and controlled subsets or neutralized versions of those units.

### Outputs
It outputs option-level diagnosis scores, audited diagnostic margins for target diagnoses, and interaction values over evidence subsets.

### Training objective (loss)
The paper introduces no new trainable model. It evaluates existing instruction-tuned medical or biomedical LLMs with prompt-conditioned scoring under controlled interventions.

### Architecture / parameterization
The contribution is an evidence-use audit protocol over multiple-choice diagnosis prompts. It combines diagnosis-relative evidence roles, low-order interaction mining, clinical adjudication, targeted counterfactual removal, and robustness filtering.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to determine whether a medical LLM's diagnostic preference is based on clinically coherent evidence use rather than on shortcut cues or misleading local interactions.

### 2. What is the method?
The method splits a case into evidence units, scores candidate diagnoses under controlled subsets, computes interaction effects in target-vs-competitor margins, and then clinically reviews only the suspicious stable patterns.

### 3. What is the method motivation?
Diagnostic accuracy is necessary but weak. A model can still be "right" while leaning on negated, absent, or clinically irrelevant evidence in a way that would be unsafe or misleading in real use.

### 4. What data does it use?
It uses `500` DDXPlus cases with structured fields, plus `200` CupCase and `200` MedCase narrative cases for broader external checks.

### 5. How is it evaluated?
It is evaluated with evidence-subset interventions, diagnosis-margin interactions, a `130`-item blinded enriched clinical review sample on DDXPlus, targeted counterfactual removals, and stability checks over prompt wording, option order, and deletion-versus-neutralization perturbations.

### 6. What are the main results?
OpenBioLLM has the best average full-evidence diagnostic accuracy at about `72.2%`, but accuracy ordering does not match evidence-use ordering. On DDXPlus, conflict or cancellation accounts for about `47.1%` of interaction strength and faithful target support for much of the rest. In the enriched DDXPlus clinical review, `111/130` interactions are valid, `8/130` questionable, and `11/130` invalid or shortcut-like, concentrated in negated or clinically local evidence. Stability filtering shrinks the candidate-failure queue from `300` to `120` while raising adjudicated precision from `0.55` to `0.80`.

### 7. What is actually novel?
The novelty is not the interaction score by itself. It is the diagnosis-relative interpretation layer plus the discipline of separating discovery from failure assignment.

### 8. What are the strengths?
It is much more honest than a raw "suspicious feature" detector. It treats many strong interactions as legitimate differential structure, uses clinical adjudication, and checks whether suspicious cases survive prompt and perturbation changes.

### 9. What are the weaknesses, limitations, or red flags?
The audit is still prompt-conditioned behavior, not a view into latent reasoning. Results depend on evidence-unit selection, candidate sets, and option scoring. The enriched review sample is descriptive rather than a prevalence estimate.

### 10. What challenges or open problems remain?
The next challenge is scaling the same audit to richer clinical tasks beyond multiple-choice diagnosis while keeping the evidence-role interpretation disciplined.

### 11. What future work naturally follows?
Use probability-sampled review sets, extend the audit to treatment and triage decisions, and combine role-aware evidence interventions with real clinical workflow constraints.

### 12. Why does this matter for cabbageland?
Cabbageland cares about evaluation that distinguishes true mechanism from respectable-looking output. This paper is a good template for auditing whether a system used the right evidence rather than merely landing on the right label.

### 13. What ideas are steal-worthy?
Use diagnosis-relative evidence roles instead of generic relevance. Mine low-order interactions in decision margins. Force clinical or domain review before calling a pattern a failure. Add stability filtering so the suspicious queue shrinks before humans spend attention on it.

### 14. Final decision
**Keep it as a diagnostic reference.** The method is more valuable than any single leaderboard number it reports.
