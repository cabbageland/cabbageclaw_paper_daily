# Dense Supervision Is Not Enough: The Readout Blind Spot in Looped Language Models

## Basic info

* Title: Dense Supervision Is Not Enough: The Readout Blind Spot in Looped Language Models
* Authors: Rituraj Sharma, Tu Vu
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.24898
* Date surfaced: 2026-06-25
* Why selected in one sentence: It gives a concrete failure mode where every recurrent loop is supervised, but the loss still cannot see an active hidden-state variable.

## Quick verdict

* Must read

This is the cleanest mechanism paper in today's scan. I inspected the full arXiv PDF, especially the scale-visibility argument, 2x2 ablation, gradient diagnostics, clamp controls, variable-depth results, 1.4B sanity check, and limitations. The paper is useful because it separates two things people often collapse: making intermediate exits predictive and controlling the recurrent state they feed back into.

## One-paragraph overview

Looped language models reuse a transformer block across recurrent depth, so the hidden state at each loop is both a prediction interface and the runtime state for later computation. The paper shows that dense per-loop cross-entropy trains the visible prediction interface but does not necessarily control variables hidden by the readout. The concrete case is hidden-state scale: RMSNorm or LayerNorm readouts make scale nearly invisible to immediate cross-entropy, while pre-norm residual recurrence still carries and updates scale. In 44M and 129M looped transformers, per-loop loss through RMSNorm readouts makes exits usable but still lets final hidden-state norms drift into the tens of thousands. Raw readouts, explicit norm penalties, or scale-removing recurrence keep scale controlled and improve the variable-depth perplexity frontier.

## Model definition

### Inputs

The models receive token sequences from WikiText-103 in the main controlled experiments. Each hidden state is looped through the same shared decoder stack for K = 4 recurrent applications. The paper also reports a separate 1.4B sanity check on FineWeb-trained Ouro-style models.

### Outputs

At each loop, the model emits next-token logits through either a normalized readout or a raw readout. Evaluation outputs include token-level cross-entropy, perplexity, early-exit quality, hidden-state norms, radial-gradient diagnostics, and throughput/perplexity curves across inference depths.

### Training objective (loss)

The main loss is autoregressive cross-entropy. The ablation crosses terminal-only versus per-loop cross-entropy with RMSNorm versus raw readouts. A norm-penalty control adds an explicit scale-visible auxiliary loss over recurrent hidden-state RMS norms. The exact point is that per-loop cross-entropy alone is not enough when the readout hides the active variable.

### Architecture / parameterization

The main models are looped pre-norm RMSNorm/SwiGLU transformer decoders with shared recurrent stacks: 8 layers at 44M parameters and 12 layers at 129M. The output projection is shared across exits. The readout is either RMSNorm(Hk), raw Hk, or a hybrid final-only normalization setup. The recurrence feeds unnormalized hidden states back into the next loop unless an explicit scale-removing control is used.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It asks what dense supervision actually controls in a recurrent-depth language model. A looped model's hidden state is not just an output interface; it is the state that later loops inherit. If the supervised readout hides some state coordinate, training can look dense while that coordinate remains underconstrained.

### 2. What is the method?

The authors formalize a readout blind spot: an active recurrent variable may be invisible to the readout loss. They instantiate it with hidden-state scale. Scale-invariant readouts remove the immediate radial cross-entropy signal, while pre-norm residual updates preserve and can change scale. They then test this with a controlled 2x2 ablation over loss placement and readout type, plus norm penalties, final-only normalization, radial-gradient measurements, recurrent scale clamps, variable-depth evaluation, and a 1.4B diagnostic.

### 3. What is the method motivation?

Looped models are attractive because test-time depth can become a compute knob. But variable-depth use only works if intermediate exits are useful and the recurrent state remains controlled. The paper's motivation is to show that these are separate design requirements.

### 4. What data does it use?

The main controlled experiments train on WikiText-103. The larger sanity check uses FineWeb for 1.4B Ouro-style checkpoints and evaluates on WikiText-103 subsets, downstream multiple-choice tasks, and held-out FineWeb-tail slices.

### 5. How is it evaluated?

The paper reports perplexity and cross-entropy at fixed recurrent depth, hidden-state norms, radial-gradient fractions, scale-clamp effects, token-level norm distributions, and variable-depth perplexity/throughput curves. The important evaluation is not just final perplexity; it is whether the model can use recurrent depth without uncontrolled state drift.

### 6. What are the main results?

In the main table, per-loop RMSNorm readouts still drift badly: final-loop hidden-state norms reach about 39,207 at 44M and 56,051 at 129M. Raw readouts keep norms in the tens, and norm penalties do the same while preserving normalized readouts. Per-loop cross-entropy makes exits usable, but does not control scale. Radial-gradient diagnostics show normalized readouts have radial-gradient fractions around 1e-8, while raw readouts restore a scale-sensitive signal. The variable-depth results show that scale-controlled variants preserve usable exits and improve the perplexity/compute frontier relative to the nearly K-invariant RMSNorm baseline.

### 7. What is actually novel?

The useful novelty is the visibility-activity distinction. The paper does not just say looped models can be unstable. It shows a specific mismatch: a variable can be active in recurrence while invisible to the immediate supervised readout. That gives a design rule, not just a warning.

### 8. What are the strengths?

The controls are good. Raw readouts alone could have many confounds, but the paper triangulates with explicit norm penalties, final-only normalization, radial-gradient measurements, and recurrent scale clamps. It also avoids overstating normalized readouts as inherently bad; the failure arises when scale remains active in the recurrent state while every loss hides it.

### 9. What are the weaknesses, limitations, or red flags?

The main controlled evidence is at 44M and 129M on WikiText-103. The 1.4B result is a sanity check, not a full seeded ablation. The mechanism is local rather than a complete theory of training dynamics. The variable-depth evaluations are teacher-forced language-model scoring, not full production autoregressive serving with real KV-cache and batching constraints.

### 10. What challenges or open problems remain?

The obvious extension is to identify other recurrent variables besides scale that are active but hidden by the supervised interface. Another is to test whether similar blind spots appear in latent-reasoning, world-model, or recurrent agent architectures where the readout is a planner, value head, or tool-call formatter rather than next-token logits.

### 11. What future work naturally follows?

Future looped-model papers should report state-control diagnostics alongside exit quality. A practical baseline is an explicit norm penalty or a scale-removing recurrent path whenever normalized readouts are kept. More broadly, training objectives should state which recurrent state coordinates they can actually supervise.

### 12. Why does this matter for cabbageland?

Cabbageland keeps caring about hidden state that actually carries work across time. This paper is a sharp reminder that supervision only controls what the interface exposes. If a world model, memory module, or agent state transition carries variables the loss cannot see, "dense supervision" may only train the visible veneer.

### 13. What ideas are steal-worthy?

For any recurrent or iterative model, explicitly distinguish exit usability from state control. Add diagnostics for variables the readout normalizes away. Use perturbation or clamp tests to check whether an accumulating state variable is doing predictive work or just drifting. In agent settings, ask the equivalent question: what does the next-step loss make visible, and what state variables are merely being carried forward unsupervised?

### 14. Final decision

**Keep it.** This is a high-signal mechanism paper. The takeaway is portable: active recurrent state needs either visibility to a loss or removal from the dynamics; dense loss placement alone is not a magic solvent.
