# Generalization in LLM Problem Solving: The Case of the Shortest Path

## Basic info

* Title: Generalization in LLM Problem Solving: The Case of the Shortest Path
* Authors: Yao Tong, Jiayuan Ye, Anastasia Borovykh, Reza Shokri
* Year: 2026
* Venue / source: ICLR 2026 / arXiv
* Link: https://arxiv.org/abs/2604.15306
* Date surfaced: 2026-04-17
* Why selected in one sentence: It uses a controlled shortest-path environment to separate local transfer from longer-horizon compositional failure in language models.

## Quick verdict

**Useful**

This is one of the cleaner reasoning-diagnosis papers because it narrows the task enough to make failure modes legible. The core result is not flattering: models can transfer to unseen maps, but they still fail at longer-horizon composition, and neither RL nor inference-time scaling really fixes that. I inspected the abstract and several PDF pages covering the setup, key findings, and early analysis, but I did not read the full appendix or every experiment variant.

## One-paragraph overview

The paper builds a synthetic shortest-path environment as a controlled testbed for systematic generalization in language models. Instead of using messy natural-language benchmarks where data contamination and fuzzy task overlap ruin interpretation, it separates two different claims: spatial transfer to unseen maps and length scaling to longer paths. Small transformer models are pretrained on random walks, then fine-tuned with supervised learning or RL to output shortest paths as sequences of movement tokens. The main finding is that spatial transfer works surprisingly well, but length scaling fails due to recursive instability: even when subproblems are individually solvable, composing them into a longer valid solution becomes unreliable. RL helps training stability somewhat, and inference-time scaling helps performance somewhat, but neither changes the underlying ceiling.

## Model definition

### Inputs
The model takes a prompt specifying the start and end nodes of a shortest-path problem on a grid-like map. The path is represented as a sequence of directional tokens such as north, south, east, and west rather than raw node identifiers.

### Outputs
The model outputs a complete path as a token sequence encoding movements from the start node to the target node.

### Training objective (loss)
In supervised fine-tuning, the model is trained autoregressively to predict shortest-path direction tokens, excluding the question prefix from the loss. In the RL setup, the paper uses Dr.GRPO with a binary reward: one if the generated sequence is a valid shortest path and zero otherwise.

### Architecture / parameterization
From the inspected text, the experiments use 8-layer, 8-head transformer models following the LLaMA architecture with RoPE positional embeddings, pretrained from scratch in the synthetic environment.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to clarify what people even mean when they say language models “generalize” in problem solving. Many reasoning benchmarks mix together data coverage, training method, and inference procedure, so it is hard to tell whether failure comes from missing rules, unstable composition, or weak decoding. The paper wants a cleaner answer.

### 2. What is the method?
The method is to replace vague reasoning tasks with a controlled composable sequential optimization problem: shortest-path planning. The authors define two distinct OOD evaluations, spatial transfer to disjoint unseen maps and length scaling to strictly longer paths. They pretrain small transformers on random walks, then compare supervised fine-tuning and RL while also varying training data and inference-time strategies.

### 3. What is the method motivation?
The motivation is that shortest path has exact answers, controllable horizon length, and clear compositional structure. That makes it a better microscope for systematic generalization than most language benchmarks, where test examples often remain semantically close to training examples in ways that make “generalization” claims suspicious.

### 4. What data does it use?
The data is synthetic. Models are pretrained on random-walk paths over training and test maps, then fine-tuned on shortest-path examples from a training map. Evaluation uses held-out node pairs on unseen maps for spatial transfer and longer path lengths for length scaling.

### 5. How is it evaluated?
Evaluation is by exact success rate: whether the generated path is a valid shortest path. The setup measures performance separately on spatial transfer and length scaling, then analyzes how training data design, RL versus SFT, and inference-time scaling affect those outcomes.

### 6. What are the main results?
The headline result is that models show strong spatial transfer but consistently fail at length scaling. The paper’s analysis says this failure is driven more by recursive compositional instability than by the simple probability that subparts each fail independently. It also finds that RL improves training stability but does not outperform the best supervised models, and stronger inference-time strategies cannot rescue the length-scaling failure.

### 7. What is actually novel?
The novel part is not shortest path itself. It is the clean separation of spatial transfer from length scaling, plus the decomposition showing that longer-horizon failure is mainly a stability-of-composition problem rather than merely insufficient local competence. That is a more useful diagnosis than a generic “models don’t reason” conclusion.

### 8. What are the strengths?
- The task is controlled enough to make causal claims about failure modes.
- Exact verification avoids benchmark ambiguity.
- Separating spatial transfer from length scaling is genuinely clarifying.
- The paper resists overselling RL and inference-time scaling.
- The recursive-instability framing is more actionable than blanket pessimism.

### 9. What are the weaknesses, limitations, or red flags?
- It is still a synthetic task, so transfer to natural reasoning is interpretive rather than direct.
- The models are small and trained from scratch, which may limit claims about large pretrained systems.
- Shortest path is an elegant probe but not the full mess of language-grounded reasoning.
- Controlled environments can accidentally reward the wrong abstraction if we overgeneralize from them.

### 10. What challenges or open problems remain?
The hard question is how to build models that can compose locally valid operations over longer horizons without recursive drift. Another open problem is whether similar failure decompositions can be made on richer planning tasks that include memory, partial observability, or latent subgoal structure.

### 11. What future work naturally follows?
- Extend the same style of analysis to richer compositional planning domains.
- Study architectural or external-memory changes that specifically target recursive instability.
- Test whether explicit intermediate state or search helps length scaling where RL does not.
- Reproduce the separation between local transfer and horizon scaling on larger pretrained models.

### 12. Why does this matter for cabbageland?
Because it gives a cleaner standard for talking about compositional reasoning. A model that can solve new local configurations is not necessarily a model that can stably compose those skills over longer horizons. That distinction matters for planning, tool use, and world-model claims.

### 13. What ideas are steal-worthy?
- Separate local transfer from horizon scaling instead of treating “generalization” as one blob.
- Use exact, controllable environments to diagnose reasoning failures before telling big stories.
- Analyze whether longer-horizon collapse comes from local error accumulation or from unstable composition even when local steps are mostly available.
- Be skeptical of RL and inference-time scaling as universal fixes for reasoning.

### 14. Final decision
**Worth preserving as a reasoning-diagnosis reference.** It will not tell us how to solve compositional reasoning outright, but it gives a cleaner microscope for where the failure actually lives.