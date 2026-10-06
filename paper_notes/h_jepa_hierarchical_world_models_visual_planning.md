# H-JEPA: End-to-End Learning of Hierarchical World Models for Visual Planning

## Basic info

* Title: H-JEPA: End-to-End Learning of Hierarchical World Models for Visual Planning
* Authors: Wancong Zhang, Basile Terver, Michael Rabbat, Yann LeCun, Randall Balestriero
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2610.06805
* Date surfaced: 2026-10-06
* Why selected in one sentence: It trains action-conditioned JEPA world models at multiple timescales and shows how abstract latent spaces and temporal subgoals separately improve planning.

## Quick verdict

* Highly relevant

H-JEPA is worth preserving because it makes hierarchy operational. Higher levels are not just extra predictors; they learn separate latent spaces, provide better goal-cost geometry, and decompose long-horizon planning into shorter subgoal-tracking problems. The limits matter: the gains are task dependent, deeper hierarchy can lose data coverage, and DROID is offline rather than closed-loop.

## One-paragraph overview

The paper extends action-conditioned JEPA world models from a single latent space to a temporal hierarchy. Level 1 encodes observations and predicts at the finest timescale; each higher level encodes lower-level latents over a coarser stride, predicts farther ahead in its own latent space, and supplies subgoals to levels below it during planning. The method is tested on FourRoomDistractors, Visual AntMaze, Push-T, OGBench Cube, and DROID robot videos. The best evidence is mechanistic: higher levels discard fast unpredictable features while preserving slow task-relevant variables, upper-level costs produce smoother planning geometry, and temporal decomposition makes subgoal costs more monotonic than a flat full-horizon goal cost.

## Model definition

### Inputs

The model trains on trajectories of observations and action blocks. Level 1 consumes RGB observations, optionally with proprioception, and primitive action blocks. Higher levels consume windows of lower-level latent states and lower-level action embeddings.

### Outputs

Each level outputs latent state embeddings and predicted future latent states at its own timescale. During planning, the top level outputs optimized macro-actions and predicted abstract states; lower levels refine those predictions into subgoals and finally primitive actions.

### Training objective (loss)

Each level uses a JEPA-style latent prediction loss: mean squared error between the predictor's future latent and the encoded target future latent, plus SIGReg to prevent collapse. For diverse real-scene DROID data, the model adds an inverse-dynamics loss that regresses the action from consecutive state representations, preventing slow-feature collapse into background identity.

### Architecture / parameterization

Level 1 is LeWM-style: a ViT-Tiny image encoder and causal transformer predictor. Higher levels use MLP encoders and causal transformer predictors with stride 2 and window size 1 in the main experiments. H-JEPA is compared with flat LeWM and HWM, a hierarchical world model whose upper levels share the same latent space through identity encoders.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It targets long-horizon visual planning with latent world models. A flat latent planner must search over long action sequences and score distant goals in a representation that may not give useful gradients far from the target.

### 2. What is the method?

Train a hierarchy of action-conditioned JEPAs, each at a coarser timescale and in its own latent space. At test time, plan top-down: the top level finds a coarse path toward the goal, and each lower level plans to match subgoals from the level above.

### 3. What is the method motivation?

Long-horizon tasks contain structure at multiple timescales. Higher levels should retain slow, predictable, task-relevant variables and discard fast details that are hard to predict over longer horizons. That creates both better abstract costs and shorter planning subproblems.

### 4. What data does it use?

The main environments are FourRoomDistractors and Visual AntMaze for navigation, Push-T and OGBench Cube for manipulation, and DROID for real teleoperated robot video. DROID varies scene, lighting, and objects across episodes and is evaluated offline with path-fidelity metrics.

### 5. How is it evaluated?

The paper evaluates representation abstraction with MLP probes and temporal-frequency analysis. It evaluates planning by success versus planner FLOPs and hierarchy depth, compares H-JEPA with LeWM and HWM, ablates cost-space versus temporal decomposition, and uses Frechet fidelity for DROID open-loop path matching.

### 6. What are the main results?

Higher levels discard fast-varying features in environments with large temporal-frequency gaps while retaining slow variables like agent position. On planning, additional levels shift the success/compute Pareto frontier upward on FourRoom, AntMaze, and Cube. On Visual AntMaze, three-level H-JEPA reaches 73.3% success in the reported cost ablation reference, compared with 18.0% for the separately trained LeWM baseline. On DROID, adding inverse dynamics avoids collapse, and a second H-JEPA level improves fidelity over flat LeWM+IDM and HWM at lower planner budgets.

### 7. What is actually novel?

The novelty is the combination of end-to-end JEPA training with distinct latent spaces per temporal level, plus a planning procedure that uses upper-level states as subgoals. The paper also isolates why hierarchy helps by separating abstract cost geometry from temporal decomposition.

### 8. What are the strengths?

The ablations are unusually useful. Changing only the cost space on AntMaze shows that upper-level representations can help even without upper-level subgoal generation. The monotonicity analysis shows that subgoal tracking creates better local progress signals than full-horizon goal costs. The DROID section identifies and repairs slow-feature collapse with inverse dynamics.

### 9. What are the weaknesses, limitations, or red flags?

Push-T degrades at deeper hierarchy because short episodes leave too few usable training clips, showing that hierarchy is data hungry. DROID is evaluated offline, not as closed-loop physical execution. The method still requires target observations as goals, and fixed strides may not match natural task boundaries.

### 10. What challenges or open problems remain?

The key challenge is proving that hierarchical latent plans transfer to real closed-loop robot control. Another open problem is learning variable-duration abstract segments rather than fixed stride-2 levels.

### 11. What future work naturally follows?

Train upper levels from action-free video, align upper-level latents with language, and use uncertainty to decide when a high-level subgoal is reliable enough for lower-level tracking. Another natural extension is combining H-JEPA-style hierarchies with explicit physical state channels like pose, velocity, contact, and object memory.

### 12. Why does this matter for cabbageland?

H-JEPA is a good example of hierarchy doing real work. It improves the state interface for planning instead of merely adding another latent abstraction layer with a grand name.

### 13. What ideas are steal-worthy?

When claiming hierarchy helps, separate cost-space benefits from temporal-subgoal benefits. Probe which variables disappear at upper levels and whether that disappearance matches timescale, not convenience. Add inverse-dynamics pressure when prediction alone would rather encode static background than controllable state.

### 14. Final decision

Preserve. This is directly relevant to world models, hierarchical planning, abstraction, and state-space design.
