# Raw-C Qplus-to-Qswitch kappa projective-sensitivity transport

## Independent question

On the exact correlated $K\times\Lambda$ strip, does the selected real
plus-recessive projective derivative $h=\partial_\kappa\rho$ remain uniformly
strictly negative after transport from $Q_+=4$ to
$Q_{\rm switch}=-29/10$?

This is a new bounded question aimed directly at the next missing P1 link. It
does not replay the endpoint anchor or use the sign-strip face values as
derivative evidence.

## Comparison transport

With $x=6\pi^2e^Q$ and $p=-h$, exact differentiation at fixed $\lambda$ gives

\[
p_x=\left(2+\frac{1+2\rho}{x}\right)p-\frac{2\kappa}{x}.
\]

The pinned selected-family barrier $-1\leq\rho\leq1$ gives

\[
2-\frac1x\leq2+\frac{1+2\rho}{x}\leq2+\frac3x.
\]

Variation of constants therefore bounds the backward transport by the two
positive kernels

\[
e^{-2(t-a)}(a/t)^3,
\qquad e^{-2(t-a)}(t/a),
\]

where $a=x(Q_{\rm switch})$. The lower forcing integral is enclosed by
monotone 512/1024-panel ladders at 80/120 decimal digits through $y=24$;
the remaining nonnegative tail is discarded from the lower bound. The upper
forcing integral over the complete segment simplifies exactly because the
factor $t/a$ cancels the $1/t$ forcing.

The singular endpoint is not assigned an extra $C^1$ hypothesis. The upstream
anchor already supplies the derivative at $Q_+$; standard smooth parameter
dependence of the finite Riccati initial-value problem on the certified finite
$\rho$ tube propagates that seed over this leg.

An elementary $\Delta Q=1/10$ comparison also gives the independent strict
floor $p(Q_{\rm switch})>\kappa_{\rm left}/20>0$. The frozen relaxations are
$x_{\rm switch}<15/4$, $e^{1/10}-1<1/9$, and $e^{17/15}<4$.

## Explicit boundary

Even a strict signed result here is only a selected projective derivative at
$Q_{\rm switch}$. It does not provide the $Q_0$ derivative, the reference
state's kappa variation, the complete differentiated minus tail,
$\partial_\kappa G$, a mixed derivative, root transversality or uniqueness, a
selector, continuation, velocity, absolute $\Gamma_1$ amplitude/sign, global
roots, nonreal Weyl/spectral data, RAQ, BFV, a physical product, or physics.

## Controlled execution

- Frozen input SHA-256:
  `dff13b4a24cd8ea3f5ff76bd72778815dc3a608ec155463b8ee31e0fdbde446e`
- Frozen runner SHA-256:
  `cf2b2171ef0a9029d220195e0cbd0b0c0bd4ce5b5e3974894589dd6a25c031b3`
- Common caps: 120 seconds; 262,144 bytes each for stdout/stderr; at most
  12 changed artifacts and 1,000,000 changed bytes.
- Declared calculation calls: 3,072 positive-kernel panels across the two
  precision tiers, and zero Bessel, ODE, quadrature, root, finite-difference,
  sampling, compact-transfer or bisection calls.

This is the pre-run source record. No result is claimed before the frozen
runner is committed cleanly and invoked through `./ice run`.
