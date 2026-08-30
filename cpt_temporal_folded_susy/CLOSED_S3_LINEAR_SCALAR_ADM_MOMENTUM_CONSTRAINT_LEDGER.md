# Linear scalar ADM momentum-constraint generator ledger

## Declared packet

This exact bounded packet supplies one missing gravitational metric-variation
ingredient.  It is not a Hamiltonian constraint or a hypersurface-deformation
algebra calculation.

On unit \(S^3\), write the linear scalar metric perturbation as

\[
q_{ab}=a^2\bigl[\gamma_{ab}+2\zeta\gamma_{ab}+2S_{ab}(E)\bigr],
\qquad
S_{ab}(E)=D_aD_bE-\frac13\gamma_{ab}\Delta E.
\]

The runner deliberately uses the **unnormalized** scalar-derived tensor
\(S_{ab}(Q_n)\), with

\[
N_n^2=\int S_{ab}(Q_n)S^{ab}(Q_n)
=\frac23\lambda_n(\lambda_n-3),\qquad \lambda_n=n(n+2),
\]

and momentum convention

\[
\delta\pi^{ab}=\frac{\sqrt\gamma}{a^2}
\left[\frac{\Pi_{\zeta,n}}6\gamma^{ab}
+\frac{\Pi_{E,n}}{2N_n^2}S_n^{ab}\right].
\]

Consequently the symplectic potential gives the canonical pairs
\((\zeta_n,\Pi_{\zeta,n})\) and \((E_n,\Pi_{E,n})\), without mixing this
with the alternate normalized-\(\widehat S_n\) convention.

## Exact target

From

\[
D_a=-2q_{ac}\nabla_b\pi^{bc},
\]

and

\[
D^bS_{ab}(Q_n)=-\frac23(\lambda_n-3)D_aQ_n,
\]

the projection against the gradient shift \(v^a=D^aL\) is

\[
D_L^{(1)}=\sum_{n\ge2}L_n
\left(\Pi_{E,n}-\frac{\lambda_n}{3}\Pi_{\zeta,n}\right).
\]

The same generator yields

\[
\delta_LE_n=L_n,\qquad
\delta_L\zeta_n=\frac{\Delta L_n}{3}
=-\frac{\lambda_n}{3}L_n.
\]

For the earlier coordinate \(\zeta=\psi+\Delta E/3\), this gives
\(\delta_L\psi=0\) and \(\delta_LE=L\), recovering the earlier
kinematic longitudinal-coordinate convention as a consequence of the
declared ADM projection.

The executable packet retains metric modes \(n=2,3\), gradient shift labels
\(Q_1,Q_2\), and records the \(n=0,1\) exceptions.  In particular,
\(S_{ab}(Q_1)=0\), so no \(E_1,\Pi_{E,1}\) canonical pair is admitted.
The explicit harmonic projection matrix also records that \(Q_1\) acts as
zero on this retained \(n=2,3\) packet, whereas \(Q_2\) selects only its
\(n=2\) metric pair.  Nonconstancy of a shift is not confused with support
inside the chosen finite packet.

## Boundary

This calculation excludes the transverse-vector shift sector.  A commutator
of gradient shifts can require that sector, so it cannot establish even a
scalar-only \(DD\) closure.  It also leaves the Hamiltonian constraint,
\(DH\), \(HH\), cubic contributions, Jacobi, BFV, anomaly and physics claims
null.

## Observed result

The controlled command

```text
./ice run closed_s3_linear_scalar_adm_momentum_constraint_ledger
```

returned `VALID_RUN`, with 31/31 exact checks and three theorem/scope guards.
The explicit mode results are

\[
n=2:\quad N_2^2=\frac{80}{3},\qquad
D_{L_2}^{(1)}=L_2\left(\Pi_{E,2}-\frac83\Pi_{\zeta,2}\right),
\]

\[
n=3:\quad N_3^2=120,\qquad
D_{L_3}^{(1)}=L_3\left(\Pi_{E,3}-5\Pi_{\zeta,3}\right).
\]

Isolated reproduction returned `REPRO 1` with no item needing attention.  The
final verdict is

```text
KEEP_UNIT_S3_LINEAR_SCALAR_ADM_MOMENTUM_CONSTRAINT_GENERATOR_NOT_FULL_HDA
```

The result establishes only the declared unit-\(S^3\) linear scalar
momentum-generator projection.  All Hamiltonian, \(DD/DH/HH\), Jacobi,
full-SVT, BFV, anomaly and physics outputs remain null.
