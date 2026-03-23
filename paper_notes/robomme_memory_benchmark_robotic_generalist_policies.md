# RoboMME: Benchmarking and Understanding Memory for Robotic Generalist Policies

## Basic info

* Title: RoboMME: Benchmarking and Understanding Memory for Robotic Generalist Policies
* Authors: Hongze Fu, Jayjun Lee, Yuejiang Liu, Haoran Zhang, Jianing Yang, Chelsea Finn, Nima Fazeli, Joyce Chai
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2603.04639
* Date surfaced: 2026-03-23
* Why selected in one sentence: It provides a more defensible way to talk about robotic memory by separating distinct memory demands and testing them under a common VLA backbone.

## Quick verdict

**Useful**

This is a benchmark paper, so the contribution is mostly evaluative framing rather than a new mechanism. Still, it is useful because it pushes against the lazy habit of reporting one “memory helps” number without distinguishing temporal, spatial, object, and procedural memory demands. I inspected substantial accessible text, but not the full supplement or all benchmark details.

## One-paragraph overview

RoboMME introduces a memory-focused robotic manipulation benchmark with 16 tasks grouped into four suites: Counting for temporal memory, Permanence for spatial memory under occlusion and change, Reference for object identity across time, and Imitation for procedural memory. On top of that benchmark, the paper builds 14 memory-augmented VLA variants on a common pi0.5 backbone to compare symbolic, perceptual, and recurrent memory representations across several integration strategies. The main result is not that one memory design wins universally, but that memory representation effectiveness is strongly task-dependent.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Memory papers in robotic manipulation are hard to compare because they use different backbones, different tasks, and different notions of memory. Existing benchmarks are either too narrow or too easy to really separate memory demands.

### 2. What is the method?
- Build a unified benchmark with four memory types: temporal, spatial, object, and procedural.
- Create 16 tasks spanning those categories.
- Train 14 memory-augmented VLA variants on a common pi0.5 backbone.
- Compare symbolic, perceptual, and recurrent memory representations.
- Compare three integration strategies: memory-as-context, memory-as-modulator, and memory-as-expert.

### 3. What is the method motivation?
If we want to understand whether a memory design works, we need both controlled comparisons and tasks that isolate different memory demands. Otherwise benchmark wins mostly measure cherry-picking.

### 4. What data does it use?
The benchmark contains 16 tasks, 1,600 demonstrations, and roughly 770k training timesteps in simulation, using a ManiSkill-based tabletop setup with a Franka Panda arm.

### 5. How is it evaluated?
The paper evaluates memory-augmented VLAs on the four task suites and compares memory representations and integration strategies under standardized conditions. The goal is to understand cross-task generality, not just one benchmark score.

### 6. What are the main results?
The accessible text says no single memory representation or integration strategy dominates across all tasks. Symbolic memory does well on counting and short-horizon reasoning, while perceptual memory is important for motion-sensitive behavior; perceptual memory with a modulator-style integration appears to give the best overall balance.

### 7. What is actually novel?
The main novelty is the benchmark framing plus the controlled comparison suite. That is less flashy than a new module, but probably more useful than many architecture papers because it clarifies which claims are actually portable.

### 8. What are the strengths?
- Distinguishes different memory demands rather than collapsing them.
- Uses a controlled backbone for comparison.
- Includes tasks with real non-Markovian structure and partial observability.
- Makes it easier to falsify vague memory claims.
- Gives a better language for discussing where symbolic versus perceptual memory helps.

### 9. What are the weaknesses, limitations, or red flags?
- It is still simulation.
- Benchmark taxonomies can harden into categories that future methods overfit.
- The memory types are useful but not exhaustive; planning, causal state, and active information gathering are only partially covered.
- Benchmark papers can attract shallow leaderboard optimization rather than mechanism progress.

### 10. What challenges or open problems remain?
Real-world transfer, active memory querying, persistent memory across episodes, and structured memory tied to planning remain open. So does evaluating whether “memory” is truly used causally rather than correlationally.

### 11. What future work naturally follows?
- Extend the benchmark to real robots and longer horizons.
- Add tasks that require explicit causal state or object permanence under intervention.
- Test hybrid memory designs that switch representation by task regime.
- Build evaluation protocols for memory editing, retrieval, and overwrite behavior.

### 12. Why does this matter for cabbageland?
Because it gives a cleaner evaluation frame for future work on memory and embodied systems. It is useful ammunition against papers that use “memory” as branding without showing what kind of memory problem they actually solve.

### 13. What ideas are steal-worthy?
- Evaluate memory by type, not just aggregate score.
- Compare representations under a common backbone.
- Separate representation choice from integration choice.
- Treat benchmark design itself as part of mechanism research when the field’s claims are too mushy.

### 14. Final decision
**Worth preserving as framing and citation material.** It is not the deepest mechanism paper of the month, but it is genuinely useful for cleaning up how the field talks about memory.