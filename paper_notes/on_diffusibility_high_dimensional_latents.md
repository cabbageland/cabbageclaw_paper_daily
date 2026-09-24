# On the Diffusibility of High-Dimensional Latents

## Basic info

* Title: On the Diffusibility of High-Dimensional Latents
* Authors: Chao Feng, Zhiyang Xu, Bowei Chen, Yuanjun Xiong, Xiyao Wang, Jui-Hsien Wang, Richard Zhang, Zhe Lin, Andrew Owens, Yijun Li
* Year: 2026
* Venue / source: arXiv:2609.28473; accepted to ECCV 2026
* Link: https://arxiv.org/abs/2609.28473
* Date surfaced: 2026-09-24
* Why selected in one sentence: It gives a mechanism-level explanation for why reconstruction-tuned high-dimensional representation latents can become hard for ordinary flow matching, then fixes the target parameterization.

## Quick verdict

* Must read

This is a strong paper because the failure mode is specific: reconstruction tuning can collapse effective dimensionality inside a nominally high-dimensional latent, and velocity prediction then wastes training on orthogonal noise rather than signal. The proposed fix, clean-latent or `x0` prediction, is small but well motivated and backed by clear ablations. The remaining caveat is that the strongest scaling result uses an internal 90M dataset, but the core diagnostic and target swap are still useful.

## One-paragraph overview

Representation autoencoders let diffusion models generate in the feature spaces of pretrained visual encoders such as DINOv2 or MAE. Those features are semantically useful, but frozen semantic encoders often reconstruct poorly, so reconstruction tuning looks attractive. This paper shows the catch: reconstruction tuning makes the feature spectrum concentrate into a much lower effective dimension. In that geometry, the standard flow-matching velocity target contains large orthogonal noise components that do not help recover the clean latent. Predicting the clean latent `x0` directly focuses the loss on the signal manifold and improves text-to-image generation across finetuned DINOv2-L and MAE-RAE latents.

## Model definition

### Inputs

The generative model receives noisy latent tokens from a representation autoencoder, diffusion or flow time, and text conditioning for text-to-image generation. The representation latents come from visual encoders such as DINOv2-L or MAE-RAE, with decoders trained for image reconstruction; the key experiments compare frozen semantic latents, reconstruction-finetuned high-dimensional latents, and a low-dimensional projected variant.

### Outputs

The diffusion transformer predicts either the standard flow-matching velocity target or the clean latent representation `x0`. Decoding the predicted latent trajectory through the RAE decoder yields images.

### Training objective (loss)

The baseline uses mean squared error on the flow-matching velocity target. The proposed method uses mean squared error to predict the clean representation `x0` from the noised latent. The paper argues that this avoids explicit regression of orthogonal noise directions induced by high-dimensional velocity prediction.

### Architecture / parameterization

The generative model is a diffusion transformer trained in RAE latent space. The representation side uses pretrained visual encoders, reconstruction-trained decoders, and in one ablation an MLP down-projection from 1024-dimensional DINOv2-L features to a 32-dimensional latent.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It tries to make high-dimensional, reconstruction-rich representation latents usable for text-to-image diffusion. Frozen semantic latents can omit fine visual detail; reconstruction tuning recovers detail but makes standard velocity-prediction flow matching hard to optimize.

### 2. What is the method?

The paper first diagnoses latent geometry using singular-value spectra and effective dimensionality. It then replaces velocity prediction with clean-latent `x0` prediction for diffusion/flow matching in high-dimensional representation spaces.

### 3. What is the method motivation?

If reconstruction-tuned latents lie near a low-dimensional signal manifold inside a high-dimensional ambient feature space, the velocity target includes a large orthogonal noise component. Fitting that component is inefficient because it is mostly unrelated to the clean latent. `x0` prediction asks the model to recover the signal directly.

### 4. What data does it use?

The effective-dimensionality analysis samples patch features from ImageNet. Core text-to-image experiments use ImageNet-trained tokenizers/decoders and COCO-30k, GenEval, and DPG-Bench evaluations. A larger-scale experiment trains on an internal 90M dataset and applies BLIP3o-60k supervised finetuning.

### 5. How is it evaluated?

The paper evaluates reconstruction PSNR, effective dimensionality (`R90`, `R95`, `R99`), single-image overfitting behavior, text-to-image alignment with GenEval and DPG-Bench, and image quality with COCO-30k FID. It compares frozen DINOv2-L, finetuned DINOv2-L with velocity prediction, finetuned DINOv2-L with `x0` prediction, low-dimensional projection, and MAE-RAE variants.

### 6. What are the main results?

Finetuned DINOv2-L has better reconstruction than frozen DINOv2-L but much lower effective dimensionality: `R90` drops from 672 to 129 while PSNR rises from 17.34 to 29.12. With velocity prediction, finetuned DINOv2-L performs badly: GenEval 30.96, DPG-Bench 67.47, FID 29.97. Switching to `x0` prediction recovers GenEval 39.48, DPG-Bench 71.83, and FID 16.80. For MAE-RAE, `x0` prediction improves GenEval from 36.17 to 40.89, DPG-Bench from 67.54 to 73.90, and FID from 22.20 to 17.24.

### 7. What is actually novel?

The novelty is the link between reconstruction-induced effective-dimensionality collapse and the failure of velocity prediction in high-dimensional latent diffusion. The `x0` target itself is not conceptually exotic, but the paper gives a useful condition for when it is the right target.

### 8. What are the strengths?

The diagnosis is crisp, the ablations separate reconstruction, dimension, and target parameterization, and the numerical pattern is easy to remember. The paper also resists the lazy conclusion that high-dimensional latents are always bad; it says the problem is the mismatch between latent geometry and training target.

### 9. What are the weaknesses, limitations, or red flags?

The biggest caveat is that the most competitive scaling comparison uses an internal 90M dataset, which limits external reproducibility. The analysis is strong for the tested RAE families but not a universal theorem for every high-dimensional latent model. The paper also does not fully explore whether other target parameterizations or noise schedules could match `x0` prediction.

### 10. What challenges or open problems remain?

The next problem is designing representation encoders whose geometry is naturally generative, not merely patch-reconstructive. Another open question is how to choose target parameterization adaptively from latent spectra, instead of hard-coding `x0` prediction.

### 11. What future work naturally follows?

Useful follow-ups include measuring effective dimensionality during tokenizer training, designing regularizers that preserve diffusibility, testing video and 3D RAE latents, and building target-selection diagnostics for flow models.

### 12. Why does this matter for cabbageland?

Cabbageland cares about explicit state that actually supports generation and reasoning. This paper says a latent can contain useful detail and still be badly shaped for the downstream learner. That is exactly the kind of state/consumer mismatch worth remembering.

### 13. What ideas are steal-worthy?

Measure latent effective dimensionality before blaming model scale. Treat prediction target as part of representation design. If a representation lives on a low-dimensional manifold inside a high-dimensional space, prefer losses that point toward the clean signal rather than losses that force the model to chase ambient noise.

### 14. Final decision

Preserve. This is the most relevant paper of the day.
