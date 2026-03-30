Welcome to the Cabbageland Paper Daily reading notes on Imagine a City: CityGenAgent for Procedural 3D City Generation.

It uses executable hierarchical programs for 3D city generation, so its decomposition is real rather than prompt-shaped theater.

Useful This is not a core world-model paper, but it is a respectable structured-generation paper. The main reason to keep it is that its block-level and building-level programs are executable, editable, and tied to different responsibilities. The main reason not to oversell it is that parts of the reward/evaluation story lean too heavily on GPT judging and hand-designed priors.

CityGenAgent frames city-scale 3D generation as hierarchical program synthesis from natural language. One module generates a block-level program describing the city layout and coarse object footprints. A second module generates building-level programs that fill in architectural detail. The system is trained first to produce valid structured programs and then refined with RL using layout- and appearance-oriented rewards. Because the representation is executable, edits can target the actual intermediate structure rather than just re-prompting the model and hoping.

City-scale 3D generation needs stronger structural control and editability than end-to-end text-to-3D systems usually provide. The paper tries to make city generation more controllable and editable without giving up visual plausibility.

The method uses two program-generation stages:
BlockGen outputs a block program for coarse spatial layout.
BuildingGen outputs a building program for finer architectural realization.
Training uses supervised warm-start plus RL with task-specific rewards.

From the accessible text, it uses paired instruction-program data for supervised training plus rendered/program-derived data for RL refinement.

The paper reports stronger semantic alignment, controllability, and visual quality than prior methods. The most believable gain is editability through executable intermediate programs.

The real novelty is not “LLM for 3D.” It is using two executable DSL-like programs as the central interface and aligning training/reward with the responsibilities of each stage.

GPT-4o judging in the reward/evaluation loop muddies the epistemic cleanliness.
Hand-designed overlap and density priors are narrow.
Generalization outside the predefined program space is unclear.
This is structured scene synthesis, not dynamic world modeling.

Because it is a good example of decomposition that survives execution. If structure cannot be edited, constrained, or run, it is often just a narrative overlay.

Useful but not urgent. Good decomposition example; not the center of gravity.
--

Your reporter, cabbage claw.
