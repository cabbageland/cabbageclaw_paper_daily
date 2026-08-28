# Calibrated Enough to Know, Not Calibrated to Act: Fabricated Evidence Makes LLM Agents Commit to the Unknowable

## Basic info

* Title: Calibrated Enough to Know, Not Calibrated to Act: Fabricated Evidence Makes LLM Agents Commit to the Unknowable
* Authors: Pranav Aggarwal
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.27167
* Date surfaced: 2026-08-28
* Why selected in one sentence: It isolates a narrow but important failure where authoritative-looking evidence flips the act gate even when the model can recognize the question is unknowable.

## Quick verdict

* Keep

I inspected the full arXiv HTML text, especially the causal display-manipulation setup, the action-versus-belief analysis, and the synthetic fine-tuning intervention. This paper earns a preserved note because it localizes a failure mode that many deployment discussions blur together. The interesting object is not confidence in the abstract. It is whether the system knows when not to act.

## One-paragraph overview

The paper studies irreducibly unknowable forecasting questions and shows that LLM agents become far more willing to commit once those questions are wrapped in professional-looking evidence panels. The key experiment fabricates the evidence while preserving the presentation, which lets the paper separate information from authoritative packaging. Models still commit at nearly the same rate even when the whole panel is fake. Follow-up probes show that the model's belief estimates barely move and that the model can often classify the question as irreducibly unknowable when asked first. The failure is therefore localized to an act/don't-act gate rather than to pure incapacity or missing judgment.

## Model definition

### Inputs
Prompts containing unknowable forecasting questions with varying levels of supporting evidence, including fully fabricated display panels.

### Outputs
A commit-or-decline action, associated probability judgments, and in later experiments a fine-tuned model's abstention behavior.

### Training objective (loss)
The main paper is an audit/evaluation study. Its intervention stage uses supervised fine-tuning on synthetic unknowability cases to train a smaller model's action gate.

### Architecture / parameterization
The paper evaluates multiple frontier LLMs as frozen decision-makers, then fine-tunes a 3B model on synthetic cases to test whether the act gate can be altered directly.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to understand why LLM agents commit to decisions on questions that are in principle unknowable in advance.

### 2. What is the method?
The method constructs matched evidence conditions, including partially and fully fabricated evidence panels, then measures commitment, stated probabilities, and knowability judgments separately.

### 3. What is the method motivation?
If fabricated evidence changes action as much as genuine evidence, then the problem is not extra information. It is the authority implied by the display format.

### 4. What data does it use?
The main settings use short-horizon price-direction questions and transfer domains including crypto, sports, and weather, plus synthetic dice, coin, jar, and timer cases for the fine-tuning stage.

### 5. How is it evaluated?
It measures commitment rates under escalating evidence, compares real and fabricated panels, probes knowability judgments directly, and tests whether synthetic supervised fine-tuning transfers the desired abstention gate.

### 6. What are the main results?
Across 12 frontier models, commitment rises from 6.5% to 54.0% as evidence is escalated. A fully fabricated panel still yields 36.8% commitment, statistically indistinguishable from 37.6% with genuine market data. When asked to classify knowability first, models call the question irreducible 90% of the time and then commit on only 0.4% of those cases. Fine-tuning a 3B model on 540 synthetic cases drives commitment on the original benchmark to 0.0%, but that fix is fragile to output-format changes.

### 7. What is actually novel?
The novelty is causally isolating presentation as the trigger and locating the failure at an action gate rather than in generic calibration or reasoning ability.

### 8. What are the strengths?
The intervention is sharp, the negative diagnosis is more useful than a vague overconfidence complaint, and the paper bothers to test whether the gate is trainable rather than stopping at criticism.

### 9. What are the weaknesses, limitations, or red flags?
Some transfer domains are weaker than the core finance setup, especially weather. The fine-tuned fix is also prompt- and format-fragile, which limits how far the result can be generalized.

### 10. What challenges or open problems remain?
A real deployment needs an action gate that survives prompt variation, different tool wrappers, and heterogeneous evidence formats. That is not solved here.

### 11. What future work naturally follows?
Action-gate training tied to richer abstention policies, explicit uncertainty interfaces, and runtime checks that preserve reasoning room under structured outputs would all follow naturally.

### 12. Why does this matter for cabbageland?
Because many agent failures are not "the model cannot tell." They are "the model can tell, but the system still routes to action." This paper makes that distinction unusually concrete.

### 13. What ideas are steal-worthy?
Separate knowability judgment from action commitment. Use fabricated but plausible evidence to test whether presentation rather than information is driving the decision. Treat abstention as a gate that can be trained and audited in its own right.

### 14. Final decision
Keep as a preserved note. This is a useful failure-analysis paper because it identifies a narrow, operationally relevant gate instead of waving at overconfidence in general.

## 6. Mandatory critical angles

The paper is strongest as diagnosis, not as a turnkey fix. The good news is that the failure is localizable. The bad news is that the learned fix is brittle. Both halves matter.

## 7. Writing style

The tone should be sharp and appreciative. The paper deserves credit for isolating the failure, but the note should keep stressing that the robust deployment solution is still open.

## 8. Repository output format

Saved as a preserved paper note because the act-gate framing is reusable across agent safety, calibration, and decision-support work.
