# Declared raw-\(C\) zero-shell local transversality and Jacobian ledger

## Scope

This calculation starts from the five roots already recorded by the bounded
raw-\(C\) zero-shell characteristic census.  It asks only whether those five
declared roots pass bounded local-simplicity controls and records conditional
local change-of-variable factors.  The factors assume the moving-boundary
Lagrange identity below: this runner does not construct the \(\lambda\ne0\)
plus-end Weyl solution or independently finite-difference \(F_\lambda\).  It
does not construct a global spectral measure or RAQ.

The generalized equation and declared boundary line are

\[
L_pu=\lambda f u,
\qquad
f(Q)=12\pi^2e^{3Q/2},
\qquad
\Gamma_{1,p}u=0.
\]

At \(\lambda=0\), \(\hbar=1\), and on the positive \(p\) branch,

\[
u_0(Q)=K_{i\kappa}(z),
\qquad z=6\pi^2e^Q,
\qquad \kappa=\sqrt{\frac32}p.
\]

## Weighted Lagrange identity

Let \(a=u_0(Q_0)\), with \(Q_0=-4\), and let \(F(\lambda,p)\) be the
declared characteristic boundary function.  The parameter variation must keep
the boundary-domain variation.  The resulting Lagrange identity is

\[
F_\lambda(0)=-\frac{1}{2\hbar^2a}N_f,
\qquad
N_f=\int_{\mathbb R}f(Q)u_0(Q)^2\,dQ.
\]

Therefore, at a simple characteristic root,

\[
\lambda_j'(p)=-\frac{F_p}{F_\lambda}
=\frac{2\hbar^2aF_p}{N_f}.
\]

For \(p>0\),

\[
F_p=\sqrt{\frac32}F_\kappa.
\]

Since the declared spectrum is even in \(p\), the negative branch has the
opposite local slope:

\[
\lambda_j'(-p)=-\lambda_j'(p).
\]

Conditional on this analytic identity and its endpoint hypotheses, the runner
records the local quantity

\[
\frac1{|\lambda_j'(p)|}
\]

for the five pinned roots only.

## Mellin normalization

With \(dQ=dz/z\),

\[
N_f=\frac{\sqrt{2/3}}{\pi}
\int_0^\infty z^{1/2}K_{i\kappa}(z)^2\,dz.
\]

The Mellin identity used is Gradshteyn–Ryzhik, 8th ed., formula 6.576(4):

\[
\int_0^\infty z^{\mu-1}K_\nu(z)^2dz
=\frac{2^{\mu-3}}{\Gamma(\mu)}
\Gamma\!\left(\frac\mu2\right)^2
\Gamma\!\left(\frac\mu2+\nu\right)
\Gamma\!\left(\frac\mu2-\nu\right),
\]

at \(\mu=3/2\), \(\nu=i\kappa\).  The gamma-expression is the primary
normalization; one finite log-\(z\) quadrature per root is only an independent
cross-check.  The numerical ledger also compares centered \(F_\kappa\)
derivatives at steps \(h\) and \(h/2\) before Richardson extrapolation, and
measures complex leakage during the quadrature instead of replacing it by a
declared zero.

## Why fixed-domain Hellmann–Feynman is excluded

The tempting expression

\[
\int |u_0|^2dQ
\]

is not used.  At the limit-circle minus end, \(K_{i\kappa}(z)\) has an
oscillatory nondecaying magnitude as \(z\to0\), so this unweighted integral
diverges.  It also ignores the \(p\)-dependent self-adjoint boundary domain.
The Wronskian/Lagrange identity above is the declared replacement.

## Fail-closed boundary

These are conditional local characteristic Jacobians, not a completed
delta-constraint measure.  In particular, a direct nonzero-\(\lambda\)
calculation of \(F_\lambda\) remains open.  The runner leaves null: global
spectral and \(\delta(C)\) measures;
rigging test space and rigging map; physical inner-product positivity and
observable action; RAQ completion; raw-\(C\)/selected-\(H\) equivalence; and
all BFV, inhomogeneous, observational, physics, and TOE outputs.

## Intended execution

After review and clean commit, execute only through the control plane:

```text
./ice run raw_c_zero_shell_transversality_jacobian
```

No runner was executed while preparing this draft.
