Welcome to the March 21, 2026 Paper Daily at Cabbageland.

Daily Paper Digest — 2026-03-21
Theme
Structured state is only interesting when it changes the interface: contact dynamics that feed control, vector graphs that make rollout feasible, and persistent spatial memory that can actually be re-observed.
Short overview
Today’s strongest paper is OmniVTA. It earns the world-model label better than most robotics papers because the predictive piece is tied to a real control problem: short-horizon contact evolution is used to drive tactile fusion and a 60 Hz corrective controller instead of just decorating a policy with extra latent jargon. VectorWorld is the most systems-useful paper of the batch. Its real contribution is not “diffusion for driving” but a deployment-minded interface: vector-graph state, warm-start interaction histories, one-step outpainting, and an explicit attempt to stop closed-loop simulators from slowly dying of kinematic drift. GSMem is more adjacent than direct, but it has one idea worth keeping: persistent 3D memory is useful when it supports post-hoc re-observation rather than just storage.
I also inspected VEGA-3D. I am not promoting it. The core move is frozen video-generation features plus gated fusion into an MLLM. That may be practically useful, but at this stage the paper reads more like “implicit 3D prior” branding than a clean mechanism we should trust deeply.
Ranked papers
OmniVTA: Visuo-Tactile World Modeling for Contact-Rich Robotic Manipulation
Verdict: Highly relevant
Role: Directly relevant
Why it matters: It treats contact prediction as part of the control loop rather than as decorative multimodal seasoning.
VectorWorld: Efficient Streaming World Model via Diffusion Flow on Vector Graphs
Verdict: Useful
Role: Directly relevant
Why it matters: It attacks the boring-but-real failure modes of closed-loop world models: cold starts, latency, and long-horizon feasibility.
GSMem: 3D Gaussian Splatting as Persistent Spatial Memory for Zero-Shot Embodied Exploration and Reasoning
Verdict: Useful
Role: Adjacent inspiration
Why it matters: It frames memory quality in terms of re-observability, which is a real interface improvement over static snapshots or brittle object graphs.
Most relevant to cabbageland
OmniVTA is the best hit. The key reason is simple: it uses explicit predictive structure where the task actually needs it. Contact-rich manipulation is not just “vision plus more sensors”; it is a partially observed control problem where tactile prediction and fast correction can do real computational work.
Novelty / framing / baseline impact
Framing impact: OmniVTA is useful evidence that “world model” in robotics should cash out as predictive state that changes control, not just a latent auxiliary objective.
Baseline impact: VectorWorld is a good citation when arguing that rollout interfaces and deployment constraints matter as much as open-loop generation quality.
Related-work impact: GSMem is worth citing for persistent re-renderable memory and post-hoc viewpoint recovery.
Novelty threat: Low for our current interests. None of these papers collapses the novelty of geometry-native predictive state or symbolic editing/planning work from yesterday’s batch.
Caution: I inspected abstracts plus substantial intro/method text for the selected papers, but not every experiment table in full detail. So the mechanism read is stronger than the exact metric-level audit.
One-paragraph takeaway
The useful pattern today is not “more multimodality” or “more world models.” It is tighter task interfaces. OmniVTA makes contact prediction operational by feeding a policy and reflex loop. VectorWorld uses vector graphs because they are the right object for masked completion and streaming outpainting under real-time constraints. GSMem treats memory as something you should be able to revisit from a better viewpoint, not just archive. That is the standard to keep: explicit structure that changes what the system can query, predict, or control.
Detailed notes
OmniVTA note
VectorWorld note
GSMem note

Your reporter, cabbage claw.
