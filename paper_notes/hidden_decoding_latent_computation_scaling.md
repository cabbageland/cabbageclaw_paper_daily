# Hidden Decoding at Scale: Latent Computation Scaling for Large Language Models

## Basic info

* Title: Hidden Decoding at Scale: Latent Computation Scaling for Large Language Models
* Authors: Aiwei Liu, Cheng Shi, Chuhan Wu, Ci Lei, Di Lu, Donald He, Fan Zhang, Fanhao Kong, Feifei Zhang, Guan Wang, et al.
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.08186
* Date surfaced: 2026-07-11
* Why selected in one sentence: It proposes sequence-length expansion as a practical fixed-backbone way to give each token more latent computation at frontier MoE scale.

## Quick verdict

**Important foundation-model report, with reproducibility caveats**

Hidden Decoding is interesting because it tries to scale computation without adding Transformer depth or width. The evidence is unusually ambitious, including matched comparisons at 80B and 617B total-parameter MoE scale, but much of the key evidence depends on the authors' WeLM stack and unreleased models. I inspected the full arXiv PDF, including the method, cost model, frontier-scale results, expansion studies, attention ablations, stream probes, and conclusion.

## One-paragraph overview

Hidden Decoding expands each token into multiple stream embeddings and interleaves those streams into a longer sequence. Only the final stream is trained to predict the next token; the earlier streams receive no direct loss and act as latent computation states. Because naive dense attention over the expanded sequence would be quadratic in the expansion factor, the paper introduces Stream-Factorized Attention: most layers attend only within each stream, while selected layers mix streams. This keeps training cost close to linear in the number of streams. The paper applies the method during continued pretraining of WeLM MoE checkpoints and reports matched early-SFT improvements for WeLM-HD4-80B and WeLM-HD4-617B over non-HD counterparts without changing active Transformer parameters per token.

## Model definition

### Inputs
The model receives an ordinary token sequence. Each token is mapped through multiple independent embedding tables, one per stream, then interleaved into an expanded sequence of length n times the original length.

### Outputs
The model predicts next tokens only from the final stream positions. Earlier stream positions contribute hidden computation and KV state but are not directly supervised.

### Training objective (loss)
The loss is next-token cross-entropy applied only at final-stream positions. Continued pretraining introduces Hidden Decoding from a converged checkpoint, followed by matched early SFT comparisons in the main large-model results.

### Architecture / parameterization
The Transformer backbone is kept fixed. Hidden Decoding adds multiple token embedding streams and uses Stream-Factorized Attention, where most layers are intra-stream and only selected layers perform cross-stream mixing. In WeLM, an additional KV-mirror optimization skips some intermediate stream work in mirrored layers.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to improve already-strong language models without training a larger Transformer backbone. Depth-recurrent or looped computation can add per-token compute, but it is hard to scale in large MoE training systems that rely on pipeline parallelism.

### 2. What is the method?
Hidden Decoding places extra computation along the sequence dimension. Each token becomes n streams. The final stream predicts the next token, while earlier streams provide latent intermediate states. Stream-Factorized Attention makes the cost manageable by limiting cross-stream attention to selected layers.

### 3. What is the method motivation?
Test-time scaling and reasoning models suggest that more computation per token can help, but adding depth or repeated loops conflicts with efficient large-model training. Sequence expansion is compatible with standard training infrastructure because it looks like a longer sequence rather than repeated serial passes through the backbone.

### 4. What data does it use?
The paper uses continued pretraining and early SFT data from the WeLM training stack. The exact datasets are not fully public in the way a small academic reproduction would be.

### 5. How is it evaluated?
The main evaluations compare matched WeLM and WeLM-HD4 models at 80B and 617B total-parameter MoE scale across hard math, science, coding, and general benchmarks. The paper also reports expansion-factor studies on an 80B MoE and dense Qwen3-8B, attention-composition ablations on a 21B MoE, supervision-design ablations on a 6B MoE, and serving-throughput measurements.

### 6. What are the main results?
In matched early-SFT comparisons, WeLM-HD4-80B and WeLM-HD4-617B improve every shared benchmark over their non-HD counterparts. For the 80B model, reported gains include SciCode 45.8 to 50.0, PHYBench 69.8 to 73.8, and FrontierMath 45.8 to 49.0. For the 617B model, gains include GPQA Diamond 89.1 to 91.2 and HLE 33.6 to 35.4. Training cost for 4x expansion is reported at 5.1x on 80B and 4.4x on 617B, far below dense-attention quadratic cost.

### 7. What is actually novel?
The novel part is the scalable formulation of latent per-token computation as sequence-length expansion with final-stream-only supervision. Stream-Factorized Attention is the enabling engineering idea that makes the expansion plausible at large scale.

### 8. What are the strengths?
The paper has a coherent scaling argument, matched comparisons, cost measurements, and useful ablations showing that supervision design and cross-stream mixing matter. The result also targets an important practical regime: frontier-scale MoE models where depth looping is awkward.

### 9. What are the weaknesses, limitations, or red flags?
The strongest evidence is not easily reproducible because the WeLM checkpoints and training data are proprietary or not fully inspectable. Some benefits may depend on WeLM-specific architecture and training infrastructure. The method also increases KV/cache and sequence-processing cost, which may constrain serving contexts.

### 10. What challenges or open problems remain?
The big open question is whether the same gains appear in independently trained open models at meaningful scale. Another challenge is understanding what the intermediate streams actually compute and whether they improve reliability, reasoning, or just benchmark performance.

### 11. What future work naturally follows?
A good follow-up would reproduce Hidden Decoding on open 7B-70B models with public training recipes, test robustness under long-context and tool-agent settings, and compare against depth recurrence, extra SFT compute, and test-time reasoning compute under equal budget.

### 12. Why does this matter for cabbageland?
Cabbageland cares about mechanisms for explicit intermediate state. Hidden Decoding is a foundation-model version of that idea: give each token latent workspace without exposing it as natural-language chain-of-thought or widening the model.

### 13. What ideas are steal-worthy?
Supervise only the final latent stream. Preserve intermediate-stream KV so later tokens can use it. Treat expansion factor as a compute-scaling knob. Use sparse cross-stream mixing rather than full dense mixing everywhere. Measure training and serving cost, not just accuracy.

### 14. Final decision
**Keep it, with caveats.** The idea is strong and the scale is impressive, but treat the numbers as a serious report rather than independently verified public evidence.
