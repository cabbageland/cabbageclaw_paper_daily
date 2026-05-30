# SAM: State-Adaptive Memory for Long-Horizon Reasoning Agent

## Basic info

* Title: SAM: State-Adaptive Memory for Long-Horizon Reasoning Agent
* Authors: Yuyang Hu, Hongjin Qian, Shuting Wang, Jiongnan Liu, Ziliang Zhao, Jiejun Tan, Zheng Liu, Zhicheng Dou
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2605.24468
* Date surfaced: 2026-05-30
* Why selected in one sentence: It turns agent memory into an explicit page-and-cue interface, then actually trains that interface instead of treating memory as prompt folklore.

## Quick verdict

* Highly relevant

This is one of the cleaner recent memory papers because the structure is real and the decomposition boundary is legible. The core idea is not exotic, but it is much less mushy than most summarize-or-retrieve agent memory work. The main caveat is that the training recipe leans heavily on frontier-model supervision and reward scaffolding, so the memory mechanism is cleaner than the full practical recipe.

## One-paragraph overview

SAM equips a frozen reasoning agent with an external memory module that converts long interaction histories into contiguous raw pages plus compact memory cues. The cues stay in the live context as lightweight handles describing what a page established, resolved, or left open, while the raw pages are stored externally. When the agent later needs old information, it selects relevant cues according to its current intent, and the memory model reconstructs targeted support from the associated raw pages. The paper then trains this memory module with supervised targets from stronger models and a tree-structured RL objective that gives credit to individual memory actions rather than only the trajectory’s final outcome.

## Model definition

### Inputs
The memory module sees page-level trajectory chunks during writing, and during recall it receives a recall intent plus one or more raw pages associated with selected memory cues. The overall agent context includes the task, recent live context, memory cues, and any recalled support.

### Outputs
On the write path, the model outputs a compact memory cue for each stored page. On the read path, it outputs recalled support content reconstructed from selected raw pages under the current recall intent.

### Training objective (loss)
The paper uses supervised fine-tuning over both cue generation and recall generation, with negative log-likelihood against expert-produced cue and recall targets. It then applies OAT-GRPO, a GRPO-style RL objective over memory-action siblings in a call tree, combining an outcome reward from downstream task success with an oracle-anchored recoverability reward judged against frontier-model references.

### Architecture / parameterization
A hybrid agent system with a frozen reasoning backbone and a separate Qwen3.5-9B memory model. Memory is page-based, cue-indexed, and recall is intent-conditioned reconstruction over stored raw pages.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Long-horizon agents fail when important evidence is scattered far back in the trajectory and becomes relevant only later. Simple truncation, rolling summaries, or naive retrieval either lose detail or fail to match the agent’s current need.

### 2. What is the method?
The method partitions history into contiguous pages once a token budget is reached. Each page is converted into a compact memory cue that stays visible in context, while the full page is stored externally. Later, the agent can issue a recall intent, select candidate cues, and ask the memory model to reconstruct the most relevant information from the corresponding raw pages.

### 3. What is the method motivation?
The authors want memory that is neither full-history baggage nor lossy one-shot compression. A cue should be a durable handle to the past, not a fake replacement for the past. The adaptive part should happen at read time, when the agent’s current state determines what old information matters.

### 4. What data does it use?
Training uses public agent-trajectory releases from OpenSeeker and OpenResearcher, filtered to remove trivial or incorrect trajectories. Evaluation uses BrowseComp, BrowseComp-ZH, WideSearch, and HLE.

### 5. How is it evaluated?
The paper compares SAM against no context management, heuristic truncation baselines like recent-k and discard-tool, rolling-summary baselines, and several frontier or open agent systems. The controlled comparisons keep the same backbone and tool interface while swapping only the context-management method.

### 6. What are the main results?
SAM is the strongest context-management method on both tested backbones. On GLM-4.7, the four-benchmark average rises from 49.4 with no context management to 57.0 with SAM. On Qwen3.5-35B-A3B, the average rises from 44.5 to 48.8. The largest gains show up on BrowseComp-style long-range browsing benchmarks, which is exactly where memory pressure should bite hardest.

### 7. What is actually novel?
The main novelty is the memory contract, not the phrase “state-adaptive.” Memory cues are explicitly not treated as final summaries, only as persistent handles to raw pages. The second real contribution is the RL credit-assignment scheme for memory actions via a memory-call tree and oracle-anchored reward.

### 8. What are the strengths?
The write/read decomposition is clean. The controlled baseline comparisons are better than the usual full-stack soup. The paper also correctly notices that memory actions need local credit assignment rather than only end-of-trajectory reward.

### 9. What are the weaknesses, limitations, or red flags?
The training recipe is expensive and somewhat baroque, relying on stronger frontier models both for supervised targets and committee-style reward shaping. The memory pages are simple contiguous chunks rather than semantically segmented episodes, which keeps the system simple but may also waste capacity. And the evaluation is benchmark-heavy rather than deployment-heavy, so practical failure modes under messy real-world tasks remain unclear.

### 10. What challenges or open problems remain?
How to make the write path more selective without becoming brittle. How to reduce dependence on expensive teacher models. How to detect when a cue is misleading or stale. And how to integrate memory with planning rather than treating it mainly as context support.

### 11. What future work naturally follows?
Learned page boundaries, memory confidence estimation, richer retrieval policies over cues, and coupling this kind of memory with explicit subgoal planning or world-state tracking.

### 12. Why does this matter for cabbageland?
Because it replaces vague “long context” talk with an actual memory interface. The raw-page plus cue split is a useful design pattern for any agent that needs continuity without drowning in its own transcript.

### 13. What ideas are steal-worthy?
Treat summaries as handles, not replacements. Keep raw episodic pages recoverable. Train memory actions with local credit assignment. Separate the agent backbone from the memory module so changes in memory behavior are actually measurable.

### 14. Final decision
Keep and cite. This is not the final answer to agent memory, but it is one of the more legible recent attempts and has reusable design ideas.
