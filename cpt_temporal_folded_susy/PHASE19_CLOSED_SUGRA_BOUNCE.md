# Phase 19 — shift-symmetric SUGRA and a closed time-symmetric bounce

## Result first

The supplied background calculation is reproducible after two important
qualifications:

1. the mass identities use the potential scale
   (H_V^2:=V/3), not the actual closed-FRW value (H(t)^2), which vanishes
   at the bounce; and
2. (zeta>1/6) in the improved Cecotti model is a convenient sufficient
   stability benchmark, not the sharp threshold and not by itself a universal
   Hubble-heavy condition.

With those corrections, exact symbolic reduction gives

\[
V_{m quad}=\frac12m^2\phi^2,
\qquad
V_{\rm St}=\frac34M^2
\left(1-e^{-\sqrt{2/3}\phi}\right)^2,
\tag{E193}
\]

and independent closed-(k=+1) integrations contain smooth, classical,
time-reflection-symmetric solutions with 50, 55, and 60 accelerated e-folds.
The quoted tables are reproduced to their displayed precision, with the
redundant Friedmann constraint below (10^{-12}) relative error.

This is an **existence result**, not an initial-condition prediction.  In each
row (phi_0) is found by shooting backwards from a requested (N_{m acc}).
Neither CPT nor Pin has yet selected (phi_0).  The result also does not
construct a fermionic CPT/Pin state, a BPS bounce, perturbations through the
bounce, reheating, or a present-day SUSY spectrum.

Reproduce the calculation with

```bash
uv run --locked python3 cpt_temporal_folded_susy/phase19_closed_sugra_bounce.py
```

The observed run returns **17 exact PASS and 30 numerical PASS** checks.

## 1. Conventions and the two different Hubble symbols

We use reduced Planck units (M_{\rm Pl}=1), a unit three-sphere
(k=+1), and

\[
ds^2=-dt^2+a(t)^2d\Omega_3^2.
\]

Two quantities must not be conflated:

\[
H(t)=\frac{\dot a}{a},
\qquad
H_V^2(\phi):=\frac{V(\phi)}{3}.
\tag{E194}
\]

In an approximately flat slow-roll regime they are close.  At the symmetric
bounce, however, (H(0)=0) while (H_V^2(phi_0)>0).  All orthogonal SUGRA
mass formulae below use (H_V).

The F-term scalar potential was derived rather than inserted:

\[
V_F=e^K\left(K^{i\bar\jmath}D_iW
D_{\bar\jmath}\bar W-3|W|^2\right),
\qquad
D_iW=\partial_iW+K_iW.
\]

The executable treats holomorphic and antiholomorphic coordinates as
independent exact symbols and checks the index orientation of
(K^{i\bar\jmath}).

## 2. Shift-symmetric quadratic control

Take

\[
K=-\frac12(\Phi-\bar\Phi)^2+S\bar S
-\zeta(S\bar S)^2,
\qquad
W=mS\Phi,
\]

on

\[
S=0,qquad \operatorname{Im}\Phi=0,qquad
\Phi=\frac{\phi}{\sqrt2}.
\]

The exact trajectory data are

\[
V=\frac12m^2\phi^2,
\qquad
m_{\operatorname{Im}\Phi}^2=m^2+6H_V^2,
\qquad
m_S^2=m^2+12\zeta H_V^2.
\tag{E195}
\]

Thus (zeta\ge0) is already non-tachyonic in the (S) direction.  The
often quoted

\[
\zeta\gtrsim\frac1{12}
\]

is the stronger large-field condition (m_S^2\gtrsim H_V^2), used to
suppress stabilizer fluctuations.  It is not the basic stability threshold.
This distinction agrees with the construction in
[Kallosh and Linde, arXiv:1008.3375v2](https://arxiv.org/html/1008.3375v2).

On the inflationary trajectory,

\[
|F^S|=\frac{m|\phi|}{\sqrt2},
\qquad
m_{3/2}=e^{K/2}|W|=0.
\]

The sign of (F^S) is convention dependent; its magnitude is not.  At
(phi=0), (F^S=V=0), so the endpoint is supersymmetric Minkowski in this
minimal model.  Inflationary F-breaking therefore does not provide a
persistent late-time soft scale.

## 3. Improved Cecotti/no-scale control

Take

\[
K=-3\log\!\left[
T+\bar T-S\bar S+\frac\zeta3(S\bar S)^2
\right],
\qquad
W=3MS(T-1).
\]

On (S=0), real (T), the canonical field is

\[
T=e^{\sqrt{2/3}\phi},
\]

and the exact potential is the second expression in (E193).  This is the
stabilized version of the Cecotti route discussed explicitly by
[Kallosh and Linde, arXiv:1306.3214v2, eq. (4.7)](https://arxiv.org/html/1306.3214v2).

Writing (t=T=\bar T\ge1), the canonical stabilizer Hessian is

\[
m_S^2=
\frac{M^2}{6t^2}
\left[4\zeta t(t-1)^2-3t^2+6t+3\right],
\]

or

\[
\frac{m_S^2}{H_V^2}
=\frac83\zeta t-2+\frac4{(t-1)^2}.
\tag{E196}
\]

The sharp potential-Hessian positivity threshold over the full (t\ge1)
trajectory is

\[
\zeta_{\rm crit}
=\frac{9\sqrt3-15}{4}
=0.147114317\ldots .
\]

Consequently (zeta>1/6) is a valid simple sufficient choice, but it is not
the exact necessary threshold.  The primary source rounds the stability
condition to (zeta>0.15) and gives the more conservative
(zeta\gtrsim0.5) when requiring firm (m_S^2\gtrsim H_V^2) stabilization.

As in the quadratic control, (W=m_{3/2}=0) on (S=0), while (D_SW\ne0)
for (T>1).  The inflationary trajectory has an F-term order parameter, but
the (T=1) vacuum restores it.

## 4. Closed-FRW bounce and the meaning of the initial data

The dimensionless equations integrated by the executable are

\[
H^2+\frac1{a^2}
=\frac13\left(\frac12\dot\phi^2+V\right),
\qquad
\dot H=-\frac12\dot\phi^2+\frac1{a^2},
\]

\[
\ddot\phi+3H\dot\phi+V_{,\phi}=0.
\tag{E197}
\]

Time-reflection-compatible bosonic data impose

\[
H_0=0,qquad \dot\phi_0=0.
\]

The constraint then fixes only

\[
a_0=\sqrt{\frac3{V(\phi_0)}}.
\tag{E198}
\]

Since

\[
\dot H_0=\frac1{a_0^2}=\frac{V(\phi_0)}3>0,
\]

(a(t)) has a local minimum.  The solution has
(a(-t)=a(t)), (phi(-t)=phi(t)), (H(-t)=-H(t)).  This proves a regular
classical time-symmetric bounce in the displayed bosonic model.  It does not
by itself prove a CPT-invariant quantum state or a fermionic Pin sewing.

We define the end of accelerated expansion by

\[
\ddot a=0
\quad\Longleftrightarrow\quad
V=\dot\phi^2,
\qquad
N_{\rm acc}=\log\frac{a_{\rm end}}{a_0}.
\tag{E199}
\]

This definition is essential: the usual (epsilon_H=-\dot H/H^2) is
undefined at (H=0).

### Independently solved shooting table

| model | target (N_{\rm acc}) | solved (phi_0) | mass scale (	imes a_0) | (H_{\max}/\)mass scale | max relative constraint error |
| --- | ---: | ---: | ---: | ---: | ---: |
| quadratic | 50 | 14.21160232 | 0.17235845 | 5.589491442 | (6.0\times10^{-14}) |
| quadratic | 55 | 14.89637634 | 0.16443528 | 5.876431461 | (3.0\times10^{-13}) |
| quadratic | 60 | 15.55122563 | 0.15751104 | 6.150309764 | (5.1\times10^{-13}) |
| Starobinsky | 50 | 5.23269928 | 2.02828882 | 0.492249532 | (2.1\times10^{-14}) |
| Starobinsky | 55 | 5.34237404 | 2.02583440 | 0.492967908 | (3.3\times10^{-15}) |
| Starobinsky | 60 | 5.44296946 | 2.02377306 | 0.493564968 | (1.3\times10^{-14}) |

For the supplied conditional scale benchmarks:

| model | input scale | (a_0[M_{\rm Pl}^{-1}]) | (H_{\max}/M_{\rm Pl}) |
| --- | ---: | ---: | ---: |
| quadratic, 60 e-fold row | (m=6.0\times10^{-6}) | (2.625184\times10^4) | (3.690186\times10^{-5}) |
| Starobinsky, 60 e-fold row | (M=1.3\times10^{-5}) | (1.556749\times10^5) | (6.416345\times10^{-6}) |

Because (k=+1) and the unit-(S^3) convention are fixed, (a_0) is a
conditional physical curvature radius, unlike the arbitrary normalization of
(a) in spatially flat noncompact FRW.  It is still not parameter free:
(a_0) depends on the chosen mass scale and on the unselected (phi_0).

## 5. Observational control

The bounce-to-end count (N_{\rm acc}) is not automatically the CMB pivot
count (N_*).  Reheating and the relation (k_*=a_*H_*) must be supplied
before identifying them.  As a separate first-order potential slow-roll
control, imposing (epsilon_V=1) at the end gives:

| (N_*) | quadratic (n_s) | quadratic (r) | Starobinsky (n_s) | Starobinsky (r) |
| ---: | ---: | ---: | ---: | ---: |
| 50 | 0.9603960 | 0.1584158 | 0.9615696 | 0.0041923 |
| 55 | 0.9639640 | 0.1441441 | 0.9649772 | 0.0034983 |
| 60 | 0.9669421 | 0.1322314 | 0.9678271 | 0.0029639 |

The quadratic model is incompatible with the published
[BK18 (r_{0.05}<0.036) limit](https://arxiv.org/abs/2110.00483) and with the
2026 combined [(r<0.034) analysis](https://arxiv.org/abs/2512.10613v2).
The Starobinsky tensor prediction is safely below those limits.  Its scalar
tilt is data-set dependent: the 2026 combined analysis reports
(n_s=0.9682\pm0.0032) for its CMB combination and
(0.9728\pm0.0029) after adding DESI BAO.  It is therefore more realistic
than the quadratic model, but “observationally settled” would be too strong.

## 6. What this changes — and what it does not

### Established here

- both displayed SUGRA trajectories reduce to the claimed one-field
  potentials;
- the corrected stabilizer conditions and (H_V/H(t)) distinction are exact;
- the closed (k=+1) bosonic equations admit the six displayed time-symmetric
  bounce solutions;
- the quadratic tensor prediction is observationally excluded, while the
  Starobinsky branch is the better background candidate;
- for a chosen mass scale and a chosen (phi_0), the bounce curvature radius
  and maximum Hubble rate are calculable.

### Still open

- no CPT/Pin principle selects (phi_0=5.442969\ldots) or any other row;
- no quantum-cosmological probability measure over (phi_0) was calculated;
- no complete (A,\psi,F) or local-SUGRA fermionic junction/domain was built;
- no scalar or tensor perturbation was propagated through the closed bounce;
- no reheating history maps (N_{\rm acc}) to (N_*);
- no late-time (F/D) order parameter or MSSM soft spectrum was derived.

The honest bounded conclusion is therefore

\[
\boxed{
\text{a realistic closed Starobinsky-SUGRA bounce background exists
conditionally,}
\quad
\text{but the temporal/CPT construction does not yet select its initial
amplitude.}
}
\]

## 7. Next decisive calculation

The highest-value next step is not another background scan.  It is a closed
(S^3) perturbation-and-state calculation on the no-scale branch:

1. evaluate the full Kähler metric and covariant scalar mass matrix along the
   entire bounce, including every orthogonal real scalar;
2. derive the quadratic scalar and tensor actions in discrete (S^3)
   harmonics and impose the Wronskian/Hadamard conditions;
3. define the candidate CPT/Pin action on those modes and determine whether it
   selects a unique Gaussian state or a measure over (phi_0);
4. only then include reheating, map to (k_*), and compare (A_s,n_s,r) with
   likelihood data.

If the state condition leaves a continuous (phi_0) family, the construction
has an existence result but no initial-value prediction.  If it selects a
normalizable state concentrated near the 50--60 e-fold window, that would be
the first genuinely new prediction from this route.
