# Learning on the Job: Continual Learning from Deployment Feedback for Frozen-Weights Agents

## Basic info

* Title: Learning on the Job: Continual Learning from Deployment Feedback for Frozen-Weights Agents
* Authors: Valentin Tablan, Scott Taylor, Kristoffer Bernhem
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.22157
* Date surfaced: 2026-07-27
* Why selected in one sentence: It shows that ordinary deployment feedback can become durable agent capability without touching model weights if the system writes reusable rules into external memory.

## Quick verdict

**Highly relevant**

This is a clean and useful frozen-agent learning paper because it measures learning between trials rather than hiding behind static evaluation. The paper uses post-episode feedback to write natural-language rules into shared memory, then shows that the resulting store helps both the original model and a different model. I inspected the arXiv HTML sections covering the setup, Spark memory system, continual-learning experiment, cross-model transfer experiment, discussion, and conclusion.

## One-paragraph overview

The paper starts from a practical complaint: deployed agents encounter the same kinds of problems repeatedly, but frozen-weight systems throw away almost all of that experience. The authors pair a frozen agent with Spark, an external memory service that writes validated natural-language rules after each episode based on either a one-bit outcome verdict or an after-the-fact correction. Future episodes can retrieve those rules when similar situations appear. On `tau`-bench banking, this turns deployment feedback into real between-trial improvement without any weight update. The extra result is organizational rather than personal: the learned store transfers across models, so one agent's experience can become another agent's starting knowledge.

## Model definition

### Inputs
The system takes a frozen base model, tool-agent interaction episodes, post-episode outcome feedback or corrected instructions, and a shared memory domain containing natural-language rules keyed to situations.

### Outputs
It outputs updated rule memory plus future agent behavior conditioned on retrieved rules from that memory.

### Training objective (loss)
There is no parameter update to the model weights. The contribution is an external memory acquisition and retrieval pipeline that converts feedback into reusable rules.

### Architecture / parameterization
The main artifact is the Spark shared memory system. Episodes can write rules into a memory domain, the agent sees memory tools and reminders through the harness prompt, and later runs retrieve rules relevant to the live situation.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to solve the wastefulness of deployed agents that repeatedly face similar tasks but start every new episode with no durable lesson from prior failures or corrections.

### 2. What is the method?
The method is to distill post-episode feedback into natural-language WHEN-THEN style rules stored in external memory, then retrieve those rules in later episodes.

### 3. What is the method motivation?
The motivation is that many deployment settings produce useful feedback already, but frozen agents cannot internalize it, so capability improvements should come from memory rather than from weight updates.

### 4. What data does it use?
The experiments use the banking domain of `tau`-bench with `97` tasks and four trials per task, plus a cross-model transfer setup between Mistral Large and Claude Sonnet 5.

### 5. How is it evaluated?
It is evaluated with no-memory, experience-memory, and instruction-memory conditions, using `pass^k`, solved-task counts, hold rates, floor-stratum conversions, per-trial learning curves, and read-only transfer from one model's frozen store to another.

### 6. What are the main results?
On Mistral Large, instruction memory raises `pass^1` from `0.064` to `0.170`, lifts solved tasks from `13/97` to `32/97`, and converts `22` of the `84` tasks the baseline never solves. Experience memory reaches `0.103` `pass^1` with a higher `0.88` hold rate. On Claude Sonnet 5, instruction raises `pass^1` from `0.248` to `0.397` and solved tasks from `40/97` to `62/97`. In cross-model transfer, Mistral Large reading the Sonnet-built store reaches `0.289` `pass^1`, and Sonnet reading the Mistral-built store reaches `0.314`.

### 7. What is actually novel?
The novelty is not "use RAG." It is the demonstration that frozen-weight agents can learn continually from deployment feedback through externalized rules, and that the acquired store can transfer uphill as well as downhill across different models.

### 8. What are the strengths?
The paper is strong on experimental structure. It separates acquisition from retention, exposes the weird blindness of `pass^4` for learning-by-later-trial conversion, and shows that the learned memory is not just a single-model answer cache because it transfers across models.

### 9. What are the weaknesses, limitations, or red flags?
The evidence is still one domain with reliable evaluator feedback. Conditions are single runs rather than repeated end-to-end runs, the experience arm is only measured on Mistral Large, and the study does not test generalization to unseen task families.

### 10. What challenges or open problems remain?
The next problems are noisy or delayed feedback, broader domains, cross-task transfer where lessons generalize more abstractly, and autonomous curation of the memory store over long horizons.

### 11. What future work naturally follows?
Run the same protocol in noisier deployment settings, compare different rule-writing and validation strategies, and study how shared organizational memory should be curated when many agents write into it.

### 12. Why does this matter for cabbageland?
Cabbageland cares about agents that accumulate usable experience without pretending weight updates are the only path to learning. This paper gives a direct recipe for learning through memory instead of through retraining.

### 13. What ideas are steal-worthy?
Distill feedback into situation-keyed rules. Separate acquisition metrics from retention metrics. Share the store across model families. Treat memory as an organizational asset, not just a personal scratchpad.

### 14. Final decision
**Keep it.** This is direct, actionable, and much more interesting than another paper claiming a frozen agent is "continually learning" because its context window got longer.
