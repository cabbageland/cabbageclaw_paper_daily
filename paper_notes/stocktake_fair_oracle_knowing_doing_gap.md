# STOCKTAKE: Measuring the Gap Between Perception and Action in LLM Agents with a Fair Oracle

## Basic info

* Title: STOCKTAKE: Measuring the Gap Between Perception and Action in LLM Agents with a Fair Oracle
* Authors: Sagar Deb, Ashwanth Krishnan
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.13618
* Date surfaced: 2026-07-16
* Why selected in one sentence: It finally gives a long-horizon agent benchmark that can separate hidden-state inference from action quality using a fair reference policy on the same observation stream.

## Quick verdict

**Must read**

This is one of the sharpest recent papers on long-horizon agent evaluation under partial observability. The real contribution is not the supply-chain theme. It is the benchmark design: a factored POMDP plus a fair Bayes-filter oracle that sees exactly what the agent sees, so belief and control can be measured separately instead of getting mushed into one score. I inspected the full arXiv HTML paper, including the task definition, reference-policy construction, metrics, main results, discussion, limitations, and appendices needed to verify the setup.

## One-paragraph overview

The paper casts an LLM as the replenishment manager of a 26-week electronics-import problem with six hidden factor processes: demand regime, supplier health, freight market, port congestion, batch quality, and canal status. Each week the agent sees only noisy symptoms, chooses mitigation actions and an order, and writes a rationale. The benchmark then evaluates the run against two references: a symptom-blind base-stock floor and a fair Bayesian oracle built from exact factor-wise Bayes filters and rollout search on the same observation stream. That produces a skill score that isolates action quality, plus rationale-derived detection lag and a knowing-doing rate that isolates whether the model noticed the right hidden state but still acted badly.

## Model definition

### Inputs
Each agent receives a weekly dashboard with on-hand inventory, pipeline inventory, realized demand, freight quotes, port delays, canal transit counts, supplier scorecards, and quality signals. It never receives the hidden factor states directly.

### Outputs
The evaluated agent chooses optional within-week actions such as locking freight, expediting by air, inspecting a batch, or buying an audit or briefing, then emits one `place_order` decision with quantity, route, supplier, contract action, and a required natural-language rationale.

### Training objective (loss)
The paper does not propose a new training loss. It evaluates frontier LLM agents zero-shot or instruction-following in a fixed environment. The oracle is not learned; it is an exact-filter rollout policy.

### Architecture / parameterization
There is no new model architecture. The benchmark evaluates Claude Sonnet 5, GPT-5.4, DeepSeek-V4-Pro, and Grok 4.5. The reference policy uses one exact Bayes filter per hidden factor plus a small candidate-action menu scored by rollout simulation.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to separate two failures that most long-horizon agent benchmarks blur together: failing to infer the hidden state and failing to act on a correct inference.

### 2. What is the method?
The method is a 26-week factored supply-chain POMDP with six hidden Markov factor processes, seeded event tapes, a fair Bayesian reference policy that sees the same observations as the agent, and rationale-based metrics that grade which hidden factors the agent claimed were active each week.

### 3. What is the method motivation?
Behavior-only benchmarks tell you that a model lost money or won money, but not whether it misunderstood the world or understood it and still chose badly. Those are different failures and need different fixes.

### 4. What data does it use?
The environment is synthetic but structured. The study runs fifty seeded episodes with isolated, persistent, and compound stress profiles. The hidden world is fully specified by published seeds and factor-transition tables rather than scraped data.

### 5. How is it evaluated?
The main metrics are skill score, detection lag, and knowing-doing rate. Skill score places each agent between a symptom-blind base-stock floor at `0` and a fair Bayes-filter oracle at `1`. Detection lag measures how quickly the rationale names a true stressed factor. Knowing-doing rate measures how often the agent still stockouts on weeks it correctly diagnosed.

### 6. What are the main results?
Detection is high and surprisingly uniform: all four models detect `84-88%` of hidden failures, usually within about a week of onset. Control is not. Skill scores span from `0.62` down to `-0.23`, and two of the four models finish below the symptom-blind floor overall. On persistent seeds, `34-43%` of correctly diagnosed stress weeks still end in stockout for every model, which is the paper's clearest evidence that the bottleneck often lies between correct stated belief and costly action.

### 7. What is actually novel?
The novelty is the fair oracle plus the metric split. Existing long-horizon benchmarks usually compare against privileged or hindsight references, which makes belief failure and action failure inseparable. This paper makes the reference policy live under the same information constraints as the agent.

### 8. What are the strengths?
The benchmark construction is clean, the fairness story is real, the hidden-state factors are explicit, and the metric design is useful beyond this domain. Requiring a rationale each week also creates a cheap belief-side probe without pretending it is perfect interpretability.

### 9. What are the weaknesses, limitations, or red flags?
It is still one domain, one SKU, one prompt arm, and four models. Each model-seed cell is a single run, so provider-side nondeterminism is not deeply characterized. Some levers are intentionally near-deterministic, which is useful for diagnosis but simplifies the action problem.

### 10. What challenges or open problems remain?
The benchmark needs broader domains, more model families, repeated runs per seed, and intervention studies that test whether explicit belief-maintenance scaffolds actually reduce the knowing-doing gap.

### 11. What future work naturally follows?
Natural next steps are richer partially observed operations tasks, new prompt arms that force explicit belief updates, and training procedures that target the gap between correct belief and action directly.

### 12. Why does this matter for cabbageland?
Cabbageland cares about agents that track state, not just agents that occasionally land the right answer. This paper gives a concrete template for evaluating whether a system is failing at inference or failing at control, which is exactly the distinction that workflow agents and world-model claims usually duck.

### 13. What ideas are steal-worthy?
Use a fair reference policy that sees the identical observation stream as the agent. Anchor agent performance between a blind floor and a constrained oracle instead of a privileged optimum. Require weekly or stepwise rationales and turn them into explicit belief-side metrics. Build persistent-stress seeds, not just isolated shocks.

### 14. Final decision
**Keep it.** This is a rare benchmark paper where the metric design itself is the result worth preserving.
