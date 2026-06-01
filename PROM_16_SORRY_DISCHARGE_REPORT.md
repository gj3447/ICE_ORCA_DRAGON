# PROM 16 — ICE 잔여 두 sorry 공략 경로

> cycle: `prom16-ice-sorry-discharge-2026-06-01` · Lesson `lesson-ice-sorry-discharge-path-2026-06-01`
> 4 axis(수학정전/Mathlib인프라/증명전략/실현가능성) × 4 sub(Aut(𝕊)/MB1/공통기반/함정) = 16 RF.
> 대상: (1) `Aut(𝕊)=G₂×S₃` (L1 대수, axiom) (2) `form_uniqueness_conjecture` (MB1, sorry).

## 0. 사전 — 두 sorry의 위상
- Aut(𝕊): L1 대수 core, 물리와 독립한 순수수학 사실.
- MB1: 물리 escape-lane의 본체. 단 escape-lane 딜레마(증명/반증 양분기 → 0)가 이미 형식화됨.

---

## 1. Consensus

### C1. Aut(𝕊)=G₂×S₃ 종이 증명은 **실재** (이전 비관론 정정)
**Eakin & Sathaye 1990, J.Algebra 129(2):263-278 (DOI 10.1016/0021-8693(90)90221-9)** — 검증됨. CD 대수 자기동형군 체계적 정리, Aut(𝕊)≅G₂×S₃ (G₂=Aut(𝕆), S₃=Spin(8) triality가 3 octonion subalgebra 치환, n≥4 stabilize). 보강: arXiv:2512.07210 (2024, Fano-15 calibration로 prior 문헌 discrepancy 해소). → **미증명인 것은 Lean 형식화이지 수학이 아님.** (D1의 "open research"는 outlier 오류.)

### C2. Mathlib 인프라 = 큰 공백
- octonion **없음** (Quaternion만), CD construction 없음 (Nuccio WIP fork). [B1]
- G₂ **group type 없음** (root system+Cartan matrix만). S₃=Equiv.Perm(Fin3) 있음. → **RHS `G₂×S₃`를 statement조차 못 씀.** [B2]
- nonassoc automorphism turnkey typeclass 없음 → custom NonAssocAlgEquiv. [B4]

### C3. 진짜 blocker = "G₂로 명명"이 structurally unreachable
Lean에서 자기동형군이 14차원·rank2·G₂-type root system임은 증명 가능하나, **추상적으로 "≅ G₂"라 부르려면 G₂를 먼저 구성해야 함(순환)**. naming 문제이지 proof 문제 아님. [C4]

### C4. MB1은 **empirically MOOT** — cheapest-settle (Mathlib 불필요)
7 FormCandidate = 3 refuted(Oscillatory/Friedmann/PPN) + 4 unfalsifiable(YukawaTower/Alpha336/RangeSub/GnNorm) = 7 전수 cover. privileged form 0 → uniqueness 증명해도 escape-lane 0, 안 해도 0. **5분 enumeration으로 확정, lake build 불필요.** [C2,D2]

### C5. 대안: Magma/GAP 계산검증 >> full Lean
Coq/mathcomp·Isabelle/AFP에 octonion/G₂ 없음. Magma/GAP은 composition algebra+automorphism 계산 지원 (1-2h, HIGH credibility). full Lean(2+주, research급) 대비 압도적 ROI. [D3]

### C6. 전략 = paper-first hybrid
decide/native_decide = 16×16 곱셈표·automorphism check·cardinality(finite). 수동 = group axiom·Lie 식별. LTE 교훈. [C3]

### C7. 우선순위 (물리 refuted 전제)
둘 다 TOE rescue 아님. Aut(𝕊)=pure-math enrichment(bounded 4-6wk PARK default). MB1=dilemma→cheapest-settle. effort 16-24wk per 0.004P → "just don't"이 최저비용 최고정합. sunk-cost는 workbench reframe로 insulated. [D1,D4]

---

## 2. Divergence
- **citation**: G₂ part=Cartan(Aut(𝕆)=G₂) / full Aut(𝕊)=Eakin-Sathaye 1990(검증) / D4 "Brown 1967"=haiku 혼동 추정 / A4 arXiv:2512.07210=2024 refinement. → canonical = **Eakin-Sathaye 1990**.
- **A1(증명 존재) vs D1(open research)**: D1 = overcautious 오류. Eakin-Sathaye가 settle. A1 우세.
- **effort**: Aut(𝕆)=G₂ Lean = 6-12 person-mo (specialist) / full Aut(𝕊) = 8-24 person-mo. 합의 = research-level.

## 3. Open Questions
- OQ1: arXiv:2512.07210의 "resolved discrepancy"가 정확히 뭐였나 (형식화 전 확인 권장 — 고친 오류 replicate 방지).
- OQ2: MB1 7-form enumeration이 실제로 3+4=7 exhaustive한가 (cheapest-settle 실행해 확인).

## 4. 권장 후속 (actionable, 우선순위)

1. **[즉시, 5분] MB1 cheapest-settle** — `SedenionPhase3_FormUniqueness.lean`의 7 FormCandidate vs refuted/unfalsifiable set enumerate. 7=7 확인 시 escape-lane 구조적 closed → posterior 0.01→0 정직 확정. **Mathlib lake build 금지** (zero ROI). MB1 sorry는 "empirically moot"로 문서화.
2. **[선택, 1-2h] Aut(𝕊) 계산검증** — Magma/GAP로 dim·S₃ closure·structure constants 검증 = HIGH-credibility computational evidence. + 정직 partial Lean ("14-dim G₂-type root system", 추상 G₂ iso는 defer).
3. **[금지/PARK] full Lean Aut(𝕊) 형식화** — 8-24 person-mo research program, 물리 refuted라 ROI 낮음. octonion+G₂를 Mathlib에 먼저 쌓아야. 사용자 explicit opt-in + 외부 Mathlib mentor 없으면 PARK.

**한 줄**: Aut(𝕊)는 *증명돼 있고(Eakin-Sathaye 1990)* Lean화만 research급 → 계산검증으로 충분. MB1은 *증명할 가치 없음(딜레마)* → 5분 enumeration으로 닫음. 둘 다 물리 부활 아닌 정리/closure 작업.

*KG: 16 RF under `lesson-ice-sorry-discharge-path-2026-06-01`. citation Eakin-Sathaye 1990 검증(WebSearch 2026-06-01).*
