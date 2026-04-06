# Hierarchical Planning with Latent World Models

## Basic info

* Title: Hierarchical Planning with Latent World Models
* Authors: Wancong Zhang, Basile Terver, Artem Zholus, Soham Chitnis, Harsh Sutaria, Mido Assran, Randall Balestriero, Amir Bar, Adrien Bardes, Yann LeCun, Nicolas Ballas
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2604.03208
* Date surfaced: 2026-04-06
* Why selected in one sentence: It shows a clean way to add temporal abstraction at planning time over pretrained latent world models, and the result seems to matter on genuinely non-greedy tasks.

## Quick verdict

**Highly relevant**

This is a strong paper, mostly because it is disciplined about scope. It is not pretending to solve representation learning, hierarchical RL, and robot policy learning all at once. It asks a narrower question — can multi-timescale latent planning make pretrained world models actually useful on long-horizon zero-shot control? — and the answer appears to be yes. I inspected the abstract and substantial HTML method text, but not the entire appendix, so some implementation details and ablation depth remain uncertain.

## One-paragraph overview

The paper takes existing latent world models and adds hierarchy at inference time rather than learning a hierarchical policy. A high-level world model plans over latent macro-actions and predicts long-horizon latent waypoints; the first predicted waypoint becomes a subgoal for a low-level planner that optimizes primitive actions with a short-horizon world model. Both levels live in the same latent space, so the subgoal handoff is just latent matching rather than code generation, skill dispatch, or inverse-model gymnastics. The result is a pragmatic but important point: flat MPC may be the wrong planning shape for long-horizon zero-shot control even when the world model itself is decent.

## Model definition

### Inputs
Current observation and goal observation, encoded into a shared latent space. The low-level model additionally takes primitive actions. The high-level model takes latent macro-actions produced by an action encoder that compresses action subsequences between waypoint states.

### Outputs
The low-level model predicts short-horizon future latent states under primitive actions. The high-level model predicts longer-horizon latent waypoint states under latent macro-actions. The planner outputs primitive actions for execution.

### Training objective (loss)
From the accessible HTML text, the high-level world model is trained with a latent prediction teacher-forcing loss that minimizes L1 distance between predicted waypoint latents and actual waypoint latents. The low-level model reuses the training objectives of the backbone world models from prior work. The action encoder is trained jointly with the high-level model to compress low-level action sequences into latent macro-actions.

### Architecture / parameterization
A hierarchical planning stack built from two latent world models operating at different temporal scales plus a learned action encoder. The framework is model-agnostic across several latent world-model backbones including VJEPA2-AC, DINO-WM, and PLDM.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Learned world models often fail on long-horizon tasks for two blunt reasons: rollout errors compound and planning over long action sequences becomes computationally ugly. The paper targets both problems by introducing temporal hierarchy into latent-space planning.

### 2. What is the method?
- Learn or reuse a low-level latent world model for short-horizon prediction under primitive actions.
- Learn a high-level latent world model that predicts longer-range waypoint transitions in the same latent space.
- Train an action encoder that compresses chunks of low-level actions into latent macro-actions.
- At test time, plan high-level macro-actions toward the final goal in latent space.
- Use the first predicted high-level latent waypoint as a subgoal.
- Run low-level MPC to choose primitive actions that reach that subgoal.
- Replan in receding-horizon fashion.

### 3. What is the method motivation?
If flat planning over long primitive-action sequences is both expensive and brittle, then the right move is to separate long-horizon reasoning from short-horizon control. The paper’s motivation is refreshingly practical: keep temporal abstraction in the planner, not in a reward-conditioned skill hierarchy, and do it in the same latent space so the interface stays simple.

### 4. What data does it use?
From the accessible text, the paper evaluates on real-world Franka robot manipulation using world models trained on unlabeled DROID and RoboSet data, plus simulated Push-T and maze navigation tasks with other latent world-model backbones. I did not inspect all dataset details in the appendix.

### 5. How is it evaluated?
It compares single-level planning against hierarchical planning on long-horizon or non-greedy tasks across multiple world-model families. Key settings include Franka pick-and-place and drawer manipulation, Push-T with extended horizons, and maze navigation with train-test mismatch.

### 6. What are the main results?
The most important reported result is that hierarchy turns a 0% success rate into 70% on a real-world non-greedy pick-and-place setting when planning from only a final goal, while also improving other tasks such as drawer manipulation, Push-T, and maze navigation. The paper also claims materially lower planning-time compute for comparable or better success. I did not independently verify every number beyond the visible text and figures.

### 7. What is actually novel?
The novelty is not hierarchical control in general. It is the specific claim that latent world models trained for zero-shot planning can be made much more effective by adding a shared-latent, multi-timescale planning abstraction at inference time. The paper’s strongest contribution is the coupling rule: high-level predicted latent states directly become low-level subgoals, without skills or inverse policies in the middle.

### 8. What are the strengths?
- Clear problem definition and restrained scope.
- The shared latent-space interface is elegant and low-friction.
- The method is modular across different world-model backbones.
- Real-world non-greedy manipulation is a better stress test than purely greedy goal-reaching.
- The planning-time abstraction is likely more reusable than another task-specific hierarchical policy.

### 9. What are the weaknesses, limitations, or red flags?
- The method depends on the latent space being good enough that latent matching corresponds to meaningful subgoal attainment.
- Macro-action compression could hide aliasing problems if distinct action chunks map to insufficiently informative latent actions.
- The paper is less about learning better world models than about planning better with them, so it does not solve representation drift by itself.
- There is some risk that success depends heavily on careful CEM tuning and planning budgets.
- I have not read the full appendix, so the sensitivity to waypoint selection and planner hyperparameters remains uncertain.

### 10. What challenges or open problems remain?
How to learn hierarchical latent spaces whose subgoals are not only useful for planning but also interpretable and robust under broader distribution shift remains open. Another open question is whether more than two temporal levels are worth the extra complexity.

### 11. What future work naturally follows?
- Learn subgoal latents that are easier to verify or decode into explicit state.
- Combine the hierarchical planner with uncertainty estimation so high-level plans know when their subgoals are unreliable.
- Extend the framework to partially observable and memory-heavy tasks.
- Study whether hierarchical planning can be merged with explicit object or scene structure rather than only dense latent embeddings.

### 12. Why does this matter for cabbageland?
Because it is a good example of decomposition that actually changes the computation. It does not just narrate a hierarchy; it creates one in the planner and forces planning to happen at two temporal scales. That is exactly the sort of reusable systems insight that matters more than another benchmark-shaped backbone tweak.

### 13. What ideas are steal-worthy?
- Add temporal hierarchy at planning time rather than policy-training time.
- Use a shared latent space so high-level plans can hand subgoals directly to a low-level planner.
- Compress action chunks into macro-actions instead of assuming fixed symbolic skills.
- Benchmark non-greedy tasks where single-level planners fail without manually provided subgoals.

### 14. Final decision
**Definitely worth preserving.** It is one of the cleaner recent arguments that long-horizon competence may require better planning decomposition before it requires another new world-model backbone.

## Key figures from HTML

### Figure 1
ArXiv HTML caption summary: top-down picture of hierarchical latent planning. A high-level planner searches over macro-actions to reach the goal, the first predicted latent waypoint becomes a subgoal for low-level planning, and the bottom panels summarize success-rate gains and planning-efficiency improvements across different world-model backbones.

### Figure 2
ArXiv HTML caption summary: latent-space hierarchy diagram showing high-level optimization toward the final goal and low-level primitive-action optimization toward the first latent subgoal.

### Figure 3
ArXiv HTML caption summary: training setup for the high-level world model, where latent actions are encoded from chunks of low-level actions and used to predict waypoint latents with a causal model trained by latent prediction loss.
