# Reinforcement Learning without Ground-Truth Solutions can Improve LLMs

## Basic info

* Title: Reinforcement Learning without Ground-Truth Solutions can Improve LLMs
* Authors: Yingyu Lin, Qiyue Gao, Nikki Lijing Kuang, Xunpeng Huang, Kun Zhou, Tongtong Liang, Zhewei Yao, Yi-An Ma, Yuxiong He
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.27369
* Date surfaced: 2026-06-27
* Why selected in one sentence: It turns unknown-optimum executable optimization tasks into calibrated RL signals for LLMs without requiring gold answers.

## Quick verdict

* Must read

This is the strongest agent-training paper in today's scan. I inspected the full arXiv PDF, including the reward formulation, training setup, main results, case study, and discussion. I did not run the code or audit the hidden-task evaluators, so the exact transfer claims remain paper claims, but the mechanism is clean and reusable.

## One-paragraph overview

RiVER extends reinforcement learning with verifiable rewards beyond exact answer matching. For each open-ended algorithmic optimization problem, the model samples multiple executable solvers, each solver is run on the same hidden instances, and the evaluator returns feasibility plus objective quality rather than a gold program. RiVER converts those raw objective values into per-instance ranks, gives a separated reward to the best valid solver, assigns bounded graded feedback to other valid solvers, and then trains with GRPO. The point is not "use scores as rewards"; the point is that raw scores are badly calibrated, while shared-instance relative comparisons can be a transferable supervision signal.

## Model definition

### Inputs

The policy model receives an algorithmic problem prompt and produces a response ending in executable code. During training, each prompt is paired with deterministic evaluators and hidden test instances from AtCoder Heuristic Contest tasks. For each prompt, a group of sampled programs is executed on the same hidden instances so their feasible outputs can be compared under identical conditions.

### Outputs

The learned model outputs executable solution programs. The training pipeline outputs validity indicators, objective scores, instance-wise ranks, shaped rewards, and GRPO advantages. Evaluation outputs ALE-Bench rating/rank and pass@1 accuracy on LiveCodeBench v5/v6 and USACO.

### Training objective (loss)

The paper uses GRPO with the standard clipped objective and KL regularization, but replaces binary correctness or raw objective rewards with RiVER's rank-induced winner-heavy advantages. Invalid executions receive -1. The best valid solver on an instance receives 1. Other valid non-winners receive bounded graded rewards in roughly [-0.5, 0.5], based on average-tie instance-wise ranks. The final advantage is averaged across hidden instances.

### Architecture / parameterization

RiVER is a post-training framework for autoregressive coding LLMs. The reported backbones are Qwen3-8B and GLM-Z1-9B-0414. The learned component is the policy model; the evaluators are deterministic program-execution environments, not learned reward models.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Standard RLVR works best when a generated answer can be checked against a known ground truth: a unit test, exact math answer, or reference output. Many valuable tasks do not look like that. In algorithm engineering, planning, scheduling, and optimization, there may be many feasible solutions, no known optimum, and only a task-specific objective for comparing quality. The paper asks whether those ground-truth-free but executable tasks can still train general LLM capability.

### 2. What is the method?

RiVER samples a group of candidate programs for a problem, executes each program on the same hidden test instances, checks feasibility, computes objective scores, ranks candidates separately within each hidden instance, and maps those ranks to shaped rewards. This removes arbitrary score-scale differences between instances and prevents frequent mediocre strategies from dominating rare strong candidates. The shaped rewards are then used as GRPO advantages.

### 3. What is the method motivation?

Raw score feedback is richer than binary correctness, but it is not automatically a good reward. One hidden instance may have a score range of thousands while another has a range of tens, so direct averaging lets scale dominate learning. Group-relative RL also has a frequency problem: a repeatedly sampled suboptimal template can receive more aggregate update mass than a rare best program. RiVER is motivated by preserving relative quality while reducing scale dominance and repeated-mode dominance.

### 4. What data does it use?

Training uses 12 AtCoder Heuristic Contest tasks from AHC047-AHC062 after excluding tasks incompatible with the paper's one-pass setting. The paper says these are after the ALE-Bench cutoff, avoiding overlap with the main score-based evaluation. Each task supplies a prompt, official evaluator, and test-instance generator.

### 5. How is it evaluated?

The score-based evaluation uses ALE-Bench, reporting AtCoder-style rating and percentile rank. Exact-solution transfer is tested on LiveCodeBench v5, LiveCodeBench v6, and USACO with average pass@1 over three runs. The paper compares RiVER against the original backbones and reward-design variants: Raw-GRPO, risk-sensitive GRPO, raw binary winner-take-all, instance-normalized score rewards, and uniform rank rewards.

### 6. What are the main results?

RiVER raises Qwen3-8B ALE rating from 845 to 987 and improves its rating percentile rank from 86.4 to 77.5. For GLM-Z1-9B-0414, ALE rating rises from 805 to 962 and rank percentile from 88.2 to 78.8. Across LiveCodeBench and USACO, the paper reports average absolute gains of 2.4 points for Qwen3-8B and 3.5 points for GLM-Z1-9B. Raw-score baselines improve ALE rating but do not consistently transfer to exact-solution benchmarks.

### 7. What is actually novel?

The novelty is the reward calibration for ground-truth-free executable optimization. The paper is not the first to use execution feedback, group-relative RL, rankings, or coding tasks. The useful new piece is the combination of shared hidden instances, instance-wise ranks, average-tie handling, and winner-heavy bounded shaping, aimed specifically at tasks where no gold solution exists.

### 8. What are the strengths?

The method targets a real limitation of answer-matching RLVR. It separates "verifiable" from "has a known answer," which is exactly the right move for open-ended agent training. The ablation set is also valuable: raw scores, normalized scores, binary winners, and uniform ranks all tell different stories, making the case that the reward shape matters rather than just the task pool.

### 9. What are the weaknesses, limitations, or red flags?

The scope is still narrow: two models, coding tasks, and 12 training environments. The paper does not have a dedicated limitations section in the main text, so the caveats have to be inferred from the setup. The method depends on deterministic evaluators that are cheap and reliable enough to run repeatedly; many real tasks will not have that. The transfer to non-coding domains is plausible but unproven. The reported gains are moderate on exact pass/fail benchmarks, and I did not audit whether the AHC tasks or generators contain hidden leakage or evaluator quirks.

### 10. What challenges or open problems remain?

The main challenge is building comparable executable environments outside programming contests. A second challenge is preventing reward hacking when the evaluator is partial, noisy, or gameable. A third is deciding how to rank candidates when objectives are multi-dimensional, safety-constrained, or have long-horizon delayed effects.

### 11. What future work naturally follows?

Apply the same reward design to planning domains, simulator tasks, theorem search, data-analysis agents, and scientific optimization where candidates can be compared but no optimum is known. Study robustness under noisy or adversarial evaluators. Combine relative executable feedback with process supervision so the model learns not only high-scoring programs but also why certain strategies work.

### 12. Why does this matter for cabbageland?

Cabbageland agents will often face tasks where there is no canonical answer: better plans, better experiments, better retrieval strategies, better code patches, better generated artifacts. RiVER gives a useful template: make a small competitive batch, evaluate under shared conditions, rank locally, then learn from relative quality instead of pretending raw scores are globally meaningful.

### 13. What ideas are steal-worthy?

Use shared-instance evaluation before comparing candidates. Convert raw objective values to within-instance ranks before aggregating. Give the best candidate a clear separated reward while keeping bounded information from non-winning valid candidates. Treat feedback resolution as a property of the environment: a good training environment should separate on-policy samples into meaningful levels, not just pass/fail.

### 14. Final decision

Keep and cite. This is a clean mechanism for moving RLVR beyond answer matching, with useful caveats about calibration and scope.
