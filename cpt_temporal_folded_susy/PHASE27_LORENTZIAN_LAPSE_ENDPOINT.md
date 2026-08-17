# Phase 27 — Lorentzian lapse rotation and the zero-lapse endpoint

## Outcome

Phase 27 closes a convention and endpoint gap left open by Phases 24--26.
The Phase-24/25 Euclidean model did not by itself choose an orientation for a
Lorentzian lapse.  This phase explicitly declares the standard closed-FLRW
Lorentzian continuation and obtains

\[
N_L=-iT_E,
\qquad
T_E=iN_L,
\qquad
e^{iS_L}=e^{-I_E}.
\]

Consequently, a positive-real Lorentzian lapse maps to the
upper-imaginary Euclidean-$T$ ray, not to the positive-real $T$ axis used for
the Phase-25 fixed-length scan.

For the equal Phase-24 boundaries, the classical principal function is regular
and odd at short signed $T$,

\[
W(T)=2.98719256735T-1.93989426134T^3+O(T^5),
\]

but the fixed-$T$ kernel is not regular there.  Its Jacobi endpoint map obeys
$B_v\sim T\mathbf 1$, while the raw two-coordinate Van Vleck magnitude scales
as $1/|T|$.  Thus $W(0)=0$ does not remove the zero-duration delta-kernel
singularity.

In the sampled domain, the unregulated positive-$N$ ray and the recorded real
raw-$W$ segment have only the common limiting point $T=0$ after the Wick map.
That endpoint contact is not an ordinary transverse interior intersection.  A
lateral prescription fixes only
the local side of the zero-lapse singularity.  The Green-function boundary
value in Section 2 also requires the independently declared large-$N$
damping/spectral $\lambda-i0$ prescription; the zero bypass alone supplies
neither that prescription nor a global Picard--Lefschetz coefficient.

## 1. Declared Lorentzian continuation

Keep the frozen Starobinsky potential and minisuperspace coordinates

\[
q^A=(a,\phi),
\qquad
V(\phi)=\frac34\left(1-e^{-\sqrt{2/3}\phi}\right)^2.
\]

It is useful to define

\[
G_{AB}(q)=
\begin{pmatrix}
-6a&0\\
0&a^3
\end{pmatrix},
\qquad
U(q)=-3a+a^3V(\phi).
\]

On $s\in[0,1]$, Phase 27 declares the Lorentzian action

\[
S_L[q,N]
=2\pi^2\int_0^1ds\left[
\frac{1}{2N}G_{AB}q_s^Aq_s^B-NU(q)
\right],
\]

or explicitly

\[
S_L=2\pi^2\int_0^1ds\left[
-\frac{3aa_s^2}{N}+3aN
+\frac{a^3\phi_s^2}{2N}-Na^3V
\right].
\]

The already frozen Euclidean action is

\[
I_E[q,T]
=2\pi^2\int_0^1ds\left[
\frac{1}{2T}G_{AB}q_s^Aq_s^B+TU(q)
\right].
\]

Direct substitution gives

\[
S_L[q,-iT]=iI_E[q,T],
\qquad
iS_L[q,-iT]=-I_E[q,T].
\]

For the corresponding on-shell branches,

\[
S_{\rm cl}(N)=iW(iN),
\qquad
S_N=-W_T,
\qquad
S_{NN}=-iW_{TT}.
\]

The canonical constraints on the two sides of this continuation must not be
identified without continuing the momenta.  With the conventions above,

\[
\mathcal H_L=
-\frac{p_{La}^2}{24\pi^2a}
+\frac{p_{L\phi}^2}{4\pi^2a^3}
-6\pi^2a+2\pi^2a^3V,
\]

whereas the Phase-24--26 Euclidean constraint is

\[
\mathcal H_E=
-\frac{p_{Ea}^2}{24\pi^2a}
+\frac{p_{E\phi}^2}{4\pi^2a^3}
+6\pi^2a-2\pi^2a^3V.
\]

They obey $p_L=i p_E$ and
$\mathcal H_L(q,i p_E)=-\mathcal H_E(q,p_E)$.  Thus the BFV calculation in
Phase 28 is a Euclidean-continued reduction of the frozen Phase-24/25 system,
not an uncontinued Lorentzian Hamiltonian with the same potential signs.

The Euclidean saddle $T_*=0.7$ therefore lies at

\[
N_*=-0.7i
\]

in this declared Lorentzian lapse plane.  It is not a saddle on the original
positive-real $N$ axis.

## 2. Positive half-line versus full-line object

For the spectral proxy

\[
K(N;\lambda)=e^{-iN\lambda},
\qquad
i\partial_NK=\lambda K,
\]

the damped positive half-line gives

\[
\int_0^\infty dN\,e^{-iN(\lambda-i0)}
=-\frac{i}{\lambda-i0}.
\]

This is a sourced resolvent.  At the operator level,

\[
\hat H\int_{\mathcal C_N}dN\,K(N)
=i[K(N)]_{\partial\mathcal C_N},
\]

so the $N=0$ endpoint supplies the identity or
$\delta(q_+-q_-)$ source.

By contrast, a suitable full-real group average is distributionally

\[
\int_{-\infty}^{+\infty}dN\,e^{-iN\hat H}
=2\pi\delta(\hat H),
\qquad
\hat H\delta(\hat H)=0.
\]

It is a constraint-supported rigging distribution, not automatically a
normalizable state or a positive trace-class density.  A contour deformation
that preserves endpoints and relative homology cannot turn the half-line
Green function into the full-line group average.

## 3. Equal-boundary short-time action

The frozen boundary is

\[
q_-=q_+=q_0,
\qquad
q_0=(3.56680319357,1.01858094640).
\]

For an analytic equal-boundary branch, a covariant short-time expansion gives

\[
W(q_0,q_0;T)
=2\pi^2\left[
U_0T
-\frac{T^3}{24}
U_{,A}G^{AB}U_{,B}
+O(T^5)
\right].
\]

At the frozen boundary,

\[
U_0=0.151332943346,
\qquad
U_{,A}G^{AB}U_{,B}=2.35862859240,
\]

so

\[
\boxed{
W(T)=2.98719256735T-1.93989426134T^3+O(T^5)
}.
\]

The executable solves the full off-constraint fixed-$T$ boundary problem and
finds quadratic convergence of both extracted coefficients:

| $T$ | $W/T$ | extracted cubic coefficient |
|---:|---:|---:|
| 0.10000 | 2.96778237147 | -1.94101958838 |
| 0.05000 | 2.98234212840 | -1.94017558038 |
| 0.01250 | 2.98688945613 | -1.93991184292 |
| 0.00625 | 2.98711679006 | -1.93989865346 |

In particular,

\[
W_T(0^+)=2.98719256735\ne0.
\]

The zero-lapse endpoint is not another saddle.

## 4. Jacobi and Van Vleck endpoint scaling

In local configuration coordinates, the initial-velocity endpoint map is

\[
B_v=
\left.\frac{\partial q_+}{\partial\dot q_-}\right|_{q_-,T}
=T\mathbf 1+O(T^3),
\]

\[
\det B_v=T^2[1+O(T^2)].
\]

The last recorded value is

\[
\frac{\det B_v}{T^2}\bigg|_{T=0.00625}
=0.999997553866.
\]

Since

\[
p_A=2\pi^2G_{AB}\dot q^B,
\]

the canonical momentum endpoint map and mixed Hessian obey

\[
B_p=T(2\pi^2G_0)^{-1}+O(T^3),
\]

\[
W_{q_-q_+}=-B_p^{-1}
=-\frac{2\pi^2}{T}G_0+O(T).
\]

Numerically,

\[
W_{q_-q_+}
=\frac1T
\begin{pmatrix}
422.435237965&0\\
0&-895.709502254
\end{pmatrix}
+O(T).
\]

For the raw two-coordinate Van Vleck matrix
$D=-W_{q_-q_+}$,

\[
\det D
=-\frac{378379.256732}{T^2}+O(1),
\]

\[
|\det D|^{1/2}
=\frac{615.1253992}{|T|}+O(|T|).
\]

The negative determinant records the indefinite gravitational configuration
metric.  The phase of its square root is not fixed without a conformal-field
contour.  Moreover, the physical power of $T$ can be changed by gauge
reduction, ghosts, and the Faddeev--Popov measure.  The executable therefore
records this only as a raw two-coordinate fixed-$T$ control.

## 5. Signed raw-$W$ control

At fixed $s$, both terms in the Euclidean action change sign under
$T\mapsto-T$.  On the corresponding analytic classical branch,

\[
W(-T)=-W(T),
\qquad
W_T(-T)=W_T(T).
\]

The direct signed solve gives

\[
W(+0.7)=+1.40669054283434,
\qquad
W(-0.7)=-1.40669054283434,
\]

with vanishing constraint at both ends.  At the eight sampled points
$T=\pm0.1,\pm0.2,\pm0.4,\pm0.65$, $W_T$ is positive and the odd-action
residual is below $5\times10^{-14}$.

These are necessary sampled raw-exponent data for a candidate Stokes segment.
They do not establish continuous positivity or solve the Picard--Lefschetz
flow equation, much less a heteroclinic of the full prefactored lapse
integrand: the Jacobi/Van Vleck factor is singular at $T=0$, while the
Phase-28 reduced Dirichlet-ghost diagnostic has not yet been combined with a
zero-lapse-uniform bulk determinant.

## 6. What the lateral prescription fixes

Under $T=iN$,

\[
N-i0\longmapsto iN+0^+,
\qquad
N+i0\longmapsto iN-0^+.
\]

Thus a below-origin Lorentzian bypass maps to the right side of the
upper-imaginary $T$ ray; the conjugate bypass maps to its left.

This fixes:

- the side of the zero-lapse singularity;
- a determinant square-root branch only after the determinant and its global
  continuation are supplied;
- which local relative-contour side is used near $T=0$ in a subsequent
  intersection count.

It does not by itself fix convergence as $|N|\to\infty$ or the sign of the
spectral $i0$.

It does not fix:

- a global $n_\sigma$;
- all complex fixed-$T$ BVP sheets;
- the FP or one-loop singularity structure;
- whether a recorded local PL arm reaches an admissible good end;
- a WDW inner product, probability, or state.

The positive-real $N$ contour maps to $i\mathbb R_+$.  The sampled raw-$W$ real
branch approaches $T=0$, and the analytic short-time limit has
$W_T(0)\ne0$.  No global dual cycle was computed.  If the two local directions
are extended through the origin they are geometrically transverse, but their
contact occurs at a singular common endpoint.  It is therefore not an
ordinary interior intersection and receives no integer or half-integer
assignment in this phase.

## 7. Claim boundary

The executable supports only the following bounded claims:

- the declared Lorentzian action has the exact Wick map $N_L=-iT_E$;
- positive-real $N$ maps to upper-imaginary $T$;
- the equal-boundary classical action has the recorded linear and cubic
  short-time coefficients;
- the raw Jacobi and Van Vleck factors remain singular at zero lapse;
- the signed raw-$W$ branch has paired $\pm0.7$ stationary points and positive
  derivative at the eight recorded samples between them;
- the positive lapse half-line is a sourced resolvent at the spectral operator
  level, while the full line is constraint-supported.

The following remain open:

- deriving the full BFV/FP endpoint measure from, among other inputs, the
  Phase-28 reduced Dirichlet-ghost diagnostic, then combining it with the raw
  zero-lapse Van Vleck factor and a gauge-fixed bulk determinant;
- a gauge-fixed bulk determinant and its phase;
- a zero-lapse-uniform full configuration-space kernel;
- a global PL flow, Stokes matrix, or intersection number;
- a physical WDW rigging domain or inner product;
- any positive density, entropy, Pin lift, or local-SUGRA completion.

## 8. Reproduction

Run:

```bash
uv run --locked python3 \
  cpt_temporal_folded_susy/phase27_lorentzian_lapse_endpoint.py
```

The current executable emits 13 exact checks, 8 numerical checks, and one
machine-readable `PHASE27_RESULT` record.  It writes no files.

## Primary references and their bounded role

- [Halliwell, *Derivation of the Wheeler--DeWitt equation from a path integral for minisuperspace models*](https://doi.org/10.1103/PhysRevD.38.2468) — BFV minisuperspace lapse range, measure, and the WDW boundary identity.
- [Teitelboim, *Causality versus gauge invariance in quantum gravity and supergravity*](https://doi.org/10.1103/PhysRevLett.50.705) — positive proper time and the distinction between causal and gauge-invariant objects.
- [Marolf, *Refined Algebraic Quantization: Systems with a single constraint*](https://arxiv.org/abs/gr-qc/9508015) — full-group averaging and the distributional physical construction; it does not imply trace-class positivity here.
- [Gutzwiller, *Phase-integral approximation in momentum space and the bound states of an atom*](https://doi.org/10.1063/1.1705112) — Jacobi/Van Vleck short-time semiclassics and caustic phases.
- [Gibbons, Hawking, and Perry, *Path integrals and the indefiniteness of the gravitational action*](https://doi.org/10.1016/0550-3213(78)90161-X) — the conformal-factor contour obstruction; it does not choose the present lapse contour.
- [Banihashemi and Jacobson, *On the lapse contour in the gravitational path integral*](https://doi.org/10.1103/PhysRevD.111.066014) — in their stated gravitational construction, integrating momenta before the lapse requires a below-origin lapse contour.  This fixes neither the FP factor nor $n_\sigma$ in the present bounded model.
