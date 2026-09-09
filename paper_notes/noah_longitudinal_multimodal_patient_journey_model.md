# NOAH: Learning the Full Patient Journey. A Longitudinal Multimodal Time-Aware Model for Representation and Forecasting

## Basic info

* Title: NOAH: Learning the Full Patient Journey. A Longitudinal Multimodal Time-Aware Model for Representation and Forecasting
* Authors: Tobias Susetzky, Raphael Rehms, Dmitrii Seletkov, Ozgun Turgut, Michelle Espranita Liman, Lisa Steinhelfer, Rickmer Braren, Daniel Rueckert
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2609.09140
* Date surfaced: 2026-09-09
* Why selected in one sentence: It models clinical records as time-aware stochastic patient-state trajectories rather than isolated discriminative snapshots.

## Quick verdict

* Highly relevant

I inspected the full arXiv HTML text, including the architecture description, MIMIC data construction, variational objective, forecasting setup, Monte Carlo outcome estimation, counterfactual sepsis-fluid experiment, probing, NEWS2, survival analysis, and discussion caveats. This is worth preserving because the temporal-state framing is strong, but it needs to be kept away from medical-simulator overclaiming.

## One-paragraph overview

NOAH is a generative transformer for full longitudinal multimodal patient timelines. It turns each clinical event into a multimodal token with type, value/content embedding, and time features, then uses causal sequence modeling with bidirectional temporal information and a context-conditional variational latent state. The model is pretrained on the MIMIC dataset family and can produce patient-state embeddings, forecast future event sequences, estimate clinical outcomes through Monte Carlo rollouts, and simulate limited counterfactual interventions. The paper is valuable because it treats time, stochasticity, and multimodality as first-class modeling problems, while explicitly showing that autoregressive clinical rollouts drift and should not be read as physiologic truth.

## Model definition

### Inputs
Longitudinal patient event sequences from MIMIC-IV, MIMIC-ED, MIMIC-Note, MIMIC-CXR-JPG, MIMIC-IV-ECG, and MIMIC-ECHO. Events include clinical notes, categorical events, numeric values, medical images, ECG waveforms, echo data, drug/procedure/diagnosis events, patient age, and inter-event timing.

### Outputs
Next-event predictions, autoregressive future patient trajectories, patient-state embeddings at each timestep, Monte Carlo outcome probabilities, generated event components, and counterfactual trajectory distributions under substituted interventions.

### Training objective (loss)
Training maximizes a per-timestep evidence lower bound. The model uses a context-conditional variational latent state to capture stochastic patient-state transitions, with reconstruction/prediction terms for multimodal event components and a KL term against the context-conditioned prior.

### Architecture / parameterization
NOAH is a causal generative transformer decoder with multimodal event embeddings, bidirectional time integration, a variational autoregressive module, context-conditioned prior/posterior networks, and modality-specific output decoders. The patient-state embedding is the 768-dimensional transformer output before the variability module.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Most clinical AI models are discriminative, modality-limited, tied to closed categorical vocabularies, or weak at forecasting irregular longitudinal records. NOAH tries to model the full patient journey as a time-aware multimodal trajectory.

### 2. What is the method?
It embeds every patient event as a token with type, content/value, and time features, processes the sequence with a causal transformer, uses bidirectional temporal integration to handle irregular gaps and prediction horizons, and adds a context-conditional variational latent state for stochastic future continuation.

### 3. What is the method motivation?
Clinical trajectories are irregular, multimodal, and inherently uncertain. A deterministic encoder cannot represent multiple plausible futures, and a fixed-vocabulary event model cannot consume the content of notes, images, waveforms, and numeric values well enough.

### 4. What data does it use?
It builds patient timelines from the MIMIC dataset family: 559 million timestamped events from 299,000 patients and 431,000 hospital visits. The sources include MIMIC-IV 2.2, MIMIC-ED 2.2, MIMIC-Note 2.2, MIMIC-CXR-JPG 2.0, MIMIC-IV-ECG 1.0, and MIMIC-ECHO 1.0.

### 5. How is it evaluated?
The paper evaluates autoregressive forecasting of future event categories and modalities, optional time-controlled rollouts, Monte Carlo classification for prolonged stay, mortality, and readmission, counterfactual simulation of saline versus lactated Ringer's in sepsis, linear probing of patient-state embeddings, NEWS2 retrieval, and time-to-event survival analysis.

### 6. What are the main results?
For event forecasting over eligible test patients, NOAH reports AUROC 0.83-0.95 and Brier scores 0.03-0.11, beating a persistence baseline. Time control can improve AUROC by up to 0.19 in shorter horizons. With a 48-hour admission prompt, Monte Carlo rollouts achieve 72-hour mortality AUROC 0.97 and length-of-stay at least 72 hours AUROC 0.74; 30-day readmission is much weaker at AUROC 0.61. Patient-state probes report AUROC 0.72-0.94 for ICD chapters and comorbidities, 0.87/0.98/>0.99 for ICU length of stay, hospital length of stay, and mortality, and NEWS2 retrieval MAE 1.34 with AUROC 0.94 and 0.91 for common risk thresholds.

### 7. What is actually novel?
The novelty is the combination of whole-record multimodal clinical tokenization, explicit irregular-time modeling, and a context-conditioned variational autoregressive patient state. It is not merely a clinical embedding model.

### 8. What are the strengths?
The scale and modality coverage are serious. The patient-state embedding is useful across probes. The paper also shows concrete failures, especially around long-horizon rollout drift and counterfactual overprediction, which makes the claims more credible than a pure victory lap.

### 9. What are the weaknesses, limitations, or red flags?
The counterfactual simulation should not be mistaken for causal identification. The sepsis-fluid experiment matches the SMART trial direction but overpredicts mortality and estimates roughly twice the effect magnitude. Autoregressive rollouts drift out of distribution, especially for long horizons such as readmission.

### 10. What challenges or open problems remain?
The main challenges are causal validity, out-of-distribution rollout drift, patient subgroup reliability, missing modalities, calibration for rare events, and connecting generated trajectories to clinically safe decision support.

### 11. What future work naturally follows?
Add causal evaluation designs, external hospital validation, uncertainty reporting for rollouts, intervention-specific calibration, retrieval of evidence behind state transitions, and mechanisms to prevent long-horizon drift.

### 12. Why does this matter for cabbageland?
NOAH is a strong example of stateful sequence modeling where the state is not just hidden context. It has a persistent embedding, stochastic transitions, time-aware attention, and explicit rollout tests. The cautionary lesson is that a generated trajectory can be useful without being a faithful simulator.

### 13. What ideas are steal-worthy?
Represent irregular event streams with explicit time features. Route stochasticity through a patient-state latent rather than random output noise. Use Monte Carlo rollouts for prediction, but report coverage and invalid-run rates. Treat surprise between prior and posterior state as a diagnostic signal.

### 14. Final decision
Keep as a preserved note. It is adjacent rather than directly cabbageland-native, but the temporal-state machinery and honest rollout caveats are valuable.
