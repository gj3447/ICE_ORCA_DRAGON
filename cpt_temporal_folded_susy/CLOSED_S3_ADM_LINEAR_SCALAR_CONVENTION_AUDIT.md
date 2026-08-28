# Closed \(S^3\) ADM homogeneous and linear-scalar convention audit

## Scope

This bounded, unnumbered calculation fixes a classical convention packet before
any cubic constraint or HDA calculation.  It derives the homogeneous
closed-FRW plus massless-scalar constraint from the declared ADM action and
checks that it is exactly the repository's existing raw \(C\) convention.  It
also checks normalized zonal scalar harmonics and one declared canonical
longitudinal spatial-gauge coordinate.

It does **not** construct the full linear ADM constraints, a complete
scalar-vector-tensor basis, Gaunt coefficients, cubic constraints, projected
Poisson brackets, HDA/Jacobi closure, BFV charge, anomaly test, state or
likelihood.

## Convention fixed by the audit

For unit \(S^3\), \(\operatorname{Vol}(S^3)=2\pi^2\) and
\({}^{(3)}R[\gamma]=6\).  With

\[
q_{ab}=a^2\gamma_{ab},\qquad G=\frac1{8\pi},
\]

the declared action convention reduces to

\[
C_{\rm ADM}=-\frac{G p_a^2}{3\pi a}
-\frac{3\pi a}{4G}+\frac{p_\phi^2}{4\pi^2a^3}.
\]

The repository variables

\[
Q=2\log a,\qquad P=\frac{a p_a}{2}
\]

are canonical and give the exact raw constraint

\[
C=-\frac{e^{-3Q/2}P^2}{6\pi^2}
+\frac{e^{-3Q/2}p_\phi^2}{4\pi^2}
-6\pi^2e^{Q/2}.
\]

The linear spatial-gauge check is deliberately kinematic.  In the declared
scalar decomposition \(h_{ab}^{(S)}=2\psi\gamma_{ab}+2D_aD_bE\), a gradient
diffeomorphism \(\xi_a=D_aL\) acts as \(\delta_LE=L\).  The audit checks
that the canonical generator \(D_L^{\rm lin}=\sum_I L_I\Pi_{E,I}\) realizes
this statement on two labels.  It does not derive \(D_L^{\rm lin}\) from the
full ADM momentum constraint.

## Next boundary

The next independent calculation must introduce full scalar, vector and tensor
hyperspherical harmonics, their Gaunt/Clebsch--Gordan coefficients, and the
off-shell constraint expansion through cubic order before testing \(DD,DH,HH\)
or Jacobi identities.  Finite-cutoff remainders must remain distinct from an
algebra residual.
