# Repairing Latent World Models with Horizon-Matched Trajectory Reachability Metrics

## Basic info

* Title: Repairing Latent World Models with Horizon-Matched Trajectory Reachability Metrics
* Authors: Shengzhi Wang, Qingwen Liu
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2605.22164
* Date surfaced: 2026-05-24
* Why selected in one sentence: It cleanly shows that a world model can encode the right state while still exposing a bad planning metric, then fixes only that interface.

## Quick verdict

* Highly relevant

This is a strong mechanism paper because it isolates a specific failure point instead of blaming “world model weakness” in the abstract. The central claim is that latent planning can fail not because the representation lacks task state, but because raw terminal Euclidean distance ranks future candidates with the wrong geometry. I inspected the arXiv HTML full text, including the abstract, introduction, related work, method, and experimental protocol sections. I did not fully audit every appendix analysis, but confidence is high on the paper’s core intervention and evidence chain.

## One-paragraph overview

The paper studies a very particular failure mode in latent model-predictive control. A learned latent world model may encode the task-relevant variables needed for control, but the planner often ranks action sequences using plain Euclidean distance between predicted terminal latent state and goal latent state. If the reachability-relevant variables occupy a small or low-energy subspace, that metric can choose bad candidates even when the right information is present. The proposed fix is trajectory reachability metrics, or TRM: train a small pairwise head on logged trajectory separations and use that learned score, either alone or hybridized with raw latent distance, as the terminal cost for candidate ranking while keeping the world model and planner otherwise fixed.

## Model definition

### Inputs
The method consumes latent states produced by a fixed world model encoder, predicted terminal latents from candidate action rollouts, goal latents, and training pairs of latent states sampled from logged trajectories with temporal-separation labels.

### Outputs
The learned head outputs a scalar reachability-style distance or ranking score between two latent states. At planning time, this score becomes the terminal candidate-ranking cost for model-predictive control.

### Training objective (loss)
The accessible text states that the pairwise head is trained to predict temporal separation between state pairs sampled from the same trajectory. The exact final loss form is not fully exposed in the inspected extract, so I am not claiming more detail than that. The key supervision signal is horizon-aware trajectory separation.

### Architecture / parameterization
A fixed latent world-model planner with a CEM-style candidate sampler, plus a small learned pairwise metric head operating on features built from two latent states, including the two latents and their differences.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Many latent world-model planners assume that terminal Euclidean distance in latent space is a reasonable proxy for task progress. The paper argues this assumption is much stronger than it looks. Even if the representation contains task-relevant variables, the terminal metric can underweight them and rank action sequences badly. The problem is therefore a planner-facing metric mismatch, not necessarily a predictive failure of the world model itself.

### 2. What is the method?
The method trains a post-hoc pairwise terminal metric called TRM on latent-state pairs sampled from logged trajectories. Training data is sampled across broad temporal separations so that the supervision matches the long-horizon candidate-ranking regime used at planning time. At inference, candidate action sequences are rolled forward by the fixed world model to predicted terminal latent states, and TRM scores each predicted endpoint against the goal latent. This learned score replaces or augments raw latent Euclidean distance as the terminal cost used by CEM.

### 3. What is the method motivation?
The motivation is excellent and unusually crisp. A world model can be predictive enough to encode position, topology, or progress signals, yet still expose the wrong scalar geometry to the planner. If so, retraining the entire world model may be overkill. The paper asks the narrower and better question: what if the representation is fine enough, but the planner’s terminal interface is wrong?

### 4. What data does it use?
The core case study is a hard TwoRoom benchmark with matched start-goal manifests, plus evaluation on PushT go50 and go75. The paper also reports improvements for a PLDM baseline in addition to LeWM. The pairwise metric is trained from logged trajectory structure rather than extra oracle planning labels.

### 5. How is it evaluated?
It is evaluated by success rate on fixed planning manifests, by ablations over different pair-sampling regimes, by same-candidate selection audits that test whether the metric changes candidate ordering, by subspace analysis showing that XY state is present but underweighted by raw MSE, and by cross-model tests on PLDM and boundary-condition tests on PushT.

### 6. What are the main results?
On a hard TwoRoom benchmark, raw latent planning with LeWM reaches 7.0% mean success while full-horizon TRM reaches 97.0%. On a PLDM baseline, the same recipe improves performance from 32.7% to 84.0% across three seeds. A short-horizon TRM variant reaches only 35.0%, which strongly supports the paper’s claim that horizon-matched supervision matters. On PushT, TRM improves ranking and selected endpoints more cleanly than closed-loop success, which is a useful and honest limitation.

### 7. What is actually novel?
The novelty is not just “learn a better distance.” The sharper contribution is to treat terminal candidate ranking as a distinct planner interface that can be repaired post hoc, and to show with mechanistic audits that the repair works by changing candidate ordering rather than by quietly changing everything else. The horizon-matched sampling rule also seems genuinely central rather than incidental.

### 8. What are the strengths?
This paper is admirably narrow and causal. It keeps the world model, planner budget, optimizer, and manifests fixed. It then changes only the terminal metric and shows the downstream effect. The evidence chain is also good: probe decodability, subspace weighting analysis, same-candidate ordering audits, and negative controls. That is much stronger than a generic “our learned metric works better” story.

### 9. What are the weaknesses, limitations, or red flags?
The biggest limitation is scope. The cleanest result is in a navigation-style topology problem where reachability geometry is especially stark. In continuous manipulation, the paper itself admits that TRM is better treated as a hybrid cost than a full replacement. So this is not a universal latent-planning cure. It is also a post-hoc patch, which means it diagnoses and fixes one interface rather than yielding a fundamentally more structured world model. That is a strength for causal isolation, but a limitation if you want broader abstraction.

### 10. What challenges or open problems remain?
How to extend reachability-aware terminal metrics to more contact-rich, multimodal, or long-horizon manipulation domains remains open. Another open question is when the better answer is metric repair versus representation redesign. The paper proves that the former can matter, but not that it is always sufficient.

### 11. What future work naturally follows?
Use similar audits on other joint-embedding world models, combine learned reachability metrics with more explicit object or topology structure, and study whether budget-conditioned or directed asymmetric metrics help in harder tasks where symmetric temporal distance is too weak.

### 12. Why does this matter for cabbageland?
It matters because it is a clean warning against confusing information presence with usable structure. A latent state can contain the right variables and still expose the wrong optimization geometry. That is exactly the kind of hidden mushy interface problem cabbageland should care about.

### 13. What ideas are steal-worthy?
Audit planner interfaces separately from representation quality. Learn terminal-ranking metrics at the temporal scale they will actually be used. Use subspace or same-candidate ordering analyses to prove where a planning fix is doing work instead of settling for downstream score changes.

### 14. Final decision
Keep. This is a compact but genuinely useful paper, both as a planner-side repair method and as a methodological example of how to diagnose world-model planning failures without collapsing everything into vague representation talk.
