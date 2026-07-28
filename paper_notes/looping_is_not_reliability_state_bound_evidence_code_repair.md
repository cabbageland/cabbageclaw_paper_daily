# Looping Is Not Reliability: State-Bound Evidence and Typed Revision Contracts for Agentic Code Repair

## Basic info

* Title: Looping Is Not Reliability: State-Bound Evidence and Typed Revision Contracts for Agentic Code Repair
* Authors: Xueping Gao, Jianwei Yang, Qiang Yang
* Year: 2026
* Venue / source: arXiv / Agentic AI for Next-Generation Software Development workshop preprint
* Link: https://arxiv.org/abs/2607.24604
* Date surfaced: 2026-07-28
* Why selected in one sentence: It is a useful correction to coding-agent evaluation because it distinguishes discovering a correct patch from preserving and certifying it.

## Quick verdict

**Highly relevant**

This paper is worth keeping because it attacks a real evaluation lie. Coding agents are often praised for iterative search even when their later revisions destroy a correct intermediate state, and this paper measures that failure directly. I inspected the arXiv HTML abstract, introduction, contribution list, related-work framing, reliability decomposition, and the main controlled-study descriptions and results.

## One-paragraph overview

The paper studies generate-test-revise loops for coding agents and asks whether repetition actually improves reliable completion. It separates proposal search from completion reliability: a trajectory may contain a correct patch somewhere while still ending in a wrong state. The core measurements track current correctness, ever-correct, correct-to-wrong regressions, evidence provenance, verifier dependence, and sound completion. On top of that, the paper proposes a typed loop contract that binds evidence to exact code state, preserves verified checkpoints, and requires fresh certification before accepting a revision as done.

## Model definition

### Inputs
The framework takes a current program state, evidence such as tests or verifier output, the provenance of that evidence, revision proposals from a coding model, and admission thresholds for stopping or continuing.

### Outputs
It outputs revised programs, admission or rejection of revisions, preserved checkpoints, and completion decisions conditioned on state-bound evidence.

### Training objective (loss)
There is no new learned repair model in the contribution. The paper studies orchestration and reliability contracts around existing coding agents and verifiers.

### Architecture / parameterization
The contribution is an admission and preservation layer around coding-agent loops. It tracks state hashes, evidence provenance, revision actions, verifier decisions, and typed loop obligations.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to stop coding-agent loops from confusing "found a correct patch at some point" with "reliably completed the task in a correct final state."

### 2. What is the method?
The method is to decompose reliability into state transitions and evidence provenance, then enforce a typed loop contract that preserves verified states and requires evidence to be bound to the exact code state it justifies.

### 3. What is the method motivation?
Repeated revision can raise ever-correct while lowering current correctness. That means more looping is not automatically more reliability.

### 4. What data does it use?
The paper uses 30 HumanEval repair tasks for controlled trajectory studies, common-state branching experiments, a prespecified 14B replication, a 540-rollout prospective policy test, and repository experiments over 24 bugs with four coder stacks.

### 5. How is it evaluated?
It is evaluated through multi-revision trajectory analysis, state-aligned evidence interventions, verifier risk and dependence analysis, prospective policy testing, and smaller repository-scale factorial studies.

### 6. What are the main results?
Under forced revision, current correctness drops from `0.820` after one revision to `0.673` after two even though ever-correct rises. Stale traces substantially increase harm on correct starts, and a prospective policy can remove observed correct-start harm only by paying a repair-rate cost and failing the joint objective.

### 7. What is actually novel?
The novelty is the reliability decomposition and the explicit contract around preservation, evidence binding, and completion, not a new foundation model for code repair.

### 8. What are the strengths?
It reports the right metrics, uses common-state controls to reduce risk-set bias, and cleanly separates competence from admission and preservation.

### 9. What are the weaknesses, limitations, or red flags?
The controlled studies are stronger than the repository studies. The real-bug experiments are smaller and noisier, and the reference implementation is an executable specification rather than proof of broad practical gains.

### 10. What challenges or open problems remain?
The field still needs stronger repository-scale evidence, better calibrated verifier dependence analysis, and loop policies that preserve correct states without collapsing repair liveness.

### 11. What future work naturally follows?
Apply the contract to stronger repo agents, combine it with better verifier abstention schemes, and make benchmark reporting include current correctness and regression rates by default.

### 12. Why does this matter for cabbageland?
Cabbageland cares about coding agents, stateful workflows, and evidence that actually licenses action. This paper is useful because it ties those together and makes loop reliability auditable.

### 13. What ideas are steal-worthy?
Track current correctness separately from ever-correct. Bind verifier evidence to exact code state. Preserve verified checkpoints. Treat admission and stopping as distinct system components rather than an invisible afterthought.

### 14. Final decision
**Keep for evaluation discipline and orchestration design.** The paper does not solve code repair, but it improves what a serious code-repair claim should have to prove.

