# CompassAD: Intent-Driven 3D Affordance Grounding in Functionally Competing Objects

## Basic info

* Title: CompassAD: Intent-Driven 3D Affordance Grounding in Functionally Competing Objects
* Authors: Jingliang Li, Jindou Jia, Tuo An, Chuhao Zhou, Xiangyu Chen, Shilin Shan, Boyu Ma, Bofan Lyu, Gen Li, Jianfei Yang
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2604.02060
* Date surfaced: 2026-04-05
* Why selected in one sentence: It turns a real embodied ambiguity problem into an explicit benchmark and uses object-bounded language grounding to stop semantic leakage across confusable objects.

## Quick verdict

**Useful**

This is a good narrower paper, mostly because it refuses the fake cleanliness of single-object affordance grounding. The paper asks a practical question: if several nearby objects afford roughly the same function, can a system infer which one is appropriate from implicit intent rather than explicit object names? The answer is framed through a new benchmark and a boundary-aware grounding model. I inspected the arXiv abstract and substantial HTML paper text, including the task definition, dataset construction, method overview, and major module descriptions, but I did not audit appendices, code, or full results tables.

## One-paragraph overview

Most 3D affordance papers quietly assume the target object is already singled out, which makes the task easier and more sterile than real embodied operation. CompassAD instead builds scenes where multiple objects are plausible candidates for the same affordance type — knife versus scissors, cup versus bowl, and so on — and asks the model to ground the correct affordance region from an intent-driven query like “I want to prepare vegetable slices.” The benchmark contribution is the main event. The method, CompassNet, then tries to prevent language-conditioned features from sloshing across object boundaries by grouping points within each object instance, performing cross-attention at the region level inside those boundaries, and adding contrastive losses to separate target and confusable surfaces.

## Model definition

### Inputs
The model takes a multi-object 3D point cloud and a natural-language instruction describing the user’s intent. The same scene may correspond to different target affordance regions under different queries, and some queries are deliberately negative so the correct answer is abstention.

### Outputs
It predicts a per-point affordance probability map over the scene, ideally highlighting the correct functional region on the correct object and staying near zero when no object in the scene supports the queried intention.

### Training objective (loss)
From the accessible HTML, the method uses standard binary affordance supervision at the point level together with additional training losses for region-level relevance and bi-level contrastive refinement. The paper explicitly mentions an auxiliary region relevance loss and contrastive learning at geometric-group and point levels. I am not claiming a fully reconstructed total-loss formula beyond what the HTML exposed.

### Architecture / parameterization
A hybrid 3D-language grounding stack: Uni3D produces point features, RoBERTa encodes the query, **Instance-bounded Cross Injection** performs object-bounded coarse-to-fine language grounding, and **Bi-level Contrastive Refinement** sharpens discrimination between target and confusable regions. This is not a giant foundation model; it is a task-specific 3D affordance grounding architecture.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
The paper is trying to solve affordance grounding in cluttered scenes where multiple objects share similar functional properties and human instructions express intent rather than naming the target object explicitly. In other words, it wants scene-level, query-dependent affordance grounding rather than sanitized single-object segmentation.

### 2. What is the method?
- Build a benchmark of “confusing pairs,” where two or more nearby objects plausibly support the same affordance class.
- Use multi-object point clouds rather than isolated object crops.
- Keep the query target implicit and intent-driven instead of giving away the object category.
- Separate points by detected object instance boundaries.
- Form object-bounded regions and inject language via cross-attention only within those regions.
- Propagate query-informed region features back to points.
- Add contrastive refinement losses so confusable objects and confusable parts become easier to separate.
- Evaluate both seen and unseen query generalization, plus abstention on negative queries.

### 3. What is the method motivation?
The paper’s motivation is that existing affordance grounding benchmarks are structurally dishonest for real use. If the model sees one object at a time or if the query names the object explicitly, it never has to solve the interesting part: choosing the right object under task intent. The instance-bounded fusion is motivated by a concrete failure mode where scene-level language grounding lets semantics bleed across similar neighboring objects.

### 4. What data does it use?
The paper constructs the CompassAD benchmark from 46 core objects, arranged into 30 confusing pairs across 16 affordance types, with distractor objects added for scene diversity. The accessible HTML reports 6,422 multi-object scenes, 87,964 or 88K-plus language queries, and 105 object categories overall, using sources including 3D AffordanceNet and Affogato objects plus synthetic and real-world scan assets. GPT is used to help generate affordance-relevant intent queries, including negative queries for abstention testing.

### 5. How is it evaluated?
The method is evaluated on seen and unseen language splits, with metrics like aIoU and SIM reported in the accessible text, and with special attention to negative-query abstention. The paper also includes a robotic manipulator deployment to show transfer from benchmark grounding to real-world grasp selection in confusing scenes.

### 6. What are the main results?
The accessible HTML reports large gains over adapted baselines, including a 24.3 percent improvement in aIoU and a 28.4 percent improvement in SIM, plus successful transfer to robot manipulation examples. I believe the qualitative result: current methods struggle badly when the task is made query-dependent and multi-object, and boundary-aware grounding helps. I did not inspect enough benchmark detail to independently certify every headline margin.

### 7. What is actually novel?
The strongest novelty is the task and dataset framing, not just the architecture. The paper makes affordance grounding query-dependent at the object-selection level, which exposes a real failure mode that previous benchmarks suppress. Method-wise, the most useful novel move is bounding language-geometry interaction by object instance so the query signal does not smear across confusable objects.

### 8. What are the strengths?
- The benchmark is closer to real embodied ambiguity than the usual single-object setting.
- The paper explicitly tests abstention, which matters for safety.
- The failure diagnosis is crisp: cross-object semantic leakage plus insufficient fine-grained discrimination.
- The architectural response is targeted and not overly baroque.
- The robotic transfer demo is the right kind of reality check for this task.

### 9. What are the weaknesses, limitations, or red flags?
- The method depends on object separation quality. If instance boundaries are messy in richer real scenes, the whole strategy may wobble.
- The benchmark still uses curated confusing pairs with controlled layouts, so there is a risk of overestimating real-world robustness.
- GPT-assisted query generation may introduce stylistic regularities that models learn too well.
- This is a useful embodied-paper note, but not a major new representation-learning theory or world-model breakthrough.

### 10. What challenges or open problems remain?
The big next challenge is moving from relatively clean point-cloud scenes to denser, messier embodied settings with partial observability, occlusion, and long-horizon interaction. Another open problem is combining this kind of query-dependent affordance grounding with persistent memory and active perception instead of treating each scene as a one-shot segmentation problem.

### 11. What future work naturally follows?
- Bring intent-dependent affordance grounding into video and embodied interaction loops.
- Test the same ideas under partial observability and egocentric exploration.
- Combine object-bounded grounding with learned memory over previously seen scene structure.
- Study whether explicit object- and affordance-factorized state helps downstream planners or manipulators.

### 12. Why does this matter for cabbageland?
Because it is a small but honest paper about explicit structure. It does not solve everything, but it exposes one place where scene reasoning gets mushy and then adds a concrete boundary to keep the semantics from leaking. That is aligned with the broader cabbageland taste for mechanisms that make the right distinctions explicit instead of letting a big model blur them away.

### 13. What ideas are steal-worthy?
- Design benchmarks around real ambiguity, not uniquely identifiable targets.
- Use object boundaries as hard constraints on cross-modal fusion when confusion between neighboring instances is the actual problem.
- Evaluate abstention explicitly instead of rewarding confident hallucination.
- Separate coarse object selection from fine part localization when the task naturally has both levels.

### 14. Final decision
**Keep as adjacent inspiration.** The main value is the task honesty and the anti-leakage design pattern, not some sweeping new foundation-model recipe.
