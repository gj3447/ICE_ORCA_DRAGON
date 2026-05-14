# ICE_ORCA_DRAGON User Guide

> Category-by-category walk-through of all 47 Python scripts and 22 JSON result files.
> Quick overview: [`../README.md`](../README.md). Production / classification status: [`STATUS.md`](STATUS.md).

---

## Table of Contents

- [How this guide is organized](#how-this-guide-is-organized)
- [Category 1 — Cayley-Dickson breaking](#category-1--cayley-dickson-breaking)
- [Category 2 — Cayley-Dickson embedding & propagator](#category-2--cayley-dickson-embedding--propagator)
- [Category 3 — Dimensional analysis](#category-3--dimensional-analysis)
- [Category 4 — Higgs mechanism & S₁~S₇ proofs](#category-4--higgs-mechanism--ssss-proofs)
- [Category 5 — Sedenion (16D) analysis](#category-5--sedenion-16d-analysis)
- [Category 6 — Orbit / rep / queue series](#category-6--orbit--rep--queue-series)
- [Category 7 — Misc verification](#category-7--misc-verification)
- [Reading a JSON result](#reading-a-json-result)
- [Running science-feedback-loop on a result](#running-science-feedback-loop-on-a-result)
- [Common pitfalls](#common-pitfalls)

---

## How this guide is organized

Each category answers:

1. **What it computes** — the physics/math claim being tested
2. **Kernel script + variants** — main entry point and refinement chain (`v2 / part2 / final / verify`)
3. **JSON result** — output file and key fields
4. **Classification verdict** — confirmation / refutation / discovery / numerology (see [`STATUS.md`](STATUS.md))
5. **Reproduce** — exact command

Scripts are *standalone Python*. No package install required beyond `numpy` / `sympy` (and `jq` for inspecting JSON). All scripts write JSON results in-place next to themselves.

---

## Category 1 — Cayley-Dickson breaking

**What it computes**: At which Cayley-Dickson level does which identity (associativity / alternativity / power-associativity / etc.) break? CD₃ = octonion (non-associative, alternative). CD₄ = sedenion (zero divisors appear). The "breaking pattern" is the focus.

| Script | Role | Notes |
|--------|------|-------|
| `cd_breaking_search.py` | First pass scan | broad sweep over CD levels |
| `cd_breaking_search2.py` | Refined scan | narrows on observed breaking signatures |
| `cd_breaking_search3.py` | Targeted scan | targets 32D vs 64D specifically |
| `cd_breaking_final.py` | **Canonical** | final result, use this for citation |
| `cd_final_quick.py` | Quick-check variant | faster CI-style run |

**Reproduce**:
```bash
python cd_breaking_final.py
# Inspect output (in-script print + result JSON if written)
```

**Pitfall**: `search` / `search2` / `search3` show *exploration history*. Cite only `cd_breaking_final.py` in papers.

---

## Category 2 — Cayley-Dickson embedding & propagator

**What it computes**: How does a CD₃ (octonion) substructure embed into CD₄ (sedenion)? Does the embedding preserve the propagator chain? Path amplitude as a function of embedding choice.

| Script | Role | Notes |
|--------|------|-------|
| `cd_embedding.py` | Base embedding | initial CD₃→CD₄ map |
| `cd_embedding_v2.py` | Refined embedding | corrects v1 sign convention |
| `cd_embedding_verify.py` | Verification | checks embedding properties |
| `cd_embedding_final_check.py` | Final canonical | use for citation |
| `cd_chain_propagator.py` | Propagator chain | composes embeddings into chain |
| `cd_path_amplitude.py` | Path amplitude v1 | first amplitude computation |
| `cd_path_amplitude_v2.py` | Path amplitude v2 | corrected normalization |

**Reproduce**:
```bash
python cd_embedding_final_check.py
python cd_path_amplitude_v2.py
```

**Pitfall**: The v1 / v2 / final progression is *not* a regression; v1 documents an early sign convention error which v2 corrects. Always run `final_check` or `v2` for current results.

---

## Category 3 — Dimensional analysis

**What it computes**: Derive *dimensionless* physical ratios (Koide Q, mass ratios, ε scaling, Lstar length) from ICE-side algebraic invariants. The honest verdict is recorded in each JSON.

| Script | What it derives | JSON result | Verdict |
|--------|------------------|-------------|---------|
| `derive_Lstar_from_ICE.py` | L* length scale | `derive_Lstar_results.json` | derivation attempt |
| `derive_dimensionless_ICE.py` | dimensionless ratios (Koide Q etc.) | `derive_dimensionless_results.json` | multiple coincidences — **numerology candidate** |
| `derive_epsilon_ICE.py` | ε small parameter | `derive_epsilon_results.json` | scaling proposal |
| `derive_mass_ratios_ICE.py` | quark/lepton mass ratios | `derive_mass_ratios_results.json` | **self-refutation: "ICE cannot genuinely derive (0/15 genuine)"** |

**Reproduce**:
```bash
python derive_mass_ratios_ICE.py
jq '.verdict' derive_mass_ratios_results.json
# → "ICE cannot genuinely derive (0/15 genuine)"
```

**Pitfall**: `derive_mass_ratios_results.json` *contains a self-refutation*. Do not cite this as a confirmation. The honest verdict is a feature, not a bug — it demonstrates the workbench's refutation discipline.

---

## Category 4 — Higgs mechanism & S₁~S₇ proofs

**What it computes**: Standard Model Higgs doublet candidates extracted from sedenion ZD pairs; S₁~S₇ are progressive structural proofs (framing, CCWZ, higher gauge, BV-A∞, Ward-Takahashi evasion).

| Script | Role | JSON result |
|--------|------|-------------|
| `higgs_mechanism.py` | Higgs mechanism baseline | (in-script print) |
| `prove_higgs_ZD_doublet.py` | **42 ZD pairs as Higgs doublet candidates** | `prove_higgs_results.json` |
| `prove_s1_framing.py` | S₁ — symplectic framing | (in-script print) |
| `prove_s2_CCWZ.py` | S₂ — Callan-Coleman-Wess-Zumino coset | (in-script print) |
| `prove_s3_higher_gauge.py` | S₃ — higher gauge (Jacobi = 6·associator) | `prove_s3_results.json` |
| `prove_s5_bv_ainfty.py` | S₅ — Batalin-Vilkovisky / A∞ algebra | `prove_s5_results.json` |
| `prove_s7_WW_evasion.py` | S₇ — Ward-Takahashi / unitarity evasion | (uses `finding_ww_evasion.json`) |

**S₄ and S₆ note**: numbered gaps reflect the *intended progression order*, not missing computations. S₄ corresponds to ww_unitarity_bound_analysis content; S₆ corresponds to queue_05 (CW potential).

**Reproduce**:
```bash
python prove_higgs_ZD_doublet.py
jq '.zd_pairs_count' prove_higgs_results.json
# → 42

python prove_s3_higher_gauge.py
jq '.jacobi_equals_associator' prove_s3_results.json
```

**Pitfall**: 42 ZD pairs were originally numerology candidates. External grounding via Lygeros 2006 "42 Assessors" promoted them to **confirmation**. Be careful not to use this as precedent for *other* "42" coincidences without independent external evidence.

---

## Category 5 — Sedenion (16D) analysis

**What it computes**: The 16-dimensional sedenion algebra S has Der(S) = g₂ (the 14-dimensional Lie algebra). This category verifies that numerically, then probes SU(2) and SU(3) embeddings.

| Script | Role | Notes |
|--------|------|-------|
| `sedenion_analysis.py` | Baseline structure | initial pass |
| `sedenion_g2_investigation.py` | g₂ derivation investigation | iterative |
| `sedenion_g2_deep.py` | **Canonical Der(S)=g₂ verification** | dim=14 verified numerically |
| `sedenion_su2.py` | SU(2) embedding attempt | first pass |
| `sedenion_su2_part2.py` | SU(2) attempt 2 | refinement |
| `sedenion_su2_part3.py` | SU(2) attempt 3 | refinement |
| `sedenion_su2_final.py` | SU(2) final | use this for citation |
| `sedenion_su2_definitive.py` | SU(2) definitive | post-final clean run |
| `sedenion_su3_check.py` | SU(3) embedding check | extends to SU(3) |

**Reproduce**:
```bash
python sedenion_g2_deep.py
# Expected output: Der(S) dim = 14 (matches g₂)

python sedenion_su2_definitive.py
```

**Pitfall**: Der(S) = g₂ is **numerically verified** here but has no external peer review yet. STATUS marks this as `confirmation_local`, pending arXiv preprint. Do not cite as established result without that step.

---

## Category 6 — Orbit / rep / queue series

**What it computes**: `queue_NN_*` is a sequential investigation series — orbit structure, custodial symmetry preservation, representation decomposition, Hosotani gauge symmetry, Coleman-Weinberg potential, cooperative vacuum, G₂ adjoint, S₃ action, group-of-6 structure, XOR invariant.

| Script | What it computes | JSON result | Headline |
|--------|------------------|-------------|----------|
| `queue_01_orbit_analysis.py` | Orbit structure | `queue_01_orbit_results.json` | 7×6=42 orbit |
| `queue_02_custodial_check.py` | Custodial SU(2)×SU(2) preservation | `queue_02_custodial_results.json` | **0/42 pairs preserve (refutation)** |
| `queue_03_rep_decomposition.py` | Representation decomposition | `queue_03_rep_results.json` | 0.75 uniform |
| `queue_03_threshold_sensitivity_scan.py` | Threshold scan | (in-script) | threshold sensitivity |
| `queue_04_hosotani_toy.py` | Hosotani gauge-Higgs unification toy | `queue_04_hosotani_results.json` | toy model |
| `queue_05_coleman_weinberg.py` | CW effective potential | `queue_05_cw_results.json` | radiative SSB |
| `queue_06_cooperative_vacuum.py` | Cooperative vacuum | `queue_06_coop_results.json` | vacuum structure |
| `queue_08_G2_adjoint.py` | G₂ adjoint representation | `queue_08_g2_results.json` | 14-dim adjoint |
| `queue_09_S3_action.py` | S₃ (symmetric group) action | `queue_09_s3_results.json` | permutation orbits |
| `queue_10_group_of_6.py` | Group-of-6 structure | `queue_10_group6_results.json` | hexagonal structure |
| `queue_11_xor_invariant.py` | XOR invariant | `queue_11_xor_results.json` | ZD breaking via XOR |

**queue_07 note**: queue_07 is intentionally absent — the numbering preserves the *original investigation chronology*. Inserting filler would violate provenance.

**Reproduce (key)**:
```bash
python queue_01_orbit_analysis.py
jq '.orbit_size' queue_01_orbit_results.json
# → 42 (7 × 6)

python queue_02_custodial_check.py
jq '.fail_count_over_total' queue_02_custodial_results.json
# → "0/42 (max_commutator ~1.9)"
```

**Pitfall**: `queue_02_custodial_results.json` is a **refutation** of the naive embedding's custodial preservation. Threshold sweep (`queue_03_threshold_sensitivity_scan.py`) was recommended but not auto-blocking. STATUS marks this Lakatos-degenerating unless an alternative custodial-preserving embedding emerges.

---

## Category 7 — Misc verification

| Script | What it verifies | JSON result |
|--------|------------------|-------------|
| `zd64_analysis.py` | 64D ZD structure | (in-script) |
| `verify_mp_mW_3_256.py` | Hypothesis: mp / mW = 3 · 256 | `verify_mp_mW_results.json` |
| `ww_unitarity_bound_analysis.py` | WW unitarity bound | (uses `finding_ww_evasion.json`) |
| `orca_friedmann.py` | Friedmann equation derivation | (in-script) |

**verify_mp_mW special note**: A numerical hit of `mp / mW = 3 · 256 = 768` is a **numerology candidate**. The Fitting Detection step (was this pre-registered or post-hoc?) determines whether it gets `:Possibility` or `:NUMEROLOGY_HOLD`. Check [`STATUS.md`](STATUS.md) for current verdict.

**Reproduce**:
```bash
python verify_mp_mW_3_256.py
jq '.' verify_mp_mW_results.json
```

---

## Reading a JSON result

All JSON results follow a loose convention. Look for these fields (when present):

| Field | Meaning |
|-------|---------|
| `verdict` | Plain-language summary (e.g., `"ICE cannot genuinely derive (0/15 genuine)"`) |
| `confirmation_count` / `total` | numerator / denominator of confirmation rate |
| `classification` | one of `confirmation` / `refutation` / `discovery` / `numerology` |
| `lakatos_status` | `progressive` / `degenerating` (often added by the feedback-loop skill, not the script itself) |
| `bayesian_posterior` | `P(H|E)` if computed |
| `fitting_detection` | `pre-prediction` / `post-fitting` / `unknown` |
| `external_references` | external papers cited (e.g., Lygeros 2006) |

If a script does not write JSON, classification happens via the feedback-loop skill reading the script's stdout.

---

## Running science-feedback-loop on a result

After a fresh computation:

```bash
python <some_script>.py
# JSON appears next to script
```

Then in Claude Code:

```
"science-feedback-loop 실행 — <result_file>.json"
```

The skill (`/Users/lagyeongjun/CD/SYMPOSIUM/METAHUMOTONIC/ICE_ORCA_DRAGON/.claude/skills/science-feedback-loop.md`) executes:

1. Read JSON
2. Classify (4-way: confirmation / refutation / discovery / numerology)
3. **Fitting Detection** — was the claim pre-registered (in `:Contract` before computation) or post-hoc?
4. **Lakatos evaluation** — does it produce *new* predictions (progressive) or only re-explain (degenerating)?
5. **Bayesian update** — compute `P(H|E) = P(E|H)·P(H) / P(E)`. Critically estimate `P(E|~H)` ("could this happen even without the theory?") — high `P(E|~H)` triggers `NUMEROLOGY_HOLD`.
6. **KG write** — update `:Contract` confidence, create `:Span` (if discovery), tag `:NUMEROLOGY_HOLD` (if numerology).
7. **Consistency check** — verify SA→SP→ST chain still holds.

If classification is `discovery`, the loop **re-enters** by dispatching `/apt-sp <new_span_id>` for D(S) decomposition. This is why the workbench can self-extend.

---

## Common pitfalls

### Pitfall 1 — Citing exploration variants

Scripts with `search` / `v1` / `part1` / `investigation` suffixes are *exploration history*. Cite only `final` / `definitive` / `deep` variants. Exception: when documenting the iteration trajectory itself (e.g., in a paper's "methods" section).

### Pitfall 2 — Treating numerology as confirmation

A numerical match (Koide Q = 2/3, mp/mW = 3·256, "42") is **not** automatically a confirmation. Run Fitting Detection. If post-hoc, require external pre-registered prediction *before* promoting from `:NUMEROLOGY_HOLD` to `:Contract`.

### Pitfall 3 — Ignoring self-refutations

`derive_mass_ratios_results.json` explicitly states `"ICE cannot genuinely derive"`. This is *valuable data*. Do not patch it out, do not bury it. The honest verdict is what distinguishes this workbench from a numerology engine.

### Pitfall 4 — Running v1 instead of final

Always check for `_final.py` / `_definitive.py` / `_v2.py` versions before running the base script. The base often documents an early sign / normalization error that the final version corrects.

### Pitfall 5 — Skipping the feedback loop

Running a Python script and *not* running the feedback-loop skill leaves the KG stale. The Python script computes; the skill *interprets and records*. Both steps are required for the result to count as a SYMPOSIUM canonical contribution.

### Pitfall 6 — Forgetting queue_07 / S₄ / S₆ "gaps"

Numbering gaps preserve original chronology. Do not fill them with placeholder scripts.

---

## FAQ

**Q: Why are there 5 variants of `sedenion_su2`?**
A: Iterative refinement — each variant fixes a specific issue (sign convention, generator choice, basis ordering). Use `_definitive.py` or `_final.py`.

**Q: Can I add new scripts to this workbench?**
A: Yes, but follow the conventions: snake_case, suffix `_results.json` for outputs, run the feedback-loop skill after computation, update [`STATUS.md`](STATUS.md) and [`../CHANGELOG.md`](../CHANGELOG.md).

**Q: How do I know if a result is pre-prediction vs post-fitting?**
A: Check git log of the corresponding `:Contract` node creation timestamp vs the computation timestamp. If `:Contract` was created *before* computation → pre-prediction. Otherwise → post-fitting (high numerology risk).

**Q: What if my classification disagrees with a previous run?**
A: Re-classifications are first-class. The feedback-loop skill creates a new `:Verdict` node linked to the prior; both are retained (Eilu va-Eilu rule from narrative-feedback-loop's machloket discipline). Never silently overwrite.

**Q: Is this workbench reproducible from scratch?**
A: Yes. All scripts are standalone Python. No data files outside the directory. `numpy` / `sympy` only. See [`REPRODUCTION/`](../../../REPRODUCTION/) for KG dump if you also want canonical metadata.

---

# KG: ICE_ORCA_DRAGON_userguide, science-feedback-loop-canonical-ice
