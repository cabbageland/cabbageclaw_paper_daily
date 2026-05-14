# Retrieve-then-Steer: Online Success Memory for Test-Time Adaptation of Generative VLAs

## Basic info

* Title: Retrieve-then-Steer: Online Success Memory for Test-Time Adaptation of Generative VLAs
* Authors: Jianchao Zhao, Huoren Yang, Yusong Hu, Yuyang Gao, Qiguan Ou, Cong Wan, SongLin Dong, Zhiheng Ma, Yihong Gong
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2605.10094
* Date surfaced: 2026-05-14
* Why selected in one sentence: It turns repeated VLA deployment into a concrete memory-guided sampling problem instead of pretending each test episode is independent.

## Quick verdict

* Highly relevant

This is not a grand new memory architecture, but it is a good paper because the mechanism is clean and the deployment framing is honest. The main contribution is a non-parametric reuse loop for successful local experience, not a deep representational breakthrough. I inspected the abstract, introduction, related work, problem formulation, and substantial method text in the arXiv HTML, including memory construction, retrieval filtering, and confidence-adaptive prior guidance, but I did not fully audit every appendix and empirical detail.

## One-paragraph overview

The paper asks whether a frozen generative vision-language-action model can get more reliable during deployment by reusing its own successful interactions in the same environment. Instead of updating parameters, it stores successful observation-action segments in an online memory, retrieves relevant past action chunks for the current state, filters inconsistent candidates, aggregates the survivors into an elite action prior, and injects that prior into the intermediate state of a flow-matching action sampler. The idea is to bias generation toward behavior that already worked in the target environment while still letting the base model refine actions from the current observation.

## Model definition

### Inputs
The policy takes the current observation, which includes multi-view RGB images and proprioceptive state, plus a language instruction. The retrieval module also consumes the current retrieval key derived from the VLA visual encoder and the stored memory bank of successful observation-action segments.

### Outputs
The system outputs an action chunk for the robot to execute. Internally it also outputs retrieved candidate action chunks, an aggregated elite action prior, and a confidence-controlled sampler initialization state.

### Training objective (loss)
The paper does not introduce a new main training loss for the policy itself in the accessible core text. The base VLA is treated as frozen at deployment time. The adaptation mechanism is inference-time and non-parametric. The paper does mention a pretrained progress critic used to score trajectory progress for memory construction rather than train the deployed policy.

### Architecture / parameterization
A generative VLA with a flow-matching action head, augmented by an online memory of successful observation-action segments, nearest-neighbor style retrieval using visual encoder features, dynamic-time-warping consistency filtering, weighted action-prior aggregation, and confidence-adaptive initialization of the flow-matching sampler.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Generative VLAs often look competent offline but become brittle during real deployment, especially when small perception shifts or execution noise accumulate over repeated long-horizon tasks. Existing evaluation usually treats test episodes as independent, which wastes the fact that real robots often operate repeatedly in the same local environment. The paper tries to exploit successful past executions as reusable evidence for future inference without full retraining.

### 2. What is the method?
The method builds an online success memory during deployment. After each episode, a progress estimator identifies whether enough progress was made and keeps only the successful prefix up to the progress peak. At inference time, the system retrieves the most similar stored states, filters the corresponding action chunks using pairwise trajectory consistency via dynamic time warping, aggregates the consistent chunks into an elite action prior, and injects that prior into the intermediate state of the flow-matching sampler. The injection strength is adjusted using a retrieval-confidence estimate so low-confidence retrieval falls back toward the original sampler.

### 3. What is the method motivation?
The motivation is good and fairly grounded. In repeated local deployment, a successful action sequence already encodes camera quirks, geometry, actuation bias, and environment-specific execution details. Throwing that information away after evaluation is wasteful. If the base model is partly competent, then steering it with environment-verified successful fragments may improve stability without the complexity and risk of online policy updates.

### 4. What data does it use?
The paper evaluates on language-conditioned robotic manipulation benchmarks including LIBERO-10 and SimplerEnv, and it also reports real-world bimanual manipulation experiments. In the accessible method text, one successful demonstration video from training is used as a reference process for the progress critic.

### 5. How is it evaluated?
It is evaluated by comparing task success and closed-loop stability against the frozen base generative VLA and against other inference-time steering or scaling approaches on simulated long-horizon manipulation benchmarks and real-world tasks. The accessible text emphasizes stronger gains on multi-stage and long-horizon settings.

### 6. What are the main results?
The paper reports improved task success and more stable closed-loop behavior in both simulation and real-world manipulation. The strongest claim is not raw scale but robustness improvement under persistent deployment. I did not fully audit every table, so I trust the direction of improvement more than the exact margins.

### 7. What is actually novel?
The real novelty is the specific formulation of deployment-time memory reuse as a retrieve-then-steer generative process. Instead of selecting among sampled actions after the fact, the method retrieves successful cross-episode action evidence first and uses it to initialize generation. The progress-calibrated memory construction plus confidence-adaptive prior injection is a reasonably coherent package.

### 8. What are the strengths?
The paper has a believable use case. It fixes a real mismatch between independent-episode evaluation and persistent deployment. The memory object is concrete, the filtering step is legible, and the steering mechanism is lightweight enough to seem deployable. I also like that it preserves the generative policy rather than collapsing immediately to nearest-neighbor action replay.

### 9. What are the weaknesses, limitations, or red flags?
The stored memory is still shallow in one important sense: it is successful observation-action segments, not an explicit causal or semantic state model. That means the method may help local reliability more than genuine abstraction or transfer. The reliance on similarity retrieval and dynamic-time-warping consistency also suggests possible fragility under larger scene changes or under tasks where the same visual state admits many distinct good futures. The progress critic is another dependency that could quietly shape what counts as “successful” memory.

### 10. What challenges or open problems remain?
How to move from local successful segment reuse to more structured reusable memory, how to handle environments that drift enough to poison retrieval, how to represent uncertainty over multiple valid futures, and how to extend this beyond repeated local settings into genuinely open-world adaptation.

### 11. What future work naturally follows?
Richer memory representations than raw observation-action chunks, explicit object- or affordance-level memory, mechanisms for forgetting stale successes, uncertainty-aware retrieval over multiple behavioral modes, and combining this kind of deployment memory with explicit world-state or task-state models.

### 12. Why does this matter for cabbageland?
It matters because it is a clean example of memory doing real work at the correct interface. The memory is not there for vibes or narrative explanation. It directly constrains the generative policy in deployment. That is aligned with cabbageland taste: use explicit stored structure when it changes action in a legible way.

### 13. What ideas are steal-worthy?
Treat repeated deployment as a distinct regime from zero-shot evaluation. Reuse successful local behavior as a soft prior rather than a hard policy override. Filter retrievals for trajectory consistency before aggregation. Inject retrieval guidance into the generative process itself instead of only ranking outputs afterward.

### 14. Final decision
Keep. This is not the final answer to robotic memory, but it is a solid mechanism paper with a sane deployment model and a transferable idea about how successful experience should bias future generation.