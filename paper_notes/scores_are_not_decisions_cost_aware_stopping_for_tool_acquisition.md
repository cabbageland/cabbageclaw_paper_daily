# Scores Are Not Decisions: Cost-Aware Stopping for Tool Acquisition in LLM Agents

## Basic info

* Title: Scores Are Not Decisions: Cost-Aware Stopping for Tool Acquisition in LLM Agents
* Authors: Yicheng Feng, Yan Zhang, Yan Cheng, Wei Qi
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.27083
* Date surfaced: 2026-07-30
* Why selected in one sentence: It cleanly separates tool ranking from tool-budget selection and makes acquisition depth a direct payoff optimization problem instead of a score-threshold superstition.

## Quick verdict

**Must read**

This is one of the clearest direct agent-systems papers in the recent batch because it fixes a real control mistake. Tool stacks keep acting as if ranking candidate tools and deciding how many to expose are basically the same problem. They are not. I inspected the full arXiv PDF, especially the formulation, main results, comparative-statics analysis, live evaluation, and ablations.

## One-paragraph overview

The paper studies a narrow but important layer in tool-using agents: once some upstream router or retriever has ranked the candidate tools, how many of those tools should the harness actually expose for the task? The proposed answer is CAM-DF, a learned stopping policy over ranked prefixes. Instead of thresholding raw scores, it compares the payoff of stopping now with the best attainable payoff from continuing further down the ranked list, where payoff explicitly trades task sufficiency against acquisition cost. That gives a task-specific acquisition depth rather than a one-size-fits-all top-k rule. The useful result is not just a benchmark bump. The paper makes the scoring object match the deployment decision.

## Model definition

### Inputs
The inputs are a task, a ranked list of candidate tools produced by an upstream scorer, per-tool costs, and observable prefix-progress features.

### Outputs
The output is a stop-or-continue decision at each ranked prefix, which determines the final acquisition depth and the exposed tool set.

### Training objective (loss)
The main policy is trained as a regret-weighted logistic classifier. For each nonterminal prefix, the target is the sign of the payoff gap between stopping now and the best continuation, and the loss is weighted by the magnitude of that payoff gap.

### Architecture / parameterization
CAM-DF is a modular stopping policy that uses ranking scores, tool costs, and prefix-progress features. The paper also introduces CAM-DF-lite, a lower-dimensional and more interpretable variant that keeps most of the gain with a simpler feature set.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the missing decision between tool ranking and tool execution. Even if a retriever ranks tools well, the agent harness still has to decide how many tools are worth exposing before the task starts. That decision gets harder when tool costs differ.

### 2. What is the method?
The method is cost-aware stopping over ranked tool prefixes. The policy computes whether the current prefix should be accepted or whether the harness should continue acquiring more tools. The supervision is generated from downstream payoff, not from tool scores alone.

### 3. What is the method motivation?
A ranking tells you order, not acquisition depth. Once tools have heterogeneous costs, the correct choice depends on marginal value relative to marginal cost, not on the next tool's raw relevance score.

### 4. What data does it use?
The evaluation covers 1,343 tasks across five tool-use domains. The main testbed is tau-bench Retail, with additional evaluations on MCP-Atlas, WorkBench, Telecom, and Airline.

### 5. How is it evaluated?
It is evaluated in offline replay with frozen tool rankings, explicit cost-pressure and cost-dispersion settings, and comparisons against fixed-k, score-threshold, score-per-cost threshold, predict-then-threshold, and a hand-written Retail rule. The paper also includes a live end-to-end tau-bench Retail evaluation.

### 6. What are the main results?
CAM-DF achieves the highest mean payoff among deployable methods on the main benchmark settings. On Retail, it beats Predict-then-threshold across all 25 cost-pressure and cost-dispersion regimes, with paired-bootstrap 95 percent confidence intervals above zero in 24 of them. The gains grow when costs are more heterogeneous and when cost pressure is higher. In the live Retail evaluation, CAM-DF reduces pre-execution tool exposure from 7 tools to 4.4 on average, about 37 percent fewer tools, while maintaining comparable observed task success.

### 7. What is actually novel?
The novelty is not another tool scorer. It is the decision-focused stopping layer over ranked prefixes, with a payoff-gap objective and a proof that score-only acquisition rules are suboptimal under heterogeneous costs.

### 8. What are the strengths?
The paper attacks the right control object, stays modular, and does not require changing the upstream ranker or the underlying LLM. The ablations are also useful: they show that next-tool and marginal-cost features matter most when costs differ, which supports the paper's main claim instead of just decorating it.

### 9. What are the weaknesses, limitations, or red flags?
Most of the evidence is still offline replay over annotated required-tool sets and simplified payoff definitions. That means the live agent messiness is only partly represented. The strongest live evidence is narrow, and the sufficiency-based payoff abstraction still simplifies real execution errors and tool interactions.

### 10. What challenges or open problems remain?
A big open problem is extending this layer from pre-execution acquisition to sequential execution, where the value of the next tool depends on what already happened. Another is learning richer set-value functions when tools are complementary, redundant, or privacy-sensitive in more realistic ways.

### 11. What future work naturally follows?
Future work should combine this stopping layer with stronger set-level retrieval, dynamic tool pricing, uncertainty estimates about missing capability, and richer downstream utility signals than binary sufficiency.

### 12. Why does this matter for cabbageland?
It matters because cabbageland keeps building agents in tool-rich environments where every exposed tool costs something: context, latency, money, privacy surface, or failure surface. This paper gives the right mental split between ranking and access allocation.

### 13. What ideas are steal-worthy?
Learn stop-versus-continue directly from downstream regret. Separate candidate ordering from acquisition depth. Include marginal cost and prefix-progress features explicitly instead of assuming the ranker already solved the problem.

### 14. Final decision
**Keep it.** This is a direct systems paper with a real control insight, believable ablations, and an easy path into actual harness design.
