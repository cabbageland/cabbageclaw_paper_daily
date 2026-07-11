# Remember When It Matters: Proactive Memory Agent for Long-Horizon Agents

## Basic info

* Title: Remember When It Matters: Proactive Memory Agent for Long-Horizon Agents
* Authors: Yifan Wu, Lizhu Zhang, Yuhang Zhou, Mingyi Wang, Bo Peng, Serena Li, Xiangjun Fan, Zhuokai Zhao
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.08716
* Date surfaced: 2026-07-11
* Why selected in one sentence: It makes agent memory a selective intervention policy, not a passive pile of retrieved context.

## Quick verdict

**Highly relevant**

This is the agent-memory paper to keep from today's scan. The paper is valuable because it names the failure mode precisely, behavioral state decay, and then changes the control loop: a separate memory agent edits a structured memory bank and decides whether to inject a targeted reminder or stay silent. I inspected the full arXiv PDF, including the method, Terminal-Bench and tau^2-Bench setup, main results, ablations, trainable memory-agent section, and conclusion.

## One-paragraph overview

Long-horizon agents often observe the right fact once and then stop acting as if they know it. A requirement, file path, tool limitation, failed diagnosis, or open subgoal may be present somewhere in the trajectory but absent from the next effective decision. The paper calls this behavioral state decay. Its proposed fix is a separate proactive memory agent that watches the trajectory, keeps a compact structured bank of execution state, and periodically chooses whether to inject one memory-grounded reminder into the next action-agent call. The key distinction is that memory is not automatically exposed. The memory agent has an explicit no-intervention action, so the system can retain state without constantly adding noisy context.

## Model definition

### Inputs
The memory agent receives the task description, a recent trajectory window, and the current memory bank. The action agent continues to receive its usual environment observations and tools, plus an optional transient reminder when the memory agent chooses to intervene.

### Outputs
The memory agent outputs constrained memory-bank edits during the management phase and either a concise reminder or a null intervention during the intervention phase. The action agent outputs ordinary environment actions.

### Training objective (loss)
The main system is evaluated without changing the action agent. A smaller open-weight memory policy is trained later on SETA using supervised fine-tuning and GRPO-style reinforcement learning against verifier rewards, then checked for partial transfer to Terminal-Bench.

### Architecture / parameterization
The architecture adds a sidecar memory agent to an unmodified action agent. The memory bank has private status, knowledge memories, and procedural memories. Phase 1 manages the bank through memory tool calls. Phase 2 reads the bank and chooses reminder or no intervention.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to solve long-horizon execution failures where decision-relevant state stops influencing later actions. This is not just context-window overflow. Even when prior information is technically available, agents may repeat failed commands, forget constraints, lose diagnoses, or stop tracking unresolved subgoals.

### 2. What is the method?
The method adds a proactive memory agent. At fixed intervals, it observes the task, a sliding window of recent steps, and the existing memory bank. It first updates the bank through constrained calls such as saving knowledge, saving procedural observations, updating private status, or deleting stale entries. It then decides whether the next action-agent call needs a targeted memory reminder. If not, it emits no intervention.

### 3. What is the method motivation?
The useful motivation is that memory should be judged by whether it changes the next decision at the right time. Passive retrieval can show too much, too little, or irrelevant context. Always-on summaries can become a second noisy planner. A calibrated memory policy should retain more state than it speaks, then reactivate only what is behaviorally relevant.

### 4. What data does it use?
The main evaluation uses Terminal-Bench 2.0 and three tau^2-Bench domains: airline, retail, and telecom. Terminal-Bench tests autonomous command-line agents doing realistic file/code/debug tasks. tau^2-Bench tests conversational tool-use agents in dynamic service-like tasks.

### 5. How is it evaluated?
The main metric is pass@1. The paper compares baseline action agents against the same action agents augmented with the memory sidecar. It also runs ablations on tau^2-Bench: full-bank context, always inject, injection-only with no bank, and Mem0-style retrieval.

### 6. What are the main results?
With Claude Opus 4.6 as memory agent, Sonnet 4.5 improves from 37.6% to 45.9% on Terminal-Bench 2.0 and from 55.0% to 61.8% task-weighted average on tau^2-Bench. Opus 4.6 as the action agent also improves, though less: 43.5% to 45.9% on Terminal-Bench and 66.2% to 68.7% on tau^2-Bench. The ablations show that full-bank context improves but trails selective intervention, and generic retrieval is not the same as deciding when memory should enter the action loop.

### 7. What is actually novel?
The novelty is treating memory as a policy over interventions. The paper does not simply propose a better summarizer or vector store. It separates retention from reactivation and makes silence an explicit action.

### 8. What are the strengths?
The conceptual framing is clean and deployable. The method keeps the action agent unchanged, making it a plausible wrapper around existing agents. The ablations test the right confounds: passive context exposure, always-on reminders, no persistent bank, and a production-style memory retrieval baseline.

### 9. What are the weaknesses, limitations, or red flags?
The strongest configuration uses a powerful and expensive memory agent. The benchmark runs are pass@1 and may have ordinary agent-run variance. The paper does not prove that reminders are causally minimal or always well calibrated. The memory agent could also introduce new failure modes by injecting stale or overconfident guidance.

### 10. What challenges or open problems remain?
The next problem is learning the memory-intervention policy cheaply and robustly. Another open problem is memory governance: when should procedural memories expire, when should the memory agent revise wrong diagnoses, and how should reminders be audited if they change downstream actions?

### 11. What future work naturally follows?
Future work should test lower-cost memory agents, causal ablations over individual reminders, adaptive trigger schedules, and memory policies that expose uncertainty about stored facts. For coding agents, it would be useful to connect reminders to concrete trace evidence and failure classes.

### 12. Why does this matter for cabbageland?
Cabbageland runs long-lived agent workflows where the agent often needs to remember tool quirks, prior failed attempts, user constraints, file paths, and partially completed plans. This paper gives the right interface: store execution state outside the action context, but reintroduce only the piece that should affect the next move.

### 13. What ideas are steal-worthy?
Use separate knowledge and procedural memory. Make "do not intervene" a first-class action. Treat reminders as transient context, not permanent prompt growth. Track private memory-agent status separately from what the action agent sees. Compare any memory layer against full-bank exposure and always-on reminders, not just against no memory.

### 14. Final decision
**Keep it.** This is a practical, mechanism-rich memory paper. The exact implementation may change, but the core contract is right: memory should be a calibrated control intervention.
