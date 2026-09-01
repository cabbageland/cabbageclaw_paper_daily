# Driving on Memory

## Basic info

* Title: Driving on Memory
* Authors: Christian Lowens, Thorben Funke, Alexandru Paul Condurache
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.31029
* Date surfaced: 2026-09-01
* Why selected in one sentence: It is a severe benchmark audit that tests how much end-to-end driving score survives when current camera input is replaced by static memories from prior traversals.

## Quick verdict

* Must read

I inspected the PDF text, especially the MemoryDrivoR intervention, the NAVSIMv1/v2 tables, the Bench2Drive and RealEngine comparisons, and the authors' own interpretation of where the shortcut does and does not hold. This earns a preserved note because it is exactly the right kind of benchmark attack: simple, legible, and informative even where it fails.

## One-paragraph overview

The paper asks whether high end-to-end driving benchmark scores really require a planner to react to the current traffic scene. Its intervention removes the evaluated scene's camera input and substitutes a memory bank of pose-indexed latent scene tokens from previous training traversals. Those memories can provide static and quasi-static context such as road layout and typical scene structure, but they cannot show the current traffic state. When this replacement almost preserves NAVSIM performance, the benchmark interpretation becomes much less flattering. When the same trick degrades badly on Bench2Drive and RealEngine, that is equally useful because it shows where stronger closed-loop evaluation does start demanding current-scene interaction.

## Model definition

### Inputs
Current ego status, current absolute pose, and retrieved latent memory tokens from prior traversals observed near the same position.

### Outputs
A planned driving trajectory plus the planner's internal subscore predictions for safety, compliance, progress, and comfort.

### Training objective (loss)
MemoryDrivoR keeps DrivoR's supervised driving objectives: imitation loss for candidate trajectories and binary cross-entropy losses for planner subscores such as collision, compliance, progress, and comfort.

### Architecture / parameterization
It builds on the transformer-based DrivoR planner. A frozen vision encoder creates pose-indexed memory tokens from prior drives; a pose embedder and transformer resampler compress retrieved memories; the unchanged planner cross-attends to those memory tokens instead of to live camera features.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to determine whether modern end-to-end driving benchmarks measure reaction to the current scene or can still be gamed by weaker static priors.

### 2. What is the method?
Replace live camera context with retrieved memories from previous traversals at nearby poses, then compare the resulting planner against the original camera-based system across multiple benchmarks.

### 3. What is the method motivation?
If a planner still scores well without seeing the evaluated scene, then the benchmark was rewarding something easier than the advertised capability.

### 4. What data does it use?
The main evaluations use NAVSIMv1, NAVSIMv2, Bench2Drive, and RealEngine, with memory banks built from training traversals for NAVSIM and Bench2Drive.

### 5. How is it evaluated?
By comparing MemoryDrivoR with camera-based DrivoR, no-camera baselines, and leaderboard systems across PDMS, EPDMS, driving score, success rate, and closed-loop variants.

### 6. What are the main results?
On NAVSIMv1, MemoryDrivoR reaches 91.1 PDMS versus 93.7 for camera-based DrivoR. On NAVSIMv2, it reaches 45.0 EPDMS versus 46.7. But on Bench2Drive it reaches only 34.7 driving score versus 61.0 for camera-based DrivoR, and the closed-loop RealEngine gap also widens sharply. The paper also notes that MemoryDrivoR still completes 21 of 220 Bench2Drive routes without infractions, showing the shortcut does not disappear entirely.

### 7. What is actually novel?
The novelty is the intervention itself. The authors use memory not as a performance booster but as an analytic probe that isolates static scene information from current dynamic perception.

### 8. What are the strengths?
The paper asks a sharp causal question and answers it with a controlled architecture-preserving intervention. The cross-benchmark comparison keeps the result honest instead of pretending one benchmark tells the whole story.

### 9. What are the weaknesses, limitations, or red flags?
The setup depends on repeated-location memory, accurate pose, and a particular planner family. It does not prove that perception is broadly unnecessary for driving; it proves that some benchmarks let static priors plus ego status travel too far.

### 10. What challenges or open problems remain?
Designing driving evaluations that truly force reaction to dynamic agents over longer horizons and under counterfactual traffic changes.

### 11. What future work naturally follows?
More counterfactual actor insertion, stronger closed-loop tests, and analogous "replace current signal with stored prior" audits in robotics and world-model evaluation.

### 12. Why does this matter for cabbageland?
Because it is a clean example of a benchmark audit that tests what the score is actually buying. Cabbageland keeps needing that posture across domains.

### 13. What ideas are steal-worthy?
Use stored priors as an ablation target for current-scene understanding. Preserve the planner and replace only the information channel you want to test. Cross-check any surprising shortcut on stronger closed-loop settings before drawing a broad conclusion.

### 14. Final decision
Keep as a preserved note. This is exactly the kind of benchmark-diagnosis paper worth citing when someone confuses a high score with evidence about the underlying mechanism.
