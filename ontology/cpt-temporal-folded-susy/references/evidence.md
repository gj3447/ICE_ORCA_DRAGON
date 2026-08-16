# Evidence guide

> This page is a human-readable memory and index over observed repository runs. It is **not** a preregistration, research contract, independent replication, peer review, final scientific verdict, or KG ratification.

Machine-readable records: [`graph.json`](../graph.json), [`phase16-result.json`](../evidence/phase16-result.json), [`phase17-result.json`](../evidence/phase17-result.json), [`phase18-result.json`](../evidence/phase18-result.json), [`phase19-result.json`](../evidence/phase19-result.json), and [`phase20-result.json`](../evidence/phase20-result.json).

## Reading `PASS` correctly

All 136 Phase 16–20 named exact checks have `status: PASS`. The snapshots also record 45 numerical checks: one Phase 18 SciPy control, 30 Phase 19 background/slow-roll checks, and 14 Phase 20 benchmark/bridge checks. A `PASS` means that an executable verified its stated equality, rank, obstruction, mutation rejection, counterexample, or bounded numerical comparison. It does not mean every scientific claim passed.

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
| 19 | `result:P19_CLOSED_SUGRA_BOUNCE_20260816`; `2026-08-16T17:23:38Z` | `cpt_temporal_folded_susy/phase19_closed_sugra_bounce.py`; SHA-256 `5dbfccd768bb13961222c289ba0754497bec94319f8b33ff602889eaeb469341`; introduced in `90aedef93eadab40156fc22daf87b2d6942f49a6` | Exit `0`; 17 exact checks plus 30 numerical checks |
| 20 | `result:P20_TWO_SHEET_WDW_SELECTION_20260816`; `2026-08-16T17:28:20Z` | `cpt_temporal_folded_susy/phase20_two_sheet_wdw_selection.py`; SHA-256 `a55ebfca78f07246679fd5fa8791537a0efe1d3370dfa53d8d6410ffc6a95807`; introduced in `c5395bc095399ca450adf555d8d24e21a9166725` | Exit `0`; 18 exact checks plus 14 numerical checks |

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
| `evidence:p19-shift-sugra` | 8 exact | Shift reduction and \(\zeta=1/12\) \(H_V\)-heavy benchmark — `SUPPORTS`; displayed endpoint F direction vanishes — `SUPPORTS` | Exact one-field shift trajectory; `DERIVED_FROM` Kallosh–Linde 2010 |
| `evidence:p19-noscale-sugra` | 7 exact | Cecotti reduction and one-sixth sufficient/not-sharp statement — `SUPPORTS`; displayed endpoint F direction vanishes — `SUPPORTS` | Exact one-field no-scale trajectory; `DERIVED_FROM` Kallosh–Linde 2013 |
| `evidence:p19-bounce-local` | 2 exact | Bosonic time-reflection data leave \(\phi_0\) free — `SUPPORTS`; target-shot branches exist — `SUPPORTS` | Classical homogeneous \(k=+1\) turning point |
| `evidence:p19-bounce-shooting` | 24 numerical | Six target-shot \(N_{\rm acc}=50,55,60\) backgrounds — `SUPPORTS`; \(\phi_0\) remains unselected — `SUPPORTS` | Conditional classical background shooting; no state, uniqueness, or parameter-free radius claim |
| `evidence:p19-slowroll-r` | 6 numerical | Quadratic compatibility with current \(r\) bound — `CONTRADICTS`; Starobinsky first-order \(r\) below bound — `SUPPORTS` | Potential slow roll at selected \(N_*\); cited papers supply comparison limits, not the bounce |
| `evidence:p20-leading-wdw-envelope` | 12 exact + 6 numerical | Leading envelope selects \(5.44\) — `CONTRADICTS`; independent-pair \(e^{4sI}\) follows from CPT — `CONTRADICTS`; coherent symmetrization only rescales probability — `CONTRADICTS` | Constant-field de Sitter/WDW control; standard \(e^{2sI}\) versus conditional independent-pair joint probability; no exact complex saddle or sheet inner product |
| `evidence:p20-cecotti-f-direction` | 5 exact + 2 numerical | Cecotti \(5.44\) point is F-flat — `CONTRADICTS` | Classical \(S=0\), positive-real \(T\) trajectory only; not the quantum local-SUSY wavefunction |
| `evidence:p20-curvature-reheating-control` | 1 exact + 6 numerical | Conditional conversion is reproducible — `SUPPORTS`; displayed number is a seam prediction — `CONTRADICTS` | One Phase 19 branch with fixed matterlike reheating, entropy, units, and late-time inputs |

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

## Phase 19 check ledger

### Shift-symmetric exact reduction — 8 checks

- `P19.shift.canonical_inflaton_metric`
- `P19.shift.quadratic_potential`
- `P19.shift.orthogonal_inflaton_mass`
- `P19.shift.stabilizer_mass`
- `P19.shift.hubble_heavy_sufficient_benchmark`
- `P19.shift.gravitino_mass_on_path`
- `P19.shift.stabilizer_F_order_parameter`
- `P19.shift.susy_minkowski_endpoint`

These checks derive the quadratic path, distinguish \(H_V^2=V/3\) from geometric \(H(t)^2\), and verify the displayed stabilizer F direction vanishes at the fully checked minimal endpoint.

### Improved Cecotti exact reduction — 7 checks

- `P19.noscale.starobinsky_potential`
- `P19.noscale.canonical_log_modulus`
- `P19.noscale.stabilizer_hessian_mass`
- `P19.noscale.global_hessian_threshold`
- `P19.noscale.one_sixth_is_sufficient`
- `P19.noscale.gravitino_mass_on_path`
- `P19.noscale.nonzero_F_direction`

These checks derive the Starobinsky path, verify the degenerate path-local stabilizer Hessian, and show that \(\zeta>1/6\) is sufficient but not the sharp full-trajectory potential-Hessian threshold.

### Closed turning-point identities — 2 checks

- `P19.bounce.friedmann_constraint_at_turning_point`
- `P19.bounce.local_minimum_of_scale_factor`

The exact constraint fixes \(a_0\) only after \(\phi_0\) is supplied and gives a local scale-factor minimum. It does not select \(\phi_0\) or construct a CPT/Pin quantum state.

### Closed-background shooting — 24 checks

- `P19.quadratic_shift_symmetric.Nacc_50`
- `P19.quadratic_shift_symmetric.table_phi0_50`
- `P19.quadratic_shift_symmetric.table_a0_50`
- `P19.quadratic_shift_symmetric.friedmann_constraint_50`
- `P19.quadratic_shift_symmetric.Nacc_55`
- `P19.quadratic_shift_symmetric.table_phi0_55`
- `P19.quadratic_shift_symmetric.table_a0_55`
- `P19.quadratic_shift_symmetric.friedmann_constraint_55`
- `P19.quadratic_shift_symmetric.Nacc_60`
- `P19.quadratic_shift_symmetric.table_phi0_60`
- `P19.quadratic_shift_symmetric.table_a0_60`
- `P19.quadratic_shift_symmetric.friedmann_constraint_60`
- `P19.improved_cecotti_starobinsky.Nacc_50`
- `P19.improved_cecotti_starobinsky.table_phi0_50`
- `P19.improved_cecotti_starobinsky.table_a0_50`
- `P19.improved_cecotti_starobinsky.friedmann_constraint_50`
- `P19.improved_cecotti_starobinsky.Nacc_55`
- `P19.improved_cecotti_starobinsky.table_phi0_55`
- `P19.improved_cecotti_starobinsky.table_a0_55`
- `P19.improved_cecotti_starobinsky.friedmann_constraint_55`
- `P19.improved_cecotti_starobinsky.Nacc_60`
- `P19.improved_cecotti_starobinsky.table_phi0_60`
- `P19.improved_cecotti_starobinsky.table_a0_60`
- `P19.improved_cecotti_starobinsky.friedmann_constraint_60`

The 24 numerical checks cover two potentials, three target values \(N_{\rm acc}=50,55,60\), and four checks per row: target count, displayed \(\phi_0\), displayed radius, and Friedmann residual.

### First-order tensor comparison — 6 checks

- `P19.slowroll.quadratic_r_exceeds_current_N50`
- `P19.slowroll.starobinsky_r_below_current_N50`
- `P19.slowroll.quadratic_r_exceeds_current_N55`
- `P19.slowroll.starobinsky_r_below_current_N55`
- `P19.slowroll.quadratic_r_exceeds_current_N60`
- `P19.slowroll.starobinsky_r_below_current_N60`

These six checks compare only first-order potential slow-roll \(r\) values with the cited tensor limits. They do not perform a closed-bounce perturbation calculation, reheating map, or full \(n_s,r\) likelihood analysis.

## Phase 20 check ledger

### Leading de Sitter/WDW envelope — 12 exact plus 6 numerical checks

- `P20.WDW.hemisphere_action_normalization`
- `P20.WDW.action_derivative`
- `P20.WDW.standard_history_weight_slope`
- `P20.WDW.independent_pair_weight_slope`
- `P20.WDW.pair_slope_factor_two`
- `P20.WDW.no_finite_stationary_envelope`
- `P20.WDW.asymptotic_zero_slope_only`
- `P20.WDW.conjugate_saddle_interference`
- `P20.WDW.independent_pair_joint_probability`
- `P20.WDW.constant_symmetrization_does_not_move_slope`
- `P20.WDW.starobinsky_epsilon`
- `P20.WDW.constant_field_is_not_exact_saddle`
- `P20.numeric.standard_slope_coefficient`
- `P20.numeric.pair_slope_coefficient`
- `P20.numeric.standard_central_difference`
- `P20.numeric.pair_central_difference`
- `P20.numeric.HH_and_tunneling_opposite_monotonicity`
- `P20.numeric.slow_roll_not_constant_field`

The standard history probability is proportional to \(e^{2sI}\). The doubled-slope \(e^{4sI}\) expression is checked only as the joint probability of an independently factorized pair; it is not derived from CPT sewing. Both leading envelopes are monotone at the Phase 19 benchmark. The same group verifies the order-one coherent \(\cos^2S\) identity and that the benchmark has small but nonzero \(\epsilon_V\), so the calculation is not promoted to an exact Starobinsky WDW saddle or no-go theorem.

### Cecotti auxiliary direction — 5 exact plus 2 numerical checks

- `P20.SUSY.cecotti_DSW`
- `P20.SUSY.cecotti_inverse_metric`
- `P20.SUSY.cecotti_auxiliary`
- `P20.SUSY.cecotti_potential`
- `P20.SUSY.static_F_flat_point`
- `P20.numeric.T_star`
- `P20.numeric.nonzero_F_star`

These checks give \(T_*=85.1288467\ldots\) and \(F^S/M=-6.4475031\ldots\), contradicting classical F-flatness at \(\varphi_*=5.442969458\). They do not solve the coupled quantum local-SUSY constraints or exclude wavefunction support there.

### Conditional curvature–reheating bridge — 1 exact plus 6 numerical checks

- `P20.curvature.matterlike_temperature_exponent`
- `P20.numeric.phase19_Nacc_bridge`
- `P20.numeric.phase19_rho_end_bridge`
- `P20.numeric.phase19_constraint_bridge`
- `P20.numeric.curvature_reheating_coefficient`
- `P20.numeric.curvature_reheating_inverse`
- `P20.numeric.closed_curvature_sign`

The bridge independently recovers the Phase 19 60-e-fold endpoint and, for the frozen inputs, obtains \(\Omega_{K0}=-5.5258\times10^{-4}(T_{\rm reh}/10^9\,{\rm GeV})^{2/3}\). The sign, branch choice, reheating equation of state, temperature, entropy factors, units, and late-time constants are all explicit inputs. This is a reproducible conversion, not a curvature detection or seam prediction.

## Reproduction commands

The commands recorded in the snapshots are:

```bash
uv run --locked python3 cpt_temporal_folded_susy/phase16_bgg_single_source.py
uv run --locked python3 cpt_temporal_folded_susy/phase17_time_line_fold_algebra.py
uv run --locked python3 cpt_temporal_folded_susy/phase18_gaussian_seam_spectrum.py
uv run --locked python3 cpt_temporal_folded_susy/phase19_closed_sugra_bounce.py
uv run --locked python3 cpt_temporal_folded_susy/phase20_two_sheet_wdw_selection.py
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

Phase 20's central bounded trace is:

```text
claim:P20_LEADING_DE_SITTER_WDW_ENVELOPE_SELECTS_5P44
  → HAS_EVIDENCE {polarity: CONTRADICTS}
  → evidence:p20-leading-wdw-envelope
  → DEFINED_IN → artifact:p20-script
  → RECORDED_IN → artifact:p20-evidence-snapshot
  → VALID_WITHIN → scope:p20-leading-de-sitter-wdw-control
  → MOTIVATES → open:p20-exact-starobinsky-wdw-state
```

The scope edge is essential: the trace concerns the leading constant-field envelope, not an exact two-sheet local-SUGRA WDW no-go.

The [programme guide](../README.md) lists every scope and open problem; the [source inventory](./source-inventory.md) explains what the literature edges do and do not cover.
