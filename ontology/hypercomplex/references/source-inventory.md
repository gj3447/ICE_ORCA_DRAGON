# Hypercomplex graph source and evidence inventory

This graph uses repository calculations and audits as evidence. Literature provenance remains in
[`docs/provenance/SOURCES.md`](../../../docs/provenance/SOURCES.md); this compact inventory records which
repository artifacts are authoritative for the graph's present distinctions.

| Role | Repository record | Boundary |
|---|---|---|
| Cayley–Dickson convention and finite kernels | `research/hypercomplex/cd_core.py` and adjacent scripts | Implemented convention, not a uniqueness theorem for all conventions |
| assessor/orbit count | `prove_higgs_results.json`, `avenue3_decisive_test_2026-06-05/avenue3_phase1_SUMMARY.py`, `RESULTS.md`, and `naesengmoon_indep_sedenion.py` | 42 assessor planes, 84 signed vectors for `a<b`, and 168 index-ordered representations are distinct objects; pair totals must state sign/order convention; none are Higgs particles |
| projected custodial test | `queue_02_custodial_results.json` | Frozen projected triples only |
| Queue-03 portability | `docs/audits/QUEUE03_PORTABILITY_AUDIT_2026-08-14.md` | Invalidates the legacy entrywise metric, not every possible invariant test |
| toy vacuum controls | `queue_04_hosotani_results.json`, `queue_05_cw_results.json`, `queue_06_coop_results.json` | Finite toy potentials; no Standard Model vacuum |
| projected g2 diagnostic | `queue_08_g2_diagnostic_results.json` | Original construction is a method artifact |
| automorphism-embedded g2 sidecar | `queue_08_g2_aut_octonion_results.json` | Rank/antisymmetry pass while full derivation/Casimir checks do not |
| explicit S3 subgroup | `queue_09_SS3TG_results.json`, `queue_09_SS3TG.py` | Subgroup computation survives; old Wilmot-refutation interpretation does not |
| S3 action on computed derivations | `aut_direct_product_test_2026-07-12/RESULT.json`, `aut_s3_direct_product_test.py` | Supports trivial action on the reconstructed 14-dimensional derivation space; not a complete classification of `Aut(S)` |
| Wilmot theta audit | `wilmot_theta_preservation_test_2026-07-12/RESULT.json`, `wilmot_theta_preservation_test.py`, `WILMOT_3FORM_CRITERION_TEST_2026-07-12.md` | Same-primary theta alignment/preservation in two implemented conventions; cross-primary realization remains open |
| Claim B finite-level protocol | `claimB_loop/prereg_claimB_loop_20260724.json` | Historical registered predicates, not a current mandatory research contract |
| Claim B finite-level results | `results_c1_zd_nullity_spectrum.json`, `results_c2_associator_distribution.json`, `results_c3_truncation_stability.json`, `CLAIMB_LOOP_FINAL_REPORT_2026-07-24.md` | Kills the registered finite statistical-stability route; does not construct or universally disprove an infinite measure, action, or gravity map |
| XOR invariant | `queue_11_xor_results.json` | Finite multiplication-label invariant |
| reproduction classification | `docs/audits/REPRODUCIBILITY_2026-06-08.md` | Reproduction status is not a physics verdict |
| workbench layer boundary | `docs/decisions/ICE_WORKBENCH_REFRAME_2026-05-18.md` | Separates algebraic archive from prediction belt |

No new external KG UID is invented. Collision-free historical Wilmot, automorphism-dispute, and
infinite-tower records are linked only as `RELATED`; the Claim B result itself and programme root remain
`UNRESOLVED` because the live connector has no matching record or write surface.

## PARTIAL corpus family index

[`ontology/research-family-index.v1.json`](../../research-family-index.v1.json) cryptographically
indexes the five PARTIAL roots owned by this graph. Its digest covers every ordinary file, while the
listed decisive units point only to existing evidence ledgers. Generated Python bytecode is counted
separately and no producer, duplicate run, or debug script becomes independent evidence merely by
appearing in the family inventory.

| Research family | Root | Ordinary / generated-cache files | Decisive units | Existing evidence target |
|---|---|---:|---:|---|
| finite hypercomplex core | `research/hypercomplex` | 53 / 32 | 4 | finite structure; projection/portability; toy/g2; S3 lifecycle ledgers |
| Avenue-3 finite test | `avenue3_decisive_test_2026-06-05` | 23 / 1 | 1 | `evidence:hyper-finite-structural-ledger` |
| Claim B sealed loop | `claimB_loop` | 20 / 1 | 2 | `evidence:hyper-claimb-sealed-finite-level-ledger` |
| direct S3 action | `aut_direct_product_test_2026-07-12` | 2 / 0 | 1 | `evidence:hyper-s3-direct-action-ledger` |
| Wilmot theta lifecycle | `wilmot_theta_preservation_test_2026-07-12` | 5 / 1 | 1 | `evidence:hyper-wilmot-theta-lifecycle` |

Run `./ice ontology families --json` to verify root ownership, decisive paths, evidence references,
counts, and normalized tree hashes. Coverage remains `PARTIAL`: this is a provenance-density
improvement, not exhaustive file-node mirroring or a physics promotion.
