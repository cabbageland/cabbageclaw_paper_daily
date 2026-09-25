# PEEL: Physics-Enabled Evidential Learning for Identifiable Uncertainty in CT Imaging

## Basic info

* Title: PEEL: Physics-Enabled Evidential Learning for Identifiable Uncertainty in CT Imaging
* Authors: Ge Wang
* Year: 2026
* Venue / source: arXiv:2609.29599
* Link: https://arxiv.org/abs/2609.29599
* Date surfaced: 2026-09-25
* Why selected in one sentence: It uses physical measurement to resolve a non-identifiability in evidential uncertainty rather than selecting a point by regularization.

## Quick verdict

* Highly relevant

This is a small proof-of-concept, but the point is sharp. Normal-inverse-gamma regression cannot identify all four parameters from the marginal Student-t likelihood alone; PEEL explicitly identifies the missing degree of freedom using CT physics and Monte Carlo noise propagation. The limitation is that the evidence is synthetic and in-distribution, but the identifiability framing is worth keeping.

## One-paragraph overview

Evidential regression often reports Normal-inverse-gamma uncertainty parameters as though the likelihood uniquely determined them. This paper points out that the marginal Student-t likelihood only determines three combinations of four NIG parameters, leaving a one-dimensional fiber. PEEL resolves that ambiguity in CT reconstruction by adding independent physical information. A reconstruction network first maps one noisy filtered-backprojection image to the identifiable Student-t coordinates. The network is frozen, repeated physical-noise realizations are propagated through its output to make a Monte Carlo target for aleatoric variance, and an aleatoric head learns that target. With the aleatoric coordinate identified, the remaining NIG parameters are recovered algebraically.

## Model definition

### Inputs

The input is a single noisy filtered-backprojection CT image derived from simulated projection data at one of five photon levels. The second-stage teacher uses repeated physical-noise realizations propagated through the reconstruction output.

### Outputs

The first stage outputs the identifiable Student-t coordinates: gamma, alpha, and c. The second stage outputs output-domain aleatoric variance. The full NIG parameters beta and nu are then recovered algebraically when the admissibility condition is satisfied.

### Training objective (loss)

Stage one trains the reconstruction network with Student-t negative log-likelihood. Stage two freezes the network and trains an aleatoric head on a Monte Carlo teacher label for output-domain aleatoric variance. The method does not use a KL term, reference prior, evidence regularizer, or hand-tuned cross-loss weight.

### Architecture / parameterization

The paper uses a reconstruction network with shared features and separate heads for Student-t coordinates and aleatoric variance. The statistical parameterization is Normal-inverse-gamma regression with algebraic recovery of the full parameter set after the physical variance coordinate is measured.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It tries to make evidential uncertainty identifiable in CT imaging. Without additional information, the Student-t likelihood leaves one NIG degree of freedom unspecified.

### 2. What is the method?

PEEL first learns the likelihood-identifiable coordinates from one noisy image, then uses physical-noise Monte Carlo propagation to supervise aleatoric variance on frozen features. That extra physical measurement identifies the remaining NIG coordinate.

### 3. What is the method motivation?

Regularizers can choose a convenient point on the unidentified fiber, but they do not identify it. CT has a known physical noise process, so repeated noise realizations can provide the missing aleatoric information.

### 4. What data does it use?

The experiment uses simulated CT objects across five photon levels. Evaluation is on 30 held-out simulated objects, with independent 400-repeat Monte Carlo references.

### 5. How is it evaluated?

The paper compares one-image predicted aleatoric variance against independent Monte Carlo reference variance using pooled Spearman correlation, within-image Spearman correlation, case-level Spearman correlation, and the fraction of pixels satisfying the algebraic admissibility condition.

### 6. What are the main results?

Across five photon levels, pooled Spearman correlations are 0.832-0.951 and median within-image correlations are 0.834-0.947 against 400-repeat references. The admissibility condition holds for 98.81-99.55% of evaluated pixels. The paper reports that spatial ordering of aleatoric uncertainty is reliably recovered from one noisy input.

### 7. What is actually novel?

The novelty is not another evidential head. It is the identifiability argument: the paper separates likelihood-identifiable Student-t coordinates from the missing NIG coordinate and uses independent physics to recover it.

### 8. What are the strengths?

The statistical failure mode is explicit, the physical measurement has a clear role, and the training path avoids vague evidence regularization. The paper is honest that this is an initial embodiment rather than a clinical-ready system.

### 9. What are the weaknesses, limitations, or red flags?

The evaluation is synthetic, in-distribution, and uses one training seed. Monte Carlo references are expensive and are used as supervision for the uncertainty head. The method is tied to settings where the physical noise process is sufficiently known.

### 10. What challenges or open problems remain?

Open problems include real scanner data, unknown or misspecified noise physics, patient anatomy outside the synthetic distribution, and extension to other inverse problems.

### 11. What future work naturally follows?

Follow-ups could test PEEL on measured CT phantoms, combine it with domain adaptation, use approximate physical repeats, and evaluate whether identified uncertainty improves downstream clinical decisions.

### 12. Why does this matter for cabbageland?

It is a clean example of not reporting uncertainty parameters the data cannot identify. That standard should carry over to agents, world models, and medical models alike.

### 13. What ideas are steal-worthy?

Ask which uncertainty parameters are identifiable from the stated loss. Use independent measurements to resolve non-identifiability rather than hiding it behind priors. Separate likelihood learning from physical uncertainty calibration.

### 14. Final decision

Preserve. The scope is narrow, but the identifiability lesson is strong.
