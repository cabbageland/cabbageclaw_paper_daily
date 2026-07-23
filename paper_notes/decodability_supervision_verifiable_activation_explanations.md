# Train the Model, Not the Reader: Decodability Supervision for Verifiable Activation Explanations

## Basic info

* Title: Train the Model, Not the Reader: Decodability Supervision for Verifiable Activation Explanations
* Authors: Hiskias Dingeto
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.20379
* Date surfaced: 2026-07-23
* Why selected in one sentence: It turns a popular activation-explanation proxy into a concrete audit target and then repairs the target model rather than polishing the explainer.

## Quick verdict

**Must read**

This is a real critique-and-repair paper rather than a vibes complaint about interpretability metrics. The ugly result is exactly the useful result: reconstruction-scored activation explanations can say false specifics while still scoring well, and the paper proves that with claim-level audits before proposing a narrower repair. I inspected the arXiv HTML sections covering the abstract, introduction, audit protocol, released-system audit, synthetic-ground-truth audit, RECAP method, sandbox results, Pythia-160M scaling section, probe-based monitoring, and discussion.

## One-paragraph overview

The paper studies natural-language autoencoders that explain a hidden activation by generating text and then reconstructing the activation from that text. It argues that the reconstruction score is structurally blind to false additions: if a lie does not change the reconstructed activation, the score never punishes it. The paper validates that failure in a released Qwen-2.5-7B verbalizer and in synthetic settings with exact ground truth, then proposes RECAP, which co-trains auxiliary linear heads on external targets so designated internal content stays probe-decodable in the target model itself. The resulting promise is narrower but much better: not that prose explanations become intrinsically truthful, but that some internal content becomes independently checkable against fresh probes and therefore harder to fake with polished verbalizer text.

## Model definition

### Inputs
The system reads hidden activations at chosen tap positions, plus external target labels for the content that RECAP is supposed to keep decodable.

### Outputs
The verbalizer outputs explanation text, the reconstructor predicts the original activation from that text, and the RECAP heads predict designated target content directly from the model state.

### Training objective (loss)
The standard natural-language autoencoder trains the verbalizer and reconstructor for activation reconstruction. RECAP adds supervised auxiliary prediction heads during target-model training so designated content remains linearly decodable; the accessible text does not spell out the exact combined loss weights in the sections I inspected.

### Architecture / parameterization
The paper audits a released Qwen-2.5-7B layer-20 verbalizer/reconstructor pair, uses exact-ground-truth synthetic domains for diagnosis, and scales the RECAP intervention to continued pretraining on Pythia-160M with auxiliary linear heads.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to determine whether activation explanations scored by reconstruction are actually faithful at the level of individual claims, and how to make important internal content verifiable when they are not.

### 2. What is the method?
The method combines claim-level minimal-pair audits, grounded-vs-true and evaluator-swap diagnostics, and RECAP, a target-model training intervention that keeps designated content decodable via auxiliary linear heads.

### 3. What is the method motivation?
If reconstruction only checks whether the explanation preserves enough gist to rebuild the activation, then it can certify smooth prose that adds false specifics. The model itself needs to preserve readable internal content, not just the reader.

### 4. What data does it use?
It studies a released Qwen-2.5-7B verbalizer on in-distribution web text with `1,517` audited claims, two synthetic domains with exact ground truth, and continued pretraining experiments on Pythia-160M.

### 5. How is it evaluated?
It is evaluated with counterfactual claim-flip audits, grounded-vs-true crosses, evaluator swaps, sandbox exact-ground-truth checks, fresh-probe readouts, and adversarial edits that try to maximize reconstruction score while lying.

### 6. What are the main results?
The released Qwen system reconstructs at about `0.84` normalized score while only about `2%` of specific claims are reconstruction-dependent. In the synthetic setup, standard-reader training produces private codes in `5/5` runs. RECAP restores claim-level faithfulness in the sandbox with about `+0.001` nat tax, transfers to Pythia-160M with stated-word truth around `0.44-0.46` versus near-zero control, and lets an independent probe score true claims above false ones at `AUC 0.96` versus `0.82` without RECAP. Under adversarial explanation edits, the RECAP probe still catches lies at `AUC 0.95` while the control probe collapses to chance.

### 7. What is actually novel?
The novelty is the combination of a claim-level audit standard and a repair that trains the target model for decodability instead of trying to make the explanation reader more sincere.

### 8. What are the strengths?
It does not hide behind a single proxy, it uses exact-ground-truth synthetic tests where needed, it distinguishes decodability from verbalizability, and it is unusually honest about what the repair does and does not guarantee.

### 9. What are the weaknesses, limitations, or red flags?
RECAP only guarantees designated content is decodable, not that the full explanation is mechanistically faithful. The scale experiment is still on Pythia-160M, so the deployment story for larger frontier models remains open.

### 10. What challenges or open problems remain?
The next challenge is scaling designated-content decodability to richer, less manually specified concepts without collapsing into weak proxies again.

### 11. What future work naturally follows?
Broaden the target content, integrate probe checks into runtime monitoring, and test whether decodability supervision can make larger frontier models safer to audit under distribution shift or adversarial prompting.

### 12. Why does this matter for cabbageland?
Cabbageland cares about legible mechanisms and falsifiable oversight. This paper strips away a seductive but weak faithfulness proxy and replaces it with something narrower, harsher, and more operational.

### 13. What ideas are steal-worthy?
Use claim-level minimal-pair flips instead of summary-level vibes. Separate grounded truth from readable prose. Train designated content to stay linearly decodable, then verify explanations with fresh probes rather than trusting reconstruction scores.

### 14. Final decision
**Keep it.** The audit is important, the repair is honest, and the paper narrows activation-explanation claims in exactly the direction future work needs.
