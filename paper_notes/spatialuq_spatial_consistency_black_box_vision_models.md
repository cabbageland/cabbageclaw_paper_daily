# SpatialUQ: Post-Hoc Uncertainty Quantification from Spatial Consistency in Black-Box Vision Models

## Basic info

* Title: SpatialUQ: Post-Hoc Uncertainty Quantification from Spatial Consistency in Black-Box Vision Models
* Authors: Md Kawsher Mahbub, Milon Biswas, Mirza Niaz Morshed, Wei Yu
* Year: 2026
* Venue / source: arXiv preprint
* Link: https://arxiv.org/abs/2610.09498
* Date surfaced: 2026-10-08
* Why selected in one sentence: It gives frozen black-box clinical vision models a simple uncertainty score based on spatial prediction consistency.

## Quick verdict

* Highly relevant

SpatialUQ is useful because it is operationally modest: six deterministic forward passes, output probabilities only, no retraining, no activations, no gradients, and no training-set feature statistics. The result is not universal, and the paper is clear about that. It works best for overconfident multi-label models and diffuse findings; it weakens for focal lesions and severe domain shift.

## One-paragraph overview

SpatialUQ scores uncertainty by asking whether a classifier's prediction is spatially reproducible. For each image, it runs the frozen model on the full image and on five fixed crops, averages the crop predictions, and computes Jensen-Shannon divergence between the global and local distributions. This Multicrop Uncertainty Score is evaluated as a failure detector, where failure is defined by high per-image Brier score. On NIH ChestX-ray14 with DenseNet-121, MUS reaches 0.784 AUC with six deterministic passes, beating MC-Dropout's 0.664 with 30 stochastic passes and offering better native calibration than raw L1 disagreement. Fusion with entropy, confidence, and L1 reaches 0.832 AUC, but the unsupervised MUS is the more deployable part.

## Model definition

### Inputs

The method takes an image and access to a frozen classifier's output probabilities. It uses one full image and five deterministic crops: four quadrants and one center crop, each upsampled back to the input size.

### Outputs

It outputs a scalar uncertainty score. In the multi-label case, the score averages Bernoulli Jensen-Shannon divergence across classes between the global prediction and mean crop prediction.

### Training objective (loss)

The unsupervised MUS score is not trained. An optional supervised fusion model uses logistic regression on a small labeled hold-out, combining MUS, entropy, inverse confidence, and L1 global-local probability shift.

### Architecture / parameterization

SpatialUQ is model-agnostic and black-box. The experiments apply it to DenseNet-121, EfficientNet-B4, ViT-B/16, CLIP ViT-B/32, BiomedCLIP, ImageNet classifiers, and COCO detectors. It requires only output probabilities.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Clinical vision models are often deployed as frozen black boxes. Many uncertainty methods require dropout at training time, ensembles, model internals, gradients, feature distributions, calibration data, or retraining. SpatialUQ asks whether a useful failure score can be computed from output probabilities alone.

### 2. What is the method?

Compute the prediction on the full image and five fixed spatial crops, average the crop predictions, and measure global-local divergence with Jensen-Shannon divergence. Larger divergence means the prediction is less spatially stable and therefore more suspicious.

### 3. What is the method motivation?

Reliable medical image predictions should be anchored in stable spatial evidence. If a classifier changes its answer sharply when looking at deterministic sub-regions, its confidence may not be tied to robust image content.

### 4. What data does it use?

The main medical experiments use NIH ChestX-ray14 with DenseNet-121, EfficientNet-B4, ViT-B/16, CLIP ViT-B/32, and BiomedCLIP. CheXpert and VinBigData test zero-shot transfer from the NIH-trained DenseNet. The paper also evaluates ImageNet-1k classifiers and MS COCO detectors.

### 5. How is it evaluated?

Failure is defined as per-image Brier score above the 75th percentile of the test distribution. The main metric is failure-detection AUC, with calibration measured by Score Calibration Error. The paper also reports Spearman correlation between MUS and Brier score, selective triage/rejection behavior, per-class lesion analysis, and transfer under domain shift.

### 6. What are the main results?

On NIH ChestX-ray14 with DenseNet-121, MUS reaches AUC 0.784 with SCE 0.049. MC-Dropout reaches 0.664 with SCE 0.121 using 30 passes; deep ensembles reach 0.813 with SCE 0.138; L1 distance reaches 0.790 but has worse SCE 0.127. Fusion reaches 0.832. On CheXpert, MUS reaches 0.708 versus MC-Dropout 0.599. On VinBigData, MUS drops to 0.614 while MC-Dropout reaches 0.764 and the MUS/Brier correlation collapses to rho 0.027, which the authors use as a shift diagnostic. With BiomedCLIP, MUS reaches 0.899 AUC and rho 0.846.

### 7. What is actually novel?

The novelty is a black-box spatial consistency score using global-vs-crop Jensen-Shannon divergence, plus a deployment diagnostic based on whether the score still correlates with error under the target distribution.

### 8. What are the strengths?

It is cheap, simple, deterministic, and applicable to frozen checkpoints. The paper compares many baselines, reports calibration, and is unusually honest about the settings where the method fails. The per-class analysis is important because it prevents a good average from hiding focal-lesion weakness.

### 9. What are the weaknesses, limitations, or red flags?

Severe shift can make failures spatially uniform and destroy the signal. Five fixed crops are bad for small focal lesions such as nodules. ViT/global-attention models can compress the dynamic range of the crop signal. Fusion improves AUC but requires labeled hold-out data and is less black-box-pure than MUS. CT, MRI, ultrasound, and temporal clinical shift remain untested.

### 10. What challenges or open problems remain?

The key challenge is adapting crop placement and aggregation to lesion scale and model architecture. Another is combining MUS with conformal calibration or clinical triage protocols without overclaiming safety.

### 11. What future work naturally follows?

Use saliency-guided or multi-scale crops, focal-lesion-enriched benchmarks, MIMIC-CXR temporal shift, subgroup audits, and extension to CT/MRI/ultrasound. Test whether spatial consistency can be combined with calibrated prediction sets.

### 12. Why does this matter for cabbageland?

It is a good uncertainty pattern: define a simple consistency relation, measure where it correlates with error, and include a diagnostic for when the relation no longer holds. That is much better than pretending a scalar uncertainty score is universally meaningful.

### 13. What ideas are steal-worthy?

Use deterministic perturbation consistency as a black-box error signal. Report calibration alongside AUC. Include a correlation-based deployment gate that tells you when the score has stopped meaning what you think it means.

### 14. Final decision

Preserve. This is a practical uncertainty note with strong caveat discipline.
