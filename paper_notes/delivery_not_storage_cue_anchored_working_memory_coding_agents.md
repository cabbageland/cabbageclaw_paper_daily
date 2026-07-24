# Delivery, Not Storage: Cue-Anchored Working Memory as a Harness Property for Coding Agents

## Basic info

* Title: Delivery, Not Storage: Cue-Anchored Working Memory as a Harness Property for Coding Agents
* Authors: Swapnanil Saha
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.20972
* Date surfaced: 2026-07-24
* Why selected in one sentence: It treats agent memory as a harness-controlled delivery channel with explicit cue semantics instead of pretending that saved notes become memory by mere existence.

## Quick verdict

**Must read**

This is one of the sharper recent agent-memory papers because it attacks the real failure boundary: the agent usually will not voluntarily store or retrieve the situational fact that matters. The best evidence is small but nasty in the right way. I inspected the arXiv PDF sections covering the abstract, introduction, two-tier design argument, cue-anchored memory model, implementation, evaluation, threats to validity, and conclusion.

## One-paragraph overview

The paper argues that current coding agents have only document memory: files, plans, and memory directories that the model must deliberately write and deliberately reread. Human expertise depends more on a second tier of situationally bound operational facts that get encoded incidentally and reappear when the situation cues them. The proposed fix is not a better note file. It is a harness-owned cue-anchored working-memory system in which each memory carries explicit trigger conditions such as path, symbol, semantic, event, or temporal cues, and the harness decides when to inject the content. The evaluation shows that voluntary memory use is basically absent even in a seeded condition, while deterministic cue-triggered delivery survives compaction and produces the only reliable memory channel in the study.

## Model definition

### Inputs
The mechanism takes the current agent context, touched paths and symbols, session events such as launch or compact-resume, semantic activity cues, and a harness-owned store of memory records with explicit trigger conditions and metadata.

### Outputs
It outputs either no delivery or a budgeted memory injection with provenance framing and staleness warnings at the exact cue point in the agent lifecycle.

### Training objective (loss)
There is no trainable model in the proposed memory mechanism. The coding agent itself is a fixed external model; the contribution is a deterministic harness-side trigger and delivery architecture.

### Architecture / parameterization
The system is a cue-anchored memory store plus a deterministic trigger engine over `{path, symbol, semantic, event, temporal}` conditions. Delivery can be implemented either through native harness hooks or through an API proxy that injects memory context on the way to the model.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It tries to solve the gap between having persistent documents and having usable operational memory in long-running coding agents.

### 2. What is the method?
The method is a two-tier memory design plus a harness-owned delivery mechanism. Memories are stored with first-class triggers, evaluated deterministically by the harness, and injected at cue points instead of relying on the agent to remember to look them up.

### 3. What is the method motivation?
The motivation is that long-running agents fail on prospective-memory behavior. They may have access to the right fact somewhere on disk, but they do not spontaneously retrieve it when the situation demands it, especially after compaction.

### 4. What data does it use?
The main evaluation uses a real feature task on a pinned Apache Camel checkout, plus a forced-compaction decay probe with planted facts and repeated compact-resume boundaries.

### 5. How is it evaluated?
It is evaluated with a controlled matrix of graded runs that vary memory surface and delivery channel, audit-log checks for trigger firing, acceptance-test completion, audit completeness, and a dedicated compaction-survival experiment.

### 6. What are the main results?
The seeded voluntary-memory arm performs `0` memory operations in `114` turns. Deterministic delivery fires in every seeded injection-equipped run with zero false alarms in the logged trigger evaluations. `39%` of intra-session rereads simply re-buy content the session had already seen before compaction. In the decay probe, conversation-only facts disappear at the first summary and remain absent from `106/108` compactions, while harness-delivered facts survive through `138/138` compact-resumes.

### 7. What is actually novel?
The novelty is the control-plane framing. The paper does not merely add another memory store or retrieval tool. It argues that the harness must own trigger evaluation and delivery if the store is supposed to function like memory rather than like a wiki.

### 8. What are the strengths?
It gives a crisp theoretical distinction, a concrete trigger vocabulary, and a rude but convincing empirical signature. The two independent delivery channels, native hooks and API proxy, also make the mechanism claim harder to dismiss as a single implementation artifact.

### 9. What are the weaknesses, limitations, or red flags?
The evaluation is still small, single-repo, and tied to one agent product and model family. Capture quality is explicitly unevaluated. Some trigger types are implemented but not exercised in graded runs, and the paper shares authorship with the evaluated harness implementation.

### 10. What challenges or open problems remain?
The big remaining problem is capture. The paper demonstrates that deterministic delivery matters, but it does not yet solve how useful operational facts get captured well in the first place without human curation.

### 11. What future work naturally follows?
Automated capture, broader trigger coverage, larger multi-repo studies, and memory architectures that integrate compaction-aware delivery with learned or semi-learned cue detection all follow naturally.

### 12. Why does this matter for cabbageland?
Cabbageland cares about memory as usable state, not decorative persistence. This paper gives a clean recipe for turning memory from an agent obligation into a harness guarantee.

### 13. What ideas are steal-worthy?
Make memory records cue-addressable rather than file-addressable. Keep trigger evaluation outside the model. Re-arm deliveries after compaction. Add provenance framing and staleness warnings to injected memories. Audit every trigger fire instead of guessing whether the memory system worked.

### 14. Final decision
**Keep it and likely build from it.** This paper is unusually explicit about where agent memory actually fails and how to move the responsibility to the right layer.
