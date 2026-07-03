# Hidden Forgetting in Continual Multimodal Learning: When Accuracy Survives but Grounding Fails

## Basic info

* Title: Hidden Forgetting in Continual Multimodal Learning: When Accuracy Survives but Grounding Fails
* Authors: Qianyu Chen, Canran Xiao, and Runxuan Tang
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.02020
* Date surfaced: 2026-07-03
* Why selected in one sentence: It shows that continual multimodal learning can preserve answer accuracy while silently losing the evidence channel that made the answer grounded.

## Quick verdict

**Highly relevant**

This is a strong evaluation-and-method paper. I inspected the full arXiv HTML / PDF, especially the hidden-forgetting definition, reliance profiling through counterfactual channel interventions, RCL losses, stream construction, baselines, results, and limitations. The caveat is that channel-reliance profiles are proxies; they are more causal than accuracy, but still not a complete account of internal reasoning.

## One-paragraph overview

The paper identifies hidden evidence-use forgetting in continual multimodal learning. After adapting to new tasks or domains, an MLLM may still answer old questions correctly, but the evidence channel behind those answers can drift from visual evidence to text priors, from chart structure to language patterns, or from document/OCR cues to shortcuts. RCL addresses this without replay by freezing the previous checkpoint as a behavioral reference, estimating teacher and student evidence-reliance profiles through counterfactual channel interventions, and training with task learning, prediction preservation, and reliance preservation losses.

## Model definition

### Inputs

Inputs are continual multimodal task streams with image, text, OCR, chart, and document evidence channels. The method also uses a previous model checkpoint as a reference.

### Outputs

The model outputs answers to multimodal tasks. The evaluation additionally outputs evidence-reliance profiles, drift measures, dominant-evidence flips, and hidden forgetting rates.

### Training objective (loss)

RCL combines the new-task learning loss with prediction-preservation and reliance-preservation losses. The reliance term encourages the adapted student to maintain the previous checkpoint's evidence-use profile when preserving old behavior.

### Architecture / parameterization

RCL is a replay-free continual-learning framework for MLLMs rather than a new multimodal backbone. It uses counterfactual channel interventions to estimate reliance profiles for teacher and student models.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Standard continual-learning metrics ask whether old answers remain correct. In multimodal settings, this misses a crucial failure: the model may keep producing the right answer while changing which evidence channel it relies on. That matters because the answer becomes less grounded, less robust, and harder to trust under distribution shift.

### 2. What is the method?

The method defines hidden evidence-use forgetting and measures it with reliance profiles estimated by counterfactual channel interventions. RCL freezes the prior checkpoint as a teacher, compares teacher and student reliance profiles, and trains the student to preserve both predictions and evidence reliance while learning new tasks.

### 3. What is the method motivation?

Correct answers are not enough in multimodal systems. A radiology model, chart model, or document VQA model can be accurate for the wrong reason. Continual adaptation can worsen that by pushing the model toward shortcuts that keep benchmark accuracy alive while making grounding brittle.

### 4. What data does it use?

The evaluation uses continual multimodal streams built from CoIN, COAST, MCITlib, and an evidence-sensitive multimodal stream. The streams cover visual, textual, OCR, chart, and document evidence.

### 5. How is it evaluated?

The paper evaluates standard final performance and forgetting, plus reliance-specific metrics such as modality reliance drift, dominant evidence flips, and hidden forgetting rates. It compares RCL with replay-free, PEFT, routing, and memory-assisted baselines.

### 6. What are the main results?

RCL improves final performance and reduces standard forgetting while also substantially lowering reliance drift, dominant evidence flips, and hidden forgetting rates across the evaluated streams. The important empirical point is that some baselines maintain accuracy while showing much worse evidence-use stability.

### 7. What is actually novel?

The novel contribution is making evidence-use stability a continual-learning object. The paper does not merely add another forgetting score; it defines a failure mode where answer retention and grounding retention diverge, then trains against that divergence.

### 8. What are the strengths?

The paper is pointed at a real deployment failure. Its counterfactual channel interventions are a much better diagnostic than aggregate accuracy. The replay-free design is also practical for settings where old data cannot be stored.

### 9. What are the weaknesses, limitations, or red flags?

Reliance profiles are coarse. A channel intervention can reveal dependency on a modality, but it does not prove the model used the clinically or semantically correct region, token, or chart component. The method also depends on the previous checkpoint as a useful teacher; if the teacher was already shortcut-heavy, preserving its reliance can preserve bad behavior.

### 10. What challenges or open problems remain?

The next challenge is finer-grained evidence preservation: not just image versus text, but region, phrase, table cell, or citation-level reliance. Another open problem is distinguishing beneficial reliance shifts from harmful ones when new tasks genuinely require different evidence channels.

### 11. What future work naturally follows?

Combine reliance preservation with region-level or citation-level grounding metrics. Extend the method to medical imaging, chart QA, browser agents, and document agents where evidence channels are explicit and auditable.

### 12. Why does this matter for cabbageland?

Cabbageland agents should not be judged only by whether they still get the answer right after adaptation. They should preserve the evidence path that made the answer defensible. Hidden Forgetting is a useful warning label for any evolving agent memory or multimodal model.

### 13. What ideas are steal-worthy?

* Track evidence-use drift separately from answer accuracy.
* Use counterfactual evidence-channel interventions during evaluation.
* Preserve reliance profiles when doing replay-free continual learning.
* Report hidden forgetting rates, not just final accuracy.
* Treat a correct answer from the wrong evidence channel as a real failure.

### 14. Final decision

**Keep it.** This paper cleanly extends continual-learning evaluation from output preservation to grounding preservation. That distinction matters for any agent expected to adapt without losing its reasons.
