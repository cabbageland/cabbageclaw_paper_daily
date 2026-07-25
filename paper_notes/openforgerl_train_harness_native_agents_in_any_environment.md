# OpenForgeRL: Train Harness-native Agents in Any Environment

## Basic info

* Title: OpenForgeRL: Train Harness-native Agents in Any Environment
* Authors: Xiao Yu, Baolin Peng, Ruize Xu, Hao Zou, Qianhui Wu, Hao Cheng, Wenlin Yao, Nikhil Singh, Zhou Yu, Jianfeng Gao
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.21557
* Date surfaced: 2026-07-25
* Why selected in one sentence: It treats the deployment harness as part of the trainable object instead of pretending a simplified loop is an adequate stand-in.

## Quick verdict

**Must read**

This is one of the more useful recent agent-systems papers because it attacks the real train-deploy mismatch rather than polishing another benchmark scaffold. I inspected the arXiv abstract / HTML sections covering the introduction, related work, methods, experiments, and discussion, with special attention to the proxy-orchestrator design, benchmark results, and the harness-choice analysis.

## One-paragraph overview

The paper argues that open RL stacks still train the wrong object for serious agents. Real agents now depend on stateful inference harnesses that manage tools, context, subprocesses, browsers, and remote environments, but open training pipelines usually flatten that into a simplified loop that only vaguely resembles deployment. OpenForgeRL keeps the real harness in place. A lightweight proxy serves the harness's model calls while recording them for standard RL codebases, and a Kubernetes-based rollout orchestrator runs each episode inside its own remote container. This lets the authors train claw-style and GUI agents in their actual harnesses rather than in a toy imitation, then study how harness choice and RL affect behavior.

## Model definition

### Inputs
The framework takes a base model, a real agent harness, an environment or sandbox in which that harness runs, and task trajectories or reward-bearing interaction episodes.

### Outputs
It outputs trajectories reconstructed in a format standard RL or SFT code can consume, plus trained agent checkpoints evaluated back inside real harnesses.

### Training objective (loss)
The paper does not introduce one new learning loss. The contribution is infrastructure that lets ordinary SFT and RL objectives operate over real harness rollouts.

### Architecture / parameterization
The system has two central pieces: a lightweight proxy that intercepts harness model calls and reconstructs training samples, and a Kubernetes rollout orchestrator that runs each harness-environment pair remotely and asynchronously at scale.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to solve the fact that strong agents are deployed inside complicated harnesses, but most open training pipelines cannot train directly on those harnesses without a large train-deploy mismatch.

### 2. What is the method?
The method is to decouple harness inference from training. The harness runs normally, but its model calls are proxied, logged, and reconstructed into trajectory data that standard RL infrastructure can optimize over. Remote rollout orchestration handles the stateful environment side.

### 3. What is the method motivation?
The motivation is that harness behavior is now a large fraction of agent capability. If tool policy, context policy, branching, and subagent behavior live in the harness, then training outside that harness misses the actual control surface.

### 4. What data does it use?
The framework is validated on claw-style and GUI-agent training data, with only hundreds to a few thousand tasks per setting. Evaluation spans ClawEval, QwenClawBench, MCPAtlas, OSWorld-Verified, Online-Mind2Web, and WebVoyager.

### 5. How is it evaluated?
The paper evaluates trained agents on multiple claw and GUI benchmarks, compares them to open baselines of similar scale, and then analyzes behavior differences across harnesses and before/after RL.

### 6. What are the main results?
OpenForge-Claw reaches `31.7` `pass^3` and `55.9` `pass@3` on ClawEval, `33.7` on QwenClawBench, and `28.1` on MCPAtlas. OpenForge-GUI reaches `37.7` on OSWorld-Verified, `63.0` on Online-Mind2Web, and `72.3` on WebVoyager. The analysis also finds that some harnesses are much easier to learn than others, and RL improves self-verification, tool coverage, and task completion, though error recovery remains difficult.

### 7. What is actually novel?
The novelty is not "RL for agents" by itself. It is the train-in-the-real-harness framing plus the lightweight proxy and remote orchestration scheme that make standard open RL stacks usable without reimplementing the harness.

### 8. What are the strengths?
It is unusually aligned with the actual deployment object, it spans both claw and GUI settings, and it uses the setup to ask a better question than most benchmark papers do: which capabilities are really coming from harness choice versus RL?

### 9. What are the weaknesses, limitations, or red flags?
The work still depends on the quality of synthesized task data, benchmark selection, and the chosen harness implementations. It is infrastructure-heavy, so reproducibility may be harder than the paper's abstraction suggests. The authors also show that RL does not magically solve core recovery failures.

### 10. What challenges or open problems remain?
Robust error recovery, broader environment diversity, cleaner behavioral attribution, and cheaper large-scale training in real harnesses remain open.

### 11. What future work naturally follows?
Train on richer long-horizon workloads, compare harness policies more systematically, and use the framework to study which agent capabilities are learned, inherited from the harness, or still missing entirely.

### 12. Why does this matter for cabbageland?
Cabbageland keeps caring about tool-using agents as systems, not just as base models. This paper gives a concrete recipe for training and studying the actual deployed system boundary instead of an easier surrogate.

### 13. What ideas are steal-worthy?
Treat the harness as part of the model. Proxy real inference instead of rewriting it. Keep rollout infrastructure separate from the trainer. Measure behavior changes like self-verification and error recovery directly, not just final success.

### 14. Final decision
**Keep it.** This is a real infrastructure paper with a clean thesis and direct practical relevance to anyone building or studying serious agent harnesses.
