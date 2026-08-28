# Gate 1 — closed \(S^3\) scalar harmonic projection ledger

## Result

This run is a kinematic ledger for one normalized scalar *zonal* subspace on a
unit three-sphere, centered on one pole and truncated at \(L=2\).  It does not
define canonical perturbation variables or a gravitational constraint system.

\[
Z_n(\chi)=\frac{1}{\sqrt{2\pi^2}}C_n^{(1)}(\cos\chi)
=\frac{1}{\sqrt{2\pi^2}}\frac{\sin((n+1)\chi)}{\sin\chi},
\qquad \Delta_{S^3}Z_n=-n(n+2)Z_n.
\]

The observed verdict is

```text
KEEP_CLOSED_S3_SCALAR_ZONAL_FINITE_CUTOFF_PRODUCT_REMAINDER_LEDGER_NOT_HDA
```

All 56 executable exact checks passed.  The calculation contains no numerical
quadrature, root solve or ODE solve.

## Exact finite-cutoff facts

For the unit-\(S^3\) volume form
\(dV=\sin^2\chi\,d\chi\,d\Omega_2\), the declared zonal functions are
orthonormal.  The product identity is

\[
Z_lZ_m=\frac{1}{\sqrt{2\pi^2}}
\sum_{k=0}^{\min(l,m)}Z_{l+m-2k}.
\]

Projection \(P_2\) retains only \(Z_0,Z_1,Z_2\).  In particular,

\[
Z_2^2=\frac{1}{\sqrt{2\pi^2}}(Z_4+Z_2+Z_0),
\]

so the finite cutoff discards the explicit remainder

\[
R_{22}=\frac{1}{\sqrt{2\pi^2}}Z_4,
\qquad \lVert R_{22}\rVert^2=\frac{1}{2\pi^2}.
\]

The non-associativity of the *projected product* is also an exact finite
truncation fact:

\[
P_2(P_2(Z_1Z_2)Z_2)-P_2(Z_1P_2(Z_2Z_2))
=-\frac{Z_1}{2\pi^2}.
\]

It is reconstructed from the recorded discarded pieces,

\[
-P_2(R_{12}Z_2)+P_2(Z_1R_{22}),
\qquad R_{12}=\frac{1}{\sqrt{2\pi^2}}Z_3.
\]

This is not an ADM bracket anomaly and it is not a failure of the continuum
harmonic algebra.  It is the ordinary loss of closure caused by applying a
finite projector before further multiplication.

## Scope boundary

The run does **not** construct or test an ADM-plus-matter action, scalar-vector-
tensor completeness, hypersurface-deformation algebra, classical Jacobi
identity, quantum BFV charge, BRST nilpotency, anomaly freedom, relational
observable, decoherence map or likelihood.  It supplies no physical state,
quantum-gravity result, physics claim or TOE claim.

Antipodal parity is only a consistency control of this zonal product basis:
\(Z_n(\pi-\chi)=(-1)^nZ_n(\chi)\).  It does not impose a quotient or boundary
condition.

## Execution and reproduction record

```text
./ice run gate1_v0_closed_s3_scalar_harmonic_projection_ledger
VALID_RUN; 56/56 executable exact checks

./ice repro --only gate1_v0_closed_s3_scalar_harmonic_projection_ledger
REPRO; 1 checked; 0 needs-attention

npm run check
67/67 tests passed
```

The definition was committed in `80a441d57e794f794dd102c26d11729d9eed1b9b`,
the successful result in `27b85feee0869ce507c982c314d31e36518b6b58`, and the
reproduction mapping in `974ded457d1357159d7eb05c2624e091a6bd390f`.

The pinned input, runner and raw result are

- `GATE1_V0_CLOSED_S3_SCALAR_HARMONIC_PROJECTION_LEDGER_INPUTS.json`
- `gate1_v0_closed_s3_scalar_harmonic_projection_ledger.py`
- `GATE1_V0_CLOSED_S3_SCALAR_HARMONIC_PROJECTION_LEDGER_RESULT.json`
