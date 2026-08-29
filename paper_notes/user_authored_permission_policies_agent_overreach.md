# Do User-Authored Permission Policies Improve Protection Against AI Agent Overreach?

## Basic info

* Title: Do User-Authored Permission Policies Improve Protection Against AI Agent Overreach?
* Authors: Ting Yan
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.27443
* Date surfaced: 2026-08-29
* Why selected in one sentence: It shows that standing permission rules can be weaker than per-action review when users mostly encode deferral rather than commitment.

## Quick verdict

* Must read

I inspected the full arXiv HTML text, especially the study design, the adjusted outcome comparisons, the rule-breakdown analysis, and the discussion section. This paper earns a preserved note because it exposes the exact place where intuitive agent-control UI can fail: a "policy" is not a boundary if most of it is just an `ask` surface that returns the decision to runtime. The negative result is more useful than most positive safety marketing.

## One-paragraph overview

The paper studies three ways to control an agent acting across ordinary digital tasks: per-action human approval, automated per-action review by a model, and a reusable standing policy authored by a non-expert user in plain language. The standing-policy condition maps tool actions into four consequence categories and lets users choose `allow`, `ask`, or `never` for each one before the simulated day begins. Across 113 participants supervising the same 18 scripted actions, including seven overreach actions, the standing-policy design reduces runtime prompts but blocks less overreach than either baseline because participants overwhelmingly choose `ask`, sending most hard decisions back to runtime where they are then often approved.

## Model definition

### Inputs
Tool-action descriptions and their mapped consequence categories, plus the user-authored rule for each category.

### Outputs
Permission decisions: allow automatically, ask the user at runtime, or block automatically.

### Training objective (loss)
The accessible paper text does not describe a new trainable model objective as the contribution. The learned piece is a language-model consequence mapper used inside the permission mechanism, but the main contribution is the permission design and its empirical evaluation.

### Architecture / parameterization
A language-model-assisted permission layer maps actions into plain-language consequence categories. Users author standing rules over those categories, and the runtime either executes, blocks, or prompts accordingly.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to give ordinary users a reusable way to constrain agent actions across different tools and services without requiring them to approve every single step forever.

### 2. What is the method?
The method compares three permission designs. The interesting one is POLICY: users see examples for four consequence categories, author one standing rule per category using allow/ask/never, and then supervise the agent's simulated day under those rules.

### 3. What is the method motivation?
Per-action confirmation does not scale well, but pre-authored standing rules are only useful if they meaningfully settle future decisions instead of recreating runtime approval in disguise.

### 4. What data does it use?
The study analyzes 113 participants without professional software backgrounds. Each participant supervises the same 18-action simulated day, which includes 7 overreach actions covering money, outbound communication, deletion, and private-data access.

### 5. How is it evaluated?
The paper compares overreach blocked, required actions completed, runtime permission prompts, total intervention time, and earlier-preference agreement across the three conditions. It also analyzes the authored-rule composition and the runtime path of executed versus blocked overreach actions.

### 6. What are the main results?
POLICY blocks less overreach than both baselines: 20.1 percentage points worse than HITL and 14.5 points worse than AUTO. Required-action completion stays high, and runtime prompts fall from 18.0 in HITL to 10.9 on average in POLICY, but total intervention time is not reliably lower once rule-setup time is included. The real story is the rule breakdown: users choose `ask` for 114 of 140 standing rules, and 133 of 148 executed overreach actions in POLICY follow explicit runtime human approval. POLICY therefore weakens protection mainly because it defers hard cases rather than deciding them in advance.

### 7. What is actually novel?
The novelty is the framing. The paper treats agent permission design as a commitment problem rather than merely a classification problem. That reframing makes the negative result interpretable instead of surprising.

### 8. What are the strengths?
The experiment is concrete, the outcome accounting is clear, and the paper tracks the full path from standing rule to final execution rather than stopping at UI preference. The analysis of where the weaker protection comes from is especially good: it is mostly runtime human approval, not silent automatic allowance.

### 9. What are the weaknesses, limitations, or red flags?
This is still a short simulated session rather than a long real deployment. The consequence categories are broad, participants only see two examples per category before authoring a standing rule, and the paper studies one particular mapping-and-prompting design rather than the whole space of permission systems.

### 10. What challenges or open problems remain?
The big open problem is how to let users encode real defaults with exceptions, rather than forcing a choice between broad standing categories and repeated case-by-case approval. Another open question is how such systems behave under long-term approval fatigue.

### 11. What future work naturally follows?
More specific rule languages, exception mechanisms, argument-sensitive policies, and deterministic enforcement layers would all follow naturally. Longer real-world deployments would also test whether people can maintain and refine policies over time.

### 12. Why does this matter for cabbageland?
Because cabbageland keeps caring about governed action rather than raw tool access. This paper shows that authorization is not solved by asking users what they prefer in plain English. A boundary exists only if it survives the next tempting runtime prompt.

### 13. What ideas are steal-worthy?
Track permission systems as decision pathways, not just top-line block rates. Separate preference expression from commitment. Measure how often a standing rule actually settles the action before runtime. Treat `ask` as a deferral state, not as evidence that control has been solved.

### 14. Final decision
Keep as a preserved note. This is a sharp negative-result paper with direct design implications for real agent permission systems.

## 6. Mandatory critical angles

The paper is strongest on motivation and decomposition. It does not pretend that a broad natural-language category is equivalent to a real policy, and it follows the permission path far enough to prove where the leak happens. The data are realistic enough to matter at the interface level, though still obviously bounded by the short scripted setting. The main transfer lesson is durable: advance policy only becomes governance when it resolves future action without instantly collapsing back into runtime approval.

## 7. Writing style

The tone should be crisp and a little grim. The paper deserves credit for saying the quiet part out loud: users often keep the right to decide later instead of defining a real boundary now.

## 8. Repository output format

Saved as a preserved paper note because the preference-versus-commitment distinction is a durable design idea for agent authorization.
