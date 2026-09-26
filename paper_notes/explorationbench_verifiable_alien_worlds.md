# ExplorationBench: Measuring AI Systems' Exploration in Verifiable Alien Worlds

## Basic info

* Title: ExplorationBench: Measuring AI Systems' Exploration in Verifiable Alien Worlds
* Authors: Ming Zhang, Zhenghao Xiang, Peizhong Gao, Yujiong Shen, Yuhui Wang, Zhonghan Yue, Shihan Dou, Zhangyue Yin, Junjie Ye, Shichun Liu, Weihuang Zheng, Jiahao Chen, Jiayi Chen, Hongzhang Liu, Jiaqi Shao, Tao Gui, Qi Zhang, Xuanjing Huang, Suncong Zheng, Maxm Pan
* Year: 2026
* Venue / source: arXiv:2609.30199
* Link: https://arxiv.org/abs/2609.30199
* Date surfaced: 2026-09-26
* Why selected in one sentence: It evaluates exploration as active evidence gathering in unfamiliar executable worlds, with exact held-out grading instead of model-judge scoring.

## Quick verdict

* Useful

This is the agent/evaluation paper worth keeping from the batch because its benchmark target is crisp. It asks whether systems can gather evidence, revise beliefs, and apply new rules after tool access ends. The caveat is that the worlds are synthetic, deterministic, and short-horizon, so this is not proof of scientific discovery ability.

## One-paragraph overview

ExplorationBench creates two "alien" sandboxes whose rules conflict with familiar priors. AlienCode is a small programming language with 31 discovery targets and 70 held-out tasks; AlienLogic is a natural-deduction system with 24 discovery targets and 70 held-out tasks. Each system starts with a flawed manual and fixed examples, then gets four rounds to run probes in the environment. After each milestone, tool access is removed and the system must solve held-out tasks and, for AlienCode, report the rules it believes it discovered. Answers are graded by an interpreter or proof checker, so success is exactly verifiable.

## Model definition

### Inputs

The evaluated systems receive a flawed manual, fixed worked examples, an exploration history, and a tool schema for probing the sandbox during exploration rounds. Held-out evaluation is tool-disabled.

### Outputs

Systems output exploratory probes during interaction, rule reports at milestones, and final answers to held-out AlienCode or AlienLogic tasks.

### Training objective (loss)

The paper does not introduce a new trainable model or training loss. It evaluates black-box frontier AI systems under a fixed benchmark protocol.

### Architecture / parameterization

The contribution is the benchmark architecture: two executable sandboxes, four exploration rounds, milestone evaluation, Best@3 and Mean@3 aggregation, rule-report diagnostics, and control conditions that remove feedback, replay probes, randomize probes, or supply the full rules.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It tries to measure exploration separately from recall and static reasoning. A system must discover unfamiliar rules through interaction and use them on new tasks.

### 2. What is the method?

The benchmark gives systems flawed manuals for executable worlds, lets them choose probes, records exploration history, and evaluates closed-book held-out performance and rule reports after each round.

### 3. What is the method motivation?

Real discovery requires choosing evidence, not just reading provided context. Standard benchmarks are vulnerable to pretraining recall or judge uncertainty, while these alien worlds are unfamiliar and exactly gradable.

### 4. What data does it use?

It uses two synthetic sandboxes: AlienCode with 31 hidden rule changes and AlienLogic with 24 hidden proof-rule patches. Together they contain 55 discovery targets and 140 held-out tasks.

### 5. How is it evaluated?

Ten AI systems run three independent exploration trajectories per sandbox. Scores track milestone held-out accuracy, Best@3, Mean@3, lowest trajectory, rule reports, open-book controls, no-feedback controls, hindsight probes, and randomized probes.

### 6. What are the main results?

In AlienCode, no system exceeds 15.7% before exploration, while the best trajectory reaches 87.6% after four rounds. The same number of turns without environment feedback stays between 0.5% and 11.0%. In AlienLogic, initial scores are higher because standard logic still partly applies, and final Best@3 ranges from 58.1% to 83.8%. The two sandboxes have weak rank correlation at Spearman 0.35. Rule reports correlate with success, but tasks whose required rules are all stated correctly are still solved only 70.9% of the time.

### 7. What is actually novel?

The novelty is the executable alien-world protocol that separates selecting evidence, discovering rules, and applying them after interaction ends.

### 8. What are the strengths?

The benchmark has exact grading, process-level milestones, control conditions, and diagnostics for whether a rule was discovered versus used. It also shows trajectory instability rather than hiding behind a single final leaderboard.

### 9. What are the weaknesses, limitations, or red flags?

The environments are deterministic, synthetic, cheap to probe, and only four rounds long. Real science has noisy observations, expensive experiments, incomplete feedback, and open-ended hypotheses. Three trajectories per system are enough to reveal variability but not to estimate it precisely.

### 10. What challenges or open problems remain?

Open problems include richer stochastic environments, longer exploration horizons, cost-aware probing, memory across sessions, and benchmarks where hypotheses can be partially correct rather than exactly executable.

### 11. What future work naturally follows?

A useful extension would combine executable hidden rules with continuous noisy measurements and explicit experiment costs. Another is to test systems that maintain structured hypotheses rather than free-form notes.

### 12. Why does this matter for cabbageland?

Cabbageland cares about systems that learn from interaction rather than merely retrieve. This benchmark is a clean diagnostic for evidence acquisition and rule use.

### 13. What ideas are steal-worthy?

Use worlds whose rules contradict familiar priors. Grade with executable checkers. Track milestones, not just endpoints. Separate "found the rule" from "can use the rule." Report trajectory spread.

### 14. Final decision

Preserve. It is synthetic, but the evaluation design is sharper than most agent benchmarks.
