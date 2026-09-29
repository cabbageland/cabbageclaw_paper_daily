# DynaTokens: Teaching Dynamics to Camera-Controlled Video Models at Test Time

## Basic info

* Title: DynaTokens: Teaching Dynamics to Camera-Controlled Video Models at Test Time
* Authors: Ziqi Ma, Hongqiao Chen, Georgia Gkioxari
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2609.35704
* Date surfaced: 2026-09-29
* Why selected in one sentence: It gives a clean adapter design for adding localized scene dynamics to a frozen camera-controlled video model without breaking camera control.

## Quick verdict

**Highly relevant**

DynaTokens is not a full solution to dynamic world modeling, but it is a sharp interface paper. It recognizes that camera motion and object dynamics have different spatial structure, then puts the trainable test-time adapter in the path that can express local dynamics. I read the full arXiv HTML text, including method, experiments, ablations, attention analyses, and robustness checks.

## One-paragraph overview

Camera-controlled video models are good at changing viewpoint in static scenes but often freeze objects, move them incorrectly, or degrade when the scene itself should change. DynaTokens adds a small set of scene-specific learnable tokens to a frozen camera-controlled video transformer. Video patch tokens cross-attend to these dynamic tokens in each transformer block, while the global camera-control path remains mostly untouched. At test time, the tokens are trained on a few example trajectories from the scene, then reused under new query camera paths. The result is a better dynamics-camera tradeoff than LoRA, block finetuning, or TTT layers on VBench2 and WorldScore.

## Model definition

### Inputs

Inputs are an initial image or scene prompt, camera-control information, text conditioning, and a small set of example trajectories for the scene. At test time, the method receives new query camera paths after training the scene-specific tokens.

### Outputs

The model outputs camera-controlled videos with learned local scene dynamics. Internally, the dynamic tokens provide cross-attention signals to video patch tokens and act as localized gates over dynamic regions.

### Training objective (loss)

DynaTokens trains only the added scene-specific tokens at test time. The base camera-controlled video model stays frozen. The accessible text frames the objective as learning from a few trajectories to reproduce scene dynamics; the detailed loss is tied to the frozen model's video training/inversion setup rather than a new standalone objective.

### Architecture / parameterization

The method inserts dynamic tokens into a pretrained video transformer. Patch tokens cross-attend to the learned dynamic tokens in every transformer block, with zero-initialized cross-attention output for minimal initial perturbation. Unlike LoRA or prompt tokens in self-attention, these tokens are designed to affect localized dynamics without entangling with the camera-control branch.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Camera-controlled video models often separate viewpoint control from scene evolution poorly. They can move the camera around a scene but fail when objects should move or when physical and stylistic changes should unfold over time.

### 2. What is the method?

DynaTokens adds scene-specific trainable tokens read through cross-attention by video patches. The tokens are optimized from a small set of trajectories at test time while the base model remains frozen.

### 3. What is the method motivation?

Camera motion is global, while object dynamics are spatially localized. A good adapter should therefore be local and should avoid disrupting the global camera-conditioning path.

### 4. What data does it use?

The paper trains DynaTokens on small numbers of scene trajectories, with robustness tests down to three trajectories. Evaluation uses VBench2 dynamic categories, WorldScore, and additional physical and stylistic dynamics examples.

### 5. How is it evaluated?

It reports dynamics-related VBench2 metrics, WorldScore motion and camera metrics, human pairwise rankings, seen/unseen camera path generalization, ablations over token design, and attention localization against SAM masks.

### 6. What are the main results?

DynaTokens beats LoRA, LoRA without PRoPE updates, finetuning, TTT layers, and VPT/APT-style alternatives on the reported dynamics-camera tradeoff. In the table shown in the paper, DynaTokens reaches VBench2 dynamic scores around 1.00/0.72/0.88 and WorldScore motion/camera values around 4.46/0.67 in the main comparison against other test-time methods, while LoRA is much weaker on motion. Human rankings favor DynaTokens by large margins.

### 7. What is actually novel?

The novelty is the adapter placement and structure. The paper is not merely doing test-time tuning; it uses dynamic tokens as localized cross-attention controls to avoid globally perturbing camera-conditioned generation.

### 8. What are the strengths?

* The camera-vs-dynamics decomposition is clear.
* The adapter is lightweight relative to the base model.
* Attention analyses support the localized-dynamics hypothesis.
* The method generalizes from training trajectories to unseen camera paths.

### 9. What are the weaknesses, limitations, or red flags?

The method still needs example trajectories for each scene, so it is not general dynamics inference from one image. The evaluations are mostly short video-generation benchmarks, not long-horizon interactive planning. The exact quality will depend heavily on the frozen base model.

### 10. What challenges or open problems remain?

Learning reusable dynamics tokens across scenes, handling multiple interacting objects, and integrating physical constraints remain open. It also needs tests in closed-loop or action-conditioned settings.

### 11. What future work naturally follows?

* Reuse or retrieve dynamic-token priors across similar scenes.
* Combine DynaTokens with physical or object-centric state.
* Train adapters that expose controllable dynamics parameters rather than scene-specific hidden tokens.

### 12. Why does this matter for cabbageland?

It is a useful example of aligning an adapter with the causal locality of the phenomenon being adapted. Camera control and local dynamics should not fight inside one undifferentiated update.

### 13. What ideas are steal-worthy?

* Keep global control pathways stable while adapting local dynamics.
* Use attention localization as a sanity check for dynamics adapters.
* Prefer small structured adapters over broad low-rank edits when the target variation is spatially localized.

### 14. Final decision

**Keep.** The method is narrow but the interface design is good.
