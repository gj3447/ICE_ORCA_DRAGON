# Fixed real-S3 scalar derivative/Gaunt identity ledger

This is a proposed bounded, unnumbered calculation.  Its runner is
`closed_s3_real_scalar_derivative_gaunt_ledger.py`, to be launched only after
commit through `./ice run closed_s3_real_scalar_derivative_gaunt_ledger`.

It reads the hash-pinned real `n<=2` scalar-basis result and only its selected
`R_n1_mL-1_mR-1_cos` square.  For two output scalar labels it records

\[
G_{abc}=\int_{S^3}R_aR_bR_c\,dV,\qquad
D_{abc}=\int_{S^3}R_a\nabla^iR_b\nabla_iR_c\,dV
=\frac{\lambda_b+\lambda_c-\lambda_a}{2}G_{abc},
\]

under the pinned convention `-Delta R_a=lambda_a R_a`,
`lambda_n=n(n+2)`, on a boundaryless unit round `S3`.  It separately checks
`D_bac+D_cab=lambda_a G_abc`.

The packet is deliberately only:

- `a=n0`, `b=c=n1`: `G=1/(sqrt(2)*pi)`, `D=3/(sqrt(2)*pi)`;
- `a=n2`, `b=c=n1`: `G=1/(sqrt(6)*pi)`, `D=-1/(sqrt(6)*pi)`.

The second sign is an algebraic consequence of the eigenvalue factor; it is
not a sign claim about a constraint residual.  No coordinate-gradient
realization, complete scalar derivative basis, vector/TT coupling, ADM
constraint, HDA/Jacobi calculation, BFV object, measure, or physical claim is
created by this ledger.

Lindblom--Taylor--Zhang (arXiv:1709.08020) is a convention generator/checker
for the unit-S3 scalar spectrum only.  The exact real-basis normalization and
Gaunt values are supplied by the pinned repository-local upstream result.
