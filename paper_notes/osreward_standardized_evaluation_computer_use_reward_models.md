# OSReward: Instituting Standardized Evaluation for Cross-Platform Computer-Use Reward Models

## Basic info

* Title: OSReward: Instituting Standardized Evaluation for Cross-Platform Computer-Use Reward Models
* Authors: Qiushi Sun, Kanzhi Cheng, Yian Wang, Bowen Yang, Hang Yan, Liheng Chen, et al.
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.28609
* Date surfaced: 2026-08-01
* Why selected in one sentence: It treats the trajectory judge as a real systems bottleneck, benchmarks it directly, exposes a shared leniency bias, and then ships a cheaper open reward model that attacks the actual cost problem.

## Quick verdict

**Must read**

I inspected the arXiv PDF, especially the benchmark construction, annotation protocol, judge evaluation, cost-vs-accuracy analysis, and the OS-Shepherd dataset/model sections. This is the strongest direct paper in the batch because it focuses on the hidden component many computer-use pipelines already depend on. The main caveat is that the benchmark and follow-on reward models still inherit the authors' task design and labeling ontology, so this is serious infrastructure work, not a final answer to judge reliability.

## One-paragraph overview

OSReward asks a necessary question that the field has mostly dodged: if VLMs are being used to judge computer-use trajectories for evaluation, filtering, and reinforcement learning, how good are those judges actually? The paper builds a human-gold benchmark of cross-platform CUA trajectories, adds a hard subset and a finer-grained multi-label subset, evaluates a large judge set, and finds a consistent leniency bias where failed trajectories are misread as successes. The useful second move is to turn that diagnosis into OS-Shepherd-100K plus open 9B and 35B reward models that sit much closer to the useful cost-accuracy frontier than prior open options.

## Model definition

### Inputs
The benchmark takes computer-use trajectories spanning actions, states, screenshots, and agent reasoning traces across multiple platforms and applications.

### Outputs
The core output is a trajectory-level judgment of whether the task succeeded, with additional fine-grained labels in OSReward-Multi for efficiency and alignment-style analysis.

### Training objective (loss)
The paper is primarily a benchmark and judge-study paper rather than a new end-to-end agent objective. The follow-on OS-Shepherd models are trained on reasoning-annotated judgment data to predict reliable reward signals for CUA trajectories.

### Architecture / parameterization
OSReward itself is a benchmark plus annotation pipeline. The learned component the paper contributes is OS-Shepherd, released in 9B and 35B variants as open reward models trained on the OS-Shepherd-100K judgment corpus.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve judge reliability for computer-use agents. The field increasingly relies on VLM judges because humans and handwritten verifiers do not scale, but that only helps if the judges are actually trustworthy enough for evaluation and RL.

### 2. What is the method?
The method is to benchmark the judge itself. The authors build human-gold cross-platform trajectories, derive OSReward-Hard for genuinely difficult cases and OSReward-Multi for finer-grained analysis, evaluate 27 judges, then train open reward models on a large reasoning-annotated judgment corpus shaped by the failure modes the study exposes.

### 3. What is the method motivation?
If the judge is noisy, the whole stack gets poisoned: benchmarks become misleading, filtered datasets drift, and RL rewards teach the wrong thing. That makes the judge part of the system rather than a disposable helper.

### 4. What data does it use?
The benchmark uses 1,019 human-gold trajectories collected on realistic stock environments spanning web, mobile, Ubuntu, and Windows workflows. The follow-on training corpus, OS-Shepherd-100K, is curated from more than 300K judge instances into nearly 100K reasoning-annotated samples.

### 5. How is it evaluated?
The paper evaluates 27 judges on full OSReward, OSReward-Hard, and the multi-label view, measuring binary judgment quality, judge bias, robustness, and cost. It also places the trained OS-Shepherd models on the same cost-accuracy frontier.

### 6. What are the main results?
Current frontier judges look less reassuring once the hard cases are isolated: the best models drop below 70 percent on OSReward-Hard, and the errors share a leniency bias that overcalls failed runs as successes. The few judges good enough to trust are too expensive for large-scale use. OS-Shepherd-9B and OS-Shepherd-35B then close much of that gap, matching strong commercial judges at roughly 30x to 60x lower cost.

### 7. What is actually novel?
The novelty is not merely another agent benchmark. The important move is to make judge reliability itself the benchmark target, then connect the diagnosis to an open reward-model training set and practical cost frontier.

### 8. What are the strengths?
The paper attacks the right hidden variable. The benchmark construction is serious, the hard subset is more informative than aggregate score theater, the bias analysis is operationally meaningful, and the paper does not stop at complaint; it turns the findings into a usable open reward model line.

### 9. What are the weaknesses, limitations, or red flags?
The benchmark scope is still finite and author-shaped. The judgment ontology is careful but not universal. OS-Shepherd is trained on labels derived from the same study ecosystem, so it reduces a revealed gap rather than fully escaping the benchmark's assumptions.

### 10. What challenges or open problems remain?
The big open problem is robust reward judging across broader environments, failure types, and agent styles without silently inheriting benchmark-specific blind spots. Calibration under distribution shift also remains unresolved.

### 11. What future work naturally follows?
Future work should test judge robustness on novel applications, adversarial trajectories, and longer tasks; measure calibration more explicitly; and build reward models that expose confidence rather than only a verdict.

### 12. Why does this matter for cabbageland?
It matters because cabbageland keeps touching agent evaluation loops. If a cheap learned judge becomes the truth oracle for filtering data or training policies, then benchmarking the judge itself is not optional bookkeeping; it is core systems work.

### 13. What ideas are steal-worthy?
Build a hard subset from human-disagreement and real failure modes rather than random sampling. Measure cost and bias jointly, not just raw score. Treat open reward-model training as a direct response to diagnosed benchmark failure modes.

### 14. Final decision
**Keep it.** This is direct, practical infrastructure for agent evaluation, and it improves the field's object-level discipline rather than just adding another scorecard.
