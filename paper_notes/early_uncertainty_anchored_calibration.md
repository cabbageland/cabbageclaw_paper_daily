# Do Not Train Away Uncertainty: Early Uncertainty Anchored Calibration

## Basic info

* Title: Do Not Train Away Uncertainty: Early Uncertainty Anchored Calibration
* Authors: Yutong Xie, Jiawei Tang, Zhenglin Hua, Yuxiang Ma, Si Qin, Yaxin Hou, Hui Liu, Junhui Hou, Yuheng Jia
* Year: 2026
* Venue / source: arXiv preprint
* Link: https://arxiv.org/abs/2610.12048
* Date surfaced: 2026-10-11
* Why selected in one sentence: It treats early-training uncertainty as a useful anchor instead of letting continued optimization erase it.

## Quick verdict

* Highly relevant

This is a useful calibration paper because it identifies a recurring training-time failure mode: accuracy keeps improving slightly while calibration gets worse. EUA-Cal turns the early checkpoint with best validation ECE into a teacher for uncertainty, using both prediction regularization and feature-prototype structure. The limitation is that it depends on selecting and storing an early anchor, so it is more of a disciplined training intervention than a universal post-hoc fix.

## One-paragraph overview

The paper observes that early checkpoints across image classifiers and fine-tuned LLMs can be better calibrated than later checkpoints, even when later models are more accurate. The early model retains low-confidence predictions and boundary features that later training compresses away. EUA-Cal uses that early checkpoint as an uncertainty anchor. Early Prediction Regularization aligns the current model's predictions with early predictive uncertainty, while Prototype Structure Regularization builds class prototypes from early features and keeps current outputs aware of that feature-space uncertainty. Experiments across image classification and multiple-choice question answering show lower ECE/AECE while mostly preserving accuracy.

## Model definition

### Inputs

The method receives the same inputs as the base classifier or fine-tuned LLM: images for classification or text/question inputs for multiple-choice QA. During training it also uses outputs and feature/prototype information from a selected early anchor checkpoint.

### Outputs

The model outputs class probabilities or answer-choice probabilities. EUA-Cal regularizes those outputs so confidence better matches empirical correctness.

### Training objective (loss)

The objective is cross-entropy plus Early Prediction Regularization and Prototype Structure Regularization: `L_EUA-Cal = L_CE + alpha * L_EPR + beta * L_PSR`. EPR uses KL alignment to early predictions; PSR uses KL alignment to prototype-derived distributions based on early feature structure.

### Architecture / parameterization

EUA-Cal is a training regularizer rather than a new backbone. It is applied to ResNet, DenseNet, ViT, Llama3-8B, Llama3.1-8B, and Qwen3-8B-Base settings. The early anchor is selected from validation calibration behavior, such as epoch 60 for CIFAR ResNet-50 settings or the pretrained checkpoint for some LLM fine-tuning.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Training and fine-tuning often create overconfident models. Later checkpoints may gain a little accuracy but lose the uncertainty signal needed for calibrated decisions.

### 2. What is the method?

Stop at an early checkpoint that has strong validation calibration, keep it as an anchor, and continue training the final model with regularizers that preserve the early model's uncertainty in predictions and feature-prototype structure.

### 3. What is the method motivation?

Low-confidence samples near class boundaries are not just errors; they encode epistemic humility. Later training can overcompact feature clusters and wipe out that uncertainty. Preserving it should improve calibration without surrendering all later accuracy gains.

### 4. What data does it use?

Image experiments use CIFAR-10, CIFAR-100, Tiny-ImageNet, CIFAR-10-C, and CIFAR-100-C with multiple backbones. LLM experiments use SciQ, ARC-Challenge, ARC-Easy, and CommonsenseQA with Llama and Qwen models.

### 5. How is it evaluated?

The paper reports accuracy, expected calibration error, adaptive expected calibration error, distribution-shift calibration, OOD detection, and ablations over EPR, PSR, anchor choice, and hyperparameters.

### 6. What are the main results?

For ResNet-50, EUA-Cal obtains the lowest ECE and AECE on CIFAR-10, CIFAR-100, and Tiny-ImageNet while keeping competitive accuracy. For Llama3-8B on ARC-C, ARC-E, and SciQ, it has the best average rank and lowest ECE/AECE on all three datasets; compared with the second-best method on each dataset, it reduces ECE and AECE by 16.24% and 47.92% on average. In shifted LLM evaluation from ARC-E to ARC-C/SciQ/CSQA, it reduces AECE by 30.94% on average against the second-best method. On ViT-B/32, it reduces ECE from 1.92% to 0.48% on CIFAR-10 and from 9.56% to 0.89% on CIFAR-100 versus vanilla.

### 7. What is actually novel?

The novelty is using the early checkpoint itself as a calibration anchor for both predictive distributions and feature-structure uncertainty, rather than only adding entropy penalties or doing post-hoc temperature scaling.

### 8. What are the strengths?

The paper connects a simple empirical phenomenon to a concrete regularizer. It tests both vision and LLM settings, checks distribution shift, and shows that both prediction and prototype regularization contribute.

### 9. What are the weaknesses, limitations, or red flags?

Anchor selection needs validation calibration signals and stores an extra checkpoint. The method assumes the early model's uncertainty is meaningful; if early uncertainty is just undertraining noise, the anchor could preserve the wrong ambiguity. The feature-prototype story is cleaner for classifiers than for more open-ended generative models.

### 10. What challenges or open problems remain?

The main challenge is distinguishing useful uncertainty from ignorance. Another open problem is applying the idea to sequence generation where confidence is spread over many tokens and calibration can be prompt-dependent.

### 11. What future work naturally follows?

Automate anchor selection, extend uncertainty anchors to long-form generation or tool-use decisions, and combine early-anchor regularization with post-hoc calibration under deployment shift.

### 12. Why does this matter for cabbageland?

It is a reminder that optimization can erase exactly the uncertainty signal a decision system needs. Cabbageland cares about models that know when not to overcommit.

### 13. What ideas are steal-worthy?

Keep early checkpoints as behavioral anchors, not just backups. Regularize both probabilities and representation geometry. Treat boundary examples as uncertainty carriers instead of training residue to be crushed.

### 14. Final decision

Preserve. It is not flashy, but the calibration lesson is practical and reusable.
