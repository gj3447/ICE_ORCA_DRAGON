<div align="center">

# ICE_ORCA_DRAGON — Physics/Math Computation Workbench

**Hypercomplex experiments and CPT × Temporal-Folded SUSY calculations with reproducible checks**

[![Runnable kernels](https://img.shields.io/badge/Committed_kernels-72-3776ab?style=for-the-badge&logo=python&logoColor=white)](#current-snapshot)
[![Reproduction ledger](https://img.shields.io/badge/Repro_cases-14-10b981?style=for-the-badge)](#reproduction-ledger)
[![Control plane](https://img.shields.io/badge/Control_plane-TypeScript_%2B_Effect-3178c6?style=for-the-badge)](package.json)
[![License](https://img.shields.io/badge/License-AGPL--3.0--or--later-yellow?style=for-the-badge)](LICENSING.md)

</div>

ICE_ORCA_DRAGON is a reproducible hypothesis-testing workbench, not a completed unified theory. It
contains two deliberately separated research programmes:

- exact and numerical tests of Cayley–Dickson, sedenion, zero-divisor, and legacy prediction claims;
- a CPT × Temporal-Folded SUSY programme studying doubled time histories, quantum seam states,
  closed-FRW/SUGRA backgrounds, Wheeler–DeWitt selection, and possible supersymmetry breaking.

The two tracks share an execution and evidence system; they are **not currently derived from one another**.
The repository preserves speculative motivations while turning them into scoped calculations. Exact
results, numerical controls, physical interpretations, failed constructions, and open conjectures are
reported separately.

The programme's current philosophical synthesis is documented in
[`docs/ICE_CENTRAL_CLAIM_PHILOSOPHY_2026-08-20.md`](docs/ICE_CENTRAL_CLAIM_PHILOSOPHY_2026-08-20.md):
mathematical structure supplies candidate possibilities; physical content requires quotienting
redundant descriptions, assigning consistent amplitudes, tracking persistent records, and confronting
observables without assuming that one branch must be singled out.
An intuitive, explicitly non-evidential companion is
[`docs/ICE_RECURSIVE_TRUTH_MEDITATION_2026-08-20.md`](docs/ICE_RECURSIVE_TRUTH_MEDITATION_2026-08-20.md).

## What this workbench is testing

| Research track | Central question | Current conclusion |
|---|---|---|
| Hypercomplex algebra | Which structures in Cayley–Dickson algebras, sedenions, zero divisors, associators, and proposed group actions survive exact or basis-invariant tests? | Reusable algebraic results exist, but no Standard Model embedding or new particle prediction has been established. |
| CPT × Temporal-Folded SUSY | Can two CPT/Pin-related histories be joined by a physical quantum seam while ordinary SUSY acts within each sheet, and can that structure select initial data or generate lasting observable SUSY breaking? | Finite algebraic, state, and cosmological witnesses exist. A full seam action, persistent soft spectrum, and unique observable prediction do not yet exist. |

### Hypercomplex-algebra programme

This track treats proposed algebra-to-physics correspondences as testable maps rather than identities.
The kernels calculate Cayley–Dickson products, associators, zero divisors, derivation candidates,
closure/rank conditions, and representation or multiplication-preservation diagnostics.

The strongest current results are algebraic:

- the repository reproduces finite combinatorial and structural results for sedenion assessors,
  zero-divisor pairs, associators, and implemented higher-algebra identity checks;
- those calculations do not by themselves identify Higgs fields, gauge groups, particles, or measured
  constants;
- the historical mass-ratio search reports `0/15` genuine derivations, and the proposed $L_\star$
  construction is non-unique;
- Koide-like and $m_p/m_W$ coincidences show high look-elsewhere risk in the recorded controls;
- Queue 03 is quarantined as basis-dependent; Queue 08's projected $g_2$ construction is recorded as a
  method artifact, and Queue 09 still lacks a multiplication-preservation gate.

The live code is under [`research/hypercomplex/`](research/hypercomplex); the bounded historical verdicts
are summarized in [`docs/STATUS.md`](docs/STATUS.md).

### CPT × Temporal-Folded SUSY programme

This track starts from a more conservative question than “the superpartner lives in the past universe.”
CPT preserves spin statistics, so a CPT image of a fermion is still a fermion; simply assigning
$B_+\leftrightarrow F_-$ does not by itself remove the corresponding fermionic content from our sheet.

The current candidate is instead:

$$
\text{SUSY parent structure}
\;\xrightarrow{\;\text{CPT/Pin quantum sewing}\;}\;
\text{CPT-related two-sheet state whose physical branch need not preserve SUSY}.
$$

Here the terms have deliberately narrow meanings:

- a **sheet** is one time-oriented history or factor in a doubled description;
- a **seam** is a boundary state or kernel relating the sheets, not automatically a material spacelike
  membrane;
- **CPT** is antiunitary; a **Pin lift** would implement the relevant spacetime reflection on spinors.
  Neither is the fermionic supercharge being sought, and neither turns bosons into fermions;
- **parent SUSY** refers to the bulk algebra or action before imposing the physical seam/state;
- **observable SUSY breaking** requires more than a non-invariant state: it requires a lasting carrier
  and a derived low-energy spectrum;
- **SUGRA** is local supersymmetry coupled to gravity; **WDW** denotes the Wheeler–DeWitt Hamiltonian
  constraint on a cosmological wavefunction;
- a **pole mass** is read from a retarded propagator's spectral pole, while **Schwinger–Keldysh (SK)**
  doubling is a real-time unitarity contour and is not automatically a pair of physical universes.

The logical chain being tested is:

| Required link | Evidence at the current frontier |
|---|---|
| doubled-sheet algebra and reality structure | finite algebraic exchange/projector witnesses exist; a common physical action, domain, and spacetime Pin lift remain open |
| positive seam state | a normalized positive finite-oscillator control exists; the unregulated noncompact zero mode is not trace class |
| seam/state fails to preserve ordinary SUSY | bounded free state/domain witnesses exist; a full physical Pin seam remains open |
| persistent finite-energy $F/D$ order parameter | **open** |
| visible-sector soft masses and present-day pole splitting | **open** |
| parameter-independent collider/cosmology signature | **open** |

## Does this explain why SUSY has not been observed?

It provides a concrete **candidate route**, but not yet a completed explanation.

Phase 18 shows the distinction sharply. A finite temporal seam can prepare a non-SUSY state, but if the
future bulk remains the same free equal-mass Wess–Zumino theory, its retarded poles remain

$$
m_{B,\mathrm{pole}}^2=m_{F,\mathrm{pole}}^2=m^2,
\qquad
\Delta m_{\mathrm{pole}}^2=0.
$$

The seam changes occupations and anomalous/statistical correlators; it does not, under those assumptions,
generate a permanent superpartner mass splitting. The inflationary $F$-term in the displayed Phase 19
models also returns to a supersymmetric Minkowski endpoint.

A viable explanation must therefore derive the full chain. The current UV-completion candidate makes
the intermediate assumptions explicit:

$$
\text{BFV-reduced connected-seam candidate}
\longrightarrow
\text{CPT/Pin completion}
\longrightarrow
\text{double-three-form }N=1\text{ SUGRA}
\longrightarrow
\text{flux-sector selection}
\longrightarrow
\text{persistent metastable }F\ne0
\longrightarrow
\text{visible-sector soft operators}
\longrightarrow
\text{present-day superpartner spectrum}.
$$

String/M-theory can potentially supply a quantized flux lattice, charged-membrane transitions, a map
from selected fluxes to soft terms, and modular ultraviolet constraints. It does **not** by itself derive
the temporal seam, its flux-sector prior, or the Picard--Lefschetz coefficient, and it does not guarantee
that the connected minisuperspace saddle survives the compactified fluctuation problem.
An additional vector/gauging sector would be needed for a \(D\)-term branch; the cited three-form route
directly motivates \(F\)-type breaking.

If a persistent order parameter $F_X$ were derived, conventional mediation could conditionally give
terms of the form

$$
m_{\tilde f_i}^2\sim c_i\frac{|F_X|^2}{M_*^2},
\qquad
M_a\sim \frac{F_X\,\partial_X f_a}{2\operatorname{Re}f_a}.
$$

No $F_X$, mediation scale $M_*$, gaugino/sfermion/gravitino spectrum, or characteristic mass ratio has
yet been derived from the seam. The non-observation of superpartners is therefore a phenomenon this route
aims to explain, not evidence that the route is correct.

## What the current calculations establish

| Calculation | Established within its stated scope | Not established |
|---|---|---|
| [Phase 12](cpt_temporal_folded_susy/PHASE12_BOUNDARY_TWIST_INTERFACE.md) | Under its collar assumptions, the open-bulk bosonic deformation is a canonical frame change, and a rigid spatial Wess–Zumino interface witness exists. | A temporal interface, physical endpoint detector, or local-SUGRA completion. |
| [Phases 13–16](cpt_temporal_folded_susy/PHASE16_BGG_SINGLE_SOURCE.md) | Several branch-charge shortcuts were closed or left inconclusive; Phase 16 reproduces a BGG bosonic kinetic parent while the specified strict auxiliary-retaining FLRW truncation fails local-SUSY tangency. | A literature-wide SUGRA no-go, a conserved physical branch charge, or the complete doubled theory. |
| [Phase 17](cpt_temporal_folded_susy/PHASE17_TIME_LINE_FOLD_ALGEBRA.md) | An abstract doubled-sheet exchange algebra and doubled real projector can be constructed; an ordinary support-local $Q$ does not exchange the two open time halves. | A doubled Lorentzian action, common self-adjoint domain, conserved physical charge, or spacetime Pin lift. |
| [Phase 18](cpt_temporal_folded_susy/PHASE18_GAUSSIAN_SEAM_SPECTRUM.md) | A seam may prepare a non-SUSY free state, but a finite instantaneous canonical seam does not move equal-mass retarded poles; a sharp kick has a UV energy cost. | Persistent vacuum soft masses, interacting late-time splitting, or Higgs UV protection. |
| [Phase 19](cpt_temporal_folded_susy/PHASE19_CLOSED_SUGRA_BOUNCE.md) | Chosen shift-symmetric and Cecotti/Starobinsky potentials admit smooth closed-$k=+1$, time-symmetric bosonic solutions with conditional 50–60 accelerated e-fold histories. | CPT/Pin selection of the initial field value, fermionic sewing, reheating, or a late-time soft scale. |
| [Phase 20](cpt_temporal_folded_susy/PHASE20_TWO_SHEET_WDW_SELECTION.md) | The tested leading de Sitter/WDW envelopes do not select $\phi_0=5.442969\ldots$; it is target-shot initial data obtained after requiring 60 accelerated e-folds. | An exact two-sheet SUGRA WDW no-go or a unique curvature/reheating prediction. |
| [Phase 21](cpt_temporal_folded_susy/PHASE21_CONNECTED_SEAM_GAUSSIAN.md) | A normalized Gaussian identifies the decoupled-sheet baseline; $R-1$ and $\log R$ have distinct connectedness meanings. | An absolute universe/flux probability, physical sector prior, or derived joint $(n,\phi)$ peak. |
| [Phase 22](cpt_temporal_folded_susy/PHASE22_FINITE_MODE_SEAM_DENSITY.md) | One positive-frequency SUSY oscillator admits a normalized positive two-sheet purification, fixed-mode SUSY algebra, and elementary SK normalization. | An unbroken SUSY vacuum or physical CPT/Pin SUGRA state: $[\rho,Q]=0$ but $\langle H\rangle>0$, and the unregulated noncompact free zero mode is not trace class. |
| [Phase 23](cpt_temporal_folded_susy/PHASE23_HOMOGENEOUS_MINISUPERSPACE_DENSITY.md) | Full-real-lapse rigging, an explicit clock/frequency choice, and a supplied compact bridge produce a positive trace-class regulated density. | A cap-derived bridge, regulator-independent cosmological density, unique $\phi_0$, or local-SUGRA/Pin/BRST completion; zero signed current alone does not select a state. |
| [Phase 24](cpt_temporal_folded_susy/PHASE24_CONNECTED_STAROBINSKY_INTERVAL.md) | A frozen real Starobinsky $S^3\times I$ benchmark has a nonzero connected boundary response; constraint-preserving endpoint variations leave one nonzero homogeneous mixed direction. | A contributing gravitational thimble, positive seam density or physical entropy, full fluctuation determinant, CPT/Pin/SUGRA completion, or initial-value selection. |
| [Phase 25](cpt_temporal_folded_susy/PHASE25_CONNECTED_LAPSE_SCAN.md) | The proper-length saddle is nondegenerate, lapse elimination exactly produces the constrained Hessian, and the tracked real branch reaches a simple Dirichlet fold. | The global contributing lapse thimble, intersection number, gauge-fixed bulk Morse spectrum, or a positive quantum seam state. |
| [Phase 26](cpt_temporal_folded_susy/PHASE26_GLOBAL_LAPSE_FLOW.md) | A bounded constant-phase complex-lapse arm continues through its projected turn, and the real simple fold has the expected Airy uniformization. | The arm's global endpoint, an original-cycle intersection coefficient, a complete determinant, or a physical state. |
| [Phase 27](cpt_temporal_folded_susy/PHASE27_LORENTZIAN_LAPSE_ENDPOINT.md) | The declared Wick map sends positive Lorentzian lapse to the upper-imaginary Euclidean ray; the positive half-line is a sourced resolvent, while the raw fixed-$T$ Van Vleck factor diverges as $1/|T|$ at zero duration. | A transverse interior intersection, global PL coefficient, or finite gauge-reduced kernel. |
| [Phase 28](cpt_temporal_folded_susy/PHASE28_THIMBLE_BFV_INTERSECTION.md) | In the reduced homogeneous BFV--BRST control, Dirichlet ghosts do not remove proper length; bounded constructed dual-cycle segments cross the recorded branch and give a conditional local Gaussian factor. | The physical original cycle, global intersection number, full boson--fermion--gravitino--ghost determinant, positive density, or soft spectrum. |
| [Phase 29](cpt_temporal_folded_susy/PHASE29_ZERO_LAPSE_UNIFORM_KERNEL.md) | For the frozen leading real-lapse quadratic kernel and local flat $da\,d\phi$ endpoint measure, the pointwise $1/N$ factor is the normalization of a distributional identity kernel. The reduced fixed-$s$ BFV ghost leaves a $dT$ modulus measure and does not cancel it. | The physical WDW endpoint measure, interacting all-orders uniform kernel, simultaneous conformal/lapse cycle, full determinant, quantum state, or global PL coefficient. Multiplying by $N$ changes the resolvent and group average. |
| [Phase 30](cpt_temporal_folded_susy/PHASE30_CONFORMAL_BFV_DETERMINANT_LINE.md) | In the frozen homogeneous finite-cutoff control, a field-dependent Schur shift gives a convergent coupled conformal/lapse Gaussian tangent cycle. One declared midpoint calibration has a stable relative determinant magnitude. | A nonlinear continuum thimble, full BFV phase-space super-Hessian, absolute determinant-line phase, physical WDW measure, or global PL coefficient. The bare determinant sign alternates with cutoff parity, and one holomorphic lapse sheet does not normalize both real sides. |
| [Phase 31](cpt_temporal_folded_susy/PHASE31_HOMOGENEOUS_BFV_SUPERHESSIAN.md) | Exact momentum elimination reproduces the Phase-30 configuration Hessian. The unreduced proper-time-gauge canonical sign is stable, and nonzero homogeneous BFV quartet factors cancel in a same-regulator benchmark/reference ratio. | An absolute BFV phase or normalization, constraint-reduced continuum determinant, global $p_a$ clock, global PL coefficient, physical probability, or SUSY/SUGRA Hessian. “Super-Hessian” here is BFV grading only. |
| [Phase 32](cpt_temporal_folded_susy/PHASE32_BELOW_ORIGIN_LAPSE_INTERSECTION.md) | For an independently specified full real lapse contour bypassing zero from below, the tracked homogeneous lapse base has one recorded finite-radius projected crossing. Its coordinate sign is $+1$ only under the declared ambient, column, dual-flow, and Gaussian-lift orientations. The positive half-line instead has endpoint contact. | A signed full-joint local intersection, the complete global coefficient $n_\sigma$, continuous-arc proof beyond five samples on each of four arcs, a CPT/Pin derivation of the contour class, the full oriented superdeterminant line, or a positive physical seam state. |
| [Phase 33](cpt_temporal_folded_susy/PHASE33_FOLD_AIRY_UNIFORMIZATION.md) | The recorded Dirichlet caustic is a transverse simple fold. Its two real branches determine the local Airy action scale, soft Jacobi scaling, and opposite determinant signs; the canonical Airy solution space remains regular when the separate Van Vleck terms diverge. | A unique Airy contour/Stokes multiplier, analytic amplitude, absolute determinant line, complete dual continuation, global $n_\sigma$, uniform physical WDW kernel, or trace-class seam state. The fold is not another lapse saddle and its local chart adds no Phase-32 crossing. |
| [Phase 34](cpt_temporal_folded_susy/PHASE34_DIRECTED_FOLD_DUAL_CONTINUATION.md) | On the frozen reflection-symmetric stationary family, the recorded incoming real segment is directed toward the fold and a separate conjugate pair of reduced constant-phase arms continues through $T=13+2.8913896i$; no sampled endpoint-Jacobi zero or bounded Phase-32 lapse-base crossing occurs. | Which outgoing arm, if either, carries the incoming cycle; the full joint field--lapse metric and gradient flow, Airy connection and oriented determinant-line transport, all sheets and good ends, global $n_\sigma$, gauge-reduced physical kernel, or trace-class state. |
| [Phase 35](cpt_temporal_folded_susy/PHASE35_REDUCED_DETLINE_TRANSPORT.md) | In the declared endpoint basis, the reduced endpoint-Jacobi determinant stays nonzero at 57 sampled points on the Phase-34 dual-aligned branch pair, admits recursively unwrapped sampled square-root transport, is finite-resolution consistent with the oriented $-iC_{\rm det}\sqrt\tau$ fold law, and has cancelling conjugate reduced endpoint phases. | A zero-free continuum interpolation or asymptotic limit, identification with the physical Van Vleck block, an endpoint measure, absolute determinant sign or Maslov orientation, the incoming-to-outgoing fold connection, a regulated full BFV/SUGRA superdeterminant, all sheets and good ends, global $n_\sigma$, or a physical state. |
| [Phase 36](cpt_temporal_folded_susy/PHASE36_AIRY_GAUSS_MANIN_CONNECTION.md) | In separately declared CW and CCW local Airy bases, the contour-, cycle-, formal dual-basis, and Stokes identities are fixed. Two distinct sampled root-sheet BVP laterals pass the same finite-radius endpoint, action-gap, and determinant gates, so those local gates alone do not select an arm. | Transport of one common incoming physical upward dual, identification of the complete original relative cycle, a global choice of arm, the regular hard determinant quotient and CFU coefficients, absolute determinant/Maslov signs, unsampled zeros or other sheets, full joint field--lapse/BFV data, global $n_\sigma$, or a physical state. |
| [Phase 37](cpt_temporal_folded_susy/PHASE37_CLOSED_FOLD_HOLONOMY.md) | On three finite enclosing loops the two BVP roots exchange at one fixed basepoint, and—conditional on no unresolved intersample zero or alias winding—the sampled reduced determinant half-form has $\operatorname{tr}L=0$, $\det L=1$, and $L^2=-I$. An uninterrupted two-turn path and a nonenclosing control reproduce the expected $-1$ and $+1$ returns. | The original relative cycle, hard CFU coefficients, all modes and good ends, an absolute Maslov/Pfaffian orientation, a spacetime Pin lift, full BFV/SUGRA data, a conserved spinorial supercharge, pole splitting, or a physical state. Root holonomy alone does not break the Phase-17 local/exchange basis equivalence. |
| [Phase 38](cpt_temporal_folded_susy/PHASE38_JOINT_CYCLE_IDENTIFIABILITY.md) | The recorded projected crossing and local-root data do not license inverse reconstruction of the missing joint cycle. A finite typed witness exposes the possible information loss without proving it for the physical projection; the correct conditional local coefficient map is $G^T$, not the root permutation $P$. The known conjugate stationary-family arms are sampled through $\operatorname{Re}T=16$. | Noninjectivity of the actual physical projection, an admissible original joint cycle, signed full-joint intersections, all sheets and relative good ends, and global $n_\sigma$. The full-joint sign, complete signed vector, and $n_\sigma$ outputs remain `null`; Gate 1 is open. |
| [Phase 39](cpt_temporal_folded_susy/PHASE39_FINITE_JOINT_INTERSECTION.md) | In one frozen $m=2$ configuration regulator, a genuine positive-$T$ discrete saddle is re-solved and two cap pieces meet one finite-radius, finite-time upward-flow chart patch at numerically locally transverse six-real-dimensional candidates. The directly computed declared configuration-coordinate signs are $+1$ at $r=.3,.2$. | A full finite-chain signed sum, straight-arm or reintersection census, exact nonlinear upward manifold, physical original relative cycle, non-Stokes chamber, cutoff/metric/regulator stability, BFV/Pfaffian/Pin orientation, or global $n_\sigma$. The bounded-chain sum, complete vector, and $n_\sigma$ remain `null`; Gate 1 is open. |
| [Phase 40](cpt_temporal_folded_susy/PHASE40_M3_REFLECTION_ODD_INTERSECTION.md) | At $m=3$, a rank-one signed endpoint mutation exposes the first reflection-odd history sector. Five sequentially continued ten-real-dimensional local candidates at $\delta\in\{-.001,-.0005,0,.0005,.001\}$ all have direct declared coordinate sign $+1$; reflection, launch-radius, variational-tangent, and local odd-coordinate-clamp controls were run. | The source probes only one direction in the two-dimensional odd field sector. A five-point local branch is not a continuous homotopy proof, cutoff/metric/regulator stability, a bounded-chain sum, the physical original relative cycle, BFV/Pfaffian/Pin orientation, or global $n_\sigma$. All global outputs remain `null`; Gate 1 is open. |
| [Phase 41](cpt_temporal_folded_susy/PHASE41_M4_TWO_SOURCE_INTERSECTION.md) | At $m=4$, independent $\phi$-only and $a$-only endpoint sources give a stable numerical rank-two anchor-subtracted odd-response matrix in the frozen normalization. Five fourteen-real-dimensional local candidates are resolved with direct declared-coordinate sign $+1$ and root-Jacobian sign $-1$; 7/7 exact and 8/9 typed numerical contracts pass. | The sole failed contract is the three-point finite-difference tangent plateau check, even though its signs and operator errors pass. Consequently the separate $\phi$/$a$ local robustness claims remain inconclusive. No cross-cutoff determinant line, physical original cycle, bounded/global signed sum, cutoff or continuum limit, BFV/Pfaffian/Pin orientation, or global $n_\sigma$ is obtained; six promoted outputs remain `null` and Gate 1 is open. |

These results deliberately include negative answers. They close specific shortcuts without claiming a
no-go theorem for all SUSY theories, all two-sheet cosmologies, or all hypercomplex mathematics.

## Next falsification gates

1. **Foundational seam:** derive a doubled Wess–Zumino or local-SUGRA bulk-plus-seam action with a
   positive inner product, common self-adjoint variational domain, conserved complex-linear charge,
   physical sheet observable, and genuine spacetime Pin lift.
2. **Persistent breaking:** derive a stable nonzero $F/D$ order parameter, its visible-sector
   mediation, late-time pole splitting, vacuum lifetime, backreaction, and soft-versus-hard UV behavior.
3. **PL/BFV completion:** continue every arm of the full joint upward cycle through its folds, enumerate
   every intersection with a separately specified physical lapse contour, and remove the endpoint and
   mode regulators. Phase 31 supplies only an unreduced homogeneous BFV hybrid, while Phase 32 supplies
   one projected lapse-base crossing with a convention-conditional coordinate sign—not a signed joint
   local or global coefficient. Phase 33 uniformizes the recorded simple fold locally, Phase 34
   continues one conjugate reduced stationary-family pair through `Re T=13`, Phase 35 transports
   only its declared endpoint-Jacobi determinant section relatively along the sampled open path, and
   Phase 36 fixes identities in separately declared lateralized Airy bases and finds that two distinct
   sampled root-sheet laterals pass the recorded finite-radius gates. Phase 37 closes the local root path:
   it records the root exchange and a conditional order-four reduced half-form return, while an exact
   control shows that bare root holonomy still does not distinguish the Phase-17 local and exchange
   charge matrices. Phase 38 then records why those projected data cannot be inverted into the missing
   joint cycle without an injectivity theorem or explicit admissible completions, guards $G^T$ against
   the root-permutation mutation $P$, and extends the sampled stationary-family arms through
   $\operatorname{Re}T=16$. It does **not** prove that the actual physical projection is noninjective;
   every global output remains `null`, so Gate 1 stays open. Phase 39 then supplies the first direct
   six-real-dimensional local determinant at two frozen cap pieces, but only for one post-feasibility
   $m=2$ metric and finite-radius chart patch. It does not search the straight arms or reintersections,
   exhaust roots/components, certify a lateral Stokes chamber, or produce even a bounded-chain signed
   sum. Phase 40 then opens the first reflection-odd history sector at $m=3$: one rank-one endpoint
   source gives five sequentially continued local ten-real-dimensional candidates with direct sign
   $+1$, while the matched local K-launch-coordinate clamp fails to reproduce the full candidate.
   This is a local mutation witness, not a proof that the sign survives every odd direction or any
   continuous deformation. Phase 41 raises the same local construction to $m=4$ and adds independent
   $\phi$-only and $a$-only endpoint sources. Their frozen, anchor-subtracted susceptibility is stably
   numerical rank two, and five local full-$\mathbb R^{14}$ roots are computed, but the finite-difference
   tangent plateau contract fails at all three audited points. The source-specific robustness verdicts
   therefore remain inconclusive rather than being promoted from the repeated local signs. These phases
   do not transport the missing original physical cycle or derive a fermionic
   Pin/Pfaffian line. None identifies the
   complete original relative cycle or supplies the physical Van
   Vleck block, absolute Maslov orientation, global arm selection, or full joint field--lapse flow. Every
   global dual arm and good end,
   and the full oriented
   inhomogeneous superdeterminant, physical WDW endpoint measure, and CPT/Pin contour-class selection
   remain required. Exploratory calculation of the hard CFU coefficients $A,B$ may run in parallel;
   only their assembly and promotion as a physical uniform kernel depends on closing Gate 1.
4. **Three-form/flux selection:** derive the harmonic- and flux-dependent seam kernel, charge lattice,
   boundary ensemble, and sector measure from an actual three-form SUGRA or membrane action; then test
   for a cutoff-independent interior peak in $(n,\phi)$.
5. **Quantum state:** combine the completed contour and determinant with the physical WDW
   current/projector; test positivity and trace class rather than assigning $|\Psi|^2$ by assumption.
6. **String completion gate:** compactify a double-three-form $N=1$ SUGRA realization, derive its flux
   and membrane data and visible-sector mediation, and rerun the Phase 24--30 saddle and fluctuation
   tests instead of importing string soft terms into the seam by analogy.
7. **Hypercomplex interpretation:** replace basis-dependent diagnostics with invariant closure,
   nondegeneracy, rank, and multiplication-preservation checks, followed by an external physical
   discriminator.

Failure of one gate closes that construction. It does not constitute a universal refutation of
supersymmetry, CPT-symmetric cosmology, or hypercomplex algebra.

## Current snapshot

| Surface | Committed state at this revision | Authority |
|---|---:|---|
| runnable Python kernels | 72 | `./ice list --json` |
| mapped reproduction cases | 14 | `./ice repro --list` |
| reproduction result | 12 `REPRO`, 1 `NONPORTABLE_FAIL`, 1 `SUPERSEDED` | `./ice repro` |
| research ontology | 579 nodes, 1617 edges, 141 claims: 74 `SUPPORTED`, 66 `CONTRADICTED`, 1 `INCONCLUSIVE` | `./ice ontology summary` |
| indexed Phase 15R--41 payload | 86 artifacts, 85 evidence nodes, 27 phases, 44 scopes; 90/90 recorded hashes verified (86 artifacts + 4 policies); 26 validation warnings | ontology graph and validator |
| named exact checks | 410 | phase result payloads in the ontology |
| typed numerical checks | 238 current = 237 `PASS` + 1 `FAIL`; 239 including the separately catalogued passing legacy control = 238 `PASS` + 1 `FAIL` | phase result payloads in the ontology |
| latest runnable CPT seam phase | Phase 41 | [`cpt_temporal_folded_susy/README.md`](cpt_temporal_folded_susy/README.md) |

The counts above describe the committed repository snapshot. `./ice list --json` is the authority for a
working tree that contains additional local kernels.

## Quick start

The control plane is strict TypeScript using Effect. Numerical kernels use the Python environment locked
by `uv.lock`.

```bash
npm ci
uv sync --locked
./ice doctor
./ice list
```

Canonical commands:

```bash
./ice doctor
./ice list [--json]
./ice info <name>
./ice run <name> [-- <kernel args>]
./ice repro [--list] [--only <mapped-name>]
./ice ontology validate
./ice ontology summary
```

`npm run ice -- <command>` is the package-script equivalent. `./ice` is the repository entry point.

## Repository layout

The repository root is intentionally limited to entry points, policy, package metadata, lockfiles, and
legal documents. Research code and historical reports live in named areas.

| Path | Contents | Runnable catalog |
|---|---|---:|
| [`ice`](ice), [`src/`](src), [`test/`](test) | Effect control plane and its tests | control plane |
| [`research/hypercomplex/`](research/hypercomplex) | Cayley–Dickson/sedenion kernels and adjacent JSON results | included |
| [`research/legacy_predictions/`](research/legacy_predictions) | dimensional, preregistration, and numerology-era kernels/results | included |
| [`cpt_temporal_folded_susy/`](cpt_temporal_folded_susy) | current phase scripts, reports, and frozen inputs | included |
| [`claimB_loop/`](claimB_loop) and named experiment directories | focused research programmes | included when a script has a main guard |
| [`ontology/`](ontology) | typed claims, evidence snapshots, scopes, sources, and open problems | not applicable |
| [`docs/`](docs) | current guides, decisions, audits, and provenance | excluded |
| [`_archive/`](_archive), [`_findings/`](_findings), [`papers/`](papers), [`output/`](output) | historical/non-runnable material and generated references | excluded |

Python scripts that import local helpers remain colocated with them. Result JSON files stay beside their
producer so direct runs and isolated reproduction use the same path contract.

## Run a kernel

Use a name returned by `./ice list` rather than depending on a physical path:

```bash
# Hypercomplex calculations
./ice info cd_path_amplitude_v2
./ice run cd_path_amplitude_v2
./ice run prove_s3_higher_gauge
./ice run queue_08_g2_diagnostic

# Legacy dimensional/numerology controls
./ice run derive_dimensionless_ICE
./ice run ice_prereg_check

# Current CPT × Temporal-Folded SUSY track
./ice run phase19_closed_sugra_bounce
./ice run phase20_two_sheet_wdw_selection
./ice run phase21_connected_seam_gaussian
./ice run phase22_finite_mode_seam_density
./ice run phase23_homogeneous_minisuperspace_density
./ice run phase24_connected_starobinsky_interval
./ice run phase25_connected_lapse_scan
./ice run phase26_global_lapse_flow
./ice run phase27_lorentzian_lapse_endpoint
./ice run phase28_thimble_bfv_intersection
./ice run phase29_zero_lapse_uniform_kernel
./ice run phase30_conformal_bfv_determinant_line
./ice run phase31_homogeneous_bfv_superhessian
./ice run phase32_below_origin_lapse_intersection
./ice run phase33_fold_airy_uniformization
./ice run phase34_directed_fold_dual_continuation
./ice run phase35_reduced_detline_transport
```

Direct runs may update an adjacent result file. Inspect `git status` afterward. Use `./ice repro` for a
non-destructive comparison against committed mapped outputs.

## Reproduction ledger

```bash
./ice repro --list
./ice repro
```

The harness copies tracked and candidate files into an Effect-scoped temporary directory, deletes each
mapped output before execution, runs cases serially, and compares the fresh result with the committed
baseline. The current ledger intentionally exits nonzero:

- 12 portable cases reproduce;
- `queue_03_threshold_sensitivity_scan` is quarantined because its legacy entrywise metric depends on an
  arbitrary null-space basis;
- `queue_06_cooperative_vacuum` is marked `SUPERSEDED` because a repaired script generated its baseline.

See the [Queue 03 portability audit](docs/audits/QUEUE03_PORTABILITY_AUDIT_2026-08-14.md) and the
[reproducibility record](docs/audits/REPRODUCIBILITY_2026-06-08.md).

## Research ontology

The repository-local [CPT × Temporal-Folded SUSY research graph](ontology/cpt-temporal-folded-susy/README.md)
links scoped claims, executable evidence, sources, and open problems. It is a memory/index layer, not a
research contract or automatic physics verdict.

```bash
./ice ontology validate
./ice ontology summary
./ice ontology show claim:P16_BGG_BOSONIC_KINETIC_PARENT
./ice ontology trace claim:P17_FUNDAMENTAL_DOUBLED_SHEET_EXCHANGE_ALGEBRA --depth 2
./ice ontology trace claim:P24_CONSTRAINT_PRESERVING_MIXED_HESSIAN_HAS_RANK_ONE --depth 2
./ice ontology trace claim:P33_RECORDED_DIRICHLET_CAUSTIC_HAS_SIMPLE_FOLD_AIRY_SCALE --depth 2
```

## Scientific scope

Reports use the following disclosure layers:

| Layer | Meaning |
|---|---|
| L1 algebra | exact or numerical statements about the implemented algebra/computation |
| L2/L3 physics belt | proposed physical interpretations and empirical discriminators |
| mythology | user-primary narrative material preserved separately from scientific evidence |

“ICE predicts X” is incomplete without a target claim, layer, assumptions, and evidence status. The
governing decision is [the workbench reframe](docs/decisions/ICE_WORKBENCH_REFRAME_2026-05-18.md); the
working rules are in [`AGENTS.md`](AGENTS.md).

## Development

```bash
npm run typecheck
npm test
npm run check
./ice doctor
```

For a Python/kernel change, also run the directly affected entry and, when mapped, its isolated repro
case:

```bash
./ice info <name>
./ice run <name>
./ice repro --only <name>
```

## Documentation

| Document | Purpose |
|---|---|
| [`docs/index.md`](docs/index.md) | documentation map |
| [`docs/USERGUIDE.md`](docs/USERGUIDE.md) | CLI and runnable-catalog guide |
| [`docs/STATUS.md`](docs/STATUS.md) | engineering status and bounded scientific ledger |
| [`research/README.md`](research/README.md) | organized research-code and report map |
| [`cpt_temporal_folded_susy/README.md`](cpt_temporal_folded_susy/README.md) | complete CPT phase index and current boundary |
| [`ontology/README.md`](ontology/README.md) | research-graph format and CLI entry points |
| [`docs/decisions/`](docs/decisions) | governing scope decisions |
| [`docs/audits/`](docs/audits) | reproducibility and method audits |
| [`docs/provenance/SOURCES.md`](docs/provenance/SOURCES.md) | mythology/physics sources and provenance |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | contribution and verification workflow |

## License

AGPL-3.0-or-later, with a separate commercial-license option. See
[`LICENSING.md`](LICENSING.md).
