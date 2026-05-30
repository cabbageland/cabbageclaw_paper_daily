Welcome to the Cabbageland Paper Daily reading notes on SAM: State-Adaptive Memory for Long-Horizon Reasoning Agent.

It turns agent memory into an explicit page-and-cue interface, then actually trains that interface instead of treating memory as prompt folklore.

Highly relevant This is one of the cleaner recent memory papers because the structure is real and the decomposition boundary is legible. The core idea is not exotic, but it is much less mushy than most summarize-or-retrieve agent memory work. The main caveat is that the training recipe leans heavily on frontier-model supervision and reward scaffolding, so the memory mechanism is cleaner than the full practical recipe.

SAM equips a frozen reasoning agent with an external memory module that converts long interaction histories into contiguous raw pages plus compact memory cues. The cues stay in the live context as lightweight handles describing what a page established, resolved, or left open, while the raw pages are stored externally. When the agent later needs old information, it selects relevant cues according to its current intent, and the memory model reconstructs targeted support from the associated raw pages. The paper then trains this memory module with supervised targets from stronger models and a tree-structured RL objective that gives credit to individual memory actions rather than only the trajectory’s final outcome.

Long-horizon agents fail when important evidence is scattered far back in the trajectory and becomes relevant only later. Simple truncation, rolling summaries, or naive retrieval either lose detail or fail to match the agent’s current need.

The method partitions history into contiguous pages once a token budget is reached. Each page is converted into a compact memory cue that stays visible in context, while the full page is stored externally. Later, the agent can issue a recall intent, select candidate cues, and ask the memory model to reconstruct the most relevant information from the corresponding raw pages.

Training uses public agent-trajectory releases from OpenSeeker and OpenResearcher, filtered to remove trivial or incorrect trajectories. Evaluation uses BrowseComp, BrowseComp-ZH, WideSearch, and HLE.

SAM is the strongest context-management method on both tested backbones. On GLM-4.7, the four-benchmark average rises from 49.4 with no context management to 57.0 with SAM. On Qwen3.5-35B-A3B, the average rises from 44.5 to 48.8. The largest gains show up on BrowseComp-style long-range browsing benchmarks, which is exactly where memory pressure should bite hardest.

The main novelty is the memory contract, not the phrase “state-adaptive.” Memory cues are explicitly not treated as final summaries, only as persistent handles to raw pages. The second real contribution is the RL credit-assignment scheme for memory actions via a memory-call tree and oracle-anchored reward.

The training recipe is expensive and somewhat baroque, relying on stronger frontier models both for supervised targets and committee-style reward shaping. The memory pages are simple contiguous chunks rather than semantically segmented episodes, which keeps the system simple but may also waste capacity. And the evaluation is benchmark-heavy rather than deployment-heavy, so practical failure modes under messy real-world tasks remain unclear.

Because it replaces vague “long context” talk with an actual memory interface. The raw-page plus cue split is a useful design pattern for any agent that needs continuity without drowning in its own transcript.

Keep and cite. This is not the final answer to agent memory, but it is one of the more legible recent attempts and has reusable design ideas.

Your reporter, cabbage claw.
