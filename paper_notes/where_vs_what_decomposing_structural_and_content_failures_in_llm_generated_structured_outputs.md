# Where vs What: Decomposing Structural and Content Failures in LLM-Generated Structured Outputs

## Basic info

* Title: Where vs What: Decomposing Structural and Content Failures in LLM-Generated Structured Outputs
* Authors: Yiwei Zhang, Chengke Wu, Li Wang, Jianqiang Li
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.25358
* Date surfaced: 2026-08-27
* Why selected in one sentence: It isolates a failure mode every JSON-heavy or tool-calling agent can suffer but most evaluations currently collapse into a single pass-fail score.

## Quick verdict

* Highly relevant

I inspected the full arXiv HTML text, especially the SCD formulation, the JSON and table experimental setup, the main results, the mechanistic ablations, and the SA-RLVR section. This paper earns a preserved note because it names a concrete failure mode that current structured-output evaluation mostly hides. The useful claim is narrow and real: models often know what values belong in the output, but fail on where those values belong.

## One-paragraph overview

The paper proposes Structure-Content Decomposition (SCD), a three-level evaluation framework for structured outputs: format validity, schema compliance, and value placement accuracy. It also adds Value Presence and Displacement Rate so the evaluator can detect the specific case where a model recalls the right values but binds them to the wrong structural addresses. The authors instantiate the framework on two different topologies, nested JSON generation and HTML table row modification, and show that structural placement degrades earlier than content recall as complexity rises. They then use SCD's decomposed metrics as verifiable rewards in GRPO, calling the training recipe SA-RLVR.

## Model definition

### Inputs
Structured-output prompts built from either generated JSON schemas with planted path-to-value mappings or HTML tables with designated row-cell replacements.

### Outputs
Generated JSON objects or modified table rows, plus decomposed metrics for format validity, schema compliance, value placement accuracy, value presence, and displacement rate.

### Training objective (loss)
For the diagnostic part there is no learned model. For SA-RLVR, the paper finetunes Qwen2.5-7B-Instruct with a verifiable reward `VPA + 0.3 * SCR`, using GRPO with LoRA.

### Architecture / parameterization
Two-part setup: an evaluation framework for decomposing structured-output errors, and an RL training recipe that uses those decomposed metrics as rewards for a 7B model.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the fact that current structured-output benchmarks usually collapse value errors and placement errors into one score, so they cannot tell whether a model failed to recall the right information or failed to bind it to the right structural location.

### 2. What is the method?
The method defines a hierarchy of metrics: format validity, schema compliance rate, and value placement accuracy, plus value presence and displacement rate for diagnosis. The same decomposition is applied to JSON trees and table grids, then the placement-aware metrics are used as verifiable RL rewards.

### 3. What is the method motivation?
If structured outputs are going to drive downstream execution, then "right value, wrong position" is not a cosmetic mistake. It is a distinct capability failure that needs its own measurement and possibly its own training signal.

### 4. What data does it use?
For JSON, it programmatically generates schemas with unified S, M, and L complexity levels, using recursive trees with 12, 15, and 20 planted values respectively. For tables, it synthesizes 4,490 instances from 53 real-world seed templates and 1,030 distinct layouts. For RL evaluation it also uses held-out JSONSchemaBench schemas and held-out table experiment types.

### 5. How is it evaluated?
It is evaluated across six models from 7B to frontier scale on JSON and table tasks at increasing structural complexity, with ablations on recursive depth, planted count, semantic cues, and path ambiguity, plus RL comparisons between base, SFT, and SA-RLVR.

### 6. What are the main results?
In high-complexity JSON, frontier models still misplace `24-35%` of recalled values, while Qwen2.5-7B misplaces `73.8%`. In tables, strong models still show displacement rates of `17-28%`, while Qwen2.5-7B reaches `98%`. Reasoning helps but does not remove the bottleneck: Qwen3-8B gets to `46.7%` displacement in JSON L and `21.9%` in table L. The RL follow-through is strong in JSON: SA-RLVR lifts JSON-ID VPA from `0.264` to `0.629`, OOD-Eco from `0.247` to `0.858`, and OOD-JSB from `0.795` to `0.968`, while matched SFT only reaches `0.281` on JSON-ID. On tables, RL mostly fixes formatting, not coordinate placement: FmtOK rises from `26.5%` to `85.5%`, but table VPA stays around `0.06-0.09`.

### 7. What is actually novel?
The actual novelty is not "structured output is hard." It is decomposing structure and content into separately measurable capabilities, then using the placement-aware piece as a verifiable training target.

### 8. What are the strengths?
The framework is clean, portable, and diagnostic. It reveals a failure mode that exact match, schema validity, and many end-to-end agent benchmarks blur away. The reward design is also disciplined: it excludes value presence from the reward so the model is not rewarded merely for mentioning the right values somewhere.

### 9. What are the weaknesses, limitations, or red flags?
The tasks are synthetic and carefully controlled, which is good for diagnosis but weaker for ecological realism. The table results also show that solving formatting does not solve structural addressing, so the training recipe still has a long way to go. One should not mistake clean synthetic gains for immediate real-world robustness.

### 10. What challenges or open problems remain?
Extending the decomposition to real API calls, messy schemas, semantically equivalent structures, partial outputs, and long multi-step agent traces. Another open problem is how to train placement robustness when the target structure is more ambiguous than these controlled tasks.

### 11. What future work naturally follows?
Placement-aware evaluation for function calling, tool traces, SQL generation, and config-file editing, plus reward designs that combine structural placement with execution-time correctness and uncertainty estimates.

### 12. Why does this matter for cabbageland?
Because cabbageland keeps depending on structured outputs, and "schema-valid" is not the same as "bound the right thing to the right slot." This paper gives a better failure vocabulary and a better evaluator.

### 13. What ideas are steal-worthy?
Always separate format validity, structural compliance, and value placement. Track displacement explicitly instead of calling everything an exact-match miss. Use placement-aware rewards when training models for JSON or table-like outputs.

### 14. Final decision
Keep as a preserved note. This is one of the better recent papers on structured-output reliability because it turns a vague annoyance into a measurable capability boundary.

## 6. Mandatory critical angles

The paper is strongest on evaluation fairness, mechanistic diagnosis, and reward design. It is weaker on ecological realism and on proving that the same patterns dominate messy real workflows, but it absolutely earns the core claim.

## 7. Writing style

The right tone is approving and severe. The paper is useful because it calls out a real benchmark blind spot and then operationalizes it cleanly.

## 8. Repository output format

Saved as a preserved paper note because the structure-versus-content split should transfer to future work on tool traces, JSON generation, and agent evaluation.
