# Rethinking Contrastive Targets in Radiology Language-Image Pretraining

## Basic info

* Title: Rethinking Contrastive Targets in Radiology Language-Image Pretraining
* Authors: Yunhe Gao, Ashwin Kumar, Jiaming Liu, Chong Wang, Maya Varma, Fuying Wang, Stefania L. Moroianu, Louisa Fay, Sergios Gatidis, Akshay S. Chaudhari, Curtis Langlotz
* Year: 2026
* Venue / source: NeurIPS 2026, as identified in the manuscript; arXiv v1 submitted November 18, 2026
* Link: https://arxiv.org/abs/2611.24016
* Date surfaced: 2026-11-19
* Why selected in one sentence: It turns a vague medical-domain gap into a testable mismatch between paired identity and directional fact compatibility, with matched-architecture corrections and informative failure cases.

## Quick verdict

* Highly relevant

Preserve the target diagnosis, synthetic control, and assertion-level compatibility construction. The strongest contribution is not another medical encoder: it is showing how a contrastive objective can keep improving its own loss while learning the wrong relation. Treat the gradient algebra as a diagnosis, not a universal optimization theorem, and discount schema-aligned AUC until seed variability and held-out-fact behavior are tested.

## One-paragraph overview

Standard CLIP treats an image's paired report as its only positive text and every other report in the batch as negative. Radiology breaks that convention: many unrelated patients share findings, and a sentence can be true of an image without describing everything visible. CorLIP parses the paired report into a proxy image fact state, checks whether candidate texts assert compatible facts, and replaces one-hot targets with normalized compatibility weights. Sentence-level hard entailment is more reliable than collapsing a whole report's partial agreement into one scalar. A synthetic CLEVR-Radiology testbed reproduces late evaluation degradation and large-batch failure without medical appearance or jargon, supporting a structural explanation. The same target correction improves controlled CXR training and a smaller 3D CT transfer experiment.

**Reading basis:** [Accessible full PDF](https://arxiv.org/pdf/2611.24016): main diagnostic, theory, method, experiments, and discussion; Appendix C's extractor conventions; Appendix E's splits, selection, training, and CT details; selected theoretical passages and the statistical-reporting checklist. Not an abstract-only note; no exhaustive proof audit or training reproduction. The [announced code repository](https://github.com/yhygao/CorLIP) and its guessed main-branch README both returned HTTP 404 on November 19. The paper's code-release claim was therefore not independently verified. AlphaXiv's paper page was reachable as a discovery supplement, not the evidence source.

## Model definition

### Inputs

A CXR image and a text unit: full FINDINGS+IMPRESSION report, impression, or a randomly sampled sentence. Training additionally uses offline parsed facts. The paired full report approximates the image-side state; the candidate text contributes only the facts it actually asserts. This is report-derived supervision, not a second direct clinical reading of the pixels.

CXR uses 224×224 images. CT uses 3D volumes with Merlin preprocessing and FINDINGS text. At inference, class prompts or grounding phrases are embedded normally; neither MedGemma nor a compatibility parser runs in the inference path.

### Outputs

Image and text embeddings and their similarity scores. Zero-shot class scores compare image embeddings with class-name prompts. Dense phrase grounding uses text-to-dense-image similarity maps. This is representation learning, not a report generator, segmentation model, causal reasoner, or calibrated diagnostic probability model.

### Training objective (loss)

Let C_ij score whether image i's inferred state supports text j's assertions.

- **Sentence target:** C_ij = 1 when all extracted assertions hold, otherwise 0.
- **Bundled report/impression target:** C_ij is the fraction of asserted facts that agree.
- **Image-to-text target:** q_ij = C_ij / sum_k C_ik.
- **Text-to-image target:** normalize the same matrix by columns.
- **Loss:** ordinary symmetric CLIP cross-entropy, replacing paired one-hot targets with these distributions. Row contribution is minus sum_j q_ij log softmax_j(s_ij); the reverse direction is analogous.

Unmentioned candidate-text facts contribute neither agreement nor disagreement. Empty/nonclinical texts keep only the paired positive rather than becoming universally compatible. Force the paired diagonal to one to guard against parser inconsistency. CXR uncertain findings are mapped to absent/negative; CT uncertain triples are ignored. These conventions are substantive modeling choices.

CXR training uses AdamW, base learning rate 1e-4 at batch 128, batch-adapted rates capped at 4e-4, 5% warmup, cosine decay, and weight decay 1e-4. Controlled comparisons keep architecture, shared training choices, and data fixed within each setting. Batch sweeps are not a fixed-learning-rate experiment.

### Architecture / parameterization

CXR: DINOv3-initialized ViT-B/16 image encoder and BioClinicalBERT text encoder inside the shared contrastive pipeline. No new learned image encoder architecture is introduced.

Two offline fact extractors instantiate different targets:

- **CheXbert-13d:** coarse CheXpert-style findings, excluding the aggregate No Finding label from compatibility.
- **MedGemma-30d:** MedGemma-27B-Text-IT extracts a finer fixed schema including laterality and device distinctions. It is a report parser, not the image model or a training-time teacher queried every step.

CT: I3D ResNet-152 and Clinical Longformer, with 512-dimensional embeddings, plus a CT-specific offline MedGemma parser covering the Merlin-30d findings. Architecture and training follow Merlin defaults; maximum batch is 18 on an L40S, so CT does not validate the CXR large-batch claim.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Two medical-CLIP training failures: evaluation rises and then falls while training loss keeps falling; large batches can stall near chance. The proposed source is not merely noisy labels. Correctly paired identity is itself an incomplete target when many off-diagonal descriptions are clinically supported.

### 2. What is the method?

Parse reports once, construct each batch's compatibility matrix, row/column-normalize it, and train the same contrastive model against that target. Prefer sentence-level hard entailment to a whole-report similarity proxy. The direction matters: an image entails an assertion; it need not be semantically identical to a full report that contains it.

The method preserves pair-only supervision outside the schema. That avoids declaring every unparsed sentence a positive, but also leaves the original identity incentive in those regions. There is no learned ontology or symbolic theorem prover; the explicit structure is a finite schema plus assertion matching.

### 3. What is the method motivation?

The logit-space descent direction has an exact decomposition:

`e_i - p_i = (q_i - p_i) + (e_i - q_i)`

The first term follows the compatibility target; the second rewards the paired identity even among compatible texts. If m_i candidates are equally valid, a purely semantic model has a vanilla loss floor log(m_i). Further loss reduction can reward nonsemantic paired cues. On CLEVR-Radiology the floor can be computed from generator metadata, and evaluation degrades around the predicted regime. CXR grounding heatmaps also drift toward devices/markers after the peak.

At approximately uniform initial logits, the ratio of identity to semantic gradient energy grows with batch size when compatible pairs are common. This is an exact statement under the reference-target setup in logit space, **not** a proof that neural optimization must collapse. Parameter gradients multiply these terms by a learned Jacobian; initialization, learning rate, features, and optimization still matter. The synthetic intervention strengthens the causal case but does not eliminate every alternative explanation.

### 4. What data does it use?

Frontal MIMIC-CXR image/report pairs with both FINDINGS and IMPRESSION. Filtering gives a pool slightly above 120k; experiments use 60k and 120k subsets and retain official validation/test splits. Remove all MS-CXR images from pretraining because its grounding annotations sit on MIMIC.

CheXpert and VinDr are external zero-shot evaluation datasets, not pretraining sources. CLEVR-Radiology has 60k synthetic pairs split 40k/10k/10k with known object-attribute facts. The supporting CT experiment trains on 25,528 scans and evaluates 30 Merlin findings. These are retrospective, curated datasets, not prospective clinical deployment.

### 5. How is it evaluated?

CXR zero-shot mean AUC and F1; external CheXpert/VinDr classification; MS-CXR pointing-game accuracy; full learning trajectories; batch/text-unit sweeps; data-scale changes; and comparison with reimplemented SAT, MedCLIP, and Ko&Park target constructions. CT compares report vanilla, sentence vanilla, and sentence CorLIP while keeping its pipeline fixed.

**Selection distinction:** in-domain MIMIC peaks are retrospective maxima of test metrics, used to diagnose trajectory degradation. They are not deployable checkpoint-selection results. External classification/grounding rows use validation-selected checkpoints. Pointing accuracy only asks whether the heatmap maximum lands inside a box; it is not segmentation or complete localization quality.

The paper explicitly reports no multi-seed significance analysis for the grid. CT table confidence intervals must not be confused with repeated-training uncertainty. Shared recipes improve attribution; they do not replace replication or comparison with every full contemporary system.

### 6. What are the main results?

- **60k MIMIC, sentence:** vanilla peak/final AUC 68.2/66.5; CorLIP-CB 81.6/81.4; CorLIP-MG 75.8/75.8. The highest in-domain result uses the schema most coupled to its evaluation labels.
- **External evaluation:** CorLIP-MG sentence gives CheXpert/VinDr AUC 86.6/87.3 versus vanilla sentence 82.1/83.1. MS-CXR pointing accuracy is 41.6 versus 30.7; these numbers are percentages, not probabilities or Dice scores.
- **Data scaling:** 120k vanilla's best peak is 70.6; 120k CorLIP-CB sentence reaches 86.5/86.0 peak/final. This does not disentangle the effect of schema-aligned supervision from general-purpose semantic coverage.
- **Batch scaling:** corrected sentence training remains useful through batch 2048; its MG peak improves up to batch 512, then is roughly flat/slightly lower. Stability at larger batches is not monotonically improving quality. Report and impression correction still fail at large batch.
- **CT:** peak AUC 67.9 for report vanilla, 75.8 for sentence vanilla, and 79.3 for sentence CorLIP. Sentence granularity explains much of the full report-to-CorLIP difference; the matched correction gain is 3.5 points.
- **Cost:** reported offline processing of 120k reports on one H100 is under half an hour for CheXbert and about 1.5 hours for MedGemma with vLLM. No parser cost at inference does not mean no added preparation cost.

### 7. What is actually novel?

The useful package is the synthetic structural failure test, target-misspecification analysis of both trajectory regimes, and a directional assertion-compatibility target with matched-pipeline evaluation. False-negative correction, soft labels, clinical parsing, and supervised multi-positive contrastive learning already exist.

The distinction from report similarity is real: a short assertion can be supported by many images whose full reports differ. The distinction from supervised class equivalence is also real: compatibility is multi-label, partial, and directional. That does not make the components individually new or establish a universal theory of the medical domain gap.

### 8. What are the strengths?

A small intervention with a clear supervision interface; a synthetic testbed where compatibility is known; informative training trajectories rather than only final leaderboards; fixed-backbone target comparisons; external and dense-task checks; explicit failed report/impression variants; and disclosure of retrospective test peaks and missing multi-seed analysis. The structure actually changes target mass and therefore gradients—it is not decorative modularity.

### 9. What are the weaknesses, limitations, or red flags?

- **Proxy truth:** reports can omit findings, misstate them, or inherit reporting conventions. CorLIP does not independently verify image truth.
- **Schema coupling:** coarse CheXbert findings align with in-domain evaluation; CT extraction uses the same 30-finding schema as evaluation. Better scores within that vocabulary do not establish preserved open-world semantics.
- **Confounded comparison:** CB versus MG changes both extractor and fact granularity. Their gap cannot be assigned to granularity alone.
- **Clinical distinctions:** merging laterality can over-correct; excessive granularity can shrink positives back toward identity. Mapping uncertainty to absent is especially worth stress-testing.
- **Residual failures:** impression MG still loses 7.4 AUC points from peak to final. Target replacement alone is insufficient when compatibility is lossy.
- **Evidence precision:** no multi-seed grid; limited backbone/scale coverage. Exact logit algebra and plausible shortcut heatmaps do not prove every mechanistic claim at parameter level.
- **Artifact gap:** the linked public repository was unavailable during this read despite the paper's release statement. No code, weights, or parser prompts were executed or inspected from that repository.

### 10. What challenges or open problems remain?

Recovering faithful image-side state from incomplete reports; modeling severity, temporal change, laterality, and uncertain evidence without collapsing useful distinctions; learning hierarchical compatibility; and retaining rare facts outside the parser vocabulary. Domain shift can change both the reporting language and the clinical relation, not merely image appearance. The paper does not establish calibration, safe decision thresholds, prospective performance, or continual adaptation.

### 11. What future work naturally follows?

Run repeated seeds on a smaller matched grid. Cross extractor and granularity independently. Audit parser errors against adjudicated image findings. Hold out whole findings and institutions, and measure laterality/negation/uncertainty discrimination. Compare exact entailment, calibrated partial compatibility, and ontology-aware kernels. Add global-local objectives only after isolating target effects; then test report generation, segmentation, and supervised fine-tuning. Measure compatibility construction cost and rare-fact behavior as batch size grows.

### 12. Why does this matter for cabbageland?

It is a reusable lesson in compositional representation learning: decide which relations deserve attraction before scaling data or adding modules. Explicit semantic state can improve supervision without being a new latent bottleneck or decoder. The same question applies to descriptions of scenes, behaviors, or scientific systems, but transferring it requires a defensible fact extractor and relation—not merely renaming negatives as compatible.

### 13. What ideas are steal-worthy?

1. Build a synthetic generator preserving only the suspected structural failure, with exact metadata to compute its predicted boundary.
2. Separate assertion entailment from instance identity and global similarity.
3. Change targets with matched encoders and optimization before crediting architecture.
4. Treat schema granularity as an experimental variable and evaluate the distinctions it merges.
5. Track a task metric throughout training: a lower objective can mean stronger shortcuts rather than better semantics.
6. Keep paired-only fallback for uncovered content, but report how often it occurs and whether it hides rare-fact failures.

### 14. Final decision

**Preserve.** Use CorLIP as a compatibility-target baseline and a template for diagnosing structural supervision errors. Before treating it as a ready-to-reproduce method, recover the unavailable code and validate the parser/schema interface. Before calling it a general medical foundation-model advance, establish repeated-seed robustness, held-out-fact preservation, and performance beyond image–text similarity probes. No audio requested or generated.
