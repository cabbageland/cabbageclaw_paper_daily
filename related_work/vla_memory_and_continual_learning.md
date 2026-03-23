# VLA Memory and Continual Learning

## Current pattern

Recent VLA memory papers are converging on an uncomfortable truth: there is no single good memory representation for all tasks.

Three useful distinctions are emerging:

1. **Timescale matters**
   - Recent dense perception is useful for occlusion, local dynamics, and manipulation correction.
   - Long-horizon task progress needs stronger compression.
   - Papers like **MEM** are useful because they admit this explicitly instead of pretending more frames in context equals solved memory.

2. **Memory type matters**
   - Temporal, spatial, object, and procedural memory are not interchangeable.
   - **RoboMME** is useful because it makes these distinctions legible in evaluation.
   - This should make us more skeptical of broad “memory module helps” claims from narrow task suites.

3. **Adaptation regime matters**
   - Continual-learning intuitions imported from smaller models do not automatically hold for large pretrained VLAs.
   - **Simple Recipe Works** suggests that pretrained representations + LoRA + on-policy RL can preserve competence much better than expected.
   - That does not remove the need for memory, but it does alter what counts as a serious continual-learning baseline.

## Working synthesis

The field still tends to collapse three different questions:

- How should an agent represent history during a task?
- How should we evaluate whether a memory design actually helps?
- How should a pretrained VLA keep adapting across tasks without losing prior competence?

These are related, but not identical.

A good paper should say which problem it is solving.
If it does not, the word “memory” is probably doing too much work.

## Useful lenses for future scouting

### 1. Representation lens
Ask what the memory object actually is:
- raw frames
- compressed video tokens
- language summaries
- object/state graphs
- recurrent latent state
- retrieved episodes
- explicit world-state cache

If the paper claims structure, check whether the structure changes retrieval, update, or control behavior.

### 2. Update lens
Ask how memory is updated:
- append-only context
- learned recurrence
- explicit write operation
- summarization
- overwrite / edit semantics
- retrieval conditioned on current state

Most current VLA work is still weak here. Memory often exists, but memory management does not.

### 3. Evaluation lens
Ask what kind of memory demand is being tested:
- counting / temporal order
- occlusion / spatial permanence
- referential identity
- procedural imitation
- long-horizon subtask progress
- causal intervention / counterfactual state

If the benchmark does not separate these, strong conclusions are suspect.

### 4. Continual-learning lens
Ask whether the paper is really about:
- within-episode memory,
- cross-task adaptation,
- or both.

Those are often blurred together. They should not be.

## Practical research takeaway for cabbageland

The promising direction is not “one giant memory module.”
The promising direction is **typed memory with explicit update and retrieval semantics**, paired with evaluation that makes different failure modes visible.

Near-term useful design instincts:
- use different substrates for different timescales,
- benchmark memory by type,
- assume stronger continual-learning baselines for large pretrained VLAs,
- and distrust any paper that says “memory” while leaving the stored object, update rule, and evaluation target vague.
