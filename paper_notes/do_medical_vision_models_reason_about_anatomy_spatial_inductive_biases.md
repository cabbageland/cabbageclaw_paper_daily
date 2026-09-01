# Do Medical Vision Models Reason About Anatomy? Probing the Spatial Inductive Biases of Learned Visual Representations

## Basic info

* Title: Do Medical Vision Models Reason About Anatomy? Probing the Spatial Inductive Biases of Learned Visual Representations
* Authors: Naren Akash, Neeraja Ramanan
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.28092
* Date surfaced: 2026-08-31
* Why selected in one sentence: It breaks the lazy phrase "anatomical reasoning" into representation, readout, and cohort effects that can actually be tested.

## Quick verdict

* Must read

I inspected the full arXiv HTML text, especially the SPAR-Bench construction, the architectural sweep, the TotalSegmentator transfer checks, and the MLLM comparison. This earns a preserved note because it is a genuinely useful evaluation paper: it shows exactly how easy it is to confuse canonical-position recall, token information, and patient-specific spatial reasoning.

## One-paragraph overview

The paper builds SPAR-Bench, a set of eight spatial probes over abdominal CT slices designed to separate localization, relational reconstruction, and within-image queries. The key move is not simply to show that some models do poorly. It is to vary what reads the representation and where the test cohort comes from. Under those changes, capabilities that looked established often collapse. Frozen features can contain relational information that pooled probes miss, in-domain anatomy questions can fall to chance under cohort transfer, and neither foundation-model scale nor fine-tuning rescues the hardest within-slice comparison tasks. The result is a much better audit of what medical encoders actually know.

## Model definition

### Inputs
Abdominal CT slices or organ tiles, question embeddings for probe tasks, and a set of baseline or foundation-model encoders with attached readout heads.

### Outputs
Coordinate predictions, permutation matrices, or classification answers for spatial queries such as relative position, orientation, organ size, distance, and bilateral symmetry.

### Training objective (loss)
Localization uses MSE on normalized coordinates, permutation recovery uses a Sinkhorn-based permutation loss, and query heads use cross-entropy. The paper is mainly an evaluation framework rather than a new end-to-end foundation model.

### Architecture / parameterization
The study factors backbone choice and readout head: CNN versus ViT, MLP versus Transformer, plus medical foundation models including RadDINO, BiomedCLIP, and SAM-Med2D, with both frozen and fine-tuned settings where relevant.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Medical vision models are often said to understand anatomy, but most evaluations do not separate canonical priors, within-image reasoning, readout limitations, and cohort-specific shortcuts.

### 2. What is the method?
Build SPAR-Bench with three levels: coordinate localization, shuffled-tile permutation recovery, and six spatial query probes, then test multiple encoder and readout combinations plus zero-shot transfer and MLLM question answering.

### 3. What is the method motivation?
A single in-domain score can flatter a model for the wrong reason. To know whether an encoder really supports spatial reasoning, you have to vary the head and the cohort and see what survives.

### 4. What data does it use?
SPAR-Bench is built from the WORD abdominal CT dataset, using 150 volumes plus 20 LiTS volumes with tumor annotations. The paper also evaluates zero-shot transfer on TotalSegmentator and probes four open-weight MLLMs.

### 5. How is it evaluated?
It compares from-scratch CNN and ViT baselines, frozen and fine-tuned medical encoders, pooled versus token-level readouts, in-domain versus cross-cohort testing, and direct MLLM answering on the Level 3 probe set.

### 6. What are the main results?
The strongest diagnostic result is the readout gap: frozen BiomedCLIP reaches only 0.7% permutation accuracy with a pooled MLP head but 67.8% with a Transformer over the same tokens. In-domain relative-position scores can exceed 98%, yet frozen RadDINO plus MLP drops to about 50.0 on TotalSegmentator, effectively chance. Bilateral symmetry stays at chance across all 13 configurations. The MLLMs also fail badly on tasks encoders handle well, with relative-position accuracy around 49.5 to 50.1 and orientation often near chance.

### 7. What is actually novel?
The novelty is not "medical models are weak." It is the decomposition: representation content, readout choice, and cohort transfer are each treated as variables that can create or destroy a capability claim.

### 8. What are the strengths?
The benchmark is clean, the controls are sharp, and the conclusions are much more specific than typical medical-AI scorecards. The pooled-versus-token readout result is especially useful.

### 9. What are the weaknesses, limitations, or red flags?
The paper is still limited to 2D slices and a specific anatomical region. Bilateral symmetry may also be a noisy probe because slice position can distort kidney area ratios. The study shows capability failure, but not always whether the failure is in the representation or just the chosen head.

### 10. What challenges or open problems remain?
Testing 3D reasoning, other organs and modalities, richer readout heads, and labels less vulnerable to anatomical shortcutting. A good follow-up would also include mask-input upper bounds for the harder probes.

### 11. What future work naturally follows?
SPAR-style audits for other medical domains, representation analyses that preserve token structure, and capability probes for multimodal medical assistants that compare internal encoders and full system outputs directly.

### 12. Why does this matter for cabbageland?
Because cabbageland keeps caring about honest evaluation. This paper shows how easily a good-looking score can be produced by the wrong mechanism.

### 13. What ideas are steal-worthy?
Always vary the readout before declaring a representation incapable. Always test cohort transfer before calling an anatomy probe a reasoning probe. Include at least one task with no stable canonical answer.

### 14. Final decision
Keep as a preserved note. This is one of the better recent evaluation papers because it exposes where the hidden shortcut actually lives.

## 6. Mandatory critical angles

The paper is strongest on evaluation realism, representation analysis, and failure-mode isolation. Its main weakness is scope: 2D abdominal CT is enough to make the point, but not enough to settle medical spatial reasoning as a whole.

## 7. Writing style

Keep the note severe. The useful contribution here is the demolition of sloppy capability claims, not a cheerful benchmark release.

## 8. Repository output format

Saved as a preserved paper note because SPAR-Bench is a reusable example of how to separate representation, readout, and cohort effects in visual reasoning claims.
