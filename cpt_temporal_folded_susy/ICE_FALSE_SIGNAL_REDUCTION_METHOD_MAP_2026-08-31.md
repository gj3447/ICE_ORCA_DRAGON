# ICE false-signal reduction method map

## Purpose

This is a practical routing map for new bounded calculations, not a universal
research contract and not a physics-ratification layer.  A calculation uses only
the checks relevant to its actual failure modes.  The map keeps four different
questions separate:

- did the code evaluate the declared finite mathematics correctly?
- did the regulator or basis manufacture the signal?
- does the finite result represent the intended continuum operator or gauge
  system?
- is there a physical observable and a valid statistical discovery procedure?

Passing an earlier question never answers a later one automatically.

## Failure-mode control menu

The numbering below is explanatory, not a seven-gate workflow. Select only the
controls that can falsify the current calculation; do not emit empty records for
the other entries.

### 1. Complete the smallest closed packet

Fix source equations, signs, density weights, reality/phase conventions,
canonical pairs and exceptional modes.  For an \(S^3\) calculation, scalar,
transverse-vector and TT sectors must be included whenever the selected bracket
can generate them. Use positive, exact-null or deliberately failing fixtures when
they exercise a failure mode of the selected packet. xPert or another tensor CAS
is a generator/checker only; its
output must be translated into the repository convention and pass low-mode
golden identities ([xPert](https://arxiv.org/abs/0807.0824),
[Cadabra](https://arxiv.org/abs/hep-th/0701238),
[unit-\(S^3\) SVT harmonics](https://arxiv.org/abs/1709.08020)).

### 2. Separate evaluator error from regulator leakage

For a nonlinear term whose finite evaluator can alias, compare:

1. exact modal/Gaunt convolution;
2. a basis-specific overintegrated transform certified by a polynomial-degree or
   cubature bound;
3. the production-resolution transform.

Record (3)-(1) first as `PRODUCTION_VS_EXACT_MODAL_DISCREPANCY`.  Call an
identified component `ALIASING_DEFECT` only after common normalization, identical
\(P_N\) placement, a sufficient quadrature/cubature degree, and separately bounded
arithmetic error have excluded other causes.  The exact \((1-P_N)\) support from
(1) is `TRUE_PROJECTION_REMAINDER` only when (1) is the declared exact Galerkin
product.  Never combine these objects into one norm.  Classical dealiasing removes
folded convolution terms, not the true Galerkin tail
([Patterson--Orszag](https://doi.org/10.1063/1.1693365),
[Orszag](https://doi.org/10.1175/1520-0469(1971)028%3C1074%3AOTEOAI%3E2.0.CO%3B2)).

### 3. Run a frozen-packet refinement ladder

Hold physical source modes, smearings, branch and conventions fixed while
increasing \(N\).  Compare only common retained coefficients, per-channel tail
support, invariant norms and condition numbers.  Record reverse/basis-conjugate
controls.  Smoothness can yield fast spectral convergence, but it must be
measured rather than assumed ([Kidder--Finn](https://arxiv.org/abs/gr-qc/9911014),
[Grandclément--Novak](https://arxiv.org/abs/0706.2286)).

Classification:

- exact selection-rule zero beyond a finite \(N_*\): finite channel completion;
- stable nonzero common-mode limit with a tail bound: continuum candidate;
- drift, parity alternation or basis dependence: regulator-dependent;
- only one cutoff: unresolved.

### 4. Check gauge/constraint structure before interpreting a residual

Compute ambient-before-project and project-after-each-operation paths separately.
For ADM, retain coefficientwise \(DD\), \(DH\) and \(HH\) residuals, structure
functions and every discarded channel.  The ordinary finite canonical Poisson
bracket satisfies Jacobi identically; this is a control, not HDA closure.  A
projected Jacobiator needs its own declared projection placements.

Discretization commonly breaks diffeomorphism symmetry and can turn constraints
into pseudo-constraints.  A small residual is therefore not automatically an
anomaly or a proof of closure.  Compare refinement/coarse-graining maps and, where
available, mimetic or perfect-action controls
([Bahr--Dittrich](https://arxiv.org/abs/0909.5688),
[broken gauge symmetries](https://arxiv.org/abs/0905.1670),
[perfect actions](https://arxiv.org/abs/0907.4323),
[consistent and mimetic discretizations](https://arxiv.org/abs/gr-qc/0404052)).

Only after the classical algebra is fixed should BFV/BV be tested.  Report the
classical master equation or \(\{\Omega,\Omega\}\) by ghost number, boundary
terms separately, and then the quantum/common-core defect.  Cutting, BV
pushforward and gluing are independent checks
([classical BV--BFV](https://arxiv.org/abs/1201.0290),
[quantum BV--BFV](https://arxiv.org/abs/1507.01221)).

### 5. Certify numerical existence, roots and spectra

Float agreement is evidence, not an enclosure.  High-impact roots, ODE/BVP
transport and signs should use outward-rounded interval/ball arithmetic and an
existence/uniqueness certificate such as interval Newton/Krawczyk or a radii
polynomial.  A sign is certified only when zero is excluded
([IEEE 1788 interval arithmetic](https://standards.ieee.org/ieee/1788/4431/),
[radii-polynomial validation](https://doi.org/10.1090/mcom/3046),
[validated PDE integration](https://arxiv.org/abs/2305.08221)).

Polynomial roots can additionally use alpha-theory certificates
([alphaCertified](https://arxiv.org/abs/1011.1091)).  Projected eigenvalues need
spectral-pollution controls; cutoff stability alone can retain spurious gap
eigenvalues ([Davies--Plum](https://arxiv.org/abs/math/0302145),
[Levitin--Shargorodsky](https://arxiv.org/abs/math/0212087)).  A finite nonreal
Weyl proxy remains distinct from a singular-endpoint \(m\)-function and spectral
measure.

### 6. Demand independent implementations and provenance

For important identities, implementation B must not read A's generated
coefficients.  Useful pairs are hand/exact Gaunt versus a tensor CAS, exact modal
versus overintegrated grid, ordinary float versus ball arithmetic, and two
different formulations of the same invariant.  Agreement only establishes a
cross-check because both implementations can share a wrong model.

A durable raw result retains the command, runner and material input/upstream
hashes plus the precision or seed information that can change the conclusion.
Lockfiles supply the shared environment. Preserve stdout/stderr only when it is
diagnostic evidence, not as an empty field in every result. Comparison remains
field-specific; no global epsilon is used.

### 7. Separate exploration from empirical discovery

Record the complete scan family: modes, parameter boxes, branches, solvers,
cutoffs, stopping rules, nulls and failures.  A selected panel is exploratory
until a frozen hold-out input and independent implementation reproduce it.
Blinding reduces analyst feedback when real data are introduced
([Klein--Roodman](https://doi.org/10.1146/annurev.nucl.55.090704.151521)).

For likelihood work, first validate the inference implementation with simulated
data and predictive checks
([simulation-based calibration](https://arxiv.org/abs/1804.06788),
[Bayesian workflow](https://arxiv.org/abs/2011.01808)).  A parameter or mode scan
requires a declared search family and a global, not merely local, significance
([Gross--Vitells](https://arxiv.org/abs/1005.1891),
[Cowan et al.](https://arxiv.org/abs/1007.1727)).  FDR procedures apply only when
there is a valid stochastic null and a declared family of p-values; they do not
turn deterministic residual thresholds into statistical discoveries.

## ICE lane routing

| lane | principal false signal | next applicable control |
|---|---|---|
| P1 Picard/sign | float tube misses a root or interval still crosses zero | panelwise interval Picard inclusion, variational \(\lambda\)-tube, zero-excluding endpoint interval |
| P4 Weyl | finite cutoff pole/eigenvalue or branch is mistaken for singular spectral data | complex ball boxes, tail theorem, second-order/pollution-free spectral control, singular Weyl boundary data |
| P2 harmonics | aliasing, phase convention, incomplete sector | exact-modal/overintegrated/production three-way audit, real SVT golden packet, cutoff ladder |
| P3 HDA | omitted vector/TT channel or projection placement looks anomalous | ambient/projected \(DD,DH,HH\), discarded support, projected-Jacobi decomposition |
| P5 BFV | gauge fixing, domain or boundary defect looks like anomaly | CME/BFV master equation by ghost number, two admissible gauges, common core, refinement and gluing |
| P6 measure/gluing | relative determinant is mistaken for an absolute measure | determinant/Pfaffian line, polarization and orientation transport, two-slab gluing, counterterm dependence |
| P7 likelihood | analysis tuning, local significance or broken inference | physical product/state first; SBC, mock recovery, blinding/hold-out, global trials and systematic variants |

## Optional reporting discipline for a future empirical claim

If a future report elects to call an empirical result a discovery candidate, it
should state explicitly rather than infer whether each of the following holds:

1. the finite mathematical predicate is reproduced independently;
2. aliasing is zero or bounded separately;
3. the frozen-packet cutoff ladder stabilizes with a tail/error certificate;
4. basis, phase and admissible gauge changes preserve the declared invariant;
5. all sectors generated by the operation are present;
6. the appropriate classical/quantum domain or master-equation checks pass;
7. a physical observable and, if data are used, a valid global statistical
   procedure exist.

For ordinary finite-workbench reporting, useful non-promotional descriptions
include calculated finite fact, regulator-dependent result, validated mathematical
predicate, interpretive lead, and open problem.  These are prose descriptions, not
mandatory repository tiers or ratification states.
