# Unit (S^3=SU(2)) complex scalar Gaunt golden ledger

This is the smallest P2 coefficient packet that reaches beyond the existing
zonal Chebyshev product rule without pretending to be an ADM or HDA result.
It fixes one **complex** scalar harmonic convention:

\[
Q^{(n)}_{m_Lm_R}(g)=\sqrt{\frac{n+1}{2\pi^2}}
D^{n/2}_{m_Lm_R}(g),\qquad -\Delta Q^{(n)}=n(n+2)Q^{(n)}.
\]

The exact product coefficient is two SU(2) Clebsch--Gordan coefficients,
one for each magnetic label. The runner stores selected low-degree golden
products, proves associativity before projection in that fixed realization,
and reports the repeated-hard-projection associator together with the
discarded intermediate components.

The latter is deliberately named
`NONZERO_UNCLASSIFIED_PROJECTION_REMAINDER_NOT_CONSTRAINT_OR_QUANTUM_ANOMALY`.
It is not a (DD), (DH), or (HH) residual: no ADM constraint is formed.

## Intended controlled command

```text
./ice run closed_s3_su2_scalar_gaunt_golden_ledger
```

It accepts no arguments and writes only its adjacent result JSON. The new
runner is presently uncommitted, so it must first be reviewed, committed, and
accepted by `./ice list` before this command is authorized by the workbench.

## What this leaves open

Before a classical BFV seed can be a classical BFV **charge**, the programme
still needs a real-basis convention bridge; scalar/vector/TT and derivative
Gaunt data; gravity, lapse, shift, and matter constraints in one cubic ADM
convention; (DD,DH,HH); the Jacobiator; and cutoff scaling/analytic-tail
separation. Only then can a classical (Ω) be tested.

Before any quantum (\hat\Omega^2) conclusion it additionally needs a fixed
ordering, regulator removal, and common invariant operator core. This ledger
supplies none of those choices or conclusions.
