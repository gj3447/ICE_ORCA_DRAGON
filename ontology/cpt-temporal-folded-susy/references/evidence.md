# Evidence guide

> This page is a human-readable memory and index over observed repository runs. It is **not** a preregistration, research contract, independent replication, peer review, final scientific verdict, or KG ratification.

Machine-readable records: [`graph.json`](../graph.json), [`phase16-result.json`](../evidence/phase16-result.json), [`phase17-result.json`](../evidence/phase17-result.json), and [`phase18-result.json`](../evidence/phase18-result.json).

## Reading `PASS` correctly

All 101 Phase 16–18 named exact checks in the three snapshots have `status: PASS`. The Phase 18 payload separately records one passing SciPy numerical control; it is not counted in the exact-check ledger. A `PASS` means that an executable verified its stated equality, rank, obstruction, mutation rejection, counterexample, or numerical comparison. It does not mean every scientific claim passed.

The scientific direction is stored on:

```text
claim → HAS_EVIDENCE { polarity: SUPPORTS | CONTRADICTS } → evidence
```

Thus `P16.off_shell_b_i_obstruction: PASS` contributes to contradicting the claim that the strict truncation is SUSY-tangent. The snapshot payload may likewise say `FAIL_BY_EXACT_CLEAN_POINT_COUNTEREXAMPLE` for the proposed property while the test detecting that failure passes.

## Observed-run provenance

| Phase | Result and observation | Executable provenance | Outcome |
| --- | --- | --- | --- |
| 16 | `result:P16_BGG_SINGLE_SOURCE_20260816`; `2026-08-16T15:53:21Z` | `cpt_temporal_folded_susy/phase16_bgg_single_source.py`; SHA-256 `95c9346bf4607d955692778a2bf91638a307a3563f51bff57af0635bc548f55c`; introduced in `25bd216cfd1d85bde59c60ec4f2a9d91bdb53d78` | Exit `0`; 20 exact checks |
| 17 | `result:P17_TIME_LINE_FOLD_ALGEBRA_20260816`; `2026-08-16T15:53:21Z` | `cpt_temporal_folded_susy/phase17_time_line_fold_algebra.py`; SHA-256 `4723f6217f1014c52001dd989fb393e7c8547a1a0556bf7c0141c0dcaa20d615`; introduced in `5c95692b4c9ca6d92c617382f5bb9bf6506bfb5d` | Exit `0`; 34 exact checks |
| 18 | `result:P18_GAUSSIAN_SEAM_SPECTRUM_20260816`; `2026-08-16T16:42:39Z` | `cpt_temporal_folded_susy/phase18_gaussian_seam_spectrum.py`; SHA-256 `01f2d5d04341093494e185529dd67630aef5896e842a4bedddc6d1309271e221`; introduced in `1a5d6d4326da3451ff63274cee654fa504f82f9c` | Exit `0`; 47 exact checks plus 1 separately recorded numerical control |

The Phase 15R evidence node points to the committed [`PHASE15R_RUN_RESULT.json`](../../../cpt_temporal_folded_susy/PHASE15R_RUN_RESULT.json). It is not duplicated under `ontology/.../evidence/`.

## Evidence-to-claim index

| Evidence group | Checks | Claim and polarity | Scope/source |
| --- | ---: | --- | --- |
| `evidence:p15r-run-result` | See Phase 15R result | Bosonic frozen-census parent — `SUPPORTS`; full off-shell frozen-census parent — `CONTRADICTS` | Frozen two-source census only |
| `evidence:p16-bosonic` | 13 | BGG bosonic kinetic parent — `SUPPORTS` | `(X,T,Y)` kinetic scope; `DERIVED_FROM` BGG |
| `evidence:p16-tangency` | 6 | Specified strict off-shell FLRW tangency — `CONTRADICTS` | Exact clean point on declared locus; `DERIVED_FROM` BGG |
| `evidence:p16-clock` | 1 | Scoped rolling-clock preserved SUSY — `CONTRADICTS` | `W=0`, `F=0`, nonzero real rate, Lorentzian conjugacy; `DERIVED_FROM` BGG |
| `evidence:p17-local` | 6 | Standard support-local half exchange — `CONTRADICTS` | Fixed positive-energy fiber plus support-locality; claim `CITES` HLS |
| `evidence:p17-doubled` | 11 | Fundamental bidirectional exchange — `SUPPORTS`; one-way closure — `CONTRADICTS`; unique basis selection — `CONTRADICTS` | Finite internal doubled-sheet algebra; no physical-action source edge |
| `evidence:p17-reflection` | 4 | Reflection-composed standard local charge — `CONTRADICTS` | Literal `t∈R` line; claim `CITES` HLS |
| `evidence:p17-seam` | 9 | Ordinary real temporal seam — `CONTRADICTS`; doubled-real projector — `SUPPORTS`; physical time reversal as the tested `Q` — `CONTRADICTS` | Finite seam/projector and literal-time scopes; boundary and reflection/Pin sources frame the first two claims, while CPT/Pin remains a separate concept |
| `evidence:p17-sk` | 4 | SK BRST as particle SUSY — `CONTRADICTS` | Abstract four-state quartet; claim cites two SK sources |
| `evidence:p18-charge-and-poles` | 18 exact | Elapsed time alone breaks SUSY — `CONTRADICTS`; free canonical seam generates permanent B/F pole splitting — `CONTRADICTS`; free seam can prepare a non-SUSY state without moving poles — `SUPPORTS` | Equal-mass free Wess–Zumino mode and unchanged future bulk operators; literature links are `CITES`, not `DERIVED_FROM` |
| `evidence:p18-state-and-cpt` | 17 exact | Free seam can prepare a non-SUSY state without moving poles — `SUPPORTS` | Finite scalar canonical kick, finite-mode fermion CAR witness, and CPT-compatible doubled scalar eigenchannels; not a local fermionic Pin action |
| `evidence:p18-uv-and-conditional-controls` | 12 exact + 1 numerical | Sharp spatially local scalar seam is UV admissible — `CONTRADICTS` | Sharp-kick cutoff asymptotics plus conditional Gaussian, collisionless FRW, and inserted-soft controls; no interacting self-energy or Higgs result |

## Phase 16 check ledger

### Bosonic derivation — 13 checks

- `P16.connection`
- `P16.connection_mixed`
- `P16.curvature_antisymmetry`
- `P16.CPN26_ab`
- `P16.CPN26_ba_mutation`
- `P16.raw_boundary`
- `P16.first_order_gravity`
- `P16.same_source_scalar`
- `P16.first_order_L`
- `P16.hessian`
- `P16.hessian_invariants`
- `P16.momenta`
- `P16.Hamiltonian`

Together these establish the source convention, reject the transposed curvature reading, remove one endpoint, and verify the exact `(-,+,+)` kinetic Hessian, momenta, and Hamiltonian.

### Strict tangency counterexample — 6 checks

- `P16.spin32_projector`
- `P16.spin32_candidate_kernel`
- `P16.clean_spinor_bilinear`
- `P16.off_shell_b_i_obstruction`
- `P16.spin32_obstruction`
- `P16.spin32_residual_trace`

The two independent normal witnesses are a nonzero `F ε¹ χ̄^{dot1}` coefficient `1/√2` in `δb₃` and a nonzero gamma-traceless spatial spin-3/2 residual for the declared clean monomial. A single exact point suffices to refute tangency of the whole declared locus; it is not a full transcription of every CPN variation.

### Rolling-clock slice — 1 check

- `P16.rolling_clock_no_residual_susy`

On the declared `W=0`, `F=0`, nonzero real proper-time-rate slice, the `δχ` parameter map has rank two, leaving only the zero Lorentzian-real parameter. The result concerns preserved background SUSY, not existence of the underlying gauge symmetry.

## Phase 17 check ledger

### Standard local fiber and support locality — 6 checks

- `P17.branch_reflection`
- `P17.branch_projectors`
- `P17.N1_CAR`
- `P17.N1_fermion_parity`
- `P17.local_standard_closure`
- `P17.local_same_half`

### Doubled-sheet algebra and nonselection — 11 checks

- `P17.fold_fixed_fiber_closure`
- `P17.fold_physical_parity`
- `P17.fold_bidirectional_exchange`
- `P17.half_sign_is_not_fermion_parity`
- `P17.unitary_mixing_family`
- `P17.mixing_not_selected`
- `P17.exchange_phase_family`
- `P17.local_fold_basis_equivalence`
- `P17.one_way_cross`
- `P17.one_way_closure_rejected`
- `P17.nonunitary_branch_mutation`

These establish a finite bidirectional unitary-flip witness while rejecting a one-way arrow, a nonunitary branch mutation, and any claim that closure alone selects the exchange basis.

### Literal reflection, translation, and positivity — 4 checks

- `P17.reflection_reverses_time_momentum`
- `P17.reflection_translation_obstruction`
- `P17.sharp_half_not_translation_invariant`
- `P17.signed_time_generator_not_positive_closure`

### Temporal seam, reality, and doubled projector — 9 checks

- `P17.real_temporal_seam_closure_obstruction`
- `P17.complexified_temporal_seam_control`
- `P17.geometric_reflection_linearity`
- `P17.physical_time_reversal_antilinearity`
- `P17.spatial_boundary_real_half`
- `P17.temporal_boundary_complex_half`
- `P17.temporal_boundary_no_real_half`
- `P17.doubled_real_temporal_projector`
- `P17.doubled_projector_mixes_sheets`

The positive control is a real rank-two spatial-boundary projector. The single-copy temporal projector preserves no nonzero real Majorana parameter. Adding a real two-sheet complex structure yields a rank-four real sheet-mixing projector, but only at finite projector level.

### Abstract Schwinger–Keldysh quartet — 4 checks

- `P17.SK_BRST_algebra`
- `P17.SK_BRST_parity`
- `P17.SK_difference_exact`
- `P17.SK_signed_contour_control_not_positive_H`

These verify nilpotence, mutual anticommutation, ghost oddness, and BRST exactness in the abstract quartet, while distinguishing its signed contour control from a positive physical-adjoint SUSY Hamiltonian.

## Phase 18 check ledger

### Conserved charge and free retarded poles — 18 exact checks

- `P18.time.conserved_charge`
- `P18.time.susy_state_stays_susy`
- `P18.domain.multiplet_marker`
- `P18.scalar.generator_square`
- `P18.scalar.evolution_equation`
- `P18.scalar.evolution_symplectic`
- `P18.scalar.general_seam_flux_identity`
- `P18.scalar.post_seam_evolution`
- `P18.scalar.characteristic_polynomial`
- `P18.fermion.hamiltonian_square`
- `P18.fermion.characteristic_polynomial`
- `P18.fermion.resolvent_factorization`
- `P18.fermion.evolution_equation`
- `P18.fermion.evolution_unitary`
- `P18.bulk.common_BF_shell`
- `P18.propagator.scalar_retarded_open_EOM`
- `P18.propagator.scalar_retarded_jump`
- `P18.propagator.scalar_retarded_seam_independence`

These checks separate time evolution from seam dynamics and prove the scoped free theorem. Conserved `[H,Q]=0` evolution keeps a `Q`-annihilated state in the kernel; an instantaneous Cauchy-data map changes amplitudes but not the unchanged future scalar or fermion generator. For the declared post-post retarded-pole definition, both characteristic denominators remain `p²-m²`, so `delta m_pole²=0`.

### Seam state and CPT-sheet controls — 17 exact checks

- `P18.seam.scalar_kick_symplectic`
- `P18.seam.scalar_kick_time_reversal_reciprocity`
- `P18.seam.scalar_mode_continuity`
- `P18.seam.scalar_mode_jump`
- `P18.seam.scalar_post_frequency`
- `P18.seam.scalar_bogoliubov_norm`
- `P18.prediction.scalar_occupation`
- `P18.seam.fermion_CAR`
- `P18.prediction.fermion_occupation`
- `P18.propagator.spectral_state_independence`
- `P18.propagator.statistical_state_dependence`
- `P18.propagator.image_bulk_equation`
- `P18.CPT.sheet_kernel`
- `P18.CPT.sheet_eigenchannels`
- `P18.CPT.real_sheet_diagonalization`
- `P18.CPT.doubled_kick_symplectic`
- `P18.prediction.sheet_occupation_sum_difference`

The explicit witnesses give scalar occupation `κ²/[4(k²+m²)]`, finite Nambu-pair fermion occupation `sin²θ`, and CPT-compatible scalar sheet eigenchannels. Unequal occupations can therefore define a non-SUSY state while the free spectral kernel remains state independent. The fermion construction is only a finite-mode CAR witness, not a local Weyl/Majorana Pin-seam action.

### UV and conditional controls — 12 exact checks plus 1 numerical control

- `P18.UV.number_density_primitive`
- `P18.UV.energy_density_primitive`
- `P18.UV.sharp_asymptotics`
- `P18.UV.gaussian_pulse_fourier`
- `P18.prediction.gaussian_Born_occupation`
- `P18.FRW.relativistic_dilution`
- `P18.FRW.nonrelativistic_dilution`
- `P18.soft.conditional_mass_ratio`
- `P18.soft.small_breaking_series`
- `P18.mutant.reject_noncanonical_scalar_seam`
- `P18.mutant.reject_nonunitary_fermion_seam`
- `P18.mutant.detect_inserted_bulk_soft_mass`

The sharp kick yields linear cutoff divergence in number density and leading energy density `κ²Λ²/(16π²)`, so it is not a finite-energy state. Gaussian smoothing, `a^-2`/`a^-3` collisionless dilution, and `sqrt(1+r²)` for an inserted persistent soft term are explicitly conditional controls, not predictions of an interacting seam theory.

The payload-only numerical control `P18.numeric.narrow_gaussian_delta_limit` used SciPy `solve_ivp` with DOP853 and passed with maximum absolute error `7.150719e-05` and Bogoliubov-normalization error `3.330669e-16`. It is recorded separately because the graph's evidence groups enumerate exact symbolic checks.

## Reproduction commands

The commands recorded in the snapshots are:

```bash
uv run --locked python3 cpt_temporal_folded_susy/phase16_bgg_single_source.py
uv run --locked python3 cpt_temporal_folded_susy/phase17_time_line_fold_algebra.py
uv run --locked python3 cpt_temporal_folded_susy/phase18_gaussian_seam_spectrum.py
```

To audit an observed result, compare the current executable hash with the snapshot's `script.sha256`, rerun the exact recorded command, and compare check IDs, statuses, statements, payload, exit code, and scope guard. A successful rerun increases reproducibility; it still does not constitute independent peer review or extend the declared scope.

## Two complete traces

Supported trace:

```text
claim:P17_FUNDAMENTAL_DOUBLED_SHEET_EXCHANGE_ALGEBRA
  → HAS_EVIDENCE {polarity: SUPPORTS}
  → evidence:p17-doubled
  → DEFINED_IN → artifact:p17-script
  → RECORDED_IN → artifact:p17-evidence-snapshot
  → VALID_WITHIN → scope:p17-fundamental-doubled-sheet
  → VALID_WITHIN → scope:p17-fixed-positive-energy-fiber
  → BLOCKED_BY → action/domain/charge/compatibility/anchor open nodes
```

Contradicted trace:

```text
claim:P16_SPECIFIED_OFF_SHELL_FLRW_GAMMA_TRACE_TANGENCY
  → HAS_EVIDENCE {polarity: CONTRADICTS}
  → evidence:p16-tangency
  → DERIVED_FROM → source:bgg-hep-th-0005225v1
  → DEFINED_IN → artifact:p16-script
  → RECORDED_IN → artifact:p16-evidence-snapshot
  → VALID_WITHIN → scope:p16-strict-flrw-tangency
```

Phase 18's central polarity pair is:

```text
claim:P18_FREE_CANONICAL_SEAM_GENERATES_POLE_SPLITTING
  → HAS_EVIDENCE {polarity: CONTRADICTS}
  → evidence:p18-charge-and-poles
  → DEFINED_IN → artifact:p18-script
  → RECORDED_IN → artifact:p18-evidence-snapshot
  → VALID_WITHIN → scope:p18-free-instantaneous-seam

claim:P18_FREE_SEAM_CAN_PREPARE_NONSUSY_STATE
  ├─ HAS_EVIDENCE {polarity: SUPPORTS} → evidence:p18-state-and-cpt
  ├─ HAS_EVIDENCE {polarity: SUPPORTS} → evidence:p18-charge-and-poles
  └─ VALID_WITHIN → scope:p18-free-instantaneous-seam
```

The [programme guide](../README.md) lists every scope and open problem; the [source inventory](./source-inventory.md) explains what the literature edges do and do not cover.
