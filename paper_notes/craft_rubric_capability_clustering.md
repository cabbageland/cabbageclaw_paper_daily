# CRAFT: Clustering Rubrics to Diagnose Weak LLM Capabilities and Generate Targeted Fine-Tuning Data

## Basic info

* Title: CRAFT: Clustering Rubrics to Diagnose Weak LLM Capabilities and Generate Targeted Fine-Tuning Data
* Authors: Vipul Gupta, Zihao Wang, Razvan-Gabriel Dumitru, MohammadHossein Rezaei, Aakash Sabharwal, Yunzhong He
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.16122
* Date surfaced: 2026-07-20
* Why selected in one sentence: It changes the diagnostic unit from whole prompts to rubric criteria, which turns evaluation output into a more useful recipe for what to fine-tune next.

## Quick verdict

**Highly relevant**

This is a good paper because the intervention is narrow and the question is practical. Instead of asking where a model failed, it asks which capability named by the rubric failed, then uses that to target synthetic SFT data. I inspected the arXiv HTML sections covering the methodology, hierarchy construction, weak-node selection, data-generation stage, and results discussion.

## One-paragraph overview

CRAFT starts from rubric-based evaluation datasets where each prompt has several explicit scoring criteria. Rather than clustering whole prompts, it flattens the dataset into prompt-rubric pairs, extracts a capability description for each criterion, clusters those descriptions into a hierarchical capability tree, scores a target model at every node, and selects low-performing nodes at the depth where each weakness is clearest. Those weak nodes then condition synthetic training-data generation. The paper argues that rubric criteria are the right unit because one prompt can test several different skills, and the experiments support that claim: under fixed data budget, teacher generation, and fine-tuning recipe, criterion-level targeting beats prompt-level targeting more often than not.

## Model definition

### Inputs
The pipeline takes prompts, rubric criteria, target-model responses, dataset metadata such as domain or rubric subcategory, and a target model whose weaknesses are being diagnosed.

### Outputs
It outputs a hierarchical capability tree, node-level pass-rate estimates, a selected set of weak capability nodes, synthetic prompt-response training data targeted at those nodes, and the resulting fine-tuned target model.

### Training objective (loss)
CRAFT itself is mostly a diagnosis and selection pipeline built from embeddings, `k`-means clustering, and prompted LLM steps for extraction and routing. The downstream target models are fine-tuned with a standard supervised fine-tuning objective on a fixed `1,000`-example synthetic dataset budget.

### Architecture / parameterization
The main components are criterion-to-capability extraction, hierarchical clustering with fixed top levels when metadata exists, top-down low-performing-node selection with support thresholds, and a synthetic-data generator conditioned on the selected weak nodes and nearby tree context.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to make evaluation more actionable by turning rubric-based failures into specific capability diagnoses that can directly guide post-training data generation.

### 2. What is the method?
The method converts each prompt-rubric pair into a capability description, organizes those descriptions into a hierarchical capability tree, scores the target model at every node, selects weak nodes top-down across levels, then generates synthetic training examples targeted at those nodes.

### 3. What is the method motivation?
The motivation is that prompt-level clustering is too coarse. A single prompt can contain several rubric criteria, and failing one criterion is not the same as failing the entire prompt's semantic region.

### 4. What data does it use?
The diagnosis data is the PRBench finance subset with `629` prompts and `10,806` rubric criteria, plus the PRBench legal subset with `532` prompts and `9,637` rubric criteria. Final reporting uses `13` held-out benchmarks, `7` legal and `6` finance, disjoint from the rubric data.

### 5. How is it evaluated?
It is evaluated by comparing CRAFT against EvalTree and Random under the same teacher generation, same `1,000`-example data budget, same SFT setup, and repeated temperature-decoding evaluation on held-out benchmarks.

### 6. What are the main results?
CRAFT achieves the best finance-domain average for all four tested open models and the best legal-domain average for three of four, while staying within the decoding-variance band of the best baseline on the remaining legal model. The results are benchmark-level heterogeneous, but the domain-average pattern consistently favors criterion-level targeting over prompt-level targeting.

### 7. What is actually novel?
The novelty is treating rubric criteria as capability probes and selecting weak nodes across tree levels rather than fixing a single analysis depth or clustering whole prompts.

### 8. What are the strengths?
The paper isolates one concrete design choice, keeps the downstream fine-tuning pipeline fixed, and asks the useful operational question: which capabilities should we train next?

### 9. What are the weaknesses, limitations, or red flags?
The method assumes high-quality rubrics and reasonably consistent judges. It is also still synthetic-data dependent, limited to finance and legal, and somewhat heavy because several LLM-assisted tree-building steps sit in the loop.

### 10. What challenges or open problems remain?
The big challenge is portability to domains without good rubrics, plus robustness to noisy or overlapping criteria where the extracted capability descriptions may drift or collapse.

### 11. What future work naturally follows?
The next steps are human-written targeted data instead of only synthetic data, better judge reliability audits, and extensions to multimodal or tool-use rubrics where criteria name more procedural capabilities.

### 12. Why does this matter for cabbageland?
Cabbageland wants evaluations that expose mechanism-level weaknesses, not only leaderboard numbers. CRAFT is useful because it turns eval artifacts into a concrete training curriculum.

### 13. What ideas are steal-worthy?
Use rubric criteria, not prompts, as the diagnostic atom. Build capability trees where depth is chosen by failure clarity rather than by a fixed reporting convention. Select disjoint weak nodes with support thresholds. Feed parent and sibling context into targeted data generation so the new data does not blur adjacent skills together.

### 14. Final decision
**Keep it.** The paper makes evaluation materially more useful without pretending to solve everything.
