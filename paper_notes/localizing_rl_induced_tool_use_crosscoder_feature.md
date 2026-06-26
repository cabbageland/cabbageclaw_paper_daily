# Localizing RL-Induced Tool Use to a Single Crosscoder Feature

## Basic info

* Title: Localizing RL-Induced Tool Use to a Single Crosscoder Feature
* Authors: Andrii Shportko, Shubham Bhokare, Ahmed Zeyad A Alzahrani, Bowen Cheng, Gustavo Mercier, Jessica Hullman
* Year: 2026
* Venue / source: arXiv; Mechanistic Interpretability Workshop at ICML 2026
* Link: https://arxiv.org/abs/2606.26474
* Date surfaced: 2026-06-26
* Why selected in one sentence: It provides a concrete model-diffing case where an RL-installed agentic behavior becomes sparse enough to steer through one crosscoder feature.

## Quick verdict

* Highly relevant

This is the sharpest mechanistic interpretability note from today's scan. I inspected the full arXiv PDF, including the DFC setup, hyperparameter sweep, reconstruction/spillover results, targeted steering experiments, discussion, limitations, and appendix table snippets surfaced by targeted text search. I did not run the code or reproduce the steering cells, so the exact feature identities and effect sizes remain paper claims.

## One-paragraph overview

The paper compares a base Qwen2.5-3B model with a ToolRL-fine-tuned Qwen2.5-3B model and trains crosscoders to jointly decompose their activations. Dedicated Feature Crosscoders split the dictionary into RL-model-exclusive, base-model-exclusive, and shared feature partitions. Across 48 crosscoder variants, reconstruction improves the RL model's tool-calling behavior and even transfers a small amount of tool correctness into the frozen base model. The core result is targeted steering: in one layer-13 setup, adding a single A-exclusive feature raises tool correctness by 65 percentage points, matching the effect of steering all available A-exclusive features in that cell. The caveat is scope: this is one model pair, one tool-use behavior, and a small evaluation harness.

## Model definition

### Inputs

The model-diffing setup takes residual-stream post-MLP activations from two Qwen2.5-3B models: Model A, ToolRL-Qwen2.5-3B fine-tuned for structured tool calls, and Model B, the base Qwen2.5-3B model. Training data includes 40,000 FineWeb samples and 40,000 ToolRL instruction-output pairs. Evaluation uses held-out ToolRL prompts.

### Outputs

The crosscoder outputs sparse feature activations and reconstructions for both models' residual streams. The behavioral evaluation outputs format accuracy, tool correctness, and an overall score. The steering experiments output changes in tool correctness under additive feature interventions.

### Training objective (loss)

The Dedicated Feature Crosscoder minimizes reconstruction mean squared error plus sparsity penalties. The dictionary is partitioned into A-exclusive, B-exclusive, and shared features, with gradient masking enforcing which model each partition can decode into. The reported objective is reconstruction MSE plus shared-feature L1 penalty and exclusive-feature sparsity penalty; top-k sparsity is enforced in the encoder.

### Architecture / parameterization

The paper compares standard CrossCoders with Dedicated Feature Crosscoders. The sweep varies architecture, dictionary size, top-k sparsity, exclusive-share percentage, and exclusive-partition penalty. Steering ranks features by Cohen's d between tool-use and general-text activations, then adds scaled decoder directions for selected features into the RL model's activation stream.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It asks where RL-induced tool-use behavior lives inside a language model. RL can make a model produce structured tool calls, but it is unclear whether that capability is diffuse, preserved in shared representations, localized to model-specific features, or steerable without retraining.

### 2. What is the method?

Train crosscoders on paired activations from a base model and its ToolRL-fine-tuned counterpart. Use Dedicated Feature Crosscoders to split the dictionary into A-exclusive, B-exclusive, and shared partitions. Evaluate whether reconstruction preserves or transfers tool-use behavior, whether the exclusive partition isolates RL-specific features, and whether high-discrimination features can be steered at inference time to increase tool correctness.

### 3. What is the method motivation?

If RL-installed behaviors condense into sparse features, they become inspectable and controllable. That would give agent builders a different kind of safety and debugging handle: not just train or prompt the model, but identify and modulate the internal features that mediate action-taking behavior.

### 4. What data does it use?

It uses Qwen/Qwen2.5-3B as the base model and chengq9/ToolRL-Qwen2.5-3B as the RL model. Crosscoder training uses 40,000 FineWeb general-domain samples and 40,000 ToolRL instruction-output pairs. The sweep evaluates 100 held-out ToolRL prompts per variant; steering cells evaluate 40 prompts with greedy decoding.

### 5. How is it evaluated?

Behavior is scored with three metrics: whether a `<tool_call>` with a JSON `name` field appears, whether the called tool name matches a numbered tool in the prompt, and an overall score. The paper measures pre- and post-reconstruction behavior, spillover into the base model, geometry of feature partitions, feature-steering effects at different feature budgets and strengths, cross-layer generalization, and sanity checks such as B-exclusive steering.

### 6. What are the main results?

Across 48 variants, post-reconstruction improves Model A tool correctness from 19% to 50.1%, a mean gain of 31.1 percentage points with 9.7 point standard deviation. The frozen base model gains 6.8 points of tool correctness after reconstruction, despite no fine-tuning; the paper calls this capability spillover. CrossCoders and DFCs have similar reconstruction error and similar unbudgeted behavioral ceilings, but the DFC A-exclusive partition reaches its steering effect with far fewer features. In the key layer-13 cell, one A-exclusive feature at alpha 32 raises tool correctness by 65 points with reported 95% CI from 47.9 to 82.1. CrossCoder steering needs 33 features to reach its unbudgeted 70-point peak.

### 7. What is actually novel?

The novelty is not "SAEs can steer behavior" in general. The useful move is paired model diffing for an RL-installed agent behavior, plus the observation that the decisive steering signal can be extremely sparse. The paper also notes a side-channel: joint decomposition can transfer some tool-selection behavior into the frozen base model.

### 8. What are the strengths?

The paper is concrete. It uses a paired model setup, sweeps crosscoder hyperparameters, distinguishes reconstruction fidelity from behavior recovery, includes steering ablations, and tests whether B-exclusive steering stays flat as a harness sanity check. The discussion is also appropriately cautious about DFCs acting as filters rather than perfect sinks for capability-specific signal.

### 9. What are the weaknesses, limitations, or red flags?

The scope is narrow: one 3B model family, one RL fine-tuning target, one tool-call behavior, 100 held-out prompts per sweep variant, and 40 prompts per steering cell. "Capability" here means reliable structured tool-call generation in this harness, not broad agent competence. The single-feature result may depend on this particular ToolRL setup and on the chosen crosscoder training recipe. The paper does not establish that more complex action policies, planning behaviors, or refusal/abstention boundaries will localize similarly.

### 10. What challenges or open problems remain?

The main open problem is generality. Do other RL-induced behaviors localize into tiny feature sets, or is tool-call formatting unusually compressible? Can these features be clamped to suppress unwanted action-taking without damaging useful capability? How stable are feature identities across seeds, layers, model sizes, and datasets? Can crosscoder releases leak capability by making spillover easy?

### 11. What future work naturally follows?

Replicate on more model families, larger models, multiple tool-use formats, and real multi-step agents. Study suppression as well as amplification. Test whether features controlling the decision to act versus abstain can be found. Compare Dedicated Feature Crosscoders with delta-style model diffing methods designed for asymmetric fine-tuning. Add adversarial tests where steering should not cause irrelevant tool use.

### 12. Why does this matter for cabbageland?

Cabbageland cares about agents that take actions. This paper suggests that some action-enabling behavior might be monitored and controlled at the feature level, not only through prompts or post-training. The spillover result is also a warning: interpretability artifacts trained across capability-separated models may themselves become a capability-transfer substrate.

### 13. What ideas are steal-worthy?

Use paired model diffing to identify features installed by post-training. Separate reconstruction quality from behavioral recovery. Treat feature partitions as filters, not magical namespaces. Look for tiny feature sets that control action-taking, then test both amplification and suppression. Include no-op partitions as steering-harness sanity checks.

### 14. Final decision

Keep and cite, with narrow-scope caution. This is not proof that agentic behavior is generally one-feature-steerable, but it is a strong concrete example of sparse internal control after RL post-training.
