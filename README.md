<div align="center">

# ICE_ORCA_DRAGON — Physics/Math Computation Workbench

**Hypercomplex experiments and CPT × Temporal-Folded SUSY calculations with reproducible checks**

[![Runnable kernels](https://img.shields.io/badge/Committed_kernels-53-3776ab?style=for-the-badge&logo=python&logoColor=white)](#current-snapshot)
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

A viable explanation must therefore derive the full chain

$$
\text{CPT/Pin seam}
\longrightarrow
\text{persistent metastable }F/D
\longrightarrow
\text{visible-sector soft operators}
\longrightarrow
\text{present-day superpartner spectrum}.
$$

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

These results deliberately include negative answers. They close specific shortcuts without claiming a
no-go theorem for all SUSY theories, all two-sheet cosmologies, or all hypercomplex mathematics.

## Next falsification gates

1. **Foundational seam:** derive a doubled Wess–Zumino or local-SUGRA bulk-plus-seam action with a
   positive inner product, common self-adjoint variational domain, conserved complex-linear charge,
   physical sheet observable, and genuine spacetime Pin lift.
2. **Persistent breaking:** derive a stable nonzero $F/D$ order parameter, its visible-sector
   mediation, late-time pole splitting, vacuum lifetime, backreaction, and soft-versus-hard UV behavior.
3. **Quantum state:** calculate the constrained complex cap, physical WDW current/projector, homogeneous
   zero-mode measure, and coupled boson–fermion–gravitino–ghost determinant; test positivity and trace
   class rather than assigning $|\Psi|^2$ by assumption.
4. **Three-form/flux selection:** derive the harmonic- and flux-dependent seam kernel, charge lattice,
   boundary ensemble, and sector measure from an actual three-form SUGRA or membrane action; then test
   for a cutoff-independent interior peak in $(n,\phi)$.
5. **Hypercomplex interpretation:** replace basis-dependent diagnostics with invariant closure,
   nondegeneracy, rank, and multiplication-preservation checks, followed by an external physical
   discriminator.

Failure of one gate closes that construction. It does not constitute a universal refutation of
supersymmetry, CPT-symmetric cosmology, or hypercomplex algebra.

## Current snapshot

| Surface | Committed state at this revision | Authority |
|---|---:|---|
| runnable Python kernels | 53 | `./ice list --json` |
| mapped reproduction cases | 14 | `./ice repro --list` |
| reproduction result | 12 `REPRO`, 1 `NONPORTABLE_FAIL`, 1 `SUPERSEDED` | `./ice repro` |
| research ontology | 225 nodes, 442 edges, 48 claims | `./ice ontology summary` |
| latest runnable CPT seam phase | Phase 22 | [`cpt_temporal_folded_susy/README.md`](cpt_temporal_folded_susy/README.md) |

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
