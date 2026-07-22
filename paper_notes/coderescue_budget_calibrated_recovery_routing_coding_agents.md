# CodeRescue: Budget-Calibrated Recovery Routing for Coding Agents

## Basic info

* Title: CodeRescue: Budget-Calibrated Recovery Routing for Coding Agents
* Authors: Qijia He, Jiayi Cheng, Chenqian Le, Rui Wang, Xunmei Liu, Yixian Chen, Jie Mei, Zhihao Wang, Xupeng Chen, Yuhuan Chen, Tao Wang
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.19338
* Date surfaced: 2026-07-22
* Why selected in one sentence: It turns coding-agent recovery from a monotone escalation habit into a budgeted choice among distinct post-failure actions.

## Quick verdict

**Must read**

This is a real deployment paper with a mechanism instead of a slogan. The best idea is that execution feedback creates heterogeneous cheap next steps, so the recovery problem is not binary deferral but action routing under cost. I inspected the arXiv HTML sections covering the abstract, problem setup, router formulation, main frontier results, ablations, and conclusion.

## One-paragraph overview

The paper studies what a coding agent should do after a cheap first attempt fails in an executable environment. Instead of assuming the only sensible move is to escalate to a stronger model, it introduces three recovery actions: `reflect` (cheap local repair), `replan` (cheap fresh solution), and `escalate` (send the problem plus feedback to a stronger model). A supervised router predicts which action is the cheapest useful next step from the post-failure signature, and a Conformal Risk Control layer calibrates a deployment-time cost penalty so the same trained router can operate under different average budgets without retraining. The central empirical claim is that cheap recovery and escalation solve different kinds of failures, so a learned router beats fixed-action baselines on the held-out cost/solve-rate frontier.

## Model definition

### Inputs
The router sees the problem statement, the execution verdict (for example wrong answer, timeout, or compile error), and the stderr trace from the failed first attempt, plus deployment-time action-cost estimates.

### Outputs
It chooses one recovery action from `reflect`, `replan`, and `escalate`.

### Training objective (loss)
The accessible paper text makes clear that the router is trained in supervised fashion toward the cheapest successful action recovered from offline rollouts, but it does not spell out the exact optimization loss in the sections I inspected. The CRC layer is then used at deployment time to choose a cost penalty that gives marginal expected-cost control under exchangeability.

### Architecture / parameterization
The primary router is a fine-tuned `Qwen3.5-4B` text model over the post-failure context, with metadata prefixes proving important in ablations. The routing policy is coupled to a CRC calibration layer rather than retrained per budget.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to decide what extra computation a coding agent should buy after a failed cheap attempt, under a fixed mean recovery budget.

### 2. What is the method?
The method collects offline recovery rollouts, labels each failed instance with the cheapest action that actually solves it, trains a router on the post-failure context, and then wraps the learned policy with CRC so the deployment budget can move without retraining the router.

### 3. What is the method motivation?
In coding, a failed attempt does not just say "this instance is hard." It also produces execution feedback that may make a cheap repair or cheap replanning step more cost-effective than escalation.

### 4. What data does it use?
The experiments use held-out failed attempts from five coding benchmarks. In the primary GPT-based setup, the reported frontier is selected on a `360`-example calibration split and evaluated on a disjoint `360`-example test split.

### 5. How is it evaluated?
It is evaluated by solve rate on held-out failed instances together with realized mean API cost, against fixed-action baselines, a binary cascade, and prompt-only routers. There is also a Gemini cross-model check.

### 6. What are the main results?
The learned frontier starts above always-replan even at the cheapest operating point and reaches `0.817` solve rate at the unconstrained argmax point. Around the medium-budget regime, the three-action router reaches `0.717` solve rate, beating the comparable-cost binary cascade (`0.636`) while using only about `35%` of the cost of always escalating.

### 7. What is actually novel?
The novelty is not "routing is good." It is the specific recovery framing: post-failure coding decisions are heterogeneous actions with complementary success regions, and CRC turns one router into a family of budgeted policies.

### 8. What are the strengths?
It uses the real post-failure signal instead of abstract difficulty estimates, separates cost control from router training, and shows that the monotone-cascade assumption is empirically wrong on some benchmark slices.

### 9. What are the weaknesses, limitations, or red flags?
The paper models only one post-failure decision, not full multi-round recovery. The cheapest-successful label is a practical proxy rather than a calibrated action-success model, and the cost guarantee is about expected spend, not solve rate.

### 10. What challenges or open problems remain?
The hard next step is multi-step recovery routing where the agent can reflect, replan, execute again, and only then escalate.

### 11. What future work naturally follows?
Add sequential decision-making, richer recovery actions, explicit uncertainty estimates over action success, and deployment constraints beyond mean API cost.

### 12. Why does this matter for cabbageland?
Cabbageland cares about agent control surfaces that survive contact with real tool feedback. This paper gives a clean abstraction for routing after failure instead of shoving every hard case up a stronger-model ladder.

### 13. What ideas are steal-worthy?
Route on execution verdict and stderr rather than only on the original prompt. Treat cheap repair and cheap replanning as distinct actions. Separate budget calibration from router retraining. Use a learned frontier instead of a single operating point.

### 14. Final decision
**Keep it.** This is one of the better recent papers on making coding agents behave like actual systems instead of benchmark puppets.
