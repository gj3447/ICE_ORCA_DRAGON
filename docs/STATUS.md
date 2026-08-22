# ICE_ORCA_DRAGON status

> Current engineering/reproduction state followed by a bounded historical scientific ledger. This file
> reports evidence; it does not authorize KG or canon mutation.

## Current state — 2026-08-22

| Component | State |
|---|---|
| Runnable catalog | 79 committed entries; `./ice list --json` is authoritative for the working tree |
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

Phase 15R–43 is indexed in a repository-local typed research graph with **607 nodes and 1717 directed
relations**. It preserves 149 claims (81 `SUPPORTED`, 67 `CONTRADICTED`, 1 `INCONCLUSIVE`) and the
Phase 16–43 run payloads: 425 named exact checks, all `PASS`, and 252 current typed numerical checks,
split as 247 `PASS`, 4 `FAIL`, and 1 `INCONCLUSIVE`. Including the separately catalogued passing legacy
Phase-18 control gives 253 typed numerical checks, split as 248 `PASS`, 4 `FAIL`, and 1 `INCONCLUSIVE`.
The graph contains 98 artifacts, 89 evidence nodes, 29 phases, and 46 scopes; all 102 recorded hashes
validate (98 artifacts and 4 policies), with 26 declared validation warnings. It also preserves cautious
bridges to the older SYMPOSIUM KG.

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

Phase 34 returns exit 0 with **5 exact checks and 10 numerical checks**.

- A deterministic positive-$a_c$ orientation fixes the fold soft coordinate. Both actual real sheets
  have $W_T<0$ and the recorded projected dual direction sends them into the fold.
- Using the Phase-33 finite-resolution seed estimator $\kappa=0.63089949$, the smallest recorded
  ratio is $\operatorname{Im}T/\tau^{3/2}=0.63089664$ and the recorded fit gives
  $p=1.49986759$ for $\operatorname{Im}T\propto\tau^p$ on the upper arm, with
  $\operatorname{Im}u<0$. These samples are consistent with the $3/2$ fold law; they are not an
  error-certified asymptotic limit. Complex conjugation supplies the lower-arm control.
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
- The committed runnable catalog at Phase 34 is 65. The full joint field--lapse metric and flow, the
  incoming-to-outgoing Airy relative-cycle connection, a separately oriented determinant line,
  complete relative cycles, global $n_\sigma$, gauge-reduced kernel, and physical trace-class state
  remain open.

See
[`../cpt_temporal_folded_susy/PHASE34_DIRECTED_FOLD_DUAL_CONTINUATION.md`](../cpt_temporal_folded_susy/PHASE34_DIRECTED_FOLD_DUAL_CONTINUATION.md)
and
[`../cpt_temporal_folded_susy/phase34_directed_fold_dual_continuation.py`](../cpt_temporal_folded_susy/phase34_directed_fold_dual_continuation.py).

## Current direct calculation — CPT × Temporal-Folded SUSY Phase 35

Phase 35 returns exit 0 with **6 exact checks and 8 numerical checks**.

- In the declared endpoint order, $B_v=M_{(a,\phi),(\dot a,\dot\phi)}$ has nonzero determinant at all
  57 sampled upper-branch points from $\tau=2\times10^{-6}$ through $\operatorname{Re}T=13$.
- Recursive principal-increment unwrapping gives relative determinant and square-root sections on the
  recorded table; the alternative sampled lift differs by an overall sign, which these data do not select.
- In the frozen upper-fold orientation, the recorded samples are finite-resolution consistent with
  $\det B_v=-iC_{\rm det}\sqrt\tau+O(\tau)$ and $C_{\rm det}>0$. Six separate conjugate-input integrations
  verify the conjugate section, and the reduced bosonic endpoint phases cancel relatively.
- This does not prove a zero-free continuum interpolation or a $\tau\to0$ limit. The endpoint-Jacobi
  determinant is not yet the physical Van Vleck factor or a full Gaussian
  prefactor. The correct canonical block and measure, absolute sign/Maslov orientation,
  incoming-to-outgoing fold connection, full BFV/SUGRA superdeterminant, global $n_\sigma$, and physical
  state remain open.

See
[`../cpt_temporal_folded_susy/PHASE35_REDUCED_DETLINE_TRANSPORT.md`](../cpt_temporal_folded_susy/PHASE35_REDUCED_DETLINE_TRANSPORT.md)
and
[`../cpt_temporal_folded_susy/phase35_reduced_detline_transport.py`](../cpt_temporal_folded_susy/phase35_reduced_detline_transport.py).

## Current direct calculation — CPT × Temporal-Folded SUSY Phase 36

Phase 36 returns exit 0 with **12 exact checks and 9 numerical checks**. In separately declared CW and
CCW local Airy bases it fixes the three-ray and Ai/Bi arm relations, the cycle-basis and inverse-transpose
formal dual-basis identities, the lateral Stokes convention, a declared leading-fold half-phase, and a
conditional soft/hard determinant bookkeeping identity. The first duals in the two bases are distinct
lateralized basis elements, not two transports of one common incoming physical upward dual.

At three finite semicircle radii, twelve prescribed-complex-$T$ BVP paths realize two distinct conjugate
root-sheet laterals, both of which pass the sampled endpoint, action-gap, and determinant gates. The
recorded local gates alone are therefore insufficient to select upper versus lower. Transport of one
common dual, the complete original relative cycle and global contour/homotopy choice, regular hard
determinant quotient and CFU coefficients, absolute signs and Maslov orientation, unsampled zeros and
other sheets, full joint field--lapse/BFV superdeterminant, global $n_\sigma$, and a physical state remain
open.

See
[`../cpt_temporal_folded_susy/PHASE36_AIRY_GAUSS_MANIN_CONNECTION.md`](../cpt_temporal_folded_susy/PHASE36_AIRY_GAUSS_MANIN_CONNECTION.md)
and
[`../cpt_temporal_folded_susy/phase36_airy_gauss_manin_connection.py`](../cpt_temporal_folded_susy/phase36_airy_gauss_manin_connection.py).

## Current direct calculation — CPT × Temporal-Folded SUSY Phase 37

Phase 37 returns exit 0 with **18 exact checks and 8 numerical checks**. It replaces the separately
trivialized open-lateral comparison by same-basepoint closed continuation of both BVP roots around the
recorded simple fold. On three finite enclosing radii the one-turn root map is $P^2=I$. Conditional on
the thirteen-angle minimal-jump determinant tables having no unresolved intersample zero or alias
winding, the sampled reduced half-form has

\[
\operatorname{tr}L=0,
\qquad \det L=1,
\qquad L^2=-I.
\]

An uninterrupted 97-point $4\pi$ continuation returns the same root with inverse-square-root
transport $-0.999999999993$; a nearby nonenclosing loop returns the root and half-form with $+1$.
The exact typed controls distinguish this root/determinant local system from the entire Airy solution,
relative-cycle Gauss--Manin map, Stokes map, fermion Pfaffian, and Pin lift. Bare root swap also commutes
with the Phase-17 parity-controlled basis change, so it does not by itself make the exchange charge
physical.

The original lapse-field relative cycle and signed intersections, hard CFU coefficients, intersample
continuum theorem, all modes and good ends, absolute Maslov/Pfaffian orientation, spacetime Pin data,
full BFV/SUGRA operator and cohomology, conserved spinorial supercharge, persistent order parameter,
pole splitting, and physical state remain open.

See
[`../cpt_temporal_folded_susy/PHASE37_CLOSED_FOLD_HOLONOMY.md`](../cpt_temporal_folded_susy/PHASE37_CLOSED_FOLD_HOLONOMY.md)
and
[`../cpt_temporal_folded_susy/phase37_closed_fold_holonomy.py`](../cpt_temporal_folded_susy/phase37_closed_fold_holonomy.py).

## Previous direct calculation — CPT × Temporal-Folded SUSY Phase 38

Phase 38 returns exit 0 with **15 exact checks and 6 numerical checks**. Its exact finite surrogate is a
typed warning about omitted information: it does **not** prove that the actual physical projection on
gravitational relative homology is noninjective. Rather, the recorded projected crossing and local-root
data contain neither an injectivity theorem nor explicit admissible joint-cycle completions, so they do
not license inverse reconstruction of the original joint cycle.

In the declared local cycle basis, coefficient transport is $c_{\rm out}=G^T c_{\rm in}$, not the root
permutation $P$. The conditional input $c_{\rm in}=(1,0)^T$ maps to $(-1,-1)^T$; treating $P$ as the
cycle map would instead fabricate $(0,1)^T$, and a typed mutation control rejects that substitution.
This is a local-basis representation, not a physical thimble vector or global intersection coefficient.

Numerically, the known conjugate stationary-family arms are sampled from the previous
$\operatorname{Re}T=13$ bound through $\operatorname{Re}T=16$. Two continuation step sizes agree on the
endpoint basin, and the recorded checkpoints show no endpoint-Jacobi zero or projected crossing with
the Phase-32-declared full-line lapse-base candidate. This bounded ledger neither classifies the origin
or two box exits as relative good ends nor enumerates all sheets and arms. Consequently
`full_joint_local_sign`, `complete_global_signed_vector`, and `global_n_sigma` are all `null`; Gate 1
remains open.

Exploratory computation of the regular hard quotient and CFU coefficients $A,B$ may proceed in parallel
with Gate 1. Only assembling and promoting those data as a physical uniform kernel depends on the
missing original cycle vector and signed intersections.

See
[`../cpt_temporal_folded_susy/PHASE38_JOINT_CYCLE_IDENTIFIABILITY.md`](../cpt_temporal_folded_susy/PHASE38_JOINT_CYCLE_IDENTIFIABILITY.md)
and
[`../cpt_temporal_folded_susy/phase38_joint_cycle_identifiability.py`](../cpt_temporal_folded_susy/phase38_joint_cycle_identifiability.py).

## Previous direct calculation — CPT × Temporal-Folded SUSY Phase 39

Phase 39 returns exit 0 with **12 exact checks and 17 numerical checks**. It reads a separately committed
post-feasibility input freeze and constructs the nonlinear two-segment midpoint action on
$\mathbb C^2\times\mathbb C_T^*$. All three joint critical equations and the Hessian are differentiated
from that same holomorphic SymPy scalar. The positive-$T$ discrete root is

$$
(a_1,\phi_1,T)_\sigma
=(3.59047203047,0.993462632204,0.816050882199),
$$

with maximum gradient residual $2.73\times10^{-12}$ and dimensionless-reference Hessian inertia
$(2_-,1_+)$. A bounded multiseed ledger also finds three other real roots, so neither uniqueness nor a
complete saddle census is claimed. All four recorded critical actions have zero imaginary part; a
lateral non-Stokes chamber remains required.

For one post-feasibility fixed positive Morse-whitened metric, the executable launches a linear Takagi
sphere and transports one finite-radius, finite-time three-real-dimensional upward-flow chart patch and
its variational tangent. Against two cap pieces of an independently endpoint-anchored lower-bypass
configuration chain, the full six-real-dimensional solves give:

| cap radius | max root residual | normalized $\sigma_{\min}$ | direct declared configuration-coordinate sign |
|---:|---:|---:|---:|
| 0.3 | $2.64\times10^{-9}$ | 0.0752060 | +1 |
| 0.2 | $3.48\times10^{-8}$ | 0.0696581 | +1 |

The sign is computed as $\operatorname{sgn}\det_{\mathbb R}[V_\Gamma,V_K]$, not reconstructed from the
Phase-32 lapse projection. The solver's actual finite-difference residual Jacobian has the opposite sign
and agrees with the positively row-scaled assembled $[V_\Gamma,-V_K]$ matrix at the recorded
$1.76\times10^{-3}$ and $1.07\times10^{-3}$ spectral relative levels. Orientation reversal and doubled
launch-radius controls preserve the expected local behavior.

This is a cap-piece local algorithm witness, not a bounded-chain intersection number. Straight-arm
intersections and later cap reintersections are not searched; a 54-direction cubed-sphere ledger is only
a non-exhaustive atlas smoke test; 21 samples leave the norm box. No exact nonlinear unstable manifold,
all-root/component/end census, Stokes jump, cutoff/metric/regulator/anchor stability, reflection-odd
history mode, BFV/Pfaffian/Pin orientation, or physical original relative cycle is established.
Accordingly `bounded_chain_signed_sum`, `complete_global_signed_intersection_vector`, and
`global_n_sigma` are all `null`, and Gate 1 remains open.

The next calculation was the same determinant API at $m=3$ with a signed endpoint-asymmetry mutation
to expose the first reflection-odd history mode.

See
[`../cpt_temporal_folded_susy/PHASE39_FINITE_JOINT_INTERSECTION.md`](../cpt_temporal_folded_susy/PHASE39_FINITE_JOINT_INTERSECTION.md)
and
[`../cpt_temporal_folded_susy/phase39_finite_joint_intersection.py`](../cpt_temporal_folded_susy/phase39_finite_joint_intersection.py).

## Previous direct calculation — CPT × Temporal-Folded SUSY Phase 40

Phase 40 returns exit 0 with **12 exact checks and 22 numerical checks**. It raises the finite-cutoff
configuration model to $m=3$, so the joint action has five complex variables and the local intersection
problem lives in ten real dimensions. One SymPy scalar generates the action, gradient, and Hessian;
exact checks cover their reflection covariance, the parity-adapted mode orientation, the root-Jacobian
sign convention, the holomorphic-flow identity, and fail-closed global outputs.

The signed endpoint mutation keeps $a_L=a_R$ and sets
$\phi_L=\phi_b-\delta/2$, $\phi_R=\phi_b+\delta/2$. It therefore probes one source direction in the
two-dimensional reflection-odd field sector, not the whole sector. At $\delta=0$, the saddle has inertia
$(3_-,2_+)$; the parity-adapted Hessian has odd eigenvalues approximately
$(-65208.7881,11360.4454)$ and even--odd cross-block norm $4.80\times10^{-12}$. The
anchor-subtracted odd response at $\delta=.001$ is nonzero.

With the $\delta=0$ positive mobility fixed and the signed spectral subspaces transported by Procrustes
alignment, five sequentially continued local candidates give:

| $\delta$ | max physical residual | normalized $\sigma_{\min}$ | direct declared-coordinate sign |
|---:|---:|---:|---:|
| $-.001$ | $6.05\times10^{-9}$ | 0.0906550 | +1 |
| $-.0005$ | $7.13\times10^{-9}$ | 0.0906768 | +1 |
| $0$ | $4.18\times10^{-9}$ | 0.0906841 | +1 |
| $+.0005$ | $1.14\times10^{-8}$ | 0.0906768 | +1 |
| $+.001$ | $4.80\times10^{-9}$ | 0.0906550 | +1 |

The endpoint-reflected candidates agree, three launch radii preserve the sign, and audited variational
tangents agree with finite-difference Jacobians in their recorded stable bands. A converged local fit
that clamps two K-launch coordinates has residual $3.98\times10^{-4}$ and does not reproduce the full
candidate at the $2\times10^{-7}$ tolerance. This is only a local coordinate-slice negative control,
not a full odd-sector ablation.

The five points do not prove a continuous determinant-nonzero branch, and the source has rank one.
There is still no straight-arm/reintersection census, exact nonlinear upward manifold, lateral Stokes
chamber, cutoff/metric/regulator independence, physical original relative cycle, or
BFV/Pfaffian/Pin orientation. Accordingly `bounded_chain_signed_sum`,
`complete_global_signed_intersection_vector`, and `global_n_sigma` remain `null`; Gate 1 remains open.

The next cutoff control was Phase 41 at $m=4$, with orientation matched to the lower cutoffs and an
independent $a$-only endpoint source alongside the $\phi$-only source.

See
[`../cpt_temporal_folded_susy/PHASE40_M3_REFLECTION_ODD_INTERSECTION.md`](../cpt_temporal_folded_susy/PHASE40_M3_REFLECTION_ODD_INTERSECTION.md)
and
[`../cpt_temporal_folded_susy/phase40_m3_reflection_odd_intersection.py`](../cpt_temporal_folded_susy/phase40_m3_reflection_odd_intersection.py).

## Previous direct calculation — CPT × Temporal-Folded SUSY Phase 41

Phase 41 returns exit 0 with **7/7 exact contracts and 8/9 typed numerical contracts**. Exit 0 denotes
a valid typed scientific run, not nine numerical passes: the sole negative record is
`P41.tangent.three_full_FD_controls = TANGENT_CONTROL_FAILED`. The calculation raises the same explicit
midpoint action to $m=4$, giving seven complex configuration variables and a full local intersection
problem in fourteen real dimensions. It uses one zero-source mobility and independent signed
$\phi$-only and $a$-only endpoint-source arms.

The anchor-subtracted two-source susceptibility has singular values approximately
$(0.00528567,0.00184589)$ and
$\sigma_{\min}/(10E_{\rm rank})=28.28$. This supports stable **numerical** rank two within the frozen
normalization; it is not an exact algebraic rank theorem. Shared zero and the four signed endpoints all
produce accepted local roots with full $7+7$ tangent ranks, normalized
$\sigma_{\min}\ge 0.08890$, direct declared-coordinate sign $+1$, and root-Jacobian sign $-1$.
The negative source arms are independently continued from the common zero. Reflection residuals are
at most $6.06\times10^{-12}$, and the radius, launch-shape, overlap-chart, and independently reintegrated
first-cap path controls pass.

At shared zero, $\phi+$, and $a+$, the finite-difference root signs and tangent-operator errors pass,
but the first adjacent finite-difference step pair has maximum relative plateau changes approximately
$0.299$, $0.222$, and $0.795$. The typed tangent contract therefore fails. The source-specific
$\phi$/$a$ robustness claims remain `INCONCLUSIVE_WITHIN_FROZEN_LOCAL_PROTOCOL`; repeated local $+1$
signs are not promoted through that failure.

No straight-arm or reintersection census, continuous-direction coverage, root exhaustion, exact
nonlinear upward manifold, common $m=2/3/4$ determinant line, physical original cycle, cutoff/continuum
limit, metric homotopy, or BFV/Pfaffian/Pin orientation has been computed. Six promoted outputs,
including the bounded-chain sum, global vector, global $n_\sigma$, cutoff limit, continuum limit, and
quantum-gravity explanation, remain `null`; all sixteen completion flags remain false and Gate 1 is
`OPEN_PARTIAL_PROGRESS`. The runnable catalog is now 72.

See
[`../cpt_temporal_folded_susy/PHASE41_M4_TWO_SOURCE_INTERSECTION.md`](../cpt_temporal_folded_susy/PHASE41_M4_TWO_SOURCE_INTERSECTION.md)
and
[`../cpt_temporal_folded_susy/phase41_m4_two_source_intersection.py`](../cpt_temporal_folded_susy/phase41_m4_two_source_intersection.py).

## Previous direct calculation — CPT × Temporal-Folded SUSY Phase 42

Phase 42 returns exit 0 with **8/8 exact contracts and 6/8 numerical contracts**. Exit 0 denotes
`VALID_TYPED_RUN`, not eight numerical passes. The two scientific non-PASS records are
`LOCAL_VARIATIONAL_IDENTITY_NOT_SUPPORTED` and
`REFERENCE_DERIVATIVE_OR_TANGENT_INCONCLUSIVE`; neither is rewritten as an infrastructure failure or
removed from the aggregate. The diagnostic consumes three immutable Phase-41 roots—shared-zero,
$\phi+$, and $a+$—without retuning a root, chart, sign, or finite-difference step.

The committed Phase-41 states, residuals, frames, and Jacobians are reproduced exactly in this run, and
the historical $u_2$ first-pair plateaus reappear at approximately 0.299, 0.222, and 0.795. At $\phi+$
and $a+$, the preselected fixed-$R_4$ references are stable and the production-to-tight discrepancy
grows as the old step shrinks. The complete tri-state ledger therefore supports both
`SOLVER_NOISE_EVIDENCE` and `STEP_PAIR_SELECTION_ARTIFACT` there. At shared-zero, the same trend is not
promoted because its fixed reference fails the prerequisite.

The all-column fixed-$R_4$ contract fails only at the shared-zero $u_2$ column: its internal-neighbor
stability is $5.97045\times10^{-3}$ against the frozen $5\times10^{-3}$ limit. Its direction, norm, and
whole-matrix comparisons remain small, so this is a reference-stability failure rather than a detected
sign reversal. Because the contract quantifies over all three roots, the Phase-42 reference tangent
remains `REFERENCE_DERIVATIVE_OR_TANGENT_INCONCLUSIVE`.

At each root, 29 of 30 local Hessian-action directions pass the reference-stability prerequisite. Among
them, 12, 11, and 10 respectively exceed the frozen $10^{-7}$ analytic-identity threshold. These stable
violations support the protocol-defined `VARIATIONAL_RHS_BUG_EVIDENCE` anomaly label at all three roots.
The label is not proof of a code defect, a faulty line, or a false continuum equation, and it is not a
unique-cause verdict. In particular, the Phase-41 time tangent is appended from the final augmented
endpoint rather than independently integrated. Its mismatch with state-only endpoints lies in the same
solver envelope, so it is explicitly excluded as independent bug evidence.

All three normalized $14\times14$ matrix pairs satisfy the sufficient $\eta<1$ nonsingular linear-
homotopy test, with $\eta$ between $4.03\times10^{-4}$ and $1.01\times10^{-3}$. This certifies only a
local path in the declared coordinate frames. It does not construct a determinant line, orient the full
upward cycle, identify the physical original contour, or repair the inconclusive reference tangent.

Six promoted outputs—including the bounded-chain sum, global vector, global $n_\sigma$, cutoff limit,
continuum limit, and quantum-gravity explanation—remain `null`; all sixteen completion flags remain
false. Global promotion is `PROHIBITED`, Gate 1 remains `OPEN_PARTIAL_PROGRESS`, and the runnable
catalog is now 74.

See
[`../cpt_temporal_folded_susy/PHASE42_M4_FIXED_ROOT_TANGENT_DISENTANGLEMENT.md`](../cpt_temporal_folded_susy/PHASE42_M4_FIXED_ROOT_TANGENT_DISENTANGLEMENT.md),
[`../cpt_temporal_folded_susy/phase42_m4_fixed_root_tangent_disentanglement.py`](../cpt_temporal_folded_susy/phase42_m4_fixed_root_tangent_disentanglement.py),
and
[`../cpt_temporal_folded_susy/PHASE42_M4_FIXED_ROOT_TANGENT_DISENTANGLEMENT_RESULT.json`](../cpt_temporal_folded_susy/PHASE42_M4_FIXED_ROOT_TANGENT_DISENTANGLEMENT_RESULT.json).

## Current direct calculation — CPT × Temporal-Folded SUSY Phase 43

Phase 43 returns exit 0 with **7/7 exact contracts and 4/6 numerical contracts**. Exit 0 denotes
`VALID_TYPED_RUN`, not six numerical passes. The two complete non-invalidating numerical `FAIL` records
retain the protocol's false universal predicates: source agreement fails because 13/90 NumPy64 outputs
cross the frozen tolerance, and the all-33 finite-difference rule fails because five disclosed anomalies
are complete exceptions.

The run consumes all 90 immutable Phase-42 $\xi,q$ slots—three points, five flow fractions, and six
directions—without root, state, direction, step, or threshold retuning. Independently rebuilt exact-
symbolic, direct-gradient, 80/120-decimal, unchanged-step, and prospective small-step paths corroborate
the local high-precision reference at 90/90 slots. Against that reference, 13 byte-pinned NumPy64
Hessian-action outputs exceed the frozen $5\times10^{-13}$ normwise threshold. This is operational
implementation-pipeline mismatch evidence only; it does not establish a wrong formula, one faulty code
line, or a unique cause.

The same-step binary64 finite-difference rule is supported at 28/33 disclosed Phase-42 anomalies:
9/12 at shared-zero, 11/11 at $\phi+$, and 8/10 at $a+$. The five exceptions make the frozen all-33
aggregate `NOT_SUPPORTED`; only $\phi+$ supports the pointwise all-disclosed-anomaly predicate. The
classifications are nonexclusive, so the failed aggregate does not mean binary64 finite-difference
error is absent.

No root, saddle, ODE, integrated tangent, time column, reference tangent, orientation, determinant line,
or global cycle is evaluated. Phase 41 therefore remains 8/9, and the Phase-42 reference tangent remains
`REFERENCE_DERIVATIVE_OR_TANGENT_INCONCLUSIVE`. Six promoted outputs and seven desired outputs remain
`null`; all sixteen completion flags remain false. Global promotion is `PROHIBITED`, Gate 1 remains
`OPEN_PARTIAL_PROGRESS`, and the runnable catalog is now 75.

See
[`../cpt_temporal_folded_susy/PHASE43_M4_HIGH_PRECISION_LOCAL_RHS_ARBITRATION.md`](../cpt_temporal_folded_susy/PHASE43_M4_HIGH_PRECISION_LOCAL_RHS_ARBITRATION.md),
[`../cpt_temporal_folded_susy/PHASE43_M4_HIGH_PRECISION_LOCAL_RHS_ARBITRATION_INPUTS.json`](../cpt_temporal_folded_susy/PHASE43_M4_HIGH_PRECISION_LOCAL_RHS_ARBITRATION_INPUTS.json),
[`../cpt_temporal_folded_susy/phase43_m4_high_precision_local_rhs_arbitration.py`](../cpt_temporal_folded_susy/phase43_m4_high_precision_local_rhs_arbitration.py),
and
[`../cpt_temporal_folded_susy/PHASE43_M4_HIGH_PRECISION_LOCAL_RHS_ARBITRATION_RESULT.json`](../cpt_temporal_folded_susy/PHASE43_M4_HIGH_PRECISION_LOCAL_RHS_ARBITRATION_RESULT.json).

## Current direct calculation — CPT × Temporal-Folded SUSY Phase 45

Phase 45 returns exit 0 with `VALID_RUN` and the fixed classification
`TANGENT_CONTROL_FAILURE_STABLE_TO_INDEPENDENT_RHS`. At the three immutable Phase-42 roots it integrates
the six chart-tangent columns along one source NumPy64 state trajectory using the Phase-41 NumPy64
Hessian action and independently rebuilt exact-decimal 50- and 80-digit Hessian actions.

The retained 50/80-digit tangent samples agree exactly after complex128 projection. The maximum
source/reference tangent discrepancy is `2.741e-12`, the maximum source/reference root-Jacobian
discrepancy is `3.748e-12`, and the independent Jacobians remain within `1.101e-5` of the Phase-42 R4
matrices with normalized sign `-1` at all three roots. Every one of the eighteen pre-output root-level
tests passes.

The historical Phase-41 `u2` plateau values remain `0.298850`, `0.221993`, and `0.795272`, above the
frozen `0.02` failure threshold. Phase 45 does not recompute that finite-difference ladder; it shows
that replacing the local tangent RHS does not materially change the integrated tangent or repair the
historical control. The unresolved local issue is therefore narrowed toward state-flow finite
differences, subtractive cancellation, solver truncation, or frozen step-pair selection.

No root search, retuning, orientation selection, determinant line, complete cycle, good-end census,
Stokes chamber, or global intersection is computed. Phase 41 stays 8/9, global promotion remains
`PROHIBITED`, Gate 1 remains `OPEN_PARTIAL_PROGRESS`, and the runnable catalog is now 77.

See
[`../cpt_temporal_folded_susy/PHASE45_M4_INTEGRATED_TANGENT_RHS_STABILITY.md`](../cpt_temporal_folded_susy/PHASE45_M4_INTEGRATED_TANGENT_RHS_STABILITY.md),
[`../cpt_temporal_folded_susy/PHASE45_M4_INTEGRATED_TANGENT_RHS_STABILITY_INPUTS.json`](../cpt_temporal_folded_susy/PHASE45_M4_INTEGRATED_TANGENT_RHS_STABILITY_INPUTS.json),
[`../cpt_temporal_folded_susy/phase45_m4_integrated_tangent_rhs_stability.py`](../cpt_temporal_folded_susy/phase45_m4_integrated_tangent_rhs_stability.py),
and
[`../cpt_temporal_folded_susy/PHASE45_M4_INTEGRATED_TANGENT_RHS_STABILITY_RESULT.json`](../cpt_temporal_folded_susy/PHASE45_M4_INTEGRATED_TANGENT_RHS_STABILITY_RESULT.json).

## Current direct calculation — CPT × Temporal-Folded SUSY Phase 46

Phase 46 returns exit 0 with `VALID_RUN` and the fixed classification
`LOCAL_FLOW_RHS_REPAIR_SUPPORTED`. At the same three immutable Phase-42 roots it consumes all 54
complete production/tight-DOP853/Radau endpoint slots from the byte-pinned Phase-42 result and newly
integrates eighteen signed endpoints with the independently reconstructed 80-digit local flow RHS.
All three historical `u2` steps (`2e-6`, `5e-7`, `1e-7`) and both signs are retained.

The independent path passes both adjacent-step plateau tests at every root; its largest plateau is
`2.019e-7` against the frozen `0.02` limit. Its finite-difference columns agree with the Phase-45
independent tangent columns to at worst `2.858e-7` against the `0.005` limit, and all 36 retained
50/80-digit local RHS probes agree exactly after final complex128 projection.

The source tight-DOP853 and Radau endpoints remain close to the independent endpoints, at worst
`3.022e-9` and `2.071e-9`. The small central differences amplify those endpoint deviations: tight
source columns differ by as much as `0.8701`, and Radau columns by as much as `0.02379`; both source
column aggregates cross the frozen `0.005` limit at all three roots. This supports local flow-RHS
repair under the declared projection, not a wrong-formula verdict or one unique coefficient/state/
gradient/solver/subtraction cause.

The historical Phase-41 result remains 8/9 as provenance. No root search, retuning, orientation
selection, determinant line, complete cycle, good-end census, Stokes chamber, or global intersection is
computed. Global promotion remains `PROHIBITED`, Gate 1 remains `OPEN_PARTIAL_PROGRESS`, and the runnable
catalog is now 78.

See
[`../cpt_temporal_folded_susy/PHASE46_M4_U2_STATE_MAP_FD_AUDIT.md`](../cpt_temporal_folded_susy/PHASE46_M4_U2_STATE_MAP_FD_AUDIT.md),
[`../cpt_temporal_folded_susy/PHASE46_M4_U2_STATE_MAP_FD_AUDIT_INPUTS.json`](../cpt_temporal_folded_susy/PHASE46_M4_U2_STATE_MAP_FD_AUDIT_INPUTS.json),
[`../cpt_temporal_folded_susy/phase46_m4_u2_state_map_fd_audit.py`](../cpt_temporal_folded_susy/phase46_m4_u2_state_map_fd_audit.py),
and
[`../cpt_temporal_folded_susy/PHASE46_M4_U2_STATE_MAP_FD_AUDIT_RESULT.json`](../cpt_temporal_folded_susy/PHASE46_M4_U2_STATE_MAP_FD_AUDIT_RESULT.json).

## Current direct calculation — CPT × Temporal-Folded SUSY Phase 47

Phase 47 returns exit 0 with `VALID_RUN` and the fixed classification
`LOCAL_SOURCE_GRADIENT_MIXED_ARITHMETIC_BUDGET_SUPPORTED`. It reuses the launch and endpoint states from
all eighteen independent Phase-46 `u2` paths and evaluates one frozen six-stage source-flow telescope at
all 36 states and after all 18 central-difference `1/(2h)` pairings. No new trajectory is integrated.

All 36 state telescopes and all 18 paired-derivative telescopes close. Their maximum component residuals
are `5.076e-116` and `1.363e-107`; independent 80/120-digit flow evaluations are identical after final
complex128 projection. The pinned Phase-41 `gradient_at` and `flow_xi` boundaries also reproduce bit for
bit, while the Phase-44 source/reference formula-mismatch state remains `NOT_SUPPORTED`.

The generated NumPy gradient-evaluation delta is the largest retained signed-stage norm at every state
and paired-derivative slot. Its maxima are `2.447e-11` and `9.823e-5`, compared with `1.139e-13` and
`5.350e-7` for state formation, `1.130e-16` and `3.640e-10` for contraction, negligible source-symbolic
deltas, and zero outer minus-conjugation deltas. This is descriptive localization, not proof of one
faulty suboperation: the stage still combines constant lowering, scalar operation order, elementary
functions, and NumPy rounding, and signed contributions can cancel.

Phase 47 therefore prioritizes a gradient-only, one-projection hybrid as the next integrated control but
does not validate that repair. Phase 46 retained no intermediate states, so intermediate error transport,
endpoint accumulation, and solver accumulation remain open. The historical Phase-41 result remains 8/9;
Phases 44 and 46 remain unchanged. No root search, orientation, determinant line, complete cycle, Stokes
chamber, or global intersection is computed. Global promotion remains `PROHIBITED`, Gate 1 remains
`OPEN_PARTIAL_PROGRESS`, and the committed runnable catalog is now 79.

See
[`../cpt_temporal_folded_susy/PHASE47_M4_SOURCE_GRADIENT_FLOW_ERROR_BUDGET.md`](../cpt_temporal_folded_susy/PHASE47_M4_SOURCE_GRADIENT_FLOW_ERROR_BUDGET.md),
[`../cpt_temporal_folded_susy/PHASE47_M4_SOURCE_GRADIENT_FLOW_ERROR_BUDGET_INPUTS.json`](../cpt_temporal_folded_susy/PHASE47_M4_SOURCE_GRADIENT_FLOW_ERROR_BUDGET_INPUTS.json),
[`../cpt_temporal_folded_susy/phase47_m4_source_gradient_flow_error_budget.py`](../cpt_temporal_folded_susy/phase47_m4_source_gradient_flow_error_budget.py),
and
[`../cpt_temporal_folded_susy/PHASE47_M4_SOURCE_GRADIENT_FLOW_ERROR_BUDGET_RESULT.json`](../cpt_temporal_folded_susy/PHASE47_M4_SOURCE_GRADIENT_FLOW_ERROR_BUDGET_RESULT.json).

## Current direct calculation — CPT × Temporal-Folded SUSY Phase 48

Phase 48 returns exit 0 with `VALID_RUN` and the fixed classification
`GRADIENT_ONLY_CLONGDOUBLE_STATE_MAP_REPAIR_NOT_SUFFICIENT`. On the pinned NumPy platform it integrates
all eighteen frozen `u2` paths after promoting only the generated gradient-callable evaluation to
`clongdouble`, then projecting that gradient once to complex128. Source state formation, `L.T`
contraction, DOP853, cap/residual, roots, and the three-step ladder remain fixed.

All eighteen integrations and ninety intermediate same-state local-flow probes complete. Every probe
passes `5e-8`, and every endpoint state agrees with the Phase-46 independent endpoint below `1e-8`;
the rootwise endpoint maxima are `2.060e-9`, `2.084e-10`, and `1.324e-10`. This records a material
normwise improvement from the gradient-stage ablation.

The complete derivative control nevertheless fails. Only `a_plus` passes both adjacent plateaus;
`shared_zero` reaches `0.02531` and `phi_plus` reaches `0.05583`, above `0.02`. Every root exceeds the
all-step `0.005` limit against both the Phase-46 independent columns and Phase-45 tangents, with maxima
from `0.008222` to `0.05208`. No failed step is dropped. The result is therefore a useful negative
control: a pinned-platform long-double gradient alone is not sufficient for the full `u2` ladder.

Phase 48 does not construct a formal endpoint propagator or separate state formation, contraction,
solver accumulation, and final subtraction. It does not rewrite Phase 41, weaken Phases 44–47, prove
one source formula defect, or establish a portable binary128 implementation. No root, orientation,
determinant line, complete cycle, Stokes chamber, or global intersection is computed. Global promotion
remains `PROHIBITED`, Gate 1 remains `OPEN_PARTIAL_PROGRESS`, and Phase 48 raised the committed runnable
catalog to 80.

See
[`../cpt_temporal_folded_susy/PHASE48_M4_CLONGDOUBLE_GRADIENT_REPAIR_STATE_MAP.md`](../cpt_temporal_folded_susy/PHASE48_M4_CLONGDOUBLE_GRADIENT_REPAIR_STATE_MAP.md),
[`../cpt_temporal_folded_susy/PHASE48_M4_CLONGDOUBLE_GRADIENT_REPAIR_STATE_MAP_INPUTS.json`](../cpt_temporal_folded_susy/PHASE48_M4_CLONGDOUBLE_GRADIENT_REPAIR_STATE_MAP_INPUTS.json),
[`../cpt_temporal_folded_susy/phase48_m4_clongdouble_gradient_repair_state_map.py`](../cpt_temporal_folded_susy/phase48_m4_clongdouble_gradient_repair_state_map.py),
and
[`../cpt_temporal_folded_susy/PHASE48_M4_CLONGDOUBLE_GRADIENT_REPAIR_STATE_MAP_RESULT.json`](../cpt_temporal_folded_susy/PHASE48_M4_CLONGDOUBLE_GRADIENT_REPAIR_STATE_MAP_RESULT.json).

## Current direct calculation — CPT × Temporal-Folded SUSY Phase 49

Phase 49 returns exit 0 with `VALID_RUN` and
`FULL_FLOW_CLONGDOUBLE_STATE_MAP_REPAIR_SUPPORTED`. It retains `clongdouble` through
`saddle + L @ xi`, generated-gradient evaluation, `L.T` contraction, and outer minus-conjugation, then
projects the complete seven-component flow once to complex128 at the DOP853 boundary. The solver state,
roots, steps, chart, cap/residual, and comparison references remain fixed.

All eighteen integrations and ninety probes complete. Every endpoint state passes `1e-8`, all three
full ladders pass `0.02`, and every retained derivative column passes `0.005` against both the Phase-46
independent finite difference and Phase-45 tangent. The largest derivative discrepancy is `0.001216`;
the largest adjacent plateau is `0.001401`. No root, step, sign, probe, or path is dropped.

Together with Phase 48, this resolves the pinned-platform implementation choice: projecting the
gradient early is insufficient, while one projection after complete local-flow evaluation passes all
frozen controls. It does not supply a formal endpoint propagator, isolate solver accumulation from
final subtraction, or establish portability to platforms with a different long-double representation.
The broader source/solver budget therefore remains open in those respects.

Phase 49 does not rewrite Phase 41, alter Phases 44–48, prove a source-formula defect, perform a new
root/tangent/orientation calculation, or compute a determinant line, complete cycle, Stokes chamber, or
global intersection. Global promotion remains `PROHIBITED`, Gate 1 remains `OPEN_PARTIAL_PROGRESS`, and
Phase 49 raised the committed runnable catalog to 81.

See
[`../cpt_temporal_folded_susy/PHASE49_M4_CLONGDOUBLE_FULL_FLOW_STATE_MAP_REPAIR.md`](../cpt_temporal_folded_susy/PHASE49_M4_CLONGDOUBLE_FULL_FLOW_STATE_MAP_REPAIR.md),
[`../cpt_temporal_folded_susy/PHASE49_M4_CLONGDOUBLE_FULL_FLOW_STATE_MAP_REPAIR_INPUTS.json`](../cpt_temporal_folded_susy/PHASE49_M4_CLONGDOUBLE_FULL_FLOW_STATE_MAP_REPAIR_INPUTS.json),
[`../cpt_temporal_folded_susy/phase49_m4_clongdouble_full_flow_state_map_repair.py`](../cpt_temporal_folded_susy/phase49_m4_clongdouble_full_flow_state_map_repair.py),
and
[`../cpt_temporal_folded_susy/PHASE49_M4_CLONGDOUBLE_FULL_FLOW_STATE_MAP_REPAIR_RESULT.json`](../cpt_temporal_folded_susy/PHASE49_M4_CLONGDOUBLE_FULL_FLOW_STATE_MAP_REPAIR_RESULT.json).

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
