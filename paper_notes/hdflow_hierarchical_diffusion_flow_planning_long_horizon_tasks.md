# HDFlow: Hierarchical Diffusion-Flow Planning for Long-horizon Tasks

## Basic info

* Title: HDFlow: Hierarchical Diffusion-Flow Planning for Long-horizon Tasks
* Authors: Gireesh Nandiraju, Jena D. Hwang, Trista Cao, Abhinav Narayan, Yixin Zhu, and Shuran Song
* Year: 2026
* Venue / source: ICML 2026 Spotlight / arXiv
* Link: https://arxiv.org/abs/2605.04525
* Date surfaced: 2026-05-07
* Why selected in one sentence: It is a rare long-horizon planning paper that makes a defensible model-allocation choice, diffusion for exploratory subgoal generation and rectified flow for fast dense execution, instead of using the same generator everywhere.

## Quick verdict

**Highly relevant**

This is one of the cleaner recent planning papers because the hierarchy is not just decorative. The paper argues that strategic subgoal search and low-level dense trajectory generation have different computational and statistical needs, then assigns different generative models to those roles and adds explicit energy guidance at the high level. I inspected the abstract, introduction, formal preliminaries, and substantial method text from the arXiv HTML, including the world-model objective and the training setup for the hierarchical planner, but I did not audit the entire appendix or every experiment table.

## One-paragraph overview

HDFlow is a hierarchical planner that operates in the latent space of a learned world model. A high-level diffusion planner proposes a sequence of sparse subgoals, while a low-level rectified-flow planner rapidly generates dense trajectories between successive subgoals. To make the latent space more useful for long-horizon planning, the world model is trained not only to reconstruct and predict dynamics but also with a contrastive objective that pulls successful intermediate states toward goal states and an inverse-dynamics loss that keeps the representation control-relevant. The high-level planner is further steered by an energy-based model that scores strategic subgoal sequences, so the system is not relying on diffusion samples alone to discover viable plans.

## Model definition

### Inputs
The world model takes multimodal observations over time and encodes them into latent states, with the paper stating an RSSM architecture and a pretrained DINOv2-based visual encoder. The high-level planner takes latent initial state and goal-conditioned context and generates a sequence of latent subgoals. The low-level planner takes neighboring latent subgoals and produces dense latent trajectories between them.

### Outputs
The world model outputs latent states, reconstructed observations, and predicted future latent states. The high-level planner outputs sparse latent subgoal sequences. The low-level rectified-flow planner outputs dense latent trajectories connecting those subgoals, which are then used for action selection through the planning stack.

### Training objective (loss)
The inspected text gives concrete losses for the world-model stage. The RSSM-style world model is trained with observation reconstruction plus KL regularization between posterior and prior latent state distributions. It is augmented with a contrastive InfoNCE-style loss that pulls successful intermediate states toward final goal representations and pushes them away from failed-trajectory states, plus an inverse-dynamics MSE loss that predicts actions from consecutive latent states. The low-level rectified-flow model is trained with a standard flow-matching objective, and the high-level planner uses diffusion training together with energy-based guidance at inference. I did not inspect enough of the paper to claim coefficient-level weighting or the exact full planner loss beyond what the accessible method text stated.

### Architecture / parameterization
An RSSM world model with a pretrained DINOv2 encoder, a high-level conditional diffusion planner for sparse latent subgoals, a low-level rectified-flow planner for dense latent trajectories, and an energy-based model for high-level strategic guidance.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
The paper is trying to solve long-horizon robotic planning where a policy must both discover a viable multi-stage strategy and execute it efficiently enough for real robotic use. Prior generative planners often use diffusion everywhere, which can help with diverse plan generation but becomes computationally expensive and awkward for fast low-level control.

### 2. What is the method?
The method has two stages. First, train a world model whose latent space is shaped not only by reconstruction and dynamics prediction but also by contrastive progress structure and inverse-dynamics supervision. Second, freeze that latent space and train a hierarchical planner on top of it: a diffusion model proposes sparse strategic subgoals, an energy model scores and guides those sequences, and a rectified-flow model quickly fills in the dense latent trajectory between subgoals.

### 3. What is the method motivation?
The motivation is that not all planning levels want the same generative behavior. High-level planning benefits from exploration and multimodal proposal generation, which diffusion is good at. Low-level trajectory generation benefits from faster and smoother deterministic transport, which rectified flow is better suited to than iterative diffusion denoising.

### 4. What data does it use?
The paper evaluates on four FurnitureBench assembly tasks in simulation and the real world, and also reports on RLBench and OGBench long-horizon tasks. The accessible text makes clear that the system is trained on trajectory data sufficient to learn the world model and planners in those settings, but I did not inspect the full appendix to verify dataset sizes, exact collection protocols, or all train-test splits.

### 5. How is it evaluated?
It is evaluated on long-horizon task success across FurnitureBench, RLBench, and OGBench, with emphasis on contact-rich assembly and more general long-horizon locomotion/manipulation settings. The paper positions itself against prior generative planning baselines and tries to show both stronger task performance and better real-time suitability.

### 6. What are the main results?
From the accessible text, the main claim is that HDFlow significantly outperforms prior methods on four challenging furniture assembly tasks in both simulation and real-world settings, and also generalizes well across RLBench and OGBench. I trust the qualitative claim that the method performed strongly enough to warrant attention, but I did not inspect enough tables to restate every numeric margin with confidence.

### 7. What is actually novel?
The genuinely novel part is not just “hierarchical generative planning.” It is the combination of three specific moves: using diffusion only for sparse high-level exploration, using rectified flow for low-level dense generation, and shaping plus guiding the latent planning space with a contrastive world-model objective and an explicit energy-based strategic scorer. Plenty of papers claim decomposition. Fewer actually give each level a different inductive bias and computational budget.

### 8. What are the strengths?
- The decomposition is legible and tied to different role requirements.
- The latent space is explicitly shaped for progress, not treated as a passive bottleneck.
- Energy guidance gives the high-level planner an explicit quality signal rather than relying only on sample plausibility.
- The method appears to care about real-time feasibility instead of benchmarking only offline sampling quality.

### 9. What are the weaknesses, limitations, or red flags?
- The energy-based guidance adds another learned component whose failure modes may be subtle and hard to diagnose.
- The latent-space quality still depends heavily on the world model; if that representation is wrong or collapses relevant distinctions, the hierarchy inherits the damage.
- The paper is still benchmark-centered, so it remains unclear how gracefully the method handles severe partial observability, hidden state, or long-memory tasks beyond the demonstrated domains.
- I did not inspect the appendix deeply enough to verify how much of the gain comes from the hybrid planner versus the contrastively shaped latent space versus other implementation choices.

### 10. What challenges or open problems remain?
A major open problem is whether this kind of hierarchy can manage tasks where success depends on persistent explicit memory rather than just well-structured latent rollout. Another is whether high-level subgoals can be made more interpretable or grounded in reusable object/state abstractions instead of existing only as learned latents.

### 11. What future work naturally follows?
- Add explicit memory or object/state structure on top of the latent subgoal hierarchy.
- Test whether the diffusion-versus-flow split still holds under heavier partial observability.
- Make the high-level subgoals more interpretable and reusable across tasks.
- Study whether the energy model can be replaced or complemented by more legible value or constraint estimators.

### 12. Why does this matter for cabbageland?
Because it supports a design instinct that keeps recurring here: different layers of cognition and control should not be forced into one generic model class just because that class is fashionable. The paper is useful not only as a planner but as a concrete argument for role-specific generators, structured latent shaping, and explicit strategic scoring.

### 13. What ideas are steal-worthy?
- Assign different generative primitives to different planning levels based on actual role requirements.
- Shape world-model latents with goal-progress contrast, not just reconstruction and prediction.
- Add an inverse-dynamics auxiliary objective to keep latent plans tied to controllable transitions.
- Use an explicit quality model to guide strategic plan generation instead of trusting sample plausibility.

### 14. Final decision
**Keep and revisit.** This is one of the better recent long-horizon planning papers because the mechanism is clear, the decomposition earns its name, and the ideas transfer beyond the specific benchmark stack.
