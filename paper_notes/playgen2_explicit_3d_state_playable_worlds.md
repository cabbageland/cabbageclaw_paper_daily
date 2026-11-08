# PlayGen2: Learning Real-Time Playable Worlds with Explicit 3D State

## Basic info

* Title: PlayGen2: Learning Real-Time Playable Worlds with Explicit 3D State
* Authors: Jihai Zhang, Yuhan Zhou, Junyou Li, Deheng Ye, Qi Dou, Yu Cheng
* Year: 2026
* Venue / source: arXiv preprint, submitted November 5, 2026
* Link: https://arxiv.org/abs/2611.07867
* Date surfaced: 2026-11-07
* Why selected in one sentence: A learned simulator keeps persistent, editable geometry and entity state outside the diffusion renderer, making world consistency an architectural responsibility rather than a wish placed on video history.

## Quick verdict

* Highly relevant

Preserve for the state/rendering boundary and explicit memory-commit protocol, not the real-time branding. This is a genuine learned state-transition model, not merely a conventional game engine hidden behind a video generator. Its evidence remains a small Doom world with privileged structured supervision, imperfect collision behavior, and paused entities outside the active region.

**Read basis:** Full-text main methods and experiments, Appendix A state/loss/memory details, Appendix B renderer objective, and Appendix C evaluation details. The public [inference README](https://github.com/MajorDavidZhang/PlayGen-2) was checked; code was not executed and weights were not downloaded. No abstract-only fallback.

## One-paragraph overview

PlayGen2 maintains a voxel occupancy map, a separate map-availability mask, and identity-indexed player/object states. A local learned model discovers geometry and entities and advances entity states under player actions, then commits updates into global memory. A separately trained latent diffusion model renders depth/semantic projections of that state using recent RGB frames for appearance continuity. Critically, generated RGB never becomes an input to state prediction. The architecture therefore prevents a visual hallucination from directly rewriting geometry, while still permitting learned state errors. Doom experiments test long simulated rollouts, unseen layouts, and limited state-based multiplayer composition and rule interventions.

## Model definition

### Inputs

The world-state model receives a fixed-size player-centered occupancy crop, its known/unknown mask, vertical-coordinate features, actions, and four-frame identity-aligned entity/player history. Historical coordinates share the current crop origin. New entities accepted during discovery also enter the transition branch; their ground-truth current states are teacher-forced during training.

The renderer receives projected target-view semantics, quantized depth, validity masks, the preceding action, four RGB-history frames, and a noisy target latent with diffusion index.

### Outputs

Discovery predicts unknown-voxel occupancy and proposals with objectness, class, position, dimensions, and velocity. The transition branch predicts residual positions and other next-state attributes, including player orientation. The renderer predicts diffusion velocity and decodes the next 160 × 120 RGB frame through a frozen domain-trained VAE. Here diffusion velocity is a denoising parameterization, not an entity's physical velocity.

### Training objective (loss)

State training is supervised one step ahead. Unknown occupancy uses focal plus volumetric Dice loss, with a smaller BCE reconstruction term on known geometry. Player/entity attributes use L1 or phase-balanced Smooth L1 losses; objectness and classes use focal losses. Equation 12 combines these with an auxiliary heatmap objective. This is neither RL nor unsupervised dynamics discovery.

The renderer uses v-prediction MSE: for noisy latent `z_n = alpha_n z + sigma_n epsilon`, its target is `v_n = alpha_n epsilon - sigma_n z`. The final training stage mixes 50% recorded RGB history, 40% cached generated history, and 10% history dropout. An intermediate stage adds clean-latent value/gradient L1 penalties; those are disabled in the final stage.

### Architecture / parameterization

A 3D convolutional encoder supplies geometry tokens to a shared-context Transformer, followed by discovery and transition Transformers with separate queries/heads. The renderer is an eight-block latent diffusion Transformer cross-attending separately to scene-condition and RGB-history tokens. Reported sizes are 41.2M state-model parameters, 29.1M renderer parameters, and a separate frozen 55.3M VAE. State transitions are deterministic given their inputs.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Pixel-recurrent playable worlds conflate persistent geometry, entity dynamics, and appearance. Turning away can destroy information that must survive for revisits and interactions; appearance errors can compound into world errors.

### 2. What is the method?

Use explicit state `S = (occupancy, availability, player, entity table)`. First complete/discover the region at the already committed player pose. Commit new geometry only where availability says unknown. Then predict next entity/player states, reusing the original context without re-encoding the completed map. Project the next state and render RGB. Store off-crop entities as dormant records and resume them when they re-enter.

The ordering matters: current-region writeback is not indexed by a same-step predicted pose, avoiding geometry/coordinate misalignment. Empty-but-known voxels are retained too; unknown is not treated as empty.

### 3. What is the method motivation?

Traditional game engines distinguish world state from the camera image. Learning state transitions within a comparable explicit interface provides a controllable model while leaving appearance generation separate. Local computation bounds per-step neural cost; persistent memory preserves previously committed content.

### 4. What data does it use?

Approximately 500 hours of rule-controller gameplay on Freedoom2 MAP01, roughly 500 GB, including engine geometry, entity identities/states, actions, and RGB. Models are trained from scratch with a reported budget of about 288 A100 GPU-hours. This supervision is much richer than ordinary gameplay videos.

### 5. How is it evaluated?

Seen-map evaluation and seven unseen Scythe maps; global-map versus local-neighborhood initialization; 64 ten-simulated-minute exploration trajectories per familiarity/initialization combination. Contact error counts severe penetration at resolved encounters. RGB action accuracy measures whether generated frames express commands. Global-map rendering has pose-aligned engine references; local generation instead uses unpaired distribution metrics. Additional tests cover monster pursuit, multiplayer visibility, and laptop performance.

### 6. What are the main results?

- At ten simulated minutes, contact error is 5.2–6.8% across settings and action accuracy 82.1–85.6%.
- On the seen map at five minutes, LPIPS is 0.42 versus PlayGen's 0.69; FVD is 1298.3 versus 2386.9. These are not supervision-matched comparisons.
- Monster pursuit succeeds in 55% of trials within 200 steps; selected figure examples use a different, longer budget.
- Multiplayer opponent-presence accuracy is 96.3%; the MultiGen comparison is quoted from that paper, not a shared rerun.
- Section 4.4 reports 4.98 FPS / 200.6 ms serial backend latency on M4 Pro. Overlap gives 7.16 FPS with 275.7 ms latency. The abstract's approximately 160 ms should not be repeated as the measured configuration.

### 7. What is actually novel?

The useful combination is learned geometry completion, identity-based entity discovery, and learned transitions sharing a persistent 3D interface while remaining independent of rendered-image feedback. Separation of simulation and rendering itself is prior art; the paper discusses explicit-state and code-driven predecessors. The advance is not merely “we used memory.”

### 8. What are the strengths?

The causal boundary is inspectable. No runtime collision correction supplies the learned motion, so collision tests reveal model error rather than silently repairing it. Writeback and entity identities enable genuine interventions and revisits. Structured rollouts support measurements beyond video quality. Public inference code and an explicit weight-download path improve reviewability, though this run did not reproduce them.

### 9. What are the weaknesses, limitations, or red flags?

- Outside-crop entities are retained but frozen. Persistence is not continuous global simulation.
- Geometry is static and effectively write-once; completion mistakes can become permanent. The demo README says doors are not simulated opening/closing and six doorways are permanently opened in its scene occupancy.
- Full-map initialization supplies geometry; unseen layouts still render in the learned Freedoom appearance rather than acquiring native textures.
- Local FID/FVD cannot establish topological correctness. Some visual clips near failures/recovery are excluded, although failures remain in contact error.
- Pixel-only PlayGen receives less structural information, and paired visual scores include trajectory divergence. This does not isolate architecture from supervision.
- Low resolution, one training map, deterministic state transitions, and nontrivial penetration/pursuit errors limit broad simulator claims. Multiplayer maps another player into a monster representation; it is not arbitrary multi-agent composition.

### 10. What challenges or open problems remain?

Correct off-crop time evolution, dynamic geometry, uncertainty over unseen layouts, reversible memory updates, richer entity interactions, and scalable supervision without engine access. Longer deployment may preserve the wrong world very consistently.

### 11. What future work naturally follows?

Ablate the memory/render boundary under matched structured supervision. Test deliberate revisits, entity exits/re-entry after long delays, adversarial state edits, and conflicting geometry evidence. Compare write-once memory with confidence-tagged revisions and event-driven updates for dormant entities.

### 12. Why does this matter for cabbageland?

It offers an explicit-state world-model design whose commitments can be named and tested: geometry availability, entity identity, update ordering, and a one-way observation interface. It also supplies a clean counterexample to the idea that external memory automatically yields a globally coherent dynamical world.

### 13. What ideas are steal-worthy?

1. Make observation synthesis a downstream consumer, not the authority over physical state.
2. Separate “unknown” from “known empty”; treat memory writes as explicit operations.
3. Commit discovery in the coordinate frame that generated it before advancing the observer.
4. Stress-test off-screen activity separately from persistent storage.
5. Report latency and throughput separately, and simulated horizon separately from wall time.

### 14. Final decision

Preserve as a highly relevant architecture and evaluation reference. Borrow the explicit state/render boundary and memory-commit protocol. Do not borrow its real-time headline, privileged-supervision comparisons, or frozen off-crop dynamics as evidence of a general-purpose simulator.
