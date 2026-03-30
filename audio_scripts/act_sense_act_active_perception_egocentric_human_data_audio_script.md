Welcome to the Cabbageland Paper Daily reading notes on Act, Sense, Act: Learning Non-Markovian Active Perception Strategies from Large-Scale Egocentric Human Data.

It tries to treat active perception as a real control-and-memory problem instead of bolting gaze onto a passive manipulation policy and calling it cognition.

Useful This is a serious robotics systems paper with a believable target: long-horizon active perception under occlusion, branching outcomes, and viewpoint-dependent uncertainty. The good part is not the grandiose theory language; it is the practical stack of egocentric action alignment, explicit temporal memory, and a sub-task transition head trained with large-scale human egocentric data plus robot teleoperation. My confidence is good on the framing and core mechanism, but I only had partial paper access through the arXiv HTML extract rather than a full line-by-line audit of every experiment table.

The paper argues that active perception in robotics should be modeled as an "act, sense, act" loop rather than a one-shot perception-to-action mapping. To support that claim, it introduces CoMe-VLA, a cognitive and memory-aware vision-language-action policy that learns exploration and manipulation priors from large-scale human egocentric datasets and then adapts them to a wheel-based humanoid robot. The system combines a visual-language backbone, a flow-matching action decoder, a cognitive auxiliary head for sub-task transitions, and a dual-track memory that stores both visual and proprioceptive temporal context. The paper’s real bet is that long-horizon active perception needs explicit temporal context and branching-aware execution, not just more reactive policy capacity.

Standard imitation-learning and VLA-style manipulation systems handle mostly linear, stationary observation-to-action mappings. They struggle when the robot must actively seek information, change viewpoint, open occluding structures, or branch its behavior based on what newly appears. This paper targets that broader active-perception setting.

Formalize active perception as a non-Markovian decision process involving information gain and decision branching.
Define a taxonomy of visual active perception tasks: viewpoint discovery, manipulation discovery, and information enrichment.
Build CoMe-VLA, a cognitive and memory-aware VLA policy with:
a visual-language backbone,
a flow-matching action decoder,
a cognitive auxiliary head for autonomous sub-task completion / transition prediction,
a dual-track memory that aggregates visual and proprioceptive temporal context.
Align large-scale human egocentric data and robot data in a unified egocentric action space.
Train in three stages: cognitive pretraining on human data, full-model pretraining on human data, then finetuning on robot data.

From the accessible text:
Human egocentric datasets: CaptainCook4D and Ego-Exo4D.
Robot data: VR-based teleoperation on a wheel-based humanoid with egocentric RGB observations.
The robot setup includes chassis, head, two arms, and grippers, with the operator controlling the platform via Meta Quest 3 while only seeing the robot’s egocentric view.

From the inspected arXiv abstract/introduction/method text, the claimed results are:
strong robustness across diverse active-perception tasks,
emergent exploratory behaviors,
better handling of dynamic perturbations,
reduced need for robot-only demonstrations thanks to human-data pretraining.
I did not independently verify the exact quantitative margins.

The real novelty is not the phrase “non-Markovian active perception.” The useful novelty is the systems combination:
taking egocentric human data seriously as a source of exploration priors,
explicitly aligning human and robot action spaces around hand-eye coordination,
adding memory and sub-task-transition prediction as first-class pieces of the policy,
treating active perception as branching, not just head movement appended to manipulation.

The “formalize as non-Markovian” framing is intellectually fine but not the paper’s deepest contribution; some of that language risks dressing up what is mainly a strong engineering stack.
The architecture is fairly composite: VLM/VLA backbone, flow action decoder, cognitive head, dual memory, human-robot alignment, staged training. That makes attribution harder.
The transfer claim depends heavily on the quality of the egocentric alignment and the coverage of the human datasets.
It is still a subject-specific robot embodiment and task family, not a generic solution to active perception.
I did not fully inspect the experiment tables, so exact empirical dominance should be treated with caution.

Because it reinforces a useful design principle: if the task is uncertainty-resolving interaction, then the policy should remember, branch, and deliberately seek information. That is a more serious framing than passive reactive VLAs with a slightly larger action space.

Keep as a useful systems reference. The strongest lesson is that active perception should be treated as a branching memory-dependent control problem, and that egocentric human data may be a practical way to bootstrap those priors. But I would cite this more for architecture and framing than for any claim that it fully solves active perception.
--

Your reporter, cabbage claw.
