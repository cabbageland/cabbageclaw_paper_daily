# LongSpace: Exploring Long-Horizon Spatial Memory from Perception to Recall in Video

## Basic info

* Title: LongSpace: Exploring Long-Horizon Spatial Memory from Perception to Recall in Video
* Authors: Shiqiang Lang, Jing Liu, Haoyang He, Peiwen Sun, Yuanteng Chen, Tao Liu, Lan Yang, Longteng Guo, and Honggang Zhang
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.05677
* Date surfaced: 2026-06-07
* Why selected in one sentence: It separates genuine long-horizon spatial memory from naive long-context video input by combining a room-tour benchmark with geometry-aware, layer-aware memory.

## Quick verdict

**Useful direct-adjacent work**

This is worth preserving mostly for the benchmark pressure and the memory interface. LongSpace-Bench is exactly the kind of evaluation that makes "we handle long video" claims less slippery: models must remember layouts, routes, viewpoint changes, object states, and spatial relations over room tours. I inspected the arXiv PDF full text, including the benchmark definition, method, main results, ablations, and limitations. I did not audit the dataset itself or reproduce the training/evaluation pipeline.

## One-paragraph overview

LongSpace introduces LongSpace-Bench, a benchmark of 445 real-world room-tour videos, about 159 hours total, and 4,073 question-answer pairs across ten spatial task types. The benchmark is split into scene perception, spatial relationship, and spatial memory questions. The model, LongSpace, uses spatial structure perception to inject 3D spatial tokens into early decoder layers and hierarchical KV memory to preserve role-specific evidence across video chunks. At question time, it retrieves relevant memory entries and uses them as a frozen memory prefix for answer generation.

## Model definition

### Inputs
The model takes long room-tour videos segmented into chunks, plus a downstream spatial question. It uses 2D visual tokens, 3D spatial tokens from a geometry encoder, and text tokens.

### Outputs
The output is an answer to spatial QA tasks such as scene classification, relative distance or orientation, appearance order, state change, egocentric reasoning, route planning, and route recall.

### Training objective (loss)
The paper trains the language backbone, geometry-aware module, and memory modeling head for one epoch on a mixed spatial/long-video training set. The inspected text gives optimizer-level details, but the important conceptual objective is supervised spatial QA with geometry-aware representation and memory retrieval.

### Architecture / parameterization
LongSpace has two main modules. Spatial Structure Perception fuses 3D spatial tokens with 2D visual representations and injects them into decoder layers. Hierarchical KV Memory writes selected key/value states into perceptual, working, and long-memory roles with layer-aware budgets, then retrieves question-relevant memory entries during answer generation.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Long video MLLMs can accept more frames, but that is not the same as spatial memory. Navigation and embodied-assistance tasks require models to preserve and retrieve evidence observed much earlier: room layout, route transitions, object state changes, and spatial relations under changing viewpoints.

### 2. What is the method?
- Build LongSpace-Bench from real-world room-tour videos.
- Define QA categories for scene perception, spatial relations, and spatial memory.
- Encode video chunks with geometry-aware spatial structure perception.
- Inject 3D spatial tokens into early decoder layers.
- Write layer-aware KV memories with separate perceptual, working, and long-memory roles.
- Retrieve question-relevant memory entries at inference and use them to answer.

### 3. What is the method motivation?
The motivation is that relevant spatial evidence is scattered across time. Uniform frame sampling can miss it, and recent-window inference forgets distant observations. A model needs both local geometry and an organized memory substrate for long-horizon recall.

### 4. What data does it use?
LongSpace-Bench contains 445 room-tour videos, approximately 159 hours of video, and 4,073 QA pairs. The videos are mostly indoor room tours. The tasks cover object counting, scene classification, scene consistency, relative distance, relative orientation, appearance order, state change, egocentric reasoning, route planning, and route recall.

### 5. How is it evaluated?
The paper evaluates LongSpace-Bench and also reports results on spatial reasoning benchmarks including VSI-Bench. It compares proprietary models, general open-source video/MLLM models, spatial-centric models, and LongSpace-9B. Ablations vary geometry-injection depth, memory organization, memory budgets, and long-memory inference settings.

### 6. What are the main results?
On LongSpace-Bench, LongSpace-9B reaches 49.2 overall, beating Qwen3-VL-32B by 2.7 points and Gemini-3-Pro by 3.9 points in the reported table. It is strongest on memory-heavy categories such as Appearance Order, State Change, and Route Recall. On VSI-Bench, LongSpace-9B reaches 70.8 average, ahead of the listed spatial-centric and general baselines. Long-memory inference reaches 49.2 on LongSpace-Bench versus 36.1 for uniform 32-frame sampling and 37.7 for recent-window inference; the gain grows with video length.

### 7. What is actually novel?
The benchmark is the more important contribution than the model. LongSpace-Bench operationalizes long-horizon spatial memory over continuous room tours. The model contribution is the combination of 3D spatial-token injection and layer-aware hierarchical KV memory with role-specific storage and retrieval.

### 8. What are the strengths?
- The benchmark targets spatial memory rather than generic video QA.
- The tasks separate perception, spatial relations, and memory.
- The model makes memory organization explicit instead of relying only on longer context.
- Ablations show layer-aware memory matters more than simply changing memory capacity.
- Gains increase as video horizons get longer, which supports the mechanism claim.

### 9. What are the weaknesses, limitations, or red flags?
- The benchmark is mostly indoor room-tour video, not interactive robot exploration.
- The task setting is observation-based QA, not closed-loop navigation or manipulation.
- Strong proprietary models still outperform LongSpace on some categories such as scene classification, egocentric reasoning, route planning, and certain relational tasks.
- The method is still a video MLLM memory system, not a persistent 3D world state that can be updated through action.

### 10. What challenges or open problems remain?
The natural next step is active spatial memory: can the agent choose views, update maps, and act using the memory rather than only answer after passive observation? Another open problem is making memory entries inspectable as explicit spatial state rather than only retrieved KV features.

### 11. What future work naturally follows?
- Extend LongSpace-Bench toward outdoor navigation and active exploration.
- Add action-conditioned updates and interactive route-following tasks.
- Compare KV memory against explicit maps, object graphs, and 3D scene memories.
- Report failure modes for view ambiguity and route recall separately.
- Test whether the benchmark predicts downstream embodied-agent performance.

### 12. Why does this matter for cabbageland?
It pressures long-video models in the right direction. Cabbageland should not accept "long context" as a substitute for spatial memory. LongSpace gives a concrete benchmark and a model design that at least tries to preserve spatial evidence in a structured way across time.

### 13. What ideas are steal-worthy?
- Separate spatial-memory evaluation into scene perception, spatial relations, and memory.
- Treat route recall, state change, and appearance order as distinct memory demands.
- Use role-specific memory rather than one undifferentiated KV store.
- Evaluate long-memory inference against uniform and recent-window frame baselines.
- Ask whether gains grow with temporal distance; if not, the memory claim is weak.

### 14. Final decision
**Keep as useful direct-adjacent work.** The model is not the final answer, but the benchmark and memory-interface pressure are worth preserving.
