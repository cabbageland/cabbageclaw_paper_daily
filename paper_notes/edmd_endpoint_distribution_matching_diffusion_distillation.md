# eDMD: Endpoint Distribution Matching for Few-Step Diffusion Distillation

## Basic info

* Title: eDMD: Endpoint Distribution Matching for Few-Step Diffusion Distillation
* Authors: Tong Zhao, Xianfang Zeng, Yucheng Han, Ruoyu Wang, Mingkun Lei, Gang Yu, Chi Zhang
* Year: 2026
* Venue / source: arXiv preprint, 2611.17194v1, November 12, 2026
* Link: https://arxiv.org/abs/2611.17194
* Date surfaced: 2026-11-13
* Why selected in one sentence: It isolates how an auxiliary model fitted to intermediate rather than delivered samples can distort few-step distillation, then tests a small endpoint-reference correction across four image backbones.

## Quick verdict

* Highly relevant

Preserve the objective diagnosis and the reference-switch controls. The central idea is not another sampler: the fake denoiser should represent the distribution the system actually delivers, while intermediate predictions remain free to serve that outcome. The exact-denoiser analysis is sharper than a convergence claim for the implemented detached updates, and the full recipe adds training cost and teacher/query choices that must be separated from the endpoint intervention.

Read basis: full-text HTML and PDF main paper, plus selected appendix material on theoretical scope, TDM's practical weighting, teacher integration, implementation, compute, calibration, baseline adaptations, reruns, held-out selection, and reference switching. No exhaustive proof verification, code execution, or reproduction. The manuscript links [an implementation](https://github.com/Westlake-AGI-Lab/eDMD).

## One-paragraph overview

Distribution matching distillation trains a fast image generator using the difference between a pretrained teacher's denoiser and a fake denoiser learned from the student's own samples. For a multistep student, “the student's samples” is ambiguous: final images, intermediate clean predictions, and noisy landing states have different distributions. eDMD shows that fitting the fake to intermediate mixtures or stage references can alter the correction even when final images already have the desired distribution. It instead trains one shared fake only on completed student outputs, yet still directly updates predictions at every selected denoising step. A short integrated teacher improves final low-noise targets, and a precomputed teacher-consistency score biases intermediate query levels. Four-step image experiments support the endpoint change through ablations, transplantation into TDM, and switches away from the endpoint reference after training.

## Model definition

### Inputs

The student takes a text-conditioned latent state z_k at its scheduled noise level sigma_k. A four-step deterministic Euler rollout starts from Gaussian latent noise; sigma decreases from 1 to 0. Text conditioning and the image VAE come from the pretrained teacher family. Teacher/fake queries are formed by adding fresh Gaussian noise to the selected step's clean prediction at query level tau. The fake's *training* input instead comes from noising the final completed sample. These two uses of the fake must not be conflated.

### Outputs

The student predicts a velocity, yielding a clean estimate x_hat_k = z_k - sigma_k G_theta(z_k, sigma_k) and the next Euler state. Only the last clean estimate is the delivered latent image. The teacher and fake provide clean denoising predictions at a query state; their difference supplies a local student correction. The teacher's existing VAE decodes the final latent into an image. This is not a pixel-space generator, reward model, action policy, or physical-state predictor.

### Training objective (loss)

The ordinary single-step DMD motivation is reverse KL between noised student and teacher distributions. Its score gradient can be expressed using the teacher-versus-student denoiser difference. eDMD implements two alternating objectives:

- **Fake:** weighted denoising regression on completed student samples x: E[lambda(tau) ||F((1-tau)x + tau epsilon, tau) - x||^2]. Practical levels lie in [0.02, 0.99), with SNR weight clipped into [1, 10]. Student samples are detached.
- **Student:** let A be the enhanced teacher target, C = A - F, and omega = mean absolute difference between the selected clean estimate and A. Regress x_hat_k toward stop_gradient[x_hat_k + C/omega] with an L2 surrogate. The teacher target, fake correction, and target branch are detached; gradients flow through the selected student's prediction, not the preceding rollout.

Five fake updates with fresh prompts/rollouts precede one student update, which reuses the last rollout. One student step is sampled uniformly per example. Intermediate tau is drawn only above that step's landing level; the final step uses its own full query range. This local surrogate is not demonstrated to be the exact gradient of the final multistep generator's KL.

### Architecture / parameterization

Student and fake inherit teacher diffusion/flow transformer families: SD3-Medium, FLUX.2-klein-4B/9B, or Qwen-Image-2.1. Students use rank-32 LoRA, alpha 64. Fakes use the analogous adaptation except the main FLUX-9B fake is fully trainable; a LoRA-fake control is also reported. Teacher weights remain fixed. The precise-teacher branch uses four Euler nodes for selected low-noise final-step queries. There is no extra student inference network or step introduced by that teacher branch.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

An auxiliary score estimator may accurately model the wrong student distribution. Multistep DMD methods that pool intermediate predictions or constrain stage marginals can penalize internal distributions that need not match the teacher for final generation to work. The question is which reference produces a correction aligned with the final distribution we care about.

### 2. What is the method?

Write p for the teacher's clean distribution, q for the student's final distribution, nu for the fake's reference, and D_r for the exact denoiser of distribution r. With an exact fake, decompose the correction:

`A - D_nu = (A - D_p) + (D_p - D_q) + (D_q - D_nu)`.

The three terms are teacher enhancement, endpoint matching, and reference residual. Under the shared Gaussian noising process, the residual is proportional to the gradient of log(q_tau / nu_tau), and vanishes identically exactly when nu=q. eDMD therefore fits the fake only to final outputs. This removes that *reference* residual at the ideal fake optimum; it does not remove fake approximation error.

It also improves targets with guided teacher integration for final-step queries below the final interval's starting noise level. Intermediate query density is proportional to exp(-estimated cross-level drift), estimated once from teacher-generated samples. Calibration tries to distinguish inconsistent predictions from the expected averaging caused by additional noise. It is a finite-feature proxy, not a guarantee that selected targets are correct.

### 3. What is the method motivation?

A fast student's internal trajectory need not reproduce a slow teacher's trajectory. Requiring intermediate predictions to resemble completed images can waste representational freedom or move an already correct output distribution. But endpoint-only *fake fitting* does not mean endpoint-only *student updates*: the paper finds that intermediate local student corrections still matter.

### 4. What data does it use?

SD3/FLUX runs use 191,500 CDM text prompts, 2,000 student updates, global batch 16, and 1024-square generation. Qwen-Image uses prompt-enhanced rewrites, a 600-update budget, and its 1K resolution tier. Student samples train the fake; teacher samples support query calibration. No real images are newly consumed during distillation, but pretrained teachers and VAEs already contain substantial image-data priors. “Data-free distillation” must not be read as image knowledge learned without data.

### 5. How is it evaluated?

Distill all four backbones to four steps. DrawBench-1000 contains 200 prompts with five generation seeds each; report learned preference/aesthetic/alignment scores, plus DPG-Bench for the SD3/FLUX main table. Peak checkpoints maximize HPSv3++ over raw and EMA weights, evaluated every 100 updates; fixed 1K/2K results accompany SD3/FLUX comparisons. Baselines include DMD2, D-DMD, TDM, and CDM, with a mixture of official checkpoints and local adaptations.

Mechanism controls include endpoint/precise-teacher/query-density removals, an endpoint fake added to otherwise retained TDM training, changing a trained student's fake reference, pre-fitting the replacement fake, final-step-only local updates, and backpropagated endpoint updates. There are also wall-clock curves, 1,000 random held-out prompt-selection splits, selected reruns, and qualitative paired examples. Generation seeds are not independent model-training seeds, and the split check reuses one 200-prompt pool rather than adding a new external benchmark.

### 6. What are the main results?

- **Main learned preference score:** peak HPSv3++ is 11.171 on SD3, 12.699 on FLUX-4B, 12.431 on FLUX-9B, and 14.691 on Qwen-Image. The strongest tabulated trained-baseline peaks are 10.841, 11.337, 11.325, and 14.212, respectively. These are proxy scores, not human win rates.
- **Endpoint ablation:** removing the endpoint component lowers SD3 from 11.171 to 10.122 and FLUX-4B from 12.699 to 11.095. Adding an endpoint fake to the local TDM implementation improves peak scores by 0.61, 1.45, and 0.53 on SD3/FLUX-4B/FLUX-9B. Those comparisons use local TDM, not the stronger official SD3 checkpoint.
- **Destructive switch:** replacing the fake reference with an intermediate mixture after FLUX-4B training loses 1.71 points in 100 updates. Even pre-fitting that fake with a frozen student yields a 2.07-point drop after updates resume, weakening the simple “new fake was untrained” explanation.
- **Update distinction:** updating only the final student step plateaus at 7.5–8.4 on FLUX-4B, well below the full method. Backpropagating endpoint supervision is not automatically better and can worsen results.
- **Robustness/cost:** three SD3 training seeds yield peak 11.05 +/- 0.10; this is not full multiseed coverage for every backbone/baseline. FLUX-4B eDMD takes 17.6 seconds per update versus DMD2's 11.8 and D-DMD's 7.1 on 16 Ascend NPUs. Its 2,000 updates take about 9.8 hours excluding evaluation, plus 15.8 minutes of query calibration. Reported matched-time curves still favor it, but four inference steps are not four cheap training calls.

### 7. What is actually novel?

The explicit reference-residual diagnosis, characterization of zero-correction sets, and use of a final-output fake to supervise every local student step form the important contribution. Final-output fake fitting has precedents, acknowledged in ADM, and final-output supervision appears elsewhere; neither is invented here. The precise teacher and query-density calibration are complementary engineering changes, not necessary ingredients of the residual identity.

### 8. What are the strengths?

The modularity does real work: the distribution represented by the fake is specified separately from the states at which it is queried. Transplantation into TDM and destructive switching make the argument more persuasive than a full-recipe leaderboard alone. Four backbones, fixed-budget scores, seed checks, held-out checkpoint selection, compute measurements, and failed interventions expose meaningful conditions of success. Intermediate trajectories are treated as implementation freedom rather than decorative physical processes.

### 9. What are the weaknesses, limitations, or red flags?

**Theory boundary:** equality of ideal denoisers across query space is not convergence of the parameterized student. The correction can be nonzero while expected parameter gradients cancel or cannot represent a useful change. A guided prediction or probability-flow integration is generally not the exact conditional-mean denoiser of one stated target distribution; the paper's corollary is conditional on that property. With a learned fake, removing the reference residual does not remove estimation lag, capacity limits, or optimization error.

**Evaluation boundary:** main selection and reporting use HPSv3++; learned evaluators can reward changes other than distributional fidelity or diversity. Held-out prompt splits mitigate checkpoint-selection bias but do not make the proxy a human judgment. Baseline adaptations differ, DMD2 omits GAN loss, and some official models have different training histories. Main backbone-wide claims are not all backed by multiseed baseline reruns. On SD3, the full method's late score drops near the best baseline peak.

**Recipe boundary:** guidance, rollout type, fake training, teacher integration, and query sampling all matter. PT also changes the normalizer, although additional controls support target integration as the main source of its benefit. PT applied to all queries collapses FLUX-4B. Query calibration has little effect when its density is nearly uniform, notably FLUX. Teacher/fake work, LoRA restrictions, and calibration add cost. There is no demonstrated transfer to video, 3D, action generation, distribution shift, or long-horizon control.

### 10. What challenges or open problems remain?

Quantify finite-fake error and lag; relate local detached updates to an explicit final-distribution objective; characterize guided/integrated targets; measure diversity and failure tails independently of the preference metric; and determine whether endpoint-only fakes stay accurate for longer or heterogeneous rollouts. Intermediate query states can differ from the fake's training-query marginal, so out-of-distribution score accuracy remains an empirical concern even when the reference is conceptually right.

### 11. What future work naturally follows?

Run a matched-total-compute factorial study of reference, teacher target, guidance, and query law, including calibration/evaluation cost and baseline tuning. Add independent human comparisons and diversity/recall checks. Test fake capacity and update ratio before attributing failures to the reference alone. Extend the reference intervention to video or action diffusion only with temporal consistency and downstream-control measurements, rather than assuming an image-score gain transfers.

### 12. Why does this matter for cabbageland?

This is a precise example of objective-interface design: the auxiliary model's statistical target should match the artifact that matters, while internal representation remains free unless a downstream use requires constraints. It is directly useful for diffusion/flow distillation baselines and adjacent inspiration for multistage generators and learned evaluators. It does not introduce causal state, interpretable world dynamics, compositional reasoning, or a physically meaningful denoising trajectory; those labels are not earned by the multistep formulation.

### 13. What ideas are steal-worthy?

- Name the exact distribution every critic, scorer, or denoiser is trained to represent.
- Separate auxiliary-model fitting data from the states where its predictions are queried.
- Check whether a supposedly correct delivered distribution is still pushed by intermediate-reference residuals.
- Transplant a proposed interface change into another objective before crediting the entire new recipe.
- Switch references after convergence, pre-fit the replacement, and inspect both final quality and intermediate changes.
- Preserve local intermediate supervision without requiring intermediate samples to look like final outputs.
- Report inference steps, fake updates, teacher calls, calibration, and total training time separately.

### 14. Final decision

Preserve as a diffusion-distillation design and ablation reference. The endpoint-only fake is the component to steal first, with its exact-denoiser assumptions and learned-fake limits attached. Do not turn the paper into a theorem of practical convergence, a claim that all trajectory constraints are harmful, or proof that four-step image gains imply better physical world models.
