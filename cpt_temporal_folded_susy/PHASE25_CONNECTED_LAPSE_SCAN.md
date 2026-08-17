# Phase 25 — connected lapse saddle, Schur reduction, and fold

## Outcome

For the frozen Phase-24 endpoints, the connected Starobinsky interval is a
nondegenerate stationary point of the proper-length modulus:

\[
T_*=0.7,
\qquad W_T(T_*)=0,
\qquad W_{TT}(T_*)=-8.9231430383.
\]

Three effects that were previously mixed together are now separated.

1. The constrained rank-one mixed response at $T_*$ is the Schur complement
   produced by eliminating the lapse modulus.  It is not a fixed-$T$
   Dirichlet caustic.
2. The real $T$ direction is locally an ascent direction for $e^{-W}$.
   The local convergent constant-phase branch is tangent to $i\mathbb R$.
3. The same recorded real, reflection-symmetric branch later reaches a simple
   Dirichlet fold at

   \[
   T_c=9.7886255681,
   \]

   where two real solutions merge and the endpoint Jacobi map loses one rank.

The first two statements strengthen the Phase-24 saddle calculation.  The
third is a genuine counterexample to treating the tracked reflection-symmetric
real proper-length family as one globally regular, single-valued graph.  None
of them determines the Picard--Lefschetz intersection number or constructs a
positive quantum-gravity state.

## 1. Frozen action and the off-shell correction

The units, potential, endpoints, and boundary order are unchanged:

\[
M_{\rm P}=M=1,
\qquad
V(\phi)=\frac34\left(1-e^{-\sqrt{2/3}\,\phi}\right)^2,
\]

\[
q=(a_-,\phi_-,a_+,\phi_+),
\qquad
q_0=(3.56680319357,1.01858094640,
     3.56680319357,1.01858094640).
\]

At fixed proper length $T$, the principal function is the on-shell value of

\[
W(q,T)=2\pi^2\int_0^T d\tau\left[
-3a(a'^2+1)+a^3\left(\frac12\phi'^2+V\right)
\right].
\]

The full off-constraint Euler--Lagrange equations are

\[
a''=\frac{1-a'^2}{2a}-\frac a4\phi'^2-\frac a2V,
\qquad
\phi''+3\frac{a'}a\phi'=V_{,\phi}.
\]

The Hamiltonian constraint function is

\[
\mathcal C=a'^2-1-\frac{a^2}{3}
\left(\frac12\phi'^2-V\right).
\]

Only on $\mathcal C=0$ may the first equation be replaced by

\[
a''=-\frac a3(\phi'^2+V),
\qquad
a''_{\rm full}-a''_{\mathcal C=0}=-\frac{\mathcal C}{2a}.
\]

This distinction leaves the constrained Phase-24 result unchanged, but it is
essential when $T$ is scanned off shell.  The earlier fixed-$T$ comparison
was therefore regenerated from the full variational equation.

## 2. Hamilton--Jacobi lapse identity

The canonical energy is

\[
E=p_a a'+p_\phi\phi'-L=-6\pi^2a\mathcal C.
\]

For fixed endpoint configurations,

\[
\boxed{W_T=-E=6\pi^2a\mathcal C}.
\]

Finite differences of $W(T)$ reproduce this identity away from the
constraint surface.  At $T_*=0.7$,

\[
W_*=1.40669054283434,
\qquad
\mathcal C=2.2\times10^{-16},
\qquad
W_T=4.7\times10^{-14}.
\]

The converged curvature is

\[
\boxed{W_{TT}=-8.9231430383}.
\]

This is a negative curvature of the lapse modulus on the chosen real slice.
It is not a count of physical bulk negative modes.

## 3. Lapse elimination is the Phase-24 rank reduction

Let $H_5$ be the Hessian of $W(q,T)$, ordered as
$(a_-,\phi_-,a_+,\phi_+,T)$.  The corrected calculation gives

\[
H_5\simeq
\begin{pmatrix}
-577.945763&67.031813&613.292969&13.565329&59.787739\\
67.031813&1281.921139&13.565329&-1296.933178&139.656496\\
613.292969&13.565329&-577.945763&67.031813&59.787739\\
13.565329&-1296.933178&67.031813&1281.921139&139.656496\\
59.787739&139.656496&59.787739&139.656496&-8.923143
\end{pmatrix}.
\]

Solving $W_T(q,T(q))=0$ gives the reduced Hessian

\[
\boxed{
\bar W_{qq}=W_{qq}-W_{qT}W_{TT}^{-1}W_{Tq}
}.
\]

Numerically, this Schur complement agrees with the independently differentiated
constraint-preserving Phase-24 Hessian at relative operator error below
$10^{-10}$.  In particular, the fixed-$T$ mixed block is full rank,

\[
\sigma(W_{q_-q_+}^{T\,{\rm fixed}})
=(1297.0295059,613.3892978),
\]

whereas the lapse-eliminated block has spectrum

\[
\sigma(\bar W_{q_-q_+})
=(1902.7254364,\,O(10^{-9})).
\]

Thus the vanishing direction is the Hamilton--Jacobi/lapse direction, not an
endpoint caustic at $T_*$.

## 4. Direct Jacobi test at the base saddle

The variational flow gives

\[
B_v=\left.\frac{\partial(a_+,\phi_+)}
{\partial(a'_-,\phi'_-)}\right|_{q_-,T}
=
\begin{pmatrix}
0.688639116937&-0.015272546281\\
0.007202850597&0.690476842295
\end{pmatrix},
\]

\[
\det B_v=0.475599368812\ne0.
\]

After converting the initial velocities to canonical momenta,

\[
B_p=
\begin{pmatrix}
-0.001630164946&-0.000017050781\\
-0.000017050781&0.000770871405
\end{pmatrix},
\]

\[
\det B_p=-1.2569382712\times10^{-6}\ne0.
\]

The type-1 Hamilton principal function obeys

\[
W_{q_-q_+}^{T\,{\rm fixed}}=-B_p^{-1},
\qquad
W_{q_-q_+}^{T\,{\rm fixed}}B_p=-\mathbf1.
\]

Therefore there is no homogeneous fixed-$T$ Dirichlet Jacobi zero at the
base saddle.

## 5. Local complex-$T$ descent branch

Near the saddle,

\[
W(T)=W_*-\frac{8.9231430383}{2}(T-T_*)^2+\cdots.
\]

For the semiclassical factor $e^{-W/\hbar}$, real $\delta T$ is locally
nonconvergent, while $\delta T=iy$ is convergent.  Solving the complex
boundary-value problem together with ${\rm Im}\,W=0$ gives:

| ${\rm Im}\,T$ | ${\rm Re}\,T$ | ${\rm Re}\,W-W_*$ |
|---:|---:|---:|
| 0.025 | 0.7001747501 | 0.0027890081 |
| 0.050 | 0.7006988672 | 0.0111623406 |
| 0.100 | 0.7027933498 | 0.0447501764 |
| 0.200 | 0.7111401293 | 0.1806062273 |
| 0.400 | 0.7440664322 | 0.7476684754 |

The maximum recorded $|{\rm Im}\,W|$ is below $2\times10^{-13}$, and
${\rm Re}\,W$ increases away from the saddle.  This is a local
constant-phase descent segment.  It is not yet a global thimble or a proof
that the saddle has nonzero intersection with a chosen original lapse cycle.

## 6. Real branch continuation and the simple fold

One reflection-symmetric real branch was continued with positive scale factor
from $T=0.2$ to $T=9.78$.  Write its midpoint data as
$c=(a_c,\phi_c)$ and its half length as $h=T/2$.  The endpoint map is

\[
F(c,h)=(a_+(c,h)-a_+,\,\phi_+(c,h)-\phi_+).
\]

The branch reaches

\[
c_*=(1.24799533,0.100167954),
\qquad
T_c=9.7886255681,
\]

where

\[
\sigma(F_c)=(8.57366239,\,O(10^{-16})).
\]

With normalized right and left null vectors $r,\ell$, the magnitudes of the
two generic fold conditions are nonzero (the individual SVD-vector signs are
conventional):

\[
\ell^TF_h\simeq0.5177826,
\qquad
\ell^TD^2F[r,r]\simeq0.368617.
\]

At $T=9.78<T_c$, two distinct regular real solutions occur:

\[
c_1=(1.35829381,0.09182399),
\qquad
c_2=(1.13901710,0.11035950),
\]

with opposite signs of the full endpoint-monodromy determinant.  This is the
recorded local two-branch structure of a simple fold.  It does not establish
that no nonsymmetric or complex saddle exists beyond $T_c$.

At the fold, a type-1 mixed Hessian and the naive Van Vleck prefactor become
singular.  The exact kernel need not diverge: a different polarization or a
uniform Airy treatment is required near a simple fold.

## 7. What the lapse contour would mean

A positive-lapse two-boundary proper-time integral generally constructs a
Green function, while a suitable full-real lapse group average is a
distributional $\delta(\hat H)$-type object.  A Picard--Lefschetz deformation
does not change which of these objects was defined by the original contour.

A saddle contributes only after specifying the original cycle and finding a
nonzero intersection number with its upward cycle.  Consequently, the
following remain open:

- the global thimble and Stokes chamber;
- the lapse measure and Faddeev--Popov factor;
- the gauge-reduced bulk fluctuation operator and physical Morse index;
- the WDW inner product, trace-class density, and CPT/Pin/SUGRA completion.

The boundary Hessian, the lapse curvature, and the bulk gauge-fixed Morse
operator are different objects and must not be used interchangeably.

## 8. Reproduction

Run:

```bash
uv run --locked python3 \
  cpt_temporal_folded_susy/phase25_connected_lapse_scan.py
```

The executable records exact algebra checks, bounded numerical controls, all
frozen inputs, the real continuation, the fold data, and the local complex
segment in `PHASE25_RESULT`.  A passing run supports only the scope stated in
that payload.

## Primary references and their role

- [Halliwell, *Derivation of the Wheeler--DeWitt equation from a path integral for minisuperspace models*](https://doi.org/10.1103/PhysRevD.38.2468) — lapse modulus, boundary conditions, and proper-time contour distinctions.
- [Halliwell and Louko, *Steepest-descent contours in the path-integral approach to quantum cosmology. I*](https://doi.org/10.1103/PhysRevD.39.2206) — contour-dependent saddle sums in minisuperspace.
- [Feldbrugge, Lehners, and Turok, *Lorentzian quantum cosmology*](https://arxiv.org/abs/1703.02076) — Picard--Lefschetz cycles and intersection numbers for lapse integrals.
- [Gutzwiller, *Phase-integral approximation in momentum space and the bound states of an atom*](https://doi.org/10.1063/1.1705112) — fixed-time/fixed-energy Hamilton principal functions and Van Vleck/Jacobi relations.
- [Chester, Friedman, and Ursell, *An extension of the method of steepest descents*](https://doi.org/10.1017/S0305004100032655) — uniform Airy-type asymptotics for coalescing saddle points.
- [Barvinsky and Nesterov, *Quantum effective action in spacetimes with branes and boundaries*](https://arxiv.org/abs/hep-th/0512291) — separation of bulk Dirichlet determinants from boundary response operators.
- [Gibbons, Hawking, and Perry, *Path integrals and the indefiniteness of the gravitational action*](https://doi.org/10.1016/0550-3213(78)90161-X) — conformal contour obstruction.
