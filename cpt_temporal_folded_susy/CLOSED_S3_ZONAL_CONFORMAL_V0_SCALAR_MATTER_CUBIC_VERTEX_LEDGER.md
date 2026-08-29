# Restricted closed-S3 V=0 scalar-matter cubic vertex

This draft runner is an unnumbered, bounded exact calculation.  It adds one
scalar-matter Hamiltonian subvertex alongside the existing zonal conformal
curvature and trace-kinetic packets.  It does not combine those packets into
an ADM constraint.

## Declared restriction

On unit round \(S^3\), with \(\mathrm{Vol}=2\pi^2\), use normalized zonal
\(Q_n=U_n(\cos\chi)/\sqrt{2\pi^2}\),

\[
q_{ab}=a^2e^{2\epsilon\psi}\gamma_{ab},\qquad
\phi=\bar\phi+\epsilon\vartheta,\qquad
\pi_\phi=\sqrt\gamma(\bar\Pi+\epsilon\xi).
\]

The potential remains exactly \(V(\phi)=0\), matching the upstream ADM
audit.  The restricted canonical normalization is \(p_\phi=2\pi^2\bar\Pi\).
With the formal fixed-\(\epsilon\) ansatz and a zero-mean sector preserved
under variations,
\(\int\pi_\phi\delta\phi=2\pi^2\bar\Pi\delta\bar\phi+
\epsilon^2\int\sqrt\gamma\xi\delta\vartheta\); the latter integral is
the coefficient at order \(\epsilon^2\), not an unscaled canonical-pair claim.
The zero-mean condition also makes \(p_\phi=\int\pi_\phi=2\pi^2\bar\Pi\),
so the homogeneous term equals the already pinned
\(p_\phi^2/(4\pi^2a^3)\).

The local scalar Hamiltonian density is

\[
\frac{\mathcal H_{\perp,\phi}}{\sqrt\gamma}=
\frac1{2a^3}\left[e^{-3\epsilon\psi}(\bar\Pi+\epsilon\xi)^2+
a^4\epsilon^2e^{\epsilon\psi}|D\vartheta|^2\right]
=\frac1{2a^3}\sum_{r=0}^3\epsilon^r m_r+O(\epsilon^4),
\]

where

\[
\begin{aligned}
m_0&=\bar\Pi^2, &m_1&=2\bar\Pi\xi-3\bar\Pi^2\psi,\\
m_2&=\xi^2-6\bar\Pi\psi\xi+\tfrac92\bar\Pi^2\psi^2+a^4|D\vartheta|^2,\\
m_3&=-3\psi\xi^2+9\bar\Pi\psi^2\xi-\tfrac92\bar\Pi^2\psi^3+a^4\psi|D\vartheta|^2.
\end{aligned}
\]

The runner independently reconstructs these coefficients and uses
\(2|Df|^2=\Delta(f^2)-2f\Delta f\) for exact zonal gradient products.

For its one minimal packet, \(N=2\) and
\(\bar\Pi=1,\psi=\xi=\vartheta=Q_2\).  The quadratic tail is
\(-[1/2+4a^4]Q_4/\sqrt{2\pi^2}\), which cannot vanish for \(a>0\).
The cubic tail has an a-independent nonzero \(3Q_4/(2\pi^2)\) coefficient.
Both are exact hard-cutoff diagnostics only.

The displayed object is the scalar contribution to the normal constraint.
The matter momentum-constraint/shift vertex is omitted, not eliminated.
Excluded outputs also include a potential or mass extension, lapse/shift
elimination, full ADM constraints, constraint brackets/HDA/Jacobi, BFV, and
physical or TOE claims.  The runner accepts no arguments, pins all five
current upstream result payloads, uses the standard 120-second resource cap,
and writes its result only when explicitly run through `./ice run` after it is
registered.
