# Evidence guide

> This page is a human-readable memory and index over observed repository runs. It is **not** a preregistration, research contract, independent replication, peer review, final scientific verdict, or KG ratification.

Machine-readable records: [`graph.json`](../graph.json), [`phase16-result.json`](../evidence/phase16-result.json), [`phase17-result.json`](../evidence/phase17-result.json), [`phase18-result.json`](../evidence/phase18-result.json), [`phase19-result.json`](../evidence/phase19-result.json), [`phase20-result.json`](../evidence/phase20-result.json), [`phase21-result.json`](../evidence/phase21-result.json), [`phase22-result.json`](../evidence/phase22-result.json), and [`phase23-result.json`](../evidence/phase23-result.json).

## Reading `PASS` correctly

All 226 Phase 16–23 named exact checks have `status: PASS`. The snapshots also record 56 numerical checks: one Phase 18 SciPy control, 30 Phase 19 background/slow-roll checks, 14 Phase 20 benchmark/bridge checks, 7 Phase 21 flux-tail/prior controls, and 4 Phase 23 normalization, convergence, spectrum, and current controls. Phase 22 contributes 31 exact checks and no numerical fit; Phase 23 contributes 32 exact and 4 numerical checks. A `PASS` means that an executable verified its stated equality, rank, obstruction, mutation rejection, counterexample, or bounded numerical comparison. It does not mean every scientific claim passed.

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
| 21 | `result:P21_CONNECTED_SEAM_GAUSSIAN_20260816`; `2026-08-16T18:11:47Z` | `cpt_temporal_folded_susy/phase21_connected_seam_gaussian.py`; SHA-256 `6ac7b2b36da9aa2eeda4c83494427c5d9f006bb9031d6b55d6678bf2ffc5b005`; introduced in `44e2865cc850bf7fef0c4ccebde788ca703ab8d8` | Exit `0`; 27 exact checks plus 7 numerical checks |
| 22 | `result:P22_FINITE_MODE_SEAM_DENSITY_20260817`; `2026-08-17T04:48:31Z` | `cpt_temporal_folded_susy/phase22_finite_mode_seam_density.py`; SHA-256 `0a4da3c60bbd2231892938cb8a74f45bd3e491d9884df4adcc86051053d58dbe`; introduced in `d1befe783386f499818c3b902c90e5a9740e7fb4` | Exit `0`; 31 exact checks, 0 numerical checks |
| 23 | `result:P23_HOMOGENEOUS_MINISUPERSPACE_DENSITY_20260817`; `2026-08-17T05:45:44Z` | `cpt_temporal_folded_susy/phase23_homogeneous_minisuperspace_density.py`; SHA-256 `62408abeeec2eb11f104d984c84ffde5c2d6f287e7f07a4021ee6fb3ec202ffd`; introduced in `634d984e25422063a66a497963380fc24ad9f9d2` | Exit `0`; 32 exact checks plus 4 numerical checks |

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
| `evidence:p21-single-mode-gaussian` | 12 exact | Unit baseline — `SUPPORTS`; normalization forces subtraction — `CONTRADICTS`; chosen zero-insertion identity — `SUPPORTS`; R-1 is connected — `CONTRADICTS`; log R is connected — `SUPPORTS` | Positive finite one-mode real-boson Gaussian only |
| `evidence:p21-multimode-gaussian` | 4 exact | Log R is the connected generator — `SUPPORTS` | Finite positive block kernel and singular-value gate; no field-theory determinant |
| `evidence:p21-flux-tail-and-prior` | 11 exact + 7 numerical | Reference subtraction guarantees normalizability — `CONTRADICTS`; one-flux constant-absolute toy sum — `SUPPORTS`; R-1 alone fixes physical flux probability — `CONTRADICTS` | One integer-flux toy with imposed kernel and prior comparisons; no WDW measure or joint \((n,\phi)\) distribution |
| `evidence:p22-susy-and-density` | 16 exact | Positive-frequency density — `SUPPORTS`; reduced Gibbs covariance — `SUPPORTS` | One free SUSY oscillator with \(\omega,\beta>0\); finite temperature is not an unbroken positive-H vacuum |
| `evidence:p22-graded-real-structure` | 5 exact | Graded anti-linear toy involution — `SUPPORTS` | Occupation-basis real structure only; no spacetime Clifford/Pin lift |
| `evidence:p22-bridge-and-sk` | 6 exact | Density/DtN factor two — `SUPPORTS`; equal-source SK normalization — `SUPPORTS` | Finite density covariance and unitarity; no SK ghost/BRST completion |
| `evidence:p22-zero-mode-obstruction` | 4 exact | Free noncompact zero mode has a trace-class TFD limit — `CONTRADICTS` | Fixed \(\beta>0\), \(\omega\to0^+\) in noncompact \(L^2(\mathbb R)\); compact/interacting constrained modes excluded |
| `evidence:p23-rigging-and-lapse` | 10 exact + 1 numerical | Full real lapse gives a distributional rigging map — `SUPPORTS`; it is a bounded kinematical projector — `CONTRADICTS` | Continuous single-constraint spectral calibration; half lapse is a resolvent, not the full rigging delta; Marolf frames RAQ |
| `evidence:p23-shell-and-current` | 10 exact + 1 numerical | Explicit clock/frequency gives positive integrated norm — `SUPPORTS`; positive-frequency local current is pointwise positive — `CONTRADICTS`; CPT-like reality plus zero signed current uniquely selects a density — `CONTRADICTS` | Compact KG-type shell/current control; induced product and signed local current remain distinct |
| `evidence:p23-trace-class-density` | 8 exact + 2 numerical | Imposed bridge gives a positive trace-class regulated density — `SUPPORTS`; unique selection from zero current — `CONTRADICTS` | Separate compact calibration with supplied \(L>0\), \(B_L\), branch orientation, and toy pairing; not cap-derived |
| `evidence:p23-zero-root-and-regulator` | 4 exact | Trace class survives massless decompactification — `CONTRADICTS`; quadratic zero root has a regular intrinsic clock — `CONTRADICTS` | Explicit double-root and massless-box obstruction models; not a universal homogeneous-density no-go |

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

## Phase 21 check ledger

### Single-mode normalized Gaussian — 12 exact checks

- `P21.gaussian.kernel_determinant`
- `P21.gaussian.schur_factorization`
- `P21.gaussian.inverse_covariance`
- `P21.gaussian.normalized_ratio`
- `P21.gaussian.no_seam_baseline`
- `P21.gaussian.nonempty_bridge_series`
- `P21.gaussian.connected_log_series`
- `P21.gaussian.remainder_is_exponential_of_connected`
- `P21.gaussian.order_four_disconnected_piece`
- `P21.gaussian.source_derivative_correlation`
- `P21.gaussian.ratio_even_correlation_odd`
- `P21.gaussian.symmetric_normal_modes`

These checks establish \(R(0)=1\), the conditional identity for a chosen zero-insertion exclusion,
and the distinction \(R-1=\exp(\log R)-1\). They do not define an exclusive event or Born
probability.

### Multimode determinant — 4 exact checks

- `P21.multimode.schur_determinant`
- `P21.multimode.determinant_ratio`
- `P21.multimode.connected_trace_expansion`
- `P21.multimode.positivity_singular_value_gate`

The finite block result is \(R=\det(I-K^TK)^{-1/2}\), with
\(\log R=\tfrac12\sum_{j\ge1}{\rm Tr}[(K^TK)^j]/j\). Infinite-mode UV control and any
fermionic/Pfaffian phase remain outside this group.

### Flux tails, finite parts, and imposed priors — 11 exact plus 7 numerical checks

- `P21.flux.absolute_coupling_remainder_tail`
- `P21.flux.absolute_coupling_log_tail`
- `P21.flux.sector_partition_difference_tail`
- `P21.flux.relative_coupling_constant_tail`
- `P21.flux.normalized_ratio_lattice_dimension_threshold`
- `P21.flux.sector_difference_lattice_dimension_threshold`
- `P21.flux.relative_sector_difference_dimension_threshold`
- `P21.flux.WDW_HH_excess_tail`
- `P21.flux.WDW_tunneling_deficit_tail`
- `P21.flux.WDW_reference_lattice_dimension_threshold`
- `P21.regularization.constant_tail_finite_part`
- `P21.numeric.absolute_coupling_sum`
- `P21.numeric.connected_generator_sum`
- `P21.numeric.truncation_convergence`
- `P21.numeric.flat_remainder_zero_sector_peak`
- `P21.numeric.sector_partition_difference_sum`
- `P21.numeric.sector_partition_prior_dependence`
- `P21.numeric.relative_coupling_linear_divergence`

The recorded one-flux constant-absolute toy is summable. Its flat-sector \(R_n-1\) weighting has
\(p_0=0.484950\ldots\), while retaining \(Z_n(0)\) gives \(0.626161\ldots\). This is a
prior-dependence witness, not an inflationary flux prediction. The lattice thresholds are stated
weight by weight: \(d<4\) for the \(n^{-4}\) normalized-ratio tails, \(d<6\) for the
\(n^{-6}\) absolute sector difference, and \(d<2\) for the \(n^{-2}\) reference or
relative-coupling sector-difference tails.

## Phase 22 check ledger

### Fixed-energy SUSY and finite density — 16 exact checks

- `P22.susy.charge_nilpotent`
- `P22.susy.adjoint_nilpotent`
- `P22.susy.positive_closure`
- `P22.susy.energy_conservation`
- `P22.susy.fermion_oddness`
- `P22.density.boson_geometric_norm`
- `P22.density.fermion_pair_norm`
- `P22.density.pure_projector_hermitian`
- `P22.density.pure_projector_trace_one`
- `P22.density.pure_projector_idempotent_rank_one`
- `P22.density.partial_trace`
- `P22.density.reduced_trace`
- `P22.density.full_reduced_positivity`
- `P22.density.gibbs_partition`
- `P22.density.supermultiplet_equal_weights`
- `P22.density.finite_temperature_not_zero_energy`

These checks establish a normalized positive purification and a positive reduced Gibbs density for
\(0<r=e^{-\beta\omega}<1\). The density commutes with the fixed-mode charges because both members of
each positive-energy supermultiplet have equal weight. The positive energy at finite \(\beta\) is a
separate exact guard against calling this an unbroken thermal vacuum.

### Graded anti-linear real structure — 5 exact checks

- `P22.theta.involution_square`
- `P22.theta.state_invariance`
- `P22.theta.parity_compatibility`
- `P22.theta.energy_compatibility`
- `P22.theta.ungraded_swap_mutant_rejected`

The displayed phase and graded swap define an exact occupation-space toy involution. They do not
construct a 4D Clifford reflection, spin structure, reflection square, or local-SUGRA Pin gluing law.

### Euclidean bridge and SK trace — 6 exact checks

- `P22.bridge.local_covariance`
- `P22.bridge.cross_covariance`
- `P22.bridge.normalized_coefficient`
- `P22.bridge.amplitude_density_factor_two`
- `P22.SK.equal_source_unitarity`
- `P22.SK.wrong_adjoint_mutant_rejected`

The density covariance is \((2K_{\rm DtN})^{-1}\), while \(K_{\rm DtN}\) is the amplitude Hessian.
The SK check is the exact unitary identity \({\rm Tr}(U\rho U^\dagger)=1\); it is not a constructed
ghost quartet or BRST cohomology.

### Noncompact free zero-mode obstruction — 4 exact checks

- `P22.zero_mode.boson_partition_diverges`
- `P22.zero_mode.fermion_partition_finite`
- `P22.zero_mode.coordinate_variance_diverges`
- `P22.zero_mode.diagonal_stiffness_vanishes`

The payload records `P22.guard.free_noncompact_zero_mode_trace_class` with
`EXPECTED_OBSTRUCTION_CONFIRMED`. It is bounded to the unregulated noncompact free oscillator; a compact
mode or the interacting constrained \((a,\phi)\) sector requires a separate physical measure and
zero-mode treatment.

## Phase 23 check ledger

### Full-lapse rigging and seed calibration — 10 exact plus 1 numerical check

- `P23.rigging.full_real_lapse_abel_kernel`
- `P23.rigging.abel_delta_normalization`
- `P23.rigging.full_real_lapse_gaussian_kernel`
- `P23.rigging.kinematical_gaussian_norm`
- `P23.rigging.regulated_seed_norm`
- `P23.rigging.normalized_shell_profile`
- `P23.rigging.not_a_bounded_kinematical_projector`
- `P23.rigging.half_lapse_is_resolvent`
- `P23.rigging.half_lapse_is_not_projector_kernel`
- `P23.rigging.naive_euclidean_lapse_mutant_diverges`
- `P23.numeric.regulated_seed_norm`

The full real lapse gives normalized Abel and Gaussian delta sequences for one constraint. The Gaussian
seed is normalized before rigging and reduces to its chosen normalized shell profile after division by
the square root of the rigging norm. This continuous spectral calibration is distributional: the kernel
supremum diverges, the positive half-lapse transform is a resolvent, and a naive Euclidean exponential
diverges on the negative spectrum. It is separate from the compact density calibration below.

### Shell, branch, and current control — 10 exact plus 1 numerical check

- `P23.constraint.dirichlet_spectrum`
- `P23.constraint.frequency_roots`
- `P23.constraint.delta_shell_jacobian`
- `P23.constraint.clock_gauge_FP_cancellation`
- `P23.WDW.frequency_modes_solve_constraint`
- `P23.current.integrated_frequency_signs`
- `P23.current.induced_sum_vs_signed_difference`
- `P23.current.two_mode_continuity`
- `P23.current.integrated_density_equals_trace`
- `P23.current.local_density_not_pointwise_positive`
- `P23.numeric.current_slice_conservation`

For the compact Dirichlet normal form, the two simple roots have opposite integrated Klein–Gordon signs.
Choosing the \(T\)-clock and one frequency orientation supplies a positive integrated norm; the quadratic
constraint alone does not. An equal-weight relative-phase family has unit induced norm and zero signed
current, with orthogonal real witnesses, so zero current does not select a unique state. Separately, the
positive-frequency two-mode state has conserved unit integrated current but the exact local value
\(-55/(768\pi)\), so the local current is not a pointwise Born probability.

### Supplied compact bridge and density — 8 exact plus 2 numerical checks

- `P23.density.spectral_comparison_gap`
- `P23.density.trace_class_geometric_bound`
- `P23.density.truncated_purification`
- `P23.density.partial_trace_positive`
- `P23.density.spectral_stationarity`
- `P23.density.bridge_weight_ratio`
- `P23.theta.toy_pairing`
- `P23.selection.preparation_length_remains_input`
- `P23.numeric.trace_sum_convergence`
- `P23.numeric.two_mode_density_spectrum`

With supplied \(L>0\), \(B_L=e^{-L\sqrt h}\), and two outward-positive constrained copies, comparison
with a geometric series proves the infinite compact spectral sum is trace class. The finite matrix checks
verify purification, reduction, positivity, and the toy anti-linear pairing; the numerical sum gives
\(Z_L=0.072625937359366\) at \(\mu=L=1\). Neither group averaging nor CPT-like pairing derives \(L\),
the compact regulator, or the relative weights.

### Zero root and decompactification — 4 exact checks

- `P23.zero_root.quadratic_root_divergence`
- `P23.zero_root.clock_FP_vanishes`
- `P23.zero_root.linear_constraint_control`
- `P23.regulator.decompactification_not_trace_class`

At the quadratic \(E=0\) root, the regulated shell integral diverges as \(1/\sqrt{2\epsilon}\) and the
intrinsic-clock determinant vanishes. A linear constraint removes that double root only by choosing an
orientation. In the separate massless box, \(Z_R\sim R/(2L)\), so the compact trace-class result has no
trace-class decompactification limit in this control. These witnesses do not prove that the Starobinsky
homogeneous mode is gauge or rule out compact/interacting constrained models.

## Reproduction commands

The commands recorded in the snapshots are:

```bash
uv run --locked python3 cpt_temporal_folded_susy/phase16_bgg_single_source.py
uv run --locked python3 cpt_temporal_folded_susy/phase17_time_line_fold_algebra.py
uv run --locked python3 cpt_temporal_folded_susy/phase18_gaussian_seam_spectrum.py
uv run --locked python3 cpt_temporal_folded_susy/phase19_closed_sugra_bounce.py
uv run --locked python3 cpt_temporal_folded_susy/phase20_two_sheet_wdw_selection.py
uv run --locked python3 cpt_temporal_folded_susy/phase21_connected_seam_gaussian.py
uv run --locked python3 cpt_temporal_folded_susy/phase22_finite_mode_seam_density.py
uv run --locked python3 cpt_temporal_folded_susy/phase23_homogeneous_minisuperspace_density.py
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

Phase 21's central distinction is:

```text
claim:P21_R_MINUS_ONE_IS_CONNECTED_VACUUM_FUNCTIONAL
  → HAS_EVIDENCE {polarity: CONTRADICTS}
  → evidence:p21-single-mode-gaussian
  → DEFINED_IN → artifact:p21-script
  → RECORDED_IN → artifact:p21-evidence-snapshot
  → VALID_WITHIN → scope:p21-positive-euclidean-gaussian

claim:P21_LOG_R_IS_CONNECTED_VACUUM_GENERATOR
  ├─ HAS_EVIDENCE {polarity: SUPPORTS} → evidence:p21-single-mode-gaussian
  ├─ HAS_EVIDENCE {polarity: SUPPORTS} → evidence:p21-multimode-gaussian
  └─ VALID_WITHIN → scope:p21-positive-euclidean-gaussian
```

Neither trace supplies the separate physical flux-sector measure represented by
`open:p21-physical-flux-measure`.

Phase 22's positive and obstructed traces are:

```text
claim:P22_POSITIVE_FREQUENCY_TFD_LIKE_DENSITY_IS_NORMALIZED_AND_POSITIVE
  → HAS_EVIDENCE {polarity: SUPPORTS}
  → evidence:p22-susy-and-density
  → DEFINED_IN → artifact:p22-script
  → RECORDED_IN → artifact:p22-evidence-snapshot
  → VALID_WITHIN → scope:p22-positive-frequency-finite-mode-density

claim:P22_FREE_NONCOMPACT_ZERO_MODE_HAS_TRACE_CLASS_TFD_LIMIT
  → HAS_EVIDENCE {polarity: CONTRADICTS}
  → evidence:p22-zero-mode-obstruction
  → DEFINED_IN → artifact:p22-script
  → RECORDED_IN → artifact:p22-evidence-snapshot
  → VALID_WITHIN → scope:p22-noncompact-zero-mode-limit
  → MOTIVATES → open:p22-homogeneous-minisuperspace-density
```

Phase 23's supplied positive density and selection obstruction are:

```text
claim:P23_IMPOSED_BRIDGE_DEFINES_POSITIVE_TRACE_CLASS_REGULATED_DENSITY
  → HAS_EVIDENCE {polarity: SUPPORTS}
  → evidence:p23-trace-class-density
  → DEFINED_IN → artifact:p23-script
  → RECORDED_IN → artifact:p23-evidence-snapshot
  → VALID_WITHIN → scope:p23-supplied-bridge-compact-density
  → MOTIVATES → open:p23-cap-derived-regulator-independent-density

claim:P23_CPT_REALITY_AND_ZERO_SIGNED_CURRENT_UNIQUELY_SELECT_A_DENSITY
  ├─ HAS_EVIDENCE {polarity: CONTRADICTS} → evidence:p23-shell-and-current
  ├─ HAS_EVIDENCE {polarity: CONTRADICTS} → evidence:p23-trace-class-density
  └─ VALID_WITHIN → scope:p23-supplied-bridge-compact-density
```

The first trace proves only a supplied compact regulated density. The full-lapse rigging map does not
derive \(B_L\), and neither trace is a cap-derived cosmological Born measure or local-SUGRA/BRST state.

The [programme guide](../README.md) lists every scope and open problem; the [source inventory](./source-inventory.md) explains what the literature edges do and do not cover.
