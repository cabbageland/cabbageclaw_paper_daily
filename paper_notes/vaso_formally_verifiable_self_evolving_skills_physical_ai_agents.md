# VASO: Formally Verifiable Self-Evolving Skills for Physical AI Agents

## Basic info

* Title: VASO: Formally Verifiable Self-Evolving Skills for Physical AI Agents
* Authors: Yunhao Yang, Neel P. Bhatt, Kevin Wang, Samuel Tetteh, Zhangyang Wang, and Ufuk Topcu
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.05395
* Date surfaced: 2026-06-06
* Why selected in one sentence: It turns formal counterexamples into updates to reusable robot skill contracts, which is a cleaner self-improvement object than a one-off plan, prompt, or model weight change.

## Quick verdict

**Highly relevant**

This is the strongest paper today because the core object is explicit and inspectable: a robot skill contract with a formal interface and a planner-facing interface. I inspected the arXiv PDF, including the introduction, formulation, method, evaluation, baseline table, ablations, and proposition-alignment failure case. Confidence is high on the mechanism and main caveat, though I did not fully audit every appendix prompt or platform-specific execution trace.

## One-paragraph overview

VASO targets a real failure mode in foundation-model robotics: LLMs can generate reusable skills cheaply, but execution feedback and self-critique only show sampled success, not safety under untested cases. The paper represents each skill as a tuple containing global temporal specifications, a local skill rule, and a semantic contract. The semantic contract includes a proposition-aligned labeling function that maps robot states, observations, and controls to logical propositions, plus a planner-facing template that guides executable plan generation. VASO first checks whether the skill rule is logically feasible, then verifies plans induced by the skill. When verification fails, the model checker returns a counterexample trace, and VASO converts that trace into a textual gradient that updates the reusable skill contract while keeping foundation-model weights frozen.

## Model definition

### Inputs

The system takes a task prompt, executable robot commands or APIs, global temporal-logic specifications, and a foundation-model-generated skill contract. For plan-level verification, it also takes the plan generated from the skill and the proposition-aligned labeling function that maps execution states to atomic propositions.

### Outputs

VASO outputs a refined skill contract. The planner can then use the refined contract to produce executable robot plans that better satisfy global and local temporal specifications.

### Training objective (loss)

This is not standard gradient training over model weights. The optimization objective is to refine the semantic contract so that plans generated from it satisfy the relevant temporal specifications. Verification failures are converted into textual gradients for iterative prompt-level contract refinement.

### Architecture / parameterization

The stack has three pieces: a skill generator, a planner, and a formal verifier. The skill is the key representation: global LTL specifications, a local LTL rule, a proposition-aligned labeling function, and a planner-facing behavior template. Plans are compiled into transition-system representations and checked with a model checker.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Reusable robot skills are becoming the interface between foundation models and physical control, but current skill-evolution loops mostly learn from sampled traces. A skill can work on sampled rollouts while still inducing plans that violate safety constraints under untested conditions.

### 2. What is the method?

- Generate a skill contract from the task, APIs, and global specifications.
- Check whether the local skill rule is logically feasible under the global specifications.
- Use the skill contract to guide plan generation.
- Compile the generated plan into a symbolic transition system through the proposition-aligned labeling function.
- Verify the plan against global and local temporal specifications.
- Translate verifier counterexamples into textual gradients that update the reusable skill contract.

### 3. What is the method motivation?

The paper's strongest idea is that verification should not merely reject bad plans. If a generated plan fails because a reusable skill contract is underspecified or misleading, the counterexample should update that contract so future plans inherit the correction.

### 4. What data does it use?

The evaluation uses Clearpath Jackal ground-robot tasks and PX4 quadcopter tasks, with 11 temporal-logic specifications and 400 generated plans. The paper uses GPT-5-nano as the skill generator and GPT-4o-mini as the planner in the reported setup.

### 5. How is it evaluated?

The paper reports safety score, task completion, skill feasibility, reuse on held-out prompts, comparison with flat prompt optimization, comparison with learning and zero-shot planning baselines, and automatic versus handcrafted proposition alignment.

### 6. What are the main results?

Optimized skills reach roughly 95% safety after seven optimization steps in the main plot and the paper reports 97.2% formal-specification compliance with handcrafted proposition alignment. Automatic proposition alignment is close, at 96.8% safety score in the baseline table. VASO also reports better safety than LLM+P, ReAct, LLM-Planner, DSPy, RoboInstruct, and RLVF while maintaining competitive task completion.

### 7. What is actually novel?

The novelty is the feedback target. VASO does not just verify a generated plan, tune a flat prompt, or fine-tune model weights. It makes the reusable skill contract the object that verification counterexamples modify.

### 8. What are the strengths?

- The representation is concrete: formal local rule, proposition alignment, and planner-facing template.
- Verification feedback is reused across future plans by updating the skill itself.
- The evaluation includes real robot platforms and held-out prompt reuse.
- The paper is explicit about the proposition-alignment assumption, which is the right failure mode to surface.

### 9. What are the weaknesses, limitations, or red flags?

- The guarantee is only as good as the proposition-aligned labeling function. The paper shows a PX4 velocity example where an incorrect mapping ignores the vertical velocity component and creates a false safety guarantee.
- The global and local specifications must be available and expressible in the chosen logic.
- The planner-facing contract still depends on foundation-model generation quality.
- The platforms are meaningful but not a proof that the approach scales to messy open-world manipulation with rich perception and contact dynamics.

### 10. What challenges or open problems remain?

The main open problem is grounding. Formal verification over the wrong abstraction can be beautifully wrong. Future systems need validation that symbolic propositions track the physical quantities and perceptual predicates they are supposed to represent.

### 11. What future work naturally follows?

- Combine proposition alignment with probabilistic grounding checks.
- Use runtime monitors to test whether symbolic predicates remain faithful under sensor noise and partial observability.
- Extend the skill-contract interface to manipulation domains where contact and object state are less clean than navigation constraints.
- Reuse verifier counterexamples across a library of related skills, not just one skill at a time.

### 12. Why does this matter for cabbageland?

Because it replaces a mushy self-improvement story with a real artifact. The skill is not just text, not just a latent habit, and not just a plan. It is a reusable contract that can be inspected, verified, and updated from counterexamples.

### 13. What ideas are steal-worthy?

- Make the reusable skill contract the optimization target.
- Translate formal counterexamples into natural-language update signals.
- Separate skill-level feasibility checking from plan-level behavior verification.
- Treat proposition alignment as a first-class interface, not background plumbing.

### 14. Final decision

**Worth keeping and worth revisiting.** VASO is a clean pattern for verifiable physical-agent self-improvement, with the right caveat: formal safety only helps if the symbolic grounding is faithful.
