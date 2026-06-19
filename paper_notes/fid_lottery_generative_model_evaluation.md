# The FID Lottery: Quantifying Hidden Randomness in Generative-Model Evaluation

## Basic info

* Title: The FID Lottery: Quantifying Hidden Randomness in Generative-Model Evaluation
* Authors: Nicolas Dufour, Alexei A. Efros, Patrick Perez
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.20536
* Date surfaced: 2026-06-19
* Why selected in one sentence: It shows that many image-generation FID claims are smaller than the training-seed randomness they do not report.

## Quick verdict

* Highly relevant

This is a strong evaluation audit. I inspected the full arXiv PDF, including the experimental setup, variance decomposition, guidance-tuning protocol, compute/scale analysis, and limitations. The result is directly useful for reading generative-model papers that claim small FID wins from a single trained model.

## One-paragraph overview

The paper treats FID not as a single deterministic leaderboard number but as a random variable over two axes: training seeds and sampling seeds. On panels of independently trained SiT diffusion/flow-matching models, the authors find that retraining the same recipe with a different seed moves FID far more than resampling images from one fixed model. Increasing model size or compute does not eliminate the relative noise floor, and lucky seeds can look like substantial compute savings. The paper's practical recommendation is to report training-seed error bars and treat gaps below the measured seed floor as inconclusive.

## Model definition

### Inputs
The studied models are class-conditional ImageNet 256x256 SiT generative models. Inputs include class labels, sampling noise, training seed choices, data ordering, initialization, and per-step Gaussian noise from the flow-matching objective.

### Outputs
The models output generated images. The evaluation outputs FID panels over training seeds and sampling seeds, variance estimates, coefficient-of-variation measurements, guided FID results, seed rankings, and compute-equivalent lucky/unlucky seed comparisons.

### Training objective (loss)
The evaluated SiT models use a flow-matching training objective with per-step Gaussian noise. The paper does not introduce a new generative-model objective; it uses the stochasticity of this existing objective as one of the measured variance sources.

### Architecture / parameterization
The paper studies SiT models at several scales, including SiT-S, SiT-B, SiT-L, and SiT-XL, trained on class-conditional ImageNet 256x256. It also introduces GS-FID, a golden-section search procedure that tunes classifier-free guidance per training/sampling seed cell for evaluation.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Image-generation papers often report a single FID number from one trained model and one or a few sampling seeds. The paper asks whether those numbers are reproducible enough to support small leaderboard claims.

### 2. What is the method?
The authors train many nominally identical SiT models under different training seeds, then sample each trained model under multiple generation seeds. This produces an N-by-K panel that separates training-seed variance from sampling-seed variance. They also isolate sources of training randomness and test whether guidance, compute, model size, or learning-rate transfer tighten the floor.

### 3. What is the method motivation?
Sampling-seed error bars on a fixed model only measure the small lottery. The larger lottery may be which model training run you happened to draw. If papers do not sample that axis, they can mistake seed luck for method improvement.

### 4. What data does it use?
The main experiments use class-conditional ImageNet 256x256 with SiT networks. The paper evaluates several hundred trained networks across scales and training budgets, with 20-25 training seeds and 10 sampling seeds in the central panels.

### 5. How is it evaluated?
The paper computes Inception FID over generated samples and decomposes variation into within-model sampling variance and between-model training variance. It also reports coefficient of variation, seed-ranking stability, guided FID through per-cell classifier-free-guidance tuning, and convergence gaps between lucky and unlucky seeds.

### 6. What are the main results?
On a converged SiT-B/2 panel, between-training-seed spread is about 3.2x the within-model sampling-seed spread. The between-seed coefficient of variation is around 1.3 percent in the central setup, while the broader scale/compute sweep keeps the floor in roughly a 1-2 percent band. Per-cell guidance tuning reduces the relative spread from about 1.26 percent to 0.67 percent but reshuffles seed rankings. Lucky training seeds can reach the same FID with up to 2x less compute than unlucky seeds.

### 7. What is actually novel?
The novelty is measuring the hidden training-seed axis directly for modern diffusion/flow-matching image generation and translating that into an evaluation protocol. The paper is not just another "FID has flaws" critique; it quantifies how much one trained model hides.

### 8. What are the strengths?
The two-axis panel is the right object. The variance decomposition is concrete, the guidance analysis blocks a common objection, and the compute-equivalent lucky-seed analysis makes the problem intuitive for paper review. The recommendations are also practical: report multiple training seeds, report a noise floor, and treat sub-floor gaps as inconclusive.

### 9. What are the weaknesses, limitations, or red flags?
The scope is intentionally narrow: SiT, flow matching, class-conditional ImageNet 256x256, and Inception FID. The 1-2 percent floor should not be treated as universal for text-to-image, video generation, latent diffusion, other metrics, or frontier-scale models. Running the recommended multi-seed protocol is also expensive.

### 10. What challenges or open problems remain?
The main open challenge is predicting seed-noise floors cheaply enough that every paper does not need many full retrains. It is also unclear how the same analysis changes under text-to-image prompts, video generation, human-preference metrics, DINO-style metrics, or RL/post-training pipelines.

### 11. What future work naturally follows?
Repeat the two-axis panel for text-to-image and video models, compare FID with newer feature metrics under the same training seeds, build cheaper proxy estimators for training-run variance, and require leaderboard claims to disclose whether the reported gap clears the method's measured noise floor.

### 12. Why does this matter for cabbageland?
Cabbageland reads many generative-model papers where the claimed gain is a small metric movement. This paper gives a concrete skepticism rule: if the method did not sample training seeds, the claimed improvement may be seed luck wearing a lab coat.

### 13. What ideas are steal-worthy?
Treat evaluation metrics as random variables over all relevant axes, not just output sampling. Report the axis that changes the conclusion. When an evaluation protocol has a known floor, mark smaller gains as inconclusive rather than pretending the leaderboard resolved them.

### 14. Final decision
Keep as a useful evaluation reference. It will save future-us from over-reading tiny FID deltas, especially in image/video generation papers with single-seed hero numbers.
