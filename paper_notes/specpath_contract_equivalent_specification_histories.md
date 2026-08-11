# SpecPath: Testing Coding Agents Across Contract-Equivalent Specification Histories

## Basic info

* Title: SpecPath: Testing Coding Agents Across Contract-Equivalent Specification Histories
* Authors: Yangfan Wu, Haozhe Wang, Huanyu Yang, Jianmin Ji, Fangzhen Lin
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.09799
* Date surfaced: 2026-08-11
* Why selected in one sentence: It isolates a concrete agent failure mode, specification-path sensitivity, with a much cleaner evaluation design than the usual long-context handwaving.

## Quick verdict

* Must read

I inspected the arXiv HTML full text. This is one of the cleaner recent agent-evaluation papers because it does not confuse longer histories with the actual thing that matters. It identifies active-contract resolution as a first-class problem, then builds an executable paired test around that problem.

## One-paragraph overview

The paper asks a very specific question: if two requirement histories resolve to the same final contract, does a coding agent produce the same tested behavior? To answer that, SpecPath fixes the repository, final contract, verifier, agent system, and execution budget, and varies only the history path that leads to the contract. It constructs contract-equivalent histories such as duplicate, override, cancellation, and split variants across five calibrated software task families. The key result is that aggregate success barely changes across histories, but paired block analysis reveals many hidden failures: among complete blocks that succeed on the direct specification, a large fraction fail under at least one equivalent history. The paper argues that the real missing skill is active-contract resolution, not merely "handling more context."

## Model definition

### Inputs
The benchmark takes a repository task, a fixed final contract, several contract-equivalent requirement histories, a coding-agent configuration, an execution budget, and an executable verifier.

### Outputs
It outputs fresh-run patches and executable outcomes for each history condition, plus metrics such as final-contract realization and conditional path violation.

### Training objective (loss)
There is no model-training objective in the contribution itself. This is an evaluation framework and dataset construction paper.

### Architecture / parameterization
The core design is a paired executable benchmark over five PR-derived task families. Each block contains a direct history plus contract-equivalent history variants, direct controls, and a verifier held fixed across fresh runs.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to measure whether coding agents resolve the active specification correctly when requirements evolve through history rather than being presented once in consolidated form.

### 2. What is the method?
The method is a diagnostic benchmark that creates multiple requirement histories with the same final contract, runs coding agents on each history under matched conditions, and compares paired executable outcomes rather than only condition-level averages.

### 3. What is the method motivation?
Conversation history is append-only, but the active contract is mutable. A later instruction can override, cancel, or narrow an earlier one, so neither "remember everything" nor "follow the latest turn" is sufficient by itself.

### 4. What data does it use?
It uses five calibrated Python PR/task families derived from real repositories: Kedro, NeMo Agent Toolkit, pytest-odoo, SBSim, and Tracecat, evaluated across fourteen coding-agent configurations.

### 5. How is it evaluated?
It evaluates final-contract realization under direct and alternative histories, then measures conditional path violation on complete paired blocks. It also includes paraphrase and length-matched controls to bound simpler wording or extra-history effects.

### 6. What are the main results?
Direct task-macro FCR is 78.8%, and the mean over alternate histories is 78.7%, so the aggregate picture looks stable. But among 100 complete direct-success blocks, 35 fail on at least one contract-equivalent history, producing a 36.4% task-macro any-CPV estimate.

### 7. What is actually novel?
The novelty is the claim boundary. The paper does not ask whether an agent can solve the final task in isolation; it asks whether the same final contract is realized invariantly across contract-equivalent requirement histories.

### 8. What are the strengths?
The experimental design is unusually clean. Pairing is preserved, the verifier is executable, the controls are sensible, and the central result survives despite the lack of a dramatic aggregate collapse.

### 9. What are the weaknesses, limitations, or red flags?
The suite is still small, only 127 of 210 possible core-history blocks are complete, and attrition is substantial. The benchmark shows the existence of the failure mode, not a universal prevalence estimate or a mechanistic diagnosis of why the failures occur.

### 10. What challenges or open problems remain?
The big open problem is identifying which agent components actually cause the path sensitivity: memory handling, prompt resolution, scaffold policy, or something else. The paper also needs broader task coverage beyond the frozen five-family Python suite.

### 11. What future work naturally follows?
Explicit contract normalization layers, better requirement-state representations, and benchmark expansions to more repositories, languages, and natural conversation histories all follow naturally.

### 12. Why does this matter for cabbageland?
Cabbageland keeps caring about explicit state, memory, and tool-using agents. This paper gives a precise evaluation pattern for the difference between "saw the conversation" and "resolved the active contract."

### 13. What ideas are steal-worthy?
Use contract-equivalent history families as paired diagnostics. Preserve pairing instead of collapsing to mean success. Treat active-contract resolution as its own subproblem before implementation starts.

### 14. Final decision
Keep as a preserved note. The result is directly relevant to agent design and evaluation, and the paired benchmark framing is reusable well beyond this exact suite.

## 6. Mandatory critical angles

This paper is strongest on evaluation design and failure-boundary clarity. The main caution is that it diagnoses a real problem without yet telling us the dominant internal mechanism, so it should change how we test agents faster than it changes how we build them.

## 7. Writing style

The right tone is favorable but unsentimental. The paper deserves credit for naming the problem cleanly, but not for pretending a five-family benchmark settles the prevalence question.

## 8. Repository output format

Saved as a preserved paper note because active-contract resolution is a reusable concept, and conditional path violation is the kind of metric cabbageland should keep nearby when thinking about agent robustness.
