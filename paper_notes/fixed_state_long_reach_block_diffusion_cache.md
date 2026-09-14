# Fixed State, Long Reach: What a Constant-Size Cache Buys Block Diffusion at Scale

## Basic info

* Title: Fixed State, Long Reach: What a Constant-Size Cache Buys Block Diffusion at Scale
* Authors: Vaibhav Singh, Pierre-Andre Noel, Torsten Scholak, Eugene Belilovsky, Oleksiy Ostapenko
* Year: 2026
* Venue / source: arXiv:2609.11998
* Link: https://arxiv.org/abs/2609.11998
* Date surfaced: 2026-09-14
* Why selected in one sentence: It shows that block diffusion can have exact cached generation with constant-length state when the mixer and training objective are designed for it.

## Quick verdict

* Must read

This is a strong mechanism paper for diffusion language models. The useful move is not "cache more cleverly" but "train the denoiser under the same single-frontier information pattern that cached block generation will use." The result is a fixed-size state-space cache that stays flat to 256k tokens, with long-context retrieval benefits and little measured quality cost at 3B scale.

## One-paragraph overview

The paper compares three 3B block-diffusion denoisers that differ mainly in sequence mixer: full attention, full bidirectional Mamba-2, and a hybrid with five attention layers plus 23 Mamba layers. All are trained on 300B tokens with a single-frontier block-diffusion objective: previous blocks are clean, the frontier block is partially masked, future blocks are fully masked, and loss is on the frontier block. During inference, generation proceeds block by block. Attention caches grow with prefix length, but the Mamba model folds finalized blocks into a constant-size recurrent state, so decode latency and memory do not grow with context length.

## Model definition

### Inputs

The model takes token sequences split into fixed-size blocks, a clean prefix of finalized blocks, a partially masked frontier block, fully masked future blocks during training, and a denoising timestep/schedule. At inference it consumes the current block plus a per-layer cache summarizing finalized blocks.

### Outputs

The denoiser predicts original tokens for masked positions in the current frontier block. During generation, it reveals high-confidence masked tokens over S denoising steps and finally updates the cache with the finalized block.

### Training objective (loss)

The training objective is a reweighted cross-entropy/negative-ELBO-style masked diffusion loss on masked positions of one sampled frontier block. The single-frontier objective matches cached generation: clean previous blocks, partially noised current block, and masked future blocks.

### Architecture / parameterization

All main models are 3B-parameter block-diffusion denoisers with dmodel 2560, depth 28, and block size 32. The attention model uses 28 attention layers and O(L) KV cache. The Mamba model uses 28 bidirectional Mamba-2 layers, with a forward recurrent prefix state and a backward recurrence restricted to the current block. The hybrid model has five attention layers and 23 Mamba layers.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Diffusion language models can decode tokens in parallel, but bidirectional denoisers do not naturally support the prefix KV caching that makes autoregressive inference efficient. Block diffusion helps, but attention-based block caches still grow with context length and retrofitted caches can approximate rather than exactly match the model computation.

### 2. What is the method?

Train block-diffusion denoisers with a single-frontier objective, then use a unified cached generation interface. For Mamba layers, finalized blocks are folded into a fixed recurrent state; for attention layers, keys and values are appended as usual; for hybrid layers, the cache is heterogeneous.

### 3. What is the method motivation?

If the training objective exactly matches the information available at cached generation, then caching is part of the model's intended computation rather than a post-hoc approximation. If the mixer can summarize the prefix into fixed state, the cache can be O(1) in sequence length.

### 4. What data does it use?

The three 3B models are trained on Nemotron-CC with a 300B token budget, sequence length 1024, global batch of 4096 sequences, and 71,525 training steps. Evaluation includes efficiency sweeps, needle-in-a-haystack retrieval, LongBench, common-sense/reasoning likelihood tasks, and generation quality metrics.

### 5. How is it evaluated?

The paper measures per-step decode latency, peak memory, throughput, passkey retrieval accuracy at lengths up to 16x training length, LongBench macro-average, eight downstream likelihood-scored tasks, and generation quality under different denoising-step budgets.

### 6. What are the main results?

At 256k tokens, the Mamba cache stays at about 6.8 ms per step and 7.5 GB, while attention grows to 29 ms and 82 GB. Mamba gives 4.3x lower latency, 11x less memory, and 2.6x higher single-stream throughput. Under batch 8 at 256k, Mamba reaches 1593 tokens/s while attention is out of memory beyond batch 1, giving a 14x aggregate-throughput advantage. In needle retrieval, attention collapses past 2x train length, while Mamba and hybrid retain useful retrieval out to 8-16x. On downstream quality, attention and hybrid are roughly tied and Mamba trails by about one macro point.

### 7. What is actually novel?

The novelty is the exact cached block-diffusion framing at scale, especially showing that a state-space mixer can make the cache length-independent while preserving the block diffusion objective. The paper also makes a fair mixer comparison by holding model size and training budget broadly constant.

### 8. What are the strengths?

The mechanism is crisp. The efficiency numbers are concrete and deployment-relevant. The long-context generalization result is tied to the position-free recurrent state rather than only to speed. The hybrid result is useful because it shows a practical middle ground: some attention for global recall, mostly Mamba for state efficiency.

### 9. What are the weaknesses, limitations, or red flags?

The models are 3B base models, not instruction-tuned frontier systems. Absolute downstream task scores are modest. Mamba trails attention/hybrid slightly on some quality measures. The paper does not prove the same tradeoff at much larger scales or for post-trained reasoning models.

### 10. What challenges or open problems remain?

Scaling to larger models, testing instruction/post-training behavior, combining constant-state block diffusion with strong reasoning/tool-use models, and understanding when attention layers remain necessary are all open. Another question is how the fixed state should be audited for content specificity, similar to video memory substitution.

### 11. What future work naturally follows?

Train larger hybrid block-diffusion models; evaluate with optimized serving stacks; test on long-context reasoning and retrieval-heavy tasks; and combine exact state caches with adaptive block sizes or confidence-based token acceptance.

### 12. Why does this matter for cabbageland?

Cabbageland cares about generative models, memory, long context, and explicit state. This paper shows that the right state carrier can turn diffusion-language inference from a nice theory into something with deployment-shaped complexity.

### 13. What ideas are steal-worthy?

Match the training mask to the inference cache interface. Prefer exact reusable state over approximate retrofit caching. Treat denoising budget S as a single quality-speed knob. Use a hybrid architecture when full constant-state efficiency and some global attention are both desirable.

### 14. Final decision

Preserve. This is a concrete design reference for efficient diffusion language models and long-context state carriers.
