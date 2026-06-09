# MemoryVLA++: Temporal Modeling via Memory and Imagination in Vision-Language-Action Models

## Basic info

* Title: MemoryVLA++: Temporal Modeling via Memory and Imagination in Vision-Language-Action Models
* Authors: Hao Shi, Weiye Li, Bin Xie, Yulin Wang, Renping Zhou, Tiancai Wang, Xiangyu Zhang, Ping Luo, Gao Huang
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.09827
* Date surfaced: 2026-06-09
* Why selected in one sentence: It gives a VLA an explicit past-present-future temporal interface instead of relying on the current frame plus implicit dynamics.

## Quick verdict

**Strong direct hit**

MemoryVLA++ is the most relevant paper in today's batch. The useful contribution is the functional decomposition: working memory for the current observation, a perceptual-cognitive memory bank for past interactions, latent world-model imagination for future state evolution, and a diffusion action expert conditioned on the fused temporal representation. I inspected the arXiv PDF, including the method, benchmark tables, ablations, analysis, and latency discussion.

## One-paragraph overview

MemoryVLA++ extends the earlier MemoryVLA idea from past-only memory to full temporal modeling. A 7B VLM encodes current RGB observations and language into perceptual tokens and a cognitive token. Those tokens query a Perceptual-Cognitive Memory Bank that stores low-level visual details and high-level semantic summaries from previous interaction steps, with redundancy-aware consolidation when memory fills. In parallel, a manipulation-adapted video world model produces compact imagined future latents through partial denoising rather than decoded future video. A memory-guided integration module fuses those future cues with memory-augmented current tokens, and a diffusion action expert predicts temporally consistent robot actions.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Most VLA policies are too reactive. They map the current observation and instruction to an action chunk, which is brittle when the task depends on what already happened or what will happen next. The paper uses two examples: button pressing, where pre-press and post-press observations can look nearly identical, and dynamic conveyor grasping, where timing depends on anticipating object motion.

### 2. What is the method?

- Encode the current observation with a VLM into perceptual tokens for fine visual detail and a cognitive token for high-level semantics.
- Treat those current tokens as working memory.
- Maintain a Perceptual-Cognitive Memory Bank with perceptual and cognitive entries from past interactions.
- Retrieve relevant history with attention plus timestep positional encoding.
- Fuse retrieved history and current tokens with learned gates.
- Consolidate memory by merging temporally adjacent, semantically similar entries when capacity is reached.
- Adapt a Stable Video Diffusion style world model to manipulation videos.
- Use partial denoising and multi-scale UNet features as latent future imagination.
- Integrate imagined future tokens under memory guidance.
- Condition a diffusion action expert on the resulting full temporal-aware tokens.

### 3. What is the method motivation?

The paper's motivating decomposition is good: past, present, and future have different representational needs. Past interaction needs retrieval and consolidation. Present perception needs fine local detail plus task semantics. Future state does not need to be decoded as RGB; it needs compact dynamics cues that help action generation.

### 4. What data does it use?

The experiments cover five simulation benchmarks and several real-robot task categories. Simulation includes Libero, SimplerEnv, Mikasa-Robo, Calvin, and Libero-Plus. Real-robot evaluation covers general manipulation, long-horizon memory-dependent tasks, long-horizon imagination-dependent tasks, and robustness/generalization variants across multiple robot platforms.

### 5. How is it evaluated?

The paper reports success on:

- general robotic manipulation in Libero and SimplerEnv
- long-horizon temporal manipulation in Mikasa-Robo and Calvin
- robustness and generalization in Libero-Plus
- real-world short-horizon general tasks
- real-world long-horizon memory-dependent tasks
- real-world long-horizon imagination-dependent tasks
- ablations on memory length, gated fusion, consolidation, timestep positional encoding, memory type, denoising steps, imagination horizon, world-model freezing, and memory-guided integration
- latency and throughput on RTX 4090 and H20 GPUs

### 6. What are the main results?

On Libero, MemoryVLA++ reports a 98.4 average success rate, ahead of the listed CogACT and pi0 baselines. On SimplerEnv it reports 73.9 average success, 16.6 points above CogACT in the table. On Mikasa-Robo it reaches 44.4 average success, with especially large gains on memory-dependent tasks. On Calvin ABC-to-D, it reports an average completed task length of 4.29. On Libero-Plus it reports 73.1 in the zero-shot setting and 82.7 with supervised fine-tuning.

The real-robot table is more nuanced. MemoryVLA, not MemoryVLA++, is reported for general and memory-dependent real tasks, reaching 85 and 83 average scores. MemoryVLA++ is evaluated on long-horizon imagination-dependent tasks and reports 77 average score, compared with 49 for pi0 and CogACT and 65 for MemoryVLA. Latency rises from 0.187 seconds for the baseline to 0.241 seconds for MemoryVLA++ on an RTX 4090, while still reporting 66.4 Hz throughput.

### 7. What is actually novel?

The novelty is not a single module. It is the combined temporal interface: perceptual-cognitive memory for past context plus latent future imagination, both integrated before action generation. The Perceptual-Cognitive Memory Bank is also useful because it explicitly stores two different kinds of history: low-level visual details and high-level cognitive semantics.

### 8. What are the strengths?

- Strong alignment with the actual failure modes of long-horizon manipulation.
- Clear separation between current working memory, past episodic context, and future imagination.
- Memory consolidation is simple but meaningful: merge adjacent similar entries instead of FIFO-only forgetting.
- Future imagination stays in latent feature space, avoiding full future video generation at action time.
- Ablations support the main mechanism rather than only the final benchmark number.
- The paper reports latency, which matters for real robot deployment.

### 9. What are the weaknesses, limitations, or red flags?

- The system is large and multi-component, so some gains may come from model capacity and engineering choices rather than the clean temporal decomposition alone.
- Comparisons span methods with different pretraining, data, and implementation conditions; the reported rankings should not be read as fully controlled.
- The imagination module uses a video world model adapted to each domain, which may be expensive to maintain across embodiments and task distributions.
- The real-robot evidence for MemoryVLA++ specifically is concentrated on imagination-dependent tasks, while MemoryVLA is the method reported on some other real-task categories.
- The future-imagination signal is still visual-latent, not explicit object/contact state, so fine contact, gripper state, and geometric precision may remain weak.

### 10. What challenges or open problems remain?

The biggest open question is how to make the memory and imagination inspectable enough for debugging. The model retrieves memories and imagines latent futures, but the resulting representation is still hard to audit. A stronger next version would expose object-level state, task-progress state, or contact state alongside the perceptual and cognitive tokens.

### 11. What future work naturally follows?

- Add explicit object or contact state to the memory bank.
- Train memory retrieval with task-progress supervision rather than only downstream action loss.
- Compare memory-plus-imagination against a strong raw-frame context baseline under matched compute.
- Test whether latent future imagination transfers across robots, or whether each embodiment needs separate adaptation.
- Use uncertainty or disagreement in imagined futures to decide when to replan or request more observation.

### 12. Why does this matter for cabbageland?

Because it is a concrete architecture for temporal state in a VLA. It says a robot policy should not pretend the current frame is enough. It should have a working memory, a long-term interaction memory, and a compact future-imagination path, each with a different job.

### 13. What ideas are steal-worthy?

- Store perceptual and cognitive memories separately instead of one generic history embedding.
- Use redundancy-aware consolidation rather than naive FIFO memory when interaction histories are long and slow-moving.
- Treat future imagination as partially denoised latent features, not decoded future frames.
- Fuse imagined future cues under memory guidance so the future branch does not inject irrelevant visual fantasy.
- Evaluate memory and imagination on different task families, because they should help different failures.

### 14. Final decision

**Preserve as a core temporal-VLA note.** MemoryVLA++ is today's most useful paper because it makes long-horizon VLA state explicit enough to criticize, ablate, and steal from.
