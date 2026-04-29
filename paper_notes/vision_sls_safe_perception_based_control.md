# VISION-SLS: Safe Perception-Based Control from Learned Visual Representations via System Level Synthesis

## Basic info

* Title: VISION-SLS: Safe Perception-Based Control from Learned Visual Representations via System Level Synthesis
* Authors: Aleena Malik, Shuyu Zhan, Melanie N. Zeilinger, and Glen Chou
* Year: 2026
* Venue / source: arXiv, extended version of an RSS 2026 paper
* Link: https://arxiv.org/abs/2604.24894
* Date surfaced: 2026-04-29
* Why selected in one sentence: It shows a disciplined way to put learned visual abstractions inside a robust control pipeline without pretending the abstraction error disappears.

## Quick verdict

**Useful**

This is the most interesting adjacent paper from today’s sweep. It is not directly about world models or agent memory, but it does something cabbageland keeps wanting more papers to do: use a learned representation while preserving explicit uncertainty accounting and a controllable downstream interface. I inspected the abstract and substantial method text from the arXiv HTML, so confidence is good on the high-level method and control framing, but weaker on every proof and appendix-level calibration detail.

## One-paragraph overview

VISION-SLS tackles safe output-feedback control from high-dimensional RGB observations under partial observability and nonlinear dynamics. The approach first learns a low-dimensional observation map from pretrained visual features, then calibrates a state-dependent bound on the reduction error so the representation can be treated as a bounded disturbance rather than as perfect state. On top of that reduced observation, it synthesizes a causal affine time-varying output-feedback controller using system level synthesis, with a scalable solver based on sequential convex programming and Riccati recursions. The point is not fancy perception alone. The point is making learned perception compatible with certifiable control.

## Model definition

### Inputs
The method takes high-resolution RGB observations or other partial measurements, system dynamics, control constraints, and pretrained visual features that are reduced into a lower-dimensional observation representation.

### Outputs
The learned perception module outputs a reduced observation plus calibrated error bounds. The controller outputs control actions over a finite horizon under robust constraint-satisfaction objectives.

### Training objective (loss)
The perception side uses a learned reduced observation map with a dynamics-aware observability loss and calibrated state-dependent error overbounds, according to the accessible text. The controller itself is synthesized by solving a constrained optimization problem in the SLS parameterization rather than trained with a standard neural-policy loss.

### Architecture / parameterization
A hybrid stack: pretrained visual features, a learned low-dimensional observation map with calibrated uncertainty, and a causal affine time-varying output-feedback controller parameterized through system level synthesis for nonlinear systems.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Safe control from pixels is hard because visual observations are high-dimensional, partial, noisy, and not naturally compatible with robust-control guarantees. End-to-end learned controllers scale, but they are hard to certify. Classical safe control offers guarantees, but usually on lower-dimensional, structured observations.

### 2. What is the method?
- Start from pretrained visual features rather than raw pixels alone.
- Learn a reduced observation map that preserves the information needed for control.
- Calibrate a state-dependent error bound on that reduction.
- Treat the residual observation uncertainty as bounded disturbance.
- Synthesize an output-feedback controller in the SLS framework for the resulting nonlinear partially observed system.
- Solve the resulting optimization with sequential convex programming and Riccati-recursion structure for scalability.

### 3. What is the method motivation?
The motivation is to keep the useful scalability of learned visual abstraction while refusing to smuggle it into the controller as if it were exact state. If the representation error is explicit and bounded, then robust control machinery can reason about it instead of ignoring it.

### 4. What data does it use?
The visible text reports two simulated RGB visuomotor tasks, a 4D car and a 10D quadrotor, plus a 59D humanoid task with partial observations and a hardware TurtleBot experiment using onboard images.

### 5. How is it evaluated?
It is evaluated on safety, solve time, and control performance relative to baselines, with emphasis on whether the controller exhibits safe information-gathering behavior and remains within reachable tubes under uncertainty.

### 6. What are the main results?
The paper reports robust constraint satisfaction with calibrated uncertainty bounds, information-gathering behavior that actively reduces uncertainty, and stronger safety rate and solve times than baselines, including successful hardware deployment on a ground vehicle.

### 7. What is actually novel?
The novel part is the full bridge between learned visual abstraction and SLS-based robust output-feedback control. The paper does not merely use a foundation-model encoder in front of a controller. It calibrates the encoder’s error so the abstraction can enter the control problem as bounded uncertainty.

### 8. What are the strengths?
- It respects uncertainty instead of hiding it.
- The representation is there to support control guarantees, not just to improve a benchmark score.
- The method explicitly allows information-gathering behavior under partial observability.
- The hybrid stack is legible enough to analyze and debug.

### 9. What are the weaknesses, limitations, or red flags?
- This is still a fairly model-heavy control paper with substantial assumptions.
- The calibrated bounds may become loose or brittle in more open-ended real settings.
- The learned abstraction is useful, but not obviously reusable as a richer world state.
- The tasks are impressive for safe visual control, but they are still far from messy open-world embodied intelligence.
- I did not verify the proofs or the full calibration procedure in the appendices.

### 10. What challenges or open problems remain?
A major open problem is extending this kind of bounded-abstraction control beyond relatively structured tasks into broader embodied settings with object interaction, larger scene variability, and stronger nonstationarity. Another challenge is keeping guarantees meaningful when the perception side shifts out of distribution.

### 11. What future work naturally follows?
- Combine bounded learned observations with richer object- or graph-based state abstractions.
- Study how calibration degrades under domain shift and partial scene novelty.
- Explore whether explicit memory can be integrated while preserving robust output-feedback guarantees.
- Use similar contracts in action-conditioned or planning-oriented world models.

### 12. Why does this matter for cabbageland?
Because it demonstrates a taste principle cabbageland keeps circling: a learned representation should come with an interface contract. If the representation is uncertain, say how uncertain. If it is reduced, say what got lost. That discipline matters far beyond classical control.

### 13. What ideas are steal-worthy?
- Treat learned perceptual state as an abstraction with calibrated error, not as truth.
- Build downstream planning or control around bounded uncertainty on the abstraction.
- Use foundation-model features only when they can be inserted into a legible system contract.
- Preserve information-gathering behavior rather than assuming estimation and control can be separated.

### 14. Final decision
**Keep it as adjacent inspiration.** It is not a direct world-model paper, but it is unusually serious about making learned representations answer to a robust downstream interface, and that general design lesson is worth preserving.