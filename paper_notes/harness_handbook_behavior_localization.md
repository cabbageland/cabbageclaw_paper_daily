# Harness Handbook: Making Evolving Agent Harnesses Readable, Navigable, and Editable

## Basic info

* Title: Harness Handbook: Making Evolving Agent Harnesses Readable, Navigable, and Editable
* Authors: Ruhan Wang, Yucheng Shi, Zongxia Li, Zhongzhi Li, Yue Yu, Junyao Yang, Kishan Panaganti, Haitao Mi, Dongruo Zhou, Leoweiliang
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.13285
* Date surfaced: 2026-07-19
* Why selected in one sentence: It treats behavior localization as a first-class engineering bottleneck for coding agents instead of assuming file search and long context are enough.

## Quick verdict

**Must read**

This is one of the stronger recent agent-infrastructure papers because it isolates a real prerequisite problem and then measures the fix cleanly. The contribution is not "better repo summaries." It is a behavior-centric representation plus a staged navigation workflow that improves localization and edit planning while reducing token use. I inspected substantial arXiv HTML sections covering the abstract, representation, construction pipeline, BGPD workflow, core experiments, and quantitative result summaries.

## One-paragraph overview

The paper argues that evolving an agent harness fails first at behavior localization: a modification request says what behavior should change, but raw repositories only say where code is stored. Harness Handbook tries to bridge that gap by building an L1-L3 behavior-centric document tree plus a cross-stage state-register view, all linked back to source code. An agent then uses Behavior-Guided Progressive Disclosure (BGPD) to move from system-level behavior to component-level context to source-grounded implementation units. The authors evaluate whether that extra structure actually helps coding agents produce better edit plans on real harness-change requests.

## Model definition

### Inputs
The system takes the harness repository, natural-language modification requests, static-analysis artifacts about files/functions/state relationships, and source snippets that are reorganized into behavior-centric handbook entries.

### Outputs
It outputs a structured handbook of behavior-to-source mappings, candidate implementation sites for a requested behavior, and a higher-quality edit plan for the coding agent.

### Training objective (loss)
There is no learned task model introduced here. The pipeline combines static analysis with LLM-assisted behavioral structuring and then uses the resulting handbook to guide planning.

### Architecture / parameterization
The architecture has two load-bearing pieces: a three-level handbook representation plus a state-register view, and BGPD, a staged workflow that progressively narrows from high-level behavior to concrete implementation sites while revalidating those sites against the current repository.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to solve the gap between behavior-level change requests and implementation-level repository structure. Coding agents may find relevant files, but still miss scattered sites, rarely executed paths, or cross-module behavior.

### 2. What is the method?
The method is to build an explicit behavior-centric handbook for the harness, then use that handbook to guide planning through progressive disclosure instead of free-form repository wandering.

### 3. What is the method motivation?
Most repository aids remain implementation-centric. They organize information around files, modules, or indexes, while the edit request is behavior-centric. The paper says that mismatch is the real localization bottleneck.

### 4. What data does it use?
The evaluation uses diverse modification requests drawn from two open-source agent harnesses, with planning runs from Codex and Terminus-2 and reference comparisons against stronger models for localization scoring.

### 5. How is it evaluated?
It is evaluated with judged plan-quality win rates, localization precision/recall/F1 against reference plans at file and symbol granularity, zero-overlap failure analysis, and planner token-use comparisons.

### 6. What are the main results?
Handbook assistance raises overall judged win rate from `28.3%` to `38.3%` on Codex and from `26.7%` to `45.6%` on Terminus-2. Planner token use drops by `12.7%` on Codex and `8.6%` on Terminus-2. Across both harnesses and both granularities, localization F1 improves by `5.0` to `18.8` points, and complete localization failures drop by as much as `25.9` points.

### 7. What is actually novel?
The novelty is not another repo index. It is the explicit decision to represent runtime behavior as a first-class artifact linked to source and then force planning to walk through that artifact in stages.

### 8. What are the strengths?
The paper asks a real systems question, the mechanism is concrete, and the quantitative story is coherent: better localization, better judged plans, fewer catastrophic misses, and lower token cost rather than more brute-force context.

### 9. What are the weaknesses, limitations, or red flags?
The evidence still comes from only two harnesses. Handbook construction also depends on the quality of static analysis and LLM-assisted behavioral structuring, so some of the method's success rides on the artifact-generation step being good enough.

### 10. What challenges or open problems remain?
The big open problem is portability. It is still unclear how well the handbook idea transfers to messier production harnesses with weaker structure, more dynamic behavior, or heavier non-Python glue.

### 11. What future work naturally follows?
Natural follow-up work would test more harness families, stress the construction pipeline under noisier codebases, and study whether handbook maintenance can stay synchronized as repositories change rapidly.

### 12. Why does this matter for cabbageland?
Cabbageland cares about coding agents, explicit structure, and state that survives past the current prompt window. This paper offers a plausible artifact layer for repository memory that is behavior-native instead of file-native.

### 13. What ideas are steal-worthy?
Represent behavior explicitly. Separate system overview from component detail from source-grounded unit detail. Treat state-crossing edges as a first-class navigation object. Make localization a staged workflow instead of a raw search sprint.

### 14. Final decision
**Keep it.** The behavior-localization framing is strong, the measured gains are real, and the artifact design is reusable.
