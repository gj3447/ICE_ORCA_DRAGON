# ICE_ORCA_DRAGON status

> Current engineering/reproduction state followed by a bounded historical scientific ledger. This file
> reports evidence; it does not authorize KG or canon mutation.

## Current state — 2026-08-17

| Component | State |
|---|---|
| Runnable catalog | 61 committed entries; `./ice list --json` is authoritative for the working tree |
| Control plane | strict TypeScript, Effect 3, Node 24 contract, exact `package-lock.json` |
| Numerical runtime | Python 3.13 contract with exact `uv.lock` |
| Mapped reproduction cases | 14 |
| Reproduction ledger | 12 `REPRO`, 1 `NONPORTABLE_FAIL`, 1 `SUPERSEDED` |
| Local engineering gate | `npm run check` |
| Environment gate | `./ice doctor` |
| Scientific workflow | lean source → calculation → independent check → scoped interpretation |

Historical source/result inventories contain more files than the live CLI. Do not use a copied prose
count or rough “N+” inventory as the runnable catalog.

## Reproduction status

`./ice repro` works in an Effect-scoped temporary copy and compares fresh mapped outputs with the
committed `HEAD` baseline. It is intentionally non-destructive and intentionally exits nonzero for the
current ledger.

- Twelve mappings satisfy their field-aware semantic comparators.
- `queue_03_threshold_sensitivity_scan` is `NONPORTABLE_FAIL`: its legacy entrywise commutator maximum
  changes under an arbitrary orthogonal basis of the SciPy null space. Observed categorical outcomes can
  change, so a wider tolerance is not a valid fix.
- `queue_06_cooperative_vacuum` is `SUPERSEDED`: the committed repaired result comes from a different
  later computation and is not reproducible by pretending the historical named script produced it.
- Queue04 permits `atol=1e-6` only for the verified circular optimizer-coordinate paths; structure,
  categories, and other fields keep their tighter comparator.

See [`audits/QUEUE03_PORTABILITY_AUDIT_2026-08-14.md`](audits/QUEUE03_PORTABILITY_AUDIT_2026-08-14.md)
and [`audits/REPRODUCIBILITY_2026-06-08.md`](audits/REPRODUCIBILITY_2026-06-08.md).

## Current scientific workflow

New work has no mandatory tier, preregistration contract, Bayes/Lakatos form, or KG ratification step.
Record the primary source, equations, conventions, assumptions, command, environment, and actual output;
then apply an independent check proportional to the calculation's risk. Exact algebra, numerical output,
physical interpretation, and open speculation must remain separate. Historical T2 labels and contract
files below describe how those old results were produced; they do not govern new work.

## Current bounded T2 result — CPT × Temporal-Folded SUSY Phase 12

Phase 12 is a `POST_HOC` exact/deductive cycle, not a confirmation or canon change.

- The Phase 11 homogeneous-quadratic strong class, and the weak dilation with an unrestricted lapse
  rescaling, are removable from the open-interval bulk by a time-dependent canonical frame change under
  the stated invariance/completeness assumptions. Endpoint twist, polarization, and (for momentum
  shears) a boundary generating function remain.
- An engineered, regular 4D rigid \(N=1\) Wess–Zumino spatial BPS wall gives scalar and chiralino
  components the same kinematic internal-flavor frame. Its scalar differential expressions have exact
  formal factorization; the executable does not derive the full Weyl operator or a self-adjoint domain.
  A boson-only collar fails the matched endpoint identity.
- This does **not** derive a local-supergravity seam, a cosmological observable, boson–fermion branch
  exchange, a physical endpoint detector, or “pre-Big-Bang time = SUSY.” The partial matter-coupled
  SUGRA candidate remains `INCONCLUSIVE`.
- The executable reports 38 exact positive checks and rejects 9 semantic mutants. It has no mapped
  legacy result JSON, so `./ice run phase12_boundary_twist_interface` is the applicable execution gate;
  it is not an additional case in the 14-entry reproduction ledger.

See
[`../cpt_temporal_folded_susy/PHASE12_BOUNDARY_TWIST_INTERFACE.md`](../cpt_temporal_folded_susy/PHASE12_BOUNDARY_TWIST_INTERFACE.md)
and
[`../cpt_temporal_folded_susy/PHASE12_RESEARCH_CONTRACT.json`](../cpt_temporal_folded_susy/PHASE12_RESEARCH_CONTRACT.json).

## Current bounded T2 result — CPT × Temporal-Folded SUSY Phase 13A

Phase 13A preregistered a direct Lorentzian local-SUGRA branch-\(Q\) kill test before its executable
was written. An independent adversarial audit found that the first run's overall `CONTRADICTS` wording
exceeded the implemented physical mapping. The original contract remains unchanged; a separate
`POST_HOC_CORRECTED` erratum records the corrected scope.

- The Moniz first-order constraint's \(\partial_a,\partial_\phi\) principal terms preserve a chosen
  formal \(e^{\pm i\lambda W}\) phase label. The implemented direct-sum labels are not relational
  expanding/contracting spectral projectors, so this control is `INCONCLUSIVE` for the physics claim.
- In a finite positive-Hilbert-space class, if \(C=\{Q,Q^\dagger\}\) and physical states are defined by
  \(\ker C\), then \(Q\) and \(Q^\dagger\) vanish on that kernel. The executable verifies a nontrivial
  off-shell sheet/parity-flipping witness whose kernel exchange map is exactly zero. This scoped shortcut
  is `CONTRADICTS`, but it is not a mapped truncation of the 4D SUGRA physical Hilbert space.
- A generic odd CAR constraint can close exactly on an even symbol while every formal-sheet cross block
  vanishes. Local constraint closure alone therefore does not imply branch exchange.
- No audited Phase 13A source model supplies a gauge-independent relational branch projector, common
  physical domain/inner product, and a nonzero fermionic charge distinct from the local gauge constraint.
  The literal “opposite time branch = superpartner” claim remains `INCONCLUSIVE/UNCONSTRUCTED`, not
  supported and not universally refuted.
- The executable reports 21 exact positive checks and rejects 8 semantic mutants. Phase 13B spatial-wall
  scattering is gated out of the core sequence; if pursued, it is a separately registered auxiliary
  interface project with zero evidence weight for the literal cosmological claim.

See
[`../cpt_temporal_folded_susy/PHASE13A_LORENTZIAN_BRANCH_SUPERCHARGE.md`](../cpt_temporal_folded_susy/PHASE13A_LORENTZIAN_BRANCH_SUPERCHARGE.md),
[`../cpt_temporal_folded_susy/PHASE13A_RESEARCH_CONTRACT.json`](../cpt_temporal_folded_susy/PHASE13A_RESEARCH_CONTRACT.json),
and
[`../cpt_temporal_folded_susy/PHASE13A_ADVERSARIAL_ERRATUM.json`](../cpt_temporal_folded_susy/PHASE13A_ADVERSARIAL_ERRATUM.json).

## Current bounded T2 result — CPT × Temporal-Folded SUSY Phase 14A

Phase 14A preregistered a compact \(T^3\), flat-FLRW, neutral-chiral-clock charge-first template before
freezing its source packet/ledger and executable. The committed first run and two independent replays
all returned exit 0 with **24 exact checks, 7 executable mutants rejected, and 6 scope guards**.

- The exact bosonic reduction gives
  \(C_B=-p_X^2+p_T^2+p_Y^2\), \(\{T,C_B\}=2p_T\), and
  \(\alpha=(p_T^2+p_Y^2)/(2V_0^2a^6)>0\) on both \(p_T\ne0\) orientations.
- On the frozen Kallosh bosonic-flat-FLRW linear-fermion domain,
  \(\delta\upsilon/\delta\epsilon=-(\alpha/2)I_4\) has rank 4 and kernel dimension 0. This excludes a
  nonzero goldstino-unitary-gauge residual parameter; it does not remove local gauge invariance or every
  reduced/dressed charge.
- A smooth compact \(T^3\) has no actual spatial boundary or asymptotic end, so the
  Regge–Teitelboim spatial-boundary channel is `NOT_APPLICABLE_IN_THIS_ROUTE`. No temporal endpoint or
  earlier collar is substituted for that surface.
- The bulk calculation is only a formal constraint-ideal control. The differentiable graded
  matter-SUGRA Dirac generator is `NOT_DERIVED`, so template completeness and equivalence-class
  deduplication remain `DEFERRED_PENDING_CANONICAL_BRIDGE`.
- The selected nonzero-charge target is therefore `INCONCLUSIVE_UNCONSTRUCTED`; the literal
  branch-superpartner target remains `INCONCLUSIVE_OUT_OF_SCOPE`. Phase 14B is not opened.
- This kernel has no mapped legacy output. The runnable catalog rises to 45, while the mapped
  reproduction ledger remains 14 cases.

See
[`../cpt_temporal_folded_susy/PHASE14A_CHIRAL_CLOCK_CHARGE_FIRST.md`](../cpt_temporal_folded_susy/PHASE14A_CHIRAL_CLOCK_CHARGE_FIRST.md),
[`../cpt_temporal_folded_susy/PHASE14A_RESEARCH_CONTRACT.json`](../cpt_temporal_folded_susy/PHASE14A_RESEARCH_CONTRACT.json),
and
[`../cpt_temporal_folded_susy/PHASE14A_RUN_RESULT.json`](../cpt_temporal_folded_susy/PHASE14A_RUN_RESULT.json).

## Current bounded T2 result — CPT × Temporal-Folded SUSY Phase 15R

Phase 15A was stopped as `INVALID/INCONCLUSIVE/PREREG_OR_PROVENANCE_INVALID` after a parent-sign
outcome was observed before the complete executable commit. Phase 15R disclosed that outcome as a
known prior, preregistered a fresh source-scoped reproduction, and kept the Hohl, Kallosh, and
non-evidential ADM symbolic graphs disjoint.

- The committed first run and independent replay both returned exit 0 with **47 exact checks,
  17 mutant categories / 18 fixtures rejected, 4 scope guards, and 24/24 known-prior matches**.
- Hohl's frozen source-native map gives (R_H=+6Q) and, after the unique endpoint removal,
  first-order inertia ((0,0,3)). It is `REJECT_SIGN` for the ADM-compatible Lorentzian bosonic target.
- Kallosh's source-native map gives (R_K=-6Q) and inertia ((1,0,2)), so it passes the bosonic
  target. Its frozen source coverage lacks the target old-minimal auxiliary-retaining action and
  complete required transformation family, so it is `BOSONIC_PARENT_ONLY`.
- The bosonic target is `VALID/SUPPORTS/NONE`; the full same-source target is
  `VALID/CONTRADICTS/NO_VALID_SINGLE_PARENT_IN_FROZEN_CENSUS`. This is a result for exactly the two
  frozen primary candidates, not a literature-wide SUGRA no-go.
- Hohl action/transformations may not be stacked with Kallosh curvature/action signs. Phase 15
  tangency and every relational branch projector remain closed. The literal branch-superpartner core
  remains `INCONCLUSIVE/UNCONSTRUCTED` with no new observable.
- The runnable catalog is now 46; the mapped reproduction ledger remains 14 cases.

See
[`../cpt_temporal_folded_susy/PHASE15R_PARENT_SIGN_REPAIR.md`](../cpt_temporal_folded_susy/PHASE15R_PARENT_SIGN_REPAIR.md),
[`../cpt_temporal_folded_susy/PHASE15R_RESEARCH_CONTRACT.json`](../cpt_temporal_folded_susy/PHASE15R_RESEARCH_CONTRACT.json),
[`../cpt_temporal_folded_susy/PHASE15R_SOURCE_CONVENTION_PACKET.json`](../cpt_temporal_folded_susy/PHASE15R_SOURCE_CONVENTION_PACKET.json),
[`../cpt_temporal_folded_susy/PHASE15R_RUN_RESULT.json`](../cpt_temporal_folded_susy/PHASE15R_RUN_RESULT.json),
and
[`../cpt_temporal_folded_susy/PHASE15R_REPLAY_RECEIPT.json`](../cpt_temporal_folded_susy/PHASE15R_REPLAY_RECEIPT.json).

## Current direct calculation — CPT × Temporal-Folded SUSY Phase 16

Phase 16 drops the former contract machinery and computes directly from one source, Binétruy–Girardi–
Grimm `hep-th/0005225v1`. The executable returned exit 0 with **20 exact checks**.

- Solving BGG CPN.13 and contracting the curvature in the literal CPN.26 `ab` order gives
  \(\mathcal R_{\rm BGG}=-6Q\). CPN.130 plus CPN.59 then gives the first-order kinetic Hessian
  \((V_0a^3/N)\operatorname{diag}(-1,1,1)\), inertia \((1,0,2)\), and
  \(H=N(-p_X^2+p_T^2+p_Y^2)/(2V_0a^3)\). This is the \((X,T,Y)\) kinetic
  parent subblock; the lapse and algebraic auxiliary constraints are outside that Hamiltonian.
- The strict auxiliary-retaining FLRW truncation does not. At an exact point on that locus, CPN.85
  gives a nonzero \(F\epsilon^1\bar\chi^{\dot1}\) coefficient in \(\delta b_3\), and CPN.40/75/77
  independently give a nonzero gamma-traceless spatial gravitino variation.
- On the bosonic \(W=0,F=0\) rolling-clock slice with nonzero proper-time rate, the CPN.93 parameter map has full rank, so the
  background preserves no nonzero local-SUSY parameter.
- This is a scoped failure of the minimal off-shell FLRW fermionic truncation, not a refutation of full
  4D \(N=1\) SUGRA, full homogeneous Bianchi I, a smaller on-shell/Killing-spinor slice, or the still
  unconstructed temporal branch supercharge.
- The runnable catalog is now 47; the mapped reproduction ledger remains 14 cases.

See
[`../cpt_temporal_folded_susy/PHASE16_BGG_SINGLE_SOURCE.md`](../cpt_temporal_folded_susy/PHASE16_BGG_SINGLE_SOURCE.md)
and
[`../cpt_temporal_folded_susy/phase16_bgg_single_source.py`](../cpt_temporal_folded_susy/phase16_bgg_single_source.py).

## Current direct calculation — CPT × Temporal-Folded SUSY Phase 17

Phase 17 treats \(t\in\mathbb R\) as the base coordinate itself: there is no chiral clock, rolling
background, or spatial-wall analytic continuation. The contract-free executable returned exit 0 with
**34 exact symbolic checks**.

- The minimal positive-energy \(4d\;N=1\) CAR fiber and the same-point local charge pass the standard
  adjoint closure, but every open-half cross block is exactly zero by support locality.
- On a fundamental two-sheet space, \(Q^X_\alpha=X_s\otimes q_\alpha\) keeps the same algebra and
  fermion oddness while giving rank-two cross blocks in both directions. A one-way sheet charge fails
  the standard adjoint closure, and a continuous unitary mixing shows that the algebra alone does not
  select the exchange basis.
- When unfolded as literal coordinate reflection, the charge is nonlocal and anticommutes rather than
  commutes with signed \(P_t\). A fixed \(t=0\) seam also has
  \(v^0=|\zeta_1|^2+|\zeta_2|^2\), so ordinary Lorentzian reality leaves only the zero preserved
  supercharge parameter.
- A doubled real Pin-like temporal projector of rank four exists. This is an algebraic opening, not yet
  a physical interface: the doubled Lorentzian action, variational domain, conserved charge, and
  basis-independent sheet observable remain open.
- Schwinger–Keldysh doubling supplies an exact nilpotent BRST algebra, but its charges encode contour
  unitarity rather than particle superpartners. The conservative physical interpretation is horizontal
  CPT/Pin sewing between histories with ordinary SUSY acting vertically inside each sheet.
- The runnable catalog is now 48; the mapped reproduction ledger remains 14 cases.

See
[`../cpt_temporal_folded_susy/PHASE17_TIME_LINE_FOLD_ALGEBRA.md`](../cpt_temporal_folded_susy/PHASE17_TIME_LINE_FOLD_ALGEBRA.md)
and
[`../cpt_temporal_folded_susy/phase17_time_line_fold_algebra.py`](../cpt_temporal_folded_susy/phase17_time_line_fold_algebra.py).

## Current direct calculation — CPT × Temporal-Folded SUSY Phase 18

Phase 18 is a bounded free initial-state/seam control, not a completed doubled Wess–Zumino/Pin
interface. Its locked executable returned exit 0 with **47 exact symbolic checks and one independent
SciPy time-integration control**.

- Under an unchanged equal-mass free post-seam bulk, a finite instantaneous canonical Cauchy-data map
  cannot move the post-post retarded poles: \(m_{B,\mathrm{pole}}^2=m_{F,\mathrm{pole}}^2=m^2\) and
  \(\Delta m_{\mathrm{pole}}^2=0\).
- A scalar kick can still break the seam action/domain and prepare a non-SUSY state with
  \(n_B(k)=\kappa^2/[4(k^2+m^2)]\), while a finite two-mode fermion Nambu control has
  \(n_F=\sin^2\theta\). Statistical correlators change; the free spectral commutator does not.
- The sharp scalar kick has linear number-density and quadratic energy-density UV divergences. A
  finite-duration Gaussian Born control suppresses high momentum exponentially, but lies outside the
  strict instantaneous-seam theorem.
- Collisionless FRW \(a^{-2}\)/\(a^{-3}\) dilution and inserted-soft-mass ratios are conditional scaling
  controls, not derived absolute mass predictions. Interacting self-energies, persistent \(F/D\)-order
  parameters, full Pin sewing and Higgs power sensitivity remain open.
- The runnable catalog is now 49; the mapped reproduction ledger remains 14 cases.

See
[`../cpt_temporal_folded_susy/PHASE18_GAUSSIAN_SEAM_SPECTRUM.md`](../cpt_temporal_folded_susy/PHASE18_GAUSSIAN_SEAM_SPECTRUM.md)
and
[`../cpt_temporal_folded_susy/phase18_gaussian_seam_spectrum.py`](../cpt_temporal_folded_susy/phase18_gaussian_seam_spectrum.py).

## Current direct calculation — CPT × Temporal-Folded SUSY Phase 19

Phase 19 tests two explicit SUGRA inflation trajectories against the closed \(k=+1\),
time-reflection-symmetric bosonic equations. Its locked executable returned exit 0 with **17 exact and
30 numerical checks**.

- Exact reduction gives \(V=m^2\phi^2/2\) for the shift-symmetric stabilizer model and the Starobinsky
  potential for the improved Cecotti/no-scale model. Orthogonal mass formulae use
  \(H_V^2=V/3\), not the actual \(H(t)^2\), which vanishes at the bounce.
- Data \(H_0=\dot\phi_0=0\) and \(a_0=\sqrt{3/V(\phi_0)}\) produce a local smooth bosonic bounce. The
  independent integrations reproduce 50, 55, and 60 accelerated-e-fold solutions for both potentials
  with maximum relative Friedmann-constraint error below \(10^{-12}\).
- Every table row is an existence witness found by shooting from a requested \(N_{\rm acc}\). Neither
  CPT nor Pin selects the input \(\phi_0\); in particular, \(\phi_0=5.44296946\ldots\) is the value
  required by the 60-e-fold Starobinsky row, not a seam prediction.
- The inflationary stabilizer F-term is nonzero, but the displayed models restore the supersymmetric
  Minkowski endpoint. No persistent soft scale, fermionic sewing, perturbation propagation, or
  reheating history is derived.
- The runnable catalog rose to 50; the mapped reproduction ledger remains 14 cases.

See
[`../cpt_temporal_folded_susy/PHASE19_CLOSED_SUGRA_BOUNCE.md`](../cpt_temporal_folded_susy/PHASE19_CLOSED_SUGRA_BOUNCE.md)
and
[`../cpt_temporal_folded_susy/phase19_closed_sugra_bounce.py`](../cpt_temporal_folded_susy/phase19_closed_sugra_bounce.py).

## Current direct calculation — CPT × Temporal-Folded SUSY Phase 20

Phase 20 checks whether the leading de Sitter/WDW envelope selects the Phase 19 Starobinsky benchmark.
Its locked executable returned exit 0 with **18 exact and 14 numerical checks**.

- The standard semiclassical history weight is proportional to \(e^{2sI}\). The \(e^{4sI}\) weight
  requires an additional independent-pair assumption; CPT sewing alone does not derive it. Both
  conventions are monotone at finite positive \(\varphi\) and have a nonzero slope at
  \(\varphi=5.442969458\), so the leading envelope does not select that value.
- A universal factor-two symmetrized probability is not established. Coherent conjugate saddles can
  produce order-one interference, while a WDW current, overlap, normalization, factor ordering, and
  decoherence prescription remain unconstructed.
- On the displayed Cecotti trajectory the benchmark has \(F^S\ne0\). Its static positive-real F-flat
  point is \(T=1,\varphi=0\), but that classical observation does not solve or localize the quantum
  local-SUSY wavefunction.
- With the Phase 19 endpoint and explicit thermal-history inputs, the code reproduces
  \(\Omega_{K0}=-5.5258\times10^{-4}(T_{\rm reh}/10^9\,{\rm GeV})^{2/3}\). This is a sensitive
  conditional conversion, including the negative closed-universe sign, not a curvature or reheating
  prediction.
- An exact complex SUGRA saddle and the boson–fermion–gravitino one-loop determinant remain open. The
  calculation is a leading-envelope control, not a two-sheet SUGRA WDW no-go.
- At Phase 20 the runnable catalog rose to 51; the mapped reproduction ledger remained 14 cases.

See
[`../cpt_temporal_folded_susy/PHASE20_TWO_SHEET_WDW_SELECTION.md`](../cpt_temporal_folded_susy/PHASE20_TWO_SHEET_WDW_SELECTION.md)
and
[`../cpt_temporal_folded_susy/phase20_two_sheet_wdw_selection.py`](../cpt_temporal_folded_susy/phase20_two_sheet_wdw_selection.py).

## Previous direct calculation — CPT × Temporal-Folded SUSY Phase 21

Phase 21 asks whether a decoupled-sheet-normalized Gaussian seam makes a reference subtraction and
flux probability emerge automatically. Its committed executable returned exit 0 with **27 exact and
7 numerical checks**.

- For one positive real-boson mode,
  \(R=Z(C)/(Z_+Z_-)=(1-\rho^2)^{-1/2}\) and \(R(C=0)=1\) exactly. This identifies the
  no-cross-sheet baseline; it does not force replacing \(R\) by \(R-1\).
- A chosen zero-insertion exclusion gives \(R-1\), but the linked-cluster object is
  \(\log R=-\tfrac12\log(1-\rho^2)\). At order \(\rho^4\), \(R-1\) already contains a
  disconnected product of connected rings.
- For \(A_n=a_0+q^2n^2\) and constant \(C_n=\kappa\), \(R_n-1\) and \(\log R_n\) have
  \(n^{-4}\) tails, while the unnormalized sector difference
  \(Z_n(0)(R_n-1)\) has an \(n^{-6}\) tail. Constant-relative coupling instead leaves a
  non-decaying normalized-ratio tail.
- The imposed flat-sector toy gives \(p_0=0.484950\ldots\); retaining the decoupled
  \(Z_n(0)\) baseline changes it to \(0.626161\ldots\). This is direct evidence that the
  determinant ratio alone does not fix the sector prior.
- Abel/zeta finite parts can define a regulated determinant but do not create a countably additive
  positive WDW probability. A physical flux measure, decoherence/current prescription, actual
  three-form SUGRA kernel, and a finite joint \((n,\phi)\) peak remain open.
- At Phase 21 the runnable catalog rose to 52; the mapped reproduction ledger remained 14 cases.

See
[`../cpt_temporal_folded_susy/PHASE21_CONNECTED_SEAM_GAUSSIAN.md`](../cpt_temporal_folded_susy/PHASE21_CONNECTED_SEAM_GAUSSIAN.md)
and
[`../cpt_temporal_folded_susy/phase21_connected_seam_gaussian.py`](../cpt_temporal_folded_susy/phase21_connected_seam_gaussian.py).

## Current direct calculation — CPT × Temporal-Folded SUSY Phase 22

Phase 22 constructs a bounded seam-state control for one free supersymmetric oscillator. Its committed
executable returned exit 0 with **31 exact checks** and no floating-point fit.

- For \(\omega,\beta>0\), the bosonic and fermionic thermofield-double-like factors form a normalized
  positive purification. Tracing out one sheet gives
  \(\rho_+=Z^{-1}e^{-\beta H}\), \(Z=(1+r)/(1-r)\), \(r=e^{-\beta\omega}\).
- The fixed-energy doublet obeys \(Q^2=0\), \(\{Q,Q^\dagger\}=2H\), and
  \([\rho_+,Q]=0\). This is covariance inside equal-energy multiplets, not an unbroken thermal vacuum:
  \(\langle H\rangle=2\omega r/(1-r^2)>0\) at finite \(\beta\).
- A graded anti-linear occupation-space involution leaves the displayed state invariant. It is not a
  spacetime Clifford/Pin lift, and the exact \(Z_{\rm SK}[J,J]=1\) check is unitarity rather than a
  constructed SK ghost/BRST quartet.
- The density cross covariance is
  \(1/[2\omega\sinh(\beta\omega/2)]\). The factor two relative to the inverse Euclidean DtN amplitude
  kernel is explicit because the density is \(|\Psi|^2\).
- In the unregulated noncompact free limit, \(Z_B\sim(\beta\omega)^{-1}\) and
  \(\langle x^2\rangle\sim(\beta\omega^2)^{-1}\). Thus the same Gaussian ansatz is not trace class at
  \(\omega=0\); this is not a no-go for compact or interacting inflaton minisuperspace.
- At Phase 22 the runnable catalog rose to 53; the mapped reproduction ledger remained 14 cases.

See
[`../cpt_temporal_folded_susy/PHASE22_FINITE_MODE_SEAM_DENSITY.md`](../cpt_temporal_folded_susy/PHASE22_FINITE_MODE_SEAM_DENSITY.md)
and
[`../cpt_temporal_folded_susy/phase22_finite_mode_seam_density.py`](../cpt_temporal_folded_susy/phase22_finite_mode_seam_density.py).

## Current direct calculation — CPT × Temporal-Folded SUSY Phase 23

Phase 23 calibrates the homogeneous constrained-density step without calling it the full cosmological
seam state. Its committed executable returned exit 0 with **32 exact checks and 4 numerical checks**.

- The full-real-lapse Abel and Gaussian averages converge distributionally to \(\delta(C)\), while a
  half-lapse integral is a resolvent and naive Euclidean evolution diverges on the negative spectrum of
  the hyperbolic constraint.
- For the compact control \(q\in(0,\pi)\), \(E_n=\sqrt{n^2+\mu^2}\), an explicit clock and
  positive-frequency choice give a positive integrated physical norm. Local KG current is not a Born
  density: an exact two-mode witness has \(j_T=-55/(768\pi)\) at one point while its integrated current
  remains one.
- Supplying \(B_L=e^{-L\sqrt h}\) after the constraint gives
  \(\rho_+=Z_L^{-1}e^{-2L\sqrt h}\), a positive trace-class regulated density. The continuous seed and
  compact bridge are separate calibrations; \(L\), the regulator, branch orientation, and toy pairing
  are inputs rather than cap/CPT predictions.
- At the quadratic \(E=0\) root the rigging integral diverges as \(1/\sqrt{2\epsilon}\) and the clock
  Faddeev--Popov determinant vanishes. The massless decompactification limit also loses trace class.
- The runnable catalog is now 54; the mapped reproduction ledger remains 14 cases.

See
[`../cpt_temporal_folded_susy/PHASE23_HOMOGENEOUS_MINISUPERSPACE_DENSITY.md`](../cpt_temporal_folded_susy/PHASE23_HOMOGENEOUS_MINISUPERSPACE_DENSITY.md)
and
[`../cpt_temporal_folded_susy/phase23_homogeneous_minisuperspace_density.py`](../cpt_temporal_folded_susy/phase23_homogeneous_minisuperspace_density.py).

## Research ontology memory

Phase 15R–34 is now indexed in a repository-local typed research graph with **476 nodes and 1214 directed
relations**. It preserves 115 claims, 69 evidence groups, 37 explicit scopes, 41 open problems, 63
literature sources, the Phase 16–34 run payloads (328 named exact checks, 158 typed numerical checks, and
one separately recorded legacy Phase-18 numerical control), 62/62 verified artifact and policy hashes,
and cautious bridges to
the older SYMPOSIUM KG.

- [`../ontology/cpt-temporal-folded-susy/README.md`](../ontology/cpt-temporal-folded-susy/README.md)
  is the human concept map.
- [`../ontology/cpt-temporal-folded-susy/graph.json`](../ontology/cpt-temporal-folded-susy/graph.json)
  is the machine-readable record.
- `./ice ontology validate` checks IDs, endpoints, claim/evidence polarity, source and scope shape,
  persisted check IDs, artifact/policy hashes, and bridge syntax.
- `./ice ontology show <id>` and `./ice ontology trace <id>` expose the result without scanning every
  phase report.

This layer is memory and navigation, not a new research contract, scientific ratification, or automatic
external-KG write. A `RELATED` bridge is not identity, and unresolved external mappings remain explicit.

## Current direct calculation — CPT × Temporal-Folded SUSY Phase 24

Phase 24 adds a connected real Starobinsky $S^3\times I$ minisuperspace control. Its executable returns
exit 0 with **6 exact checks and 14 numerical checks**.

- The explicitly supplied calibration $\phi_{\rm center}=1$, $T_0=0.7$ gives
  $q_0=(3.56680319,1.01858095,3.56680319,1.01858095)$ and
  $I_0=1.40669054283430$. These inputs are not an initial-value selection rule.
- Constraint-preserving endpoint variations solve the proper length as a modulus. The connected mixed
  Hessian has singular values $(1902.725436,1.3\times10^{-9})$ after fourth-order Richardson control;
  the small value converges away and the Hamilton--Jacobi flow vectors are its null directions.
- Holding $T=0.7$ fixed instead gives a full-rank mixed spectrum $(1297.02951,613.38930)$. Rank one is
  therefore a constraint-reduction result, not a consequence of connectedness alone.
- The complete boundary Hessian has two negative eigenvalues, and the real-contour scalar Schur
  complement is indefinite. The fixed-scale precision coupling is $+0.2563195$, while the position
  covariance correlation is $-0.2563195$. The $0.0875594$-nat Gaussian diagnostic is not a physical
  gravitational entropy without a contour, boundary factorization, physical measure, and trace test.
- The live runnable catalog rose to 55 at Phase 24. The machine ontology now indexes the frozen Phase 24
  evidence snapshot and its scoped claim/evidence/source/open-problem traces.

See
[`../cpt_temporal_folded_susy/PHASE24_CONNECTED_STAROBINSKY_INTERVAL.md`](../cpt_temporal_folded_susy/PHASE24_CONNECTED_STAROBINSKY_INTERVAL.md)
and
[`../cpt_temporal_folded_susy/phase24_connected_starobinsky_interval.py`](../cpt_temporal_folded_susy/phase24_connected_starobinsky_interval.py).

## Current direct calculation — CPT × Temporal-Folded SUSY Phase 25

Phase 25 uses the full off-constraint Euler–Lagrange system and returns exit 0 with **5 exact checks and
12 numerical checks**.

- The fixed Phase-24 boundaries give a lapse saddle at $T_*=0.7$, with
  $W_T=0$ and $W_{TT}=-8.9231430383$. The real direction is locally nonconvergent for $e^{-W}$;
  the recorded constant-phase descent segment leaves in the imaginary direction.
- The symmetric $5\times5$ $(q,T)$ Hessian reduces by a lapse Schur complement to the independently
  computed constrained Phase-24 Hessian with relative error $7.01\times10^{-11}$.
- The base fixed-$T$ Jacobi map is nonsingular, so its constrained rank loss is not a caustic.
- The tracked real reflection-symmetric branch reaches a corank-one simple fold at
  $T_c=9.7886255681$. Two real roots at $T=9.78$ and both fold transversality conditions were checked.
- This does not fix the original lapse contour, global intersection number, FP measure, physical bulk
  Morse index, or a positive WDW/SUGRA seam state. The runnable catalog rose to 56 at this phase; the
  current ontology now freezes its Phase 25 snapshot together with the later Phase 26–29 records.

See
[`../cpt_temporal_folded_susy/PHASE25_CONNECTED_LAPSE_SCAN.md`](../cpt_temporal_folded_susy/PHASE25_CONNECTED_LAPSE_SCAN.md)
and
[`../cpt_temporal_folded_susy/phase25_connected_lapse_scan.py`](../cpt_temporal_folded_susy/phase25_connected_lapse_scan.py).

## Current direct calculation — CPT × Temporal-Folded SUSY Phase 26

Phase 26 returns exit 0 with **4 exact checks and 9 numerical checks**.

- The upper constant-phase complex-lapse arm continues through its projected
  $\operatorname{Im}T$ turn over the recorded bounded domain, with increasing $\operatorname{Re}W$ and
  constant $\operatorname{Im}W$ to the stated tolerances.
- No monitored scale zero or homogeneous complex Dirichlet Jacobi zero appears on that bounded arm.
- The real reflection-symmetric branch ends at the Phase-25 simple Dirichlet fold and obeys the expected
  square-root splitting and Airy uniformization. The fold is a field-saddle projection caustic, not a
  second stationary point of the lapse integral.
- This does not determine the arm's global endpoint, the original-cycle intersection coefficient, the
  complete determinant, or a physical state. The live committed catalog rose to 57 at this phase.

See
[`../cpt_temporal_folded_susy/PHASE26_GLOBAL_LAPSE_FLOW.md`](../cpt_temporal_folded_susy/PHASE26_GLOBAL_LAPSE_FLOW.md)
and
[`../cpt_temporal_folded_susy/phase26_global_lapse_flow.py`](../cpt_temporal_folded_susy/phase26_global_lapse_flow.py).

## Current direct calculation — CPT × Temporal-Folded SUSY Phase 27

Phase 27 returns exit 0 with **13 exact checks and 8 numerical checks**.

- The declared continuation $N_L=-iT_E$ maps positive Lorentzian lapse to
  $T_E\in i\mathbb R_+$; the positive-real Euclidean axis is not that contour.
- A positive lapse half-line produces a sourced resolvent, not the full-line group-averaging
  distribution. Equal-boundary short-time checks reproduce the stated raw action and canonical
  constraint limits.
- The fixed-$T$ endpoint Jacobi map scales as $B_v\sim T\mathbf1$, so the raw two-coordinate Van Vleck
  magnitude diverges as $1/|T|$. Contact at zero lapse is therefore not an ordinary transverse interior
  intersection.
- The global Picard--Lefschetz coefficient and a finite full gauge-reduced kernel remain open. The live
  committed catalog rose to 58 at this phase.

See
[`../cpt_temporal_folded_susy/PHASE27_LORENTZIAN_LAPSE_ENDPOINT.md`](../cpt_temporal_folded_susy/PHASE27_LORENTZIAN_LAPSE_ENDPOINT.md)
and
[`../cpt_temporal_folded_susy/phase27_lorentzian_lapse_endpoint.py`](../cpt_temporal_folded_susy/phase27_lorentzian_lapse_endpoint.py).

## Current direct calculation — CPT × Temporal-Folded SUSY Phase 28

Phase 28 returns exit 0 with **10 exact checks and 9 numerical checks**.

- Pseudo-arclength continuation carries the recorded upper constant-phase arm past its projected turn;
  the monitored bounded branch remains regular. Constructed two-sided vertical segments cross the
  recorded real dual branch once, but these are bounded crossings rather than a global relative-homology
  coefficient for the physical positive-lapse contour.
- In the Euclidean-continued homogeneous BFV--BRST control, the reduced Abelian constraint has a
  nilpotent charge. Dirichlet ghosts have no zero mode, yet proper length remains a global modulus after
  auxiliary elimination; the negative $W_{TT}$ direction is therefore not removed as a ghost-cancelled
  gauge zero mode within this reduction.
- The displayed local rotated Gaussian factor is conditional on a nonzero global thimble coefficient.
  A complete conformal/lapse contour, inhomogeneous boson--fermion--gravitino--ghost determinant,
  positive density, Pin lift, and soft SUSY spectrum remain open.
- A bounded string-completion design route is
  $\text{BFV seam candidate}\to\text{CPT/Pin completion}\to
  \text{double-three-form }N=1\text{ SUGRA}\to\text{flux selection}
  \to F\ne0\to\text{soft terms}$. A \(D\)-term branch needs an additional vector/gauging sector.
  String/M-theory can supply flux quantization, charged-membrane
  transitions, soft-term maps, and modular UV constraints; it does not derive the temporal seam or
  sector prior and does not guarantee this saddle survives compactification.
- The committed runnable catalog is now 59.

See
[`../cpt_temporal_folded_susy/PHASE28_THIMBLE_BFV_INTERSECTION.md`](../cpt_temporal_folded_susy/PHASE28_THIMBLE_BFV_INTERSECTION.md)
and
[`../cpt_temporal_folded_susy/phase28_thimble_bfv_intersection.py`](../cpt_temporal_folded_susy/phase28_thimble_bfv_intersection.py).

## Current direct calculation — CPT × Temporal-Folded SUSY Phase 29

Phase 29 returns exit 0 with **18 exact checks and 7 numerical checks**.

- For the frozen leading quadratic real-lapse kernel, pairing with endpoint test functions under the
  declared local flat $da\,d\phi$ measure gives
  $K_{N\to0}=\delta^{(2)}_{\rm flat}$. The diagonal $1/N$ growth is the normalization of this identity
  distribution in the stated scope, not by itself a removable infinity or a probability divergence.
- In the fixed-$s$ reduced open-interval BFV normalization, the Dirichlet-ghost determinant and
  coordinate Jacobian leave the proper-length modulus measure proportional to $dT$. The ghost does not
  cancel the pointwise pole.
- Multiplying the measure by $N$ changes the positive-half-line sourced resolvent from a simple to a
  double pole and changes the full-line group average from $\delta(H)$ to $\delta'(H)$. It is therefore
  a different operator prescription, not an endpoint renormalization of the same construction.
- The frozen homogeneous kinetic form has one negative and one positive eigenvalue. Either sign of an
  imaginary lapse damps one direction and amplifies the other, so a simultaneous conformal-field/lapse
  cycle is required.
- This is not a physical WDW endpoint measure, interacting all-orders uniform kernel, conformal cycle,
  complete boson--fermion--gravitino--ghost determinant, quantum state, or global PL coefficient. The
  committed runnable catalog is now 60.

See
[`../cpt_temporal_folded_susy/PHASE29_ZERO_LAPSE_UNIFORM_KERNEL.md`](../cpt_temporal_folded_susy/PHASE29_ZERO_LAPSE_UNIFORM_KERNEL.md)
and
[`../cpt_temporal_folded_susy/phase29_zero_lapse_uniform_kernel.py`](../cpt_temporal_folded_susy/phase29_zero_lapse_uniform_kernel.py).

## Current direct calculation — CPT × Temporal-Folded SUSY Phase 30

Phase 30 returns exit 0 with **10 exact checks and 10 numerical checks**.

- The frozen finite-cutoff joint field–lapse Hessian does not become convergent under the tested
  standard product of independent field and lapse rotations: one negative real direction remains at
  every recorded cutoff.
- Completing the square instead gives the fibered tangent cycle
  $\delta T=iu$, $\eta=R\xi-iu\mathcal O_D^{-1}j$. Its mixed block vanishes numerically and its real
  Gaussian quadratic form is positive over the tested finite cutoffs.
- In one explicitly declared hybrid midpoint calibration, the relative magnitude approaches the
  endpoint Jacobi/Van Vleck value $1.015026557031$. This is not an absolute zeta determinant. The bare
  field-determinant sign alternates with odd/even cutoff parity, so the continuum determinant-line phase
  remains open.
- A scalar holomorphic $1/N$ prefactor has the wrong identity-kernel sign on the negative real-lapse
  side compared with $1/|N|$. Two shifted rays sharing a pointwise open limit does not determine the
  singular endpoint bypass or a global intersection number.
- The executable contains no full BFV phase-space ghost/gauge super-Hessian, nonlinear continuum
  thimble, inhomogeneous superdeterminant, physical endpoint measure, quantum state, or integer PL
  coefficient. The committed runnable catalog is now 61.

See
[`../cpt_temporal_folded_susy/PHASE30_CONFORMAL_BFV_DETERMINANT_LINE.md`](../cpt_temporal_folded_susy/PHASE30_CONFORMAL_BFV_DETERMINANT_LINE.md)
and
[`../cpt_temporal_folded_susy/phase30_conformal_bfv_determinant_line.py`](../cpt_temporal_folded_susy/phase30_conformal_bfv_determinant_line.py).

## Current direct calculation — CPT × Temporal-Folded SUSY Phase 31

Phase 31 returns exit 0 with **9 exact checks and 11 numerical checks**.

- Exact momentum elimination reproduces the Phase-30 configuration-plus-global-lapse Hessian from the
  declared unreduced canonical `(q,p,T)` midpoint system.
- The unreduced proper-time-gauge canonical determinant sign is positive over all recorded odd and even
  cutoffs. This does not determine the momentum-contour orientation or physical determinant line.
- Each nonzero homogeneous alpha=0 BFV gauge/ghost quartet is background-independent in the stated
  finite-dimensional factorization and drops out of a same-hybrid-regulator benchmark/reference ratio.
  No absolute Gaussian phase, ghost normalization, or zero-mode measure is assigned.
- The bare full bosonic BFV block still has an odd/even gauge-pair parity sign. The bounded `p_a` clock
  scan is locally regular, but changing the endpoint polarization produces a nonzero Legendre term.
- “Super-Hessian” denotes the BFV Z2 gauge/ghost grading, not a SUSY/SUGRA Hessian. No physical
  probability, global PL coefficient, or SUGRA seam state is obtained. The committed runnable catalog
  is now 62.

See
[`../cpt_temporal_folded_susy/PHASE31_HOMOGENEOUS_BFV_SUPERHESSIAN.md`](../cpt_temporal_folded_susy/PHASE31_HOMOGENEOUS_BFV_SUPERHESSIAN.md)
and
[`../cpt_temporal_folded_susy/phase31_homogeneous_bfv_superhessian.py`](../cpt_temporal_folded_susy/phase31_homogeneous_bfv_superhessian.py).

## Current direct calculation — CPT × Temporal-Folded SUSY Phase 32

Phase 32 returns exit 0 with **14 exact checks and 7 numerical checks**.

- The causal positive-lapse half-line is a sourced resolvent. Its lower-lateral regulator meets the
  recorded positive-real upward dual only at the contour endpoint, so no ordinary transverse
  intersection integer is assigned.
- For the independently declared full real lapse contour bypassing zero from below, every recorded
  finite radius has one projected lapse-base crossing at `T=r`. Its coordinate sign is positive only
  under the declared ambient, column, dual-flow, and Gaussian-lift orientations. The connected complex
  BVP was evaluated at five angles on each of four lower arcs with no Jacobi zero at those samples.
- The declared signature-(-,+) principal momentum rays are locally decaying, but analytic `C/N`
  transport does not by itself reproduce the independently normalized negative-real `C/|N|` kernel;
  additional orientation-line gluing is required; it is not derived as a Maslov index.
- The signed full-joint local intersection and global coefficient are both unassigned. Other
  upward-cycle pieces, unsampled arc segments, complex sheets, good ends, Stokes data, determinant-line
  trivialization, and the oriented inhomogeneous superdeterminant remain open.
- Complex conjugation exchanges lower and upper lateral loci. CPT/Pin does not yet select the
  below-origin ket contour, and no positive trace-class physical state is derived. The committed
  runnable catalog is now 63.

See
[`../cpt_temporal_folded_susy/PHASE32_BELOW_ORIGIN_LAPSE_INTERSECTION.md`](../cpt_temporal_folded_susy/PHASE32_BELOW_ORIGIN_LAPSE_INTERSECTION.md)
and
[`../cpt_temporal_folded_susy/phase32_below_origin_lapse_intersection.py`](../cpt_temporal_folded_susy/phase32_below_origin_lapse_intersection.py).

## Current direct calculation — CPT × Temporal-Folded SUSY Phase 33

Phase 33 returns exit 0 with **8 exact checks and 7 numerical checks**.

- The Phase-25 real Dirichlet caustic at $T_c=9.78862556808$ is a transverse simple fold. Two actual
  fixed-boundary branches were resolved down to $\delta=T_c-T=2\times10^{-4}$.
- Their action gap approaches $|\Delta W|=93.0272\,\delta^{3/2}$, giving the invariant local action-scale
  magnitude $\zeta_{\rm act}=16.94783\,\delta+o(\delta)$. The soft Jacobi singular value scales as
  $\sqrt\delta$, the endpoint determinants have opposite signs, and separate Van Vleck proxies diverge
  as $\delta^{-1/4}$.
- This separate-saddle divergence does not force divergence in the canonical Airy fold normal form.
  It also does not prove the uncomputed physical kernel finite: the analytic amplitude, measure,
  superdeterminant, and absolute phase remain absent.
- Local regularity does not select a unique kernel. Both $\operatorname{Ai}$ and $\operatorname{Bi}$ are
  regular at the fold and have Wronskian $1/\pi$; the original relative cycle must still fix the
  contour/Stokes combination, separately from the even/odd analytic-amplitude data.
- The fold has $W_T=-73.72585376\ne0$ and is not another lapse saddle. Its radius-one $T$-plane chart is
  disjoint from the imaginary-axis full-lapse contour and every recorded Phase-32 bypass with
  $r\le0.1$, so it adds no local crossing there. Dual arms outside that chart remain uncomputed.
- The committed runnable catalog is now 64. The complete global $n_\sigma$, gauge-reduced uniform
  kernel, determinant line, physical WDW product, and trace-class seam state remain open.

See
[`../cpt_temporal_folded_susy/PHASE33_FOLD_AIRY_UNIFORMIZATION.md`](../cpt_temporal_folded_susy/PHASE33_FOLD_AIRY_UNIFORMIZATION.md)
and
[`../cpt_temporal_folded_susy/phase33_fold_airy_uniformization.py`](../cpt_temporal_folded_susy/phase33_fold_airy_uniformization.py).

## Current direct calculation — CPT × Temporal-Folded SUSY Phase 34

Phase 34 returns exit 0 with **5 exact checks and 9 numerical checks**.

- A deterministic positive-$a_c$ orientation fixes the fold soft coordinate. Both actual real sheets
  have $W_T<0$ and the recorded projected dual direction sends them into the fold.
- The Phase-33 action-gap seed gives
  $\operatorname{Im}T=0.63089949\,\tau^{3/2}+O(\tau^{5/2})$ on the upper arm and
  $\operatorname{Im}u<0$; complex conjugation supplies the lower arm.
- On the frozen reflection-symmetric stationary family and declared flat complex-$T$ metric, the
  constant-$\operatorname{Im}W$ tangent is a positive reparametrization of
  $dT/ds=-\overline{W_T}$. Independently re-solved centered differences agree with the
  Hamilton--Jacobi slope to a largest normalized difference of $1.29\times10^{-6}$.
- The upper complex boundary-value branch is continued through
  $T=13+2.89138959974i$. All fourteen frozen endpoint reintegrations pass; the smallest sampled
  endpoint-Jacobi singular value is $0.05780$.
- Because the bounded chart has $\operatorname{Re}T>T_c>9.7$, neither conjugate lapse base meets the
  Phase-32 imaginary axis or its $r\le0.1$ endpoint caps. This is not a census of uncontinued arms,
  other sheets, unsampled Jacobi zeros, or good ends.
- The committed runnable catalog is now 65. The full joint field--lapse metric and flow, oriented Airy
  connection and determinant line, complete relative cycles, global $n_\sigma$, gauge-reduced kernel,
  and physical trace-class state remain open.

See
[`../cpt_temporal_folded_susy/PHASE34_DIRECTED_FOLD_DUAL_CONTINUATION.md`](../cpt_temporal_folded_susy/PHASE34_DIRECTED_FOLD_DUAL_CONTINUATION.md)
and
[`../cpt_temporal_folded_susy/phase34_directed_fold_dual_continuation.py`](../cpt_temporal_folded_susy/phase34_directed_fold_dual_continuation.py).

## Historical scientific ledger

The rows below summarize previously committed outputs and audits. They are historical evidence, not a
current execution policy and not proof that similarly named KG nodes exist.

| Topic | Source | Historical evidence relation / caveat |
|---|---|---|
| 42 sedenion assessors / 84 ZD pairs | `research/hypercomplex/prove_higgs_results.json` | supports the L1 combinatorial count; does not by itself support a Higgs referent |
| S3 Jacobi/associator structure | `research/hypercomplex/prove_s3_results.json` | structural algebra result |
| S5 BV bounded result | `research/hypercomplex/prove_s5_results.json` | structural/numerical consistency result |
| Der(S) dimension 14 computation | sedenion result corpus | local numerical result; external review and precise method provenance remain separate |
| mass-ratio derivation | `research/legacy_predictions/derive_mass_ratios_results.json` | script self-report says 0/15 genuine |
| L-star derivation | `research/legacy_predictions/derive_Lstar_results.json` | script self-report says it does not uniquely predict L-star |
| naive custodial construction | queue02 result corpus | structural closure diagnostics contradict the proposed construction |
| Koide-like matches | `research/legacy_predictions/derive_dimensionless_results.json`, numerology judge | historical null scan found high coincidence risk |
| mp/mW search | `verify_mp_mW_results.json`, numerology judge | literal mismatch and high look-elsewhere coincidence risk |
| queue03 threshold scan | `research/hypercomplex/queue_03_threshold_sensitivity_results.json` | invalid as a portable pass/fail metric because of basis dependence |
| queue08 projected g2 claim | queue08 diagnostics | method-artifact warning: projected/non-alternative construction did not establish the claimed Lie representation |
| queue09 group action | queue09 result corpus | earlier orbit-membership test was too permissive; multiplication-preservation gate remains needed |

### Workbench reframe

The 2026-05-18 position treats ICE as a `HypercomplexHypothesisTestbench`, not a completed
`PhysicsTheoryProgramme`:

- L1 algebra results may be useful independently.
- L2/L3 physical interpretations remain a separate tested belt and require external discriminators.
- User-primary mythology remains a separate narrative layer.

Historical wording such as “L1 progressive / L2-L3 stagnant” is a checkpoint assessment of those
declared fibers, not a label to recompute after every script. Statements must disclose their layer.

## Known limitations and bounded follow-ups

1. Queue03 needs a separately versioned, independently checked, basis-invariant method. A candidate must check
   closure, nondegeneracy, and combined rank before evaluating cross-commutation; the existing ledger is
   quarantined rather than silently rewritten.
2. Queue09 needs a multiplication-preservation criterion before a group-theoretic interpretation.
3. Several historical result schemas and names differ from the live CLI; new kernels should use stable
   JSON types and cheap imports.
4. Local typecheck/tests exist, but scheduled remote reproduction is a separate operational task.
5. External peer review and formalization are separate projects; this repository cannot self-ratify them.

Each item is a bounded follow-up candidate. None automatically opens a child cycle or changes canon.
