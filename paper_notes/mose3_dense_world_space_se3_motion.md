# MoSE3: Learning World-Space SE(3) at Every Pixel

## Basic info

* Title: MoSE3: Learning World-Space SE(3) at Every Pixel
* Authors: Jiahuan Cheng, Zhiyi Li, Tian Xia, Ruojin Cai, Yilun Du, Qianqian Wang
* Year: 2026
* Venue / source: arXiv; listed as NeurIPS 2026 Spotlight
* Link: https://arxiv.org/abs/2610.03716
* Date surfaced: 2026-10-05
* Why selected in one sentence: It turns dense video motion from point translation tracks into per-pixel world-space rigid transforms, using learned tracks plus rigidity embeddings rather than direct SE(3) regression.

## Quick verdict

* Must read

MoSE3 is the strongest paper in today's batch because it makes the representation more explicit in a way that actually does work. A pixel does not just get a 3D trajectory; it gets a local rigid transform, and pixels that move together become recoverable soft rigid groups. The main caveat is that the supervision is synthetic and downstream planning value is not yet demonstrated, but the representation move is real.

## One-paragraph overview

The paper argues that current 3D point trackers are too low-level for physical reasoning because they only say where surface points move, not how the underlying part rotates or which pixels belong to the same moving body. MoSE3 predicts dense 3D point tracks and per-pixel rigidity embeddings from monocular RGB video, then recovers per-pixel world-space SE(3) transforms by differentiably fitting rigid transforms within soft rigid clusters. It trains on Art-Kubric, a synthetic dataset designed to expose articulated objects, physics-driven contacts, dense tracks, per-link SE(3), and rigid-part labels. The result is a feed-forward model that improves dense SE(3) estimation and also strengthens 3D point tracking.

## Model definition

### Inputs

The model takes a sequence of monocular RGB frames, a query frame index, and the frozen geometric representation from a Pi3-style geometry branch. The prediction target is anchored at the query frame and spans the video sequence.

### Outputs

MoSE3 emits dense 3D point tracks, per-pixel visibility logits, L2-normalized rigidity embeddings, and recovered per-pixel world-frame SE(3) transforms for each target frame. At the object or part level, those embeddings can be clustered into rigid groups and refit into one transform per group.

### Training objective (loss)

The paper trains the model with joint losses for point tracking, rigidity embeddings, and SE(3) recovery. The tracking losses cover image-plane and depth consistency, visibility, temporal displacement, and related track terms; the rigidity loss encourages pixels sharing rigid motion to be close in embedding space; the SE(3) losses supervise recovered transforms. The full loss is a weighted sum applied in one training stage with scheduled learning-rate phases.

### Architecture / parameterization

MoSE3 reuses a Pi3 image encoder and shared decoder layers, then forks into a frozen geometry branch and a trainable tracking branch. Tracking tokens attend to frozen geometry tokens at every tracking-branch layer. Two heads produce point tracks and rigidity embeddings; Horn-style weighted Procrustes recovery turns tracks plus soft rigid weights into valid SE(3) transforms.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

It tries to make video motion representations useful for physical reasoning and manipulation. Dense 2D or 3D tracks describe point translations, but many tasks need rotations, rigid groups, articulated parts, and local frames.

### 2. What is the method?

Predict 3D tracks and rigidity embeddings, then recover per-pixel SE(3) transforms analytically from soft groups of nearby points. The model learns the easier intermediate objects and uses geometry to enforce a valid rigid-motion representation.

### 3. What is the method motivation?

Direct dense SE(3) regression is hard because rotations live on a curved manifold and real dense SE(3) labels are scarce. But 3D tracks are learnable, and if rigid grouping is known, the transform can be recovered in closed form.

### 4. What data does it use?

The key training data is Art-Kubric: 5,000 synthetic scenes with rigid and articulated objects, physics simulation, moving cameras, dense long-range 2D/3D tracks, per-link SE(3), visibility, depth, normals, segmentations, and rigid-motion labels. Evaluation includes HO3D, iTACO, YCBInEOAT, and TAPVid-3D-style 3D tracking datasets.

### 5. How is it evaluated?

The paper evaluates per-pixel and object/part-level SE(3) on HO3D and iTACO using rotation error, ADD, AUC, and cluster IoU. It also evaluates world-coordinate 3D point tracking on PointOdyssey, ADT, and PStudio, and runs ablations for direct SE(3) regression, Art-Kubric, rigidity loss, SE(3) loss, and track-only variants.

### 6. What are the main results?

MoSE3 reports best SE(3) estimation across rigid and articulated benchmarks. With rigid clustering, it reports substantially lower HO3D and iTACO rotation/translation error than adapted tracker baselines. On 3D tracking, it improves average L-50 accuracy to 0.5946 versus 0.5402 for Track4World in the reported table. The ablation is important: direct SE(3) regression, track-only recovery, removal of Art-Kubric, removal of rigidity loss, and removal of SE(3) loss all degrade the small-scale iTACO result.

### 7. What is actually novel?

The novelty is not "tracking plus a dataset"; it is the decomposition of dense SE(3) prediction into learnable 3D tracks, learnable soft rigid groups, and differentiable analytic transform recovery. Art-Kubric matters because it supplies the supervision that this decomposition needs.

### 8. What are the strengths?

The representation is compact, structured, and physically meaningful. The method directly tests the claimed decomposition with ablations. The dataset targets exactly the missing supervision channel: articulated multi-link motion with exact rigid-group and SE(3) labels.

### 9. What are the weaknesses, limitations, or red flags?

The model is trained on synthetic motion and evaluated on benchmarks where ground truth or proxies still simplify real deployment. In-the-wild qualitative results are encouraging but not a substitute for real dense SE(3) validation. The paper does not show that downstream planners or robot policies actually improve when fed these transforms. It also depends on strong frozen geometry priors.

### 10. What challenges or open problems remain?

The open question is whether dense SE(3) fields can become a stable interface for planning, manipulation, editing, or persistent world models outside synthetic annotation regimes. Real dynamic scenes, deformable objects, contact ambiguity, and occlusion remain hard.

### 11. What future work naturally follows?

Use MoSE3-like outputs as an explicit state layer for action-conditioned world models, manipulation planning, articulated-object memory, and simulation-ready scene tracking. Another natural next step is to pair it with uncertainty over transforms and rigid-group assignments.

### 12. Why does this matter for cabbageland?

Cabbageland keeps circling the same rule: state should carry the claim. MoSE3 is a good example. It does not bury "motion understanding" inside a latent; it exposes rotations, translations, and co-moving groups as explicit objects.

### 13. What ideas are steal-worthy?

Predict easier intermediate structure and recover the hard structured object analytically. Use rigidity embeddings as an interface between point-level perception and part-level state. Treat articulated synthetic data as a way to force representations to split bodies by motion rather than by instance labels.

### 14. Final decision

Preserve. This is directly relevant to explicit physical state, world models, and action-facing representations.
