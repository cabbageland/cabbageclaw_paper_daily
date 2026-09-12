# Logit Refiner: Improving Visual Autoregressive Models via Intra-Scale Dependency Modeling

## Basic info

* Title: Logit Refiner: Improving Visual Autoregressive Models via Intra-Scale Dependency Modeling
* Authors: Meimingwei Li, Stefan Andreas Baumann, Felix Krause, Bjorn Ommer
* Year: 2026
* Venue / source: arXiv:2609.11804
* Link: https://arxiv.org/abs/2609.11804
* Date surfaced: 2026-09-12
* Why selected in one sentence: It locates a visual generation failure in VAR's within-scale independence assumption and fixes it with a lightweight joint sampler over frozen backbone features.

## Quick verdict

* Highly relevant

This is a clean mechanism paper. The key point is not that adding parameters helps; it is that independent same-scale token sampling throws away dependencies the image needs. Full arXiv HTML inspected.

## One-paragraph overview

Visual Autoregressive Models generate images scale by scale, predicting all tokens inside a scale in parallel. The paper argues that this is a mean-field-style approximation: same-scale tokens are sampled independently even though the image distribution requires local and structural dependencies. Logit Refiner adds a causal autoregressive module over frozen VAR hidden states, sequentially sampling tokens inside each scale while leaving the expensive backbone intact. The result is a plug-in correction that improves ImageNet generation across VAR scales and transfers to text-to-image variants.

## Model definition

### Inputs

Frozen VAR backbone hidden states for the current scale, previously generated coarser-scale tokens, and previously sampled tokens within the current scale during autoregressive refinement.

### Outputs

Refined logits for same-scale discrete visual tokens, sampled sequentially within the scale.

### Training objective (loss)

Cross-entropy / next-token prediction over ground-truth same-scale tokens under a causal attention mask, with the backbone frozen. The paper also studies end-to-end variants, but the main method trains only the refiner.

### Architecture / parameterization

A lightweight causal transformer-style autoregressive refiner initialized to be functionally close to the original VAR output head, using frozen backbone features as conditioning. It adds roughly 10% parameters and less than 5% of the base model's training compute.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

VAR image generators are efficient but can produce locally incoherent samples because all tokens inside a scale are sampled independently.

### 2. What is the method?

Add a Logit Refiner that samples same-scale tokens autoregressively, conditioned on frozen backbone features and the already sampled same-scale context.

### 3. What is the method motivation?

The authors show the flaw is in the decoding rule. Even correct pointwise marginal distributions can produce invalid joint samples when sampled independently.

### 4. What data does it use?

The main experiments use class-conditional ImageNet 256x256 with 50k generated samples for FID evaluation. The paper also tests text-to-image variants in the appendix.

### 5. How is it evaluated?

FID is the primary metric, with IS, precision, and recall also reported. The paper includes ablations that separate joint sampling from extra capacity, architecture choices, scale coverage, and backbone fine-tuning.

### 6. What are the main results?

Across VAR backbones from 310M to 2B parameters, Logit Refiner improves FID by 0.16 to 0.49 and recall by 0.04 to 0.06. A frozen-backbone refiner improves VAR-d16 FID from 3.30 to 2.81 with 66M added parameters. Jointly training the backbone improves further to 2.57 but costs much more.

### 7. What is actually novel?

The paper reframes VAR artifacts as a sampling-factorization problem and offers a plug-in joint sampler that preserves the pretrained backbone.

### 8. What are the strengths?

The diagnosis is crisp. The ablations are convincing: a capacity-matched bidirectional add-on with independent sampling does not match causal autoregressive sampling. The method is modular and cheap relative to retraining a generator.

### 9. What are the weaknesses, limitations, or red flags?

The refiner reintroduces sequential work inside each scale, so inference is not as parallel as vanilla VAR. The evidence is mostly image-generation metrics; controllability and semantic editing behavior are not the central focus.

### 10. What challenges or open problems remain?

How to get joint same-scale dependency without giving up too much parallelism remains open. The same idea should be tested in video, 3D token hierarchies, and multimodal generative models.

### 11. What future work naturally follows?

Use conditional or blockwise refiners that model local dependencies where they matter most. Combine the refiner with semantic controls or uncertainty estimates to allocate sequential sampling only to risky regions.

### 12. Why does this matter for cabbageland?

It is a compact example of a good architectural diagnosis: bigger latent machinery is not always the missing piece. Sometimes the state variable was present, but the sampler erased the dependency.

### 13. What ideas are steal-worthy?

When a model generates structured outputs in parallel, audit whether the decoding factorization destroys important dependencies. Add a small joint module at the handoff rather than retraining the whole system.

### 14. Final decision

Preserve. This is a useful reference for compositional generation, structured decoding, and "representation was not the bottleneck" arguments.
