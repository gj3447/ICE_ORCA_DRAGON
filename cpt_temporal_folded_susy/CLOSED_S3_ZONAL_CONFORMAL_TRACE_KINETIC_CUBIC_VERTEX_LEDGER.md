# Closed \(S^3\) zonal conformal-trace kinetic cubic-vertex ledger

## Scope

This bounded ledger evaluates the ADM DeWitt kinetic density on one explicitly
restricted cotangent submanifold.  It complements the separate zonal
conformal-curvature ledger, but their combination is still not a cubic ADM
constraint: the scale cotangent sector, shear, lapse, shift, matter, and all
nonzonal/SVT data remain absent.

The upstream ADM, zonal-convolution, full-SVT, and curvature ledgers are
hash-pinned.  Their stated non-constraint and non-HDA boundaries are retained.

## Restricted canonical ansatz

Hold \(a>0\) fixed and set

\[
q_{ab}=a^2e^{2\omega}\gamma_{ab},
\qquad
\pi^{ab}=
\frac{\sqrt\gamma\,\Pi}{6a^2e^{2\omega}}\gamma^{ab}.
\]

This normalization is chosen for the restricted variation:

\[
\pi^{ab}\delta_\omega q_{ab}=\sqrt\gamma\,\Pi\,\delta\omega.
\]

It also fixes the sometimes easy-to-miss DeWitt factor:

\[
\pi=\frac{\sqrt\gamma\Pi}{2},\qquad
\pi^{ab}\pi_{ab}=\frac{\gamma\Pi^2}{12},
\]

\[
\pi^{ab}\pi_{ab}-\frac12\pi^2=-\frac{\gamma\Pi^2}{24}.
\]

Therefore the ADM kinetic density becomes

\[
\frac{\mathcal H_{\rm kin}}{\sqrt\gamma}
=-\frac{2\pi G}{3a^3}e^{-3\omega}\Pi^2.
\]

The external factor \(-2\pi G/(3a^3)\) is preserved symbolically.  It is
not \(-8\pi G/(3a^3)\): that larger value is inconsistent with the displayed
canonical \(\Pi\) normalization.

## Cubic packet coefficients

For \(\omega=\epsilon\psi\) and
\(\Pi=\overline P+\epsilon\chi\), the runner declares
\(\overline P=1\) only as a dimensionless packet normalization.  It does not
assign a physical background momentum.  The dimensionless expansion is

\[
e^{-3\epsilon\psi}(\overline P+\epsilon\chi)^2
=k_0+\epsilon k_1+\epsilon^2k_2+\epsilon^3k_3+O(\epsilon^4),
\]

\[
\begin{aligned}
k_1&=2\overline P\chi-3\overline P^2\psi,\\
k_2&=\chi^2-6\overline P\psi\chi+\frac92\overline P^2\psi^2,\\
k_3&=-3\psi\chi^2+9\overline P\psi^2\chi-\frac92\overline P^2\psi^3.
\end{aligned}
\]

The normalized zonal product algebra forms these exact coefficient vectors for
two \(N=2\) packets.  The runner records \(P_Nk_2\), \(P_Nk_3\), their
orthogonal tails, and exact tail norms.  A tail is only hard-cutoff leakage in
this restricted nonlinear density; it is not an ADM bracket residual or an
anomaly.

## Fail-closed boundary

This ledger leaves null the \((a,p_a)\) cotangent sector, tracefree/shear
momenta, complete scalar/vector/tensor bases and Gaunt data, matter,
lapse/shift, full ADM constraints, HDA/Jacobi, BFV, RAQ, observables,
likelihoods, and physics or TOE claims.

The next real obstacle is an off-shell canonical treatment including lapse and
shift with nonzonal scalar and SVT couplings.  These restricted zonal vertices
do not remove that obstacle.

## Observed bounded result

The committed runner was executed only through the repository control plane:

```text
./ice run closed_s3_zonal_conformal_trace_kinetic_cubic_vertex_ledger
```

It produced a `VALID_RUN` with 42/42 exact checks and three source/scope
guards.  With the common external factor left symbolic, the aligned
\((\psi,\chi)=(Q_2,Q_2)\) packet has

\[
(K_0,K_1,K_2,K_3)
=\left(2\pi^2,0,-\frac12,\frac{3\sqrt2}{4\pi}\right),
\]

while the mixed \((Q_1+Q_2,Q_2)\) packet has

\[
(K_0,K_1,K_2,K_3)
=\left(2\pi^2,0,4,-\frac{3\sqrt2}{2\pi}\right).
\]

Both packets have nonzero exact quadratic and cubic tails beyond \(N=2\).
This supplies a restricted kinetic companion to the curvature packet, not a
combined ADM constraint or closure calculation.

Result SHA-256:
`8f962252978582635470ab404f06dec52c6fca7e9e40dbed6e42f8bdbc7a21d9`.
