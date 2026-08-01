# ORCA-bench: How Ready Are Language Model Agents for Oncall?

## Basic info

* Title: ORCA-bench: How Ready Are Language Model Agents for Oncall?
* Authors: Albert Gong, Kyuseong Choi, Abhineet Agarwal, Jason Schechner, Ryan Huang, Raj Agrawal, Anish Agarwal, Raaz Dwivedi
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.28545
* Date surfaced: 2026-08-01
* Why selected in one sentence: It is a sharp reality check on coding-agent deployment claims because it measures diagnosis over real telemetry interfaces, source code, and ambiguous incident reports rather than frozen bug-fix tasks.

## Quick verdict

**Keep**

I inspected the arXiv PDF, especially the benchmark comparison table, construction pipeline, difficulty ladder, scoring setup, and headline failure rates. The paper's best move is to make the task operationally realistic in the right ways rather than cosmetically complicated. The main caveat is that the benchmark still lives on one public system, so its numbers are a lower bound on deployment difficulty, not a universal measure of oncall readiness.

## One-paragraph overview

ORCA-bench studies whether current language-model agents can actually do oncall root cause analysis. Instead of presenting a neat failing test or a single frozen repo issue, it gives agents a live OpenTelemetry-instrumented microservice system, real telemetry interfaces through Prometheus, Jaeger, and OpenSearch via Grafana, full source-code access, and ambiguous user-facing incident reports with variable specificity and detection lag. The benchmark contains 1,079 RCA tasks and human-curated plausible root causes plus verified symptoms. The result is grim but useful: even strong frontier agents perform poorly, hallucinate implausible causes, and degrade further when source-code access is removed.

## Model definition

### Inputs
The evaluated agents receive an incident report plus access to telemetry interfaces over metrics, logs, and traces, along with the corresponding source code.

### Outputs
The output is a root-cause analysis identifying all plausible root causes of the incident, which is then scored against expert-curated ground truth.

### Training objective (loss)
This is a benchmark paper rather than a new learning objective. Its contribution is the evaluation environment, task parameterization, and scoring protocol.

### Architecture / parameterization
The benchmark centers on a production-style microservice environment and a context ladder that varies report specificity, time-to-detection offset, and co-occurring fault scenarios. It evaluates general-purpose frontier agents rather than introducing a new agent architecture.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to measure whether modern LLM agents are actually ready for oncall diagnosis, where evidence is noisy, incomplete, distributed across telemetry and code, and framed by ambiguous user complaints rather than explicit failing tests.

### 2. What is the method?
The method is to build a production-fidelity RCA benchmark. Agents investigate a live telemetry stack plus source code under task settings that vary issue specificity and time-to-detection, and they are scored against plausible-root-cause sets validated by expert SREs.

### 3. What is the method motivation?
Software-engineering benchmarks are too clean for operational diagnosis. Real oncall work starts from messy symptoms, delayed reports, and multiple evidence channels. If evaluation ignores that, it overstates readiness.

### 4. What data does it use?
The benchmark uses a public microservice system with six days of telemetry data, roughly 50 GB of evidence, and 1,079 RCA tasks. It also includes a human-verified subset and human-rescored judge validation.

### 5. How is it evaluated?
It evaluates frontier agents on RCA accuracy, hallucination rate, and ablations such as removing source-code access. The paper also validates its LLM judge through human rescoring, reporting strong agreement.

### 6. What are the main results?
Across five frontier agents, the best RCA accuracy is only 25.3 percent on medium difficulty and 10.0 percent on hard tasks. Hallucination rates range from 7.2 percent to 40.2 percent. Removing source-code access hurts every metric.

### 7. What is actually novel?
The paper's novelty is not merely "another agent benchmark." It is the combination of real telemetry interfaces, source code, ambiguous user-facing reports, time-offset variation, plausible-root-cause scoring, and human-verified ground truth.

### 8. What are the strengths?
It makes the task harder in the right way. The benchmark captures evidence heterogeneity, operational ambiguity, and human verification better than most adjacent work. The hallucination metric is especially useful because wrong confident diagnosis is the real hazard here.

### 9. What are the weaknesses, limitations, or red flags?
The environment is still one public system, task isolation remains cleaner than real production, and even careful human verification cannot perfectly capture every operational nuance. It is a lower bound, not the full mess.

### 10. What challenges or open problems remain?
A major open problem is benchmarking across larger, more idiosyncratic systems and longer-lived incidents with organizational context, prior runbooks, and changing instrumentation. Another is agent calibration under deep uncertainty.

### 11. What future work naturally follows?
Future work should expand to multi-system settings, incorporate longer incident histories and team artifacts, and test whether agents can avoid hallucinated diagnoses through explicit uncertainty reporting.

### 12. Why does this matter for cabbageland?
It matters because cabbageland cares about agents that do real work, not just benchmark theater. ORCA-bench is a sober reminder that operational reasoning over live evidence is still much harder than patching a toy issue in a static repo snapshot.

### 13. What ideas are steal-worthy?
Benchmark against the real evidence stack. Vary ambiguity and time-offset explicitly. Score against sets of plausible causes rather than a single answer. Track hallucinated diagnoses as a first-class failure mode.

### 14. Final decision
**Keep it.** This is one of the cleaner reality-check papers in the current agent wave and worth preserving as a deployment calibration note.
