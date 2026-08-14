# QuoteBench: How Matched Scores Can Hide Command-Path Failures

## Basic info

* Title: QuoteBench: How Matched Scores Can Hide Command-Path Failures
* Authors: Shangao Li, Yao Zhang, Volker Tresp, Yuanyuan Yang
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.13547
* Date surfaced: 2026-08-14
* Why selected in one sentence: It cleanly shows that a coding agent's measured success can be dominated by downstream command-path damage rather than by the quality of the generated command itself.

## Quick verdict

* Must read

I inspected the arXiv HTML full text. This is the strongest paper in the batch because it attacks a real failure mode with exact-state validation and a mechanism-identification design instead of vague agent lore.

## One-paragraph overview

QuoteBench studies one-shot Bash command generation under a deliberately crossed setup that separates the generation contract from the execution transport. The benchmark contains 56 exact-state tasks drawn from 14 incident-derived families such as literal byte writing, hostile filenames, heredocs, JSON editing, argv preservation, and SSH-like nesting. The key move is fixed-reply replay: the same stored raw-conditioned reply is executed with and without one extra downstream parser, so post-generation transport damage can be isolated from generation quality. Across the same-window configurations, replay through the added parser costs 55.4-73.2 points, while contract-conditioned generation recovers 30.4-60.7 points for six of eight settings. The result is a useful humiliation for matched scores: a deployment path can look nearly fine while hiding huge opposing effects.

## Model definition

### Inputs
The benchmark takes natural-language task prompts plus payload variants involving quotes, dollars, backticks, glob characters, newlines, JSON structure, Git state, or remote-like wrappers.

### Outputs
It evaluates generated shell commands by final filesystem state, argv bytes, environment values, JSON content, directory state, or Git history, and it also outputs replay-based transport-damage and compensation estimates.

### Training objective (loss)
There is no new training objective. The paper is a benchmark and causal evaluation design for existing coding-agent configurations.

### Architecture / parameterization
The core apparatus is a crossed benchmark over generation contract and execution transport, with fixed-reply replay under a single added parser, exact final-state validators, and multiple public frontier-model configurations plus native-tool hosted models.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to determine whether failures in command-issuing coding agents come from the generated command itself or from a downstream boundary that serializes, wraps, interpolates, or reparses that command before execution.

### 2. What is the method?
The method builds a 56-task exact-state benchmark, varies generation contract and execution transport independently, and replays the same stored replies through different transports so matched success can be decomposed into transport damage and contract-conditioned compensation.

### 3. What is the method motivation?
Agent benchmarks usually conflate planning, command construction, retries, and harness behavior. If a benchmark score drops, you still do not know whether the model emitted the wrong command or whether the command was correct for one boundary and broken by another.

### 4. What data does it use?
It uses 56 one-shot tasks from 14 incident-derived families, covering multiline text, hostile filenames, heredocs, literal argv and environment values, regex and glob metacharacters, Git metadata, and two local SSH-like simulations.

### 5. How is it evaluated?
It evaluates matched nested success, raw-path success, fixed-reply replay under added parsing, control versus hostile payload splits, effort ladders, native hosted tool-use settings, GNU versus BSD userlands, and private-payload follow-up replays.

### 6. What are the main results?
Across every same-window configuration, replaying the same stored reply through one added parser lowers success by **55.4-73.2** points. Contract-conditioned generation recovers **30.4-60.7** points for six of eight configurations. In the paper's most vivid example, GPT-5.6-sol shows a matched gap of only **-3.6** points while replay reveals **-64.3** transport damage and **+60.7** compensation. Matched nested success across the frozen same-window sweep spans **14.3-91.1%**, so the deployment path can meaningfully reorder models.

### 7. What is actually novel?
The novelty is the replay-based decomposition. The paper does not just show that shell quoting is fragile; it isolates a concrete command-path mechanism and measures how much of the observed score comes from transport damage versus generation adaptation.

### 8. What are the strengths?
The design is exact, mechanistic, and honest. Final-state validators prevent hand-wavy grading, fixed-reply replay attributes the failure to the boundary itself, and the paper is willing to publish a measurement result instead of pretending the point is an algorithmic repair.

### 9. What are the weaknesses, limitations, or red flags?
The benchmark is intentionally scoped to one class of command-path hazard. It does not solve the problem, and some deployment settings with typed operations or different shells may behave differently. The paper is about measurement, not full tool-agent coverage.

### 10. What challenges or open problems remain?
The open problems are designing typed or boundary-safe action interfaces, measuring other transport hazards beyond one nested parser, and deciding how benchmarks should expose or standardize command-path contracts.

### 11. What future work naturally follows?
Natural follow-ons include typed operation benchmarks, broader parser and transport families, harness audits for public agent systems, and path-aware model or effort selection during deployment.

### 12. Why does this matter for cabbageland?
Because tool reliability is never just "did the model know the command?" It is "did the whole action path preserve intent?" QuoteBench gives a reusable way to reason about that boundary.

### 13. What ideas are steal-worthy?
Use fixed-reply replay whenever a boundary can mutate model output. Separate event detection from downstream actionability. Treat benchmark scores as properties of a model-plus-boundary, not as pure model traits.

### 14. Final decision
Keep as a preserved note. This is the kind of operationally sharp evaluation paper that is easy to need later and annoying to reconstruct from memory.

## 6. Mandatory critical angles

The paper is strongest on mechanism isolation, evaluation fairness, and deployment honesty. Its main limitation is scope: it isolates one failure family extremely well rather than claiming to summarize all tool-use reliability.

## 7. Writing style

The right tone is bluntly approving. The paper earns credit by refusing to let a matched score blur together generation quality and transport corruption.

## 8. Repository output format

Saved as a preserved paper note because the benchmark design and the decomposition result are both useful reference points for future agent-evaluation work.
