# When Errors Become Narratives: A Longitudinal Taxonomy of Silent Failures in a Production LLM Agent Runtime

## Basic info

* Title: When Errors Become Narratives: A Longitudinal Taxonomy of Silent Failures in a Production LLM Agent Runtime
* Authors: Wei Wu
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.14589
* Date surfaced: 2026-06-15
* Why selected in one sentence: It turns long-running LLM-agent reliability into a mechanism-level postmortem taxonomy, with a concrete account of how errors become fluent false output.

## Quick verdict

* Highly relevant

This is a single-system case study, not population-level evidence, but it is one of the most useful agent-reliability papers in the scan because the unit of analysis is right: silent-failure mechanisms and observation paths. I inspected the full arXiv PDF, including the system context, taxonomy, representative incidents, cross-cutting findings, defense framework, discussion, and threats to validity. I did not audit the public repository or postmortem corpus, so the numeric counts should be treated as paper claims rather than independently verified facts.

## One-paragraph overview

The paper studies eight weeks of silent failures in a production personal-assistant LLM agent runtime with roughly 40 scheduled jobs, 8 LLM providers, a memory plane, 4,286 unit tests, and 827 declarative governance checks. Across 22 documented incidents, it derives five mechanism classes: environment/platform quirks, design-assumption mismatches, error swallowing and dilution, chained hallucination/fabrication, and operational omission or forensic blind spots. The strongest contribution is the analysis of "fail-plausible" failures, where polluted context or fake success-shaped output gets transformed into fluent user-facing narrative. The paper's practical lesson is severe: tests and audits encode the past, but agent failures often live in seams between components, so durable defenses need meta-rules, mechanized scanners, sabotage validation, declared-state convergence, context hygiene, and user-view observation.

## Model definition

### Inputs
This is not a new trained model paper. The studied system receives scheduled job inputs, user conversations from messaging surfaces, tool results, knowledge-base notes, alerts, logs, runtime state, and external data pulled into synthesis jobs.

### Outputs
The runtime outputs user-facing messages, digests, alerts, tool-call results, memory updates, status files, governance reports, and postmortems. The paper outputs a taxonomy and defense framework rather than a predictive model.

### Training objective (loss)
No new model is trained as the method. The paper describes off-the-shelf LLMs used inside the production runtime and an AI collaborator used in engineering/postmortem drafting, but there is no optimization objective for the paper's contribution.

### Architecture / parameterization
The studied runtime is a systems stack: a control plane with tool governance, declarative checks, SLO monitoring, and convergence machinery; a capability plane routing across LLM providers; and a memory plane with knowledge-base/RAG indexing and synthesis jobs. The research artifact is a mechanism-oriented incident taxonomy plus a defense framework, not a neural architecture.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Long-running LLM agents can fail without crashing, without tripping tests, and without sending an actionable alert. Worse, because the system speaks, an upstream error can be converted into fluent, plausible output that looks like a normal success to the human recipient.

### 2. What is the method?
The paper performs a longitudinal case study over 22 production incidents, each closed with a structured postmortem protocol. Incidents are classified by mechanism rather than by file or subsystem. The analysis then extracts cross-cutting patterns: silence latency, discovery channel, trigger/amplifier/concealer structure, recurrence under shallow fixes, and the maturation path from point fix to meta-rule to scanner.

### 3. What is the method motivation?
Location-based failure labels do not transfer. A path bug, parser bug, stderr/stdout leak, or alert-routing bug matters because of the failure mechanism it instantiates. If the mechanism is named and mechanized, future unrelated locations can be protected.

### 4. What data does it use?
The corpus is every completed postmortem between 2026-04-09 and 2026-06-02 that reached production, had a silent phase, and was closed under the postmortem protocol. The system is described as a single macOS-hosted personal-agent runtime with roughly 40 scheduled jobs, 8 LLM providers, 3 supervised services, 4,286 unit tests, and 22 published incident postmortems.

### 5. How is it evaluated?
This is evaluated as an empirical systems case study. Evidence consists of incident counts, silence durations, discovery channels, taxonomy stability over later incidents, retrospective audit scoring, and whether added meta-rules/scanners blocked recurrence. The paper also reports sabotage validation as a way to test whether guards actually fire.

### 6. What are the main results?
The paper reports five silent-failure classes and at least 28 manifestations of the meta-pattern "an error signal existed somewhere but never reached a human in actionable form." Roughly 70% of silent failures were ultimately discovered by human user-view observation rather than automated checks. A retrospective audit over 15 incidents had 0% ex-ante prevention, 13% partial early warning, and 87% ex-post regression blocking. Silence latency ranged from 13 hours to 60 days and tracked observational distance more than code complexity.

### 7. What is actually novel?
The cleanest novelty is the fail-plausible class: LLM systems do not merely hide errors; they can narrativize them into plausible false output. The second valuable novelty is the trigger/amplifier/concealer decomposition as an operational postmortem contract. The third is the framing of audits as regression engines rather than prediction engines.

### 8. What are the strengths?
The paper is concrete, uncomfortable, and systems-literate. It understands that reliability work needs causal chains, not vibes. The examples are mechanically specific: stdout pollution into command substitution, stale alerts contaminating chat context, status files lying about LLM success, reserved control files muting the agent, and forensic tools silently denied by the same sandbox they were trying to inspect.

### 9. What are the weaknesses, limitations, or red flags?
The study is one system, one operator pair, one host OS, and eight weeks. Classification was performed by the system operators without independent annotation, so there is no inter-annotator agreement. The corpus only includes failures that were discovered and closed with postmortems, so still-silent failures are necessarily missing. The author used an AI collaborator in operating the system and drafting the paper, which is disclosed but still raises narrative-bias risk. The exact frequencies should not be treated as general constants.

### 10. What challenges or open problems remain?
Mechanizing user-view judgment remains hard. Audits can regress against known classes, but novel silent failures still require observation, adversarial review, and target-environment exposure. The paper also leaves open how to generalize these mechanisms across larger teams, different operating systems, less attentive users, and multi-tenant agent products.

### 11. What future work naturally follows?
Independent replication across other agent runtimes, shared incident schemas for LLM-agent postmortems, benchmarkable sabotage suites for agent observability, and automated user-view observers that can detect low-information or fabricated outputs without becoming another unvalidated LLM component.

### 12. Why does this matter for cabbageland?
Cabbageland is exactly the kind of long-running agent context where a green test suite is not enough. The paper says to design for loud failure, provenance hygiene, read-only observers, declared-state convergence, and mechanized checks for mechanism classes. It also says to trust the user's eye as a real observability signal, not as an embarrassing fallback.

### 13. What ideas are steal-worthy?
Use trigger/amplifier/concealer in every serious postmortem. Promote point fixes into named meta-rules. Mechanize meta-rules as repository-wide scanners. Sabotage-test every guard. Keep alerts out of normal chat context. Treat summaries and digests as high-risk because they can turn polluted context into confident narrative. Prefer seam reduction over defense accretion.

### 14. Final decision
Keep and cite. Do not overgeneralize the percentages, but preserve the mechanism taxonomy. The paper is especially useful as a design checklist for personal agents, scheduled LLM jobs, and memory-bearing runtimes that push fluent output to humans.
