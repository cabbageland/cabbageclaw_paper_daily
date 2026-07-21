# The Calibration Channel Determines the Bayes-Error Proxy: An Exact Law for Temperature-Induced Distortion

## Basic info

* Title: The Calibration Channel Determines the Bayes-Error Proxy: An Exact Law for Temperature-Induced Distortion
* Authors: Shreyas Pradeepkumar Khandale
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.18162
* Date surfaced: 2026-07-21
* Why selected in one sentence: It proves that a soft-label Bayes-error proxy can be pushed almost arbitrarily by temperature scaling while the classifier and its test error stay unchanged.

## Quick verdict

**Useful**

This is a small diagnostic paper, but the central theorem is sharp enough to matter. It turns a hand-wavy warning about calibration channels into an exact law with a clean practical consequence: the proxy is not a task property. I inspected the arXiv PDF in full, including the setup, theorem statements, experiments, discussion, and limitations.

## One-paragraph overview

The paper studies the soft-label Bayes-error estimator `beta(z) = E[min(z, 1-z)]`, which is supposed to reflect irreducible classification error when the probabilities are true posteriors. It asks what happens when those probabilities instead come from a common post-hoc calibration channel: temperature scaling of a fixed classifier's logits. The answer is bad in a precise way. The proxy becomes an exact function of the classifier's margin distribution, increases strictly with temperature, and ranges over the whole interval `(0, 1/2)` while the classifier's decisions and `0-1` error remain unchanged. So the reported proxy is about the probability-producing channel, not just the task.

## Model definition

### Inputs
The analysis takes a fixed binary classifier's logits and a temperature parameter `T`, which defines a temperature-scaled probability channel.

### Outputs
It outputs the temperature-dependent Bayes-error proxy `beta(T)` together with an exact margin-based identity and an approximate Gaussian closed-form curve.

### Training objective (loss)
The paper does not train a new model. It analytically characterizes how the proxy changes for fixed classifiers under temperature scaling and validates the prediction empirically on trained classifiers.

### Architecture / parameterization
There is no new model architecture. The main objects are a fixed classifier, its margin distribution, and the temperature scaling map applied to its logits.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to determine how much the soft-label Bayes-error proxy depends on the calibration channel rather than the underlying task.

### 2. What is the method?
The method is analytic. The paper reduces the proxy under temperature scaling to the expectation of `sigma(-|margin| / T)`, proves a strict monotone bijection from temperature to proxy value, and gives a two-parameter Gaussian closed form in the well-separated regime.

### 3. What is the method motivation?
The motivation is that people treat soft-label Bayes-error estimates as if they describe task difficulty, even though the probabilities fed into the estimator often come from model outputs or calibrated channels rather than true posteriors.

### 4. What data does it use?
The experiments use binary tasks derived from `CIFAR-10`, `Fashion-MNIST`, and `SVHN`, plus a small channel comparison using a `CIFAR-10H` human-soft-label source and a deep ensemble.

### 5. How is it evaluated?
It sweeps temperatures over fixed trained classifiers, records the proxy, `0-1` test error, and `ECE`, and compares the exact curve with the Gaussian closed form.

### 6. What are the main results?
Across eight binary tasks, the proxy varies by `56x` to `980x` while test error stays exactly constant. The closed form tracks the exact curve to within `0.018`, and the temperature that minimizes `ECE` does not define any special or stable proxy value.

### 7. What is actually novel?
The novelty is the exact law: temperature scaling turns the proxy into a strictly increasing bijection over `(0, 1/2)` for a fixed classifier. That makes the interpretive failure mathematically explicit rather than anecdotal.

### 8. What are the strengths?
It is clean, exact where it matters most, and the empirical validation matches the theory closely. The paper also states the practical recommendation plainly instead of hiding behind neutral math prose.

### 9. What are the weaknesses, limitations, or red flags?
The analysis is binary-only, diagnostic rather than constructive, and specific to the temperature-scaling family. The Gaussian closed form is approximate and only tight in the well-separated regime.

### 10. What challenges or open problems remain?
The obvious open directions are multi-class extensions and characterizing how other calibration maps such as isotonic, beta, or Platt scaling distort the proxy.

### 11. What future work naturally follows?
People should stop reporting raw Bayes-error proxies without the probability channel, and future work should either characterize or correct the distortion for more general channels.

### 12. Why does this matter for cabbageland?
Cabbageland cares about calibration, uncertainty, and measurement honesty. This paper is a compact reminder that a neat scalar can still be lying if the reporting channel is under-specified.

### 13. What ideas are steal-worthy?
Always annotate evaluation numbers with the channel that produced them. When a proxy is channel-dependent, prove the dependency exactly if you can. Separate diagnostic papers from constructive ones instead of pretending a theorem also fixed the estimator.

### 14. Final decision
**Keep it.** Small paper, real lesson, very reusable diagnostic instinct.
