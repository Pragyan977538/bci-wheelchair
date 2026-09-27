# Shared Control of a BCI-Driven Wheelchair

**Pragyan Mohanty** | Roll No. 24250 | Control Systems Project

---

## 1. Problem Statement and Objective

Motor-imagery brain–computer interfaces (BCIs) decode imagined movements from scalp EEG. They offer an alternative control channel to people with severe motor impairment. Treated as a control input, however, the decoded signal is a degraded measurement of user intent. It has a high error rate, a transport delay of several seconds, and an update rate limited by the decoder's decision window. Closing a feedback loop directly through such a channel compromises both stability and safety.

This project addresses the resulting arbitration problem. The aim is to design and analyse a **shared-control law** that allocates control authority between the BCI user and an autonomous navigator, so that the closed-loop system remains **stable under transport delay** and **safe under decoder error**, while preserving as much user authority as possible. The central question is how the authority parameter $\alpha$ should be chosen, and what that choice costs in stability, performance and user agency.

## 2. Proposed Solution

The actuator command is a convex combination of the user's decoded command and the autonomous controller's command:

$$
u(t) = \alpha(t)\,u_{\text{BCI}}(t) + \bigl(1-\alpha(t)\bigr)\,u_{\text{auto}}(t), \qquad \alpha \in [0,1]
$$

The authority $\alpha$ is adapted online from the decoder's calibrated confidence $c$ and a situational risk signal $r$:

$$
\alpha = c\,(1-r)
$$

For a fixed $\alpha$ and total loop delay $\tau$, one axis of the blended loop has the characteristic equation

$$
\Delta(s) = s^2 + d\,s + (1-\alpha)(K_1 + K_2 s) + \alpha\,(K_p + K_d s)\,e^{-\tau s} = 0
$$

and is delay-independently stable for

$$
\alpha < \alpha^* = \frac{K_1}{K_1 + K_p}
$$

### Framework

| Concept | Role in the project |
|---|---|
| **Motor-imagery EEG decoding** | Common Spatial Patterns (CSP) with shrinkage Linear Discriminant Analysis maps band-limited EEG (8–30 Hz, μ and β rhythms) to one of four commands |
| **Probability calibration** | Platt scaling converts classifier scores into calibrated posteriors, assessed by Expected Calibration Error (ECE); the posterior supplies the confidence $c$ |
| **Stochastic channel model** | Decoder errors are modelled as a two-state Markov process (reliable / degraded) with empirically measured latency and class-confusion structure |
| **Plant dynamics** | Nonholonomic unicycle with first-order actuator lag (wheelchair), plus a damped double integrator $\dot p = v,\ \dot v = u - d\,v$ for analytical tractability |
| **Operator model** | Delayed proportional–derivative controller, $u_h(t) = K_p\,e(t-\tau_h) - K_d\,v(t-\tau_h)$ |
| **Optimal control** | Linear Quadratic Regulator (LQR), gains $K_1, K_2$ from the algebraic Riccati equation |
| **Obstacle avoidance** | Dynamic Window Approach (DWA) over the velocity space reachable under actuator limits |
| **Situational risk** | Time-to-collision (TTC) mapped to $r \in [0,1]$, low-pass filtered to keep the loop quasi-stationary |
| **Hysteresis and rate limiting** | Schmitt-trigger gating and a slew-rate limit on $\alpha$ prevent authority chattering |
| **Time-delay stability** | Substituting $s = j\omega$ removes the delay from the magnitude condition and leaves a quadratic in $\omega^2$; its roots give the crossing frequencies and the closed-form delay margin $\tau_{\max}(\alpha)$ |
| **Padé approximation** | A rational (2,2) approximation of $e^{-\tau s}$, used only as a comparison against the exact boundary |
| **Numerical verification** | Delay-differential-equation (DDE) integration and bisection, the Python `control` package, and an independent MATLAB implementation |
| **Statistical evaluation** | Paired Monte-Carlo simulation across subjects, environments and seeds; subject-level bootstrap confidence intervals |

## 3. Dataset

**BCI Competition IV, Dataset 2a** (BNCI2014_001)

| Property | Value |
|---|---|
| Subjects | 9 |
| Channels | 22 EEG, 250 Hz |
| Classes | Left hand, right hand, feet, tongue |
| Sessions | 2 per subject (different days), 288 trials each |
| Command mapping | Turn left, turn right, forward, stop |

- Dataset: https://www.bbci.de/competition/iv/#dataset2a
- Stage 1 report (PDF): *link to be added*

## 4. Methodology

**Stage 1: Baseline characterisation.** The dataset serves as the empirical foundation. The decoder is trained on session 1 and evaluated on session 2, so the evaluation is strictly cross-session. The resulting performance parameters are then frozen and form the baseline model of the BCI channel.

| Parameter (mean over 9 subjects) | Result |
|---|---|
| Accuracy | 0.443 (chance level 0.25) |
| Cohen's κ | 0.258 |
| Expected calibration error, raw → calibrated | 0.196 → 0.096 |
| Confidence discrimination (ROC AUC) | 0.676 |
| Decision latency (median) | 2.0–4.0 s, subject-dependent |

**Stage 2: Control design and optimisation.** The Stage 1 parameters feed a stochastic model of the BCI channel. That model is used to design the arbitration law, derive the stability boundary and evaluate closed-loop performance in simulation.

## 5. Repository Structure

```
├── README.md
├── report/                 Stage 1 report
├── config/                 (incomplete)
├── src/                    (incomplete)
├── data/                   (incomplete)
├── results/                (incomplete)
├── tests/                  (incomplete)
└── requirements.txt        (incomplete)
```

## 6. Remaining Work

1. **BCI channel model.** Fit a per-subject Markov error model and latency distribution from the Stage 1 outputs.
2. **Plant and operator models.** Implement the wheelchair and double-integrator plants and the delayed-PD operator.
3. **Autonomous controllers.** Implement LQR and the Dynamic Window Approach with obstacle avoidance.
4. **Arbitration policies.** Implement fixed blending, confidence-only and risk-gated adaptive allocation, $\alpha = c(1-r)$.
5. **Stability analysis.** Derive $\tau_{\max}(\alpha)$ and $\alpha^*$, and verify them numerically.
6. **Simulation study.** Compare all policies across 9 subjects, 3 environments and 20 random seeds on success rate, collision rate and retained user authority.
7. **Final report.** Consolidate results, ablations and limitations.

## 7. Note

This project is **under active development** and is not yet complete. Stage 1 (EEG decoding and baseline characterisation) is finished, and its results are documented in the Stage 1 report. Stage 2 (control design, stability analysis and simulation) is in the development phase.

The source code in `src/` will be uploaded after the mid-semester evaluation. The repository structure above reflects the planned layout, and this README will be updated as each stage is completed.
