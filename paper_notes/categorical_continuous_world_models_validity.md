# Beyond Visual Fidelity: Comparing Categorical and Continuous World Models

## Basic info

* Title: Beyond Visual Fidelity: Comparing Categorical and Continuous World Models
* Authors: Sarah Parisot, Melanie Fernandez Pradier, David Bignell, Sergio Valcarcel Macua, Katja Hofmann
* Year: 2026
* Venue / source: arXiv preprint, v1 submitted November 20, 2026
* Link: https://arxiv.org/abs/2611.27870
* Date surfaced: 2026-11-23
* Why selected in one sentence: A controlled four-model comparison separates valid dynamics, calibrated stochastic outcomes, and visual reconstruction instead of treating good video as a good simulator.

## Quick verdict

* Highly relevant

Preserve the experimental design and the counterexample to a single world-model quality ranking. Categorical models win validity efficiently in these environments, but continuous models beat one categorical family on calibration. This is a strong small-world diagnostic study, not proof that continuous generative world models are the wrong research direction.

**Read basis:** Full main paper from the [primary PDF](https://arxiv.org/pdf/2611.27870), plus training/evaluation details, inference-step analysis, and selected component/ghost-policy appendix results. Plots and tables are paper-reported, not independently reproduced. No code execution or release audit.

## One-paragraph overview

The paper builds four action-conditioned visual predictors by crossing categorical versus continuous outputs with sequential patch generation versus iterative whole-frame generation. In a stochastic Pac-Man environment, lossless categorical encoding removes tokenizer reconstruction error, while an exact simulator checks permissible transitions and hidden-state-consistent rollout prefixes. Separately, repeated next-frame samples are compared with known conditional outcome probabilities. Greedy categorical next-token prediction reaches approximately 86% fully valid 64-step rollouts at 2 PFLOPs, but high validity does not imply calibrated sampling: at 10 PFLOPs, sampled iterative categorical prediction has empirical TV 0.67 versus 0.33-0.34 for continuous models. A simple 3D maze then shows that worse reconstruction from lossy tokens need not imply worse long-horizon semantic/FVD performance. The useful result is this separation of targets; tiny controlled worlds and unequal inference procedures limit extrapolation.

## Model definition

### Inputs

Observation/action history and the action leading to the next frame. Pac-Man uses at most 15 prior frames, an 8-by-8 occupancy grid, and five discrete actions. Its categorical representation has sixteen 2-by-2 patches, each enumerating seven valid cell states: 7^4 = 2,401 possible patch tokens. Continuous models receive the same information as fixed-color RGB patches, each a 12-dimensional vector.

The maze uses 64-by-64 RGB images, continuous steering/forward commands, and 64 vertical image strips per frame. Categorical variants use either a lookup-table lossless encoding covering encountered column patterns or a learned VQ-VAE. Continuous models operate on RGB strips. Iterative models additionally receive masked tokens or a noisy target and flow time.

### Outputs

The next observation, either categorical patch distributions or continuous patch velocities. Next-token models factorize the frame in patch order. Iterative models update all target locations through repeated masked-token revelation or joint flow integration. Generated observations feed back into temporal context during rollout.

Continuous Pac-Man output is projected to the nearest valid palette color before evaluation and feedback. This enforces valid individual cell types, not correct entity counts, motion, or history.

### Training objective (loss)

- **Cat-NT:** Cross-entropy over all next-frame target tokens, teacher-forced on previous target patches.
- **Cont-NT:** Conditional flow-matching squared error for each RGB patch. With `y_tau = (1 - sigma_tau)y + sigma_tau epsilon`, regress velocity to `epsilon - y`, conditioned on the autoregressive backbone output.
- **Cat-Iter:** MaskGIT-style cross-entropy only on randomly masked target positions.
- **Cont-Iter:** The same flow-matching objective applied jointly to the entire target frame.

All temporal training uses ground-truth context rather than generated-history training. The lossy maze VQ-VAE has a separate L1 reconstruction/codebook/commitment objective; its training is excluded from reported world-model compute.

### Architecture / parameterization

Six-block transformer backbones: decoder-only, pre-normalized next-token models versus DiT-style iterative models with block-causal temporal attention. Cat-NT ties token input/output embeddings; Cont-NT adds a small conditional residual-MLP flow head. Cont-Iter uses time-conditioned adaptive normalization. Cat-Iter commits highest-confidence tokens under a linear reveal schedule.

Backbone capacity is approximately matched, not every parameter or architectural choice. All main models use AdamW and the same nominal learning rate; differing embeddings/heads and losses remain part of each method.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Do world models learn valid action-conditioned stochastic dynamics, or just visually plausible frames? Existing categorical/continuous comparisons often bundle tokenization, generation order, capacity, and perceptual fidelity. Matching a single sampled future also wrongly penalizes other valid stochastic outcomes.

### 2. What is the method?

Use a two-by-two model comparison, then evaluate distinct targets:

1. **Transition validity:** Is this transition permitted, even if an earlier one failed?
2. **Rollout validity:** Has the entire generated prefix remained compatible with the simulator, including hidden pellet history and reset rules?
3. **Probability calibration:** Do repeated ghost configurations match the exact conditional distribution?
4. **Visual/semantic quality:** Exact RGB agreement, semantic pixel accuracy, and 64-frame FVD in the maze.

The validators accept valid alternative outcomes rather than demanding replay of one reference. A locally recovered transition does not erase a broken rollout prefix.

### 3. What is the method motivation?

Remove reconstruction error before attributing differences to dynamics learning. Cross generation order with output family rather than comparing only autoregressive tokens with whole-frame flow. Most importantly, validity and probability accuracy answer different questions: a deterministic choice can remain legal while misrepresenting a stochastic world.

### 4. What data does it use?

Generated trajectories in two purpose-built worlds. Pac-Man's main setting has a fixed 8-by-8 wall layout and three randomly moving ghosts; ablations vary ghost count and random/flee policies. Training initial positions/pellet density vary, with uniformly sampled actions. The maze has solid-color geometry and three bouncing spheres, randomized routes and initial sphere states.

Shared settings list 2,048 trajectories per epoch, 16 frames per trajectory, and batch size 128. Main training budgets are 10 PFLOPs for Pac-Man and 30 for the maze. These are not naturalistic visual datasets or real-world transition logs.

### 5. How is it evaluated?

Pac-Man validity uses 512 shared evaluation contexts, 64 generated steps, and three training seeds. Shading generally shows seed minimum/maximum, not a confidence interval. Calibration uses 32 next-frame samples on 232 fixed contexts where conditional ghost probabilities are exactly identifiable; the simulator's own 32-draw discrepancy supplies a sampling reference.

Maze results use one training seed and 512 evaluation cases with pointwise bootstrap intervals. These quantify evaluation-case variability, not training-run variation. Exact validity is not available in this partially observed continuous-action environment; semantic agreement and FVD are substitutes, not equivalent certificates.

### 6. What are the main results?

- Greedy Cat-NT retains approximately 86% fully valid 64-step Pac-Man rollouts at only 2 PFLOPs.
- Deterministic-component next-frame validity is near-perfect for all families from 2 PFLOPs; stochastic ghost mechanics drive much of the separation.
- At 10 PFLOPs, empirical ghost TV is 0.30 for sampled Cat-NT, 0.67 for sampled Cat-Iter, 0.33 for Cont-NT, and 0.34 for Cont-Iter. Continuous prediction is therefore not universally worse at stochastic modeling.
- Lossy categorical maze models lose exact next-frame RGB accuracy but remain competitive on long-horizon semantic accuracy/FVD.
- Sampling improves categorical maze FVD, whereas greedy decoding favors Pac-Man validity. Decoding must match the target metric.
- Continuous models improve with additional compute and inference steps; the main Pac-Man comparison uses 50 Euler evaluations, while maze comparisons use 20.

Do not convert the TV values into exact population calibration errors: they include finite-sample estimation effects.

### 7. What is actually novel?

The contribution is the controlled crossing and a rule-aware evaluation that separates possible futures from their probabilities. The components are familiar transformer, flow-matching and masked-generation machinery. No new explicit symbolic physics model is introduced.

### 8. What are the strengths?

Known rules make failures interpretable and distinguish distributional uncertainty from error. Lossless encoding addresses a real confound. Component checks and cumulative-prefix validity reveal errors that visual metrics hide. The calibration reversal prevents the paper from reducing to a simplistic categorical-wins story. Inference-step and decoding analyses test obvious alternative explanations.

### 9. What are the weaknesses, limitations, or red flags?

- Small worlds and tiny backbones are far from textured video, deformable objects, diverse scenes, or rare real-world events.
- Categorical vocabularies exploit restricted rendering; generalizing the lookup-table approach to unseen appearances is a different problem.
- The two-by-two design does not make all architectures, optimization difficulty, or inference costs identical.
- Compute uses a 6ND approximation and excludes encoder training. Training efficiency is not end-to-end wall-clock or deployment efficiency.
- One maze training seed weakens claims about reliable model-family ordering there.
- Thirty-two calibration samples leave a meaningful statistical floor, and next-step calibration is not a full long-horizon joint-law test.
- Greedy valid trajectories may suppress rare outcomes; high legality does not imply correct risk estimates.

These are boundaries on the conclusion, not reasons to discard a useful controlled experiment.

### 10. What challenges or open problems remain?

Preserve validity, calibrated stochastic branching, visual detail and fast inference simultaneously. Extend rule-aware evaluation when hidden state is ambiguous or no exact simulator is available. Determine which trends survive matched scaling and richer dynamics rather than assuming either reversal or universality.

### 11. What future work naturally follows?

Match complete training/inference cost, include tokenizer costs, add training seeds, and vary generalization axes separately: new layouts, object counts, transition rules, rendering and action distributions. Evaluate rare-event probabilities and downstream planning policies. Test whether explicitly structured state or constraint-aware decoding improves both legality and frequency accuracy without simply collapsing diversity.

### 12. Why does this matter for cabbageland?

It is a compact blueprint for evaluating world models and generative simulators with actual standards. It also corrects a common framing error: categorical image tokens are an output parameterization, not automatically an interpretable causal representation. Test what a model preserves before naming it physically grounded or compositional.

### 13. What ideas are steal-worthy?

- Cross representation with generation procedure; do not let architecture labels stand in for controlled comparisons.
- Report local validity, globally consistent prefix survival, and calibrated branching separately.
- Show the empirical estimator floor using simulator draws.
- Keep both sampled next-token and iterative categorical baselines; they are not interchangeable.
- Decompose hidden-state consistency and reset behavior rather than checking only neighboring frames.
- Treat perceptual reconstruction and useful dynamics as separate axes, especially when judging lossy representations.

### 14. Final decision

Preserve as an evaluation/reference note and baseline-design guide. Start here before claiming a visual world model learned controllable dynamics. Do not cite it as a universal theorem that discrete representations are better than continuous ones.
