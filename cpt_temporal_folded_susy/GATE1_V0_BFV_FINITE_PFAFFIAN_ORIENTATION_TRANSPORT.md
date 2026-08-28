# Gate 1 — finite BFV Pfaffian relative-orientation transport

## Outcome

For one declared finite odd direct sum, consisting of the pinned zero block
and one pinned (m=2) nonzero block, the ordered Pfaffian has a nonvanishing
relative sign on

\[
\lambda\in[1/2,2].
\]

With the inherited concatenated odd order

\[
(\rho_0,\bar\rho_0,g_1,b_1,\rho_1,\bar\rho_1),
\]

the exact result is

\[
\operatorname{Pf}(A_0\oplus A_1)
=-\lambda(\lambda^2+\pi^2),
\qquad
\frac{\operatorname{Pf}(A(\lambda))}{\operatorname{Pf}(A(1))}
=\frac{\lambda(\lambda^2+\pi^2)}{1+\pi^2}>0.
\]

The bounded verdict is therefore

```text
KEEP_V0_FINITE_POSITIVE_LAMBDA_ODD_PFAFFIAN_RELATIVE_ORIENTATION_TRANSPORT
```

This transports only the relative odd-basis sign from the declared
\(\lambda=1\) reference. It does not construct an absolute BFV measure.

## Declared finite matrices

\[
A_0(\lambda)=
\begin{pmatrix}0&-\lambda\\ \lambda&0\end{pmatrix},
\qquad
\operatorname{Pf}(A_0)=-\lambda,
\qquad
\det A_0=\lambda^2,
\]

and, in the declared \((g_1,b_1,\rho_1,\bar\rho_1)\) order,

\[
A_1(\lambda)=
\begin{pmatrix}
0&-\lambda&0&\pi\\
\lambda&0&\pi&0\\
0&-\pi&0&-\lambda\\
-\pi&0&\lambda&0
\end{pmatrix}.
\]

Its exact finite factor is

\[
\operatorname{Pf}(A_1)=\lambda^2+\pi^2,
\qquad
\det A_1=(\lambda^2+\pi^2)^2.
\]

The declared bosonic comparison matrix is

\[
M_1=\begin{pmatrix}\pi&\lambda\\\lambda&-\pi\end{pmatrix},
\qquad
\det M_1=-(\lambda^2+\pi^2)<0.
\]

That last sign is deliberately not converted into a Gaussian contour, Maslov
phase, or square-root prescription.

## Eight exact checks

All eight checks passed in the committed bounded execution.

1. (A_0), (A_1), and (A_0\oplus A_1) are antisymmetric in their declared orders.
2. \(\operatorname{Pf}(A_0)=-\lambda\) and \(\det A_0=\lambda^2\).
3. \(\operatorname{Pf}(A_1)=\lambda^2+\pi^2\) and \(\det A_1=\operatorname{Pf}(A_1)^2\).
4. The concatenated-order direct-sum Pfaffian is \(-\lambda(\lambda^2+\pi^2)\).
5. Its ratio to the \(\lambda=1\) reference is strictly positive on \([1/2,2]\).
6. \(\lambda=0\) degenerates the zero block while the \(m=2\) block remains nondegenerate.
7. The \(\lambda=-1/2\) control reverses the Pfaffian sign and any real continuation crosses the sole zero at \(0\).
8. \(\det M_1<0\) does not select a bosonic contour or phase.

## Boundary

The calculation leaves null: absolute finite or functional BFV measure,
bosonic contour/Maslov phase, lapse modulus or contour, endpoint polarization,
Gribov data, two-slab gluing, continuum determinant/Pfaffian line, BRST
cohomology, raw-\(C\) equivalence, anomaly freedom, observables, empirical
likelihood, quantum-gravity, physics, and TOE claims.

The cited determinant-line literature supplies only the interpretation boundary:
a nonvanishing family has relative line data after a basis/reference is fixed.
It does not promote this two-block interval to a continuum determinant-line or
absolute-measure result.

## Provenance and reproduction

Definition commit: `98c6310d13345756440cafc84b94426bb387b623`.

Observed result commit: `d36445e3b4ea166bcd69b118f30532243f2270e6`
(2026-08-28T07:27:54Z), produced by:

```text
./ice run gate1_v0_bfv_finite_pfaffian_orientation_transport
```

Observed output: `VALID_RUN; 8/8 exact checks; 3 theorem guards`.

The reproduction-manifest mapping was registered in
`974ded457d1357159d7eb05c2624e091a6bd390f`
(2026-08-28T07:29:18Z). The raw result is
[`GATE1_V0_BFV_FINITE_PFAFFIAN_ORIENTATION_TRANSPORT_RESULT.json`](GATE1_V0_BFV_FINITE_PFAFFIAN_ORIENTATION_TRANSPORT_RESULT.json),
with outer SHA-256
`1a4ecfb9c955e564e142aeb800b9e591eb425ed34765330f882452d1ac16e8c8`
and payload SHA-256
`ef341b5f2427f35e81d2cf25476b2fce8b7f7d640e3e46bed2995b8188b57ffc`.
