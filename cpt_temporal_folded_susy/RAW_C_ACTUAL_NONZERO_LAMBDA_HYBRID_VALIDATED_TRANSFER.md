# Raw-C nonzero-lambda scale-free outer-transfer pilot

## Question and scope

This bounded calculation asks whether the inherited \(x\geq3\) Riccati
barrier can be connected to \(Q_0=-4\) by a rigorous compact transfer and to
the complete \(Q<-4\) tail by a scale-free Volterra bound.  It covers the
full inherited root-1 interval in \(\kappa\), the two real boxes

\[
\lambda\in[-10^{-4},-10^{-8}],\qquad
\lambda\in[10^{-8},10^{-4}],
\]

and a \(\lambda=0\) regression control.

The switch datum is deliberately the complete inherited
\(\rho(Q_s)\in[-1,1]\) barrier box at \(Q_s=-29/10\), rescaled to
\(v(Q_s)=1\).  It contains the selected actual plus-recessive direction, but
it is not a new sharp transport of that direction from \(Q=4\) to \(Q_s\).

## Calculation

For

\[
x=6\pi^2e^Q,\qquad
v_{QQ}=A_{\lambda}v,\qquad
A_{\lambda}=x^2+\frac{\lambda x^{3/2}}{\sqrt{6\pi^2}}-\kappa^2,
\]

the runner propagates \(Y=(v,v_Q)\) over sixteen exact backward steps of
size \(-11/160\).  At Taylor order 12 it uses the actual derivative
recurrence

\[
Y^{(n+1)}=\sum_{j=0}^{n}{n\choose j}B^{(j)}Y^{(n-j)},
\qquad
B=\begin{pmatrix}0&1\\A_\lambda&0\end{pmatrix},
\]

with one endpoint factor \(1/n!\) and a whole-step outward remainder
\(D_{13}|h|^{13}/13!\).  No SciPy ODE solve, quadrature, finite difference,
root solve or sampling grid is used.

Only after the final interval for \(v(-4)\) excludes zero does the runner
form

\[
g_\lambda=\frac{\Gamma_1(v)}{v(-4)}
=\frac{v_Q(-4)}{v(-4)}
-\lambda\frac{\int_{-\infty}^{-4}a(Q)v(Q)c_p(Q)\,dQ}{v(-4)}.
\]

The second term is enclosed with the inherited rotating-frame masses on the
entire half-line.  The exact \(\lambda=0\) modified-Bessel solution is an
independent regression target for inclusion, not for sharpness.

## Observed result

The controlled command

```text
./ice run raw_c_actual_nonzero_lambda_hybrid_validated_transfer
```

returned `VALID_RUN`, with 14/14 exact checks, 113/119 Arb checks and five
theorem/scope guards.  Isolated reproduction also returned `REPRO 1` with no
item needing attention.

All six parameter/precision tiers establish the following partial facts:

- the outward interval for \(v(-4)\) is strictly positive;
- the complete quotient-tail correction is finite;
- the 80- and 120-digit enclosures overlap;
- both \(\lambda=0\) Bessel containment regressions pass.

At 120 digits the scale-free outer intervals are approximately

| box | outward interval for \(g_\lambda\) | width | tail correction upper bound |
|---|---:|---:|---:|
| negative \(\lambda\) | \([-0.6259515733,\ 0.5774079934]\) | \(1.2033595666\) | \(3.1118356842\times10^{-5}\) |
| positive \(\lambda\) | \([-0.6259606471,\ 0.5773801850]\) | \(1.2033408321\) | \(3.1118206935\times10^{-5}\) |
| \(\lambda=0\) control | \([-0.6258909693,\ 0.5773295099]\) | \(1.2032204792\) | \(0\) |

Every interval contains zero.  More importantly for the aggregate decision,
all six tiers miss the fixed width target \(1/4\).  The final verdict is
therefore

```text
HYBRID_VALIDATED_TRANSFER_NOT_CERTIFIED
```

Increasing arithmetic precision alone is not the remedy: the 80- and
120-digit widths are essentially unchanged.  The dominant uncertainty is
the full \(\rho(Q_s)\in[-1,1]\) direction box.

## What this changes, and what remains open

This is a real computational advance over the earlier enormous absolute
rectangle: the compact interval-Taylor transfer keeps the complete outer
family away from a node at \(Q_0\) and closes a finite scale-free tail
quotient.  It does not satisfy the declared sharpness gate, exclude a
\(\Gamma_1\) zero, continue a root, construct spectral or RAQ data, prove
\(C\leftrightarrow H\), or make a physics claim.

The next independent question is narrower: certify the actual
plus-recessive \(\rho(Q_s;\kappa,\lambda)\) in an interval substantially
smaller than \([-1,1]\), using a Liouville--Green-preconditioned Riccati or
equivalent validated transport from \(Q=4\) to \(Q_s\).  Only then should the
same compact/tail map be applied to a sharp actual-family input.
