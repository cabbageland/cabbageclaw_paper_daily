# ISLA: A Coordinate-Free, Measure-Weighted Transformer for Boundary-Driven PDEs

## Basic info

* Title: ISLA: A Coordinate-Free, Measure-Weighted Transformer for Boundary-Driven PDEs
* Authors: Peter Sharpe
* Year: 2026
* Venue / source: arXiv preprint, arXiv:2611.17141v1, November 12, 2026
* Link: https://arxiv.org/abs/2611.17141
* Date surfaced: 2026-11-15
* Why selected in one sentence: It separates physical boundary information from mesh/frame/query-set accidents, and tests each separation with a targeted intervention.

## Quick verdict

* Highly relevant

Preserve the measure-weighted invariant interface and the falsifiable ablations, not a generic claim of superior physics intelligence. Exact invariance has explicit hypotheses; the fast interior implementation uses approximations outside those hypotheses. The appendix's warning that an exact read can worsen an approximate-trained model is as useful as the headline accuracy.

**Read basis:** Full-text main paper, plus selected theorem/assumption and proof passages, architecture, AeroZoo protocol/loss/baselines, cost, and D.7 approximation/ablation appendices. No exhaustive proof audit, code execution, or independent artifact-release verification. The paper says an implementation will be available in NVIDIA PhysicsNeMo.

## One-paragraph overview

ISLA predicts steady boundary-driven PDE solutions from boundary meshes and conditions. Its boundary tokens exchange information through learned slices, but their learned states never receive raw coordinates: positions enter through distances and relative inner products to moving slice anchors. Every pooling operation over physical boundary tokens uses cell measure, with inclusion-probability corrections when subsampling. Declared physical scales nondimensionalize inputs and redimensionalize outputs. Interior locations read boundary information without changing it or interacting with other query locations. This makes rigid motions, units, sampling density, and query composition separately addressable. AeroZoo results are strong, AirfRANS remains better served by GLOBE, and conventional automotive benchmarks reveal smaller gains and some regressions.

## Model definition

### Inputs

One mesh per boundary-condition type: cell centroid, unit normal, area or boundary length, and prescribed values such as inlet velocity or outlet pressure. Global inputs include declared physical scales/directions and dimensionless material/flow quantities, including a Reynolds number when relevant. Interior tasks also supply requested query coordinates; signed distance and its direction are computed from the full boundary. Large interior cases use a 200,000-token draw from much larger meshes. Query locations are read-only, not physical integration tokens.

### Outputs

Scalar, vector, or tensor fields at surface cells or interior query locations. Examples are surface pressure/wall shear and volume velocity/pressure. AeroZoo predicts seven fields: velocity, pressure, and five turbulence quantities. Learned invariant coefficients multiply covariant geometric basis directions/tensor products; declared scales restore physical units.

### Training objective (loss)

Supervised prediction against CFD/other reference solutions, not a residual-minimizing physics-informed objective. The pose/discretization recipe uses Huber loss with delta one on standardized targets, measure-weighted for surface tasks. AeroZoo instead uses per-case relative L2 loss per field, velocity weighted three, with 200,000 interior queries and boundary tokens per case and step. The boundary-supervised variant additionally uses boundary pressure/velocity/wall-shear targets where not fixed by Dirichlet conditions. Dataset-specific recipes differ; there is no single universal Huber objective across all tables.

### Architecture / parameterization

A slice-attention transformer with 12 blocks, width 512, and 128 slices; approximately 66.3M surface or 67.5M interior parameters. Each block routes tokens to slices with measure-weighted softmax, forms anchor positions/normals, computes relative invariant scalars, refines routing, transforms slice states with MLPs, and reads them back. There is no slice-to-slice self-attention. Interior queries additionally attend through a learned geometry/content boundary kernel, tree-accelerated at opening angle theta=1 by default; theta=0 is the exact read. Boundary encoding is reused across independently processed query chunks.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

A surrogate can learn the dataset's presentation instead of the physical problem. Rotating geometry together with all conditions should rotate vector outputs, not destroy predictions. Increasing sample density in one region should not increase that region's physical influence. Asking for extra output locations should not change predictions at the old ones. Ordinary benchmark errors can conceal all three defects.

### 2. What is the method?

1. Compute an intrinsic length from the boundary's RMS pairwise distance. Declare speed/density and other necessary scales explicitly; pass dimensionless quantities to learned maps.
2. Weight a boundary-token softmax by represented measure, equivalently adding log-measure to its logits. For subsampling use area/inclusion probability; normalize named conditions separately with learned shares.
3. Pool soft slice anchors from positions/normals that move with the object. Give learned maps only distances, log-distances, and inner products among co-transforming directions.
4. Update invariant scalar token states. Form physical vector/tensor outputs only through covariant basis directions.
5. Let an interior query read the boundary/slices without contributing to any shared sum. Approximate distant boundary clusters as virtual weighted tokens for speed.

The learned slices are an explicit numerical bottleneck, not named physical parts. Pictures of wheel-like slices do not establish causal semantic modularity.

### 3. What is the method motivation?

Boundary-integral methods already expose relative geometry, integration measure, and independent field queries. ISLA combines those interface properties with learned slice pooling without assuming a linear PDE. The point is to constrain nuisance dependence while preserving expressive learned interactions, not to derive Navier-Stokes or make all intermediate features vector-valued.

### 4. What data does it use?

AeroZoo contains 3,815 released time-averaged RANS cases; the study uses 2,816 with converged averages. The full split has 2,011 training, 290 validation, and 515 test cases. It varies geometry families, eight boundary layouts, size 0.02-20 m, speed 0.25-50 m/s, Reynolds numbers 1,000-100 million, and pose. Other datasets are AirfRANS and automotive DrivAerML, WindsorML, and AhmedML; pose/resampling tests also cover additional aerodynamic and solid-mechanics tasks. These are numerical reference solutions, not measurements demonstrating unrestricted real-world physical generalization.

### 5. How is it evaluated?

Field-wise relative L2 errors and reference-scaled volume errors, using physical cell measures/volumes in scoring. AeroZoo also compares with a constant free-stream predictor and holds out geometry families, Reynolds ranges, or layouts. Presentation tests rotate/translate the entire PDE, including conditions and targets, or resample cells by area. Architectural ablations remove one rule and retrain. Comparators include Transolver, GeoTransolver, and GLOBE, with explicit boundary-condition/nondimensionalization variants where applicable. Main automotive entries involve tuned ensembles; some reported outcomes use validation rather than held-out test cases and must remain labeled that way.

### 6. What are the main results?

- **AeroZoo:** Interior-only mean reference-scaled velocity/pressure errors are 0.082/0.298, versus scaled, boundary-conditioned GeoTransolver's 0.294/1.292. ISLA beats free-stream velocity on 98% of full-split test cases. Additional boundary targets reduce pressure error to 0.171 at 1.46 times training step cost.
- **Mechanism controls:** Equal-count pooling retains stored-case accuracy but gives 11 times the reference model's pressure error after area resampling. Adding centered/scaled coordinates slightly improves stored-case fit but gives 21 times the reference error under rotation. Removing all anchor relations gives about 71% pressure error across presentations.
- **AirfRANS:** GLOBE wins all four primary full-split fields. ISLA's errors are at least 1.6 times lower than Transolver/GeoTransolver's, but angle-of-attack extrapolation raises every family's error substantially.
- **Automotive:** Full-data surface gains are modest; volume velocity can be 9-13% worse than tuned GeoTransolver on DrivAerML and 27-30% worse on full AhmedML. On DrivAerML's 11-training-case split, ISLA's validation errors are 8-13% lower across four fields.
- **Approximation matters:** Retraining AirfRANS with an exact read gives errors within 0.9% of the approximate-read recipe at 2.7 times step time. Merely switching approximate-trained weights to exact evaluation worsens errors 2.0-5.1 times.

The strong claim is targeted robustness plus competitive prediction, not dominance on every CFD benchmark.

### 7. What is actually novel?

The contribution is the combination of invariant slice-anchor relations, physical-measure-aware routing, declared scale handling, and independent boundary-reading queries, with explicit guarantees and intervention tests. Equivariant scalar-to-tensor maps, quadrature/importance weights, proportional attention, boundary kernels, and read-only query decoders have precedents. Do not credit ISLA with inventing these ingredients or with being the first equivariant physical surrogate generally.

### 8. What are the strengths?

- Architectural rules correspond to independently testable invariances.
- Boundary values are explicit inputs rather than missing information quietly blamed on insufficient scale.
- Frozen prediction at one query is independent of which other queries are requested, even with the approximate read and fixed boundary draw.
- Measure-aware pooling addresses representation bias from the mesher, not merely training augmentation.
- Reports topology failures, competing-model wins, approximation dependence, and high memory costs.
- A smaller-model/sampling control weakens a simplistic parameter-count explanation of AeroZoo's gains.

### 9. What are the weaknesses, limitations, or red flags?

**Exact versus deployed operator:** Exact rigid-motion/reflection/unit claims need full-cell tokenization, suitable weight-floor conditions, and, for interior outputs, theta=0 plus closed-boundary/unique-closest-point assumptions. The scalable token draw and principal-axis-ordered tree introduce effects outside that theorem. Tiny numerical/approximation sensitivity is measured, not magically absent.

**Remeshing:** Consistency means convergence along refining meshes with converging normals and suitable continuous data. It is not invariance under arbitrary finite remeshes. The formal refinement result removes the weight floor; an implementation with a fixed floor is not the same asymptotic object.

**Baseline fairness:** AeroZoo baselines are single seeds at 9.0M/27.6M parameters, versus four ISLA seeds near 67.5M. The 28.2M control helps but also changes token budget and schedule; it does not equalize every compute/data choice. Uniform SO(3) augmentation largely fixes baseline rotation changes at a small stored-error cost. Compare that recipe rather than declaring augmentation categorically ineffective.

**Physical scope:** No exact conservation, PDE residual, calibrated uncertainty, contact dynamics, or long-horizon rollout guarantee. A deterministic equivariant map cannot select a unique symmetry-breaking instantaneous wake from symmetric inputs. Units invariance requires declaring the relevant dimensional information; omitting Reynolds number can collapse distinct physical sizes to the same prediction.

**Engineering:** Large 3D interior training exceeds 80 GiB per GPU even with memory optimizations. Sampling, spatial searches, tree building, boundary complexity, and query count matter in addition to nominally linear attention. Code was not executed here.

### 10. What challenges or open problems remain?

Generalization to unseen boundary topology is weak: some held-out layouts are only slightly better than free stream, and held-out non-box enclosures can be worse. Intrinsic length changes when a far-field truncation boundary changes. Approximation and learned weights co-adapt, complicating claims about improving discretization after training. Instantaneous multimodal flows, unsteady forcing, unknown conditions, and uncertainty are outside the main demonstration.

### 11. What future work naturally follows?

Test unseen layouts with matched boundary-conditioned baselines and evaluate geometry, condition, and topology shifts separately. Train across tree angles/token budgets before asking for resolution-adaptive inference. Add conservation/residual diagnostics without conflating them with field error. Study stochastic equivariant outputs for symmetry-breaking solutions. Audit whole-pipeline memory/time against augmented smaller models and direct boundary-integral alternatives.

### 12. Why does this matter for cabbageland?

This is a concrete interface-design reference for physical models and compositional generation. Physical support, numerical sampling, and requested outputs should not silently share the same status in a learned representation. The transfer is a disciplined way to define nuisance transformations and write adversarial tests for them, not evidence that an aerodynamic surrogate is already a robotics world model.

### 13. What ideas are steal-worthy?

- Add log represented-measure to pooling logits when tokens approximate an integral; use inclusion probabilities for actual sampling corrections.
- Separate physical-condition inputs from geometric observation density.
- Derive moving anchors from the represented object instead of imposing an unstable canonical frame.
- Keep query tokens read-only when outputs should be independent of requested batch composition.
- Test each claimed invariance by removing its enabling rule while retaining ordinary fit.
- Treat the numerical approximation as part of the learned model. Better quadrature at inference need not mean better predictions after approximation-specific training.
- Report a cheap physically meaningful null predictor and unseen-layout failures alongside aggregate relative error.

### 14. Final decision

Preserve as a **highly relevant architecture and evaluation reference**. The keeper is the measure/invariance/query separation plus its ablations. Before implementation, verify released code and reproduce a small pose/resampling/query test; before claiming physical generalization, add boundary-topology, approximation-mismatch, residual, and uncertainty checks. Do not turn a conditional exact-operator theorem into an unconditional guarantee for the fast deployed network.
