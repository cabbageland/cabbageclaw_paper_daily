# NEMSim: Learning Control-Conditioned Multi-Event Physical Dynamics via Executable Event-Mechanism Priors

## Basic info

* Title: NEMSim: Learning Control-Conditioned Multi-Event Physical Dynamics via Executable Event-Mechanism Priors
* Authors: Junsong Yu, Junjie Xie, Pengwei Liu, and Dong Ni
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2609.30718
* Date surfaced: 2026-09-28
* Why selected in one sentence: It turns discrete event-rule knowledge into an executable neural transition structure for long-horizon physical dynamics.

## Quick verdict

**Highly relevant**

NEMSim is useful because it is not satisfied with giving a neural operator a bag of prior features. It makes event rules operational through event intensity, mechanism attribution, and state response compilation, then shows that this structure matters in 100-step rollouts.

## One-paragraph overview

NEMSim studies control-conditioned multi-event physical systems where macroscopic dynamics emerge from many localized events. The concrete benchmark is a 3D KMC-based plasma-etching simulator with explicit event rules and process controls. Instead of learning a pure state-control transition, NEMSim compiles the event-rule library into an executable transition structure: event intensities are computed from controls and rule attributes, events are attributed to shared mechanism families, and mechanism drives produce state-dependent responses. The model still trains only from one-step state transitions, but its architecture forces the learned update to pass through an event-mechanism organization.

## Model definition

### Inputs
Inputs are the current 3D state field, a 14-dimensional process-control vector, and a fixed event rules library containing control bindings, probability relations, yield relations, dependencies, and event-mechanism roles.

### Outputs
The model outputs the next normalized 3D signed-distance-field state. In rollout evaluation, this prediction is fed back autoregressively for 100 steps.

### Training objective (loss)
Training minimizes voxel-wise mean squared error between predicted and ground-truth next states. There is no event-level, mechanism-level, or rollout-loss supervision.

### Architecture / parameterization
NEMSim uses a state encoder, an Event-Mechanism Compiler, and a Mechanism Response Compiler. The compiler constructs event intensities, bounded rule corrections, event-to-mechanism attributions, and state-dependent response modes from fixed rule priors plus learned corrections.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Purely data-driven physical surrogates struggle when expensive trajectories cannot cover all control-state-event combinations. Standard physics-guided methods do not naturally use discrete event-rule priors.

### 2. What is the method?
Compile event attributes into an executable transition factorization: controls and rules determine base event intensities, event descriptors and state context route events to mechanism families, and learned response modules translate mechanism drives into state updates.

### 3. What is the method motivation?
In multi-event systems, many specific events share a smaller set of mechanisms. Encoding that organization should improve extrapolation and reduce long-horizon error accumulation.

### 4. What data does it use?
The benchmark contains 500 high-fidelity 3D KMC trajectories, each with 101 two-channel 3D signed-distance fields and 100 transitions on a 127 x 54 x 54 grid. Splits are trajectory-level.

### 5. How is it evaluated?
The paper evaluates 100-step autoregressive rollouts under control interpolation, control extrapolation, and temporal extrapolation. Metrics include average rollout RMSE, final-step RMSE, final-step Chamfer distance, and parameter count. Baselines include ConvLSTM, FNO, U-NO, CNO, DeepONet, and prior-feature variants.

### 6. What are the main results?
NEMSim reduces Avg. RMSE by 63.3% under Control-ID versus DeepONet, by 58.9% under OOD-Joint versus the strongest standard baseline, and by 81.3% under Vis-50 temporal extrapolation. It also beats CNO+Prior and DeepONet+Prior, indicating that prior access alone does not explain the gains.

### 7. What is actually novel?
The novelty is executable event-mechanism compilation from discrete rule attributes, not merely adding physics features or residual penalties.

### 8. What are the strengths?
The benchmark is well-structured: trajectory-level splits, explicit controls, rule perturbation studies, data-efficiency tests, and prior-access controls. The model is also compact at about 0.253M trainable parameters.

### 9. What are the weaknesses, limitations, or red flags?
The evaluation is limited to one plasma-etching style benchmark. The rollouts are deterministic and assume predefined event-attribute descriptions. The method needs a meaningful event-rule library up front.

### 10. What challenges or open problems remain?
The next hard problems are probabilistic rollouts, uncertainty over rules, automatic event discovery, and transfer to domains where event rules are partial or wrong.

### 11. What future work naturally follows?
Apply the executable-prior idea to robotics contact events, chemical reaction systems, traffic/fleet control, and agent-environment simulators with known discrete mechanisms.

### 12. Why does this matter for cabbageland?
It is a strong template for "explicit structure that does work." The rule library is not decorative; it defines how the transition must be computed.

### 13. What ideas are steal-worthy?
Separate event intensity, mechanism attribution, and state response. Compare executable priors against prior-feature baselines. Evaluate whether structure helps under long autoregressive rollout, not only one-step prediction.

### 14. Final decision

**Preserve.** This is a strong scientific world-model/control paper with a mechanism that transfers beyond plasma etching.
