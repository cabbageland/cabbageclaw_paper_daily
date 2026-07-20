# Understanding Reasoning from Pretraining to Post-Training

## Basic info

* Title: Understanding Reasoning from Pretraining to Post-Training
* Authors: Jingyan Shen, Ang Li, Salman Rahman, Yifan Sun, Micah Goldblum, Matus Telgarsky, Pavel Izmailov
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.16097
* Date surfaced: 2026-07-20
* Why selected in one sentence: It studies reasoning as a full pretraining-to-RL pipeline and shows that pretraining loss is a strong predictor of post-RL returns.

## Quick verdict

**Highly relevant**

The main value here is not that it uses chess. The value is that it gives a controlled way to ask what RL post-training is actually buying and how much pretraining quality still matters afterward. I inspected the arXiv HTML sections covering the chess framework, synthetic reasoning-trace construction, RL setup, scaling analysis, mechanism analysis, and transfer-to-math discussion.

## One-paragraph overview

The paper builds a controlled testbed for studying reasoning across pretraining, supervised fine-tuning, and RL post-training. Models are pretrained on human chess games, fine-tuned on synthetic reasoning traces plus correct continuations, and then optimized with verifiable binary rewards on chess puzzles. Within that setup, the authors show that pretraining loss strongly predicts post-RL pass@1 at fixed RL compute and that the compute-optimal frontier shifts toward a larger RL fraction as total compute grows. The mechanism analysis then complicates the usual story: on easy puzzles RL mostly amplifies moves the SFT policy already liked, while on hard puzzles it can surface previously buried correct moves but also reinforce bad ones.

## Model definition

### Inputs
The model takes serialized chess move sequences during pretraining, puzzle states plus synthetic reasoning traces during supervised fine-tuning, and puzzle states plus sampled trajectories during RL.

### Outputs
It outputs reasoning traces in chess-move-token form and the move sequence for the puzzle solution, one solver move at a time.

### Training objective (loss)
Pretraining uses standard next-token prediction on human game trajectories. Supervised fine-tuning trains on synthetic reasoning traces followed by the target continuation, masking opponent moves from the loss. RL uses `GRPO` with a binary reward of `1` only when the full solver move sequence matches the ground-truth line exactly.

### Architecture / parameterization
The models are dense `Qwen3`-style autoregressive language models ranging from `5M` to `1B` parameters over an `81`-token chess vocabulary, trained in a standard pretrain -> SFT -> RL pipeline.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to explain how pretraining choices shape the gains available from RL post-training, and what RL is actually changing in a reasoning policy.

### 2. What is the method?
The method is a controlled chess testbed with large pretraining sweeps, synthetic reasoning-trace SFT, RL on verifiable puzzles, compute-frontier analysis, and a smaller transfer study on math-domain language modeling.

### 3. What is the method motivation?
The motivation is that normal LLM pipelines are too entangled and expensive to cleanly attribute effects to pretraining versus RL.

### 4. What data does it use?
It uses a `54B`-token pretraining corpus of Lichess games, `156K` quality-filtered Lichess puzzles for post-training, a `1,480`-puzzle benchmark for evaluation, and a transfer study with a `1B` language model pretrained on `10B` to `200B` tokens of math-domain text.

### 5. How is it evaluated?
It is evaluated with scaling sweeps, pass@1 and pass@16 puzzle performance, compute-allocation frontiers, local RL scaling slopes, policy-evolution analysis on easy versus hard puzzles, and a qualitative transfer study in math.

### 6. What are the main results?
Post-RL performance at a fixed RL compute level is well predicted by pretraining loss. Along the pass@1 frontier, the optimal RL fraction grows as total compute increases, while pass@16 remains more sensitive to pretraining scale. Mechanistically, RL mainly amplifies already-correct moves on easy puzzles, but on hard puzzles it both surfaces rare correct moves and reinforces some wrong ones. The same qualitative pretraining-loss pattern appears in the math-domain transfer study.

### 7. What is actually novel?
The novelty is the joint pretraining-RL scaling analysis and the policy-evolution story that separates easy-puzzle amplification from hard-puzzle redistribution.

### 8. What are the strengths?
The paper asks a real science question, keeps the environment controlled, and gives a usable mental model for compute allocation instead of only another benchmark score.

### 9. What are the weaknesses, limitations, or red flags?
Chess is still a narrow domain with a tiny vocabulary and exact rewards, so the transfer to open-ended natural-language reasoning is suggestive rather than settled. The math transfer section is also smaller and more qualitative than the chess core.

### 10. What challenges or open problems remain?
The main challenge is testing whether the same pretraining-loss and RL-slope relationships survive in larger natural-language settings where reward is noisier and solution diversity matters more.

### 11. What future work naturally follows?
Future work should extend the same analysis to language tasks with verifiable rewards, study why pass@1 can improve without pass@k following, and look for RL methods that improve diversity instead of only concentrating mass.

### 12. Why does this matter for cabbageland?
Cabbageland cares about reasoning, world models, and how much post-training can really fix. This paper argues that the pretrained state still governs a lot of the downstream story and gives a cleaner way to think about that interface.

### 13. What ideas are steal-worthy?
Use pretraining loss as a practical predictor of RL returns. Study compute allocation across pretraining and RL on the same frontier instead of optimizing them separately. Generate structured internal reasoning traces from the model's own proposal policy rather than bolting on an external searcher. Separate easy-case amplification from hard-case mode reshaping when diagnosing RL.

### 14. Final decision
**Keep it.** Even if chess is only a proxy, it is a useful proxy here because the paper actually uses the control it buys.
