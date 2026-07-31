# Stage-Replay Divergence Follows the KV Cache: Fixed-Prefix Precision Controls and Bidirectional Cache Transplantation

## Basic info

* Title: Stage-Replay Divergence Follows the KV Cache: Fixed-Prefix Precision Controls and Bidirectional Cache Transplantation
* Authors: Alexander Boesgaard Lorup
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.28495
* Date surfaced: 2026-07-31
* Why selected in one sentence: It gives a clean mechanistic answer to a common replay mistake: identical token prefixes do not guarantee that fresh replay preserved the decoder state that originally produced them.

## Quick verdict

**Must read**

This is one of the sharpest mechanistic papers in today's batch because it tests the right object directly. I inspected the full arXiv PDF, especially the introduction, matched replay experiment, fixed-prefix precision crossing, live-to-incremental bridge, bidirectional KV transplantation, limitations, and conclusion. The main caveat is external validity: the evidence is strong inside the tested Qwen2.5-derived family and runtime surface, but it is not yet a universal law for every model, kernel, or hardware stack.

## One-paragraph overview

The paper studies stage replay in a Qwen2.5-derived multi-branch reasoning system and asks whether replaying an intermediate token prefix through fresh prefill actually recreates the live decoder state that originally reached that prefix. The answer is no under the tested BF16 setup. A 200-item comparison shows that retained live cache and one-shot prefill of identical tokens diverge on 166 suffixes and 20 correctness labels despite exact within-construction replicas. A fixed-prefix 2x2 shows the divergence recurs in BF16 and disappears behaviorally in the tested FP32 setup. A prospective bridge verifies that ordinary live decoding and token-by-token incremental construction can be tensor-exact when they consume the same newly reached prefix. Then full bidirectional transplantation of all 48 KV layers makes the continuation follow the cache donor on every tested divergent row. The practical lesson is that exact-token replay can be stable and still fail state fidelity.

## Model definition

### Inputs
The audited system takes a fixed token prefix at a reasoning-stage boundary, along with the exact role, mask, position, decoding, and cache-construction contract used to continue generation.

### Outputs
The outputs are continued suffix trajectories, final answers, and correctness labels under different replay and intervention conditions.

### Training objective (loss)
No new model is trained in this paper. It is an audit of an existing Qwen2.5-derived multi-branch reasoning system, so the relevant contribution is experimental design and intervention rather than optimization.

### Architecture / parameterization
The studied model is a Qwen2.5-derived multi-branch reasoner. The paper compares retained live cache versus fresh one-shot prefill at a stage boundary, then intervenes directly by transplanting the complete 48-layer KV cache between paired continuations.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to determine whether reconstructed replay from an identical token prefix is a faithful substitute for the decoder state reached during live execution. Many replay diagnostics quietly assume that it is.

### 2. What is the method?
The method is a four-part audit: a matched retained-live versus fresh-prefill comparison, a fixed-prefix precision-by-construction crossing, a prospective live-to-incremental bridge, and bidirectional full KV-cache transplantation.

### 3. What is the method motivation?
Replay diagnostics, token-credit analyses, and stage ablations often treat stored intermediate text as if it were equivalent to the internal state that produced it. That assumption is stronger than exact token identity or replay repeatability can justify.

### 4. What data does it use?
The main matched and fixed-prefix analyses use a frozen 200-item holdout drawn from GPQA Main inside the tested multi-branch reasoning pipeline. The transplantation replication uses a later checkpoint from the same model family.

### 5. How is it evaluated?
Evaluation tracks suffix divergence, correctness churn, replica exactness, precision sensitivity, tensor-exact cache bridging on newly reached prefixes, and donor-following behavior under full KV transplantation. The paper uses both selected divergent rows and an outcome-blind later-checkpoint replication.

### 6. What are the main results?
In BF16, retained live cache and one-shot prefill disagree on 166 suffixes and 20 correctness labels out of 200, even though replicas within each construction are exact. In the fixed-prefix crossing, the BF16 disagreements recur while the tested FP32 setting shows no decoded disagreement. The live-to-incremental bridge is tensor-exact on 12 of 12 rows. Full bidirectional KV transplantation makes every tested divergent continuation follow the donor cache on 24 of 24 selected rows and 43 of 43 divergent rows in the later-checkpoint outcome-blind replication.

### 7. What is actually novel?
The novelty is not merely showing that replay can differ. The novel contribution is the clean separation of replica stability, token identity, state fidelity, and causal sufficiency in one experimental design, plus direct whole-cache transplantation at a reasoning-stage boundary.

### 8. What are the strengths?
The paper tests the right object instead of stopping at answer accuracy. The fixed-prefix control removes the easy discrete-state confound. The transplantation result is especially strong because it shows donor-following directly rather than just inferring it from correlations.

### 9. What are the weaknesses, limitations, or red flags?
The evidence comes from one Qwen2.5-derived family, one primary hardware/runtime surface, greedy decoding, and a specific reasoning architecture. The paper does not isolate the exact numerical origin of the drift, does not separate the causal roles of keys versus values, and does not establish a universal BF16 versus FP32 law.

### 10. What challenges or open problems remain?
The biggest open problem is generalizing the audit across architectures, runtimes, hardware, sampling temperatures, and replay settings. Another is locating the more specific operations that create the divergent live-versus-prefill states.

### 11. What future work naturally follows?
Future work should repeat this protocol across more model families, certify batch-invariant kernels where possible, separate key and value interventions, and reevaluate interpretability methods that rely on reconstructed replay.

### 12. Why does this matter for cabbageland?
It matters because cabbageland regularly builds or audits systems that reason over stored intermediate text, branch traces, or replayed contexts. This paper is a blunt warning: unless a live-state comparison passes, replay is measuring behavior from a reconstructed state, not from the state the end-to-end decoder actually occupied.

### 13. What ideas are steal-worthy?
Separate token identity from state fidelity explicitly. Use retained-live references rather than only replay stability checks. Treat direct state transplantation as the cleanest sufficiency test when the suspected state variable is manipulable. Report paired item churn instead of only net accuracy.

### 14. Final decision
**Keep it.** Narrow external validity is real, but the measurement rule is too important and too broadly transferable to ignore.
