# From Weights to Features: SAE-Guided Activation Regularization for LLM Continual Learning

## Basic info

* Title: From Weights to Features: SAE-Guided Activation Regularization for LLM Continual Learning
* Authors: Evan Ning, Wei Xue, Dong Lou, Yike Guo
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.26629
* Date surfaced: 2026-06-27
* Why selected in one sentence: It gives continual learning a more selective coordinate system by regularizing drift in SAE feature space instead of parameter space.

## Quick verdict

* Highly relevant

This is a strong bridge between mechanistic interpretability and continual learning. I inspected the full arXiv PDF, including the constrained objective, SAE mask construction, TRACE/MedCL results, separability analysis, cost analysis, and limitations. I did not reproduce the Gemma experiments, so exact margins remain paper claims.

## One-paragraph overview

The paper argues that weight-space continual-learning regularizers fail on LLMs partly because weights are polysemantic: one weight can participate in many unrelated concepts, so "important weight" is too coarse a protection unit. The proposed method freezes pretrained Sparse Autoencoders over Gemma activations, builds a task-specific feature relevance mask from current-task data, and regularizes feature drift rather than parameter drift. Low-mask features get a stability/protect constraint; high-mask features get a plasticity/guide constraint. After mask construction, the method stores only compact feature masks, not previous-task examples.

## Model definition

### Inputs

The method takes a sequence of supervised continual-learning tasks, current-task examples, a frozen base LLM, LoRA adapters being trained, and frozen pretrained SAE dictionaries over selected residual-stream layers. In the reported experiments, the base model is Gemma-2 9B-it with LoRA applied to linear projections, and the SAE dictionaries are Gemma Scope 16k-width SAEs at layers 9, 20, and 31.

### Outputs

The method outputs an updated LoRA-adapted LLM after each task. It also produces per-task continuous SAE feature masks that identify adaptive and protected regions of feature space. Evaluation outputs overall performance, backward transfer, average retained accuracy, and plasticity.

### Training objective (loss)

The training loss is cross-entropy plus two squared-hinge regularizers. `Lprotect` penalizes drift on low-mask SAE features when protected-feature drift exceeds a stability budget. `Lguide` penalizes insufficient movement on high-mask task-relevant features when feature movement is below a plasticity threshold. The frozen SAE is used only as a coordinate system for measuring activation-feature drift.

### Architecture / parameterization

The model family is an instruction-tuned LLM with LoRA adapters. The regularizer uses frozen sparse autoencoders as feature dictionaries. The task mask is built by mean absolute SAE activation on current-task content tokens, then expanded through k-nearest-neighbor propagation over SAE decoder-vector cosine similarity.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Sequential LLM fine-tuning forgets prior tasks. Weight-space methods like EWC try to protect important parameters, but in large models parameters and neurons are entangled across many concepts. Protecting a parameter to preserve one concept can block adaptation for another. The paper tries to make continual-learning protection happen at a more concept-aligned level.

### 2. What is the method?

For each task, the frozen base model and frozen SAE encode current-task activations. The method computes a feature relevance profile, propagates it over nearby SAE decoder directions, and stores the resulting continuous mask. During training, both the current LoRA model and frozen base are encoded into SAE space, and per-feature drift is split by the mask: protected features should not move too far, and task-relevant features should be allowed or encouraged to move enough.

### 3. What is the method motivation?

The motivation is the superposition hypothesis. If concepts are distributed through overlapping directions, parameter importance is not concept importance. SAE features are intended to be more monosemantic than neurons or weights, so they can act as a better bookkeeping system for which task-relevant representations should remain stable and which should adapt.

### 4. What data does it use?

The paper evaluates on TRACE-5000, an eight-task cross-domain continual-learning benchmark spanning stance detection, financial sentiment, meeting summarization, code completion, science QA, arithmetic, and German simplification. It also evaluates on MedCL, a 10-task biomedical continual-learning sequence with QA, relation extraction, topic classification, and rating tasks.

### 5. How is it evaluated?

Baselines include unprotected fine-tuning, EWC, SI, MAS, ELLA, O-LoRA, and replay buffers. Metrics include overall performance, backward transfer, average retained accuracy, and plasticity. The paper also runs analyses of task-feature separability, collateral constraint under weight vs feature protection, hyperparameter sensitivity, mask-importance variants, and computational/storage cost.

### 6. What are the main results?

On TRACE, SAE-guided regularization reaches OP 0.545, outperforming tested non-architectural methods such as SI at 0.513, ELLA at 0.475, EWC at 0.447, MAS at 0.419, and replay baselines up to 10 percent. O-LoRA remains higher at 0.630. On MedCL, SAE reaches OP 0.510, leading methods that store no previous-task examples, but replay with 5 percent and 10 percent buffers is higher. EWC has very high retention on TRACE but weak plasticity, supporting the paper's claim that it reduces forgetting partly by suppressing learning.

### 7. What is actually novel?

The novelty is not simply "use SAEs for interpretability." The paper uses frozen SAE features as the coordinate system for a training-time continual-learning regularizer. The objective is also more principled than a plain anti-drift penalty: it has separate stability and plasticity constraints, relaxed into protect and guide losses.

### 8. What are the strengths?

The central argument is strong: weight-space protection is too coarse under superposition. The paper supports this with mechanistic analyses, not just benchmark numbers. Task-relevant units are linearly separable in SAE feature space with AUC around 0.866 to 0.882, but near chance in MLP neuron directions. Weight-space protection exposes other tasks' features at 91 to 96 percent of the intended rate, while feature-space protection is more selective. The storage story is also useful: per-task feature masks are tiny compared with weight-space anchors.

### 9. What are the weaknesses, limitations, or red flags?

The method depends on good SAE coverage. The paper notes current SAEs leave some activation variance invisible to the regularizer, which is a channel for unpenalized forgetting. The main validation is on Gemma-2 9B-it; cross-model validation is listed as in progress. Output-format interference remains unsolved: some MedCL tasks with idiosyncratic answer formats fail under no-replay methods. O-LoRA still wins on overall performance through task-specific parameter isolation, and replay can beat SAE on MedCL when past data storage is allowed.

### 10. What challenges or open problems remain?

The biggest question is whether SAE feature masks are robust across model families, model scales, and domains where available SAEs are weaker. Another challenge is combining this feature-space protection with replay or architectural isolation without over-constraining the model. The method also needs better handling of output-format memory, which may not live cleanly in protected internal features alone.

### 11. What future work naturally follows?

Test on Mistral, Llama-family, and larger Gemma models with comparable SAE coverage. Combine SAE-guided regularization with small replay buffers targeted at output formats. Explore online mask updates and mask merging across tasks. Use causal feature importance or activation patching to improve the relevance mask beyond mean activation.

### 12. Why does this matter for cabbageland?

Cabbageland cares about durable agents and long-lived adaptation. This paper gives a concrete way to preserve knowledge at a more semantic granularity than weights. It also suggests a general memory principle: before protecting something, choose a coordinate system where the thing you care about is actually separable.

### 13. What ideas are steal-worthy?

Build task masks over interpretable feature coordinates. Separate stability and plasticity instead of using a one-sided anti-drift penalty. Store compact task masks rather than past examples when privacy or storage matters. Diagnose continual-learning methods by whether they preserve plasticity, not only by whether they reduce forgetting.

### 14. Final decision

Keep and cite. The empirical scope is not complete, but the feature-space regularization idea is exactly the kind of mechanism worth preserving.
