# Recursive Code World Models: Building Complex Worlds through Recursive Scene Programs

## Basic info

* Title: Recursive Code World Models: Building Complex Worlds through Recursive Scene Programs
* Authors: Zhiqi Li, Yuxuan Liao, Bo Zhu
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2609.11499
* Date surfaced: 2026-09-11
* Why selected in one sentence: It turns image-to-3D code reconstruction into recursive executable world construction with explicit subworld handoffs.

## Quick verdict

* Highly relevant

I inspected the full arXiv HTML text, including the Recursive Scene Program representation, recursive solver process, reference/camera crop handoff, benchmark setup, reconstruction metrics, ablation, and limitations. This is worth preserving because the recursion is doing representational work: local details get their own solve while the parent scene still revisits global composition.

## One-paragraph overview

Recursive Code World Models reconstruct complex 3D worlds from a single reference image as executable scene programs. The key representation is a Recursive Scene Program: code that contains local construction procedures, editable parameters, references to child programs, and shared dependencies. The construction process uses the same vision-language coding solver at every node. Each call establishes the current whole, selects unresolved components for child calls using matched reference and camera crops, then recomposes and refines the assembled scene after the children return. The result is not just a generated mesh or a flat code file; it is a nested executable world with component references that can be rendered, edited, and reused.

## Model definition

### Inputs
The system starts from one reference image and a reference-view camera configuration. Recursive child calls receive matched reference crops, matched camera views, the inherited parent context, current component code, and render-feedback snapshots.

### Outputs
The output is a Recursive Scene Program: executable Three.js scene code containing nested child program references, editable parameters, component procedures, shared assets, and spatial relationships. Rendering the assembled program should match the reference view while remaining inspectable from additional views.

### Training objective (loss)
The paper does not train a new model. It uses a frozen vision-language coding agent in an iterative render-inspect-edit loop. Numerical metrics are used for evaluation, while the solver itself is guided by visual comparison between reference images and rendered program outputs.

### Architecture / parameterization
The system is an agentic reconstruction pipeline around a parameterized Three.js compiler. The paper reports using the same base model and reasoning setting across methods. Each recursive node is a solver call that can render, inspect, edit code, request children, and revise the parent after child programs return.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Flat image-to-code reconstruction struggles when a scene has many interacting parts at different scales. Fine local details need focused perception and editing, but those local solves still have to preserve whole-scene geometry and relationships.

### 2. What is the method?
RCWM builds a recursive scene program. The solver first establishes the whole scene, then gives selected unresolved parts their own solver calls with matched reference evidence, then assembles the returned child programs and revisits the parent to fix composition, boundaries, and shared errors.

### 3. What is the method motivation?
The paper's useful motivation is that a part is not merely an asset to generate and paste. It is a subworld that may need its own perception-and-editing loop, while the parent remains responsible for the relationships among parts.

### 4. What data does it use?
The evaluation uses five whole-scene references and five local crops, including city and scene references from public sprite/world demonstrations. Reconstruction uses reference images only.

### 5. How is it evaluated?
The paper compares against three code-based image-to-scene reconstruction baselines under the same base model. Metrics include PSNR, SSIM, edge F1, LPIPS, and CLIP image similarity against the unmodified reference view. Additional views and source programs are inspected qualitatively. Ablations compare flat, flat-plus-zoom, non-recursive hierarchy, fixed-depth recursion, and free-depth recursion.

### 6. What are the main results?
RCWM obtains the highest PSNR and lowest LPIPS on every reported reference, and the highest SSIM on nine of ten references. In the ablation, free-depth recursion improves school-block whole-frame PSNR from 16.8 to 19.0 and local SSIM from 0.52 to 0.60 relative to the fixed two-level variant. The paper also reports recursive call trees for all ten scenes.

### 7. What is actually novel?
The novelty is the explicit recursive program representation plus the global-local-global construction loop. Code-as-world-state is not new by itself, but this paper gives local structures their own complete solve and then forces a parent revisitation step to repair cross-part relationships.

### 8. What are the strengths?
The mechanism is legible and transferable. The output remains executable and editable, not just visually plausible. The recursion also matches the problem structure: detailed components need focused evidence, while composition errors only become visible after the pieces return.

### 9. What are the weaknesses, limitations, or red flags?
The experiments are small, single-run, and expensive. The method depends heavily on a strong frozen coding/vision agent and a carefully structured execution environment. Single-view input leaves hidden geometry underspecified, and the paper admits that larger benchmarks and repeated runs are still needed.

### 10. What challenges or open problems remain?
The hard problems are scaling the recursive solve, measuring editability and physical validity, handling ambiguous hidden geometry, preventing recursive drift, and learning when to delegate a child solve versus refine in the parent.

### 11. What future work naturally follows?
Natural next steps include multi-view evidence, automatic uncertainty over hidden components, benchmark suites for executable scene programs, learned delegation policies, and hybrid pipelines where learned geometry priors feed executable code reconstruction.

### 12. Why does this matter for cabbageland?
Cabbageland wants structured, inspectable world representations. RCWM is useful because it treats code as a state carrier and recursion as a way to preserve both local detail and global relationships.

### 13. What ideas are steal-worthy?
Represent worlds as executable programs with child references. Give subcomponents their own reference-aligned camera crops. Always revisit the parent after child returns. Preserve the construction trace so the world can be audited and edited later.

### 14. Final decision
Keep as a highly relevant preserved note. The scale is limited, but the global-local-global recursion is a real design pattern for compositional world construction.
