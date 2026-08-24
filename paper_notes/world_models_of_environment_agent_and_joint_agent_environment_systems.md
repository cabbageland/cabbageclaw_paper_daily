# World models of environment, agent and joint agent-environment systems

## Basic info

* Title: World models of environment, agent and joint agent-environment systems
* Authors: Manuel Baltieri, Filippo Torresan, Yivan Zhang, Alexander Boyd, Fernando E. Rosas
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.20401
* Date surfaced: 2026-08-24
* Why selected in one sentence: It is the cleanest theoretical paper in the batch on separating world models by the channel they model and on showing how realised closed-loop support can collapse an infinite environment model into a finite joint-induced one.

## Quick verdict

* Must read

I inspected the full PDF text, especially the introduction, the canonical model definitions, the support-restricted construction, and theorems 16 through 18 with the finite-controller example. This paper earns a preserved note because it fixes a category error that a lot of world-model talk quietly inherits. The useful distinction is not only what variables are predicted, but which channel is being modelled: environment, agent, or realised joint process. Once that is made explicit, the support-restricted result becomes both natural and powerful.

## One-paragraph overview

The paper argues that "world model" is too vague unless you first say what predictive channel the model is about. It defines canonical predictive models for three objects over the same agent-environment interface: the environment channel that predicts observations from actions, the agent channel that predicts actions from observations, and the realised joint process that predicts future action-observation traces from no external input. Using computational mechanics, it builds canonical epsilon-transducer or epsilon-machine models for each channel, then defines support-restricted environment and agent models induced by the realised closed-loop interaction. The central structural result is that the non-sink support-restricted environment states factor through the joint causal states and their transitions are induced directly from the joint model. In the worked example, the unrestricted environment model is infinite, while the realised joint model has 5 causal states and the support-restricted environment model has 6 states including the sink.

## Model definition

### Inputs
Past action-observation histories. Depending on the channel, future action continuations, future observation continuations, or no external continuation at all are queried.

### Outputs
Canonical predictive states and transition dynamics for one of three channels: environment, agent, or realised joint interaction.

### Training objective (loss)
There is no trainable model here. The paper is a theoretical framework that defines canonical predictive equivalence classes and proves structural relations among them.

### Architecture / parameterization
Computational-mechanics construction using epsilon-transducers for the environment and agent channels and an epsilon-machine for the realised joint process, plus support-restricted variants induced by closed-loop coupling.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the fact that world models are usually discussed only in terms of predicted variables or latent states, which hides a more basic distinction: what predictive channel the model is actually meant to represent.

### 2. What is the method?
The method is to define canonical predictive models for three channels over the same agent-environment interface, then define support-restricted environment and agent models whose predictive equivalence ranges only over continuations supported by the realised closed-loop interaction.

### 3. What is the method motivation?
Predictive sufficiency depends on the predictive question. A state sufficient for predicting future observations under future actions need not be sufficient for predicting the agent's future actions, and neither need match the minimal predictive state of the realised joint interaction.

### 4. What data does it use?
This is primarily a theoretical paper, not a learned-data paper. Its main concrete example is a hidden-state POMDP-style environment coupled to a deterministic finite-state controller.

### 5. How is it evaluated?
By formal definitions, theorem proofs, and a worked coupling example that compares unrestricted environment prediction with support-restricted prediction under the realised controller.

### 6. What are the main results?
The key result is that the non-sink canonical support-restricted environment states factor through the joint causal states, and the joint model determines the support-restricted environment model with only a totalisation sink added. In the running example, the unrestricted environment model is infinite because arbitrary hold continuations accumulate unbounded evidence about a hidden state, while the realised joint process has 5 causal states and the support-restricted environment model has 6 states including the sink.

### 7. What is actually novel?
The real novelty is the channel-first ontology plus the support-restriction theorem. The paper does not merely rename predictive state representations. It extends the same canonical predictive logic to environment, agent, and joint channels, then proves that the realised joint model canonically determines the support-restricted environment model.

### 8. What are the strengths?
The paper is conceptually sharp. It distinguishes counterfactual predictive scope from realised closed-loop scope, clarifies what different world models are models of, and gives a clean structural compression result rather than only philosophical framing.

### 9. What are the weaknesses, limitations, or red flags?
It is a theory paper, so it does not yet tell you how to estimate these objects robustly from finite data or how learned deep latent states approximate them in practice. The value is mostly conceptual and structural, not algorithmic.

### 10. What challenges or open problems remain?
The obvious next challenge is approximate estimation: learning channel-specific or support-restricted predictive states from finite traces, noisy observations, and large continuous action-observation spaces.

### 11. What future work naturally follows?
Use these distinctions to probe learned agent latents, build diagnostics for whether a learned state is environment-, agent-, or joint-predictive, and study when support-restricted models are the right abstraction target for deployed systems.

### 12. Why does this matter for cabbageland?
Because cabbageland cares about explicit state, world models, memory, and closed-loop interaction. This paper says a lot of "world model" talk is under-specified until you name the channel, and it gives a principled reason why the realised interaction support can be the right compression target instead of the full counterfactual environment.

### 13. What ideas are steal-worthy?
Separate environment, agent, and joint predictive states instead of collapsing them into one latent-state story. Distinguish unrestricted counterfactual prediction from support-restricted realised prediction. Use the joint model as a canonical compression target for support-restricted environment modelling.

### 14. Final decision
Keep as a preserved note. This is one of the rare theory papers that genuinely improves the ontology around world models instead of just decorating it.

## 6. Mandatory critical angles

The paper is strongest on mechanism, explicit state, abstraction, and transferability of framing. It earns the world-model label because it says exactly what the model is a model of. The main limitation is that the estimation story is still missing.

## 7. Writing style

The right tone is severe and approving. The paper is valuable because it corrects a conceptual sloppiness that a lot of more fashionable work depends on.

## 8. Repository output format

Saved as a preserved paper note because the channel-first distinction and support-restriction result are likely to age well and transfer across many agent settings.
