# Can a Language Model Learn Facts Continually in Its Weights?

## Basic info

* Title: Can a Language Model Learn Facts Continually in Its Weights?
* Authors: Charles O'Neill
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.11020
* Date surfaced: 2026-07-14
* Why selected in one sentence: It cleanly separates weight-based storage from question-keyed access and shows why later writes break continual factual learning even when the fact is still in the model.

## Quick verdict

**Must read**

This is the clearest recent paper I have seen on why post-training weight updates are such a shaky substrate for durable factual memory. The paper does not just show forgetting. It shows that a model can still store the effect of a fact in its weights while losing the retrieval path that makes the fact operationally usable. I inspected the full arXiv HTML paper, including the abstract, introduction, measurement setup, data-breadth experiments, sequential writing results, access-versus-storage analysis, capability-drift analysis, discussion, and limits.

## One-paragraph overview

The paper studies whether a language model can keep learning facts in its weights after training in a way that accumulates rather than collapses. It writes invented facts into Qwen3 models, then follows what happens after twenty to one hundred later writes. The key finding is that later training often destroys access before it destroys storage. Broad study-style training data creates more usable facts than bare statements and keeps them alive longer, but even those facts eventually become hard to reach after subsequent writes. Forgotten facts often recover once the fact is supplied in context, which leads to the paper's central claim: the weights may still hold the content, but the question routing that reaches it has drifted away. For anything that must remain retrievable and composable through future updates, context remains the reliable memory channel.

## Model definition

### Inputs
The experiments feed the model invented facts, training sets of either bare factual statements or broader study-style paraphrases and exercises, and held-out questions probing recall, entailment, reversal, and multi-step use. Some conditions also provide the fact in context as a reference ceiling.

### Outputs
The model outputs next-token completions to factual and reasoning questions, plus token probabilities that let the paper measure whether a forgotten fact still leaves a storage trace in the model.

### Training objective (loss)
The main write operations are supervised next-token training updates, usually implemented with LoRA adapters. The paper also evaluates context-distillation variants and KL-regularized recipes, but there is no single new loss that solves accumulation.

### Architecture / parameterization
The main experiments use Qwen3-4B with LoRA writes, with an 8B replication for part of the entailment-gap analysis. The paper is about the behavior of weight updates and evaluation probes rather than about a new model architecture.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It asks whether a language model can keep learning discrete facts in its weights after training without those facts becoming brittle, inaccessible, or destructive to previously learned content.

### 2. What is the method?
The method is a controlled writing-and-follow-up protocol. The author writes invented facts into the model using different training-data recipes, then measures immediate usability, retention after many later writes, conflict under new facts, access versus storage after forgetting, and collateral damage to unrelated abilities.

### 3. What is the method motivation?
Much of the continual-learning story for LLMs quietly assumes that if a fact can be written once, then enough regularization or better training will let many such facts accumulate. This paper tests that assumption directly instead of relying on one-step factual recall as a proxy for durable memory.

### 4. What data does it use?
It uses invented facts, question sets designed to probe different types of factual use, repeated sequential-write experiments, prior-conflict evaluations, and capability tests against a frozen base reference. The facts are synthetic by design so the interference pattern is controlled.

### 5. How is it evaluated?
The evaluation measures the recitation-to-use gap after a write, retention after twenty to one hundred later writes, sensitivity to conflicting later facts, recovery when forgotten facts are supplied in context, the persistence of storage traces through log-probability probes, and the relationship between retention loss and KL drift from the original model.

### 6. What are the main results?
Broad study-style data is much better than bare statements at creating usable written knowledge. It reduces the recitation-to-use gap from `27.4` points to `5.4` points and after twenty later writes retains about `46%` strict accuracy versus `1%` for bare-statement facts. But no tested intervention keeps earlier facts reliably reachable under continued writing. Forgotten facts often still carry the storage trace of the original write and recover to `77-80%` when the fact is reintroduced in context. Capability loss tracks KL divergence from the base model, while long-horizon reachability remains unsolved.

### 7. What is actually novel?
The novelty is not just another forgetting curve. The paper distinguishes storage from access and argues that many later-write failures are routing failures rather than literal erasure. The phrase "stored but question-keyed" is the key conceptual contribution.

### 8. What are the strengths?
The study asks the right question, uses a clean controlled setup, and produces a memorable mechanistic conclusion rather than a vague empirical warning. It also avoids the cheap win of declaring success when the same fact can still be recited right after a write.

### 9. What are the weaknesses, limitations, or red flags?
The experiments mostly use one model family, invented facts, and LoRA-style write operations. The paper is about discrete factual accumulation, not skill learning. Some causal and storage probes are necessarily narrow, and the access-versus-storage tests are run at a small number of operating points rather than across many scales and architectures.

### 10. What challenges or open problems remain?
The big open problem is preserving reachability under many later writes. The paper suggests that broad study data can improve what a write creates and frozen-teacher distillation can reduce general capability damage, but neither solves long-horizon factual accumulation in weights.

### 11. What future work naturally follows?
The obvious next steps are cross-family replications, extensions from discrete facts to reusable skills, and architectures or external-memory schemes that explicitly preserve retrieval pathways instead of only constraining parameter drift.

### 12. Why does this matter for cabbageland?
Cabbageland cares about durable agents, memory systems, and continual adaptation. This paper is a clean warning that weight updates are a dangerous thing to treat as primary memory. If the knowledge must survive later changes and remain composable on demand, context or explicit external memory is still the safer system of record.

### 13. What ideas are steal-worthy?
Measure access and storage separately. If you must write weights, use broad study-style data rather than bare statements. Treat capability preservation and fact reachability as distinct problems. Assume weight memory is a cache unless you have a stronger guarantee than this paper could find.

### 14. Final decision
**Keep it.** This is one of the clearest papers I have seen on why post-training weight writes are not yet a trustworthy substrate for durable factual memory.
