# Reclaim Evaluation: A Lossy Memory Is Worse Than an Empty One

## Basic info

* Title: Reclaim Evaluation: A Lossy Memory Is Worse Than an Empty One
* Authors: Alex Kwon
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.25449
* Date surfaced: 2026-06-25
* Why selected in one sentence: It turns agent memory into a correctability interface and shows that keeping a stale conclusion while dropping the source can be worse than keeping no memory at all.

## Quick verdict

* Must read

This is the most cabbageland-relevant paper in today's scan. I inspected the full arXiv PDF, especially the reclaim protocol, paired memory policies, deployed-memory tests, MultiWOZ replication, memory-loop cascade, and limitations. The paper is strong because the mechanism is simple and falsifiable: a memory note either preserves the answer-determining source, or it preserves a conclusion that may become an attractor for future error.

## One-paragraph overview

The paper studies whether compressed language-model memory remains correctable after an earlier interaction drifted to a wrong answer. Its key protocol, reclaim evaluation, compresses a drifted interaction under matched-budget memory policies and later gives a correction that names the error without supplying the answer. A lossy memory keeps the salient wrong conclusion and drops the recomputable source; a source-first memory keeps the source and drops the re-derivable conclusion. On arithmetic, logic, deployed memory systems, and MultiWOZ slot recovery, source-first memory preserves correction while lossy memory often turns a recoverable error into a confident stale answer. The useful point is not "store everything"; it is "do not store conclusions in place of the evidence needed to repair them."

## Model definition

### Inputs

The evaluation inputs are drifted interactions with known ground-truth answers, a compressed carried memory note, and a later correction. The memory note is constructed under policies such as lossy, source-first, lossy-padded, blank, and source-first-auto. The paper also tests deployed memory systems including running summaries, fact extraction, and naive vector retrieval over session turns.

### Outputs

The answering model emits a recovered answer, a stale wrong answer, a novel wrong answer, or an abstention. The harness reports Reclaim Rate, wrong-emission behavior, attractor reuse, source presence, and cascade blast radius in chained memory loops.

### Training objective (loss)

There is no new trained model objective in the core contribution. The paper defines an evaluation protocol and memory-writing policies. The underlying LLMs are used as memory writers, readers, or answerers; source-first-auto is a prompt-level compression policy rather than a learned objective.

### Architecture / parameterization

The main apparatus is a paired-memory evaluation harness. It controls memory budget, source retention, correction type, and session boundary. The policy contrast is deliberately simple: lossy keeps the conclusion, source-first keeps the recomputable source, and lossy-padded controls for length by adding neutral filler without adding the source.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It asks when compressed agent memory remains correctable. A normal summary can preserve the answer-like surface while deleting the evidence that would let a later model repair the answer. For long-running assistants and agents, that is worse than ordinary forgetting because the memory can actively attract future behavior toward the old error.

### 2. What is the method?

The method is reclaim evaluation. First, induce or observe a wrong commitment on a task with a known answer. Second, compress the interaction into a fixed-budget memory note. Third, start a later session with only that carried memory and give a correction that names the error locus but not the answer. Fourth, score exact recovery against ground truth.

The core comparison is between memory policies. Lossy memory keeps a stale conclusion and drops source facts; source-first memory keeps the recomputable facts and drops the conclusion; lossy-padded proves that the gain is not just more text.

### 3. What is the method motivation?

The paper is attacking a bad default in memory design: summaries are optimized to preserve salient takeaways, but correctability often depends on the working, not the takeaway. If the conclusion was wrong, preserving it is a liability unless the source survives beside it.

### 4. What data does it use?

The paper uses synthetic arithmetic and constraint-logic tasks with objective answers, deployed-memory reproductions, and a MultiWOZ dialogue slot-recovery setting. The arithmetic and logic tasks are controlled so source presence can be checked exactly. MultiWOZ tests whether the same effect appears in messier real task-oriented dialogue.

### 5. How is it evaluated?

The main metric is Reclaim Rate: whether the later correction recovers the true answer. The paper also measures whether a failed reclaim returns the inherited stale value, a new wrong value, or abstains. The deployed-system section swaps memory systems and answerers, and the memory-loop section tracks how many downstream hops become wrong after one dropped-source error.

### 6. What are the main results?

On arithmetic wall cells, lossy and lossy-padded sit at 0.00 Reclaim Rate when the source has been dropped, while source-first reaches roughly 0.99 to 1.00 in the same budget regime for the base models. A blank memory can be safer than a wrong-valued memory: in the reported arithmetic wall test, blank memory causes abstention while lossy memory makes models emit confident wrong values. Three deployed memory systems wall below source-first, each for a different reason: the summary drops the source, extraction buries it under generated figures, and naive retrieval misses the source-bearing turns. In chained memory loops, a single lossy error spreads across later hops and becomes uncorrectable, while source-first only holds until the source outgrows the fixed budget.

### 7. What is actually novel?

The novelty is the correctability framing and the matched-budget source-versus-conclusion test. The paper does not merely say summaries can omit details. It shows a behavioral inversion: a memory that kept a wrong answer can be worse than an empty memory because it removes the reason to abstain and supplies an attractor.

### 8. What are the strengths?

The strongest part is the control design. The paper separates anchoring from information loss, controls for note length, uses exact scoring rather than a judge, and states the boundary of the fix. It also tests memory as a loop, not only as a one-hop recall artifact. That matters for agents, where yesterday's memory becomes tomorrow's input to a new memory.

### 9. What are the weaknesses, limitations, or red flags?

The guarantee depends on a compact identifiable source. The paper is honest about diffuse-evidence settings where the answer-determining source cannot be isolated at write time. Some headline behavior is model- and decoding-dependent: whether a source-less model abstains or emits a wrong value varies by model and task. The source-first-auto prompt is materially weaker than the oracle source-first note, so the clean policy is easier to define than to deploy.

### 10. What challenges or open problems remain?

The main open problem is source locating. A memory writer has to know which facts are recomputable source, which are derived conclusions, and whether the preserved source is complete. Another open problem is memory under diffuse evidence: qualitative judgments, long code investigations, and scientific claims often lack a small source string that can simply be carried forward.

### 11. What future work naturally follows?

A useful next step is a memory regression test for agent frameworks: induce known drift, compress under the framework's real memory policy, deliver a correction, and score exact reclaim. Another is source-completeness tagging for notes, so partial source-first memory fails loudly instead of confidently summing an incomplete source. For coding agents, the analogous test would preserve failing logs, diffs, and reproduction commands rather than preserving only "root cause: X."

### 12. Why does this matter for cabbageland?

Cabbageland keeps caring about state that remains useful under correction, not just state that sounds informative. This paper gives a clean rule for long-running agents: memory should preserve the evidence needed for future repair. A stale conclusion without the source is not memory; it is a delayed bug report written as fact.

### 13. What ideas are steal-worthy?

Use reclaim rate as a memory-system metric. Store source before conclusion when the conclusion can be recomputed. Add completeness tags when budget truncates source evidence. Test memory policies under later corrections, not just recall. In agent handoff notes, preserve the observations and commands that generated a conclusion, especially if the conclusion is uncertain.

### 14. Final decision

**Keep it.** This is a compact, high-value mechanism paper for agent memory. The key lesson is brutal and portable: if future correction matters, preserve the source of truth, not just the answer-shaped residue.
