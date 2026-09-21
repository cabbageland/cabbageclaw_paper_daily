# Abstention and Noise Filtering: Two Missing Primitives of Softmax Attention

## Basic info

* Title: Abstention and Noise Filtering: Two Missing Primitives of Softmax Attention
* Authors: Richard Zhe Wang
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2609.22005
* Date surfaced: 2026-09-21
* Why selected in one sentence: It decomposes attention value gating into two separate mechanisms and tests their scale behavior.

## Quick verdict

* Highly relevant

This is useful because it refuses to leave "gating helps" as an explanation. It separates the zero-output option from value-pathway filtering and tests each with matched models. The paper is small-scale by frontier standards, but the mechanism split is clear.

## One-paragraph overview

The paper argues that standard softmax attention lacks two primitives: an attention head cannot output nothing because its routing weights sum to one, and the value pathway is linear, so noisy superposed reads are aggregated like signal. It supplies abstention with a learned per-head sink logit whose phantom value is zero, and supplies filtering with value gates based on read norm or a learned projection. Across 10M, 50M, 124M, and 350M models trained on FineWeb-Edu, the benefit of explicit abstention shrinks with scale while filtering grows. The combined sink-logit plus projection-gate arm has the best validation loss at every tested scale.

## Model definition

### Inputs

The trained models are causal language models receiving token sequences from FineWeb-Edu. The attention mechanisms receive standard query, key, and value vectors per token position.

### Outputs

The language models output next-token distributions. The attention variants output head activations, optionally with mass sent to a zero-valued phantom slot or reads attenuated by gates.

### Training objective (loss)

The training objective is standard next-token language modeling cross-entropy, reported as validation loss in nats. The causal injection experiments measure loss increases under controlled value-read noise.

### Architecture / parameterization

The baseline is standard causal softmax attention. Variants include off-by-one denominator, learned sink logit, sink token, norm gate, routing-slot control, projection gate, sink logit plus norm gate, and sink logit plus projection gate.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It tries to explain why value or output gates improve attention models, and whether that improvement comes from abstention, noise filtering, or something else.

### 2. What is the method?

The author constructs attention arms that isolate each proposed primitive. A sink logit gives exact abstention. Value gates provide filtering. Routing-slot controls distinguish filtering from merely reweighting attention mass.

### 3. What is the method motivation?

Standard attention must route all mass somewhere, which leads to attention sinks. It also linearly aggregates value reads, making it poor at suppressing interference from superposed features.

### 4. What data does it use?

The models are trained from scratch on FineWeb-Edu web text, with token budgets from 0.2B at 10M scale to 5.8B at 350M scale.

### 5. How is it evaluated?

The main metric is paired validation-loss improvement over matched baselines. The paper also uses attention-mass diagnostics and causal value-read noise injection experiments.

### 6. What are the main results?

The sink-logit zero-option gain falls from 0.0185 nats at 10M to 0.0068, 0.0052, and 0.0013 at 50M, 124M, and 350M. Filtering gains rise with scale: the norm gate's filtering increment reaches 0.0074 at 350M, and the projection gate reaches 0.0114. The sink-logit plus projection-gate arm has the lowest validation loss at every tested scale, including 3.0210 nats at 350M.

### 7. What is actually novel?

The novelty is the decomposition. A value gate is shown to contain both a partial zero option and a filter, and the paper designs controls that separate those roles.

### 8. What are the strengths?

The experiments are cleanly matched and seed-paired where possible. The scale trend is interpretable: large baselines learn their own sinks, so explicit abstention helps less, while filtering becomes more valuable.

### 9. What are the weaknesses, limitations, or red flags?

The largest scale is 350M with a single seed. The work does not prove frontier-model behavior, and the tasks are mostly pretraining loss plus limited zero-shot checks.

### 10. What challenges or open problems remain?

The natural question is whether the same two-primitives split holds in billion-scale models, long-context settings, and architectures with other routing or memory mechanisms.

### 11. What future work naturally follows?

Run sink-logit plus projection-gate variants in larger LMs and inspect whether filtering aligns with identifiable superposed features or merely improves optimization.

### 12. Why does this matter for cabbageland?

It shows how to turn an architectural hunch into a mechanistic distinction. That is directly useful for thinking about memory, attention, and controllability in future model designs.

### 13. What ideas are steal-worthy?

The best steal is the distinction between a query-level zero option and a key/read-level filter. They solve different failures and should not be collapsed into "gating."

### 14. Final decision

Preserve. The paper is compact, mechanistic, and useful for architecture taste.
