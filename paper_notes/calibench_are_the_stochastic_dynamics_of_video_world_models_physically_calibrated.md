# CaliBench: Are the Stochastic Dynamics of Video World Models Physically Calibrated?

## Basic info

* Title: CaliBench: Are the Stochastic Dynamics of Video World Models Physically Calibrated?
* Authors: Jonathan Sadeghi, Jenny Seidenschwarz, Jesse Allardice, Sirish Srinivasan, Benjamin Graham, Jeffrey Hawke
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.16829
* Date surfaced: 2026-08-18
* Why selected in one sentence: It evaluates whether video world models generate the right stochastic distribution rather than merely believable individual samples.

## Quick verdict

* Highly relevant

I inspected the arXiv HTML full text. This is the benchmark paper I most wanted from today's batch because it tests exactly the claim world-model papers keep implying and rarely measuring. The authors do not ask whether a rollout looks plausible. They ask whether repeated samples from the same macro-state produce the right physical outcome distribution.

## One-paragraph overview

CaliBench is a benchmark for stochastic physical calibration in generative video world models. It constructs nine environments whose outcome spaces are discrete and physically interpretable, such as Galton-board bins, die faces, card suits, lottery outcomes, roulette colors, and other simple stochastic scenes, and where the reference distribution is known in closed form. Each frontier video model receives the same conditioning image and prompt, then generates 32 samples under different seeds. A VLM extracts the discrete outcome from each generated video, and the benchmark measures both scorability and distance from the true distribution. The main result is that current frontier video models can produce physically plausible-looking individual videos while still collapsing or over-concentrating probability mass at the population level.

## Model definition

### Inputs
The paper introduces no new trainable world model. Its evaluation pipeline feeds existing video models a conditioning frame, a text prompt, and a random seed, then feeds the generated videos to a VLM-based outcome extractor.

### Outputs
The evaluated video models output videos. The benchmark maps each video to a discrete physical outcome and then outputs calibration statistics such as normalized total variation distance and model compliance over the suite.

### Training objective (loss)
There is no new learning objective in the benchmark itself. The paper evaluates off-the-shelf frontier video models and uses a fixed multi-sample scoring protocol.

### Architecture / parameterization
The contribution is a benchmark protocol rather than a model architecture: closed-form stochastic scenes, 32-sample repeated generation, VLM-based discrete outcome extraction, and separate measurement of scorability and distributional calibration.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the gap between single-sample realism metrics and the actual requirement for a stochastic world model: generating the correct distribution of physically possible outcomes from the same macro-state.

### 2. What is the method?
The method builds discrete stochastic scenes with known reference distributions, samples many rollouts from identical conditioning inputs, extracts outcomes into an interpretable state space, and measures deviation from the known target distribution.

### 3. What is the method motivation?
At macroscopic scales, apparent randomness comes from unresolved micro-state variation, so a world model has to map one visible macro-state to a distribution of plausible futures. Sample-level realism does not test that claim.

### 4. What data does it use?
It uses nine benchmark environments and evaluates six frontier video models, including SeeDance-2.0, WAN-2.7, Veo 3.1, Cosmos3-Super, Runway Gen-4.5, and HappyHorse-1.0.

### 5. How is it evaluated?
It is evaluated with normalized total variation distance to the closed-form reference distribution, hypothesis tests for calibration error, a scorability axis that measures whether the output is even readable as a valid outcome, and aggregate compliance over the suite.

### 6. What are the main results?
All six evaluated models remain far above the null sampling-noise floor. The best empirical mean normalized TV distance is **0.39** from SeeDance-2.0, still far from a calibrated simulator. The best benchmark compliance rate is **63.3%**, while HappyHorse lands at **16.7%**, effectively chance. The paper shows many scene-model cells with severe over-concentration or outright mode collapse, including several with TV distance **1.0**.

### 7. What is actually novel?
The real novelty is not another model comparison table. It is the benchmark design: physically interpretable discrete outcome spaces with known closed-form target distributions, plus explicit separation of structural instability from distributional miscalibration.

### 8. What are the strengths?
The benchmark measures the right thing, uses interpretable outcomes instead of learned feature proxies, and makes distributional failure visible in a way FID-style summaries do not. The scorability-versus-calibration split is also genuinely helpful because it isolates distinct failure modes.

### 9. What are the weaknesses, limitations, or red flags?
The scenes are intentionally simple and stylized, so success here is not the same as open-world competence. Outcome extraction depends on a VLM, which introduces another learned component into the loop. The protocol is also expensive, requiring many rollouts and VLM calls, and it does not yet prove that calibration on these scenes predicts calibration on real video data.

### 10. What challenges or open problems remain?
The main open problem is whether closed-form stochastic calibration benchmarks can predict distributional fidelity in richer open-world settings where the target distribution is not analytically known. Another is how to train models to satisfy this distributional criterion rather than merely optimize sample realism.

### 11. What future work naturally follows?
Use CaliBench-style signals during model training or alignment, scale the suite to more environments, and test whether benchmark calibration correlates with real-world predictive utility in physical simulators and embodied planning systems.

### 12. Why does this matter for cabbageland?
Because cabbageland cares about world models as decision tools, not as pretty video machines. If the stochastic distribution is wrong, downstream planning, uncertainty estimation, and safety logic all inherit the error.

### 13. What ideas are steal-worthy?
Use small closed-form environments with exact target distributions to grade generative models. Separate output validity from calibration. Evaluate repeated samples from the same macro-state instead of pretending one attractive rollout says anything about uncertainty quality.

### 14. Final decision
Keep as a preserved note. This is a benchmark contribution with real teeth, and the calibration frame should influence how future world-model papers are read.

## 6. Mandatory critical angles

The paper is strongest on evaluation fairness and on making the target construct explicit. It does not confuse "physically plausible sample" with "correct stochastic simulator." The biggest limitation is ecological breadth: the benchmark's strength comes from simple scenes with exact answers, so its long-range predictive value for messy open-world dynamics is still unproven.

## 7. Writing style

The right tone is strongly approving. The paper goes after a real measurement blind spot and does so with unusually clean mechanics.

## 8. Repository output format

Saved as a preserved paper note because the benchmark directly sharpens how stochastic video world models should be evaluated.
