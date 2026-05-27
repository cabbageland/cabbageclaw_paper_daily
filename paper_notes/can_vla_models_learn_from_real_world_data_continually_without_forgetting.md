# Can VLA Models Learn from Real-World Data Continually without Forgetting?

## Basic info

* Title: Can VLA Models Learn from Real-World Data Continually without Forgetting?
* Authors: Jiarun Zhu, Yijun Hong, Xiaoquan Sun, Zetian Xu, Mingqi Yuan, Zhiyong Wang, Wenjun Zeng, Jiayu Chen
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2605.26820
* Date surfaced: 2026-05-27
* Why selected in one sentence: It moves continual VLA learning out of comfortable simulation assumptions and shows that real-world sequential adaptation is fragile enough that protocol details can decide the whole conclusion.

## Quick verdict

**Useful**

This is more of a grounding and evaluation paper than an architectural leap, but it is exactly the kind of paper that should change how later claims are read. I inspected the arXiv HTML full text, including the abstract, introduction, setup, and main results discussion, but not every appendix analysis. The headline message looks credible: naive sequential fine-tuning forgets badly, and replay only works reliably when the implementation details are handled with unusual care.

## One-paragraph overview

The paper asks a basic deployment question that a lot of VLA work still dodges: if a robot keeps learning from newly arriving real-world demonstrations, does it retain earlier skills or overwrite them? To test this, the authors build a four-task real-world sequential manipulation stream spanning rigid-object pick-and-place, hook interaction, button pressing, and deformable towel folding. Using a π0.5-style baseline, they show that naive sequential fine-tuning catastrophically forgets earlier tasks, then study experience replay and find that it helps substantially, but only under specific choices about replay frequency, buffer size, and especially action normalization. The useful contribution is not a glamorous new memory mechanism. It is a cleaner empirical picture of where continual VLA learning actually breaks.

## Model definition

### Inputs
The learned policy consumes visual observations from multiple RGB cameras and task-conditioned robot demonstration data from a sequential stream of four real-world manipulation tasks. During replay-based continual learning it also consumes buffered demonstration samples from earlier tasks.

### Outputs
The model outputs robot actions under a supervised fine-tuning setup using a π0.5-style vision-language-action policy backbone.

### Training objective (loss)
The accessible paper text explicitly defines supervised fine-tuning with a negative log-likelihood loss over demonstrated actions. The continual-learning variants keep this basic objective while changing the data stream and replay schedule rather than introducing a fundamentally new model loss.

### Architecture / parameterization
The baseline is a π0.5-style VLA policy fine-tuned under supervised learning. The paper’s main contribution is the real-world continual-learning protocol and replay analysis, not a novel architecture.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to determine whether current VLA systems can acquire new real-world skills sequentially without catastrophically forgetting previously learned ones. The paper also asks which practical factors most strongly determine whether replay-based continual learning works.

### 2. What is the method?
The method is primarily an empirical study. The authors construct a real-world four-task sequential manipulation dataset, fine-tune a VLA policy task by task, measure forgetting with per-task scores and backward-transfer metrics, and compare naive sequential fine-tuning against replay-based variants under different implementation choices such as replay frequency and action normalization strategy.

### 3. What is the method motivation?
The motivation is straightforward and important. Real deployment is sequential and heterogeneous, but many existing continual-VLA claims come from narrower simulated settings with weaker distribution shift and occasionally unrealistic training assumptions. The paper wants a more causally honest test.

### 4. What data does it use?
It uses a real-world sequential manipulation dataset collected on an AgileX PiPER robot with four tasks and about 500 trajectories per task. The tasks span bowl stacking, cup hanging, button pressing, and towel folding, chosen to induce substantial variation in object geometry, grasping strategy, and motion primitive.

### 5. How is it evaluated?
It evaluates per-task normalized score after each sequential training stage, average score, negative backward transfer, and forward transfer. The paper compares single-task training, naive sequential fine-tuning, joint training, and replay-based continual-learning variants, while also analyzing the effects of replay frequency, replay budget, and action normalization choices.

### 6. What are the main results?
The main result is that naive sequential fine-tuning collapses badly on earlier tasks. In the reported main table, the first three tasks fall from near-perfect single-task performance to roughly 15.0, 25.0, and 13.3 after sequential training, with large positive backward transfer indicating heavy forgetting. The paper also reports that modest replay can recover much of this loss, and that a stable action-normalization strategy matters enough to change whether the continual-learning setup looks viable.

### 7. What is actually novel?
The novelty is mostly in the evaluation regime and diagnosis, not in a new network block. This appears to be one of the first explicit real-world continual-learning studies for VLA models that stresses heterogeneous tasks and calls out confounds like future-information leakage through normalization statistics.

### 8. What are the strengths?
- It studies the right failure mode in a more realistic setting.
- The task stream is heterogeneous enough to make forgetting meaningful.
- The paper highlights implementation details that are often hand-waved away.
- It usefully distinguishes real retention from benchmark comfort.

### 9. What are the weaknesses, limitations, or red flags?
- This is primarily a protocol paper, so there is less architectural mechanism to steal directly.
- Four tasks is useful but still small as a lifelong-learning proxy.
- Results are tied to one main baseline family, so I would not over-generalize absolute numbers.
- Replay helping is important, but it does not by itself solve longer-term memory editing, conflict handling, or open-ended skill growth.

### 10. What challenges or open problems remain?
We still need continual-learning methods that scale beyond a short sequence of tasks, handle changing action spaces or embodiments, and do more than preserve old demonstrations in a replay buffer. Another open issue is how to evaluate retention when tasks overlap partially and success cannot be summarized cleanly by small benchmark scores.

### 11. What future work naturally follows?
- Test stronger memory or adapter methods in the same real-world protocol.
- Expand the sequential stream to more tasks and longer time horizons.
- Study replay selection and forgetting-aware memory curation instead of mostly buffer size and cadence.
- Compare against explicit modular or world-model-based continual-learning schemes under the same constraints.

### 12. Why does this matter for cabbageland?
Because it improves research hygiene. A lot of continual-learning rhetoric in embodied AI still rides on narrow or forgiving setups. This paper makes it harder to wave away forgetting with pretty averages and easier to ask whether a method survives real sequential heterogeneity.

### 13. What ideas are steal-worthy?
- Treat evaluation protocol design as part of the mechanism story, not as background boilerplate.
- Audit future-information leakage in continual-learning pipelines, especially normalization.
- Measure forgetting in settings with genuinely different manipulation primitives, not only neighboring benchmark tasks.
- Use this paper as a baseline sanity check for later continual VLA claims.

### 14. Final decision
**Preserve as framing-critical reference.** It is not a glamorous new memory architecture, but it materially sharpens how continual VLA results should be interpreted.