# PerceptionRubrics: Calibrating Multimodal Evaluation to Human Perception

## Basic info

* Title: PerceptionRubrics: Calibrating Multimodal Evaluation to Human Perception
* Authors: Yana Wei, Hongbo Peng, Yanlin Lai, Liang Zhao, Kangheng Lin, En Yu, Keyu Lv, Han Zhou, Yin Tang, Haodong Li, Mitt Huang, Hangyu Guo, Jianjian Sun, Zheng Ge, Xiangyu Zhang, Daxin Jiang, Vishal M. Patel
* Year: 2026
* Venue / source: arXiv / ICML 2026
* Link: https://arxiv.org/abs/2606.28322
* Date surfaced: 2026-06-29
* Why selected in one sentence: It replaces smooth holistic caption scoring with instance-specific mandatory visual facts and gated penalties.

## Quick verdict

* Highly relevant

This is the strongest evaluation paper in today's scan because its scoring rule encodes an important deployment truth: missing a mandatory visual fact should not be averaged away by mentioning many easy details. I inspected the full arXiv PDF, including dataset construction, rubric generation, gated metric, experiments, analysis, appendices visible in text extraction, and conclusion. I did not inspect the released data or rerun the benchmark, so claims about judge stability and model ranking remain paper claims.

## One-paragraph overview

PerceptionRubrics builds a multimodal perception benchmark from 1,038 dense images and more than 12,000 instance-specific rubrics. The pipeline first creates long golden captions through a circular peer-review process among multiple frontier MLLMs plus human verification, then distills two kinds of rubrics: Must-Right facts that are mandatory, and Easy-Wrong facts that capture common fine-grained mistakes. The scoring rule is gated: if a model fails any Must-Right criterion, its score for that image becomes zero; only models that pass the gate receive graded credit for Easy-Wrong details. This makes the benchmark a useful critique of average-style caption metrics that reward fluent partial descriptions while hiding catastrophic visual omissions.

## Model definition

### Inputs
The benchmark input is an image spanning domains such as natural scenes, documents and OCR, digital UI, structured data, STEM/expert diagrams, logic puzzles, and creative/cultural images. Evaluated MLLMs receive the image and produce a description or answer.

### Outputs
The evaluated model outputs text. The benchmark outputs boolean judgments for each rubric item, a binary Must-Right gate per image, Easy-Wrong scores for passed images, domain scores, overall compliance scores, and model rankings.

### Training objective (loss)
No evaluated model is trained in this paper. The benchmark construction uses MLLMs to generate captions and rubrics, then LLM-as-judge scoring to evaluate outputs. There is no learned loss for the benchmark itself.

### Architecture / parameterization
The method is an evaluation pipeline rather than a model architecture. It uses a multi-model caption consensus process, Gemini-3-Pro as a rubric proposer, GPT-OSS-120B as the primary judge in the paper, and a gated metric defined by a product over Must-Right rubric pass indicators multiplied by the average Easy-Wrong pass rate.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It targets the gap between saturated multimodal benchmark scores and visible deployment brittleness. Existing holistic similarity metrics can give high scores to responses that sound plausible but miss essential visual facts.

### 2. What is the method?
The method builds dense golden captions, converts them into image-specific rubrics, separates mandatory facts from common fine-detail traps, and scores model outputs with a gate. The gate is strict: fail any Must-Right fact, and the score for that item is zero.

### 3. What is the method motivation?
Human perception is often conjunctive for important facts. If a caption misses that the object is a skateboard rather than rollerblades, or misses a key sign, chart element, or UI layout, extra correct minor details should not fully compensate. The scoring rule tries to make that brittleness visible.

### 4. What data does it use?
The benchmark contains 1,038 images, 1,038 golden captions, 12,004 rubrics, 4,232 Must-Right rubrics, and 7,772 Easy-Wrong rubrics. The images cover seven domains: natural scenes, document/OCR, digital UI/UX, structured data, STEM/expert, logic/puzzle, and creative/cultural material.

### 5. How is it evaluated?
The paper evaluates 25 proprietary and open-weight MLLMs, reports domain and overall compliance scores, compares atomic rubric accuracy with all-Must-Right pass rate, checks alignment with Vision Arena human preference scores, probes length bias, tests judge robustness with a second judge, and studies rubric subsampling stability.

### 6. What are the main results?
The best overall model in the reported table reaches about 70 percent, leaving substantial headroom. The best open-source model trails the proprietary frontier by about 8 points in the paper's scoring. GUI and information-dense interfaces are major failure sources. A reliability gap appears: models often pass many individual atomic checks but fail the strict conjunction of mandatory facts. For five overlapping models, PerceptionRubrics reports stronger alignment with Vision Arena scores than DOCCI or DetailCaps, with Pearson 0.916 and Spearman 1.000.

### 7. What is actually novel?
The gated scoring rule is the main useful novelty. Atomic rubrics are not new, LLM-as-judge is not new, and dense captioning benchmarks are not new. But combining instance-specific mandatory facts with a hard gate is a cleaner approximation of how many perceptual failures matter in real systems.

### 8. What are the strengths?
The benchmark directly attacks metric smoothing. The domain split is broader than normal natural-image captioning, with UI, structured data, documents, and expert diagrams included. The paper also checks length bias and judge robustness instead of pretending LLM judging is magically objective.

### 9. What are the weaknesses, limitations, or red flags?
The pipeline relies heavily on frontier MLLMs to create golden captions, propose rubrics, and judge outputs. Human verification is present but lightweight and discard-on-divergence may bias the dataset toward images where model consensus is already high. The hard gate is intentionally severe, but it can over-penalize a response if a single rubric is flawed, too strict, or not actually mandatory for the user's task.

### 10. What challenges or open problems remain?
The hard part is making rubrics trustworthy enough to deserve hard gates. Future benchmarks need stronger human auditing, task-conditioned mandatory facts, and perhaps multiple gates for different downstream uses rather than one universal perception standard.

### 11. What future work naturally follows?
Apply gated rubric scoring to agent UI operation, chart understanding, medical image reports, robotics scene descriptions, and visual grounding in long-running workflows. Study how model training changes when the reward is a hard mandatory-fact gate instead of a smooth caption score.

### 12. Why does this matter for cabbageland?
Cabbageland needs evaluation that notices when an agent misses the one thing that matters. PerceptionRubrics gives a simple rule worth stealing: if a necessary fact fails, do not let fluent peripheral detail launder the mistake into a passing score.

### 13. What ideas are steal-worthy?
Split checks into mandatory facts and fine-grained traps. Use common model errors to generate Easy-Wrong rubrics. Report atomic accuracy and all-mandatory pass rate separately. Treat UI and structured-data perception as first-class, not as a footnote to natural-image captioning.

### 14. Final decision
Keep and cite. The MLLM-generated rubric pipeline needs auditing, but the gated evaluation idea is sharp and broadly reusable. This is especially useful for agent evaluation where one missed visual fact can invalidate the whole action.
