# Register Tokens for Bounded-State Reasoning in Diffusion Language Models

## Basic info

* Title: Register Tokens for Bounded-State Reasoning in Diffusion Language Models
* Authors: Albert Ge, Chandan Singh, Yufan Zhuang, Xiaodong Liu, Jianfeng Gao, Frederic Sala
* Year: 2026
* Venue / source: arXiv:2609.16372
* Link: https://arxiv.org/abs/2609.16372
* Date surfaced: 2026-09-16
* Why selected in one sentence: It gives diffusion language models a fixed-size continuous state that survives chunk resets, then tests whether reasoning can continue without keeping previous text visible.

## Quick verdict

* Highly relevant

This is a strong memory/mechanism paper for diffusion LMs. It is not claiming registers beat full context everywhere; the useful claim is narrower and cleaner: when output must span fixed windows, a small continuous carry channel can outperform discrete text carry and no-carry chunking. This note is based on the full arXiv HTML text.

## One-paragraph overview

Masked diffusion language models generate chunks by denoising masked tokens with bidirectional attention. Normally, reasoning across chunks requires keeping previous generated text in context. This paper instead adds fixed register-token positions whose hidden states are read after one chunk and reused as embeddings in the next chunk after the previous text is cleared. Training forces usefulness by clearing generated text, masking prompt access in continuation passes, and sometimes using fully masked chunks so the registers become the only cross-chunk information path. On LLaDA and Dream, registers beat discrete-text carry on every main benchmark row and are especially useful for bounded code generation.

## Model definition

### Inputs

The model receives a prompt, a fixed number of register-token positions, and a current masked generation chunk. For continuation chunks, prior generated text is removed and the register positions are initialized from hidden states saved after the previous chunk.

### Outputs

The model outputs denoised text chunks. It also outputs updated register hidden states after a clean forward pass over the completed chunk, which become the carried state for the next chunk.

### Training objective (loss)

The main objective is chunked supervised fine-tuning under the masked-denoising objective used by diffusion LMs. Continuation chunks are trained with prompt masking and fully masked passes so that gradients encourage prediction from carried register state. The paper also extends this to chunked diffu-GRPO for reinforcement learning on long-horizon reasoning tasks.

### Architecture / parameterization

The base models are LLaDA-8B-Base and Dream-7B-Base. Registers are fixed-position tokens whose last-layer hidden states are extracted after a chunk and reused as input embeddings at the same positions for the next chunk. The method changes the state-carry protocol and training masks rather than replacing the backbone.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Diffusion LMs can generate text in parallel chunks, but long reasoning usually requires preserving earlier generated text. That makes the active context grow and weakens the promise of bounded-window generation. The paper asks whether a model can clear visible text and continue from a compact learned state.

### 2. What is the method?

After each chunk, the model runs a clean forward pass and saves hidden states at register positions. For the next chunk, it clears the generated text, inserts those saved hidden states into the register positions, and denoises the next masked chunk. Training uses attention masks and fully masked passes so the continuation cannot cheat by reading erased text or prompt shortcuts.

### 3. What is the method motivation?

Discrete summaries are lossy and consume text tokens. Full context is accurate but expensive and unbounded. A continuous register state might store task progress in a form that is compact, writable, and readable by the model's own computation.

### 4. What data does it use?

The chunked SFT training data is a 60K-example mixture of math and code reasoning traces. Evaluations cover GSM8K, GSM-Hard, MATH500, Omni-MATH easy, HumanEval, and MBPP under fixed chunk sizes and chunk budgets.

### 5. How is it evaluated?

The paper compares full-sequence SFT, discrete-text carry, memory-token reconstruction, and registers. Math uses first-answer accuracy with 128-token chunks and up to 8 chunks. Code uses pass@1 with 64-token chunks and up to 16 chunks. It also reports continuation behavior by completion chunk, slot-count ablations, smaller-window controls, and chunked diffu-GRPO.

### 6. What are the main results?

Registers outperform discrete-text carry in all 12 main rows and lead both carry baselines in 10. Gains over discrete text reach 8.5 points on LLaDA GSM8K and 8.0 on Dream GSM8K. The largest code gain is 19.5 points on Dream MBPP. Registers lead every code row. The strongest caveat is that full-sequence SFT leads all eight 128-token math rows, while registers are strongest when success needs continuation beyond one chunk.

### 7. What is actually novel?

The novelty is the write/read protocol for continuous register state across cleared diffusion chunks, plus a training recipe that makes the state necessary rather than decorative. The paper also tests the mechanism against discrete text and memory-token alternatives under matched bounded-generation protocols.

### 8. What are the strengths?

The experimental setup directly tests the intended claim. The paper does not hide the full-context baseline. The chunk analysis shows where the gains come from: for code, correct programs often require later chunks, while math at the chosen window can be compressed into first-chunk answers by full-sequence SFT.

### 9. What are the weaknesses, limitations, or red flags?

Registers do not replace full-context decoding at longer visible horizons. Most SFT comparisons use one seed, and not every numerical lead is individually significant. Continuous and discrete slots are matched by count rather than information capacity. Masking probabilities and number of denoising passes are not fully ablated. The instruction-tuned pilot degrades with the unmodified recipe.

### 10. What challenges or open problems remain?

The main open question is whether register state scales to larger models, more domains, longer horizons, and input compression rather than just output continuation. Another question is how to inspect or supervise what the registers store without turning them back into brittle summaries.

### 11. What future work naturally follows?

Use registers as learned long-context compressors for inputs, not only generated outputs. Combine registers with retrieval and KV-cache policies. Train auxiliary losses for interpretable intermediate state. Test multi-chunk RL where reward credit crosses multiple register boundaries.

### 12. Why does this matter for cabbageland?

Cabbageland cares about memory that does work after the visible trace disappears. This paper gives a concrete state-carry mechanism and a useful evaluation shape: clear the text, preserve only the state, and see whether the next decision still works.

### 13. What ideas are steal-worthy?

Force a memory channel to be causal by erasing the shortcut. Match carry mechanisms under the same bounded-window protocol. Separate "short answer compression" from genuine multi-chunk reasoning. Use chunk-of-success analysis to tell whether memory is actually helping.

### 14. Final decision

Preserve. This is a compact, testable mechanism for bounded-state reasoning in diffusion LMs.
