# Look Back: Reinforcement Learning with Counterfactual World Models

## Basic info

* Title: Look Back: Reinforcement Learning with Counterfactual World Models
* Authors: Jinwoo Kim, Toghrul Abbasov, Lucius E.J. Bynum, Aahlad Puli, Stephanie Milani, Hyunwoo Ryu, Seunghoon Hong, Kyunghyun Cho, Rajesh Ranganath
* Year: 2026
* Venue / source: arXiv preprint, submitted November 22, 2026
* Link: https://arxiv.org/abs/2611.29259
* Date surfaced: 2026-11-24
* Why selected in one sentence: Uses observed experience to hold environmental luck fixed while estimating action effects, reducing the world-modeling burden and exposing precise conditions for policy-gradient improvement.

## Quick verdict

Highly relevant

Preserve the counterfactual-model interface and coupled-branch estimator, not a claim of universal causal identification. The construction is especially useful when environmental evolution is hard but action-dependent edits are simple. Learned counterfactuals can bias gradients, and the diffusion implementation buys sample reuse with substantial wall-clock cost.

## One-paragraph overview

Ordinary model-based branching imagines independent futures, mixing action differences with random environmental events. A counterfactual world model instead conditions on a factual transition and predicts another state/action's next state under the same underlying environmental noise. This can be learned from same-noise transition pairs, or induced from an ordinary diffusion WM by inverting a factual outcome to latent noise and regenerating under changed conditioning. REINFORCE Look Back (RLB) groups a factual trajectory with counterfactual branches, uses fresh policy randomness, and subtracts leave-one-out branch returns in the policy-gradient estimate. The paper connects this to common random numbers, gives conditional bias/variance and model-learning results, and tests contextual bandits, multi-agent bandits, and a modified Chrome Dino game.

**Inspection basis:** Primary full PDF: main definitions/theorem statements and all main experiments; selected appendices on assumptions, architectures, splits, inversion, leakage and runtime. Proofs were not independently verified. [PDF](https://arxiv.org/pdf/2611.29259). [Code landing page](https://github.com/ToghrulAbbasov19/look-back) resolved; no code execution or reproduction.

## Model definition

### Inputs

An ordinary WM takes current state x and action a. A CWM additionally receives a factual transition o = (factual state, factual action, factual next state). Each counterfactual rollout uses the corresponding factual transition at each time, even after its own state has diverged. Policy randomness is freshly sampled; environmental noise is coupled through the factual reference.

Dino's policy sees four grayscale 128x64 decision frames. Its diffusion model is trained on RGB frames encoded through a pretrained VAE, conditioned on eight preceding frames and an action.

### Outputs

A next-state/next-frame counterfactual distribution, not a causal explanation in language. The policy emits discrete actions. In Dino a separately trained frozen visual classifier assigns collision/no-event/obstacle-clear rewards to generated transitions. The policy gradient uses observed and modeled returns.

### Training objective (loss)

Paired CWM training minimizes next-state negative log likelihood conditioned on alternative state/action plus the factual transition. Both paired directions are used; a corresponding ordinary WM uses the same paired members as separate observations. Bandit models predict Gaussian mean/scale and optimize likelihood.

For unpaired Dino data, train an ordinary conditional diffusion U-Net with the velocity-prediction objective; invert the factual transition with DDIM, then regenerate using the same latent under changed conditioning. No extra paired CWM training is required for this route.

RLB estimates the discounted policy gradient with terms proportional to `grad log pi(a|x) * (return - mean(other group returns))`, averaged across m branches. Policy updates include entropy regularization. The model, visual reward classifier and policy are distinct learned components; this is not a single end-to-end causal loss.

### Architecture / parameterization

Bandit policies are linear softmax heads. Bandit WMs/CWMs have two hidden layers of eight SiLU units, Gaussian outputs and a linear mean connection. Dino uses a three-layer convolutional policy and a 101M-parameter conditional diffusion U-Net, pretrained VAE and learned action embedding. Models are trained offline and frozen during policy learning.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Environmental luck obscures policy credit, and a full WM may waste capacity predicting nuisance evolution unrelated to the intervention. Independent model-generated branches do not fix either problem just by increasing sample count.

### 2. What is the method?

Represent transitions as x_next = f(x,a,u). Condition counterfactual outcomes on the posterior of u implied by factual experience. Either learn this conditional edit from matched-noise pairs or infer/reuse diffusion latent noise. Generate coupled branches, then compute leave-one-out policy-gradient advantages.

### 3. What is the method motivation?

Predicting what changes under an intervention can be simpler than predicting everything that happens. Sharing nuisance variation also cancels part of its contribution to return variance. It helps most when luck dominates interaction between action and noise; it need not help when actions fundamentally alter the nuisance process.

### 4. What data does it use?

Constructed contextual bandits, coupled multi-agent bandits, and modified Chrome Dino. Bandit model datasets contain same-noise pairs. Dino's offline WM uses 1,000 episodes of 150 decisions, or 150,000 observed decisions, and trains for 9,000 steps. This is not a real-world deployment dataset.

### 5. How is it evaluated?

Compare REINFORCE, learned-value baselines, CCA, RLOO and RLB, using ground-truth branches or frozen WMs/CWMs. Bandit plots distinguish real-interaction accounting from accounting that includes imagination; six randomized trials test noise/agent-count changes.

Dino uses 15 policy-training seeds, 2,000 updates and m=4 groups. One checkpoint index per method is selected by mean performance on separate validation episodes across seeds, then evaluated on 100 test episodes per seed. Survival terminates at first collision and is capped at 375 decisions. Reported +/- values are seed standard deviations, not confidence intervals. Counterfactual quality includes composition, effectiveness, realism and minimality diagnostics.

### 6. What are the main results?

RLB remains effective as contextual noise or the number of other agents increases, with CWM learning easier than ordinary WM learning in the constructed regimes. At matched real interactions, learned CWMs can beat costly simulator branching.

On Dino, RLB+CWM reports collision rate 3.77% +/- 1.15 and survival 109.0 +/- 18.9 decisions versus RLOO+WM's 7.89% +/- 14.10 and 97.5 +/- 28.2. With true counterfactuals RLB reaches 3.29% +/- 0.36 and 113.9 +/- 7.9. CWM image FID is 15.94 versus ordinary WM's 37.72, but conditioning on the factual outcome supplies additional information, so this is not a like-for-like unconditional prediction task.

Theorems establish unbiasedness for exact counterfactuals with independent parameter-independent SCM noise and fresh policy randomness. Variance reduction requires sufficient environmental-luck dominance. For learned CWMs, bias is bounded by branch expected-return error times a policy-score bound; it is not zero by construction.

### 7. What is actually novel?

The integrated counterfactual transition interface, conditions for easier modeling, and RLB estimator/model-error analysis. SCMs, common-random-numbers variance reduction, hindsight baselines and diffusion inversion are prior ingredients. Reusing the same prompt or initial state alone is not equivalent to sharing the subsequent environment noise.

### 8. What are the strengths?

A mechanism that identifies what information the model no longer needs to generate. Explicit paired/unpaired routes; shared-underlying-WM comparison; conditional rather than blanket variance claims; useful appendix audits of inversion error, action leakage and compute.

### 9. What are the weaknesses, limitations, or red flags?

The bandits deliberately favor nuisance cancellation. Dino is small and modified to make jump/duck/stand consequential; no broad continuous-control or robot transfer follows. Observational data do not identify a unique physical SCM. Exact counterfactuals of any MDP-consistent SCM can give unbiased gradients under the stated conditions, but their variance differs; an arbitrary learned editor need not be MDP-consistent.

Inverted Dino noise predicts factual action with 98% accuracy. A generated-counterfactual classifier found no additional leakage beyond context/new action, which is reassuring but not a causal guarantee. At ten inversion steps, an appendix rollout diagnostic still finds missing/invented obstacles in 9.9% of generated frames. Learned visual rewards and distribution shift are additional error sources.

CWM policy training takes 74.95 minutes per 100 updates versus WM's 58.91 on one RTX 3090, about 27% slower. Simulator methods take about 7–8 minutes. Offline diffusion training additionally uses eight GPUs for 2h15m. Sample efficiency is not compute efficiency.

### 10. What challenges or open problems remain?

Can factual randomness remain meaningfully reusable after long action-induced state divergence? When can partial observations recover useful noise without leaking actions into baselines? Can counterfactual return error be controlled under changing policies rather than only on the training distribution?

### 11. What future work naturally follows?

Test continuous control, hidden-state environments and strong action-noise interactions; independently evaluate reward-model error; measure actual gradient bias/variance at matched compute; use sparse branching and faster diffusion. Compare paired training, induced counterfactuals, ordinary shared-seed simulation, and independent branches on the same data/model budget.

### 12. Why does this matter for cabbageland?

It decomposes model capacity around the intervention rather than assuming a complete predictive universe is necessary for useful control. “Counterfactual” earns a formal SCM definition here, but the practical approximation still needs testing. This is a useful world-model/RL design lesson without generic agent branding.

### 13. What ideas are steal-worthy?

- Expose factual transitions as an explicit conditioning interface for intervention models.
- Couple environmental uncertainty while keeping policy randomness independent.
- Evaluate edits on composition, intervention effectiveness and nuisance preservation separately.
- Measure return error and gradient bias, not just image fidelity.
- Keep real samples, offline model data, model calls and wall-clock as separate budgets.

### 14. Final decision

Preserve as a high-value RL/world-model mechanism paper. The next experiment should test where luck cancellation breaks, not merely reproduce another favorable stochastic bandit. Treat diffusion counterfactuals as useful approximations, never automatic causal certificates.
