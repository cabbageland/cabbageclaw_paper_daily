# Learning Multimodal One-step Flow Policy via Value-weighted Optimal Transport

## Basic info

* Title: Learning Multimodal One-step Flow Policy via Value-weighted Optimal Transport
* Authors: Jaehun Shon, Jinha Choi, Jongwook Jeon, Jongmin Lee
* Year: 2026
* Venue / source: arXiv:2609.15883
* Link: https://arxiv.org/abs/2609.15883
* Date surfaced: 2026-09-15
* Why selected in one sentence: It turns one-step offline RL flow-policy distillation into a value-weighted transport assignment instead of direct critic chasing.

## Quick verdict

* Highly relevant

This is a useful offline RL paper because the central mechanism is concrete: use value to weight which reference actions deserve mass, and use optimal transport to assign one-step samples to geometrically compatible targets. The evidence is broad enough to keep, though the method adds training complexity and still depends on critic quality. This note is based on the full arXiv text.

## One-paragraph overview

OptiFlow targets offline RL settings where the behavior data contains multiple valid action modes but a deployed policy must sample in one step. Multi-step flow policies can model multimodality, but pointwise one-step distillation can collapse modes and direct critic maximization can exploit overestimated out-of-distribution regions. OptiFlow trains a value-aware reference flow policy and a one-step flow policy, samples actions from both for each state, constructs a value-weighted marginal over reference actions, and solves an entropic optimal transport problem that assigns one-step samples to high-value but nearby reference-policy actions.

## Model definition

### Inputs

Inputs are offline transition tuples of states, actions, rewards, and next states. During training, each state is paired with samples from a one-step policy and a multi-step value-aware reference flow policy, plus critic estimates for sampled actions.

### Outputs

The final output is a one-step stochastic policy that maps state and base noise directly to an action. The training procedure also outputs transport assignments from one-step samples to reference-policy action samples.

### Training objective (loss)

The method learns a critic from offline data, trains a value-aware reference flow policy with behavior regularization, and trains the deployed one-step policy by regression to transport-selected reference actions. The transport plan uses critic-estimated values in the reference marginal and action-space distances in the cost matrix, with entropic regularization solved by Sinkhorn iterations.

### Architecture / parameterization

The policy family is flow-based conditional action generation. In the reported implementation, OptiFlow samples N = 16 one-step-policy actions and M = 64 reference-policy actions per state, uses 30 Sinkhorn iterations, and then distills the maximum transport assignment for each one-step-policy sample.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Offline RL policies must improve on fixed data without drifting into unsupported actions. This is especially hard when the dataset has multiple good action modes and the deployed policy must be fast enough for one-step inference.

### 2. What is the method?

For each state, OptiFlow samples candidate actions from a reference flow policy and the one-step policy. It computes a value-weighted probability marginal over reference actions, then solves a state-wise entropic optimal transport problem between one-step samples and reference samples. The resulting assignments become distillation targets for the one-step policy.

### 3. What is the method motivation?

Value should choose which modes matter, but it should not directly pull the deployed actor through unreliable critic gradients. Geometry should keep assignments near plausible reference samples, but pure nearest-neighbor matching ignores which modes are high value. OT gives a place to combine both.

### 4. What data does it use?

The experiments use OGBench single-task navigation and manipulation variants, OGBench visual tasks, and D4RL AntMaze and Adroit tasks.

### 5. How is it evaluated?

It is evaluated against BC, IQL, ReBRAC, IDQL, IFQL, FQL, and GFP. Metrics are success rates or normalized returns depending on the benchmark, averaged mostly over 8 seeds, with 4 seeds for visual tasks.

### 6. What are the main results?

On OGBench state-based tasks, OptiFlow reaches a 48.3 +/- 0.4 average, above GFP at 45.6 +/- 0.4 and FQL at 39.0 +/- 0.4. On OGBench manipulation, it reaches 44.5 +/- 0.5 versus 40.8 +/- 0.5 for GFP and 36.3 +/- 0.4 for FQL. On OGBench visual tasks, it reaches 75.9 +/- 1.3 versus 65.4 +/- 1.8 for FQL and 57.7 +/- 1.0 for GFP. On D4RL AntMaze it averages 86.6 +/- 0.7, above GFP at 82.6 +/- 1.5. Ablations show the gain is not just more sampled actions: FQL and GFP variants with 64 sampled actions still do not close the gap. OptiFlow-BC also improves over FQL with matched weak references, supporting the distillation mechanism itself.

### 7. What is actually novel?

The novelty is treating one-step flow-policy learning as value-weighted sample allocation. The critic shapes the target distribution, but the actor is trained through transport-guided in-distribution assignments rather than direct critic maximization.

### 8. What are the strengths?

The method addresses a real failure mode in multimodal policy distillation. The diagnostics make the mode-collapse story plausible. The ablations separate reference quality, sampling budget, value weighting, and direct Q maximization. The strongest gains appear in manipulation and visual OGBench, where multimodal action structure is likely to matter.

### 9. What are the weaknesses, limitations, or red flags?

The method is more complex than standard actor extraction and introduces transport hyperparameters, reference-policy sample count, value-weighting temperatures, and Sinkhorn cost. Some navigation tasks still favor GFP or ReBRAC. The method remains dependent on critic estimates and reference-policy candidate quality, even if it avoids direct actor maximization.

### 10. What challenges or open problems remain?

The main open problem is whether the transport objective remains stable in very high-dimensional action spaces, long-horizon closed-loop deployment, and online fine-tuning with distribution drift. Another is how to choose transport temperatures without task-specific tuning.

### 11. What future work naturally follows?

Test transport-guided one-step policies in real robot imitation/offline RL datasets, combine the assignment with uncertainty over critic values, and study whether transport plans reveal distinct behavioral modes that can be inspected or constrained.

### 12. Why does this matter for cabbageland?

This is a clean example of separating selection pressure from representation support: value chooses which behavior modes matter, while transport keeps learning anchored to plausible action geometry. That is exactly the kind of mechanism cabbageland tends to steal.

### 13. What ideas are steal-worthy?

Use value as a marginal, not a direct actor gradient. Distill via assignments rather than pointwise noise matching. Evaluate whether a one-step policy preserves multimodal structure, not just average return. Treat sample allocation as the missing interface between expressive teacher and cheap deployed policy.

### 14. Final decision

Preserve. This is not the deepest theory paper in the batch, but the mechanism is portable and the ablations are useful.
