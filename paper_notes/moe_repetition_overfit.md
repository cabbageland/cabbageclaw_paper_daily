# Data Scarcity and Model Sparsity: Mixtures-of-Experts Overfit More to Repeated Data

## Basic info

* Title: Data Scarcity and Model Sparsity: Mixtures-of-Experts Overfit More to Repeated Data
* Authors: Atindra Jha, Margaret Li, Jure Leskovec, Percy Liang, Luke Zettlemoyer
* Year: 2026
* Venue / source: arXiv:2609.11917
* Link: https://arxiv.org/abs/2609.11917
* Date surfaced: 2026-09-12
* Why selected in one sentence: It identifies a concrete sparse-model failure mode under repeated data and connects it to routing stabilization and expert specialization.

## Quick verdict

* Highly relevant

This is a foundation-model training paper with a mechanism, not just a scaling complaint. The important thing is that repetition interacts badly with sparse routing, and the paper gives internal evidence for why. Full arXiv HTML inspected.

## One-paragraph overview

The paper studies dense and MoE language models under repeated data. It varies repetition rate, model size, expert count, expert granularity, domain, filtering, and regularization. Dense models tolerate more repetition, while MoEs lose performance earlier and more sharply, especially as sparsity increases. The authors argue that repeated data pushes sparse experts toward over-specialization because routers stabilize early, causing experts to update on small and stationary token subsets.

## Model definition

### Inputs

Repeated or unique text token sequences from OLMoE-style mixes and single-domain corpora, with controlled repetition rates from low to extremely high.

### Outputs

Next-token distributions from dense transformer language models and sparse MoE transformer language models.

### Training objective (loss)

Standard autoregressive language-model cross-entropy / validation loss, under compute-matched training budgets.

### Architecture / parameterization

Dense transformer LMs versus MoE transformer LMs where feed-forward blocks are replaced by routed experts. The study varies active parameter scale, total expert count, expert granularity, and regularization choices.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

As unique human-written data becomes scarce, pretraining often repeats data. The paper asks whether MoE sparsity changes how damaging that repetition is.

### 2. What is the method?

Train controlled dense and MoE models across repetition rates, domains, sizes, and regularizers, then analyze validation loss and internal routing/expert behavior.

### 3. What is the method motivation?

MoEs decouple active and total parameters. If routing partitions data into smaller expert-specific streams, repeated data may effectively become even more repetitive for each expert.

### 4. What data does it use?

OLMoE-style data mixes and domains including web crawl, academic text, code, and encyclopedic text, plus mixed-domain repetition experiments.

### 5. How is it evaluated?

Validation cross-entropy and held-out LM tasks, plus mechanistic analyses of router stability, router output magnitude, expert load, and expert specialization.

### 6. What are the main results?

MoEs begin to degrade around 4x repetition where dense 80M models remain relatively stable past 8x. By 32x repetition, MoEs can cede their all-unique-data advantage to dense models. Higher sparsity worsens the effect. Dropout and output masking help, and strong masking can let MoEs outperform dense models even beyond 64x repetition, but no method matches all-unique training data.

### 7. What is actually novel?

The useful novelty is showing the interaction between repeated data and sparse routing, then tying the degradation to early router ossification and expert specialization.

### 8. What are the strengths?

The controlled sweeps are broad enough to make the phenomenon hard to dismiss as one MoE setup. The internal analyses give a plausible mechanism. The regularization experiments are actionable.

### 9. What are the weaknesses, limitations, or red flags?

The models are smaller than frontier training runs, so the exact repetition thresholds may not transfer. Validation loss is informative but not the only downstream measure that matters. Some conclusions about frontier data scarcity remain extrapolations.

### 10. What challenges or open problems remain?

How to design sparse routing that avoids early specialization under repeated data. How to measure per-expert effective data diversity during training. How to combine data mixing and regularization without wasting compute.

### 11. What future work naturally follows?

Routing entropy schedules, anti-specialization objectives, expert reset/rotation, per-expert data-diversity monitoring, and repetition-aware data curricula for sparse models.

### 12. Why does this matter for cabbageland?

It is a crisp warning about hidden state partitioning. A sparse model can look compute-efficient while silently shrinking the effective data stream each expert sees.

### 13. What ideas are steal-worthy?

Audit not only global data repetition, but repetition as seen through each routed subsystem. Watch for router stabilization as a training-phase transition.

### 14. Final decision

Preserve. This is useful for model-scaling intuition, data-mix design, and sparse architecture skepticism.
