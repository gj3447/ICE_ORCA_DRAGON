# Gate 1 — finite (m=2) bosonic canonical-source pushforward

## Outcome

For the retained homogeneous scale-factor and scalar momenta, no one common
(N-i0) or (N+i0) sign makes all four **unchanged real** momentum axes
absolutely convergent before the lapse integration:

\[
\boxed{
\text{COMMON SINGLE LATERAL ABSOLUTE REGULATOR}
=\text{KILLED IN THIS FINITE CONTROL}
}
\]

This is narrower than rejecting every all-real distributional source.  It does
not test an independently regulated oscillatory distribution, a gauge-fixed
reduction, or a deformation from the lapse-first distribution to complex
momentum thimbles.

The separately declared centered complex Gaussian rays do pass their finite
test.  Exact momentum elimination recovers the configuration action, the four
normalized high-precision quadratures reproduce the analytic prefactor, and
the lower and upper half-turn orientation ledgers agree:

\[
J_gJ_s
=\frac{\mu_g\mu_s}{\pi^2\hbar^2z^2}
=\frac{24\pi^2A^4}{\hbar^2z^2},
\qquad
g_{\rm momentum}=+1,
\qquad
g_{x,q}=-1.
\]

The resulting workbench verdict is
`CONFORMAL_PRESCRIPTION_AND_DETLINE_GLUE_REQUIRED`.  It keeps only a declared
finite Gaussian branch.  It does not derive the physical original cycle, a
BFV determinant line, a global intersection coefficient, or a physics claim.
Gate 1 therefore remains `OPEN_PARTIAL_PROGRESS`, and global promotion remains
`PROHIBITED`.

## 1. Frozen finite action and conventions

Take equal endpoints

\[
(a_0,\phi_0)=(a_2,\phi_2)=(a_b,\phi_b),
\qquad
a_1=a_b+x,
\qquad
\phi_1=\phi_b+q,
\]

with the shared midpoint

\[
A=a_b+\frac{x}{2}>0,
\qquad
\Phi=\phi_b+\frac{q}{2}.
\]

For (h=1/2), define

\[
\mu_g=12\pi^2A,
\qquad
\mu_s=2\pi^2A^3,
\qquad
U=2\pi^2[-3A+A^3V(\Phi)],
\]

\[
V(\Phi)=\frac34
\left(1-e^{-\sqrt{2/3}\,\Phi}\right)^2.
\]

The two-element Lorentzian canonical action is

\[
I_2=
x(p_{a0}-p_{a1})+q(p_{\phi0}-p_{\phi1})
+\frac{z}{4\mu_g}(p_{a0}^2+p_{a1}^2)
-\frac{z}{4\mu_s}(p_{\phi0}^2+p_{\phi1}^2)
-zU,
\]

where (z\ne0) is the complex lapse.  The pinned momentum orientation is

\[
dp_{a0}\wedge dp_{\phi0}\wedge dp_{a1}\wedge dp_{\phi1}.
\]

The displayed (J_g) and (J_s) below are scalar products of their respective
one-dimensional Gaussian factors.  The authoritative total is evaluated in
the pinned interleaved order; the differential-form measure is not silently
reordered into gravity-then-scalar groups.

## 2. Exact pushforward

The four algebraic stationary momenta are

\[
p_{a0}^*=-\frac{2\mu_gx}{z},
\quad
p_{a1}^*=+\frac{2\mu_gx}{z},
\quad
p_{\phi0}^*=+\frac{2\mu_sq}{z},
\quad
p_{\phi1}^*=-\frac{2\mu_sq}{z}.
\]

Substitution and direct square completion give

\[
I_2^*=-\frac{2\mu_gx^2}{z}
+\frac{2\mu_sq^2}{z}-zU.
\]

With (T=iz), the independently frozen Euclidean configuration action is

\[
I_{E,2}=-\frac{2\mu_gx^2}{T}
+\frac{2\mu_sq^2}{T}+TU,
\]

and SymPy verifies the identity

\[
iI_2^*=-I_{E,2}.
\]

This is a finite Legendre/Gaussian identity.  It says nothing yet about which
integration cycle is physically selected.

## 3. Why one common lateral sign fails

For a real momentum displacement, the real parts of the quadratic exponent
coefficients are

| Lapse boundary | (p_a^2) block | (p_\phi^2) block |
|---|---:|---:|
| (z=N-i\epsilon) | (+\epsilon/(4\mu_g\hbar)), growth | (-\epsilon/(4\mu_s\hbar)), damping |
| (z=N+i\epsilon) | (-\epsilon/(4\mu_g\hbar)), damping | (+\epsilon/(4\mu_s\hbar)), growth |

Thus changing the side only exchanges which real block diverges.  No single
lateral sign damps the unchanged real (p_a) and (p_\phi) axes together.

This is also the precise boundary of the Banihashemi--Jacobson citation.  Their
momentum-first convergence argument assumes a gauge fixing that eliminates the
negative full-theory trace-momentum Gaussian, illustrated by
(p=q_{ij}p^{ij}=0); under that assumption (N-i\epsilon) damps the remaining
positive momentum block.  The present finite minisuperspace control instead
retains a negative-kinetic (p_a) block.  It neither identifies (p_a)
literally with the full trace density nor derives a global maximal-slicing
gauge.

## 4. Declared complex Gaussian branch

Write (z=\rho e^{i\theta}), (\rho>0).  The declared centered rays are

\[
p_{a,e}-p_{a,e}^*
=e^{i(\pi/4-\theta/2)}y_{a,e},
\qquad
p_{\phi,e}-p_{\phi,e}^*
=e^{i(-\pi/4-\theta/2)}y_{\phi,e}.
\]

Both exponent remainders become strictly negative real Gaussians:

\[
\frac{i z}{4\mu_g\hbar}
(p_a-p_a^*)^2
=-\frac{\rho y_a^2}{4\mu_g\hbar},
\]

\[
-\frac{i z}{4\mu_s\hbar}
(p_\phi-p_\phi^*)^2
=-\frac{\rho y_\phi^2}{4\mu_s\hbar}.
\]

The two scale-factor and two scalar Gaussian factors give

\[
J_g=\frac{i\mu_g}{\pi\hbar z},
\qquad
J_s=\frac{\mu_s}{\pi i\hbar z},
\qquad
J_gJ_s=\frac{24\pi^2A^4}{\hbar^2z^2}.
\]

Holding the scale factor fixed recovers the earlier scalar ablation

\[
J_s=\frac{2\pi A^3}{\hbar T}.
\]

This agreement keeps the finite complex Gaussian pushforward as a declared
branch.  It does not prove a deformation from the lapse-first all-real
distribution.

## 5. Where the negative-arm sign enters

Transporting (\theta:0\to\pm\pi), each two-variable momentum pair contributes
(-1), so the two pairs multiply to

\[
g_{\rm momentum}=(-1)(-1)=+1.
\]

The configuration rays

\[
x=e^{i(\theta/2-\pi/4)}X,
\qquad
q=e^{i(\theta/2+\pi/4)}Q
\]

instead have combined endpoint Jacobian

\[
g_{x,q}=-1
\]

on both half-turns.  In the frozen-(A) flat Gaussian tangent control, the
combined cap glue is therefore (-1).

The flat-kernel control derives the same result without inserting it as an
assumption.  On (N>0), the ordered momentum Fresnel phases are

\[
(e^{+i\pi/4},e^{-i\pi/4},e^{+i\pi/4},e^{-i\pi/4}),
\]

and the (x,q) phases are

\[
(e^{-i\pi/4},e^{+i\pi/4}).
\]

On (N<0), every phase is conjugated.  Each complete real-arm phase product is
(+1), giving

\[
K_{\mathbb R}(N)=\frac{C}{|N|},
\qquad
C=\frac{\sqrt{\mu_g\mu_s}}{2\pi\hbar}.
\]

On the transported (x,q) rays, their Jacobian product gives instead

\[
K_{\rm hol}(z)=\frac{C}{z}.
\]

Consequently (K_{\rm hol}(-n)/K_{\mathbb R}(-n)=-1).  The missing negative-arm
sign is configuration/determinant-line glue, not an additional momentum
Gaussian Jacobian.

This last ledger freezes (A) while applying the standard regulated Fresnel
boundary phases.  It is not a proof that the simultaneous nonlinear
configuration contour is admissible: once (x) is complex,
(A=a_b+x/2) is complex as well, so momentum damping, avoidance of (A=0),
mixed ends, and regulator removal must be established together.  The
full nonlinear configuration glue therefore remains open.

## 6. High-precision normalization check

The numerical benchmark used

\[
a_b=3.5668031935672753,
\quad
\phi_b=1.0185809464006637,
\quad
x=0.03125,
\quad
q=-0.046875,
\quad
\hbar=1.
\]

At each of

\[
z\in\{0.6-0.15i,-0.6-0.15i,0.6+0.15i,-0.6+0.15i\},
\]

the executable evaluated four independent one-dimensional integrals of the
original linear-plus-quadratic momentum terms after centering on the declared
rays.  Their products agree with (J_gJ_s) at relative errors

\[
4.196\times10^{-71},
\quad
4.196\times10^{-71},
\quad
3.903\times10^{-71},
\quad
1.301\times10^{-71},
\]

against the frozen (10^{-45}) tolerance at 70 decimal digits.  This is a
normalization and implementation sanity check.  Because the parameterization
reduces the centered terms to standard Gaussians, it is not independent
evidence for source-to-thimble deformation or for a physical amplitude.

## 7. Computed facts, interpretation, and open work

### Computed in this control

- the exact finite (m=2) canonical action, stationary momenta, square
  completion, and Wick identity;
- the opposite convergence signs of the retained real (p_a) and (p_\phi)
  blocks for both lateral prescriptions;
- the exact declared steepest-ray prefactors;
- lower and upper formal momentum/configuration half-turn Jacobian ledgers;
- the frozen-(A) real (C/|N|) and transported (C/z) flat-tangent comparison;
- 17 exact checks, two analytic theorem guards, and four high-precision
  quadrature-product checks.

### Interpretation supported only inside this scope

- a single common lateral (i0) cannot provide absolute momentum-first
  convergence on the unchanged real (p_a,p_\phi) axes;
- the declared centered complex rays are algebraically and numerically
  consistent as a finite Gaussian branch;
- an additional conformal prescription and determinant-line/BFV orientation
  are required before relating that branch to a physical source.

### Still open

- alternative distributional all-real definitions or independent regulators;
- a gauge-fixed reduction of the negative (p_a) analogue and its FP/BFV
  measure;
- deformation of the lapse-first distribution to the declared complex rays;
- (a_1=0), (A=0), (a_1\to\infty), mixed scale--field ends, and nonlinear
  Starobinsky configuration admissibility;
- the zero-lapse full distribution, complete saddle/upward-cycle/sheet/end
  census, Stokes data, regulator and cutoff removal;
- the physical original cycle, full joint orientation, global
  (n_\sigma), physics claim, or TOE claim.

The most direct next discriminator is therefore a finite gauge-fixed/BFV
control that states exactly how the negative minisuperspace momentum is removed
and derives its FP and orientation factors.  Only after that should the
source-to-thimble relative-end deformation be attempted.

## 8. Provenance

Command:

```text
./ice run cpt_temporal_folded_susy/gate1_bosonic_canonical_source_pushforward
```

Observed terminal record:

```text
run_status=VALID_RUN
classification=GATE1_M2_UNCHANGED_REAL_PA_PPHI_SINGLE_I0_NOT_ABSOLUTELY_CONVERGENT_COMPLEX_GAUSSIAN_PUSHFORWARD_MATCHES
verdict=CONFORMAL_PRESCRIPTION_AND_DETLINE_GLUE_REQUIRED
programme_impact=NARROW
exact_checks_passed=17
theorem_guards_verified=2
numerical_checks_passed=4
quadratures=16
gate1=OPEN_PARTIAL_PROGRESS
global_n_sigma=null
physical_original_cycle=null
automatic_next=null
```

Observed runtime was 10.581 seconds under Python 3.13.5, SymPy 1.14.0, and
mpmath 1.3.0.  The run made zero root calls, zero ODE calls, and launched no
descendant.

Frozen hashes:

| Artifact | SHA-256 |
|---|---|
| input | `fc3f1061a053639665c87c0b9f6badddda49e6d63dc93d183c3aadfec89f9eaf` |
| runner | `fe557b1d86522bf1966513f32edb7555b8ddad770095d3c2412ab4571bbd1533` |
| raw result | `f7d64a09eeb4132e4975b056ee76eedfa32b75c7d29ca1a78bede5b052a66bc6` |
| canonical payload without self field | `4c6be750b82009eb987a087d6e51f35bb520c9cf8052b9835aa396d6253d4ba4` |

Two independent read-only audits checked the canonical/Wick signs, source
scope, Fresnel factors, half-turn orientation, numerical magnitudes, and result
digest.  Their first pass caused the source verdict to be narrowed and the flat
kernel check to be replaced by the explicit Fresnel derivation above.  The
corrected run then passed the second audit without a conclusion-changing issue.

## Primary-source boundaries

- [Banihashemi and Jacobson, *On the lapse contour*](https://doi.org/10.1103/PhysRevD.111.066014):
  momentum-first below-origin convergence under the paper's stated
  trace-momentum gauge assumption; not an unchanged real-(p_a) authorization
  or global slicing theorem.
- [Gibbons, Hawking, and Perry, *Path integrals and the indefiniteness of the gravitational action*](https://doi.org/10.1016/0550-3213(78)90161-X):
  conformal-factor obstruction framing only.
- [Witten, *Analytic Continuation Of Chern-Simons Theory*](https://arxiv.org/abs/1001.2933):
  relative-cycle and oriented-intersection framework only; it does not select
  this finite gravitational cycle.
