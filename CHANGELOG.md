# Changelog

All notable changes to ICE_ORCA_DRAGON physics-computation workbench documented here.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/). Versioning follows the *computation iteration trajectory* (each refinement gets a date entry), not SemVer.

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
