# Evidence-State Rewards for Long-Context Reasoning

## Basic info

* Title: Evidence-State Rewards for Long-Context Reasoning
* Authors: Ya Gao and Pekka Marttinen
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.02073
* Date surfaced: 2026-07-03
* Why selected in one sentence: It turns long-context reasoning from answer-only RL into explicit optimization over evidence-state transitions.

## Quick verdict

**Must read**

This is the most directly useful paper in today's scan. I inspected the full arXiv HTML / PDF, especially the evidence-state definition, add / link / drop reward construction, GRPO integration, datasets, baselines, and ablations. The caveat is that the method assumes a parseable evidence-action format and a useful frozen verifier; open-ended agent traces will need sturdier state extraction.

## One-paragraph overview

Maven studies long-context reasoning where the model must locate, revise, connect, and discard evidence across long inputs. Instead of rewarding only the final answer or asking for static evidence extraction, Maven gives the model an editable evidence memory and rewards the state transitions that make that memory more answer-supportive. Add actions are credited for marginal gain and hindsight contribution, link actions for evidence synergy, drop actions for removing misleading context, and answer actions for final support. These span-level rewards are inserted into GRPO so the model learns not only to answer, but to manage the evidence state that makes answering possible.

## Model definition

### Inputs

Inputs are long-context questions with distributed evidence, candidate evidence states, structured action traces containing add / link / drop / answer operations, and a frozen verifier or answer model used to estimate answer-conditioned evidence-state value.

### Outputs

The trained model emits reasoning traces that build and edit an evidence memory before producing an answer. The training signal assigns token-span rewards to the actions that changed the evidence state.

### Training objective (loss)

The main optimization is GRPO with action-level rewards derived from evidence-state value changes. The reward is not just correctness at the end; it credits or penalizes state transitions according to their contribution to answer support.

### Architecture / parameterization

Maven is a reinforcement-learning framework for LLMs rather than a new backbone. The architecture around the model is an editable evidence memory plus reward functions for add, link, drop, and answer actions.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Long-context reasoning is usually trained with sparse outcome reward or with static supervision for evidence identification. Both miss the actual process: a model must build, revise, and curate a working evidence state as it reads. Rewarding only the final answer gives no local signal about whether a retrieved sentence helped, whether two facts should be linked, or whether a distractor should be dropped.

### 2. What is the method?

The method defines an editable evidence memory and an answer-conditioned value for that memory. The model's trace is segmented into actions. Add actions are rewarded by marginal improvement and hindsight usefulness; link actions are rewarded when combined evidence supports the answer better than isolated snippets; drop actions are rewarded when removing a misleading item improves answer support; answer actions receive the final answer support signal. These action rewards are assigned to corresponding spans during GRPO.

### 3. What is the method motivation?

The motivation is that retrieval and reasoning are entangled. A model can retrieve a relevant-looking fact too early, fail to connect two partial facts, keep a distractor, or produce a lucky answer from a messy state. Maven tries to train the state-management behavior, not just the last token.

### 4. What data does it use?

The evaluation uses long-context reasoning benchmarks including LongBench v2, LongReason, and RULER. The experiments include Llama and Qwen backbones and compare against outcome-only RL and evidence-identification style baselines.

### 5. How is it evaluated?

The paper evaluates final task performance, evidence sufficiency, distractor retention, and ablations of the reward components. It checks whether the learned traces contain better evidence states, not only whether answer accuracy increases.

### 6. What are the main results?

Maven reports consistent improvements over outcome-only RL and evidence-identification baselines across the tested long-context benchmarks and model families. The strongest qualitative result is lower distractor retention and more sufficient evidence sets, which supports the claim that state-transition rewards are changing the evidence-management process rather than merely polishing answers.

### 7. What is actually novel?

The novel part is the action-level reward interface for editable evidence memory. Many long-context methods reward final answers or supervise retrieval lists; Maven rewards the operations that transform the evidence state on the way to the answer.

### 8. What are the strengths?

The paper's abstraction is clean. Add, link, drop, and answer are primitive enough to transfer to agent traces, retrieval-augmented generation, and tool-using workflows. The reward definitions also target real failure modes: irrelevant additions, missing synthesis, and stale distractors.

### 9. What are the weaknesses, limitations, or red flags?

The reward relies on a frozen verifier's estimate of answer support. If that verifier is brittle, overconfident, or biased toward surface overlap, the state rewards inherit those problems. The structured action grammar also makes the environment cleaner than real agent logs, where evidence can be hidden in tool output, code execution, browser state, or user corrections.

### 10. What challenges or open problems remain?

The important next challenge is applying evidence-state rewards to messy tool traces. The system needs reliable extraction of candidate facts, stable evidence IDs, support links, and reasons for dropping evidence. It also needs a verifier that can distinguish "supports the answer" from "sounds compatible with the answer."

### 11. What future work naturally follows?

A natural follow-up is an agent harness where tool outputs become evidence objects, claims must link back to those objects, and the agent receives reward for improving the evidence graph before answering or acting. Another useful direction is replacing the frozen verifier with a calibrated ensemble or a verifier trained on counterfactual evidence states.

### 12. Why does this matter for cabbageland?

Cabbageland cares about long-lived agents that read, browse, remember, and act under context pressure. Maven's key lesson is that the agent's working evidence state should be an explicit training and evaluation object. A correct answer from a bad evidence state is not good enough.

### 13. What ideas are steal-worthy?

* Promote retrieved snippets, tool outputs, and user constraints into evidence objects.
* Reward add / link / drop operations rather than only final answers.
* Penalize distractor retention as an evidence-state failure.
* Use hindsight contribution to decide whether an early addition was actually useful.
* Treat evidence sufficiency as a first-class metric for long-context agents.

### 14. Final decision

**Keep it.** This is a strong mechanism paper for long-context agent training. The implementation assumptions are cleaner than deployment, but the reward interface is exactly the right direction.
