# Phase 33 — simple-fold Airy uniformization and intersection scope gate

## Outcome

The real fixed-boundary branch found in Phase 25 reaches a genuine simple
Dirichlet fold at

\[
T_c=9.78862556808.
\]

The two real classical branches were solved down to

\[
\delta\equiv T_c-T=2\times10^{-4}.
\]

At the smallest recorded separation, the action-gap ratio is

\[
\boxed{
\left.\frac{|\Delta W|}{\delta^{3/2}}\right|_{\delta=2\times10^{-4}}
=93.02721
}
\]

and the last four recorded points have log--log slope $1.499976$.  The
corresponding invariant local Airy **action-scale** magnitude satisfies

\[
\boxed{
\zeta_{\rm act}
=\left(\frac{3|\Delta W|}{4}\right)^{2/3}
\quad\text{with}\quad
\left.\frac{\zeta_{\rm act}}{\delta}\right|_{\delta=2\times10^{-4}}
=16.94783.
}
\]

Its last-four-point log--log slope is $0.999984$.  These are recorded
finite-resolution ratios and slopes, not error-certified asymptotic
coefficients.

The soft Jacobi singular value scales as $\delta^{1/2}$, while each separate
endpoint Van Vleck proxy scales as $\delta^{-1/4}$.  That divergence is the
expected failure of separate-saddle asymptotics at a fold.  It does not, by
itself, prove that an exact kernel diverges: the canonical fold has a regular
two-dimensional Airy solution space.

There are two equally important negative results.

First, the fold is not another lapse saddle:

\[
\boxed{W_T(T_c)=-73.72585376\neq0.}
\]

Second, local regularity does not choose a unique uniform kernel.  Both
$\operatorname{Ai}$ and $\operatorname{Bi}$ are regular at the fold and

\[
W[\operatorname{Ai},\operatorname{Bi}](0)=\frac1\pi\neq0.
\]

Thus an original relative cycle is still needed to choose an Airy
contour/Stokes combination.  The determinant line separately fixes a
prefactor orientation/phase, while the analytic path-integral amplitude fixes
the coefficients multiplying that contour function and its derivative.  The
fold removes a coordinate singularity; it does not solve these global data.

Finally, a radius-one $T$-plane patch around $T_c$ is disjoint from both the
imaginary-axis full-lapse contour and all Phase-32 lower bypasses with
$r\leq0.1$.  The fold therefore adds no **local lapse-base intersection** to
the Phase-32 projected crossing whose coordinate sign is $+1$ under the
declared orientations.  This statement is local; other
dual arms outside the patch remain uncomputed.

The executable passes 8 exact and 7 numerical checks.  No desired inflation
or SUSY value is supplied.

## 1. Frozen simple fold

Use the reflection-symmetric midpoint data

\[
c=(a_c,\phi_c),\qquad h=T/2
\]

and endpoint map

\[
F(c,h)=
\bigl(a_+(c,h)-a_+,\,\phi_+(c,h)-\phi_+\bigr).
\]

At the fold,

\[
c_*=(1.24799533026,0.100167953907),
\]

\[
\sigma(F_c)
=(8.57366238563,\,9.98\times10^{-17}).
\]

If $r$ and $\ell$ are normalized right and left null vectors, the two generic
fold transversality magnitudes are nonzero:

\[
|\ell^TF_h|=0.5177826518,
\qquad
|\ell^TD^2F[r,r]|=0.3686170857.
\]

The signs of individual singular vectors are conventional; only these
magnitudes and the resulting two-branch structure are used.

The full fixed-$T$ endpoint monodromy has one vanishing singular direction at
the fold.  This is a Dirichlet caustic of the endpoint projection.  It is not
a critical point of the lapse-reduced action because $W_T\neq0$ there.

## 2. Canonical fold normal form

The local canonical phase is

\[
\Phi(u;\zeta)=\frac{u^3}{3}-\zeta u.
\]

For $\zeta>0$ its stationary points are

\[
u_\pm=\pm\sqrt\zeta.
\]

Their phase gap is exactly

\[
\Phi(u_-)-\Phi(u_+)
=\frac43\zeta^{3/2}.
\]

Hence a measured branch-action gap fixes the action-to-the-$2/3$-power scale

\[
\zeta_{\rm act}
=\left(\frac{3|\Delta W|}{4}\right)^{2/3}.
\]

The second derivatives are

\[
\Phi''(u_+)=2\sqrt\zeta,
\qquad
\Phi''(u_-)=-2\sqrt\zeta.
\]

A separate Gaussian saddle magnitude therefore contains

\[
|\Phi''|^{-1/2}
=\frac1{\sqrt2}\zeta^{-1/4}.
\]

This divergent factor is exactly why ordinary isolated-saddle asymptotics is
not uniform at $\zeta=0$.  The standard treatment of coalescing saddles is the
Airy uniformization of
[Chester--Friedman--Ursell](https://doi.org/10.1017/S0305004100032655).

In the declared real canonical chart with exponent $e^{-W/\hbar}$, set
$u=-\hbar^{1/3}t$.  Then

\[
-\frac{\Phi}{\hbar}
=\frac{t^3}{3}
-\frac{\zeta_{\rm act}}{\hbar^{2/3}}t,
\qquad
z=\frac{\zeta_{\rm act}}{\hbar^{2/3}}.
\]

An off-real argument phase would have to come from an explicitly derived
complex canonical map or exponent branch.  The relative cycle instead
selects the Ai/Bi (or rotated-Ai) contour combination, while the determinant
line fixes a prefactor orientation/phase.  None of those latter data is
inferred from the real action gap.

## 3. Numerical two-branch scaling

The two actual connected fixed-boundary solutions give:

| $\delta=T_c-T$ | $|\Delta W|/\delta^{3/2}$ | $\zeta_{\rm act}/\delta$ ($\hbar=1$ units) | $\sigma_{\min,-}/\sqrt\delta$ | $\sigma_{\min,+}/\sqrt\delta$ |
|---:|---:|---:|---:|---:|
| 0.0200 | 92.96908 | 16.94077 | 4.39624 | 3.80553 |
| 0.0100 | 92.99846 | 16.94434 | 4.30247 | 3.88554 |
| 0.0050 | 93.01315 | 16.94613 | 4.23785 | 3.94331 |
| 0.0020 | 93.02197 | 16.94720 | 4.18162 | 3.99543 |
| 0.0010 | 93.02490 | 16.94755 | 4.15366 | 4.02203 |
| 0.0005 | 93.02639 | 16.94773 | 4.13403 | 4.04097 |
| 0.0002 | 93.02721 | 16.94783 | 4.11672 | 4.05787 |

The endpoint-monodromy determinants have opposite signs on the two branches.
After division by $\sqrt\delta$, their last recorded values are

\[
-1.03403\times10^4,
\qquad
+1.01334\times10^4.
\]

Correspondingly, the endpoint Jacobi/Van Vleck proxy

\[
|\det B_v|^{-1/2}
\]

diverges as $\delta^{-1/4}$.  The rescaled values

\[
\delta^{1/4}|\det B_v|^{-1/2}
\]

give two finite recorded values, $0.0098341$ and $0.0099340$, at the smallest
$\delta$.  Their separation decreases monotonically over the recorded scan,
consistent with approach to a common leading value; distinct branch limits
have not been established.

This proxy differs from a complete quantum prefactor.  It omits the chosen
functional measure, ghost superdeterminant, Airy amplitude function, and
global determinant phase.  The numerical result establishes the fold scaling
only.

All 14 branch solves have endpoint residual below

\[
4.2\times10^{-13}.
\]

## 4. Why regularity does not select the contour

The local uniform equation is

\[
y''(z)-z y(z)=0.
\]

Both

\[
\operatorname{Ai}(z),\qquad\operatorname{Bi}(z)
\]

are regular at $z=0$.  Their Wronskian is

\[
\operatorname{Ai}(0)\operatorname{Bi}'(0)
-\operatorname{Ai}'(0)\operatorname{Bi}(0)
=\frac1\pi.
\]

Therefore the local Airy ODE solution space is rank two.  In an
Ai/Bi basis one may write

\[
\mathcal A_{\mathcal C}(z)
=c_A\operatorname{Ai}(z)+c_B\operatorname{Bi}(z).
\]

Neither finiteness nor the simple-fold equations says that both basis
solutions are admissible lifted gravitational contours, or fixes the
contour/Stokes combination.  That combination encodes how the original
relative cycle enters and leaves the local Airy chart.

There is a second, distinct layer.  For a generic analytic path-integral
amplitude $G(u,\zeta)$, the CFU decomposition has the form

\[
G(u,\zeta)
=A(\zeta)+B(\zeta)u+(u^2-\zeta)H(u,\zeta).
\]

At the two saddles,

\[
G_\pm=A\pm B\sqrt\zeta.
\]

Thus $A$ and $B$ are even/odd **amplitude data**, not the Ai/Bi contour
coefficients.  For a chosen contour, the uniform expansion schematically
contains

\[
e^{-W_0/\hbar}
\left[
\alpha A\hbar^{1/3}\mathcal A_{\mathcal C}(z)
+\beta B\hbar^{2/3}\mathcal A'_{\mathcal C}(z)
+\cdots
\right],
\]

where the phases $\alpha,\beta$ depend on the canonical exponent convention.
The present phase computes neither the Airy contour/Stokes multiplier nor the
full analytic amplitude.  In Picard--Lefschetz language, the former requires
the complete cycle and oriented intersection data, not merely the Hessian; see
[Witten](https://arxiv.org/abs/1001.2933).

Accordingly, this phase does **not** claim that the uncomputed physical kernel
is finite.  It proves the narrower statement that divergence of the two
separate endpoint Van Vleck terms is not, in the canonical fold normal form,
a necessary divergence of a uniform kernel.  A singular measure or amplitude
could still change the answer and has not been excluded.

## 5. Relation to the Phase-32 lapse contour

Under $T=iN$, the declared full real lapse away from the small endpoint cap
lies on the imaginary $T$ axis.  Every Phase-32 lower bypass obeys

\[
|T|=r\leq0.1.
\]

The fold is centered at $T_c\simeq9.7886$.  Thus a radius-one fold patch has

\[
\operatorname{Re}T>8.7886
\]

and cannot meet either the imaginary axis or those endpoint caps.  The fold
does not add a local crossing to the recorded finite-$r$ Phase-32 projected
lapse-base crossing.

This does not determine the global intersection matrix.  The complete dual
may leave the fold chart and cross the original cycle elsewhere, and other
complex saddle sheets may exist.  Airy uniformization is a continuation tool,
not a substitute for the global relative cycle.

## 6. What is established and what remains open

Established in the frozen homogeneous connected model:

- the recorded caustic is a transverse simple fold;
- two actual fixed-boundary branches have the universal
  $|\Delta W|\sim\delta^{3/2}$ scaling;
- at $\delta=2\times10^{-4}$, the recorded ratio
  $\zeta_{\rm act}/\delta=16.94783$, with last-four-point log slope
  $0.999984$;
- the soft Jacobi direction scales as $\sqrt\delta$ and the branch
  determinants have opposite signs;
- separate endpoint Van Vleck proxies scale as $\delta^{-1/4}$;
- the fold is not a lapse saddle;
- a radius-one fold chart is locally disjoint from the Phase-32 lapse cycle;
- local Airy regularity leaves a rank-two ODE solution space, distinct from
  the even/odd analytic-amplitude data; admissible lifted gravitational
  cycles remain uncomputed.

Still open:

- an off-real canonical-map/exponent branch for the Airy argument, and the
  separately selected contour/Stokes combination;
- the analytic amplitude coefficients multiplying the chosen Airy function
  and its derivative, plus the absolute determinant/Maslov line;
- every joint upward-cycle arm outside the fold chart;
- the complete global $n_\sigma$;
- the nonlinear BFV/BV measure, inhomogeneous SUGRA modes, and physical WDW
  inner product;
- a trace-class seam state, initial-value peak, or SUSY-breaking prediction.

The next decisive calculation is to choose one complete regulated relative
cycle, transport its oriented determinant line from the short-time identity
kernel into this Airy chart, fix its Airy contour/Stokes multiplier and
analytic amplitude data, and then continue every dual arm to its good ends.

## Reproduction

```bash
uv run --locked python3 \
  cpt_temporal_folded_susy/phase33_fold_airy_uniformization.py

./ice run phase33_fold_airy_uniformization
```

The final JSON payload contains:

```json
{"exact_checks": 8, "numerical_checks": 7}
```

The script writes no files.

## Primary-source boundaries

- [Chester--Friedman--Ursell](https://doi.org/10.1017/S0305004100032655):
  uniform asymptotics for coalescing saddles; not the cosmological branch
  calculation or a choice of contour/Stokes data.
- [Witten](https://arxiv.org/abs/1001.2933): relative cycles and thimble
  coefficients; not a derivation of the original lapse contour here.
- [Halliwell--Louko](https://doi.org/10.1103/PhysRevD.42.3997): lapse-contour
  sensitivity in minisuperspace; not the present Airy connection data.
- [Gibbons--Hawking--Perry](https://doi.org/10.1016/0550-3213(78)90161-X):
  conformal-factor contour obstruction; not a computation of this fold's
  determinant line.
