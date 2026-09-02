# MemoryWalker: Stop Training Agents on Contexts They Never Saw

## Basic info

* Title: MemoryWalker: Stop Training Agents on Contexts They Never Saw
* Authors: Zinco J, Xunjie Zhu, Shen Huang, Zhenyi Wang, Pengjun Xie, Jieping Ye
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2609.00865
* Date surfaced: 2026-09-02
* Why selected in one sentence: It identifies context-compressed agent training as a conditioning-tree problem and then gives exact plus practical fixes.

## Quick verdict

* Must read

I inspected the full arXiv HTML text, especially the two replay pitfalls, the LogitTree / 4D-mask equivalence, the SDCC relaxation, the main result matrix, and the black-box harness transfer sections. This earns a preserved note because it does more than notice a train-inference mismatch. It turns the mismatch into a precise structural invariant and shows how to restore it.

## One-paragraph overview

The paper starts from a simple production fact: long-horizon agents often rewrite or summarize their own history during rollout. That makes post-training replay tricky, because earlier tokens were generated under the pre-eviction prefix while later tokens were generated under the compressed replacement. A trainer that replays only the final compressed path teaches time-travel leakage; a trainer that replays the full depth-first union teaches the model to condition on context it did not have at generation time. The authors therefore treat the rollout as a conditioning tree rather than a single sequence, then propose two exact fixes, LogitTree and a packed 4D attention mask, plus a cheaper self-distillation relaxation called SDCC for cases where exact replay is too expensive or black-box harnesses hide the internal edits.

## Model definition

### Inputs
The base policy takes the live context view that existed at each decoding step, including compressed summaries or memory-edited prefixes, plus the current prompt / tool trace tokens. The exact methods also need eviction-junction records that say when the live prefix changed.

### Outputs
The model outputs the next-token distribution used by the agent policy during replay-time SFT or RL training.

### Training objective (loss)
The exact methods keep the usual policy objective but replay it on tree-consistent branches so that each token is scored under the same context that produced it. SDCC adds a forward KL term at eviction junctions between a compressed student view and a stop-gradient teacher evaluated on the reconstructed pre-eviction prefix, yielding an `O(sqrt(epsilon_KL))` bound on the residual train-deployment gap.

### Architecture / parameterization
The learned policy is still an ordinary LLM agent. The novelty is the replay formulation around it: LogitTree branch materialization, a packed 4D attention mask, or the SDCC self-distillation wrapper.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
How do you train an agent on rollouts whose context was actively edited during inference without teaching it to condition on the wrong history?

### 2. What is the method?
Formulate memory-compressed rollouts as a conditioning tree, then either replay each branch exactly with LogitTree, pack the same conditioning into a 4D attention mask, or approximate it with SDCC.

### 3. What is the method motivation?
The naive replay options fail in opposite directions. One conditions earlier tokens on summaries that were created later. The other conditions later tokens on raw prefixes that had already been evicted. Both silently change the policy-learning target.

### 4. What data does it use?
Three white-box context editors (TC-RAG, AgentFold, MemexRL), two black-box harnesses (Claude Code and OpenCode), seven web-search benchmarks, and a larger WideSearch evaluation. The main model matrix uses Qwen3-4B in live-compression settings.

### 5. How is it evaluated?
By train-rollout logit drift, downstream EM / reward under live compression, white-box versus black-box transfer, editor-specific eviction regimes, and a larger-scale Claude Code WideSearch run.

### 6. What are the main results?
The exact methods return drift to the no-compression floor by construction. On the low-eviction MemexRL anchor, LogitTree reaches `0.0133` drift and 4D reaches `0.0140`, against a `0.0135` no-compression control. On eviction-heavy AgentFold, the 4D mask keeps drift around `0.022` while Naive-Compressed reaches `0.366`. Cross-harness EM does not have to be traded away for consistency: on AgentFold, 4D reaches `34.2` versus `33.2` for Naive-Compressed; on TC-RAG, `37.2` versus `36.7`. In black-box runs, SDCC reaches `37.5` average EM on Claude Code and `36.9` on OpenCode while keeping low observed drift.

### 7. What is actually novel?
The novelty is the conditioning-tree formulation itself, the proof that LogitTree and the packed 4D mask are gradient-equivalent exact walks of that tree, and SDCC as a black-box-friendly relaxation.

### 8. What are the strengths?
It isolates a real production failure mode, gives exact and approximate fixes, spans white-box and black-box harnesses, and reports cost tradeoffs instead of pretending the exact method is free.

### 9. What are the weaknesses, limitations, or red flags?
The exact methods are expensive or infrastructure-heavy. LogitTree needs `K + 1` backward passes, while the 4D mask needs custom masking support plus white-box eviction records. The empirical study is still concentrated in search-style agent benchmarks rather than a broader mix of coding or embodied settings.

### 10. What challenges or open problems remain?
The open problem is getting exact or near-exact conditioning consistency with lower systems cost, especially when the harness exposes only coarse replay logs or uses richer memory edits than prefix replacement.

### 11. What future work naturally follows?
Broader evaluation on coding and browser agents, better black-box eviction instrumentation, and learned memory editors whose training objective is tree-consistent from the start.

### 12. Why does this matter for cabbageland?
Because cabbageland keeps caring about long-horizon agents with edited histories. This paper gives a clean answer to the question "what exactly are we training on after the harness rewrites the context?"

### 13. What ideas are steal-worthy?
Treat memory-edited interaction logs as trees, not sequences. Persist replay-time evidence about when the live view changed. Use a cheap KL regularizer only at divergence points instead of diffusing the penalty everywhere.

### 14. Final decision
Keep as a preserved note. This is one of the better recent agent-memory papers because the mechanism is specific, the failure mode is real, and the fixes are structurally clean.
