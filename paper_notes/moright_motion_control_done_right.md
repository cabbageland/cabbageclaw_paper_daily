# MoRight: Motion Control Done Right

## Basic info

* Title: MoRight: Motion Control Done Right
* Authors: Shaowei Liu, Xuanchi Ren, Tianchang Shen, Huan Ling, Saurabh Gupta, Shenlong Wang, Sanja Fidler, Jun Gao
* Year: 2026
* Venue / source: arXiv preprint (cs.CV / cs.AI / cs.GR / cs.LG / cs.RO)
* Link: https://arxiv.org/abs/2604.07348
* Date surfaced: 2026-04-09
* Why selected in one sentence: It gives controllable video generation a real decomposition by separating canonical object motion from camera motion and by modeling active actions separately from passive consequences.

## Quick verdict

* Highly relevant

This is one of the better recent controllable-video papers because the structure is doing actual work instead of just decorating the claim. The canonical-view motion branch plus target-view branch is a sensible way to disentangle camera and object motion, and the active/passive split is at least a concrete attempt at causal structure. I only inspected the arXiv abstract and HTML paper text, not the full PDF figures/tables in detail, so the mechanism read is more trustworthy than my confidence in every reported metric.

## One-paragraph overview

MoRight tackles a common failure mode in motion-controlled video generation: most methods treat motion prompts as pixel trajectories in image space, which immediately entangles object motion with camera motion and reduces “reasoning” to trajectory following. The paper introduces a dual-stream latent video diffusion setup. One stream generates motion in a canonical static camera where user-specified object motion is easy to express; the other generates the target video under arbitrary camera motion. Cross-view attention transfers the canonical motion into the target view. On top of that, the training setup decomposes motion into active motion, meaning user-driven action, and passive motion, meaning downstream consequence, so the model can support both forward reasoning from actions and inverse reasoning from desired outcomes.

## Model definition

### Inputs
The model takes a single reference image, user-specified object motion trajectories in a canonical view, and a target camera-motion sequence. During training it also uses paired supervisory videos for the canonical stream and the target stream, with different mixtures of motion-only, camera-only, and coupled data as described in the accessible HTML text.

### Outputs
The output is a generated video over the requested time horizon. Depending on conditioning, the model can generate scene evolution from active motion inputs, or infer plausible driving actions for desired passive outcomes while also rendering the scene from user-specified viewpoints.

### Training objective (loss)
From the accessible HTML text, the backbone is a DiT-based latent video diffusion model trained with a flow-matching objective. The paper explicitly gives an MSE loss on predicted velocity, where the model regresses the flow field toward the standard latent interpolation target between clean latent video and Gaussian noise. I did not inspect the full supplemental details, so any auxiliary losses beyond the main flow-matching loss may be missing here.

### Architecture / parameterization
A DiT-based latent video diffusion model with a dual-stream generation architecture. One stream models canonical-view object motion, the other models target-view video under camera motion, and the two streams share weights while exchanging information through self-attention / cross-view attention. Camera conditions are encoded by warping the first image with pose and depth; motion conditions are encoded from trajectory maps with a lightweight track encoder and injected into every transformer block.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Existing motion-controlled video models make two messes at once. First, they represent motion in image-space trajectories, which means camera motion and object motion are entangled from the start. Second, they treat control as kinematic displacement following instead of modeling what user-driven motion should cause elsewhere in the scene. The paper wants a generator that can separately control viewpoint and object motion while also producing interaction-aware consequences.

### 2. What is the method?
The method has two coupled parts. For disentanglement, it uses a canonical stream with object motion under a static view and a target stream with camera motion; target tokens attend to motion-conditioned canonical tokens so motion can be transferred across views. For causal motion modeling, the paper splits motion into active and passive components during training, so the model learns to map actions to consequences and can also invert desired outcomes back to plausible actions.

### 3. What is the method motivation?
Object motion is easy to specify in a fixed canonical view and hard to specify after viewpoint changes. So the paper moves motion definition into the canonical branch rather than forcing the user to encode camera changes inside a trajectory prompt. The active/passive split is motivated by the gap between “make this pixel move” and “model how one object’s action changes other objects.”

### 4. What data does it use?
From the accessible text, the paper trains on paired videos with motion-only, camera-only, and fully coupled supervision, and evaluates on three benchmarks covering interaction-heavy scenarios. I did not verify the full dataset inventory or curation details beyond the paper HTML, so this section is necessarily partial.

### 5. How is it evaluated?
The evaluation reportedly covers generation quality, motion controllability, and interaction awareness across three benchmarks. The key claimed behaviors are disentangled camera/object control and support for both forward reasoning from actions and inverse reasoning from desired passive outcomes.

### 6. What are the main results?
The paper claims state-of-the-art performance on its three benchmarks for generation quality, motion control, and interaction awareness. More interesting than raw score claims is that the system allegedly handles both forward and inverse motion reasoning under free camera changes. I did not independently inspect all tables, so I am treating the numerical superiority claims as reported rather than fully audited.

### 7. What is actually novel?
The strongest novelty is the decomposition, not the diffusion backbone. The canonical-object-motion versus target-camera-motion split is a cleaner interface than trajectory-conditioned video generation usually offers. The active/passive motion split is also more substantive than generic “reasoning-aware” language, because it creates a concrete representational distinction for action versus consequence.

### 8. What are the strengths?
The paper attacks the representation problem directly. It avoids requiring explicit 3D object trajectories or heavy privileged signals for disentanglement. The active/passive distinction gives the causal claim at least some architectural teeth. And the inverse-reasoning setup is a nice stress test because it asks the model to infer causes rather than just animate effects.

### 9. What are the weaknesses, limitations, or red flags?
This is still a video generator, not a grounded physics simulator, so “causality” here should be read cautiously. The active/passive split may still rely heavily on dataset regularities rather than real intervenable state. The paper also seems vulnerable to the usual question in this genre: do the benchmarks test long-horizon consequence structure, or mostly short-range interaction plausibility? And since I did not do a full PDF audit, I am not yet confident about ablation depth or failure-case honesty.

### 10. What challenges or open problems remain?
The big unresolved issue is whether this kind of decomposition can scale to richer object state, longer horizons, and partially observed interactions where consequences are delayed or hidden. Another open problem is making the causal variables more explicit than trajectory roles, so the model can support editing, intervention, and planning rather than just plausible generation.

### 11. What future work naturally follows?
A natural next step is combining the dual-stream motion interface with persistent 3D or object-centric state, so the system is not just transferring motion but maintaining a reusable scene model. Another is testing whether active/passive decomposition helps embodied planning or robotics data, where action-consequence structure matters more than pretty video. A third is replacing the latent causal split with more explicit affordance, contact, or object-interaction variables.

### 12. Why does this matter for cabbageland?
Because this repo keeps preferring explicit interfaces over blended mush. MoRight is a good example of a paper that earns some of its structural claims. It separates roles that many nearby papers collapse together, and that makes it relevant to controllability, world modeling, action representations, and scene interaction.

### 13. What ideas are steal-worthy?
- Put user-controlled motion in a canonical reference frame where it is actually legible.
- Transfer that motion into target views through cross-view attention instead of asking one prompt channel to do everything.
- Separate action-like motion from consequence-like motion at the representation level.
- Evaluate inverse as well as forward control, because inverse tasks expose whether the model learned anything beyond direct trajectory imitation.

### 14. Final decision
Keep. This is a strong design-reference paper for controllable generation with a real decomposition, even if the causal claims should still be treated with healthy suspicion.
