# Conservation Buys Stability and Factoring Buys Counterfactuals in Physical World Models

## Basic info

* Title: Conservation Buys Stability and Factoring Buys Counterfactuals in Physical World Models
* Authors: Yufeng Wang, Parivesh Priye, Lu Wei, Haibin Ling
* Year: 2026
* Venue / source: arXiv:2609.19674
* Link: https://arxiv.org/abs/2609.19674
* Date surfaced: 2026-09-20
* Why selected in one sentence: It cleanly separates two different physical-world-model failures and shows which structural prior fixes each one.

## Quick verdict

* Must read

This is one of the better world-model structure papers because the claim is not "add physics" in the abstract. It tests conservation and coupling factorization as separable commitments, then shows a double dissociation: conservation stabilizes long rollouts, while factorization enables changed-law transfer. This note is based on the full arXiv PDF text.

## One-paragraph overview

The paper studies learned physical simulators under two failures: long-horizon drift and counterfactual failure when a physical coupling changes outside the training regime. The core model is a learned Hamiltonian evolved with a symplectic update, optionally with the interaction potential factored so that a coupling parameter enters linearly. On a three-body gravity setup trained only on attractive gravity, the symplectic structure keeps rollouts bounded while the factored coupling lets the model follow an unseen repulsive-gravity law. The paper then repeats the separation across formalisms, larger object counts, alternate force families, pixel-grounded state estimation, contact, and dissipative variants.

## Model definition

### Inputs

The main experiments use physical states such as positions and momenta plus physical parameters such as the gravitational coupling and masses. Pixel-grounded variants infer state from images or frozen visual representations before applying the structured dynamics.

### Outputs

The models output the next physical state or a rollout trajectory. The key behavioral outputs are long-horizon energy drift and whether the generated trajectory matches the intervened repulsive law.

### Training objective (loss)

The main models are trained with one-step prediction on attractive-gravity trajectories. Controls include ordinary MLP transition predictors, energy-penalized predictors, neural ODEs, graph-network simulators, Hamiltonian/Lagrangian variants, and factored/unfactored versions. The paper also reports short-rollout losses and dissipative/port-Hamiltonian variants in boundary settings.

### Architecture / parameterization

The central model is a Hamiltonian neural network with a symplectic leapfrog step. In the factored version, the potential isolates the physical coupling as a linear multiplier of a learned interaction shape. The comparison includes non-factored Hamiltonian models, factored graph networks, Lagrangian models, SymODEN-style control-Hamiltonian models, port-Hamiltonian dissipative models, and pixel-readout pipelines.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It asks what structural commitments let a learned physical world model remain stable over long rollouts and generalize to changed laws. The important move is separating these two goals instead of assuming one physics prior solves both.

### 2. What is the method?

Use a symplectic learned-Hamiltonian update for conservation and a factored coupling in the potential for counterfactual law changes. Then remove or replace one component at a time to test which behavior disappears.

### 3. What is the method motivation?

Long-horizon stability is a geometric integration problem: a model needs to respect conserved structure rather than merely match one-step errors. Counterfactual transfer is a parameterization problem: if the sign or form of a coupling is hidden inside a black-box potential, the model has no reason to extrapolate the changed law correctly.

### 4. What data does it use?

The main setting uses simulated three-body gravity trajectories trained only with attractive gravity. Extensions include more bodies, Coulomb-like force families, contact settings, MuJoCo-style generalized coordinates, stochastic dissipative systems, and pixel-based observations.

### 5. How is it evaluated?

The paper evaluates true-energy drift over long rollouts, nMSE under sign-flip counterfactuals, regime-match indicators, divergence/finiteness, pixel-grounded inversion, transfer across object counts and force families, and boundary failures under dissipation or wrongly specified factors.

### 6. What are the main results?

In the long-rollout comparison, ordinary MLPs, energy-penalized MLPs, and neural ODE controls diverge or drift severely, while the symplectic model remains finite over 2000 steps. In the sign-flip test, the factored symplectic model reaches regime match 1 at every tested repulsive coupling with nMSE around 0.03-0.18, while the non-factored symplectic model has regime match 0 and error near 2.7. In the crossed comparison, the factored graph net follows the changed law but diverges, the non-factored symplectic model is stable but fails inversion, and the factored symplectic model is the only one that does both.

### 7. What is actually novel?

The novelty is the double dissociation and the matched-controls design. The ingredients are individually familiar, but the paper shows that conservation and factorization buy different capabilities and should not be collapsed into a generic "physics prior" label.

### 8. What are the strengths?

The controls are unusually useful: equal-capacity predictors, energy penalties, neural ODEs, factored and non-factored variants, graph simulators, and pixel-grounded variants all probe obvious alternative explanations. The paper also names boundary failures, including dissipative systems where conservation is wrong and factored laws with the wrong parameter dependence.

### 9. What are the weaknesses, limitations, or red flags?

The strongest evidence is in controlled simulators, not real-world video generation. The method works when the right structural form is known; a wrongly specified factor can fail badly. Pixel-grounded tests show the idea survives perception, but they do not prove robust large-scale visual world modeling.

### 10. What challenges or open problems remain?

The hard problem is discovering the right structural factorization rather than hand-specifying it. Another open problem is combining conservation, dissipation, contact, perception, and learned interventions in one deployable model without making the structure brittle.

### 11. What future work naturally follows?

Learn candidate factorization forms from interventions, add model-selection diagnostics for structural priors, test on richer articulated and contact-heavy systems, and connect the structured latent dynamics to planning or controllable video generation.

### 12. Why does this matter for cabbageland?

Cabbageland cares about world models whose state variables carry useful structure. This paper gives a sharp design rule: a prior should be judged by the failure it fixes, not by whether it sounds physically grounded.

### 13. What ideas are steal-worthy?

Use double-dissociation tests for architectural priors. Pair every structural claim with a removal control. Treat stability and counterfactual transfer as separate axes. Build mechanisms that expose physical parameters explicitly when interventions matter.

### 14. Final decision

Preserve. This is directly useful for thinking about world models, controllable simulators, and mechanism-level evaluation.
