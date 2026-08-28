# When Tool Outputs Become Commands: Separating Action Induction from Runtime Authorization in Tool-Augmented LLM Agents

## Basic info

* Title: When Tool Outputs Become Commands: Separating Action Induction from Runtime Authorization in Tool-Augmented LLM Agents
* Authors: Xiaokun Guo, Zhen Xu, Dongdong Huo, Yanqiu Zhang, Wei Wang, Qinfu Yang, Dongjin Yu, Yu Wang
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.27146
* Date surfaced: 2026-08-28
* Why selected in one sentence: It draws the right runtime boundary for tool agents by separating observation-induced action suggestions from actual execution authority.

## Quick verdict

* Must read

I inspected the full arXiv HTML text, especially the threat model, the SARA runtime design, the authorization-state machinery, and the main AgentDojo/AgentDyn results. This paper earns a preserved note because it makes a clean conceptual separation that directly changes the computation: tool outputs can help instantiate a task without ever becoming self-authenticating permission to execute. That is a better framing than generic prompt-injection alarmism.

## One-paragraph overview

The paper studies indirect prompt injection in tool-using LLM agents and argues that the core mistake is conflating action induction with execution authorization. SARA fixes this by placing an explicit runtime authorization layer between the agent and the real tool executor. A context-isolated Action Probe records when tool observations induce candidate actions and preserves that provenance across steps. Actual execution is then authorized only if the candidate call is supported by the user objective plus audited evidence from prior authorized executions, with checks at the goal, execution-chain, and argument levels. A No-History-Promotion rule prevents repeated historical mentions from laundering an injected action into authority.

## Model definition

### Inputs
The user objective, tool schemas, the agent's candidate tool calls, runtime observations from tools, and SARA's own persistent authorization state.

### Outputs
A runtime decision to authorize, block, or further review each candidate tool call before it reaches the real executor.

### Training objective (loss)
There is no base-model retraining claim. The contribution is a runtime authorization scaffold around an existing tool-using agent.

### Architecture / parameterization
SARA is an execution-boundary controller with an Action Probe for observation-side provenance, an audited-execution-evidence store, and authorization logic that separately checks user-goal support, execution-chain support, and argument-level support.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to stop untrusted tool outputs from turning into unauthorized real-world actions in multi-step agents.

### 2. What is the method?
The method records action-inducing provenance from observations, keeps that provenance persistent across steps, and requires candidate tool calls to re-establish independent authorization support at the execution boundary.

### 3. What is the method motivation?
Open-ended tasks do need runtime observations to fill in real identifiers, files, recipients, and other missing details. The point is not to forbid observation influence, but to stop that influence from becoming authority on its own.

### 4. What data does it use?
It evaluates on AgentDojo and AgentDyn with multiple foundation-model backbones and compares against agent-only and several defense baselines.

### 5. How is it evaluated?
The paper measures benign utility, utility under attack, and attack success rate, plus backbone transfer, component ablations, and additional inference cost.

### 6. What are the main results?
Across four primary evaluation settings, SARA keeps ASR at or below 0.63% while maintaining utility under attack no lower than the corresponding agent-only baseline. On GPT-4o-mini, ASR falls from 15.79% and 16.07% to 0.06% and 0.17%. On Gemini-2.5-Flash-Lite, it falls from 33.28% and 30.91% to 0.62% and 0.63%.

### 7. What is actually novel?
The real novelty is not "another agent guard." It is explicitly separating action induction from authorization, then preserving action-origin provenance so that historical recurrence cannot silently promote an injected instruction into authority.

### 8. What are the strengths?
The decomposition is crisp, the runtime state is explicit, and the evaluation lives in dynamic tool environments instead of toy static settings. It also targets the actual execution boundary where harm occurs.

### 9. What are the weaknesses, limitations, or red flags?
The mechanism still depends on an authorization scaffold that must itself be robust, and the paper does not magically solve every possible confused-deputy or sandbox-bypass problem. Utility remains backbone-sensitive, especially when the base agent already struggles with tool errors.

### 10. What challenges or open problems remain?
The next questions are how this style of authorization scales to richer stateful environments, concurrent tools, cross-agent collaboration, and irreversible external side effects such as payments or code deployment.

### 11. What future work naturally follows?
Typed evidence objects, finer-grained tool-side effect models, and integration with explicit policy languages or capability contracts would all follow naturally.

### 12. Why does this matter for cabbageland?
Because cabbageland keeps caring about tool use as governed action rather than raw capability. This paper offers a clean way to say what observations are allowed to influence without pretending that influence itself is permission.

### 13. What ideas are steal-worthy?
Separate action induction from execution authorization. Preserve action-origin provenance across steps. Prevent historical recurrence from upgrading a suspicious instruction into legitimate authority. Require goal-level, chain-level, and argument-level support at the actual execution boundary.

### 14. Final decision
Keep as a preserved note. This is one of the better recent papers on runtime control for tool agents because it draws a boundary that is both principled and executable.

## 6. Mandatory critical angles

The paper is strongest exactly where many security papers are weakest: it does not confuse "observation influenced the agent" with "the agent should therefore be blocked." It instead asks what evidence is sufficient for execution. That is the right object. The main caveat is that it is still a runtime governance mechanism, not a full theory of safe delegation.

## 7. Writing style

The tone should be crisp and approving. The paper deserves credit for naming the right boundary and for evaluating it in a setting where the boundary matters.

## 8. Repository output format

Saved as a preserved paper note because the action-induction versus authorization split is a durable design idea for tool-using agents.
