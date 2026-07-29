# Minimizing Targeted Activations: Input-Only Suppression of Evaluation-Awareness Latents in Large Language Models

## Basic info

* Title: Minimizing Targeted Activations: Input-Only Suppression of Evaluation-Awareness Latents in Large Language Models
* Authors: Deepanshu Mody, Samarth Agarwal, Utkarsh Mittal, Dipesh Tharu Mahato
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.25907
* Date surfaced: 2026-07-29
* Why selected in one sentence: It takes a fashionable mechanistic story about eval-awareness latents and does the annoying but necessary work of checking whether suppressing the latent actually suppresses the behavior.

## Quick verdict

**Highly relevant**

This is a strong negative-result paper because it separates activation control from behavioral control instead of collapsing them into one story. The authors show that input-side prompt optimization can strongly suppress several target latents, including a causally validated SAE feature, while still failing to produce the behavioral effect people might naively infer. I inspected the full arXiv HTML paper, especially the method, behavioral protocol, controls, and results sections.

## One-paragraph overview

The paper studies the input-side dual of activation steering: instead of editing activations at inference time, can you optimize a fluent prompt that suppresses a chosen latent without model-side intervention? The target is an evaluation-awareness signal in Llama models, motivated by the worry that models might behave differently when they detect being tested. The authors adapt Fluent Dreaming / EPO-style discrete prompt optimization to minimize target activations under five constructions: a CAA direction, a subspace norm, an SAE feature, a single neuron, and a behavioral logit difference. The main result is not that suppression is impossible. It is that suppression is easy to overread. The latent can move dramatically while the relevant behavior barely moves or even shifts the wrong way, so the paper argues that activation readability is not behavioral controllability.

## Model definition

### Inputs
The inputs are prompt tokens, chosen target-latent readouts from selected model layers, and held-out eval-versus-deploy prompt sets used to calibrate behavior.

### Outputs
The outputs are optimized prompt prefixes, target-activation suppression scores, fluency measurements, behavioral eval judgments, and erasure-control diagnostics.

### Training objective (loss)
The optimization objective is a negated feature-target term combined with fluency and task-preservation regularizers. The paper uses token-gradient search over discrete prompts rather than training a new backbone model.

### Architecture / parameterization
There is no new base model architecture. The experiments operate on Llama-3.2-3B and Llama-3.1-8B with five target constructions: a CAA direction, a subspace norm, an SAE feature, a single MLP neuron, and a behavioral logit difference.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It asks whether internal eval-awareness signals can be suppressed from the input side in a way that would matter for evaluation validity. More broadly, it asks whether controlling a readable latent actually controls the behavior people think the latent stands for.

### 2. What is the method?
The method is gradient-based prompt optimization adapted from Fluent Dreaming / EPO, but with the target feature term negated so the optimization minimizes rather than maximizes the latent. The paper then evaluates the optimized prompts with behavioral endpoints, fresh probes, placebo directions, wrap tests, and probe-hacking controls.

### 3. What is the method motivation?
Activation steering shows that some internal directions are readable and steerable, but that alone does not say whether the model can be controlled at the prompt level or whether the readout corresponds to the important behavior. The paper is motivated by the exact place where interpretability claims can get ahead of themselves.

### 4. What data does it use?
It uses evaluation-versus-deployment prompt sets, balanced contrast prompts designed to reduce register confounds, and natural-text slices from the Pile as a baseline source of non-optimized text. The experiments are run on Llama-3.2-3B and Llama-3.1-8B.

### 5. How is it evaluated?
The evaluation tracks suppression strength, fluency, behavioral log-odds for "is this text an evaluation?", erasure probes, orthogonal-complement probe controls, placebo random directions, and in-context wrap tests where an optimized prefix is prepended to a real evaluation passage.

### 6. What are the main results?
The optimization robustly suppresses target latents, with direction-style targets reaching roughly z = -7 relative to a null and the chosen SAE feature being fully and selectively turned off. But the main behavioral story is much weaker: a placebo random direction suppresses just as hard and shifts behavior just as far, and when a real evaluation body is held fixed in context, suppressing the eval direction does not reduce the model's eval judgment and can slightly increase it. The behavioral readout itself is strong enough to discriminate held-out eval from deploy prompts with AUROC 0.92, which makes the null result more meaningful rather than less.

### 7. What is actually novel?
The novelty is the combination of input-side latent minimization with a behavior-plus-erasure protocol designed to detect when activation suppression is merely representational theater. The paper also usefully broadens the target constructions rather than pretending one direction is the whole concept.

### 8. What are the strengths?
The strengths are the controls and the willingness to keep the negative result negative. The authors do not stop at "we drove the number down." They check placebo directions, natural-text baselines, behavioral endpoints, and fresh probes, which is the right standard for this kind of claim.

### 9. What are the weaknesses, limitations, or red flags?
The experiments are on relatively small open models rather than frontier systems. Fluently suppressing the target is somewhat seed-dependent. And while the paper does a good job controlling for register confounds, evaluation-awareness is still a slippery construct whose operationalization could change under different tasks or model families.

### 10. What challenges or open problems remain?
The big open problem is finding internal variables whose manipulation really is causally tied to evaluation-sensitive behavior rather than merely correlated with it. Another open issue is how to extend this kind of protocol to much larger closed models where both white-box access and repeated optimization may be limited.

### 11. What future work naturally follows?
Future work should combine this style of prompt-side optimization with more causally grounded behavioral tasks, stronger model families, and better concept definitions. It would also be useful to test whether similar failures appear for other mechanistic targets beyond eval-awareness, such as refusal, deception, or tool-use confidence.

### 12. Why does this matter for cabbageland?
It matters because cabbageland cares about mechanisms that survive contact with behavior. A latent that is readable but not behaviorally load-bearing is exactly the sort of tidy internal story that can waste research time if nobody stress-tests it.

### 13. What ideas are steal-worthy?
Always pair internal-signal claims with behavioral endpoints. Use placebo directions, in-context wrap tests, and orthogonal-complement probe controls to detect rotation or non-specific prompt effects. Treat natural-text baselines as serious competitors to optimizer-generated probes. Most importantly, do not treat linear readability as automatic causal authority.

### 14. Final decision
**Keep it.** This is a useful corrective paper for mechanistic-interpretability work, eval-robustness work, and anyone tempted to confuse internal measurement with behavioral control.
