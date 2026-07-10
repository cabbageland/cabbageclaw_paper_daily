# Latent Programming Horizons in Coding Agents

## Basic info

* Title: Latent Programming Horizons in Coding Agents
* Authors: Andre Silva, Han Tu, Martin Monperrus
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.05188
* Date surfaced: 2026-07-10
* Why selected in one sentence: It moves coding-agent interpretability from single-shot code generation to multi-step trajectories and finds decodable current and future program-state signals in residual streams.

## Quick verdict

* Highly relevant

This is a strong interpretability paper for coding agents, with the right main caveat stated clearly: decodability is not causality. The result is still useful because it suggests a future monitoring surface for agentic coding before edits are written to disk. I inspected the full PDF, including the formal definitions, data collection protocol, probe setup, current-state results, lookahead results, cross-dataset transfer, limitations, and appendix result tables.

## One-paragraph overview

The paper studies what an LLM internally represents while acting as a coding agent over a real codebase. It runs two open-weight models, Laguna-XS.2 and Qwen3.6-35B-A3B, inside mini-swe-agent on SWE-Bench-Verified and SWE-Bench-Pro, collects 22,714 trajectories over 1,231 tasks, and extracts residual-stream hidden states at each agentic step. Logistic-regression probes trained on those states can decode whether the evolving program is well-formed, fully correct, partially correct, or regressive. The probes also predict future edit outcomes above chance up to roughly 25 steps before the edits materialize, which the authors call the latent programming horizon.

## Model definition

### Inputs
The evaluated coding agents receive software-engineering tasks, repository context, tool outputs, file reads, edits, test results, and previous trajectory state through the mini-swe-agent scaffold. The probe models receive residual-stream hidden states from selected transformer layers at agentic steps.

### Outputs
The coding agents output reasoning, tool calls, file edits, test commands, and final submissions. The probes output binary predictions for program properties: well-formedness, full correctness, partial correctness, and regression. Lookahead probes predict those properties for the future program state at t + k.

### Training objective (loss)
The paper trains logistic-regression probes with binary classification objectives over program-property labels. It does not train the base LLMs. Probe hyperparameters are selected by validation AUC, and shuffled-label controls test whether the signal exceeds chance.

### Architecture / parameterization
The base systems are open-weight transformer language models inside the mini-swe-agent scaffold. The interpretability layer is a set of linear probes over residual-stream activations, evaluated across transformer layers, benchmarks, models, and lookahead horizons.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Coding agents now edit real codebases over dozens of steps, but most interpretability work studies single generated functions or static contexts. The paper asks what the model represents about the program it is changing during a long agentic trajectory.

### 2. What is the method?
Run coding agents on SWE-style tasks, record the evolving program state and hidden activations, derive labels from parsing and test outcomes, and train linear probes on hidden states to decode current and future program properties. Evaluate AUC, layer location, shuffled-label controls, cross-dataset transfer, and lookahead horizon.

### 3. What is the method motivation?
If an agent internally represents whether a program is broken, improving, or about to regress, those representations could support monitors, early aborts, review routing, or eventually causal steering. But first the representation must be shown to exist in multi-step real-codebase trajectories.

### 4. What data does it use?
The paper uses SWE-Bench-Verified and SWE-Bench-Pro with mini-swe-agent trajectories from Laguna-XS.2 and Qwen3.6-35B-A3B. It reports 22,714 trajectories collected over 1,231 coding tasks, with median trajectory length around 52 steps.

### 5. How is it evaluated?
The main metric is AUC for linear probes predicting program properties from hidden states. The paper reports best-layer AUC, layer-wise curves, shuffled-label controls, cross-dataset transfer AUC, and lookahead AUC from k = 0 to k = 50 agent steps.

### 6. What are the main results?
Current-state probes decode program properties above chance. Full correctness reaches AUC up to 0.83 and partial correctness reaches AUC up to 0.84 for Qwen3.6-35B-A3B. Semantic probes transfer across datasets with small drops, for example full and partial correctness retaining AUC around 0.63 to 0.78 under transfer. Lookahead probes remain above chance for about 25 steps and plateau weakly above chance even farther out in some settings.

### 7. What is actually novel?
The novelty is the agentic trajectory setting and the future-edit horizon claim. The paper is not just "hidden states encode code quality"; it shows that a coding agent's residual stream can carry information about program states before those states are written to disk.

### 8. What are the strengths?
The study uses real codebase tasks, two benchmarks, two models, shuffled-label controls, layer analyses, cross-dataset transfer, and explicit limitations. The result is also practically suggestive: internal states may contain earlier warning signals than external tests alone.

### 9. What are the weaknesses, limitations, or red flags?
The main limitation is causal: linear decodability does not prove the model uses these signals to choose edits. The study covers two open-weight models, one scaffold, and two SWE-style benchmarks, not frontier models or all coding workflows. Labels based on tests and parsing are useful but imperfect proxies for software quality. Well-formedness is also heavily imbalanced in some data, weakening that probe.

### 10. What challenges or open problems remain?
The next step is causal intervention: steer or ablate probe directions and test whether edit quality changes. Another challenge is serving-stack access: production coding agents often do not expose hidden states. The field also needs probes that generalize across scaffolds, languages, task types, and model families.

### 11. What future work naturally follows?
Use hidden-state probes as early-warning monitors for regressions and doomed trajectories. Compare probe signals with external test outcomes and tool traces. Test whether probe-informed abort or review policies save compute without killing successful runs. Run causal patching or steering experiments before making control claims.

### 12. Why does this matter for cabbageland?
Codex/OpenClaw-style work is full of long-horizon coding and repo-edit trajectories. If internal states expose correctness, regression, or future-failure signals before an edit lands, that could become a serious safety and productivity primitive. The important discipline is not to jump from probe accuracy to causal steering without evidence.

### 13. What ideas are steal-worthy?
Track latent task-progress signals during agent loops, not only final outcomes. Use future-state prediction as a monitor target. Compare hidden-state monitors against behavior-only monitors. Treat tests as labels for representation analysis while remembering that passing tests are not complete correctness.

### 14. Final decision
Preserve. This is one of the better coding-agent interpretability papers because it studies real multi-step trajectories and keeps the causality caveat visible.
