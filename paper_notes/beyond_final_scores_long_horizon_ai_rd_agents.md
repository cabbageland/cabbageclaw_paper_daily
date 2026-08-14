# Beyond Final Scores: A Systematic Evaluation of Agents for Long-Horizon AI Research and Development

## Basic info

* Title: Beyond Final Scores: A Systematic Evaluation of Agents for Long-Horizon AI Research and Development
* Authors: Yiwei Li, Wanli Yang, Hexiang Tan, Xiangzhou Huang, Zhengyu Chen, Ziran Li, Borun Chen, Shanglin Lei, Huaisheng Zhu, Hao Tian, Fei Sun, Xunliang Cai, Jingang Wang
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.13417
* Date surfaced: 2026-08-14
* Why selected in one sentence: It evaluates long-horizon AI R&D agents at the process level instead of pretending that a final leaderboard score explains where research capability actually lives.

## Quick verdict

* Highly relevant

I inspected the arXiv HTML full text. This is a strong evaluation paper because it adds a usable process vocabulary to long-horizon agent assessment and backs it with controlled experience and harness comparisons.

## One-paragraph overview

The paper evaluates seven frontier agents on 36 long-horizon AI R&D tasks from AutoLab and asks four questions instead of one: how strong are the final results, where is progress gained or lost inside the run, does accumulated experience help later decisions, and how much does the harness matter? To answer the process question, it decomposes behavior into Solution Framing, Execution, and Feedback Control using rule-based metrics extracted from verifier outcomes and trajectory signals rather than LLM vibes. The main conclusion is not that agents are useless, but that they are still closer to engineering optimizers than autonomous researchers: reliability separates models more than peak score, execution is usually stronger than framing or feedback control, transferred experience can help or mislead, and genuine novelty is rare.

## Model definition

### Inputs
The evaluation uses 36 long-horizon tasks across Model Development, System Optimization, Puzzle and Challenge, and CUDA workloads, together with model traces, verifier signals, and stored experience artifacts.

### Outputs
It outputs task scores, avg@3 and best@3 summaries, cost and resource measurements, process metrics for Solution Framing / Execution / Feedback Control, experience-reuse deltas, harness comparisons, and novelty classifications.

### Training objective (loss)
There is no new trainable model in the main contribution. This is a benchmark and analysis framework over existing frontier agents and harnesses.

### Architecture / parameterization
The core apparatus is a shared long-horizon agent harness plus rule-based process scoring, controlled intra-task and inter-task experience-reuse experiments, native-versus-shared harness comparisons, and a conservative novelty review protocol.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to measure what current long-horizon AI R&D agents can actually do without collapsing everything into one final score that hides process bottlenecks, learning dynamics, and harness effects.

### 2. What is the method?
The method evaluates seven frontier models on 36 AutoLab tasks, reports avg@3 and best@3 outcome scores, scores within-run behavior through Solution Framing, Execution, and Feedback Control, tests experience reuse within and across tasks, compares harnesses, and separately audits solution novelty.

### 3. What is the method motivation?
A final score cannot tell whether an agent found a good direction early, implemented it badly, or recovered from failure well. It also cannot tell whether the system improves from accumulated experience or whether the harness is carrying more weight than the model.

### 4. What data does it use?
It uses 36 expert-curated AutoLab tasks spanning model development, system optimization, puzzle/challenge, and CUDA workloads, plus trajectory logs, verifier outcomes, commit histories, and stored lessons or raw workspace experience.

### 5. How is it evaluated?
It evaluates overall and category-level avg@3 and best@3, process metrics for C1/C2/C3, cost and elapsed-time trade-offs, intra-task and inter-task self-improvement, native versus shared harnesses, and LLM-judge plus manual-review novelty classifications.

### 6. What are the main results?
The paper's headline diagnosis is that reliability matters more than peak performance: the gap between strongest and weakest models is **0.237** on avg@3 but only **0.122** on best@3. GPT-5.5 and Gemini-3.1-Pro can land on similar final scores while differing sharply in Execution versus Feedback Control. Only **3 of 252** best-seed solutions qualify as genuinely novel under the review protocol. Experience transfer is not uniformly good: inter-task experience raises DeepSeek-V4-Pro's avg@3 by **0.093** but lowers Gemini-3.1-Pro's by **0.017**. Native harnesses mostly improve stability rather than best-case ceilings.

### 7. What is actually novel?
The novelty is not a new agent algorithm. It is the combination of process decomposition, controlled experience-reuse measurement, and harness comparison on the same long-horizon suite, which gives a more structural picture of agent capability.

### 8. What are the strengths?
The paper does not overclaim. It gives a practical diagnostic frame, keeps the process metrics deterministic, measures experience rather than only static capability, and reports the inconvenient novelty result instead of inflating composition or tuning as research creativity.

### 9. What are the weaknesses, limitations, or red flags?
The task suite is still AI-for-AI flavored rather than fully general. Rule-based process metrics capture only what they instrument, novelty judgment still needs human review to stay sane, and the conclusions are inevitably tied to the chosen harnesses and task families.

### 10. What challenges or open problems remain?
The big open problems are improving Solution Framing and Feedback Control, building experience systems that transfer without anchoring agents to bad prior conclusions, and designing harnesses that help without hiding model weaknesses.

### 11. What future work naturally follows?
Better rollout selection, trajectory-level training for reliability, richer experience filtering, more realistic external-side-effect tasks, and process metrics for broader agent settings all follow naturally from this benchmark.

### 12. Why does this matter for cabbageland?
Because "the model scored X" is not enough if the real question is how an agent reasons, recovers, and learns over long research loops. This paper gives a much better decomposition for that conversation.

### 13. What ideas are steal-worthy?
Separate Solution Framing, Execution, and Feedback Control explicitly. Measure experience reuse as a meta-capability. Treat harness choice as part of realized capability, especially for reliability rather than only peak score.

### 14. Final decision
Keep as a preserved note. It is one of the better recent papers on long-horizon agent evaluation because it adds useful structure without dissolving into benchmark theater.

## 6. Mandatory critical angles

The paper is strongest on evaluation fairness, failure-mode decomposition, and honesty about novelty. The main caution is that the process metrics are still abstractions over a particular benchmark family rather than universal truths about all agent work.

## 7. Writing style

The right tone is favorable but unsentimental. The paper deserves credit for showing that current agents are often competent optimizers while still falling short of real autonomous research.

## 8. Repository output format

Saved as a preserved paper note because the process-metric framing and the experience/harness findings are both likely to be reusable later.
