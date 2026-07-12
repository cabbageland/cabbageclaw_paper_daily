# Learning Sparse Latent Predictive Foundation Model for Multimodal Neuroimaging

## Basic info

* Title: Learning Sparse Latent Predictive Foundation Model for Multimodal Neuroimaging
* Authors: Haoxu Huang, Long Chen, Jingyun Chen, Jinu Hyun, James Ryan Loftus, Kara Melmed, Daniel Orringer, Jennifer Frontera, Seena Dehkharghani, Arjun Masurkar, Narges Razavian
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.14957
* Date surfaced: 2026-07-12
* Why selected in one sentence: It is a missed-but-strong multimodal neuroimaging foundation-model paper that combines JEPA, sparse MoE routing, neuroimaging-specific masking, and unusually serious clinical plus public evaluation.

## Quick verdict

* Highly relevant

This absolutely should have been surfaced in the daily scout. The paper is not a totally new paradigm in the abstract, but it is much more serious than the average medical-foundation-model preprint because the authors do three things at once: adapt the representation-learning recipe to the geometry of 3D brain MRI, train at real health-system scale, and compare against both foundation-model peers and a simple supervised CNN baseline. I inspected the full PDF, including the architecture, JEPA objective, masking and foreground-loss design, unimodal and multimodal result sections, few-shot analysis, scaling and ablation studies, cross-cohort and unseen-modality checks, CNN comparison, and MoE routing analysis.

## One-paragraph overview

Neuro-JEPA is a 3D multimodal brain MRI foundation model built from a ViT backbone, JEPA latent prediction, and sparse Mixture-of-Experts routing. It is pretrained on 1,551,862 curated T1w, T2w, and FLAIR scans from 428,647 studies and 282,693 patients at NYU Langone, then evaluated across three health systems and 12 public cohorts on diagnosis, prognosis, time-to-event, age-prediction, multimodal fusion, few-shot, and transfer settings. The main pitch is not merely "JEPA works for MRI." The more useful claim is that multimodal brain MRI needs specific design choices: masking that respects fine 3D anatomy, loss weighting that suppresses huge low-information background regions, and sparse routing that can separate heterogeneous anatomical tokens. The paper reports consistent gains over BrainIAC, VoCo, and NeuroVFM, and it is the only evaluated foundation model in the paper that consistently beats a simple task-specific CNN baseline on the public-task average.

## Model definition

### Inputs
The model receives structural brain MRI volumes from three core modalities: T1-weighted, T2-weighted, and FLAIR. Volumes are resized and cropped to 96 x 108 x 96 with patch size 12 x 12 x 12, yielding 576 tokens per scan.

### Outputs
During pretraining, the model predicts latent target embeddings for masked regions. During downstream evaluation, fine-tuned heads produce diagnosis, prognosis, time-to-event, and age-prediction outputs, and the learned embeddings are also evaluated in multimodal fusion settings.

### Training objective (loss)
Pretraining uses JEPA: an online encoder predicts latent embeddings for masked regions while a momentum EMA encoder provides target embeddings from the full volume. The latent prediction loss is a foreground-aware L1 objective that down-weights background-heavy regions with beta = 0.1 after normalization. Downstream tasks use task-appropriate supervised heads and losses after fine-tuning.

### Architecture / parameterization
Neuro-JEPA uses a 12-layer 3D ViT with hidden size 768, MLP size 3072, and 12 attention heads. MoE routing is applied on alternating layers, so 6 of 12 layers are sparse. The MoE uses 2 shared experts, 16 total experts, and 6 active experts per forward pass with softmax gating and routing scale 4.0. The evaluated ViT-Base MoE configuration has 122 million total parameters and 86 million activated parameters.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Clinical brain MRI is inherently multimodal, but most neuroimaging foundation-model evaluation still treats each sequence separately or uses weak fusion comparisons. The paper is trying to learn a single representation space that can encode complementary T1w, T2w, and FLAIR information robustly enough to transfer across real health-system data and public cohorts.

### 2. What is the method?
The method is a multimodal 3D ViT trained with JEPA latent prediction and sparse MoE routing, plus two domain-specific changes: multiscale masking tailored to volumetric anatomy and a foreground-aware latent loss that suppresses low-information background regions. The authors then evaluate the same pretrained backbone in unimodal, multimodal, few-shot, scaling, and transfer settings.

### 3. What is the method motivation?
The motivation is that routine brain MRI is not one image source but a coordinated bundle of complementary contrasts. T1w carries anatomy, T2w highlights fluid-sensitive structure, and FLAIR accentuates lesion-relevant signal after suppressing CSF. A useful model should learn the shared structure and the complementary differences without wasting capacity on skull-stripped background or using a masking scheme borrowed blindly from video.

### 4. What data does it use?
Pretraining uses 1,551,862 curated structural MRI scans from 428,647 studies and 282,693 patients in the NYU Langone archive. Downstream evaluation spans three health systems and 12 public datasets, with 47 task settings described in the paper across diagnosis, prognosis, time-to-event prediction, age prediction, and multimodal fusion. The paper also reports cross-cohort transfer and unseen-modality evaluation on diffusion-weighted MRI tasks.

### 5. How is it evaluated?
The paper evaluates unimodal encoding quality, multimodal fusion gain over the best unimodal baseline under matched sample counts, few-shot label efficiency with K in {16, 32, 64, 128, 256}, ablations for masking, MoE, foreground-aware loss, and pretraining data scale, plus cross-cohort and unseen-modality transfer. It compares against VoCo, BrainIAC, NeuroVFM, and a simple supervised neuroimaging CNN trained from scratch.

### 6. What are the main results?
The paper reports that Neuro-JEPA consistently beats the compared neuroimaging foundation models across unimodal and multimodal settings. On best-achievable unimodal public-task performance, it reports average gains of 4.4 to 6.4 in AUROC and 6.4 to 9.4 in AUPRC over the compared foundation-model baselines. On the evaluated multimodal public tasks, it reports gains of 5.8 to 7.6 in AUROC and 6.2 to 8.5 in AUPRC, with consistent wins on the majority of task combinations. The ablations are also important: multiscale masking alone improves mean AUROC by 1.5 and AUPRC by 2.5, adding MoE contributes another 3.9 AUROC and 3.4 AUPRC, and the foreground-aware loss adds 0.9 AUROC and 2.8 AUPRC. In few-shot settings the model remains strongest, and it is the only foundation model in the paper that consistently outperforms the simple CNN baseline on the public benchmark average, with reported gains of 3.7 AUROC and 4.5 AUPRC.

### 7. What is actually novel?
The paper's novelty is mostly in the integrated recipe and the evaluation discipline rather than in inventing JEPA or MoE from scratch. The most useful novel pieces are: adapting masked latent prediction to 3D neuroanatomy through multiscale masking, explicitly suppressing background signal in the latent loss, and showing that sparse routing plus these data-specific choices hold up across multimodal, few-shot, and CNN-baseline comparisons.

### 8. What are the strengths?
The paper is strong on scale, benchmarking breadth, and ablation discipline. It uses real clinical data volume, compares against serious domain baselines, checks multimodal gain under matched sample counts, tests few-shot and cross-cohort transfer, and does the rare but important thing of comparing foundation models against a simple supervised CNN. That CNN comparison makes the paper much more trustworthy than a lot of medical-foundation-model work that only compares inside the foundation-model club.

### 9. What are the weaknesses, limitations, or red flags?
This is more of a strong systems-and-evaluation paper than a clean conceptual leap. The pretraining data still comes from one health-system source, so scanner, protocol, and disease-distribution biases can survive despite the large scale. The evaluation focuses on image-level tasks rather than segmentation or clinically interactive reasoning, so it does not prove universal neuroimaging competence. The multimodal setup is still limited to structural MRI rather than broader clinical modalities, and MoE routing analyses are suggestive rather than proof that the experts learned semantically clean anatomical specializations. Also, some gains over NeuroVFM are more modest on external multimodal MGH tasks than the headline public-benchmark averages.

### 10. What challenges or open problems remain?
The big open problems are broader site generalization, missing-modality robustness, prospective clinical validation, and extension beyond structural MRI into richer neuroimaging regimes such as diffusion, perfusion, or functional data. Another open question is whether the learned multimodal representation helps with more structured downstream tasks like segmentation, report grounding, or causal disease progression modeling rather than only image-level prediction.

### 11. What future work naturally follows?
A natural next step is testing the same recipe on broader neuroimaging modality families and more external institutions, especially prospective or semi-prospective workflows. Another good follow-up would connect the learned representation to localization-heavy tasks such as lesion segmentation or report-grounded reasoning, where the background-suppression and routing ideas could be stress-tested more sharply. Missing-modality training and calibration analysis would also matter for actual clinical deployment.

### 12. Why does this matter for cabbageland?
This is exactly the kind of medical or neuro paper Paper Daily should catch. It is mechanism-rich enough to matter, but it also carries a healthy evaluation lesson: do not celebrate a foundation model just because it beats other foundation models. Compare it with a simple task-specific baseline, test multimodal gain under matched sample counts, and make sure the data geometry actually shaped the pretraining recipe. The transferable design instinct is clear: when the measurement process creates distinct but complementary channels, give the representation explicit help to preserve that structure instead of flattening everything into one generic latent mush.

### 13. What ideas are steal-worthy?
Adjust predictive latent training to the topology of the data rather than reusing a default masking scheme from another domain. Down-weight low-information background aggressively when it dominates the volume. Treat sparse routing as an ablated capacity tool, not as automatic magic. When claiming multimodal learning, measure gain over the best unimodal result under matched sample counts. And always include a plain supervised baseline if the pitch is "foundation model superiority."

### 14. Final decision
Preserve. This is a strong multimodal neuroimaging foundation-model note, a useful evaluation reference, and a deserved backfill for a paper that should have cleared the scout the first time.
