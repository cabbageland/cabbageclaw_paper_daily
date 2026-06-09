# iMaC: Translating Actions into Motion and Contact Images for Embodied World Models

## Basic info

* Title: iMaC: Translating Actions into Motion and Contact Images for Embodied World Models
* Authors: Zhenyu Wu, Xiuwei Xu, Yukun Zhou, Yifan Li, Qiuping Deng, Xiaofeng Wang, Zheng Zhu, Bingyao Yu, Ziwei Wang, Jiwen Lu, Haibin Yan
* Year: 2026
* Venue / source: arXiv
* Link: https://arxiv.org/abs/2606.09813
* Date surfaced: 2026-06-09
* Why selected in one sentence: It turns future robot actions into explicit robot-motion and contact-geometry images, making action-conditioned world modeling less dependent on abstract action vectors.

## Quick verdict

**Strong direct hit**

iMaC is worth preserving because it tackles the right bottleneck for learned robot simulators: the action condition. If a world model is supposed to evaluate policies, it must distinguish small action differences that decide contact and task success. I inspected the arXiv PDF, including the method, policy-evaluation protocol, ablations, limitations, and appendix task analysis.

## One-paragraph overview

iMaC is an embodied world model for closed-loop robot policy evaluation. It builds on a Wan2.2 image-to-video DiT, but instead of feeding future actions only as compact vectors, it translates them into image-like controls. The first control is a motion image: future robot observations rendered from the robot URDF and forward kinematics. The second and third controls are contact images: scene-to-gripper and robot-to-scene distance fields built from point clouds using predicted depth. The model rolls out RGB-D-style future video chunks, feeds the last generated frame back as the next reference, and evaluates whether simulated policy success tracks real-world policy success across checkpoints.

## Key questions this summary must address

### 1. What problem is the paper trying to solve?

Learned world models are attractive for robot policy evaluation, but they are only useful if rollouts respond to actions in the right way. Compact action vectors are a weak condition for video diffusion models: the model must infer where the robot body will appear, what it will contact, and how small action differences change object motion. In manipulation, that missing spatial interface can destroy the ranking of policies.

### 2. What is the method?

- Arrange one head-camera view and two wrist-camera views into a single image mosaic.
- Use an image-to-video DiT backbone to generate future observation chunks.
- Render future robot configurations from future joint actions using URDF and forward kinematics.
- Use those rendered robot observations as motion-image controls.
- Predict depth alongside RGB so the model has geometric state for later chunks.
- Build a current scene point cloud after removing the robot.
- Build future robot and gripper point clouds from the action-implied robot configurations.
- Create scene-to-gripper contact images by measuring current scene point distance to the future gripper.
- Create robot-to-scene contact images by measuring future robot point distance to the current scene.
- Inject motion and contact controls into future-video tokens.
- Use training-time rollout so later chunks are conditioned on generated references, reducing the train-test mismatch of closed-loop generation.

### 3. What is the method motivation?

The action interface should expose the geometry that the world model needs. Future robot appearance is mostly determined by kinematics; contact-relevant distances can be computed from robot and scene point clouds. If those signals are made visible as images, a pretrained video model has a much easier conditioning problem than decoding contact from a low-dimensional action vector.

### 4. What data does it use?

The paper evaluates on eight real-world manipulation tasks with paired multi-view RGB videos and robot action trajectories collected from teleoperation and policy rollouts. The policy-evaluation protocol tests checkpoints from two VLA policy families, pi0.5 and GigaBrain-0.5. Depth supervision is estimated with Depth Anything 3 from multi-view RGB observations and camera poses.

### 5. How is it evaluated?

The evaluation has two main layers:

- Future-video prediction quality against ground-truth videos under the same initial observations and action sequences.
- Closed-loop policy evaluation, where a policy acts inside the learned world model and the resulting world-model success scores are correlated with real-world success rates for matched policy checkpoints.

The paper also ablates motion images, contact images, and the source of depth used for contact-image construction.

### 6. What are the main results?

On future-video metrics, iMaC reports the best task-averaged FID, PSNR, SSIM, and FVD among the compared variants. The reported FVD is 489.51 for iMaC, compared with 591.47 for Ctrl-World and 642.98 for ABot-PhysWorld. Removing contact images weakens FID and FVD.

For policy evaluation, the important result is correlation with real hardware. Six of eight tasks show strong positive correlation between normalized world-model success and normalized real-world success, with reported correlations of 0.956, 0.931, 0.915, 0.870, 0.856, and 0.833. The weaker tasks, with 0.678 and 0.428 correlation, are analyzed as missing-observation failures: the available cameras do not reveal height relations that determine success.

### 7. What is actually novel?

The novelty is the action-to-control translation. iMaC does not merely condition a video generator on actions. It renders the robot's future body and constructs contact-distance control images so that the action's likely physical consequences are spatially explicit in the model input.

### 8. What are the strengths?

- Attacks the action-conditioning bottleneck directly.
- Uses robot kinematics where kinematics are actually available, rather than making the generator infer robot pose.
- Represents contact geometry with two complementary distance fields.
- Evaluates the world model as a policy-checkpoint ranking tool, which is the right downstream use case.
- Includes failure-case analysis showing when missing camera coverage breaks policy-evaluation reliability.
- Treats generated rollouts as complementary to real evaluation, not a replacement for hardware.

### 9. What are the weaknesses, limitations, or red flags?

- The method assumes access to a robot URDF, camera calibration, forward kinematics, and usable depth or depth estimates.
- The final evaluation uses one task-specific world model per task, so general world-model claims should be kept modest.
- Depth supervision comes from Depth Anything 3, which can introduce centimeter-level errors in manipulation scenes.
- Correlation is strong for most tasks but not all; missing task-relevant views can make the world model confidently wrong.
- The method evaluates policy checkpoints, but it does not prove the generated simulator is accurate enough for open-ended policy improvement.

### 10. What challenges or open problems remain?

The main challenge is observation coverage. If the cameras never see the physical relation that decides success, no amount of contact-image engineering can fully recover it. The paper's Task 3 and Task 5 failures make this clear: box-ear height and dustpan entrance height are load-bearing state variables hidden from the available views.

### 11. What future work naturally follows?

- Add active view selection or additional cameras when contact-critical geometry is occluded.
- Replace estimated depth with manipulation-tuned depth or real depth sensing.
- Learn uncertainty over contact-image quality and rollout reliability.
- Test whether a single multi-task iMaC model can preserve policy-ranking quality across tasks.
- Use the world model not only for checkpoint ranking but for targeted policy red-teaming.

### 12. Why does this matter for cabbageland?

Because it is a clean example of making an action interface explicit enough for a world model to use. A world model that only sees a compact action vector is being asked to invent too much. iMaC shows how to give the model the robot body and contact geometry directly.

### 13. What ideas are steal-worthy?

- Render action-implied robot observations from URDF/FK and feed them as controls.
- Build bidirectional contact-distance images rather than one generic action heatmap.
- Predict depth as part of the world-model state so the next chunk can construct new controls.
- Evaluate learned simulators by policy-ranking correlation, not just video metrics.
- Analyze low-correlation tasks as missing-state failures, not as mysterious benchmark noise.

### 14. Final decision

**Preserve as a core embodied-world-model interface note.** iMaC is valuable because it makes the physical action condition visible to the generator and evaluates the result against real-world policy ranking.
