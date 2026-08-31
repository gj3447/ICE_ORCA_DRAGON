# Finite real scalar-harmonic basis ledger on unit \(S^3\)

This independent work unit translates the pinned complex Wigner--D scalar
realization into an explicit real scalar basis through degree \(n=2\).  It
uses the fixed conjugation rule

\[
\overline{Q^{(n)}_{m_Lm_R}}=(-1)^{(m_L-m_R)/2}Q^{(n)}_{-m_L,-m_R}
\]

for doubled magnetic labels.  For each nonself conjugate pair, the ledger
uses its real cosine and sine combinations; a self-conjugate \(Q_{00}\) is
retained unchanged.  The calculation checks the finite unitary transform,
reality and orthonormality, then converts one exact low-mode product.

The selected product is

\[
R_{1,-1,-1}^{\cos}R_{1,-1,-1}^{\cos}
=\frac{R_{0,0,0}}{\sqrt2\pi}
+\frac{R_{2,-2,-2}^{\cos}}{\sqrt3\pi}
+\frac{R_{2,0,0}}{\sqrt6\pi}.
\]

The runner also records what a hard \(L=1\) projection drops from that full
product.  This is a finite scalar projection remainder, never a constraint
residual or quantum anomaly.

No execution has been recorded in this document yet.  In particular, this
does not supply complete scalar/vector/TT harmonics, derivative Gaunt data,
ADM constraints, HDA/Jacobi closure, a BFV charge, a quantum common core, or
a physics claim.  The controlled command is:

```text
./ice run closed_s3_real_scalar_harmonic_basis_ledger
```
