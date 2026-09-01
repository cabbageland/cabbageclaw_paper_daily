# Measure Before You Manage: Evaluating Agent Working Memory in Coding Agents

## Basic info

* Title: Measure Before You Manage: Evaluating Agent Working Memory in Coding Agents
* Authors: Le Chen, Zishen Wan, Baixi Sun, Xiaolong Ma, Chih-Hsuan Yang, Feng Yan, Sheng Di, Franck Cappello, Rajeev Thakur
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2608.31057
* Date surfaced: 2026-09-01
* Why selected in one sentence: It is a rare memory paper that spends more effort auditing what was really measured than selling a flashy policy.

## Quick verdict

* Must read

I inspected the full arXiv HTML text, especially the typed-object working-memory model, the calibration versus held-out comparisons, the retrieval-study caveats, and the four-level evaluation framework. This earns a preserved note because it is more valuable as a measurement correction than as a new memory trick, and that is exactly why it matters.

## One-paragraph overview

The paper studies coding-agent working memory as a heterogeneous object system rather than as a uniform token pool. Instructions, artifacts, tool outputs, and agent-generated state differ in size, retention, representation, and lifecycle behavior, so a memory policy that treats them as the same thing is already standing on a bad abstraction. The authors characterize that heterogeneity across archived coding-agent traces, then examine two semantically informed management policies: an object-aware compression heuristic and a retrieval-based policy. The deeper result is that apparently fair comparisons can still be misleading. A nominal budget cap does not guarantee matched delivered context, management work, or even meaningful outcome interpretation. The paper ends by proposing a four-level frame for reporting memory studies: stored state, delivered context, management work, and task/process outcome.

## Model definition

### Inputs
Typed working-memory objects such as instructions, artifacts, tool outputs, and agent-generated state, along with metadata including size, age, access behavior, dependencies, and representation form.

### Outputs
Managed message plans under different memory policies plus descriptive accounting statistics and process metrics such as repeated tool calls.

### Training objective (loss)
There is no central learned model. The object-aware policy is a hand-specified heuristic calibrated on development tasks, and the retrieval policy adapts recency, relevance, and importance scoring from prior work.

### Architecture / parameterization
An existing coding-agent host maintains a working-memory object store with raw, compressed, summary, and pointer forms plus recall support; the paper evaluates policy choices within that system.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It asks how semantic heterogeneity should affect both memory management and the evaluation of memory policies in coding agents.

### 2. What is the method?
First, measure typed-object memory behavior across archived trajectories. Then evaluate an object-aware compression policy and a retrieval-based policy, while explicitly auditing what the comparisons really control.

### 3. What is the method motivation?
If different memory objects serve different roles and decay differently, then a single budget number or uniform compression rule is a poor abstraction for both design and evaluation.

### 4. What data does it use?
Fifty-five archived coding-agent trajectories for characterization, 15 SymPy calibration tasks, 8 held-out tasks across five other repositories, and 24 retrieval follow-up task blocks.

### 5. How is it evaluated?
By typed-object accounting, paired repeated-call contrasts, held-out comparisons, delivered-context audits, auxiliary-call counts, wall time, and a replay-based serving-boundary check.

### 6. What are the main results?
Tool outputs account for 55.5% of pooled content volume and 40.2% of retention-weighted cost, while artifacts account for 28.3% and 38.9%. The object-aware policy improves the calibration repeated-call metric against FIFO by -1.633, but the held-out contrast shrinks to -0.500 and no held-out comparison survives Holm correction. In the retrieval study, shared caps still do not equalize delivered context, GA adds 285 importance calls, and OA adds 169 summary calls. The paper is explicit that many outcomes are process evidence rather than repair-success evidence.

### 7. What is actually novel?
The novelty is the measurement frame, not the presence of compression or retrieval. The paper separates multiple layers that memory papers usually collapse into one headline number.

### 8. What are the strengths?
It is unusually honest about calibration leakage, held-out weakness, instrumentation defects, and the difference between a cap on admissible state and actual delivered context.

### 9. What are the weaknesses, limitations, or red flags?
The archive is small, clustered, and only partly supports valid repair outcome claims. The main process metric is repeated calls rather than official task success, and some lifecycle signals in the object-aware system are known to be defective.

### 10. What challenges or open problems remain?
Running the same style of analysis on larger, cleaner, fully reconstructable coding-agent archives with real success metrics and corrected lifecycle instrumentation.

### 11. What future work naturally follows?
Better typed-object utility models, cleaner access and invalidation signals, and evaluation suites that jointly report delivered context, management overhead, and real task outcomes.

### 12. Why does this matter for cabbageland?
Because coding-agent memory is a live concern here, and this paper gives a much better standard for evaluating it than "we used fewer tokens and the number went up."

### 13. What ideas are steal-worthy?
Report memory studies at four levels. Distinguish nominal cap from delivered context. Treat management work as part of the intervention cost, not as invisible background.

### 14. Final decision
Keep as a preserved note. The paper's main gift is not a new policy. It is a better standard for what a memory-policy claim has to survive.
