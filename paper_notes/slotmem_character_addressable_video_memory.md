# SlotMem: Character-Addressable Internal Memory for Narrative Long Video Generation

## Basic info

* Title: SlotMem: Character-Addressable Internal Memory for Narrative Long Video Generation
* Authors: Yilai Liu, Xin Zhang, Shiyuan Zhang, Hongyang Du
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.15772
* Date surfaced: 2026-07-20
* Why selected in one sentence: It replaces frame-level memory retrieval with explicit character-addressable slot memory, which is a cleaner mechanism for long-range identity consistency.

## Quick verdict

**Useful**

This is adjacent inspiration rather than a foundational paper, but the mechanism is real and explicit. The paper earns its keep by asking what the memory should be indexed by if the real target is recurring character identity. I inspected the arXiv HTML sections covering the memory architecture, training objectives, implementation details, quantitative results, and limitations.

## One-paragraph overview

SlotMem targets one of the worst failure modes in long narrative video generation: recurring characters gradually drift because the model retrieves memory from frames, keyframes, or global context that entangles identity with background and scene junk. The proposed fix is to make memory character-addressable. A Character-Semantic Probe localizes character-relevant visual tokens using cross-attention responses to character names in the prompt, a Memory Encoder compresses those features into role-wise slots, a Memory Writer updates the stored slots conservatively as new chunks arrive, and Character-Wise Cross-Attention injects only the matching slot back into localized tokens for the same character. That is much closer to an actual memory interface than "retrieve a nice-looking frame."

## Model definition

### Inputs
The system takes the current video chunk latent, image condition, prompt text with recurring character names, stored role-wise memory slots from previous chunks, and optional update chunks that contain additional observations of those characters.

### Outputs
It outputs the denoised target video chunk and updated character-specific memory slots used for later chunks.

### Training objective (loss)
Stage 1 optimizes the base diffusion denoising loss plus an auxiliary slot-contrastive loss that encourages character slots to be separable from background slots. Stage 2 adds an update chunk, freezes the memory encoder and injection interface, trains the Memory Writer to produce conservative residual memory updates, and continues optimizing the denoising objective.

### Architecture / parameterization
The method is built on `Wan2.2-I2V-A14B` with rank-`128` LoRA fine-tuning. The added modules are a Character-Semantic Probe, a role-wise Memory Encoder, a Memory Writer for dynamic updates, and sparse Character-Wise Cross-Attention for targeted memory injection.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to preserve recurring character identity across long, multi-chunk narrative video generation, especially when characters disappear and reappear after scene changes.

### 2. What is the method?
The method builds internal role-wise slot memory for each recurring character, updates that memory over time, and injects it only into the localized visual tokens associated with the same character.

### 3. What is the method motivation?
The motivation is that frame-level or global memory stores entangle identity with incidental visual factors like background, other characters, and transient scene state.

### 4. What data does it use?
It uses a curated dataset of publicly available films and videos with hierarchical captions. Chunks contain `81` frames each, and training pairs are selected so that memory chunks, target chunks, and update chunks share at least one recurring character name.

### 5. How is it evaluated?
It is evaluated against the base `Wan2.2` model and baselines such as `StoryDiffusion`, `StoryMem`, and `IAMFlow` using `VBench`, `ViStoryBench`, and `NarraStream-Bench`, plus qualitative comparisons and ablations.

### 6. What are the main results?
SlotMem achieves the best reported `Human Anatomy` score on VBench (`0.9480`), the best `Character Similarity` on ViStoryBench (`0.8603`), and the best `Subject Consistency` on NarraStream-Bench (`0.8771`). It also reaches the top `Motion Smoothness` score (`0.9912`) while keeping competitive overall dynamics instead of collapsing into overly static videos.

### 7. What is actually novel?
The novelty is the address scheme and memory interface: character-semantic token probing, role-wise slot memory, conservative online memory updates, and sparse reinjection into matching character tokens.

### 8. What are the strengths?
The mechanism is explicit, the injection is local instead of global, and the paper directly targets the identity-entanglement failure that frame-retrieval baselines mostly dodge.

### 9. What are the weaknesses, limitations, or red flags?
The pipeline relies on consistent character-semantic anchors in the captions, which is brittle when characters are similarly described or naming is noisy. The training scale is also still limited, so the generalization story is not fully stress-tested.

### 10. What challenges or open problems remain?
The hard case is open-world identity tracking where simple prompt names are not enough to disambiguate visually similar characters across diverse styles and settings.

### 11. What future work naturally follows?
The obvious next step is richer attribute-level character anchoring, larger and more diverse training data, and memory interfaces that can handle more ambiguous multi-character scenes without relying on clean caption names.

### 12. Why does this matter for cabbageland?
Cabbageland cares about explicit memory, reusable abstractions, and generation systems that know what their state is keyed by. SlotMem is useful because it turns "memory for identity" into an actual keyed subsystem.

### 13. What ideas are steal-worthy?
Bind memory addresses to the entity you actually care about. Use internal cross-attention responses as a cheap localization signal. Update stored memory conservatively with residual corrections instead of wholesale replacement. Inject retrieved memory sparsely at the matching tokens rather than globally.

### 14. Final decision
**Keep it.** This is not the deepest paper of the day, but the memory interface is clean enough to be worth preserving.
