# Theoria: Rewrite-Acceptability Verification over Informal Reasoning States

## Basic info

* Title: Theoria: Rewrite-Acceptability Verification over Informal Reasoning States
* Authors: Michael Saldivar, Ben Slivinski
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.01223
* Date surfaced: 2026-07-02
* Why selected in one sentence: It turns informal reasoning verification into local checks over licensed state transitions, making hidden premises visible as unlicensed mutations.

## Quick verdict

**Highly relevant**

Theoria is valuable because it identifies the right intermediate artifact: not a confidence score, not a free-form critique, but a proof witness made of typed state rewrites. The empirical story is narrower than the framing might suggest, because the current judges are still LLMs and the main benchmark is small. I inspected the full arXiv PDF, including the rewrite formalism, architecture, calibration discussion, HLE / GPQA results, adversarial tests, limitations, and conclusion; confidence is high on the witness-format idea, lower on the absolute reliability of the current implementation.

## One-paragraph overview

Theoria verifies candidate answers by rewriting them into an initial state and a sequence of state transitions. Each transition must be licensed by exactly one justification type: citation, computation, or problem-given evidence. The central invariant is completeness of change: every semantic difference between consecutive states must be accounted for by the stated license, so hidden assumptions become visible as unlicensed state mutations. Specialized LLM judges audit the initial state and each typed step, while a pedantry filter and convention lift handle over-strict or standard-convention objections. The paper reports high-precision certified buckets on HLE-Verified Gold and GPQA Diamond, plus stronger detection of hidden premises and fabricated citations in poisoned proofs, but it is best read as a verifier-format paper rather than a solved verification product.

## Model definition

Theoria is a verification architecture built from a solver, formalizer, specialized judges, filters, and bounded repair loops. It does not introduce a new trained model.

### Inputs
The pipeline receives a problem statement and a candidate natural-language solution. The formalizer constructs an initial state and a sequence of typed transitions. Judges receive the problem, previous state, next state, justification type, evidence, and full proof context where needed.

### Outputs
The system outputs either `judge-passed` / certified with an auditable proof trace, or declined. Certified traces contain the initial state, each transition, the justification type, the evidence, and any explicit convention-lift assumptions.

### Training objective (loss)
There is no training loss. Theoria is evaluated by coverage, strict certified precision, favorable certified precision under adjudication, certified-versus-declined asymmetry, matched-coverage comparison to holistic judges, error overlap, adversarial poisoned-proof detection, and out-of-distribution GPQA Diamond certification.

### Architecture / parameterization
The architecture is solve, formalize, judge, filter, and repair. A solver proposes an answer. A formalizer rewrites it into a proof witness: `S0` plus steps `(S_i, tau_i, e_i)`. Specialized judges audit computation, citation, problem-given, and initial-state checks. A pedantry filter overrides only when every enumerated issue is cosmetic. A convention lift can add a standard citable assumption when it fully resolves a rejection. Failed verdicts can trigger bounded repair or final decline.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
The paper targets the gap between formal proof assistants and scalar LLM judges. Formal verification is strong when the problem is formalized correctly, but much real reasoning remains informal and semantic. Scalar judges cover more cases but produce opaque scores that do not say which premise, computation, citation, or transformation was trusted. Theoria tries to create an auditable certificate for informal reasoning.

### 2. What is the method?
The method rewrites a solution into a state trajectory. Each step changes the current state and must be licensed by citation, computation, or problem-given evidence. The verifier asks a local question: does this license account for the entire observed change from the previous state to the next? If not, the answer is declined or repaired.

### 3. What is the method motivation?
Hidden assumptions are easy to smuggle through fluent prose. A holistic judge may miss them because it must reconstruct the whole argument. If every semantic mutation has to appear in a state diff and carry a license, hidden premises and fabricated citations become local, inspectable failures. This reduces exposure failure even though judge failure remains possible.

### 4. What data does it use?
The main evaluation uses 185 completed runs from a 200-problem random sample of HLE-Verified Gold text-only problems, with early harness-development problems excluded. It also evaluates 95 adversarial poisoned proofs across 15 domains and reports a smaller GPQA Diamond test with 65 problems. The solver baseline is web-augmented, which makes the filtering result more meaningful than a pure parametric-knowledge baseline.

### 5. How is it evaluated?
Theoria reports certified precision and coverage. On HLE-Verified Gold, two independent LLM graders judge final answer correctness. The paper compares against a solver-only baseline and holistic confidence judges at matched coverage, analyzes error overlap, performs cross-model adjudication on disputed certifications, tests poisoned proofs by error class, and evaluates GPQA Diamond certification.

### 6. What are the main results?
On HLE-Verified Gold, Theoria certifies 105 of 185 completed problems, for 56.8 percent coverage and 96/105 strict certified precision, or 91.4 percent with Wilson 95 percent CI [84.5, 95.4]. Favorable adjudication credits 105/105, but that claim depends on LLM-mediated dispute analysis and should be treated cautiously. The solver-only baseline is 83.8 percent accurate at full coverage; Theoria's certified bucket roughly halves the error rate. Holistic judges achieve statistically indistinguishable strict precision at matched coverage, but their error overlap with Theoria is low. In poisoned proofs, structured judging catches 94.7 percent versus 83.2 percent for holistic judging, with the advantage concentrated in hidden premises and fabricated citations.

### 7. What is actually novel?
The novelty is the witness format and the completeness-of-change invariant. Process supervision and LLM judges are not new, but Theoria asks judges to verify licensed state rewrites rather than global prose quality. The formal decomposition between exposure failure and judge failure is also useful: the architecture's claim is not that LLM judges become infallible, but that certain errors are forced into visible local checks.

### 8. What are the strengths?
The method has a real theory-to-evaluation loop. It predicts that hidden premises and fabricated citations should benefit most from structured rewriting, while arithmetic and theorem-misapplication errors get less format advantage; the poisoned-proof results follow that pattern. The certify-or-decline output is also product-relevant because it treats abstention as a first-class system behavior, not a confidence footnote.

### 9. What are the weaknesses, limitations, or red flags?
The implementation still relies on LLM judges with tools, not formal backends. Semantic diffing is judge-mediated rather than an explicit symbolic diff layer. The primary benchmark is one HLE subset with 185 completed problems, and GPQA Diamond has only 65 examples. The favorable precision number rests on LLM-mediated adjudication. Convention lifts are ad hoc and need a real registry. A prover optimized to fool Theoria's specific judges has not been tested.

### 10. What challenges or open problems remain?
The biggest challenge is reducing judge failure after exposure failure has been lowered. Computation steps should be discharged by CAS or SMT where possible; formalizable citation / theorem steps should connect to Lean or other proof systems; semantic diffs should be made explicit; and convention management needs source, domain, scope, and version metadata. Another hard problem is initial-state interpretation, where a wrong reading of the natural-language problem can survive even a correct derivation.

### 11. What future work naturally follows?
Attach formal backends to typed step classes, build explicit semantic-diff extraction, create public adversarial witness suites, evaluate on legal / scientific / engineering workflows, and combine Theoria with holistic judges as complementary filters because their error sets are different. For agent systems, a natural extension is tool-trace verification: every state mutation in an external workflow should carry a licensed observation, computation, or user-given premise.

### 12. Why does this matter for cabbageland?
Cabbageland agents often need to decide whether an answer, plan, or file edit is trustworthy enough to act on. Theoria suggests a better contract than "the model said it checked": represent the current state, require each mutation to cite its license, and decline when the trace cannot be made locally auditable.

### 13. What ideas are steal-worthy?
* Verify state transitions, not fluent final answers.
* Require every state change to be licensed by a typed evidence source.
* Treat hidden premises as unlicensed mutations.
* Separate exposure failure from judge failure when designing verifiers.
* Make decline a structural output, not an apologetic confidence score.
* Use formal tools for typed subcases when available, but keep an informal witness format for the rest.

### 14. Final decision
**Keep and reuse carefully.** Theoria is not a solved verifier, but its witness format is a strong design pattern for auditable reasoning and agent trace checking.
