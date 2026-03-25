# MemoryVLA: Perceptual-Cognitive Memory in Vision-Language-Action Models for Robotic Manipulation

## Basic info

* Title: MemoryVLA: Perceptual-Cognitive Memory in Vision-Language-Action Models for Robotic Manipulation
* Authors: Hao Shi, Bin Xie, Yingfei Liu, Lin Sun, Fengrong Liu, Tiancai Wang, Erjin Zhou, Haoqiang Fan, Xiangyu Zhang, Gao Huang
* Year: 2026
* Venue / source: ICLR 2026 / arXiv
* Link: https://arxiv.org/abs/2508.19236
* Date surfaced: 2026-03-25
* Why selected in one sentence: It is a strong recent example of a VLA paper that gives memory explicit storage, retrieval, fusion, and consolidation semantics instead of just extending temporal context.

## Quick verdict

**Highly relevant**

This is one of the better recent VLA memory papers because it at least specifies the memory object and its update path. The key move is to separate perceptual detail from cognitive summary, retrieve both from a long-horizon bank, fuse them with current working memory, and let a diffusion policy act on the result. I inspected the abstract and substantial method text, but I did not verify every benchmark protocol or appendix detail, so I trust the mechanism read more than every reported number.

## One-paragraph overview

MemoryVLA tries to fix a real VLA weakness: many manipulation tasks are non-Markovian, yet mainstream VLA policies still behave like frame-conditioned reactors. The paper proposes a dual-memory design where the current observation and instruction produce a short-term working memory made of perceptual tokens and a cognitive token, while a Perceptual-Cognitive Memory Bank stores older perceptual details and semantic summaries over time. At each step, the current tokens query this bank, retrieve relevant history, fuse it through learned gates, and then condition a diffusion action expert to produce multi-step actions. The useful part is not the neuroscience metaphor; it is the typed memory interface.

## Model definition

### Inputs
Current RGB observation from a third-person view, a language instruction, and the current contents of the Perceptual-Cognitive Memory Bank built from previous timesteps. The working-memory side uses perceptual visual tokens plus a compact cognitive token derived from the VLM/LLM stack.

### Outputs
A sequence of future 7-DoF robot actions, where each action contains relative translation, relative rotation, and binary gripper state. Internally, the model also emits retrieved and fused perceptual/cognitive memory representations used to condition action generation.

### Training objective (loss)
From the accessible method text, the action expert is trained with mean squared error between predicted and target actions in the diffusion denoising process. The retrieval, gating, and memory-bank components are trained jointly as part of the end-to-end imitation objective. I did not inspect appendix-level details for all auxiliary terms or optimization hyperparameters.

### Architecture / parameterization
A 7B Prismatic-style VLM with DINOv2 and SigLIP visual encoders plus an LLaMA-7B language backbone produces perceptual and cognitive tokens. A Perceptual-Cognitive Memory Bank stores separate perceptual and cognitive streams, uses attention-based retrieval with temporal positional encodings, learned gate fusion, and similarity-based consolidation. A diffusion transformer / DiT-style action head with DDIM-style denoising predicts continuous robot action sequences.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
VLA policies often ignore temporal dependency and fail on long-horizon manipulation tasks where current observations do not reveal prior task progress or earlier world state. The paper aims to give VLAs within-episode memory that preserves both semantic and perceptual history.

### 2. What is the method?
- Encode the current RGB observation and instruction into perceptual tokens and a cognitive token.
- Treat those as short-term working memory.
- Store previous perceptual and cognitive representations in a Perceptual-Cognitive Memory Bank.
- Retrieve relevant history through attention using current tokens as queries and temporal positional encodings over memory entries.
- Fuse retrieved and current representations with learned gates.
- Consolidate memory by merging temporally adjacent, semantically similar entries when capacity is exceeded.
- Condition a diffusion action expert on the fused tokens to predict a sequence of future actions.

### 3. What is the method motivation?
The motivation is sound: manipulation is often non-Markovian, and simply stacking a few frames does not create durable task memory. The paper argues that low-level perceptual detail and high-level semantic abstraction should not be collapsed into one undifferentiated context buffer.

### 4. What data does it use?
From the accessible text, the paper evaluates on SimplerEnv-Bridge, Fractal, LIBERO-5, Mikasa-Robo, and 12 real-world tasks across Franka and WidowX robots. It claims 150+ tasks and 500+ variations across simulation and real-world settings.

### 5. How is it evaluated?
It compares against VLA baselines such as CogACT and pi-0 on simulated and real-world robotic manipulation suites, including long-horizon temporal tasks and out-of-distribution conditions. The accessible text also emphasizes robustness under changes in backgrounds, distractors, lighting, containers, and occlusion.

### 6. What are the main results?
From the accessible text, MemoryVLA reports 71.9% on SimplerEnv-Bridge, 72.7% on Fractal, 96.5% on LIBERO-5, 41.2% on Mikasa-Robo, and 84–85% on the real-world task sets, with sizable gains over CogACT and pi-0 on several benchmarks. I did not independently verify the full evaluation setup or statistical reliability of those gains.

### 7. What is actually novel?
The real novelty is not “memory for VLAs” in the abstract. It is the typed split between perceptual and cognitive memory, with explicit retrieval, gate-based fusion, and consolidation inside a VLA-to-diffusion-action pipeline. That is more concrete than the usual recurrence or prompt-history story.

### 8. What are the strengths?
- It defines the memory object more clearly than many VLA papers.
- It distinguishes low-level perceptual history from high-level semantic summary.
- Retrieval and consolidation are explicit enough to inspect and critique.
- The action interface remains continuous and control-oriented rather than purely language-autoregressive.
- It is directly relevant to long-horizon manipulation rather than only table-top imitation.

### 9. What are the weaknesses, limitations, or red flags?
- The cognitive-science framing is heavier than necessary and risks overstating biological grounding.
- Similarity-based consolidation by merging adjacent entries is simple and may discard rare but important events.
- The memory is still learned latent state, not a causal or symbolic world model.
- It is not yet clear from the accessible text how robust the retrieval scheme is under severe distribution shift or very long horizons.
- Benchmark gains alone do not prove the retrieved memory is semantically correct; they prove usefulness, not interpretability.

### 10. What challenges or open problems remain?
How to maintain memory without deleting low-frequency but crucial events, how to expose or edit the memory state for intervention, how to unify typed memory with explicit object/state structure, and how to handle longer real-world temporal dependencies remain open.

### 11. What future work naturally follows?
- Add uncertainty estimates or confidence-aware retrieval.
- Replace or augment latent memory entries with more explicit object- or state-centric structure.
- Study editability and debugging of stored memory.
- Test whether typed memory helps planning and counterfactual reasoning, not just reactive control.

### 12. Why does this matter for cabbageland?
Because it is a serious attempt at typed memory in embodied control rather than another “more tokens equals more reasoning” paper. The details are still neural and approximate, but the decomposition is real enough to steal from.

### 13. What ideas are steal-worthy?
- Separate perceptual-detail memory from semantic-summary memory.
- Use explicit retrieval and fusion rather than undifferentiated temporal context.
- Treat memory update and consolidation as first-class mechanisms.
- Condition action generation on memory-augmented state instead of hoping recurrence handles everything implicitly.

### 14. Final decision
**Worth preserving and likely worth a deeper read.** The memory design is specific enough to influence future architecture thinking, even if the cognitive-science dressing can be ignored.
