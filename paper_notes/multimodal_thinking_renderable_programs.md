# Multimodal Thinking with Renderable Programs

## Basic info

* Title: Multimodal Thinking with Renderable Programs
* Authors: Sunli Chen, Ding Zhong, Ziqiao Ma, Jiaxin Liu, Zeyuan Yang, Hao Zhang, Lie Lu, Joyce Chai, and Chuang Gan
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2609.30130
* Date surfaced: 2026-09-27
* Why selected in one sentence: It uses SVG programs as an explicit, renderable multimodal scratchpad for geometry reasoning instead of relying on opaque raster edits or text-only rationales.

## Quick verdict

**Highly relevant**

This is a good mechanism paper for tool-using multimodal reasoning. The absolute benchmark scores are still low, but the representation choice is right: SVG is inspectable, editable, deterministic, and naturally tied to geometric structure.

## One-paragraph overview

SVGLM teaches VLMs to generate SVG overlays as intermediate visual reasoning steps. The model can call a rendering tool with XML-encoded SVG plus a canvas specification, receive the rendered image, and continue reasoning from that visual state. The authors curate an 8K dataset of SVG tool-call samples for geometry problems using MathCanvas sources, GPT-5 filtering/verification, and Gemini coordinate generation. Fine-tuned 7B/8B VLMs improve on MathCanvas-Bench geometry categories, and SVG rendering beats a GPT-4o plus image-editing pipeline that suffers from hallucinated or domain-misaligned raster edits.

## Model definition

### Inputs
Inputs are geometry question images, text questions, conversation history, and optionally a rendered SVG overlay on the question canvas. During tool use, the model receives prior visual context and can emit SVG code inside tool-call tokens.

### Outputs
The model outputs either a final answer or a tool call containing XML-encoded SVG and a canvas selection. The external tool renders the SVG overlay into an image that is fed back into the conversation.

### Training objective (loss)
The models are trained with supervised fine-tuning on SVG-enhanced conversation data. The paper uses full fine-tuning of language model parameters while freezing the VLM vision towers and multimodal projectors, with learning rate 1e-5 for three epochs.

### Architecture / parameterization
SVGLM is a tool-use/paradigm layer applied to existing open-source VLMs. The evaluated bases are LLaVa-Next-Mistral-7B, Qwen2.5-VL-7B, and InternVL3-8B, trained via LLaMA-Factory-style SFT.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Text-only chain-of-thought is weakly grounded in diagrams, while raster or latent image edits are hard to inspect and often hallucinate. Geometry reasoning often needs explicit auxiliary lines, labels, and coordinate-like edits.

### 2. What is the method?
Let the model generate SVG programs during reasoning, render them deterministically onto the image, and feed the rendered image back into the VLM. The SVG acts as both text program and visual artifact.

### 3. What is the method motivation?
SVG is grounded, editable, semantically meaningful, and resolution-independent. Unlike Python plotting, it is declarative and lightweight. Unlike raster image generation, it preserves explicit primitives such as lines, points, text, paths, and coordinates.

### 4. What data does it use?
The authors curate 8,000 SVG samples from MathCanvas-Instruct plane and solid geometry tasks. GPT-5 filters tasks where a solution image can be constructed by adding captions and figures. Gemini-3.0-Thinking creates SVG annotations on a 1000x1000 canvas. GPT-5 verifies rendered outputs, and human evaluation finds 79.5% perfect reconstructions, 10% slight translation errors, 9.5% major translation errors, and 1% structural errors.

### 5. How is it evaluated?
The main benchmark is MathCanvas-Bench, restricted to plane geometry and solid geometry samples with images, giving 1,244 QA pairs. Weighted accuracy gives later subquestions higher weight. The paper compares zero-shot VLMs, direct SFT, SVGLM, GPT-4o, V-Thinker, and GPT-4o plus Qwen-Image-Edit.

### 6. What are the main results?
Qwen2.5-VL-7B improves from 19.5 weighted zero-shot and 21.8 direct SFT to 30.9 with SVGLM. InternVL3-8B improves from 19.5 zero-shot and 23.0 SFT to 29.8. LLaVa-Next-Mistral-7B improves from 14.6 zero-shot to 23.1 with SVGLM. GPT-4o plus Qwen-Image-Edit reaches only 19.6, roughly matching GPT-4o alone.

### 7. What is actually novel?
The novelty is using renderable vector programs as the reasoning medium for multimodal chain-of-thought, plus a practical data pipeline for teaching VLMs to emit useful SVG overlays.

### 8. What are the strengths?
The representation has the right inductive bias for diagrams. The tool output is deterministic and inspectable. The ablations show both SVG generation and rendered feedback matter, and the comparison with image editing clarifies why raster generation is a poor fit for this task.

### 9. What are the weaknesses, limitations, or red flags?
The method is demonstrated mainly on geometry-style diagram reasoning. The absolute accuracies remain far from solved, and the data pipeline leans heavily on strong closed models for filtering, coordinate generation, and verification. It may not transfer cleanly to natural images where SVG primitives are a worse substrate.

### 10. What challenges or open problems remain?
Scaling to richer diagrams, charts, UI screenshots, and document reasoning will require better primitive libraries, more reliable coordinate grounding, and stronger correction loops when rendered SVG is wrong.

### 11. What future work naturally follows?
Combine SVG workspaces with verifier loops, extend from geometry to charts and interfaces, and let models edit existing SVG trees rather than generate overlays from scratch.

### 12. Why does this matter for cabbageland?
It is a concrete case where explicit state beats latent vibes. The model's intermediate reasoning becomes renderable, checkable, and editable, which is exactly the kind of structure that makes agents less mushy.

### 13. What ideas are steal-worthy?
Use deterministic renderable programs as multimodal scratchpads. Feed the rendered artifact back to the model. Keep the intermediate representation human-inspectable and geometry-aware.

### 14. Final decision

**Worth keeping.** The benchmark is narrow, but SVG-as-scratchpad is a strong pattern for visual reasoning systems.
