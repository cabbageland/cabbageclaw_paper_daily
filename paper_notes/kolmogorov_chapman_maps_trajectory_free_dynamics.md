# Kolmogorov-Chapman Maps: Trajectory-Free Learning for Simulating Molecular Dynamics

## Basic info

* Title: Kolmogorov-Chapman Maps: Trajectory-Free Learning for Simulating Molecular Dynamics
* Authors: Majdi Hassan, Marta Skreta, Dominique Beaini, Kirill Neklyudov
* Year: 2026
* Venue / source: arXiv preprint, 2611.12880v1, submitted November 9, 2026
* Link: https://arxiv.org/abs/2611.12880
* Date surfaced: 2026-11-10
* Why selected in one sentence: A transition-density model separates known infinitesimal physics from learned consistency across time, without requiring paired future-state supervision.

## Quick verdict

* Highly relevant

Preserve the mechanism, not an inflated “physics solved” story. Time-gated normalizing flows anchor the local SDE, while a distributional composition objective learns longer transitions. The molecular results are useful, but rare-mode kinetic errors, per-system training, existing simulation-derived configurations, and substantial inference corrections delimit the claim.

**Read basis:** Full-text HTML main methods/results, proposition statements, and selected data/training/evaluation and inference-correction appendices. The interrupted HTML transfer was resumed to completion. No independent proof audit, code execution, or numerical reproduction.

## One-paragraph overview

KC-maps learns a conditional probability distribution over future states of a known stochastic differential equation. Rather than regress on pairs from recorded trajectories, it starts from unpaired configurations and known local drift/diffusion. A Gaussian reference and time-gated invertible corrections preserve short-time dynamics; a longer learned transition is trained by likelihood on samples produced by composing two shorter teacher transitions. For peptides, a late detailed-balance loss and inference-time force/momentum/proposal corrections help long rollouts. Tests show useful equilibrium exploration and GPU throughput on small molecular systems, while transition rates involving a sparsely represented mode remain inaccurate. “Trajectory-free” describes the supervision, not the provenance or cost of all input configurations.

## Model definition

### Inputs

An initial state, start/end times or elapsed duration, and random Gaussian noise. For overdamped Lennard-Jones systems the state is particle positions; for underdamped peptide dynamics it is positions and momenta. Known force fields, diffusion/friction, masses, atomic identities, source geometry, and reference-kernel statistics condition the molecular model. It is trained separately for each system, not conditioned on an arbitrary unseen molecule.

### Outputs

Samples from a finite-time conditional transition density and its tractable log density. The peptide map outputs new positions and momenta. Sequentially applying it generates stochastic rollouts; it predicts distributions, not the particular path associated with a specified Brownian realization.

### Training objective (loss)

The conceptual constraint is the Kolmogorov–Chapman identity: integrating the product of two intermediate transition kernels should recover the single longer transition kernel. Minimize KL between that composed distribution and the direct kernel, while preserving the prescribed short-time limits.

The practical stop-gradient/EMA target construction samples `x' ~ q_eta(s,r | x)` and `y ~ q_eta(r,t | x')`, then minimizes `E[-log q_theta(s,t; y | x)]`. Gradients do not propagate through the teacher-generated endpoints. This is likelihood against composed model targets, not likelihood on observed future states and not differentiation through the full self-dependent KL.

Peptide models add a detailed-balance KL near the end of training. Practical losses also normalize by degrees of freedom and cap per-sample NLL; those interventions belong in a reproduction. An alternative probability-flow velocity objective is compared, not the main peptide recipe. Exact kernel identification/global-optimum arguments do not establish convergence of finite EMA training.

### Architecture / parameterization

Conditional affine-coupling normalizing flows around a time-scaled Gaussian reference. Bounded learned corrections and duration gates preserve the no-jump and infinitesimal-moment boundary conditions under the stated assumptions. Second-order Langevin dynamics receives position/momentum-specific gates and a free-flight term. Transformer conditioners use source/reference features; molecular implementations center configurations, work in a source-defined rotation frame, and track center-of-mass behavior separately. Peptide models have about 46.6M parameters; this is not merely an unconstrained transformer with a physics label.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Molecular simulation uses tiny stable timesteps, while meaningful conformational transitions occur much later. Learned coarse transitions can skip numerical steps, but conventional supervision first requires generating long paired trajectories. The goal is to learn finite-time stochastic transitions using local physical laws and unpaired states instead.

### 2. What is the method?

1. Build a transition-density family with the correct infinitesimal behavior.
2. Draw initial configurations, time intervals, and intermediate times.
3. Compose two teacher-kernel transitions to produce an endpoint.
4. Fit a single student transition to that endpoint by NLL; update the teacher through EMA.
5. For peptides, add late detailed-balance training and use the documented corrections when rolling out.

The architectural anchor prevents consistency from selecting an arbitrary self-consistent process unrelated to the governing SDE.

### 3. What is the method motivation?

A known SDE determines local drift and noise. A valid Markov transition family must compose across time. Combining those constraints identifies the desired transition law under the paper's regularity assumptions, making local equations useful supervision for long stochastic steps. It is the distributional analogue of deterministic flow-map consistency.

### 4. What data does it use?

LJ-13 and LJ-55 configurations, including target-temperature public data and a higher-temperature NUTS setting. Peptides are AL2, AL4, and AL6, with 22, 42, and 63 atoms. Their source configurations come from existing MD datasets; random train/validation/test splits are 800K/100K/100K, 560K/70K/70K, and 240K/30K/30K respectively. Training ignores trajectory order and paired transitions; source momenta are sampled independently with augmentation. Known molecular energies/forces are checked against OpenMM.

Random configuration splits are not independent molecular-system generalization, and unpaired data is not free data. Higher-temperature LJ training is a useful demonstration of sourcing configurations beyond the target equilibrium, not evidence that arbitrary source support suffices.

### 5. How is it evaluated?

- LJ: energy and geometric Wasserstein distances, using Metropolis–Hastings-corrected learned proposals; compare MALA and published trajectory-free samplers.
- Peptides: energy, torsion, and TICA-distribution distances against long MD references; aggregate simulated time and mode discovery per GPU-hour.
- AL2 kinetics: mode mean first-passage times, occupancy autocorrelations, and supplementary transition probabilities.
- Ablations: Gaussian-reference stabilization, time priors, conditioning features, gate orders, teacher updates, detailed balance, and parameterization.

Peptide sampling budgets are one L40S GPU-hour with four CPU cores, excluding compilation/initialization; chain counts and step sizes are swept. AL4/AL6 HFM training is matched in estimated FLOPs, not parameter count: HFM has about 9.09M parameters versus KC-maps' 46.58M. Distribution metrics average repeated sample draws, which are not independent model-training seeds.

### 6. What are the main results?

The model learns transitions up to 100 fs on the three peptide systems. The paper reports about 2.3× AL6 aggregate simulation throughput over MD on one L40S, with faster mode discovery: three of four TICA modes reached while MD misses two after one hour. At matched sampling budgets KC-maps has the lowest reported TICA distance across all three molecules while remaining competitive on energy/torsion measures.

Kinetic agreement is mixed. Several common AL2 modes have useful first-passage and autocorrelation agreement, but entering a sparsely represented mode is too slow and its long-lag occupancy autocorrelation decays too rapidly. Broad equilibrium exploration—including some AL6 configurations outside training coverage—does not remove that limitation.

### 7. What is actually novel?

The concrete contribution is a tractable SDE transition-density flow with infinitesimal constraints built into its parameterization, trained through model-generated Kolmogorov–Chapman consistency instead of observed transition pairs. It belongs to stochastic flow-map research; neither the semigroup identity nor the general idea of amortizing integration is new. Unlike deterministic Hamiltonian maps plus a separate thermostat, it learns a stochastic transition kernel directly.

### 8. What are the strengths?

A legible division between physical boundary conditions and learned timescale composition; tractable density evaluation; stochastic rather than deterministic state prediction; explicit comparison of equilibrium and kinetics; relevant system/correction ablations; and matched sampling budgets rather than only per-step claims. Reporting rare-mode errors is more informative than declaring equilibrium histograms sufficient evidence of faithful dynamics.

### 9. What are the weaknesses, limitations, or red flags?

- Known drift/diffusion is a major privilege. This is not identification of unknown physics from video.
- Each system gets its own trained model; transfer to unseen molecules is not demonstrated.
- Source configurations still have acquisition cost and determine coverage. Existing MD-derived random splits do not establish novel-system or long-time independence.
- Force capping, momentum adjustment, angular-momentum handling, and fresh-noise retries with step-size reduction materially affect deployed behavior. The raw learned kernel's theorem is not automatically a theorem for that corrected procedure.
- Learned long steps do not guarantee accurate rare-event kinetics, even with good equilibrium statistics.
- Sampling throughput is not end-to-end savings: training, dataset generation, startup, and compilation require separate amortization accounting.
- LJ's Metropolis correction and peptide correction stack differ. Do not casually transfer exact-equilibrium claims between their samplers.

### 10. What challenges or open problems remain?

Quantify composition and kinetic errors at finite training loss; distinguish improvements due to the map from improvements due to corrections; cover rare states without prohibitive reference simulation; scale to larger molecules; and understand when known local physics plus limited support determines reliable long-time behavior in practice.

### 11. What future work naturally follows?

Train across molecular systems; deliberately acquire rare-mode configurations; compare uniform versus coverage-aware source sampling; measure transition fidelity before/after each correction; test non-equilibrium forcing; and publish total-cost break-even curves. A learned-drift extension would need separate identification and uncertainty checks, not just reuse the current guarantee.

### 12. Why does this matter for cabbageland?

It gives an operational definition of useful structure in a stochastic world model: anchor the infinitesimal process, then constrain composition of conditional distributions. For learned simulators, stable long rollouts, correct stationary samples, and correct intervention/transition responses should remain separate evaluation axes. This is strong cross-domain design inspiration even if molecular dynamics is not the eventual application.

### 13. What ideas are steal-worthy?

- Split known local behavior from learned long-horizon behavior rather than forcing one network to discover both.
- Use an expressive conditional density so composition can be trained without collapsing stochastic futures to a mean.
- Distill multiple short teacher transitions into one longer step, while auditing whether teacher errors self-reinforce.
- Include kinetics and rare-state coverage alongside endpoint distribution metrics.
- Treat inference corrections as named components of the method, with their own accuracy and cost ablations.

### 14. Final decision

Preserve as a highly relevant structured stochastic-simulation mechanism. Carry four qualifications into every reuse: known physics, non-free source configurations, per-system training, and no demonstrated exact kinetics for the practical corrected sampler. The next experiment to steal is a composition-plus-local-anchor ablation, not the headline speedup alone.
