# CAGE: Certified Authorization under Typed-Return Uncertainty for Tool-Using Agents

## Basic info

* Title: CAGE: Certified Authorization under Typed-Return Uncertainty for Tool-Using Agents
* Authors: Blaise Delattre, Cong Wang, Yang Cao
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2607.29190
* Date surfaced: 2026-08-03
* Why selected in one sentence: It identifies a concrete safety bug in tool authorization, separate certification of categorical and numerical uncertainty does not compose, and replaces it with a joint-neighborhood certificate.

## Quick verdict

**Keep it**

I inspected the arXiv HTML paper, especially the threat model, the CAGE certification method, the experiment map, and the discussion and scope section. This is a strong runtime safety paper because it names a real failure mode rather than another vague "agent uncertainty" complaint: a tool action can be safe under each marginal check and still unsafe under the combined typed-return perturbation. The paper's own limits are also important. The guarantee is for a single authorization decision under a declared budget, with validated typed-return construction, enumerable discrete neighborhoods, and explicit fidelity assumptions for learned gates.

## One-paragraph overview

The paper studies tool-using agents that act on typed returns containing provenance or categorical fields plus numerical values. Existing runtime gates usually authorize the observed return-action pair at a point, or certify categorical and numerical uncertainty separately. CAGE shows that this is not enough. A small binding fault plus bounded numerical drift can jointly make an action unsafe even when each channel looks safe alone. The method therefore certifies the actual joint neighborhood. It enumerates the discrete branch space exactly, runs a sound continuous certificate inside each branch, and only allows the action if every branch passes. It offers an exact backend when the policy is executable and learned-gate backends under explicit gate-policy fidelity assumptions.

## Model definition

### Inputs
The system takes a typed tool return, a candidate action, an authorization policy or learned authorization gate, and a declared uncertainty budget over discrete binding faults and continuous numerical drift.

### Outputs
It outputs an allow or deny decision, together with a certificate that the action remains authorized throughout the declared joint neighborhood.

### Training objective (loss)
The exact backend is not a learned model. The learned backends certify a trained gate under explicit fidelity assumptions, but the paper's core contribution is the certification framework rather than a new learning objective.

### Architecture / parameterization
The architecture is an authorization wrapper with three levels: CAGE-Exact for executable policies, CAGE-Lip for a Lipschitz-style learned gate, and CAGE-RS for a smoothed black-box gate. All share the same basic structure of discrete branch enumeration plus per-branch continuous certification.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?
It is trying to solve the case where authorization decisions depend on uncertain typed tool returns and pointwise or marginal checks fail to protect against small but realistic return-binding errors.

### 2. What is the method?
The method is CAGE. It defines a joint neighborhood over one admissible binding fault plus bounded numerical drift, enumerates the discrete branches of that neighborhood, certifies the continuous perturbation inside each branch, and permits an action only if all branches remain safe.

### 3. What is the method motivation?
Tool authorization often treats the observed return as ground truth. But if the return is slightly misbound or numerically off, a locally safe decision can become unsafe. The motivation is to certify the decision that should have been authorized under plausible correctly bound returns, not just the literal observed one.

### 4. What data does it use?
The evaluation spans synthetic finance, SRE, and operations settings, policy-as-code with Open Policy Agent, regulatory and real-transaction settings, OpenFisca boundary cases, and live-system style settings including k8s, MCP, and Marble-style decision engines.

### 5. How is it evaluated?
The paper first establishes the existence of joint-gap witnesses, then measures the soundness-autonomy trade-off, then checks for committed side effects. It also studies dependence on attack strategy, budget choice, fidelity assumptions, and policy stationarity.

### 6. What are the main results?
Across the reported settings, CAGE removes measured in-budget false allows that pointwise gates admit while retaining useful autonomy. The paper also quantifies what happens when assumptions weaken, such as budget escape and constructor corruption, instead of pretending the certificate is universal.

### 7. What is actually novel?
The novelty is the non-composition result and the response to it. The paper does not just add a wider safety margin. It shows that separate certification of categorical and numerical channels is structurally wrong for this problem, then certifies the joint neighborhood directly.

### 8. What are the strengths?
The threat model is concrete, the certification ladder is honest about what each backend guarantees, and the evaluation spans more than one toy domain. The paper also does a good job distinguishing policy-certified versus gate-certified claims.

### 9. What are the weaknesses, limitations, or red flags?
The guarantee is local and single-step. Cross-turn accumulation, tool selection, prompt injection resistance, MCP metadata issues, and multi-step execution remain outside the certificate. Learned backends also need continued fidelity auditing.

### 10. What challenges or open problems remain?
Sequential certification, provenance-conditioned policies, live measurement of binding faults, and tighter integration with runtime validation infrastructure remain open.

### 11. What future work naturally follows?
Extending the certificate beyond one step, tightening fidelity monitoring for learned gates, and treating multi-tool workflows as certified trajectories rather than isolated decisions would all be natural next steps.

### 12. Why does this matter for cabbageland?
It matters because cabbageland works with tool-using agents, typed tool returns, and MCP-like runtime surfaces. The paper provides a clean pattern for when permissioning should depend on more than the raw observed return.

### 13. What ideas are steal-worthy?
Model typed-return uncertainty as a joint neighborhood rather than two marginal channels. Keep an explicit assumption ladder from policy-certified to learned-gate-certified behavior. Measure and report budget escape separately instead of pretending out-of-budget failures invalidate the in-budget certificate.

### 14. Final decision
**Keep it.** This is a genuinely useful safety paper with a crisp threat model, a real technical point, and direct relevance to tool-using agents.
