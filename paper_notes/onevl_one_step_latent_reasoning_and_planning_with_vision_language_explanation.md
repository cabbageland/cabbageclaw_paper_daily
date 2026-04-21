# OneVL: One-Step Latent Reasoning and Planning with Vision-Language Explanation

## Basic info

* Title: OneVL: One-Step Latent Reasoning and Planning with Vision-Language Explanation
* Authors: Jinghui Lu, Jiayi Guan, Zhijian Huang, Jinlong Li, Guang Li, Lingdong Kong, Yingyan Li, Han Wang, Shaoqing Xu, Yuechen Luo, Fang Li, Chenxu Dang, Junli Wang, Tao Xu, Jing Wu, Jianhua Wu, Xiaoshuai Hao, Wen Zhang, Tianyi Jiang, Lingfeng Zhang, Lei Zhou, Yingbo Tang, Jie Wang, Yinfeng Gao, Xizhou Bu, Haochen Tian, Yihang Qiu, Feiyang Jia, Lin Liu, Yigu Ge, Hanbing Li, Yuannan Shen, Jianwei Cui, Hongwei Xie, Bing Wang, Haiyang Sun, Jingwei Zhao, Jiahui Huang, Pei Liu, Zeyu Zhu, Yuncheng Jiang, Zibin Guo, Chuhong Gong, Hanchao Leng, Kun Ma, Naiyang Wang, Guang Chen, Kuiyuan Yang, Hangjun Ye, and Long Chen
* Year: 2026
* Venue / source: arXiv technical report
* Link: https://arxiv.org/abs/2604.18486
* Date surfaced: 2026-04-21
* Why selected in one sentence: It makes latent reasoning less hand-wavy by forcing the compressed bottleneck to reconstruct both language explanations and future visual dynamics.

## Quick verdict

**Useful**

There is real mechanism here, even if the paper is long and a little eager to declare victory. I inspected the abstract, introduction, architecture description, and training framing from the arXiv HTML, which is enough to trust the main design and claims, but not enough to independently validate every benchmark detail in this 49-page report. The interesting part is the representational contract, not the leaderboard chest-thumping.

## One-paragraph overview

OneVL is a driving VLA that tries to get the accuracy benefits of chain-of-thought without paying autoregressive reasoning latency. Instead of generating a full text reasoning trace at inference time, it compresses reasoning into latent tokens that are produced in one prefill pass. The key move is that these latents are not supervised only through text. One decoder reconstructs language CoT, while another visual decoder predicts future-frame tokens, effectively making the latent bottleneck answer to both semantic explanation and causal scene dynamics. The decoders are thrown away at inference, leaving a faster planning model whose hidden state has been shaped by both language and world-model-style supervision.

## Model definition

### Inputs
The model takes visual driving observations, a text prompt or instruction, and the context needed for trajectory prediction or planning. During training, it additionally uses explicit CoT text and future visual targets for the auxiliary decoders.

### Outputs
At training time the system outputs trajectory or planning predictions, reconstructed language reasoning, and predicted future visual tokens. At inference time the auxiliary decoders are removed and the main model outputs the planned answer or trajectory using prefilled latent tokens.

### Training objective (loss)
The paper uses a combined objective across planning, language-decoder reconstruction, and visual future-token reconstruction, with a three-stage training pipeline to stabilize optimization. The exact algebraic form and weighting were not fully visible in the inspected text.

### Architecture / parameterization
A vision-language-action model with latent reasoning tokens, a language auxiliary decoder, a visual auxiliary decoder that acts as a world-model-style future predictor, and a prefill inference procedure that inserts all latent tokens in one pass.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Explicit CoT helps driving VLAs, but it is too slow for real-time use. Prior latent-CoT methods are faster, but they underperform because compressing language alone does not force the bottleneck to retain the causal structure of the driving scene.

### 2. What is the method?
OneVL learns compact latent tokens supervised by two auxiliary decoders. One reconstructs human-readable CoT text, and the other predicts future visual tokens. Training happens in stages, then inference discards the decoders and prefills the latent tokens in one shot so reasoning no longer has to be generated step by step.

### 3. What is the method motivation?
The paper’s core argument is that language is too abstract a compression target for embodied planning. If you want hidden-state reasoning to preserve what actually matters, the bottleneck should also be forced to encode future physical scene evolution.

### 4. What data does it use?
The inspected text says the paper evaluates on four autonomous-driving benchmarks, including NAVSIM and ROADWork, with explicit CoT supervision and future visual targets. I did not inspect the full dataset section closely enough to summarize every source without risking bluffing.

### 5. How is it evaluated?
It is evaluated on planning or trajectory-prediction accuracy, reasoning quality, and inference latency, with comparisons against explicit CoT, answer-only baselines, and prior latent-CoT methods.

### 6. What are the main results?
The headline claim is that OneVL is the first latent-CoT method to surpass explicit CoT while retaining answer-only latency. The paper reports about 1.5 times speedup over explicit CoT on NAVSIM, 2.3 times on ROADWork, and a practical deployment variant running at about 0.24 seconds per step. I did not verify the full benchmark tables.

### 7. What is actually novel?
The main novelty is the dual supervision of the latent bottleneck. The visual auxiliary decoder matters more than the language decoder alone because it turns the latent space into something answerable to future scene dynamics rather than just text compression. The prefill trick is also practically important because it removes sequential latent generation overhead.

### 8. What are the strengths?
- Good diagnosis of why prior latent-CoT methods fail in embodied settings.
- Stronger supervision contract for the latent bottleneck than language-only approaches.
- Inference-time design is clean: auxiliary machinery disappears after training.
- The paper explicitly cares about latency rather than pretending big reasoning traces are free.
- The visual decoder is a useful bridge between reasoning and world modeling.

### 9. What are the weaknesses, limitations, or red flags?
- The paper is extremely benchmark- and engineering-heavy, so the conceptual contribution is wrapped in a lot of system mass.
- It is still very driving-specific, and transfer to robotics or broader embodied control is not established.
- “Surpasses explicit CoT” is a strong claim that needs external replication.
- The visual decoder predicts future tokens, but that does not automatically mean the latent space becomes deeply interpretable or causally faithful.

### 10. What challenges or open problems remain?
It remains unclear how well this idea works when future visual prediction is less aligned with the actual control bottleneck, for example in manipulation with occlusion, tactile dependence, or hidden state. There is also a broader open question around whether latent reasoning can stay inspectable once it stops decoding rich explicit traces at inference.

### 11. What future work naturally follows?
- Test the dual-decoder latent recipe in robotics VLAs, not just driving.
- Replace future-frame prediction with more structured future-state prediction where geometry or object state matters more than pixels.
- Measure whether the latent bottleneck actually improves out-of-distribution robustness, not just average benchmark score.
- Probe whether the visual and language decoders can be made more disentangled and legible.

### 12. Why does this matter for cabbageland?
Because it is a concrete example of a good instinct: if you want compact reasoning to remain useful, do not supervise it only through language. Force the bottleneck to encode a world-facing predictive contract as well. That general idea should transfer beyond driving.

### 13. What ideas are steal-worthy?
- Dual supervision for latent reasoning, one semantic and one world-predictive.
- Prefill all latent tokens in one pass instead of generating them autoregressively.
- Treat future-state prediction as a regularizer on hidden reasoning quality.
- Use training-only auxiliary decoders to shape internal representations without adding deployment cost.

### 14. Final decision
**Keep as an adjacent architecture note.** I would not treat it as settled proof that latent CoT is solved, but the bottleneck-supervision idea is genuinely worth carrying forward.