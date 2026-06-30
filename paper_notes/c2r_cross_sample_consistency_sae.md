# C^2R: Cross-sample Consistency Regularization Mitigates Feature Splitting and Absorption in Sparse Autoencoders

## Basic info

* Title: C^2R: Cross-sample Consistency Regularization Mitigates Feature Splitting and Absorption in Sparse Autoencoders
* Authors: Haoran Jin, Xiting Wang, Shijie Ren, Hong Xie, and Defu Lian
* Year: 2026
* Venue / source: ICML 2026 / arXiv
* Link: https://arxiv.org/abs/2606.30609
* Date surfaced: 2026-06-30
* Why selected in one sentence: It proposes a concrete training-time mechanism for making SAE latents more consistent across samples, rather than merely naming interpretability pathologies after the fact.

## Quick verdict

**Must read**

This is the strongest interpretability paper in today's scan. The important move is to treat feature splitting and feature absorption as failures of cross-sample latent assignment, then intervene at that level with a batch-level consistency regularizer. I inspected the full arXiv PDF's main theory, method, experiment, ablation, downstream-task, and limitation sections; confidence is high on the main mechanism and empirical claim, with normal caution around the conditional theory and AutoInterp-heavy evaluation.

## One-paragraph overview

Sparse autoencoders are supposed to turn dense LLM activations into sparse, interpretable latents, but large dictionaries can split one coherent concept across multiple latents or let specific exception latents absorb parts of a general feature. C^2R argues that the root cause is per-sample sparsity: the SAE can choose different redundant latents for the same underlying feature across samples because the objective does not enforce assignment consistency. The proposed regularizer penalizes co-activation of directionally similar latents across a batch, using decoder geometry and activation statistics to push the model toward a unified latent for the same semantic feature. Experiments on Gemma-2-2B, Qwen3-8B, and Llama-3-8B suggest reduced splitting and absorption while preserving reconstruction fidelity and downstream causal-intervention utility.

## Model definition

### Inputs
The model consumes internal LLM activation vectors, primarily residual stream activations from selected layers. Main experiments train SAEs on Gemma-2-2B layer 12 using 500M OpenWebText tokens, with additional evaluations on deeper layers, The Pile, 1B-token training, Qwen3-8B, and Llama-3-8B.

### Outputs
The SAE outputs sparse latent activations and reconstructs the original model activation. The analysis focuses on whether learned latents correspond to stable semantic features rather than split, absorbed, or redundant fragments.

### Training objective (loss)
The base SAE objective is reconstruction error plus a sparsity constraint such as TopK / Batch TopK. C^2R adds a cross-sample consistency regularization term weighted by lambda_C2R. The term penalizes redundant co-activation among decoder-direction-similar latents, with nearest-neighbor restriction and a ReLU cosine gate to avoid overly broad merging.

### Architecture / parameterization
The regularizer is designed to be compatible with multiple SAE backbones, including Batch TopK, TopK, OrtSAE, and AbsTopK. The architecture remains an SAE with encoder, sparse latent code, and linear decoder; the novelty is the batch-level structural constraint.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It targets two SAE reliability failures. Feature splitting fragments a coherent concept into multiple narrower latents. Feature absorption creates exception latents that steal activation from a general feature, turning the general feature into something like "starts with S except short/small." Both make latent-level interpretation and causal intervention less trustworthy.

### 2. What is the method?
C^2R adds a cross-sample consistency penalty to SAE training. Instead of only forcing each individual sample to be sparse, it looks across the batch and discourages similar decoder-direction latents from redundantly co-activating for the same semantic feature. The implementation uses efficient block-wise computation and applies the regularizer periodically to reduce overhead.

### 3. What is the method motivation?
Per-sample sparsity can punish hierarchical feature activation and does not care whether the same semantic feature gets assigned to one latent or scattered across several. If the pathology is inconsistent assignment across samples, then the fix should be cross-sample rather than another local sparsity trick.

### 4. What data does it use?
Main experiments use a 500M-token OpenWebText subset for Gemma-2-2B residual activations. Robustness experiments include 1B OpenWebText tokens, The Pile, layer 20, Qwen3-8B, Llama-3-8B, and multiple random seeds. Interpretability evaluation samples latents and uses activation examples for AutoInterp-style explanations and judgments.

### 5. How is it evaluated?
The paper evaluates reconstruction fidelity, KL divergence / loss recovery, AutoInterp, RAVEL disentanglement, feature splitting, feature absorption, feature composition, dead feature rates, ablations, scale/layer/data robustness, and SAEBench causal intervention tasks such as spurious correlation removal and targeted probe perturbation.

### 6. What are the main results?
C^2R reduces feature splitting and absorption compared with high-fidelity baselines while preserving reconstruction fidelity. Matryoshka can reduce some structural metrics but at a fidelity cost; C^2R aims for the better fidelity-structure tradeoff. The paper reports robustness across random seeds, layers, datasets, and 8B-scale models, and says C^2R improves downstream causal-intervention tasks compared with TopK, Batch TopK, and Ort.

### 7. What is actually novel?
The novelty is the cross-sample consistency framing. The paper treats splitting and absorption as two faces of the same redundancy problem and uses decoder-direction geometry plus batch activation patterns to discourage inconsistent latent assignment.

### 8. What are the strengths?
The mechanism is local enough to add to existing SAE backbones, but addresses a real structural failure. The paper includes theory, main metrics, ablations, scalability checks, backbone compatibility checks, and downstream intervention tasks. The limitation section is also usefully honest about the conditional guarantee and possible over-merge behavior.

### 9. What are the weaknesses, limitations, or red flags?
The theoretical guarantee is conditional and empirically verified for a subset of absorption pairs, not unconditional. AutoInterp uses proprietary GPT-5-mini as judge, with GPT-5/human consistency checks but still a reproducibility burden. The method is tested up to 8B-scale dense models, not frontier-size models or MoE systems. It may also suppress legitimate polysemanticity when separate features have moderately aligned decoder directions.

### 10. What challenges or open problems remain?
The main open problem is distinguishing harmful redundancy from legitimate compositional or hierarchical structure. Larger-scale SAE training could also reveal different failure modes. Another open question is whether better structural metrics reliably predict better causal interpretability in downstream analyses that matter.

### 11. What future work naturally follows?
Test C^2R on larger and MoE models, integrate it with newer SAE variants, evaluate on more causal circuit-discovery tasks, and develop metrics that detect over-merging of genuinely distinct but aligned features. A strong follow-up would compare C^2R-trained latents inside real interpretability workflows, not only standalone benchmarks.

### 12. Why does this matter for cabbageland?
Cabbageland cares about explicit representations that actually do work. C^2R is a reminder that naming latents is cheap; making them stable under assignment pressure is the real work.

### 13. What ideas are steal-worthy?
* Diagnose representation failures as assignment failures, not just feature-quality failures.
* Penalize inconsistent redundant activation across samples.
* Preserve reconstruction fidelity while improving structural legibility.
* Evaluate interpretability tools on causal intervention, not just explanation prettiness.
* Treat "one concept, one reliable handle" as an engineering goal.

### 14. Final decision
**Keep as a must-read interpretability mechanism.** It is not the last word on SAE reliability, but it is exactly the kind of structural intervention worth tracking.
