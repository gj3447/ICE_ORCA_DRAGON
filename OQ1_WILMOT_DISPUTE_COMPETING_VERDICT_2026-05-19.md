# OQ1 — Aut(𝕊) Brown 1967 vs Wilmot 2025 :CompetingVerdict 양립

**User verdict 2026-05-19**: option (c) `:CompetingVerdict` 양립. machloket Eilu va-Eilu 원칙 따라 두 정전 모두 KG 보존, downstream 작업 측 conditional branch.

## 1. Two competing canons

### Verdict A — Brown 1967 G₂ × S₃

- **Primary source**: Brown 1967, *Pacific J. Math.*
- **Claim**: Aut(𝕊) = G₂ × S₃
- **Citation chain (58 years)**: Eakin-Sathaye → Moreno → Kirshtein → Cawagas → Gillard-Gresnigt → Furey-Hughes → Masi 2021
- **Physics interpretation**: doubling rotation preserves multiplication on 16D level via Spin(8) triality
- **Enables**: R4 (Aut(𝕊) commuting SU(2)×SU(2) embedding), PROM_16 §1 D1 consensus

### Verdict B — Wilmot 2025 G₂ only

- **Primary source**: Wilmot 2025, arXiv:2512.07210 + arXiv:2505.11747
- **Claim**: Aut(𝕊) = G₂ only (S₃ rejected)
- **Argument**: calibration-Θ argument — Brown's doubling rotation does NOT preserve canonical 3-form on 𝕊
- **Implies**: MB1 escape lane re-design without S₃ assumption (R4 redesign)

## 2. Possible resolution — different objects in dispute

| Verdict | Object | Method |
|---|---|---|
| Brown (G₂×S₃) | algebra Aut via Spin(8) triality (physics lit) | doubling rotation invariance |
| Wilmot (G₂ only) | algebra Aut via calibration-Θ (math lit) | canonical 3-form preservation |

Both may be correct on their respective domains. Status: `CANDIDATE_RESOLUTION`.

## 3. Downstream impact — conditional branches

### Under Brown assumption:
- R4 Aut(𝕊) commuting SU(2)×SU(2) embedding proceeds
- PROM_16 §1 D1 consensus stands
- queue_02 custodial pivot to Aut(𝕊) native SU(2)×SU(2) (yield 14-28/42 pairs predicted)
- ICE 6-family (#2 사도) ↔ G₂×S₃ structural cross-ref

### Under Wilmot assumption:
- MB1 escape lane re-design (S₃-dependent parts revise)
- R4 redesign (no S₃ factor for embedding)
- SS3TG (queue_09) measure G₂-only subset
- ICE 6-family structural cross-ref re-derived from G₂ alone

### Under :CompetingVerdict 양립 (current):
- Both downstream branches preserved in KG, executed conditionally per call-site
- Citations cite "Aut(𝕊) per Brown 1967 (G₂×S₃) [or per Wilmot 2025 (G₂ only) — see :CompetingVerdict]"
- New papers MUST disclose which canon assumed; cross-canon claims flag explicitly
- Resolution attempt left as `:OpenQuestion` (future work — Lean 4 formal disambiguation?)

## 4. KG nodes (Cypher written 2026-05-19)

- `aut-sedenion-brown-vs-wilmot-competing-verdict-2026-05-19` (:CompetingVerdict:CanonicalDispute)
- `brown-1967-aut-sedenion-G2xS3-2026-05-19` (:CanonicalVerdict:VerdictA)
- `wilmot-2025-aut-sedenion-G2-only-2026-05-19` (:CanonicalVerdict:VerdictB)
- `aut-sedenion-different-objects-interpretation-2026-05-19` (:DisputeInterpretation, CANDIDATE_RESOLUTION)

Edges: `CONTAINS_VERDICT × 2`, `HAS_POSSIBLE_RESOLUTION × 1`, `DISPUTES (bidirectional)`

## 5. Downstream R-tasks (PROM_16 §4)

| R-task | Brown branch | Wilmot branch |
|---|---|---|
| R4 (Aut(𝕊) SU(2)×SU(2)) | proceeds as-is | re-design without S₃ |
| R10 (정전 update) | minor (cite Wilmot caveat) | major (rewrite 정전 from G₂ base) |
| OQ4 (ICE 6-family ↔ SO(4) 6-gen) | cross-ref G₂×S₃ | cross-ref G₂ + add 6-source identification |
| OQ8 (Mathlib sedenion Aut theorem) | Lean formalize G₂×S₃ | Lean formalize G₂ + show S₃ disproof |

## 6. Future resolution path

1. **Direct comparison**: Wilmot calibration-Θ argument 측 audit by independent algebra expert
2. **Object-distinction proof**: formalize Brown's Spin(8)-triality object vs Wilmot's calibration-Θ object; show they ARE the same OR ARE distinct
3. **Lean 4 formalization** (OQ8): both verdicts as theorems; Mathlib disambiguates

## 한 줄

**OQ1 측 `:CompetingVerdict` 양립 채택 (2026-05-19) — Brown + Wilmot 모두 KG 정전 보존, downstream 측 conditional branch, machloket Eilu va-Eilu 원칙 따름.**

# KG: aut-sedenion-brown-vs-wilmot-competing-verdict-2026-05-19 (:CompetingVerdict 정전 2026-05-19)
