# Closed \(S^3\) zonal scalar aliasing and cutoff-ladder audit

## Question

For the frozen packet \(\phi=Q_1+Q_2\), this bounded calculation separates two
effects which must not be given the same name:

1. **aliasing defect** — a high harmonic is incorrectly folded into a retained
   coefficient because the physical-space product is evaluated with too few
   quadrature nodes;
2. **true projection remainder** — an exact modal product really contains
   harmonics above the declared hard cutoff \(N\).

Dealiasing can remove the first effect.  It cannot remove the second; only a
larger retained space or an analytic tail treatment can do that.

## Fixed exact packet

With

\[
Q_aQ_b=s\sum_{j=0}^{\min(a,b)}Q_{a+b-2j},
\qquad s=(2\pi^2)^{-1/2},
\]

the exact square is

\[
(Q_1+Q_2)^2=s(2Q_0+2Q_1+2Q_2+2Q_3+Q_4).
\]

The audit compares the retained coefficients obtained from:

- exact modal convolution;
- the smallest Gauss-Chebyshev-\(U\) grid certified to integrate every retained
  coefficient of this frozen packet exactly;
- the declared production grid \(M=N+1\), whose adequacy is tested rather than
  assumed.

The packet is frozen while \(N=2,3,4\) is varied.  Common low coefficients and
the discarded-channel norm are recorded at every cutoff.

## Interpretation boundary

This is a scalar-zonal nonlinear evaluator audit.  A nonzero aliasing defect is
an evaluation error.  A nonzero true projection remainder is a regulator effect.
Neither is by itself a gravitational constraint-algebra residual, a classical
or quantum anomaly, a continuum obstruction, or a physics result.

The runner performs no numerical quadrature.  It evaluates finite transform sums
exactly and records their count separately from the zero numerical-quadrature call
budget.

The source and input are committed before execution.  The controlled command is

```text
./ice run closed_s3_zonal_scalar_aliasing_cutoff_ladder_audit
```

The observed result is added only after that clean committed run.
