# SHERLOC: Structured Diagnostic Localization for Code Repair Agents

## Basic info

* Title: SHERLOC: Structured Diagnostic Localization for Code Repair Agents
* Authors: Hovhannes Tamoyan, Sean Narenthiran, Erik Arakelyan, Mira Mezini, Boris Ginsburg
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.24820
* Date surfaced: 2026-06-24
* Why selected in one sentence: It treats code localization as structured diagnosis that must transfer to a repair agent, not just file retrieval that looks good on a leaderboard.

## Quick verdict

* Highly relevant

This is a strong agent-engineering paper because it asks whether localization outputs actually help downstream repair. I inspected the full arXiv PDF, especially the tool loop, structured finding format, localization tables, downstream transfer experiments, contamination controls, quality analysis, and limitations. The paper has a real SWE-Bench familiarity caveat, but it names that caveat and runs useful controls instead of hiding it.

## One-paragraph overview

SHERLOC is a training-free localization framework for repository-level code repair. Given an issue and repository snapshot, it runs a reasoning LLM with a small fixed tool suite: view file, codebase search, repository tree, and connected import tree. The system iterates for up to 20 turns and emits both locations and a five-field diagnostic finding: location explanation, root cause, solution idea, dependencies, and testing impact. The paper's main claim is that useful localization is not merely a file path. A repair agent needs diagnostic context that can change the editing trajectory.

## Model definition

### Inputs

Inputs are a natural-language issue report, a filtered repository tree, compact repository tools, previous tool observations, and a required structured output format. Downstream transfer experiments inject SHERLOC findings into SWE-Agent and OpenHands repair agents.

### Outputs

SHERLOC outputs predicted file/line locations and a structured diagnostic finding with five fields: location explanation, root cause, solution idea, dependencies, and testing impact. In transfer experiments, those outputs become additional context for a separate repair agent.

### Training objective (loss)

SHERLOC is training-free. There is no fine-tuning or reinforcement-learning objective for the localizer. The evaluation objective is localization accuracy/recall and downstream SWE-Bench Verified resolve rate under token budgets. A GPT-5.2 judge is used only for retrospective finding-quality analysis and quality-filtered experiments, not for training SHERLOC.

### Architecture / parameterization

The architecture is a bounded tool-using reasoning loop. A backbone LLM selects from a small deterministic tool suite, receives tool observations, and either continues searching or emits the final structured finding. Self-recovery handles context truncation, repeated calls, malformed tool calls, response-length limits, and forced final synthesis at the turn budget.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Repository-level repair agents spend a large fraction of their budget finding the fault before editing. Existing localization papers often evaluate file retrieval, but a correct file can still be unhelpful if the repair agent does not know why it matters or how the bug propagates.

### 2. What is the method?

SHERLOC frames localization as active repository diagnosis. It gives a reasoning model a compact repository view and bounded tools for file inspection, search, tree navigation, and import/dependency navigation. The model must produce both location spans and a structured diagnostic finding. The outputs can then be injected into repair agents.

### 3. What is the method motivation?

The motivation is that localization should be evaluated by actionability. A path without root cause is a weak interface. A path plus a wrong diagnosis can actively mislead the editor. A path plus a compact, evidence-backed diagnosis is more likely to reduce search and improve the first patch.

### 4. What data does it use?

Localization is evaluated on SWE-Bench Lite and SWE-Bench Verified, with component ablations on 100 SWE-Gym development issues. Downstream repair transfer is measured on all 500 SWE-Bench Verified instances through SWE-Agent and OpenHands across five repair backbones.

### 5. How is it evaluated?

The paper reports file-level accuracy/recall, chunk-level coverage and precision, reasoning turns, zero-tool shortcut rate, token usage, and downstream resolve rate. It compares multiple LLM backbones and leading localizers. It also runs implicit-knowledge controls by masking tools, repository trees, and file paths in issue text.

### 6. What are the main results?

With Qwen3-235B-A22B-Thinking, SHERLOC reaches 84.33 percent accuracy@1 on SWE-Bench Lite and 81.27 percent recall@1 on SWE-Bench Verified. At the roughly 30B matched scale, Qwen3-30B reaches 75.07 percent recall@1 on Verified, above the prior listed 32B baselines. Injecting Qwen3-235B SHERLOC findings into repair agents improves average resolve rate by 5.95 points while cutting localization tokens by 36.7 percent and total tokens by 23.1 percent. The strongest gains are for smaller or weaker repair agents; for very strong agents, low-quality findings can hurt unless filtered.

### 7. What is actually novel?

The novelty is the diagnostic interface. SHERLOC is not just another retriever and not just a bigger code-search prompt. It makes the localization artifact a structured, transferable object and evaluates whether that object changes downstream repair outcomes.

### 8. What are the strengths?

The paper has unusually useful transfer experiments. It tests the output inside real repair agents rather than stopping at Hit@1. It also has a good failure/validity posture: the implicit-knowledge controls show that a large part of SWE-Bench localization can be recovered from issue text alone, while tools and repository exploration still add measurable value.

### 9. What are the weaknesses, limitations, or red flags?

SWE-Bench familiarity remains a serious caveat. The paper estimates that about 58 percent recall on SWE-Bench Verified is achievable from masked issue text alone, and some repositories are much easier than others because they are widely represented in pretraining. The best localization numbers also use a large Qwen3-235B thinking model and substantial inference compute. Quality-filtered SHERLOC is not yet deployable because its best analysis uses a GPT-5.2 judge shown the ground-truth patch.

### 10. What challenges or open problems remain?

The main open problem is clean evaluation on held-out repository distributions where pretraining familiarity is much lower. Another is judge-independent quality estimation: a repair system needs to know whether a finding is reliable before it trusts it, without seeing the gold patch.

### 11. What future work naturally follows?

A good next step is a localizer that produces calibrated confidence over the diagnostic fields, not just over file paths. Another is using SHERLOC-like findings as supervision for smaller localizers or repair agents, while evaluating on non-Python and private-code benchmarks.

### 12. Why does this matter for cabbageland?

Cabbageland agents edit code, inspect systems, and hand off state across tools. SHERLOC gives a clean lesson for those workflows: the state that crosses an agent boundary should be diagnostic, not merely locational. "Look in this file" is weaker than "this function violates this invariant, affecting these dependencies, so test this behavior."

### 13. What ideas are steal-worthy?

Make localization outputs structured and actionable. Separate location explanation, root cause, solution idea, dependencies, and testing impact. Evaluate handoff artifacts by downstream task success and token savings. Add contamination controls for public-code benchmarks. Treat low-quality external findings as potentially harmful, not just noisy.

### 14. Final decision

**Keep it.** This is not a universal code-repair solution, and the SWE-Bench contamination caveat is real. But the diagnostic-localization interface is exactly the kind of agent handoff object worth preserving.
