# Permanent and Transient Representations for Continual Reinforcement Learning

## Basic info

* Title: Permanent and Transient Representations for Continual Reinforcement Learning
* Authors: Nishanth Anand; Doina Precup
* Year: 2026
* Venue / source: NeurIPS 2026; arXiv:2611.07327v1
* Link: https://arxiv.org/abs/2611.07327
* Date surfaced: 2026-11-08
* Why selected in one sentence: A slow neural value estimator and a fast, identity-aware residual dictionary give generalization and immediate correction genuinely different representations.

## Quick verdict

* Highly relevant

Preserve the complementary representation design, not a claim of solved lifelong learning. Strong ablations and explicit memory operations make this more useful than another plasticity regularizer. The large-scale implementation is about twice as slow as PQN, and the linear prediction theorem does not certify the deep controller.

## One-paragraph overview

The agent estimates action value as a permanent neural prediction plus a transient correction. The permanent network generalizes slowly across experiences; a non-parametric MinHash dictionary learns local TD corrections immediately. Observation tokens determine approximate similarity, tagged slots prevent all collisions from becoming shared identity, and LRU eviction bounds storage. Periodic consolidation trains the permanent predictor toward accumulated combined estimates, then decays transient values. The point is not simply having two learning rates: the two components have different generalization rules. This note is based on full-text main methods/results, theorem assumptions and proof outline, memory pseudocode, and relevant implementation/cost appendices, not an abstract-only read. The author-linked GitHub repository is reachable; no implementation reproduction was performed.

## Model definition

### Inputs

The permanent network receives the current observation. The transient estimator receives a tokenized observation: object-type/location tokens for symbolic grids, or quantized grayscale pixel tokens for the CIFAR image MDP. Craftax also supplies inventory and intrinsic variables. Updating uses action, reward, next observation, discount, and periodic consolidation state; the large-scale agent does not receive task boundaries.

### Outputs

For each discrete action, a permanent estimate Q_P(o,a) and transient residual Q_T(o,a). Their sum determines epsilon-greedy action choice. This is an action-value learner, not a transition model, generated trajectory, or explicit planner.

### Training objective (loss)

The fast correction uses the one-step Q-learning error: delta = r + gamma max_a' [Q_P(o',a') + Q_T(o',a')] - [Q_P(o,a) + Q_T(o,a)]. Table values receive direct TD increments distributed across tables and focal/neighbour slots by their interpolation weights. The slow component periodically regresses toward combined estimates, transferring residual information into the neural baseline; Equations 3–4 give squared-error-style semi-gradient updates. Transient values are then decayed (or reset in boundary-aware illustrative experiments). Hashing and LRU are storage operations, not learned representations or losses.

### Architecture / parameterization

A neural permanent approximator plus multiple bounded MinHash tables. The image-task permanent network follows PQN's two 1024-unit hidden layers with LayerNorm and ReLU. Hash signatures choose bins; each bin has multiple tagged observation slots. A parameter rho controls how much of a lookup comes from the exact slot versus neighbouring entries; estimates are summed over tables. The hash transform is fixed, while both neural weights and stored action values learn.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

A continual agent must adapt immediately without destroying estimates that support later reuse. Forcing a single neural feature space to serve both functions can make corrections slow or globally disruptive.

### 2. What is the method?

Add a fast residual dictionary to a slow neural value function. Tokenize observations, apply MinHash, split signatures into table indices, insert or retrieve tagged slots, and interpolate locally. Empty slots admit new observations; full bins evict their least-recently-used slot. Update the transient memory online; periodically consolidate and decay it. Importantly, similarity decides which observations can share corrections, while tags preserve distinct entries inside a similar bin.

### 3. What is the method motivation?

Complementary learning systems suggest broad, slowly acquired structure and fast episode-specific adjustment should not share every representational constraint. Here that analogy becomes an actual difference in storage and updates, rather than biological naming pasted onto an unchanged network.

### 4. What data does it use?

Online interaction in small chain/grid MDPs, CIFAR-10-based image MDPs with changing rewarding actions, and Craftax-Classic. CIFAR observations are sampled from class-dependent state emissions; these are controlled visual tasks, not unconstrained natural-image navigation. Craftax supplies structured observations, inventory, and intrinsic variables.

### 5. How is it evaluated?

Small prediction/control tasks isolate feature allocation with known boundaries. Image MDPs hide boundaries and switch the optimal action every 100K steps over 600K steps; results use 30 seeds and 90% confidence intervals. Craftax uses two streams with three seeds and a 250M-step/1024-stream benchmark with ten seeds. Baselines include PQN, neural permanent–transient, table-only, unslotted hashing, EWC, continual backprop, NEC, and boundary-aware reset/composition methods in an adaptation experiment.

### 6. What are the main results?

The slot-based hybrid adapts faster on the controlled image tasks and leads the reported Craftax curves. It exceeds Craftax return 10 before 50M steps and reaches 15 within 150M, versus over 200M for PQN(32) to reach 15. Removing the permanent network limits capacity; using a neural residual impairs rapid local adjustment; unslotted hash collisions degrade learning. Appendix A.4.2 is the necessary counterweight: at 1024 streams the implementation is about twice as slow as PQN, while two-stream wall-clock times are roughly 16–18 hours versus 14–15 hours. Sample-efficiency gains are not established wall-clock wins.

### 7. What is actually novel?

The permanent–transient value decomposition is prior work by the same authors. The extension gives its two components different feature spaces, establishes a corresponding linear prediction result, and introduces the slot-based MinHash residual estimator. Do not claim invention of episodic control, tile coding, complementary learning systems, or fast/slow learning.

### 8. What are the strengths?

The architecture exposes what changes quickly, what generalizes, and where interference is restricted. Same-bin observations need not become the same record. Ablations challenge the particular representation/storage design rather than only comparing a full system against a weak neural baseline. Explicit runtime reporting prevents a clean sample-efficiency plot from hiding implementation cost.

### 9. What are the weaknesses, limitations, or red flags?

Token overlap is a convenient bias for symbolic grids, not guaranteed task-relevant similarity under viewpoint changes, distractors, or sensor noise. Grayscale quantization sacrifices information. Tables, slots, hashes, rho, decay, and learning rates introduce substantial tuning; Craftax coordinate searches use 150M-step runs. Fixed capacity and LRU can evict rare useful situations. Appendix runtime shows sequential insertion overhead at scale. Theorem 5.5 assumes linear features, fixed-policy mixing, bounded/full-rank features, observed boundaries, i.i.d. tasks, and separated diminishing step sizes; deep off-policy control does not inherit that guarantee. The public-code repository was reachable, but these implementation claims were checked against the paper rather than by running its code.

### 10. What challenges or open problems remain?

Select what to consolidate instead of indiscriminately transferring transient corrections; separate persistent changes from temporary anomalies; retrieve semantically equivalent states without amplifying perceptual aliasing; and bound errors introduced by collisions, decay, and eviction. No learned dynamics, calibrated uncertainty, or long-horizon planning mechanism is provided.

### 11. What future work naturally follows?

Test nuisance transformations and rare revisits, evaluate collision/eviction errors directly, compare against a capacity-matched residual dictionary with alternative keys, and measure end-to-end cost including tuning. Extend beyond discrete Q-learning only with an explicit account of how memory corrections affect the policy objective.

### 12. Why does this matter for cabbageland?

It is a concrete hybrid-memory pattern for continual adaptation: preserve broadly reusable knowledge while allowing a local override that can later be consolidated or forgotten. Its modularity earns the label because it changes representation, credit assignment, retrieval, and forgetting. It is not yet a neurosymbolic world model merely because observations become tokens.

### 13. What ideas are steal-worthy?

- Separate similarity routing from record identity: approximate bins plus exact-ish tags and multiple slots.
- Use a fast residual to correct a stable model without immediately rewriting it.
- Make generalization and forgetting explicit knobs rather than accidental optimizer behaviour.
- Evaluate ablations at equal memory, preprocessing, tuning effort, and wall-clock budget—not only environment steps.

### 14. Final decision

Keep as an architecture and baseline reference for continual RL and hybrid memory. Before transplanting it into visual embodied systems, validate the key space under nuisance variation and account for insertion/runtime overhead. The most transferable claim is complementary representations, not universal convergence or biological fidelity.
