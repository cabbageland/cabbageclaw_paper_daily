# MosaiChunk: Compositing Spatio-Temporal Memory for Autoregressive Video Generation

## Basic info

* Title: MosaiChunk: Compositing Spatio-Temporal Memory for Autoregressive Video Generation
* Authors: Yiwen Zhang, Haocheng Xi, Michael Tian-Yue Liu, Alexei A. Efros, Hadar Averbuch-Elor, Qianqian Wang, Haiwen Feng
* Year: 2026
* Venue / source: arXiv:2610.02153
* Link: https://arxiv.org/abs/2610.02153
* Date surfaced: 2026-10-02
* Why selected in one sentence: It gives autoregressive video models a bounded memory mechanism that retrieves fine-grained historical KV sections instead of whole old chunks.

## Quick verdict

* Highly relevant

This is a strong memory-mechanism paper. The useful idea is that a frozen video generator can reuse non-contiguous historical KV entries if the right spatial sections are selected. The paper is not solving semantic memory in general, but it gives a concrete pattern for preserving visual evidence over long rollouts.

## One-paragraph overview

MosaiChunk addresses long-horizon video revisits. Sliding-window autoregressive generation evicts old key-value cache entries, so when an object reappears the model often invents a new version of it. MosaiChunk stores historical KV in spatial sections, learns a descriptor encoder to retrieve sections whose content is relevant to the latest chunk, and concatenates the selected sections into a small far-memory "mosaic." The video backbone stays frozen. The router is trained by self-distillation: a teacher receives whole historical chunks known to contain the relevant content, while the student receives only its selected mosaic, and the student matches the teacher's denoising velocity. On RememBench, this improves revisit consistency over sliding-window and whole-chunk retrieval baselines.

## Model definition

### Inputs

The method uses generated video chunks, the frozen backbone's historical key-value cache, the current/latest chunk sections, prompts for text-to-video revisits or camera trajectories for image-to-video revisits, and a fixed active far-memory budget measured in chunk equivalents.

### Outputs

The router outputs a selected set of historical KV sections and associated value weights. The frozen autoregressive video generator then outputs future video chunks conditioned on the sliding window plus the composed MosaiChunk.

### Training objective (loss)

The descriptor encoder is trained with a self-distillation mean-squared-error loss between the frozen DiT teacher's denoising velocity and the student's denoising velocity. The teacher receives richer whole-chunk far memory; the student receives the smaller selected MosaiChunk. The backbone and stored KV remain fixed.

### Architecture / parameterization

MosaiChunk partitions unrotated KV entries into equal-size spatial sections using balanced k-means. A lightweight descriptor encoder maps pooled keys from each section into a retrieval descriptor. At generation time, sections from the latest chunk query historical sections outside the sliding window, global top-N sections are selected under the memory budget, selected values are reweighted, and the selected KV entries are concatenated as far memory.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Autoregressive video models forget fine visual details once relevant frames leave the sliding context window. Whole-history attention is too expensive, while whole-chunk retrieval wastes memory on irrelevant tokens.

### 2. What is the method?

Retrieve and compose non-contiguous historical KV sections across space and time, rather than retrieving whole chunks. The composed memory is read by the frozen video generator alongside its ordinary sliding-window context.

### 3. What is the method motivation?

Reusable visual content often occupies only a region of an old frame, not an entire chunk. A cookie inside a tin, a background decoration, or a doorway should be remembered at the level of the relevant cached features.

### 4. What data does it use?

The paper builds RememBench with two splits: 100 prompt-driven text-to-video samples and 150 image-to-video scenes from DL3DV with camera revisits, including 90-, 180-, and 360-degree turns and translation variants. Training the router uses prompt schedules or matching camera poses to identify richer teacher memory.

### 5. How is it evaluated?

The paper measures departure-to-revisit consistency with median CLIP similarity and LPIPS, plus rollout-quality metrics TempSSIM and Local Scene Drift. It compares against a sliding-window base model and Mixture of Contexts whole-chunk retrieval.

### 6. What are the main results?

On T2V at a two-chunk budget, MosaiChunk improves median CLIP from 0.751 for Base and 0.841 for MoC to 0.936, and improves LPIPS from 0.652/0.569 to 0.500. On I2V 180-degree rotation, it improves CLIP from 0.793 for Base and 0.807 for MoC to 0.863 at the two-chunk budget, with LPIPS improving to 0.609. Rollout quality metrics remain roughly matched.

### 7. What is actually novel?

The novelty is section-level retrieval inside native KV memory, plus the teacher/student velocity-matching scheme that trains a descriptor space without ground-truth target videos.

### 8. What are the strengths?

The mechanism is minimal and plausible: keep the generator fixed, retrieve the evidence it already knows how to consume, and spend memory budget on selected content rather than whole chunks. The ablations show learned descriptors and global top-N selection both matter.

### 9. What are the weaknesses, limitations, or red flags?

The evaluation mostly uses perceptual similarity proxies for revisit identity. It is not yet a full spatial memory or object model, and it depends on the backbone's KV features being reusable in this way. Dynamic interactions and exact geometry are not fully tested.

### 10. What challenges or open problems remain?

Harder revisits, moving objects, causal interactions, multiple simultaneous memory targets, and links to explicit object or map state remain open. The memory router also needs stronger tests under very long rollouts and real interactive use.

### 11. What future work naturally follows?

Combine section-level KV retrieval with geometry-aware addressing, object-centric state, or programmable world records. A useful next step would be memory entries that can be inspected and updated rather than only retrieved.

### 12. Why does this matter for cabbageland?

Cabbageland cares about memory that is usable by the next computation. MosaiChunk shows that bounded video memory can be a selective evidence interface, not just a recurrent blob.

### 13. What ideas are steal-worthy?

Retrieve historical evidence at the granularity that matches the thing to remember. Train memory selection by matching a richer-memory teacher. Use global budgeted selection instead of giving every query its own retrieval allowance.

### 14. Final decision

Preserve. It is a crisp mechanism for long-horizon video memory and a useful companion to LOCI-style spatial memory work.
