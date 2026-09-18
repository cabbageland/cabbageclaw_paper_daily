# Score Centering Stabilizes Off-policy Reinforcement Learning

## Basic info

* Title: Score Centering Stabilizes Off-policy Reinforcement Learning
* Authors: Martin Marek, Max Ryabinin
* Year: 2026
* Venue / source: arXiv:2609.20807
* Link: https://arxiv.org/abs/2609.20807
* Date surfaced: 2026-09-18
* Why selected in one sentence: It gives a concrete drift mechanism for LLM RL collapse under training-inference mismatch and a simple additive correction.

## Quick verdict

* Highly relevant

This is a strong RL/post-training paper because the explanation is clean and the correction is minimal. The experiments deliberately amplify mismatch, but the mechanism is transferable. This note is based on the full arXiv PDF text.

## One-paragraph overview

The paper studies training-inference mismatch in LLM reinforcement learning, where the sampler and trainer differ because of quantization, staleness, or numerical mismatch. It shows that under mismatch, the policy-gradient update decomposes into a reward covariance term plus a drift term. The drift term does not encode reward signal; it distills the trainer toward the sampler. Since the sampler is a biased copy of the trainer and is periodically synced, the bias compounds. Score centering subtracts the expected score under the sampler, cancelling drift while composing with importance-sampling corrections.

## Model definition

### Inputs

The method uses sampled rollouts, rewards or advantages, trainer log probabilities/scores, and sampler next-token distributions or top-k log probabilities. Experiments train Qwen3 models on Countdown and INTELLECT-2 math settings.

### Outputs

The training update outputs corrected policy-gradient losses. In practice the method outputs an additive score-centering correction term that can be expressed as a scalar loss.

### Training objective (loss)

The shared base objective is REINFORCE with group-centered rewards. Score centering modifies the gradient by subtracting the expected score under the sampler. Approximate score centering uses top-k sampler log probabilities when the full distribution is unavailable.

### Architecture / parameterization

The method is architecture-agnostic. Experiments use Qwen3-0.6B-Instruct, Qwen3-1.7B, and Qwen3-30B-A3B-Base, including quantized sampler and stale sampler settings.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

LLM RL can be unstable when the sampler used for rollouts differs from the trainer used for gradients. Fully eliminating mismatch is expensive, and standard importance-ratio approaches do not cover every mismatch mode well.

### 2. What is the method?

Derive the expected off-policy policy-gradient update as drift plus signal. Then subtract the sampler-expected score so the drift term vanishes. The correction can be used alone or composed with truncated or masked importance sampling.

### 3. What is the method motivation?

With a constant reward, on-policy policy gradient should produce no update. Under mismatch, the expected gradient is nonzero because tokens are sampled from q while scores are computed under p. That nonzero term is a pure artifact.

### 4. What data does it use?

Experiments use Countdown for smaller Qwen3 models and the math subset of INTELLECT-2 for Qwen3-30B-A3B.

### 5. How is it evaluated?

The paper tests synthetic sampler weight noise, int8 sampler quantization, severe sampler staleness, and 30B quantization. It compares policy gradient, naive importance sampling, TIS, MIS, PPO, DAPO, DPPO, GSPO, TOPR, score centering, and compositions.

### 6. What are the main results?

Under severe synthetic weight noise, only score centering and its compositions with TIS or MIS train stably. Under int8 sampler mismatch, score centering variants perform best. Under staleness, score centering composed with TIS or MIS dominates. At 30B, when KV cache quantization becomes severe, score centering remains stable while vanilla policy gradient and several ratio-based methods collapse or end near zero.

### 7. What is actually novel?

The novelty is isolating drift as an additive off-policy policy-gradient artifact and cancelling it directly. The paper also shows that a top-k approximation is enough in its experiments.

### 8. What are the strengths?

The derivation is intuitive and useful. The correction has no new hyperparameter. The paper tests multiple mismatch types and explains why importance sampling helps staleness more than quantization.

### 9. What are the weaknesses, limitations, or red flags?

The headline experiments intentionally use severe mismatch to separate methods quickly. Under mild mismatch, methods can overlap for long runs. Score centering cancels drift measured under the sampler; under severe staleness, it still benefits from importance sampling to better align the sampling distribution.

### 10. What challenges or open problems remain?

The next question is how much this matters in long, realistic production RL runs with milder but persistent mismatch. Another open problem is replaying or correcting expert routing in mixture-of-experts settings.

### 11. What future work naturally follows?

Integrate score centering into practical RLHF/RLAIF stacks, test across longer horizons and richer reward models, and compare compute cost against tighter trainer/sampler numerical matching.

### 12. Why does this matter for cabbageland?

Cabbageland cares about making training dynamics legible. This paper turns "RL is fragile under mismatch" into a specific drift term that can be measured and removed.

### 13. What ideas are steal-worthy?

When a training loop has teacher/student or sampler/trainer copies, look for compounding self-distillation drift. Separate covariance signal from distribution-shift bias. Prefer additive correction when the artifact is additive.

### 14. Final decision

Preserve. This is a compact mechanism paper with practical post-training implications.
