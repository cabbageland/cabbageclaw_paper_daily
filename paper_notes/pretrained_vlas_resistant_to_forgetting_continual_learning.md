# Pretrained Vision-Language-Action Models are Surprisingly Resistant to Forgetting in Continual Learning

## Basic info

* Title: Pretrained Vision-Language-Action Models are Surprisingly Resistant to Forgetting in Continual Learning
* Authors: Not fully captured from the inspected arXiv HTML excerpt; author list should be verified from the PDF / abstract page before formal citation export.
* Year: 2026
* Venue / source: ICML 2026 / arXiv
* Link: https://arxiv.org/abs/2603.03818
* Date surfaced: 2026-03-28
* Why selected in one sentence: It usefully raises the baseline bar by showing that large pretrained VLAs with simple replay already resist forgetting much better than the old small-policy story suggests.

## Quick verdict

**Useful**

This is a baseline-sharpening paper more than an architectural one, but that still matters. If its empirical story holds, then future continual-learning and memory papers for VLAs should stop pretending that catastrophic forgetting under small from-scratch policies is the relevant default. The paper is strongest as a corrective to evaluation culture, not as a deep mechanistic theory of continual learning.

## One-paragraph overview

The paper studies continual learning for robotic policies in the regime that now matters more: large pretrained VLAs rather than small behavior-cloning models trained from scratch. The central claim is that pretrained VLAs are much more resistant to catastrophic forgetting than the older literature would lead you to expect, especially when paired with simple experience replay. Across LIBERO task suites, the authors report that replay buffers far smaller than those usually needed for small policies can already preserve prior skills fairly well, and sometimes even produce positive backward transfer. The practical message is that pretraining changes the continual-learning landscape enough that weak baselines are no longer acceptable.

## Model definition

### Inputs
Task-conditioned robotic policy inputs include image observations, language instructions, and typically proprioceptive state / action history, depending on the underlying VLA backbone.

### Outputs
The VLA predicts robot action chunks or low-level actions for manipulation tasks.

### Training objective (loss)
From the inspected text, the continual-learning setup is based primarily on **behavior cloning loss** under sequential task training, optionally combined with **experience replay** using stored samples from previous tasks. The exact per-backbone action parameterization is not fully specified in the accessible excerpt.

### Architecture / parameterization
This is mainly an empirical study over existing VLA architectures rather than a new architecture. The inspected text explicitly discusses pretrained **Pi0** and **GR00T N1.5** as the main VLA backbones, compared against smaller non-pretrained policies such as BC-Transformer and related baselines.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Continual learning in robotic policies usually suffers from catastrophic forgetting, but most evidence comes from smaller models. The paper asks whether large pretrained VLAs behave the same way.

### 2. What is the method?
- Evaluate pretrained VLAs under sequential task learning on LIBERO suites.
- Compare simple experience replay, naive sequential finetuning, and EWC-style baselines.
- Compare against smaller non-pretrained behavior-cloning policies.
- Vary replay buffer size and pretraining level to see what actually drives forgetting resistance.

### 3. What is the method motivation?
Large pretrained models may reuse broad representations instead of overwriting them aggressively, so their continual-learning behavior may differ qualitatively from older small-policy regimes.

### 4. What data does it use?
LIBERO benchmark suites, using filtered task datasets referenced in the paper.

### 5. How is it evaluated?
Primarily by average task success rate and negative backward transfer across sequential continual-learning settings, with comparisons across architectures, replay buffer sizes, and initialization/pretraining conditions.

### 6. What are the main results?
From the inspected text, pretrained VLAs with experience replay achieve near-zero or even positive backward transfer in several settings, and they require far less replay data than non-pretrained small policies to maintain previous-task competence. I did not inspect the full appendix, so treat this as the paper’s reported empirical direction rather than a fully audited scoreboard.

### 7. What is actually novel?
The paper’s novelty is mostly empirical and conceptual: it argues that **pretraining fundamentally changes continual-learning dynamics** for VLAs, which means old baseline intuitions are misleading.

### 8. What are the strengths?
- Useful correction to stale assumptions in the literature.
- Compares multiple pretrained VLAs rather than a single cherry-picked model.
- Shows strong low-replay behavior, which is practically important.
- Separates the role of pretraining from architecture more carefully than many benchmark papers.

### 9. What are the weaknesses, limitations, or red flags?
- It is still mostly benchmark evidence, not a satisfying mechanism-level explanation.
- LIBERO is useful but not the whole continual-learning world.
- Replay still matters, so this is not “forgetting is solved.”
- The paper may invite overgeneralization from simulated manipulation benchmarks to messier real-robot regimes.

### 10. What challenges or open problems remain?
Understanding why pretrained VLAs retain knowledge, testing under harder embodiment shifts, moving beyond replay-heavy settings, and separating within-task memory from cross-task continual adaptation.

### 11. What future work naturally follows?
- Study internal representation retention directly.
- Test stronger real-world continual adaptation regimes.
- Benchmark memory-heavy VLAs against these stronger replay baselines.
- Ask which forms of pretraining matter most for retention.

### 12. Why does this matter for cabbageland?
Because it changes the baseline assumptions for any future work on VLA memory or continual learning. If simple replay on pretrained models is already strong, new methods need to beat that honestly.

### 13. What ideas are steal-worthy?
- Treat pretraining level as a first-class continual-learning variable.
- Use low-replay baselines before inventing complicated memory machinery.
- Distinguish apparent performance loss from true representational forgetting.

### 14. Final decision
**Preserve as a baseline-setting note.** Not because the mechanism is beautiful, but because it changes what future papers should be allowed to claim.
