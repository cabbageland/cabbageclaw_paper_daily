# Is One Layer Enough? Training A Single Transformer Layer Can Match Full-Parameter RL Training

## Basic info

* Title: Is One Layer Enough? Training A Single Transformer Layer Can Match Full-Parameter RL Training
* Authors: Zijian Zhang, Rizhen Hu, Athanasios Glentis, Dawei Li, Chung-Yiu Yau, Hongzhou Lin, and Mingyi Hong
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.01232
* Date surfaced: 2026-07-03
* Why selected in one sentence: It localizes RL post-training gains to a small, stable set of middle transformer layers instead of treating adaptation as uniformly distributed.

## Quick verdict

**Highly relevant**

This is a strong diagnostic paper for LLM post-training. I inspected the full arXiv HTML / PDF, especially the layer-contribution definition, model and task coverage, RL algorithm comparisons, layer ranking stability, and discussion. The caveat is that the paper identifies where adaptation concentrates more clearly than why it concentrates there.

## One-paragraph overview

The paper asks whether full-parameter RL post-training actually needs to update all transformer layers. It freezes all but one layer, runs RL on that layer, and measures how much of the full-parameter RL improvement is recovered. Across Qwen3 and Qwen2.5 models, GRPO, GiGPO, and Dr. GRPO, and tasks spanning math, code, and agentic decision-making, a small number of middle layers recover most of the gain. The layer rankings are surprisingly stable across datasets, model families, and algorithms.

## Model definition

### Inputs

Inputs are pretrained LLMs, RL training tasks, and a chosen transformer layer to update while the rest of the model is frozen.

### Outputs

The output is a post-trained model variant plus a layer-contribution score measuring how much of full-parameter RL improvement was recovered by updating that layer alone.

### Training objective (loss)

The paper uses standard RL post-training algorithms, including GRPO, GiGPO, and Dr. GRPO. The methodological novelty is the layer-isolated training protocol and contribution metric, not a new RL loss.

### Architecture / parameterization

The study covers Qwen3 and Qwen2.5 model families. For each layer-wise run, only one transformer layer is trainable; all other layers are frozen.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

RL post-training is usually treated as a whole-model update. That hides where the behavioral change is actually happening. If only a few layers absorb most of the useful adaptation, full-parameter RL wastes compute and makes interpretability, safety auditing, and modular adaptation harder.

### 2. What is the method?

The method trains one transformer layer at a time under RL while freezing the rest of the model. It then compares the resulting performance gain with the gain from full-parameter RL. This produces a layer-contribution score, which can be ranked across layers and compared across tasks, algorithms, and model families.

### 3. What is the method motivation?

Different layers likely play different functional roles. Early layers may encode lexical and local features, late layers may format outputs, and middle layers may carry the abstract transformations that RL rewards. A layer-wise RL study can test that distribution instead of assuming all layers matter equally.

### 4. What data does it use?

The study spans mathematical reasoning, code generation, and agentic decision-making tasks, including ALFWorld-style settings. It evaluates multiple model families and RL algorithms rather than a single benchmark recipe.

### 5. How is it evaluated?

The evaluation measures task performance after single-layer RL and compares it with full-parameter RL. It also measures the stability of layer rankings across tasks, datasets, algorithms, and model families.

### 6. What are the main results?

The headline result is that one middle transformer layer can often recover most of the improvement from full-parameter RL, and in some cases surpass it. High-contribution layers concentrate in the middle of the stack, while layers close to the input or output tend to contribute less. The paper reports that rankings are strongly correlated across datasets, tasks, model families, and RL algorithms.

### 7. What is actually novel?

The novelty is the systematic localization of RL gains. The paper gives a simple experimental handle for asking which layers actually absorb post-training behavior.

### 8. What are the strengths?

The design is simple and hard to hand-wave away. Because it repeats across model families, task domains, and RL algorithms, the result is more interesting than a single ablation. The layer-contribution metric is also easy for other labs to reproduce.

### 9. What are the weaknesses, limitations, or red flags?

The result is diagnostic, not a full recipe. Single-layer RL may recover task performance while still changing hidden representations in ways that differ from full-parameter RL. The paper also does not fully explain why middle layers dominate or how this interacts with safety alignment, distribution shift, or very large frontier models.

### 10. What challenges or open problems remain?

The main open problem is mechanistic explanation. Are middle layers carrying search policy, reward-sensitive abstraction, tool-use state, or merely optimization-friendly parameters? Another open problem is whether layer-local RL preserves safety and calibration better or worse than full-model updates.

### 11. What future work naturally follows?

Try layer-local RL as a cheap adaptation baseline before LoRA or full-parameter runs. Pair layer-contribution scores with activation analysis to identify what behavior changes inside high-contribution layers. Test whether safety-critical behavior is localized to the same layers as task reward.

### 12. Why does this matter for cabbageland?

Cabbageland cares about modifiable, inspectable agents. If post-training gains are localized, future adaptation should not blindly update every parameter. The right workflow is to locate the adaptation locus, train there first, and audit there hardest.

### 13. What ideas are steal-worthy?

* Use layer-contribution as a cheap diagnostic before full post-training.
* Compare adaptation loci across tasks to find stable behavior modules.
* Treat middle layers as candidate sites for reasoning-policy changes.
* Audit high-contribution layers more aggressively after RL.
* Use single-layer RL as a compute-saving baseline.

### 14. Final decision

**Keep it.** This is a practical, mechanism-revealing post-training study. It should change the default question from "how do we RL the model?" to "where does RL actually need to act?"
