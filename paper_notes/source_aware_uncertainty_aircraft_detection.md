# Not All Confusion Is Equal: A Source-Aware Uncertainty Diagnosis for Fine-Grained Aircraft Detection

## Basic info

* Title: Not All Confusion Is Equal: A Source-Aware Uncertainty Diagnosis for Fine-Grained Aircraft Detection
* Authors: Hai Huang, Helmut Mayer
* Year: 2026
* Venue / source: arXiv:2609.29959
* Link: https://arxiv.org/abs/2609.29959
* Date surfaced: 2026-09-25
* Why selected in one sentence: It turns confusion matrices into source-specific uncertainty diagnoses with different remedy verdicts.

## Quick verdict

* Highly relevant

This is useful because it refuses to collapse uncertainty into one scalar. The paper separates aleatoric and epistemic uncertainty, then further separates within-class and between-class confusion, producing four named causes with different interventions. The scope is one fine-grained aircraft dataset, so it is more a framework and proof-of-concept than a general detector solution.

## One-paragraph overview

Fine-grained detectors usually report where classes are confused, but not why that confusion happens or whether extra data would help. This paper proposes A2E2, a 2x2 diagnosis grid: aleatoric vs epistemic crossed with within-class vs between-class. The four quadrants are affinity, heterogeneity, contested, and collapsed. Each is measured in a different place: input geometry, output-space ensemble disagreement, or bias-parameter posterior. On aircraft detection, this lets the authors distinguish irreducible size-based confusion from learnable boundaries and data-starved classes, then test targeted interventions for the reducible cases.

## Model definition

### Inputs

Inputs are fine-grained aircraft detection examples with class labels, oriented bounding-box geometry, trained detector outputs, ensemble predictions, and class-level parameter information from a Laplace-style posterior over classifier bias terms.

### Outputs

The framework outputs a source diagnosis for confusion: affinity, heterogeneity, contested boundary, or collapsed class. It also outputs a remedy verdict, such as more class data, boundary data, relabeling, or no data-based fix.

### Training objective (loss)

The diagnostic framework is not a new detector training objective. It uses trained detector predictions and post-hoc measures. Targeted interventions, such as oversampling or boundary sharpening, are then used to test whether the diagnosis predicts the effect of additional data.

### Architecture / parameterization

The detector itself is treated mostly as an existing fine-grained object detector. The diagnostic layer combines oriented-box geometry, ensemble mutual information, and posterior variance over class bias parameters.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It tries to explain the source of detector confusion. A confusion matrix can say "A is confused with B," but it cannot tell whether the confusion is irreducible, data-starved, a contested boundary, or label heterogeneity.

### 2. What is the method?

A2E2 decomposes confusion along two axes: aleatoric vs epistemic and within-class vs between-class. Affinity is measured by geometric overlap, heterogeneity by within-class size dispersion, contested boundaries by pairwise mutual information, and collapsed classes by bias-posterior variance.

### 3. What is the method motivation?

The same off-diagonal confusion can imply opposite remedies. Adding data may help a collapsed class or contested boundary, but not a pair whose classes are intrinsically similar in observable geometry.

### 4. What data does it use?

The paper studies fine-grained aircraft detection with aircraft types such as ARJ21, A220, A350, A330, Boeing787, and Boeing777. The held-out test split remains model-unseen for the epistemic measurements.

### 5. How is it evaluated?

The paper evaluates whether diagnosed sources match measurable geometry and uncertainty patterns, then tests interventions: oversampling a collapsed class and adding boundary-focused data for a contested class pair. It checks whether targeted quantities move while unrelated aleatoric quantities remain stable.

### 6. What are the main results?

ARJ21 is diagnosed as a collapsed class, with the highest bias-posterior variance, zero retention, and low-to-moderate output-space MI. Oversampling ARJ21 specifically revives the collapsed source while an untreated collapsed control does not revive. A220-A350 is diagnosed as contested and the boundary-focused treatment supports that reading. A330-Boeing787 is diagnosed as affinity, an irreducible between-class aleatoric source, while A330 heterogeneity points toward relabeling rather than simply more data.

### 7. What is actually novel?

The novelty is the structured source decomposition and the insistence that the two epistemic sources are different phenomena. Contested boundaries show up as output-space disagreement; collapsed classes can produce stable wrong agreement and require a different diagnostic.

### 8. What are the strengths?

The framework produces action-relevant diagnoses. It separates measurement sites by construction instead of relying only on correlations. It also states limitations plainly, especially for heterogeneity and directionless collapsed-class quantities.

### 9. What are the weaknesses, limitations, or red flags?

The empirical domain is narrow. Heterogeneity is only partially identifiable in this setup, and the collapsed quantity has no direction by itself. Geometry-based aleatoric measures depend heavily on whether the chosen geometry actually captures the relevant visual similarity.

### 10. What challenges or open problems remain?

Open problems include validating the grid across more datasets and detectors, adding richer geometry or part-based measures, and turning the diagnosis into a robust active-data-acquisition loop.

### 11. What future work naturally follows?

Good follow-ups include medical imaging confusion diagnosis, open-vocabulary class confusion analysis, and intervention policies that route each confusion source to data collection, relabeling, feature redesign, or abstention.

### 12. Why does this matter for cabbageland?

Cabbageland cares about uncertainty that changes decisions. This paper is useful because it says "uncertain" is not enough; the source of uncertainty determines the next move.

### 13. What ideas are steal-worthy?

Split uncertainty by remedy. Keep reducible and irreducible sources separate. Do not trust ensemble disagreement alone for collapsed classes. Validate diagnoses with targeted interventions, not just correlation plots.

### 14. Final decision

Preserve. This is a compact diagnostic framework with transferable uncertainty vocabulary.
