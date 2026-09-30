# FORM: Robot Manipulation through Direct Material Law Identification

## Basic info

* Title: FORM: Robot Manipulation through Direct Material Law Identification
* Authors: Stepan Tretiakov, Ruihan Zhao, Cheng-Hsi Hsiao, Xingjian Li, Adam Thorpe, Hassan Iqbal, Sandeep Chinchali, Ufuk Topcu, Krishna Kumar
* Year: 2026
* Venue / source: arXiv:2609.38105
* Link: https://arxiv.org/abs/2609.38105
* Date surfaced: 2026-09-30
* Why selected in one sentence: It recovers explicit material laws from one robot interaction and uses them directly for planning new deformable-object actions.

## Quick verdict

* Highly relevant

This is the robotics paper worth keeping today because the mechanism is explicit. Instead of learning another opaque dynamics model, FORM identifies coefficients of a constitutive law through weak-form momentum balance and then uses the recovered law in an MPM simulator. The limitation is that the method still needs usable motion reconstruction and an appropriate material-law basis.

## One-paragraph overview

FORM, short for From Observed Response to Material laws, estimates material properties from a single probing interaction. The robot observes material motion and contact loads, reconstructs deformation, expresses stress as a linear combination of candidate constitutive responses, and uses weak-form momentum balance to turn identification into a linear least-squares problem. Because the equations are assembled using the same material point method discretization as the forward simulator, the recovered coefficients can be used directly for prediction and motion planning. In simulation and hardware tasks, the method identifies elastic, granular, elastoplastic, and fluid behavior far faster than iterative baselines while enabling material-specific manipulation.

## Model definition

### Inputs

Inputs include observed material motion from stereo texture tracking or RGB-D reconstruction, contact force or load information when needed, geometry, density, and chosen constitutive basis functions. For planning, the identified material coefficients condition an MPM simulator and an action-parameter optimizer.

### Outputs

The identification stage outputs coefficients of a constitutive material law, such as elastic modulus, yield threshold, viscosity, or learned-basis coefficients. The planning stage outputs robot motion parameters for new actions or geometries.

### Training objective (loss)

Online identification is a linear least-squares solve derived from weak-form momentum balance, not gradient-based training over repeated rollouts. When learned neural basis functions are used, those bases are trained offline from generated constitutive laws, but the online fit remains linear in coefficients.

### Architecture / parameterization

The method is a hybrid physics and optimization pipeline rather than a standard neural network. Stress is parameterized as a linear combination of analytic or learned constitutive response bases. The recovered coefficients are inserted into an MPM simulator for prediction and planning.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Robots manipulating deformable materials need to know how a material responds to forces and motion. Learned dynamics can remain implicit and brittle, while differentiable system identification can require expensive repeated simulation and trajectory matching.

### 2. What is the method?

FORM reconstructs material motion from one interaction, plugs it into weak-form momentum balance, removes or handles pressure terms through suitable test fields, and solves for constitutive-law coefficients. The same coefficients are then used by the forward MPM simulator for planning.

### 3. What is the method motivation?

If the robot can identify a material law quickly, it can plan new actions under new geometries without collecting a large interaction dataset or fitting a black-box dynamics model.

### 4. What data does it use?

The paper uses simulated material trajectories and real robot data from a Franka Panda arm. It evaluates elastic rod insertion, elastic golf putting, elastoplastic shaping, and target-volume pouring, with both simulated and physical materials.

### 5. How is it evaluated?

It compares identification accuracy and solve time against NCLaw and differentiable system identification baselines. It also evaluates whether material-specific identified models improve downstream robot tasks compared with swapped incorrect material models.

### 6. What are the main results?

FORM reduces identification from roughly 10-25 minutes for iterative baselines to about 2-5 seconds in the abstracted summary and table values around 0.1-21.8 seconds depending on material and observation variant. It keeps competitive reconstruction accuracy across Jell-O, sand, plasticine, and water. In elastic tasks, matched identified models insert rods successfully and land golf balls inside the target, while swapped models collide or miss. For elastic property estimates, errors are reported at 0.76% and 3.38%; elastoplastic estimates are below 2% error in simulation. Hardware shaping uses real RGB-D observations for Play-Doh, butter slime, and plasticine.

### 7. What is actually novel?

The key novelty is reducing material-law identification from robot interaction data to a weak-form linear inverse problem that connects directly to the simulator used for planning.

### 8. What are the strengths?

The method is interpretable, fast, and tied to downstream manipulation. It also tests whether the identified law transfers from a probe to new actions and geometries, which is the right evaluation question.

### 9. What are the weaknesses, limitations, or red flags?

The method depends on reconstructed motion quality and assumptions about interior deformation from surface observations. It also depends on choosing a suitable constitutive basis. If the real material behavior is outside the basis, the least-squares solve will still return coefficients but the simulator may mislead planning.

### 10. What challenges or open problems remain?

Better motion reconstruction under occlusion, richer material mixtures, contact uncertainty, online re-identification during manipulation, and automatic basis selection remain open.

### 11. What future work naturally follows?

Combine FORM-style explicit law recovery with uncertainty estimates, active probing policies, and adaptive planning that updates material coefficients after each manipulation attempt.

### 12. Why does this matter for cabbageland?

It is a good example of replacing mushy latent dynamics with explicit physical state. The recovered material law is not merely explanatory; it is the thing the planner uses.

### 13. What ideas are steal-worthy?

Use one targeted interaction to identify an explicit model before planning. Keep the identification parameterization compatible with the forward simulator. Prefer linear-in-coefficients physical bases when speed and interpretability matter.

### 14. Final decision

Preserve. It is a robotics paper, but it clears the higher bar because the explicit material law does real work.
