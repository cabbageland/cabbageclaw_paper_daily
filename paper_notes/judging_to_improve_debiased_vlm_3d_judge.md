# Judging to Improve: A De-biased VLM-as-3D-Judge Protocol for Single-Image 3D Generation

## Basic info

* Title: Judging to Improve: A De-biased VLM-as-3D-Judge Protocol for Single-Image 3D Generation
* Authors: Ali Asaria, Tony Salomone, Deep Gandhi
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.20364
* Date surfaced: 2026-06-20
* Why selected in one sentence: It turns a VLM-as-judge setup into a tested evaluation protocol and finds that cheap public-data TRELLIS specialization reaches parity, not a real win.

## Quick verdict

* Useful

This is not a big architecture win, and that is the point. I inspected the full arXiv PDF, including the judge protocol, preference-signal construction, specialization study, mechanism analysis, and limitations. The paper is worth keeping because it documents the traps in using VLM judges for 3D generation and gives a negative result with localized failure modes.

## One-paragraph overview

The paper asks whether a de-biased VLM judge can be used not only to rank single-image 3D generations, but to improve a strong open generator, TRELLIS, on furniture with lightweight public-data adaptation. The answer is mostly no: six adaptation methods across clean and degraded input regimes fail to beat the base, with the best conditioner-repair adapter reaching parity under severe degradation. The useful artifact is the evaluation protocol: use separate judge families for training and evaluation, query both presentation orders and keep only swap-consistent verdicts, render meshes with normal-map montages so geometry defects are visible, and run clear-gap plus base-vs-base sanity checks.

## Model definition

### Inputs
Inputs include single furniture images from 3D-FUTURE, generated TRELLIS meshes, candidate mesh renderings, quality-contrastive pairs from high-budget versus degraded/low-budget generation, and VLM judge prompts. The hard regime uses synthetic crop, occlusion, downscale, and blur degradations.

### Outputs
The judge outputs pairwise preferences between two candidate meshes. Adaptation methods output specialized TRELLIS variants or a repaired conditioning feature path. Evaluation outputs held-out judge win rates against the base, geometry-validity deltas, flip rates, clear-gap controls, and base-vs-base sanity checks.

### Training objective (loss)
The tested adaptation objectives include SFT-on-best, DPO with beta 0.1 and 0.5, ORPO, SFT-on-clean for degraded inputs, and supervised conditioner repair from degraded DINOv2 conditioning features to clean features. The judge itself is not fine-tuned in this paper; Qwen2.5-VL-7B labels training preferences and InternVL3-8B evaluates held-out results.

### Architecture / parameterization
The generator is TRELLIS, a structured-latent rectified-flow transformer conditioned on DINOv2 image features. Flow-DIT adaptations use custom LoRA on sparse-linear blocks. Conditioner repair freezes the flow DIT and trains a residual adapter over DINOv2 conditioning features. The evaluation system is a cross-model VLM-as-3D-judge protocol with swap-consistency filtering.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Single-image 3D generation needs trustworthy evaluation and preference signals. If a VLM judge is used both to optimize and to declare victory, the generator can learn judge quirks. Worse, the judge can be fooled by presentation order, overloaded image panels, render choices that hide geometry defects, or clean-looking but wrong outputs.

### 2. What is the method?
The method is protocol-first. It uses one VLM family as the training judge and a different VLM family as the evaluation judge. Each pair is queried in both orders, and only swap-consistent verdicts are kept. Meshes are shown with normal-map montages rather than deceptive Gaussian-splat renders. Clear-gap controls verify that the judge detects real quality gaps, while base-vs-base controls check for no systematic preference.

### 3. What is the method motivation?
The motivation is that ranking is easier than optimization. A judge that looks stable for broad cross-generator comparisons may fail when pushed into a training loop where candidate differences are subtle and presentation artifacts dominate. The protocol has to survive the optimization setting, not just make plausible rankings.

### 4. What data does it use?
The specialization study uses 3D-FUTURE furniture objects, public TRELLIS, public VLM judges, and synthetic degraded inputs. The held-out evaluation uses eight disjoint furniture objects, which is small and explicitly treated as directional.

### 5. How is it evaluated?
The paper evaluates clear-gap sanity controls, base-vs-base controls, judge flip rates, high-budget versus degraded preference construction, held-out specialized-vs-base win rates, geometry-validity deltas, and mechanism probes such as flow-matching MSE and conditioner feature reconstruction MSE.

### 6. What are the main results?
The judge protocol passes clear-gap controls with 0.83 to 1.0 win rate for better meshes and roughly 0.5 base-vs-base behavior where estimable. Independent samples from the strong base carry almost no learnable preference: the training judge flips on 0.94 of same-base pairs. Quality-contrastive high-budget versus degraded pairs recover a training signal with 0.89 training-judge win rate. Across six adaptation methods, no method reaches the 0.65 held-out win target. The best result is conditioner repair under severe degradation, reaching 0.50 parity with a small positive geometry delta.

### 7. What is actually novel?
The novelty is the optimization-grade judge protocol plus the negative specialization result. The paper does not invent DPO, ORPO, LoRA, or TRELLIS. It identifies which parts of the evaluation loop fail and localizes why cheap adaptation does not beat a strong base.

### 8. What are the strengths?
The paper is unusually honest about null results. It names concrete judge failure modes: image overload can collapse the judge into position answering, splat renders can hide geometry defects, and reference-free judging can reward clean but wrong meshes. It also separates training and evaluation judges, which is the minimum boundary for model-in-the-loop preference claims.

### 9. What are the weaknesses, limitations, or red flags?
The final held-out sample is only eight objects, so the win rates are directional. The paper uses VLM judges rather than human raters. It tests one base model, one asset class, public data, synthetic degradations, and lightweight parameter-efficient adaptation only. Full fine-tuning, larger adapters, better data, or real-world photographs could change the result.

### 10. What challenges or open problems remain?
Open problems include human validation of the judge protocol, larger held-out sets, other 3D generators, real input degradations, stronger preference-signal construction, and adaptation methods that can move the generator past parity without learning judge artifacts.

### 11. What future work naturally follows?
The next step is to run the protocol on larger human-calibrated benchmarks and test whether conditioner-side repair remains the best intervention point for other generators. Another useful follow-up is an automated judge audit suite that reports position flips, clear-gap calibration, render sensitivity, and reference-dependence before any VLM judge is used for optimization.

### 12. Why does this matter for cabbageland?
Cabbageland will keep encountering VLM-as-judge claims in 3D, video, and agent evaluation. This paper is a reminder that judge reliability is an engineered property, not a vibes certificate. If the preference signal is not real, optimizing harder just learns measurement junk.

### 13. What ideas are steal-worthy?
Use separate model families for training and evaluation judges. Query both candidate orders and discard inconsistent pairs. Add clear-gap and no-gap sanity controls. Render assets in a way that exposes the defect being judged. Treat high flip rates as evidence that the preference signal may not exist, not merely as judge noise.

### 14. Final decision
Keep as an evaluation-protocol reference. The model result is negative and small-sample, but the protocol lessons are directly reusable for 3D generation and broader model-as-judge evaluation.
