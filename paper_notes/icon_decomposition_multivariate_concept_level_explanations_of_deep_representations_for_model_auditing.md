# ICON Decomposition: Multivariate Concept-Level Explanations of Deep Representations for Model Auditing

## Basic info

* Title: ICON Decomposition: Multivariate Concept-Level Explanations of Deep Representations for Model Auditing
* Authors: Roshan Prakash Rane, Marco Simnacher, Manuel Pfeuffer, Marc-Andre Schulz, Nys Tjade Siegel, Maximilian Dreyer, Frederik Pahde, Wojciech Samek, Sonja Greven, Kerstin Ritter
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.26083
* Date surfaced: 2026-08-27
* Why selected in one sentence: It is the sharpest interpretability paper in the batch on disentangling genuine model reliance from correlated concept clutter.

## Quick verdict

* Useful

I inspected the full arXiv HTML text, especially the motivation, the PLS-based ICON construction, the skin-cancer shortcut experiment, and the neuroimaging case studies. This paper earns a preserved note because it attacks a real concept-audit pathology instead of just complaining about probes. The valuable move is to stop asking whether each concept is decodable in isolation and instead ask how much variance it explains once the other concepts and the outcome are already on the table.

## One-paragraph overview

ICON reframes concept-based model auditing as a multivariate variance-decomposition problem. For each layer, it uses partial least squares to find orthogonal latent concept directions jointly linking the layer representation to a concept matrix and the outcome, then decomposes the explained variance back onto the original concepts with Type I sums of squares. The result is a per-layer concept-importance breakdown plus an explicit unexplained share. That lets the method distinguish genuine shortcut use from mere concept correlation, and also warn when the supplied concept set is insufficient to explain what the model is doing.

## Model definition

### Inputs
Hidden activations from a chosen model layer, a matrix of annotated human concepts, and the target outcome variable.

### Outputs
Per-layer concept-importance shares, orthogonal latent ICON factors, and an unexplained variance share capturing what the supplied concepts do not account for.

### Training objective (loss)
There is no trainable model here. ICON is a post-hoc decomposition method built from partial least squares and variance attribution.

### Architecture / parameterization
Iterative PLS to extract orthogonal latent concept-activation pairs, followed by variance decomposition over the original concepts and outcome. The method adaptively stops adding factors when a new pair contributes less than 1% of total squared cross-covariance.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the fact that common concept probes and CAV-like methods often assign importance to concepts that are merely correlated with the true driver, rather than actually used by the model.

### 2. What is the method?
The method builds latent concept factors with PLS on the joint space of layer activations and concepts, then attributes the explained variance back to individual concepts after accounting for the others and the outcome. It also reports how much layer variance remains unexplained by the supplied concepts.

### 3. What is the method motivation?
If concepts are correlated with one another or with the outcome, one-concept-at-a-time probes cannot tell genuine reliance from statistical hitchhiking. A multivariate method can.

### 4. What data does it use?
It uses synthetic simulation data with known ground truth, the ISIC 2019 skin-lesion benchmark with natural and injected shortcut artifacts, and UK Biobank brain-MRI models for binge-drinking classification and brain-age prediction.

### 5. How is it evaluated?
It is evaluated against seven baseline concept-based explainability methods on synthetic data, with controlled shortcut experiments on skin-cancer models, and with qualitative plus out-of-distribution validation on neuroimaging research questions.

### 6. What are the main results?
On synthetic data the paper reports better recovery of ground-truth concept importance than seven alternatives. In the skin-cancer shortcut test, ICON keeps false-positive microscope importance below `0.01` on models that never used the artifact, while baselines drift to `0.05-0.12` as test-set correlation changes. As shortcut corruption increases across ten models, ICON tracks microscope importance from about `0.00` to `0.44`, while the baselines move only `0.02-0.15`. In the neuroimaging case studies, ICON shows that a binge-drinking MRI classifier assigns about `0.39` of final-layer variance to sex and essentially none to the actual binge-drinking outcome, while a brain-age model assigns about `0.63` to the outcome and leaves about `0.36` unexplained.

### 7. What is actually novel?
The real novelty is not concept decomposition by itself. It is the multivariate framing plus the unexplained share, which lets the method say both "this concept matters after controlling for the others" and "your candidate concept set still misses a lot."

### 8. What are the strengths?
It directly targets collinearity, which is one of the biggest reasons concept audits go off the rails. The unexplained-share output is also excellent because it prevents fake completeness. The case studies are high-stakes enough that this matters.

### 9. What are the weaknesses, limitations, or red flags?
The method is still linear and still depends on the user supplying a meaningful concept set. If the real behavior is nonlinear or conceptually mis-specified, the unexplained bucket will grow, but ICON will not discover new concepts for you. The variance attribution step also inherits the usual caveats of post-hoc decomposition choices.

### 10. What challenges or open problems remain?
Handling nonlinear concept relations, discovering missing concepts automatically, and scaling the method to settings where concept annotations are sparse or noisy. Another open problem is turning the unexplained share into a more actionable follow-up search process.

### 11. What future work naturally follows?
Hybrid linear-plus-nonlinear decomposition methods, automated concept-set expansion triggered by large unexplained shares, and broader use in multimodal foundation models where shortcut risk is high and concept entanglement is severe.

### 12. Why does this matter for cabbageland?
Because cabbageland keeps wanting audits that do not confuse correlated labels with actual mechanism. ICON is useful as a reminder that interpretability without multivariate control can become decorative nonsense very quickly.

### 13. What ideas are steal-worthy?
Treat concept auditing as shared-variance allocation rather than isolated decoding. Report an unexplained residual instead of pretending the chosen concept list is complete. Use controlled shortcut injections to test whether an interpretability method actually tracks learned behavior.

### 14. Final decision
Keep as a preserved note. This is a serious interpretability paper with a real target and a more honest output object than most probe-based work.

## 6. Mandatory critical angles

The paper is strongest on auditing honesty, shortcut specificity, and explicit uncertainty about missing concepts. It is limited by linearity and by the fact that concept selection still comes from the human side, not the method.

## 7. Writing style

The right tone is favorable but skeptical. The paper is useful because it fixes a specific blind spot, not because it solves interpretability.

## 8. Repository output format

Saved as a preserved paper note because the multivariate-audit framing is reusable well beyond biomedical examples.
