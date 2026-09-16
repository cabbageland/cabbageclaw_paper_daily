# SlotDiT: Object-Centric Representations for Diffusion Transformers

## Basic info

* Title: SlotDiT: Object-Centric Representations for Diffusion Transformers
* Authors: Gjergj Plepi, Sven Behnke
* Year: 2026
* Venue / source: arXiv:2609.17414
* Link: https://arxiv.org/abs/2609.17414
* Date surfaced: 2026-09-16
* Why selected in one sentence: It directly tests whether object-centric slots are a better latent space for diffusion transformers than VAE or generic feature latents in task-oriented video prediction.

## Quick verdict

* Highly relevant

This is a preserve-worthy object-centric generation paper, with the caveat that most evidence is in robotics datasets. The useful lesson is that visual fidelity metrics can favor VAE latents while object-centric slots better preserve task-relevant state for instructions and control. This note is based on the full arXiv HTML text.

## One-paragraph overview

SlotDiT is a text-guided diffusion transformer that generates future scene dynamics in slot space. A reference image is parsed into object-centric slots, language is encoded with a text encoder, and the DiT autoregressively denoises future slot trajectories. The authors compare slots against VAE-based and semantics-aligned latent spaces using a controlled DiT framework across LanguageTable-Synthetic, CLIPort, LanguageTable-Real, and BridgeData V2. SlotDiT is often not the best under pure video fidelity metrics, but it is much better at task completion and downstream robot control, suggesting that compact object-level latents retain the variables that matter for action.

## Model definition

### Inputs

SlotDiT takes a reference image, language instruction, and observed scene slots. Scenes are represented with 8 or 10 object slots of dimension 128 or 256 depending on the dataset. The text condition comes from a frozen T5-small encoder.

### Outputs

The model predicts future slot trajectories. The generated slots can be decoded into future frames or passed through inverse dynamics models to support robot control.

### Training objective (loss)

Training has two stages. First, the object-centric representation module is trained with image and feature reconstruction objectives. Second, the slot encoder is frozen and SlotDiT is trained with a diffusion denoising objective using the Diffusion Forcing Transformer framework, cosine noise schedule, v-prediction parameterization, fused min-SNR loss reweighting, and DDIM sampling at inference.

### Architecture / parameterization

The representation learner uses Slot Attention with a broadcast decoder. SlotDiT is a diffusion transformer over slot tokens, with bidirectional self-attention over slots and time, text-to-slot cross-attention, and RoPE variants that either preserve or relax slot permutation equivariance.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Most latent diffusion video models operate in pixel, VAE, or generic feature spaces. Those spaces can be visually rich but do not necessarily isolate task-relevant objects and relations. The paper asks whether object-centric slots make diffusion rollouts more useful for robotic task completion and control.

### 2. What is the method?

The method learns object slots from images, freezes that slot encoder, and trains a text-conditioned DiT to denoise future slot windows autoregressively. The same DiT architecture is compared across slot, VAE, and DINO-style representation spaces to isolate the effect of the latent.

### 3. What is the method motivation?

Robotic environments need compact state carriers for objects, relations, and motion. A visually faithful latent can waste capacity on appearance while failing to carry the object-level variables needed for planning. Slots provide an explicit decomposition that may be easier for a dynamics model to use.

### 4. What data does it use?

The paper evaluates on LanguageTable-Synthetic, CLIPort, LanguageTable-Real, and BridgeData V2. These include simulated and real tabletop manipulation tasks with language-conditioned goals.

### 5. How is it evaluated?

Video generation is evaluated with LPIPS, FVD, JEDi, and VLM-judged task success. Robot-control evaluation uses inverse dynamics models to map predicted latents to actions on LanguageTable-Synthetic and CLIPort. The paper also reports robustness to harder scene configurations and unseen instruction templates, controllability examples, efficiency, and RoPE ablations.

### 6. What are the main results?

On CLIPort text-guided video generation, SlotDiT achieves 87.8% task success versus 63.0% for TextOCVP and 57.1% for DiT + VideoVAE, even though VideoVAE has stronger visual metrics. On LanguageTable-Synthetic, SlotDiT reaches 79.7% task success versus 55.8% for VideoVAE and 25.9% for TextOCVP. On CLIPort robot control, SlotDiT reaches 73.0% success versus 50.0% for TextOCVP and 10.0% for VideoVAE. On LanguageTable-Synthetic control, SlotDiT nearly matches the GT-slot oracle in the in-distribution Block-4 setting, 74.5% versus 75.0%.

### 7. What is actually novel?

The novelty is not simply using slots, but using them as the latent space of a diffusion transformer and comparing representation spaces under a controlled DiT setup. The paper turns "object-centric is good for robotics" into a sharper latent-space question.

### 8. What are the strengths?

The controlled comparison against VAE and DINO-style latents is the core strength. The result that visual metrics and task success diverge is important and believable. The efficiency result is also useful: slots reduce the per-frame token count from 256 to 10 and generate 39 CLIPort frames at 9.33 FPS, a 5.68x speedup over DiT + SD-VAE.

### 9. What are the weaknesses, limitations, or red flags?

The robot-control evaluation is restricted to synthetic environments such as LanguageTable-Synthetic and CLIPort. Task success for video generation depends on a VLM-as-judge. Slots use a fixed number of object slots chosen before training, which can under-segment clutter or waste capacity. The compact slot space can lag high-capacity VAE latents in fine appearance detail and temporal consistency.

### 10. What challenges or open problems remain?

The main challenge is robust object-centric decomposition in more cluttered, open-world real scenes. Another is reducing error accumulation in long autoregressive rollouts and improving visual detail without giving up object-level structure.

### 11. What future work naturally follows?

Scale SlotDiT to richer instructions and more complex real scenes. Pair slots with stronger object-centric decoders. Integrate slot rollouts with planners and policies directly. Test whether learned slots remain stable under occlusion, contact, and changing camera viewpoints.

### 12. Why does this matter for cabbageland?

Cabbageland wants generative world models whose state variables are useful for planning, not just reconstruction. SlotDiT is evidence that a structured latent can lose some visual detail but preserve more decision-relevant structure.

### 13. What ideas are steal-worthy?

Compare latents by downstream task success, not only video metrics. Use a controlled architecture when testing representation spaces. Preserve permutation equivariance when the slot identities should be exchangeable, but relax it when real-world diversity needs more flexibility.

### 14. Final decision

Preserve. This is a useful structured-representation paper and a good citation for object-centric diffusion/world-model design.
