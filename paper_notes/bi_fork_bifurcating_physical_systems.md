# Bi-FORK: Generative Modeling of High-Dimensional Bifurcating Systems

## Basic info

* Title: Bi-FORK: Generative Modeling of High-Dimensional Bifurcating Systems
* Authors: Anna Zimmel, Fleur Hendriks, Markus Holzleitner, Florian Sestak, Martin Weichselbaumer, Vlado Menkovski, Johannes Brandstetter
* Year: 2026
* Venue / source: arXiv preprint
* Link: https://arxiv.org/abs/2610.12449
* Date surfaced: 2026-10-09
* Why selected in one sentence: It models symmetry-breaking physical bifurcations as branch-coherent generative distributions instead of averaging multiple valid futures into mush.

## Quick verdict

* Must read

This is a strong adjacent paper for scientific generative modeling. The paper's useful move is to treat one-to-many physical prediction as a distribution over valid solution branches, with explicit symmetry-aware diagnostics. The method still learns rather than enforces most symmetries, and particle guidance can trade accuracy for diversity, but the formulation is much better than pointwise trajectory prediction for bifurcating systems.

## One-paragraph overview

Bi-FORK targets physical systems where the same condition can lead to multiple valid trajectories after a symmetry-breaking bifurcation. A compressed autoencoder represents full physical states, a latent flow model generates complete trajectories, and particle guidance repels concurrent samples after the predicted bifurcation point so a batch of samples covers distinct branches. The paper evaluates buckling beams, buckling mechanical metamaterials, and Allen-Cahn phase separation, with trajectories from 32 to 200 timesteps and discretizations up to 260,000 points. The key contribution is not just better error; it is branch-coherent sampling plus metrics that detect mode collapse under the relevant symmetry group.

## Model definition

### Inputs

The model receives a physical condition `c`, such as reference geometry and loading protocol for beams or metamaterials, or physical parameters for Allen-Cahn. In standard settings it also observes the first trajectory state. Sampling starts from Gaussian latent noise.

### Outputs

The model outputs one or more complete future physical trajectories. For Beam3D and metamaterials these are displacement fields over nodes or meshes; for Allen-Cahn they are 3D scalar phase-field trajectories on a voxel grid.

### Training objective (loss)

Training is two-stage. The first stage trains an autoencoder with a reconstruction MSE over valid nodes or voxels. The second stage freezes the autoencoder and trains a latent flow model with a frame-masked MSE between predicted and target clean latent trajectories. Beam3D and metamaterials optionally add a temporal binary cross-entropy loss for predicting post-bifurcation frames.

### Architecture / parameterization

Beam3D and metamaterials use a Perceiver-style cross-attention autoencoder that maps variable-size point sets to fixed latent tokens and decodes states by querying reference positions. Allen-Cahn uses a 3D ViT autoencoder over volumetric patches. The trajectory generator is a Scalable Interpolant Transformer over latent trajectories. At inference, particle guidance adds a repulsive term among samples in post-bifurcation latent frames.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It addresses physical prediction problems where one input condition admits multiple equally valid stable outcomes. A deterministic surrogate or pointwise loss tends to average branches or collapse to one mode, which is physically wrong.

### 2. What is the method?

Compress full physical states into latent tokens, train a latent flow model over complete trajectories, predict where bifurcation happens, and then sample multiple trajectories jointly. After the bifurcation point, particle guidance pushes similar samples apart so the generated set covers distinct branches.

### 3. What is the method motivation?

Bifurcating systems need global coordination over space and time. A beam should not buckle left at one end and right at the other, and a metamaterial branch should remain coherent across the structure. Modeling full trajectories in latent space makes branch choice structural instead of local.

### 4. What data does it use?

The paper uses three simulated physical datasets: Beam3D buckling beams with continuous SO(2)-like branch directions, 2D porous mechanical metamaterials spanning wallpaper groups with one, two, or four post-buckling modes, and Allen-Cahn phase separation on 64 cubed grids.

### 5. How is it evaluated?

Evaluation uses mode-conditioned mean absolute error, rejection rate, and Jensen-Shannon divergence over symmetry orbits or mode coverage. The paper compares against GeoTDM and STFlow on Beam3D, an affine baseline on metamaterials, and ablates particle guidance. It also reports runtime for generating many samples.

### 6. What are the main results?

On Beam3D, Bi-FORK reaches MCon-MAE 0.018, JSD 0.041, and less than 0.01% rejection. STFlow reaches MCon-MAE 0.114, JSD 0.074, and 0.5% rejection; GeoTDM has JSD 0.036 but rejects 99.2% of samples. Generating 180 Beam3D samples takes 3.95 seconds for Bi-FORK, versus 72.32 seconds for STFlow. On metamaterials, Bi-FORK gives JSD 0.013 for two-mode cases and 0.023 for four-mode cases, with full coverage 74% and 48%. On Allen-Cahn, particle guidance improves MCon-MAE from 0.0515 to 0.0453 and mean JSD from 0.217 to 0.204.

### 7. What is actually novel?

The novelty is the combination of complete-trajectory latent flow matching, bifurcation-aware particle guidance, and symmetry-orbit distribution evaluation for high-dimensional physical bifurcations. The paper turns branch coverage into the object of evaluation.

### 8. What are the strengths?

The problem is well chosen, the failure mode of averaging is real, and the metrics are better aligned with the physics than standard pointwise scores. The method scales to systems that are far too large for the graph baselines used in smaller particle systems. The particle-guidance ablation makes the diversity mechanism visible.

### 9. What are the weaknesses, limitations, or red flags?

Particle guidance can push samples away from the solution manifold if it repels trajectories that are already valid. Allen-Cahn evaluation is incomplete because the full distribution over morphologies is not known. The method learns most symmetry structure from data and augmentation instead of enforcing it architecturally.

### 10. What challenges or open problems remain?

The hard remaining problem is certified coverage of continuous and high-dimensional branch distributions. The method also needs stronger tests under out-of-distribution conditions, noisy observations, and systems with hierarchical or rare branches that are not well sampled.

### 11. What future work naturally follows?

Build symmetry-equivariant latent flow architectures, learn adaptive repulsion that respects local manifold structure, add physics residual checks during sampling, and use active sampling to discover missing branches. A useful extension would combine Bi-FORK-style branch sampling with downstream decision-making under multiple valid physical futures.

### 12. Why does this matter for cabbageland?

Cabbageland cares about generative models that preserve the structure of possible worlds. Bi-FORK is a strong reminder that when multiple futures are valid, the right target is not a mean forecast but a branch-aware distribution with diagnostics for mode coverage.

### 13. What ideas are steal-worthy?

Generate whole trajectories when branch coherence matters. Use particle repulsion only after the predicted branch point. Evaluate by symmetry-orbit coverage and per-input distribution match, not just global error. Treat best-of-K as insufficient because it can hide distribution collapse.

### 14. Final decision

Preserve. This is a mechanism-rich scientific generative modeling paper with useful ideas beyond its physical-simulation domain.
