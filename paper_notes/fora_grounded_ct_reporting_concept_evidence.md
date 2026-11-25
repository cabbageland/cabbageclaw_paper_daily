# Reliable and grounded reporting of any computed tomography scan with FORA

## Basic info

* Title: Reliable and grounded reporting of any computed tomography scan with FORA
* Authors: Sezgin Er, Utku Turkbey, Alperen Gür, Omer Faruk Durugol, and colleagues; senior authors include Bernhard Kainz, Bjoern Menze, and Ibrahim Ethem Hamamci
* Year: 2026
* Venue / source: arXiv preprint, 2611.32823v1, submitted November 24, 2026
* Link: https://arxiv.org/abs/2611.32823
* Date surfaced: 2026-11-25
* Why selected in one sentence: It links a large explicit radiological concept vocabulary to localized evidence and report planning, while exposing exactly where coverage, weak labels, and visual bypasses complicate interpretability claims.

## Quick verdict

* Highly relevant

Preserve as a serious structured-perception-to-language recipe and an important CT baseline. The headline performance is not a clean matched-capability comparison, and its “concept bottleneck” is not concept-only: the writer also reads visual features. Strong classification and additive evidence maps do not establish causal faithfulness or clinical readiness.

**Access:** Full PDF acquired. Read main results/discussion and methods for data/splits, label extraction, encoder objectives, anatomical routing, evidence construction, writer training, baseline scoring, localization/report evaluation, and release statements. Selected supplementary figures consulted, not the entire supplement. The [public repository](https://github.com/forithmus/FORA) resolves; no weights or inference were executed. The paper says complete CT data are not yet fully available and offers model-submission evaluation.

## One-paragraph overview

FORA trains a volumetric encoder from routine CT, extracts a hierarchy of findings from accompanying reports, and learns examination-level finding classifiers over all available views. Anatomical routing narrows attention without deleting the rest of the scan. Each finding's study score decomposes into token contributions, which become spatial evidence and a structured report plan. A language model receives that plan together with image features and evidence views, then learns to write reports through supervised fine-tuning and preference optimization. The contribution is a broad, inspectable integration of recognition, weakly supervised localization, and reporting—not proof that every generated sentence is grounded exclusively in a causally necessary concept.

## Model definition

### Inputs

All usable CT reconstructions and intensity views form an examination bag. Series are resampled to 1.5×0.5×0.5 mm; views include full-range intensities, native windows, and specified lung projections. Anatomical masks from CADS supply routing and locations. During training, translated reports supply finding labels and report targets. The writer receives a tiered finding plan, compressed visual tokens, study/focus tokens, and selected evidence images; it does not need the reference report as inference input.

### Outputs

Probabilities for 1,028 hierarchical radiological concepts; additive token-level evidence and up to four spatial foci per finding; a finding/location/probability/measurement plan; and a generated Findings section. “Any CT” means broad protocol coverage in this study, not validated coverage of every scanner, patient population, or acquisition protocol.

### Training objective (loss)

1. **Encoder:** DINO, iBOT, KoLeo, and cross-crop patch self-distillation objectives. A later Gram-anchoring loss preserves pairwise patch-feature similarities.
2. **Report alignment:** Contrastive alignment of image features to report-derived presence/absence sentences, treating a report's statements as positives.
3. **Finding classifiers:** Unweighted binary cross-entropy across modeled findings. Rare children initialize from and are regularized toward an ancestor head.
4. **Writer:** Supervised report-token training followed by sigmoid DPO with beta 0.1 and a cross-entropy term on preferred reports. Preference pairs include omissions, additions, wrong attributes, repetition, and contradictions; the second-stage writer is the frozen reference.
5. **Calibration:** Per-finding Platt scaling and Youden thresholds fit using training predictions only, not external evaluation labels.

### Architecture / parameterization

A 302.9M-parameter 3D ViT-L has 24 blocks, 1,024-dimensional embeddings, four register tokens, millimetre-aware 3D rotary positions, and 2×16×16-voxel patches. After self-supervised training, blocks 1–23 freeze; block 24 supports later alignment/classification.

A finding-specific gated attention head scores tokens, a separate network assigns token logits, and the study logit is their attention-weighted mean plus scale/bias. Routing subtracts a learned penalty from outside-organ attention scores; it is soft, not an exclusion constraint. Positive signed logit contributions are combined across views and smoothed to construct evidence maps.

The writer is Gemma-4-31B-it with rank-16 LoRA on attention/feed-forward projections, a 512-token query resampler, and a vision pathway for evidence images. Its visual bypass means this is an explicit concept interface, not a strict concept bottleneck.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Broad CT interpretation requires finding recognition, spatial support, and coherent reporting across anatomy and protocols. Existing released systems often cover only a subset of these functions or findings. FORA attempts to combine them using routine reports rather than manual lesion labeling.

### 2. What is the method?

Build a report-derived hierarchical vocabulary, pretrain volumetric features, learn organ-routed multiple-instance recognition, convert token score contributions into evidence foci, and give a writer a structured finding plan plus images. Preference training emphasizes completeness and factual attributes. Train a separate chest-radiograph model to establish the recipe in 2D before the CT system; the results are not one CT model evaluated on X-rays.

### 3. What is the method motivation?

Study-level reports are plentiful, whereas exhaustive lesion masks are expensive. MIL lets examination labels supervise localized evidence. Hierarchical heads share information with rarer findings; anatomical routing reduces irrelevant search; a finding plan exposes decisions before prose generation. The design earns “explicit structure” through identifiable targets and score decomposition, but not through a guaranteed faithful language bottleneck.

### 4. What data does it use?

341,581 CT examinations from 238,469 patients in one hospital network, spanning 28 protocol classes. The patient-disjoint split contains 304,962 training examinations from 213,106 patients and 36,619 held-out examinations from 25,363 patients. CT-RATE validation studies, including ReXGroundingCT cases, are excluded from training. Training contains 2,332,070 intensity views.

Reports are translated from Turkish into English and labeled by Gemma-4-31B-it with candidate extraction, quote verification, correction, and hierarchy propagation. Asserted and uncertain findings count positive; unmentioned findings count negative. The 1,459-concept vocabulary yields 749 common and 279 rare modeled targets. These are derived report labels, not exhaustive independent radiologist annotations.

### 5. How is it evaluated?

Internal recognition against 18 released CT models; public recognition on CT-RATE, Merlin, and RAD-ChestCT; independent localization annotations including FUMPE, KiTS23, RibFrac, and ReXGroundingCT; reporting against released generators using finding extraction and an LLM judge. Public datasets include genuinely external institutions, while CT-RATE shares the training hospital network with patient exclusions.

Crucial baseline rule: unavailable findings and unprocessable examinations count as negative predictions. Thus broad internal metrics assess coverage plus discrimination. They do not isolate architecture quality on identical supported labels. Localization comparisons also score unsupported targets zero. Matched-label external comparisons are particularly valuable checks.

### 6. What are the main results?

- Internal macro AUROC 0.918 versus CoLiPri 0.705; AUPRC 0.393 versus 0.146.
- External Merlin AUROC 0.907 versus Merlin 0.826; RAD-ChestCT 0.816 versus 0.796 for the strongest alternative. On the selected Merlin concepts, RADAR's published protocol yields 0.885 versus FORA 0.916.
- Top-focus hit rates: pulmonary emboli 69.7%, renal masses 72.8%, renal cysts 66.1%, rib fractures 58.3%, and ReXGroundingCT chest findings 27.6%.
- Internal report macro recall/precision 0.215/0.285 versus NV-Reason-CT 0.066/0.132. More than threefold recall is still only about one fifth of modeled reference findings under that macro metric.
- Not universal dominance: renal-cyst recognition on KiTS23 is below RADAR, and ReXGroundingCT top-focus localization is similar to GLINT-CT, 27.6% versus 27.9%.

### 7. What is actually novel?

The broad hierarchy, organ-routed MIL evidence interface, and concept-plus-evidence report pipeline form the substantive integrated contribution. DINO-style pretraining, MIL, LoRA, calibration, and DPO are established components. Dataset scale, coverage, annotation engineering, and training recipe must not be relabeled as a single new architecture effect.

### 8. What are the strengths?

Patient-disjoint development, training-only calibration, explicit external checks, independent lesion annotations, exposed intermediate findings, separate reporting/localization metrics, and an unusually concrete account of baseline failure/coverage handling. The paper explicitly distinguishes additive evidence from causal dependence. The representation and longitudinal-profile analyses are additional probes, not a substitute for clinical evaluation.

### 9. What are the weaknesses, limitations, or red flags?

- Single-network training limits institutional generalization; translated and LLM-extracted labels inherit reporting conventions and omissions.
- Unmentioned-as-negative introduces false negatives; uncertain-as-positive merges different clinical states.
- Coverage penalties can inflate headline gaps over narrower models. Generative baselines also receive the longest series while FORA exploits multi-view bags.
- Spatial evidence sums into the classifier score but has not undergone the interventional tests needed for causal attribution. Only a fraction of 1,028 concepts has annotated localization validation.
- Overlap of an evidence region with a lesion is not segmentation accuracy; “348× chance” is not 348× clinical utility.
- The writer can bypass concepts through image tokens. Concept edits need not fully determine prose.
- Report labels, writer initialization, extraction, and judging share a model family, creating correlated-error concerns. Independent clinical review remains necessary.
- The full CT cohort is not publicly downloadable, and large-scale pretraining uses 128 H200 GPUs. This is not a cheap-reproduction claim.

### 10. What challenges or open problems remain?

Validate small/diffuse findings and rare concepts across institutions; quantify omitted-report labels; calibrate under prevalence/protocol shift; measure report hallucinations and meaningful omissions with clinicians; and establish whether evidence actually supports efficient correction. Stable patient profiles do not establish accurate disease-progression reasoning.

### 11. What future work naturally follows?

Run concept-only, visual-only, and combined writer ablations with matched training and decoding. Intervene on localized evidence and finding plans, including false but high-confidence findings. Evaluate shared-label subsets separately from coverage, with matched input views. Conduct external reader studies measuring diagnostic accuracy, review time, corrections, and automation-induced mistakes rather than only LLM preference.

### 12. Why does this matter for cabbageland?

This is a non-robotics example of explicit structure doing actual work: a finding vocabulary, an anatomical routing table, spatial evidence, and a report plan. It offers a reusable evidence-bearing perception-to-language interface while illustrating why inspectability, causal faithfulness, and deployment validity must remain separate claims.

### 13. What ideas are steal-worthy?

1. Expose prediction, evidence, and prose as separately scored interfaces.
2. Route evidence softly through anatomy while allowing exceptions for displaced or absent organs.
3. Preserve rare-target structure through ancestor initialization/regularization.
4. Build omission-focused preference pairs, but verify completeness with an independent evaluator.
5. Publish coverage-aware and matched-support comparisons side by side.
6. Treat concept editing and evidence occlusion as required tests before claiming explanations.

### 14. Final decision

Preserve as an architectural recipe, CT baseline, and evaluation case study. Reproduce an accessible matched-label/localization comparison before trusting the broad leaderboard gap. Describe it as structured, evidence-bearing reporting—not a causally faithful concept-only system or a clinically validated autonomous reader.
