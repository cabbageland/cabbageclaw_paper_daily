# OASIS: Observation-Action Space Alignment via SE(3) Trajectory Prediction for Robotic Manipulation

## Basic info

* Title: OASIS: Observation-Action Space Alignment via SE(3) Trajectory Prediction for Robotic Manipulation
* Authors: Xinzhe Chen, Sihua Ren, Liqi Huang, Haowen Sun, Mingyang Li, Xingyu Chen, Zeyang Liu, and Xuguang Lan
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2605.25829
* Date surfaced: 2026-05-26
* Why selected in one sentence: It makes a sharp representational claim that a manipulation policy should align its intermediate state with rigid-body action geometry by explicitly predicting an SE(3) end-effector trajectory.

## Quick verdict

**Highly relevant**

This is one of the cleaner recent arguments for explicit structure in robotic manipulation. The paper’s key idea is not just “add more spatial supervision,” but “make the intermediate state live closer to the action geometry itself.” I inspected substantial full-text arXiv HTML, including the abstract, introduction, problem formulation, design argument for aligned intermediates, architecture description, and headline results, but I did not fully audit the appendix or low-level implementation details.

## One-paragraph overview

OASIS starts from a simple criticism of both VLA-style policies and world-action models: even when they use richer vision features or predict future visual states, their decisive intermediate representation often still lives in observation space rather than in the rigid-body geometry where robot actions actually live. The proposed fix is to predict a camera-frame SE(3) end-effector trajectory as an intermediate target, then feed the pose-supervised hidden states from that predictor into an action decoder that outputs the action chunk. The point is not to replace learning with pure geometry. It is to give the policy a geometrically aligned internal state so the action decoder does less implicit recovery work.

## Model definition

### Inputs
The policy takes image observations, a language instruction, and the current robot end-effector state. Internally, it also extracts metric-depth features from the current image and fuses them with vision-language features.

### Outputs
The system predicts a horizon-matched camera-frame SE(3) end-effector trajectory as an intermediate representation, then outputs an action chunk consisting of relative 6-DoF actions plus gripper commands.

### Training objective (loss)
From the inspected text, the trajectory predictor is supervised against expert-demonstration pose trajectories, and the overall system is trained end to end from standard expert demonstrations without extra spatial labels or large-scale robot pretraining. I did not inspect enough low-level training detail to state the exact loss decomposition beyond pose-supervised trajectory prediction plus action-generation training.

### Architecture / parameterization
This is a hybrid visuomotor policy with three learned components: a 3D-aware feature encoder that fuses vision-language and metric-depth features, a transformer-style SE(3) trajectory predictor that uses horizon-indexed trajectory queries, and an action decoder conditioned on the trajectory predictor’s hidden states plus current robot state.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the mismatch between the geometry of robot action and the geometry of the intermediate states used by many current manipulation policies. Existing VLA and WAM approaches often ask the action decoder to infer rigid-body structure from image-space or visual-latent intermediates.

### 2. What is the method?
The method predicts an SE(3) end-effector trajectory in the camera frame as an intermediate target. A 3D-aware encoder builds fused visual, language, and depth features, a trajectory predictor converts those into pose-supervised hidden states and predicted future poses, and an action decoder emits the executable action chunk conditioned on those hidden states.

### 3. What is the method motivation?
The motivation is that adding depth, regions of interest, or future visual prediction still leaves the hard pose-recovery step implicit inside the decoder. If the task is geometric control, then the intermediate representation should expose geometry that is closer to the action space itself.

### 4. What data does it use?
The paper reports experiments on LIBERO, CALVIN ABC to D, and real-world multi-task manipulation across Franka Research 3 and Kinova Gen3 setups. Training supervision is derived from standard expert demonstrations rather than extra spatial annotations.

### 5. How is it evaluated?
It is evaluated by task success on simulation benchmarks, by average sequence length and multi-task success on CALVIN, by real-robot success across several task suites, by out-of-distribution perturbation tests, and by ablations that isolate the value of the SE(3) trajectory predictor.

### 6. What are the main results?
The paper reports a 97.6 percent average success rate across the four LIBERO suites, a 4.57 average sequence length and 83.3 percent success on CALVIN ABC to D over five consecutive tasks, and an 89.2 percent average real-world success rate across multi-task, spatial-relationship, and long-horizon suites. In the ablations described in the inspected text, adding the SE(3) trajectory predictor raises success from 89.5 to 95.2 percent on LIBERO-Long and from 91.6 to 99.0 percent on LIBERO-Spatial. I treat the qualitative lesson as stronger than the exact headline numbers, because I did not audit the full benchmark protocol in detail.

### 7. What is actually novel?
The paper’s real novelty is the alignment claim. It argues that a policy intermediate should be judged by whether it exposes a pose readout that lives closer to the rigid-body action space, rather than by whether it merely improves perception or predicts future visuals. The SE(3) trajectory is used as a geometrically aligned intermediate, not just as another side task.

### 8. What are the strengths?
- The design claim is crisp and easy to reason about.
- The explicit structure is in the control pathway, not only in auxiliary supervision.
- The framing cleanly distinguishes action-space alignment from observation-space enrichment.
- The ablations, at least as presented in the main text, seem aimed at the core claim rather than only overall benchmark wins.

### 9. What are the weaknesses, limitations, or red flags?
- The action decoder still absorbs a lot of the hard residual work, including frame conversion and contact dynamics.
- The method is geometry-biased, but not truly geometry-complete.
- The exact training-loss story and implementation details were not fully clear from the inspected sections.
- It is still a learned chunked policy, so long-horizon credit and memory limitations do not disappear just because the intermediate is better aligned.

### 10. What challenges or open problems remain?
A major open question is how far action-space alignment can go before one needs more explicit object state, contact state, or memory. Another is whether this idea scales to more severe partial observability, richer scene dynamics, or stronger embodiment transfer.

### 11. What future work naturally follows?
- Combine SE(3)-aligned intermediates with explicit object-centric or contact-centric state.
- Test whether aligned intermediates help long-horizon replanning or memory, not just chunked imitation.
- Compare against stronger explicit-state world-action models rather than mostly image- or latent-space baselines.
- Study whether the same alignment principle helps mobile manipulation and multi-object tasks.

### 12. Why does this matter for cabbageland?
Because it attacks a recurring failure mode in VLA and world-action model work: the explicit structure often sits beside the real policy rather than inside it. OASIS is a useful example of moving the explicit state closer to the actual decision interface.

### 13. What ideas are steal-worthy?
- Judge representation quality partly by whether it is aligned with the downstream action geometry.
- Use predicted pose trajectories as a decision-facing intermediate instead of only as auxiliary supervision.
- Keep geometric structure explicit even when the final controller remains learned.
- Separate observation-space enrichment from action-space alignment as two distinct design choices.

### 14. Final decision
**Keep.** This is a strong mechanism paper for anyone thinking about how explicit geometry should enter robot control. I would not treat it as a final answer to structured manipulation, but it is better than the usual “more visual context” story and worth preserving.
