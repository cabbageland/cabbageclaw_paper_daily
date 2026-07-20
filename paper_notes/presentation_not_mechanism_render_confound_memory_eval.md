# Presentation, Not Mechanism: A Render Confound in Deprecation-Aware Memory Evaluation

## Basic info

* Title: Presentation, Not Mechanism: A Render Confound in Deprecation-Aware Memory Evaluation
* Authors: Zhaoyang Jiang, Zhizhong Fu, Zicheng Li, Yunsoo Kim, Jiacong Mi, Xuanqi Peng, Fei Teng, Honghan Wu
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.16019
* Date surfaced: 2026-07-20
* Why selected in one sentence: It shows that a supposedly better deprecation-aware memory architecture mostly wins because its rendered state is easier to read, not because the fine-grained mechanism adds real value.

## Quick verdict

**Must read**

This paper is sharper than most memory-eval work because it bothers to isolate the thing it claims to measure. The render-matched control is the whole point: once presentation is held fixed, most of the fine-ledger win disappears. I inspected the arXiv HTML sections covering the framing, the ESR formalization, benchmark construction, main ablations, and discussion.

## One-paragraph overview

The paper studies evidence-state revision: tasks where records revise themselves over time and a system must answer what is currently true, what got superseded, and when it should abstain. It compares three memory styles under the same task: a flat GraphRAG-like baseline without deprecation state, a coarse live/dead invalidation store, and a fine RevisionLedger with typed relations and unresolved status. The key result is that the apparent advantage of the fine ledger mostly comes from its structured render. When the authors create a render-matched control that keeps the same layout but disables the fine deprecation logic, nearly all of the gain remains. The real mechanism that pays is the coarse live/dead invalidation signal, not the extra typing.

## Model definition

### Inputs
The pipeline takes an evidence stream of timestamped events, extracted atoms keyed by entity and attribute, and a query asking for the current value or abstention under revision.

### Outputs
It outputs either an answer or an abstain decision, along with internal state representations such as current value, supporting evidence, deprecated evidence, and unresolved conflict status.

### Training objective (loss)
The paper does not train a new end-to-end model for the task. It uses frozen LLM-based extraction and judging components plus rule-driven state updates, so there is no standalone task loss beyond the frozen components' original pretraining.

### Architecture / parameterization
The compared systems are a `d`-blind GraphRAG+abstain baseline, a coarse edge-invalidation store with binary live/dead state, and a fine `RevisionLedger` with relation labels such as supersedes, refines, and unresolved contradiction.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to determine what memory machinery is actually needed for records that change over time, especially when prior claims are revised, reverted, or left unresolved.

### 2. What is the method?
The method is a controlled benchmark and ablation design. The authors define the evidence-state-revision task, build ESR-Bench, compare flat, coarse, and fine memory classes, and introduce a render-matched control that preserves the fine ledger's layout while disabling its fine-grained deprecation logic.

### 3. What is the method motivation?
The motivation is that many memory evaluations change mechanism and prompt presentation at the same time, then credit the mechanism for gains that may come from easier reading by the answer model.

### 4. What data does it use?
The main ESR-Bench version contains `2,907` QAs from GitHub issue histories, multi-repo issue histories, Wikipedia revisions, and a DyKnow-style temporal split. A stratified `N=150` subset is human validated.

### 5. How is it evaluated?
It is evaluated with semantic-correctness judgments, abstain calibration, rare-stratum analysis such as reverted-revert and cross-source conflict cases, paired bootstrap intervals, and an out-of-family secondary judge to test robustness of the decomposition.

### 6. What are the main results?
On reverted-revert items, `RevisionLedger` appears to beat the flat GraphRAG+abstain baseline by about `+0.182`, but the render-matched decomposition shows roughly `+0.159` of that is render effect and only about `+0.025` is fine-mechanism residual, which is indistinguishable from zero. The coarse live/dead invalidation mechanism is the one that produces a real gain, about `+0.087` over the render-matched control.

### 7. What is actually novel?
The novelty is not the ledger itself. It is the evaluation correction: hold render fixed, then ask whether the mechanism still wins.

### 8. What are the strengths?
The paper isolates variables cleanly, ties the memory choice to query sufficiency rather than vibes, and backs the argument with rare-stratum analysis instead of only aggregate averages.

### 9. What are the weaknesses, limitations, or red flags?
The study is mostly about current-state queries, not the full space of historical or faceted queries. It also depends on an extraction pipeline and LLM judges that can introduce their own noise, and some rare strata remain small.

### 10. What challenges or open problems remain?
The main open problem is extending the same discipline to richer query families where fine relation typing might actually matter, rather than assuming the current-state result generalizes automatically.

### 11. What future work naturally follows?
The obvious next step is to build revision benchmarks for history queries, facet-specific state, and provenance-sensitive explanations, then rerun the same render-controlled comparison.

### 12. Why does this matter for cabbageland?
Cabbageland cares about explicit state, honest evaluations, and not crediting architecture for UI sugar. This paper is a direct warning against benchmark self-deception in memory-heavy systems.

### 13. What ideas are steal-worthy?
Add render-matched controls to structured-memory evaluations. Choose the coarsest state that is sufficient for the query mixture. Retain invalidated evidence when prior-value or provenance questions may appear. Treat abstention as a first-class contract, not a polite failure case.

### 14. Final decision
**Keep it.** This is the kind of correction paper that saves future work from optimizing the wrong thing.
