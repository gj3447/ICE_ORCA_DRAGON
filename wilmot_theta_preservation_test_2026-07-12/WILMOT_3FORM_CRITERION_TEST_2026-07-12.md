# Wilmot eq-(9) calibration-3-form criterion test — OQ1 Aut(𝕊) dispute (2026-07-12)

> lakatotree `ice-orca-dragon` / frontier `q_aut_full_proof`. Node `wilmot_eq9_theta_criterion_test`
> (verdict `partial`, closes `q_wilmot_eq9_theta_criterion`, opens `q_wilmot_cross_primary`).
> Receipt: `wilmot_theta_preservation_test_2026-07-12/RESULT.json` (sha256 90eafef9…). L1 algebra layer only.
> Method: ground Wilmot's *actual* Θ (workflow wf_2bb1662d-598, full PDF) → independently verified by own
> `pdftotext` of arXiv:2512.07210**v2** → decisive exact computation (run + 2× idempotent) → adversarial pre-check GO_WITH_FIXES applied.

---

## 0. 한 줄

**58년 "분쟁"의 절반은 오귀속이었다.** SYMPOSIUM 정전이 Wilmot에게 붙인 "Aut(𝕊)=G₂ only, Ψ는 진짜 자기동형 아님"은 **Schafer(1954)의 입장**이고, Wilmot 2025(arXiv:2512.07210 v2)는 **정반대로 `G₂×S₃ ⊂ Aut(S)`를 확언**하며(Thm 5 `Aut(S)=Φ_S⋊S₃`) Brown의 σ,Ψ를 *genuine weak automorphism*으로 분류한다. 그리고 처음으로 Wilmot의 **실제 기준(곱셈 아닌 정준 3-form Θ)**을 테스트했더니 — **Wilmot의 eq-9 Θ(35항)가 SYMPOSIUM 자체 구조상수의 반대칭부와 부호까지 정확히 일치**(두 CD convention 모두)했고, 따라서 σ,Ψ는 이 Θ를 **정확히 보존**(잔차 σ=0, Ψ=2.8e-17)한다. 즉 SYMPOSIUM convention에서 Brown의 S₃는 Wilmot 의미의 *strong* automorphism이다. Wilmot이 말하는 "weak(Θ→Θ' primary 이동)"은 **cross-primary 현상**으로 한 convention 안에서는 보이지 않는다 → 이 부분은 sharpened OPEN.

**결론: Brown도 Wilmot도 반증되지 않았다.** "분쟁"은 *정의 차이*다 — Θ-고정(strong)=G₂ vs 모든 대수 자기동형(곱셈 보존)=G₂×S₃. 둘 다 각자의 정의에서 옳다. OQ1의 "different objects" resolution이 Wilmot의 1차 소스에서 **grounding됨**.

---

## 1. 정전 오귀속 정정 (primary source verbatim)

SYMPOSIUM 정전 3곳(`OQ1_WILMOT_DISPUTE…`, `queue_09_SS3TG.py`, `SedenionAut.lean` 헤더)이 모두 "**Wilmot 2025: Aut(𝕊)=G₂ only, Brown의 Ψ가 canonical 3-form을 깬다 → Wilmot REFUTED**"로 기술. **이는 오귀속이다.** arXiv:2512.07210v2(8 Jul 2026, 자체 pdftotext 검증) 실제 문장:

- **Intro (line 51)**: *"This analysis extends the work of Schafer[6] and Brown[7] for sedenions to find that **G₂ × S₃ ⊂ Aut(S)** and the full automorphism group is much more complicated. This result disagrees with Brown's full result that Aut(Aₙ)≅Aut(Aₙ₋₁)×S₃ for n∈(4,5,6)."* — Wilmot은 sedenion의 S₃를 **확언**하고, Brown의 *일반 귀납공식*만 반대.
- **Def. (line 792)**: *"Any transformation … that keeps the labels of the simplex in the same relative order shall be called a **strong automorphism**, which implies the associative calibration is invariant. Any transformation that changes the calibration to another calibration is a **weak automorphism** even if the labels change to equivalent labels in another primary."*
- **Theorem 5 (line 1304)**: *"The sedenion Harp(4) automorphisms satisfy the semi-direct product **Aut(S) = Φ_S ⋊ S₃**."*
- **Proof (line 1339)**: *"**Brown's extension of Schafer's automorphisms has introduced weak automorphisms**, Φ_O^{C(2)}, which do not keep Θ invariant. This allows all such automorphisms to be included. … By transforming to another calibration these are **acceptable automorphisms**."*

즉 "Aut=G₂ only"는 **Schafer**(strong-only 판독), Wilmot은 그것을 확장해 G₂×S₃⊂Aut로 간다. Θ = eq-(9), 35항, 64,864,800개 primary representation.

> 방법론 교훈: HTML을 소형 요약모델로 읽은 WebFetch는 이 논문의 결론을 **정반대("Aut≅G₂, supports Schafer")**로 보고했다. 밀도 높은 수학 논문의 load-bearing claim은 **버전 고정 + pdftotext 직접 문장 추출**로만 확정 (`lesson-webfetch-smallmodel-inverts-dense-math-claim-2026-07-12`).

---

## 2. 검증된 계산 (exact, 재현 2×)

`wilmot_theta_preservation_test.py` — Wilmot eq-9 Θ(35항)를 eq-10 index map(생성자 o1,o2,o3,o4=e1,e2,e4,e8 → binary CD 인덱스, m→e_m identity)으로 Im(𝕊)에 인코딩 후:

| 측정 | Convention A (Baez) | Convention B (opposite) | 의미 |
|---|---|---|---|
| **sign-alignment Θ_eq9 vs Alt(struct const)** | scale 1.0, resid **0.0**, support identical, sign-agree **1.0** | scale −1.0, resid 0.0, ident, 1.0 | **eq-9 Θ = SYMPOSIUM 자체 calibration, 정확 일치** (independent transcription vs independent CD computation) |
| σ residual on Θ_eq9 | **0.0** | 0.0 | σ가 Θ 보존 (strong) |
| Ψ residual on Θ_eq9 | **2.78e-17** | 2.78e-17 | Ψ가 Θ 보존 (strong) |
| G₂=Der(𝕊) 양성대조 | 8.3e-17 | 1.1e-16 | ✅ PASS (Θ는 G₂-invariant) |
| random O(15) 판별대조 | 0.256 | 0.256 | ✅ 깨짐 (apparatus 판별력 有) |
| tautology guard: Alt(struct const) under σ,Ψ | σ=0, Ψ=2.2e-16 (random 1.53) | 동일 | ✅ "everything breaks" 아님 |
| der_dim / σ,Ψ auto residual | 14 / 0.0, 1.1e-16 | 14 / 동일 | ✅ 대수 자기동형 확인 |

핵심: σ,Ψ는 곱셈을 보존(0/256)하므로 Θ=Alt⟨x,y·z⟩를 **정리에 의해** 보존. sign-alignment가 uncertain했던 진짜 예측(같은 primary인가 다른 primary인가?)은 **same-primary(Branch A)**로 판명 → SYMPOSIUM convention이 Wilmot의 "pure sedenion" primary에 위치.

---

## 3. Reconciliation — OQ1 resolution grounded

Wilmot은 "Brown의 weak automorphism은 Θ를 다른 primary로 보낸다(Rβ Θ R−β ≠ Θ)"고 하는데, 내 계산은 σ,Ψ가 Θ를 **보존**(잔차 0)한다. 모순 아님:

- **SYMPOSIUM의 σ,Ψ = 대수 자기동형의 행렬 실현**: 곱셈 보존 → 대수 자체 calibration Θ=Alt(struct const) 고정 → 이 실현에서는 *strong*.
- **Wilmot의 weak = Cl(15) 2-form 회전 Rβ 실현**: 같은 추상 S₃이지만 특정 signed calibration primary를 다른 primary로 이동.
- 같은 추상 S₃의 **다른 구체 실현**이 고정된 signed tensor에 다르게 작용. "different objects" — Brown(대수 자기동형 = 곱셈 보존)과 Schafer(strong = Θ 고정)는 *서로 다른 정의*이며 각자 옳다. Wilmot 논문이 strong/weak로 이걸 명시적으로 화해시킴.

**따라서 OQ1 = `:CompetingVerdict` 양립은 유지되되, "다른 대상" 해석이 Wilmot 1차 소스로 승격 (CANDIDATE_RESOLUTION → GROUNDED). "Wilmot refuted"는 available outcome 아님 (오귀속).**

---

## 4. 열린 채로 (NO forced closure)

- `q_wilmot_cross_primary` (OPEN): Wilmot의 Θ→Θ' cross-primary 이동은 단일 convention의 대수-자기동형 실현에서 안 보임. 실측하려면 *다른* primary Θ*와 Wilmot의 명시적 2-form Rβ 실현을 인코딩해 Θ*→Θ*' 확인. (64,864,800 primary 구조)
- `q_aut_full_proof` (OPEN 유지): `Aut(S)=Φ_S⋊S₃`(또는 G₂×S₃)의 Lean sorry=0 형식증명. `SedenionAut.lean` 34 sorry (§5.1 `sigmaMap_mul`은 CD `HasDistribNeg` instance 완성으로 환원, Phase-2 대수작업).
- DIRECT vs SEMIDIRECT: SYMPOSIUM은 Der 인자 위 direct(A_φ=I) 확인; Wilmot은 Φ_S⋊S₃(semidirect). 양립 — S₃가 더 큰 Φ_S엔 nontrivial, G₂=Der 인자엔 trivial. Wilmot의 Φ_S 정의 대조는 미검증.

---

## 5. Receipts / KG

- 스크립트: `wilmot_theta_preservation_test_2026-07-12/wilmot_theta_preservation_test.py` (sha256 `90eafef960148bb15a6aab284f75ceac37f312358ce3d606f9427e34b2249dce`), 재현 `python … RESULT.json`.
- 토대: `aut_s3_direct_product_test_2026-07-12`(byte-재현 확인, direct product), `queue_09_SS3TG.py`(0/256 곱셈 보존).
- lakatotree: node `wilmot_eq9_theta_criterion_test` (verdict partial, novel=false — Branch A는 정리귀결이라 nobel-grade novel 아님; 정직), closes `q_wilmot_eq9_theta_criterion`, opens `q_wilmot_cross_primary`.
- 1차 소스: arXiv:2512.07210v2 (Wilmot, *Automorphisms of Sedenions*), arXiv:2505.11747; Brown 1967 Pacific J. Math. 20:415; Schafer 1954 Amer. J. Math. 76; Cawagas 2004.
- 신화 layer(USER_PRIMARY)는 손대지 않음 (Eilu va-Eilu).

# KG: lesson-ice-wilmot-misattribution-schafer-not-g2only-2026-07-12, lesson-webfetch-smallmodel-inverts-dense-math-claim-2026-07-12, wilmot-eq9-theta-eq-symposium-calibration-2026-07-12
