# When Derived Measurements Mislead: Quantifying and Mitigating LLM Over-Trust with Privileged-Modality Reliability Evidence

## Basic info

* Title: When Derived Measurements Mislead: Quantifying and Mitigating LLM Over-Trust with Privileged-Modality Reliability Evidence
* Authors: Zongheng Guo, Tao Chen, Tianli Li, Mingzhe Cui, Yang Jiao, Lei Xie, Yi Pan, Xiao Hu, Manuela Ferrario
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.28421
* Date surfaced: 2026-08-02
* Why selected in one sentence: It names a neglected modular-systems failure, downstream LLM over-trust in upstream derived features, and gives a clean matched-versus-shuffled evaluation design for measuring whether reliability evidence actually survives the interface.

## Quick verdict

**Useful**

I inspected the arXiv HTML paper, especially the DFOT problem formulation, evaluation protocol, proof-of-concept case study, and result sections. The paper's strongest contribution is conceptual and evaluative rather than raw mitigation strength: it gives a reusable failure target and a metric chain for testing whether a downstream LLM uses an upstream estimate appropriately. The main caveat is that the proof-of-concept is narrow and the measured gains are modest, so this should be read as a rigorous interface benchmark more than a complete solution.

## One-paragraph overview

The paper studies what happens when a downstream language model treats an upstream derived measurement as if it were a direct fact. It calls this failure derived-feature over-trust, or DFOT. Using physiological sensing as a case study, the authors build a pipeline where ECG serves as privileged supervision to learn PPG-only reliability evidence, then test whether that reliability signal helps a downstream LLM avoid over-trusting a rhythm estimate. The key methodological move is matched-versus-shuffled evidence: if reliability evidence matters because it is specific to the current case rather than because it generically makes the model more cautious, matched evidence should help more than shuffled donor evidence.

## Model definition

### Inputs
The overall system takes raw physiological signals, derived rhythm estimates, patient context/history, and optional reliability evidence produced for the current case.

### Outputs
The upstream stack emits derived measurements plus reliability evidence; the downstream LLM emits a decision about whether to trust, verify, or revise the interpretation.

### Training objective (loss)
The proof-of-concept mitigation trains a PPG-only student to predict reliability using privileged ECG supervision during training. The paper does not frame the main contribution as a new end-to-end downstream loss, but as a measurement-and-mitigation protocol for the interface.

### Architecture / parameterization
This is a hybrid modular pipeline: an ECG teacher, a PPG-only reliability student, a structured reliability-evidence interface, and a frozen downstream LLM evaluated under matched and shuffled evidence conditions.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the case where an LLM over-trusts an upstream derived estimate whose validity is instance-dependent, using that estimate as if it were a direct observation.

### 2. What is the method?
The method is to define DFOT as an interface-level failure target, construct challenge tasks around contradictory and misleading contexts, introduce five evaluative estimands, and test a privileged-modality reliability signal as a proof-of-concept mitigation.

### 3. What is the method motivation?
Many modular AI systems compress uncertain upstream inference into a neat token or field. Once that happens, downstream language models can reason coherently from the wrong thing. The paper wants to measure that interface bug directly instead of calling it generic uncertainty.

### 4. What data does it use?
The case study uses 50,000 paired PPG-ECG records from 1,275 patients and evaluates on a protocol-locked 187-patient test set.

### 5. How is it evaluated?
The evaluation defines D1 and D2 challenge tasks, then measures conflict over-trust rate, context-induced error rate, correct repair rate, evidence-specific repair margin, and utility harm rate. The crucial design choice is matched case-specific evidence versus patient-disjoint shuffled evidence.

### 6. What are the main results?
On the locked test, the privileged reliability baseline improves four repair and specificity endpoints by 1.82 to 6.69 percentage points, with paired confidence intervals excluding zero. The utility harm rate increases by only 0.67 percentage points with a confidence interval spanning roughly -0.4 to +1.7. The matched-versus-shuffled design shows that some of the benefit is genuinely case-specific rather than generic caution.

### 7. What is actually novel?
The main novelty is defining DFOT as a reusable downstream evaluation target and coupling it to a matched-versus-shuffled evidence test that can distinguish specific evidence use from bland conservative behavior.

### 8. What are the strengths?
It identifies a real modular-systems failure that shows up far beyond medicine, gives a properly structured metric chain, uses a sharp control condition, and keeps the claims narrower than most "uncertainty-aware LLM" papers.

### 9. What are the weaknesses, limitations, or red flags?
The proof-of-concept is domain-specific and depends on a particular privileged-supervision setup. The improvement is real but not huge. The paper also does not show that fixing DFOT automatically improves end-to-end clinical outcomes, only that it improves the interface behavior under the defined challenge tasks.

### 10. What challenges or open problems remain?
The main open problem is generalizing DFOT beyond physiological sensing into other modular pipelines such as VLM toolchains, retrieval summaries, and agent planners consuming upstream scores or labels. Stronger reliability generators and better abstention policies also remain open.

### 11. What future work naturally follows?
Test DFOT in other modalities, replace the proof-of-concept reliability generator with stronger ones, connect interface metrics to downstream decision outcomes, and design agent interfaces that preserve uncertainty more richly than a single label plus confidence tag.

### 12. Why does this matter for cabbageland?
It matters because cabbageland keeps caring about modular systems where one component hands symbolic or linguistic summaries to another. This paper is a clean reminder that the handoff itself can be the failure mode.

### 13. What ideas are steal-worthy?
Name the downstream over-trust failure explicitly instead of burying it in generic uncertainty language. Use matched-versus-shuffled controls to test whether evidence is case-specific. Preserve reliability information across module boundaries instead of flattening everything into a clean-looking field.

### 14. Final decision
**Keep it.** The mitigation is only a beginning, but the evaluation frame is strong and broadly reusable.
