# DecompRL: Solving Harder Problems by Learning Modular Code Generation

## Basic info

* Title: DecompRL: Solving Harder Problems by Learning Modular Code Generation
* Authors: Juliette Decugis, Fabian Gloeckle, Francis Bach, Taco Cohen, Gabriel Synnaeve
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.02390
* Date surfaced: 2026-07-05
* Why selected in one sentence: It turns hard verified code generation into modular generation plus cheap recombination, which is a more interesting scaling axis than more monolithic retries.

## Quick verdict

* Must read

This is the strongest paper today because it changes the unit of search. I inspected the full arXiv HTML, including the method, results, cost analysis, and limitations. The central mechanism is transferable: when generation is expensive and verification is cheap, generate recombinable parts rather than whole attempts.

## One-paragraph overview

DecompRL targets code problems where ordinary pass@k sampling and standard RL both run out of steam. If the base model almost never writes a correct monolithic program, sampling more full programs burns GPU tokens without exploring the right space, while RL can improve pass@1 but often reduces diversity at high sampling budgets. DecompRL instead trains a model to decompose a programming problem into subfunctions and then generate multiple implementations for each subfunction. Recombining those implementations yields many candidate full programs for a small generation budget, moving the dominant search cost from GPU inference to CPU-side test execution. The paper is not saying decomposition is free; it explicitly names the format tax and low-budget weakness. But for hard verifier-rich tasks, the mechanism is good.

## Model definition

### Inputs
The system takes a competitive-programming problem statement, plus the training-time verifier signal from executable tests. In hierarchical inference, the decomposition policy conditions on the problem and emits a module structure; the implementation policy conditions on the problem plus a selected function specification or decomposition context.

### Outputs
It outputs a hierarchy of function definitions and multiple candidate implementations per function. At inference time, these module implementations are recombined into complete candidate programs that are executed against tests.

### Training objective (loss)
The paper trains decomposition and implementation policies with reinforcement learning from verifiable code-execution rewards. It emphasizes pass@tokens / high-pass@k behavior rather than only pass@1. The objective uses reward aggregation such as logmeanexp to optimize utility across recombinations, with leave-one-out style baselines and ablations discussed in the accessible text.

### Architecture / parameterization
A two-policy hierarchical code-generation stack built on LLM code models. The experiments reported in the accessible text include Qwen 2.5 7B and Code World Model 32B settings. The learned pieces are the decomposition policy and implementation policy; the verifier is executable code testing.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Hard code-generation problems often have sparse rewards. Standard sampling scales linearly in GPU cost, and ordinary RL can make one attempt better while reducing the diversity needed for high-budget search. DecompRL asks how to solve tasks whose correct monolithic program is nearly absent from the base policy distribution.

### 2. What is the method?
The method decomposes the problem into independently implementable functions, samples multiple implementations for each function, recombines them into candidate full programs, and evaluates those combinations cheaply with tests. Training explicitly encourages decompositions and implementations whose recombinations produce successful programs.

### 3. What is the method motivation?
If a problem has modular structure and a cheap verifier, the combinatorial product of modules can cover far more candidate programs than the same number of monolithic samples. This is the classic engineering intuition behind modularity, but turned into a training and inference scaling method for LLM code generation.

### 4. What data does it use?
The paper evaluates on LiveCodeBench and CodeContests-style programming tasks. The accessible text reports experiments with Qwen 2.5 7B and Code World Model 32B, with executable code tests providing reward / verification.

### 5. How is it evaluated?
It reports solve rate under token budgets, pass@tokens, pass@k-style behavior, recombination ablations, and wall-clock / GPU-token cost comparisons. The paper also checks whether recombination itself matters and whether the learned decomposition policy improves over hierarchical inference without RL.

### 6. What are the main results?
On LiveCodeBench with Qwen 2.5 7B, DecompRL is weak at low budgets but improves at high budgets: the table reports 0.48 solve rate at 500K tokens versus 0.46 for the strongest listed high-pass baseline and 0.44 for GRPO. The cost table is more important than the small absolute benchmark gap: at 512 evaluations per problem, DecompRL generates about 4K tokens versus about 198K for standard sampling, a roughly 50x GPU-token reduction, with the remaining cost dominated by CPU execution.

### 7. What is actually novel?
The novelty is not "use helper functions." It is treating modular decomposition as the object of RL and evaluating the resulting policy in the high-budget verified-search regime. The method explicitly optimizes the usefulness of recombinations rather than only the quality of a single sampled program.

### 8. What are the strengths?
The paper has a real mechanism, a clear cost model, and a failure-mode-aware limitations section. It also aligns well with practical agent engineering: verifiers, unit tests, schemas, and simulators are often cheaper than additional model calls.

### 9. What are the weaknesses, limitations, or red flags?
The decomposition format has a tax. The paper says hierarchical inference without RL can underperform standard inference, and DecompRL is worse on easy problems or low token budgets where a strong base model can already write the program directly. There is also a size-collapse concern: the decomposition policy can learn to reduce the number of functions, drifting back toward ordinary whole-program generation.

### 10. What challenges or open problems remain?
The big open problem is robust decomposition for tasks where module boundaries are ambiguous or where local module correctness does not compose cleanly into global correctness. Another challenge is verifier realism: competitive programming has crisp tests, while agent workflows often need partial, probabilistic, or human-facing validators.

### 11. What future work naturally follows?
Use DecompRL-style search for code repair, tool-plan synthesis, verified data transforms, formal proof lemmas, scientific workflow generation, and other tasks with cheap validators. Distillation from successful recombinations back into a stronger monolithic or modular policy is also a natural next step.

### 12. Why does this matter for cabbageland?
Cabbageland keeps caring about explicit structure that does real computational work. DecompRL is a good example: modules are not decoration in the prompt, they create a different search geometry. For agent infrastructure, this suggests a concrete recipe: generate smaller pieces, recombine them, and let validators do as much cheap work as possible.

### 13. What ideas are steal-worthy?
Shift expensive model calls from whole-solution retries to candidate module generation. Use cheap validators to search the recombination space. Optimize for high-budget diversity and recombinability, not only pass@1. Treat decomposition collapse as a reward-hacking failure to monitor.

### 14. Final decision
Keep as a must-read mechanism paper. It is narrow to verified code in the current evidence, but the idea is broadly useful for agent systems where generation is expensive and validation is comparatively cheap.
