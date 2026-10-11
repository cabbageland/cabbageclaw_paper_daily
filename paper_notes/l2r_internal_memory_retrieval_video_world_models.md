# Learning to Retrieve: Internalizing Memory Retrieval for Video World Models

## Basic info

* Title: Learning to Retrieve: Internalizing Memory Retrieval for Video World Models
* Authors: JiaKui Hu, Tailai Chen, Yuqi Pan, Xuerui Qiu, Jialun Liu, Xiao Cao, Zhenxin Zhu, Guang Chen, Hangjun Ye, Bing Wang, Yanye Lu
* Year: 2026
* Venue / source: arXiv preprint
* Link: https://arxiv.org/abs/2610.11444
* Date surfaced: 2026-10-11
* Why selected in one sentence: It turns video-world-model memory retrieval from an external frame bank into an internal attention-state behavior with explicit when-to-retrieve supervision.

## Quick verdict

* Must read

This is directly relevant because it fixes a clean memory boundary in explorable video world models: past views should be retrievable by the generator itself, not only by a separate pose-overlap side channel. The mechanism is simple enough to steal: a persistent state, a camera-conditioned retrieval gate, and a re-visibility trigger supervised from 3D visibility. The main caveat is that the method still depends on camera-conditioned scene exploration benchmarks and inferred 3D re-visibility during training, so it is not a general memory solution for unconstrained video.

## One-paragraph overview

L2R targets camera-controlled video world models that drift when the camera revisits an earlier region. Existing methods often store previous frames in an external memory and retrieve them by camera overlap or explicit 3D cues. L2R instead repurposes the model's persistent internal state as memory. A camera-conditioned gate decides what historical state to read, and a retrieval trigger decides when retrieval is needed. The trigger is trained from a 3D re-visibility signal: if content left the field of view or became occluded and later re-enters, tokens for that view should retrieve history. At inference, the model can improve long-horizon revisit consistency without a separate external memory bank or explicit 3D condition.

## Model definition

### Inputs

The model receives a reference image or video context, a target camera trajectory represented with camera rays or pose-derived conditioning, noisy latent/video tokens during denoising, and accumulated persistent attention state from previous tokens or chunks.

### Outputs

The video world model generates future video frames along the requested camera trajectory. Internally, L2R emits or applies a retrieval trigger for each token and a camera-conditioned gate over the persistent state, which controls which historical information contributes to the current token generation.

### Training objective (loss)

The base model keeps its video generation / diffusion training objective. L2R adds supervision for the retrieval trigger using a 3D re-visibility target computed from depth, camera geometry, occlusion, and re-entry. The inspected text describes this as supervised trigger learning plus the normal generation training pipeline; the exact total objective is tied to the selected base world-model implementation.

### Architecture / parameterization

L2R modifies state-update attention in camera-controlled video diffusion transformers. It uses a persistent contextual state, a camera-conditioned multiplicative gate over that state, and a learned retrieval trigger. The paper evaluates variants including L2R-GLA and L2R-GDN, so the mechanism is presented as a plug-in for several state-update rules rather than a single monolithic architecture.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Video world models need long-horizon scene consistency when the camera revisits previously observed content. Recent-frame windows cannot preserve old evidence, while external memory retrieval is outside the model's own generation dynamics.

### 2. What is the method?

L2R stores historical context inside the model state and reads it through a camera-conditioned gate. A retrieval trigger decides whether a token should retrieve from history; when it fires, the gated state is used as context. The trigger is supervised by a re-visibility label that marks when previously seen content reappears.

### 3. What is the method motivation?

If memory retrieval is a side module, the generator does not learn when its own internal dynamics need history. The paper's core bet is that memory should be intrinsic: the same generative pathway that makes frames should learn how to maintain and access historical state.

### 4. What data does it use?

The paper constructs revisit and loop-closure benchmarks from RealEstate10K, DL3DV-10K, and RealCam-Vid. The re-visibility supervision is computed from depth and camera geometry. Evaluation uses controlled replay, in-domain loop closure, and open-domain return settings.

### 5. How is it evaluated?

The evaluation measures memory capacity with replay and loop-closure PSNR, SSIM, and LPIPS, plus open-domain return consistency using a vision-language judge. It also checks video quality, camera controllability, and revisit consistency so that memory gains are not just static-copy artifacts.

### 6. What are the main results?

On the memory-capacity benchmark, L2R-GLA improves replay PSNR to 14.74, versus 13.71 for VMem and 12.54 for Context as Memory at K=20. It also raises replay SSIM to 0.513 and lowers LPIPS to 0.430. L2R-GDN reaches 13.86 replay PSNR and 69.37 open-domain return score. On broader video quality and camera-control tests, L2R improves revisit consistency while maintaining competitive quality and pose control.

### 7. What is actually novel?

The useful novelty is not just adding memory; it is moving retrieval into the model's state-update dynamics and training a separate when-to-retrieve signal from geometric re-visibility.

### 8. What are the strengths?

The mechanism isolates two different questions: whether retrieval is needed and which historical state to access. It avoids explicit external memory banks at inference, evaluates loop closure directly, and shows ablations where camera-conditioned retrieval supplies the main gain while the trigger sharpens revisits.

### 9. What are the weaknesses, limitations, or red flags?

The training signal depends on estimated depth and camera geometry, so label quality matters. The benchmarks are camera-trajectory-centric and do not fully test dynamic object identity, physical interaction, or task-level planning. The method can retrieve history, but it does not guarantee that the stored state is semantically organized or editable.

### 10. What challenges or open problems remain?

The next hard step is dynamic memory: subjects that leave, move off-screen, and re-enter with changed pose or state. Another open problem is making the retrieved state inspectable enough for downstream planning rather than only improving visual consistency.

### 11. What future work naturally follows?

Extend the trigger from geometric re-visibility to object/state re-visibility, add explicit state slots for persistent entities, and test whether the internal retrieval signal can support action-conditioned prediction or robot planning.

### 12. Why does this matter for cabbageland?

Cabbageland keeps caring about world models that remember what matters. L2R is a concrete mechanism for turning memory from an external lookup table into a learned part of the generative state machine.

### 13. What ideas are steal-worthy?

Separate "when to retrieve" from "what to retrieve." Supervise retrieval using re-entry events, not just reconstruction loss. Keep memory in the model's recurrent state but make access conditional on pose or query structure.

### 14. Final decision

Preserve. This is one of the cleaner memory-mechanism papers in the batch.
