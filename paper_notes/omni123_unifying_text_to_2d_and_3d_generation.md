# Omni123: Exploring 3D Native Foundation Models with Limited 3D Data by Unifying Text to 2D and 3D Generation

## Basic info

* Title: Omni123: Exploring 3D Native Foundation Models with Limited 3D Data by Unifying Text to 2D and 3D Generation
* Authors: Chongjie Ye, Cheng Cao, Chuanyu Pan, Yiming Hao, Yihao Zhi, Yuanming Hu, Xiaoguang Han
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2604.02289
* Date surfaced: 2026-04-04
* Why selected in one sentence: It is one of the more structurally interesting recent 3D-generation papers because it treats image-3D consistency as an explicit learning constraint rather than just another data source.

## Quick verdict

**Useful**

This paper is ambitious and more interesting than the average “3D foundation model” pitch, mainly because it has a real answer to the limited-3D-data problem. The answer may still be somewhat industrial and data-heavy, but at least it is structurally coherent: unify text, image, and 3D as tokens, then use interleaved cross-modal generation cycles to force geometric consistency. I inspected the arXiv abstract and substantial HTML paper text, including the motivation, data pipeline, architecture framing, and training setup, but I did not audit appendices, code, or exact benchmark tables.

## One-paragraph overview

Omni123 is trying to build a native autoregressive model that can handle text-to-image, text-to-3D, image-to-3D, and 3D editing inside one tokenized multimodal sequence space. The core problem is obvious: web-scale 2D data exists, but 3D data is scarce and noisy, so a purely text-to-3D system is badly under-constrained. The paper’s solution is to make images do more than supply extra supervision. It uses interleaved text-image-3D training and cross-modal generation cycles so that semantic intent, appearance fidelity, and geometric consistency have to line up across modalities. In other words, the image channel is supposed to function as a bridge and geometric prior, not just more stuff in the batch.

## Model definition

### Inputs
The unified model takes tokenized text, image tokens, and 3D geometry tokens in different conditional-generation configurations. Depending on the task, any subset of those modalities can act as input context for autoregressive prediction over the target modality.

### Outputs
It outputs sequences of image tokens or 3D geometry tokens, supporting tasks such as text-to-image generation, image-to-3D generation, text-to-3D generation, and iterative 3D editing.

### Training objective (loss)
From the accessible text, the core learning setup is autoregressive next-token prediction over mixed multimodal sequences rather than a diffusion objective. The paper also relies heavily on cross-modal task design and interleaved training curricula. I am not claiming more detailed full-loss bookkeeping than what was visible in the HTML.

### Architecture / parameterization
Unified autoregressive multimodal transformer over discrete text, image, and 3D tokens, with a shared sequence space and interleaved X-to-X training across heterogeneous paired and triplet datasets.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Native 3D generation is data-starved compared with 2D generation. Text-to-3D is especially under-constrained, and many existing methods end up depending on indirect 2D optimization loops or pipelines that sacrifice geometric consistency.

### 2. What is the method?
- Tokenize text, images, and 3D geometry into one shared sequence space.
- Train a unified autoregressive model across many conditional generation directions rather than one narrow task.
- Use paired text-image, image-3D, and text-3D data, plus synthesized text-image-3D triplets.
- Interleave cross-modal tasks so the model traverses semantic-visual-geometric cycles such as text to image to 3D to image.
- Treat consistency across those cycles as an implicit structural constraint on the learned 3D representation.

### 3. What is the method motivation?
The paper argues, correctly, that simply mixing modalities does not guarantee useful transfer because different tasks carry different priors and can interfere with each other. The motivation for the interleaved cycle design is that images contain abundant geometric hints, so forcing 3D predictions to remain consistent with image generations may partially compensate for the scarcity of native 3D supervision.

### 4. What data does it use?
The accessible HTML describes a very large multi-stage corpus: text-image pairs, image-3D pairs, text-3D pairs, and synthesized triplets for supervised fine-tuning. The pipeline includes large-scale rendered 3D assets, VLM-generated and filtered captions, and synthetic text-to-image-to-3D data creation. The numbers are big enough that data engineering is clearly a major part of the story.

### 5. How is it evaluated?
The paper evaluates text-guided 3D generation and editing, and studies how different multimodal objectives affect semantic alignment and geometric consistency. The accessible text frames the comparisons against prior text-to-3D paradigms and other native 3D generative approaches, but I did not inspect enough of the results section to verify exact benchmark winners.

### 6. What are the main results?
The reported story is that interleaved cross-modal generation improves geometric consistency and semantic alignment for text-guided 3D generation and editing relative to weaker multimodal formulations. I believe the direction of that claim. I am less willing to endorse the full scale of the headline without reading the complete results tables and ablations more carefully.

### 7. What is actually novel?
The useful novelty is not merely “unified text-image-3D model.” That phrase is cheap now. The better claim is that cross-modal generative cycles are used as an implicit geometric regularizer, with interleaving designed to reduce task interference rather than just pooling all modalities into one training soup.

### 8. What are the strengths?
- The paper recognizes the actual bottleneck instead of pretending 3D scarcity is solved.
- Cross-modal consistency is treated as a structural learning device, not just a marketing phrase.
- The setup could plausibly support native 3D editing rather than endless 2D-lift hacks.
- It is directly relevant to multimodal world-model ambitions where 2D and 3D evidence should constrain each other.

### 9. What are the weaknesses, limitations, or red flags?
- A lot of the paper’s power may come from industrial-scale data curation and synthesis rather than a crisp architectural breakthrough.
- The data pipeline is heavy enough that reproduction and attribution of gains may be messy.
- “Foundation model” framing may overstate how general the learned representation really is.
- I did not inspect enough hard ablations to know whether the cycle structure itself, rather than sheer data volume and curation quality, is carrying most of the benefit.

### 10. What challenges or open problems remain?
The main open problems are disentangling architecture gains from data-pipeline gains, extending this beyond mostly object-centric 3D generation toward richer scenes and persistent worlds, and testing whether the learned geometry is genuinely robust or just benchmark-friendly.

### 11. What future work naturally follows?
- Push the same cross-modal consistency idea toward full 3D scenes and world states.
- Study whether explicit object/state factorization works better than flat autoregressive token streams.
- Use the bridge between images and 3D as persistent memory for embodied or interactive systems.
- Probe whether interleaved multimodal generation can support planning or simulation, not just asset generation.

### 12. Why does this matter for cabbageland?
Because it is one of the few recent 3D papers that at least tries to turn multimodality into an actual constraint rather than a vague promise. If 3D learning is under-constrained, borrowing structure from image generation is sensible, provided the bridge preserves geometry instead of merely decorating outputs.

### 13. What ideas are steal-worthy?
- Treat cross-modal cycles as regularizers, not just extra tasks.
- Use abundant 2D data as a structural prior for scarce 3D learning.
- Design multimodal curricula to manage task interference explicitly.
- Ask whether token unification is buying real geometry or only implementation convenience.

### 14. Final decision
**Keep, but with some skepticism.** Worth preserving because the structure is more serious than usual, but I would want deeper ablations before treating it as a clean architectural victory.
