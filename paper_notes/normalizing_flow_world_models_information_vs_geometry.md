# Normalizing Flows are Capable World Models

## Basic info

* Title: Normalizing Flows are Capable World Models
* Authors: Zijia Li, Yong-Hyun Park, Shusheng Yang, and Jiatao Gu
* Year: 2026
* Venue / source: arXiv preprint, 2611.33872v1
* Link: https://arxiv.org/abs/2611.33872
* Date surfaced: 2026-11-27
* Why selected in one sentence: An invertible likelihood-trained state supports stochastic prediction and control, while unusually useful ablations show why information retention alone does not provide decision geometry.

## Quick verdict

* Highly relevant

Preserve the construction and the evaluation decomposition, not a claim that normalizing flows universally beat JEPA or Dreamer. The useful result is a workable information-preserving predictive state with separate interfaces for rewards and goals. Its own scorer and cost diagnostics sharply limit the headline: exact observation likelihood neither makes the latent state compact nor makes Euclidean distance a task criterion.

## One-paragraph overview

NFWM replaces an observation flow's fixed base density with a history- and action-conditioned predictive density. Joint conditional maximum likelihood learns the invertible image coordinates and next-state distribution together; predictions roll forward in latent space, and inverse decoding makes imagined images inspectable. A likelihood-only backbone supports Flappy Bird planning after reward/termination heads are fitted. For goal-distance control, an inverse-dynamics auxiliary loss makes action-relevant differences more accessible. Separate simulator experiments cover deterministic control, branching Teleport dynamics, a custom LIBERO candidate-ranking task, frozen-feature action experts, and policy learning inside a stochastic Boxing model. The paper distinguishes prediction quality from the quality of the function that scores a prediction.

## Model definition

### Inputs

RGB observations, action embeddings, and a bounded observation/action history. Context length and action-block layout vary by experiment, not one universal agent configuration. The main deterministic-goal protocol begins from one observation, predicts five blocks of five raw actions toward a goal image 25 raw steps away, and can plan twice within 50 execution steps. Goal images enter the decision cost; they are not a universal conditioning input to the learned dynamics. LIBERO candidate ranking uses one external camera and seven-dimensional actions.

### Outputs

The encoder emits full-dimensional latent patch tokens. A temporal transformer predicts a conditional mean and positive diagonal standard deviations for the next latent state; sampling gives the next imagined state. Inverting the encoder produces an observation, with optional score-denoising for visualizations. Separate trained heads predict rewards/termination; an inverse-dynamics model predicts action embeddings from neighboring observed states. Imagination-trained actor/critic outputs and frozen-feature action experts are downstream components, not the density model itself.

### Training objective (loss)

With z = Enc_theta(o), the world-model loss is:

`L_nll = -log p_phi(z_next | history, action) - log |det J_Enc_theta(o_next)|`.

Both encoder and predictor receive gradients. The main diagonal-Gaussian density contributes a variance-weighted squared error plus log-standard-deviation terms. Gaussian observation noise is added during training: exact likelihood refers to that noise-smoothed observation distribution.

For goal-distance configurations, add `lambda_inv * ||IDM(z_t,z_next) - stopgrad(action_embedding)||^2`. Flappy Bird uses lambda_inv = 0, then fits task heads on the frozen backbone; it is not an entirely reward-free agent. Boxing fits task heads and trains an actor–critic on imagined returns with a KL penalty to the frozen behavior-cloned actor. These objectives belong to distinct stages/configurations.

### Architecture / parameterization

TARFlow-style invertible transformer observation encoder, action MLP, and action/history-conditioned transformer density predictor. The default generates all next-frame patch parameters in parallel. A more expressive token-wise variant additionally autoregresses within a frame. The invertible latent has observation dimensionality, not a compressed bottleneck. An inverse-dynamics query readout/MLP and task-specific learned heads expose information for decisions.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Learn representations and probabilistic dynamics jointly while keeping future observations recoverable and allowing decisions without rendering every candidate future. Point-prediction latent models can average incompatible futures; video predictors can be costly and expose a poor distance for planning. NFWM asks whether a flow-based state can bridge prediction, inspection, and control.

### 2. What is the method?

Use change of variables to turn latent predictive density into conditional image density. Roll sampled latent states into the history. For reward-based planning, fit task readouts and optimize imagined return using CEM. For goal planning, sample intermediate futures but compare the terminal conditional mean to the encoded goal. For policy learning, start an actor with behavior cloning and improve it through predicted experience. Optional inverse dynamics changes the coordinates used by the goal cost.

### 3. What is the method motivation?

Invertibility excludes constant representation collapse without a separate anti-collapse regularizer and retains image information. Likelihood trains the predictive distribution and coordinates together. But an invertible rescaling can leave reconstruction intact while changing every Euclidean ranking: the motivation for inverse dynamics is task geometry, not information recovery.

### 4. What data does it use?

Offline, simulator-generated image/action trajectories, with separate models per benchmark. Deterministic training/validation splits are episode-held-out: Push-T has 16,816/1,869 episodes, and Cube, Reacher, and TwoRoom each have 9,000/1,000. Teleport uses 20,000 training episodes including paired stochastic branches. The custom LIBERO-PRO mug-on-plate dataset has 18,685 episodes and approximately 70% successes/30% failures. Boxing combines ten PPO checkpoints and randomizes the unseen opponent's action with probability 0.5. These are controlled simulator data, not broad real-world video.

### 5. How is it evaluated?

Held-out closed-loop Flappy Bird levels; deterministic CEM goal planning; open-loop Teleport branching; fixed shared LIBERO candidate pools, with full-sequence execution; separately trained frozen-feature action experts across 40 LIBERO tasks; and Boxing actor improvement through imagination. Main NFWM/LeWM/SMWM results generally average three training runs, but several ablations and Wan comparisons use one. Controls include full-patch baseline states, likelihood versus MSE/inverse-dynamics objectives, and scoring actual simulator endpoints instead of predicted ones.

### 6. What are the main results?

- Flappy Bird: 10/10 held-out games reach the 100-pipe stopping cap, with likelihood-only backbone training followed by task heads.
- Four deterministic tasks: 84.5% average success, versus LeWM 82.5% and SMWM 74.8%; this is a modest average lead, not dominance on each task.
- Teleport: 37.3 ± 2.3%, versus 11.3 ± 7.6% and 33.3 ± 4.6%. A single token-wise run reaches 25/50 cases, at much higher cost.
- Custom LIBERO ranking: 46.0 ± 3.5% versus 23.3 ± 2.3%/32.7 ± 4.2%. Oracle simulator-endpoint scoring raises NFWM only to 54.0 ± 2.0%.
- Boxing: 77.37 ± 9.28 return versus 64.47 ± 6.32 for three-frame-restricted DreamerV3, with improvement over NFWM's behavior-cloned starting policy in all three runs.
- One-run Push-T objective ablation: 86% full model versus 34% without inverse dynamics, and 28%/40% for clean/noisy forward-MSE substitutions.

### 7. What is actually novel?

The contribution is the demonstrated combination of jointly likelihood-trained invertible observation coordinates, conditional latent dynamics, and direct latent decision interfaces. Flows, conditional video densities, inverse dynamics, and imagination RL are prior ingredients. The evidence does not establish the first probabilistic world model, first generative JEPA alternative, or universally sufficient planning metric.

### 8. What are the strengths?

The model earns the world-model label through action-dependent counterfactual predictions and downstream decisions, not image reconstruction alone. Stochastic prediction and imagination improvement are tested separately. The simulator-endpoint ranking control distinguishes a bad forecast from a bad cost. State-size, objective, and token-wise-prediction checks make the trade-offs unusually legible.

### 9. What are the weaknesses, limitations, or red flags?

The complete state is expensive. Push-T decisions cost 10.038 seconds for NFWM versus 0.286 for compact LeWM; full-patch LeWM costs 10.478 seconds. The token-wise Teleport variant is 22.3x slower per planning decision than the parallel one. Models/tasks and decision procedures are separately configured. Dreamer is intentionally context-restricted; Wan has one training run and a different VAE goal geometry. The robot ranking experiment is one custom task; the 40-task action experts are not that same ranking evaluation. PCA pictures do not prove good geometry. Invertibility retains nuisances as well as useful state.

### 10. What challenges or open problems remain?

Task-aware outcome scoring remains weak: even actual simulator endpoints produce only 54% top-one success. Final Mean scoring drops terminal variance and is not expected-risk minimization. A diagonal latent density need not express all dependencies efficiently. Exact observation density is not calibrated dynamics uncertainty, especially not epistemic uncertainty under novel physics. Real observations, shared multitask training, and longer-horizon drift are unresolved.

### 11. What future work naturally follows?

Train a task-success readout and compare it against image-goal distance on identical oracle/predicted endpoints. Match compact and full-state competitors on time, context, and data. Compare mean-only, expected-distance, and risk-sensitive scoring at fixed rollout budgets. Test out-of-distribution branches and calibration independently of generation. Explore a compact decision state paired with an invertible audit path, without claiming the compact state preserves all pixels.

### 12. Why does this matter for cabbageland?

It provides a clean architecture question: what must be retained, what must be predicted, and what must be made geometrically easy for a controller? The separation is useful across world models, generative media, and explicit-state systems. A representation can be perfectly reconstructible and still have the wrong interface for deciding what to do.

### 13. What ideas are steal-worthy?

- Audit the scorer with true future states before spending effort on a better predictor.
- Treat invertibility as an information guarantee, not task abstraction.
- Learn decision geometry explicitly and ablate it separately from density learning.
- Keep decoding optional for action selection but available for inspection.
- Report both state-size-matched controls and wall-clock cost; neither alone is sufficient.

### 14. Final decision

Preserve as a useful flow-based world-model design and a particularly good prediction-versus-scoring diagnostic. Read alongside uncertainty work, not as its solution. Any reproduction should begin with the goal-cost bottleneck and matched compute, not another reconstruction gallery.

## Reading scope and provenance

Based on the accessible full PDF: main method, experiments, discussion, limitations, and selected appendix data/splitting/planning protocols. Not an abstract-only summary. Proofs, the entire appendix, visual galleries, and code were not exhaustively audited; results are author-reported. Primary [PDF](https://arxiv.org/pdf/2611.33872); supplemental [AlphaXiv landing page](https://www.alphaxiv.org/abs/2611.33872).
