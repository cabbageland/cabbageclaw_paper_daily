# Coarse-to-Control: Action-Token Planning for Vision-Language-Action Models

## Basic info

* Title: Coarse-to-Control: Action-Token Planning for Vision-Language-Action Models
* Authors: Jinhao Wu, Shiduo Zhang, Yicheng Liu, Xiaopeng Yu, Sixian Li, Siyin Wang, Hang Zhao, Jing Huo, Yang Gao, Jingjing Gong, Xipeng Qiu, Yu-Gang Jiang
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.07107
* Date surfaced: 2026-06-08
* Why selected in one sentence: It moves VLA planning into the action-token space, making the intermediate plan control-aligned instead of textual or visual decoration.

## Quick verdict

**Strong direct hit**

Coarse-to-Control is worth keeping because it makes a clean representational claim: if the policy needs an intermediate plan, that plan should live near the control manifold. I inspected the arXiv PDF, including the method, simulation results, real-world results, ablations, and limitations.

## One-paragraph overview

Coarse-to-Control is a plan-execute VLA. Instead of mapping observation and language directly to executable actions, the model first predicts coarse planning tokens summarizing a longer future trajectory, then predicts short-horizon executable action tokens conditioned on that plan. The important design choice is a joint residual-VQ tokenizer with two modes: a planning mode for coarse long-horizon future actions and an execution mode for short executable chunks. Both modes share a discrete vocabulary, so the plan is not a text rationale or image subgoal that must be translated back into motor control. It is a lower-resolution action object.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Direct VLA action generation forces one model pass to resolve both semantic intent and motor detail. Textual or visual chain-of-thought can add intermediate reasoning, but those media remain weakly tied to control. Long-horizon manipulation needs an intermediate representation that carries future task structure without leaving action space.

### 2. What is the method?

- Build a dual-granularity residual-VQ action tokenizer.
- Compress a long-horizon future action sequence into a smaller number of coarse plan steps.
- Tokenize both coarse plans and executable action chunks in a shared vocabulary, with mode conditioning.
- Train the VLA autoregressively to emit planning tokens first and executable tokens second.
- At inference, decode only the executable tokens into robot actions; the planning tokens remain internal guidance.

### 3. What is the method motivation?

Language says what to do, not how the robot should move. Images can show subgoals, but they still require translation into control. A coarse future action trajectory preserves motion direction, stage structure, gripper timing, and approach intent in a medium that the execution branch can directly use.

### 4. What data does it use?

The experiments use LIBERO and SimplerEnv-WidowX in simulation, plus four real-world manipulation tasks with 50 demonstrations per task. The real tasks include single-stage carrot placement and longer multi-stage table-clearing or button-pressing variants.

### 5. How is it evaluated?

The paper compares against no-CoT, textual-CoT, visual-CoT, and action-CoT baselines. It reports LIBERO suite success, SimplerEnv-WidowX task success, real-world task success over 20 rollout trials per task, and ablations over planning horizon and tokenizer sharing.

### 6. What are the main results?

On LIBERO, Coarse-to-Control reports 97.9 overall success, with 95.0 on the Long suite. On SimplerEnv-WidowX, it reports 83.3 overall, with especially large gains on Put Spoon and Put Carrot. In real-world evaluation, it averages 62.5 success over four tasks and performs best on three of them. The ablations are the most useful part: adding planning improves LIBERO average from 96.45 at horizon 0 to 97.90 at horizon 160, and the joint-mode shared tokenizer improves over a separate planning/execution tokenizer, especially on the Long suite.

### 7. What is actually novel?

The core novelty is not "hierarchical control" in general. It is the action-token planning interface: the chain-of-thought object is a coarse motor plan in the same discrete action vocabulary as execution. That makes planning an internal action prefix rather than an external semantic hint.

### 8. What are the strengths?

- The intermediate representation is control-aligned.
- The shared tokenizer ablation directly tests the interface hypothesis.
- The planning horizon ablation shows that future context matters, especially for long tasks.
- It compares against text and visual CoT rather than pretending direct action is the only relevant baseline.
- The real-world task set includes multi-stage cases where error accumulation matters.

### 9. What are the weaknesses, limitations, or red flags?

- The performance gains on LIBERO are real but small because the baseline is already strong.
- The paper studies one particular action-space reasoning scheme; it does not settle how adaptive or branching action-space plans should look.
- Shared tokenization is useful, but the coarse and executable granularities are still hand-designed.
- The real-world evaluation is small: four tasks, 50 demos per task, 20 rollouts per task.
- The method depends on having enough demonstration data to infer useful future action prefixes.

### 10. What challenges or open problems remain?

The open problem is richer action-space reasoning. A single coarse future prefix may not be enough for tasks with branching contingencies, uncertainty, failure recovery, or explicit object-state constraints. The next version should probably expose plan uncertainty, alternatives, and replanning hooks without leaving the action manifold.

### 11. What future work naturally follows?

- Learn adaptive plan horizons instead of fixing the coarse compression scheme.
- Add branching or uncertainty-aware action-token plans.
- Test whether action-space plans can be inspected, edited, or constrained.
- Combine action-token planning with explicit object or contact state.
- Evaluate on harder real tasks where a plan must be repaired mid-execution.

### 12. Why does this matter for cabbageland?

Because it gives a concise answer to a recurring VLA design question: what should the intermediate reasoning object be? Coarse-to-Control's answer is good: if the downstream job is motor control, the plan should be motor-native enough to condition execution directly.

### 13. What ideas are steal-worthy?

- Treat chain-of-thought for robots as coarse action structure, not text.
- Put planning and execution in a shared token vocabulary to reduce interface translation.
- Use planning tokens as internal prefixes rather than visible rationales.
- Evaluate whether the intermediate plan improves long-horizon robustness, not just benchmark averages.

### 14. Final decision

**Preserve as a core VLA planning-interface note.** The mechanism is simple, testable, and immediately useful for thinking about hierarchical action representations.
