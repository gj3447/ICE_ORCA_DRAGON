# Closed \(S^3\) scalar-derived harmonic ledger

## Observed result

The committed bounded run returned

```text
KEEP_CLOSED_S3_SCALAR_DERIVED_HARMONIC_NORMALIZATION_LEDGER_NOT_SVT_COMPLETENESS_OR_HDA
```

All 26 exact checks passed.  The general integrated identities and the
\(n=0\) vector/\(n=1\) tracefree-tensor degeneracies agree for the explicit
\(n=0,\ldots,4\) ledger.  This fixes scalar-derived normalizations only.

## Scope

This bounded, unnumbered calculation starts from one normalized general scalar
harmonic \(Q_I\) on unit round \(S^3\), with

\[
\Delta Q_I=-\lambda_nQ_I,\qquad \lambda_n=n(n+2).
\]

It fixes the scalar-derived gradient vector and tracefree-Hessian tensor
normalizations by integration by parts and the integrated Bochner identity.
It is neither a complete scalar-vector-tensor harmonic basis nor an ADM
constraint, Gaunt-coefficient, HDA/Jacobi or BFV calculation.

## Identities

For \(\int Q_I^2=1\) and \(\operatorname{Ric}_{ab}=2\gamma_{ab}\),

\[
\int |DQ_I|^2=\lambda_n,
\qquad
\int |D_aD_bQ_I|^2=\lambda_n(\lambda_n-2).
\]

Define

\[
V_a=\lambda_n^{-1/2}D_aQ_I \quad(n\ge1),
\]

\[
S_{ab}=D_aD_bQ_I+\frac{\lambda_n}{3}\gamma_{ab}Q_I,
\qquad
T_{ab}=\left[\frac23\lambda_n(\lambda_n-3)\right]^{-1/2}S_{ab}
\quad(n\ge2).
\]

Then \(\int V^aV_a=1\), \(\int T^{ab}T_{ab}=1\), and

\[
D^aV_a=-\sqrt{\lambda_n}Q_I,
\qquad
D^bT_{ab}=-\sqrt{\frac23(\lambda_n-3)}V_a.
\]

The low modes are not optional details: \(n=0\) has no gradient vector, and
at \(n=1\), \(\lambda_1=3\), the tracefree Hessian is zero.  Therefore the
tensor normalization begins at \(n=2\).

## Boundary

These identities only set conventions needed before the future full SVT and
Gaunt/Clebsch--Gordan ledger.  They cannot be read as finite-cutoff closure or
as a quantum anomaly result.

## Execution

```text
./ice run closed_s3_scalar_derived_harmonic_ledger
VALID_RUN; 26/26 exact checks
```

The result artifact is
`CLOSED_S3_SCALAR_DERIVED_HARMONIC_LEDGER_RESULT.json`, with outer SHA-256
`3d67333d30b5baa4a24533993b93d9028367373f8195c7bdfde4e99885cfc66f`.
