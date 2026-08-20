# A Jagged Frontier: Evaluating Robustness of Code Agents to Semantics-Preserving Transformations

## Basic info

* Title: A Jagged Frontier: Evaluating Robustness of Code Agents to Semantics-Preserving Transformations
* Authors: Hasan Najib Mahmud, Shreya Gupta, Isha Chaudhary, Nathaniel Enis, Ravi Mangal, Gagandeep Singh, Corina Pasareanu
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.18389
* Date surfaced: 2026-08-20
* Why selected in one sentence: It is the cleanest code-agent robustness paper in the batch because it isolates scaffold-sensitive brittleness under semantically equivalent repository rewrites instead of hiding behind single-run benchmark noise.

## Quick verdict

* Highly relevant

I inspected the arXiv HTML full text. This is a useful robustness paper because it tests the right thing the right way: semantically equivalent code perturbations, repeated paired runs, and separate accounting for solve-rate loss versus extra effort. The resulting effect sizes are not apocalyptic, but the paper still lands a serious blow against naive benchmark rankings.

## One-paragraph overview

The paper evaluates whether repository-level code agents remain reliable when the surrounding codebase is rewritten through semantics-preserving transformations. It contributes a catalog of **14** transformations, a randomized variant sampler that perturbs real repositories without changing test-suite behavior, and an experimental design that repeatedly runs the same agent on the original and perturbed variants to estimate resolve-rate degradation while controlling for stochastic agent noise. Two scaffolds, mini-SWE agent and OpenCode, are paired with four frontier models across SWE-bench Verified and SWE-bench Pro. The main result is not massive collapse. It is something more annoying and more useful: robustness is jagged, scaffold-dependent, and often shows up first as increased cost and search confusion rather than spectacular solve-rate failure.

## Model definition

### Inputs
The evaluation pipeline takes a repository-level issue instance, the base repository state, a semantically equivalent perturbed variant created by one or more transformations, and a scaffolded code agent backed by a frontier model.

### Outputs
It outputs a candidate patch, pass/fail outcomes against FAIL_TO_PASS and PASS_TO_PASS tests, step counts, token cost, and paired degradation estimates between unperturbed and perturbed runs.

### Training objective (loss)
There is no new trainable model or learning loss. The paper is an evaluation and perturbation framework for existing code agents.

### Architecture / parameterization
The core architecture is a transformation catalog plus randomized variant sampler, coupled to repeated agent runs under two scaffolds and multiple frontier models, with resolve-rate, effort, and cost diagnostics.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to measure whether code-agent benchmark performance survives semantically irrelevant codebase rewrites, or whether agents are quietly brittle to surface form.

### 2. What is the method?
The method is to generate semantics-preserving repository variants, run agents repeatedly on both original and perturbed versions, and estimate paired resolve-rate degradation plus effort overhead.

### 3. What is the method motivation?
A single failed run on a perturbed repo proves almost nothing because these agents are stochastic. The right question is whether the perturbation changes the paired distribution of outcomes, effort, and cost across repeated runs.

### 4. What data does it use?
The experiments use **54** instances drawn from SWE-bench Verified and SWE-bench Pro. For each instance, the paper reports baseline resolve rates from **20** unperturbed runs and perturbed resolve rates from **20** variant runs.

### 5. How is it evaluated?
It is evaluated across two scaffolds, four frontier models, and two benchmarks using mean resolve-rate degradation, step overhead, cost overhead, and qualitative trajectory inspection.

### 6. What are the main results?
The worst affected configurations show a mean resolve-rate drop of up to **6.7** percentage points, with statistically significant degradations in **6 of 16** scaffold-model-dataset configurations. Even when solve rate moves little, effort often rises: on SWE-bench Verified, cost increases in all eight configurations, reaching up to **22.9%**, while step count increases by up to **9.9%**. Qwen is among the most robust models in mini-SWE on SWE-bench Verified yet the most brittle under OpenCode, which is exactly the paper's main point.

### 7. What is actually novel?
The novelty is not merely "perturb code and test agents." It is the combination of repository-level semantics-preserving transformations, repeated paired evaluation that separates perturbation effect from intrinsic stochasticity, and the claim that robustness rankings are scaffold-relative.

### 8. What are the strengths?
The experiment design is much better than the usual single-run robustness theater. The paper also looks past final solve rate to effort and cost, which is where a lot of real deployment pain shows up first.

### 9. What are the weaknesses, limitations, or red flags?
The study is still limited to **54** instances and a non-adversarial random perturbation process, so the reported degradations should be read as lower bounds rather than worst-case brittleness. Test-suite equivalence is also an empirical operationalization of semantic equivalence, not a formal proof.

### 10. What challenges or open problems remain?
The next open problem is mitigation: can agent localization, search, and planning be made invariant to this kind of superficial rewrite pressure without just brute-forcing more context?

### 11. What future work naturally follows?
Future work should test adversarially selected transformations, broader language ecosystems, and robustness-aware scaffolds that explicitly defend against grep decoys, dead-code distractions, and superficial control-flow rewrites.

### 12. Why does this matter for cabbageland?
Because it directly attacks a false comfort that benchmark rows often provide. A repository can remain semantically identical for tests and humans while still becoming materially harder for an agent to search, localize, and patch.

### 13. What ideas are steal-worthy?
Use repeated paired runs instead of one-shot robustness claims. Measure cost-per-step and context inflation, not just pass rate. Add semantics-preserving rewrite checks when evaluating code agents. Treat scaffold choice as part of the robustness story.

### 14. Final decision
Keep as a preserved note. This is exactly the kind of benchmark-severe paper future-us will want when thinking about code-agent trustworthiness.

## 6. Mandatory critical angles

This paper is strongest on evaluation fairness, failure-mode exposure, and deployment realism. It shows that semantic equivalence for a program is not automatically semantic equivalence for an agent's search process. The main caution is that the effect sizes are lower-bound and the instance count is still modest.

## 7. Writing style

The right tone is approving and slightly annoyed. The paper earns that tone by puncturing benchmark complacency without overselling disaster.

## 8. Repository output format

Saved as a preserved paper note because the scaffold-sensitive robustness lesson is directly relevant to how cabbageland should evaluate code and terminal agents.
