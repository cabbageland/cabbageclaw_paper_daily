# Legibility is Not Interpretability: Comparing Judged and Actual Importance in Chain-Of-Thought Reasoning

## Basic info

* Title: Legibility is Not Interpretability: Comparing Judged and Actual Importance in Chain-Of-Thought Reasoning
* Authors: Kevin Du, Alexander Hoyle, Laura Ruis, Acyr Locatelli
* Year: 2026
* Venue / source: COLM 2026 / arXiv
* Link: https://arxiv.org/abs/2609.04194
* Date surfaced: 2026-09-04
* Why selected in one sentence: It replaces text-only intuition about reasoning steps with a behavioral importance measure and then shows how poorly judges recover it.

## Quick verdict

* Must read

I inspected the full arXiv HTML text, especially the advantage formulation, the changepoint labeling method, the empirical characterization of reasoning traces, and the judge-versus-critic experiments. This deserves a preserved note because it attacks one of the lazier assumptions in current reasoning work: that a readable chain-of-thought step tells you how much it mattered. The paper does not just say "be careful." It builds a concrete behavioral target and then measures how far text-only interpretations miss it.

## One-paragraph overview

The paper defines the importance of a reasoning step as its **advantage**: how much including that step changes expected reward, such as the probability of ending with the correct or original final answer. It estimates that quantity with Monte Carlo rollouts from intermediate prefixes, then uses changepoint analysis to identify consequential steps. That gives the paper two complementary products. First, it uses step advantage to characterize what reasoning traces are actually doing across math problems and model scales. Second, it tests whether prompted judges or fine-tuned critics can infer that behavioral importance from the text of the reasoning step alone. The answer is only partly, and mainly when the trace is already heading toward a wrong answer.

## Model definition

### Inputs
For the reasoning model, the input is the chain-of-thought prefix plus the current step within a math reasoning trace. For the judge and critic models, the input is the text of the reasoning step and its local textual context.

### Outputs
The reasoning model outputs a continuation and final answer distribution. The judge or critic outputs a predicted importance score for a step, intended to track its estimated advantage.

### Training objective (loss)
The paper does not introduce a new reasoning model objective as the main contribution. Step importance is estimated by Monte Carlo rollouts. Fine-tuned critics are trained to predict step-level importance from text, but the inspected sections do not foreground a more specific loss than continuous score prediction, so I am not claiming a narrower objective than that.

### Architecture / parameterization
The main empirical generators are Qwen3 reasoning models. The analysis layer consists of Monte Carlo advantage estimation plus judge or critic LLMs that try to decode importance from step text.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
How do we tell which reasoning steps in a chain-of-thought actually mattered to the model's behavior, and can that importance be recovered from the step text alone?

### 2. What is the method?
Define step importance as RL-style advantage, estimate it with Monte Carlo rollouts from step prefixes, identify consequential steps with changepoint analysis, and then test judges and critics on retrieving those steps from text.

### 3. What is the method motivation?
Readable text is not the same as causal or functional importance. Process reward models, LLM judges, and faithfulness analyses often assume otherwise.

### 4. What data does it use?
The main analysis uses 30 problems from each of six math benchmarks: AIME 24, AIME 25, AIME 26, AMC 23, MATH500, and GSM8K. The authors generate 10 responses per prompt from Qwen3-1.7B, 4B, and 8B with thinking mode off, plus Qwen3-1.7B with thinking mode on for AIME 24, AIME 25, and GSM8K, totaling 1,800 responses across 180 questions per model in the non-thinking setup.

### 5. How is it evaluated?
The paper evaluates advantage patterns across step types, correctness, model scale, and dataset difficulty, then evaluates judges and critics with retrieval-style metrics such as PR-AUC and precision@k for consequential steps. It also compares against cue-based faithfulness setups.

### 6. What are the main results?
The qualitative framing result is that many apparent reasoning gains come from strong answer priors before the first reasoning step rather than dramatic mid-trace discovery. On judge performance, out-of-the-box models beat prevalence baselines but remain far below the noise ceiling: the best judge is about 9x below the in-distribution ceiling and 6x below the out-of-distribution one. Fine-tuned critics help most on incorrect responses, reaching PR-AUC around 0.28-0.30 and precision@0.5% around 0.55-0.60, but on correct responses they manage only PR-AUC around 0.065-0.10 and remain weak at small-budget retrieval. In the cue-based faithfulness comparison, 58% of uncued responses contain at least one consequential step versus only 15% with the inserted cue, which is a nice demonstration that self-advantage exposes dead-looking reasoning without prompt perturbation.

### 7. What is actually novel?
The novel move is to operationalize reasoning-step importance as behavioral advantage and then use that object both for trace analysis and for auditing the limits of text-only judges.

### 8. What are the strengths?
It uses a cleaner target than discourse-label judging, reports a noise ceiling before overclaiming interpretability, and keeps correct versus incorrect traces separate instead of averaging away the interesting asymmetry.

### 9. What are the weaknesses, limitations, or red flags?
Monte Carlo rollouts are expensive, the study is concentrated in math reasoning, and the importance estimates depend on step segmentation and the rollout policy. The critic-training objective is also less central than the evaluation object, so the paper is stronger as a measurement paper than as a direct method for improving reasoning.

### 10. What challenges or open problems remain?
Open questions include scaling this measurement to richer domains, finding cheaper proxies for advantage without collapsing back into text-only heuristics, and connecting true step importance to better process supervision or selective intervention.

### 11. What future work naturally follows?
Extend the method beyond math, probe whether internal activations predict advantage better than text, and use advantage-conditioned intervention or pruning to see whether consequential steps can be manipulated directly.

### 12. Why does this matter for cabbageland?
Because cabbageland cares about whether agent reasoning artifacts are genuinely informative or just narratively legible. This paper gives a disciplined way to keep those apart.

### 13. What ideas are steal-worthy?
Define importance behaviorally before judging it linguistically. Report a noise ceiling before calling a reasoning artifact interpretable. Always stratify correct and incorrect traces when auditing step-level supervision.

### 14. Final decision
Keep as a preserved note. This is a strong measurement paper because it replaces a flattering interpretability proxy with a harder behavioral object and then follows through on the consequences.
