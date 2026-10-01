# LOCI: Spatial Linear Memory for Streaming World Models

## Basic info

* Title: LOCI: Spatial Linear Memory for Streaming World Models
* Authors: Ji Xia, Tingting Liao, Xuezhi Liang, Hao Li, Guangyi Liu
* Year: 2026
* Venue / source: arXiv:2609.40222
* Link: https://arxiv.org/abs/2609.40222
* Date surfaced: 2026-10-01
* Why selected in one sentence: It gives streaming video world models a hybrid memory that combines compact recurrent scene state with explicit retained visual evidence.

## Quick verdict

* Must read

This is one of the cleaner world-model memory mechanisms in the batch. The paper is strongest where it refuses the false choice between unbounded key-value history and lossy recurrent compression. The evidence is still relative rather than absolute, but the architecture is directly useful for thinking about persistent state in camera-controlled world models.

## One-paragraph overview

LOCI targets a specific failure mode in long video world models: when a camera revisits a previously seen place, the model often invents a new scene because the relevant observation is no longer in recent context. LOCI modifies a Wan 5B video transformer so half of its blocks keep explicit historical softmax attention, while half use a recurrent linear-attention memory conditioned on projective camera geometry. The recurrent state accumulates compact spatial context, and its readout changes the feature stream that later historical-attention blocks use to query retained key-value evidence. This lets bounded recurrent memory guide retrieval from detailed stored observations. On MIND and held-out rendered trajectories, LOCI improves revisit fidelity over external world models and over a same-recipe full-softmax baseline under identical retained-history budgets.

## Model definition

### Inputs

The model takes an initial conditioning video latent, generated video chunks, camera poses, camera intrinsics, and optional retained historical observations. Each generated chunk contains five latent frames.

### Outputs

The model generates future video latents for a camera-controlled trajectory. The desired behavior is faithful continuation and faithful reconstruction of previously observed regions when the camera returns to them.

### Training objective (loss)

The paper uses chunk-wise diffusion forcing on a Wan2.2-TI2V-5B backbone. The full training loss is the video diffusion objective used for the chunk-causal generation recipe; LOCI changes the memory and attention architecture rather than introducing a separate explicit reconstruction loss for revisits.

### Architecture / parameterization

LOCI adapts a 30-block Wan video transformer. Fifteen blocks use intra-chunk softmax attention plus recurrent Kimi Delta Attention, and fifteen blocks retain historical softmax attention. The recurrent branch uses PRoPE-style projective camera conditioning for queries, keys, and values. The recurrent readout is gated into the token features, which then form queries in later historical-attention blocks. The recurrent branch adds about 90.7M parameters, roughly 1.7% of the 5.38B model.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Streaming video world models need to remember visual evidence that is spatially relevant but not temporally recent. Full KV attention preserves individual observations but grows with sequence length. Pure recurrent memory stays bounded but can discard or smear scene-specific details.

### 2. What is the method?

Use a hybrid memory architecture. A camera-conditioned recurrent state integrates full-history context at fixed size, while retained KV entries keep direct observation-level evidence. The recurrent readout changes the current token features, and those features later query retained historical KV.

### 3. What is the method motivation?

A revisit is a spatial retrieval problem, not a simple next-frame problem. Camera geometry tells the model which old surfaces might matter, and explicit retained evidence gives the model details that a compressed state alone might lose.

### 4. What data does it use?

Training uses rendered Unreal Engine and CARLA scenes, about 98 hours, plus real walking videos from Sekai. The model is not trained on MIND. It is evaluated on MIND and on held-out recorded Unreal Engine trajectories.

### 5. How is it evaluated?

The paper evaluates MIND memory segments, WBench-style camera-return consistency, and held-out rendered trajectories with ground truth. Metrics include MSE, PSNR, SSIM, and LPIPS. A revisit is defined by pose proximity to a prior view after a time gap and after looking away.

### 6. What are the main results?

On MIND, LOCI reaches 0.0455 MSE, 14.36 PSNR, 0.464 SSIM, and 0.643 LPIPS, the best MSE/PSNR/SSIM among the external world models run on all segments. In the controlled comparison, bounded-history LOCI improves PSNR by 0.89 dB over a same-recipe full-softmax model and is better in 44 of 50 segments. With full history, it also completes long segments on which full softmax runs out of GPU memory.

### 7. What is actually novel?

The novelty is the coupling between projectively conditioned recurrent memory and explicit historical KV. The recurrent memory is not merely an extra summary; it shapes the features used to query retained observations.

### 8. What are the strengths?

The problem is precise, the architecture matches the problem, and the same-backbone ablation is unusually useful. The method also handles bounded streaming more plausibly than a pure cache.

### 9. What are the weaknesses, limitations, or red flags?

Absolute video fidelity remains low, with benchmark-average PSNR below 15 dB. The held-out trajectories are rendered rather than real-world captures. The study uses one 5B backbone with a short 5,000-update fine-tuning budget, and the camera-attention branch still keeps explicit history in all blocks.

### 10. What challenges or open problems remain?

Real-world revisit fidelity, longer interactive rollouts, stronger geometry errors, dynamic objects, and memory under incorrect camera estimates remain open. The method also needs evidence under richer embodied tasks, not only recorded camera trajectories.

### 11. What future work naturally follows?

Apply the hybrid memory pattern to world-action models, navigation systems, and agents that need addressable persistent spatial state. A natural follow-up is to connect the memory entries to explicit maps or object-centric state.

### 12. Why does this matter for cabbageland?

Cabbageland wants world models whose state remains usable over time. LOCI gives a concrete pattern: keep compact context for long horizon continuity, but keep direct evidence for details that must be retrieved later.

### 13. What ideas are steal-worthy?

Use camera geometry as a memory address. Let recurrent state modify the query into explicit evidence, rather than expecting a compressed state to hold all details. Evaluate memory by revisits after looking away, not only by local continuation quality.

### 14. Final decision

Preserve. This is the strongest paper of the day for persistent world-model state.

