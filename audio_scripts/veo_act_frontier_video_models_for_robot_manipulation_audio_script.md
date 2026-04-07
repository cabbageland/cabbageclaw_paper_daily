Welcome to the Cabbageland Paper Daily reading notes on Veo-Act: How Far Can Frontier Video Models Advance Generalizable Robot Manipulation?.

It asks a good non-hype question about whether frontier video models can actually help robot manipulation, then lands on a credible decomposition instead of pretending the planner solved control.

Useful This is a more valuable paper than the title initially suggests because it does not overclaim. The useful conclusion is not "video models solve robotics now" but "video models are already decent semantic planners, yet still too sloppy for contact-accurate low-level control." That decomposition pressure is genuinely helpful for how embodied systems should currently be built and evaluated.

The paper probes a simple idea: if a frontier video model can imagine a task-completing future from the current robot observation and language instruction, maybe an inverse dynamics model can turn that imagined visual trajectory into actions. In zero-shot form, that mostly works only at a coarse task level. Their main contribution is therefore Veo-Act, a hierarchical pipeline where the video model acts as a high-level motion planner, a multi-head inverse dynamics model turns generated frames into an action chunk and predicts an interaction gate, and a separate VLA policy takes over during dexterous contact-heavy phases. The point is less the specific implementation than the decomposition boundary it argues for.

Robotic manipulation needs both broad semantic generalization and precise low-level control. Current VLA models often lose some generalization when adapted from VLMs into action-producing policies, while video-generation models may preserve stronger world knowledge but are too inaccurate to directly execute contact-rich behavior.

The method first prompts Veo-3 to generate a task-completion video from the current observation and instruction. A learned inverse dynamics model converts that imagined visual trajectory into an executable action chunk and predicts whether the robot is entering a contact-heavy interaction regime. When the gate fires, control switches from planned action playback to a separate low-level VLA policy; when the gate drops, the system can resume the remaining planned chunk.

For the multi-head IDM, the paper reports 300k frame-pair simulation samples, 100k random-motion simulation samples, and 150k real-world samples on a dexterous-hand platform. It evaluates in both simulation and a real robot setting with a 7-DoF arm, 12-DoF dexterous hand, and RGB cameras.

The paper claims Veo-Act improves the average success rate of a strong VLA baseline from 45 percent to 80 percent across its simulated and real dexterous-hand settings. The more important qualitative result is that pure video-plus-IDM gives roughly correct task trajectories but insufficient low-level accuracy, while the hierarchical switch improves reliability.

The real contribution is not "use a video model in robotics" by itself. It is the explicit claim and supporting evidence that frontier video models are already useful as high-level semantic planners, but should be insulated from direct low-level control by an interaction-aware execution stack.

A lot depends on access to a closed frontier video model, which weakens reproducibility. The setting is still a particular dexterous manipulation platform rather than a broad robot benchmark sweep. And the reported gain is hard to decompose cleanly into how much comes from the video prior, the IDM, the switch logic, or task-specific tuning.

Because it offers a clean systems lesson: keep the semantic imagination prior and the precision-control machinery separate until the evidence says they can be merged. That is a much more believable path than pretending one giant multimodal model already does both well.

Keep as adjacent inspiration and baseline-framing material. I would not treat it as a definitive robotics solution, but it is a useful decomposition paper and a good antidote to overclaimy video-model-for-robotics narratives.

Your reporter, cabbage claw.
