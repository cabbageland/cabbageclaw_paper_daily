# Context-Aware RL for Agentic and Multimodal LLMs

## Basic info

* Title: Context-Aware RL for Agentic and Multimodal LLMs
* Authors: Peiyang Xu, Bangzheng Li, Sijia Liu, Karthik R. Narasimhan, Pramod Viswanath, Prateek Mittal, Xingyu Fu
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.17053
* Date surfaced: 2026-06-16
* Why selected in one sentence: It adds a context-selection auxiliary objective to RL so agentic and multimodal models learn which evidence supports an answer, not only whether the final output gets reward.

## Quick verdict

* Highly relevant

This is a clean training-method paper with a mechanism that transfers across two cabbageland-relevant failure modes: tool/trace context in agents and fine-grained visual evidence in VLMs. I inspected the full arXiv PDF, including the contrastive data construction, loss definition, long-horizon experiments, multimodal experiments, augmentation baselines, mechanism analysis, and limitations. I did not audit the code, data release, synthetic editing process, or verifier prompts, so the exact benchmark gains should be treated as paper claims.

## One-paragraph overview

The paper argues that many agentic and multimodal failures are really context-unawareness failures: the decisive evidence is present, but the model's answer is not grounded in it. ContextRL adds a small auxiliary task to GRPO. Given a query, a candidate answer, and two highly similar contexts, the model must select the context that actually supports that answer. For agentic coding, the contexts are trajectories from the same repository/file/function but different issues; for multimodal reasoning, the contexts are similar or edited images that support different answers. Across 5 long-horizon benchmarks and 12 multimodal benchmarks, the method improves over standard GRPO. The most important result is the baseline failure: simply adding the same contrastive data through SFT or outcome-only RL does not reproduce the gains and can catastrophically collapse agentic policies.

## Model definition

### Inputs
Training inputs include ordinary task instances for GRPO and contrastive context instances of the form `(Q, A, C+, C-)`. `Q` is a query, `A` is a candidate answer, `C+` is the supporting context, and `C-` is a superficially similar confounder that supports a different answer. In the agentic setting, contexts are coding-agent trajectories containing reasoning traces, tool interactions, sandbox observations, and patches. In the multimodal setting, contexts are images.

### Outputs
The policy outputs normal task responses: patches or answers for the main task, and an option letter indicating which context supports a fixed query-answer pair for the auxiliary task. Evaluation outputs include resolve rates, exact answer accuracy, context-selection accuracy, and benchmark scores across coding, long-context, visual, scientific, and scene-understanding tasks.

### Training objective (loss)
The method optimizes a joint loss: standard GRPO on the task data plus a context-awareness loss on contrastive examples. The context-awareness loss uses the logit margin between the option token assigned to `C+` and the option token assigned to `C-`, applies clipping, and optimizes `-log sigmoid(margin)`. In the agentic setting, the GRPO reward is based on test-case success; in the multimodal setting, it is based on exact answer match.

### Architecture / parameterization
The paper does not introduce a new model architecture. It post-trains existing models: Qwen3-8B and Klear-AgentForge-8B for agentic/long-horizon tasks, plus Qwen2.5-VL-7B and Qwen3-VL-8B for multimodal tasks. The key design is objective-level: a bounded auxiliary context-selection loss inside an on-policy GRPO loop, with KL/clipping machinery preserving the base policy distribution.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Models often fail even when the right evidence is already in the context. In agents, that evidence may be one line in a tool trace or source file. In VLMs, it may be a small visual cue. Final-answer reward can miss the problem because a model may sometimes get the answer right for the wrong reason, or fail because it never bound its output to the decisive context.

### 2. What is the method?
The method builds contrastive context pairs and trains the policy to choose which context supports a fixed query-answer pair. This auxiliary context-selection loss is mixed with ordinary GRPO. The contrastive pair is deliberately hard: the two contexts share surface features, so the model has to inspect the evidence rather than rely on easy cues.

### 3. What is the method motivation?
Outcome rewards are sparse and late. They say whether the output was accepted, not whether the model used the right part of the context. The auxiliary objective turns context grounding into a dense, process-level signal while leaving the main task distribution mostly intact.

### 4. What data does it use?
For agentic coding, the paper mines 1K contrastive trajectory pairs from 66K SWE-smith-derived trajectories using repository, commit, file, function/class, issue-relatedness, and verifier filters. These are combined with 7K standard SWE-Gym/SWE-Smith coding tasks for agentic training. For multimodal reasoning, it builds 7K contrastive image pairs: roughly 700 from controlled natural-image edits after a high rejection rate, plus 6,300 from similarity-based retrieval over structured images. These are combined with 38K standard single-image task instances for multimodal training.

### 5. How is it evaluated?
The agentic evaluation uses SWE-Bench Verified, SWE-Bench Lite, LiveCodeBench v6, LongBench v2, and Needle-in-a-Haystack. The multimodal evaluation uses 12 benchmarks spanning mathematical reasoning, general multimodal understanding, fine-grained perception, scientific reasoning, and real-world scene understanding. The paper also measures held-out context-selection accuracy and compares against data-augmentation baselines that use the same contrastive data via SFT or outcome-only RL.

### 6. What are the main results?
ContextRL improves over the GRPO baseline across all 5 long-horizon benchmarks for both base models. On Klear-AgentForge-8B, SWE-Bench Verified rises from 28.0 to 30.2 and SWE-Bench Lite from 21.7 to 24.0; on Qwen3-8B the gains are smaller but consistently positive. On multimodal benchmarks, average performance rises by +2.0 points over RL on Qwen2.5-VL-7B and +1.6 on Qwen3-VL-8B, with improvements on every listed benchmark. Data augmentation does not explain the result: DA-SFT learns context selection but collapses agentic performance as low as 0 on Qwen3-8B SWE-Bench, while DA-RL stays close to the baseline. ContextRL is the only variant that pairs high context-selection accuracy with downstream task gains.

### 7. What is actually novel?
The novelty is not contrastive examples alone. The paper's contribution is making "which context supports this answer?" an auxiliary policy objective that is bounded enough to preserve the task policy. That is more specific than generic RL or generic contrastive SFT.

### 8. What are the strengths?
The method targets a real failure interface: evidence binding. The ablations are unusually helpful because they show that the data and the objective are separable. The same idea works in both agentic trajectories and images, which supports the claim that context grounding is a cross-modal process-level bottleneck rather than a niche benchmark artifact.

### 9. What are the weaknesses, limitations, or red flags?
The gains are real but modest, especially in the long-horizon setting. Most tested base models are from the Qwen family and all experiments stay below 10B parameters, so the result may not transfer unchanged to larger or different model families. The contrastive data construction uses strong frontier-model verification and generated image editing, so hidden artifacts or verifier bias remain possible. The paper also does not prove that improved benchmark scores always come from more faithful grounding in deployed settings.

### 10. What challenges or open problems remain?
The main challenge is scaling the objective without overfitting to contrastive-pair artifacts or damaging long-form agent behavior. Another open problem is whether context-selection objectives can be made online, with real tool traces and changing memory, rather than mined offline from curated pairs.

### 11. What future work naturally follows?
Test the objective on larger and non-Qwen models, web/search agents, long-document research agents, medical VQA, and tool-use settings with adversarial or stale context. Combine it with provenance labels so the model can identify not only which context supports an answer, but which exact span, tool call, or image region is decisive.

### 12. Why does this matter for cabbageland?
Cabbageland agents often fail not because the answer is impossible, but because the decisive observation is buried in the context and the model treats the surrounding text as mush. ContextRL suggests a training shape for that failure: ask the model to choose the evidence that justifies a candidate answer before rewarding the answer itself.

### 13. What ideas are steal-worthy?
Train context support as a separate skill. Keep the query and answer fixed, vary the context, and force the model to identify which one licenses the answer. Use bounded auxiliary losses so the model learns evidence binding without losing long-horizon policy behavior. Evaluate with hard-negative contexts that share repository, file, visual layout, or semantic neighborhood so shortcuts are less useful.

### 14. Final decision
Keep and cite. The method is not a complete solution to agent grounding, but the objective shape is very reusable: final success plus evidence-support selection is better than final success alone.
