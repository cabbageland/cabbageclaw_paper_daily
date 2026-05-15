# Slot-MPC: Goal-Conditioned Model Predictive Control with Object-Centric Representations

## Basic info

* Title: Slot-MPC: Goal-Conditioned Model Predictive Control with Object-Centric Representations
* Authors: Jonathan Spieler, Angel Villar-Corrales, and Sven Behnke
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2605.14937
* Date surfaced: 2026-05-15
* Why selected in one sentence: It turns object-centric representation learning into an actual planning interface instead of leaving it as interpretability decoration.

## Quick verdict

* Highly relevant

This is one of the cleaner recent cases where explicit structure does real downstream work. The important move is not merely learning slots, it is using a differentiable object-centric dynamics model so gradient-based model predictive control can optimize actions directly in slot space. I inspected substantial arXiv HTML full text including the method and losses, so the mechanism summary is fairly solid, though I did not fully audit every appendix result.

## One-paragraph overview

Slot-MPC learns slot-based object representations from visual sequences, trains an action-conditioned object-centric predictor over those slots, and then uses that learned dynamics model at inference time to plan action sequences toward a goal image via gradient-based model predictive control. Instead of planning in pixel space or a large holistic latent, it parses the current image and the goal image into object slots, rolls predicted slot futures under candidate actions, and directly optimizes the actions to make the terminal slot configuration match the goal slots.

## Model definition

### Inputs
Current image, goal image, and a sequence of candidate low-level actions over a planning horizon. During world-model training, the model uses visual frames plus aligned action sequences.

### Outputs
The learned scene parser outputs slot representations for objects or entities in the scene. The conditional object-centric predictor outputs future slot states autoregressively, and a decoder can reconstruct future frames from those predicted slots.

### Training objective (loss)
The slot parser is trained self-supervised with image reconstruction loss. The action-conditioned predictor is trained with a combined future-frame prediction loss plus slot-alignment loss against slots extracted from ground-truth future frames.

### Architecture / parameterization
A SAVi-style slot-based scene parser and decoder, combined with a transformer-based action-conditioned object-centric predictor, called cOCVP. Planning uses gradient-based model predictive control over the differentiable dynamics model.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Most object-centric world models still end in reactive policy learning or expensive sampling-based planning, which limits adaptation to novel situations and makes structured latents feel conceptually nice but operationally underused. The paper tries to show that object-centric state can be a practical substrate for online planning directly from visual goals.

### 2. What is the method?
It first parses images into slot representations with SAVi-style scene decomposition. It then trains an action-conditioned object-centric predictor, cOCVP, to forecast future slots and frames. At inference time, it parses the current observation and goal image into slots, rolls forward future slots under candidate actions, and uses gradient descent on the action sequence to minimize distance between predicted terminal slots and goal slots.

### 3. What is the method motivation?
If the latent state is object-centric and compact, planning should become both cheaper and more controllable than in large holistic latent spaces. The paper’s real bet is that explicit object factorization is not just semantically nicer, it is a better control interface for goal-conditioned planning.

### 4. What data does it use?
Simulated robotic manipulation tasks from an offline reward-free setting. The accessible text emphasizes purely visual training data with action sequences rather than online reward-driven interaction.

### 5. How is it evaluated?
Against non-object-centric world-model baselines on simulated manipulation tasks, with attention to task success and planning efficiency. The paper also compares gradient-based MPC against gradient-free sampling-based MPC in the low-coverage offline regime.

### 6. What are the main results?
The accessible text claims Slot-MPC improves both task success and planning efficiency relative to non-object-centric baselines, and that gradient-based MPC works better than sampling-based MPC in the studied offline setting with limited state-action coverage. The claimed reason is that slot structure reduces latent dimensionality dramatically and supports more direct optimization.

### 7. What is actually novel?
The useful novelty is the combination, object-centric latent dynamics plus gradient-based MPC directly in slot space for goal-conditioned visual planning. Slot learning alone is not new, and MPC with learned dynamics is not new, but tying them together in a compact differentiable planning interface is the point.

### 8. What are the strengths?
The structure actually affects control. The planning loop is legible. The model is task-agnostic at training time and reused at inference. The paper also targets a realistic weak-data regime instead of assuming perfect coverage and giant policy training budgets.

### 9. What are the weaknesses, limitations, or red flags?
Everything depends on slot stability and whether object decomposition captures task-relevant interactions. Contact-rich physics can be awkward for neat object slots. The evaluation appears to be in simulation, so robustness to messy real-world perception is still open. Also, optimizing a latent distance to goal slots may miss details that matter physically but not representationally.

### 10. What challenges or open problems remain?
Better handling of contact, occlusion, and non-rigid interactions. Extending object-centric planning to longer horizons and partial observability. Making the learned object state reliable enough for real robot deployment.

### 11. What future work naturally follows?
Add explicit memory across longer trajectories, object permanence under occlusion, uncertainty-aware planning, and richer structured costs than simple terminal slot matching. A natural next step is combining object-centric state with explicit symbolic or graph-level subgoal structure.

### 12. Why does this matter for cabbageland?
Because it is a concrete example of explicit structure improving the action interface rather than merely improving narrative. It supports the broader cabbageland instinct that factorized state becomes valuable when it makes planning cheaper, more controllable, or more legible.

### 13. What ideas are steal-worthy?
Use compact object state as the actual planning substrate. Train task-agnostic structured dynamics from offline visual data. Prefer differentiable action optimization when the learned state is compact enough to make it tractable.

### 14. Final decision
Keep it. This is not a foundational universal solution, but it is a strong reference for how object-centric world models can earn their keep in planning.
