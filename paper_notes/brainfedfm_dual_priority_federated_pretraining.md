# A generalizable structural brain MRI foundation model built through dual-priority federated pretraining

## Basic info

* Title: A generalizable structural brain MRI foundation model built through dual-priority federated pretraining
* Authors: Zhen Yu, Yang Liu, Xiahai Zhuang, Qingchao Chen
* Year: 2026
* Venue / source: arXiv:2609.27611
* Link: https://arxiv.org/abs/2609.27611
* Date surfaced: 2026-09-24
* Why selected in one sentence: It is a large-scale neuroimaging foundation model with an explicit federated prioritization mechanism and broad downstream evaluation.

## Quick verdict

* Useful

This is worth preserving as a serious medical/neuro foundation-model note. The mechanism is not only privacy-preserving federation; it adds spatial-priority masking, site-priority aggregation, and a global priority memory to avoid letting large cohorts dominate pretraining. The evidence is broad, though the method is still tied to carefully preprocessed structural MRI and the segmentation gains are narrower than the classification/regression gains.

## One-paragraph overview

BrainFedFM is a structural brain MRI foundation model pretrained across 164,707 3D scans distributed over 42 federated sites. The method uses masked image modeling, but changes both what each site masks and how the server weights site updates. At the site level, random, lifespan-guided, and difficulty-guided masks emphasize broad anatomy, lifespan-informative regions, and persistently hard-to-reconstruct regions. At the server level, site-priority aggregation weights updates by lifespan support and residual reconstruction difficulty, linked back to a global priority memory that guides future local masking. The pretrained encoder is evaluated on 20 downstream datasets spanning 17 classification, regression, and segmentation tasks and reports the best overall mean rank across seven compared models.

## Model definition

### Inputs

Pretraining inputs are 3D structural brain MRI scans stored at local federated sites. Each local scan is transformed into masked views: random masking, lifespan-guided masking, and difficulty-guided masking. Downstream inputs are task-specific structural MRI volumes for classification, regression, or segmentation.

### Outputs

During pretraining, the model reconstructs full MRI volumes from masked inputs. After pretraining, the decoder is discarded and the encoder outputs representations for downstream heads. Downstream outputs include class labels, scalar regression targets such as age or outcome measures, and voxel-level segmentation masks.

### Training objective (loss)

Pretraining uses masked-voxel mean squared reconstruction loss across the three masking views, plus a low-weight consistency term encouraging reconstructions from different masks of the same scan to agree. Local model updates are aggregated by site-priority weights at the server. Downstream training uses task-appropriate supervised losses for classification, regression, and segmentation.

### Architecture / parameterization

The foundation model is a 3D convolutional U-Net-style encoder-decoder for masked image modeling. Federated training keeps raw images local, exchanges model updates and site summaries, and maintains a global priority memory for spatial masking priorities. The retained foundation component is the pretrained encoder.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It tries to build a generalizable structural MRI foundation model without pooling raw images across sites and without letting large cohorts dominate pretraining at the expense of specialized or underrepresented cohorts.

### 2. What is the method?

BrainFedFM uses dual-priority federated pretraining. Spatial-priority masking at each site targets informative and difficult anatomical regions, while site-priority aggregation at the server weights sites by lifespan support and residual reconstruction difficulty. A global priority memory links these levels over training rounds.

### 3. What is the method motivation?

Centralized pooling can be blocked by privacy and governance constraints. Naive federated masked pretraining can still overemphasize large sites and random anatomy. The paper argues that a useful neuroimaging foundation model should prioritize both informative anatomy and complementary site contributions.

### 4. What data does it use?

Pretraining uses 164,707 structural brain MRI scans across 42 federated sites. Evaluation uses 20 downstream datasets covering 17 tasks: 11 classification datasets, 4 regression datasets, and 5 segmentation datasets, including autism, dementia, multiple sclerosis, epilepsy, radiogenomics, brain-age prediction, brain tumor segmentation, infant tissue segmentation, and MS lesion segmentation.

### 5. How is it evaluated?

The paper compares BrainFedFM against random initialization, centralized-pretraining models, and federated baselines such as FedMAE. Primary metrics are balanced accuracy for classification, RMSE for regression, and Dice for segmentation. It also evaluates limited-label settings, corresponding clinical tasks across cohorts, frozen-encoder adaptation, five-shot adaptation, and perturbation robustness.

### 6. What are the main results?

BrainFedFM reports the best overall mean rank, 1.68, across seven models. It reports best mean rank in classification, 1.50, and regression, 1.25, with segmentation mean rank 2.40 tied with S3D. Mean classification balanced accuracy reaches 74.0%, and the model maintains the best overall rank of 1.93 at both 50% and 25% labeled-data fractions. The paper also reports strong performance on underrepresented or clinically specialized tasks such as parkinsonism subtype classification, psychiatric differential diagnosis, and pediatric MS lesion segmentation.

### 7. What is actually novel?

The novelty is the dual-priority federation mechanism: local spatial priority plus server-side site priority, linked by a global priority memory. It is not just applying masked autoencoding in a federated setting.

### 8. What are the strengths?

The scale and breadth of evaluation are serious. The method directly addresses cohort imbalance, not only privacy. The paper also checks limited-label, frozen-encoder, and perturbation settings, which are closer to medical deployment constraints than a single leaderboard table.

### 9. What are the weaknesses, limitations, or red flags?

The segmentation gains are smaller than classification/regression gains. The method depends on a shared spatial coordinate system and standardized structural MRI preprocessing. Site summaries and priority weighting may still leak aggregate information if governance is strict, even though raw images stay local. The model is structural MRI-specific, not a general medical imaging foundation model.

### 10. What challenges or open problems remain?

Open problems include multi-modal MRI, cross-protocol generalization, prospective clinical validation, stronger privacy accounting for site summaries, and showing that priority aggregation remains stable when sites have noisy metadata or systematically biased cohorts.

### 11. What future work naturally follows?

Good follow-ups include adapting the priority-memory idea to multimodal medical imaging, testing differential privacy, extending to longitudinal MRI, and comparing against large centralized models under matched governance constraints.

### 12. Why does this matter for cabbageland?

It is a useful example of explicit prioritization in foundation-model pretraining. The model decides which anatomy and which sites deserve more learning pressure, instead of pretending scale alone will discover equitable representation.

### 13. What ideas are steal-worthy?

Keep a global priority memory across distributed learners. Separate local content priority from global contributor priority. In heterogeneous data, aggregation weights should reflect information contribution, not just sample count.

### 14. Final decision

Preserve as a useful medical/neuro foundation-model reference, with the caveat that its strongest mechanism is domain-specific.
