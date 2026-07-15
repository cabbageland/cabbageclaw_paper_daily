# GRID: Grammar-Railed Decoding for Enterprise SQL Generation

## Basic info

* Title: GRID: Grammar-Railed Decoding for Enterprise SQL Generation
* Authors: Mohsen Arjmandi
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.11951
* Date surfaced: 2026-07-15
* Why selected in one sentence: It turns grammar, role policy, and schema validity into exact decoding constraints with explicit guarantees and unusually honest systems boundaries.

## Quick verdict

**Must read**

This is the sort of systems paper I want more often: explicit invariants, measured hot paths, and clear statements about what the method cannot do. The useful move is keying the decoding mask on live parser configuration plus lexer state, rather than on token history, so exactness and caching can coexist. I inspected the full arXiv HTML paper, including the abstract, preliminaries, viable-prefix oracle, token-terminal bridge, guarantees, evaluation, limitations, and conclusion.

## One-paragraph overview

GRID is a grammar-constrained decoding system for SQL that tries to solve the actual deployment problem rather than the demo version. It compiles three things into the constrained language: the SQL grammar itself, a role projection that bans forbidden verbs or clauses, and schema lexicons that restrict identifiers to what the database actually contains. The next-token mask is computed from the current LALR parser stack plus lexer scan state, not from raw token prefixes, and a byte-level trie bridges tokenizer tokens to grammar terminals exactly. That yields a deterministic decoder with provable syntax and schema-validity guarantees, near-constant hot-path cost, and an explicit checker-guided repair step for the parts the mask cannot prove, especially column-level alias binding.

## Model definition

### Inputs
The system takes the current generated prefix, the live parser and lexer configuration induced by that prefix, the SQL grammar, a role-specific production subset, schema-specific identifier lexicons, and the external language model's token vocabulary and logits.

### Outputs
GRID outputs an exact next-token mask, constrained SQL continuations, and an auditable replay trace of per-token decisions. In checker-guided mode it also emits specific semantic violations for one constrained retry.

### Training objective (loss)
The paper does not introduce a new trainable model or loss. It studies inference-time constrained decoding around an external language model and evaluates correctness, latency, and serving behavior.

### Architecture / parameterization
The operative system is a deterministic stack: an incrementally advanced LALR(1) parser acting as the viable-prefix oracle, a contextual lexer, a byte-level token trie, configuration-keyed cache layers, Rust kernels for the hot path, and an optional semantic checker for out-of-mask residue. The underlying LM is unchanged.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to make enterprise SQL generation provably syntactic, policy-compliant, and schema-valid at decode time, while staying fast enough for real serving.

### 2. What is the method?
The method computes exact next-token masks from parser configuration rather than token-sequence tables. It compiles role policy and schema lexicons into the language, uses a byte-level trie to map tokenizer tokens onto grammar terminals, and adds a semantic checker plus one constrained repair pass for the semantic residue the mask cannot enforce.

### 3. What is the method motivation?
Prompted SQL generation is brittle in exactly the ways enterprise use cannot tolerate: invalid syntax, invalid identifiers, role violations, and weak auditability. The paper wants those guarantees to live in the decoding interface rather than in model goodwill.

### 4. What data does it use?
The main evaluation uses the full Spider dev set with per-database lexicons, a 315-schema MaskBench sample for JSON-style grammar stress tests, latency harnesses against XGrammar, llguidance, and Outlines, and vLLM-style serving experiments.

### 5. How is it evaluated?
It is evaluated on per-token latency, flat-cost scaling, MaskBench compile and runtime behavior, Spider execution accuracy, batched serving behavior, policy enforcement, and audit replay and tamper detection.

### 6. What are the main results?
The mask hot path reaches about `3.6` to `6.7` microsecond median latency and beats llguidance at p50 and p90 on the reported tokenizers, though llguidance keeps the flattest p99 tails. On Spider, the mask is worth `+13` execution-accuracy points for the `0.5B` model (`16.0%` to `29.0%` EX) and a smaller but real gain at `7B`, where checker-guided repair lifts EX from `53.7%` to `55.2%`. The audit trail also replays exactly on the reported test and flags tampering rather than hand-waving it.

### 7. What is actually novel?
The novelty is not "use grammars for SQL." It is the configuration-keyed exact mask, policy compiled into the language, and a system that states its guarantees with explicit preconditions instead of pretending semantic correctness falls out automatically.

### 8. What are the strengths?
The paper is rigorous about invariants, honest about boundaries, and system-minded in the right places. It measures both correctness and hot-path cost, and it explicitly handles the checker residue rather than burying it.

### 9. What are the weaknesses, limitations, or red flags?
The guarantees stop at the mask's actual scope. Column-level RBAC is not solved at parse time. The first version is limited to LALR(1)-parsable languages. Cold specialization and cold trie walks still have tail costs, and the method does not claim distribution-faithful sampling.

### 10. What challenges or open problems remain?
The main unresolved pieces are semantics outside the grammar boundary, support for non-LALR grammars, and further reduction of cold-start serving costs without losing the explicit guarantees.

### 11. What future work naturally follows?
Natural follow-ups are Earley-style fallback for harder grammars, tighter handling of column-level policy, and broader application of the same contract-compiled decoding idea to other structured tool languages.

### 12. Why does this matter for cabbageland?
This is a direct lesson for tool-using agents. If a constraint matters, compile it into the action interface instead of hoping a prompt or reward model will keep the policy honest. The paper is especially relevant for tool calling, structured outputs, and agent authorization boundaries.

### 13. What ideas are steal-worthy?
Key decoding state on parser configuration, not raw token prefixes. Compile policy into the formal language when possible. Treat checker-guided repair as an explicit residue handler, not as an excuse to weaken the main guarantees. Publish honesty boundaries alongside performance numbers.

### 14. Final decision
**Keep it.** This is a genuinely useful systems paper about making structured generation exact where exactness actually matters.
