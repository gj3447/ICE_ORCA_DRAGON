# Phase 40 — m=3 reflection-odd local joint intersections

## Outcome

Phase 40 raises the Phase-39 configuration regulator from two to three
segments.  This is the smallest cutoff with a genuine reflection-odd
interior-history sector.  One scalar midpoint action on

\[
X_3=\mathbb C_{a_1,\phi_1,a_2,\phi_2}\times\mathbb C_T^*
\]

generates every joint equation and Hessian.  A rank-one signed endpoint
probe is applied,

\[
a_L=a_R=a_b,\qquad
\phi_L=\phi_b-\delta/2,\qquad
\phi_R=\phi_b+\delta/2,
\]

and one local upward-cycle chart is continued through the five sampled
values

\[
\delta=-10^{-3},-5\!\times\!10^{-4},0,
+5\!\times\!10^{-4},+10^{-3}.
\]

At every sampled value, the declared cap piece and the finite-time upward
chart have a resolved local intersection in all ten real ambient
coordinates, with

\[
\boxed{\operatorname{sgn}\det_{\mathbb R}[V_\Gamma,V_K]=+1.}
\]

For the three fully audited points \(\delta=-10^{-3},0,+10^{-3}\), the
physical maximum residual is \(4.2\!\times\!10^{-9}\) to
\(6.1\!\times\!10^{-9}\), and the column-normalized direct determinant has
\(\sigma_{\min}=0.09065\) to \(0.09068\).  Independent two-step finite
differences agree with the transported variational Jacobian at relative
operator error below \(1.2\times10^{-4}\).

This is a local finite-cutoff result.  It does not determine the signed sum
on the whole regulated chain.  Accordingly,

```text
bounded_chain_signed_sum = null
complete_global_signed_intersection_vector = null
global_n_sigma = null
Gate 1 = OPEN_PARTIAL_M3_REFLECTION_ODD_LOCAL_PROGRESS
```

The executable passes 12 exact and 22 numerical checks and exits zero.

## 1. Provenance, including failed checks

The initial post-feasibility input freeze was committed as
`dd2a9d54b386dcc7bb090f446d5d32aad59743e7`, with SHA-256
`897c9788cf1b2706ddf6e2c75f56f4ac7da1eb0aea64ea01cb31971a35920426`.
It was not a preregistration: the symmetric saddle, an approximate cap hit,
the existence of the odd Hessian block, and exploratory local signs were
already known.

The first fail-closed run exposed an ill-posed instruction.  Exact
delta-zero Morse whitening makes each signed Hessian block internally
degenerate, so individual eigenvectors at nonzero delta cannot be anchored
to unique delta-zero eigenvectors.  The manifest was amended in commit
`a6b369e0a9518cd491f8116204ec67ab36fdf2a1` to transport the invariant
positive and negative spectral subspaces by orthogonal Procrustes alignment.
The final manifest SHA-256 is
`60dfc9c31e45408c92b5fbcd1e1487bcd53b02a62ccf4ee71272f7c3dcc382ae`.
The action, source direction, delta grid, fixed flow mobility, cap, and
promotion boundary were not changed.

The manifest's hand-written `amended_at_utc` is later than the actual
amendment commit timestamp.  Both raw values are preserved; the mismatch is
not silently rewritten.

Three further numerical repairs occurred before the zero-exit run:

- roots found with a coarse BDF flow were initially evaluated on a different
  DOP853 numerical map and missed the frozen residual threshold; BDF is now
  seed-only and the final root is Newton-refined on the strict DOP853 map;
- the finite-difference audit initially stepped past its stable plateau;
  the final two-point bands use the observed stable range, retain the original
  two-percent acceptance threshold, and are post-failure controls rather
  than out-of-sample predictions;
- the first odd-coordinate clamp used numerical differentiation and was
  interrupted for cost; the completed version uses the already transported
  variational columns as its analytic Jacobian.

These events are evidence about the method's fallibility, not results to
hide.  Phase 40 is an explicit construction and adversarial audit, not a
prediction made blind to its outcome.

## 2. One action, reflection, and the first odd sector

With \(h=1/3\),

\[
S_3=2\pi^2\sum_{e=0}^{2}\left[
\frac{-6a_{e+1/2}(\Delta a_e)^2
+a_{e+1/2}^3(\Delta\phi_e)^2}{2Th}
+Th\left(-3a_{e+1/2}+a_{e+1/2}^3V(\phi_{e+1/2})\right)
\right],
\]

where

\[
V(\phi)=\frac34(1-e^{-\sqrt{2/3}\phi})^2.
\]

SymPy differentiates this single scalar to produce the five-component
gradient and full \(5\times5\) Hessian.  The action is holomorphic away from
the excluded divisor \(T=0\); its simple-pole residue polynomial is not
identically zero.

For node reflection

\[
R(a_1,\phi_1,a_2,\phi_2,T)
=(a_2,\phi_2,a_1,\phi_1,T),
\]

the code verifies exactly

\[
S_3(Rz;-\delta)=S_3(z;\delta),\quad
\nabla S_3(Rz;-\delta)=R\nabla S_3(z;\delta),\quad
H(Rz;-\delta)=RH(z;\delta)R.
\]

In the oriented mode order

\[
(a_{\rm even},\phi_{\rm even},T,
a_{\rm odd},\phi_{\rm odd}),
\]

the nodal-to-mode determinant is \(+1\), reflection parity is
`diag(+,+,+,-,-)`, and the delta-zero Hessian separates exactly into
three even and two odd directions.  At the discrete saddle the odd-block
eigenvalues are

\[
(-6.5208788071\times10^4,\ 1.1360445359\times10^4),
\]

while the even/odd cross norm is \(4.8\times10^{-12}\).

The phi-only source has rank one, whereas the odd field sector has dimension
two.  It therefore does not probe the full odd sector.  At
\(\delta=10^{-3}\), the anchor-subtracted odd saddle amplitude is

\[
(5.23\times10^{-6},-8.83\times10^{-7}),
\]

so the recorded response is not solely the odd component forced by the
linear cycle anchor.  It reverses under \(\delta\mapsto-\delta\), and the
half-step/full-step susceptibility differs by \(4.4\times10^{-6}\).

## 3. Fixed metric versus delta-dependent launch ellipsoid

At the delta-zero saddle,

\[
(a_1,\phi_1,a_2,\phi_2,T)_\sigma=
(3.5842806045,0.9998956289,3.5842806045,0.9998956289,
0.7450719778),
\]

the dimensionless Hessian has inertia \((3_-,2_+)\).  Write

\[
H_0=O\Lambda O^T,\qquad L_0=O|\Lambda|^{-1/2},\qquad
w=w_\sigma(\delta)+L_0\xi.
\]

The fixed object in the original \(w\) coordinates is the positive
inverse-metric mobility

\[
M_0=L_0L_0^T,
\]

while the metric tensor is \(g_0=M_0^{-1}\).  The flow is

\[
\dot\xi=-\overline{L_0^T\nabla_wS_\delta}.
\]

For holomorphic \(S\), the code checks algebraically

\[
\frac{dS}{d\tau}=-\sum_I|\partial_I S|^2,
\]

so \(\Re S\) is nonincreasing and \(\Im S\) is constant.  The numerical
trajectories test the same identities, remain below the frozen
\(\|\xi\|=40\) cap, and show no earlier \(|T|=0.3\) crossing among 81
recorded samples.  This is a sampled statement, not continuous event
detection or a search for later reintersections.

At nonzero delta, the positive and negative spectral projectors are aligned
as whole subspaces.  Within each aligned subspace, the inverse positive
square root of the restricted Hessian gives a Morse-normalized launch frame
\(J_\delta\).  Numerically,

\[
\max_\delta\|J_\delta^TH_\delta J_\delta+I\|_2
=3.2\times10^{-13},
\]

and the reflected signed-projector residual is \(6.5\times10^{-15}\).
The launch surface at nonzero delta is a delta-dependent ellipsoid, not a
new metric and not a determinant-line or Pin holonomy.  The three-radius
control scales this same ellipsoid family; it is not a metric-homotopy test.

## 4. Five sampled full-space intersections

Both \(\Gamma\) and \(K\) have real dimension five in an ambient
\(\mathbb R^{10}\).  The requested local orientation is computed directly:

\[
\epsilon_x=\operatorname{sgn}\det_{\mathbb R}[V_\Gamma,V_K].
\]

The nonlinear solver instead sees \([V_\Gamma,-V_K]\).  Since five columns
are negated, its orientation must be the opposite sign.  Both independent
parameter-orientation reversals also flip the direct sign.

| delta | max physical residual | normalized sigma-min | direct sign |
|---:|---:|---:|---:|
| -0.0010 | 6.05e-9 | 0.0906550 | +1 |
| -0.0005 | 7.13e-9 | 0.0906768 | +1 |
| 0 | 4.18e-9 | 0.0906841 | +1 |
| +0.0005 | 1.14e-8 | 0.0906768 | +1 |
| +0.0010 | 4.80e-9 | 0.0906550 | +1 |

The two intermediate points are sequential continuation controls.  Full
two-step finite-difference and flow audits are applied at the two endpoints
and at zero.  Their maximum adjacent-step changes are respectively
1.24%, 0.87%, and 1.07%; the FD-to-variational operator errors are all below
\(1.2\times10^{-4}\).  The two endpoint candidates reflect into one another
with maximum residual \(5.2\times10^{-14}\).

At \(\delta=10^{-3}\), launch radii
\(5\times10^{-5},10^{-4},2\times10^{-4}\) all give direct sign \(+1\) and
normalized \(\sigma_{\min}\simeq0.090655\).  This is finite-radius stability
of one local family, not a proof of the exact nonlinear unstable manifold or
the \(\rho\to0\) limit.

Sequential success at five points does not prove a continuous branch between
them, exclude an unsampled determinant zero, establish uniqueness in the
box, or exhaust other roots and upward components.

## 5. Local K-launch-coordinate clamp

As a negative control, the two frozen reference coordinates corresponding
to the delta-zero odd launch directions are set to zero at
\(\delta=10^{-3}\).  The remaining eight variables minimize ten real
matching equations using the transported analytic Jacobian.  The local fit
converges with optimality \(2.0\times10^{-8}\), but leaves

\[
\max|\Gamma-K|=3.98\times10^{-4},
\]

far above the \(2\times10^{-7}\) candidate tolerance.

This only says that the continued-seed local slice obtained by clamping those
two K-launch coordinates does not reproduce the tracked candidate.  Gamma's
odd field directions and nonlinear odd/even mixing remain present.  It is
not a full odd-sector ablation, a no-root theorem, or evidence that odd
dynamics is ontologically fundamental.

## 6. What the result does and does not mean

Phase 40 supports a narrow statement:

> In one frozen m=3 configuration regulator, one rank-one phi endpoint
> source has a nonzero anchor-subtracted reflection-odd response, and a
> locally transverse full-R10 cap candidate with declared sign +1 can be
> sequentially followed at five sampled delta values.

It does not yet compute:

- the independent a-only source needed to probe the full odd field sector;
- m=4 agreement, cutoff convergence, or a continuum limit;
- the straight arms, later cap intersections, all roots or all upward
  components;
- a non-Stokes lateral chamber, connecting flows, jumps, or all good ends;
- a physical selection of the declared Gaussian-lift original cycle;
- a bounded-chain sum, global signed vector, or global \(n_\sigma\);
- canonical momenta, ghosts, fermions, gravitino, BFV/Pfaffian/Pin data,
  conserved spinorial charge, persistent order parameter, pole splitting,
  or quantum gravity.

The next adversarial calculation is the orientation-matched m=4 control,
using both the phi-only source and an independent a-only source.  Only after
that comparison should the programme attempt the larger chain, Stokes, and
relative-good-end completion required by Gate 1.

## Reproduction

```bash
uv run --locked python3 \
  cpt_temporal_folded_susy/phase40_m3_reflection_odd_intersection.py
```

Expected terminal summary:

```text
All 12 exact checks and 22 numerical checks passed.
```
