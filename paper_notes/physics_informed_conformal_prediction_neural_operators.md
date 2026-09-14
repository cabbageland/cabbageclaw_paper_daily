# Physics-Informed Conformal Prediction: Embedding PDE Consistency into Distribution-Free Uncertainty Quantification for Neural Operators

## Basic info

* Title: Physics-Informed Conformal Prediction: Embedding PDE Consistency into Distribution-Free Uncertainty Quantification for Neural Operators
* Authors: Michael Chin
* Year: 2026
* Venue / source: arXiv:2609.11935
* Link: https://arxiv.org/abs/2609.11935
* Date surfaced: 2026-09-14
* Why selected in one sentence: It uses PDE residuals to make conformal prediction intervals spatially adaptive while preserving split-conformal marginal coverage.

## Quick verdict

* Highly relevant

This is useful because it joins two things that often stay separate: distribution-free uncertainty and physical consistency. The core score is simple, and the coverage argument is just standard split conformal exchangeability after redefining nonconformity. The caveat is equally important: the method helps when residual magnitude correlates with prediction error, and can over-widen when that assumption fails.

## One-paragraph overview

The paper proposes Physics-Informed Conformal Prediction, or PI-CP, for neural PDE operators. Instead of calibrating on raw absolute prediction error, it calibrates on error divided by 1 plus a weighted PDE residual. The final interval is then widened locally by that same residual factor, so predictions that violate the governing equation receive wider intervals. The paper also shows that vanilla FNO translation equivariance is structurally mismatched to nontrivial Dirichlet boundary conditions, and validates coordinate channels as a practical fix.

## Model definition

### Inputs

The method takes a trained neural operator prediction, calibration inputs and outputs, a PDE differential operator or residual evaluator, a target miscoverage level, and a physics weight lambda. Test-time inputs are PDE parameters or fields such as conductivity, permeability, source terms, or state histories depending on the scenario.

### Outputs

The method outputs prediction intervals around the neural operator prediction. For each test point, the interval width is scaled by the magnitude of the PDE residual at that predicted solution.

### Training objective (loss)

PI-CP itself is a post-training conformal calibration method and does not change the neural operator training loss. The underlying FNO models are trained for PDE solution prediction; the conformal score is computed after training. The paper also evaluates coordinate-aware FNOs but the uncertainty method is calibration-time, not a new supervised loss.

### Architecture / parameterization

The base predictor is an FNO2d/3d with coordinate channels, modes 12, width 32, four layers, and about 1.19M parameters. PI-CP parameterizes uncertainty through the nonconformity score s = |y - f(x)| / (1 + lambda |R(x)|), where R(x) is the PDE residual of the prediction.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Neural operators can predict PDE solutions quickly, but they usually lack reliable uncertainty intervals. Standard conformal prediction gives marginal coverage but tends to use one global width, ignoring where the predicted solution is physically inconsistent.

### 2. What is the method?

Compute the PDE residual for each calibration prediction. Define nonconformity as absolute error divided by 1 + lambda times residual magnitude. Take the conformal quantile of those scores. At test time, output f(x) plus/minus qhat times 1 + lambda times the test residual magnitude.

### 3. What is the method motivation?

A PDE residual is a physically meaningful error indicator. If the predicted field violates the governing equation, uncertainty should widen there. If the prediction satisfies the physics, intervals can remain tighter.

### 4. What data does it use?

The paper evaluates six physics scenarios: 2D/3D heat conduction, 2D/3D structural mechanics, 2D Darcy flow, and 2D Navier-Stokes Taylor-Green vortex. The experiments use 1000 to 2000 training samples per scenario, 200 calibration samples, and 300 test samples.

### 5. How is it evaluated?

It measures empirical coverage, interval width, spatial adaptivity via width coefficient of variation, coordinate-channel ablations, architecture ablations, and baseline comparisons against CNN, DeepONet, and MGN on Darcy flow.

### 6. What are the main results?

On Darcy flow, standard CP and PI-CP both hit about 89.4-89.7% empirical coverage for a 90% target. PI-CP with lambda=1 gives width CV 0.221 with only 1.04x average width relative to standard CP. With lambda=5, CV rises to 0.643 but average width becomes 1.31x. Coordinate channels are crucial: Darcy flow error drops from 63.37% without coordinates to 1.00% with coordinates, a 63.4x improvement; strong 3D Dirichlet cases show similar large gains.

### 7. What is actually novel?

The novelty is using the PDE residual inside the conformal score and then returning the residual-scaled interval while retaining the split-conformal exchangeability guarantee. The coordinate-aware FNO theorem is not the main uncertainty contribution, but it is a useful architectural warning.

### 8. What are the strengths?

The method is simple and easy to retrofit. It preserves marginal coverage under standard split-conformal assumptions. It gives a clear knob, lambda, for adaptivity versus width. It explicitly analyzes the FNO boundary-condition mismatch.

### 9. What are the weaknesses, limitations, or red flags?

The method depends on residual-error correlation. The paper itself notes that if residuals are dominated by discretization or are poorly aligned with true error, PI-CP can over-widen without improving conditional reliability. Coverage remains marginal, not true conditional coverage. The experiments are modest-sized and mostly controlled PDE benchmarks.

### 10. What challenges or open problems remain?

The big open problem is robust conditional coverage when physics residuals are imperfect error proxies. Other questions: how to choose lambda, how to handle learned residual surrogates, and how the method behaves under distribution shift or real simulator mismatch.

### 11. What future work naturally follows?

Test PI-CP on harder PDE families and operational solvers; learn or calibrate residual-error mappings; combine residuals with epistemic uncertainty; and evaluate under OOD boundary conditions or parameter distributions.

### 12. Why does this matter for cabbageland?

It is a good example of uncertainty using an explicit structural variable rather than a black-box confidence score. That is relevant to scientific ML, world models, calibration, and safety gates.

### 13. What ideas are steal-worthy?

Use physically meaningful residuals as local interval carriers. Keep conformal validity by putting the structure into a deterministic score. Audit architecture symmetries against boundary conditions before trusting operator performance.

### 14. Final decision

Preserve. It is a compact and reusable uncertainty design, with clear caveats.
