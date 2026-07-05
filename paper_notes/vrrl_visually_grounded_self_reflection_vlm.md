# Visually Grounded Self-Reflection for Vision-Language Models via Reinforcement Learning

## Basic info

* Title: Visually Grounded Self-Reflection for Vision-Language Models via Reinforcement Learning
* Authors: Liyan Tang, Fangcong Yin, Greg Durrett
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.02490
* Date surfaced: 2026-07-05
* Why selected in one sentence: It trains VLMs to recover from visual-feedback mistakes instead of mistaking reflective text for grounded self-correction.

## Quick verdict

* Highly relevant

This is a strong multimodal-agent training paper. I inspected the full arXiv HTML, including the problem setup, VRRL method, visual grounding results, spatial navigation results, and ablation framing. The key contribution is a good training interface for recovery: random turn masking plus buffered roll-ins from past mistake prefixes.

## One-paragraph overview

The paper studies vision-language models in multi-turn visual feedback settings. A model predicts a visual answer, receives feedback such as a marked point or environment state, and then has to revise its next action. Off-the-shelf VLMs and reflection-tuned baselines often fail here: they repeat bad guesses or produce reflective-looking language without actually using the image feedback. VRRL first teaches the interaction format with supervised fine-tuning, then applies reinforcement learning that deliberately emphasizes recovery from bad intermediate states. Random Turn Masking computes policy updates only on suffixes of rollouts, while Buffered Roll-In starts new rollouts from stored failure prefixes. This pushes the model toward grounded repair rather than clean first-pass imitation.

## Model definition

### Inputs
The model receives an image, a natural-language instruction, and in multi-turn settings visual feedback from previous predictions or actions. In the visual grounding task, feedback includes prior coordinate predictions rendered back into the image. In spatial navigation, the model sees visual state feedback from grid-like environments.

### Outputs
It outputs visual grounding coordinates, navigation actions, stopping decisions, and intermediate reflective responses depending on the task. The important behavioral output is not only the final answer but the sequence of corrections across turns.

### Training objective (loss)
Training has two stages. Stage one uses supervised fine-tuning to teach the multi-turn interaction format. Stage two uses reinforcement learning, described as GRPO-style in the accessible method details, with task success rewards and reflection reward shaping. VRRL modifies the RL update with Random Turn Masking and Buffered Roll-In so gradients focus on recovering from suffix states and replayed mistake prefixes.

### Architecture / parameterization
The experiments use Qwen2.5-VL 3B / 7B and Qwen3-VL-4B style vision-language backbones in the accessible result tables. VRRL is a post-training recipe on top of those LVLMs rather than a new visual encoder architecture.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Vision-language models can generate chains of thought, but they often do not perform visually grounded self-correction. When visual feedback reveals a mistake, the model may ignore the evidence, repeat the same answer, or revise text without improving the visual action.

### 2. What is the method?
VRRL trains multi-turn visual recovery. Random Turn Masking masks out prefix losses so the model is optimized on continuation / recovery behavior rather than blamed for every earlier trajectory choice. Buffered Roll-In samples historical mistake prefixes from a replay buffer and asks the model to continue from those states. Together, these expose the model to diverse bad states it must learn to repair.

### 3. What is the method motivation?
Self-reflection is only useful if it changes behavior in response to evidence. A model trained mostly on clean traces can learn the format of reflection without learning what to do after an error. Training from bad prefixes creates the actual recovery distribution.

### 4. What data does it use?
The paper uses synthetic visual grounding tasks involving tables and charts, plus spatial navigation tasks based on grid-like visual environments. The visual grounding setup includes in-distribution small table localization and OOD splits such as larger tables, cell queries, bar charts, and scatter plots.

### 5. How is it evaluated?
It evaluates in-distribution and out-of-distribution accuracy, comparing zero-shot single-turn and multi-turn prompting, VL-Rethinker baselines, supervised fine-tuning, reflection tuning, standard GRPO variants, and VRRL. It also reports turn behavior to show whether models actually refine predictions across turns.

### 6. What are the main results?
On visual grounding, Qwen2.5-VL-7B with VRRL reports a 78.4 OOD average, above Multi-SFT to GRPO at 73.2 and Reflection Tuning at 55.6. For the 3B model, VRRL reports 45.7 OOD average versus 40.0 for Multi-SFT to GRPO. On spatial navigation, Qwen3-VL-4B VRRL reports 52.2 OOD average versus 40.8 for Multi-SFT and 38.4 for Reflection Tuning. The paper also argues that prompting alone does not elicit reliable correction and often leads to repeated predictions.

### 7. What is actually novel?
The novelty is the recovery-oriented RL recipe. Random Turn Masking and Buffered Roll-In are simple but pointed: they train the model on the distribution where reflection matters, namely after something has already gone wrong.

### 8. What are the strengths?
The paper tests a real failure mode in multimodal agents. It distinguishes reflective language from grounded corrective behavior and uses OOD visual tasks where simple memorization of the training layout is insufficient. The turn-level analysis is also useful because it checks whether additional turns improve behavior rather than just adding text.

### 9. What are the weaknesses, limitations, or red flags?
The tasks are still controlled synthetic environments. Tables, charts, and grid navigation are useful, but they are cleaner than real browser, robotics, medical, or interactive design settings. The method also assumes an environment can provide visual feedback in a structured loop. That is true for some agents, not all.

### 10. What challenges or open problems remain?
The next challenge is scaling this recovery training to messier action spaces where feedback is partial, delayed, or ambiguous. Another open problem is distinguishing genuine visual evidence use from learned correction heuristics under richer scene distributions.

### 11. What future work naturally follows?
Apply recovery-state training to GUI agents, browser agents, diagram editing, visual coding assistants, medical image review, and embodied simulators. Also test whether replay buffers of human-corrected failures produce stronger recovery than model-generated mistake prefixes alone.

### 12. Why does this matter for cabbageland?
OpenClaw-style agents live in loops. They click, inspect, revise, and try again. VRRL is a reminder that "reflection" should mean recovery from state, not decorative introspection. If an agent gets feedback, the training and evaluation should care about whether that feedback changes the next action.

### 13. What ideas are steal-worthy?
Train on bad intermediate states, not just successful demonstrations. Use replay buffers of failures as curriculum. Mask prefix losses when the learning target is suffix recovery. Evaluate turn-by-turn correction rather than final answer alone.

### 14. Final decision
Keep as highly relevant. The evidence is controlled, but the mechanism is exactly the right shape for grounded multimodal agents.
