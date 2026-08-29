# Closed \(S^3\) zonal conformal-curvature cubic-vertex ledger

## Scope

This is an exact, bounded ledger for one geometric contribution that would
enter a later ADM potential expansion: the spatial scalar-curvature density
of a conformally perturbed, **zonal** unit-three-sphere.  It neither derives
the ADM constraints nor substitutes for their cubic expansion.

The three pinned upstream results fix the homogeneous ADM convention, the
normalized zonal product/projection rule, and the all-sector spectral
convention.  Their explicit boundaries remain in force: no complete SVT
basis, nonzonal Gaunt data, constraint algebra, BFV construction, or physical
claim is imported here.

## Declared geometry

With \(\gamma_{ab}\) the unit round \(S^3\) metric, \(R[\gamma]=6\), and
\(\Delta=D^aD_a\), take

\[
q_{ab}(\epsilon)=a^2e^{2\epsilon\psi}\gamma_{ab},
\]

where \(a\) is a spatial constant and \(\psi\) is a finite zero-mean zonal
packet.  The source-pinned conformal transformation gives

\[
\frac{\sqrt q\,R[q]}{a\sqrt\gamma}
=e^{\epsilon\psi}
\left(6-4\epsilon\Delta\psi-2\epsilon^2|D\psi|^2\right).
\]

The runner records only its coefficients through cubic order,

\[
\begin{aligned}
d_1&=6\psi-4\Delta\psi,\\
d_2&=3\psi^2-4\psi\Delta\psi-2|D\psi|^2,\\
d_3&=\psi^3-2\psi^2\Delta\psi-2\psi|D\psi|^2.
\end{aligned}
\]

On compact boundaryless \(S^3\), integration by parts gives

\[
I_1=6\!\int\psi,\qquad
I_2=3\!\int\psi^2+2\!\int|D\psi|^2,\qquad
I_3=\!\int\psi^3+2\!\int\psi|D\psi|^2.
\]

The conformal formula and the closed-manifold integration-by-parts theorem
are recorded as source/theorem guards.  The executable work verifies their
exact transport into the predeclared zonal algebra; it is not a computer proof
of either theorem.

## Zonal cutoff diagnostic

For

\[
Q_n(\chi)=\frac{U_n(\cos\chi)}{\sqrt{2\pi^2}},
\qquad \Delta Q_n=-n(n+2)Q_n,
\]

the runner uses the upstream exact product rule to form \(d_1,d_2,d_3\).
For each packet it then splits the local coefficients as

\[
d_r=P_Nd_r+(1-P_N)d_r,\qquad r=2,3,
\]

and records the coefficient vectors and squared norms of the tails.  These
tails measure the loss caused by a hard finite zonal cutoff after a nonlinear
local operation.  They are not Poisson-bracket residuals and cannot be called
an HDA or quantum anomaly.

## Fail-closed boundary

The runner leaves null: an explicit complete scalar/vector/tensor basis;
nonzonal or SVT Gaunt data; linear or cubic ADM constraints; momentum/kinetic,
matter, lapse, and shift terms; lapse-shift brackets; \(DD\), \(DH\), or
\(HH\) closure; Jacobi; BFV charge or anomaly; RAQ; observables; likelihood;
and physics or TOE claims.

If this bounded packet is later used, the next actual obstacle is not more
zonal algebra.  It is an off-shell ADM expansion with canonical momenta,
lapse/shift treatment, and nonzonal scalar plus SVT coupling data.

## Intended execution

After review and a clean commit, execute only through the repository control
plane:

```text
./ice run closed_s3_zonal_conformal_curvature_cubic_vertex_ledger
```

No runner was executed while preparing this draft.
