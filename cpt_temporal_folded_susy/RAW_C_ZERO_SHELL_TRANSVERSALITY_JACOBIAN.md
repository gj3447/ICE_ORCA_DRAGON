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

## Observed execution

The reviewed definition was committed first and then executed only through the
control plane:

```text
./ice run raw_c_zero_shell_transversality_jacobian
VALID_RUN; 9/9 executable boolean checks; 3/3 numerical checks;
4 analytic theorem/scope guards
KEEP_DECLARED_RAW_C_FIVE_LOCAL_SIMPLE_ROOT_JACOBIANS_ONLY
```

The result SHA-256 is
`cfc2179c87d84b875060d05f8ff2466106af73fd18da723dfb89da5468e1647e`.
The five positive-\(p\) branch values were

| root | \(p>0\) | conditional \(\lambda'(p)\) | conditional \(1/|\lambda'|\) |
|---:|---:|---:|---:|
| 1 | 1.6513865754 | 13.3952860005 | 0.0746531280 |
| 2 | 3.2146605875 | 15.5910214561 | 0.0641394794 |
| 3 | 4.4149322571 | 15.5099449055 | 0.0644747616 |
| 4 | 5.4814417905 | 15.2508585095 | 0.0655700792 |
| 5 | 6.4692226902 | 14.9719946432 | 0.0667913677 |

The maximum \(h\)-versus-\(h/2\) derivative difference was
\(1.05\times10^{-42}\), the maximum Mellin/quadrature difference was
\(4.36\times10^{-43}\), and the minimum \(|a(Q_0)|\) was
\(3.52\times10^{-6}\).  The run used 15,735 Bessel evaluations and five
quadratures, within the declared caps.

These numbers remain conditional on the analytic moving-boundary Lagrange
identity.  They do not fill any global spectral, \(\delta(C)\), rigging-map,
physical-inner-product, or \(C\leftrightarrow H\) field.
