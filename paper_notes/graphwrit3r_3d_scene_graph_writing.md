# GraphWrit3R: End-to-End 3D Scene Graph Writing

## Basic info

* Title: GraphWrit3R: End-to-End 3D Scene Graph Writing
* Authors: Luka Milivojevic, Nikola Popovic, Sayan Deb Sarkar, Sebastian Koch, Iro Armeni, Luc Van Gool, and Danda Pani Paudel
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2609.31595
* Date surfaced: 2026-09-28
* Why selected in one sentence: It directly writes 3D scene graphs as structured JSON from point clouds or Gaussian splats without ground-truth object nodes at inference.

## Quick verdict

**Useful**

This is worth keeping as a practical explicit-state paper. It is not as deep as the top world-model papers, but the output contract is valuable: structured objects and relations that a downstream system can inspect, query, or plan over.

## One-paragraph overview

GraphWrit3R takes a 3D scene represented as a point cloud, Gaussian splats, or both, and autoregressively writes a JSON scene graph containing object entries and directed relationships. Point clouds are encoded with Sonata, Gaussian splats with Chorus, and co-located voxel tokens are aligned and fused before being decoded by a Qwen2.5-0.5B language model initialized from SpatialLM-style scene parsing. A per-voxel contrastive alignment loss pulls Chorus features toward Sonata's LLM-aligned feature space. The system is designed to avoid the typical multi-stage dependencies on ground-truth object boxes, proprietary VLM calls, and slow object-first pipelines.

## Model definition

### Inputs
Inputs are point clouds with XYZ/RGB features, Gaussian splat parameters, or both. The model also receives a fixed prompt specifying the JSON output format.

### Outputs
The model outputs a structured JSON scene graph with object labels, centroids, box extents, yaw angles, and subject-predicate-object relationship triplets.

### Training objective (loss)
Training uses next-token cross-entropy for JSON generation plus an auxiliary per-voxel cross-modal alignment loss. The alignment loss combines symmetric InfoNCE over co-located voxel features, cosine similarity, and MSE; gradients are stopped through Sonata so Chorus adapts toward the already LLM-aligned point-cloud space.

### Architecture / parameterization
The point-cloud branch uses Sonata, the Gaussian-splat branch uses Chorus, co-located voxel tokens are averaged, a two-layer MLP projects tokens into the LLM embedding space, and Qwen2.5-0.5B decodes the graph.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Existing 3D scene graph methods often depend on multi-stage object pipelines, ground-truth nodes or masks, proprietary model calls, or slow per-scene inference.

### 2. What is the method?
Encode 3D inputs into voxel tokens, align point-cloud and Gaussian-splat features in a shared space, fuse co-located tokens, and decode a complete graph as JSON.

### 3. What is the method motivation?
Scene graphs are useful only if they are available from real inputs. Assuming ground-truth object nodes at inference makes the representation look more operational than it is.

### 4. What data does it use?
Training uses 3DSSG/SceneVerse-style indoor scene graph annotations, with 1,170 point-cloud scenes and 620 Gaussian-splat representations from SceneSplat++. ScanNet is used for zero-shot/out-of-domain evaluation.

### 5. How is it evaluated?
The paper reports object/node recall, predicate recall, and triplet recall on 3DSSG/RIO10 and ScanNet-style evaluation, plus object-detection F1 and ablations over modality, alignment loss, and token fusion.

### 6. What are the main results?
GraphWrit3R reports state-of-the-art recall while jointly detecting objects and relationships without ground-truth nodes at inference. The ablation shows next-token loss alone is not enough for 3DGS alignment; the asymmetric contrastive alignment and simple average fusion are strongest.

### 7. What is actually novel?
The useful novelty is end-to-end local graph writing from 3D modalities, especially the voxel-level feature alignment that lets one set of weights handle point clouds and Gaussian splats.

### 8. What are the strengths?
The output is inspectable JSON, the system runs locally, and it removes a common but unrealistic inference assumption. The paper also identifies output truncation, not malformed JSON, as the main generation failure for very dense scenes.

### 9. What are the weaknesses, limitations, or red flags?
The evaluation is mostly indoor reconstructed scenes. 3DGS input quality can be noisy or incomplete, and point-cloud-only inference is strongest. The 3DSSG benchmark often uses small annotated subgraphs, so full-scene relational scaling remains under-tested.

### 10. What challenges or open problems remain?
Scaling to full, cluttered, dynamic scenes is the obvious challenge. The JSON sequence length will become a bottleneck unless the model uses hierarchical graph emission or external memory.

### 11. What future work naturally follows?
Use graph writing as a front end for embodied planning, add incremental graph updates over time, and test whether generated graphs improve downstream navigation or manipulation.

### 12. Why does this matter for cabbageland?
It is a concrete way to turn 3D perception into explicit relational state. Even if imperfect, the structure is easier to inspect and repair than latent scene features.

### 13. What ideas are steal-worthy?
Write the state in a structured format. Test with and without privileged ground-truth nodes. Align modalities at co-located spatial tokens before asking a language model to produce relations.

### 14. Final decision

**Preserve, but as useful rather than must-read.** It is a practical explicit-structure paper with real limitations and a good output contract.
