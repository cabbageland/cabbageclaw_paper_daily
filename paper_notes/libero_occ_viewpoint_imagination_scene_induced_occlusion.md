# LIBERO-Occ: Evaluating and Improving Vision-Language-Action Models under Scene-Induced Occlusion via Viewpoint Imagination

## Basic info

* Title: LIBERO-Occ: Evaluating and Improving Vision-Language-Action Models under Scene-Induced Occlusion via Viewpoint Imagination
* Authors: Taishan Li, Jiwen Zhang, Siyuan Wang, Xuanjing Huang, Zhongyu Wei
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.10862
* Date surfaced: 2026-06-10
* Why selected in one sentence: It turns scene-induced occlusion into a controlled VLA partial-observability benchmark and tests generated complementary views as an explicit missing-evidence interface.

## Quick verdict

**Keep.**

This is a useful VLA robustness and framing paper. The benchmark is at least as important as the proposed method: it shows that standard LIBERO success can hide dependence on full visibility of task-relevant objects and receptacles. I inspected the full arXiv PDF. Confidence is good on the benchmark construction, main tables, and limitations. The main caveat is that LIBERO-Occ is simulation-only, so the results should be treated as a controlled partial-observability study rather than proof of real-world occlusion robustness.

## One-paragraph overview

LIBERO-Occ extends LIBERO by physically adding occluders to manipulation scenes while preserving task semantics and replay-verifying that tasks remain executable. It categorizes occlusions by target type: manipulated object, receptacle, and dual occlusion, and splits severity by how much of the target becomes invisible. The authors show that several strong VLA baselines drop sharply under this scene-induced occlusion, even when they perform well on original LIBERO. Their method, VIM, generates a complementary viewpoint from the occluded primary observation, then predicts actions conditioned on both the observed and imagined visual evidence. The point is not that generated views solve occlusion completely. The point is that missing task evidence is a real state variable and should be represented explicitly.

## Model definition

### Inputs
The policy receives a primary RGB observation and language instruction. During training, it can use paired primary and complementary views. At inference, it can operate camera-free by generating the complementary view from the primary occluded observation.

### Outputs
The model generates an imagined complementary view and a low-level action sequence. The paper also reports a ground-truth complementary-view setting as an upper-bound reference.

### Training objective (loss)
VIM uses a two-stage strategy. Stage 1 trains viewpoint imagination. Stage 2 jointly optimizes action prediction with an auxiliary view-generation loss so the intermediate visual segment stays valid and useful for control.

### Architecture / parameterization
The implementation builds on a UniVLA-style world model with an Emu3-MoE autoregressive backbone for unified image-token and action-token generation. Robot actions are tokenized with FAST. The key interface is an autoregressive sequence containing language, observed visual tokens, generated complementary visual tokens, and action tokens.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Most VLA evaluations assume task-relevant objects and goal regions are visible. Real manipulation often violates that assumption through occlusion by nearby objects, open drawers, robot arms, or scene geometry. The paper asks whether VLAs can act when crucial evidence is missing from the primary view.

### 2. What is the method?
The work has two pieces. First, LIBERO-Occ creates physically grounded occluded manipulation tasks with controlled occlusion target type and severity. Second, VIM generates a complementary viewpoint from the occluded primary observation and conditions action prediction on both the observed and imagined evidence.

### 3. What is the method motivation?
The motivation is that generation can act as perception completion. If the model can imagine a complementary view that exposes hidden task evidence, that intermediate representation may help the policy recover object/receptacle state without extra cameras or active viewpoint control.

### 4. What data does it use?
LIBERO-Occ is built from LIBERO. The benchmark contains 2,000 occluded tasks across manipulated-object, receptacle, and dual occlusion types, with light, medium, and heavy severity levels. The paper evaluates on original LIBERO and LIBERO-Occ, with 500 rollouts per suite for main evaluation.

### 5. How is it evaluated?
The paper compares VIM against UniVLA, OpenVLA, OpenVLA-OFT, pi-0, and pi-0.5 on original LIBERO and LIBERO-Occ. It reports average success by suite, average drop under occlusion, occlusion-target-type breakdowns, severity breakdowns, and ablations for the two-stage viewpoint-imagination training.

### 6. What are the main results?
On original LIBERO, most methods perform strongly. On LIBERO-Occ, success drops substantially. The best baseline average is UniVLA at 57.10%, while VIM reaches 65.05% without ground-truth complementary view. With the ground-truth complementary view, VIM reaches 74.00%, showing that missing visual evidence is genuinely useful. VIM also has the smallest average drop from original LIBERO to LIBERO-Occ among the camera-free methods.

### 7. What is actually novel?
The novelty is the combination of physically instantiated occlusion evaluation and generated complementary-view conditioning. Many robustness tests alter pixels while preserving task evidence. LIBERO-Occ removes or hides task evidence in the scene itself, making the problem a partial-observability test rather than a cosmetic perturbation test.

### 8. What are the strengths?
- Occluders are physically placed in 3D scenes, not pasted as image masks.
- The benchmark checks visibility, physical validity, and demonstration replay executability.
- The target-type/severity taxonomy makes failures easier to interpret.
- The ground-truth complementary-view upper bound usefully measures how much value hidden evidence contains.

### 9. What are the weaknesses, limitations, or red flags?
- LIBERO-Occ is simulation-only and inherits LIBERO's limits.
- Generated complementary views are constrained by the model's learned visual prior and may hallucinate plausible but wrong evidence.
- The two-stage training is brittle enough that removing the Stage-2 view loss causes format collapse in the reported ablation.
- The method does not solve active perception; it imagines another view rather than choosing to observe one.

### 10. What challenges or open problems remain?
The main open challenge is calibrated uncertainty. If a generated complementary view is wrong, a policy needs to know that it is guessing. Future VLA systems need a way to distinguish visible evidence, inferred evidence, and unknown state.

### 11. What future work naturally follows?
- Add uncertainty or confidence estimates to imagined views.
- Combine viewpoint imagination with active camera/viewpoint selection.
- Evaluate on real-robot occlusion with sensor noise, lighting variation, and object variability.
- Treat generated views as hypotheses that can be verified through action or future observation.

### 12. Why does this matter for cabbageland?
Because it makes partial observability concrete. A VLA should not get credit for "reasoning" if the benchmark always shows the answer. LIBERO-Occ forces the system to represent missing state, and VIM gives a simple inspectable form for that missing state: an imagined complementary view.

### 13. What ideas are steal-worthy?
- Physically instantiate occlusion and replay-verify task executability.
- Separate manipulated-object, receptacle, and dual occlusion instead of reporting one average.
- Use a generated view as an intermediate missing-evidence object, not just a hidden latent.
- Compare against a ground-truth complementary-view upper bound to measure the value of the missing evidence.

### 14. Final decision
**Keep.** The method is imperfect, but the benchmark and framing are valuable. It is a good reminder that robust VLA evaluation should hide task evidence, not merely corrupt pixels.
