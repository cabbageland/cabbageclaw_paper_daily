# HASTE: A Platform for Rapid Post-Disaster Building Damage Assessment

## Basic info

* Title: HASTE: A Platform for Rapid Post-Disaster Building Damage Assessment
* Authors: Caleb Robinson, Anthony Ortiz, Simone Fobi Nsutezo, Cameron Birge, Meygha Machado, Marcelo Duarte, Joaquin Rivero Rodriguez, Anthony Cintron Roman, Kevin White, Inbal Becker-Reshef, Juan M. Lavista Ferres
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.11838
* Date surfaced: 2026-07-14
* Why selected in one sentence: It is rare serious field-deployment documentation showing what a damage-assessment system can do when matched pre/post imagery and large in-domain training sets are missing.

## Quick verdict

**Useful**

This is not a novelty-maximizing model paper, which is part of why it is worth keeping. The useful contribution is a deployable interface between operators, labels, imagery, and lightweight models under real disaster-response constraints. I inspected the full arXiv HTML paper, including the abstract, introduction, platform and method sections, experiment summary, operational-response section, and limitations.

## One-paragraph overview

HASTE is a no-code platform for making rapid building-damage maps from post-disaster overhead imagery when the ideal benchmark assumptions do not hold. It offers two practical routes. One route trains a small segmentation model on a single scene from quick polygon labels and joins the resulting mask back to building footprints. The other route embeds building footprints with a pretrained vision model, asks the user for a small number of building labels, and fits an in-browser logistic regression model that scores the rest of the scene. The paper's value is not just the methods in isolation, but the fact that they are packaged for real response workflows and backed by examples from more than thirty deployments since 2023.

## Model definition

### Inputs
The platform takes post-disaster imagery, building footprints, and small amounts of user labeling such as scene polygons or per-building damage labels.

### Outputs
It outputs per-building damage scores or classes, scene-level overlays for analyst review, and response-ready damage maps.

### Training objective (loss)
The paper does not center a single novel loss. Method 1 uses standard supervised scene-specific segmentation training, while Method 2 uses a logistic-regression classifier over pooled pretrained image embeddings.

### Architecture / parameterization
The system is a platform with two modeling paths: a per-scene segmentation model plus footprint join, and a post-event-only embedding pipeline with pretrained vision features and in-browser logistic regression.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to provide useful building-damage maps quickly after disasters, when matched pre-event imagery, in-domain labels, and time for heavyweight retraining may all be unavailable.

### 2. What is the method?
The method is a two-path platform. Analysts can either label a small number of polygons and train a scene-specific segmenter, or label a small set of building footprints and let an embedding-plus-logistic-regression model score the remaining buildings.

### 3. What is the method motivation?
The paper starts from the real operational constraint that public-benchmark winners often assume exactly the things disaster response does not have on the first day: matched pre/post imagery, good registration, and a training set from similar past events.

### 4. What data does it use?
For experiments it uses xBD-style benchmark data in a label-efficiency sweep for the embedding path, plus operational response examples from real disasters such as wildfires, hurricanes, floods, and earthquakes.

### 5. How is it evaluated?
The paper reports label-efficiency curves on xBD, compares pretrained embedding routes against weaker feature baselines and a fine-tuned ResNet reference, and describes operational use across more than thirty real response deployments.

### 6. What are the main results?
The embedding route reaches roughly `0.82` macro ROC-AUC from only `1%` of labels, climbs to about `0.92` by `50%`, and reportedly matches a fully supervised ResNet-50 baseline with about a twentieth of its labels. The broader platform has also been used in more than thirty real disaster responses since 2023, delivering results within hours to days of imagery arrival.

### 7. What is actually novel?
The novelty is not one flashy model component. It is the combination of operator-facing design, post-event-only fallback logic, and label-efficient deployment paths that accept the ugly realities of disaster imagery instead of pretending the benchmark setup will appear on demand.

### 8. What are the strengths?
The paper is grounded in a real operational setting, presents two usable adaptation paths instead of one brittle pipeline, and gives evidence that foundation-model embeddings can be genuinely useful with tiny labeling budgets.

### 9. What are the weaknesses, limitations, or red flags?
The platform only sees overhead-visible damage, depends on the quality of building footprints, and can be conservative when rubble falls outside footprint boundaries. The xBD experiments are preliminary, binary rather than fine-grained, and cleaner than real response imagery, so the benchmark numbers should not be mistaken for guaranteed field accuracy.

### 10. What challenges or open problems remain?
The hard problems are better robustness under bad registration, handling roads and infrastructure beyond buildings, improving sensitivity without sacrificing fast turnaround, and integrating richer vision-language or active-learning loops without making the tool unusable.

### 11. What future work naturally follows?
The paper itself points to vision-language assessment, active learning, damage-specific foundation models, and infrastructure beyond buildings. A very practical next step would be stronger uncertainty presentation for operators deciding where to trust or override the model.

### 12. Why does this matter for cabbageland?
Cabbageland values serious deployment evidence, operator-aware interfaces, and systems that stay useful under distribution shift instead of collapsing outside curated benchmarks. HASTE is a good reminder that minimal, locally adaptable systems can matter more than one more global leaderboard model.

### 13. What ideas are steal-worthy?
Package fallback methods as first-class options instead of pretending one model fits every condition. Use post-event-only embeddings when pre-event assumptions break. Keep the human labeling loop small and concrete. Treat deployment interfaces as part of the method, not as afterthought glue.

### 14. Final decision
**Keep it.** This is a practical deployment note with real systems value, even if the modeling novelty is more modest than the papers above.
