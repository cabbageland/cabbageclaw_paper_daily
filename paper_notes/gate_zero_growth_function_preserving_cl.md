# Gate-Zero Growth: A Geometric Framework for Function-Preserving Continual Learning

## Basic info

* Title: Gate-Zero Growth: A Geometric Framework for Function-Preserving Continual Learning
* Authors: Dante Lok
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.14571
* Date surfaced: 2026-07-17
* Why selected in one sentence: It gives a geometric explanation for why zero-gated growth and related zero-init tricks can preserve old behavior during continual learning instead of treating them as loose engineering folklore.

## Quick verdict

**Highly relevant**

This is the kind of continual-learning paper I would rather keep than three louder benchmark papers. The useful contribution is the geometric story: at the growth point, old directions, new weights, and gate directions are not interchangeable, and that separation explains why some growth-and-freeze recipes preserve behavior while others forget catastrophically. I inspected the full arXiv HTML paper, including the theoretical framework, dense and MoE experiments, comparisons to non-function-preserving growth, and limitations.

## One-paragraph overview

The paper introduces gate-zero growth, a function-preserving way to expand a trained model by adding new residual blocks behind zero-initialized gates. Under a transversality condition, the functional Jacobian separates cleanly: old parameters keep their original effect, new branch weights are flat at first order, and only the new gates create first-order functional variation. That local geometry turns the common "freeze the old weights and train the new branch" recipe into something principled instead of ad hoc. The paper then shows how the same analysis also covers LoRA, ReZero, and zero-init adapters as instances of the same template.

## Model definition

### Inputs
The grown model takes the same sequence inputs as the base language model. The new ingredients are additional residual blocks or experts introduced behind zero-initialized gates.

### Outputs
It outputs next-token predictions like the base language model, while the continual-learning setup tracks both old-domain retention and new-domain adaptation after growth.

### Training objective (loss)
The model is trained with standard language-modeling objectives on the old and new domains, then evaluated under different continual-learning strategies such as Isolation, replay, and distillation after growth.

### Architecture / parameterization
The main instantiation is Transformer depth growth from `300M` to `857M`, with an additional MoE validation setting. The framework explicitly links gate-zero growth to LoRA, ReZero, and zero-init adapter constructions.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to explain and improve how a model can be expanded and adapted to a new domain without forgetting what the smaller model already knew.

### 2. What is the method?
The method is to add new residual capacity behind zero-initialized gates, analyze the resulting local geometry, and use that structure to motivate continual-learning strategies that preserve old behavior while letting new capacity activate gradually.

### 3. What is the method motivation?
Zero-init growth tricks often work, but the field mostly explains them operationally. This paper argues that the key property is geometric rank separation at the growth point, not generic regularization luck.

### 4. What data does it use?
The main sequential adaptation experiment grows a Transformer from WikiText-103 to BookCorpus. The paper also includes MoE cross-architecture validation.

### 5. How is it evaluated?
The paper measures old-domain perplexity, new-domain perplexity, forgetting after growth and adaptation, and cross-architecture behavior under dense and MoE setups. It compares Gate-FP to non-function-preserving stacking and several continual-learning strategies.

### 6. What are the main results?
In the `300M -> 857M` dense Transformer setting, Gate-FP plus Isolation holds forgetting to `Delta_A = +0.04` while reducing new-domain perplexity from `560.75` to `28.41`. A non-function-preserving control degrades badly and, under naive fine-tuning, drives old-domain perplexity past `1200`. In the MoE setting, the same preservation story still holds with `Delta_A = +0.20`, but plasticity is much weaker: the old behavior is preserved, yet the new-domain improvement is far less dramatic than in the dense case.

### 7. What is actually novel?
The novelty is the unified geometric explanation. The paper turns gate-zero growth, LoRA-style zero-init, ReZero, and adapter-style constructions into one local functional-Jacobian story rather than treating them as unrelated recipes.

### 8. What are the strengths?
The paper offers a real mechanism, not just a bag of ablations. The dense-model preservation results are strong, and the MoE section is useful because it shows where the story transfers cleanly and where it does not.

### 9. What are the weaknesses, limitations, or red flags?
The main adaptation story is still one sequential domain shift, and the transversality framework is local rather than a complete long-run training theory. The MoE results also expose a serious plasticity gap, which means preservation transfers more cleanly than useful adaptation.

### 10. What challenges or open problems remain?
The open problem is how to keep the preservation geometry while improving plasticity, especially for MoE-style growth where the safe operator is not yet enough.

### 11. What future work naturally follows?
Future work should test longer multi-domain sequences, design better MoE-specific growth operators, and connect the local geometric picture to longer-horizon continual-learning dynamics.

### 12. Why does this matter for cabbageland?
Cabbageland cares about continual learning, reusable capacity, and explicit structural reasons why a model keeps or loses competence. This paper gives a cleaner way to think about safe capacity expansion than generic "just freeze some weights" advice.

### 13. What ideas are steal-worthy?
Use zero-gated growth so new capacity is inert at insertion time. Treat the gate as the first-order control knob for new function rather than immediately updating all new weights. Evaluate retention and adaptation separately, especially when moving to architectures like MoE where preservation can transfer without adequate plasticity.

### 14. Final decision
**Keep it.** The geometry is the result, and it is worth preserving.
