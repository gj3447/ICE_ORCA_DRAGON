# Starobinsky Morse scalar fiber — positivity obstruction for one declared ordering

## Status and question

This is a same-model, fixed-fiber spectral observation for one explicitly
declared quantization.  It is **not** a new Starobinsky--Morse reduction:
McGuigan already notes the Morse/SUSYQM connection and writes an adiabatic
Morse wavefunction near the potential bottom.  The narrow additional question
here is whether the specified fixed-\(a\), Laplace--Beltrami fiber can be
nonnegative for the direct square-root route:

> If the raw Lorentzian homogeneous Starobinsky constraint is quantized with
> the Laplace--Beltrami ordering below, can its fixed-\(a\) scalar operator
> \(D_a\) be used as a nonnegative operator in the direct
> \(\alpha=\log a\) positive-frequency construction?

The answer is no.  For every \(a>0\), the specified fiber operator has negative
spectrum.  Thus a construction requiring the ordinary real square root
\(\sqrt{D_a}\) on the whole fiber is unavailable in this ordering.

This is a **supporting, scoped quantum-source constraint**.  It is not a
construction of the original path-integral source, a physical Hilbert space, a
global Wheeler--DeWitt spectral theorem, a group-averaging result, or a Gate-1
resolution.

The named consumer is the quantum-input side of
`open:gate1-starobinsky-exact-gauge-preserving-element-source`, alongside the
explicitly conditional Phase-23 positive-operator bridge. The pre-run planner
returned `CURRENT_BLOCKER_CANDIDATE` for the source-audit question. Direct
review retains this calculation as supporting: it changes a particular
quantum positivity premise, not an original joint relative class or the G1
intersection vector. The prerequisite chain to G2--G5 and full-theory review
therefore remains open.

## 1. Raw constraint and the declared ordering

The common same-Starobinsky classical input is the raw Lorentzian constraint

\[
 H_L=-\frac{p_a^2}{24\pi^2a}
      +\frac{p_\phi^2}{4\pi^2a^3}
      -6\pi^2a+2\pi^2a^3V(\phi),
 \qquad
 V(\phi)=\frac34\left(1-e^{-\beta\phi}\right)^2,
 \quad \beta^2=\frac23 .
\tag{1}
\]

It is recorded in the exact same-model BFV chart, including the Lorentzian
sign convention, in [the chart's input](STAROBINSKY_POLYNOMIAL_BFV_CHART.md).
The present note makes a **new ordering choice**, rather than importing a
quantization from that classical chart.  Let

\[
 G_{AB}\,dq^Adq^B=-6a\,da^2+a^3d\phi^2,
 \qquad |G|^{1/2}=\sqrt6\,a^2,
\tag{2}
\]

and define, at \(\hbar=1\),

\[
 \widehat H_L=-\frac{1}{4\pi^2}\Delta_G-6\pi^2a+2\pi^2a^3V(\phi).
\tag{3}
\]

The positive multiplier \(24\pi^2a^3\) is used here only to rewrite the
*differential equation* on \(a>0\).  It is not asserted to preserve a quantum
constraint, domain, rigging-map normalization, or physical inner product.
That distinction is material: the repository's (V=0) densitized model makes
exactly this warning for a different rescaling and ordering
([its source-and-convention boundary](GATE1_V0_DENSITIZED_QUANTUM_COSMOLOGY_DERIVATION.md#1-source-and-convention-boundary)).

Writing \(\alpha=\log a\), direct evaluation of (2) gives

\[
 24\pi^2a^3\!\left[-\frac{1}{4\pi^2}\Delta_G\right]
 =a^2\partial_a^2+a\partial_a-6\partial_\phi^2
 =\partial_\alpha^2-6\partial_\phi^2.
\tag{4}
\]

Consequently the ordered equation is

\[
 \left(\partial_\alpha^2+D_a\right)\Psi=0,
\tag{5}
\]

with the fixed-\(a\) scalar fiber expression

\[
 D_a=-6\partial_\phi^2
 +36\pi^4a^6\left(1-e^{-\beta\phi}\right)^2
 -144\pi^4a^4.
\tag{6}
\]

For this limited fiber question, take the natural scalar Hilbert space
\(L^2(\mathbb R,d\phi)\) and the self-adjoint operator associated with the
closed, lower-bounded quadratic form of (6), equivalently the Friedrichs
realization of its restriction to \(C_c^\infty(\mathbb R)\).  The potential is
real, locally bounded, and bounded below for fixed \(a>0\), so this specifies
the one-dimensional operator used below.  This does **not** specify a domain
or self-adjoint realization of the full two-variable Wheeler--DeWitt operator.

## 2. Exact Morse identification

Set

\[
 \lambda=3\pi^2a^3,
 \qquad x=\beta\phi,
 \qquad z=2\lambda e^{-x}.
\tag{7}
\]

The coordinate rescaling gives the standard unit-kinetic Morse operator

\[
 D_a=4A_\lambda-144\pi^4a^4,
 \qquad A_\lambda=-\partial_x^2+\lambda^2(1-e^{-x})^2,
\tag{8}
\]

whose essential spectrum begins at \(\lambda^2\). Therefore
\(\sigma_{\rm ess}(D_a)=[36\pi^4a^4(a^2-4),\infty)\).
Its discrete energies, after restoring the constant in (6), are

\[
 E_n(D_a)=36\pi^4a^6
 -4\left(\lambda-n-\frac12\right)^2
 -144\pi^4a^4,
 \qquad n\in\mathbb N_0,
 \quad n<\lambda-\frac12 .
\tag{9}
\]

The strict inequality is the normalizability condition. The substitution
\(\psi=z^{\lambda-n-1/2}e^{-z/2}f(z)\) reduces the eigen-equation to the
associated Laguerre equation. Polynomial termination gives the listed integers;
the threshold exponent zero is not square integrable in \(dz/z\).
For example, when \(\lambda>1/2\), a normalized ground state is

\[
 \psi_0(\phi)=N z^{\lambda-1/2}e^{-z/2},
 \qquad
 N^2=\frac{\beta}{\Gamma(2\lambda-1)}.
\tag{10}
\]

Indeed \(d\phi=-dz/(\beta z)\), so (10) has unit \(L^2(d\phi)\) norm.  The
Morse formula and this normalizability condition are standard exact spectral
facts; the present use only substitutes the parameters fixed by (1).

## 3. A negative spectral value for every scale factor

The following proof deliberately does not require a complete spectral
classification of the full Wheeler--DeWitt problem.

### 3.1 \(0<a<2\): a compact trial-function witness

At \(\phi\to+\infty\), the potential in (6) tends to

\[
 36\pi^4a^6-144\pi^4a^4=-\Delta(a),
 \qquad
 \Delta(a):=36\pi^4a^4(4-a^2)>0 .
\tag{11}
\]

Thus the essential threshold is negative.  A direct compact witness also
makes the conclusion independent of invoking the complete Morse spectrum.
Choose

\[
 L=\sqrt{\frac{12\pi^2}{\Delta(a)}}
\tag{12}
\]

and an \(H^1\) sine packet supported on \([1,1+L]\), normalized in
\(L^2(d\phi)\).  On this support the Morse correction
\(36\pi^4a^6[(1-e^{-\beta\phi})^2-1]\) is nonpositive.  The packet kinetic
expectation is \(6\pi^2/L^2=\Delta(a)/2\), and hence

\[
 \langle D_a\rangle
 \le \frac{6\pi^2}{L^2}-\Delta(a)
 =-\frac{\Delta(a)}2<0.
\tag{13}
\]

This is enough to exclude nonnegativity.  Equivalently, (11) identifies the
negative essential threshold.

### 3.2 \(a\ge2\): an exact normalizable ground state

For \(a\ge2\), \(\lambda=3\pi^2a^3>1/2\), so the \(n=0\) state (10) exists.
Equation (9) simplifies to

\[
 E_0(D_a)
 =-144\pi^4a^4+12\pi^2a^3-1
 =12\pi^2a^3(1-12\pi^2a)-1<0.
\tag{14}
\]

Together, (13) and (14) prove

\[
 \boxed{\text{For every }a>0,\quad D_a\not\ge0
 \text{ on the declared scalar fiber.}}
\tag{15}
\]

## 4. Exact consequence and its boundary

Equation (15) closes only this direct route:

\[
 \text{raw }H_L+\text{LB ordering}+\text{fixed-}a\text{ fiber}
 +\alpha\text{-clock}+\sqrt{D_a}
 \quad\not\Longrightarrow\quad
 \text{a real all-fiber positive-frequency generator}.
\tag{16}
\]

It is relevant to the repository's Phase-23 bridge because that phase defines
\(A=\sqrt{\hat h}\) and \(B_L=e^{-LA}\) only after selecting a different,
compact positive operator \(\hat h=-\partial_q^2+\mu^2\).  It explicitly
labels that bridge, regulator, and positive-frequency orientation as supplied
inputs rather than Starobinsky-cap outputs
([Phase 23, sections 2--4](PHASE23_HOMOGENEOUS_MINISUPERSPACE_DENSITY.md#2-compact-positive-frequency-control)).
The result here says that this particular direct reuse with \(h=D_a\) fails.
It does not invalidate that compact control.

Mostafazadeh's §7 uses a reference \(\alpha_0\) for which
\(D(\alpha_0)>0\); it does not require positivity at all times. Equation (15)
shows that even one such reference fiber is unavailable for this operator.
His broader §3 discussion explicitly treats non-positive operators: it
discusses \(|D|\) when zero is outside the spectrum, and a separately chosen
positive \(D'\) for a nontrivial null space. Those qualifications matter here:
zero lies in the essential spectrum for \(a\le2\). No replacement operator or
physical inner product is constructed in this audit. It does not refute the
general framework or every Hilbert-space construction, clock, or inner product.

```mermaid
flowchart LR
  H[raw Starobinsky H_L] --> O[declared LB ordering]
  O --> F[fixed-a Morse fiber D_a]
  F --> N[negative spectral witness]
  N --> X[direct sqrt(D_a) frequency route closed]
  X -.does not decide.-> G1[original joint source/cycle remains open]
```

In particular, this note does **not** establish any of the following:

- self-adjointness, spectrum, or a direct-integral decomposition of the full
  \((\alpha,\phi)\) Wheeler--DeWitt operator;
- a choice of physical scale \(a\), a scale-selection invariant, or a physical
  clock;
- equivalence or inequivalence of other factor orderings, lapse rescalings,
  densitizations, or boundary domains;
- a rigging map, positive trace-class state, BFV boundary condition, lapse or
  field contour, relative cycle, or signed global intersection;
- a refutation of Mostafazadeh's general Hilbert-space framework or of every
  positive-\(D'\) construction.

It therefore remains supporting evidence for the open same-model source and
state questions, rather than a physics discovery or a change to the Gate-1
global-cycle status.

## 5. Pending bounded-run record

The companion bounded runner is responsible for pinning its own input, source
hash, environment, exact checks, and actual output.  Insert the actual result
identifier, command, runner hash, result SHA-256, and check summary here only
after that run has completed.

## References and limited roles

Source discovery used
`./ice literature search "Morse potential Starobinsky Wheeler DeWitt positive Hilbert space" --json`
at `2026-09-06T13:53:59.119Z`, followed by primary-paper reads. Its OpenAlex
hit for McGuigan led to the explicit prior connection below. Search metadata
are not evidence of novelty; no claim of a new physical discovery is made.

- P. M. Morse, [“Diatomic molecules according to the wave mechanics. II.
  Vibrational levels”](https://doi.org/10.1103/PhysRev.34.57), *Physical
  Review* **34** (1929) 57.  Historical source of the exactly solvable Morse
  potential; it does not provide this cosmological ordering or source.
- J. Apanavicius, Y. Feng, Y. Flores, M. Hassan, and M. McGuigan,
  [“Morse Potential on a Quantum Computer for Molecules and Supersymmetric
  Quantum Mechanics,” §2](https://arxiv.org/pdf/2102.05102).  Used only as a
  convenient modern presentation of the Morse ladder, exact bound-state
  energies, and normalizability structure; no quantum-computing result is used.
- M. McGuigan, [“Quantum Cosmology and Black Hole Interiors in
  Nonsupersymmetric String Theory and Canonical Gravity,” §5,
  pp. 22--23](https://arxiv.org/pdf/2309.15021).  This is the prior direct
  Starobinsky--Morse/SUSYQM connection: it treats (a) adiabatically near the
  potential bottom and gives an approximate Morse wavefunction in its (5.16).
  The paper also states that no exact minisuperspace WDW solution for the
  Starobinsky potential is then available.  It is not used here for a kinetic
  normalization, operator domain, or the all-\(a\) fiber positivity result.
- A. Mostafazadeh, [“Quantum Mechanics of Klein--Gordon-Type Fields and
  Quantum Cosmology”](https://arxiv.org/abs/gr-qc/0306003), especially §§3 and
  7.  Used to distinguish a positive-\(D\) Klein--Gordon construction from
  more general Hilbert-space choices; it neither selects this model's ordering
  nor its path-integral source.
- [Phase 23](PHASE23_HOMOGENEOUS_MINISUPERSPACE_DENSITY.md) is the local
  repository comparison for a separately supplied positive compact bridge.
