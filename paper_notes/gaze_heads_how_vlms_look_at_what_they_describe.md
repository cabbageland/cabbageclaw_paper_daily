# Gaze Heads: How VLMs Look at What They Describe

## Basic info

* Title: Gaze Heads: How VLMs Look at What They Describe
* Authors: Rohit Gandikota, David Bau
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.14703
* Date surfaced: 2026-06-15
* Why selected in one sentence: It finds a small set of VLM attention heads whose image-region attention is not just correlated with grounding, but causally steers what the model says.

## Quick verdict

* Highly relevant

This is the best mechanistic ML paper in today's scan because it turns interpretability into an inference-time control lever. I inspected the full arXiv PDF, including the discovery score, steering intervention, comic-strip evaluation, natural-image transfer, model-family comparisons, and limitations. I did not audit the code, generated comic dataset, or LLM-judge implementation, so the exact margins remain paper claims, but the causal intervention is the right kind of evidence.

## One-paragraph overview

Gaze Heads studies how vision-language models connect generated text to image regions. Using six-panel comic strips as a controlled testbed, the authors identify attention heads in the language-model backbone whose text-to-image attention tracks the currently described panel. In Qwen3-VL-8B, the top 100 heads, fewer than 9% of all heads, can be forced to attend to a chosen panel with a simple attention-mask bias; the model's answer then describes that target panel at 83.1% accuracy on visual question answering, far above chance and random-head controls. The same head set can be switched mid-generation, making the model move to a new visual target within a few tokens. The mechanism also appears in several VLM families and partially transfers to COCO natural images, though some frozen-encoder families show no comparable gaze-head set.

## Model definition

### Inputs
The studied models take image tokens plus text prompts. Discovery primarily uses six-panel comic strips where panel identity gives a controlled visual grounding target. Later experiments use natural COCO images with object-region targets.

### Outputs
The model outputs natural-language answers or narrations. The paper also extracts per-head text-to-image attention patterns, gaze scores, steering outcomes, and redirection accuracy.

### Training objective (loss)
No new model is trained for the core method. The paper performs inference-time analysis and attention-mask intervention on pretrained VLMs. The original VLM pretraining/fine-tuning losses are not the paper's optimization target.

### Architecture / parameterization
The primary model is Qwen3-VL-8B-Instruct, a transformer-based VLM. The method scores attention heads in the language-model backbone and redirects selected heads by adding an attention bias toward a target image region. Comparisons include Qwen3-VL model sizes and several other VLM architectures.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
VLMs can describe images, but it is often unclear which internal mechanism decides what part of the image gets grounded into the current words. Existing attention visualizations are mostly correlational; the paper asks whether there is a small causal channel that controls the described region.

### 2. What is the method?
The authors use comic strips because the correct visual target is spatially separated into panels. For each attention head, they compute a gaze score measuring whether the head attends to the queried or currently narrated panel. They then take the top-scoring heads and inject an additive attention-mask bias so those heads can only attend to a chosen target region. If output follows the target, the head set is causally involved.

### 3. What is the method motivation?
Grounded language generation is temporally local: as a model describes one object or panel, it should attend to the corresponding visual evidence, then shift when the description shifts. A head set that tracks and controls that shift would be more useful than a static localization map.

### 4. What data does it use?
The main discovery and evaluation data are generated six-panel comic strips with controlled panel layouts. The paper also evaluates region steering on COCO val2017 images and compares across several VLM families and sizes.

### 5. How is it evaluated?
Evaluation measures whether steering selected heads redirects the generated answer or narration to the chosen panel or image region. Controls include random non-gaze heads, image/localization head baselines, all-head interventions, different numbers of selected heads, dynamic target switching, natural-image region targets, and model-family transfer.

### 6. What are the main results?
On Qwen3-VL-8B, redirecting the top 100 gaze heads reaches 83.1% accuracy on six-panel VQA and 79.4% on static narration, with chance at 16.7%. Random non-gaze heads fail to redirect, and all-head intervention damages generation. Dynamic steering follows the target schedule much better than controls. On COCO, gaze-head steering more than doubles the non-gaze control across object-size classes. The mechanism recurs across Qwen3-VL sizes and several other VLMs, but not all architectures.

### 7. What is actually novel?
The novelty is causal localization of a multimodal grounding mechanism. The paper does not merely show that attention overlaps an object; it shows that redirecting a small head set redirects what the model describes.

### 8. What are the strengths?
The experiment has a clean controlled setting, direct causal intervention, strong controls, dynamic steering, and cross-model probing. The mechanism is cheap to find: a few forward passes and a correlation score, no gaze supervision or retraining. The intervention is also precise enough that too few heads under-controls and too many heads break generation, which supports the idea of a tuned functional subset.

### 9. What are the weaknesses, limitations, or red flags?
Comic strips are a clever testbed but also a shaped one; panel identity is cleaner than normal visual grounding. Natural-image transfer is weaker, especially for small objects where there are fewer image tokens. The evaluation uses LLM judging for some redirection decisions. The mechanism is not universal: some frozen-encoder families show no comparable gaze-head set. The paper does not prove why certain training recipes produce gaze heads or how stable the interface is under fine-tuning.

### 10. What challenges or open problems remain?
The big open question is whether gaze-head-like channels can be made robust enough for debugging or control in deployed multimodal systems. It is also unclear how the mechanism interacts with hallucination, multi-object reference, occlusion, dense documents, video, and instruction-following under adversarial prompts.

### 11. What future work naturally follows?
Apply the same intervention to video-language models, document VLMs, medical VLMs, and embodied perception stacks. Test whether gaze-head steering can reduce hallucination or expose ungrounded answers. Study training factors that create or suppress the mechanism, especially encoder fine-tuning versus frozen vision encoders.

### 12. Why does this matter for cabbageland?
Cabbageland wants explicit, controllable interfaces between perception and language. Gaze heads are a candidate micro-interface: a small causal channel for "what visual region is currently being spoken about." Even if the exact head set is model-specific, the method is a useful recipe for finding grounding levers instead of treating multimodal attention as decorative heatmaps.

### 13. What ideas are steal-worthy?
Use structured visual tasks to discover causal grounding channels. Prefer intervention over visualization. Search for small head/token subsets that control behavior without retraining. Treat "what the model is looking at while it speaks" as an editable state variable. Compare against all-head intervention, because global steering can break generation and hide the useful local control surface.

### 14. Final decision
Keep and cite. This is a strong example of mechanistic interpretability becoming a practical control tool. The caveats matter, but the paper earns the "causal control surface" framing.
