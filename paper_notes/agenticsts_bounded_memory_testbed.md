# AgenticSTS: A Bounded-Memory Testbed for Long-Horizon LLM Agents

## Basic info

* Title: AgenticSTS: A Bounded-Memory Testbed for Long-Horizon LLM Agents
* Authors: Xiangchen Cheng, Yunwei Jiang, Jianwen Sun, Zizhen Li, Chuanhao Li, Xiangcheng Cao, Yihao Liu, Fanrui Zhang, Li Jin, Kaipeng Zhang
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.02255
* Date surfaced: 2026-07-06
* Why selected in one sentence: It turns long-horizon agent memory into a bounded, typed, ablatable decision contract instead of an accumulating transcript habit.

## Quick verdict

* Must read

This is the most directly useful agent paper today. I inspected the full PDF, including the contract design, fixed-A0 results, token/cost comparison, conclusion, and limitations. The win-rate evidence is modest and the authors are explicit about that; the preserved value is the evaluation substrate and the memory-interface framing.

## One-paragraph overview

AgenticSTS studies long-horizon LLM agents through Slay the Spire 2, a closed-rule stochastic deck-building game that requires many tactical and strategic decisions. Instead of appending a growing cross-decision transcript, every decision is made from a fresh prompt assembled from five typed slots: fixed protocol instructions, state-specific schemas and legal action formats, retrieved game rules, episodic summaries, and triggered strategic skills. This keeps context bounded and makes each memory layer ablatable. The paper reports 298 completed trajectories, a balanced fixed-A0 ablation subset, cross-backbone probes, and ladder runs. The headline skill-layer improvement is directional rather than statistically decisive, but the contract is valuable because it turns memory from a vague store into an inspectable interface.

## Model definition

### Inputs
The agent receives the current Slay the Spire 2 state and a prompt freshly assembled from typed memory layers: L1 protocol instructions, L2 state schemas and legal action formats, L3 retrieved game rules, L4 episodic summaries, and L5 triggered strategic skills. Raw cross-decision transcripts are deliberately not appended.

### Outputs
The agent outputs game decisions, plus structured records that can later update episodic summaries or strategic skills in the postrun workflow. The paper's released artifact also outputs trajectories, prompt records, condition tags, and frozen memory / skill snapshots for analysis.

### Training objective (loss)
This is primarily an evaluation harness and agent design, not a learned model with a single loss. The evaluation objective is game performance under controlled conditions, with win rate, derived run score, highest attempted ascension, token use, and layer ablations.

### Architecture / parameterization
The core architecture is a bounded per-decision prompt-composition contract over five memory layers. L1 and L2 are fixed; L3 is retrieved game knowledge; L4 and L5 are mutable stores that can be disabled, frozen, or updated between runs. The underlying LLM can vary, and the paper probes backbone sensitivity.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Long-horizon LLM agents need memory, but the common solution of appending prior observations, actions, and reflections produces a growing, entangled prompt where it is hard to know which memory component helped or harmed. The paper asks whether memory can be bounded, typed, inspectable, and ablatable at decision time.

### 2. What is the method?
AgenticSTS rebuilds each decision prompt from named slots rather than carrying a raw transcript forward. The five-layer contract separates protocol, state schema, game rules, episodic memory, and strategy skills. Because each layer has a role and mutability policy, experiments can switch layers on and off without changing the whole agent.

### 3. What is the method motivation?
Memory is not merely storage; it is a contract about what evidence a future decision may see. Typed retrieval makes that contract explicit and keeps prompt size from scaling with the number of prior decisions.

### 4. What data does it use?
The testbed is Slay the Spire 2. The release includes 298 completed trajectories with condition tags, frozen L4 / L5 snapshots, decision-time prompt records, and analysis scripts. The headline fixed-A0 matrix uses a balanced subset of 50 games, ten per condition.

### 5. How is it evaluated?
The paper evaluates fixed-A0 ablations, auto-mode ascension ladder runs, cross-backbone transfer, token/cost behavior, and comparisons against public ecosystem baselines as difficulty calibration. It emphasizes within-harness comparisons over causal claims from mismatched external agents.

### 6. What are the main results?
The fixed-A0 no-store baseline wins 3/10 games. Skill-enabled rows report 6/10 wins, with the largest observed difference tied to triggered L5 skills. The authors explicitly report Fisher exact p around 0.37 for 3/10 versus 6/10, so this is directional rather than statistically decisive. Auto-mode streams with postrun-active memory attempt A6-A8, while no-postrun streams stop lower. The bounded contract also avoids the per-call transcript growth seen in accumulating-context agents.

### 7. What is actually novel?
The novelty is the memory interface as an evaluation object. Typed memory layers are not just implementation hygiene; they create an ablation surface for long-horizon agent behavior.

### 8. What are the strengths?
The paper is unusually careful about denominators, sample size, and external comparisons. It releases enough artifacts for re-analysis, and it frames memory in a way that directly supports engineering decisions.

### 9. What are the weaknesses, limitations, or red flags?
The headline result is underpowered. The authors say the fixed-A0 difference is not statistically significant, and the strongest direct comparison to a same-codebase accumulating-context agent is left to future work. The current headline uses one character and one game ecosystem.

### 10. What challenges or open problems remain?
The cleanest next step is a matched accumulating-context row under the same codebase, stores, prompts, and scoring scripts. Another challenge is transferring the typed memory contract from a closed-rule game into messier browser, coding, and real-world tool environments.

### 11. What future work naturally follows?
Run same-codebase comparisons against transcript accumulation, test different memory-layer schemas, add stronger statistical power, and adapt the contract to software agents where rules, task state, episodic summaries, and reusable workflow skills are separable.

### 12. Why does this matter for cabbageland?
OpenClaw-style agents need durable memory, but untyped memory easily becomes garbage retrieval with a nice name. AgenticSTS gives a better interface: separate fixed policy, current state, durable knowledge, episodic summaries, and triggered skills before the model reasons.

### 13. What ideas are steal-worthy?
Treat memory as a per-decision contract. Keep raw transcripts out of the default future prompt. Give each memory layer a mutability policy. Store condition tags and frozen memory snapshots so future claims are auditable.

### 14. Final decision
Keep as a must-read for agent memory evaluation. The evidence does not prove that bounded memory beats accumulating context, but it gives the right experimental surface for finding out.
