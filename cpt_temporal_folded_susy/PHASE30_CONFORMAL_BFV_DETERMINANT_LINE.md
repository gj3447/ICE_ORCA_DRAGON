# Phase 30 — coupled conformal field–lapse contour and determinant-line gate

## Outcome

The frozen connected Starobinsky interval admits a **finite-cutoff, local,
convergent, coupled** homogeneous Gaussian tangent cycle.  It is not the direct product of an
independent conformal rotation and an independent lapse rotation.  The lapse
fluctuation moves the field contour:

\[
\boxed{
\delta T=iu,
\qquad
\eta=R\xi-iu\,\mathcal O_D^{-1}j .
}
\]

On this fibered contour the mixed term vanishes and

\[
I_E^{(2)}
=\frac12\xi^TR^T\mathcal O_D R\xi
+\frac12(-W_{TT})u^2,
\qquad
-W_{TT}=8.9231430383>0.
\]

Every tested cutoff gives a positive real quadratic form.  In contrast, the
tested standard direct-product rotation leaves exactly one negative direction.

The determinant calculation also separates two notions that had been mixed.
A naked lattice Hessian magnitude ratio grows rapidly over the recorded
refinements.  Including the declared midpoint configuration measure gives a
stable relative endpoint **magnitude**,

\[
\boxed{
\left(\frac{\det B_v}{T_*^2}\right)^{-1/2}
=1.01502655703 .
}
\]

This is a declared-measure-normalized Jacobi/Van Vleck magnitude, not an
absolute zeta determinant of the gravitational fluctuation operator.  Odd
and even cutoffs have opposite absolute field-determinant signs.  The chosen
constant-principal reference cancels that finite-lattice sign in the relative
determinant ratio, but it does not derive a continuum determinant-line phase.

The remaining global obstruction is now sharper.  On the real lapse axis the
identity-normalized signature-$(-,+)$ kernel requires $1/|N|$.  A single
holomorphic sheet supplies $1/N$, which has the wrong sign on the negative
real axis.  A determinant-line/Maslov orientation must jump at $N=0$.
The closure of the positive imaginary lapse ray can touch the putative
continued real dual at the singular endpoint $N=0$.  This is not a recorded
transverse intersection, and no complete upward cycle has been constructed.
Consequently

\[
\boxed{
\text{the finite-cutoff coupled Gaussian tangent cycle exists, but the physical integer }
n_\sigma\text{ is not fixed.}
}
\]

No new BFV ghost complex is evaluated in this phase.  The reduced
proper-time BFV result from Phase 28 is inherited only as context; a full
phase-space BFV super-Hessian and its determinant line remain the next gate.

## 1. Frozen homogeneous action

The boundary, potential, and saddle are inherited unchanged from Phases
24--29:

\[
q_0=(3.56680319357,1.01858094640,
     3.56680319357,1.01858094640),
\]

\[
V(\phi)=\frac34
\left(1-e^{-\sqrt{2/3}\phi}\right)^2,
\qquad
T_*=0.7,
\]

\[
W_*=1.40669054283434,
\qquad
W_T=0,
\qquad
W_{TT}=-8.92314303834.
\]

On the unit parameter interval $s\in[0,1]$ the configuration action is

\[
I_E=2\pi^2\int_0^1ds
\left[
\frac1{2T}G_{AB}(q)\dot q^A\dot q^B+TU(q)
\right],
\]

\[
G=\operatorname{diag}(-6a,a^3),
\qquad
U=-3a+a^3V(\phi).
\]

For Dirichlet field fluctuations and $T=T_*+\nu$, write the quadratic form
as

\[
I_E^{(2)}
=\frac12\langle\eta,\mathcal O_D\eta\rangle
+\nu\langle j,\eta\rangle
+\frac12A\nu^2.
\]

Completing the square gives

\[
I_E^{(2)}
=\frac12\left\langle
\eta+\mathcal O_D^{-1}j\,\nu,
\mathcal O_D
(\eta+\mathcal O_D^{-1}j\,\nu)
\right\rangle
+\frac12
\left(A-j^T\mathcal O_D^{-1}j\right)\nu^2,
\]

with

\[
\boxed{
W_{TT}=A-j^T\mathcal O_D^{-1}j .
}
\]

The executable verifies this Schur identity exactly and reproduces its value
from independent midpoint discretizations.

## 2. Principal conformal cycle and the Maslov line

Freeze the principal kinetic form as

\[
M=\operatorname{diag}(-\mu_g,+\mu_s),
\qquad \mu_g,\mu_s>0,
\]

and write $N=\rho e^{i\theta}$.  The coupled configuration rays

\[
\delta a
=e^{i(\theta/2-\pi/4)}y_g,
\qquad
\delta\phi
=e^{i(\theta/2+\pi/4)}y_s,
\qquad y_g,y_s\in\mathbb R,
\]

give

\[
\frac{i}{2N}\delta q^TM\delta q
=-\frac{\mu_gy_g^2+\mu_sy_s^2}{2\rho}.
\]

Their Jacobian is $e^{i\theta}$, so the local holomorphic prefactor

\[
\frac{\sqrt{\mu_g\mu_s}}{2\pi N}
\]

normalizes the rotated Gaussian to one.  At the Euclidean saddle
$N_*=-iT_*$,

\[
\delta a\in-i\mathbb R,
\qquad
\delta\phi\in\mathbb R.
\]

This is the finite homogeneous version of the conformal rotation.  The
negative gravitational principal direction cannot be treated by rotating
the lapse alone; the field and lapse cycles must be specified together.  The
general conformal-factor obstruction is the one isolated by
[Gibbons--Hawking--Perry](https://doi.org/10.1016/0550-3213(78)90161-X).

For real nonzero lapse, however, the original real field cycle has

\[
K_N^{(0)}(\Delta q)
=\frac{\sqrt{\mu_g\mu_s}}{2\pi\hbar|N|}
\exp\left[
\frac{i}{2\hbar N}
(-\mu_g\Delta a^2+\mu_s\Delta\phi^2)
\right].
\]

The one-dimensional gravity and scalar Fresnel phases cancel separately on
both sides, so $K_N\to+\delta^{(2)}$ as $N\to0^+$ and $N\to0^-$.  A single
holomorphic $1/N$ sheet instead gives $-\delta^{(2)}$ on the negative side.
Thus the full real unitary group needs a Maslov/determinant-line gluing at the
origin.  It cannot be represented by a single scalar holomorphic lapse
integrand without that extra data.

## 3. Why the product contour fails

The midpoint discretization keeps both homogeneous field histories and the
global lapse modulus.  At every tested cutoff, the standard prescription that
rotates the negative spectral field directions and the lapse direction
independently leaves one negative eigenvalue in the real part of the joint
Hessian:

| segments | direct-product minimum eigenvalue | negative count |
|---:|---:|---:|
| 10 | $-10.3366$ | 1 |
| 20 | $-10.2859$ | 1 |
| 40 | $-10.0756$ | 1 |
| 80 | $-9.6857$ | 1 |
| 160 | $-9.0710$ | 1 |

The failure is caused by the $q$--$T$ mixing $j$.  Let $R$ rotate the negative
spectral subspace of $\mathcal O_D$ to the imaginary axis and leave the
positive subspace real.  The fibered transformation

\[
\nu=iu,
\qquad
\eta=R\xi-iu\,\mathcal O_D^{-1}j
\]

gives a vanishing mixed block to numerical precision and the following
Schur sequence:

\[
-8.8201408,
-8.8973668,
-8.9166974,
-8.9215315,
-8.9227402,
-8.9230423
\longrightarrow -8.9231430.
\]

The smallest real eigenvalue on the fibered contour is positive at every
tested cutoff.  This establishes a local Gaussian cycle.  It does not prove
that the nonlinear contour reaches admissible asymptotic sectors or belongs
to the original Lorentzian relative-homology class.

## 4. Canonical measure versus a naked determinant

The canonical endpoint blocks at the saddle are

\[
\det B_p=-1.25693827119\times10^{-6},
\]

\[
W_{q_-q_+}=-B_p^{-1},
\qquad
\det W_{q_-q_+}=-795584.017861.
\]

The Jacobi inverse agrees with an independently differentiated fixed-$T$
boundary Hessian at relative operator residual $4.01\times10^{-12}$; it is
not verified merely by multiplying a matrix by its constructed inverse.

The fixed-$T$ branch was sampled at 18 points between $T=0.02$ and $0.7$.
$\det B_v$ and its smallest singular value stay positive at every recorded
point.  This is a bounded numerical no-caustic scan, not an interval proof.

A midpoint lattice comparison against a constant endpoint principal symbol
shows why a naked determinant is not meaningful here.  The kinetic metric
$G(a)$ changes along the saddle.  The raw determinant magnitude ratio grows as

\[
1.10686, 1.25824, 1.62848, 2.73004, 7.67565, 60.6870
\]

for 10, 20, 40, 80, 160, and 320 segments.

The declared midpoint configuration measure contains

\[
\prod_e
\sqrt{
\frac{|\det M(a_e)|}{|\det M(a_-)|}
},
\]

where $a_e$ is evaluated at the exact continuum midpoint of each slice.
This freezes one explicit hybrid midpoint calibration: the element action
uses arithmetic node midpoints, while the declared measure samples the
continuum saddle at exact slice midpoints.  It is a reproducible convergence
test, not a uniqueness theorem for all orderings or time-slicings.

The even-cutoff table alone hides an additional fact.  At 9, 10, 11, 19, 20,
and 21 segments, the field-Hessian negative-mode count is exactly
\(N_{\rm seg}-1\), so the bare absolute lattice determinant sign alternates
\(+,-,+,+,-,+\).  The constant-principal reference has the same
finite-lattice orientation, making the displayed relative sign positive.
This does not determine a continuum Maslov/determinant-line phase.

After including the declared measure, the relative magnitudes are

\[
1.0142811, 1.0146458, 1.0148341,
1.0149298, 1.0149781, 1.0150023,
\]

converging to

\[
\boxed{
\left(\frac{\det B_v}{T_*^2}\right)^{-1/2}
=0.970610956760^{-1/2}
=1.015026557031.
}
\]

Boundary/Jacobi data can encode determinant information only after the
operator, boundary domain, and measure are fixed; this is the relevant scope
of [Forman's boundary-value determinant
analysis](https://doi.org/10.1007/BF01391828).  The present number must not be
called an absolute gravitational zeta determinant.

## 5. Conditional local magnitude

In the frozen flat endpoint normalization and with $\hbar=1$,

\[
\frac{\sqrt{|\det W_{q_-q_+}|}}{2\pi}
=141.959073659,
\]

and the lapse Gaussian has magnitude

\[
\sqrt{\frac{2\pi}{|W_{TT}|}}
=0.8391333983.
\]

Therefore

\[
A_{\rm loc}^{\rm magnitude}
=119.122599903,
\]

and including $e^{-W_*}$ gives

\[
\boxed{
e^{-W_*}A_{\rm loc}^{\rm magnitude}
=29.1793909650.
}
\]

This is deliberately **not** reported as a physical tunneling probability or
full one-loop amplitude.  Its sign and phase depend on the conformal and lapse
orientations, and it still multiplies the unknown global intersection number
$n_\sigma$, endpoint density, and BFV normalization.  The Dirichlet ghost
determinant $2$ is convention dependent and is not an additional physical
factor of two.  Careful homogeneous negative-mode reduction in gravity is
also known to depend on the phase-space variable and constraint treatment;
see [Gratton--Turok](https://doi.org/10.1103/PhysRevD.63.123514).

## 6. The unresolved endpoint

Two shifted rays can be used to display the missing endpoint datum:

\[
\mathcal C_+(\delta):
T=+\delta+iy,
\qquad y\in[0,\infty),
\]

\[
\mathcal C_-(\delta):
T=-\delta+iy,
\qquad y\in[0,\infty).
\]

For every fixed $y>0$, both tend pointwise to the same positive imaginary ray
as $\delta\to0^+$.  This fact alone does **not** compute an intersection
number: a half-ray's contact at $y=0$ is an endpoint, not a transverse
interior crossing.  The regulated cycle must specify how it bypasses the
identity-kernel singularity, and the complete upward cycle must be followed
before an integer can be assigned.  Thus the present calculation leaves
$n_\sigma$ open rather than assigning either zero or one.

The full real lapse range is a different object.  It gives the rigging
distribution only after the two real Maslov branches are glued.  Phase 28's
bounded $+1$ crossing does not provide the missing determinant-line gluing,
the global ends of the cycle, or all other saddle intersections.  Relative
Picard--Lefschetz coefficients require a complete middle-dimensional cycle
and a non-Stokes chamber, as emphasized in
[Witten's relative-cycle formulation](https://arxiv.org/abs/1001.2933) and
the minisuperspace contour analyses of
[Halliwell--Louko](https://doi.org/10.1103/PhysRevD.42.3997).

## 7. Verdict

| Question | Result |
|---|---|
| Does a local coupled conformal/lapse Gaussian cycle exist? | **Yes, in the frozen homogeneous quadratic control.** |
| Does the tested standard direct-product Wick rotation work? | **No, at the tested finite cutoffs.** |
| Does the declared-measure relative magnitude have a stable recorded limit? | **Yes, numerically.** |
| Does the bare absolute lattice determinant sign have a cutoff-independent limit? | **No; it alternates with cutoff parity.** |
| Is the properly regularized continuum Maslov/determinant-line phase known? | **No.** |
| Is a naked bulk Hessian determinant adequate? | **No.** |
| Is the conditional local magnitude finite? | **Yes: $29.1793909650$ at $\hbar=1$.** |
| Is that a physical probability or complete one-loop determinant? | **No.** |
| Does a single holomorphic $N$ sheet normalize both real sides? | **No.** |
| Does the positive half-ray fix $n_\sigma$? | **Not yet; its endpoint bypass and global dual cycle are unspecified.** |
| Is the full connected-saddle PL coefficient known? | **No.** |

The calculation strengthens the local connected-saddle construction while
providing counterexamples to two shortcuts: independent Wick rotations and
an unqualified naked determinant.  It identifies where the remaining PL ambiguity resides
at the determinant-line gluing, endpoint bypass, and global relative cycle;
it does not compute that ambiguity's integer value.

## Scope

Included:

- the frozen homogeneous $(a,\phi,T)$ quadratic action;
- the lapse-dependent principal conformal rays;
- midpoint field--lapse Hessians through 320 time slices;
- direct-product and fibered-contour eigenvalue tests;
- a declared midpoint configuration-measure convergence test;
- the endpoint Jacobi/Van Vleck datum and a conditional local magnitude;
- the common pointwise open limit of two shifted endpoint rays.

Excluded:

- an absolute zeta determinant and its global determinant-line phase;
- inhomogeneous metric, scalar, vector, tensor, fermion, gravitino, and ghost
  modes;
- all nonlinear coupled thimbles and all complex saddle sheets;
- an admissible global relative-homology cycle at infinity;
- a physical half-lapse endpoint bypass selected by the theory;
- the BFV ghost/gauge complex and its boundary normalization;
- a WDW trace, positive density, Pin lift, SUSY spectrum, or initial-value
  distribution.

## Primary references

- G. W. Gibbons, S. W. Hawking, and M. J. Perry, “Path integrals and the
  indefiniteness of the gravitational action,”
  [DOI:10.1016/0550-3213(78)90161-X](https://doi.org/10.1016/0550-3213(78)90161-X).
- J. J. Halliwell and J. Louko, “Steepest-descent contours in the path-integral
  approach to quantum cosmology. III,”
  [DOI:10.1103/PhysRevD.42.3997](https://doi.org/10.1103/PhysRevD.42.3997).
- R. Forman, “Functional determinants and geometry,”
  [DOI:10.1007/BF01391828](https://doi.org/10.1007/BF01391828).
- S. Gratton and N. Turok, “Homogeneous modes of cosmological instantons,”
  [DOI:10.1103/PhysRevD.63.123514](https://doi.org/10.1103/PhysRevD.63.123514).
- J. A. Garcia, J. D. Vergara, and L. F. Urrutia, “BRST--BFV quantization and
  the Schwinger action principle,”
  [arXiv:hep-th/9511092](https://arxiv.org/abs/hep-th/9511092).
- E. Witten, “Analytic continuation of Chern--Simons theory,”
  [arXiv:1001.2933](https://arxiv.org/abs/1001.2933).

## Reproduction

```bash
uv run --locked python3 \
  cpt_temporal_folded_susy/phase30_conformal_bfv_determinant_line.py
```

The executable emits ten exact checks, ten numerical checks, and one
`PHASE30_RESULT=` payload.  It writes no files.
