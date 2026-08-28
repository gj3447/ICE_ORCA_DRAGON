# Closed \(S^3\) zonal scalar convolution and hard-cutoff ledger

## Scope

For the normalized zonal scalar functions

\[
Q_n(\chi)=\frac{U_n(\cos\chi)}{\sqrt{2\pi^2}},
\qquad
\int_{S^3}Q_nQ_m=\delta_{nm},
\]

this calculation records exact scalar convolution coefficients and the loss
created by a hard projection \(P_N\).  It is preparatory harmonic data for a
future full SVT/Gaunt and constraint expansion.  It does not construct the
cubic ADM constraint or test HDA, Jacobi or BFV nilpotency.

## Exact rule

\[
U_aU_b=\sum_{j=0}^{\min(a,b)}U_{a+b-2j},
\]

therefore

\[
Q_aQ_b=\frac1{\sqrt{2\pi^2}}
\sum_{j=0}^{\min(a,b)}Q_{a+b-2j}.
\]

The zonal triple Gaunt coefficient is consequently

\[
\int_{S^3}Q_aQ_bQ_c=
\begin{cases}
(2\pi^2)^{-1/2}, & c\in\{a+b,a+b-2,\ldots,|a-b|\},\\
0, & \text{otherwise}.
\end{cases}
\]

For each declared finite packet \(\phi=\sum_{n\le N}c_nQ_n\), the result
records

\[
\left\|(1-P_N)\phi^2\right\|^2,
\qquad
\int\phi^3,
\qquad
P_N(\phi^3)-P_N\!\left(\phi\,P_N(\phi^2)\right).
\]

The final quantity measures the local error introduced by applying the hard
cutoff between two nonlinear multiplications.  It is a scalar-zonal
convolution remainder, not an ADM bracket residual or anomaly.

There is an important exact null: if \(\phi\in P_N\), then

\[
\int\phi^3=\langle\phi,\phi^2\rangle
=\langle\phi,P_N\phi^2\rangle.
\]

So a retained-versus-full cubic *pairing* difference is exactly zero and is
recorded as such.  The actual hard-cutoff information is the discarded
quadratic vector \((1-P_N)\phi^2\), its norm, and the residual produced when a
projection is inserted between successive nonlinear convolutions.
