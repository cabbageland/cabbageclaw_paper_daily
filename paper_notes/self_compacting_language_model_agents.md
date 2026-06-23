# Self-Compacting Language Model Agents

## Basic info

* Title: Self-Compacting Language Model Agents
* Authors: Tianjian Li, Jingyu Zhang, William Jurayj, Xi Wang, Chuanyang Jin, Mehrdad Farajtabar, Eric Nalisnick, Daniel Khashabi
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.23525
* Date surfaced: 2026-06-23
* Why selected in one sentence: It gives long-horizon agents an explicit, rubric-gated way to decide when a reasoning trace is safe to compact instead of firing summaries on dumb token-count thresholds.

## Quick verdict

* Must read

This is the strongest paper in today's scan because it turns context compaction into a trajectory-state decision. I inspected the full arXiv PDF, especially the scaffold definition, math and agentic-search experiments, ablations, cost analysis, and limitations. The result is not a complete learned memory system, but the mechanism is practical, inspectable, and immediately stealable.

## One-paragraph overview

The paper studies long agent traces made of reasoning, tool calls, search results, and intermediate attempts. Fixed-interval compaction fires after some token threshold, which can erase a partial derivation or a verified fact before the model is done using it. SELF COMPACT instead exposes summarization as an inline tool and asks the same language model, through a lightweight rubric probe, whether the current trajectory is ready to compress. The rubric encourages compression after a subtask has resolved or the trajectory is converging, and suppresses it mid-derivation or when stuck. When the model emits COMPRESS, the scaffold asks it to summarize the accumulated trajectory, resets the context to the original prompt plus summary, and continues generation.

## Model definition

### Inputs

Inputs are the original task prompt, the accumulated reasoning/tool trajectory, a probe interval, a rubric prompt that defines when to compress or continue, and a summarizer prompt. In the agentic-search setting, the trajectory includes search and document-observation turns.

### Outputs

The scaffold outputs intermediate rubric decisions, either COMPRESS or CONTINUE, optional summaries of the trajectory, and the final task answer. Operationally, the summary becomes the new compacted context prefix.

### Training objective (loss)

SELF COMPACT is training-free. There is no new optimization objective for the compaction policy. The underlying language models are used at inference time for generation, rubric judgment, and summarization. The evaluation objective is task accuracy under token/cost budgets, not a learned loss.

### Architecture / parameterization

The architecture is a language-model agent wrapped with a compaction tool. Every N steps, the scaffold appends the rubric probe while reusing the KV prefix. If the model chooses COMPRESS, the same model generates a summary and the context is hard reset to the prompt plus summary. If it chooses CONTINUE, the temporary probe and response are removed and the original trajectory remains unchanged.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Long-horizon agents accumulate stale reasoning, failed searches, irrelevant observations, and partial plans. This context is expensive and can actively hurt generation through context rot. Existing compaction usually fires when the context reaches a fixed token threshold, but token count does not know whether the agent is mid-proof, mid-search, or just finished a useful subtask.

### 2. What is the method?

The method pairs an inline summarization tool with a short rubric. At probe points, the model judges whether the trajectory is in a compressible state. If yes, it summarizes the full trace, replaces the long trajectory with that summary, and resumes. If no, it removes the probe and continues from the original trace. The same model performs generation, judgment, and summarization.

### 3. What is the method motivation?

Compaction is asymmetric. A well-timed summary can crystallize verified facts and remove junk. A poorly timed summary can delete the exact intermediate result needed for the next step. The paper's BrowseComp example makes this concrete: fixed-interval summarization wipes verified facts, while rubric-gated summarization fires after facts are resolved.

### 4. What data does it use?

The math evaluation uses IMO-Answerbench, HMMT November 2025, and HMMT February 2026 with Qwen-family models. The agentic-search evaluation uses BrowseComp, BrowseComp-Plus, and DeepSearch QA with GLM-4.7-Flash, MiniMax-M2.5, and Mimo-V2-Flash. The paper reports runs over subsampled search benchmarks and repeated math generations.

### 5. How is it evaluated?

The paper compares no compaction, fixed-interval summarization, delete-all, keep-last-N, SELF COMPACT, and ablated SELF COMPACT without rubrics. Metrics include answer accuracy, per-question token use, and per-question cost. The math setting constrains fixed-interval summarization to similar token budgets; the search setting reports accuracy and USD cost.

### 6. What are the main results?

On competition math, SELF COMPACT achieves the best result in 11 of 12 settings under matched token budgets. On Qwen3.5-9B thinking-disabled, it improves over the no-compaction baseline by 16.4 points on IMO-Answerbench, 10.0 on HMMT November, and 18.1 on HMMT February. On agentic search, SELF COMPACT improves BrowseComp-Plus by 8.5 points for GLM-4.7-Flash, 9.2 for MiniMax-M2.5, and 5.3 for Mimo-V2-Flash over no compaction. It also lowers BrowseComp-Plus per-question cost by 67 percent, 63 percent, and 33 percent respectively versus no compaction.

### 7. What is actually novel?

The novelty is not summarization itself. The useful novelty is making compaction timing depend on the reasoning state through a lightweight rubric, while keeping the mechanism training-free and compatible with tool-using agents. The paper also isolates the importance of the rubric: tool access alone is not enough.

### 8. What are the strengths?

The mechanism is simple, inspectable, and immediately implementable. The ablations are useful: removing the rubric collapses performance toward fixed-interval summarization, showing the gain comes from structural timing rather than extra summary calls. The cost analysis is also practical because it accounts for KV-cache reuse and cached prompt tokens.

### 9. What are the weaknesses, limitations, or red flags?

The work evaluates open-weight models and notes that stronger frontier systems may already have better internal metacognition. The compaction policy is prompted, not learned, so it may be brittle under domains where the rubric does not identify good closure points. The summaries are still natural-language lossy state, not a guaranteed sufficient statistic. The paper also does not solve how to verify summary fidelity or recover facts lost by a bad summary.

### 10. What challenges or open problems remain?

Open problems include summary verification, task-specific compaction rubrics, learned compaction policies distilled from the rubric, richer state objects than natural-language summaries, and detecting when a summary has silently damaged an execution trace.

### 11. What future work naturally follows?

A natural next step is to train a small compaction controller from rubric-labeled trajectories, then compare it with the prompted rubric under distribution shift. Another useful follow-up is to attach provenance to summary claims so later steps can recover the original tool evidence when needed.

### 12. Why does this matter for cabbageland?

Cabbageland cares about agents with long-lived state, tools, and memory. This paper says compaction should be a deliberate state transition, not a context-window panic button. For any agent that reads files, searches, reasons, or edits code over many turns, the right question is whether the current subtask is closed enough to preserve as a compact state.

### 13. What ideas are steal-worthy?

Use an explicit compaction tool. Gate compaction with a short rubric that names compressible and non-compressible states. Remove the probe if the decision is CONTINUE so the probe itself does not contaminate the trace. Treat fixed token thresholds as a fallback, not the primary memory policy. Evaluate compaction by accuracy, cost, and failure modes, not just compression ratio.

### 14. Final decision

**Keep it.** This is a direct hit for long-horizon agent memory. The paper does not make compaction magically reliable, but it gives a clean design primitive: compact after closed reasoning units, not after arbitrary token counts.
