# Raw-C actual-direction sharp contraction transfer

## Question and scope

This bounded calculation asks whether the actual plus-recessive direction can
be enclosed sharply at

\[
Q_s=-\frac{29}{10},\qquad x_s=6\pi^2e^{Q_s}>3,
\]

and whether that enclosure makes the already audited scale-free
\(Q_s\to-4\) and complete left-tail map narrower than \(1/4\).  It covers
only root bracket 1, the two real boxes

\[
\lambda\in[-10^{-4},-10^{-8}],\qquad
\lambda\in[10^{-8},10^{-4}],
\]

and a \(\lambda=0\) Bessel regression.  It is not a root, spectrum, RAQ or
physics calculation.

## Sharp backward direction calculation

With \(C=6\pi^2\), \(x=Ce^Q\), and

\[
r=-\frac{u_Q}{u}=x+\frac12+\rho,
\]

the actual direction obeys

\[
\rho_x=\left(2+\frac1x\right)\rho
 +\frac{\rho^2+\kappa^2+\frac14}{x}
 -\lambda\sqrt{\frac{x}{C}}.
\]

The exact homogeneous propagator from \(t\) down to \(x_s<t\) is

\[
M(x_s,t)=e^{-2(t-x_s)}\frac{x_s}{t}.
\]

Consequently

\[
\rho(x_s)=M(x_s,x_4)\rho(x_4)
 -(\kappa^2+\tfrac14)J_0-J_{\rho^2}+\lambda J_\lambda,
\]

where

\[
J_0=x_s\int_{x_s}^{x_4}\frac{e^{-2(t-x_s)}}{t^2}\,dt,
\qquad
J_\lambda=\frac{x_s}{\sqrt C}
\int_{x_s}^{x_4}\frac{e^{-2(t-x_s)}}{\sqrt t}\,dt.
\]

The pinned invariant barrier gives \(-1\leq\rho\leq1\) throughout this
chart, so

\[
0\leq J_{\rho^2}\leq J_0.
\]

The runner encloses the two positive kernel masses using 512- and 1024-panel
monotone denominator bounds.  Each panel integrates \(e^{-2y}\) exactly;
the positive \(y\geq24\) remainder is added analytically.  This is not a
black-box ODE solve or sampled trajectory.

The resulting direction is rescaled to \(v(Q_s)=1\), then transported by
the same sixteen order-12 whole-step Taylor bounds and complete rotating-frame
left-tail quotient bound used in the preceding hybrid calculation.

## Observed result

The controlled command

```text
./ice run raw_c_actual_direction_sharp_contraction_transfer
```

returned `VALID_RUN` and
`CERTIFY_ACTUAL_DIRECTION_SHARP_CONTRACTION_AND_SCALE_FREE_GAMMA1_WIDTH_BRACKET1_ONLY`.
All 18 exact/structural checks and all 133 Arb checks passed; six theorem and
scope guards were recorded.  Both lambda-zero switch and endpoint Bessel
regressions are contained at 80 and 120 decimal digits.

At 120 digits the outward enclosures are approximately:

| parameter box | actual \(\rho(Q_s)\) | switch width | scale-free \(\Gamma_1/v(-4)\) | endpoint width |
|---|---:|---:|---:|---:|
| negative \(\lambda\) | \([-0.6463060626,-0.5185229895]\) | \(0.1277830731\) | \([-0.03079597076,0.03298735694]\) | \(0.06378332770\) |
| positive \(\lambda\) | \([-0.6462950792,-0.5185120060]\) | \(0.1277830731\) | \([-0.03081003652,0.03297233948]\) | \(0.06378237600\) |
| \(\lambda=0\) | \([-0.6462950626,-0.5185230061]\) | \(0.1277720565\) | \([-0.03076376970,0.03294059314]\) | \(0.06370436284\) |

All six 80/120-digit endpoint tiers are narrower than the fixed \(1/4\)
target.  The earlier full switch box had width 2 and produced endpoint widths
near 1.203; the contraction enclosure removes that identified bottleneck.
The nonzero-lambda complete-tail correction is about
\(1.82045\times10^{-5}\).

## Scientific boundary and next question

Every displayed endpoint interval still contains zero.  Therefore the result
does **not** determine a sign, exclude or establish a \(\Gamma_1\) zero,
continue the lambda-zero root, construct a Weyl function or spectral measure,
or supply a rigging map, RAQ completion, quantum-gravity claim, physics claim,
or TOE claim.

The remaining width is dominated by the deliberately global bound
\(0\leq J_{\rho^2}\leq J_0\), not arithmetic precision or the infinite tail.
The next independent calculation should replace that global nonlinear box by
a panelwise Picard/affine Riccati enclosure, preferably centered on the exact
\(\lambda=0\) Bessel direction and accompanied by validated
\(\partial_\lambda\rho\).  Only a substantially sharper parameter-sensitive
enclosure could support sign separation or a local root-continuation test.

## Provenance

- input SHA-256: `6e2b5f9047484c09197f0723af1a7c1c78a9f496648a8d39e4dbc268be70a9a3`;
- runner SHA-256: `a6324cd9120c29ae16064aec3872151efb4aacdd3378022d773a933cf19e275e`;
- result-file SHA-256: `3c02a76a45e8b8e054e03b6dabea7562b927b7d37585daa2a23cb442565c6453`;
- canonical result payload SHA-256, excluding its self field:
  `f3c23fb49720a85a294493c0ba4e0f2f09caa6525186837248e490498fa23baa`.
