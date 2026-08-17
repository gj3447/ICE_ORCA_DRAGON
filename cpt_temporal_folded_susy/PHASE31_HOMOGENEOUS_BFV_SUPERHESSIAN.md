# Phase 31 — homogeneous finite-cutoff BFV super-Hessian gate

Here **super-Hessian** means the $\mathbb Z_2$-graded BFV gauge/ghost
quadratic system.  It is not a supersymmetry or supergravity Hessian.

## Outcome

The Phase-30 configuration calculation has now been lifted back to canonical
phase space and completed by the **nonzero homogeneous** proper-time-gauge BFV
quartets.  At every recorded odd and even cutoff, exact momentum elimination
reproduces the independently assembled configuration Hessian, while the
unreduced proper-time-gauge canonical block in

\[
(q_{\rm int},p,T)
\]

has an even number of negative directions and positive determinant sign:

\[
\boxed{
n_-(B_{pp})=m,
\qquad
n_-(B_{qT\mid p})=m,
\qquad
n_-(B_{q,p,T})=2m,
\qquad
\operatorname{sgn}\det B_{q,p,T}=+1 .
}
\]

This is useful, but it does **not** derive the absolute phase of the
configuration-space determinant.  Integrating the momentum block requires a
contour orientation of its own.  The stable canonical sign therefore shows
where the Phase-30 odd/even split entered; it does not by itself solve the
continuum determinant-line or global Picard--Lefschetz problem.

For each nonzero gauge mode the coupled bosonic block and ordered first-order
ghost block give

\[
\det
\begin{pmatrix}
A&C&0\\
C^T&0&-d\\
0&-d&0
\end{pmatrix}
=-d^2\det A,
\qquad
\operatorname{Pf}F_{(c,\bar c,\rho,\bar\rho)}=d^2.
\]

The first identity is independent of the actual lapse coupling $C$.  Hence at
a fixed hybrid regulator the nonzero quartet factors are background-independent and
drop out of a benchmark/reference ratio.  No absolute bosonic Gaussian phase
or ghost normalization is assigned.  Indeed, the bare full **bosonic** BFV
block gains $m-1$ additional negative directions and its cutoff sign still
alternates:

\[
\boxed{
n_-(B_{\rm BFV,bos})=3m-1,
\qquad
\operatorname{sgn}\det B_{\rm BFV,bos}=(-1)^{m-1}.
}
\]

The bounded clock diagnostic is also sharper.  On this real saddle,
$p_a$ has a strictly positive local Faddeev--Popov bracket and is monotone.
The intrinsic $a$ and $\phi$ clocks both stop at the reflection neck.  But
using $p_a$ at the endpoints would change the fixed-$(a,\phi)$ boundary
polarization; the nonzero boundary Legendre term is $300.8819681$.  Therefore
this scan does not turn the existing fixed-$q$ seam kernel into a global
$p_a$-clock amplitude.

The executable passes 9 exact and 11 numerical checks.  Its result is a
finite-cutoff homogeneous quadratic BFV completion gate, not a physical seam
state, a probability, a full SUGRA determinant, or an absolute thimble
coefficient.

## 1. Canonical lift of the Phase-30 action

The frozen potential and Euclidean Hamiltonian constraint are

\[
V(\phi)=\frac34
\left(1-e^{-\sqrt{2/3}\phi}\right)^2,
\]

\[
\boxed{
H_E
=-\frac{p_a^2}{24\pi^2a}
+\frac{p_\phi^2}{4\pi^2a^3}
+2\pi^2\left(3a-a^3V\right).
}
\]

On a unit parameter interval divided into $m$ elements, one midpoint element
is

\[
S_e
=p_{a,e}\Delta a_e+p_{\phi,e}\Delta\phi_e
-hT H_E(q_{e+1/2},p_e),
\qquad h=\frac1m.
\]

The momentum equations are algebraic:

\[
p_{a,e}=-\frac{12\pi^2a_{e+1/2}\Delta a_e}{hT},
\qquad
p_{\phi,e}=\frac{2\pi^2a_{e+1/2}^3\Delta\phi_e}{hT}.
\]

Substitution gives exactly

\[
S_e^{\rm conf}
=2\pi^2\left[
\frac{-6a_{e+1/2}(\Delta a_e)^2
+a_{e+1/2}^3(\Delta\phi_e)^2}{2Th}
+Th\left(-3a_{e+1/2}+a_{e+1/2}^3V\right)
\right],
\]

which is the Phase-30 midpoint element.  For a quadratic block

\[
B_{\rm ph}=\begin{pmatrix}B_{xx}&B_{xp}\\B_{px}&B_{pp}\end{pmatrix},
\qquad x=(q_{\rm int},T),
\]

Gaussian momentum elimination gives

\[
B_{\rm conf}=B_{xx}-B_{xp}B_{pp}^{-1}B_{px},
\qquad
\det B_{\rm ph}=\det B_{pp}\det B_{\rm conf}.
\]

The symbolic element calculation proves the Legendre identity.  The full
independently assembled lattice matrices agree with relative operator
residual at most $1.70\times10^{-16}$ over the recorded cutoffs.

The numerical background is still the continuum Phase-25 solution sampled on
the lattice; it is not promoted here to a theorem about a fully gauge-exact
finite-lattice discretization.  Its maximum element-midpoint constraint
residual is nonzero and decreases as

\[
0.122087,
0.0377040,
0.0305347,
0.0252422,
0.00763628,
0.00190923
\]

for $m=(5,9,10,11,20,40)$.  The products
$m^2\max_e|H_{E,e}|$ are constant to about one part in $10^3$.  This
$O(m^{-2})$ convergence is a useful Galerkin control, but it explicitly shows
that no new exact finite-lattice critical point was solved.

## 2. Homogeneous $\alpha=0$ BFV sector

Introduce the lapse momentum $\Pi$ and ghost pairs so that, for the Abelian
homogeneous constraint,

\[
\Omega=cH_E+\rho\Pi,
\qquad
\{H_E,\Pi\}=0,
\qquad
\{\Omega,\Omega\}=0.
\]

The proper-time gauge fermion used here is the $\alpha=0$ member

\[
\Psi_0=-N\bar\rho.
\]

With the sign convention frozen in the executable, the gauge-fixed
first-order action is represented schematically by

\[
I_{\Psi_0}=\int ds\,[
p\dot q-NH_E+\Pi\dot N
+\bar\rho\dot c+\bar c\dot\rho-\bar\rho\rho].
\]

The frozen mode boundary conditions are

\[
(c,\bar c,\Pi):\ \text{endpoint-vanishing sine modes},
\qquad
(N,\rho,\bar\rho):\ \text{cosine modes}.
\]

Endpoint-vanishing reparametrizations therefore use sine modes.  Their lapse
partners are the zero-average cosine modes

\[
n_k^{\rm gauge}(s)=\sqrt2\sin(k\pi s),
\qquad
n_k(s)=\sqrt2\cos(k\pi s),
\qquad d_k=k\pi,
\qquad k=1,\ldots,m-1.
\]

Here $\partial_s n_k^{\rm gauge}=d_kn_k$ is the **continuum** spectral
identity.  The gauge harmonics are truncated at $k=m-1$ and projected against
the separate $(q,p)$ midpoint discretization by midpoint quadrature.  This is
a hybrid continuum-spectral regulator: $d_k=k\pi$ is not an exact derivative
eigenvalue of the midpoint lattice.

Thus the constant mode is not placed in a ghost quartet:

\[
\int_0^1n_k(s)\,ds=0,
\qquad
N(s)=T+\sum_{k\ge1}n_k(s).
\]

The proper time $T$ remains the global lapse modulus whose negative Schur
curvature was isolated in Phase 30.

The actual mixed matrix $C$ is assembled from

\[
-\int ds\,n_k(s)\,\delta H_E.
\]

It is not set to zero: its spectral norm ranges from $47.05$ to $107.92$ in
the recorded sample.  Nevertheless, for one mode the exact bosonic block
identity is

\[
\det
\begin{pmatrix}
A&C&0\\
C^T&0&-d\\
0&-d&0
\end{pmatrix}
=-d^2\det A.
\]

For ghost order $(c,\bar c,\rho,\bar\rho)$,

\[
F_d=
\begin{pmatrix}
0&0&0&-d\\
0&0&-d&0\\
0&d&0&1\\
d&0&-1&0
\end{pmatrix},
\]

and

\[
\operatorname{Pf}F_d=d^2,
\qquad
\det F_d=d^4.
\]

These identities justify only the following relative statement: with the
same hybrid regulator and mode conventions in numerator and denominator, all
$d_k$-dependent nonzero quartet normalizations are identical and divide out.
They do not say that the bosonic Gaussian and fermionic Pfaffian multiply to
one inside a single absolute amplitude.  The $(n_k,\Pi_k)$ bosonic contour,
its square-root phase, and the absolute Pfaffian orientation are all left
unassigned.  This endpoint-sensitive distinction is consistent with the BFV analysis of
[García, Vergara, and Urrutia](https://arxiv.org/abs/hep-th/9511092).

The endpoint-vanishing $c$, $\bar c$, and $\Pi$ ledgers have no $k=0$ mode.
The algebraic $k=0$ $\rho$--$\bar\rho$ pair is eliminated and normalized to a
background-independent unit only in the same-hybrid-regulator relative ratio.  This
is a convention of the reduced ledger, not an absolute zero-mode measure.
The only retained lapse $k=0$ variable is the global modulus $T$.

## 3. Recorded cutoff inertia

The unreduced proper-time-gauge canonical block includes all interior
$(a,\phi)$ values, both element momenta, and the single global $T$.  It is not
a constraint-reduced physical phase space.  The full bosonic BFV block
additionally includes $(n_k,\Pi_k)$ for every $k=1,\ldots,m-1$.

| segments $m$ | $n_-(B_{pp})$ | $n_-(B_{qT\mid p})$ | $n_-(B_{q,p,T})$ | sign canonical | $n_-(B_{\rm BFV,bos})$ | sign BFV bosonic |
|---:|---:|---:|---:|:---:|---:|:---:|
| 5  | 5  | 5  | 10 | $+$ | 14  | $+$ |
| 9  | 9  | 9  | 18 | $+$ | 26  | $+$ |
| 10 | 10 | 10 | 20 | $+$ | 29  | $-$ |
| 11 | 11 | 11 | 22 | $+$ | 32  | $+$ |
| 20 | 20 | 20 | 40 | $+$ | 59  | $-$ |
| 40 | 40 | 40 | 80 | $+$ | 119 | $-$ |

The largest absolute log-determinant factorization residual is
$1.17\times10^{-11}$.  No eigenvalue is classified as zero at the recorded
finite cutoffs.  At $m=40$, the smallest absolute eigenvalue divided by the
spectral radius is $4.03\times10^{-7}$ in the proper-time-gauge canonical
block and
$1.58\times10^{-7}$ in the full bosonic BFV block.  This is a bounded numerical
statement, not a uniform continuum spectral gap.

The global-lapse Schur sequence is

\[
-8.5127778,
-8.7960194,
-8.8201408,
-8.8379976,
-8.8973668,
-8.9166974,
\]

for $m=(5,9,10,11,20,40)$, approaching the independent Phase-30 result

\[
W_{TT}=-8.92314303834.
\]

The field--lapse fibered contour from Phase 30 is therefore still required.
The present BFV algebra does not make the negative global modulus disappear.

## 4. What the parity result does and does not say

Phase 30 found that its fixed-$T$ configuration-field determinant had an
odd/even lattice sign.  Phase 31 finds

\[
\operatorname{sgn}\det B_{pp}=(-1)^m,
\qquad
\operatorname{sgn}\det B_{qT\mid p}=(-1)^m,
\]

so their product in canonical phase space is positive.  This locates the
split between momentum integration and the configuration Schur complement.
It does not determine the Gaussian contour phase associated with either
factor.  Adding the bare gauge pair contributes a further
$(-1)^{m-1}$, while the positive algebraic ghost Pfaffian does not by itself
select the missing bosonic square-root branch.

Consequently neither the stable canonical sign nor the relative quartet
cancellation fixes:

- a continuum determinant-line orientation;
- the conformal/lapse contour through $N=0$;
- an integer upward-thimble intersection coefficient;
- an absolute quantum seam weight.

Those remain global contour and measure questions.  A finite-dimensional
Hessian cannot replace the relative-homology calculation described by
[Witten](https://arxiv.org/abs/1001.2933), and the gravitational conformal
rotation still carries the general issue identified by
[Gibbons, Hawking, and Perry](https://doi.org/10.1016/0550-3213(78)90161-X).

## 5. Local extrinsic-clock diagnostic

For $\chi=p_a-f(s)$, the local Faddeev--Popov bracket is

\[
\boxed{
\{p_a,H_E\}
=-\frac{p_a^2}{24\pi^2a^2}
+\frac{3p_\phi^2}{4\pi^2a^4}
-6\pi^2(1-a^2V).
}
\]

Using

\[
p_a=-12\pi^2a\dot a,
\qquad
p_\phi=2\pi^2a^3\dot\phi
\]

and the Hamiltonian constraint gives

\[
\{p_a,H_E\}
=2\pi^2\left[-6+a^2\dot\phi^2+4a^2V\right].
\]

A 1001-point scan on the recorded real saddle finds

\[
118.4352528131
\le \{p_a,H_E\}\le
124.6409311427,
\]

\[
p_a(0)=-42.1781006382,
\qquad
p_a(T)=+42.1781006382,
\]

and every recorded step in $p_a$ is positive.  At the reflection neck,

\[
\{p_a,H_E\}=12\pi^2,
\qquad
\{a,H_E\}=\dot a\simeq0,
\qquad
\{\phi,H_E\}=\dot\phi\simeq0.
\]

Thus $p_a$ is a good **local bulk** clock on this particular real branch,
whereas $a$ and $\phi$ fail at the neck.  This is not a global gauge theorem.
For the fixed-$q$ kernel, endpoint-preserving gauge parameters vanish at the
boundaries.  Imposing a $p_a$ clock there instead changes the boundary data,
with the recorded Legendre term

\[
[ap_a]_-^+=300.8819681096.
\]

One must explicitly transform to a mixed $(p_a,\phi)$ polarization before
using that clock to define an amplitude.  Multiplying this boundary term into
the Phase-30 fixed-$(a,\phi)$ kernel would mix two different kernels.

## 6. Reproduction and checks

Run either entry point:

```bash
uv run --locked python3 cpt_temporal_folded_susy/phase31_homogeneous_bfv_superhessian.py
./ice run phase31_homogeneous_bfv_superhessian
```

Both print one `PHASE31_RESULT=...` JSON record.  The checks are:

- 9 exact symbolic checks: canonical stationary momenta, exact Legendre
  elimination, Schur determinant, Abelian BFV nilpotence, bosonic quartet
  determinant, ghost Pfaffian, the continuum sine/cosine derivative pair, global-mode
  separation, and the $p_a$ bracket identity;
- 11 numerical checks: the frozen saddle, sampled $O(m^{-2})$ constraint
  convergence, sampled momenta, independent phase/configuration Hessians,
  proper-time-gauge canonical inertia, full bosonic BFV inertia,
  coupled determinant factorization, relative quartet cancellation, absence
  of recorded finite-cutoff zero modes, global-$T$ Schur convergence, and the
  bounded $p_a$ clock scan.

## 7. Scope and next gate

Computed here:

- the unreduced proper-time-gauge canonical midpoint Hessian in $(q,p,T)$;
- exact and numerical momentum Schur reduction;
- every nonzero homogeneous $\alpha=0$ lapse--multiplier mode and its
  first-order ghost quartet at the recorded cutoffs;
- relative same-hybrid-regulator quartet cancellation;
- finite-cutoff inertia and a bounded local $p_a$ bracket scan.

Not computed here:

- an absolute BFV measure, square-root branch, or determinant-line phase;
- a global nonlinear lapse contour or Picard--Lefschetz intersection number;
- gauge-parameter independence away from $\alpha=0$;
- a global $p_a$ clock or the mixed-polarization kernel;
- inhomogeneous scalar, tensor, fermion, gravitino, and ghost harmonics;
- a WDW density matrix, Pin lift, flux distribution, SUSY-breaking spectrum,
  or physical probability.

The next meaningful gate is therefore not another bare sign count.  It is a
regulated global lapse-contour orientation together with an inhomogeneous
$S^3$ relative BFV superdeterminant.  Only after both are controlled can this
homogeneous connected saddle be assigned a quantum seam weight.

## 8. Primary-source framing

These sources frame the formal issues; none proves the repository-specific
finite lattice or its physical relevance:

- [Fradkin and Vilkovisky](https://doi.org/10.1016/0370-2693(75)90448-7)
  for constrained phase-space quantization;
- [Halliwell, *Physical Review D* 38, 2468](https://doi.org/10.1103/PhysRevD.38.2468)
  for lapse/path-integral treatment in minisuperspace;
- [García, Vergara, and Urrutia](https://arxiv.org/abs/hep-th/9511092) for
  endpoint-sensitive BFV boundary conditions;
- [Gratton and Turok](https://arxiv.org/abs/hep-th/0008235) for the fact that
  gravitational negative-mode statements depend on constraint reduction and
  variable choice;
- [Rogers](https://arxiv.org/abs/hep-th/9902133) for gauge-fermion admissibility
  and Gribov-type caveats;
- [Witten](https://arxiv.org/abs/1001.2933) for global relative homology and
  Picard--Lefschetz thimbles.
