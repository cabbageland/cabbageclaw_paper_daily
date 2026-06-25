# Project Auto-World: Towards Automated Benchmarking of Neural Relational Reasoners

## Basic info

* Title: Project Auto-World: Towards Automated Benchmarking of Neural Relational Reasoners
* Authors: Anirban Das, Joanne Boisson, Irtaza Khalid, Sumita Garai, Steven Schockaert
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.24965
* Date surfaced: 2026-06-25
* Why selected in one sentence: It uses LLM-generated programs to discover hard relational-reasoning instances whose difficulty is not explained by the usual hand-designed metrics.

## Quick verdict

* Highly relevant

This is a strong evaluation and data-generation paper for neural-symbolic reasoning. I inspected the full arXiv PDF, especially the Datalog world setup, FunSearch-style priority-function evolution, auto-research agent loop, Edge Transformer training, NoRA and Iron Coast experiments, unexplained-difficulty analysis, and limitations. The paper is not proof that autonomous research is solved; it is evidence that LLM-written generators can expose hidden benchmark dimensions that static metrics miss.

## One-paragraph overview

Project Auto-World asks whether LLMs can automate the construction of difficult benchmark instances for neural relational reasoners. Given Datalog world rules and constraints, the system learns samplers that generate small knowledge graphs and queries that challenge an Edge Transformer evaluator. The main approach adapts FunSearch: an LLM writes Python priority functions for adding graph edges, the evaluator's failure rate scores the functions, and evolution improves the sampler. The paper also tests a single coding-agent auto-research loop and direct Claude-generated samplers. The generated instances reveal forms of difficulty beyond inference depth, off-path edge count, and backtrack load; one discovered axis is inferred off-path edges, where an edge needed for the derivation is itself entailed rather than directly present.

## Model definition

### Inputs

The sampler receives Datalog world rules, constraints, a partial knowledge graph, and candidate triples that could be added. The reasoning evaluator receives graph queries of the form `(G, h, t, ?)` and must predict the set of relations that hold between two entities. The LLM generator receives prior priority functions, evaluation artifacts, and prompts that ask it to improve the sampler.

### Outputs

The LLM outputs Python priority functions or sampler programs. These functions output scores for candidate graph edges, inducing generated worlds and queries. The Edge Transformer outputs multi-label relation predictions for head-tail entity pairs. The evaluation outputs exact-match accuracy and unexplained-difficulty scores.

### Training objective (loss)

The Edge Transformer is trained with multi-label binary cross-entropy over relation labels. The LLM-written priority functions are not trained by gradient descent; they are selected by evolutionary fitness, where fitness is based on how poorly the current reasoning model performs on generated queries. The SuperET model is trained on a mixture of original NoRA splits and generated hard examples.

### Architecture / parameterization

The reasoner is an Edge Transformer, chosen because it is strong for relational reasoning and can in principle capture expressive logical formulas. The generator is a program-synthesis loop: FunSearch-style evolutionary search over Python priority functions, a separate coding-agent loop that iteratively edits one priority function, and direct dialogue-generated samplers from Claude Opus 4.6. Experiments also compare LLM backbones such as Qwen3-Coder-Next, gpt-oss-120b, and DeepSeek-Coder-33B for priority generation.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Neural relational reasoners are usually evaluated by hand-designed difficulty metrics such as inference depth, off-path edge count, and backtrack load. But those metrics can miss the actual structures that make a model fail. The paper tries to automate benchmark construction so the evaluator itself helps reveal what is difficult.

### 2. What is the method?

The main method learns graph samplers. A sampler builds a world one edge at a time by scoring candidate triples with a priority function. An LLM proposes or edits priority functions; generated worlds are scored by how much they challenge a trained Edge Transformer. Over rounds, the sampler evolves, the reasoner can be retrained on generated hard cases, and the process repeats. A separate auto-research setup lets a coding agent inspect artifacts and iteratively write new priority functions.

### 3. What is the method motivation?

If a benchmark only tests known difficulty axes, models can look systematically competent while failing on unmeasured structures. LLM-written generators are useful here because the output is a program that can be executed and verified, not a free-form ungrounded benchmark item. That keeps the LLM in a search/generation role while exact logical evaluation supplies the score.

### 4. What data does it use?

The primary domain is NoRA 1.1, a family-relationship reasoning benchmark with Datalog rules and constraints. The paper also uses an LLM-generated world called Iron Coast to test whether the approach transfers to novel rules. Generated worlds are deliberately small, capped at up to eight entities, so difficulty cannot be dismissed as just graph size.

### 5. How is it evaluated?

The paper evaluates exact-match relation prediction on generated queries. It cross-evaluates models trained on different sampler outputs, tests whether SuperET trained on mixed hard sources resists future samplers, and measures how much query difficulty remains unexplained by known metrics. It also tests whether adding a new metric, Off-Path Entailed Edge Count, reduces unexplained difficulty.

### 6. What are the main results?

The evolved and Claude-generated samplers produce hard queries that do not transfer cleanly across sampler families, suggesting they expose different failure modes. SuperET, trained on a broad mixture of generated and existing hard cases, resists the standard evolutionary loop better than the base Edge Transformer. But the auto-research sampler still challenges it. The unexplained-difficulty analysis shows that generated queries often remain hard for reasons not captured by depth, OPEC, or backtrack load. Adding inferred off-path edges as a feature reduces unexplained difficulty, supporting the claim that the samplers discovered a real missing axis.

### 7. What is actually novel?

The novelty is using executable LLM-generated samplers as benchmark-discovery tools for relational reasoning, then analyzing the discovered failures to name new difficulty metrics. This is better than simply asking an LLM to invent benchmark questions because the generated graph/query pairs are grounded in Datalog rules and exact labels.

### 8. What are the strengths?

The paper has a good closed loop: generate, evaluate, retrain, generate again, then analyze what changed. It also avoids treating one sampler as universal by cross-evaluating sampler families. The inferred-off-path-edge analysis is the most valuable part because it converts a discovered adversarial pattern into an interpretable difficulty axis.

### 9. What are the weaknesses, limitations, or red flags?

The scope is still narrow: Datalog worlds, a specific Edge Transformer evaluator, and small graphs. It is unclear how much the learned priority functions transfer to other rule sets or models. The auto-research language is a bit grander than the evidence; the agent is useful as a program search loop, not an independent scientist. Some Claude-generated generic samplers produced nonsensical worlds and had to be omitted, which is a reminder that constraints and validators are doing real work.

### 10. What challenges or open problems remain?

The biggest open question is model transfer. A sampler that breaks an Edge Transformer may be discovering a genuine reasoning difficulty, or it may be exploiting that model's quirks. Another challenge is extending beyond monotonic Datalog to negation, disjunction, uncertainty, and richer world dynamics without letting invalid generated items pollute the benchmark.

### 11. What future work naturally follows?

Run the same generator against multiple reasoning architectures and only promote difficulty axes that transfer. Use discovered sampler programs as a source of candidate benchmark metrics, then validate those metrics on fresh domains. Also, close the loop with human-readable explanations for why generated instances are hard, so the benchmark does not become an opaque adversarial generator.

### 12. Why does this matter for cabbageland?

Cabbageland cares about mechanisms that expose structure rather than decorate it. Auto-World is a useful pattern for evaluation: if you do not know which structures make a model fail, build a generator that searches for them, then name the discovered axis. That is directly relevant to world models, agent memory, and symbolic/latent hybrids where existing benchmarks often test the wrong proxy.

### 13. What ideas are steal-worthy?

Use LLMs to write executable adversarial data generators, not just items. Score generators by downstream model failure, then analyze generated failures into interpretable metrics. Retrain on discovered hard cases and rerun the generator to find residual blind spots. Keep generated worlds small so difficulty has to come from structure rather than size.

### 14. Final decision

**Keep it.** This is a good benchmark-generation paper with real transferable machinery. Its strongest lesson is that model-aware data generators can discover hidden difficulty axes, but those axes still need post-hoc interpretation and cross-model validation before they become science rather than adversarial overfitting.
