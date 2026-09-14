# Does Video Memory Use What It Retrieves? A Causal Audit of Memory Specificity

## Basic info

* Title: Does Video Memory Use What It Retrieves? A Causal Audit of Memory Specificity
* Authors: Aditi Tiwari, Akshit Bhalla, Darshan Prasad, Heng Ji
* Year: 2026
* Venue / source: arXiv:2609.12090
* Link: https://arxiv.org/abs/2609.12090
* Date surfaced: 2026-09-14
* Why selected in one sentence: It gives a clean causal test for whether video memory gains come from exact retrieved content, broader context, or generic representation repair.

## Quick verdict

* Must read

This is one of the most useful memory-evaluation papers in the recent batch. It turns "memory helps" into a causal question by intervening only on the consumed memory value while preserving the rest of the read pathway. The method is simple enough to reuse, and the results are uncomfortable in the right way: some world-model memory gains barely depend on the exact retrieved episode, while SAM 2's spatial memory is strongly content-specific.

## One-paragraph overview

The paper introduces read-time memory substitution for video systems. At a target memory read, it replaces the memory value consumed by the model while keeping the query, selected memory locations, number of entries, temporal path, weights, and downstream computation fixed. This lets the authors measure benefit recovery: how much of the original memory benefit remains when the correct memory is swapped for a wrong, context-matched, identity-free, perturbed, or zero value. Across frozen video world models, WorldMem, and SAM 2, the paper finds three different regimes: generic representation repair, graded broader-context dependence, and exact spatial-memory dependence.

## Model definition

### Inputs

The audit consumes already trained video-memory systems and a target memory read. Depending on the system, the inputs include current video state or frame features, the model's memory query, selected memory slots, stored value tensors, temporal context, and evaluation-specific substitution values.

### Outputs

The audited system outputs the normal task prediction: revisit latent consistency for frozen video world models, generated future video quality for WorldMem, or segmentation masks for SAM 2. The audit outputs benefit recovery scores under each substitution control.

### Training objective (loss)

The paper does not train the main audited systems for the core intervention. It evaluates frozen or pretrained systems. For the identity-free and learned-constant controls, some substitute values are estimated from training-memory representations, but the central method is a read-time causal intervention, not a new model-training objective.

### Architecture / parameterization

The intervention is model-family agnostic. It is applied to memory pathways attached to frozen video world models, WorldMem's native generative memory, and SAM 2's native spatial memory and object pointer. The key parameterization is the substitution ladder: correct memory, wrong memory, same-trajectory wrong memory, disjoint donor memory, identity-free memory, perturbed memory, mean content, learned constant, and zero/content-free controls.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Video memory papers often show that memory improves performance, but that does not prove the retrieved content is causally responsible. A memory module might help by giving the model a generic representation stabilizer, by preserving broader trajectory context, or by retrieving exact episodic evidence. The paper tries to distinguish these regimes.

### 2. What is the method?

The method is read-time memory substitution. At a selected memory read, replace only the value consumed by the memory pathway and leave the rest of the model intact. Then compute benefit recovery:

* 1 means the substitute recovers the full correct-memory benefit.
* 0 means it does no better than the content-free reference.
* intermediate values reveal partial dependence on the removed information.

The substitution ladder removes information in stages, from exact place identity to broader context to memory-like structure.

### 3. What is the method motivation?

Ordinary memory ablations destroy the entire pathway, so they conflate "the pathway helps" with "the retrieved content matters." Substitution keeps the memory interface alive and changes only the content, making the causal claim testable.

### 4. What data does it use?

The experiments use Ego-Exo4D, 7-Scenes, TUM, WorldMem evaluation cases, DAVIS 2017, and MOSEv2 reappearance events. The systems evaluated include frozen latent/action-conditioned video world models, WorldMem, and SAM 2 with a Hiera small backbone.

### 5. How is it evaluated?

Frozen world models are evaluated by revisit consistency error. WorldMem is evaluated by PSNR and LPIPS beyond the context window. SAM 2 is evaluated by mean region and boundary score, plus reappearance recovery over one, five, and ten frames.

### 6. What are the main results?

On DINO-WM-style frozen world models, identity-free training-memory controls recover 102% of correct-memory benefit on Ego-Exo4D and 101% on 7-Scenes; TUM shows a mixed 70% recovery. Recovery falls from 102% to 1% as identity-free values are perturbed away from observed training-memory representations, supporting representation repair. WorldMem shows graded context dependence: same-trajectory wrong memory recovers 94.1% of the PSNR benefit, while a disjoint trajectory and biome donor recovers 43.7%. SAM 2 is strongly content-dependent: wrong spatial memory drops DAVIS J and F from 0.926 to 0.182, and at MOSEv2 reappearance wrong spatial memory collapses the return-frame score from 0.459 to 0.000.

### 7. What is actually novel?

The novelty is not a new memory architecture. It is the causal audit: measuring memory specificity by substituting the value consumed at a read while preserving the selected read interface and earlier trajectory. The representation-repair dose response is also a useful addition because it distinguishes generic magnitude injection from proximity to learned memory representations.

### 8. What are the strengths?

The intervention is clear, reusable, and interpretation-friendly. It compares multiple memory families rather than selling one architecture. It explicitly separates exact identity, broader context, and identity-free memory-like support. It also reports limitations honestly, especially for TUM and WorldMem controls.

### 9. What are the weaknesses, limitations, or red flags?

The full substitution ladder and representation-repair tests are deepest for DINO-WM; V-JEPA 2 gets a lighter second-host check. WorldMem controls change several context factors at once, so they show graded dependence but do not isolate a single semantic variable. The TUM split is small. The audit still requires access to internal read values, which may be unavailable for closed systems.

### 10. What challenges or open problems remain?

The obvious next step is to turn this audit into a standard protocol across long-video language models, recurrent state models, retrieval-based world models, and agent memories. Another open problem is training objectives that reward the desired specificity regime rather than discovering after the fact that a memory does not use its content.

### 11. What future work naturally follows?

Apply substitution ladders across channels, layers, and times; audit KV-cache and recurrent state "memory"; design losses that encourage exact-content use only when task ambiguity demands it; and build benchmarks where representation repair is separated from true episodic recall.

### 12. Why does this matter for cabbageland?

Cabbageland cares about world models, memory, explicit state, and long-horizon consistency. This paper gives a direct test for whether the alleged memory state is actually carrying the episode-specific variable the architecture claims it carries.

### 13. What ideas are steal-worthy?

Use benefit recovery rather than only performance deltas. Build substitution ladders instead of one wrong-memory control. Test representation repair by moving identity-free values away from the training-memory manifold and by holding magnitude fixed while rotating direction. Treat memory specificity as task-dependent rather than automatically good or bad.

### 14. Final decision

Preserve. This is a high-value diagnostic primitive for any future memory or world-model work.
