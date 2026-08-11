# Multimodal Model Diffing for Feature Discovery and Control

## Basic info

* Title: Multimodal Model Diffing for Feature Discovery and Control
* Authors: Hunar Batra, Lachin Naghashyar, Ashkan Khakzar, Philip Torr, Christian Schroeder de Witt, Constantin Venhoff, and Ronald Clark
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.09928
* Date surfaced: 2026-08-11
* Why selected in one sentence: It turns multimodal SAE work into a genuinely causal control interface by isolating the features that multimodal training actually changed.

## Quick verdict

* Preserve-worthy direct paper

I inspected the arXiv HTML full text. This is one of the better recent multimodal interpretability papers because it does not stop at "we found an interesting feature." It uses feature discovery to support selective ablation and steering across multiple tasks.

## One-paragraph overview

The paper starts from a simple but important observation: SAEs trained directly on MLLM activations mix inherited language-model features with features actually changed by multimodal adaptation. MMDiff addresses that by adapting a base-LM SAE to a frozen MLLM, then diffing the two dictionaries to find features whose decoder directions rotate and whose activations become visually responsive. It uses contrastive token-level firing analysis to find task-specific subsets for spatial reasoning, multimodal safety, and OCR, and then applies causal removal or steering to those features. The result is a feature-level interface that is interpretable enough to inspect and concrete enough to control.

## Model definition

### Inputs
The method takes internal activations from frozen multimodal language models, along with task-specific prompt/image distributions used for contrastive feature discovery.

### Outputs
It outputs adapted SAE feature dictionaries, task-specific feature subsets, and intervention effects from feature ablation or steering.

### Training objective (loss)
The main training objective is the sparse autoencoder reconstruction objective used to adapt a base-LM SAE to multimodal activations. Downstream task-specific feature discovery and steering are inference-time procedures rather than new task-training losses.

### Architecture / parameterization
The pipeline has three stages: train multimodal SAEs initialized from base-LM dictionaries, identify multimodal-adapted features through model diffing, and discover task-specific causal features through contrastive firing analysis. Those features are then used for ablation and layer-targeted steering.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to identify which internal multimodal features actually drive specific behaviors, and to turn those features into practical control handles.

### 2. What is the method?
The method diffs a base-LM SAE against its multimodal-adapted counterpart, filters for visually adapted features, then finds task-specific subsets via contrastive firing analysis and uses them for targeted ablation or steering.

### 3. What is the method motivation?
If you train an SAE directly on a multimodal model, you do not know which features are inherited from the base LM and which were created or reshaped by multimodal training. The paper wants the latter, because those are the plausible causal handles for multimodal behavior.

### 4. What data does it use?
It studies three MLLM families: LLaVA-MORE, PaliGemma 2, and InternVL3.5-2B, and evaluates on visual-spatial reasoning, multimodal safety, and OCR settings such as VSR, VLSBench, and OCRBench.

### 5. How is it evaluated?
It evaluates feature causality through projection ablations and steering, measuring target-task drops or gains alongside control metrics like general VQA accuracy and benign-control behavior.

### 6. What are the main results?
Ablating top spatial features drops VSR by roughly 10-15% on average with minimal VQA loss. Top unsafe features reduce multimodal-safety attack success by 17-28% per category, and OCR-specific features produce a mean 16.9% category drop with low spillover. MMDiff-CAA steering improves spatial and OCR over vanilla CAA by 3.6% and 1.8% on average.

### 7. What is actually novel?
The novelty is not just multimodal SAEs. It is the combination of model diffing, task-specific contrastive feature discovery, and feature-level intervention in one pipeline that stays tied to measurable behavioral effects.

### 8. What are the strengths?
The paper evaluates across multiple backbones and multiple task types, and the control metrics matter. It is especially strong that the ablations reduce target behavior while keeping general VQA nearly unchanged.

### 9. What are the weaknesses, limitations, or red flags?
Safety and OCR experiments are only done on PaliGemma 2, so the full story is not yet shown across all backbones. Some safety-candidate ablations can collapse generation rather than cleanly induce refusal, which still requires post-hoc filtering.

### 10. What challenges or open problems remain?
The obvious next challenge is extending the recipe to larger and more diverse multimodal architectures, including MoE-style systems. Another is pushing from analysis-and-control demos toward more stable real deployment interventions.

### 11. What future work naturally follows?
Broader backbone coverage, embodied-AI safety targets, medical-image grounding, and sharper automatic feature interpretation all follow naturally from this pipeline.

### 12. Why does this matter for cabbageland?
Cabbageland cares about controllability and interpretability that actually touches behavior. This paper shows a way to isolate multimodal features that can be intervened on without bluntly damaging everything else.

### 13. What ideas are steal-worthy?
Diff feature dictionaries across training stages, not just within a final model. Use task-specific contrastive firing to separate real causal features from lexical artifacts. Measure target drop and collateral damage together.

### 14. Final decision
Keep as a preserved note. The pipeline is reusable, the interventions are concrete, and the paper gives a good template for behavior-level mechanistic work in MLLMs.

## 6. Mandatory critical angles

This paper is strongest on causal specificity and intervention design. The main caution is that it is still an early-stage control interface, not yet a mature general method for every multimodal family or safety regime.

## 7. Writing style

The right tone is favorable and precise. The paper deserves praise for turning interpretability into something you can actually use, while keeping clear that the current recipe still has coverage limits.

## 8. Repository output format

Saved as a preserved paper note because the diff-and-intervene pattern is directly relevant to future work on controllable multimodal systems.
