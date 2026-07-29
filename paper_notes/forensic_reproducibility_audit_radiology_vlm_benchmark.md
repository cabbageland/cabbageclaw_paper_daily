# Forensic Reproducibility Audit of a Radiology Vision-Language Model Benchmark: From Intended Protocol to Released Artifact

## Basic info

* Title: Forensic Reproducibility Audit of a Radiology Vision-Language Model Benchmark: From Intended Protocol to Released Artifact
* Authors: Mateusz Kozlowski
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.25589
* Date surfaced: 2026-07-29
* Why selected in one sentence: It turns benchmark integrity into an explicit contract over prompts, pixels, measurements, and release artifacts instead of treating reproducibility as a vibes problem.

## Quick verdict

**Must keep**

This is one of the best recent evaluation papers because the method is not another checklist. It reconstructs a broken benchmark end to end, shows exactly where identity was lost, and proposes machine-verifiable clauses that would have failed the release before bogus claims escaped. I inspected the full arXiv HTML paper, especially the conceptual framework, results, claim-disposition ledger, and benchmark-contract sections.

## One-paragraph overview

The paper audits an archived chest-radiograph vision-language-model benchmark rather than proposing a new model. Its core move is to treat a benchmark result as a chain of state transitions: intended protocol, executed runtime bindings, preserved outputs, keyed measurements, and released artifacts. The authors then show that the audited benchmark lost identity at multiple points: nominally different prompts collapsed to the same executed prompt, some images were rendered with the wrong polarity, cohort identity drifted, outputs were missing or truncated, matched statistics were reconstructed from the wrong unit, and corrected values failed to propagate cleanly into public artifacts. The payoff is a fail-closed benchmark contract that binds cohort membership, prompt hashes, rendered inputs, model identity, annotation provenance, keyed analysis, and release checks.

## Model definition

### Inputs
The inputs are preserved code, prompt definitions, DICOM metadata, rendered images, output files, analysis scripts, manuscript tables and figures, and released repository artifacts from an existing benchmark.

### Outputs
The outputs are an adjudicated ledger of which artifact facts remain supportable, which scientific claims must be withdrawn, and a proposed machine-verifiable benchmark contract.

### Training objective (loss)
There is no predictive training objective here. The work is an evidentiary audit plus a contract design for future benchmark releases.

### Architecture / parameterization
The paper's main structure is a six-state view of computational results plus an eight-clause benchmark contract. The contract covers cohort identity, pixel identity, prompt identity, model identity, output completeness, annotation provenance, keyed analysis, and derived-artifact propagation.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to solve the gap between what a benchmark paper says happened and what the preserved artifact chain actually supports. In other words, it asks how a benchmark can look numerically tidy while still failing to identify the experiment it claims to report.

### 2. What is the method?
The method is a forensic audit of one benchmark plus a formalized contract for future ones. The audit traces prompt routing, input rendering, cohort identity, output completeness, label extraction, statistical reconstruction, and release propagation; the contract translates those failure modes into explicit checks.

### 3. What is the method motivation?
The motivation is that benchmark failures are usually treated as isolated mistakes when many of them are really identity failures across transitions. If prompt hashes, image renderings, or analysis keys are not bound and preserved, the final table may no longer describe the named condition even when the arithmetic is locally consistent.

### 4. What data does it use?
It uses an archived local project snapshot and the public repository record of a chest-radiograph VLM pilot benchmark. No new model calls were made and no new clinical annotations were created.

### 5. How is it evaluated?
It is evaluated by reconstructing the benchmark artifact chain. The audit inspects runtime prompt bindings, DICOM headers and patient aliases, report-file completeness, truncation in the automated extractor, matched statistical units, and propagation into manuscript and repository artifacts. Claims are then classified as supported artifact facts, corrected arithmetic, or withdrawn scientific claims.

### 6. What are the main results?
The nominal benchmark planned 300 model-prompt calls, but only 297 yielded nonempty reports. Sixty Claude calls labeled A and B were actually executed with the same C prompt. The 30 studies corresponded to 28 patients, not 30 independent cases, and four undocumented MONOCHROME1 images were rendered without the required polarity inversion. Reconstructing the keyed comparison changed the historical Cochran statistic from 154.73 to 182.29 and changed the number of Holm-adjusted nominally significant McNemar comparisons from 18 out of 45 to 20 out of 45, but the paper still withdraws the original benchmark claims because the prompt estimand and input identity were already broken.

### 7. What is actually novel?
The novelty is not finding arithmetic bugs. It is turning benchmark validity into an explicit state machine with contract clauses that can fail closed before release. The paper also cleanly separates artifact facts from scientific claims, which many reproducibility discussions blur.

### 8. What are the strengths?
The strongest part is the discipline of the audit. The paper does not pretend that corrected arithmetic rescues an invalid experiment. It also treats build and release propagation as first-class scientific concerns instead of "ops" trivia, which is exactly right for modern benchmark work.

### 9. What are the weaknesses, limitations, or red flags?
This is a single deep case study, not a prospective validation across many benchmark families. The contract is partially implemented with synthetic fixtures rather than fully proven in live future studies. Also, because the benchmark is already broken, the paper cannot show that the proposed contract is sufficient to prevent every important semantic mistake.

### 10. What challenges or open problems remain?
The big open problem is how to standardize this level of artifact binding without making benchmark pipelines too brittle or laborious for ordinary labs. Another open issue is how much of the contract can be generalized when closed APIs, non-preservable provider metadata, or sensitive clinical data limit what can be stored and released.

### 11. What future work naturally follows?
The obvious next step is prospective deployment of the contract on live multimodal benchmark pipelines, ideally outside radiology too. It would also be useful to build reusable tooling that automatically emits prompt hashes, input-render hashes, keyed analysis manifests, and release propagation checks by default.

### 12. Why does this matter for cabbageland?
It matters because cabbageland keeps building systems where the failure hides in transitions, not just in model weights. This paper is a direct reminder that if prompts, rendered inputs, runtime identities, and release artifacts are not tied to the claim, then evaluation can silently become fiction.

### 13. What ideas are steal-worthy?
Treat benchmark outputs as stateful artifacts with identity, not just rows in a table. Bind prompt conditions to immutable text and hashes. Key analyses on the real comparison unit rather than positional truncation. Add derived-artifact checks so a corrected source cannot leave stale public figures or model names behind. Most of all, separate "the file exists" from "the scientific claim is supportable."

### 14. Final decision
**Keep it.** This is a high-signal methods paper about evaluation integrity, artifact truthfulness, and fail-closed release discipline.
