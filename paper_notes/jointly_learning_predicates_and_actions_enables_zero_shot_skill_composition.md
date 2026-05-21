# Jointly Learning Predicates and Actions Enables Zero-Shot Skill Composition

## Basic info

* Title: Jointly Learning Predicates and Actions Enables Zero-Shot Skill Composition
* Authors: Benedict Quartey, Sebastian Castro, Eric Rosen, Wil Thomason, George Konidaris, and Stefanie Tellex
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2605.20648
* Date surfaced: 2026-05-21
* Why selected in one sentence: It is a rare recent robot learning paper that gives compositionality a real symbolic interface inside the skill model instead of pretending raw trajectory generation alone will solve recomposition.

## Quick verdict

* Useful

This is a thoughtful and fairly honest hybrid-systems paper. Its best move is to jointly generate action trajectories and predicate-belief trajectories, so the skill model itself carries an online outcome trace that planners can use for sequencing and monitoring. The price is obvious and important: the symbolic interface still depends on manually designed predicates, operators, and planning domains.

## One-paragraph overview

The paper introduces Predicate-Action Skills, or PACTS, a class of closed-loop generative robot skills that model a joint distribution over action trajectories and predicate-belief trajectories conditioned on current observations. Instead of learning only how to act, the model learns how the symbolic state is expected to evolve while acting. At inference time that predicted predicate trace becomes an online interface for skill composition: a planner chooses which skill to run next, execution can be monitored against expected predicate changes, and replanning can happen when the symbolic rollout deviates from the goal. This is a much cleaner composition story than training an action policy and a separate predicate classifier independently.

## Model definition

### Inputs
The model takes current observations and conditions on the current skill context. During training it also uses paired action trajectories and predicate label trajectories extracted from demonstration data. In composition mode it additionally consumes initial and goal predicate conditions from the symbolic planner.

### Outputs
The model jointly predicts an action trajectory chunk and a predicate-belief trajectory over the same horizon. The predicate output is continuous during generation and can be thresholded into discrete symbolic state estimates for planning and monitoring.

### Training objective (loss)
The paper implements the joint action-predicate rollout model using diffusion and conditional flow-matching formulations. The exact optimization target depends on the chosen backbone, but in both cases the training objective is the generative denoising or flow objective over the coupled action and predicate trajectories. I inspected the full arXiv text, but I did not independently re-derive every low-level hyperparameter from the appendix.

### Architecture / parameterization
A conditional generative visuomotor policy over coupled action and predicate trajectories, instantiated with DDPM and conditional flow-matching variants. The model predicts both modalities within a single backbone rather than with separate post hoc modules. Composition at test time uses off-the-shelf symbolic planning over predicates, with the learned model providing online predicate-belief traces during execution.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Robots can often learn short-horizon skills from demonstrations, but recomposing those skills into new long-horizon tasks usually requires either retraining or hand-built symbolic scaffolding. Action-only generative policies do not expose the symbolic outcomes needed for robust composition, monitoring, or replanning. The paper tries to make learned skills composable by giving them an explicit outcome trace.

### 2. What is the method?
PACTS models each skill as a joint generative process over an action trajectory and a predicate-belief trajectory. Starting from noise, the model denoises both modalities together to produce a coherent action-outcome rollout. At execution time the robot samples an action chunk and the associated predicate rollout, executes a short prefix of the action, re-observes, and resamples. The predicted predicate trajectory becomes an online symbolic interface for a planner, which uses preconditions and effects over predicates to sequence skills and revise plans when needed.

### 3. What is the method motivation?
The motivation is that composition requires knowing not just what action to emit, but what state transition that action is supposed to cause. If the same learned object predicts both the motor behavior and the expected symbolic change, then planning and execution monitoring can be attached to something more coherent than a policy plus an independent classifier.

### 4. What data does it use?
The paper evaluates on a controlled 2D compositional benchmark called PushBarrier and on 3D manipulation tasks from RoboMimic with MimicGen demonstrations, specifically Kitchen and Coffee Preparation. The pipeline includes a skill segmentation and labeling toolkit that converts monolithic demonstrations into skill-centric training examples with paired predicate traces.

### 5. How is it evaluated?
There are two layers of evaluation. First, single-policy rollout evaluation checks whether joint modeling harms or helps action performance and predicate prediction when learning one policy per task without composition. Second, planning-based composition evaluation tests whether the predicted predicate traces actually support zero-shot recomposition and monitoring. The paper also measures predicate-action coherence, meaning whether the predicted symbolic rollout agrees with the realized outcome of the generated actions.

### 6. What are the main results?
The main result is qualitative but meaningful: across PushBarrier and RoboMimic settings, jointly modeling predicate beliefs with actions maintains competitive action performance while usually improving predicate classification and outcome coherence relative to action-only or loosely coupled baselines. The paper’s strongest claim is not that PACTS crushes every action metric, but that it makes skill composition and monitoring possible without giving up ordinary policy competence. I inspected the full text, but the extracted PDF text in this environment did not preserve all table values cleanly, so I am more confident in the directional result and evaluation design than in every exact reported number.

### 7. What is actually novel?
The novelty is putting the symbolic outcome trace inside the generative skill rollout itself. That is better than a separate predicate predictor attached after policy learning, and better than treating symbolic abstraction as entirely external to the motor model. The contribution is really an interface design for compositional skill execution.

### 8. What are the strengths?
The paper asks the right question about composition. It evaluates predicate-action coherence instead of only downstream return. It is also admirably clear about where symbolic structure lives: in the predicate vocabulary, the planner, and the online rollout interface. The open-source skill segmentation and labeling pipeline also makes the paper more operational than many hybrid-policy proposals.

### 9. What are the weaknesses, limitations, or red flags?
The core limitation is manual symbolic structure. Predicate coverage and quality matter a lot, and the planning setup assumes a hand-defined PDDL-style domain with operators and goals. Joint modeling improves coherence but does not remove perception errors, aliasing, or distribution shift. There is also still a gap between success on curated skill vocabularies and truly open-ended abstraction discovery.

### 10. What challenges or open problems remain?
Automatic predicate discovery, automatic operator discovery, and more robust abstraction under partial observability remain open. The approach also needs testing on broader task families where the symbolic state is less cleanly enumerable and where skill boundaries are noisier.

### 11. What future work naturally follows?
Learn or propose predicates from richer pretrained perceptual models instead of fully manual vocabularies. Study whether the joint outcome trace can support more flexible replanning and failure recovery in longer tasks. Compare joint action-predicate generation against stronger fully end-to-end baselines on harder compositional benchmarks.

### 12. Why does this matter for cabbageland?
Because it is a clean example of **explicit symbolic state doing real work without fully replacing learned control**. The steal-worthy idea is not nostalgia for PDDL. It is the tighter contract: a skill should predict both what it will do and what state change it expects to cause.

### 13. What ideas are steal-worthy?
Jointly model motor rollout and state-transition belief. Evaluate symbolic interfaces with coherence metrics, not only downstream reward. Use predicted outcome traces as online monitors for skill sequencing and failure detection. Treat composition as an interface-design problem between learned control and reusable abstractions.

### 14. Final decision
Worth keeping as a compositional robotics reference. It does not solve abstraction discovery, but it states the problem cleanly and offers a better hybrid interface than most recent “compositional” robot policy papers.
