# TRACE: Turn-level Reward Assignment via Credit Estimation for Long-Horizon Agents

## Basic info

* Title: TRACE: Turn-level Reward Assignment via Credit Estimation for Long-Horizon Agents
* Authors: Leitian Tao, Baolin Peng, Wenlin Yao, Tao Ge, Hao Cheng, Mike Hang Wang, Jianfeng Gao, Sharon Li
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.13988
* Date surfaced: 2026-07-16
* Why selected in one sentence: It offers a compact, critic-free way to assign useful credit to individual tool turns in long-horizon agent RL without needing step labels or a heavyweight judge model.

## Quick verdict

**Highly relevant**

This is a good direct paper on agentic RL because it attacks a real bottleneck rather than dressing up another search benchmark. The core contribution is a reward construction that stays anchored to final correctness while assigning denser credit at tool boundaries. I inspected the full arXiv HTML paper, including the method, training setup, main results, ablation framing, and limitations.

## One-paragraph overview

TRACE treats a tool-using rollout as a sequence of state transitions at tool-call boundaries. A frozen reference model scores how predictable the gold answer becomes after each tool interaction, converts those prefix scores into log-ratio state values, and then uses temporal-difference changes between adjacent states as local rewards. Those turn-level credits are combined with the usual outcome-level GRPO reward, so the policy still optimizes final correctness but no longer assigns the same signal to every turn in a long trajectory. The result is a critic-free dense reward recipe for deep-search agents.

## Model definition

### Inputs
During training, the policy model receives the prompt, the growing transcript, tool observations, and the available browser-style tools. The reward computation additionally uses the gold answer and a frozen reference model to score trajectory prefixes at tool boundaries.

### Outputs
The policy outputs assistant tokens, tool calls, and the final answer. TRACE additionally computes per-turn rewards from the change in answer predictability across tool-boundary states.

### Training objective (loss)
The policy is trained with GRPO-style RL using a combination of outcome-level reward and turn-level temporal-difference rewards. The dense part uses log-ratio state values from a frozen reference model rather than a learned critic or a process reward model.

### Architecture / parameterization
The experiments use Qwen3-4B-Thinking-2507 and Qwen3-30B-A3B-Thinking-2507 search agents in a browser-style harness. TRACE itself is not a new backbone; it is a reward-shaping and credit-assignment method layered onto existing agent policies.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tackles the credit-assignment problem in long-horizon agent RL, where a final success or failure signal is too sparse to tell which intermediate tool turns helped.

### 2. What is the method?
The method is turn-level temporal-difference credit on tool-boundary states. A frozen reference model scores the gold answer probability from each trajectory prefix, those scores are converted into log-ratio state values, and the per-turn reward is the change in that value across adjacent tool-boundary states.

### 3. What is the method motivation?
Outcome-only RL treats a failed but mostly useful trajectory almost the same as a useless one. The paper wants a denser signal that rewards progress without requiring human step labels, Monte Carlo critics, or a strong LLM judge.

### 4. What data does it use?
Training uses deeper synthetic search questions designed for long-horizon search behavior. Evaluation covers BrowseComp-Plus in a closed-web setting plus BrowseComp, GAIA, and xbench-DeepSearch with open-web retrieval.

### 5. How is it evaluated?
The paper compares TRACE against base models and other RL variants such as GRPO, GSPO, and GiGRPO on the same backbones, training data, browser interface, and evaluation protocol. It reports benchmark scores plus learning-curve behavior.

### 6. What are the main results?
On BrowseComp-Plus, TRACE lifts Qwen3-4B from `7.2` to `35.6` and Qwen3-30B-A3B from `8.4` to `42.6`. Across the four-benchmark average, it improves the 4B model from `29.5` under outcome-only GRPO to `34.0`, and the 30B-A3B model from `32.5` to `38.1`. The learning curves also improve earlier and converge faster than the outcome-only baselines.

### 7. What is actually novel?
The useful novelty is frozen-reference turn credit without a learned critic. The paper stays anchored to final-answer correctness while assigning local rewards at the points where agents actually interact with tools.

### 8. What are the strengths?
The controlled RL comparison is good, the method is simple enough to reuse, and the paper avoids the common trap of sneaking in a stronger judge or extra supervision and then attributing the gain to "credit assignment."

### 9. What are the weaknesses, limitations, or red flags?
The current value proxy depends on short, known answers. That is much cleaner for search than for code agents, multi-file patches, or open-ended assistants. The training data is also synthetic search rather than a broader agentic task mix.

### 10. What challenges or open problems remain?
The main open question is how to construct equally reliable progress signals for longer, structured, or underspecified outputs where gold-answer log-probability is a bad stand-in for state value.

### 11. What future work naturally follows?
Natural follow-ups include code-agent versions with execution-based progress signals, decomposed subgoal reward construction, and tests on richer tool environments where the final output is not a short answer string.

### 12. Why does this matter for cabbageland?
If cabbageland wants agents that learn from interaction traces rather than just from final task labels, this is exactly the kind of compact mechanism worth remembering. It is a plausible building block for long-horizon tool-use training without a giant supervision stack.

### 13. What ideas are steal-worthy?
Compute credit at tool boundaries rather than token boundaries. Use a frozen model as a stable value probe instead of training a critic. Combine final-outcome reward with local progress reward so dense credit does not drift away from the real objective.

### 14. Final decision
**Keep it.** The scope is narrower than the title sounds, but the reward-construction idea is genuinely worth preserving.
