# PAWBench: How Far Are We from Probabilistically Aligned World Modeling?

## Basic info

* Title: PAWBench: How Far Are We from Probabilistically Aligned World Modeling?
* Authors: Yuandong Pu, Le Zhuo, Sayak Paul, Gabriel Jorge Menezes, Avram Dordevic, Shiyang Li, Yifan Zhou, Bin Fu, Wenlong Zhang, Junjun He, Qiao Yu, Yihao Liu, Jingbo Xing, Xi Chen
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.27345
* Date surfaced: 2026-08-29
* Why selected in one sentence: It evaluates video world models against the right object: the induced distribution over valid futures under fixed observation and action.

## Quick verdict

* Must read

I inspected the full arXiv HTML text, especially the benchmark design, the repeated-rollout evaluation protocol, the language/noise/training interventions, and the limitation section. This paper earns a preserved note because it stops letting a single plausible sample impersonate a world model. The benchmark is not decorative; it changes what failure becomes visible.

## One-paragraph overview

The paper formalizes probabilistic alignment for video world models: under the same initial observation and action, a model should recover both the valid set of possible futures and the relative probability mass over them. It introduces PAWBench, a 50-scenario benchmark with two tracks. PAW-Calibration contains scenes with defensible reference distributions, while PAW-Coverage contains scenes where only the valid support can be enumerated. PAWEval maps repeated rollouts to terminal outcomes, then scores total variation distance on the calibrated track and valid-support recovery on the coverage track. The authors then probe whether prompt engineering, coupled noise sampling, or training-distribution adaptation can move a model closer to genuine distributional alignment.

## Model definition

### Inputs
Fixed source images, fixed action prompts, repeated video rollouts from the evaluated generators, and a discrete outcome schema per scenario. Some auxiliary experiments also use direct VLM future descriptions instead of generated videos.

### Outputs
Empirical outcome distributions, readable-scene pass rates, calibration TVD, and valid-support coverage scores.

### Training objective (loss)
There is no new learnable predictive model as the main contribution. The paper is primarily a benchmark and evaluation protocol. The LoRA intervention section fine-tunes a Wan2.2 base model, but the benchmark itself is not a training method.

### Architecture / parameterization
PAWBench is an evaluation scaffold built around repeated sampling, a fixed outcome ontology, and outcome-level aggregation via PAWEval. The evaluated models are external video generators and VLMs, not components introduced by the paper.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to measure whether video generators that are increasingly called world models actually learn the distribution of possible futures rather than merely emit a plausible-looking sample.

### 2. What is the method?
The method is a repeated-rollout benchmark. For each scenario, the initial observation and action are fixed, the model is sampled many times, each rollout is mapped to a terminal outcome, and the induced outcome distribution is compared either to a known reference distribution or to the valid support set.

### 3. What is the method motivation?
Single-rollout plausibility misses the central world-model question in stochastic environments. A system can produce individually plausible videos while collapsing to too few futures or assigning them the wrong relative frequencies.

### 4. What data does it use?
It uses 50 controlled scenarios spanning multiple physical mechanism groups. The main evaluation covers 11 current video generators, and auxiliary experiments also test several VLMs that predict possible outcomes directly from the same initial observation and action.

### 5. How is it evaluated?
PAW-Calibration uses conditional TVD against reference outcome distributions. PAW-Coverage measures valid-support recovery. Both tracks also report scoreable-scene pass rate so conditional accuracy is not confused with evaluation reliability. Auxiliary studies test human agreement, larger rollout budgets, prompt engineering, coupled noise sampling, and LoRA adaptation.

### 6. What are the main results?
No evaluated model jointly achieves accurate probability mass, broad support recovery, and strong scene reliability. In the main table, Cosmos 3 Super I2V has the best calibration TVD at 20.5 but only 80.0% calibration scene pass rate. LTX-2.3 has the best coverage average at 71.7% but only 72.0% coverage scene pass rate. C2C noise coupling improves finite-budget exploration for all three tested generators without changing the learned distribution itself. LoRA adaptation can shift outcome frequencies, but the shifts look like a shared directional bias rather than clean scene-conditioned probability learning.

### 7. What is actually novel?
The novelty is not "yet another video benchmark." It is defining world-model quality at the distribution level and operationalizing it with separate tests for probability-mass alignment, support recovery, and scene-level scoreability.

### 8. What are the strengths?
The paper measures the right object, keeps reliability separate from conditional quality, and uses interventions that distinguish steering, exploration, and learning. The causal versus non-causal cue probes are especially strong because they test whether the model responds to the underlying transition rather than to irrelevant surface hints.

### 9. What are the weaknesses, limitations, or red flags?
The evaluation collapses trajectories to terminal outcomes, so it does not fully score intermediate dynamics. The scenarios are controlled and short-horizon rather than richly interactive. Outcome readout itself can fail, which is why the pass-rate accounting is necessary. The training-intervention section is diagnostic rather than a full recipe for fixing the problem.

### 10. What challenges or open problems remain?
Longer-horizon, interactive, embodied, and partially observed environments remain open. So does evaluating whether a world model learns the right state-conditioned distribution without reducing everything to terminal outcomes.

### 11. What future work naturally follows?
The obvious next step is to extend the protocol into interactive environments with stronger state interventions, richer outcome schemas, and trajectory-level measurements. Another direction is training models directly against distributional alignment rather than relying on prompt tricks or sampling heuristics.

### 12. Why does this matter for cabbageland?
Because cabbageland keeps caring about explicit state and honest evaluation. This paper gives a concrete way to say when a video generator is doing world modeling versus when it is just producing a good-looking sample from the wrong distribution.

### 13. What ideas are steal-worthy?
Evaluate repeated samples under fixed initial conditions. Separate conditional quality from evaluation reliability. Distinguish support recovery from probability-mass alignment. Use paired causal and non-causal scene edits to test whether a model is tracking the transition rather than reacting to distraction text or surface style.

### 14. Final decision
Keep as a preserved note. This is one of the better recent benchmark papers because it forces the field to answer the right question instead of polishing the wrong metric.

## 6. Mandatory critical angles

The motivation is right, the mechanism is explicit, and the representation claim is honest: the paper is not pretending a latent rollout is enough unless the induced distribution is right. The evaluation is also much fairer than usual because it refuses to hide readout failures, and the intervention section helps separate what belongs to prompting, sampling, or learning. The main limitation is scope. The scenarios are still controlled enough that a future system could game the protocol while remaining weak in richer environments, but that is a normal benchmark limit rather than a conceptual flaw.

## 7. Writing style

The tone should be approving but severe. The paper deserves credit for measuring the real object without inflating itself into a total theory of world models.

## 8. Repository output format

Saved as a preserved paper note because probabilistic alignment is a durable evaluation lens for future world-model work.
