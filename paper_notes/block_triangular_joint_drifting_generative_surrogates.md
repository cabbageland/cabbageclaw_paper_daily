# One-Step Generative Surrogate Models via Block-Triangular Joint Drifting

## Basic info

* Title: One-Step Generative Surrogate Models via Block-Triangular Joint Drifting
* Authors: Nicholas Geissler, Shreya Jha, Ricardo Baptista, Benjamin Peherstorfer
* Year: 2026
* Venue / source: arXiv:2609.26435
* Link: https://arxiv.org/abs/2609.26435
* Date surfaced: 2026-09-23
* Why selected in one sentence: It learns one-step stochastic transition models from ordinary trajectory pairs by using a block-triangular joint distribution construction.

## Quick verdict

Highly relevant. This is a clean stochastic-world-model paper: it changes the distribution being learned so that the desired conditional transition becomes accessible from available data. Full arXiv text was inspected.

## One-paragraph overview

For stochastic dynamics, a useful surrogate must sample a distribution over next states conditioned on the current state. Standard trajectory data usually gives only one realized next state for each current state, which is not enough to estimate a conditional distribution directly. Block-triangular joint drifting solves this by applying drifting to the joint law of consecutive states, where samples are available as trajectory pairs, while constraining the learned map to keep the current-state component fixed. The second component then becomes a direct conditional next-state sampler. The payoff is fast rollout: one neural-network evaluation per time step, with no reverse diffusion loop, flow integration, or teacher distillation.

## Model definition

### Inputs

Inputs are trajectory pairs `(X(t), X(t+1))`, the current state at rollout time, a noise variable, and a time index or conditioning variable. For high-dimensional PDE examples, inputs may pass through learned latent features.

### Outputs

The learned generator outputs a sampled next state conditioned on the current state. Autoregressive rollout gives stochastic trajectories and trajectory-dependent quantities of interest.

### Training objective (loss)

The method uses a projected drifting loss on the empirical joint law of consecutive states. The drifting field is built from a Sinkhorn-style distribution-dependent field, then projected onto the second block so the first block remains the current state.

### Architecture / parameterization

The generator has a block-triangular form: the first component is fixed to the conditioning current state, and the second component is a learnable map from current state, noise, and time to next state. The experiments use problem-dependent neural networks, including MLP-like models and latent CNN/U-Net-style generators.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It solves the data-access problem in learning stochastic transition laws: a trajectory dataset provides joint samples of consecutive states but not repeated samples from the same current state.

### 2. What is the method?

The method learns the joint law of consecutive states under a block-triangular parameterization. By preserving the first block and drifting only the second block, the model recovers a conditional sampler for the next state.

### 3. What is the method motivation?

Diffusion and flow models can learn rich conditional dynamics but are expensive during rollout because each time step needs many denoising or integration steps. One-step models are fast, but direct conditional drifting lacks the right target samples. The joint construction fixes that mismatch.

### 4. What data does it use?

The experiments use simulated stochastic dynamics: Duffing oscillator, Rayleigh-Benard convection, stochastic Burgers, and two-dimensional forced turbulence.

### 5. How is it evaluated?

The paper compares marginal distribution errors, trajectory-dependent quantities of interest, energy and enstrophy errors, visual rollout quality, and number of neural function evaluations per time step against deterministic surrogates, marginal diffusion, learned SDEs, autoregressive diffusion, conditional flow matching, MeanFlow, and ReFlow-style distillation.

### 6. What are the main results?

BTJD achieves the lowest reported errors across several systems while using one function evaluation per step. On Duffing, it has the lowest marginal and trajectory-QoI errors under both random and fixed initial conditions. On stochastic Burgers, it reduces enstrophy error to 5.87e-2 versus 1.40e-1 for the next-best ReFlow+Distill baseline. On turbulence, it reduces energy error by roughly a factor of four and enstrophy error by almost a factor of three over the next-best baseline.

### 7. What is actually novel?

The novelty is the block-triangular joint-drifting construction: learn from the empirically accessible joint transition law while exposing the desired conditional through architecture.

### 8. What are the strengths?

The paper solves a real mismatch between data and objective. It also evaluates trajectory-dependent statistics, which matters because matching time marginals alone can hide broken dynamics.

### 9. What are the weaknesses, limitations, or red flags?

The experiments are simulation-based, and the method depends on the quality of trajectory data and the chosen latent representation for high-dimensional systems. Sinkhorn-style drifting and particle sampling may also carry training cost even if inference is cheap.

### 10. What challenges or open problems remain?

The big challenge is applying this to messy partial-observation settings where the state is not cleanly known. Another is understanding long-horizon error accumulation when the learned conditional is rolled out far beyond the training horizon.

### 11. What future work naturally follows?

Natural follow-ups include learned latent state versions for video/world models, uncertainty-calibrated rollouts, and combining BTJD with explicit physical constraints or control inputs.

### 12. Why does this matter for cabbageland?

Cabbageland cares about world models and reusable transition abstractions. This paper is a good pattern for making the conditional transition law learnable without pretending the dataset contains repeated branches it does not contain.

### 13. What ideas are steal-worthy?

Steal the move of changing the target distribution to match the available data, then using structure to recover the object you actually wanted. Also steal the evaluation focus on trajectory-dependent quantities, not only marginal snapshots.

### 14. Final decision

Preserve. This belongs in the stochastic world-model and generative-surrogate pile.
