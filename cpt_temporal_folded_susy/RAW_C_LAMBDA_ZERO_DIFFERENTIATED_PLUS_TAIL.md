# Raw-C lambda-zero differentiated plus-tail certificate

## Narrow question and answer

At exactly \(\lambda=0\), and only on the five full \(\kappa\)-brackets
already certified to contain sign-changing zeros of the declared endpoint
characteristic, the scale-invariant datum

\[
h(4;\kappa)=
\left.\partial_\lambda\!\left[-\frac{u_Q}{u}\right]
\right|_{\lambda=0}
\]

now has rigorous positive ball enclosures.  The calculation does not
transport this datum from \(Q=4\) to \(Q_0=-4\), compute an endpoint
\(F_\lambda\), or construct spectral or RAQ data.

## Correct plus-end identity

For

\[
u_{QQ}=A u,\qquad
A_0=36\pi^4e^{2Q}-\kappa^2,\qquad
A_\lambda=6\pi^2e^{3Q/2},
\]

put \(g=-u_Q/u\) and \(h=\partial_\lambda g|_0\).  Exact algebra gives

\[
g_Q=g^2-A_0,\qquad h_Q=2gh-A_\lambda,
\qquad (u^2h)_Q=-A_\lambda u^2.
\]

The correct recessive boundary condition is

\[
u(Q)^2h(Q)\longrightarrow0,
\]

not \(h(\infty)=0\).  In fact the leading sensitivity scale is
\(h\sim e^{Q/2}/2\), while the recessive \(u\) decays superexponentially.
Consequently,

\[
h(Q)=\frac{1}{u(Q)^2}
\int_Q^\infty A_\lambda(s)u(s)^2\,ds>0.
\]

This formula is invariant under \(u_\lambda\mapsto c(\lambda)u_\lambda\):
the \(c'(0)\) term cancels in \(\partial_\lambda[-u_Q/u]\), and the
constant \(c(0)^2\) cancels in the integral ratio.

At \(\lambda=0\), with

\[
C=6\pi^2,\qquad x=Ce^Q,\qquad
u=K_{i\kappa}(x),
\]

the exact identity at \(Q=4\) is

\[
h(4;\kappa)=\frac{1}{\sqrt C\,K_{i\kappa}(x_+)^2}
\int_{x_+}^{\infty}\sqrt{x}\,K_{i\kappa}(x)^2\,dx,
\qquad x_+=Ce^4.
\]

## Rigorous finite integral and improper tail

Direct unscaled values are superexponentially small.  The runner therefore
uses

\[
S_\kappa(x)=e^xK_{i\kappa}(x),\qquad y=x-x_+,
\]

and encloses the finite integral on \(0\le y\le32\):

\[
J_{32}=\int_0^{32}
\sqrt{x_++y}\,e^{-2y}S_\kappa(x_++y)^2\,dy.
\]

The locked `python-flint==0.9.0` `acb.integral` routine provides the finite
complex-ball enclosure.  Every callback stays in \(\operatorname{Re}x>0\),
and the square root receives the integration routine's analytic flag.
Each exact-rational \(\kappa\)-bracket is passed as a whole Arb parameter
ball, not sampled at its midpoint.

[DLMF 10.32.9](https://dlmf.nist.gov/10.32.E9) gives, for real \(\kappa\)
and positive \(x\),

\[
K_{i\kappa}(x)=\int_0^\infty e^{-x\cosh t}\cos(\kappa t)\,dt.
\]

Using \(|\cos(\kappa t)|\le1\) and
\(\cosh t\ge1+t^2/2\) gives

\[
|K_{i\kappa}(x)|\le e^{-x}\sqrt{\frac{\pi}{2x}}.
\]

Thus the omitted contribution to \(h\) is bounded outwardly by

\[
0\le R_{32}\le
\frac{\pi e^{-64}}
{4\sqrt C\,S_\kappa(x_+)^2\sqrt{x_++32}}.
\]

The denominator ball has a strictly positive real lower bound on every
full parameter bracket.  The largest emitted tail upper bound is below
\(6.013\times10^{-28}\).  The older Liouville--Green inequality is not
differentiated or used as an \(h\)-error theorem here.

## Observed certificate

The clean committed runner was executed through the repository control
plane:

```text
./ice run raw_c_lambda_zero_differentiated_plus_tail
```

It returned `VALID_RUN`, exact checks 9/9, ball checks 70/70, six
theorem/scope guards, and five certified bracket boxes.  The final entries
are outward-rounded enclosures of the intersections of two rigorous
same-backend runs at 80 and 120 decimal digits.  The higher-precision boxes
are strictly narrower; this is a consistency refinement, not
independent-backend validation.

| upstream root bracket | certified \(h(4;\kappa)\) enclosure on the full bracket |
|---:|---:|
| 1 | \([3.6942432085987834026630306568684260514,\ 3.6942432085987834026630306902027183146]\) |
| 2 | \([3.6942452234303816457633197741008911442,\ 3.6942452234303816457633198101840026466]\) |
| 3 | \([3.6942476489736796102212146227195824128,\ 3.6942476489736796102212146618360033887]\) |
| 4 | \([3.6942504445405026566149833420457312433,\ 3.6942504445405026566149833845138882089]\) |
| 5 | \([3.6942535712156081158524514491947179913,\ 3.6942535712156081158524514953715743099]\) |

These are enclosures over each entire bracket.  They are not evaluations at
an already unique root: the upstream result proves at least one root per
bracket but still does not prove root uniqueness or global census
completeness.

The run used 10 finite quadrature calls, 500 quadrature callbacks and 540
Bessel evaluations.  It used no ODE solver, root solver or finite
difference, and created no automatic successor.

## What moved and what remains open

The following narrow P1 item is now closed:

- the normalization-invariant \(\lambda=0\) differentiated plus-tail datum
  \(h(4;\kappa)\) on the five certified characteristic-root brackets.

The next mathematical gap is a separate node-safe transport of this datum
from \(Q=4\) to \(Q_0=-4\), using an unwrapped Prüfer/projective atlas.  A
convention-free numerical amplitude \(F_\lambda\) away from a root still
requires an explicit amplitude normalization.  At a root, nonvanishing of
\(F_\lambda\) and the ratio \(-F_\lambda/F_\kappa\) can be tested in a
normalization-invariant way only after the transport exists.

Nonzero-\(\lambda\) tail control, endpoint root velocity, nonreal Weyl data,
spectral measure, rigging test space, RAQ, \(C/H\) quantum equivalence, BFV,
physics, quantum gravity and TOE remain explicit nulls.

## Provenance

- source commit: `54d10b1`;
- input SHA-256:
  `91e8cb4ffcc8a310b6aebfddff508a70574907901cfb71a7d0807e6567c7f691`;
- runner SHA-256:
  `9b74027a7a2be9535e427e79a709cd57efdd2015ec5e872c6c1c96f159712dee`;
- result-file SHA-256:
  `7e1d3d74534392532ec800472a2a2bac8e2e87c5f5306ff3b2842d6a9d177ad6`;
- canonical result payload SHA-256, excluding its self field:
  `a5ea98b1ec3c93173c5d8da2ce3ebafcb355737408db113d7d8f69b0882a90fc`.
