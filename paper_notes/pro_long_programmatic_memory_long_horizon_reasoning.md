# PRO-LONG: Programmatic Memory Enables Long-Horizon Reasoning

## Basic info

* Title: PRO-LONG: Programmatic Memory Enables Long-Horizon Reasoning
* Authors: Alexis Fox, Junlin Wang, Paul Rosu, Bhuwan Dhingra
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.20064
* Date surfaced: 2026-07-23
* Why selected in one sentence: It argues that long-horizon agent memory should default to lossless logging plus code-based retrieval instead of brittle selective summarization.

## Quick verdict

**Highly relevant**

This is one of the better context-engineering papers because it resists fake elegance. The main contribution is almost embarrassingly simple: save everything in a structured log and let a coding agent search it programmatically. I inspected the arXiv HTML sections covering the abstract, introduction, environment and scoring setup, PRO-LONG harness definition, main ARC-AGI-3 results, general ablations, and conclusion.

## One-paragraph overview

The paper studies long-horizon exploratory tasks where an agent must infer environment dynamics over many observations and actions. It argues that most memory systems force a fidelity-versus-tractability tradeoff by deciding too early what to compress, summarize, or store. PRO-LONG avoids that tradeoff by treating memory as a complete structured interaction log and retrieval as programmatic search over that log using ordinary coding-agent tools. The claim is not that logs are philosophically pure; it is that modern coding agents are finally good enough at regex, scripting, and file search to make lossless memory practical over trajectories that would otherwise be painful to keep in prompt context.

## Model definition

### Inputs
The wrapped coding agent receives the current environment state, recent tool outputs, and access to the full structured interaction log `logs.txt`.

### Outputs
It outputs code, searches, notes, and action sequences for the benchmark environment.

### Training objective (loss)
PRO-LONG introduces no new learned component and no new training objective. It is a context-management harness around existing coding agents.

### Architecture / parameterization
The harness appends every observation, action, and outcome to a structured log, then lets an off-the-shelf coding agent read and search that log programmatically. The evaluated agents include Codex-based and Claude-based coding setups on ARC-AGI-3.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to give long-horizon LLM agents a memory system that preserves all relevant environment detail without making retrieval too expensive or too lossy.

### 2. What is the method?
The method is an append-all write operation to a structured interaction log and a code-based read operation over that log, with no learned retriever, no vector database, and no heuristic pre-filter about what to save.

### 3. What is the method motivation?
Selective summaries solve short-term prompt pressure by throwing away details whose importance may only become obvious much later. A lossless log avoids that early compression mistake.

### 4. What data does it use?
The main benchmark is the full public ARC-AGI-3 game set: `25` environments with `6-10` levels each, plus matched evaluations across multiple frontier coding-agent backbones.

### 5. How is it evaluated?
It is evaluated on ARC-AGI-3 pass@1 and best@k performance, token cost, matched comparisons against stronger specialized harnesses, and ablations that remove or weaken different memory and tooling components.

### 6. What are the main results?
PRO-LONG improves over the base coding agent by an average of `18.0` percentage points across frontier models, reaches up to `76.1%` pass@1 while using `4.2x` to `5.8x` fewer tokens than specialized harnesses, and gets `97.4%` best@2 with Fable 5 at a total cost of about `1,750` dollars. The ablations also say something useful: the full log access does real work, while extra persistent-workspace abstractions add little.

### 7. What is actually novel?
The novelty is not "memory helps." It is the specific memory stance that a coding agent may now be competent enough to treat raw interaction history itself as the searchable substrate.

### 8. What are the strengths?
The design is simple, lossless, and compatible with existing tools. The paper also does the important ablation work needed to show that the log itself matters more than decorative memory extras.

### 9. What are the weaknesses, limitations, or red flags?
The empirical case is still heavily tied to ARC-AGI-3, which is a specialized exploratory benchmark. A strong benchmark result is not the same thing as a general law of long-horizon memory.

### 10. What challenges or open problems remain?
The big question is whether the same log-first design still wins in richer multimodal settings where the history is not easily serialized into compact searchable text.

### 11. What future work naturally follows?
Test the same write/read design in robotics, scientific workflows, or tool-using research agents; add indexing only where measurement proves it is needed; and study when lossless logs finally become too big even for code-based search.

### 12. Why does this matter for cabbageland?
Cabbageland cares about memory, long-horizon reasoning, and explicit state. This paper gives a strong argument for treating memory as infrastructure and retrieval as a programmable operation rather than as a sacred learned module.

### 13. What ideas are steal-worthy?
Separate accessed state from accessible state. Default to append-all logging when hindsight relevance is hard to predict. Let coding agents use ordinary search and scripting over the history instead of hiding everything behind a bespoke retrieval stack.

### 14. Final decision
**Keep it.** The benchmark scope keeps it below the top two papers today, but the write-all and search-later design principle is strong enough to preserve.
