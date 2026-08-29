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

## Observed bounded result

The committed runner was executed through the repository control plane:

```text
./ice run closed_s3_zonal_conformal_curvature_cubic_vertex_ledger
```

The result is `VALID_RUN` with 52/52 executable exact checks and three
source/scope guards.  For the single-\(Q_2\) packet it gives

\[
(I_1,I_2,I_3)=\left(0,19,\frac{9\sqrt2}{2\pi}\right),
\]

and for the mixed \(Q_1+Q_2\) packet it gives

\[
(I_1,I_2,I_3)=\left(0,28,\frac{13\sqrt2}{\pi}\right).
\]

Both packets have nonzero exact quadratic and cubic tails beyond the declared
\(N=2\) cutoff.  This is a concrete truncation diagnostic: nonlinear local
curvature terms escape the retained zonal mode space.  It is still not an ADM
constraint expansion or a measurement of HDA closure.

Result SHA-256:
`d76ce0feae39c2ecd7fb13455b22e26dc4e045d491e0f1b2c73434c9ac23dc53`.
