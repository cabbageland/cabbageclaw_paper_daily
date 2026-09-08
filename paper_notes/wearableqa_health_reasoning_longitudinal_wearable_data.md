# WearableQA: A Benchmark for Health Reasoning over Real-World Wearable Data

## Basic info

* Title: WearableQA: A Benchmark for Health Reasoning over Real-World Wearable Data
* Authors: Ji Soo Lee, Xilun Chen, Pierce Chuang, Ashish Shenoy, Jason Wei, Dohwan Ko, Hyunwoo J. Kim, Benoit Corda
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2609.05405
* Date surfaced: 2026-09-08
* Why selected in one sentence: It tests whether models compute over noisy personal wearable histories rather than merely reciting health priors.

## Quick verdict

* Strong adjacent paper

I inspected the full arXiv HTML text, especially the benchmark construction, dual-grounding procedure, model comparisons, input-representation analysis, tool-use experiment, and time-series ablations. This earns a preserved note because it cleanly separates health interpretation from longitudinal data computation.

## One-paragraph overview

WearableQA is a benchmark of 4,084 ten-option questions grounded in longitudinal records from 200 real users. Each user has up to 500 days of wearable measurements, plus blood biomarkers, demographics, and cohort-relative context. The benchmark separates data reasoning from health reasoning and single-signal from cross-signal reasoning across 16 question types. Its most useful result is that current models struggle to compute from personal measurement histories, and that giving an agent Python access helps far more than reformatting the same time series as CSV, Markdown, or plots.

## Model definition

### Inputs
Wearable time-series records, demographics, blood biomarker panels, cohort references, and multiple-choice questions.

### Outputs
One of ten answer options, scored by exact match.

### Training objective (loss)
There is no new trained model. WearableQA is a benchmark and analysis suite.

### Architecture / parameterization
The benchmark taxonomy crosses two axes: data versus health reasoning and single-signal versus cross-signal reasoning. The construction uses literature-grounded physiological findings and statistically validated population-grounded patterns.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It asks whether LLMs can reason over a real person's longitudinal wearable record, not just answer static medical questions or synthetic time-series puzzles.

### 2. What is the method?
Construct deterministic multiple-choice questions from real wearable records using a dual-grounding framework: peer-reviewed physiological relationships plus cohort-validated empirical patterns.

### 3. What is the method motivation?
Wearable health assistants need both computation over noisy personal data and physiological interpretation. Existing benchmarks usually test one side weakly or use simulated signals.

### 4. What data does it use?
The benchmark uses 200 real users with up to 500 days of daily measurements, including heart rate, sleep, activity, heart-rate variability, 17 blood biomarkers, demographics, and cohort-relative context.

### 5. How is it evaluated?
Fourteen proprietary and open-weight models are evaluated with chain-of-thought and direct-answer prompting. The paper also tests input serialization formats, plots, explicit Python tool access, positional bias, prior reliance, and time-series ablations.

### 6. What are the main results?
Overall accuracy ranges from 19.6% for Llama-3.2-3B to 72.9% for Gemini-3.1-Pro against a 10% chance baseline. Claude Opus 4.6 reaches 60.2%, while the strongest open model, Gemma-4-26B-A4B, reaches 42.5%. Most models perform better on health reasoning than direct data reasoning; cross-signal questions remain hard. For GPT-5.4, changing text formats barely helps, but Python access raises overall accuracy from 51.2% to 71.3%. Removing all wearable time series drops Claude Opus 4.6 from 60.2% to 17.3%, confirming the benchmark depends on the measurements rather than answer-position shortcuts alone.

### 7. What is actually novel?
The novelty is the benchmark object: real-user longitudinal wearable reasoning with a taxonomy that can separate computation failure from health-interpretation failure.

### 8. What are the strengths?
The benchmark is diagnostic, has real measurement noise, includes blood and demographics, balances answer positions, and explicitly tests whether computation tools help.

### 9. What are the weaknesses, limitations, or red flags?
It is still multiple choice and uses a limited 200-user sample. The clinical meaning of benchmark accuracy should not be inflated into safe health-assistant deployment.

### 10. What challenges or open problems remain?
Open questions include free-form longitudinal health reasoning, calibrated uncertainty, personalization, privacy-preserving evaluation, and real clinical outcome validation.

### 11. What future work naturally follows?
Build tool-using health agents that compute over personal timelines, expose their data dependencies, and distinguish prior medical knowledge from user-specific evidence.

### 12. Why does this matter for cabbageland?
It is a clean example of an agentic reasoning bottleneck: the system needs structured access to measurements, not prettier prompt serialization.

### 13. What ideas are steal-worthy?
Separate data reasoning from domain interpretation. Use ablations that remove history versus window data. Compare text formatting against actual computational tool access. Control answer-position bias before trusting multiple-choice results.

### 14. Final decision
Keep as an adjacent preserved note. It is not a method paper, but the benchmark is useful for thinking about evidence-grounded personal agents.

## 6. Mandatory critical angles

The evidence is strongest when the paper shows that tool access changes performance and that withholding time-series data collapses accuracy. The main caution is not to mistake a multiple-choice benchmark for clinical deployment readiness.

## 7. Writing style

Tone should be interested but skeptical. The benchmark is worth keeping because it finds a real reasoning gap, not because it solves health AI.

## 8. Repository output format

Saved as a preserved paper note because longitudinal personal-data reasoning is a durable evaluation lens for agent systems.
