# Explaining Attention with Program Synthesis

## Basic info

* Title: Explaining Attention with Program Synthesis
* Authors: Amiri Hayes, Belinda Z. Li, Jacob Andreas
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.19317
* Date surfaced: 2026-06-18
* Why selected in one sentence: It tests whether attention-head explanations can be executable programs that reproduce and replace neural attention maps, not just natural-language labels.

## Quick verdict

* Highly relevant

This is the sharpest paper in today's scan because it gives interpretability a causal handle. A description of an attention head is only so useful; a Python program that can replace the head's attention matrix during a forward pass is a much stronger object. I inspected the full PDF, including the method, program-synthesis pipeline, alignment results, head-replacement results, downstream QA evaluation, and limitations.

## One-paragraph overview

The paper synthesizes executable Python programs that approximate the attention maps of transformer attention heads from input tokens alone. For each head, the authors extract real attention patterns, summarize high-weight token-pair interactions in a prompt, ask an auxiliary language model to write candidate programs, refine those programs with error feedback, and select the best one using held-out attention similarity. The key move is causal validation: high-fit programs are inserted into the model in place of learned attention maps. Across BERT-base, GPT-2-small, TinyLlama-1.1B, and Llama-3.2-3B-style decoder models, many attention heads are approximated well enough that replacing a substantial fraction of heads causes only modest perplexity or downstream QA degradation.

## Model definition

### Inputs
The pipeline takes a target transformer model, a corpus of token sequences, and recorded attention matrices for each attention head. The synthesis prompt receives token-pair attention summaries, especially high-weight attention edges, plus structured feedback from the program's best and worst examples. The generated program itself takes input tokens and returns a predicted attention matrix.

### Outputs
The output is one executable Python function per attention head, or a best-fit program selected from the program library. Each function emits an attention matrix for a given token sequence. In the causal tests, the program's emitted matrix replaces the original neural attention matrix during the target model's forward pass.

### Training objective (loss)
The paper does not train a new target model. Candidate programs are selected and refined using Jensen-Shannon distance against real attention maps and evaluated with intersection-over-union similarity on held-out examples. The auxiliary language model is used for program synthesis; its native training objective is not part of the paper's method.

### Architecture / parameterization
The method is a post-hoc interpretability pipeline around existing transformer language models. It uses an auxiliary language model to synthesize Python functions with access to tools such as NumPy, spaCy, and NLTK. The target models include BERT-base, GPT-2-small, TinyLlama-1.1B, and a Llama-3B-class decoder model. The final artifact is a library of 1,664 head-level programs.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Automated interpretability often produces ambiguous natural-language descriptions of neural components. Those descriptions may be suggestive, but they are hard to verify and cannot be directly substituted into the computation. The paper asks whether a neural component can instead be explained by executable code that approximates its behavior.

### 2. What is the method?
For each attention head, the authors collect attention maps on TinyStories examples, summarize the salient token-pair patterns, and prompt an auxiliary language model to synthesize a Python function mapping input tokens to an attention matrix. Invalid programs are rejected, valid ones are scored, and the best candidate receives one round of feedback-conditioned refinement. The selected programs are then evaluated by attention-map similarity and by replacing actual attention heads during model inference.

### 3. What is the method motivation?
Programs sit between opaque weights and vague prose. They are readable, executable, testable, and substitutable. If a program really captures a head's behavior, it should not only look similar to the attention map; it should also preserve model behavior when inserted into the forward pass.

### 4. What data does it use?
The program synthesis and held-out attention-alignment tests use TinyStories, chosen for relatively simple structure. The causal downstream evaluations use HellaSwag, PIQA, SciQ, ARC-Easy, Social IQA, and COPA. The target models are pretrained language models rather than models trained from scratch for this paper.

### 5. How is it evaluated?
The paper uses two main evaluation modes. First, it measures attention-map alignment with intersection-over-union similarity against held-out real attention maps, comparing intended programs, globally best programs, and random or structural baselines. Second, it performs interchange interventions by replacing real attention heads with program outputs, then measures perplexity and multiple-choice QA accuracy as more heads are replaced.

### 6. What are the main results?
The globally best program outperforms random and uniform baselines across the evaluated models. Decoder models are easier to approximate than BERT-base, and larger decoder models show higher mean best-program IoU: GPT-2 around 69%, TinyLlama around 74%, and Llama-3B around 79% in the reported summary. IoU is strongly negatively correlated with perplexity increase after replacement. The paper reports that replacing roughly 30-40% of attention heads with high-similarity programs does not significantly degrade downstream QA performance, while the abstract highlights a 25% replacement point with about a 16% perplexity increase.

### 7. What is actually novel?
The novelty is not using an LLM to describe attention. The novelty is producing executable head-level surrogates and then causally inserting them into real model forward passes. That turns interpretability from a labeling exercise into a substitution test.

### 8. What are the strengths?
The substitution test is the main strength. It prevents the explanation from being merely decorative. The approach is also surprisingly practical: the paper reports producing the whole program library for roughly $150 in API cost. The best-program library result is useful too, because it shows that reusable symbolic motifs can explain multiple heads better than per-head first guesses.

### 9. What are the weaknesses, limitations, or red flags?
The method explains attention matrices, not the full head computation including value vectors and downstream residual effects. TinyStories is a simple in-distribution source for synthesis, so broader text and harder behavior may expose brittle programs. Some high-scoring programs are simple, and performance improvements at low replacement levels may partly resemble pruning rather than faithful explanation. BERT-base is much less well characterized, and many heads still score below 40% IoU.

### 10. What challenges or open problems remain?
The hard next step is scaling from attention-map imitation to fuller circuit-level explanations that include values, MLPs, residual stream effects, and cross-head interactions. Another challenge is synthesizing richer programs without letting the auxiliary model overfit superficial patterns in the prompt examples.

### 11. What future work naturally follows?
Natural follow-ups include OOD substitution tests on more varied corpora, richer program languages, automatic simplification of synthesized programs, and using executable surrogates for model editing. A useful variant would compare program replacement against pruning and low-rank surrogate replacement to separate true symbolic explanation from removal of unimportant heads.

### 12. Why does this matter for cabbageland?
Cabbageland cares about explicit structure that does work. This paper gives a clean standard: an explanation should be runnable, intervenable, and behavior-preserving under the right conditions. That principle transfers to memory systems, world models, planners, source trackers, and evaluation probes.

### 13. What ideas are steal-worthy?
Make explanations executable. Evaluate them by substitution, not just correlation. Build libraries of reusable mechanism programs rather than independent labels for each component. Use similarity metrics only as a filter before a causal intervention, not as the final proof.

### 14. Final decision
Preserve and revisit. This is directly useful for interpretability framing and for any future cabbageland work that wants explanations to be operational rather than ornamental.
