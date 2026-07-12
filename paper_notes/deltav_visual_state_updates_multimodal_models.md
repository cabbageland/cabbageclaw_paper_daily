# DeltaV: Thinking with Visual State Updates in Unified Large Multimodal Models

## Basic info

* Title: DeltaV: Thinking with Visual State Updates in Unified Large Multimodal Models
* Authors: Pengjie Wang, Linger Deng, Zujia Zhang, Shaojie Zhang, Zhenbo Luo, Pei Fu, Jian Luan, Xiang Bai, Yuliang Liu
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.08434
* Date surfaced: 2026-07-12
* Why selected in one sentence: It replaces full intermediate image generation with compact visual state updates, which is a cleaner interface for multimodal reasoning.

## Quick verdict

**Highly relevant**

This is a good multimodal reasoning paper because it identifies a concrete inefficiency instead of just scaling interleaved image generation harder. The model spends tokens on what changed, not on redrawing what stayed the same. I inspected the full arXiv HTML paper, including the method, TSIM Router design, StructCoT dataset framing, reconstruction analysis, reasoning results, and ablations.

## One-paragraph overview

DeltaV starts from a straightforward complaint about unified large multimodal models: when they generate intermediate visual states during reasoning, they usually generate full images, which wastes tokens on unchanged content and weakens supervision on the small visual changes that actually matter. The proposed fix is to model visual updates instead. Conditioned on earlier visual states, DeltaV predicts compact update tokens for the changed region or content, and a TSIM Router decides how many tokens to allocate by stopping when extra reconstruction gain becomes marginal. The paper also introduces StructCoT, a 1.05 million sample dataset spanning 44 task domains, to train interleaved multimodal reasoning with these update states.

## Model definition

### Inputs
The model consumes interleaved multimodal reasoning context, including prior textual reasoning and historical visual states.

### Outputs
Instead of generating a full next image at each step, it generates compact visual update tokens plus the textual reasoning outputs required by the task.

### Training objective (loss)
The training objective is unified autoregressive modeling over multimodal sequences, but with visual-update tokenization in place of full-image intermediate generation.

### Architecture / parameterization
The key pieces are the visual-update representation module and the TSIM Router. The router allocates token budget according to temporal similarity and stops adding tokens when marginal reconstruction gain falls below a threshold.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to make interleaved multimodal reasoning less wasteful and more reasoning-relevant. Full-image intermediate generation burns tokens on static content and can even hurt reasoning quality.

### 2. What is the method?
The method is to represent intermediate visual reasoning steps as updates to the previous visual state, not as complete new images. DeltaV predicts update tokens and uses the TSIM Router to decide how many are worth allocating.

### 3. What is the method motivation?
If most of the scene is unchanged from one reasoning step to the next, then regenerating the entire scene is redundant supervision. The useful signal lives in the changed part.

### 4. What data does it use?
The paper introduces StructCoT, a large interleaved multimodal reasoning dataset with 1.05 million samples across 44 task domains, and also uses broader multimodal training data for the DeltaV-2B model.

### 5. How is it evaluated?
The paper evaluates reconstruction efficiency, Zebra-CoT interleaved reasoning, in-domain multimodal reasoning, external multimodal understanding / reasoning benchmarks, and internal component ablations for token routing and allocation.

### 6. What are the main results?
TSIM-Router-driven visual updates reduce newly generated visual tokens by 55.6% on average while preserving reconstruction quality. On multimodal reasoning, routed visual updates improve overall score by 3.3 points over full-image modeling while using only 64 visual update tokens on average. DeltaV-2B also beats substantially larger open-source models on the paper's in-domain evaluations and surpasses Qwen3-VL-2B by 5.9 points on external multimodal reasoning and understanding benchmarks.

### 7. What is actually novel?
The novelty is the visual-update interface plus the token-allocation rule. The paper is not just compressing images; it is claiming that the right computational object for many reasoning steps is the state delta.

### 8. What are the strengths?
The paper includes a clean negative result: naive full-image intermediate generation can perform worse than text-only reasoning. That strengthens the case that the improvement is not simply "more visuals are better," but specifically that change-focused visual supervision is better.

### 9. What are the weaknesses, limitations, or red flags?
The strongest evidence sits inside the authors' StructCoT training setup. Routed updates do not beat text-only reasoning on every subtask, especially some 2D reasoning cases where local detail still needs more token budget. The method also remains image-generation flavored rather than giving a more explicit symbolic or geometric world state.

### 10. What challenges or open problems remain?
A major next question is when visual deltas are enough and when the model really needs a richer explicit state representation. Another open problem is extending the same idea to video, 3D, or tool-conditioned state updates.

### 11. What future work naturally follows?
It would be useful to compare visual updates against object-level or slot-level state updates, test the method in agentic tool loops, and see whether delta modeling helps robustness rather than only efficiency and benchmark accuracy.

### 12. Why does this matter for cabbageland?
Cabbageland cares about explicit state, multimodal reasoning, and avoiding mushy redundant computation. DeltaV offers a concrete example of replacing "repaint the world" with "update the part that changed."

### 13. What ideas are steal-worthy?
Model the delta, not the whole scene. Use a learned or derived stop rule for token allocation. Check whether intermediate modality generation is actually helping instead of assuming it does. Treat unchanged content as a compression opportunity and changed content as the supervision target.

### 14. Final decision
**Keep it.** The paper is worth preserving because the state-update interface is sharp, transferable, and more believable than generic full-image chain-of-thought.
