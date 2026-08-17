# Phase 26 — global complex-lapse flow and fold uniformization

## Outcome

For the frozen connected Starobinsky interval of Phases 24–25, the local
imaginary lapse direction is not merely a formal quadratic contour.  It
continues to a long, genuine constant-phase solution branch of the complex
boundary-value problem:

\[
\operatorname{Im}W\simeq0,
\qquad
\frac{d\operatorname{Re}W}{ds}=|W_T|^2>0.
\]

The recorded upper arm starts at

\[
T_*=0.7,
\qquad
W_*=1.406690542834,
\qquad
W_{TT}=-8.9231430383,
\]

turns in its projection to the complex $T$ plane, and reaches

\[
T=4.340610405+0.6i,
\qquad
\operatorname{Re}W=4.6740\times10^4
\]

before the deliberately imposed shooting-data cutoff.  Its lower arm is the
complex conjugate.  This establishes a long convergent thimble segment on one
specified analytic sheet.  It does **not** prove the exact endpoint of the
thimble.

The real fixed-$T$ fold at

\[
T_c=9.7886255681
\]

is a different phenomenon.  There

\[
W_T(T_c)=-73.72585\ne0,
\]

so it is not a new lapse saddle.  It is a projection caustic of the
fixed-$T$ field saddles, and the two real sheets obey the expected Airy fold
scaling.

Finally, the Lorentzian contour coefficient remains open.  Phase 27 shows
that positive Lorentzian lapse maps to the upper-imaginary Euclidean-$T$ ray.
In the sampled local domain, its only candidate contact with the recorded
real branch is the singular zero-duration endpoint, not a transverse interior
intersection.  No global dual cycle has been computed.  Consequently no
integer Picard–Lefschetz coefficient, WDW state, or initial value is inferred
here.

## 1. Frozen model and flow convention

The potential, boundary variables, and endpoints are unchanged:

\[
V(\phi)=\frac34\left(1-e^{-\sqrt{2/3}\,\phi}\right)^2,
\]

\[
q=(a_-,\phi_-,a_+,\phi_+),
\]

\[
q_0=(3.56680319357,1.01858094640,
     3.56680319357,1.01858094640).
\]

At fixed complex proper length $T$, $W(q,T)$ is the on-shell value of

\[
I_E=2\pi^2\int_0^T d\tau\left[
-3a(a'^2+1)+a^3\left(\frac12\phi'^2+V\right)
\right],
\]

using the full off-constraint Euler–Lagrange equations

\[
a''=\frac{1-a'^2}{2a}-\frac a4\phi'^2-\frac a2V,
\qquad
\phi''+3\frac{a'}a\phi'=V_{,\phi}.
\]

For the semiclassical integrand $e^{-W/\hbar}$, the convergent
Picard–Lefschetz flow is

\[
\boxed{
\frac{dT}{ds}=\overline{W_T}
}
\]

and therefore

\[
\frac{dW}{ds}=|W_T|^2,
\qquad
\frac{d\operatorname{Re}W}{ds}=|W_T|^2,
\qquad
\frac{d\operatorname{Im}W}{ds}=0.
\]

Since $W_{TT}(T_*)<0$, the local convergent tangent is imaginary and the
dual/upward tangent is real.  This sign is tied to $e^{-W}$; reversing the
exponent reverses the flow naming.

## 2. Recorded upper arm

The complex BVP is solved with real endpoint data while imposing
$\operatorname{Im}W=0$.  Representative points are:

| $\operatorname{Im}T$ | $\operatorname{Re}T$ | $\operatorname{Re}W$ |
|---:|---:|---:|
| 0.000 | 0.700000 | 1.406691 |
| 0.400 | 0.744066 | 2.154359 |
| 1.000 | 0.961582 | 7.107114 |
| 1.500 | 1.276257 | 17.652273 |
| 2.000 | 1.774260 | 42.174690 |
| 2.400 | 2.554232 | 112.846797 |
| 2.4748 | 3.050000 | 209.21 |
| 0.988 | 4.370000 | 12229.77 |
| 0.600 | 4.340610 | 46740.36 |

Along the frozen table:

- the endpoint BVP residual stays below $8\times10^{-8}$;
- the constant-phase residual stays below $8\times10^{-8}$;
- $\operatorname{Re}W$ increases strictly;
- the minimum normalized alignment with $\overline{W_T}$ is
  $0.997638$.

The maximum projected imaginary part occurs near

\[
T\simeq3.05+2.47480i.
\]

This is a turn of the projected curve.  It does not by itself establish a
saddle, caustic, sheet transition, or endpoint; no Jacobi determinant was
evaluated at the turn in this phase.  The continuation is stopped when the
shooting-velocity norm
exceeds the declared control threshold; the stop is therefore labelled
`FIELD_NORM_CUTOFF_CONTROL`.

Because the equations and endpoint data have real coefficients, complex
conjugation produces the lower constant-phase arm.  The executable verifies
this explicitly at $\operatorname{Im}T=\pm0.4$.

## 3. Plateau endpoint control

The large-field plateau has $V_0=3/4$.  In the associated asymptotic control,
the projected round-trip length is

\[
T_s=2\sqrt{\frac3{V_0}}
\int_0^1\frac{dx}{\sqrt{x^{-1}-x^2}}.
\]

Using $u=x^3$,

\[
\int_0^1\frac{dx}{\sqrt{x^{-1}-x^2}}
=\frac13B\left(\frac12,\frac12\right)=\frac\pi3,
\]

so

\[
\boxed{T_s=\frac{4\pi}{3}}.
\]

This identity is exact for the frozen plateau control.  The present
executable does not promote it to a proof that the full Starobinsky thimble
reaches $4\pi/3$; that requires an asymptotic existence and analytic-sheet
argument beyond the bounded continuation.

## 4. The real fold is not a lapse saddle

Phase 25 found a simple fold of the reflection-symmetric fixed-$T$ field
solutions at $T_c=9.7886255681$.  Re-evaluating the Hamilton–Jacobi derivative
on that solution gives

\[
\boxed{W_T(T_c)=-73.72585\ne0}.
\]

Thus the fold is not a stationary point of the lapse integral.  It is where
the projection from field-saddle space to the fixed-$T$ coordinate becomes
singular.

Let $\delta=T_c-T>0$.  The two real branches satisfy

\[
\Delta W\propto\delta^{3/2},
\qquad
\Delta q\propto\delta^{1/2}.
\]

Numerically,

\[
\frac{\Delta W}{\delta^{3/2}}\longrightarrow93.0274,
\qquad
\frac{\|\Delta q\|}{\sqrt\delta}\longrightarrow2.37036.
\]

These are the characteristic scalings of the cubic normal form

\[
\Phi(u,\delta)=b\,\delta u+\frac c3u^3.
\]

Accordingly, a semiclassical kernel obtained after eliminating the field
saddles must use a uniform Airy treatment near this projection fold.  Which
Airy combination and phase occurs is fixed by the original contour; the fold
alone does not choose it.

## 5. Why the global intersection number remains open

Phase 27 freezes the Lorentzian continuation

\[
N_L=-iT_E,
\qquad
T_E=iN_L,
\qquad
e^{iS_L}=e^{-I_E}.
\]

Therefore positive Lorentzian lapse is the ray $T_E=i\mathbb R_+$, not the
positive-real Euclidean-$T$ branch used as a Phase-25 analytic control.

At equal endpoints, the short-time principal function is regular,

\[
W(T)=2.98719256735T-1.93989426134T^3+O(T^5),
\]

but the kernel prefactor is not: the fixed-$T$ endpoint Jacobi map behaves as
$B_v\sim T\mathbf1$ and the raw Van Vleck magnitude as $1/|T|$.  The sampled
local branches have a common candidate contact at $T=0$.  This is an
identity-kernel endpoint singularity, not a generic transverse interior
intersection.  A global dual cycle has not been constructed.

This leaves the integer thimble coefficient dependent on data not yet fixed:

- half-line versus full-line Lorentzian lapse;
- the $i\epsilon$ or lateral bypass of $N=0$;
- the BFV/Faddeev–Popov lapse measure;
- the conformal and nonzero-mode determinant phase;
- the global relative-homology endpoints of the complex BVP sheets.

The positive-real Euclidean branch is also not a recorded convergent relative
cycle: before its fold, $W$ falls from $1.40669$ to below $-1156$, so
$e^{-W}$ grows enormously.  That fact does not prove a global divergence; it
shows only that this bare real segment needs a contour completion or regulator.

## 6. Verdict

| Question | Result |
|---|---|
| Does the local imaginary tangent extend to a nontrivial complex saddle family? | **Yes, on the recorded analytic sheet.** |
| Does $\operatorname{Re}W$ grow and $\operatorname{Im}W$ remain constant? | **Yes, over the full bounded arm.** |
| Is the projected turn a new saddle or caustic? | **No such inference is supported.** |
| Is the real $T_c$ fold a lapse saddle? | **No; $W_T(T_c)\ne0$.** |
| Does the fold show Airy scaling? | **Yes.** |
| Is $T_s=4\pi/3$ exact? | **For the plateau asymptotic control only.** |
| Is the Lorentzian thimble coefficient known? | **No; endpoint and measure prescription required.** |
| Is a positive WDW/seam state or $\phi_0$ selected? | **No.** |

The result is therefore a genuine strengthening plus one useful obstruction:
the connected saddle has a long convergent complex continuation, while the
real fold and zero-lapse endpoint prevent a naive one-chart, one-contour
interpretation.

## Scope

Included:

- one homogeneous, reflection-symmetric Starobinsky analytic sheet;
- the full off-constraint fixed-$T$ equations;
- one bounded upper arm and its conjugate lower-arm control;
- the real simple-fold scaling;
- an exact plateau endpoint control.

Excluded:

- nonsymmetric and inhomogeneous saddles;
- a proof of the complex arm's exact asymptotic endpoint;
- a BFV/BRST gauge-fixed determinant and lapse measure;
- a global Stokes matrix or integer intersection number;
- a WDW physical inner product, positive density, CPT/Pin lift, or local-SUGRA
  completion.

## Primary references

- E. Witten, “Analytic Continuation of Chern–Simons Theory,”
  [arXiv:1001.2933](https://arxiv.org/abs/1001.2933).  Used only for the
  Picard–Lefschetz flow and relative-cycle framework.
- J. Feldbrugge, J.-L. Lehners, and N. Turok, “Lorentzian Quantum Cosmology,”
  [arXiv:1703.02076](https://arxiv.org/abs/1703.02076).  Used for the role of a
  declared Lorentzian lapse contour; it does not supply this saddle.
- C. Chester, B. Friedman, and F. Ursell, “An Extension of the Method of
  Steepest Descents,”
  [DOI:10.1017/S0305004100032655](https://doi.org/10.1017/S0305004100032655).
  Used for the uniform Airy treatment of coalescing saddles.
- J. J. Halliwell and J. Louko, “Steepest-descent contours in the path-integral
  approach to quantum cosmology. I. The de Sitter minisuperspace model,”
  [DOI:10.1103/PhysRevD.39.2206](https://doi.org/10.1103/PhysRevD.39.2206).
  Used for the minisuperspace contour boundary, not as evidence for the
  present numerical branch.

## Reproduction

```bash
uv run --locked python3 \
  cpt_temporal_folded_susy/phase26_global_lapse_flow.py
```

The executable emits four exact and nine numerical checks followed by one
`PHASE26_RESULT=` JSON payload.  It writes no files on import or execution.
