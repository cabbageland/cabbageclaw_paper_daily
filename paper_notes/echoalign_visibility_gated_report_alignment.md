# EchoAlign: Echocardiography foundation model with multilevel report alignment

## Basic info

* Title: EchoAlign: Echocardiography foundation model with multilevel report alignment
* Authors: Ahmed Aly, Darya Taratynova, Lotfi Abdelkrim Mecharbat, Roman A. Sandler, Joseph Z. Sokol, Joshua Penn, Klaus H. Maier-Hein, Numan Saeed, Mohammad Yaqub
* Year: 2026
* Venue / source: arXiv preprint, v1 submitted November 20, 2026
* Link: https://arxiv.org/abs/2611.27517
* Date surfaced: 2026-11-23
* Why selected in one sentence: It turns view-dependent observability into explicit contrastive-supervision rules and evaluates structured clinical features across external sources.

## Quick verdict

* Highly relevant

Preserve the supervision design: a clip should not inherit every finding in its study report. The external comparisons and matched-data recipe experiment are useful, but they do not isolate visibility gating from the rest of the architecture. Anatomical embedding names and eligibility masks should not be mistaken for enforced anatomical localization.

**Read basis:** Main results/discussion and substantive Methods inspection, including architecture, all four losses, visibility/caption construction, pretraining counts, evaluation splits, feature/probe construction, and statistical analysis; selected extended-data results. Not every extended-data cell or preprocessing artifact audited. Primary [full PDF](https://arxiv.org/pdf/2611.27517); no result reproduction.

**Artifact check:** The manuscript's advertised [GitHub repository](https://github.com/BioMedIA-MBZUAI/EchoAlign) returned HTTP 404 during this run. Public code/weight availability is therefore unverified, despite the manuscript's release statement. Full-text access itself succeeded directly through arXiv.

## One-paragraph overview

EchoAlign learns from echocardiographic studies and their structured reports using global and anatomical video/study embeddings. An expert matrix specifies which cardiac structures are expected to be visible in each view; it controls eligible structure supervision, samples view-appropriate captions, and restricts part of training-time study pooling. Four contrastive losses align the visual hierarchy with report text. Training uses 2.65 million videos/stills from 60,782 studies, with another 0.217 million validation videos included in the headline 2.87 million. Across 68 classification task-source pairs, frozen-feature probes reach mean AUROC 0.890 versus EchoPrime's 0.880; severity grading averages QWK 0.530 versus 0.505. The model is not best on every dataset or task family. This is promising structured weak supervision, not a demonstrated shortcut-free or clinically deployed system; internal cross-attention remains unrestricted and the advertised release could not be verified.

## Model definition

### Inputs

Videos, still images and clinical reports during pretraining; view labels and modality labels are also available for training. Each video clip uses 16 frames resized to 224-by-224. Reports provide a conclusion and findings for 12 cardiac structures. Text inputs are limited to 256 tokens, with sentence-window sampling for longer passages. A batch contains chunks of one to eight videos from a study.

Inference uses images/videos without reports or view labels. Fitted clinical probes receive fixed study-level feature vectors. Prompt-based scoring additionally receives present/absent text descriptions.

### Outputs

Each video produces one global and 12 anatomical embeddings. A study transformer pools videos into the corresponding 13 study embeddings, each 512-dimensional. These are representations, not directly calibrated clinical diagnoses or pixel masks.

Text-prompt classification uses cosine-similarity differences between present and absent descriptions. Fitted classification, grading and measurement heads use 832 features: 64 principal components for each of 13 study embeddings, concatenated. Segmentation requires a separately trained convolutional decoder.

### Training objective (loss)

Four CLIP-style contrastive losses, using normalized embeddings and a shared learned logit scale bounded to [1, 32]:

`L_align = L_video + 0.5 L_video-structure + 0.5 L_study + 0.1 L_study-structure`.

- **Video:** Match the global embedding to a sampled caption. Identical captions are excluded from negatives; videos from the same study can otherwise remain negatives.
- **Video-structure:** Match eligible anatomical video embeddings to that structure's report finding. Eligibility requires positive view visibility and a nonempty finding; identical findings are excluded from negatives.
- **Study:** Match the global pooled embedding to the study text. Identical texts form an equal-weight positive set.
- **Study-structure:** Match eligible anatomical study embeddings to their structure text. At least one sampled view must have positive visibility. An absent finding is encoded as empty text when the structure otherwise qualifies.

Downstream classification uses regularized logistic regression; measurement uses ridge regression. The paper calls the grading head an ordinal probe, but implements multinomial logistic regression followed by expected-grade scoring and QWK-tuned cut points, not a monotonic cumulative-link architecture. Segmentation decoders are supervised separately.

### Architecture / parameterization

A Kinetics-400-initialized TimeSformer video encoder and PubMedBERT text encoder, both fine-tuned. Linear projections map 768-dimensional class tokens to 512-dimensional normalized global embeddings.

Twelve learned anatomical queries cross-attend to all 3,136 video patch tokens. They are not spatially masked. The structure losses teach each query its anatomical association.

The study model uses two self-attention layers, four heads and no video positional encoding, treating videos as an unordered set. Modality/token-role embeddings distinguish inputs. Thirteen learned pooling queries read global or structure-specific tokens. Self-attention mixes all study tokens before this pooling.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

A study report describes anatomy distributed across many views. Pairing every clip with that entire report supervises findings the clip cannot show and permits spurious correlations. The goal is reusable, anatomically associated representations without collecting new labels for every downstream task.

### 2. What is the method?

Construct a 66-view by 12-structure expert visibility matrix with weights in `{0, 0.1, 0.3, 0.5, 0.8, 1}`. For caption construction, draw a threshold uniformly in [0, 1] and include findings whose visibility exceeds it, with additional dropping/shuffling. A caption prefix includes modality, view and available study measurements. Conclusions are used as fallback in specified cases.

Use the matrix to gate video-structure loss eligibility and training-time anatomical pooling. Jointly optimize global and structure-level video/study alignment. At inference, pool without view labels and read either prompt similarities or fitted heads.

### 3. What is the method motivation?

Move weak supervision closer to the evidence that could support it. Report structure is a reusable annotation resource; expected observability is a supervision constraint. Multi-video study aggregation then restores information that no individual view contains.

This is a softer claim than proving that a prediction used only visible anatomy. The global branches, caption measurements/fallbacks, unrestricted patch attention and cross-token study attention retain other information paths.

### 4. What data does it use?

The detailed pretraining count is 2,651,674 videos/stills from 60,782 studies across 150 centers: 1,033,450 B-mode videos, 832,319 color Doppler videos and 785,905 stills. The separate pretraining validation set adds 217,195 videos from nine centers, bringing development to 2,868,869 items across 159 centers.

The private test set has 11,797 studies and 362,374 videos from 18 external centers. MIMIC-IV-Echo contributes patient-split evaluation; CardioBench supplies eight public datasets. The private corpus is not released. MIMIC access requires credentialing/data-use compliance.

### 5. How is it evaluated?

Six models on the same task-specific test samples and labels: EchoAlign, EchoPrime, EchoCLIP, PanEcho, EchoJEPA and EchoFM. Across sources there are 68 classification task-source pairs, 31 grading pairs, 25 measurement pairs and three segmentation targets, representing 62 distinct findings rather than 68 independent diseases.

Frozen-feature heads are selected using validation performance and refitted on training plus validation data. EchoAlign's PCA is fitted without labels on private training studies and transferred unchanged to external sources. Text prompts are selected on private validation data and transferred where findings overlap: zero-shot means no fitted target-task head, not an absence of all prompt selection.

Main means weight task-source pairs equally. Cluster bootstraps resample studies or patients according to source, with paired comparisons across models; P values are not adjusted for multiple comparisons. One comparator, released EchoJEPA, was pretrained on MIMIC videos, so its MIMIC result is not genuinely external to its pretraining.

### 6. What are the main results?

- Classification linear-probe mean AUROC: 0.890, versus EchoPrime 0.880 and EchoCLIP 0.860. EchoAlign ranks first on 32/68 task-source pairs, not all 68.
- Text-prompt mean AUROC: 0.796, versus 0.692 for both EchoPrime and EchoCLIP over the evaluated 68-pair extension protocol.
- Severity mean QWK: 0.530, versus EchoPrime 0.505. On MIMIC alone, 0.562 versus 0.561 is not significantly different.
- Mean classification is not significantly better than EchoPrime on MIMIC or than any comparator on CardioBench. An aggregate win should not erase this.
- Matched 30K-study pretraining: EchoAlign recipe 0.869 versus reproduced EchoPrime recipe 0.803 AUROC. This compares entire recipes, not an isolated visibility ingredient.
- EchoPrime has the lowest measurement RMSE on 11/25 tasks versus EchoAlign on six. EchoFM beats EchoAlign on mean CAMUS Dice, 0.892 versus 0.880.

### 7. What is actually novel?

The defensible mechanism is integrating view-dependent supervision eligibility with report-structured anatomical video/study representations. CLIP, TimeSformer, learned queries and attention pooling are existing components. This is structured weak supervision, not a new causal anatomical parser.

### 8. What are the strengths?

Clinical report organization does real work in the objective. The paper supplies concrete supervision rules, handles duplicate negatives, combines local and study-level information, and checks external datasets instead of only within-center performance. Matched-data recipe comparisons and frozen-feature heads strengthen the representation case. Reporting measurement/segmentation losses and nonsignificant source-level comparisons keeps the claim honest.

### 9. What are the weaknesses, limitations, or red flags?

- Queries can attend to every image patch, and study self-attention mixes structures. Eligibility/pooling masks do not enforce localized evidence or exclude shortcuts.
- The expected-visibility matrix is expert prior knowledge, not a per-instance measurement of actual observability. Pathology, image quality and unusual views may violate it.
- At inference all views are treated as unknown and anatomical queries attend across all videos. Training includes a 10% all-visible pooling fallback to bridge this change.
- Comparisons vary encoders, initialization, feature dimensions and pooling. Matched data do not match all capacity or isolate components.
- Retrospective report-derived targets inherit reporting variability and missingness. Some severity grades are merged/excluded according to dataset-specific rules.
- Aggregate metrics obscure small cohorts and task dependence; repeated unadjusted significance tests should not be overread.
- No prospective diagnostic benefit, calibration guarantee, or net clinical benefit is demonstrated.
- Private pretraining data and the unverified advertised release limit independent reproduction. The recipe uses 64 MI210 GPUs, not a cheap head-only training exercise.

### 10. What challenges or open problems remain?

Determine whether visibility gating reduces shortcut use under targeted interventions and external shifts. Maintain quality when view labels are wrong or anatomy is only partially visible. Establish whether named features improve explanations and clinical decisions, not just retrospective ranking.

### 11. What future work naturally follows?

Run factorial ablations of visibility weights, sampled captions, anatomical queries and study pooling with matched compute/features. Perturb non-target structures and scanner/view correlations to test evidence localization. Compare learned versus expert per-instance visibility. Evaluate calibration, referral thresholds, rare findings and prospective reading-time/missed-diagnosis outcomes.

### 12. Why does this matter for cabbageland?

It is a clear example of explicit structure operating at the supervision interface. The same idea transfers to multimodal scientific data: do not train every local observation on every global label. But keep the distinction between a constrained loss, a structured representation, and a constrained information pathway; only the first two are partially addressed here.

### 13. What ideas are steal-worthy?

- Model supervision eligibility separately from label content and confidence.
- Exploit existing structured reports before generating additional labels.
- Preserve global and part-level readouts, then test whether each earns its role.
- Separate anatomy association from evidence localization in evaluation.
- State data counts by training/validation/test role; do not turn development scale into training scale.
- Audit comparator pretraining exposure, prompt selection, task-source weighting and release availability alongside headline scores.

### 14. Final decision

Preserve as a mechanism-rich clinical representation paper and a visibility-aware supervision pattern. Use it as a baseline/framing reference, not as proof of anatomy-grounded causality or clinical deployment readiness. Revisit reproduction when the advertised artifacts become accessible.
