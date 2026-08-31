# Raw-C Q0-normalized differentiated rotating-tail Gamma_1 functional

## Question and scope

This bounded calculation takes the certified root-1 projective endpoint data
at \(Q_0=-4\) and asks whether the declared boundary functional divided by
that endpoint amplitude, together with its local \(\lambda\)-derivative, can
be enclosed after a finite left cutoff and an analytic complete-tail bound.

For \(U=u/u(Q_0)\), \(Z=\partial_\lambda U\), and the pinned
lambda-independent reference \(c_p\), it evolves

\[
Y=(U,U_Q,Z,Z_Q,c_p,c_{p,Q}).
\]

The Q0 seed is \(U=1\), \(U_Q=-x_0-1/2-\rho(Q_0)\), \(Z=0\),
\(Z_Q=-s(Q_0)\), \(c_p=1\), \(c_{p,Q}=0\). At each cutoff \(Q_c\),
the finite Wronskians receive analytic rotating-frame tail radii:

\[
g=\frac{\Gamma_{1,p}(u)}{u(Q_0)}=-W(U,c_p)(Q_c)+\operatorname{tail},
\qquad
\partial_\lambda g=-W(Z,c_p)(Q_c)+\operatorname{differentiated\ tail}.
\]

The scope is root bracket 1, the negative and positive punctured real
lambda boxes, plus a lambda-zero convention regression. It is a
Q0-normalized/projective functional calculation, not an absolute amplitude
calculation.

## Method and controls

The runner hash-pins the Q0 projective result and the selected declared
Gamma_1 boundary convention. It also hash-pins the older hybrid runner only
for its exact-rational interval-Taylor and whole-step-majorant semantics;
none of that runner's result is evidence here.

The six-state actual-derivative Taylor recurrence uses order 12 and complete
\(D_{13}|h|^{13}/13!\) remainders on the full parameter boxes. It uses

- \(Q_c=-5\) with 16 and 32 steps for discretization refinement;
- \(Q_c=-6\) with 32 steps for a complete-tail cutoff control;
- 80- and 120-decimal Arb tiers.

The left-tail radii bound both \(\lambda aUc_p\) and
\(aUc_p+\lambda aZc_p\). Thus the differentiated omitted tail is not
silently replaced by the older non-differentiated correction estimate.

## Explicit nonclaims

Even if a displayed finite interval happens to omit zero, this runner does
not claim an absolute actual \(\Gamma_1\) value or sign, a zero/root,
continuation or velocity. It also does not construct a Weyl function,
spectral measure, RAQ object, or physical/empirical result.

## First controlled execution: valid but not certified

The committed runner was executed through the bounded control plane:

```text
./ice run raw_c_q0_normalized_differentiated_rotating_tail_gamma1
```

It returned `VALID_RUN` with verdict
`Q0_NORMALIZED_DIFFERENTIATED_ROTATING_TAIL_NOT_CERTIFIED`: 6/8 exact checks
and 676/685 controls passed. The two exact failures have residuals
`cq*uq*(cq - 1)` and `cq*zq*(cq - 1)`. They expose an extra `cq` factor in
the executable symbolic chain-rule audit, not a counterexample to either
Wronskian identity.

The nine numerical failures are six cutoff-overlap/tail-decrease controls and
the three final width controls. At the refined (Q_c=-10) row the punctured
boxes already have (g) width about 4.935 and (g') width about 3139.6;
the (Q_c=-12) boxes are much wider. The analytic tail formulas remained
finite, but the axis-aligned six-state boxes accumulated oscillatory wrapping
before the cutoff, so the deeper-cutoff state norm also made the nominal tail
radius larger rather than smaller. This is an unresolved enclosure, not a
Gamma_1 sign or root result.

The raw first result is preserved in commit `76c5d1a` with file SHA-256
`34453152467f2099f876992e99be9392686c6c32e6590b444a470d891368b67e`
and payload SHA-256
`859da3cac3545467147a7f751c151b17b26d3541b1e930a51be182553553add4`.
All absolute-Gamma, sign, root, Weyl, spectral, RAQ and physical outputs
remain null.

The narrow correction is to fix the symbolic audit typo and hand off to the
already proved analytic rotating-frame tail at earlier cutoffs, before
axis-aligned rotation wrapping dominates. This does not change the functional,
root/lambda scope, width target or nonclaims. The corrected source and input
were committed as `1d4eede` before the next controlled execution.

## Corrected controlled execution: certified normalized functional

The same control-plane command then returned `VALID_RUN` with verdict
`CERTIFY_COMPLETE_Q0_NORMALIZED_DIFFERENTIATED_ROTATING_TAIL_FUNCTIONAL`.
All 8 exact checks and all 541 executable controls passed; the three theorem
guards were also recorded. The run used 480 compact Taylor steps, no black-box
ODE solve, quadrature, root solve, finite difference, or sampling.

The final intersections are:

| lambda box | complete normalized \(g\) | local \(\partial_\lambda g\) |
| --- | --- | --- |
| \([-10^{-4},-10^{-8}]\) | \([-8.00901806745\times10^{-5},\ 9.89752287094\times10^{-5}]\) | \([-0.265406832808,-0.110106479154]\) |
| \([10^{-8},10^{-4}]\) | \([-9.89742402344\times10^{-5},\ 8.00892542083\times10^{-5}]\) | \([-0.265404655305,-0.110106231584]\) |
| \(\lambda=0\) regression | \([-5.56090587207\times10^{-10},\ 5.56089642650\times10^{-10}]\) | \([-0.265366343175,-0.110145226679]\) |

Each displayed \(g\) enclosure contains zero. Each local derivative enclosure
excludes zero and has width below the preregistered \(1/4\) target. This is a
uniform interval fact on each displayed product box, but it does not establish
an actual \(\Gamma_1\) sign, a correlated root curve, uniqueness, continuation,
or root velocity. Those require a separately justified parameter/root
localization rather than a mean-value inference across the puncture.

The corrected raw result has file SHA-256
`5568d2b857ed9f39385ec06c1cbe383b1cba8f3d133e9ba12a083d21c5202d2a`
and payload SHA-256
`7c11e75fea722c09ec58708ffb1943278d0b0b452a9fa622d707914953976413`.
The input SHA-256 is
`183a7c4fd1e2f5823338203ef9143212c572f5ca3a74f2e7450713e4a0b5dbdd`.
All absolute-Gamma, sign, root, Weyl, spectral, RAQ, and physical outputs stay
explicitly null.
