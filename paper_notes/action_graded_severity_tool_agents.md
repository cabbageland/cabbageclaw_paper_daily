# Beyond Attack-Success Rate: Action-Graded Severity Scale for Tool-Using AI Agents

## Basic info

* Title: Beyond Attack-Success Rate: Action-Graded Severity Scale for Tool-Using AI Agents
* Authors: Harry Owiredu-Ashley
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.07474
* Date surfaced: 2026-07-09
* Why selected in one sentence: It gives agent red-teaming a trace-grounded severity scale based on the action actually executed, not just a binary attack-success label.

## Quick verdict

* Useful

This is a compact evaluation-instrument paper, and the instrument is worth keeping. I inspected the full PDF sections on the severity rubric, programmatic oracle, judge panel, AgentDojo evaluation, disagreement cases, reliability analysis, and limitations. The paper is narrow, but the narrowness is productive: it fixes one measurement bug clearly.

## One-paragraph overview

Agentic red-teaming often reports attack-success rate as one bit: the injected task succeeded or it did not. That loses the difference between a blocked attempt, a local reversible edit, an external leak, a privilege grant, and an escalating chain of actions. This paper introduces a seven-level action-graded severity scale from L0 to L6. The level is assigned from the worst action actually executed in the tool-call trace, using effect properties: whether the action completed, whether it was reversible, whether it crossed scope to another party or shared state, whether it expanded privilege, and whether a sequence of harmful actions escalated over steps. The paper implements both a deterministic oracle and a three-frontier-model judge panel, then applies the instrument to AgentDojo workspace logs.

## Model definition

### Inputs
Inputs are tool-call trajectories from agent episodes, attacker goals, per-tool effect metadata, and tag-free natural-language trace summaries for LLM judges. The deterministic oracle reads raw actions and the attacker's stated goal.

### Outputs
The instrument outputs an ordinal severity level from L0 to L6. L0 means no attack-attributed action; L1 means attempted but blocked; middle levels distinguish reversible local, irreversible local, cross-scope, and privilege-expanding actions; L6 marks an escalating chain of harmful completed actions.

### Training objective (loss)
There is no trained model in the main method. The oracle is rule-based. The judge panel uses prompted frontier models, and judge reliability is evaluated against the oracle rather than optimized by a loss.

### Architecture / parameterization
The instrument has a per-action effect metadata layer, an argument-match attribution rule tied to the attacker's goal, a deterministic severity oracle, and a judge-panel protocol. The AgentDojo experiments layer this severity computation onto existing execution logs.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Binary attack-success rate hides how bad an agent's actual behavior was. Two episodes can both count as success while one writes a local note and another grants external access. A defense can also report zero binary attack success while still allowing a harmful cross-scope action that the benchmark's success check did not watch.

### 2. What is the method?
The method defines a seven-level ordinal severity rubric over executed tool actions. A programmatic oracle converts raw AgentDojo traces into attributed actions, scores each action using reversibility, scope, and privilege properties, then takes the peak severity and raises the level for escalation chains. A separate LLM judge panel grades tag-free summaries so judge reliability can be measured.

### 3. What is the method motivation?
For deployment decisions, defenders need to know the consequence of the action, not just whether the attacker's exact benchmark objective completed. Severity should be tied to environment effects because tools turn model mistakes into state changes.

### 4. What data does it use?
The evaluation uses the AgentDojo workspace suite with a canonical prompt-injection attack, four victim models across two providers and two capability tiers, and two defenses. It judges a stratified sample of 188 episodes for oracle-versus-judge reliability.

### 5. How is it evaluated?
The paper applies severity grading to AgentDojo traces and compares it against binary attack-success rate. It reports cases where the two disagree, then evaluates judge agreement with the deterministic oracle using exact agreement, distance metrics, weighted kappa, and ordinal Krippendorff alpha.

### 6. What are the main results?
Severity scoring exposes three cases binary scoring hides: a defense with 0% attack-success rate that still permits a cross-scope leak, a defense that lowers attack-success rate while raising the worst-case severity tail, and a model comparison where harmful behavior localizes to one model despite aggregate rates being less informative. The three-judge panel reaches ordinal Krippendorff alpha 0.91 across judges and 0.92 including the oracle, but all judges share a blind spot for escalation chains.

### 7. What is actually novel?
The novelty is not a general harm taxonomy. It is a reusable, trace-grounded severity instrument for actual tool-call logs, with both deterministic scoring and measured judge reliability.

### 8. What are the strengths?
The rubric is small enough to be operational. It separates action consequence from attacker intent and benchmark success checks. The paper also does not blindly trust LLM judges; it measures where they agree and where they fail.

### 9. What are the weaknesses, limitations, or red flags?
The scale is validated on one AgentDojo suite, and some high-severity levels have few examples. The deterministic oracle depends on per-tool metadata and attribution rules that may be hard to maintain across broad tool ecosystems. Judges struggle with escalation chains, which are exactly the failures deployment monitors should care about.

### 10. What challenges or open problems remain?
The main challenge is porting severity metadata to richer tools without turning it into another brittle hand-coded policy table. Another challenge is scoring multi-step harms where the bad outcome is not visible in any single tool call.

### 11. What future work naturally follows?
Apply the scale to email, file, shell, browser, payment, and messaging agents; train lightweight severity judges on oracle labels; add environment-specific effect metadata; and combine severity grading with authorization logs and cross-agent provenance.

### 12. Why does this matter for cabbageland?
OpenClaw agents can act. A binary "attack succeeded" flag is too dull for deciding whether a tool policy, confirmation prompt, or runtime monitor is acceptable. Severity levels based on executed actions would make red-team results easier to compare and harder to launder.

### 13. What ideas are steal-worthy?
Grade the worst executed action, not the model's stated plan. Separate reversible local effects from cross-scope and privilege-expanding effects. Keep a deterministic oracle where possible, but report judge reliability explicitly when using LLM graders.

### 14. Final decision
Keep as a useful evaluation primitive. It is not a whole safety framework, but it gives agent red-teaming a measurement surface that is much harder to game than a single attack-success bit.
