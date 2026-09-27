# Training Object Permanence in World Models

## Basic info

* Title: Training Object Permanence in World Models
* Authors: Haotian Zhang, Fengyuan Yu, Dezhi Luo, Haoran Sun, Zehong Zhao, Qingying Gao, Yihan Li, Siyuan An, Huayi Qin, Yilan Zhang, Zhengze Jiang, Pinyuan Feng, Renrui Zhang, Ziyu Guo, Letian Wang, Mengyue Yang, Kangfu Mei, Maijunxian Wang, Ran Ji, Vikash Kumar, Freda Shi, Chandra Sripada, Vincent C. Muller, Philip Torr, Alan Yuille, Nikolaus Kriegeskorte, Felix Juefei-Xu, Lvmin Zhang, Jieneng Chen, Yilun Du, and Hokin Deng
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2609.28654
* Date surfaced: 2026-09-27
* Why selected in one sentence: It turns object permanence and solidity into a large controlled train/eval contract for video world models, with human judgment rather than VLM-judge scoring.

## Quick verdict

**Highly relevant**

This is a strong benchmark/data paper because it targets a real missing capability in video world models and builds controlled generators around it. The model result is promising but should not be overread: a benchmark-specific fine-tune winning on benchmark-specific synthetic tasks is not the same as broad physical intelligence.

## One-paragraph overview

The paper introduces WROP, a Blender-generated benchmark and training corpus for object permanence and object solidity in video generation models. It contains 150 hand-designed task generators across six cognitive-science-inspired families, a 1.5M-sample training corpus, and a fixed 300-question evaluation exam. Models receive the first half of a clip and must generate the physical continuation. The authors fine-tune a 16B Cosmos3-Nano-derived continuation model, PWM-WROP, on this corpus and compare it with 13 other video-to-video systems using blind human pairwise judgments fit to Elo ratings. PWM-WROP becomes the top true-continuation model and ranks third overall, behind two reference-to-video systems.

## Model definition

### Inputs
For WROP tasks, the input is the first part of a generated video clip plus a natural-language prompt. PWM-WROP conditions on the input half of the sample and text prompt.

### Outputs
The model outputs a predicted continuation video. Evaluation compares this continuation against hand-authored physically correct target animations and against other model outputs.

### Training objective (loss)
PWM-WROP is fine-tuned on the WROP video-to-video contract: conditioning frames plus prompt in, target continuation out. The accessible main text says the architecture and tokenizer remain identical to Cosmos3-Nano and that only the training signal changes, but it does not spell out every low-level loss term.

### Architecture / parameterization
PWM-WROP is a 16B video world model fine-tuned from Cosmos3-Nano using the authors' native-PyTorch PWM training stack on AWS Trainium2. The benchmark itself is generated with Blender task generators.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Modern video models can produce plausible footage while violating primitive physical constraints: hidden objects disappear, identities drift, or objects pass through barriers. The paper asks whether object permanence and solidity can be evaluated and trained directly.

### 2. What is the method?
It builds WROP: 150 self-contained Blender generators organized into object-permanence and object-solidity families. Each generator randomizes nuisance factors while preserving the task's causal structure. The authors release training data, exam items, model outputs, scores, weights, and a training stack.

### 3. What is the method motivation?
Generic video metrics and VLM-judge scores are weak tools for testing core physical reasoning. A model needs to keep object identity and causal constraints across occlusion, support removal, barriers, and collisions.

### 4. What data does it use?
The training corpus has 1.5M samples, with 10,000 samples from each of 150 generators. The evaluation exam has 300 questions, two per generator. Every sample includes input video, target video, prompt, per-frame trajectory, and metadata.

### 5. How is it evaluated?
The primary metric is human pairwise blind comparison. Twenty raters judge model continuations for prompt consistency, natural motion, physical plausibility, and object permanence/solidity. The authors fit Bradley-Terry strengths on an Elo scale. Automatic metrics such as LPIPS, SSIM, PSNR, CLIP, and FID are reported only as secondary evidence.

### 6. What are the main results?
Across 14 evaluated systems, PWM-WROP ranks third overall at 1679.5 Elo with a 95% interval of [1603.5, 1781.5], and first among true-continuation models. The top two systems are reference-to-video models, Wan 3.0 Prime and MiniMax H3, both around 1724 Elo, whose interface can regenerate the scene rather than strictly continue the input. PWM-WROP also reports strong automatic target-fit metrics at the common 320x192 comparison resolution, including LPIPS 0.081 and PSNR 26.45.

### 7. What is actually novel?
The novelty is the controlled cognitive benchmark plus trainable corpus. The paper is not just asking whether a video model looks realistic; it operationalizes six families of object permanence and solidity with known physical outcomes.

### 8. What are the strengths?
The benchmark design is much cleaner than broad prompt-based video evaluation. The human evaluation is better matched to the claim than VLM scoring. The release includes data, exam, model answers, scores, weights, and a training stack, which makes the result more useful than a closed leaderboard.

### 9. What are the weaknesses, limitations, or red flags?
The task distribution is synthetic and generator-defined, so a fine-tuned model may learn WROP regularities without acquiring broad physical understanding. Interface classes are not directly comparable: reference-to-video systems have more freedom than true-continuation systems. The human study has only about 50-52 judgments per model in the overall fit.

### 10. What challenges or open problems remain?
The next challenge is transfer: do gains on WROP improve real videos, robot prediction, occlusion-heavy manipulation, or long-horizon physical reasoning? The benchmark also needs stronger probes for compositional generalization outside the generator families.

### 11. What future work naturally follows?
Use WROP-style generators as diagnostic curricula for other video world models, test transfer to real occlusion/control tasks, and separate continuation ability from reference-to-video regeneration in future leaderboards.

### 12. Why does this matter for cabbageland?
It is a concrete example of turning a vague world-model claim into an explicit capability contract. If a model cannot keep hidden objects alive or preserve solidity, higher-level planning over that model is built on sand.

### 13. What ideas are steal-worthy?
Build synthetic curricula around cognitively grounded invariants. Store trajectories and scene metadata alongside video. Prefer human or rule-grounded judgments when the thing being tested is exactly what VLM judges fail at.

### 14. Final decision

**Worth keeping.** Use it as a reference point for benchmark design and for the claim that physical reasoning needs controlled task families, not just prettier video samples.
