# Unit \(S^3\) \(Q_2\) coupled \(DH\) strain cancellation

This selected zonal calculation combines the pinned \(n=2\) gravitational
momentum generator with scalar matter.  It tests only whether its metric
variation cancels the explicitly separated fixed-metric \(DH\) strain for
\(v=D_\gamma Q_2\), \(N=Q_1\), and \(\theta=\xi=Q_1+Q_2\), at cutoffs 2 and 3.

The shift convention deliberately has no \(a^{-2}\) factor.  It therefore
matches the pinned linear ADM generator

\[
D_g=\Pi_{E,2}-\frac83\Pi_{\zeta,2},\qquad
\delta\zeta_2=-\frac83,\quad\delta E_2=1,
\]

whose trace plus shear action gives
\(\delta q_{ab}=2a^2D_aD_bQ_2\).  For the selected matter packet, the two
metric derivatives and their canonical bracket are

\[
H_{\zeta_2}=\frac{a^4-3}{\pi^2a^3},\qquad
H_{E_2}=-\frac{40a}{3\pi^2},\qquad
\{D_g,H_\phi\}=\frac{8(2a^4-1)}{\pi^2a^3}.
\]

Direct metric variation independently gives

\[
R_{q\,\mathrm{fixed}}=-\frac{8(2a^4-1)}{\pi^2a^3},
\]

so the two terms cancel exactly.  The ambient combined bracket at both
cutoffs is

\[
\{D_g+D_\phi,H_\phi[Q_1]\}
=H_\phi[\mathcal L_{D Q_2}Q_1]
=\frac{10a^4+1}{\pi^2a^3}.
\]

At \(L=2\), the projection remainder is
\(5(2a^4+1)/(\pi^2a^3)\) and comes only from omitted channel \(k=3\).
At \(L=3\), that remainder is exactly zero.

It does not construct a gravitational Hamiltonian constraint, \(DD\) or
\(HH\) bracket, full HDA/Jacobi identity, BFV charge, anomaly result, or a
physical claim.

The first bounded run returned 6/9 and was not retained as evidence.  Its
failure was traced to an implementation omission: \(H_{E_2}\) used the
radial Hessian instead of the tracefree
\(S_{rr}=D_rD_rQ_2+(8/3)Q_2\).  The corrected clean runner computes the
canonical Poisson bracket explicitly, checks radial and tangential metric
components, and returned 13/13 exact checks.  This correction is a code-path
audit, not a physical effect.

```text
./ice run closed_s3_q2_coupled_dh_strain_cancellation
VALID_RUN; 13/13 exact checks
KEEP_Q2_COUPLED_DH_STRAIN_CANCELLATION_NOT_FULL_ADM_HDA
```
