# Limits of Confidence in Diffusion

## Basic info

* Title: Limits of Confidence in Diffusion
* Authors: Russ Webb, Amitis Shidani, Alice Bizeul, Dan Busbridge
* Year: 2026
* Venue / source: arXiv:2609.20581
* Link: https://arxiv.org/abs/2609.20581
* Date surfaced: 2026-09-19
* Why selected in one sentence: It shows that confidence-ranked parallel writes in discrete diffusion can match per-position predictions while still breaking the joint distribution.

## Quick verdict

* Must read

This is a very strong diffusion-evaluation paper because it turns a vague decoding worry into a precise joint-distribution failure. The useful point is not that all parallel discrete diffusion is doomed; it is that per-position confidence cannot certify the conditional independence needed for exact parallel writes. This note is based on the full arXiv PDF text.

## One-paragraph overview

The paper studies discrete diffusion samplers that write multiple token positions per step from per-position distributions, including masked diffusion, remasking, and uniform-state samplers. It proves that writing a group of positions independently is exact only when that group is conditionally independent given the frozen tokens; if the group is dependent, the step incurs at least the total correlation of the group. It then builds ScanAndAdd, a synthetic distribution whose conditionals and support are computable, and shows that confidence-ordered remasking can reach perfect per-sample correctness while producing a token distribution far from the training distribution.

## Model definition

### Inputs

The theoretical object is a partially fixed token sequence with some positions still writable. The empirical model is trained on ScanAndAdd sequences containing value positions, operation/command positions, and answer digits.

### Outputs

The sampler outputs complete token sequences. During a step, it outputs independent token draws for the selected positions from per-position distributions.

### Training objective (loss)

The paper assumes the per-position predictions are as good as training can make them: exact conditionals under masked cross-entropy style objectives. The ScanAndAdd model is trained with masked-token prediction; the key result is that even exact per-position conditionals do not remove the grouping error.

### Architecture / parameterization

The empirical ScanAndAdd model uses a small transformer with sinusoidal positional encoding, dmodel 256, 8 attention heads, 6 layers, feed-forward dimension 1024, no dropout, and 4.75M trainable parameters. The theory is architecture-independent and applies to independent-update samplers reading per-position distributions.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Discrete diffusion is attractive partly because it can write several positions in parallel. The paper asks when that parallel write is distributionally valid, not merely when a decoded sample looks correct.

### 2. What is the method?

The paper defines an independent-update sampler, proves conditions under which a parallel write cannot match the true conditional joint distribution, then validates the failure mode on ScanAndAdd where the target distribution is exactly analyzable.

### 3. What is the method motivation?

Per-position confidence looks like a natural scheduling signal, but dependencies between tokens are joint facts. A sampler that only reads marginal distributions cannot know whether a group is safe to write together.

### 4. What data does it use?

The empirical task is ScanAndAdd, a synthetic sequence distribution with computable conditionals, entropies, and support. The authors generate 10M training examples with a 0.9/0.1 train/validation split.

### 5. How is it evaluated?

The paper compares correctness, well-formedness, uniqueness, and token total-variation distance between generated and training samples. It compares confidence-ordered remasking with hand-specified write orders that either respect or destroy the independent free group.

### 6. What are the main results?

A trained ScanAndAdd model reaches 1.00 well-formedness, correctness, and uniqueness, but confidence-ordered remasking remains far from the training distribution. The best confidence-ordered setting with near-perfect correctness sits around 29x the sampling-noise floor in token TV. A hand-specified dependency-respecting write order reaches the noise floor, with TV around 0.0050 to 0.0066 and correctness 0.987 to 0.996.

### 7. What is actually novel?

The main novelty is a clear decomposition of the error: even with exact per-position predictions, an independent product over a dependent group incurs a grouping term equal to total correlation. The paper also proves that per-position distributions cannot certify whether a group is independent.

### 8. What are the strengths?

The theory is clean, the synthetic task is well chosen, and the paper avoids hiding behind aesthetic sample metrics. It directly explains why per-sample correctness can miss a distributional failure.

### 9. What are the weaknesses, limitations, or red flags?

The empirical measurement is on one synthetic task. The paper does not show the same total-variation accounting on natural language, where the full distribution is unavailable. A learned domain-aware scheduler is not ruled out, though it would need information beyond per-position confidence.

### 10. What challenges or open problems remain?

The obvious next problem is designing schedulers or block samplers that can detect or model dependencies without giving up all parallelism. Natural-language diagnostics that expose this failure without access to the full distribution are also needed.

### 11. What future work naturally follows?

Train schedulers that predict safe groups, decode through dependency-aware blocks, evaluate diffusion language models with distributional probes rather than only task accuracy, and connect this to observed diversity loss under confidence-ordered decoding.

### 12. Why does this matter for cabbageland?

Cabbageland cares about explicit state and uncertainty. This paper is a useful warning that local confidence is not a reliable proxy for joint state, especially when a system commits multiple pieces at once.

### 13. What ideas are steal-worthy?

Evaluate the distribution a sampler carries, not just correctness. Treat conditional independence as a precondition for parallel commitment. Build synthetic tasks where the true joint structure is computable before trusting a decoding rule on real data.

### 14. Final decision

Preserve. This is the strongest conceptual paper in today's non-duplicate batch.
