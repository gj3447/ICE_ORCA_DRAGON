# Phase 16 — BGG single-source parent and off-shell FLRW tangency

## Outcome

The direct calculation has a split result.

1. **Bosonic kinetic parent: PASS.**  One BGG source gives the Lorentzian Einstein/scalar
   sign, rank-three \((X,T,Y)\) Hessian, and target kinetic Hamiltonian without
   combining conventions from another paper. Algebraic auxiliary constraints
   and the lapse primary constraint are not part of this three-velocity block.
2. **Specified strict off-shell FLRW/gamma-trace truncation: FAIL.**  The same BGG local-SUSY
   transformations excite both the discarded spatial auxiliary vector and a
   gamma-traceless spatial gravitino mode at an exact point of the proposed
   FLRW locus.

This closes the Phase 15R same-source *bosonic* gap, but it does not construct
Temporal-Folded SUSY.  Instead it rules out the smallest off-shell FLRW
fermionic truncation with arbitrary homogeneous chiralino and auxiliary
fields.

Primary source: P. Binétruy, G. Girardi and R. Grimm, “Supergravity couplings:
a geometric formulation,” [hep-th/0005225v1](https://arxiv.org/abs/hep-th/0005225v1).
The exact archive and formula locators are recorded in
[`PHASE16_BGG_SOURCE_NOTES.md`](PHASE16_BGG_SOURCE_NOTES.md).

Executable:

```bash
uv run --with sympy python3 cpt_temporal_folded_susy/phase16_bgg_single_source.py
```

The run returned exit 0 with 20 exact checks.

## 1. Source-native curvature

Use

\[
e^0=N(t)dt,\qquad e^i=a(t)dx^i,\qquad
Q=\frac{\ddot a}{aN^2}+\frac{\dot a^2}{a^2N^2}
-\frac{\dot a\dot N}{aN^3}.
\]

Solving BGG CPN.13 together with
\(\omega_{mab}=-\omega_{mba}\) gives the only independent nonzero
lower-pair components

\[
\omega_{i0i}=\frac{\dot a}{N}\qquad(i=1,2,3).
\tag{E177}
\]

The curvature is then built from BGG's reverse-order two-form convention,
not assigned from a metric formula.  In storage
\(R[n,m,b_{\rm lower},a_{\rm upper}]\), the literal CPN.26 contraction
\(e_a{}^ne_b{}^m(R_{nm})^{ab}\) raises the first stored Lorentz index and
returns

\[
\boxed{\mathcal R_{\rm BGG}=-6Q.}
\tag{E178}
\]

Reading the printed `ab` as the transposed storage order `ba` instead gives
\(+6Q\).  The executable evaluates and rejects that opposite-sign mutation
exactly.

## 2. Action, Hessian, and Hamiltonian

BGG CPN.130 and CPN.59 at \(W\equiv0\), one flat neutral chiral field, and
vanishing fermions give

\[
e^{-1}\mathcal L=-\frac12\mathcal R
-g^{mn}\partial_mA\partial_n\bar A
-\frac13M\bar M+\frac13b^ab_a+F\bar F.
\]

The auxiliary fields are algebraic and are not needed to compute the velocity
subblock.  With

\[
S_{\rm phys}=M_P^2S_{\rm BGG},\qquad
\Phi=M_PA=\frac{T+iY}{\sqrt2},\qquad
X=\sqrt6M_P\ln a,
\]

define

\[
B=\frac{3M_P^2V_0a^2\dot a}{N},\qquad
C=\frac{M_P^2V_0a\dot a^2}{N}.
\]

The raw second-order Einstein term satisfies the exact arbitrary-lapse
identity

\[
L_{\rm EH,raw}=\dot B-3C.
\tag{E179}
\]

Removing this one endpoint gives

\[
\boxed{
L_{\rm 1st}=\frac{V_0a^3}{2N}
\left(-\dot X^2+\dot T^2+\dot Y^2\right).
}
\tag{E180}
\]

For \(f=V_0a^3/N>0\),

\[
G_{\dot q\dot q}=f\,\mathrm{diag}(-1,1,1),\qquad
\operatorname{rank}G=3,\qquad
\det G=-f^3,
\]

so its inertia in the order (negative, zero, positive) is \((1,0,2)\).
The Legendre transform gives

\[
\boxed{
H_{\rm kin}=\frac{N}{2V_0a^3}
\left(-p_X^2+p_T^2+p_Y^2\right).
}
\tag{E181}
\]

Thus BGG passes the Phase 15R bosonic parent test in one convention-complete
source.

## 3. First exact tangency obstruction: \(b_i\)

Consider the following exact point of the proposed homogeneous FLRW locus:

\[
N=a=1,\quad \dot e=0,\quad
b_a=M=\bar M=0,\quad A,\bar A=\text{constant},\quad
\psi_m=\bar\psi_m=0,
\]

while the off-shell retained fields \(F,\bar F,\chi,\bar\chi\) and the
homogeneous SUSY parameters remain arbitrary.  BGG CPN.85 reduces to

\[
\delta b_i=\frac1{\sqrt2}
\left[F(\epsilon\sigma_i\bar\chi)
+\bar F(\bar\epsilon\bar\sigma_i\chi)\right].
\tag{E182}
\]

With BGG's \(\sigma^3=\mathrm{diag}(1,-1)\), the independent Grassmann
monomial \(F\epsilon^1\bar\chi^{\dot1}\) has coefficient

\[
[\delta b_3]_{F\epsilon^1\bar\chi^{\dot1}}
=\frac1{\sqrt2}\ne0.
\]

Here \(b_a\) is BGG's source Lorentz vector, whereas the discarded spatial
normal \(b_i=e_i{}^ab_a\) is part of the analyst-defined FLRW truncation.
Because \(b_a=0\) at the witness point, the tetrad term in
\(\delta(e_i{}^ab_a)\) vanishes.  Homogeneous diffeomorphism and common local
Lorentz transformations also act trivially on this zero field, so they cannot
cancel the monomial.  This statement uses the source auxiliary \(b_a\)
defined by BGG CPN.7; it does not silently replace it by the later shifted
diagonal auxiliary.

## 4. Independent tangency obstruction: spatial spin \(3/2\)

At the same point BGG CPN.40 gives the composite Kähler connection

\[
A_i=\frac{i}{4}(\chi\sigma_i\bar\chi),
\]

and CPN.75, using the parameter derivative defined in CPN.77, therefore gives

\[
\delta\psi_i=\frac{i}{2}
(\chi\sigma_i\bar\chi)\epsilon.
\tag{E183}
\]

For the identity spatial frame take \(\Gamma_i=-\sigma_i\) and

\[
(P_{3/2})_i{}^j=\delta_i{}^j
-\frac13\Gamma^j\Gamma_i.
\]

The projector is an analyst-defined covariant decomposition, not a formula
claimed to be printed by BGG. The executable proves \(P_{3/2}^2=P_{3/2}\),
\(\operatorname{rank}_{\mathbb C}P_{3/2}=4\), and that it annihilates the
retained gamma-trace ansatz \(\psi_i=\lambda\Gamma_i\).  For the coefficient
of \(\chi^1\bar\chi^{\dot1}\epsilon^1\),
\((\chi\sigma_i\bar\chi)=(0,0,1)\), but

\[
\delta\rho_i=\delta\psi_j(P_{3/2})_i{}^j
=\left(
(0,-i/6),\ (0,-1/6),\ (i/3,0)
\right)\ne0.
\tag{E184}
\]

The displayed calculation extracts a coefficient in the complexified free
Grassmann algebra; the conjugate BGG transformation supplies the barred
counterpart. Its gamma trace is exactly zero, so this is a genuine discarded spin-3/2
mode, not a different parametrization of \(\lambda\).  At \(\psi_i=0\), the
\(\psi\,\delta P_{3/2}\) term and homogeneous diffeomorphism/Lorentz
compensator actions vanish.

## 5. Interpretation

A submanifold is invariant only if every discarded-mode variation vanishes
at every point.  Either E182 or E184 is therefore sufficient to disprove
tangency of the proposed **off-shell** FLRW truncation.  A full all-fermion
residual is unnecessary for that negative conclusion. The executable is an
exact clean-point counterexample, not a transcription engine for every term
in CPN.40/75/77/85.

This result does **not** disprove:

- full four-dimensional \(N=1\) supergravity;
- homogeneous Bianchi I with all \(b_i\) and spin-3/2 modes retained;
- a smaller on-shell or Killing-spinor slice with \(F=\chi=0\);
- a separately derived truncation using the shifted diagonal auxiliary;
- or a Temporal-Folded branch supercharge.

It does show that the simple route “canonical chiral clock + arbitrary
chiralino + algebraic auxiliaries, but only isotropic/gamma-trace gravity
modes” is not a consistent off-shell local-SUSY reduction.  The next honest
route is either to retain the complete homogeneous vector and spin-3/2 sector
through the Bianchi-I canonical reduction, or explicitly move to an
on-shell/SUSY-breaking gauge-fixed model and relinquish the off-shell FLRW
claim.

There is also a complementary background result.  On the bosonic \(W=0\)
auxiliary equation \(F=0\), CPN.93 gives for a homogeneous real rolling
clock, with \(D_\tau A=N^{-1}dA/dt\),

\[
\delta\chi_\alpha
=i\sqrt2\,D_\tau A\,
(\bar\epsilon\bar\sigma^0\varepsilon)_\alpha.
\tag{E185}
\]

The two-component parameter map has determinant
\(-2(D_\tau A)^2\ne0\).  Hence a nonzero clock rate leaves no nonzero SUSY
parameter that preserves this bosonic background; Lorentzian reality relates
the barred and unbarred parameters, and the conjugate CPN.99 gives the same
conclusion.  This is a statement that
the rolling solution has no residual Killing supersymmetry; it is not a
statement that the underlying local gauge symmetry or the full BGG theory is
absent.
