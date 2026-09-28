# FuseReg: Regularizing Layer Fusion Mitigates the Reconstruction-Generation Gap in Representation Autoencoders

## Basic info

* Title: FuseReg: Regularizing Layer Fusion Mitigates the Reconstruction-Generation Gap in Representation Autoencoders
* Authors: Hongyang Du, Yunfei Xie, Junjie Ye, Jiawei Yang, Xiaoyan Cong, Haodong Zhang, Yongchao Huang, Haiyu Wu, Zongxia Li, Shihang Gui, Dawei Liu, Runhao Li, Jingcheng Ni, Chen Wei, Randall Balestriero, and Yue Wang
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2609.31620
* Date surfaced: 2026-09-28
* Why selected in one sentence: It identifies layer fusion in representation autoencoders as a decoder/generator interface problem and fixes it with mean-preserving random subset training.

## Quick verdict

**Highly relevant**

FuseReg is valuable because it turns a vague tokenizer choice into a measurable robustness problem. It is a practical generative-model paper with a transferable mechanism: train downstream consumers to tolerate the representation hierarchy instead of binding them to one brittle layer mix.

## One-paragraph overview

Representation autoencoders use frozen visual-encoder features as latents for both reconstruction and diffusion. The problem is that shallow layers help pixel reconstruction, deeper layers often help generative modeling, and fixed layer fusion forces the decoder and DiT into one compromise. FuseReg samples normalized random subsets of encoder layers during decoder and generator training. The subset mean preserves the full-layer latent in expectation while exposing downstream models to layer disagreement. In experiments on ImageNet-256 with DINOv3-L, a single decoder works across full, sparse, and single-layer fusions; swapping that decoder into a fixed generator improves gFID; and regularizing both decoder and DiT gives complementary gains.

## Model definition

### Inputs
Inputs are frozen visual encoder layer features from DINOv3-L, sampled nonempty layer masks, class labels for class-conditional DiT training, noise, and diffusion/flow time.

### Outputs
The decoder outputs reconstructed images from fused feature latents. The DiT outputs the full-layer latent target from a noisy subset-fusion input.

### Training objective (loss)
Decoder training uses pixel reconstruction, LPIPS, and adversarial losses on normalized subset fusions. DiT training uses a time-weighted x-prediction loss to regress the full-layer fusion target from a noisy subset fusion. The paper also analyzes the random subset objective as an explicit disagreement penalty under linear squared loss.

### Architecture / parameterization
The setup uses a frozen DINOv3-L encoder with 23 candidate layers, a ViT decoder, and DiT-Base/DiT-XL generators. FuseReg is not a new backbone; it is a layer-subset sampling distribution with separate decoder and DiT drop rates.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Fixed layer fusion in RAEs binds reconstruction and generation to the same encoder-layer mixture even though the two stages prefer different information.

### 2. What is the method?
During training, sample a nonempty Bernoulli subset of encoder layers, average the retained features, and train the decoder and/or DiT on these normalized subset means. At inference, use the full-layer mean by default.

### 3. What is the method motivation?
The subset mean stays aligned with the deployment latent in expectation, while randomizing the layer composition punishes consumers that depend too strongly on one layer shortcut.

### 4. What data does it use?
Experiments use ImageNet-256 with a frozen DINOv3-L encoder.

### 5. How is it evaluated?
The paper evaluates reconstruction with PSNR, SSIM, and rFID over 50k images, and generation with gFID and Inception Score over 50k class-conditional samples using 50 Euler steps. It isolates decoder robustness, decoder swapping with a fixed generator, and joint decoder/generator regularization.

### 6. What are the main results?
A FuseReg decoder reconstructs strongly from k=7, k=23, and single-layer fusion, while fixed RAEv2 decoders collapse off their training fusion. Decoder replacement alone lowers unguided gFID from 3.01 to 2.21 in the native k=23 DiT-XL setting and from 27.73 to 1.92 under a shifted k=7 fusion. Joint regularization reduces DiT-Base unguided gFID from 13.96 to 9.93.

### 7. What is actually novel?
The novelty is treating layer fusion as a training distribution rather than a fixed design choice, with a theoretical account of why normalized random subsets induce cross-layer disagreement regularization.

### 8. What are the strengths?
The method is simple, architecture-light, and separates decoder and generator rates. The decoder-swap experiment is especially clean because it holds generated latents fixed and changes only the readout.

### 9. What are the weaknesses, limitations, or red flags?
The empirical scope is ImageNet-256, DINOv3-L, and matched DiT budgets. The theory uses linear squared-loss consumers, while the actual decoder and guided sampling dynamics are nonlinear. The best rates depend on scale and guidance.

### 10. What challenges or open problems remain?
It remains open whether the same fusion regularization transfers cleanly to video RAEs, 3D latents, larger resolutions, and longer training schedules.

### 11. What future work naturally follows?
Try separate layer-subset schedules for video/image/3D tokenizers, use layer robustness as a tokenizer diagnostic, and combine FuseReg with learned input-dependent routing only after the robust baseline is understood.

### 12. Why does this matter for cabbageland?
It is a good example of preserving useful structure in an interface, not only inside a model. Future world-model stacks will have the same encoder hierarchy/readout problem.

### 13. What ideas are steal-worthy?
Make representation consumers robust to subsets of the upstream hierarchy. Test decoder replacement with fixed generated latents to isolate readout quality. Treat disagreement across representation layers as signal, not nuisance.

### 14. Final decision

**Preserve.** This is a strong practical mechanism paper for generative representation learning.
