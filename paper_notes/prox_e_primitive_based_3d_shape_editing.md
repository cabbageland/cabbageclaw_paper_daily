# Prox-E: Fine-Grained 3D Shape Editing via Primitive-Based Abstractions

## Basic info

* Title: Prox-E: Fine-Grained 3D Shape Editing via Primitive-Based Abstractions
* Authors: Etai Sella and collaborators from the accessible arXiv HTML were not fully visible in the fetched excerpt
* Year: 2026
* Venue / source: SIGGRAPH 2026 / arXiv
* Link: https://arxiv.org/abs/2604.23774
* Date surfaced: 2026-04-28
* Why selected in one sentence: It uses a crude but explicit primitive proxy to turn vague text-guided 3D editing into a controllable structural editing problem, which is exactly the kind of proxy design that often matters more than raw generator scale.

## Quick verdict

**Useful**

This is adjacent rather than central for cabbageland, but it is a good adjacent paper because the proxy representation is doing real conceptual work. Instead of hoping 2D image editors understand 3D metric edits, the method gives a vision-language model a small interpretable vocabulary of primitives and uses that edited proxy to guide 3D generation. I inspected the abstract and substantial method text from the arXiv HTML, so confidence is good on the pipeline and motivation, but weaker on quantitative details and how often the verification loop truly saves bad edits.

## One-paragraph overview

Prox-E is a training-free 3D editing system for fine-grained structural edits. It first decomposes an input shape into superquadric primitives, then asks a vision-language model to edit a color-coded JSON description of those primitives, including adding or deleting parts when needed. The edited proxy is not treated as the final geometry. Instead, it acts as a coarse structural guide inside a 3D generative model through a proxy-induced denoising process that preserves unchanged regions, warps transformed regions, and synthesizes new geometry where required. Appearance edits are handled later with 2D image editing. The key point is that the primitive abstraction gives the model an explicit handle on structure and metric relationships.

## Model definition

### Inputs
The system takes an input 3D shape and a text editing instruction. For the proxy-editing stage, the VLM also receives orthogonal renders of the primitive decomposition, a render of the original shape, and a JSON file listing primitive parameters such as scale, pose, and shape exponents.

### Outputs
It outputs an edited JSON proxy, then an edited 3D structure generated under proxy guidance, and finally an appearance-refined edited 3D asset.

### Training objective (loss)
The paper describes Prox-E as training-free. The accessible text does not present a new task-specific learning objective for the overall editing system. It reuses existing components, including a primitive decomposition method, a pretrained VLM, a 3D generative backbone based on TRELLIS, and 2D image editors.

### Architecture / parameterization
A hybrid pipeline: primitive decomposition into superquadrics, VLM-based editing over a color-coded JSON abstraction, iterative visual verification on the proxy, proxy-induced denoising inside a 3D generative model, and separate appearance refinement via 2D image editing.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Modern text-guided 3D editing often piggybacks on strong 2D image editors, but those editors are bad at precise geometric or metric changes. They can add a bunny to a chair, but they struggle with instructions like widening a seat by a fixed factor or changing one structural part while preserving identity everywhere else. The paper wants controllable structural editing rather than just semantically plausible image edits.

### 2. What is the method?
- Decompose the input shape into a small set of superquadric primitives.
- Render those primitives with unique colors and package their parameters in JSON.
- Ask a VLM to edit that abstraction under a minimal-intervention principle, potentially changing parameters or adding and deleting primitives.
- Run a visual verification loop by re-rendering the edited proxy and asking the VLM to confirm or revise it.
- Use the edited proxy to guide a 3D generative model through proxy-induced denoising and latent blending.
- Apply separate appearance refinement with 2D image editing after the structural edit is coherent.

### 3. What is the method motivation?
The motivation is that pixel-space editing is the wrong interface for precise 3D edits. If the edit is fundamentally structural, the system needs a representation where lengths, orientations, part identity, and topology changes are at least somewhat explicit. A primitive proxy is coarse, but it is far better suited to metric editing than hoping a diffusion model infers geometry from a few rendered views.

### 4. What data does it use?
The accessible text describes broad experiments across text-guided 3D editing tasks and comparisons to training-based and image-based 3D editors, but the fetched excerpt did not include a full dataset breakdown. I am therefore not claiming exact benchmark names beyond the visible references to broad comparative evaluation.

### 5. How is it evaluated?
The paper evaluates the balance among three things: preservation of structural identity, quality of the generated shape, and fidelity to the text edit. It compares against several 3D editing paradigms, including 2D-based lifting approaches and training-based 3D editors.

### 6. What are the main results?
The visible text claims the method achieves a better balance of identity preservation, shape quality, and instruction fidelity than the compared baselines. That claim is plausible because the method changes the representation in a way the baselines often avoid, but I did not inspect the full quantitative tables or user studies.

### 7. What is actually novel?
The key novelty is not merely using primitives. It is treating a primitive abstraction as the editable interface for a VLM and then using the edited proxy as a volumetric guide inside 3D generation. The proxy is neither only a user-control widget nor merely a preprocessing artifact. It is the core control channel.

### 8. What are the strengths?
- It cleanly diagnoses why 2D-driven 3D editing fails on metric structure.
- The primitive abstraction is interpretable and compact.
- The method supports structural edits, part addition and deletion, and local preservation within one interface.
- The training-free framing is meaningful here because the gains come from representation and orchestration rather than another end-to-end finetune.

### 9. What are the weaknesses, limitations, or red flags?
- The primitive decomposition is only a coarse approximation, so some shapes will fit awkwardly.
- The VLM verification loop may still miss subtle structural mistakes, especially when the proxy looks plausible from a few views.
- The full stack is fairly elaborate, so “training-free” does not mean simple.
- The method still depends on a strong generative prior downstream, so proxy faithfulness is not guaranteed.
- This is great for controllable editing, but less obviously helpful if you need native generative abstraction rather than editing an existing shape.

### 10. What challenges or open problems remain?
The big challenge is scaling this kind of explicit proxy control to richer topology, deformable objects, and more open-ended scene-level generation. Another is deciding when the coarse proxy is good enough and when it is actually bottlenecking the edit.

### 11. What future work naturally follows?
- Learn better editable proxies that stay explicit without becoming unbearably detailed.
- Extend the method from single objects to scenes and interaction-aware assets.
- Use uncertainty or verification signals to detect when proxy edits are under-specified.
- Explore whether explicit proxy editing can help planning or affordance reasoning, not just generation.

### 12. Why does this matter for cabbageland?
Because it is a crisp reminder that explicit structure does not need to be perfect to be useful. A coarse primitive abstraction can still be enough to make a large generative system much more controllable. That is a reusable design lesson well beyond 3D editing.

### 13. What ideas are steal-worthy?
- Use a small explicit proxy vocabulary as the interface for editing or planning.
- Let a strong model operate on interpretable intermediate structure instead of raw pixels alone.
- Treat minimal intervention and identity preservation as first-class constraints.
- Separate structural editing from appearance editing rather than forcing one model to do both.

### 14. Final decision
**Keep as adjacent inspiration.** This is not a robotics paper, but it is a strong example of the kind of proxy design cabbageland should keep noticing: explicit enough to guide the model, coarse enough to stay manageable, and actually used rather than merely decorative.