# Case Study #2 — Furey C⊗O Bioctonion Programme (scaffold for PROM 16 dispatch)

> **Purpose**: generalize the *pre-registered Lakatos rigorous test* protocol beyond ICE (case study #1). Furey's bioctonion programme is the natural case study #2: same SM-derivation aspiration, different algebra (C⊗O 16-real-dim), different mechanism (SU(3)⊂G₂ route instead of 3 octonion subalgebras + S₃).
> **Why this case study**: validates the protocol generalizes, AND tests whether Furey's programme reaches SIGNAL_GENUINE where ICE did not. If Furey passes → methodology is sharp (distinguishes Progressive from Stagnant). If Furey also fails → methodology has identified a *class-wide* problem in hypercomplex-SM-derivation.
> **Next action**: `/prom 16 "Furey C⊗O bioctonion programme — apply asymmetric Lakatos cycle-novel + pre-registered rigorous test (case study #2 generalization beyond ICE)"`
> **Estimated dispatch cost**: 16 haiku subagents in parallel (~5-10 min wall + ~30-80kB findings)

---

## 1. Programme identity (hard core)

**Programme**: Furey C⊗O bioctonion programme — Standard Model derivation from complex-octonion algebra.

**Hard core** (HC):
- C⊗O ≅ ℂ ⊗ 𝕆 — complex octonion algebra (real dim 16)
- Aut(C⊗O) = G₂ × ℤ₂ (G₂ = Aut(O), ℤ₂ = complex conjugation)
- Left actions space End_ℂ(C⊗O) ≅ M(2,ℂ) ⊕ ... ≅ Cl(6,ℂ)
- Single octonion subalgebra (NOT 3 — distinguishing from ICE sedenion)
- 3-generation count emerges from SU(3) ⊂ G₂ acting on 64-dim left-action space split (16 + 48 = 16 + 3×16)

**Protective belt** (PB), with sub-belt decomposition:
- **PB_algebra**: G₂ representation theory on Cl(6), Connes-Lott-style triple decomposition, complex octonion ZD characterization
- **PB_physics**: SU(3)_color × U(1)_em embedding, single fermion generation derivation per Cl(6) minimal left ideal, 3-generation count from dimension splitting

**Key citations (canonical Furey lineage)**:
- Furey, C. (2014). "Generations: three prints, in colour." *JHEP* 10: 046. arXiv:1405.4601.
- Furey, C. (2018). "Three generations, two unbroken gauge symmetries, and one eight-dimensional algebra." *Physics Letters B* 785: 84-89.
- Furey, C., & Hughes, M. J. (2022). "One generation of fermions from the complexified Dixon algebra." *Phys. Lett. B* 827: 136959.
- Furey, C., & Maddugoda, P. (2025). [Recent — to verify exact title]. *Phys. Lett. B* / arXiv 2025.
- Dixon, G. M. (1994). *Division Algebras: Octonions, Quaternions, Complex Numbers and the Algebraic Design of Physics*. Kluwer.

---

## 2. Algebraic primitive enumeration (proposed 28-primitive set for protocol)

Following the protocol structure of `prereg_lakatos_methodology_paper §2.1`, the primitives derivable purely from Furey HC:

| # | Primitive | Value | Source |
|---|---|---|---|
| F1 | dim ℝ(C⊗O) | 16 | construction |
| F2 | dim ℂ(C⊗O) | 8 | construction |
| F3 | dim End_ℂ(C⊗O) | 64 | left-action space |
| F4 | dim G₂ adjoint | 14 | Aut(O) |
| F5 | dim G₂ fundamental | 7 | rep theory |
| F6 | rank G₂ | 2 | Lie algebra |
| F7 | Weyl(G₂) | 12 | root system |
| F8 | dim SU(3) | 8 | subgroup |
| F9 | SU(3) fundamental | 3 | rep |
| F10 | SU(3) octet | 8 | adjoint rep |
| F11 | dim U(1)_em | 1 | em gauge |
| F12 | dim Cl(6) | 64 | Clifford |
| F13 | Cl(6) minimal left ideal dim | 8 | Pauli-Furey idempotent |
| F14 | 64 = 16 + 3×16 split | 1 + 3 | G₂ → SU(3) reduction |
| F15 | quaternionic complex structure | exists | Dixon |
| F16 | bioctonion ZD chiral pairs | TBD | research needed |
| F17 | complex conjugation Z₂ | 1 | Aut(C⊗O) |
| F18 | Furey idempotent count | 2 | primitive idempotents |
| F19 | electric charge eigenvalues | {-1, 0, +1, +1/3, +2/3, -1/3} | Furey 2014 derivation |
| F20 | leptoquark mass split factor | TBD | Furey 2018 |
| F21 | weak isospin from C₂ | 1/2 | Pauli |
| F22 | hypercharge from U(1) gen | varies | Furey 2014 |
| F23 | Yukawa coupling primitive | TBD | research needed |
| F24 | CP-violation phase primitive | TBD | research needed |
| F25 | Furey 3-generation count | 3 | dim 48/16 = 3 |
| F26 | Cabibbo angle primitive | TBD | research needed |
| F27 | Weinberg angle primitive | TBD | research needed |
| F28 | proton-to-W mass ratio | TBD | research needed |

Note: F16, F20, F23-F28 = TBD pending Furey literature deep-dive in PROM 16 dispatch agents.

---

## 3. Frozen observable set (same 20 PDG observables as ICE for fair cross-programme comparison)

Same set as `ice_prereg_predictions_2026-05-18.json` for direct comparison:
- 3 generations / Higgs isospin doublet / EW rank / m_W/m_Z / m_H/m_Z / m_H/m_W / m_top/m_Z / α_em⁻¹(MZ) / α_s(MZ) / sin²θ_W / Cabibbo angle / Cabibbo² / Koide Q / SU(3) fundamental / SU(3) octet / spin 1/2 / spin 1 / spin 2 / lepton-quark charge ratio / proton-to-W mass.

---

## 4. Pre-registered prediction list (proposed canonical 15, to be sha256-committed BEFORE dispatch)

Following same protocol as ICE 15-prediction canonical set:

| # | Prediction (P_corr threshold dependent) | Candidate primitive ratio |
|---|---|---|
| FP01 | 3 generations | F25 = 48/16 = 3 |
| FP02 | Higgs isospin 1/2 | F21 |
| FP03 | EW rank 2 | F6 = G₂ rank |
| FP04 | SU(3) color count 8 | F8 = dim SU(3) |
| FP05 | Charge eigenvalue ±1 | F19 lepton charges |
| FP06 | Charge eigenvalue ±1/3 / ±2/3 | F19 quark charges |
| FP07 | spin-1/2 fundamental | F13 / 16 ratio |
| FP08 | spin-1 gauge | F4 / 14 ratio |
| FP09 | Cabibbo angle | F26 (research) |
| FP10 | sin²θ_W | F27 (research) |
| FP11 | m_W/m_Z | TBD candidate |
| FP12 | Yukawa hierarchy | F23 (research) |
| FP13 | CP phase | F24 (research) |
| FP14 | mass ratios | F20 (research) |
| FP15 | proton-to-W | F28 (research) |

---

## 5. PROM 16 dispatch — 4×4 axis matrix

Following 16-agent PROM dispatch convention:

| Axis | Sub-axis | Agent question |
|---|---|---|
| A1 (algebra) | S1 | Verify Aut(C⊗O) = G₂ × ℤ₂ vs disputes |
| A1 | S2 | Furey idempotent uniqueness analysis |
| A1 | S3 | Cl(6) embedding canonicality |
| A1 | S4 | Bioctonion ZD characterization (deep) |
| A2 (3-generation) | S1 | Dimension count 48/16=3 emergence vs SU(3) action |
| A2 | S2 | Compare with Gillard-Gresnigt CxS 3-generation route |
| A2 | S3 | Independence of 3-gen from SU(3) embedding choice |
| A2 | S4 | Furey-Hughes 2022 one-generation derivation status |
| A3 (Lakatos verdict) | S1 | Identify Furey's protective belt additions 2014-2025 |
| A3 | S2 | Novel confirmed predictions in Furey programme |
| A3 | S3 | Stagnant vs Degenerating sub-classification |
| A3 | S4 | Bayesian posterior P(Furey physics validated) prior |
| A4 (rigorous test) | S1 | sha256-commit candidate 15 predictions list |
| A4 | S2 | Run MC null gate per prediction |
| A4 | S3 | Bonferroni correction across n_trials = 300 |
| A4 | S4 | Verdict synthesis + comparison with ICE asymmetric verdict |

---

## 6. Predicted outcomes (Bayesian prior before dispatch)

- **Algebra fiber**: PROGRESSIVE expected (Furey has 50+ year lineage, peer-reviewed PLB/JHEP, distinct from ICE)
- **Physics-prediction fiber**: 
  - If 0/15 SIGNAL_GENUINE → confirms *class-wide* algebra-based physics SIGNAL_GENUINE deficiency (strong methodology paper §4 generalization claim)
  - If 1/15+ SIGNAL_GENUINE → Furey ≠ ICE on this axis, asymmetric verdict NOT uniform across hypercomplex programmes (interesting refinement)
- **Most likely**: 0/15 or 1/15 SIGNAL_GENUINE (algebra primitives are similar small integers; same look-elsewhere hazard applies)
- **Bayesian prior**: P(Furey physics validated by protocol) = 0.10 (slightly higher than ICE prior 0.20 → 0.015 because Furey is older + peer-reviewed, lower than original ICE prior because same algebra-class hazards apply)

---

## 7. KG hooks (pre-allocated nodes)

When dispatch completes, ingest into:
- `prom16-furey-CxO-case-study-2-2026-05-19` (`:CaseStudyDispatch:VerdictPending`)
- `furey-CxO-algebra-primitives-canonical-2026-05-19` (`:AlgebraicPrimitiveSet` — 28 primitives F1-F28)
- `furey-CxO-prereg-predictions-2026-05-19` (`:PreRegisteredPrediction` — sha256-committed)
- `furey-CxO-MC-null-results-2026-05-19` (`:NumerologyMCScanResult` after dispatch)
- `cross-programme-comparison-ICE-vs-Furey-2026-05-19` (`:CrossProgrammeAudit`)

---

## 8. Status: SCAFFOLD_READY, dispatch pending one-line user authorize

This scaffold sets up the test bed. The actual `/prom 16` dispatch is a fresh-context heavy operation (~5-10 min wall, ~30-80kB findings, ~10-50 tool calls). To preserve current session context, dispatch is deferred to next session.

**To proceed**: in fresh session, invoke:
```
/prom 16 "Furey C⊗O bioctonion programme — apply asymmetric Lakatos cycle-novel + pre-registered rigorous test (case study #2 generalization beyond ICE). Reference scaffold: METAHUMOTONIC/ICE_ORCA_DRAGON/FUREY_CxO_PROGRAMME_SCAFFOLD_2026-05-19.md"
```

The dispatch will use this scaffold's 4×4 axis matrix (§5) and 28 primitives (§2) to generate 16 substantive findings, sha256-commit the prediction list, and synthesize a verdict report `PROM_16_FUREY_CxO_REPORT_2026-05-19.md`.

---

## 9. Why this is the right next move

After case studies #1 (ICE) + #2 (Furey C⊗O) both run under the same protocol:
- If both = 0 SIGNAL_GENUINE → **class-wide methodology paper conclusion** is empirically backed by 2 independent programmes
- Combined ICE + Furey result becomes the **strongest empirical witness** for the prereg paper's §4 generalization claim
- Suggested referee Niels Gresnigt can verify both case study primitives (he is published in both lineages)
- Cycle continues with case studies #3 (Trayling-Baylis Cl(7)), #4 (Lisi E₈), #5 (Connes-Marcolli NCG) — building toward "5 case study series" which is what the methodology paper needs to claim *generalized validity*

---

# KG: furey-CxO-programme-scaffold-2026-05-19, case-study-2-dispatch-pending,
#     methodology-paper-generalization-empirical-backing-roadmap-2026-05-19
