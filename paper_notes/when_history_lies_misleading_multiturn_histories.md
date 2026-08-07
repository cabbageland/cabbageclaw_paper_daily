# When History Lies: Evaluating and Improving Tool Use under Misleading Multi-Turn Histories

## Basic info

* Title: When History Lies: Evaluating and Improving Tool Use under Misleading Multi-Turn Histories
* Authors: Xiaoqing Wu, Xingyu Fan, Feifei Li, Wenhui Que
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.06057
* Date surfaced: 2026-08-07
* Why selected in one sentence: It isolates a real tool-agent failure mode where stale but plausible history hijacks an otherwise correct policy and offers a concrete reliable-state distillation recipe for fixing it.

## Quick verdict

**Highly relevant**

I inspected the arXiv HTML paper, especially the synchronized Original/Polluted/Oracle views, the intervention taxonomy, the Oracle-OPD training objective, the ablations on prefix source and teacher view, and the transfer results. The paper's best move is separating "the model lacks the policy" from "the model has the policy but the history hijacks it." The main caveat is that both the benchmark and the fix rely on a strong controlled setup: polluted histories are constructed interventions, and the training recipe gets access to an Oracle State teacher that ordinary deployments do not have.

## One-paragraph overview

The paper studies a failure mode that feels obvious once named: a tool agent can have the right current tools, the right latest request, and the right underlying policy, but still copy a stale or non-authoritative precedent from earlier turns. To isolate that effect, the authors build synchronized Original, Polluted, and Oracle State views so the gold next action stays fixed while the misleading history changes. They then train a polluted-context student with soft supervision from an Oracle-conditioned teacher on the student's own generated prefixes. The result is not a generic agent-improvement recipe. It is a targeted way to teach a model which state should govern the decision when transcript precedent and current task state disagree.

## Model definition

### Inputs
Training uses synchronized Polluted and Oracle-State contexts, the latest request, current available tools, and student-generated prefixes. At deployment, the student sees only ordinary interaction history.

### Outputs
The model outputs the next tool-use decision or non-call answer action, including complete calls, arguments, or answer-side decisions depending on the benchmark item.

### Training objective (loss)
Oracle-OPD trains the student with token-level reverse KL against a frozen Oracle-conditioned teacher over the union of the teacher and student top-16 token supports. The teacher is evaluated on student-generated prefixes, and the paper uses four student rollouts per prompt with no additional gold cross-entropy term.

### Architecture / parameterization
The experiments use Qwen3-1.7B and Qwen3-8B teacher/student language models. The contribution is a reliable-state distillation procedure rather than a new base model architecture.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the fact that multi-turn tool agents can be redirected by stale but plausible historical traces even when the gold action for the current state has not changed.

### 2. What is the method?
The method builds a paired benchmark with Original, Polluted, and Oracle-State views, then distills an Oracle-conditioned teacher policy into a polluted-context student using on-policy student prefixes and token-level soft supervision.

### 3. What is the method motivation?
The motivation is that aggregate tool-use errors conflate two very different failures: not knowing the right policy at all, versus knowing it under clean state but being hijacked by misleading history.

### 4. What data does it use?
The benchmark, ContextPollute-Bench, uses synchronized interventions over tool-use decision points with eleven gold-preserving operators across complete calls and non-call decisions. The paper also evaluates transfer on external tool-use and noisy multi-hop QA settings.

### 5. How is it evaluated?
It is evaluated by Balanced Tool-Use Accuracy and related decompositions across Original, Polluted, and Oracle views, plus ablations over teacher view, prefix source, teacher size, student size, unseen functions, cross-generator transfer, and robustness transfer to other tasks.

### 6. What are the main results?
On Qwen3-1.7B, misleading history flips 32.14% of decisions that are correct under the Original trajectory. Oracle-OPD reaches 87.0% Balanced Tool-Use Accuracy, ahead of Gold-SFT at 66.3%, Oracle sequence distillation at 82.3%, and off-policy token distillation at 85.0%. With an 8B teacher, the same compact 1.7B student reaches 91.9%.

### 7. What is actually novel?
The novelty is not merely "robust tool use." The real contribution is isolating history-induced policy hijacking as its own failure mode and then showing that reliable-state policy transfer works best when supervision follows the student's own polluted-context prefixes.

### 8. What are the strengths?
It asks the right causal question, builds a controlled benchmark that actually separates the failure mode, and uses ablations that show why the method works instead of only reporting one big final number.

### 9. What are the weaknesses, limitations, or red flags?
The interventions are constructed rather than harvested from messy organic production logs, and the fix assumes an Oracle-State teacher during training. That means the paper proves a real mechanism, but not yet that the same signal is cheap to obtain at scale in the wild.

### 10. What challenges or open problems remain?
The big open problems are deriving Oracle-like state views automatically, handling richer long-horizon environment drift, and making the same robustness transfer work when the history failures are more entangled than clean benchmark operators.

### 11. What future work naturally follows?
Natural follow-ons are automatic state summarizers for teacher views, online training or self-repair loops for stale-history failures, and evaluation on real product logs where misleading precedent arises naturally rather than by controlled insertion.

### 12. Why does this matter for cabbageland?
It matters because cabbageland keeps running multi-turn agents where a stale trace can stay syntactically plausible long after it stopped being authoritative. The paper offers a sharp vocabulary for that failure and a useful training instinct: teach the policy which state should govern the action.

### 13. What ideas are steal-worthy?
Build synchronized clean/polluted/oracle views to isolate state-hijack failures. Distill from a reliable-state teacher onto student-visited polluted prefixes. Separate "policy missing" from "policy redirected by misleading context" in evaluation.

### 14. Final decision
**Keep it.** The setup is controlled, but the failure mode is real and the distillation lesson is genuinely useful.

## Confidence / access note

This note is based on full-text inspection of the arXiv HTML paper, including the benchmark design, training objective, ablations, and transfer results.
