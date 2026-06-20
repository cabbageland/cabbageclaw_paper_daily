# DeepSWIP: Quotient-WMC Counterfactuals for Neural Probabilistic Logic Programs

## Basic info

* Title: DeepSWIP: Quotient-WMC Counterfactuals for Neural Probabilistic Logic Programs
* Authors: Saimun Habib, Vaishak Belle, Fengxiang He
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.20526
* Date surfaced: 2026-06-20
* Why selected in one sentence: It gives neural probabilistic logic programs an explicit single-world counterfactual transformation and makes calibration error visible in the weighted-model-count quotient.

## Quick verdict

* Highly relevant

This is a useful neurosymbolic causal-inference paper. I inspected the full arXiv PDF, including the transformation, propositions, experiments, appendix examples, and limitations. The paper is strongest where it draws a clean boundary: symbolic counterfactual inference can be exact relative to a materialized learned model while still being statistically wrong if the neural predicates are miscalibrated.

## One-paragraph overview

DeepSWIP extends single-world intervention programs to DeepProbLog-style neural probabilistic logic. For a fixed context, neural predicates are first evaluated and materialized into ordinary categorical ProbLog choices. The method then applies intervention surgery in a single transformed program instead of duplicating the endogenous structure into a Twin Network. Counterfactual queries are computed as a quotient of weighted model counts. This quotient form identifies which neural probabilities are active, which are removed by intervention cleaning, and where calibration or rare-evidence errors get amplified.

## Model definition

### Inputs
Inputs are finite-ground DeepProbLog programs with deterministic rules, ordinary probabilistic facts, neural predicates with finite output domains, fixed neural parameters, fixed input contexts, interventions, evidence, and counterfactual query atoms.

### Outputs
The method outputs counterfactual probabilities such as `P(Y_x = y | E = e)` under the materialized program. It also yields transformed single-world ProbLog programs, active probability sets, pruning behavior, and weighted-model-count numerator/denominator polynomials.

### Training objective (loss)
DeepSWIP itself is not a training method. It assumes learned neural predicates already produce categorical probabilities. The paper analyzes how error in those learned probabilities propagates through the WMC quotient. In the SUMO experiment, AIPW/DML is used only for a scoped randomized binary-treatment population estimand, not arbitrary individual counterfactuals.

### Architecture / parameterization
The architecture is a neurosymbolic inference layer: neural predictors produce probabilities over symbolic atoms; neural materialization converts those probabilities into ordinary ProbLog choices; SWIP-style program rewriting performs the intervention; weighted model counting computes the final quotient.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
DeepProbLog and related neural probabilistic logic systems can compose perception with symbolic rules, but ordinary conditional prediction is not counterfactual reasoning. Existing Twin Network counterfactual transformations duplicate endogenous program structure and are awkward for neural predicates.

### 2. What is the method?
DeepSWIP evaluates each fixed-context neural predicate once, materializes its categorical outputs as probabilistic choices, applies a single-world intervention transformation to the ordinary ProbLog program, and computes the counterfactual query through weighted model counting.

### 3. What is the method motivation?
The motivation is to separate neural perception uncertainty from causal-symbolic intervention semantics. Once neural outputs are materialized, intervention surgery should happen on explicit symbolic mechanisms rather than by re-evaluating or duplicating neural modules in two worlds.

### 4. What data does it use?
The paper uses MPI3D-toy images for visual factor counterfactuals and SUMO traffic simulations for an HOV policy calibration/DML stress test. MPI3D supplies factor labels for shape, size, color, and related symbolic rules. SUMO supplies paired restricted/open-lane potential outcomes and noisy traffic-state estimates.

### 5. How is it evaluated?
MPI3D checks DeepSWIP against a DeepTwin construction across 12,000 ProbLog calls and compares against factor-level ground truth. It reports predicate accuracies, calibration gaps, inference time, pruning, and RMSE/bias for symbolic queries. The SUMO experiment measures how neural calibration noise affects plug-in estimates and when a correctly scoped AIPW estimator reduces population-estimand bias.

### 6. What are the main results?
On MPI3D, DeepSWIP and DeepTwin agree on 100 percent of 12,000 queries. DeepSWIP averages 3.57 ms per query versus 7.65 ms for DeepTwin, a 2.14x speedup. RMSE is zero for intervention-determined queries and small for queries depending on non-intervened predicates. On SUMO, worsening congested-state calibration increases naive plug-in bias, while AIPW/DML stays near zero bias for the constructed randomized population estimands.

### 7. What is actually novel?
The novelty is the combination of neural materialization, single-world intervention rewriting, and quotient-WMC analysis for neural probabilistic logic programs. The quotient view is especially useful because it exposes active neural probabilities, intervention cleaning, calibration sensitivity, and rare-evidence instability in one algebraic object.

### 8. What are the strengths?
The paper is precise about assumptions and scope. It distinguishes exact symbolic inference from neural statistical error, avoids pretending DML solves every counterfactual query, and uses Twin agreement as an implementation correctness check rather than overclaiming semantics. The single-world transformation is also computationally cleaner than duplicating endogenous structure.

### 9. What are the weaknesses, limitations, or red flags?
The assumptions are strong: finite grounding, finite neural output domains, unique supported models, fixed neural contexts, and explicit causal structure. The MPI3D rules are intentionally simple and do not prove anything about realistic vision or physics. Approximate WMC, continuous variables, richer relational counterfactuals, and arbitrary path-specific effects are left open.

### 10. What challenges or open problems remain?
Open problems include approximate counterfactual WMC with denominator-aware error bounds, efficient influence functions for broader relational counterfactual estimands, calibration procedures for active neural predicates, and scaling the transformation to larger neural-symbolic programs with more complex causal structure.

### 11. What future work naturally follows?
Good follow-ups would combine DeepSWIP with calibrated neural predicates, add active-predicate diagnostics, test on less toy neurosymbolic perception tasks, and build tooling that reports which neural probabilities actually influence a counterfactual answer.

### 12. Why does this matter for cabbageland?
It is a clean example of explicit neural-symbolic boundaries. If a system uses learned perception inside causal or logical reasoning, it should know which learned probabilities are active, which are intervened away, and where calibration error can make an exact symbolic answer exactly wrong.

### 13. What ideas are steal-worthy?
Materialize neural outputs before symbolic surgery. Track active learned probabilities in structured inference. Treat counterfactual answers as quotients with denominator instability, not magic logic. Keep exactness claims relative to the model that was actually learned.

### 14. Final decision
Keep as a strong neurosymbolic reference. It is not a universal causal discovery method, but it is a precise counterfactual inference layer for programs whose causal structure is already explicit.
