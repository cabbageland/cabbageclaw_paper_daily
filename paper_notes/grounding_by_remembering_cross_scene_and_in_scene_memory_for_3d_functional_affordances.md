# Grounding by Remembering: Cross-Scene and In-Scene Memory for 3D Functional Affordances

## Basic info

* Title: Grounding by Remembering: Cross-Scene and In-Scene Memory for 3D Functional Affordances
* Authors: Qirui Wang, Jingyi He, Yining Pan, Xulei Yang, and Shijie Li
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2605.11616
* Date surfaced: 2026-05-13
* Why selected in one sentence: It uses two explicit memory mechanisms to solve two distinct affordance-grounding failures, which is much cleaner than generic retrieval-flavored mush.

## Quick verdict

**Useful**

This is not a foundational world-model paper, but it is a satisfying explicit-structure paper. The authors identify two concrete failure modes in training-free 3D affordance grounding and give each one its own memory mechanism, which already puts it above a lot of vaguer “memory” work. I inspected the abstract and substantial arXiv HTML full text through the problem setup, method, and part of the scene-memory construction, so confidence is good on the mechanism and lower on exhaustive implementation and benchmark details.

## One-paragraph overview

The paper studies 3D functional affordance grounding, where the model must locate the specific operable subregion in a scene, such as the correct drawer handle rather than the entire drawer face. It argues that training-free vision-language pipelines fail for two different reasons: they cannot localize small operable regions precisely, and they cannot reliably disambiguate among multiple similar instances under spatial qualifiers like “second from the top.” AffordMem addresses this with two explicit memories: a cross-scene affordance memory bank that recalls category-level masked exemplars to sharpen fine-grained localization, and an in-scene spatial memory that organizes candidate affordance instances and their relations in a 3D scene graph for language-guided disambiguation.

## Model definition

### Inputs
The system takes a posed RGB-D sequence with intrinsics and camera poses, plus a natural-language functional query. It also uses a reusable cross-scene memory bank built from previously annotated source scenes.

### Outputs
It predicts a 3D instance mask for the target operable region, such as the correct handle or button associated with the query.

### Training objective (loss)
There is no main end-to-end learned model trained for the target task in the usual sense. The system is largely training-free at inference time, using frozen language and segmentation components plus memory construction from source-scene annotations. The accessible text does not present a single unified learnable loss for the whole pipeline.

### Architecture / parameterization
It is a hybrid pipeline built from frozen VLM prompting, SAM-based segmentation, multi-view 3D lifting and clustering, a cross-scene masked-image memory bank, and an in-scene structured spatial graph for candidate reasoning.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to make 3D affordance grounding precise enough for real interaction. The task is not just to find an object category, but to identify the exact operable subregion and choose the right instance under spatially qualified language.

### 2. What is the method?
- Parse the query into a reference object label, an interaction label, and a spatial qualifier.
- Use cross-scene affordance memory, a bank of masked category exemplars, to visually prompt a frozen VLM toward the right fine-grained operable region.
- Lift the resulting 2D masks into a 3D candidate pool using depth-consistent multi-view fusion.
- Build an in-scene spatial memory graph over candidate instances and reference objects.
- Use that graph to resolve ordinal and relational language like “second from the top.”

### 3. What is the method motivation?
The motivation is that the two dominant failure modes are structurally different. Fine-grained subregion localization needs category-level affordance priors from past scenes, while spatial disambiguation needs a global memory of candidate layout within the current scene. Trying to solve both with one flat visual prompt is the wrong abstraction.

### 4. What data does it use?
The paper evaluates on SceneFun3D using posed RGB-D scene sequences and uses previously annotated source scenes to build its cross-scene memory bank. I did not inspect all split construction and annotation details in full.

### 5. How is it evaluated?
It is evaluated on training-free 3D functional affordance grounding, comparing AP50 results against prior training-free methods and running ablations on the two memory components.

### 6. What are the main results?
The paper reports gains over the prior training-free state of the art on both reported SceneFun3D splits, with ablations indicating that cross-scene memory helps fine-grained localization while in-scene spatial memory gives the larger gain on spatially qualified queries.

### 7. What is actually novel?
The novelty is the decomposition. The paper does not just say “use memory.” It maps two different grounding failures to two different explicit memory structures: category-level cross-scene affordance recall and scene-specific spatial candidate memory.

### 8. What are the strengths?
- The failure analysis is concrete and believable.
- The memory structures are explicit and interpretable.
- The decomposition into cross-scene and in-scene memory is genuinely useful.
- It avoids pretending that a generic VLM prompt can solve geometry and instance disambiguation by itself.

### 9. What are the weaknesses, limitations, or red flags?
- It is still a fairly engineered pipeline with many moving parts.
- The source-scene annotation requirement for building the memory bank may limit portability.
- The memory seems category-centric, so open-world generalization is unclear.
- This is affordance grounding, not a full world-model or policy-learning solution.
- Some of the gain may reflect benchmark-specific structure rather than a broadly reusable memory law.

### 10. What challenges or open problems remain?
The next challenge is turning this kind of explicit memory into something more reusable across tasks, categories, and dynamic scenes. It also remains open how to fold interaction feedback back into the memory instead of treating it mainly as a static support structure.

### 11. What future work naturally follows?
- Learn more transferable affordance memories with weaker supervision.
- Extend the scene-memory layer to dynamic or manipulation-conditioned updates.
- Connect this memory structure directly to policy execution rather than just grounding.
- Test whether the same decomposition helps other small-target spatial grounding tasks.

### 12. Why does this matter for cabbageland?
Because it is a clean example of memory earning its keep. The paper stores two kinds of structure because the task really has two different missing variables, and that is exactly the habit cabbageland wants more of.

### 13. What ideas are steal-worthy?
- Decompose “memory” claims by failure mode instead of using one generic retrieval buffer.
- Use cross-scene memory for category-level priors and in-scene memory for relational disambiguation.
- Prefer explicit spatial graphs when language depends on global instance layout.
- Treat fine-grained affordance localization as a distinct problem from object grounding.

### 14. Final decision
**Keep.** Not top-tier foundational work, but it contains a real and reusable design lesson about explicit memory decomposition.
