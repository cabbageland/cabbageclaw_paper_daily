# The Interaction Tax: When Communication Erases Diversity in Multi-Agent Teams

## Basic info

* Title: The Interaction Tax: When Communication Erases Diversity in Multi-Agent Teams
* Authors: Summer Eunhyung Ann, Haokun Liu, Chenhao Tan
* Year: 2026
* Venue / source: ICML 2026 (PMLR 306) / arXiv
* Link: https://arxiv.org/abs/2608.23541
* Date surfaced: 2026-08-25
* Why selected in one sentence: It is a strong adjacent paper because it isolates the real variable in multi-agent coordination - what information gets exchanged - and shows that full-solution sharing can destroy the diversity the system was supposed to exploit.

## Quick verdict

* Useful

I inspected the full arXiv HTML text, especially the abstract framing, the benchmark setup, the diverse-versus-same-model comparisons, and the result section on interaction tax. This paper earns a preserved note because it contributes a clean failure concept rather than another generic "agents collaborate" story. The useful distinction is between having multiple agents and preserving multiple approaches.

## One-paragraph overview

The paper studies multi-agent LLM workflows on verifier-scored optimization tasks and argues that the contradictory literature on agent interaction partly comes from treating all communication as equivalent. It compares same-model and diverse-model teams built from Claude Sonnet 4, GPT-4o, and Gemini 2.5 Flash across multiple protocols such as Chain, Debate, MAgICoRe, HPE, and MoA. The central finding is that when diverse agents read each other's full solutions, they often converge after one round and lose the diversity benefit that motivated using different models at all. Independent proposal generation plus later selection or synthesis performs better because it preserves solution diversity until the final decision point.

## Model definition

### Inputs
Verifier-scored optimization tasks, visible development evaluators during search, and depending on the protocol either independent proposals or peer solutions/critiques exchanged during refinement.

### Outputs
JSON candidate solutions scored by deterministic verifiers, with final evaluation performed by hidden evaluators for the main comparisons.

### Training objective (loss)
There is no trainable model. The paper evaluates interaction protocols over existing frontier LLMs under matched compute budgets.

### Architecture / parameterization
Ten workflow configurations including single-agent baselines and multi-agent protocols such as Chain, MAgICoRe, Debate, HPE, and MoA, tested with same-model and diverse-model proposer sets.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to explain why multi-agent interaction sometimes helps and sometimes hurts, and whether the difference comes from the number of agents or from the type of information they exchange.

### 2. What is the method?
Run matched-budget workflows on verifier-scored optimization tasks, vary whether teams are same-model or diverse-model, and compare protocols where agents do or do not read each other's full solutions before the final selection step.

### 3. What is the method motivation?
Different model families often find structurally different solutions. If communication makes them converge too early, the system loses exactly the diversity benefit that made model mixing attractive.

### 4. What data does it use?
Eleven verifier-scored optimization tasks, four adapted from the AlphaEvolve suite. The main benchmark uses five seeds per configuration cell, and a 2 x 2 factorial study uses ten seeds on three tasks with enough score variance.

### 5. How is it evaluated?
With deterministic visible and hidden evaluators, normalized quality scores in [0,1], aggregate gain measures on hidden scores, and same-model versus diverse-model interaction-gain comparisons.

### 6. What are the main results?
The controlled factorial shows a positive diversity coefficient of +0.188 with confidence interval [+0.073, +0.299] and p < 0.001, while synthesis itself is near zero. Same-model interaction can help, but with diverse teams the full-solution protocols turn negative: Chain reaches -0.024, MAgICoRe -0.035, and Debate -0.078 on the diverse-model interaction-gain measure. MoA is the clean counterexample because its proposers never read each other's outputs, so it preserves diversity until final aggregation. The paper's qualitative point is equally important: agents often converge toward the first complete solution they see rather than exploring distinct approaches.

### 7. What is actually novel?
The novelty is isolating communication content as the variable of interest. The paper is not just another comparison of agent counts or orchestration recipes; it asks whether full-solution sharing itself is the mechanism that harms diverse teams.

### 8. What are the strengths?
The paper uses matched budgets, hidden evaluators, and genuinely different model families. It also connects its empirical result to an interpretable mechanism - diversity collapse after full-solution exchange - instead of leaving the coordination effect mysterious.

### 9. What are the weaknesses, limitations, or red flags?
The task suite is restricted to verifier-scored optimization problems, so transfer to open-ended research, factual debate, or social interaction is not automatic. The findings are also task-dependent, as the authors note in the leave-one-out analysis. Three model families are enough for the claim to be interesting but not enough to treat the effect as universal.

### 10. What challenges or open problems remain?
Understanding when critique should be exchanged instead of whole solutions, how to preserve diversity over many rounds, and whether similar collapse happens in longer-horizon tool-using agents outside deterministic optimization tasks.

### 11. What future work naturally follows?
Protocol designs that expose only partial plans, local repairs, or uncertainty summaries; explicit diversity regularizers for agent teams; and evaluation of information-sharing policies in open-ended coding, science, and planning environments.

### 12. Why does this matter for cabbageland?
Because cabbageland already cares about multi-agent orchestration and often benefits from model diversity. This paper is a warning not to destroy that diversity by making agents read each other's full solutions too early.

### 13. What ideas are steal-worthy?
Keep proposals independent longer. Share critiques, constraints, or repair targets instead of complete candidate solutions when diversity matters. Track whether interaction is actually producing convergence before assuming it is producing insight.

### 14. Final decision
Keep as a preserved note. The interaction-tax concept is crisp and likely to age well.

## 6. Mandatory critical angles

The paper is strongest on coordination mechanism, evaluation control, and failure-mode clarity. It is weaker on breadth because the tasks are optimization-heavy and verifier-defined. Still, the structural point about diversity collapse is probably real beyond this benchmark.

## 7. Writing style

The tone should be approving with a little bite. The paper is useful because it punctures a lazy pro-communication default.

## 8. Repository output format

Saved as a preserved paper note because the "preserve diversity, do not prematurely share full solutions" lesson maps directly onto future agent-system design.
