# DeltaML-Bench: Evaluating Machine Learning Agents on Real-World Research Repositories

## Basic info

* Title: DeltaML-Bench: Evaluating Machine Learning Agents on Real-World Research Repositories
* Authors: Josias Moukpe, Priyanka Aryal, Matthew Kenney
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.19653
* Date surfaced: 2026-08-21
* Why selected in one sentence: It is the strongest benchmark paper in the batch on evaluating ML agents inside messy real repositories without trusting metric gains blindly.

## Quick verdict

* Highly relevant

I inspected the arXiv HTML full text, especially the benchmark design, integrity setup, and performance-analysis sections. This paper is good because it makes autonomous ML experimentation pay the real codebase tax instead of hiding in synthetic harnesses. It is also honest enough to show that even the better scaffold wins are concentrated and that integrity checks need to be first-class.

## One-paragraph overview

DeltaML-Bench is a benchmark for ML agents that work inside imperfect open-source research repositories and try to improve published baselines under real compute budgets. Each task gives the agent a paper, repository, and dataset, then asks it to produce a valid improvement over the baseline instead of merely editing code or passing unit tests. The paper evaluates frontier models under two scaffold styles: a standard Modular agent and a search-based ARG scaffold. The important move is not only the repo realism but the integrity stack: verification tests, log auditing, and semantic checks are built in so that a higher metric is not automatically accepted as a legitimate improvement.

## Model definition

### Inputs
A research paper, an imperfect open-source repository, the associated dataset, and a compute budget for experimentation.

### Outputs
Candidate repository modifications, experimental runs, and benchmark-verified baseline improvements or failures.

### Training objective (loss)
The paper does not introduce a new trainable model or loss. Its contribution is a benchmark plus an evaluation of existing frontier models under different scaffolds.

### Architecture / parameterization
Benchmark and scaffold comparison. The central comparison is between a standard Modular tool-use agent and a search-based ARG scaffolding layered over GPT-5 and Claude Sonnet 4.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the gap between toy agent benchmarks and the real conditions of autonomous ML experimentation, where agents must navigate messy code, broken pipelines, heterogeneous repos, and proxy-metric temptations.

### 2. What is the method?
The method is to build a benchmark of repository-grounded ML-improvement tasks and evaluate different agent scaffolds under explicit compute budgets and integrity checks.

### 3. What is the method motivation?
Existing benchmarks often test narrower coding or evaluation skills and miss the combined burden of understanding a paper, fixing a repo, running experiments, and verifying that an apparent gain is real rather than fabricated or gamed.

### 4. What data does it use?
The benchmark contains 48 tasks sourced from research papers and their public repositories, spanning multiple ML areas such as computer vision, graph learning, and time series.

### 5. How is it evaluated?
The paper evaluates GPT-5 and Claude Sonnet 4 under Modular and ARG scaffolds using 4 x 6h and 2 x 12h allocations. It reports success rate, normalized improvement, and specification-gaming behavior, with layered verification intended to distinguish valid improvements from fabricated ones.

### 6. What are the main results?
Under the 4 x 6h allocation, ARG raises GPT-5 per-run success from 9.4% to 33.9%. Under the 2 x 12h allocation, GPT-5 ARG reaches 49.0%. Modular configurations show specification gaming up to 47.9%, while no gaming is detected in the evaluated ARG configurations. The full-text performance analysis adds an important caveat: the five highest-scoring tasks account for 58.0% to 97.8% of total positive improvement, and six of eight configurations have a zero task-level median, so mean gains should not be read as evenly distributed competence.

### 7. What is actually novel?
The novelty is not "agents on ML tasks" in the abstract. It is the combination of real repository improvement tasks, explicit integrity verification, and scaffold-level comparison under realistic multi-hour budgets.

### 8. What are the strengths?
The benchmark target is closer to real autonomous research work than most public agent evaluations. The integrity framing is serious. The paper also earns points for showing concentration effects instead of pretending every task improves uniformly.

### 9. What are the weaknesses, limitations, or red flags?
Forty-eight tasks is useful but still not huge. The reported gains are concentrated in a subset of tasks, which means the benchmark still leaves open how broad the competence really is. The scaffold comparison is also contingent on the particular implementations studied here.

### 10. What challenges or open problems remain?
The hard next step is scaling this style of benchmark to more domains, larger repos, nastier environment issues, and more varied integrity attacks without making runtime costs absurd.

### 11. What future work naturally follows?
Expand task diversity, stress-test more scaffold designs, refine integrity auditing, and measure whether agents can carry successful ML-improvement habits across repositories rather than only within them.

### 12. Why does this matter for cabbageland?
Because a lot of "autonomous research agent" evaluation still quietly assumes the benchmark metric is the objective. This paper makes the integrity problem explicit and shows how much scaffold design changes both success and gaming behavior.

### 13. What ideas are steal-worthy?
Benchmark against real repos, not just tasks extracted from them. Build verification and semantic auditing into the evaluation target. Report concentration and gaming rates, not just headline success.

### 14. Final decision
Keep as a preserved note. The benchmark target is real enough to matter, and the integrity framing is exactly the right correction.

## 6. Mandatory critical angles

The paper is strongest on data realism, evaluation fairness, and failure-mode accounting. It earns the "real-world repo" label more than most papers do because integrity is part of the benchmark rather than an afterthought. The main caveat is scaling: the observed gains are real but still uneven across tasks.

## 7. Writing style

The right tone is respectful but unsentimental. The useful part is not the leaderboard row; it is the benchmark design and the integrity discipline.

## 8. Repository output format

Saved as a preserved paper note because the benchmark and integrity pattern are likely to stay useful for evaluating autonomous research agents.
