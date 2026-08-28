# Gate 1 V0 quantum-cosmology formula, philosophy, and ontology map

## Status and purpose

This document is the human-readable map for the repository-local ontology of
the selected closed-FRW \(V=0\) quantum-cosmology calculation. It joins three
layers without identifying them:

1. exact or numerical facts already recorded by executable evidence;
2. philosophical interpretation that carries no evidential polarity by itself;
3. open research directions with explicit prerequisites and success/failure
   discriminators.

The result is a computational workbench record, not a quantum-gravity, physics,
or TOE promotion. Gate 1 remains `OPEN_PARTIAL_PROGRESS`, global promotion is
`PROHIBITED`, and every direction below has `automatic_next=null`.

## 한눈에 보는 결론

- **수학적으로 확인된 것:** 선택한 양의 densitization과 ordering 안에서는
  Fourier--KL 변환, self-adjoint multiplier domain, \(p>0\) RAQ measure,
  \(p=0\) cutoff 경계, full-real-\(p\) regular-shell 두-가지 완성, 국소 BFV Ward
  항등식까지 정확히 연결된다.
- **철학적 의미:** 정확히 풀렸다는 말은 “선택한 모형 안에서 정확하다”는 뜻이다.
  물리적 측도, 경계조건, ghost determinant는 부수 장식이 아니라 양자이론을
  구성하는 데이터다.
- **부정적 결과의 의미:** 현재 KILL은 잘못된 지름길만 제거한다. 양자우주론이나
  양자중력 전체가 틀렸다는 결론은 아니다.
- **다음 연결 방향:** standard full-\(p\) 완성은 scoped `KEEP`으로 닫혔다. 그 뒤
  raw \(C\leftrightarrow H\) domain 감사, microlocal/exact endpoint, absolute BFV,
  고전 \(S^3\) closure, quantum anomaly, relational/BO/decoherence, 관측 likelihood를
  서로 독립된 작업 단위로 연결한다.
- **현재 경계:** 마지막 두 단계가 완성되기 전에는 이 결과를 양자중력 설명이나
  관측 가능한 물리 주장으로 승격하지 않는다.

## 1. Mathematical formula ledger

### 1.1 Classical variables and raw constraint

Use

\[
Q=2\log a,
\qquad
P=\frac{ap_a}{2},
\qquad
\{Q,P\}=\{\phi,p\}=1.
\]

The homogeneous closed-FRW \(V=0\) constraint pinned by the upstream classical
calculation is

\[
C=
-\frac{e^{-3Q/2}P^2}{6\pi^2}
+\frac{e^{-3Q/2}p^2}{4\pi^2}
-6\pi^2e^{Q/2}.
\]

### 1.2 Explicit positive densitization

The selected calculation makes the additional classical choice

\[
\boxed{
H=12\pi^2e^{3Q/2}C
=-2P^2+3p^2-72\pi^4e^{2Q}.
}
\]

The multiplier is strictly positive for real \(Q\). This preserves the
classical zero set and reparametrized gauge orbits, but it does not by itself
establish equality of quantum operators, domains, rigging maps, or physical
inner products.

### 1.3 Declared auxiliary space and ordering

The selected auxiliary representation is

\[
\mathcal H_{\rm aux}
=L^2(\mathbb R_Q\times\mathbb R_\phi,dQ\,d\phi),
\qquad
P=-i\hbar\partial_Q,
\qquad
p=-i\hbar\partial_\phi.
\]

Flat Schrödinger ordering of the already-densitized polynomial gives

\[
\boxed{
\widehat H
=2\hbar^2\partial_Q^2
-3\hbar^2\partial_\phi^2
-72\pi^4e^{2Q}.
}
\]

This is not an ordering prescription for undensitized raw \(C\).

### 1.4 Fourier--Liouville--Kontorovich--Lebedev reduction

With the \(\hbar\)-Fourier convention

\[
\psi(Q,\phi)
=(2\pi\hbar)^{-1/2}
\int_{\mathbb R}e^{ip\phi/\hbar}\widetilde\psi(Q,p)\,dp
\]

and the selected \(p>0\) component, define

\[
z=\frac{6\pi^2}{\hbar}e^Q,
\qquad
dQ=\frac{dz}{z},
\qquad
L=-\partial_Q^2+z^2.
\]

Then

\[
\widehat H_p=-2\hbar^2L+3p^2,
\qquad
LK_{i\kappa}(z)=\kappa^2K_{i\kappa}(z).
\]

The normalized KL kernel is

\[
\chi_\kappa(z)
=\frac{\sqrt{2\kappa\sinh(\pi\kappa)}}{\pi}K_{i\kappa}(z).
\]

The selected Fourier--KL realization is the real multiplication operator

\[
\boxed{h(\kappa,p)=3p^2-2\hbar^2\kappa^2}
\]

on \(L^2(\mathbb R_{+,\kappa}\times\mathbb R_{+,p},d\kappa\,dp)\), with

\[
D(\widehat H)
=\{A\in L^2:hA\in L^2\}.
\]

Self-adjointness here belongs to this explicitly selected spectral
realization.

### 1.5 RAQ zero fiber and physical measure

On compact-interior spectral tests, the selected group average is

\[
\eta_H(A)[B]
=\int_{\mathbb R}\frac{dN}{2\pi\hbar}
\langle A,e^{-iN\widehat H/\hbar}B\rangle
\]

and hence

\[
\eta_H(A)[B]
=\int_0^\infty dp\int_0^\infty d\kappa\,
\delta\!\left(3p^2-2\hbar^2\kappa^2\right)
\overline{A(\kappa,p)}B(\kappa,p).
\]

For \(p>0\),

\[
\kappa_0(p)=\sqrt{\frac32}\frac p\hbar,
\qquad
\left|\partial_\kappa h\right|_{\kappa_0}
=2\sqrt6\,\hbar p.
\]

Therefore

\[
\boxed{
\eta_H(A)[B]
=\int_0^\infty\frac{dp}{2\sqrt6\,\hbar p}
\overline{A(\kappa_0(p),p)}B(\kappa_0(p),p)
}
\]

and the selected completion is

\[
\boxed{
\mathcal H_{\rm phys}^{(H,+)}
=L^2\!\left((0,\infty),\frac{dp}{2\sqrt6\,\hbar p}\right).
}
\]

The null ideal consists of tests whose restriction to the positive zero ray
vanishes.

### 1.6 Comparison with the declared Darboux \(M_c\) fiber

The earlier local representation declared

\[
\eta_{M_c}(\psi,\varphi)
=\int_0^\infty dp\,
\overline{\psi(0,p)}\varphi(0,p).
\]

The identity map does not turn this \(dp\) form into the derived
\(dp/(2\sqrt6\hbar p)\) form up to one state-independent constant. The map

\[
(JA)(p)=\frac{A(p)}{\sqrt{2\sqrt6\,\hbar p}}
\]

is an abstract Hilbert-space isometry, but it is not the missing endpoint
transform and does not intertwine raw \(C\), selected \(H\), and \(M_c\).

### 1.7 The \(p=0\) cutoff boundary

For \(p\geq\epsilon>0\), the nonzero-edge witness \(A_0(p)=e^{-p}\) has

\[
\eta_\epsilon[A_0,A_0]
=\frac{E_1(2\epsilon)}{2\sqrt6\,\hbar}
=\frac{\log(1/\epsilon)-\gamma-\log2+o(1)}
       {2\sqrt6\,\hbar}.
\]

It diverges logarithmically as \(\epsilon\to0^+\). The vanishing witness
\(A_1(p)=pe^{-p}\) instead has

\[
\eta[A_1,A_1]=\frac1{8\sqrt6\,\hbar}>0.
\]

More generally, \(A=O(p^\alpha)\) gives local integrand
\(O(p^{2\alpha-1})\), so \(\alpha>0\) is the selected local integrability
criterion. A finite part may be declared with a reference momentum
\(p_\star>0\):

\[
\operatorname{FP}_{p_\star}
=\lim_{\epsilon\to0^+}
\left[
\eta_\epsilon[A_0,A_0]
-\frac{\log(p_\star/\epsilon)}{2\sqrt6\,\hbar}
\right]
=\frac{-\gamma-\log(2p_\star)}{2\sqrt6\,\hbar}.
\]

Changing \(p_\star\) changes the finite part. The cutoff therefore does not
select a canonical counterterm, origin sector, superselection rule, or global
branch gluing.

### 1.8 Full-real-\(p\) regular-shell completion

For the selected maximal multiplication operator, write \(p=\sigma r\),
\(\sigma=\pm1\), \(r>0\). On both regular rays,

\[
\kappa_0(r)=\sqrt{\frac32}\frac r\hbar,
\qquad
\left|\partial_\kappa h\right|_{\kappa_0}
=2\sqrt6\,\hbar r.
\]

The full regular-shell form is therefore

\[
\eta_{\rm reg}(A,B)=
\sum_{\sigma=\pm1}\int_0^\infty
\frac{dr}{2\sqrt6\,\hbar r}\,
\overline{A(\kappa_0(r),\sigma r)}B(\kappa_0(r),\sigma r).
\]

With \(x=\log(r/r_\star)\), \(dr/r=dx\), and the normalized trace map gives

\[
\boxed{
\overline{\Phi_{\rm reg}/\ker\eta_{\rm reg}}
\simeq L^2(\mathbb R,dx)_+\oplus L^2(\mathbb R,dx)_-.
}
\]

The point \(r=0\) is \(x=-\infty\), not a finite endpoint. The zero set of
\(h\) has zero two-dimensional auxiliary Lebesgue measure, so the selected
multiplication operator supplies no normalizable zero eigenprojection or
independent origin atom. A finite part, origin distribution, parity quotient
or cross-branch gluing law would be additional theory data. Changing
\(r_\star\) merely translates \(x\) unitarily.

### 1.9 BFV algebraic zero block and Ward identity

The pinned local zero block is

\[
S_0(\lambda)
=\lambda(N_0c_0-\rho_0\bar\rho_0),
\qquad \lambda>0,
\]

with

\[
sN_0=\rho_0,
\qquad
s\bar\rho_0=c_0,
\qquad
s\rho_0=sc_0=0,
\qquad
sS_0=0.
\]

The bosonic Fourier factor is

\[
\int_{\mathbb R}\frac{dN_0}{2\pi\hbar}
e^{i\lambda N_0c_0/\hbar}
=\frac{\delta(c_0)}{\lambda}.
\]

The oriented odd Gaussian contributes

\[
i\hbar[\rho_0\bar\rho_0]
e^{-i\lambda\rho_0\bar\rho_0/\hbar}=\lambda.
\]

Its ordered Hessian satisfies

\[
F=\begin{pmatrix}0&-\lambda\\ \lambda&0\end{pmatrix},
\qquad
\det F=\lambda^2,
\qquad
\operatorname{Pf}F=-\lambda.
\]

Thus

\[
Z_0^{\rm direct}
=Z_0^{\rm weighted\ elimination}
=\delta(c_0),
\qquad
Z_0^{\rm unweighted\ deletion}
=\frac{\delta(c_0)}{\lambda},
\]

and

\[
\partial_\lambda Z_0^{\rm direct}
=\partial_\lambda Z_0^{\rm weighted\ elimination}=0,
\qquad
\partial_\lambda Z_0^{\rm unweighted\ deletion}
=-\lambda^{-2}\delta(c_0).
\]

The equality of the first two ledgers is a local finite-dimensional Ward
accounting result. It does not choose a lapse contour or prove full BFV gauge
independence. The constant \(\lambda\) scaling here is not the field-dependent
constraint densitization \(C\mapsto H\).

## 2. Computed facts, interpretation, and open hypotheses

### Computed facts

- one selected densitized and order-fixed homogeneous constraint has an exact
  Fourier--KL multiplication realization;
- its \(p>0\) group average has the positive weighted zero fiber above;
- that fiber is not the prior \(dp\) static form under the identity map and one
  constant normalization;
- a nonzero \(p=0\) edge witness diverges logarithmically, a linearly vanishing
  witness is finite, and a finite-part subtraction introduces an arbitrary
  reference scale;
- on the declared full-real-\(p\) regular shell, the completion is
  \(L^2(\mathbb R,dx)_+\oplus L^2(\mathbb R,dx)_-\), \(p=0\) lies at
  \(x=-\infty\), and no origin atom is inherited from the auxiliary measure;
- direct Berezin integration equals determinant-weighted ghost elimination;
  unweighted ghost deletion fails the local Ward identity.

### Interpretation

The record has advanced from a declared local spectral fiber to one selected,
order/domain-fixed minisuperspace realization and two sharp boundary discriminators.
It shows how ordering, branch, test space, measure, edge domain, and determinant
bookkeeping are constitutive data of the selected quantum model.

### Open hypotheses

No current result establishes a raw-\(C\) quantum theory, equivalence between
raw \(C\), densitized \(H\), and \(M_c\), a canonical origin sector or
cross-branch gluing beyond the standard selected-\(H\) direct sum, an absolute
lapse/BFV measure, an inhomogeneous anomaly-free constraint algebra,
relational observables, a semiclassical Einstein limit, an empirical
prediction, quantum gravity, or a TOE.

## 3. Philosophical implications

### 3.1 Exact solvability is conditional knowledge

An exact solution is exact relative to a specified model, representation,
ordering, branch, domain, and averaging prescription. Mathematical closure
inside that package is real progress, but it is not evidence that nature chose
the package.

### 3.2 Classically equivalent descriptions need not be quantum-identical

Positive rescaling preserves the classical constraint surface while changing
the operator and measure problem. The philosophical lesson is not that
quantization is arbitrary; it is that a claimed physical equivalence must be
carried by an explicit domain-preserving intertwiner and observable map rather
than by classical notation alone.

### 3.3 The physical measure is part of the theory

The difference between \(dp\) and \(dp/p\) is not cosmetic bookkeeping. It
changes which states are normalizable and exposes the \(p=0\) boundary. An
abstract isomorphism between separable Hilbert spaces does not identify the
meaning of observables or the lineage of constraints.

### 3.4 Gauge redundancy is harmless only with complete bookkeeping

The ghost pair does not represent an additional physical object. Its
determinant records the change of variables needed to remove redundancy.
Dropping the variables and dropping their Jacobian are different operations.
The repaired Ward identity illustrates how a formal contradiction can be a
measure-accounting error rather than a physical inconsistency.

### 3.5 Negative results are directional information

The current KILLs reject specific shortcuts: constant-normalization identity
of two measures, naive nonzero \(p=0\) extension, a canonical finite part from
the cutoff alone, and unweighted ghost deletion. They do not reject quantum
cosmology or quantum gravity. A scoped negative result is useful because it
removes an invalid bridge and identifies the extra datum a successor must earn.

### 3.6 Minisuperspace is a laboratory, not the world

The model retains homogeneous scale and matter degrees of freedom while
discarding local gravitational waves and most of the Dirac constraint algebra.
It can test quantization logic but cannot by itself establish a theory of local
quantum spacetime. The move from model to world requires anomaly control,
observables, a classical limit, and empirical discrimination.

## 4. Forward research roadmap

Each row is an independent question. The dependency edges are memory and
planning metadata; they neither authorize execution nor predict success.

The explicit work order is

```text
1 full-p regular completion [scoped KEEP]
  -> 2 raw-C operator/domain audit [fiber classification NARROW; global domain open]
  -> 3 microlocal then exact endpoint
  -> 4 absolute BFV
  -> 5 classical closed-S3 HDA/Jacobi closure
  -> 6 quantum BFV anomaly
  -> 7 relational observables + BO/Ehrenfest + decoherence
  -> 8 non-flat transfer + observational likelihood
```

This is an ordering ledger, not one recursively authorized calculation. Stage
5 can start as an independent classical audit once its action and harmonic
couplings are declared; Stage 6 remains downstream of raw-domain, BFV and
classical-closure results.

| Stage and node | Prerequisite | Success discriminator | Failure or branch discriminator |
| --- | --- | --- | --- |
| 1 `open:gate1-v0-p-zero-p-negative-global-spectral-completion` | the \(p>0\) KL fiber and cutoff edge result | **observed:** selected-\(H\) regular completion is the two \(L^2(dx)\) branches with no inherited origin atom | any nonstandard origin sector or gluing still needs independent data |
| 2 `open:gate1-v0-raw-constraint-rescaling-and-p-zero-completion` | one declared weighted raw-\(C\) candidate and the selected-\(H\) comparison target | **observed:** each fixed-\(p\) raw fiber is limit-circle at \(Q\to-\infty\), limit-point at \(Q\to+\infty\), with indices \((1,1)\); a measurable global extension and RAQ equivalence remain open | the classical multiplier alone does not select the fiber boundary line or establish quantum equivalence |
| 3 `open:gate1-v0-exact-endpoint-mc-intertwiner-and-full-symbol` | the classical Darboux chart and principal FIO; a raw-\(C\) exact map additionally needs a selected global raw domain | a full symbol and common domains give the raw-\(C\) map, or a separately labelled selected-\(H\) support-restricted spectral intertwiner | the unrestricted selected-\(H\to M_c\) joint-support mismatch or lower-symbol/domain obstruction survives |
| 4 `open:gate1-v0-lapse-modulus-contour-and-absolute-bfv-measure` | the relative quartet and repaired zero-ghost Ward ledger | one contour/modulus/orientation prescription yields an absolute measure and passes Ward/gluing checks | contour, orientation, normalization or Gribov dependence persists |
| 5 `open:gate1-v0-classical-s3-hda-closure` | full ADM+matter action, perturbative order and \(S^3\) coupling ledger | projected HDA and Jacobi identities close with the projection remainder separately bounded | a genuine classical remainder survives after cutoff error is removed |
| 6 `open:gate1-v0-quantum-inhomogeneous-bfv-nilpotency-anomaly` | Stages 2, 4 and 5 plus a common operator domain | \(\widehat\Omega^2\) vanishes to declared perturbative, \(\hbar\) and cutoff orders | a regulator-stable operator anomaly or domain leakage remains |
| 7 `open:gate1-v0-relational-observables-bo-decoherence` | physical product, Stage 6 modes, clocks and a selected contour | clock-cross-checked observables and BO/Ehrenfest/decoherence residuals meet fixed errors | observables or classical recovery remain clock/domain/contour dependent |
| 8 `open:gate1-v0-empirical-likelihood-bridge` | Stage 7 plus an explicit \(V\ne0\) or alternative generation/reheating extension | discrete closed-universe spectra propagate through non-flat transfer to posterior-predictive tests | no primordial/late-time map or empirical discriminator exists |

## 5. KG connection map

The repository graph should be read in this direction:

```text
raw C
  -> positive densitization H
  -> declared H-hat ordering
  -> Fourier--KL spectral reduction
  -> multiplier/domain
  -> RAQ coarea fiber
  -> comparison with M_c
  -> p-zero cutoff boundary
  -> selected-H full-p two-branch regular completion

declared weighted raw C candidate
  -> Fourier fibers
  -> Q-minus limit-circle / Q-plus limit-point
  -> one boundary line per fixed p
  -> measurable global extension + RAQ equivalence still open

BFV source algebra
  -> zero-block Gaussian determinant
  -> local Ward equality
  -> lapse/absolute-measure open problem

computed formula ledgers
  -> interpretation boundaries
  -> eight-stage forward-research sequence
  -> raw/domain + exact-intertwiner + absolute-BFV
  -> classical S3 closure -> quantum BFV anomaly
  -> relational/BO/decoherence -> empirical likelihood
```

These are local typed edges. No external KG UID is invented, and no edge is a
ratification or automatic successor receipt.

## 6. Evidence and source anchors

- [`GATE1_V0_DENSITIZED_QUANTUM_COSMOLOGY_DERIVATION.md`](GATE1_V0_DENSITIZED_QUANTUM_COSMOLOGY_DERIVATION.md)
  derives the densitized KL/RAQ and BFV Ward formulas.
- [`GATE1_V0_DENSITIZED_RAQ_P_ZERO_BOUNDARY.md`](GATE1_V0_DENSITIZED_RAQ_P_ZERO_BOUNDARY.md)
  derives the cutoff, logarithmic divergence, vanishing-witness criterion, and
  finite-part scale ambiguity.
- [`GATE1_V0_FULL_P_REGULAR_RAQ_COMPLETION.md`](GATE1_V0_FULL_P_REGULAR_RAQ_COMPLETION.md)
  derives the two-ray coarea form, logarithmic branch coordinates, scoped
  direct-sum completion and no-inherited-origin-atom boundary.
- [`GATE1_V0_RAW_C_WEIGHTED_OPERATOR_DOMAIN_AUDIT.md`](GATE1_V0_RAW_C_WEIGHTED_OPERATOR_DOMAIN_AUDIT.md)
  records the declared weighted raw-\(C\) ordering, fiber Weyl classification,
  boundary-form ledger, extension debt and still-null global measurable domain.
- `evidence:gate1-v0-densitized-liouville-raq-result`,
  `evidence:gate1-v0-densitized-raq-p-zero-boundary-result`, and
  `evidence:gate1-v0-full-p-regular-raq-completion-result`,
  `evidence:gate1-v0-raw-c-weighted-operator-domain-audit-result`, together with
  `evidence:gate1-v0-bfv-zero-mode-elimination-ward-result`, carry executable
  checks and provenance.
- `source:nist-dlmf-bessel-kl`,
  `source:nist-dlmf-exponential-integral`, `source:marolf-1995`,
  `source:giulini-2000-group-averaging-raq`, and
  `source:louko-martinez-pascual-2011` bound the special-function, RAQ, and
  constraint-rescaling interpretation. Weyl's endpoint alternative, von
  Neumann's extension theorem, and Nussbaum/Lennon direct-integral reduction
  bound the raw-\(C\) fiber and global-measurability statements.

The ontology remains a memory and navigation layer. Evidence remains in the
committed calculation results, and philosophical interpretation remains
explicitly non-evidential.
