# Fixed-background zonal \(V=0\) scalar-matter \(HH\) bracket ledger

## Scope

This is the smallest local bracket calculation on the closed-\(S^3\) route.
It deliberately keeps the spatial metric fixed,

\[
q_{ab}=a^2\gamma_{ab},\qquad a>0,
\]

and retains only a massless scalar field in the normalized zonal basis

\[
Q_n(\chi)=\frac{U_n(\cos\chi)}{\sqrt{2\pi^2}},
\qquad
\Delta Q_n=-n(n+2)Q_n.
\]

Writing

\[
\phi=\sum_n\theta_nQ_n,\qquad
\pi_\phi=\sqrt\gamma\sum_n\xi_nQ_n,\qquad
\{\theta_i,\xi_j\}=\delta_{ij},
\]

the declared scalar pieces are

\[
H_\phi[N]=\frac12\int\sqrt\gamma\,N
\left(a^{-3}\xi^2+a|D\theta|^2\right),
\qquad
D_\phi[v]=\int\sqrt\gamma\,\xi v^aD_a\theta.
\]

The target identity is the matter-only fixed-metric relation

\[
\{H_\phi[N],H_\phi[M]\}=D_\phi[v_{NM}],
\qquad
v_{NM}^a=a^{-2}(ND^aM-MD^aN).
\]

The selected lapses are \(N=Q_1\) and \(M=Q_2\).  They are the smallest
distinct nonconstant zonal pair.  The three declared packets hold
\(\theta=Q_2\) and \(\xi=Q_1\) at scalar cutoffs \(L=2,3,4\).  This
asymmetric packet is selected because its continuum matter target is
nonzero.  At \(L=2\), the ambient calculation also has a nonzero \(k=3\)
canonical derivative channel which the projected calculation omits; at
\(L\geq3\) that channel is retained.

## Exact cutoff comparison

For each \(L\), the runner makes two different finite calculations.

1. **Full-before-project control.** It first forms and differentiates both
   Hamiltonians in the ambient coefficient space through
   \(L+\max(\deg N,\deg M)=L+2\), then substitutes all modes above \(L\)
   to zero.
2. **\(L\)-only bracket.** It forms the canonical bracket only after the
   scalar field has been restricted to \(0\leq n\leq L\).

The difference is decomposed into the omitted ambient canonical derivative
channels.  It is labelled a finite `UNCLASSIFIED_PROJECTION_REMAINDER`, even
if it happens to be nonzero.  It is neither a continuum HDA residual nor an
anomaly statement.

The coefficient implementation uses the exact identities

\[
\int Q_iQ_jQ_k=
\frac{1}{\sqrt{2\pi^2}}\,\mathbf 1_{k\in\{|i-j|,|i-j|+2,\ldots,i+j\}},
\]

and

\[
\int Q_iD Q_j\!\cdot\!D Q_k
=\frac{\lambda_j+\lambda_k-\lambda_i}{2}\int Q_iQ_jQ_k,
\qquad\lambda_n=n(n+2).
\]

Four low-degree triple and gradient coefficients are checked independently by
direct \(\chi\)-integration.  No numerical quadrature, ODE or root solve is
used.

## Boundaries retained

This runner does not construct the gravitational Hamiltonian or momentum
constraint, metric/scalar gauge completion, shear sector, nonzonal or full
SVT Gaunt data, full linear/cubic ADM constraints, \(DD\) or \(DH\) brackets,
Jacobi closure, BFV charge, anomaly freedom, a physical inner product, or a
physical/TOE claim.

It is an implementation definition only until the controlled command below
is run and its result is independently reproduced.

```text
./ice run closed_s3_zonal_v0_scalar_matter_hh_bracket_cutoff_ledger
```
