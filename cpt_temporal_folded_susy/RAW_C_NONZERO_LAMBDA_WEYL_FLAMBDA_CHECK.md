# Finite-cutoff nonzero-\(\lambda\) raw-\(C\) \(F_\lambda\) check

## Narrow question

This bounded runner independently tests one previously conditional local
identity at the five hash-pinned raw-\(C\) zero-shell roots.  It does **not**
construct RAQ, a global spectral measure, or a physical state space.

For the positive \(p\) branch, it uses

\[
2u''+\left[3p^2-72\pi^4e^{2Q}-12\pi^2\lambda e^{3Q/2}\right]u=0,
\qquad p=\sqrt{\frac23}\kappa .
\]

The prior census pins five \(\kappa\) roots of the declared
\(\Gamma_{1,p}=0\) zero-shell condition.  The prior conditional ledger pins

\[
F_\lambda(0)=-\frac{N_f}{2a},\qquad
a=K_{i\kappa}(z_0),\qquad z_0=6\pi^2e^{-4}.
\]

Here the propagated solution is rescaled at \(Q_0=-4\) so that
\(u_\lambda(Q_0)=1\).  Thus the comparable prediction is

\[
\partial_\lambda F^{\rm norm}(0)=-\frac{N_f}{2a^2}.
\]

This is a scale conversion only; it does not add a spectral normalization.

## Node-safe numerical route

At finite \(Q_+\), the runner seeds a decaying WKB proxy with

\[
u(Q_+)=1,qquad
u'(Q_+)=-\left(\sqrt A+\frac{A'}{4A}\right),
\]

where

\[
A=\frac{72\pi^4e^{2Q}+12\pi^2\lambda e^{3Q/2}-3p^2}{2}.
\]

It propagates the two-component linear system \((u,u')\) backwards in
segments, rescaling the vector after each segment.  This deliberately avoids
the Riccati ratio \(u'/u\): roots 2 and 4 have negative
\(K_{i\kappa}(z_0)\), and the associated large-\(Q\) logarithmic derivative
route can cross a node before \(Q_0\).

After checking the nonzero normalization denominator at \(Q_0\), the runner
propagates to the finite minus cutoff alongside the fixed zero-energy
reference pair

\[
c(Q_0)=1,qquad c'(Q_0)=0.
\]

The actual finite-cutoff characteristic is

\[
F_{Q_-}(\lambda;p)=-W(u_\lambda,c)(Q_-).
\]

At nonzero \(\lambda\), replacing this by \(u_\lambda'(Q_0)\) would be
wrong: the Wronskian is not then constant.  The runner requires stabilization
between \(Q_-=-16\) and \(-14\), a two-cutoff control for the approximate
plus-end datum (\(Q_+=1.6\) versus \(1.4\)), and a central-difference ladder
\(10^{-4},5\cdot10^{-5},2.5\cdot10^{-5}\).

## Checks and failure handling

For every pinned root the result records the \(\lambda=0\) residual,
normalization denominator, plus/minus cutoff shifts, delta-refinement shift,
direct \(p\leftrightarrow-p\) parity sentinel, and comparison with the
separately pinned conditional prediction.  At \(\lambda=0\), it also compares
the scaled finite-\(Q_-\) Wronskian with the independently retained
\(u'(Q_0)\) value, where the Wronskian is constant.  The declared caps are 120 seconds,
4,500 bounded ODE calls, 4,500 integration segments, and a 1 MB result.

A finite plus-cutoff mismatch, a node making the \(Q_0\) denominator too
small, a solver failure, a negative WKB \(A\), or lack of stabilization makes
the result fail closed.  Such a failure says this finite numerical
realization did not validate the comparison; it is not a disproof of the
analytic moving-boundary identity.

## Explicit nulls

Even a passing result supplies only a numerical finite-cutoff check of a
declared local characteristic derivative.  It leaves global spectral or
\(\delta(C)\) measure, test space, rigging map, positivity, observables,
raw-\(C\) RAQ completion, \(C\leftrightarrow H\) equivalence, BFV claims,
inhomogeneous anomaly claims, phenomenology, physics claims, and TOE claims
null.

No result is included in this draft.  Once clean and committed, it may be
executed only through the repository control plane:

```text
./ice run raw_c_nonzero_lambda_weyl_flambda_check
```
