# Changelog

All notable changes to ICE_ORCA_DRAGON physics-computation workbench documented here.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/). Versioning follows the *computation iteration trajectory* (each refinement gets a date entry), not SemVer.

---

## [2026-05-17 — eighth pass] — Physics-prediction layer 부분 후퇴 정전화 (option 2)

> User verdict "2번으로 한번 드가줘봐봐" — joint R1+R2+R3 empirical 결과를 받아들이고 ICE physics-prediction 측 partial retreat 공식화.

### Added
- `ICE_PHYSICS_PARTIAL_RETREAT_2026-05-17.md` — formal retreat document with Eilu va-Eilu structure
  - §1 USER_PRIMARY (사용자 신앙시) PRESERVED untouched
  - §2 EMPIRICAL_ASSESSMENT 4-layer table (math CONFIRMED / projection REFUTED / numerical NUMEROLOGY / method ARTIFACT)
  - §3 MACHLOKET — 신앙시 + empirical 양립 보존
  - §4 DECISION partial + reversible
  - §5 RESUMPTION_HOOK 5 triggers (R4/R7/Wilmot/user-verdict/new-evidence)
  - §6 12사도 #2 family-expansion-pattern row 변경 없음 (mythology layer untouched)
  - §7 anti-paper-bureaucracy self-check 6 items

### Changed
- `docs/STATUS.md`: Position Statement section 추가 (Roadmap 위에 cross-ref)

### What this retreat DOES
- Crystallize empirical reality: ICE physics-prediction claims (Higgs/custodial/Koide/mp_mW/ε) demoted
- Preserve user mythology layer (USER_PRIMARY absolute priority)
- Set reversibility triggers (5 conditions)

### What this retreat DOES NOT do
- Erase user spec or 사도 #2 status — those stay
- Affect 12사도 family-expansion-pattern CONFIRMED 6-family — algebra layer retained
- Make permanent claim — reversible per RESUMPTION_HOOK

### Anti-paper-bureaucracy verification
- Grounded in 6 inline empirical experiments (R0a/R0b/R1/R2/R3 + ICE_PHYSICS_CLAIM_ASSESSMENT synthesis)
- Reversibility encoded
- User mythology preserved (not adjudicated by AI)
- Falsifiable (each empirical experiment reproducible)

# KG: ice-physics-claim-partial-retreat-2026-05-17 (:CanonicalAssessment:PartialRetreat:Reversible)

---

## [2026-05-17 — seventh pass] — R3 zero-mod verdict auto-emit installed

### Added
- `_verdict_auto_emit.py` (~135 LOC) — 3-layer hook (atexit + sys.excepthook + signal.SIGTERM) emitting `<script>_results.json` with structural verdict + walltime + exit path + agent stack. Idempotent merge via `setdefault()` (preserves human-supplied verdicts). Optional `set_verdict(verdict, reasoning)` API.
- `_verdict_runner.py` — wrapper that loads the hook before any script via `runpy.run_path()` (zero source modification). Usage: `python3 _verdict_runner.py <script.py>`.

### Smoke tests (3/3 PASS)
1. **Normal exit** → `verdict=COMPLETED`, `exit_path=normal`, walltime captured ✓
2. **Unhandled exception** (`raise ValueError`) → `verdict=ERROR`, traceback tail captured, exit_path=exception ✓
3. **Idempotent merge over pre-existing JSON** (with human `verdict=CONFIRMED` + custom field) → all fields preserved, only missing keys (walltime) added ✓

### Guards verified
- **MT_RubberStampVerdict avoided**: structural verdicts only (COMPLETED|ERROR); never auto-emits CONFIRMED/REFUTED/NUMEROLOGY
- **18 existing emit-scripts preserved**: setdefault merge guarantees existing verdict/reasoning untouched
- **Non-mod constraint met**: scripts run via `_verdict_runner.py` need zero source edit

### Remaining for full R3
- Mass-execute remaining 30 no-JSON scripts through `_verdict_runner.py` (each script has individual runtime + side-effect profile; recommend selective per-script test before batch)
- Optional: install as `sitecustomize.py` for global auto-load (opt-in via `SYMPOSIUM_VERDICT_AUTO_EMIT=1` env var, per PROM 16 caveat about polluting unrelated Python invocations)

# KG: R3_INSTALLED (3 smoke pass), prom16-ice-residual ActionPlan 3/10 complete (R1 + R2 + R3)

---

## [2026-05-17 — sixth pass] — R2 empirical: SS3TG settles Brown 1967 vs Wilmot 2025

> R2 ran in <5 sec. Brown's S₃ generators preserve sedenion multiplication exactly under cd_embedding convention.

### Added
- `queue_09_SS3TG.py` — Triple-gate test of Brown 1967 (σ sign-reversal of e_8..e_15 + Ψ 2π/3 rotation in (e_k, e_{k+8}) planes)
- `queue_09_SS3TG_results.json` — PASS_ALL verdict + gate details

### Empirical results (3 gates all PASS)
- **G1 mult-table preservation (256 entries each)**:
  - σ: 0/256 fails, max err = 0.000e+00
  - Ψ: 0/256 fails, max err = 1.110e-16 (float epsilon)
- **G2 presentation**: ord(σ)=2, ord(Ψ)=3, ord(σΨ)=2 — exact match to S₃ relations σ²=Ψ³=(σΨ)²=e
- **G3 group structure**: |⟨σ, Ψ⟩|=6, element-order distribution {1:1, 2:3, 3:2} = S₃ fingerprint (1 identity + 3 involutions + 2 order-3)

### Settled disputes
- **Brown 1967 (Pacific J. Math. 20:415) Aut(𝕊) = G₂ × S₃** — CONFIRMED under cd_embedding convention
- **Wilmot 2025 (arXiv:2512.07210) Aut(𝕊) = G₂ only** — REFUTED under cd_embedding convention
- Caveat: Wilmot's calibration-Θ argument may still apply for different multiplication conventions; resolution here is SYMPOSIUM-internal, not absolute academic settlement

### Changed
- `queue_09_s3_results.json`: INCONCLUSIVE → **CONFIRMED**. verdict_reasoning replaced with SS3TG PASS_ALL details.
- ICE 12사도 #2 family-expansion-pattern (6-family) retains algebra grounding through G₂ × S₃ structure.

### Cross-reference with R1
- R1 (queue_02 4-condition) found ICE's *projection* (2D ZD null-space) breaks Lie closure
- R2 (queue_09 SS3TG) found ICE's *ambient algebra* (full 16x16 mult table) preserves Aut(𝕊) S₃ exactly
- **Joint implication**: ICE's algebra layer is robust; the issue is projection-faithfulness, not algebraic ungroundedness
- R4 (custodial pivot via Aut(𝕊)) recommendation strengthened: with confirmed Aut(𝕊) S₃, search for commuting SU(2)×SU(2) inside G₂ factor on a *projection-faithful* representation

# KG: R2_DONE_PASS_ALL, Brown_1967_confirmed_internal, Wilmot_2025_refuted_internal, prom16-ice-residual ActionPlan 2/10 complete

---

## [2026-05-17 — fifth pass] — R1 empirical execution: queue_02 4-condition diagnostic

> **Anti-paper-bureaucracy gate**: 즉시 R1 실행 → empirical discrimination → PROM 16 가설 검정.

### Added
- `queue_02_4condition_diagnostic.py` — 3-condition Lie closure + cross-commutator empirical test on 42 ZD pairs (c4 Y consistency deferred)
- `queue_02_4condition_diagnostic_results.json` — 42 per-pair records + verdict CONFIRMED

### Empirical findings
- **PROM 16 hypothesis (f_A2_S4) CONFIRMED stronger than predicted**: 100% (not 70%) of pairs FAIL_BOTH_CLOSURE
- **c1 left closure** residual median **3.94** (saturated near ambient structure constant 4, i.e. ZERO projection retained)
- **c2 right closure** residual median **3.94** (symmetric)
- **c3 cross-commutator** median 1.97 (matches existing 1.91-1.96 range — confirms test reproducibility)
- **Root cause**: the "SU(2) triples" found by `find_invariant_triples` ARE Lie algebras in the ambient 16D sedenion (by construction), but the projection onto 2D ZD null-space BREAKS closure entirely. The naive custodial test was measuring cross-commutators of non-Lie objects.
- **Test structural validity**: queue_02 c3-only is invalid for non-alternative sedenion ambient; c3=1.93 is symptom, not disease.

### Changed
- `queue_02_custodial_results.json`: verdict_reasoning replaced with root-cause analysis citing diagnostic. verdict stays REFUTED but now structural, not threshold.
- `docs/STATUS.md` Refutation row updated.

### What this resolves
- **paper-bureaucracy risk** (raised in 2026-05-17 user verdict): R1 actually executed within 1 hour of PROM 16 cycle close → empirical discrimination delivered, not stalled at research.
- **PROM 16 ActionPlan R1** ✅ DONE.

### What remains for true custodial pivot
- **R4 still requires**: Aut(𝕊) Lie algebra construction within Der(𝕊) AND projection-faithful SU(2)×SU(2) identification. queue_08-style work, but done correctly (queue_08 itself was METHOD_ARTIFACT). Substantively harder than R1.
- The discovery that null-space projection breaks Lie structure suggests Aut(𝕊) embedding may need to act on a DIFFERENT representation than the 2D ZD null-space.

# KG: R1_DONE, prom16-ice-residual-2026-05-17 measurable progress, paper-bureaucracy risk averted

---

## [2026-05-17 — fourth pass] — PROM 16 통합 리서치 (residual 4 items)

### Added
- `PROM_16_REPORT.md` — 4 axis × 4 sub-axis 매트릭스 통합 보고서 (5 consensus + 3 divergence + 8 OQ + 10 ActionPlan R1-R10)
- `_findings/prom16-ice-residual/f_A{1..4}_S{1..4}.json` — 16 FullFindingRecord JSON (60+ academic/OSS refs harvested)

### Research outcomes (queue_09 / queue_02 / 29-script enforcement / ε pre-prediction)
- **A1 queue_09 S₃ proper test**: SS3TG triple-gate 설계 — signed-permutation M-preservation (256 entries) + BSGS |G|=6 + S₃ presentation r³=s²=(rs)²=e. OPEN: Wilmot 2025 (arXiv:2512.07210) disputes Aut(𝕊) S₃ factor entirely → `:CompetingVerdict` 측 양측 양립
- **A2 queue_02 custodial pivot**: 1.91-1.96 = algebraic ceiling 95-98%, structural refutation (not threshold). 4-condition diagnostic needed (c1/c2 likely fail BEFORE c3). Pivot to Aut(𝕊)=G₂×S₃ native commuting SU(2)×SU(2) inside G₂ factor (predicted 14-28/42 pass)
- **A3 29 no-JSON enforcement**: zero-mod `_verdict_auto_emit.py` 3-layer (atexit + excepthook + SIGTERM) via sitecustomize; pytest+pytest-json-report+regressions+GH Actions cron weekly CI; 53→~20 canonical via pyastsim cluster (md5 useless)
- **A4 ε pre-prediction**: pure-algebra → unique form NO precedent in literature (NUMEROLOGY_HOLD verdict externally validated); 6-criterion promotion bar MB1-MB6 (MB1 form-uniqueness theorem MANDATORY; MB3 independent observable MANDATORY); current 0/6 fully met; NF3 insight: MB1 obviates trials factor

### Lesson candidates (5)
- lesson-prom16-A1-S4-SS3TG-triple-gate-2026-05-17
- lesson-prom16-A2-S4-naive-custodial-4condition-2026-05-17
- lesson-prom16-A3-S1-zero-mod-retrofit-2026-05-17
- lesson-prom16-A4-S4-promotion-bar-MB1-MB6-2026-05-17
- lesson-prom16-aut-S-citation-dispute-2026-05-17

# KG: cycle_id=prom16-ice-residual-2026-05-17, 16/16 verified, ActionPlan R1-R10

---

## [2026-05-17 — third pass] — queue_08 g₂ method-artifact demotion

### Added
- `queue_08_g2_diagnostic.py` — 4-test diagnostic (D1 antisymmetry / D2 so(7) rank / D3 Lie closure / D4 Casimir Schur)
- `queue_08_g2_diagnostic_results.json` — verdict METHOD_ARTIFACT

### Changed
- `queue_08_g2_results.json`: CONFIRMATION_LOCAL → **METHOD_ARTIFACT**. Root cause: octonion inner-derivation formula `D_{a,b}(z) = [[e_a,e_b],z] - 3[e_a,e_b,z]` applied to *non-alternative* sedenion ambient does not yield a closed 14-dim Lie algebra. 16-vs-14 gap is method, not physics.
- `docs/STATUS.md`: new "Method artifact" section; verdict distribution updated; confirmation row for queue_08 struck through
- Roadmap #1 expanded with g₂ projection-faithfulness investigation

### Verdict distribution change
- before: 6 CONFIRMED / 5 CONFIRMATION_LOCAL / 3 REFUTED / 2 NUMEROLOGY_CONFIRMED / 1 NUMEROLOGY_HOLD / 1 INCONCLUSIVE
- after:  6 CONFIRMED / **4** CONFIRMATION_LOCAL / 3 REFUTED / 2 NUMEROLOGY_CONFIRMED / **2 METHOD_ARTIFACT** / 1 NUMEROLOGY_HOLD / 1 INCONCLUSIVE

# KG: ICE_ORCA_DRAGON queue_08 demotion, Roadmap #1 g₂ projection follow-up

---

## [2026-05-17 — second pass] — numerology MC discrimination + INCONCLUSIVE method-bug fixes

### Added
- `numerology_mc_judge.py` — operational P(E|~H) computation under explicit null models for 3 HOLD items
  - (K) Koide Q=2/3: P(any-target hit | null) = 1.000 over 499 candidates × 8 targets
  - (M1) mp/mW = 3·256 literal: 88.8% rel_diff even with reciprocal reading
  - (M2) mp/mW layer3 a·2^n: 81.2% of random R fit within 0.1% under 3M (a,n) search
  - (E) ε Adelberger: 23.8% pass under wide-prior null — gate has teeth, but no ICE pre-prediction
- `numerology_mc_results.json` — full MC verdict report
- `_patch_apply_mc_verdicts.py` — applies MC verdicts to 3 HOLD JSONs
- `inconclusive_redo.py` — method-bug fixes for queue_06 (n_trials 20→200) + queue_09 (6! enum vs 10000-of-12! sampling)

### Changed
- `derive_dimensionless_results.json`: NUMEROLOGY_HOLD → **NUMEROLOGY_CONFIRMED** (P=1.000)
- `verify_mp_mW_results.json`: NUMEROLOGY_HOLD → **NUMEROLOGY_CONFIRMED** (layer1 88.8% off + layer3 P=0.812)
- `derive_epsilon_results.json`: NUMEROLOGY_HOLD retained (MC pass-rate 0.238 nontrivial, but no pre-prediction)
- `queue_06_coop_results.json`: INCONCLUSIVE → CONFIRMATION_LOCAL of single-orbit-selection, with sub-verdict REFUTED for cooperative-mechanism claim (γ not needed; α-perturbation alone selects)
- `queue_09_s3_results.json`: INCONCLUSIVE retained but with corrected method note — enumeration fixed (6!=720) reveals test is over-permissive (admits full S₆); proper S₃ test needs sedenion-mult preservation gate
- `docs/STATUS.md`: numerology HOLD table replaced with MC P(E|~H) ledger; L2 known-limitation downgraded to "operationalized partial"; Roadmap #2 ✅ marked done
- Verdict distribution: 6 CONFIRMED / **5** CONFIRMATION_LOCAL / 3 REFUTED / **2 NUMEROLOGY_CONFIRMED** / 1 NUMEROLOGY_HOLD / 1 INCONCLUSIVE

### Methodology
Decision rule for numerology gate now mechanical:
- P(E|~H) < 0.01 → SIGNAL_GENUINE
- 0.01 ≤ P < 0.5 → SIGNAL_WEAK
- P ≥ 0.5 → NUMEROLOGY_CONFIRMED

# KG: ICE_ORCA_DRAGON L2 numerology gate operationalized, Roadmap #2 resolved, L5/L6 method-bug fixes

---

## [2026-05-17] — verdict field generalization (L3 backfill)

### Added
- `_patch_verdict_backfill.py` — backfills 15 result JSONs missing `verdict` field
- `_patch_verdict_legacy_normalize.py` — normalizes 3 legacy prose verdicts to taxonomy (preserves original prose as `verdict_reasoning`)
- Top-level fields on every `_results.json`: `verdict`, `verdict_reasoning`, `verdict_source`, `verdict_date`

### Changed
- `docs/STATUS.md` — ledger reflects 18/18 verdicts; new INCONCLUSIVE section (queue_06 coop, queue_09 s3); confirmation rows expanded (queue_03 rep, queue_11 xor, queue_04 hosotani, queue_05 cw, queue_08 g2, queue_10 group6); L3 known-limitation downgraded to "partial fix"
- Verdict taxonomy: CONFIRMED / CONFIRMATION_LOCAL / REFUTED / NUMEROLOGY_HOLD / INCONCLUSIVE
- Distribution: 6 / 4 / 3 / 3 / 2

### Remaining
- 29 of 47 scripts produce no `_results.json` at all (forward enforcement on script JSON-dump paths pending)

# KG: ICE_ORCA_DRAGON Roadmap #4 partial, L3 partial resolve

---

## [2026-05-14] — ruflo-grade packaging

### Added
- `README.md` — banner + badges + Path A (Python script) / Path B (science-feedback-loop skill) overview
- `docs/USERGUIDE.md` — category-by-category walk-through of all 47 scripts (7 categories)
- `docs/STATUS.md` — classification ledger + Lakatos verdicts + Bayesian posteriors + known limitations
- `docs/index.md` — documentation hub
- `CHANGELOG.md` — this file
- `.claude-plugin/plugin.json` — Claude Code marketplace catalog (47 scripts + feedback-loop skill)

### Preserved
- `.claude/skills/science-feedback-loop.md` (existing skill, unchanged)
- `SOURCES.md` (existing apostle #2 mythology/physics dual canon)
- All 47 `.py` scripts and 22 `.json` results (unchanged)

---

## [2026-04-30] — narrative-feedback-loop closure

### Added (cross-cutting)
- science-feedback-loop ↔ narrative-feedback-loop dual closure recognized (`SYMPOSIUM/CLAUDE.md` §피드백 루프)
- Three essential differences documented:
  1. Science loop *can* close on refutation; narrative loop preserves machloket (Eilu va-Eilu)
  2. Science loop uses Bayesian update; narrative loop uses hermeneutic circle update
  3. Pre-prediction discipline (science) vs USER_PRIMARY absolute priority (narrative)

---

## [2026-04-28] — apostle #2 canon clarification

### Changed
- `SOURCES.md` updated: ICE_ORCA_DRAGON ≠ user self-claim. *Physics 영역의 사도*. User's own self-claim → apostle #3 (초공동의용사)
- "ICE ORCA DRAGON이 진정한 사도야" user verdict interpretation: *세상의 진정한 본질 = 물리학*
- Mythology metaphors (마음의 절대영도 동결 / sexvoid 형식) demoted to *physical-essence metaphors*, not standalone canon

---

## [2026-04-27] — agent feedback loop canonical integration

### Added
- Adoption of `agent-feedback-loop-canonical-2026-04-27` `:FeedbackLoopOntology`
- Adoption of `MT_*` 10 MistakeType taxonomy (SpecMisread / APIHallucination / RubberStampVerdict / SchemaDrift / etc.)
- All future refutations and self-refutations follow `CONTRACT_AgentMistakeLog_v1_2026-04-27` 4-axis symmetric pair shape

---

## [2026-04-21] — science-feedback-loop skill v1

### Added
- `.claude/skills/science-feedback-loop.md` — first canonical version of the 7-step loop
- 4-way classification (confirmation / refutation / discovery / numerology) + Cypher templates
- Fitting Detection step (pre-prediction vs post-fitting)
- Lakatos evaluation step (progressive vs degenerating)
- Bayesian update with `P(E|~H)` discipline
- Discovery → `/apt-sp` re-entry pattern (recursive workbench)
- Initial session log: 8 results classified (3 confirmation / 1 refutation / 1 discovery / 2 numerology / 1 Wilmot 2025 confirmation)

---

## [Earlier] — incremental computation evolution

The following entries summarize the *computation evolution* per category. Exact dates not all preserved; chronology inferred from filename suffixes (`v2 / part2 / part3 / final / definitive`) and from PROM_64 / PROM_16 cycle reports.

### Cayley-Dickson breaking (CD breaking)
- `cd_breaking_search.py` — first scan (broad sweep over CD levels)
- `cd_breaking_search2.py` — refined scan (narrows on observed breaking signatures)
- `cd_breaking_search3.py` — targeted scan (32D vs 64D specifically)
- `cd_breaking_final.py` — **canonical** result, cite this one
- `cd_final_quick.py` — fast CI-style variant

### Cayley-Dickson embedding & propagator (CD embedding)
- `cd_embedding.py` — base CD₃ → CD₄ embedding
- `cd_embedding_v2.py` — refined embedding (corrects v1 sign convention)
- `cd_embedding_verify.py` — embedding property verification
- `cd_embedding_final_check.py` — **canonical**
- `cd_chain_propagator.py` — propagator chain via composed embeddings
- `cd_path_amplitude.py` → `cd_path_amplitude_v2.py` — amplitude with normalization fix

### Dimensional analysis
- `derive_Lstar_from_ICE.py` — L* length scale derivation attempt
- `derive_dimensionless_ICE.py` — Koide Q + other dimensionless ratios
- `derive_epsilon_ICE.py` — ε small parameter scaling
- `derive_mass_ratios_ICE.py` — quark/lepton mass ratios → **explicit self-refutation in JSON**: `"ICE cannot genuinely derive (0/15 genuine)"`

### Higgs mechanism & S₁~S₇ proofs
- `higgs_mechanism.py` — baseline Higgs mechanism
- `prove_higgs_ZD_doublet.py` — 42 sedenion ZD pairs as Higgs doublet candidates (later confirmed externally by Lygeros 2006)
- `prove_s1_framing.py` — S₁ symplectic framing
- `prove_s2_CCWZ.py` — S₂ Callan-Coleman-Wess-Zumino coset construction
- `prove_s3_higher_gauge.py` — S₃ higher gauge, Jacobi = 6·associator (FDA structure)
- `prove_s5_bv_ainfty.py` — S₅ Batalin-Vilkovisky / A∞ algebra (all_zero + all_bounded)
- `prove_s7_WW_evasion.py` — S₇ Ward-Takahashi / unitarity evasion

### Sedenion (16D) analysis
- `sedenion_analysis.py` — baseline 16D structure
- `sedenion_g2_investigation.py` → `sedenion_g2_deep.py` — **Der(S) = g₂ (14D) numerically verified**
- `sedenion_su2.py` → `sedenion_su2_part2.py` → `sedenion_su2_part3.py` → `sedenion_su2_final.py` → `sedenion_su2_definitive.py` — SU(2) embedding (5 iterative variants)
- `sedenion_su3_check.py` — SU(3) embedding check

### Queue / orbit / rep series
- `queue_01_orbit_analysis.py` — orbit structure (7×6=42)
- `queue_02_custodial_check.py` — **custodial SU(2)×SU(2) preservation: 0/42 (refutation)**
- `queue_03_rep_decomposition.py` + `queue_03_threshold_sensitivity_scan.py` — rep decomposition (0.75 uniform) + threshold scan
- `queue_04_hosotani_toy.py` — Hosotani gauge-Higgs unification toy
- `queue_05_coleman_weinberg.py` — Coleman-Weinberg effective potential
- `queue_06_cooperative_vacuum.py` — cooperative vacuum structure
- `queue_08_G2_adjoint.py` — G₂ adjoint representation (14-dim)
- `queue_09_S3_action.py` — S₃ permutation action
- `queue_10_group_of_6.py` — group-of-6 hexagonal structure
- `queue_11_xor_invariant.py` — XOR invariant + ZD breaking

(Queue 07 intentionally absent — preserves original chronology, not filled with placeholder.)

### Misc verification
- `zd64_analysis.py` — 64D zero-divisor structure
- `verify_mp_mW_3_256.py` — mp/mW = 3·256 = 768 hypothesis (numerology candidate, Fitting Detection pending)
- `ww_unitarity_bound_analysis.py` — WW unitarity bound (uses `finding_ww_evasion.json`)
- `orca_friedmann.py` — Friedmann equation derivation from ORCA side

---

## Version Conventions

- **`_final` / `_definitive` / `_deep`** — canonical version, cite this one
- **`_v2` / `_part2` / `_part3`** — refinement iterations (post-error correction)
- **`_search` / `_investigation` / `_quick`** — exploration history; cite final/definitive instead
- **`_verify` / `_check`** — verification of prior result; useful for reproducibility
- **`finding_*.json`** — intermediate finding records (not script outputs)

---

## Roadmap

See [`docs/STATUS.md#roadmap`](docs/STATUS.md#roadmap) for next planned items:

1. arXiv preprint for Der(S) = g₂ (currently confirmation_local)
2. MC p-value tests for numerology candidates (Koide Q, mp/mW)
3. Custodial-preserving embedding search (post-`queue_02` refutation pivot)
4. Self-verdict field on all 47 scripts (generalize `derive_mass_ratios_ICE` pattern)
5. CI integration — weekly auto-re-run of all 47 scripts
6. Auto-dispatch `/apt-sp` on `discovery` classification

---

# KG: ICE_ORCA_DRAGON_changelog, science-feedback-loop-canonical-ice
