# CLaD: Planning with Grounded Foresight via Cross-Modal Latent Dynamics

## Basic info

* Title: CLaD: Planning with Grounded Foresight via Cross-Modal Latent Dynamics
* Authors: Andrew Jeong, Dinesh Jayaraman, Yuke Zhu
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2603.29409
* Date surfaced: 2026-04-06
* Why selected in one sentence: It reframes cross-modal alignment around transitions rather than static states, which is one of the more interesting recent instincts in latent robot planning.

## Quick verdict

**Useful**

This paper has a real idea in it, but I trust the framing more than the full stack. Modeling semantic and proprioceptive transitions jointly is smarter than aligning static embeddings, and grounding latent foresight with EMA targets plus reconstruction is a sensible anti-collapse recipe. Still, the paper feels more fragile than DIAL or HWM because more of the contribution lives in a bundle of latent-learning choices that are harder to disentangle. I inspected the abstract and substantial HTML text, but not the full appendix.

## One-paragraph overview

CLaD argues that robotic planning should model how semantic scene state and proprioceptive state co-evolve under action, rather than plan in a generic latent space or generate expensive semantic artifacts like text or images. It builds transition embeddings for each modality, uses asymmetric cross-attention so proprioceptive transitions query semantic transitions, pools the result into a shared dynamics representation, and predicts future latent states for both modalities from that dynamics code. Those predicted latent foresights are then modulated with current observations to condition a diffusion policy. The paper’s best move is the transition-centric framing. The rest of the stack is decent but less obviously inevitable.

## Model definition

### Inputs
Current and past proprioceptive states, semantic states derived from vision-language features, and recent action sequences. Language is incorporated into the semantic state through FiLM-style conditioning on a frozen pretrained VLM representation.

### Outputs
Predicted future latent foresights for semantic and proprioceptive modalities, plus action sequences from the downstream diffusion policy.

### Training objective (loss)
From the accessible text, Stage 1 uses self-supervised latent prediction losses against EMA target encoders for future semantic and proprioceptive states, along with auxiliary reconstruction losses back to observable proprioceptive and visual-semantic quantities. Stage 2 trains a diffusion policy conditioned on the predicted foresight.

### Architecture / parameterization
A two-stage framework with modality-specific transition encoders, asymmetric cross-attention for shared cross-modal dynamics, lightweight MLP predictors for future latent foresights, EMA target encoders, reconstruction heads, and a diffusion policy that consumes observation-modulated foresight.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Many robot planners either reason semantically by generating explicit artifacts like text or images, which is slow, or they plan in latent space without any real mechanism ensuring semantic and kinematic consistency. The paper tries to make latent foresight more grounded by tying semantic and proprioceptive transitions together.

### 2. What is the method?
- Encode semantic and proprioceptive states separately.
- Build transition embeddings for each modality from past state, current state, and action history.
- Use asymmetric cross-attention in which proprioceptive transitions query semantic transitions.
- Pool the result into a shared cross-modal dynamics representation.
- Predict future latent foresights for both modalities from that shared dynamics code.
- Train the predictors with EMA target encoders and auxiliary reconstruction losses.
- Feed the predicted foresight, after observation-conditioned modulation, into a diffusion policy for control.

### 3. What is the method motivation?
The motivation is that actions couple how the robot moves and how the scene changes, so cross-modal consistency should be enforced over transitions rather than just states. That is the strongest conceptual claim in the paper, and it is a good one.

### 4. What data does it use?
From the visible text, the main benchmark is LIBERO-LONG. I did not inspect the appendix, so I cannot say much more about training data scale or collection procedure than what the accessible HTML revealed.

### 5. How is it evaluated?
It is evaluated on long-horizon robot manipulation via LIBERO-LONG and compared against strong VLA baselines as well as planning methods that reason in semantic or latent space. The paper also studies design variants of the cross-attention structure.

### 6. What are the main results?
The paper reports a 94.7% success rate on LIBERO-LONG and claims competitiveness with substantially larger VLAs despite using far fewer parameters. I did not verify the full ablation tables or all baseline settings, so these should be read as paper-reported results.

### 7. What is actually novel?
The most novel part is the shift from static cross-modal alignment to transition-level cross-modal dynamics. The asymmetry — proprioceptive transitions querying semantic transitions — is also specific enough to count as a real design choice rather than generic fusion.

### 8. What are the strengths?
- The transition-centric framing is genuinely stronger than static alignment.
- Grounding foresight with both EMA targets and reconstruction losses is a sensible combination.
- The method avoids expensive explicit semantic generation at planning time.
- The architecture is compact relative to giant VLAs.
- The paper seems to care about physically coherent cross-modal evolution, which is the right target.

### 9. What are the weaknesses, limitations, or red flags?
- The contribution is distributed across several interacting latent-learning choices, which makes it harder to isolate what really matters.
- “Grounded” is only partly earned here; the foresight is still latent and only indirectly tied to observables.
- The asymmetric cross-attention story is plausible, but I am not yet convinced it is universally the right asymmetry.
- The overall pipeline may be more brittle than the paper’s clean framing suggests.
- I did not inspect appendix-level ablations, so confidence about robustness is limited.

### 10. What challenges or open problems remain?
How to verify that latent foresight remains causally faithful rather than merely benchmark-useful remains open. More broadly, we still need better ways to make cross-modal planning structure explicit and inspectable rather than just statistically aligned.

### 11. What future work naturally follows?
- Add explicit uncertainty or verification around the predicted foresight.
- Test alternative directionalities or graph structures for cross-modal interaction.
- Replace dense latent semantics with more object-structured or spatially explicit state.
- Study whether transition-level cross-modal modeling helps beyond manipulation benchmarks.

### 12. Why does this matter for cabbageland?
Because it points at a better place to impose structure. If semantics and kinematics are coupled by action, then enforcing that coupling over transitions is a cleaner research instinct than simply aligning static embeddings and calling it grounding.

### 13. What ideas are steal-worthy?
- Model cross-modal consistency over transitions, not only states.
- Predict future subgoal-like latent states from a shared dynamics representation.
- Use EMA targets plus reconstruction to keep latent foresight from drifting into pure mush.
- Keep planning in compact latent space while still preserving some modality structure.

### 14. Final decision
**Worth preserving as adjacent inspiration, but with moderate confidence rather than full conviction.** The transition-level idea is strong. I am just less certain the rest of the recipe is the final form.

## Key figures from HTML

### Figure 2
ArXiv HTML caption summary: two-stage CLaD architecture. Stage 1 builds semantic and proprioceptive transition embeddings, fuses them through asymmetric cross-attention, predicts future modality latents with EMA targets and auxiliary reconstruction, and Stage 2 uses the predicted foresight to condition a diffusion policy.
