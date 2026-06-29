# Vision-Default, Prior-Override: Causal Mechanisms of Perception-Knowledge Conflict in Vision-Language Models

## Basic info

* Title: Vision-Default, Prior-Override: Causal Mechanisms of Perception-Knowledge Conflict in Vision-Language Models
* Authors: Niclas Lietzow, Danielle Bitterman, Carsten Eickhoff, William Rudman, Michal Golovanevsky
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.28273
* Date surfaced: 2026-06-29
* Why selected in one sentence: It gives a causal component-level account of when VLMs follow conflicting visual evidence versus stored world knowledge.

## Quick verdict

* Must read

This is the most relevant paper in today's scan because it turns a fuzzy multimodal reliability problem into a sparse circuit story with interventions. I inspected the full arXiv PDF, including the task setup, activation-patching method, head and MLP ablations, cross-architecture comparison, discussion, and limitations. I did not run the released code or independently reproduce the patching experiments, so the exact head lists and margins remain paper claims.

## One-paragraph overview

The paper studies vision-language models shown counterfactual color images, such as a blue strawberry, while being asked either what color the object is here or what color it usually is. Across Qwen-VL, LLaVA-NeXT, and PaliGemma models, the authors find that visual grounding behaves like the default path, while prior-knowledge answers require active injection by a small late-network set of attention heads. Patching those components can shift answers, and ablating the promoting heads flips many prior-grounded answers back toward visual answers while barely disturbing ordinary visual grounding. The useful claim is not just that VLMs can be biased toward pixels; it is that the override from visual evidence to stored knowledge has concrete routing and writing components.

## Model definition

### Inputs
The analyzed systems are VLMs receiving a counterfactual image plus a text prompt. The image is drawn from the Visual-Counterfact dataset, which contains 469 recolored everyday objects. The prompts compare a visual grounding mode, asking about the observed color, with a prior grounding mode, asking about the usual color.

### Outputs
The model emits a color answer token. The paper also outputs restoration scores, flip rates, component classifications, attention-routing measurements, logit-lens hit rates, and ablation effects for attention heads and MLP sublayers.

### Training objective (loss)
The paper does not train the VLMs. It uses existing instruction-tuned VLMs and applies activation patching, causal component ablation, PCA-based component classification, and logit-lens analysis. There is no new optimization loss for the inspected models.

### Architecture / parameterization
The inspected architectures are transformer-based VLMs: Qwen-VL 3B/7B, LLaVA-NeXT 7B, and PaliGemma 3B/10B. The interventions target residual-stream activations, individual attention-head outputs at the WO input, and MLP sublayer outputs at the last token position.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It asks how VLMs resolve conflicts between what they see and what they know. The motivating failure is not a lack of perception or a lack of stored knowledge, but a control problem: the model may have both signals and still surface the wrong one for the prompt.

### 2. What is the method?
The authors run each model on the same counterfactual image under visual and prior prompts, cache activations, and patch components across grounding modes. They measure whether patched components restore the source-mode answer. They then zero-ablate selected heads or MLP outputs to test necessity, not just sufficiency.

### 3. What is the method motivation?
Behavioral accuracy cannot tell whether the model failed to perceive the image, forgot world knowledge, or routed the wrong signal into the answer. Component-level causal interventions can distinguish those possibilities and expose where a control mechanism might be edited.

### 4. What data does it use?
The main data is Visual-Counterfact: 469 recolored object images paired with color questions. The paper restricts many analyses to correctly conflicting examples so that patching and ablation are measuring conflict resolution rather than generic model failure.

### 5. How is it evaluated?
Evaluation combines accuracy under no-conflict and conflict conditions, activation patching restoration scores, answer flip rates under patching, group and single-component ablations, image-token attention fractions, and logit-lens checks for whether late heads directly write answer tokens.

### 6. What are the main results?
No-conflict accuracy is high, around 86-96 percent across conditions, but prior-prompt accuracy on counterfactual images collapses to 17.7-55.7 percent. Only 2.5-4.8 percent of attention heads are classified as strongly mediating the conflict. Ablating promoting heads flips prior-grounded predictions in 68-96 percent of correctly conflicting examples, while changing visual-grounded predictions in only 0.8-7.5 percent. MLP effects point in the same direction but are weaker.

### 7. What is actually novel?
The novelty is the causal asymmetry: visual grounding is robust and default-like, while prior grounding depends on a sparse late attention circuit. The routing/writing decomposition is also useful: some heads redirect information flow, while later heads project the answer token into the residual stream.

### 8. What are the strengths?
The paper uses both patching and ablation, so it checks sufficiency and necessity. It repeats the story across three VLM families rather than one model. It also avoids pretending all architectures implement the mechanism identically: Qwen-VL and LLaVA-NeXT shift attention between image and text tokens, while PaliGemma appears to route through differences in attended representations.

### 9. What are the weaknesses, limitations, or red flags?
The conflict type is narrow: mostly color-property conflict. The models are in the 3B-10B range, so larger frontier VLMs may learn different control strategies. The interventions target the last token position, which is standard but can miss earlier-sequence components. The dataset is clean and controlled, which helps mechanism discovery but may overstate how directly the result transfers to messy visual reasoning.

### 10. What challenges or open problems remain?
The next challenge is testing whether the same sparse prior-override pattern appears for shape, size, spatial relations, object identity, medical evidence, charts, and UI screenshots. Another open problem is whether interventions on these heads can improve behavior without producing brittle prompt- or dataset-specific hacks.

### 11. What future work naturally follows?
Extend the intervention setup to larger VLMs and richer conflict types, compare model families with different visual-token integration schemes, test editing or steering methods that modulate the identified heads, and pair the internal circuit with external uncertainty or evidence-routing policies.

### 12. Why does this matter for cabbageland?
Cabbageland cares about agents and multimodal systems that decide when to trust perception, memory, retrieval, or prior knowledge. This paper gives a concrete object to inspect: not "the VLM is confused," but "a sparse override circuit failed to route the right evidence source." That is much more useful for building monitors, gates, and interventions.

### 13. What ideas are steal-worthy?
When a model has two plausible evidence sources, construct paired prompts that hold one source fixed while switching the requested grounding mode. Use both patching and ablation before calling a component causal. Separate routing heads from writing heads. Treat "visual default" as an architectural prior that may need explicit override when the task asks for stable world knowledge.

### 14. Final decision
Keep and cite. This is a strong mechanistic paper with a narrow but clean setup. The right use is as a template for evidence-source routing audits in multimodal agents, not as a universal map of all VLM conflict behavior.
