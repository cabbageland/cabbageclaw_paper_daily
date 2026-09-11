# UBone3D: Physics-Rectified Conditional Flow Matching for Anatomical 3D Shape Completion from Ultrasound

## Basic info

* Title: UBone3D: Physics-Rectified Conditional Flow Matching for Anatomical 3D Shape Completion from Ultrasound
* Authors: Weiying Chen, Yuchong Gao, Siyuan Li, Marek Reformat, Rui Zheng, Edmond Lou
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2609.11506
* Date surfaced: 2026-09-11
* Why selected in one sentence: It pairs a CT-trained anatomical flow prior with a differentiable ultrasound physics proxy to complete 3D bone shape from artifact-heavy ultrasound point clouds.

## Quick verdict

* Highly relevant

I inspected the full arXiv HTML text, including the BoneFM conditional flow model, USimNet physics proxy, physics-rectified inference, simulation and in-vivo datasets, baseline comparisons, in-vivo laminae metrics, and ablations. This is worth preserving as adjacent medical/generative work because the method separates anatomical plausibility from imaging-physics consistency instead of hiding both inside one black-box predictor.

## One-paragraph overview

UBone3D reconstructs complete anatomical 3D bone point clouds from partial ultrasound-derived point clouds. Ultrasound observations are difficult because the missingness and artifacts are not random; they are shaped by acoustic physics such as finite beamwidth, attenuation, reverberation, streaking, and dropout. The method trains BoneFM, a conditional flow-matching anatomy prior, on clean CT-derived spine point clouds. It also trains USimNet, a differentiable proxy that maps completed anatomy into ultrasound-like observations. At inference, BoneFM generates plausible anatomy while USimNet supplies observation-consistency gradients that rectify the flow trajectory late in generation. The goal is to recover anatomically plausible bone geometry while respecting the physics of what ultrasound actually saw.

## Model definition

### Inputs
Inputs are partial, artifact-heavy 3D ultrasound point clouds extracted from segmentation outputs. Training also uses clean CT-derived complete anatomy point clouds and simulated ultrasound-style paired observations.

### Outputs
The output is a completed 3D bone point cloud, especially vertebral structures for spine ultrasound.

### Training objective (loss)
BoneFM is trained with an optimal-transport conditional flow-matching regression objective over clean complete point clouds conditioned on partial observations. USimNet is trained to minimize symmetric Chamfer Distance between its predicted ultrasound-style point cloud and the simulated ultrasound point cloud. At inference, physics rectification uses gradients from USimNet plus the BoneFM flow, with classifier-free guidance on the anatomy prior.

### Architecture / parameterization
BoneFM uses a PointNet++ backbone modulated with FiLM layers to parameterize a conditional velocity field. USimNet uses a lightweight PointNet++-based encoder-decoder with an MLP decoder. Inference solves the flow with Heun integration and applies USimNet guidance late in the trajectory through a time-dependent guidance schedule.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
3D ultrasound is safer than repeated CT or X-ray imaging, but segmentation-derived ultrasound point clouds are incomplete and artifact-heavy. The paper wants to recover complete anatomical bone geometry from partial ultrasound observations without pretending the input noise is generic.

### 2. What is the method?
UBone3D trains a generative anatomy prior from CT-derived point clouds and a differentiable ultrasound physics proxy from simulated ultrasound artifacts. During inference, the anatomy prior proposes clean complete shapes while the physics proxy steers generation toward shapes whose simulated ultrasound observations match the actual partial input.

### 3. What is the method motivation?
The motivation is that ultrasound artifacts are structured by acquisition physics. A pure completion prior may hallucinate plausible anatomy that does not explain the observed ultrasound, while a pure geometric baseline may preserve artifacts. Decoupling anatomy and physics makes the two constraints inspectable.

### 4. What data does it use?
The paper uses Spine1K-PC, derived from the CTSpine1K dataset, with 5,502 training samples and 1,373 test samples. It simulates ultrasound-style partial observations under geometric, simple-physics, and full-physics settings. It also evaluates zero-shot on 15 in-vivo ultrasound point clouds from thoracic and lumbar regions.

### 5. How is it evaluated?
The evaluation includes distributional similarity between simulated and in-vivo point clouds, simulation completion metrics with Chamfer Distance, Earth Mover's Distance, and F-score@1%, in-vivo laminae distance error against raw input and VNN references, and ablations for the physics proxy, anatomy prior, guidance strength, and sampling steps.

### 6. What are the main results?
The full physics simulation best matches in-vivo observations among the reported simulation variants, with MMD-CD 877.394, COV 0.205, JSD 0.638, and SWD 12.917. On simulation completion, UBone3D gives stable performance under the full-physics training setting: CD 28.161, EMD 74.298, and F1 0.079. On in-vivo laminae distance, UBone3D reports 0.819 mm against raw input and 1.293 mm against VNN reference, improving the VNN-reference error over SVDFormer and SSM-Net. The USimNet ablation is strong: full USimNet improves CD/EMD/F1 from 49.196/96.673/0.064 without USimNet to 28.161/74.298/0.079.

### 7. What is actually novel?
The novelty is physics-rectified conditional flow matching for ultrasound shape completion: an anatomy prior and a differentiable imaging-physics proxy act as separate forces during inference. The method does not simply train a completion network on partial point clouds.

### 8. What are the strengths?
The paper respects the imaging modality. It makes the artifact model explicit, tests simulation-to-in-vivo similarity, evaluates on real patient data, and provides ablations showing that the physics proxy materially changes completion quality.

### 9. What are the weaknesses, limitations, or red flags?
The real in-vivo set is small. The physics proxy is still simulation-trained, so real ultrasound variation may not be fully captured. The paper also admits that real-world outputs need further improvement. Clinical deployment would need much stronger validation, segmentation robustness, and uncertainty estimates.

### 10. What challenges or open problems remain?
Open problems include learning better patient-specific ultrasound physics, modeling upstream segmentation uncertainty, scaling the in-vivo evaluation, validating clinically meaningful measurements, and preventing anatomically plausible but observation-inconsistent hallucinations.

### 11. What future work naturally follows?
Use uncertainty-aware flow inference, adapt USimNet with real ultrasound pairs when available, integrate probe pose and acquisition metadata, and evaluate downstream scoliosis or surgical-navigation measurements rather than point-cloud metrics alone.

### 12. Why does this matter for cabbageland?
Cabbageland cares about explicit structure and physics-guided generation. UBone3D is a good example of separating a generative prior from an observation-formation model and combining them through test-time gradients.

### 13. What ideas are steal-worthy?
Do not make one network absorb both object prior and sensor physics. Train a differentiable proxy for observation formation. Apply physics guidance late in generation when the anatomy prior has formed a plausible structure. Evaluate whether simulated artifacts statistically resemble real observations before trusting sim-to-real results.

### 14. Final decision
Keep as a highly relevant adjacent note. It is not a core world-model paper, but the anatomy-prior plus physics-proxy pattern is useful beyond medical ultrasound.
