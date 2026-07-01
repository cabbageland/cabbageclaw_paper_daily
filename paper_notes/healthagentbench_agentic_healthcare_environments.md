# HealthAgentBench: A Unified Benchmark Suite of Realistic Agentic Healthcare Environments for Challenging Frontier AI Agents

## Basic info

* Title: HealthAgentBench: A Unified Benchmark Suite of Realistic Agentic Healthcare Environments for Challenging Frontier AI Agents
* Authors: Qianchu Liu, Sheng Zhang, Guanghui Qin, Jeya Maria Jose Valanarasu, Maximilian Rokuss, Mingyu Lu, Timothy Ossowski, Juan Manuel Zambrano Chaves, Cliff Wong, Peniel Argaw, Yashna Hasija, Mu Wei, Wen-wai Yim, Qin Liu, Zilin Jing, Jason Entenmann, Naoto Usuyama, Tristan Naumann, Hoifung Poon
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.31179
* Date surfaced: 2026-07-01
* Why selected in one sentence: It pushes medical-agent evaluation from static question answering toward raw terminal environments with real clinical artifacts, tool use, search, and exact success criteria.

## Quick verdict

**Highly relevant**

This is a benchmark paper, but it is a useful one because it changes the unit of evaluation. The target is not "can a model answer a medical vignette"; it is "can an agent inspect messy clinical data and complete a workflow under verifier-grade constraints." I inspected the full arXiv PDF, including task construction, selection criteria, baseline results, category analyses, imaging discussion, and conclusion; confidence is high on the benchmark design and reported headline numbers, lower on the durability of the model leaderboard.

## One-paragraph overview

HealthAgentBench defines 54 terminal-based healthcare-agent tasks across seven categories: X-ray report correction, pathology tumor area selection, CT abnormality classification, clinical trial matching, EHR data quality auditing, EHR event modelling, and EHR format conversion. Each task gives the agent raw or semi-raw clinical artifacts and minimal instructions, then scores success with task-specific binary criteria based on expert labels, human baselines, exhaustive recall, or exact verifier checks. The paper evaluates 10 frontier agents and finds the suite far from saturated: the strongest reported setup, Codex GPT-5.5, reaches only about 42 percent success overall, while imaging and large-search compositional tasks remain especially difficult.

## Model definition

The paper introduces a benchmark suite, not a new healthcare model. The "models" under evaluation are external coding / tool-use agents.

### Inputs
Each task supplies a terminal environment with patient-grounded healthcare data. Inputs include 2D radiographs, 3D CT volumes, whole-slide pathology images, free-text clinical documents, clinical trial protocols, structured EHR tables, longitudinal EHR records, and supporting resources. Agents receive minimal instructions rather than step-by-step workflows.

### Outputs
Outputs vary by task: corrected radiology reports, CT abnormality labels, selected pathology tumor regions or tiles, eligible clinical-trial lists, identified EHR data-quality issues, trained event-prediction outputs, or converted EHR data formats that pass verifier checks.

### Training objective (loss)
There is no training objective. Evaluation uses task-specific binary success/failure criteria. Examples include all CT labels correct, all ETL verifier checks passing, full recall for data-quality and trial-matching tasks, no clinically significant report errors, tumor tile F1 above threshold, or AUROC matching a human-engineered baseline.

### Architecture / parameterization
The benchmark packages tasks as terminal environments using a containerized agent-evaluation style. Gold labels and verifier code are withheld from the agent container, identifiers are made opaque, web browsing is disabled for evaluated agents, and data is fetched on demand from original sources when credentials are available.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Most medical benchmarks are static, narrow, or already too easy for frontier models. They do not test whether an agent can navigate raw data, choose tools, decompose large search spaces, inspect medical images, query databases, write code, and produce exact outputs under clinical-like constraints.

### 2. What is the method?
The method is a suite of agent-native healthcare environments. The authors select tasks that require multi-step interaction, realistic clinical workflows, diverse modalities, and verifiable low-chance success. They convert existing healthcare resources and curated patient data into terminal tasks, apply anti-cheat design, and score each run through a separate verifier.

### 3. What is the method motivation?
Healthcare work is often not a single prompt. It requires inspecting large 3D volumes, gigapixel slides, longitudinal records, relational tables, and trial protocols. Agent evaluation should therefore measure the whole workflow: exploration, tool use, decomposition, exactness, and recovery from messy data.

### 4. What data does it use?
The suite spans 54 tasks across seven categories. It uses real clinical artifacts and patient-grounded data sources, including X-rays, CT, pathology whole-slide images, clinical text, trial documents, MIMIC-style structured EHR tables, and longitudinal EHR data. The paper emphasizes on-the-fly data download rather than redistributing protected data.

### 5. How is it evaluated?
Agents are run in terminal environments with disabled web access. Gold labels and verifier code are mounted only during verification. The main metric is overall task success rate, a fraction of benchmark tasks passed. The paper also reports task-specific metrics, costs, wall-clock time, and category-level analyses.

### 6. What are the main results?
The headline result is that the benchmark remains hard. Across 3 attempts on 54 tasks, Codex GPT-5.5 is reported as the strongest and most cost-effective agent at about 42 percent task success. Copilot CLI with Opus-4.8 and GPT-5.5 follow at about 36 and 35 percent, and Claude Code Opus-4.8 reaches about 32 percent. Imaging tasks are much harder than text tasks: averaged across Codex and Claude Code agents, imaging success is about 17 percent versus about 49 percent on text tasks. The best imaging setup, Codex GPT-5.5, averages only about 35 percent.

### 7. What is actually novel?
The novelty is the environment design, not a new medical model. HealthAgentBench makes medical-agent evaluation look more like real work: raw files, containers, tools, search, decompositions, exact verifiers, and heterogeneous outputs. Its anti-cheat and low-chance-success rules are also useful for future benchmark design.

### 8. What are the strengths?
The benchmark hits several important design marks: broad modality coverage, realistic workflow framing, objective verification, low random-guess probability, withheld labels, minimal instructions, and category-level diagnosis. It also exposes the specific gap between text-heavy tasks and imaging tasks, rather than compressing all healthcare capability into one number.

### 9. What are the weaknesses, limitations, or red flags?
The leaderboard is time-sensitive and harness-sensitive. The paper itself shows that agent harness choices can change performance, so the exact Codex / Claude / Copilot ranking should not be treated as a permanent model truth. The benchmark is also not exhaustive for healthcare deployment: it does not settle questions of clinical safety, prospective validation, privacy, calibration, clinician workflow integration, or liability.

### 10. What challenges or open problems remain?
The hard parts are specialized medical perception, large search spaces, compositional data auditing, and exact retrieval under messy criteria. Closing the imaging gap likely needs better tools or specialized medical vision backends, not just larger general-purpose agents. Clinical usefulness also requires uncertainty handling and clinician-facing interfaces that the benchmark does not evaluate.

### 11. What future work naturally follows?
Add more modalities and workflows, including ultrasound, genomics, medication reconciliation, longitudinal care plans, administrative prior authorization, and real-time clinician interaction. Report failure taxonomies beyond pass/fail. Evaluate agents with tool libraries designed for medical imaging and structured EHR query rather than generic terminal affordances alone.

### 12. Why does this matter for cabbageland?
Cabbageland should prefer environment-level evaluation over theatrical static prompts. HealthAgentBench is a reminder that agent competence lives in workflow details: finding the right data, choosing inspection tools, managing search, writing exact outputs, and satisfying a verifier.

### 13. What ideas are steal-worthy?
* Turn real workflows into terminal environments with exact verifiers.
* Use binary task success only when the success criterion is genuinely low-chance and near-expert.
* Hide labels and verifier code from the agent runtime.
* Keep instructions minimal so the benchmark tests strategy, not prompt following.
* Report modality-level gaps instead of hiding them behind an aggregate score.

### 14. Final decision
**Keep and cite.** This is a strong benchmark-design reference for realistic agent evaluation, especially where raw data and tool use matter more than polished answers.
