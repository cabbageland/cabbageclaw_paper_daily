# Does Marginal Coverage Guarantee Class-Conditional Safety for Zero-Shot VLMs Under Shift?

## Basic info

* Title: Does Marginal Coverage Guarantee Class-Conditional Safety for Zero-Shot VLMs Under Shift?
* Authors: Jai Kumar Sharma, Amartya Dutta
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.19376
* Date surfaced: 2026-08-22
* Why selected in one sentence: It is a severe audit showing that respectable marginal conformal coverage can coexist with near-zero protection on the worst classes under shift.

## Quick verdict

* Highly relevant

I inspected the arXiv HTML full text, especially the audit protocol and the shift, tail-coverage, and repair sections. This paper earns a preserved note because it attacks a very common deployment slippage directly: people see a decent marginal coverage number and infer something like safety or reliability for all classes. The paper shows that inference is badly wrong in frozen zero-shot VLMs, and the negative result remains ugly even after applying the most natural deployable repair.

## One-paragraph overview

The paper audits split-conformal prediction as an abstention layer for frozen zero-shot VLMs under deployment shift. Instead of proposing another conformal method, it asks a harsher question: if a practitioner calibrates on in-distribution ImageNet and then deploys on shifted or non-ImageNet data, does a respectable marginal coverage number still protect the tail classes that need it most? The answer is no. Across CLIP, OpenCLIP, and SigLIP, acceptable-looking marginal coverage can hide widespread class-conditional collapse, and the deployable fixes that improve marginal or average behavior still fail to repair the worst-class tail.

## Model definition

### Inputs
Frozen zero-shot VLM logits or scores from CLIP, OpenCLIP, and SigLIP; source calibration splits; shifted test datasets; label prompts; and standard conformal scores including LAC, APS, and RAPS.

### Outputs
Prediction sets, marginal coverage, class-conditional coverage statistics, worst-class coverage, average set size, below-null and below-nominal fractions, and repair comparisons under source-side or target-side calibration variants.

### Training objective (loss)
The paper does not train new VLMs. It fits conformal thresholds on calibration data and evaluates frozen models under different calibration and repair schemes.

### Architecture / parameterization
Black-box audit of frozen zero-shot VLM families wrapped with conformal prediction. The relevant parameterization lives in the score choice, calibration regime, and repair variant, not in new backbone training.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve a deployment misconception: treating marginal conformal coverage under shift as if it guaranteed something like class-conditional safety for frozen zero-shot VLMs.

### 2. What is the method?
The method is a cross-family audit of CLIP, OpenCLIP, and SigLIP under several visual and vocabulary shifts, using marginal and Mondrian conformal calibration, finite-sample null comparisons for worst-class behavior, and available repair options such as Conf-OT and target-side recalibration.

### 3. What is the method motivation?
Under shift, exchangeability breaks. The real question is then not the theorem but the empirical failure mode: whether average-looking coverage can conceal severe per-class under-coverage that a deployer would care about.

### 4. What data does it use?
ImageNet-val is split for calibration and in-distribution testing, then the audit evaluates ImageNet-V2, ImageNet-Sketch, ImageNet-R, ImageNet-A, ImageNet-C, Stanford Cars, and Food-101. Results are reported over 10 random splits with bootstrap confidence intervals.

### 5. How is it evaluated?
The paper reports marginal coverage, set size, per-class coverage percentiles, worst-class coverage, below-null and below-nominal fractions, mean per-class under-coverage, source-versus-target threshold correlations, and repair behavior under different calibration schemes.

### 6. What are the main results?
On ImageNet-Sketch, APS marginal coverage stays around 0.86, yet the worst class falls to roughly 0 coverage and 10-12% of classes fall below the 0.70 finite-sample null floor while 41-44% sit below the 0.90 target. Source-side Mondrian calibration improves the in-distribution tail but does not transfer under shift. Conf-OT restores marginal coverage to about 0.89-0.90 and roughly halves mean per-class under-coverage, but worst-class coverage on Sketch still stays at or below 0.02 across the tested settings. The failing classes are strongly aligned with target accuracy but essentially invisible to the tested source-side diagnostics, which correlate only rho = 0.06-0.19 with the classes that later under-cover.

### 7. What is actually novel?
The novelty is diagnostic rather than algorithmic. The paper adds a worst-class finite-sample audit lens and shows, cleanly, that average-level conformal success does not imply class-tail safety in frozen zero-shot VLM deployment.

### 8. What are the strengths?
The paper asks the right ugly question. It is careful about finite-sample null effects instead of overreacting to one minimum statistic. It compares multiple VLM families, score geometries, shifts, and repair schemes. The negative result is operationally useful rather than performatively pessimistic.

### 9. What are the weaknesses, limitations, or red flags?
The paper does not propose a strong new repair. It studies frozen black-box deployment rather than train-time adaptation. Its notion of "safety" is statistical class-conditional coverage, not downstream harm. Some readers may want stronger causal separation between conformal wrapper failure and underlying representation failure.

### 10. What challenges or open problems remain?
The open problem is how to recover tail-safe uncertainty under shift without needing target labels for every class or exploding prediction-set size. More generally, practitioners still lack cheap diagnostics for identifying at-risk classes before deployment.

### 11. What future work naturally follows?
Future work should explore repair methods that explicitly target worst-class or group-tail coverage in frozen VLM settings, plus better label-free diagnostics for anticipating when source thresholds will fail under shift.

### 12. Why does this matter for cabbageland?
Because cabbageland cares about uncertainty that survives contact with deployment rather than average-looking calibration numbers. This paper is a useful warning against treating one comfort metric as if it covered the tail.

### 13. What ideas are steal-worthy?
Audit average metrics against explicit tail diagnostics. Use simulated null bands before declaring a worst-class collapse. Report repair methods jointly on coverage and set size. Treat representation failure and uncertainty-wrapper failure as coupled but separable audit targets.

### 14. Final decision
Keep as a preserved note. The paper does not solve the problem, but it exposes the right problem sharply enough that it should shape how future uncertainty claims are read.

## 6. Mandatory critical angles

The paper is strongest on uncertainty quantification, data realism under shift, and evaluation fairness. It earns the "safety" label only in the limited statistical sense it defines, and to its credit it says that plainly. The main caveat is that the paper remains an audit of frozen deployment-time wrappers rather than a constructive solution.

## 7. Writing style

The right tone is approving and severe. The paper is valuable because it removes a flattering inference that many people would otherwise keep making.

## 8. Repository output format

Saved as a preserved paper note because the audit logic is clean, reusable, and relevant well beyond this single vision-language setting.
