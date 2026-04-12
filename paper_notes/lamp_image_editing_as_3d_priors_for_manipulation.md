# LAMP: Lift Image-Editing as General 3D Priors for Open-world Manipulation

## Basic info

* Title: LAMP: Lift Image-Editing as General 3D Priors for Open-world Manipulation
* Authors: Jingjing Wang, Zhengdong Hong, Chong Bao, Yuke Zhu, Junhan Sun, Guofeng Zhang
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2604.08475
* Date surfaced: 2026-04-12
* Why selected in one sentence: It tries to convert image-editing priors into explicit inter-object 3D transformations for manipulation, which is a much saner target representation than sparse language constraints alone.

## Quick verdict

* Useful

The best part of this paper is the representation choice, not the marketing line about open-world manipulation. Treating an edited target image as a source of dense geometric intent, then lifting it into an inter-object SE(3) transformation, is a real mechanism. The main caveat is that the whole pipeline inherits the failure modes of image editing, monocular depth, and cross-state registration, so I do not fully trust the precision story yet. This note is based on the arXiv abstract and accessible HTML, not a full appendix audit.

## One-paragraph overview

LAMP starts from a monocular RGB-D observation and a natural-language manipulation instruction, then asks an image-editing model to render the intended post-manipulation scene. Instead of stopping at that 2D edit, it reconstructs geometry for both the observed and edited states, identifies the active and passive objects, and estimates a relative inter-object 3D transformation that can be converted into a target pose for execution. The paper’s core claim is that image-editing models encode denser spatial interaction priors than language-only grounding or sparse 2D keypoints, and that lifting those priors into 3D yields a more generalizable manipulation representation.

## Model definition

### Inputs
The system takes an RGB observation, an aligned depth map from an RGB-D camera, and a natural-language subtask instruction. Internally it also uses an image-edited target state, monocular depth estimation for the edited image, object masks, reconstructed point clouds, and active/passive object identities.

### Outputs
The main output is an inter-object 3D transformation, effectively a target relative SE(3) relation for the manipulated object. The execution stack then converts that transformation into a target pose and end-effector trajectory.

### Training objective (loss)
From the accessible text, the paper is mostly a perception-reasoning-execution pipeline built from image editing, reconstruction, registration, and trajectory optimization modules. The exact training losses for the learned subcomponents were not fully visible in the fetched HTML. I can say the image-editing model and depth estimator are reused foundation components, but I am not going to invent a single end-to-end loss that the available text did not expose.

### Architecture / parameterization
A modular pipeline rather than a single monolithic policy: image editing for target-state synthesis, monocular 3D lifting for the edited image, point-cloud filtering and registration across observed and edited states, scale alignment, estimation of an inter-object SE(3) transformation, and downstream motion execution.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to support open-world manipulation from natural-language instructions in settings where conventional policies and VLAs often fail to generalize to unseen tasks and object combinations. More specifically, it wants a representation rich enough to express precise relative geometry, contact alignment, and pose change, which language-only or sparse 2D grounding often cannot capture.

### 2. What is the method?
The method edits the current scene image into a target post-manipulation image conditioned on the instruction, lifts both observed and edited states into 3D, filters noisy geometry, aligns the active and passive objects across states, and computes an inter-object transformation that serves as the manipulation prior. That transformation is then used to produce executable motion targets.

### 3. What is the method motivation?
The motivation is that natural language and simple 2D annotations are too sparse and ambiguous for fine-grained 3D manipulation, while current generative video and 4D models are still too inconsistent or expensive to serve as reliable 3D priors. Image editing, by contrast, may already contain strong spatial cues about how objects should move relative to one another.

### 4. What data does it use?
From the accessible text, the method operates from real monocular RGB-D observations and evaluates on diverse real-world manipulation tasks. The fetched HTML makes clear that the paper targets single-view real-world manipulation rather than synthetic full-geometry inputs, though I did not inspect the full benchmark table or dataset appendix.

### 5. How is it evaluated?
It is evaluated on open-world manipulation and on the precision of the estimated 3D transformations. The main comparison seems to be against VLM- and LLM-based manipulation pipelines, plus nearby methods that use 2D or weaker intermediate representations.

### 6. What are the main results?
The accessible text claims that LAMP yields precise 3D transformations and strong zero-shot generalization across diverse real-world manipulation tasks. I believe the qualitative mechanism, but I would want the full tables before fully trusting the precision margins.

### 7. What is actually novel?
The real novelty is lifting image edits into a continuous, geometry-aware inter-object transformation representation. That is more interesting than the paper’s broader “general priors for open-world manipulation” packaging.

### 8. What are the strengths?
It chooses a better intermediate representation than a lot of recent manipulation papers. The pipeline is explicit about active object, passive object, edited target state, and final relative transform. It also tries to preserve geometric structure instead of letting the whole problem collapse into opaque action tokens.

### 9. What are the weaknesses, limitations, or red flags?
The entire stack is brittle to compounding upstream errors. If the image edit changes object scale, invents geometry, or misreads the instruction, the 3D lifting and registration stages inherit that damage. The paper acknowledges some of this with special handling for scale inconsistency and noisy point clouds, which is honest, but it also reveals how fragile the path from edited image to reliable SE(3) target may be.

### 10. What challenges or open problems remain?
The big open problem is whether edited target images are stable enough to serve as precision manipulation priors in cluttered or contact-rich settings. Another is whether the method can handle genuinely novel objects and affordances where image editing is semantically plausible but geometrically wrong. More broadly, the field still needs representations that are both dense and grounded without relying on a long chain of brittle reconstruction heuristics.

### 11. What future work naturally follows?
A natural next step is uncertainty-aware transformation estimation, where the system does not collapse to one edited target if the edit is ambiguous. Another is combining the representation with stronger 3D scene models or object-centric world models that can verify whether the proposed transformation is physically feasible before execution.

### 12. Why does this matter for cabbageland?
Because it points toward a useful design rule: if manipulation needs geometry, then the intermediate representation should itself be geometric and inter-object, not just linguistic or tokenized action mush. Even if LAMP is not yet robust enough to be the answer, it is asking the right representational question.

### 13. What ideas are steal-worthy?
Treat edited futures as candidate geometric goals rather than as final outputs. Represent manipulation intent as an explicit inter-object transformation. Use dense target-state synthesis to recover alignment cues that sparse text grounding misses. Keep the execution interface anchored in object relations rather than only in end-effector trajectories.

### 14. Final decision
Keep as adjacent inspiration. The representation is worth remembering. The full pipeline is still fragile enough that I would not elevate it to a core anchor without a deeper read.
