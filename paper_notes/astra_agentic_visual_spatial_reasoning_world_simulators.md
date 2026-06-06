# Thinking with Imagination: Agentic Visual Spatial Reasoning with World Simulators

## Basic info

* Title: Thinking with Imagination: Agentic Visual Spatial Reasoning with World Simulators
* Authors: Chenming Zhu, Jingli Lin, Yilin Long, Peizhou Cao, Tai Wang, Jiangmiao Pang, and Xihui Liu
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.06476
* Date surfaced: 2026-06-06
* Why selected in one sentence: It treats a world simulator as an action-conditioned evidence tool for spatial reasoning, then shows that both simulator consistency and learned selective use matter.

## Quick verdict

**Highly relevant**

This is a strong world-model reasoning paper because it refuses the lazy version of "just generate another image." I inspected the arXiv PDF, including the problem formulation, simulator training, RL curriculum, main results, ablations, and limitations. Confidence is high on the mechanism and caveats, but I did not audit the generated-view examples one by one.

## One-paragraph overview

Astra reframes visual spatial reasoning as interactive evidence acquisition. A VLM can answer directly or invoke a world simulator with a camera-motion query, receive an imagined novel-view observation, and continue reasoning over observed plus imagined evidence. The system has two learned parts: Astra-WM, a Bagel-based world simulator fine-tuned with view consistency tuning, and Astra-VL, a Qwen3-VL-based policy trained with a two-phase simulator-in-the-loop RL curriculum. The paper's useful result is that simulator access alone is not enough. Off-the-shelf image generation is spatially unreliable, forced simulator use can hurt object and region relations, and a policy must learn when, where, and how to imagine.

## Model definition

### Inputs

The reasoning task provides a spatial question and one or more context images. At each turn, the policy sees the trajectory so far: the question, original images, prior reasoning, simulator actions, and generated observations.

### Outputs

The policy either answers the question or issues an Invoke action specifying a reference image and camera-motion query. The simulator returns an imagined novel-view observation plus motion provenance.

### Training objective (loss)

Astra-WM is fine-tuned on quality-verified world-simulator SFT data for action-conditioned novel-view generation. Astra-VL is trained with GRPO in two phases: first, an exploration phase with answer, format, and capped simulator-use rewards; second, a selective-imagination phase that rewards simulator use when it improves over a direct-answer baseline and penalizes harmful simulator use.

### Architecture / parameterization

Astra-WM is a Bagel-based world simulator conditioned on context images and natural-language camera-motion instructions. Astra-VL is initialized from Qwen3-VL-8B and trained as an agentic policy that can invoke the simulator or answer.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

VLMs often struggle when spatial questions require unobserved layout, alternative viewpoints, or cross-view consistency. Text-only chain-of-thought does not create missing visual evidence, and static visual context can leave the relevant spatial relation ambiguous.

### 2. What is the method?

- Train a world simulator to generate novel views from camera-motion queries.
- Give the VLM an action space with two high-level actions: Invoke simulator or Answer.
- Include motion provenance so generated views are not confused with original observations.
- Train the VLM policy in two RL phases: first to keep valid tool use alive, then to use the simulator selectively when it helps more than direct answering.

### 3. What is the method motivation?

The paper's real motivation is that imagination should be governed. A generated view is useful only if it is spatially consistent and if the policy knows when the added evidence is worth the noise.

### 4. What data does it use?

The simulator SFT data is constructed from ARKitScenes, DL3DV, and ScanNet++ according to the appendix. The RL data is a Spatial QA corpus focused on questions where direct answering is difficult. Evaluation uses MMSI-Bench and MindCube.

### 5. How is it evaluated?

The paper evaluates spatial reasoning accuracy under direct answer, forced tool use, and agentic tool use. It also reports simulator-quality measures for pose consistency and content consistency, and ablates view consistency tuning, RL reward design, and inference-time workflow mode.

### 6. What are the main results?

Astra-WM improves simulator-augmented Gemini-3-Flash on MMSI-Bench from 45.1 to 49.5 in the abstract-reported result. The full Astra framework improves the Qwen3-VL backbone from 29.8 to 38.8 on MMSI-Bench and from 36.8 to 42.7 on MindCube. The inference workflow ablation shows forced tool use helps camera-centric relations but hurts some object and region relations, while agentic tool use gives the best overall balance.

### 7. What is actually novel?

The novelty is not just using generated images. It is the combination of a camera-action-conditioned simulator, consistency training for generated evidence, and a learned policy for selective simulator invocation.

### 8. What are the strengths?

- Good framing: world model as evidence tool, not just video generator.
- The ablations test the core claim: simulator quality, reward design, and inference-time control all matter.
- The paper explicitly shows that forced imagination can hurt.
- Motion provenance in the trajectory is a small but important interface detail.

### 9. What are the weaknesses, limitations, or red flags?

- The simulator can still produce plausible but wrong or unhelpful views.
- The policy can overuse the simulator, collapse to direct answers, confuse image indices, over-trust generated observations, or stop exploring too early.
- The reward is based on exact-match differences, which is sparse and may miss partially useful observations.
- The benchmarks are spatial reasoning benchmarks, not physical robot deployment.

### 10. What challenges or open problems remain?

The hard problem is knowing when imagined evidence is trustworthy. A future system needs a verifier or uncertainty layer that can judge whether a generated observation is spatially consistent enough to act on.

### 11. What future work naturally follows?

- Train simulator actions around expected information gain.
- Add explicit verification after each generated observation.
- Contrast helpful and harmful simulator calls with preference data.
- Extend the interface from camera motion to richer embodied actions and map updates.

### 12. Why does this matter for cabbageland?

Because it gives world models a useful role in reasoning: acquire missing evidence under an action query, then let the policy decide whether that evidence should enter the reasoning trace. That is much better than treating generation as decorative visual scratch paper.

### 13. What ideas are steal-worthy?

- Treat imagined observations as tool outputs with provenance.
- Evaluate generated worlds by consistency and downstream utility, not only visual quality.
- Train the policy to govern imagination, not merely to have access to it.
- Use a two-phase curriculum to avoid both tool-use collapse and tool-use addiction.

### 14. Final decision

**Worth keeping.** Astra is not a solved spatial-reasoning system, but it is a good interface paper: world models become more useful when they are queried, verified, and selectively admitted into the reasoning loop.
