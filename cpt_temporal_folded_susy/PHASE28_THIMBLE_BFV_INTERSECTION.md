# Phase 28 — bounded lapse thimble, intersection, and BFV diagnostic

## Outcome

Phase 28 adds the BFV--BRST reduction and a separately bounded intersection
diagnostic to the Phase-25--27 lapse calculations while
keeping the frozen homogeneous Starobinsky boundary problem unchanged.

First, the upper constant-phase branch was continued with pseudo-arclength.
It passes smoothly through a maximum of its coordinate
$\operatorname{Im}T$:

\[
T_{\rm turn}=3.0344675280+2.4747060441i,
\qquad
W=204.9823519742+O(10^{-10})i,
\]

and reaches the bounded endpoint

\[
T_{\rm last}=3.3942970911+2.4311344118i,
\qquad
W=339.5058547285+O(10^{-10})i.
\]

Thus the failure of a fixed-$\operatorname{Im}T$ parametrization near
$\operatorname{Im}T\simeq2.47$ is **not** the end of the recorded thimble arm.
No scale zero or homogeneous complex Dirichlet Jacobi zero occurs at the
monitored points.  This is a bounded continuation, not a determination of the
arm's endpoint at a good asymptotic region or singularity.

Second, one real dual/upward branch was followed from $T_*=0.7$ to $T=0.2$.
For each explicitly specified two-sided vertical cycle

\[
\mathcal C_{\epsilon}^{\rm full}:
T=\epsilon+iN,
\qquad -2.5\leq N\leq2.5,
\]

with $\epsilon=0.25,0.35,0.45,0.55$, that recorded branch has one transverse
crossing at $T=\epsilon$.  This is a **bounded crossing diagnostic**, not the
global relative-homology intersection number.  In particular, the positive
half-cycle $N\geq0$ meets it at the cycle endpoint, while a positive-real
Euclidean-$T$ contour overlaps the dual branch nontransversely.  Neither case
receives a coefficient here.

The reduced BFV calculation of the **Euclidean-continued Phase-24/25
constraint** also shows that the lapse modulus is not removed by the chosen
Dirichlet ghost normalization.  At the time-symmetric neck, intrinsic $a$ and
$\phi$ clocks are locally singular, whereas the extrinsic $p_a$ clock is
regular:

\[
\{a,\mathcal H\}=0,
\quad
\{\phi,\mathcal H\}=0,
\quad
\{p_a,\mathcal H\}=12\pi^2.
\]

## 1. Frozen Euclidean problem

The units, potential, boundary order, and endpoints are inherited unchanged
from Phases 24 and 25:

\[
M_{\rm P}=M=1,
\qquad
V(\phi)=\frac34\left(1-e^{-\sqrt{2/3}\phi}\right)^2,
\]

\[
q=(a_-,\phi_-,a_+,\phi_+),
\]

\[
q_0=(3.56680319357,1.01858094640,
     3.56680319357,1.01858094640).
\]

The fixed-endpoint Euclidean principal function is

\[
W(T)=2\pi^2\int_0^T d\tau
\left[-3a(a'^2+1)+a^3\left(\frac12\phi'^2+V\right)\right].
\]

Its Hamilton--Jacobi derivative on a fixed-$T$ boundary-value branch is

\[
W_T=-E=6\pi^2a\mathcal C.
\]

The recorded saddle remains

\[
T_*=0.7,
\quad
W_*=1.40669054283434,
\quad
W_{TT}=-8.92314303834.
\]

Nothing in this phase selects the supplied midpoint $\phi=1$, the boundary,
or $T_*$.  They remain calibration inputs.

## 2. Picard--Lefschetz convention

For the Euclidean semiclassical factor

\[
e^{-W(T)/\hbar},
\]

the one-complex-dimensional flows used here are

\[
\frac{dT}{ds}=\overline{W_T}
\qquad\text{(downward thimble)},
\]

\[
\frac{dT}{ds}=-\overline{W_T}
\qquad\text{(dual/upward cycle)}.
\]

They obey exactly

\[
\frac{d\operatorname{Re}W}{ds}=\pm|W_T|^2,
\qquad
\frac{d\operatorname{Im}W}{ds}=0.
\]

Writing $W_{TT}=-\mu$ with $\mu>0$, the local quadratic form is

\[
W=W_*-\frac\mu2(T-T_*)^2+\cdots.
\]

The descent directions are tangent to $i\mathbb R$ and the dual directions
to $\mathbb R$.  If a global intersection coefficient were nonzero, rotating
$\delta T=iu$ would give the local modulus integral

\[
\int_{\mathcal J_*}d(\delta T)
e^{+\mu(\delta T)^2/(2\hbar)}
=i\sqrt{\frac{2\pi\hbar}{\mu}}
=i\,0.8391333983\sqrt\hbar.
\]

The coefficient is explicitly conditional: a local Gaussian never determines
whether the saddle belongs to the decomposition of an original contour.

## 3. Pseudo-arclength continuation

At fixed real boundary data, the complex shooting variables are

\[
x=(\operatorname{Re}T,\operatorname{Im}T,
   \operatorname{Re}a'_-,\operatorname{Im}a'_-,
   \operatorname{Re}\phi'_-,\operatorname{Im}\phi'_-).
\]

The five equations are the real and imaginary parts of the two endpoint
conditions together with

\[
\operatorname{Im}W=0.
\]

They define a one-dimensional curve.  Each continuation step adds a sixth
pseudo-arclength equation.  The executable starts from independent fixed-$\Im
T$ solutions at $0.10$ and $0.15$, then accepts 70 steps of coordinate length
$0.06$.

Across the 72 recorded points:

- the largest endpoint residual is $3.86\times10^{-13}$;
- the largest $|\operatorname{Im}W|$ is $7.84\times10^{-11}$;
- $\operatorname{Re}W$ increases strictly;
- the maximum normalized gradient-alignment residual is $2.27\times10^{-3}$.

Independent fixed-$\Im T$ solves at $\Im T=0.4,1.0,2.0$ agree with an
interpolation of the pseudo-arclength curve with six-variable Euclidean errors

\[
1.83\times10^{-4},
\quad1.05\times10^{-4},
\quad2.74\times10^{-4}.
\]

The potential and equations have real coefficients, so Schwarz reflection
produces a lower arm.  Direct reintegration at four conjugate points gives a
maximum endpoint/action-conjugation residual below $4\times10^{-13}$.

## 4. Singularity monitoring

The complex variational equations were integrated at six points, including
the $\Im T$ turn and the last recorded point.  The velocity-to-endpoint
Dirichlet block is

\[
B_v=\frac{\partial(a_+,\phi_+)}
          {\partial(a'_-,\phi'_-)}\bigg|_{q_-,T}.
\]

At the turn,

\[
\sigma(B_v)=(4.48490,1.41908),
\]

and at the last point,

\[
\sigma(B_v)=(4.59486,1.17010).
\]

The smallest monitored $|a|$ is larger than $3.56$.  Therefore neither the
fixed-$\Im T$ projection turn nor the bounded endpoint is accompanied by a
homogeneous scale zero or Dirichlet caustic.  The unmonitored continuation can
still encounter either one later, and inhomogeneous fluctuation modes were not
examined.

## 5. The recorded dual branch

Because the saddle and coefficients are real, the dual flow remains on the
real $T$ axis while that branch is analytic.  On the recorded left interval
$0.2\leq T<0.7$,

\[
W_T>0,
\qquad
\frac{dT}{ds}=-W_T<0.
\]

The endpoint Jacobi determinant remains positive and no sampled stationary
point occurs.  Representative values are

| $T$ | $W$ | $W_T$ | $\det B_v$ |
|---:|---:|---:|---:|
| 0.25 | 0.71637736 | 2.62126349 | 0.0622567 |
| 0.35 | 0.96175300 | 2.26583010 | 0.1215703 |
| 0.45 | 1.16538497 | 1.78559883 | 0.1999771 |
| 0.55 | 1.31453328 | 1.17513700 | 0.2969194 |
| 0.68 | 1.40492581 | 0.17548142 | 0.4495443 |

This is the branch used by the bounded intersection diagnostic.

## 6. What was and was not intersected

For each declared full vertical segment

\[
\mathcal C_{\epsilon}^{\rm full}
=\{\epsilon+iN:-2.5\leq N\leq2.5\},
\]

the real dual branch crosses at $N=0$.  Orient $\mathcal C$ by increasing $N$
and the left dual arm outward from the saddle.  Their tangent columns are

\[
\begin{pmatrix}0&-1\\1&0\end{pmatrix},
\qquad
\det=+1.
\]

Thus each of the four **specified, truncated** cycles has one recorded
transverse crossing.  This does not prove that the full global dual cycle has
no other pieces or crossings, that the truncation endpoints lie in admissible
relative-homology sectors, or that this full two-sided object is the desired
cosmological amplitude.

Three contour questions must not be conflated:

1. The Euclidean positive-real $T$ contour overlaps the dual branch and is
   nontransverse.
2. The regulated two-sided vertical cycle has the bounded interior crossings
   calculated here.
3. A positive-lapse half-cycle has $N=0$ as an endpoint, so its contact is not
   an ordinary interior intersection and depends on an endpoint/lateral
   prescription.

Phase 27 fixes the Lorentzian Wick convention

\[
T_E=iN_L,
\]

and demonstrates that the $N_L=0$ fixed-$T$ kernel has a singular raw Van
Vleck factor even though $W(T)$ is regular there.  Its zero-lapse analysis is
the relevant refinement for the positive half-cycle.  The Phase-28 bounded
full-line crossings remain an independent diagnostic and must not be read as
overriding Phase 27's endpoint result.

## 7. Euclidean-continued reduced BFV--BRST calculation

Use the arbitrary-lapse homogeneous constraint frozen by the Euclidean
Phase-24/25 action,

\[
\mathcal H=
-\frac{p_a^2}{24\pi^2a}
+\frac{p_\phi^2}{4\pi^2a^3}
+2\pi^2(3a-a^3V)
=-6\pi^2a\mathcal C.
\]

The extended variables and frozen conventions are

\[
(N,\Pi;c,\bar\rho;\rho,\bar c),
\qquad
\Omega=c\mathcal H+\rho\Pi,
\qquad
\Psi=-N\bar\rho.
\]

The gauge-fixed action is

\[
S_{\rm BFV}=\int_0^1ds\,[
p\dot q-N\mathcal H+\Pi\dot N
+\bar\rho\dot c+\bar c\dot\rho-\bar\rho\rho].
\]

The BRST transformations are

\[
sq^A=c\,\partial_{p_A}\mathcal H,
\quad
sp_A=-c\,\partial_{q^A}\mathcal H,
\quad
sN=\rho,
\quad
s\bar c=-\Pi,
\quad
s\bar\rho=-\mathcal H.
\]

This is not being presented as an undeformed Lorentzian Hamiltonian.  With the
Phase-27 continuation, the corresponding canonical quantities obey

\[
p_L=i p_E,
\qquad
\mathcal H_L(q,ip_E)=-\mathcal H_E(q,p_E).
\]

There is one Abelian Euclidean-continued constraint and
$[\mathcal H,\Pi]=0$, so
$\Omega^2=0$.  The ghost equations give

\[
\rho=\dot c,
\qquad
\bar\rho=-\dot{\bar c},
\]

and the Dirichlet ghost operator is

\[
-\partial_s^2,
\qquad
\lambda_n=(\pi n)^2,
\quad n=1,2,\ldots.
\]

It has no zero mode and, in the zeta scheme on a unit coordinate interval,

\[
\det_{\zeta}(-\partial_s^2)=2.
\]

The number 2 is scheme- and coordinate-normalization-dependent.  It is an
internal check of this reduced gauge-fixing convention, not a physical
one-loop prefactor.

Off shell, $sN=\rho$, so $sT=\int_0^1\rho ds$.  Only after eliminating the
auxiliary ghost momentum with its equation $\rho=\dot c$ does this become

\[
sT=\int_0^1\rho ds=c(1)-c(0)=0
\]

under the Dirichlet ghost endpoint condition.  Hence $T$ survives as a
BRST-invariant global modulus after auxiliary elimination in this reduced
model.  Its negative curvature $W_{TT}<0$ is not a gauge zero mode canceled by
the nonzero Dirichlet ghost determinant.

At the neck

\[
p_a=p_\phi=0,
\qquad a^2V=3,
\]

the constraint vanishes, but

\[
\{a,\mathcal H\}=\{\phi,\mathcal H\}=0,
\qquad
\{p_a,\mathcal H\}=12\pi^2.
\]

Thus $a-a_0=0$ and $\phi-\phi_0=0$ have zero local FP determinant at the
time-symmetric neck; $p_a=0$ is a locally regular extrinsic clock.  This is a
local homogeneous statement, not a complete BFV measure or Gribov analysis.

## 8. Claim boundary

The executable supports only these bounded statements:

- the recorded upper constant-phase arm continues past its $\Im T$ projection
  turn and is aligned with the one-dimensional PL descent flow;
- its conjugate lower arm exists over the tested interval;
- no homogeneous complex Dirichlet caustic or scale zero appears at the
  monitored points;
- four explicitly declared two-sided vertical cycles have one transverse
  crossing with the recorded left dual branch;
- intrinsic neck clocks are singular, the extrinsic $p_a$ clock is locally
  regular, and the chosen reduced Dirichlet ghost normalization does not
  remove $T$ after auxiliary elimination.

It does **not** establish:

- a global intersection coefficient for a complete physical lapse contour;
- a coefficient for the positive-lapse half-cycle or nontransverse Euclidean
  cycle;
- completeness of the saddle set or absence of Stokes jumps;
- the full graviton/scalar/matter/gravitino/ghost determinant;
- a positive WDW/BFV density, trace-class state, Pin lift, soft SUSY spectrum,
  or string embedding.

## 9. String/M-theory completion route (design gate, not computed evidence)

The calculation above does not become a string construction merely by
renaming its two boundaries an orientifold or crosscap.  The most direct
completion route suggested by existing string/SUGRA structures is instead

\[
\boxed{
\text{BFV-reduced seam state}
\longrightarrow
\text{double-three-form }\mathcal N=1\text{ SUGRA}
\longrightarrow
\text{flux-sector selection}
\longrightarrow
F\ne0\text{ and visible soft terms}.}
\]

This route would replace the presently chosen Starobinsky potential and any
ad hoc flux prior by an action in which flux parameters arise as four-form
integration constants.  Schematically, the flux superpotential has the form

\[
W=e_A\mathcal Z^A+m^A\mathcal G_A(\mathcal Z),
\qquad (e_A,m^A)\in\Gamma_{\rm flux}.
\]

The three-form variational boundary term must be included before evaluating a
Euclidean saddle; otherwise even the on-shell scalar-potential sign can be
misidentified.  A kappa-symmetric charged membrane would additionally supply
physical jumps of the electric/magnetic flux data.  Without such a transition
operator, the electric/magnetic data are constant on each source-free local-EFT
region.  Whether a global path integral sums those sectors, and with which
measure, is additional input that the local action does not provide.

If a normalized seam state selected a sector with nonzero auxiliary order
parameters, the phenomenological chain to be tested would be

\[
\text{seam selects }n_*
\longrightarrow F^I(n_*)\ne0
\longrightarrow
(M_{1/2},m_{\tilde f}^2,A_{ijk}).
\]

Flux-induced soft terms are known in concrete Type-IIB D-brane settings, but
none has been computed for this seam.  This is the viable way to evade the
Phase-18 free instantaneous-seam result: the seam would select a persistent
bulk flux vacuum rather than directly kick a free pole mass.
A (D^a\ne0) branch would require additional vector-multiplet/gauging data;
it is not supplied by the cited three-form construction alone.

Two further distinctions are mandatory:

- the BFV ghost here gauges spacetime time reparametrization, whereas a
  worldsheet BRST charge gauges worldsheet diffeomorphism/Weyl symmetry;
- an orientifold crosscap is a worldsheet quotient and is not a CPT temporal
  seam.  Crosscap sewing and tadpole cancellation are useful consistency
  templates, not an identification of the two objects.

Likewise, misaligned supersymmetry can support ultraviolet finiteness without
level-by-level superpartners only after constructing a complete tachyon-free,
modular-invariant string spectrum.  It cannot be imported into the present
finite doubled EFT as a cancellation theorem.

This completion programme has sharp failure gates: the physical lapse cycle
may have zero intersection with the connected saddle; the BFV/BV Ward
identities or quantum master equation may fail; tadpoles, flux quantization or
Pin/anomaly conditions may be inconsistent; no normalizable sector measure
may exist; or the selected flux may give $F=D=0$ or no acceptable soft
spectrum.  Moreover, replacing the benchmark action by an actual compactified
SUGRA action requires rerunning Phases 24--28 from the beginning; their saddle
need not survive.

## 10. Reproduction

Run:

```bash
uv run --locked python3 \
  cpt_temporal_folded_susy/phase28_thimble_bfv_intersection.py
```

The executable emits 10 exact checks, 9 numerical checks, and one
machine-readable `PHASE28_RESULT`.  It writes no files.

## Primary references and their bounded role

- [Halliwell and Louko, *Steepest-descent contours in the path-integral approach to quantum cosmology. I*](https://doi.org/10.1103/PhysRevD.39.2206) — lapse contours, saddle decompositions, and endpoint dependence in minisuperspace.
- [Feldbrugge, Lehners, and Turok, *Lorentzian quantum cosmology*](https://arxiv.org/abs/1703.02076) — Picard--Lefschetz flows and dual-cycle intersection numbers for lapse integrals.
- [Batalin and Vilkovisky, *Gauge algebra and quantization*](https://doi.org/10.1016/0370-2693(81)90205-7) — BV gauge-algebra framework.
- [Fradkin and Vilkovisky, *Quantization of relativistic systems with constraints*](https://doi.org/10.1016/0370-2693(75)90448-7) — Hamiltonian constrained path integrals and gauge fixing.
- [Halliwell, *Derivation of the Wheeler--DeWitt equation from a path integral for minisuperspace models*](https://doi.org/10.1103/PhysRevD.38.2468) — lapse reduction, the Wheeler--DeWitt equation, and measure/operator ordering.
- [Gibbons, Hawking, and Perry, *Path integrals and the indefiniteness of the gravitational action*](https://doi.org/10.1016/0550-3213(78)90161-X) — the gravitational conformal-contour obstruction that this homogeneous lapse calculation does not remove.
- [Farakos, Lanza, Martucci, and Sorokin, *Three-forms in Supergravity and Flux Compactifications*](https://arxiv.org/abs/1706.09422) — double-three-form SUGRA and flux parameters as four-form expectation values; it does not derive this seam.
- [Bandos et al., *Three-forms, dualities and membranes in four-dimensional supergravity*](https://arxiv.org/abs/1803.01405) — duality-covariant three-form multiplets and charged kappa-symmetric membranes; no membrane is present in the Phase-28 executable.
- [Witten, *On Flux Quantization in M-Theory and the Effective Action*](https://arxiv.org/abs/hep-th/9609122) — the gravitationally shifted flux lattice that an M-theory embedding must respect.
- [Cámara, Ibáñez, and Uranga, *Flux-induced SUSY-breaking soft terms*](https://arxiv.org/abs/hep-th/0311241) — explicit D-brane soft terms from background fluxes; cited as the downstream spectrum template, not as evidence for seam selection.
- [Dienes, *Modular Invariance, Finiteness, and Misaligned Supersymmetry*](https://arxiv.org/abs/hep-th/9402006) — full-string ultraviolet cancellations without level-by-level spacetime SUSY, conditional on the complete modular-invariant spectrum.
- [Kiermaier, Okawa, and Zwiebach, *The boundary state from open string fields*](https://arxiv.org/abs/0810.1737) — a BRST-cohomological boundary-state template; its worldsheet BRST charge is distinct from the BFV charge used here.
- [Moosavian, Sen, and Verma, *Superstring Field Theory with Open and Closed Strings*](https://arxiv.org/abs/1907.10632) — the quantum BV/master-equation completion gate for an actual string-field construction.
