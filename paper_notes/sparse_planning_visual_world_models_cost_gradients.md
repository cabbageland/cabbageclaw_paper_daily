# Sparse Planning in Visual World Models via Cost Gradients

## Basic info

* Title: Sparse Planning in Visual World Models via Cost Gradients
* Authors: Yingchen Xu, Edward Grefenstette
* Year: 2026
* Venue / source: arXiv preprint
* Link: https://arxiv.org/abs/2610.10274
* Date surfaced: 2026-10-08
* Why selected in one sentence: It selects spatial world-model tokens by the downstream planning objective rather than by attention, prediction error, or random sparsity.

## Quick verdict

* Highly relevant

This is a sharp planning paper because it finds a small, testable lever in token-based world models. COSTGRAD is training-free, goal-conditioned, and directly tied to the planning cost. The main caveat is that its success is architecture-dependent: when action conditioning is changed from AdaLN to concat, the same token selector can lose its advantage.

## One-paragraph overview

Token-based visual world models keep a dense spatial grid of latent features, which is useful for planning but expensive for CEM rollouts. COSTGRAD performs one full-token probe per planning step, backpropagates the goal-conditioned planning cost to the input tokens, ranks tokens by gradient norm, and then runs CEM using only the selected subset. The key conceptual move is that planning relevance is not the same as prediction difficulty. On AdaLN-conditioned predictors, 50% token retention matches or beats full-token planning on three of four continuous-control environments and gives a 2.6x measured per-step speedup; combining sparsity with fewer CEM iterations reaches about 5.2x total speedup on Wall. The paper's best warning is that sparse planning must be evaluated with the predictor architecture because token removal changes the model's action pathway.

## Model definition

### Inputs

The method uses encoded observation tokens and goal tokens from a frozen DINOv2 ViT-S/14 encoder, plus candidate action sequences inside CEM planning. The world model is a fixed action-conditioned transformer predictor.

### Outputs

COSTGRAD outputs a selected subset of spatial token indices for the current planning step. The planner then outputs the first action of the best CEM action sequence after sparse latent rollout.

### Training objective (loss)

COSTGRAD itself has no training objective. The underlying world model is already trained to predict next DINO token grids. The selection probe uses a planning cost: squared distance between one-step predicted tokens and goal tokens under a default zero action.

### Architecture / parameterization

The main predictor is a six-block transformer with 16 attention heads using AdaLN-Zero action conditioning. A matched concat-conditioned variant is trained for the selector-architecture comparison. The selection score is the L2 norm of the gradient of the planning cost with respect to each input token.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Token-based world-model planning is computationally heavy because CEM repeatedly rolls out large spatial token grids. The question is how to choose a smaller token subset for the current goal without retraining the model or sacrificing planning success.

### 2. What is the method?

Run a full-token one-step probe, compute the planning cost to the goal, backpropagate to the input token grid, keep the top-K tokens by gradient norm, and run CEM on those tokens for the rest of the planning step. Reselect tokens at the next observation.

### 3. What is the method motivation?

Prediction error and attention can highlight visually hard or model-salient regions, but planning needs the tokens whose state affects the goal-reaching objective. The object that matters for control can be easy to predict, so prediction-derived selectors can miss it.

### 4. What data does it use?

The experiments use four continuous-control environments from the DINO-WM and JEPA-WMs suites: PointMaze, Wall, PushT, and MetaWorld. The predictors are trained on trajectory data from prior JEPA-WM/DINO-WM setups and are fixed during selection.

### 5. How is it evaluated?

The primary evaluation is planning success rate over three evaluation seeds with 96 episodes each, comparing full-token planning to COSTGRAD, attention selection, prediction-gradient selection, ToMe, and random token selection. The paper also measures wall-clock speed, sparsity sweeps, token selection stability, probe-action robustness, and action-pathway drift under token removal.

### 6. What are the main results?

At 50% tokens, full-token planning averages 73.5% success across the four environments, while COSTGRAD averages 77.3%. It is slightly below full on PointMaze but higher on Wall, PushT, and MetaWorld. It gives a measured 2.6x wall-clock speedup per environment planning step. On Wall, 50% tokens plus 15 CEM iterations reaches 92.0% success at about 17 seconds per step, a 5.2x speedup over full-token planning at 84.7% and 88.6 seconds. Under matched concat conditioning, however, COSTGRAD has essentially no advantage over random selection.

### 7. What is actually novel?

The novelty is selecting sparse world-model tokens from the gradient of the downstream planning objective, then showing that this interacts strongly with action-conditioning architecture.

### 8. What are the strengths?

The method is simple, training-free, and tied to the control objective. The paper compares against plausible alternatives and does not hide the architecture failure mode. The action-pathway drift diagnostic is a useful addition because it explains why relevance alone is not enough.

### 9. What are the weaknesses, limitations, or red flags?

The evaluation is limited to four simulated environments, one encoder family, and CEM. The method needs a backward pass per planning step, though this is amortized over CEM. The one-step probe may not identify all tokens needed for longer-horizon plans. Physical robot performance under perception noise and model mismatch remains untested.

### 10. What challenges or open problems remain?

The big open question is how to design world-model architectures that remain stable under sparse token subsets. The selector also needs tests with learned policies, alternative planners, real robots, and longer-horizon probes.

### 11. What future work naturally follows?

Test FiLM, cross-attention, prefix conditioning, and sparse-trained predictors using the same action-pathway drift metric. Combine COSTGRAD with learned sparse dynamics or adaptive token budgets. Use the planning-cost gradient as a diagnostic even when not using it directly for selection.

### 12. Why does this matter for cabbageland?

It makes a clean distinction cabbageland should keep: the model's prediction objective and the planner's control objective are not the same. World-model compression should be evaluated under the actual search procedure that will use it.

### 13. What ideas are steal-worthy?

Rank internal state by downstream cost gradients, not generic saliency. Measure whether sparsification changes action effects. Treat the planner as part of the world model's operating distribution.

### 14. Final decision

Preserve. The mechanism is small, transferable, and unusually honest about when it breaks.
