# Memory-Conditioned Diffusion Model for Generalized Langevin Dynamics

## Basic info

* Title: Memory-Conditioned Diffusion Model for Generalized Langevin Dynamics
* Authors: Minglei Yang, Sicheng He
* Year: 2026
* Venue / source: arXiv:2609.28371; Journal of Computational Physics manuscript
* Link: https://arxiv.org/abs/2609.28371
* Date surfaced: 2026-09-24
* Why selected in one sentence: It gives a compact explicit memory state for learning non-Markovian stochastic flow maps from observed trajectories.

## Quick verdict

* Highly relevant

This is a strong direct hit for world-model and stochastic-dynamics interests. The paper does not hide non-Markovianity inside a recurrent black box; it builds a multiscale exponential-filter memory and then learns conditional stochastic flow maps around that state. The limitations are mostly scope: the experiments are numerical and the memory-selection recipe is still handcrafted enough that real physical deployments would need care.

## One-paragraph overview

Generalized Langevin equations describe systems where the next resolved state depends on hidden unresolved degrees of freedom carried through history. This paper learns those dynamics from observed trajectories by compressing the past into a bank of recursively updated exponential filters. It then uses a kernel-based, training-free conditional diffusion estimator to sample next-step conditionals given the current observation and memory state, and distills those conditional samples into a neural flow map for autoregressive simulation. The result is a learned simulator that can preserve long-memory correlations and non-Gaussian burst statistics better than memoryless models, raw finite windows, or Gaussian-head LSTMs in the tested settings.

## Model definition

### Inputs

Inputs are observed trajectories of resolved variables. At deployment, the model conditions on the current observation and a recursively updated memory state made from exponential filters of past increments. Some experiments optionally project the memory bank into lower-dimensional predictive coordinates.

### Outputs

The conditional sampler and neural flow map output samples from the next-step increment or next resolved state distribution. Repeated sampling plus memory updates yields autoregressive trajectory simulations.

### Training objective (loss)

The score estimator for conditional diffusion is training-free: it estimates conditional scores from neighboring trajectory pairs rather than training a score network. The neural flow map is trained by supervised regression to the conditional samples produced by the reverse probability-flow sampler. The paper uses forecasting and rollout errors to choose and validate memory budgets.

### Architecture / parameterization

The memory representation is a multiscale exponential moving-average filter bank over observed increments. Conditional sampling uses a kernel-based score estimator and reverse probability-flow integration. The deployed simulator is a neural flow map, described in the experiments as a multilayer feed-forward network, conditioned on current observation and memory.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It tries to learn stochastic dynamics when the observed state is not Markovian. In such systems, a one-step law conditioned only on the current observation pools histories that should have different futures.

### 2. What is the method?

The method builds a recursively updated memory state from exponential filters across multiple time scales. It estimates conditional next-step distributions with training-free conditional diffusion and then distills those samples into a neural stochastic flow map for fast autoregressive simulation.

### 3. What is the method motivation?

Long raw windows make conditional estimation high-dimensional and brittle. A bank of exponential filters gives explicit memory scales with fixed update cost, making it a compact predictive state for fading-memory dynamics.

### 4. What data does it use?

The paper uses simulated trajectories from three numerical systems: a scalar linear GLE with multiscale memory, a two-dimensional viscoelastic GLE, and a stochastic model of intermittent scrape-off-layer plasma fluctuations.

### 5. How is it evaluated?

It evaluates memory representation quality, one-step conditional forecast distributions, autocovariance and long-time correlation behavior, autoregressive rollouts, Wasserstein forecast errors, and burst-tail statistics. Baselines include memoryless diffusion, raw-history conditioning, and LSTM models with Gaussian output heads.

### 6. What are the main results?

In the scalar GLE benchmark, the memory model has median normalized squared Wasserstein error 0.0040 against the exact full-history conditional law at the tested horizon, compared with 0.0145 for the LSTM and about 0.04 for memoryless and raw-history models. The slow-tail error is 0.087 for the memory model, while LSTM variants remain around 0.97 to 0.99 even with longer training contexts. In the scrape-off-layer example, memory plus diffusion has one-step excess error 0.0050 on quiet histories and 0.0113 on active histories, much lower than the moment-matched Gaussian and Gaussian-head LSTM. It also preserves skewed positive burst tails that the Gaussian LSTM suppresses.

### 7. What is actually novel?

The novelty is the combination of explicit multiscale memory, training-free conditional diffusion, and flow-map distillation for non-Markovian stochastic dynamics. The individual ingredients are familiar; the useful part is the clean assembly and error-separated evaluation.

### 8. What are the strengths?

The paper is careful about separating memory representation error from sampler and rollout error. It also uses physical examples where the hidden-memory problem is not decorative. The comparison with longer-context LSTMs is helpful because it shows that simply feeding more history does not automatically recover slow modes.

### 9. What are the weaknesses, limitations, or red flags?

The memory filters are interpretable but still selected with domain-informed diagnostics. The method is tested on controlled simulations rather than messy observed scientific data. Kernel score estimation can become difficult as conditioning dimension rises, which is why the memory compression matters so much.

### 10. What challenges or open problems remain?

Scaling to high-dimensional observations, learning memory rates rather than selecting them, and keeping conditional score estimation reliable under sparse data are the main open problems. Real systems may also have state-dependent memory that fixed exponential filters only approximate.

### 11. What future work naturally follows?

Good follow-ups include learned filter banks, hybrid explicit/recurrent memory, uncertainty diagnostics for memory adequacy, and applying the method to partial-observation physical simulators where burst or rare-event tails matter.

### 12. Why does this matter for cabbageland?

It is a useful pattern for world models: represent memory as an explicit, updateable state with known time scales, then train the generative transition around that state. That is much cleaner than hoping a context window magically contains the right past.

### 13. What ideas are steal-worthy?

Use multiscale exponential memory as a cheap persistent state. Evaluate representation, conditional sampler, and rollout separately. When the output law is skewed or multimodal, do not use a Gaussian head just because it is convenient.

### 14. Final decision

Preserve. This is a strong state/memory mechanism paper.
