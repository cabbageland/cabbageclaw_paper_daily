# Tunable Tool-Call Rates in LLM Agents via Representation Steering

## Basic info

* Title: Tunable Tool-Call Rates in LLM Agents via Representation Steering
* Authors: Yuqi Chen, Vincent Siu, Yang Liu, Dawn Song, Chenguang Wang
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.25198
* Date surfaced: 2026-08-27
* Why selected in one sentence: It is the cleanest direct paper in the batch on turning whether-to-call into an explicit inference-time control variable instead of a prompt superstition.

## Quick verdict

* Must read

I inspected the full arXiv HTML text, especially the method sections on the forward-pass propensity proxy and difference-of-means extraction, the main results on PopQA, the cross-model results, and the held-out tool analysis. This paper earns a preserved note because it isolates a real agent-control object and then shows that it is cheap, transferable, and practically useful. The useful move is not "steer tool use" in the vague sense. It is separating whether to call any tool from which tool to call, then showing the first one is readable as a single direction.

## One-paragraph overview

The paper studies whether tool use can be controlled at inference time without retraining the model or rewriting the prompt. It extracts a residual-stream direction from a multi-tool harness by ranking prompts with the log-probability of the shared `<tool_call>` token, splitting them into high- and low-propensity sets, and taking a difference of means at a chosen decoder layer. Adding that direction with a positive or negative coefficient then raises or lowers the model's chance of calling a tool. The important result is that this is not just a local hack for one tool. The same direction generalizes across models and also transfers to six held-out tools that never appeared in the extraction harness.

## Model definition

### Inputs
Prompts rendered in a multi-tool chat harness, available tool schemas, and the residual-stream activation at the last prompt token for a selected decoder layer.

### Outputs
A scalar tool-call propensity signal during extraction, and at inference a modified agent response that is more or less likely to emit a tool call while preserving the underlying model's tool-choice routing.

### Training objective (loss)
There is no additional training objective. The steering direction is extracted from the base model's activations with a difference-of-means procedure and applied directly at inference time.

### Architecture / parameterization
Residual-stream steering on top of an instruction-tuned tool-calling LLM. The direction is computed from a high-propensity minus low-propensity activation mean in a three-tool harness, then added back with coefficient `alpha` at a selected decoder layer.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the fact that tool-using agents often both under-call and over-call tools, and that changing this behavior usually means retraining or prompt hacking instead of using an explicit control variable.

### 2. What is the method?
The method uses the model's own tool-calling opener token as a forward-pass proxy for whether it wants to call any tool. It ranks prompts by that score, computes a residual-stream difference-of-means vector between high- and low-propensity prompts, and adds that vector back during generation to raise or lower tool use.

### 3. What is the method motivation?
If the decision to call a tool is internally represented in a simple way, then agent cost and reliability can be controlled directly at inference time instead of being nudged indirectly through prompts or expensive finetuning.

### 4. What data does it use?
For extraction it uses a few thousand prompts drawn in equal parts from PopQA, GSM8K, and the BIG-Bench Hard tasks word sorting and date understanding. For evaluation it uses 200 questions per dataset, plus six held-out tools with 300 matching template queries each and 200 non-matching queries from the main pool.

### 5. How is it evaluated?
It is evaluated by sweeping steering strength in single-tool and multi-tool settings, checking live-tool cost/accuracy trade-offs on PopQA, testing cross-model transfer on five models, and testing whether a direction extracted from search, calculator, and Python transfers to six unseen tools.

### 6. What are the main results?
On the main model, raising `alpha` from `-2` to `+3` moves tool-call rates from near zero to `0.79-1.0` while calls remain well formed until the edge of the operating window. On PopQA with live search, accuracy rises from `0.29` with no searches to `0.56` at about `1.1` searches per question, and combining steering with a search-heavy prompt reaches `0.58`. Across five models, zero-search PopQA accuracy rises from `0.18-0.34` to peaks of `0.44-0.52` at roughly `0.75-1.2` searches per question. On held-out tools, the multi-tool direction suppresses all six and is stronger than each tool's own extracted direction for five of the six tools.

### 7. What is actually novel?
The real novelty is not just representation steering. It is showing that whether-to-call is a tool-general direction distinct from tool choice, that it can be extracted from a mixed-tool harness without labels or training, and that it keeps working on unseen tools.

### 8. What are the strengths?
The method is simple, cheap, and operational. It uses the model's own native tool-calling interface rather than an externally imposed scoring head. It also shows good transfer across model families and across unseen tools, which makes it more than a one-off interpretability anecdote.

### 9. What are the weaknesses, limitations, or red flags?
The evaluation still lives in a relatively clean harness with three core tools and mostly single-step tasks. The main live accuracy result is on PopQA plus search, not on more complex stateful agent tasks. Over-steering also causes malformed or invalid tool names in some models, which means the dial is useful but not free.

### 10. What challenges or open problems remain?
The obvious next question is whether the same separation survives in long-horizon agents where tool calls alter state, trigger side effects, or depend on memory rather than one-step knowledge gaps. Another open problem is how to choose the steering coefficient adaptively rather than fixing it per deployment.

### 11. What future work naturally follows?
Adaptive steering based on uncertainty or cost budgets, combining whether-to-call steering with explicit risk models for irreversible tools, and extending the analysis from binary tool use to richer decision factors such as timing, sequencing, and stop conditions.

### 12. Why does this matter for cabbageland?
Because cabbageland keeps caring about tool use as policy, not just capability. This paper gives a clean pattern for controlling agent cost and external-action appetite without retraining the whole stack.

### 13. What ideas are steal-worthy?
Use the model's own tool-call opener token as a forward-pass proxy for tool-use propensity. Extract a general whether-to-call direction in a mixed-tool setting instead of per-tool. Treat tool propensity and tool selection as different objects. Use inference-time steering as a cheap deployment dial rather than as a replacement for all training.

### 14. Final decision
Keep as a preserved note. This is one of the better recent agent-control papers because the mechanism is simple, testable, and directly useful.

## 6. Mandatory critical angles

The paper is strongest on explicit control, decomposition, and transferability. It is not solving all of agent planning, but it does earn its narrow claim. The main caveat is ecological scope: real-world agents do more than PopQA plus calculator plus Python.

## 7. Writing style

The right tone is crisp and approving. The paper deserves credit for finding a real dial and validating it, not for pretending a residual vector is the whole story of tool use.

## 8. Repository output format

Saved as a preserved paper note because the whether-to-call decomposition is a durable idea for future tool-using agents.
