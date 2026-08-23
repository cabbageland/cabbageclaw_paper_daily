# Forgetting, plasticity, and co-observation: a third facet of continual learning

## Basic info

* Title: Forgetting, plasticity, and co-observation: a third facet of continual learning
* Authors: Timm Hess, Abhishek Jha, Gido M. van de Ven, Tinne Tuytelaars
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.18803
* Date surfaced: 2026-08-23
* Why selected in one sentence: It is the cleanest paper in the batch on showing that continual-learning gaps to joint training are not explained by forgetting and plasticity alone.

## Quick verdict

* Highly relevant

I inspected the arXiv HTML full text, especially the co-observation framing, the ensemble-plus-linear-probing diagnostic, and the replay-versus-distillation comparison. This paper earns a preserved note because it names a third failure mode that is both conceptually sharp and practically useful: even if you retain everything and stay plastic, separate training can still miss structure that only appears when related data is seen together. The paper is strongest when it stops arguing in abstractions and uses the ensemble baseline to make forgetting a controlled variable rather than the default excuse.

## One-paragraph overview

The paper argues that continual learning has overcommitted to the stability-plasticity story. Forgetting and plasticity matter, but they do not fully explain why sequential training underperforms joint training. The missing piece, according to the authors, is co-observation: the representational benefit of seeing related samples together during optimization. To isolate that factor, they construct a diagnostic setup based on continual pre-training, linear probing, and a full-retention ensemble baseline that preserves earlier representational states by design. Because the ensemble controls forgetting, any remaining gap to joint training is interpreted as a loss of co-observation. The paper then reinterprets replay and distillation through that lens.

## Model definition

### Inputs
Sequential chunks of image data, supervised or self-supervised training objectives, replay buffers or distillation targets, and linear-probe evaluation data.

### Outputs
Learned visual representations whose quality is measured by downstream linear-probe performance after sequential versus joint or replay-based training.

### Training objective (loss)
There is no single new model or loss. The paper studies supervised and self-supervised continual pre-training setups, including Barlow Twins and I-JEPA style representation learning, and analyzes how different continual-learning mechanisms affect the resulting representation quality.

### Architecture / parameterization
Diagnostic continual-learning framework. The key pieces are naive sequential training, joint training, a full-retention ensemble baseline, replay baselines, and distillation baselines, all compared via linear probing.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to explain why continual learning still underperforms joint training even after one controls for catastrophic forgetting and, conceptually, loss of plasticity.

### 2. What is the method?
The method is a diagnostic decomposition. The paper separates forgetting from co-observation by using a full-retention ensemble baseline, evaluates representation quality through linear probing, and then measures how replay and distillation behave relative to that forgetting-controlled baseline.

### 3. What is the method motivation?
If the field keeps assuming that fixing forgetting and preserving plasticity would automatically recover joint-training quality, it will keep misdiagnosing what replay, distillation, and other continual-learning methods are actually doing.

### 4. What data does it use?
The paper studies generic data-incremental "chunking" scenarios in the vision domain, including supervised and self-supervised continual pre-training settings. It specifically discusses IN-100 replay experiments and self-supervised settings using Barlow Twins and I-JEPA.

### 5. How is it evaluated?
Evaluation is done at representation level via linear probing rather than only end-to-end task accuracy. The paper compares naive sequential training, joint training, a full-retention ensemble, replay with different buffer sizes, and distillation-based continual-learning methods.

### 6. What are the main results?
The main result is qualitative but strong: joint training consistently beats separate training even when forgetting is controlled. On IN-100 replay experiments, about 15% replay storage is enough to match the full-retention ensemble, while 30% replay storage pushes beyond the ensemble and closes about half the remaining gap to incremental joint training. Distillation closely mirrors the ensemble and the 15% replay regime, which suggests it preserves earlier features but does not recreate the stronger co-observation benefits that larger replay buffers can approximate.

### 7. What is actually novel?
The novelty is the explicit identification of co-observation as a third factor in continual learning, plus a diagnostic methodology that makes that claim testable rather than merely rhetorical.

### 8. What are the strengths?
The paper isolates the phenomenon better than most conceptual CL papers do. The ensemble baseline is a smart move. The replay-versus-distillation comparison is particularly useful because it turns an abstract claim into a mechanism-level interpretation.

### 9. What are the weaknesses, limitations, or red flags?
The work is mostly in vision continual-learning settings, so transfer to language or agent systems is still an inference. It is more diagnostic than prescriptive. And while the replay findings are suggestive, the exact replay percentages should not be treated as portable constants.

### 10. What challenges or open problems remain?
A major open problem is how to recover co-observation benefits when full replay is impossible because of privacy, storage, or cost constraints. Another is whether the same phenomenon governs long-lived agent memory and world-model updating.

### 11. What future work naturally follows?
Test analogous co-observation diagnostics in language-model continual pre-training, memory-augmented agents, and tool-using systems. Study whether structured replay, synthetic rehearsal, or state abstractions can approximate co-observation without storing large raw buffers.

### 12. Why does this matter for cabbageland?
Because cabbageland cares about long-lived systems that update over time. This paper gives a useful warning: even perfect retention may not recover the structure you lost by never letting the right pieces interact during learning.

### 13. What ideas are steal-worthy?
Use a full-retention ensemble baseline to separate forgetting from other causes of degradation. Evaluate representation quality with linear probing when end-to-end metrics would confound it. Interpret replay as restoring co-observation, not only as preserving memory.

### 14. Final decision
Keep as a preserved note. The paper adds a real conceptual tool rather than just another continual-learning curve.

## 6. Mandatory critical angles

The paper is strongest on representation, evaluation fairness, and mechanism-level reinterpretation of replay and distillation. It earns the "third factor" claim because it actually controls forgetting rather than merely asserting that something else must be happening. The main caution is domain scope: most evidence comes from vision and continual pre-training rather than agentic systems directly.

## 7. Writing style

The right tone is approving and exact. The useful move here is not hype about a new term, but the clean diagnostic separation the paper builds around it.

## 8. Repository output format

Saved as a preserved paper note because the co-observation lens is likely to be useful well beyond this one batch.
