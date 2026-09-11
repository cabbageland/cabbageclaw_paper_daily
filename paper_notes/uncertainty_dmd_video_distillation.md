# Uncertainty DMD: Restoring Diversity in Few-Step Autoregressive Video Distillation

## Basic info

* Title: Uncertainty DMD: Restoring Diversity in Few-Step Autoregressive Video Distillation
* Authors: Zixuan Duan, Xunzhi Xiang, Yabo Chen, Xin Zhang, Changhan Liu, Haibin Huang, Chi Zhang, Qi Fan, Xuelong Li
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2609.11265
* Date surfaced: 2026-09-11
* Why selected in one sentence: It identifies autoregressive cache collapse as the state carrier behind diversity loss in few-step video distillation.

## Quick verdict

* Highly relevant

I inspected the full arXiv HTML text, including the DMD collapse diagnosis, variance decomposition, cache transplantation, teacher/student sampler swap, timestep perturbation, stochastic cache writing, quantitative tables, and ablations. This is worth preserving because it explains why diversity collapses in autoregressive video distillation and perturbs the exact state variables that carry the collapse.

## One-paragraph overview

Uncertainty DMD studies few-step autoregressive video generators distilled with Distribution Matching Distillation. DMD is mode-seeking, so a student can map different noise samples to similar first video chunks. In autoregressive generation, that first chunk is written into a deterministic history cache, which then conditions every later chunk. The paper shows that later diversity is dominated by cache-inherited variation, so once the first cache collapses, later denoising steps have little ability to recover high-level variation. The proposed fix is structured uncertainty injection: perturb the first-chunk timestep condition and stochastically perturb clean chunk predictions before cache insertion. The same rules are used during training and inference, with a curriculum during training.

## Model definition

### Inputs
Inputs are text prompts, random noise seeds, autoregressive video chunks, denoising timesteps, and the historical AR cache. The method is tested on Causal Forcing and Self Forcing frameworks built on Wan2.1-T2V-1.3B, with additional generalization to frame-wise and chunk-wise settings.

### Outputs
The model outputs autoregressively generated video chunks. The goal is to preserve per-prompt sample diversity and motion dynamics while retaining comparable visual quality.

### Training objective (loss)
The base training uses the standard DMD objective, a reverse-KL-style distribution matching objective against a multi-step teacher. Uncertainty DMD does not replace the DMD loss; it changes the rollout states seen by that loss by perturbing first-chunk timestep conditioning and stochastic cache writing.

### Architecture / parameterization
The method is an add-on to DMD-distilled autoregressive video diffusion systems. Module A perturbs the first denoising timestep while keeping the latent unchanged. Module B perturbs the predicted clean chunk once before inserting it into the cache. A curriculum increases perturbation probabilities over training, and inference uses the final perturbation probabilities.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Few-step DMD makes video generation faster, but it can collapse diversity: different noise seeds under the same prompt produce very similar videos with weaker motion. In autoregressive video, that collapse is amplified because early chunks become cache state for later chunks.

### 2. What is the method?
The method injects uncertainty into two structured AR state variables. It perturbs the first-chunk timestep condition to diversify the root of the rollout, and it stochastically perturbs chunks before cache insertion so later chunks inherit more varied histories.

### 3. What is the method motivation?
The paper's key diagnostic is that later chunks mostly inherit diversity from the cache. Perturbing arbitrary latents downstream is less useful if the first cache already collapsed. The method therefore targets the root timestep and cache write, not generic noise injection.

### 4. What data does it use?
The experiments sample 100 text prompts from VBench and generate 20 videos per prompt with shared random seeds, producing 2,000 videos per method. Training uses text prompts from VidProM and the Wan-based Causal Forcing and Self Forcing setups.

### 5. How is it evaluated?
The paper evaluates diversity with TE-CLIP, TE-Inception, TE-DINO, VENDI-CLIP, VENDI-Inception, and VENDI-DINO, plus VBench quality metrics such as subject consistency, background consistency, motion smoothness, dynamic degree, aesthetic quality, and imaging quality. It also includes ablations and a user study.

### 6. What are the main results?
On Causal Forcing, DMD + Ours improves TE-CLIP from 19.8 to 22.1, TE-DINO from 69.3 to 71.9, VENDI-DINO from 3.6 to 4.7, and dynamic degree from 31.1 to 41.8 while keeping quality comparable. On Self Forcing, DMD + Ours improves TE-CLIP from 16.4 to 19.5, VENDI-DINO from 2.6 to 3.3, and dynamic degree from 25.1 to 42.4. The ablation shows timestep perturbation is crucial: removing it drops TE-CLIP from 19.5 to 16.7 and VENDI-DINO from 3.3 to 2.6.

### 7. What is actually novel?
The novelty is the diagnosis of structured uncertainty collapse in AR video distillation and the targeted perturbation of root timestep and cache state. This is more specific than "add noise for diversity."

### 8. What are the strengths?
The paper does a good job locating the bottleneck. Variance decomposition, cache transplantation, and sampler swapping all support the claim that first-chunk cache collapse drives later diversity loss. The fix is lightweight and does not require architectural changes.

### 9. What are the weaknesses, limitations, or red flags?
The metrics are still diversity and video-quality proxies. The paper does not prove that restored variation corresponds to better semantic coverage, controllability, factuality, or downstream utility. The method also relies on a careful perturbation schedule; too much or poorly placed uncertainty could easily damage coherence.

### 10. What challenges or open problems remain?
The next problems are semantic diversity, prompt-faithful diversity, long-horizon consistency, uncertainty calibration, and deciding when a rollout should be diverse versus stable. Another open question is how this interacts with explicit control signals, camera constraints, or physical simulation.

### 11. What future work naturally follows?
Combine structured uncertainty with semantic coverage metrics, prompt-conditioned diversity objectives, uncertainty-aware ranking, and cache diagnostics for long video generation. Test the method on action-conditioned world models and video planning systems.

### 12. Why does this matter for cabbageland?
Cabbageland should care because the paper identifies the cache as the state carrier. If the carrier collapses, the rest of the system inherits that collapse. That lesson transfers to memory, planning, and any autoregressive system with persistent state.

### 13. What ideas are steal-worthy?
Decompose later variation into innovation versus inherited state. Test state-carrier causality by transplantation. Perturb the earliest carrier of diversity instead of adding generic downstream noise. Use the same stochastic state rule during training and inference.

### 14. Final decision
Keep as a highly relevant preserved note. The method is narrow, but the diagnosis is exactly the kind of mechanism-level generative insight worth retaining.
