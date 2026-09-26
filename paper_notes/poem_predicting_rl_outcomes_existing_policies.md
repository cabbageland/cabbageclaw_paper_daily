# PoEM: Predicting RL Outcomes from Existing Policies

## Basic info

* Title: PoEM: Predicting RL Outcomes from Existing Policies
* Authors: Kimia Hamidieh, Giannis Daras, Antonio Torralba
* Year: 2026
* Venue / source: arXiv:2609.30226
* Link: https://arxiv.org/abs/2609.30226
* Date surfaced: 2026-09-26
* Why selected in one sentence: It reframes reward adaptation as composition in log-policy space and gives a coverage diagnostic for when old RL policies can approximate a new reward.

## Quick verdict

* Highly relevant

PoEM is worth keeping because the central claim is geometric rather than merely heuristic adapter mixing. The paper shows that post-trained policies can have nearly orthogonal parameter updates while their log-ratios span a much lower-rank behavioral space. The caveat is that the evidence is still on small language models, public reward-model adapters, and Stable Diffusion v1.4 LoRAs.

## One-paragraph overview

PoEM asks whether the policy produced by RL on a new reward can be approximated without running RL again. Under KL-regularized RL, if the target reward is a linear combination of rewards used to train existing policies, the optimal target policy is a weighted log-mixture of the reference policy and those existing policies. The paper then relaxes the reward-linearity assumption empirically: trained adapters may occupy a low-rank space in log-policy ratios, so a held-out reward can be reachable if its desired policy direction lies in that span. PoEM fits composition weights from a small calibration set scored by the target reward, checks a coverage score, and composes the existing policies at inference time.

## Model definition

### Inputs

PoEM receives a reference policy, a set of policies or adapters post-trained on existing rewards, and a calibration set of prompts/responses scored by the new target reward. It can use either basis reward scores or basis policy log-ratios.

### Outputs

It outputs an inference-time composed policy: a weighted product/log-mixture of the reference and basis policies. For diffusion models, the analogous composition mixes adapted denoisers with step-specific weights.

### Training objective (loss)

PoEM itself performs no new RL training. It estimates weights by least-squares or non-negative least-squares regression on centered target rewards or policy log-ratios. The basis policies are trained separately with GRPO, DPO, PPO, or DDPO depending on the experiment.

### Architecture / parameterization

The method is not a new model architecture. It is a policy-composition procedure over existing adapters or policies, parameterized by learned scalar mixture weights and a decoding strength.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It tries to avoid rerunning expensive and unstable RL every time a reward changes, especially when one wants to preview, combine, or approximate reward models.

### 2. What is the method?

PoEM evaluates basis policies on calibration samples, regresses the target reward against centered basis rewards or log-ratios, checks whether the target is covered by the basis, and composes the policies at inference time.

### 3. What is the method motivation?

KL-regularized RL has a closed-form exponential tilt. That means reward addition corresponds to log-policy addition in the ideal case. The empirical bet is that post-trained policies occupy reusable behavioral directions even when the rewards are not literally linear combinations.

### 4. What data does it use?

The paper uses Qwen3-0.6B LoRA adapters trained on 20 programmatic text rewards with GRPO or DPO, PPO adapters trained on public reward models, and 13 Stable Diffusion v1.4 LoRA experts trained with DDPO on image rewards.

### 5. How is it evaluated?

It compares composed policies to directly RL-trained target policies on combined rewards and held-out rewards. Metrics include recovered reward gain, KL to the target policy, coverage score, rank correlation between coverage and error, and qualitative image effects.

### 6. What are the main results?

On combined rewards, PoEM recovers much of the direct RL reward gain and is often close to a second RL run. In held-out reward tests, coverage predicts which rewards are reachable, with rank correlations between coverage and reward error around -0.71 to -0.81. Covered held-out rewards recover more of RL's gain than uncovered ones. On RM-Div, PoEM is closer to the held-out expert than the top expert on 9 of 10 rewards and recovers more reward on 8 of 10.

### 7. What is actually novel?

The useful novelty is the log-policy span view plus a pre-decoding coverage diagnostic. It is adapter composition with a theory-shaped warning label.

### 8. What are the strengths?

The paper separates reward recovery from policy similarity, includes held-out reward tests, and explicitly shows failure when coverage is low. The low-rank log-ratio observation is more interesting than the raw composition recipe.

### 9. What are the weaknesses, limitations, or red flags?

The scale is modest. A composed policy can match reward without matching behavior, especially for offline DPO experts. Inference over many experts is expensive, and low coverage means PoEM has no magic. The method inherits reward-model errors and can only reuse directions already present in the basis.

### 10. What challenges or open problems remain?

Open problems include building diverse expert bases, distilling the mixture into one model, starting RL from PoEM, and testing whether the low-rank policy-space structure persists in larger frontier-scale post-training.

### 11. What future work naturally follows?

A practical next step is coverage-driven expert collection: train the next expert on rewards the current basis cannot span. Another is to use PoEM as a cheap reward preview before expensive RLHF/RLAIF.

### 12. Why does this matter for cabbageland?

Cabbageland cares about reusable abstractions and avoiding repeated expensive loops. PoEM says old post-training runs may contain reusable policy directions, but only when coverage says the new objective lives in their span.

### 13. What ideas are steal-worthy?

Analyze adapters in log-policy space, not just parameter space. Fit reward directions from small calibration sets. Use coverage as a distrust signal before spending compute. Treat RL outcomes as composable only when the behavioral direction is covered.

### 14. Final decision

Preserve. The paper is not a universal RL replacement, but the policy-space framing is useful.
