# Unit closed \(S^3\) SVT spectral, degeneracy, and exceptional-mode ledger

## Scope

This bounded ledger records spectral and counting conventions for scalar,
transverse-vector, and transverse-traceless tensor sectors on unit round
\(S^3\).  It does not provide explicit full basis functions, Gaunt data, an
ADM action or constraint expansion.  `FULL_SVT` means only that all three
spectral sectors occur in one packet; it does not mean an explicit basis,
chirality resolution, or a proof of completeness.

The spectrum, degeneracies, and geometric low-mode statements are imported as
source-pinned theorem guards from Lindblom--Taylor--Zhang (Gen. Rel. Grav. 49
(2017) 139) and Higuchi (including the 2002 erratum).  The executable portion
checks transport into a separately fixed low-mode table, operator-shift
arithmetic, exceptional norm-polynomial consequences, and finite cutoff sums.
It is not a computer proof of the source theorems.

The positive rough Laplacian is \(\Delta_{\rm rough}=-D^2\).  For one-forms
the declared Hodge operator is \(\Delta_H=\Delta_{\rm rough}+2\).  For
tracefree symmetric two-tensors, the declared Lichnerowicz convention is
\(\Delta_L=\Delta_{\rm rough}+6\).  These are different operators and their
eigenvalues must not be interchanged.

Explicitly, the sign convention is

\[
R_{ikjl}=\gamma_{ij}\gamma_{kl}-\gamma_{il}\gamma_{kj},
\]

\[
(\Delta_Lh)_{ij}=-D^2h_{ij}+R_i{}^kh_{kj}+R_j{}^kh_{ik}
-2R_{ikjl}h^{kl}.
\]

For tracefree \(h\), the two Ricci terms and the Riemann term contribute
\(2+2+2=6\).  This fixes exactly what the displayed Lichnerowicz eigenvalues
mean; other sign conventions must be translated before comparison.

## Sector data

With \(\lambda_n=n(n+2)\), the ledger uses

\[
d_0(n)=(n+1)^2,\quad n\ge0,
\]

\[
d_1(n)=2n(n+2),\quad n\ge1,
\]

\[
d_2(n)=2(n-1)(n+3),\quad n\ge2.
\]

The vector and TT rough eigenvalues are \(\lambda_n-1\) and
\(\lambda_n-2\), respectively.  The \(n=1\) transverse vectors are Killing:
their symmetrized gradient vanishes.  The TT sector begins at \(n=2\).
The vector and TT degeneracy polynomials are not interpreted as sector counts
below their declared ranges; in particular, the negative value obtained by
formally inserting \(n=0\) into \(d_2\) has no spectral meaning.

For the scalar-derived objects,

\[
G_a=\lambda_n^{-1/2}D_aQ,\qquad
\int|G|^2=1,
\]

and

\[
S_{ab}=D_aD_bQ+\frac{\lambda_n}{3}\gamma_{ab}Q,
\qquad
\int|S|^2=\frac23\lambda_n(\lambda_n-3).
\]

Thus \(S_{ab}\) vanishes at \(n=1\); it is normalized only for \(n\ge2\).
All of these identities are harmonic bookkeeping, not ADM or BFV closure.

This corrected definition has not yet been executed.  After a clean commit,
the only authorized command is:

```text
./ice run closed_s3_full_svt_spectral_ledger
```
