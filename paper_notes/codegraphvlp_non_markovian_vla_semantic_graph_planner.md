# CodeGraphVLP: Code-as-Planner Meets Semantic-Graph State for Non-Markovian Vision-Language-Action Models

## Basic info

* Title: CodeGraphVLP: Code-as-Planner Meets Semantic-Graph State for Non-Markovian Vision-Language-Action Models
* Authors: Khoa Vo, Sieu Tran, Taisei Hanyu, Yuki Ikebe, Duy Nguyen, Bui Duy Quoc Nghi, Minh Vu, Anthony Gunderman, Chase Rainwater, Anh Nguyen, and Ngan Le
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2604.22238
* Date surfaced: 2026-04-28
* Why selected in one sentence: It is one of the cleaner recent attempts to replace long-horizon VLA history mush with an explicit persistent state and a planner that actually operates over it.

## Quick verdict

**Highly relevant**

This paper is pointed at a real problem and uses a mechanism that actually matches the complaint. Instead of pretending longer context or repeated VLM prompting solves non-Markovian manipulation, it builds a persistent semantic graph and lets an executable planner query that state for progress checks and subtask selection. I inspected the abstract and substantial method text from the arXiv HTML, so confidence is good on the architecture and motivation, but weaker on appendix-only implementation details and the full breadth of evaluation tables.

## One-paragraph overview

CodeGraphVLP is a hierarchical manipulation system for long-horizon tasks where the next correct action depends on past evidence that may no longer be visible. The core idea is to maintain an online semantic graph of task-relevant entities, attributes, and relations, then run a synthesized code planner over that graph to estimate progress and choose the next subtask. The planner also emits the relevant objects for that subtask, which are used to construct clutter-suppressed visual prompts for the downstream VLA executor. So the main contribution is not “code generation” alone. It is using code over an explicit state as the interface between long-horizon reasoning and short-horizon control.

## Model definition

### Inputs
The full system receives multi-view RGB observations, proprioceptive state, and a natural-language instruction. The semantic-graph builder also uses segmented object masks, VLM relevance judgments, CLIP-based cross-view matching, and simple geometric relation induction. The code planner itself takes the current semantic graph as input.

### Outputs
The online planner outputs the next subtask instruction and the set of subtask-relevant objects. The downstream VLA then outputs the next action chunk for robot control.

### Training objective (loss)
The accessible text did not expose one unified end-to-end loss for the whole system. The VLA executor is a pretrained action policy used downstream, while the planner is synthesized as executable code from an LLM prompt rather than trained in the standard supervised sense. The perception stack uses off-the-shelf segmentation, tracking, CLIP features, and VLM filtering. So the key mechanism here is mostly systems composition around explicit state, not a novel monolithic loss.

### Architecture / parameterization
A hybrid stack: segmentation and tracking for object grounding, a persistent semantic graph for explicit state, an LLM-synthesized Python planner that queries the graph, clutter-suppressing visual-language prompt construction, and a downstream VLA executor.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
Standard VLAs are usually reactive short-horizon policies that assume the latest observation is enough for deciding the next action. That breaks in non-Markovian tasks where the critical evidence may have appeared earlier, become occluded, or be hard to recover in clutter. History-augmented VLAs help somewhat but are expensive and still unstructured, while VLM-in-the-loop planners are slow and rely too much on language-only interfaces.

### 2. What is the method?
- Build an explicit semantic graph whose nodes are task-relevant objects and whose edges represent relations like in, on, and near.
- Update that graph online from multi-view observations using segmentation, cross-view association, tracking, and relation refresh.
- Prompt an LLM once at initialization to synthesize an executable planner over the graph API.
- Repeatedly run that planner online to check progress, select the next subtask, and identify subtask-relevant objects.
- Construct clutter-suppressed visual and textual prompts from those relevant objects.
- Feed those grounded prompts into a downstream VLA for action execution.

### 3. What is the method motivation?
The paper’s motivation is that neither raw history nor snapshot-based VLM replanning gives a clean interface for long-horizon manipulation. History is costly and unstructured. Repeated VLM calls are slow and brittle in clutter. A persistent symbolic-ish state is supposed to hold the sparse facts that matter, and code over that state is supposed to make progress reasoning cheap, explicit, and less dependent on prompt-time luck.

### 4. What data does it use?
The accessible text says the evaluation uses three real-world tabletop manipulation tasks with non-Markovian dependencies, including one task that emphasizes clutter-robust reasoning. I did not inspect the appendices in full, so I am not claiming broader dataset details or sample counts beyond what was visible in the HTML.

### 5. How is it evaluated?
It is evaluated against strong VLA baselines, history-enabled variants, and VLM-in-the-loop alternatives. The key reported axes are task completion on real-world long-horizon tasks and planning latency, with ablation studies for the semantic graph, code planner, and clutter-suppressed prompting components.

### 6. What are the main results?
The visible text claims better task completion than the baseline families above, plus substantially lower planning latency than keeping a VLM in the loop for repeated progress checks. I trust the qualitative result and the intended comparison more than any exact number here because I did not audit every table.

### 7. What is actually novel?
The real novelty is the combination of a persistent semantic graph, code-based progress reasoning over that graph, and using the planner’s object outputs to create clutter-suppressed prompts for the VLA. None of those ingredients alone is unprecedented, but the integration is coherent and aimed at the right failure mode.

### 8. What are the strengths?
- It uses explicit state for a situation that actually needs explicit state.
- The planner interface is meaningfully cheaper and clearer than repeated VLM prompting.
- It recognizes that grounding errors in clutter are often downstream of a bad interface, not only a weak controller.
- The decomposition is legible enough to debug component-wise.

### 9. What are the weaknesses, limitations, or red flags?
- The semantic graph quality depends on perception, association, and relation heuristics, so upstream errors can silently poison the planner.
- The relation set looks fairly lightweight, which may be enough for tabletop tasks but not for richer physical manipulation.
- The planner is only as good as the generated graph API code, and I did not inspect how robust that synthesis is across task variation.
- This is still a fairly hand-built systems stack, which may limit scale or portability.
- There is always a risk that “code planner” is doing less real reasoning than the framing suggests if the tasks are narrow.

### 10. What challenges or open problems remain?
The open question is how far this style of explicit-state manipulation can scale before graph maintenance becomes the new bottleneck. Another problem is uncertainty: the system needs a good way to know when the graph is wrong or incomplete. More complex tasks will also require richer relations, temporal persistence, and maybe causal state rather than simple spatial relations.

### 11. What future work naturally follows?
- Add uncertainty and confidence estimates to graph updates and planner decisions.
- Learn richer relational state representations without collapsing back into opaque latent mush.
- Use the explicit graph for counterfactual planning or failure diagnosis, not just subtask selection.
- Test the same interface on harder tasks with more object novelty and longer temporal gaps.

### 12. Why does this matter for cabbageland?
Because it is a clean example of a principle cabbageland keeps caring about: if long-horizon behavior depends on facts that can disappear from view, then those facts should probably live in an explicit state rather than in vibes spread across a history buffer. The graph is imperfect, but the interface discipline is right.

### 13. What ideas are steal-worthy?
- Persistent task state as a graph of entities and relations, updated online.
- Executable planner logic over explicit state instead of repeated language-only replanning.
- Having the planner emit both subtask text and relevant objects, so the control policy sees less clutter.
- Treating non-Markovian manipulation as a state-interface problem, not just a bigger-context problem.

### 14. Final decision
**Keep it.** This is not a solved blueprint for general manipulation, but it is one of the more structurally honest recent long-horizon VLA papers. The graph may be crude and the stack may be brittle, but the decomposition is worth remembering.