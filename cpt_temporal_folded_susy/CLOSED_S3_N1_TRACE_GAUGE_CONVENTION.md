# Unit \(S^3\) \(n=1\) trace-only scalar gauge convention

For \(Q_1=2\cos\chi/\sqrt{2\pi^2}\), \(\Delta Q_1=-3Q_1\) and
\(D_aD_bQ_1=-Q_1\gamma_{ab}\).  Hence the scalar-derived tracefree tensor
\(S_{ab}(Q_1)=D_aD_bQ_1+Q_1\gamma_{ab}\) vanishes: there is no independent
\((E_1,\Pi_{E,1})\) shear pair.

The bounded convention retains only an unreduced trace pair
\((\zeta_1,\Pi_{\zeta,1})\), with
\[
D_{L_1}^{(1)}=-L_1\Pi_{\zeta,1},\qquad \delta\zeta_1=-L_1.
\]
In the historical scalar-coordinate labels, \(\zeta_1=\psi_1-E_1\) is a
coordinate bridge only: \(E_1\) is not an independent canonical shear coordinate.
It checks that \(\delta q_{ab}=-2a^2L_1Q_1\gamma_{ab}\) equals
\(2a^2D_aD_b(L_1Q_1)\).  This refines the earlier n=2,3 scalar-derived
packet; it is neither a full gauge reduction nor an ADM/HDA/Jacobi result.

Run after the source commit only:

```text
./ice run closed_s3_n1_trace_gauge_convention
```
