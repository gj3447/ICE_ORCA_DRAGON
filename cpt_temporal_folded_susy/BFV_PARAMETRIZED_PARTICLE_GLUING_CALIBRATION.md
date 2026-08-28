# BFV parametrized-particle gluing calibration

## Scope

This is a finite convention calibration, not a gravity calculation.  Its sole
model is the parametrized free particle with extended variables

\[
(t,p_t;x,p_x),\qquad C=p_t+\frac{p_x^2}{2m},\qquad m>0,
\]

and action

\[
S=\int_0^1\left(p_t\dot t+p_x\dot x-NC\right)d\tau.
\]

The calculation fixes all of the following simultaneously in this toy:

- the affine gauge \(\chi=t-\tau\);
- fixed \(x_i,x_f\) endpoint polarization and \(T=t_f-t_i>0\);
- the full-real-lapse constraint distribution;
- ordered finite ghost orientation;
- a damped \(+i0\) Fresnel branch;
- short-time delta normalization; and
- two-slab \(x\)-polarized gluing.

It does **not** supply an absolute BFV measure for gravity or minisuperspace.
It does not supply a continuum determinant/Pfaffian line, a gravity Gribov
census, a gravity contour, or a physical claim.

## Gauge and finite ghost block

The constraint flow changes the clock as

\[
t\longmapsto t+\epsilon,
\qquad \chi\longmapsto\chi+\epsilon.
\]

Thus every declared affine orbit has the one slice intersection

\[
\epsilon=\tau-t,
\qquad \{\chi,C\}=1.
\]

In the explicitly declared Berezin order \((\bar c,c)\), take

\[
A_{\mathrm{gh}}=
\begin{pmatrix}0&1\\-1&0\end{pmatrix},
\qquad \operatorname{Pf}(A_{\mathrm{gh}})=+1.
\]

This is an ordered finite Pfaffian orientation convention.  It is not a
continuum ghost determinant-line orientation.

## Full-real lapse and endpoint kernel

The declared group-average normalization is

\[
\eta_C:=\int_{\mathbb R}d\lambda\,
e^{-i\lambda C/\hbar}=2\pi\hbar\,\delta(C).
\]

This is a tempered constraint distribution, not a bounded idempotent projector.
In the clock representation, the \(p_t\) integral gives

\[
\delta(t_f-t_i-\lambda),
\]

so the full-real \(\lambda\) integral selects \(\lambda=T\).  With fixed
\(x\) endpoints, the calibrated kernel is

\[
K_T(x_f,x_i)=
\left(\frac{m}{2\pi i\hbar(T-i0)}\right)^{1/2}
\exp\left[\frac{im(x_f-x_i)^2}{2\hbar(T-i0)}\right].
\]

The rule is \(T\mapsto T-i\epsilon\), \(\epsilon>0\), before taking the
boundary value.  For a positive quadratic coefficient \(A\),

\[
\left|e^{iA/(T-i\epsilon)}\right|
=e^{-A\epsilon/(T^2+\epsilon^2)},
\]

which fixes the damped Fresnel continuation used by every slab.

## Gluing and short-time normalization

For \(T_1,T_2>0\), common polarization and common branch give

\[
\int_{\mathbb R}dx_m\,
K_{T_2}(x_f,x_m)K_{T_1}(x_m,x_i)
=K_{T_1+T_2}(x_f,x_i).
\]

The runner verifies the quadratic completion and squared prefactor relation
exactly; the branch equality itself is retained as a positive-time Fresnel
continuation theorem guard.

The short-time statement is distributional:

\[
K_T\xrightarrow[T\downarrow0]{}\delta(x_f-x_i).
\]

Its bounded diagnostic uses \(\varphi_a(x)=e^{-ax^2}\), for which

\[
(K_T*\varphi_a)(x)=
\left(1+\frac{2ia\hbar T}{m}\right)^{-1/2}
\exp\left[-\frac{ax^2}{1+2ia\hbar T/m}\right].
\]

This is a test-function check, not a pointwise definition of a delta function.

## Fail-closed boundary

Even if every toy check passes, the following remain null: gravity or
minisuperspace absolute BFV measure; continuum determinant/Pfaffian line;
gravity Gribov, contour, endpoint, and gluing data; raw-\(C\) RAQ or
rescaling equivalence; inhomogeneous closure; quantum anomaly freedom;
relational/decoherence and empirical predictions; quantum-gravity, physics,
and TOE claims.

## Observed execution

The clean committed runner was executed only through the repository control
plane:

```text
./ice run bfv_parametrized_particle_gluing_calibration
```

The run returned
`CALIBRATED_PARAMETRIZED_PARTICLE_FINITE_BFV_NORMALIZATION_AND_GLUE_ONLY`.
All 8 exact checks and the one bounded numerical check passed; the 12-sample
Gaussian short-time diagnostic had maximum absolute error
`9.9999999986250004e-06` against the declared `5e-5` bound.  Four analytic
theorem guards retain the distributional and branch hypotheses.  The result
artifact SHA-256 is
`d373476f3e20f17c60431bb4fa21c22afda22087cb947e6257470f33c8c7ba3f`.

This observed success does not alter any fail-closed gravity field.
