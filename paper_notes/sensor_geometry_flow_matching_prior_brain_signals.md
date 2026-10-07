# Sensor Geometry as a Flow-Matching Prior for Multi-Channel Brain Signals

## Basic info

* Title: Sensor Geometry as a Flow-Matching Prior for Multi-Channel Brain Signals
* Authors: Jaedong Hwang
* Year: 2026
* Venue / source: arXiv preprint
* Link: https://arxiv.org/abs/2610.08355
* Date surfaced: 2026-10-07
* Why selected in one sentence: It improves flow matching for EEG and related sensor arrays by moving known spatial structure into the source distribution.

## Quick verdict

* Highly relevant

This is a compact, useful paper because the intervention is almost embarrassingly sensible: if the sensor layout is known, do not start from channel-independent noise. The graph-Matern source prior adds no learned parameters and improves spectral fidelity across many settings. The limits are also clear: it mostly targets spatial covariance and spectral match, not full sample realism or downstream clinical validity.

## One-paragraph overview

The paper replaces the usual isotropic Gaussian source in flow matching with a graph-Matern Gaussian source built only from sensor coordinates. For EEG, electrodes are connected with a sparse k-nearest-neighbor graph, the normalized graph Laplacian supplies spatial eigenvectors, and a Matern spectral density assigns more variance to smooth scalp patterns than to high-frequency channel flips. The same source prior is then used with standard flow-matching methods and unchanged drift networks. Across eight EEG datasets and four flow-matching formulations, the prior lowers PSD-KL by 12% to 17% in geometric mean, with the largest gains on dense montages such as PhysioNet-MI. Ablations show that the gain comes from the eigenvectors of a sparse physical sensor graph, not merely from low effective dimension or empirical covariance fitting.

## Model definition

### Inputs

The generative model trains on multi-channel time series with known sensor coordinates. The prior construction uses only coordinates, not recorded signals, to build the sensor graph.

### Outputs

The model generates multi-channel time-series windows. Evaluation focuses on log band-power distributions across clinical frequency bands, cross-channel phase-lag coupling, and downstream augmentation on one EEG classification task.

### Training objective (loss)

The base objective is the standard flow-matching squared-error loss between the learned vector field and the conditional velocity along an interpolation path. For stochastic-interpolant methods, the target includes the derivative of the interpolant noise term. The graph prior changes only the source distribution.

### Architecture / parameterization

The prior builds a k-nearest-neighbor graph over sensor coordinates, computes the normalized Laplacian, and samples from a Gaussian covariance whose eigenbasis is the graph eigenbasis and whose eigenvalues follow a graph-Matern density. The experiments use SF2M, SI, OT-CFM, and rectified flow with a shared 1D U-Net drift over time, treating sensors as channels.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Flow-matching generators for EEG usually start from independent channel noise, even though sensor layout and volume conduction impose shared spatial structure. The model then has to learn that structure from data.

### 2. What is the method?

Build a source covariance from the sensor graph. Nearby sensors are connected, the graph Laplacian supplies smooth spatial modes, and a Matern spectrum gives smooth modes more variance. Sampling starts from spatially coherent noise rather than white channel noise.

### 3. What is the method motivation?

Known structure should live in the prior when it is stable across subjects and tasks. For EEG and related sensor arrays, coordinates are known before training and capture an inductive bias that is not dataset-specific.

### 4. What data does it use?

The main experiments cover eight EEG datasets: TUAB, TUEV, Mumtaz-MDD, BCI-IV 2a, FACED, SHU, SEED-V, and PhysioNet-MI. Generalization tests use whole-head MEG, patient-specific intracranial EEG grids, and the PEMS-BAY traffic-sensor network.

### 5. How is it evaluated?

The primary metric is PSD-KL, a symmetric KL divergence between real and generated log band-power distributions across five clinical bands. The paper also reports weighted phase-lag index correlation, a Mumtaz-MDD augmentation test with EEGNet, and ablations that replace eigenvectors, spectra, or graph construction.

### 6. What are the main results?

Across the eight EEG datasets, graph-prior variants have geometric mean PSD-KL ratios of 0.83 to 0.88 relative to isotropic baselines. PhysioNet-MI drops from roughly 33-35 PSD-KL to 20-22 across methods, and SHU drops from roughly 111-116 to 81-85. wPLI correlation rises by 0.01 to 0.03 on average. On Mumtaz-MDD augmentation, balanced accuracy improves from 60.8% real-only to 83.3% with graph-prior synthetic windows, slightly above the 81.9% isotropic-source result.

### 7. What is actually novel?

The novelty is moving a graph-based spatial covariance into the flow source distribution, while leaving the coupling, drift architecture, and training objective unchanged.

### 8. What are the strengths?

The intervention is simple, architecture-agnostic, and well ablated. The paper shows that empirical covariance priors can be worse than isotropic noise, which is a useful warning against naive data-covariance matching. The extension to MEG, iEEG, and traffic sensors shows the idea is about spatial sensor graphs, not just scalp EEG.

### 9. What are the weaknesses, limitations, or red flags?

PSD-KL is a spectral fidelity metric, not a full realism metric. The prior encodes only spatial covariance and leaves temporal structure to the drift network. Some datasets and methods see weak or negative gains, especially where sensor coverage is sparse or dataset-specific high-frequency noise dominates.

### 10. What challenges or open problems remain?

The next step is a separable spatiotemporal prior that also encodes temporal structure. It also needs stronger tests on downstream clinical, BCI, and source-space tasks before claiming practical medical value.

### 11. What future work naturally follows?

Combine graph-Matern spatial priors with temporal Gaussian-process priors. Test source-space cortical meshes, variable electrode layouts, and continuous-time diffusion models. Use the ablation discipline here when adding domain priors elsewhere.

### 12. Why does this matter for cabbageland?

This is a clean example of putting known structure where it belongs. Instead of asking a model to rediscover sensor geometry, the prior names the spatial relationship upfront and lets learning handle the residual dynamics.

### 13. What ideas are steal-worthy?

When a domain has known geometry, structure the source distribution before changing the network. Ablate eigenvectors separately from eigenvalues. Beware empirical covariance priors: fitted covariance is not the same as a useful inductive bias.

### 14. Final decision

Preserve. This is a strong adjacent generative-modeling and neuro-signal paper with a transferable design pattern.

