# Pretraining Data Can Be Poisoned through Computational Propaganda

## Basic info

* Title: Pretraining Data Can Be Poisoned through Computational Propaganda
* Authors: Victoria Graf, Hannaneh Hajishirzi, Noah A. Smith, David Kohlbrenner, Kyle Lo
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.15267
* Date surfaced: 2026-07-19
* Why selected in one sentence: It traces poisoning through actual web-corpus pipeline stages instead of stopping at the webpage-injection story.

## Quick verdict

**Highly relevant**

This is one of the better recent data-poisoning papers because it models the path from attack surface to corpus inclusion instead of pretending that visible webpage injection is the same thing as model training exposure. The key artifact is HalfLife, a pipeline-level inclusion estimate. I inspected substantial arXiv HTML sections covering the threat model, HalfLife decomposition, public-comment and ad analyses, controlled model-scaling results, and synthetic-rewrite appendix summaries.

## One-paragraph overview

The paper studies whether adversarial text placed through third-party web interfaces can survive crawling, text extraction, and quality filtering strongly enough to matter for language-model pretraining. Its central tool, HalfLife, decomposes poison inclusion into injectability, capture by the crawler/extractor, and survival through curation. The empirical claim is that public discussion interfaces, unlike programmatic ads, provide a real scalable route into web corpora. The paper then runs controlled model experiments showing that when such poison is included, it can shift both pretrained and instruction-tuned completions, even when the poison looks more like ordinary prose than like an obvious synthetic trigger string.

## Model definition

### Inputs
The analysis takes an attack vector such as public comments or ads, sampled webpages, crawler and text-extraction behavior, quality-filtering rules, and poisoned documents used in controlled training experiments.

### Outputs
It outputs estimated poison-inclusion probabilities for specific pipeline/vector combinations and measured shifts in downstream model behavior under controlled poisoned pretraining.

### Training objective (loss)
HalfLife itself is not a learned model. The paper's learned-model part is the controlled scaling study, where pretrained and instruction-tuned language models are trained on corpora containing different levels of poison.

### Architecture / parameterization
The architecture is a probabilistic pipeline analysis plus controlled training experiments. HalfLife models inclusion as a product of injection, capture, and not-filtered probabilities, and the paper contrasts different poison formats and vectors under that lens.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to solve the gap between "I can inject text onto the web" and "that text actually enters a modern pretraining corpus and changes model behavior."

### 2. What is the method?
The method is HalfLife: estimate poison inclusion through the full pipeline, compare attack vectors, and then validate practical impact with controlled poisoned pretraining experiments.

### 3. What is the method motivation?
Previous pretraining-poisoning work often focused on narrow sources like Wikipedia or ignored how much injected content is removed before training. This paper argues the survival stage is the real missing variable.

### 4. What data does it use?
The analysis uses Common Crawl-derived webpages and open-data pipeline assumptions related to corpora such as Dolma, DCLM, and FineWeb, plus controlled pretraining experiments on models from `65M` up to `1.3B` parameters.

### 5. How is it evaluated?
It is evaluated by pipeline-stage survival estimates, concrete vector comparisons between public comments and programmatic ads, poison survival under WRAP-style synthetic rewriting, and downstream completion shifts in poisoned models.

### 6. What are the main results?
The estimated inclusion probability for public-comment poisoning is about `0.13%`, which is enough to exceed the effective Wikipedia slice (`0.067%`) in a modern corpus mix. The paper argues that poisoning `100k-1M` webpages could already be enough to reach the `n=250` poisoned-document regime previously shown sufficient for pretraining attacks. Programmatic ads largely fail to survive scraping, while belief-manipulation poison survives WRAP-style paragraph rewriting at `65.3%`. In controlled model experiments, poison shifts both base and instruction-tuned generations, though instruction tuning retains less of the effect as model size grows.

### 7. What is actually novel?
The novelty is not just the attack vector. It is the insistence on modeling post-injection survival through crawling, extraction, and filtering, plus the comparison showing that some seemingly scalable vectors die before the corpus while others do not.

### 8. What are the strengths?
The paper treats the data pipeline seriously, distinguishes viable from non-viable vectors, and avoids equating webpage visibility with training-data inclusion. The synthetic-rewrite analysis is also useful because it separates naturalistic poison from obviously brittle trigger strings.

### 9. What are the weaknesses, limitations, or red flags?
The downstream model experiments are still much smaller than frontier pretraining. The pipeline analysis also depends on proxy assumptions about curation stacks and crawl behavior, so exact inclusion rates may move across different corpora or closed pipelines.

### 10. What challenges or open problems remain?
The hard open problem is provenance-aware filtering at web scale. Document-level quality filters are not designed to distinguish primary authored content from user-injected fragments.

### 11. What future work naturally follows?
Future work should test more realistic closed-pipeline settings, quantify attack cost under different moderation regimes, and develop extraction or filtering defenses that explicitly reason about third-party content channels.

### 12. Why does this matter for cabbageland?
Cabbageland cares about long-lived data pipelines, model grounding, and safety at the infrastructure layer. This paper is a reminder that corpus provenance is part of model security, not a boring preprocessing footnote.

### 13. What ideas are steal-worthy?
Model attack viability through the whole pipeline, not just the initial surface. Treat provenance and third-party content boundaries as first-class. Compare vectors empirically instead of assuming the most scalable-looking one survives extraction.

### 14. Final decision
**Keep it.** The threat model is practical enough to matter, and HalfLife is a reusable way to reason about corpus-poisoning surfaces.
