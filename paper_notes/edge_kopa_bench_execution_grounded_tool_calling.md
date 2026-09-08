# Multi-Step Tool-Calling over Korean Open Public APIs: A Benchmark and a Data-Synthesis Recipe

## Basic info

* Title: Multi-Step Tool-Calling over Korean Open Public APIs: A Benchmark and a Data-Synthesis Recipe
* Authors: Dain Kim, Eungi Cho, Kyumin Kim, Shinyeong Noh, Kyuseong Lim
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2609.05395
* Date surfaced: 2026-09-08
* Why selected in one sentence: It builds tool-use training data by executing dependency edges against live APIs instead of trusting plausible schemas.

## Quick verdict

* Highly relevant

I inspected the full arXiv HTML text, especially the KOPA-Bench construction, EDGE graph update loop, trajectory synthesis, ablations, live-endpoint caveats, and statistical reliability section. This is worth preserving because it treats tool-call data synthesis as an execution problem, not a prompt-writing problem.

## One-paragraph overview

The paper introduces KOPA-Bench, a 145-task benchmark for multi-step tool calling over live Korean public APIs, and EDGE, a data-synthesis pipeline that builds executable trajectories from verified tool dependencies. EDGE first proposes output-to-input dependency edges between tools, then tests those edges through live execution, updates edge posteriors, prunes unreliable edges, and uses the resulting graph to synthesize sequential, fan-out, comparison, conditional, and parallel trajectories. Fine-tuning small Qwen3.5 models on the resulting data improves KOPA-Bench and transfers to BFCL.

## Model definition

### Inputs
An inventory of typed tools over Korean public APIs, candidate output-to-input dependencies, live execution outcomes, and natural-language tasks over public-sector domains.

### Outputs
A validated dependency graph, executable synthetic trajectories, generated questions and answers, and fine-tuned tool-calling models.

### Training objective (loss)
The paper trains on EDGE trajectories with SFT and GRPO. The strongest results use GRPO over the filtered EDGE dataset.

### Architecture / parameterization
EDGE is a two-phase system: execution-grounded dynamic graph construction, followed by type-based trajectory synthesis that handles single-value, multi-value, fan-out, comparison, conditional, and semantic-parallel tool-use patterns.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Open-source on-premise agents often fail at public-sector multi-step tool use, especially when they need prerequisite code lookups, pagination, high-cardinality outputs, and dependent API calls.

### 2. What is the method?
Construct a tool dependency graph, verify candidate edges by live execution, prune edges with poor posterior success, and generate trajectories only from dependencies that survived actual endpoint contact.

### 3. What is the method motivation?
Schema matching and LLM judgments can make an edge look valid even when the live endpoint rejects it or returns a shape that breaks the next call.

### 4. What data does it use?
KOPA-Bench contains 145 tasks across 10 platforms and six domains: traffic, finance, education, law, politics, and district administration. The tool inventory has 2,318 functions, average tasks require five calls, and up to 59% involve parallel execution.

### 5. How is it evaluated?
The paper reports pass@1, pass@4, action correctness, out-of-distribution BFCL performance, objective and trajectory ablations, filtering effects, graph-edge execution success, and confidence intervals over seeds.

### 6. What are the main results?
On KOPA-Bench, Qwen3.5-4B improves pass@1 from 0.1758 to 0.3094, and Qwen3.5-9B improves from 0.33 to 0.43, nearly matching an untuned 27B model at 0.45. The gains transfer to BFCL, especially multi-turn settings, with +4.04 points for 4B and +5.87 points for 9B. SFT on the same data already gives most of the gain, while GRPO further improves pass@4 from 0.3586 to 0.4690. Filtering stale or malformed synthesized tasks adds 6.7 points. Execution-grounded graph refinement raises executable edge success from 50.2% to 62.7%, while pruned edges execute only 14.8% of the time.

### 7. What is actually novel?
The novelty is grounding multi-step tool-use data synthesis in live execution evidence and representing high-cardinality handoffs explicitly during trajectory generation.

### 8. What are the strengths?
The paper attacks the real messy part of tools: endpoint drift, dependent lookups, pagination, and many-record handoffs. The edge-pruning ablation directly supports the core claim.

### 9. What are the weaknesses, limitations, or red flags?
The benchmark is tied to live Korean public APIs, so reproduction depends on endpoint stability. The comparison is mostly against controlled EDGE variants rather than full end-to-end alternative synthesis systems.

### 10. What challenges or open problems remain?
The method needs evidence across other languages, private APIs, commercial SaaS tools, authenticated flows, and state-changing endpoints.

### 11. What future work naturally follows?
Apply execution-grounded graph synthesis to broader tool inventories, add endpoint-versioning memory, and connect edge posterior confidence to runtime tool-call planning.

### 12. Why does this matter for cabbageland?
Cabbageland cares about agents whose tool use survives reality. EDGE is a useful pattern: plausible dependency edges are not enough; tool-link knowledge should be earned by execution.

### 13. What ideas are steal-worthy?
Maintain posteriors over dependency edges. Prune with live evidence. Treat high-cardinality outputs as first-class. Evaluate response, environment state, and tool-action correctness separately.

### 14. Final decision
Keep as a preserved note. The domain is narrow, but the execution-grounded synthesis pattern is broadly useful.

## 6. Mandatory critical angles

The mechanism is strong because execution evidence changes the graph. The caveat is that live endpoints make both benchmarking and reproducibility harder, so the same commitment to reality creates operational instability.

## 7. Writing style

Tone should be favorable but grounded. This is not a general tool-use solution; it is a good recipe for refusing fake executable data.

## 8. Repository output format

Saved as a preserved paper note because execution-grounded tool dependency learning is reusable for agent infrastructure.
