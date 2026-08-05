# TraceCompiler: Skill-Guided Mining and Compilation of LLM Agent Traces into Mostly Deterministic Workflows

## Basic info

* Title: TraceCompiler: Skill-Guided Mining and Compilation of LLM Agent Traces into Mostly Deterministic Workflows
* Authors: Salma El Yadouni, Guanyi Li
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.02680
* Date surfaced: 2026-08-05
* Why selected in one sentence: It is the sharpest direct agent-systems paper in today's batch because it treats recurring trace reuse as a compilation problem and only admits workflow edges that can be justified by attributable value flow.

## Quick verdict

**Must read**

I inspected the arXiv HTML paper, especially the problem definition under partial observability, argument-level dependency verification, provenance typing, the compiler skill, the Venmo and Spotify/Todoist case studies, and the execution-focused limitations. The paper is strong because it refuses both replay and vibes: it compiles only what can be evidenced, marks ambiguous relations as suspected rather than pretending they are hard constraints, and correctly refuses to compile underdetermined irreversible behavior. The main caveat is scope. The paper demonstrates two recurring intents and explicitly does not claim net efficiency because offline compilation cost is not measured.

## One-paragraph overview

TraceCompiler starts from a useful observation: agent traces mix reusable procedure with accidental execution history. The reusable part includes genuine tool dependencies, stable configuration, value transformations, and branch conditions. The accidental part includes retries, exploratory detours, schema lookups, and stylistic ordering. The system clusters traces by intent, denoises behavior, and then applies a conservative dependency rule: keep an edge only when a consumer argument contains a value uniquely attributable to an earlier producer and no alternative source explains it. Bindings are typed as constants, user inputs, copied outputs, transforms, or residual LLM decisions. The result is an executable mostly deterministic workflow that compiles away evidence-backed decisions while leaving genuinely open choices to the model or the human.

## Model definition

### Inputs
The input is a set of agent traces containing system context, user request, execution events, tool names, structured arguments, optional outputs, exceptions, metadata, and sometimes missing observability about tool returns.

### Outputs
The system outputs intent clusters, denoised workflow graphs, evidence tuples for hard dependencies, typed bindings, and an executable workflow IR with only residual open choices left as LLM or human nodes.

### Training objective (loss)
There is no end-to-end learned compiler loss that defines the paper. The main implementation is a frozen compiler skill plus a mechanized dependency rule, evaluated against labeled dependency references and execution outcomes.

### Architecture / parameterization
The pipeline has five main parts: unsupervised intent discovery, normalization and behavioral denoising, argument-level dependency verification, provenance and static-context handling, and workflow compilation plus validation. The first implementation is a versioned LLM skill rather than a newly trained neural model.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the fact that tool-using agents repeatedly rediscover procedures they have already executed, but naive replay or process mining preserves retries, accidental order, and fake dependencies.

### 2. What is the method?
The method clusters noisy traces by recurring intent, removes accidental behavior, verifies dependencies at the argument level by excluding alternative value origins, types the remaining bindings, and compiles the result into a mostly deterministic executable workflow.

### 3. What is the method motivation?
Observed adjacency is not a safe proxy for causality in agent traces. Structured arguments expose provenance clues that ordinary event-order mining throws away, and partial observability makes the compiler's job conservative by design.

### 4. What data does it use?
The main evaluations use the T1 corpus for labeled producer-consumer dependency recovery and AppWorld trajectories for replay-based token attribution and workflow execution checks.

### 5. How is it evaluated?
It is evaluated on dependency precision and recall against reference labels, token-edge precision on AppWorld replay, call reduction, leave-one-out execution on withheld instances, and an important negative test where the compiler should refuse compilation.

### 6. What are the main results?
On T1, the mechanized dependency rule reaches 0.928 precision and 0.943 recall over 15,775 def-use edges, versus about 0.711 F1 for both adjacency and a directly-follows baseline. The compiler skill run blind reaches 0.992 precision on 250 audited edges. On a recurring Venmo money-request intent, the compiled workflow reduces 34 observed API calls to 11 runtime calls and passes 15 of 21 leave-one-out state tests. On the Spotify/Todoist case, the compiler correctly refuses to compile because the irreversible side effect is underdetermined by the observed traces.

### 7. What is actually novel?
The novelty is not merely workflow reuse. The key move is dependency admission by exclusion of alternative origins, with explicit evidence tuples for hard edges and abstention through suspected relations when proof is insufficient.

### 8. What are the strengths?
The paper uses the right unit of analysis, value flow instead of event order. It is explicit about partial observability, treats refusal as a success mode, and reports corrections forced by its own execution harness rather than pretending the pipeline is cleaner than it is.

### 9. What are the weaknesses, limitations, or red flags?
The execution case studies are still small. Offline compilation cost is not measured, static-context injection is specified more than demonstrated, and some evaluation machinery such as AppWorld replay is partly self-consistent with the rule rather than fully independent.

### 10. What challenges or open problems remain?
The big open problems are scaling from a few recurring intents to messier enterprise traces, handling richer branching with sparse observation, and deciding when a compiled workflow should be re-audited as tools or schemas change.

### 11. What future work naturally follows?
More robust compile-time branch discovery, stronger authorization around irreversible side effects, and live monitoring of drift between compiled workflows and new traces would all be natural next steps.

### 12. Why does this matter for cabbageland?
It matters because cabbageland keeps building and evaluating agents that rediscover the same procedures. This paper offers a disciplined path from traces to reusable workflows without pretending that event order or high-level summaries are enough.

### 13. What ideas are steal-worthy?
Only keep hard dependencies with attributable value evidence. Distinguish hard edges from suspected edges instead of forcing both into the same graph. Type bindings explicitly. Treat refusal to compile as a legitimate outcome when irreversible behavior is underdetermined.

### 14. Final decision
**Keep it.** This is a direct systems paper with an auditable mechanism, honest failure modes, and a design lesson that transfers cleanly to agent workflow tooling.
