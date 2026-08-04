# Don't Offer What Can't Be Done: Deterministic Executability Gating for LLM Skill Selection at Scale

## Basic info

* Title: Don't Offer What Can't Be Done: Deterministic Executability Gating for LLM Skill Selection at Scale
* Authors: Ortal Ashkenazi, Vitalii Kloz, Mykhailo Ulianchenko
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.01050
* Date surfaced: 2026-08-04
* Why selected in one sentence: It isolates a concrete production failure mode in tool agents and fixes it with a narrow deterministic contract instead of more prompt gymnastics.

## Quick verdict

**Highly relevant**

I inspected the arXiv HTML paper, especially the failure-mode definition, exit-condition inversion, formal gate contract, production evaluation, deployment lessons, and limitations. The paper is strong because the claim is narrow and true: if the authoritative state already implies a skill will abort, that skill should not be shown to the model. The limitations are equally clear. The evidence comes from one ten-skill topic family, the gate only handles deterministic preconditions, and the paper does not claim customer-outcome lift.

## One-paragraph overview

The paper argues that semantic tool retrieval solves the wrong problem when skills have hard business-state preconditions. A user message can be topically relevant to a skill while the current account state already guarantees that the skill cannot complete. The proposed solution is a three-stage pipeline: a recall-oriented semantic matcher identifies the domain family, a deterministic gate removes candidates whose own exit conditions hold in authoritative state, and only then does the LLM decide whether to activate one of the remaining skills. The gate is built by inverting each skill's internal abort conditions into pre-execution predicates, so the claim is contract-relative soundness rather than a learned estimate of usefulness.

## Model definition

### Inputs
The system takes a user message, a domain-family candidate set from a state-blind semantic matcher, and the authoritative account or site state required to evaluate each skill's exit predicates.

### Outputs
It outputs a filtered visible skill set and then a final activation decision by the LLM over that filtered set.

### Training objective (loss)
There is no new learnable gate in the contribution. The executability gate is deterministic code over state predicates. The semantic matcher and final LLM decision stage are existing components in the deployed pipeline rather than the paper's novel learned model.

### Architecture / parameterization
The architecture is a three-stage pipeline: recall-oriented semantic matching, deterministic executability gating based on inverted exit conditions, and final agent decision over the remaining visible skills.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve non-executable skill exposure: a skill can be semantically relevant to the message while being impossible to execute under the current business state.

### 2. What is the method?
The method is deterministic executability gating. For each skill, the system reuses the same state predicates that would make the skill exit during execution and applies them before exposing the skill to the model.

### 3. What is the method motivation?
Prompting the model to remember every business-state constraint is brittle and wasteful. A deterministic backend can decide whether a skill is even eligible before the model sees it.

### 4. What data does it use?
The production study covers 756,641 user messages from 267,612 conversations over Jun 9, 2026 through Jul 10, 2026 in a ten-skill customer-care domain family, plus a risk-enriched counterfactual replay cohort of 1,000 conversations.

### 5. How is it evaluated?
It is evaluated by message, conversation, candidate-pair, and skill-description-token counts, plus a replay analysis that measures how often the model selects a production-blocked skill when the gate is removed.

### 6. What are the main results?
The semantic stage matches 174,927 messages, or 23.1% of all chatbot messages. Within that stream, the gate removes 1,039,462 of 1,749,270 skill-message pairs, or 59.4%. It saves 228.8 million skill-description tokens, which is 59.1% of the post-semantic skill-description footprint and 90.5% relative to exposing all ten skills to every message. In the 1,000-conversation replay, the model selects a production-blocked skill in 78 conversations, or 7.8%.

### 7. What is actually novel?
The novelty is not another retrieval heuristic. It is the clean separation of topical relevance from state-feasible executability, plus the use of exit-condition inversion to make the gate sound relative to the implemented skill contract.

### 8. What are the strengths?
The paper has a precise failure mode, a deterministic contract, real production-scale data, and good deployment lessons about predicate parity, state freshness, and monitoring.

### 9. What are the weaknesses, limitations, or red flags?
The scope is narrow: one topic family, one observation window, and deterministic preconditions only. The replay study measures model selection under captured context, not downstream execution success or customer outcome changes.

### 10. What challenges or open problems remain?
Keeping predicates aligned with evolving skill logic is an ongoing engineering burden. The gate also does not solve ambiguous user intent, missing information, or runtime failures unrelated to represented exit conditions.

### 11. What future work naturally follows?
Testing the design across more skill families, measuring end-to-end customer outcomes, integrating richer authorization logic, and combining deterministic gating with broader action-risk controls would all be natural follow-ons.

### 12. Why does this matter for cabbageland?
It matters because any tool-using agent with persistent state faces this exact problem. Semantic relevance is not enough if the environment already knows an action is impossible or unauthorized.

### 13. What ideas are steal-worthy?
Separate semantic recall from state-feasibility gating. Reuse the skill's own abort predicates instead of learning a proxy. Treat predicate parity and state freshness as explicit release invariants with regression tests and monitoring.

### 14. Final decision
**Keep it.** This is a useful systems paper with a concrete mechanism and a lesson that transfers directly to real agent stacks.
