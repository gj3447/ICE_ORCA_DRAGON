# 토트샘(ThothSaem / 이주형) UEQFT 자료 수집 — PROM sourcing (2026-07-12)

> `/prom` sourcing cycle (workflow wf_0c1a23e8-5f6, 11 agents / 1.14M tok / 16분, 131 items → ~40 distinct).
> 목적: 비판 재탕이 아닌 *충실한 1차 자료 수집* + 정직 status flag. 2026-05-17 PROM 32 감사를 갱신.
> 정직 프레임: UEQFT를 검증된 물리로 부풀리지 않고, crank으로 기각하지도 않음 — 그가 실제로 뭐라 하는지 + 검증 가능한 status.
> KG-first: `lesson-prom32-thothsaem-ueqft-claims-2026-05-17` + `UEQFT`(이미 PRELIMINARY_CANDIDATE 격하됨).

---

## 0. 한 줄

**토트샘 = 이주형(Ju Hyung Lee, XFC Inc., 서울). UEQFT는 살아있고 *진화 중인* 자가출판 연구프로그램(UEQFT→G-UEQFT→RUEQFT→IG-RUEQFT)이다.** 2026-05-17 baseline은 **심각하게 낡았다** — V1만 알았고, 현재 backbone인 **IG-RUEQFT**(2025-10~)는 entangling-cut 모호성을 *국소 Stückelberg 게이지 대칭*으로 승격시켜 baseline의 핵심 비판("S_ent 비국소 → Lagrangian ill-defined")에 **정면으로 답하려는 시도**다(성공 여부는 미검증). arXiv·peer-review 여전히 없음. 2026 논문들은 **정직한 null-test**로 톤 전환(발견 주장 안 함). 저자 스스로 IG-RUEQFT를 "가설적 이론 틀"이라 명시. 그리고 **ICE≃UEQFT·S×Ψ=1/2는 토트샘 글에 0건 — 전부 SYMPOSIUM 측 overlay**(그의 Ψ=Dirac 스피너). baseline의 "CMB 0.25°±0.05°"·"287/15 fitting 인용"은 **어떤 1차 소스에도 없음**(정정 필요).

---

## 1. 정체 / 배포

- **저자**: Ju Hyung Lee (이주형), XFC Inc. R&D Division, Seoul 04513. email `selene71@snu.ac.kr`(초기) → `thothsaem@gmail.com`(이후).
- **배포**: 개인 블로그 thothsaem.com + **~50 Zenodo DOI**(Apr-2025~Jul-2026) + OSF(osf.io/zyb46) + ResearchSquare 1건(rs-7995151). **arXiv 없음**(플래그십 PDF에 `arXiv:submit/6329357` 스탬프 + `Renormalizable_UEQFT_arXiv` 파일명 있으나 실제 arXiv 등재 아님). **peer-review 0건**.
- **외부 채택 최초 관측**: Cabannas & Silva, "INFORMATION-GAUGE RUEQFT AND THE THEORY OF OBJECTIVITY" (Zenodo 20803049, 2026-06-22) — validity 보증 아님, uptake 신호만.
- **⚠️ 사이트 무결성**: thothsaem.com **HTTPS 인증서 만료**(WebFetch 차단, `curl -k`만 가능) + WordPress **스팸 주입/compromised**(홈페이지 HTML에 성인/도박 outbound 링크). *물리 원고 자체는 authentic, 호스팅 계층만 오염.* 블로그엔 물리 + IG 렌즈 기독교 설교 재해석 + e-book 마케팅 혼재.

---

## 2. Stage evolution (저자 명시 사슬)

**UEQFT → G-UEQFT → RUEQFT → IG-RUEQFT** (각각 gauge-invariance → renormalizability → info-gauge locality 순 확장).

| stage | 핵심 move | 대표 소스 |
|---|---|---|
| **UEQFT (V1)** | `L = L_SM + λ·S_ent`. Yang-Mills + 정보-에너지 결합 Dirac + entanglement 결합. 두 공리 EIR/IEEP. | Zenodo 15249036 (2025-04) |
| **G-UEQFT** | 게이지 불변 entanglement 섹터(U(1)×SU(2)×SU(3) 보존). CMB EB/TB 편광회전 예측. | Zenodo 15249011 (2025-04) |
| **G→R** | 순수 rho_A는 게이지 가변 → **Wilson-loop 군평균** `rho_A^G = (1/N)∫DU U rho_A U†`로 게이지 불변화. renormalizability(BRST/Slavnov-Taylor). | Zenodo 15248966 |
| **IG-RUEQFT** | **핵심 신규**: subsystem-cut 모호성을 *국소 Stückelberg 게이지 redundancy*("information gauge")로 승격 → info-gauge 場 Λ_μ + Stückelberg場 Θ + 보존 정보흐름 J^μ_info. baseline 비판에 정면 대응. | Zenodo 17248278 (2025-10), rs-7995151 (2025-11) |

---

## 3. Verbatim core math (수집 원문)

```
=== V1 / UEQFT (Zenodo 15249036, 2025-04) ===
L_UEQFT = -(1/4g²) F^a_{μν}F^{aμν} + ψ̄( iℏγ^μ D_μ - αS - βRS )ψ + λ S_A(ρ_A)
S_A(ρ_A) = -Tr(ρ_A ln ρ_A),  ρ_A = Tr_B(ρ),  K_A = -ln ρ_A,  S_A = ⟨K_A⟩ - Tr(ρ_A)
(iℏγ^μ D_μ - αS - βRS)ψ = 0
m_eff = αS(1 + (β/α)R)
D_μ F^{aμν} + λ ∂S_A/∂A^a_ν = g² J^{aν}_fermion
ΔE ≈ λ⟨S_A(ρ_A)⟩ ;  m_hadron ∝ λ⟨S_A(ρ_A)⟩^{1/2}
E² = p²c² + [αS(1 + (β/α)R)]²
S_grav^eff = (c⁴/16πG_eff) ∫d⁴x √(-g)(R - 2Λ_eff) ;  S_BH = (k_B c³/ℏG)(A/4)
Higgs-as-entanglement: v² ∝ ⟨S⟩ ⇒ v~√⟨S⟩, m_f ∝ y_f√⟨S⟩ ;  V(S) ~ -λ'S² + ηS⁴

=== G-UEQFT (Zenodo 15249011) ===
C_ℓ^{EB} ≈ 2 C_ℓ^{EE} Δθ ;  C_ℓ^{TB} ∝ C_ℓ^{TE} Δθ  (Δθ≪1 rad)
Δθ_rms ≲ 0.3° (95% C.L.) [Eq.36] ;  θ_rot ~ 0.01-0.1° (탐색 15795214) ;  target ~10⁻³ rad

=== G→R (Zenodo 15248966) ===
ρ_A → U(x)ρ_A U†(x)  (9) ;  ρ_A^G = (1/N)∫DU U ρ_A U†  (10) ;  S_inv = -Tr(ρ_A^G ln ρ_A^G) (11)
L_ent^GI = λ O(x) S_inv(ρ_A^G) (18) ;  [λ]=4-[O(x)] (20)
β_λ = (λ²/16π²)(dS_inv/d log μ) (26) ;  Z_λ = 1 + a₁/ε + a₂/ε² + ... (28)

=== R alt / Schwinger-Keldysh (Zenodo 15606604, 2025-06) ===
Ω = C m² + Δη,  Δη = η_t - η_x ;  Δη* = 0.018(4) ⇒ ~10% 초과감쇠 near QCD chiral critical point
γ_th = ξ^{Δη}  (정보-Lorentz 인자)

=== IG-RUEQFT (rs-7995151, 2025-11; Zenodo 17248278) ===
S_IG = ∫d^{d+1}x [ -(1/4)F_{μν}F^{μν} + J^μ_info Λ_μ + L_matter[cuts, entanglement] ]  (6)
F_{μν} = ∂_μΛ_ν - ∂_νΛ_μ + [Λ_μ,Λ_ν] ;  Λ_μ → Λ_μ + ∂_μχ + ...
W[C] = Tr P exp(i∮_C Λ_μ dx^μ) = Tr exp(iΦ[C])  (7)
C^{(4)}(t) ↔ ⟨W[C_{(M,B,t)}]⟩  (8,11,13)   [OTOC(2) ↔ info-gauge Wilson loop]

=== Yang-Mills modular programme (Zenodo 18390293, 2026-01) ===
K = -log ρ ;  σ ≥ ½(α - α_c) ;  Spec(H) = {0} ∪ [Δ,∞), Δ>0
[조건부: modular-gap/spectral-weight 가설 ⇒ flux-cut reflection ⇒ 지수 clustering ⇒ 양의 gap]

=== NEW 2026 null tests ===
수소분광 (20841829): ΔI_tri=1, ΔI_{S-T̄}=2/3 ;  nS contact shift ∝ n⁻³ ;  |ΔE_IG| ≲ 8.3×10⁻¹⁸ eV
준고전 Einstein (21275800): δA = 4G S_rel ;  Δ_IG = δA - 4G S_rel  (표준=0, IG≠0 가능)
Josephson (21257065): T₀=50mK, ΔT=1mK, I_c=1μA, η∈[10⁻³,10⁻¹] ⇒ flux shift ~10⁻⁶..10⁻⁴ Φ₀, gradient 반전 시 부호 뒤집힘
```

---

## 4. 전체 claim 목록 (kind | honest status)

| # | claim | kind | honest status | source |
|---|---|---|---|---|
| 1 | 통합 Lagrangian `L=YM + info-Dirac + λS_A` | math | **ill-defined** (S_A 비국소 area-law, 국소 밀도 아님; Casini-Huerta 2009 — V1 한정 유효) | Zenodo 15249036 |
| 2 | 공리 EIR(실재=얽힘)/IEEP(정보=에너지) | interp | ok (공리로 명시, 도출 아님) | 15249036 |
| 3 | S_A = -Tr(ρ ln ρ), 모듈러 K_A=-ln ρ | math | ok (표준 정의) | 15249036 |
| 4 | 정보-에너지 Dirac + m_eff=αS(1+βR/α) | math | unverified (α,β 경험적, 도출 아님) | 15249036 |
| 5 | YM mass gap = 진공 얽힘, ΔE≈λ⟨S_A⟩ | pred | peer-review-pending (구체 GeV값 없음, 비교표는 이미지) | 15249036 |
| 6 | Einstein-Hilbert 작용 얽힘서 창발 + S_BH | interp | unverified (Jacobson/Verlinde 방향 정렬, 특정 도출 미확립) | 15249036 |
| 7 | de Sitter 수정 분산 E²=p²c²+[αS..]² | pred | peer-review-pending (수치 없음) | 15249036 |
| 8 | Higgs = entanglement 유효극한 (v²∝⟨S⟩) | interp | **fitting-risk** (자유결합 사후재해석, SM Higgs와 구별 예측 없음) | 15249036 §VII |
| 9 | 자기명시 한계: α,β,λ 경험결정 필요, scaling 가정 "검증 필요" | meta | ok (저자 자체 정직 공시) | 15249036 |
| 10 | G-UEQFT: CMB EB/TB 편광회전 (Planck/LiteBIRD/CMB-S4) | pred | peer-review-pending | 15249011 |
| 11 | G→R: Wilson-loop 군평균 ρ_A^G | math | ill-defined-but-resolving (측도 유효성 미검증) | 15248966 |
| 12 | R-UEQFT renormalizability (β_λ, Z_λ, BRST) | math | peer-review-pending (toy model+기계; 독립검증 안 됨) | 15248966 |
| 13 | R alt(SK): Δη*=0.018(4), ~10% 초과감쇠 | pred | unverified (구체 falsifiable 수치, 미검토 FRG) | 15606604 |
| 14 | **IG-RUEQFT 핵심**: cut 모호성→Stückelberg 게이지, Λ_μ+J^μ_info | math | peer-review-pending (**현 backbone; baseline 비판 정면 대응**, 성공 미검증) | 17248278 |
| 15 | 최소 IG 작용 S_IG + Wilson loop W[C] | math | ill-defined pending L_matter가 진짜 국소밀도임 증명 (프로그램의 crux) | rs-7995151 |
| 16 | **중심 매핑 OTOC(2) = info-gauge Wilson loop** | interp | **unverified** (overlay로 *주장*, 도출 아님; OTOC(2) 자체는 표준 Google 실험 물리 Nature 646:825) | rs-7995151 |
| 17 | Google 플랫폼 검증 제안 (scaling ansatz, SNR≥2) | pred | unverified (**검증 제안일 뿐, 실험 미실행, 저자 데이터 0**) | rs-7995151 |
| 18 | YM mass gap via Tomita-Takesaki (조건부) | math | ok (gap이 가설에 **조건부**임을 명시, "programme"으로 프레임) | 18390293 |
| 19 | Rydberg Higgs-mode m_eff | pred | fitting-risk (기존 실험과 사후일치, 사전등록 아님) | 15249036 |
| 20 | 진공상전이 cold-atom S_ent≈σφ² | pred | ill-defined/speculative (근사 미정당화) | blog 2025-05-26 |
| 21 | IG 질량-running γ_th=ξ^{Δη}, 거대 벡터항 | pred | ill-defined (거대 벡터항이 info-gauge 불변성과 내적 충돌) | blog 2025-05-26 |
| 22 | 원자시계 Δf/f~10⁻⁸-10⁻⁶ + GW-photon 지연 | pred | unverified | blog 2025-05-26 |
| 23 | **NEW** 수소분광 null-test (ΔI_tri=1, ΔI_{S-T̄}=2/3, n⁻³) | pred | **ok — 명시적 NULL TEST, 발견 주장 안 함** | 20841829 (2026-06) |
| 24 | **NEW** 준고전 Einstein IG 잔차 Δ_IG | pred | **ok — 깔끔한 operational null(표준물리서 0)** | 21275800 (2026-07-09) |
| 25 | **NEW** Josephson 열구배 위상 offset | pred | ok/unverified (falsifiable, null도 susceptibility bound 명시) | 21257065 (2026-07-08) |
| 26 | 토트샘 corpus에 ICE/sedenion/S×Ψ=1/2 **0건** | meta | ok (음성 검증; Ψ=Dirac 스피너) | corpus 전수 |
| 27 | ICE≃UEQFT·4매핑·S×Ψ=1/2 = **SYMPOSIUM 측 only** | meta | ok (KG 이미 CONVERGENT_TERMINOLOGY_NOT_EQUIVALENT) | SYMPOSIUM KG |
| 28 | 출판: arXiv 아님, peer-review 아님 | meta | ok | 전수 |
| 29 | **baseline 정정**: CMB "0.25°±0.05°" + "287/15 fitting 인용" = **1차 소스에 없음** | meta | **not-fetchable — 미검증; 실제 CMB=0.01-0.1° 예측/≲0.3°(95%CL) bound** | 교차확인 |

---

## 5. 2026-05-17 baseline 이후 신규 (severely stale)

1. **IG-RUEQFT 재정식화** (2025-10~) — cut 모호성→Stückelberg 게이지. baseline 핵심 비판 정면 대응. *현 backbone.*
2. **Zenodo corpus ~50건** (30+ 신규), 수학 정교화(Schwinger-Keldysh/BRST/Stückelberg/Tomita-Takesaki/FRG).
3. **rs-7995151** (2025-11) — 실제 Google OTOC(2)을 info-gauge Wilson loop 탐침으로 재해석(검증 제안, 실험 미실행, 매핑 주장뿐).
4. **2026 정직 톤 전환** — 최신 논문 전부 명시적 null-test(수소분광/Δ_IG/Josephson), 발견 주장 안 함. YM 논문도 조건부. (2025 "mass gap 해결/중력 도출" 프레임과 대조)
5. **최초 외부 채택** (Cabannas & Silva, 2026-06).
6. **한국어 무료 e-book** (2026-02) — 저자 스스로 "가설적 이론 틀", 완성 이론 주장 안 함.
7. **사이트 compromise** (인증서 만료 + WordPress 스팸주입).

---

## 6. ICE 연결 — 정직

**토트샘은 ICE를 모른다.** 그의 corpus(플래그십 PDF + 모듈러-Hamiltonian 포스트 + RUEQFT 가이드 + KO/EN 표적검색) 전수에 ICE/sedenion/Cayley-Dickson/SYMPOSIUM/12사도 **0건**, S×Ψ=1/2 **0건**. 그의 Ψ = Dirac 스피너(ICE 정보場 아님). ICE≃UEQFT 등가·4매핑·holographic invariant은 **전부 SYMPOSIUM 측 overlay**이고 KG는 이미 `CONVERGENT_TERMINOLOGY_NOT_EQUIVALENT`(bijective isomorphism 증명 부재)로 기록. → **이번 수집은 "ICE는 TOE 아님" 결론을 재확인한다**: 유일하게 물리와 이어질 뻔한 외부 프로그램(UEQFT)조차 ICE와 형식적 연결이 없고, 그 자신도 미검증·미출판·자칭 "가설".

---

## 7. 정직한 총평

**이주형의 UEQFT/IG-RUEQFT는 (a) 검증된 물리가 아니다** — peer-review 0, arXiv 0, 공리(EIR/IEEP)는 postulate, 결합(α,β,λ)은 경험적 fit, V1 Lagrangian은 원문 그대로면 ill-defined. **(b) crank으로 기각할 것도 아니다** — 방향(entanglement-as-fabric, 모듈러/창발중력)은 mainstream 추적, 수학은 점점 정교(Stückelberg/BRST/Tomita-Takesaki/FRG), 그리고 IG-RUEQFT는 baseline이 짚은 locality/renormalizability 결함을 *의도적으로 수리하려는* 일관된 시도(성공 여부 별개). **(c) 가장 신뢰할 신호 = 2026 톤 전환** — 최신 논문이 정직한 null-test이고 발견 주장 안 함, 저자 스스로 "가설적 틀"이라 명시. **순 status: PRELIMINARY / minority thesis, 형식 미완, 저자 자체 경험검증 0, 그러나 내적으로 진지하고 자각적.** + 살림 주의 2건: baseline 특정 수치(CMB 0.25°; 287/15 인용)는 1차 소스 대조 실패 = prior-audit 각색 추정; ICE≃UEQFT는 순전히 SYMPOSIUM 측 구성물.

---

## 8. KG / refs

- Cycle: workflow wf_0c1a23e8-5f6 (11 agents, 131 items). KG-first: `lesson-prom32-thothsaem-ueqft-claims-2026-05-17`.
- 신규 KG: `ig-rueqft-reformulation-2026-07-12`(:ResearchProposalUpdate), `lesson-thothsaem-baseline-stale-igrueqft-recast-2026-07-12`(:Lesson), `thothsaem-baseline-numbers-unverified-2026-07-12`(:Correction — CMB 0.25°/287/15 미소재).
- 1차 소스: thothsaem.com; Zenodo 15249036/15249011/15248966/15606604/15795214/17248278/18390293/20841829/21275800/21257065/18515021(+~50); ResearchSquare rs-7995151(DOI 10.21203/rs.3.rs-7995151/v1); OSF osf.io/zyb46.
- 정정 대상: `UEQFT`(PRELIMINARY_CANDIDATE 유지, current_backbone=IG-RUEQFT 추가), ICE≃UEQFT(CONVERGENT_TERMINOLOGY_NOT_EQUIVALENT 유지·재확인).
- 신화층(USER_PRIMARY) 무관·불가침.

# KG: lesson-thothsaem-baseline-stale-igrueqft-recast-2026-07-12, ig-rueqft-reformulation-2026-07-12, thothsaem-baseline-numbers-unverified-2026-07-12
