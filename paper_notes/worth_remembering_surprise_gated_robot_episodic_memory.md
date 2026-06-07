# Worth Remembering: Surprise-Gated Robot Episodic Memory

## Basic info

* Title: Worth Remembering: Surprise-Gated Robot Episodic Memory
* Authors: Nicolas Gorlo, Derek K. Wise, Alberto Speranzon, and Luca Carlone
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.03787
* Date surfaced: 2026-06-07
* Why selected in one sentence: It gives long-term robot memory a causal, unsupervised write gate based on predictive surprise instead of storing frames uniformly or trusting retrieval to fix a bad memory policy later.

## Quick verdict

**Highly relevant**

This is a strong embodied-memory paper. Its best idea is simple but important: memory formation is a write-policy problem, not just a retrieval problem. The method stores compact visual episodes only when V-JEPA-2 latent features show robust surprise under a causal sliding-window predictive model. I inspected the arXiv PDF full text, including the approach, OC-NaVQA results, GEBD results, limitations, and appendix table pointers. I did not independently verify the code or rerun the benchmarks.

## One-paragraph overview

Worth Remembering augments a 4D scene-graph robot memory with sparse episodic visual records selected by surprise. At each timestep, a causal window of frames is embedded with V-JEPA-2, pooled into a latent vector, and compared against a sliding diagonal Gaussian over recent latent history. Local maxima above a median-plus-MAD robust threshold trigger stored visual episodes, including nearby frames, robot pose, surprise score, and retrieval embeddings. These episodes are added as a layer on top of DAAAM's spatial memory and retrieved by a multimodal agent for long-horizon spatio-temporal robot QA.

## Model definition

### Inputs
The method consumes a robot image stream, robot pose at event time, and later language queries over the robot's experience. It also uses V-JEPA-2 latent features computed from causal frame windows.

### Outputs
The memory module outputs sparse episodic visual records around surprise triggers. At query time, the downstream agent can retrieve these episodes along with the existing 4D scene-graph memory.

### Training objective (loss)
There is no supervised memory-write training objective. Surprise is computed online with a sliding-window Gaussian surrogate over V-JEPA-2 features, and events are triggered by robust thresholding and non-maximum suppression.

### Architecture / parameterization
The core parameters are the frame window for V-JEPA-2, the sliding predictive window, the diagonal Gaussian feature statistics, the median absolute deviation threshold, and the stored episode size. Retrieval uses Perception-Encoder image-text embeddings over the stored episode frames.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Generalist robots cannot store every observation forever, but future instructions may refer to past events. A useful long-term memory system therefore needs a generic write rule for deciding which events are likely to matter before knowing future tasks.

### 2. What is the method?
- Embed a causal sliding window of recent frames with V-JEPA-2.
- Pool the embedding tokens into a latent feature vector.
- Maintain a sliding diagonal Gaussian over recent latent features.
- Compute a robust per-frame surprise score from normalized latent deviations.
- Trigger memory writes at local maxima above a median-plus-MAD threshold.
- Store short visual episodes around the trigger, plus pose, score, and retrieval embeddings.
- Add those episodes as an episodic layer over DAAAM's 4D scene-graph memory.

### 3. What is the method motivation?
The motivation is cognitive and practical. Surprise is a plausible signal for episodic encoding, and V-JEPA-2 features are trained to preserve predictive structure rather than pixel-level noise. That helps avoid storing every rustling leaf while still capturing semantically or spatially meaningful changes.

### 4. What data does it use?
The robot QA evaluation uses OC-NaVQA over CODa in-the-wild recordings. The generic event-boundary evaluation uses Kinetics-GEBD validation, with TAPOS results discussed separately in the appendix.

### 5. How is it evaluated?
For robot memory, the paper evaluates spatio-temporal question answering, positional error, and temporal error with GPT-5-mini reasoning over the constructed memory. It compares plain DAAAM, DAAAM plus uniform episodic memory, DAAAM plus random episodic memory, and DAAAM plus surprise-gated episodic memory under the same episodic memory budget. For event segmentation, it reports F1 across relative temporal distance thresholds.

### 6. What are the main results?
On OC-NaVQA, DAAAM plus surprise-gated episodic memory improves question accuracy from 0.711 to 0.796, reduces positional error from 41.75 meters to 36.57 meters, and reduces temporal error from 1.792 minutes to 1.510 minutes. Uniform and random episodic memory improve some accuracy but are weaker and can degrade temporal/spatial reasoning. With the default sensitivity, the method stores about 1.28 episodes per minute, roughly 30 episodes per CODa sequence and 1.7% of all frames. On Kinetics-GEBD, the method reports an average F1 of 0.833 while running online and unsupervised.

### 7. What is actually novel?
The novel part is the write gate: a causal, deployment-agnostic surprise signal in predictive video-feature space, used to decide which robot observations deserve episodic storage. It is not just another retrieval layer over all frames.

### 8. What are the strengths?
- The method has a clear memory budget story.
- The write policy is causal and unsupervised.
- It improves over same-budget uniform and random episodic storage.
- It connects high-resolution episodic evidence to a structured 4D scene-graph memory.
- The paper reports both robot QA and generic event-boundary evidence.

### 9. What are the weaknesses, limitations, or red flags?
- The causal predictive model is a simple sliding diagonal Gaussian over embeddings.
- V-JEPA-2 itself is trained non-causally, so the online surprise model is a surrogate.
- Stored episodes are sparse visual frames, not compressed temporally rich event representations.
- Retrieval uses image-text embeddings, which may miss temporal evolution inside an episode.
- Adding episodic visual evidence increases token usage and requires a multimodal LLM for downstream reasoning.

### 10. What challenges or open problems remain?
The main open problem is replacing the simple Gaussian surprise model with a richer causal or action-conditioned video world model without losing deployment robustness. Another is learning habituation, so repeatedly surprising but already-understood events do not keep triggering redundant writes.

### 11. What future work naturally follows?
- Use action-conditioned video world models as memory-write predictors.
- Store compressed event representations instead of raw sparse visual frames.
- Add habituation and consolidation so repeated events become knowledge rather than repeated episodes.
- Compare surprise gating against task-conditioned active memory policies.
- Test whether surprise-gated episodes improve robot control, not only QA.

### 12. Why does this matter for cabbageland?
Cabbageland keeps caring about explicit memory semantics. This paper says the write path matters. A memory system that stores everything and hopes retrieval will fix it later is sloppy; this gives a clean, inspectable first-pass criterion for what gets preserved.

### 13. What ideas are steal-worthy?
- Treat memory writes as first-class decisions, not passive logging.
- Compute surprise in a predictive latent space, not raw pixels.
- Use robust median-plus-MAD thresholds for capacity-controlled event storage.
- Attach episodes to a structured spatial memory instead of keeping them as disconnected clips.
- Evaluate write policies under equal memory budgets.

### 14. Final decision
**Keep.** This is one of the cleaner recent embodied-memory mechanisms because it makes the storage decision explicit, causal, and capacity-aware.
