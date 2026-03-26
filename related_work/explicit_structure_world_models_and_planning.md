# Explicit Structure in World Models and Planning

## Current pattern

A useful split is emerging between papers that merely generate futures and papers that impose structure that actually changes planning.

The latter are still rare, but more interesting.

Four recurring forms of useful structure are showing up:

1. **Temporal abstraction over reusable behaviors**
   - **Compositional Planning with Jumpy World Models** is a good example.
   - It predicts state occupancy under pre-trained policies across multiple timescales.
   - That matters because the planning object changes from primitive actions to behavior chunks.

2. **Symbolic task structure plus perceptual grounding**
   - **H-WM** is a useful example.
   - Its symbolic state/action layer gives long-horizon consistency, while visual latent subgoals keep the controller grounded.
   - The caution is that this kind of structure often depends on costly symbolic scaffolding.

3. **Geometric / physical constraints in generative composition**
   - **Interact3D** is adjacent but illustrative.
   - It treats compositional generation as registration plus collision-aware optimization, not just unconstrained mesh hallucination.
   - This is useful because it moves composition from style to constraint satisfaction.

4. **State bottlenecks designed for planning rather than reconstruction**
   - **Planning in 8 Tokens / CompACT** is a good example.
   - It asks a sharper question than most tokenizer papers: what is the smallest latent state that still preserves action-relevant semantics and spatial relations for planning?
   - This matters because token count is not a cosmetic detail; it determines whether decision-time rollouts are actually usable.

## Working synthesis

“Structure” only deserves the name if it changes at least one of these:
- what the model predicts,
- what the planner searches over,
- what constraints are enforced,
- what intermediate state can be inspected,
- or how control is conditioned.

If none of those change, the structure is probably branding.

A related practical rule is emerging too: if a paper says it improves planning, ask whether it changes the **planning substrate** or merely makes the generated samples look better. The planning substrate can be the planning object, the predictive state, or the rollout cost. If none of those move, the claimed planning advance is often vapor.

## Useful lenses for future scouting

### 1. Planning object lens
Ask what the planner is actually choosing over:
- primitive actions,
- skills / policies,
- symbolic actions,
- object edits,
- latent goals,
- or graph/state transitions.

If the answer is still “token soup,” the paper is probably less compositional than it claims.

### 2. Predictive state lens
Ask what future object is modeled:
- one-step observations,
- successor occupancy,
- symbolic states,
- latent subgoals,
- object-centric graphs,
- physical constraints.

Good structure changes this object in a way aligned with the downstream task.

Also ask how expensive that predictive state is. A planning state that is too large to roll out is often structure in name only.

### 3. Grounding lens
Ask whether the explicit structure is actually connected to perception and control.
A symbolic layer that cannot survive perception noise, or a latent world model that cannot influence action meaningfully, is only half a solution.

### 4. Constraint lens
Ask what is enforced explicitly:
- temporal consistency,
- physical feasibility,
- state preconditions/effects,
- collision avoidance,
- persistence,
- or uncertainty bounds.

Constraint-free “structured” generation is often just aspiration.

### 5. Utility lens
Ask what the structure buys downstream:
- faster planning,
- stabler long rollouts,
- better checkpoint selection,
- better data generation,
- more legible failure analysis,
- or easier intervention.

If the answer is only “slightly prettier samples,” the structure is probably decorative.

## Practical research takeaway for cabbageland

The promising direction is not generic world modeling.
It is **typed predictive state matched to the planning object**.

Useful near-term instincts:
- plan over reusable behaviors when they exist,
- keep task-structure state distinct from perceptual grounding state,
- prefer compact inspectable subgoals over long fragile rollouts,
- force the state bottleneck to justify its computational cost,
- and distrust any paper that says “hierarchical” or “structured” without changing the actual planning contract.
