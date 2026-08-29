export const excludedTopLevelKeys = new Set([
  "verdict",
  "verdict_reasoning",
  "verdict_source",
  "verdict_date",
  "self_refutation",
  "sub_verdicts",
  "verdict_provenance",
  "verdict_reasoning_prior",
  "mc_evidence_ref",
  "mc_null_model",
  "mc_p_e_given_not_h",
  "mc_verdict_reasoning",
  "mc_layer1_rel_diff_literal_pct",
  "mc_layer1_rel_diff_reciprocal_pct",
  "mc_null_model_layer3",
  "mc_p_e_given_not_h_layer3",
  "researchedAt",
  "timestamp",
  "generated_at",
  "createdAt",
  "run_at"
])

export interface DefaultNumericRule {
  readonly kind: "close"
  readonly relativeTolerance: number
  readonly absoluteTolerance: number
}

export type PathNumericRule =
  | {
      readonly path: string
      readonly kind: "close"
      readonly relativeTolerance: number
      readonly absoluteTolerance: number
    }
  | {
      readonly path: string
      readonly kind: "circular"
      readonly period: number
      readonly absoluteTolerance: number
    }
  | {
      readonly path: string
      readonly kind: "near-zero"
      readonly absoluteTolerance: number
    }

export interface ComparePolicy {
  readonly defaultNumeric: DefaultNumericRule
  readonly pathRules?: ReadonlyArray<PathNumericRule>
}

export type ReproCase =
  | {
      readonly name: string
      readonly script: string
      readonly output: string
      readonly policy: "portable"
      readonly compare: ComparePolicy
    }
  | {
      readonly name: string
      readonly script: string
      readonly output: string
      readonly policy: "nonportable"
      readonly reason: string
    }
  | {
      readonly name: string
      readonly script: string
      readonly output: string
      readonly policy: "superseded"
      readonly reason: string
    }

const tight: ComparePolicy = {
  defaultNumeric: {
    kind: "close",
    relativeTolerance: 1e-12,
    absoluteTolerance: 1e-15
  }
}

export const reproCases = [
  {
    name: "derive_Lstar_from_ICE",
    script: "research/legacy_predictions/derive_Lstar_from_ICE.py",
    output: "research/legacy_predictions/derive_Lstar_results.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "derive_dimensionless_ICE",
    script: "research/legacy_predictions/derive_dimensionless_ICE.py",
    output: "research/legacy_predictions/derive_dimensionless_results.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "derive_mass_ratios_ICE",
    script: "research/legacy_predictions/derive_mass_ratios_ICE.py",
    output: "research/legacy_predictions/derive_mass_ratios_results.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "prove_higgs_ZD_doublet",
    script: "research/hypercomplex/prove_higgs_ZD_doublet.py",
    output: "research/hypercomplex/prove_higgs_results.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "prove_s3_higher_gauge",
    script: "research/hypercomplex/prove_s3_higher_gauge.py",
    output: "research/hypercomplex/prove_s3_results.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "prove_s5_bv_ainfty",
    script: "research/hypercomplex/prove_s5_bv_ainfty.py",
    output: "research/hypercomplex/prove_s5_results.json",
    policy: "portable",
    compare: {
      ...tight,
      pathRules: [
        {
          path: "$.S5.4.s5_4_master_residual",
          kind: "near-zero",
          absoluteTolerance: 1e-12
        }
      ]
    }
  },
  {
    name: "queue_01_orbit_analysis",
    script: "research/hypercomplex/queue_01_orbit_analysis.py",
    output: "research/hypercomplex/queue_01_orbit_results.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "queue_03_threshold_sensitivity_scan",
    script: "research/hypercomplex/queue_03_threshold_sensitivity_scan.py",
    output: "research/hypercomplex/queue_03_threshold_sensitivity_results.json",
    policy: "nonportable",
    reason:
      "legacy metric max(abs(commutator)) depends on scipy null_space's arbitrary orthogonal basis; a tolerance cannot repair changed pass/fail counts"
  },
  {
    name: "queue_04_hosotani_toy",
    script: "research/hypercomplex/queue_04_hosotani_toy.py",
    output: "research/hypercomplex/queue_04_hosotani_results.json",
    policy: "portable",
    compare: {
      ...tight,
      pathRules: [
        {
          path: "$.case3_realistic.best_theta[*]",
          kind: "circular",
          period: 2 * Math.PI,
          absoluteTolerance: 1e-6
        },
        {
          path: "$.case3_realistic.theta_spread",
          kind: "close",
          relativeTolerance: 0,
          absoluteTolerance: 1e-6
        }
      ]
    }
  },
  {
    name: "queue_05_coleman_weinberg",
    script: "research/hypercomplex/queue_05_coleman_weinberg.py",
    output: "research/hypercomplex/queue_05_cw_results.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "queue_06_cooperative_vacuum",
    script: "research/hypercomplex/queue_06_cooperative_vacuum.py",
    output: "research/hypercomplex/queue_06_coop_results.json",
    policy: "superseded",
    reason:
      "committed output is generated by inconclusive_redo.py (method_fix and larger n_trials), not by the mapped historical script"
  },
  {
    name: "queue_10_group_of_6",
    script: "research/hypercomplex/queue_10_group_of_6.py",
    output: "research/hypercomplex/queue_10_group6_results.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "queue_11_xor_invariant",
    script: "research/hypercomplex/queue_11_xor_invariant.py",
    output: "research/hypercomplex/queue_11_xor_results.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "verify_mp_mW_3_256",
    script: "research/legacy_predictions/verify_mp_mW_3_256.py",
    output: "research/legacy_predictions/verify_mp_mW_results.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "gate1_v0_principal_endpoint_fio",
    script: "cpt_temporal_folded_susy/gate1_v0_principal_endpoint_fio.py",
    output:
      "cpt_temporal_folded_susy/GATE1_V0_PRINCIPAL_ENDPOINT_FIO_RESULT.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "gate1_v0_improved_static_bfv_source",
    script: "cpt_temporal_folded_susy/gate1_v0_improved_static_bfv_source.py",
    output:
      "cpt_temporal_folded_susy/GATE1_V0_IMPROVED_STATIC_BFV_SOURCE_RESULT.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "gate1_v0_constraint_spectral_domain",
    script: "cpt_temporal_folded_susy/gate1_v0_constraint_spectral_domain.py",
    output:
      "cpt_temporal_folded_susy/GATE1_V0_CONSTRAINT_SPECTRAL_DOMAIN_RESULT.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "gate1_v0_endpoint_subprincipal_nonuniqueness",
    script:
      "cpt_temporal_folded_susy/gate1_v0_endpoint_subprincipal_nonuniqueness.py",
    output:
      "cpt_temporal_folded_susy/GATE1_V0_ENDPOINT_SUBPRINCIPAL_NONUNIQUENESS_RESULT.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "gate1_v0_static_spectral_pairing",
    script: "cpt_temporal_folded_susy/gate1_v0_static_spectral_pairing.py",
    output:
      "cpt_temporal_folded_susy/GATE1_V0_STATIC_SPECTRAL_PAIRING_RESULT.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "gate1_v0_bfv_m2_spectral_trajectory",
    script: "cpt_temporal_folded_susy/gate1_v0_bfv_m2_spectral_trajectory.py",
    output:
      "cpt_temporal_folded_susy/GATE1_V0_BFV_M2_SPECTRAL_TRAJECTORY_RESULT.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "gate1_v0_densitized_liouville_raq",
    script: "cpt_temporal_folded_susy/gate1_v0_densitized_liouville_raq.py",
    output:
      "cpt_temporal_folded_susy/GATE1_V0_DENSITIZED_LIOUVILLE_RAQ_RESULT.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "gate1_v0_densitized_raq_p_zero_boundary",
    script:
      "cpt_temporal_folded_susy/gate1_v0_densitized_raq_p_zero_boundary.py",
    output:
      "cpt_temporal_folded_susy/GATE1_V0_DENSITIZED_RAQ_P_ZERO_BOUNDARY_RESULT.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "gate1_v0_full_p_regular_raq_completion",
    script:
      "cpt_temporal_folded_susy/gate1_v0_full_p_regular_raq_completion.py",
    output:
      "cpt_temporal_folded_susy/GATE1_V0_FULL_P_REGULAR_RAQ_COMPLETION_RESULT.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "gate1_v0_raw_c_weighted_operator_domain_audit",
    script:
      "cpt_temporal_folded_susy/gate1_v0_raw_c_weighted_operator_domain_audit.py",
    output:
      "cpt_temporal_folded_susy/GATE1_V0_RAW_C_WEIGHTED_OPERATOR_DOMAIN_AUDIT_RESULT.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "raw_c_constant_boundary_direct_integral",
    script:
      "cpt_temporal_folded_susy/raw_c_constant_boundary_direct_integral.py",
    output:
      "cpt_temporal_folded_susy/RAW_C_CONSTANT_BOUNDARY_DIRECT_INTEGRAL_RESULT.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "gate1_v0_endpoint_support_restricted_spectral_intertwiner",
    script:
      "cpt_temporal_folded_susy/gate1_v0_endpoint_support_restricted_spectral_intertwiner.py",
    output:
      "cpt_temporal_folded_susy/GATE1_V0_ENDPOINT_SUPPORT_RESTRICTED_SPECTRAL_INTERTWINER_RESULT.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "gate1_v0_bfv_zero_mode_elimination_ward",
    script:
      "cpt_temporal_folded_susy/gate1_v0_bfv_zero_mode_elimination_ward.py",
    output:
      "cpt_temporal_folded_susy/GATE1_V0_BFV_ZERO_MODE_ELIMINATION_WARD_RESULT.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "gate1_v0_bfv_finite_pfaffian_orientation_transport",
    script:
      "cpt_temporal_folded_susy/gate1_v0_bfv_finite_pfaffian_orientation_transport.py",
    output:
      "cpt_temporal_folded_susy/GATE1_V0_BFV_FINITE_PFAFFIAN_ORIENTATION_TRANSPORT_RESULT.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "gate1_v0_closed_s3_scalar_harmonic_projection_ledger",
    script:
      "cpt_temporal_folded_susy/gate1_v0_closed_s3_scalar_harmonic_projection_ledger.py",
    output:
      "cpt_temporal_folded_susy/GATE1_V0_CLOSED_S3_SCALAR_HARMONIC_PROJECTION_LEDGER_RESULT.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "closed_s3_adm_linear_scalar_convention_audit",
    script:
      "cpt_temporal_folded_susy/closed_s3_adm_linear_scalar_convention_audit.py",
    output:
      "cpt_temporal_folded_susy/CLOSED_S3_ADM_LINEAR_SCALAR_CONVENTION_AUDIT_RESULT.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "closed_s3_scalar_derived_harmonic_ledger",
    script:
      "cpt_temporal_folded_susy/closed_s3_scalar_derived_harmonic_ledger.py",
    output:
      "cpt_temporal_folded_susy/CLOSED_S3_SCALAR_DERIVED_HARMONIC_LEDGER_RESULT.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "v0_two_clock_relational_observable_comparison",
    script:
      "cpt_temporal_folded_susy/v0_two_clock_relational_observable_comparison.py",
    output:
      "cpt_temporal_folded_susy/V0_TWO_CLOCK_RELATIONAL_OBSERVABLE_COMPARISON_RESULT.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "bfv_parametrized_particle_gluing_calibration",
    script:
      "cpt_temporal_folded_susy/bfv_parametrized_particle_gluing_calibration.py",
    output:
      "cpt_temporal_folded_susy/BFV_PARAMETRIZED_PARTICLE_GLUING_CALIBRATION_RESULT.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "closed_starobinsky_background_export_audit",
    script:
      "cpt_temporal_folded_susy/closed_starobinsky_background_export_audit.py",
    output:
      "cpt_temporal_folded_susy/CLOSED_STAROBINSKY_BACKGROUND_EXPORT_AUDIT_RESULT.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "raw_c_zero_shell_characteristic_census",
    script:
      "cpt_temporal_folded_susy/raw_c_zero_shell_characteristic_census.py",
    output:
      "cpt_temporal_folded_susy/RAW_C_ZERO_SHELL_CHARACTERISTIC_CENSUS_RESULT.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "closed_s3_zonal_scalar_convolution_cutoff_ledger",
    script:
      "cpt_temporal_folded_susy/closed_s3_zonal_scalar_convolution_cutoff_ledger.py",
    output:
      "cpt_temporal_folded_susy/CLOSED_S3_ZONAL_SCALAR_CONVOLUTION_CUTOFF_LEDGER_RESULT.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "closed_s3_full_svt_spectral_ledger",
    script:
      "cpt_temporal_folded_susy/closed_s3_full_svt_spectral_ledger.py",
    output:
      "cpt_temporal_folded_susy/CLOSED_S3_FULL_SVT_SPECTRAL_LEDGER_RESULT.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "homogeneous_closed_frw_starobinsky_two_clock_fp_domain_audit",
    script:
      "cpt_temporal_folded_susy/homogeneous_closed_frw_starobinsky_two_clock_fp_domain_audit.py",
    output:
      "cpt_temporal_folded_susy/HOMOGENEOUS_CLOSED_FRW_STAROBINSKY_TWO_CLOCK_FP_DOMAIN_AUDIT_RESULT.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "raw_c_zero_shell_transversality_jacobian",
    script:
      "cpt_temporal_folded_susy/raw_c_zero_shell_transversality_jacobian.py",
    output:
      "cpt_temporal_folded_susy/RAW_C_ZERO_SHELL_TRANSVERSALITY_JACOBIAN_RESULT.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "closed_s3_zonal_conformal_curvature_cubic_vertex_ledger",
    script:
      "cpt_temporal_folded_susy/closed_s3_zonal_conformal_curvature_cubic_vertex_ledger.py",
    output:
      "cpt_temporal_folded_susy/CLOSED_S3_ZONAL_CONFORMAL_CURVATURE_CUBIC_VERTEX_LEDGER_RESULT.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "raw_c_nonzero_lambda_weyl_flambda_check",
    script:
      "cpt_temporal_folded_susy/raw_c_nonzero_lambda_weyl_flambda_check.py",
    output:
      "cpt_temporal_folded_susy/RAW_C_NONZERO_LAMBDA_WEYL_FLAMBDA_CHECK_RESULT.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "closed_s3_zonal_conformal_trace_kinetic_cubic_vertex_ledger",
    script:
      "cpt_temporal_folded_susy/closed_s3_zonal_conformal_trace_kinetic_cubic_vertex_ledger.py",
    output:
      "cpt_temporal_folded_susy/CLOSED_S3_ZONAL_CONFORMAL_TRACE_KINETIC_CUBIC_VERTEX_LEDGER_RESULT.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "closed_s3_zonal_conformal_v0_scalar_matter_cubic_vertex_ledger",
    script:
      "cpt_temporal_folded_susy/closed_s3_zonal_conformal_v0_scalar_matter_cubic_vertex_ledger.py",
    output:
      "cpt_temporal_folded_susy/CLOSED_S3_ZONAL_CONFORMAL_V0_SCALAR_MATTER_CUBIC_VERTEX_LEDGER_RESULT.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "raw_c_plus_endpoint_liouville_green_tail_bound",
    script:
      "cpt_temporal_folded_susy/raw_c_plus_endpoint_liouville_green_tail_bound.py",
    output:
      "cpt_temporal_folded_susy/RAW_C_PLUS_ENDPOINT_LIOUVILLE_GREEN_TAIL_BOUND_RESULT.json",
    policy: "portable",
    compare: tight
  },
  {
    name: "homogeneous_closed_frw_starobinsky_time_symmetric_clock_boundary_local_ledger",
    script:
      "cpt_temporal_folded_susy/homogeneous_closed_frw_starobinsky_time_symmetric_clock_boundary_local_ledger.py",
    output:
      "cpt_temporal_folded_susy/HOMOGENEOUS_CLOSED_FRW_STAROBINSKY_TIME_SYMMETRIC_CLOCK_BOUNDARY_LOCAL_LEDGER_RESULT.json",
    policy: "portable",
    compare: tight
  }
] as const satisfies ReadonlyArray<ReproCase>

export const outputForScript = (name: string): string | undefined =>
  reproCases.find((entry) => entry.name === name)?.output
