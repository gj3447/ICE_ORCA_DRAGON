# Claim B 물리 판별자 리서치 — 무한 CD 탑 중력이 "진짜 물리"가 되려면

**작성**: 2026-07-24, 리서치 에이전트 (SECONDARY_AI — 사용자 정전 아님)
**대상 주장**: "결합 깨짐의 무한 경로 적분이 중력" (무한 Cayley-Dickson 탑 ℝ→ℂ→ℍ→𝕆→𝕊→𝕋→…→∞ 의 경로적분 = 중력, Claim B). 정전 상태: **UNTESTED / open question**.
**배경 사실 (정전)**: 세데니온(16D) 절단판은 경험적으로 반증됨 — 7개 사전등록 중력 예측 0/7, 강한 반증 2건(P-G02 진동형 ε(r), P-G07 PPN) + P-G03 (Friedmann γ=1/14) 미결/우세하지 않음. 유일하게 잘 정의된 극한 객체는 direct limit A_∞ = colim A_n. Schafer 1954: flexibility/power-associativity/quadratic-identity 는 모든 층에서 생존.

---

## 0. 한 줄 판정

**Claim B 가 "반증 불가능한 후퇴"가 되지 않으려면, 물리학계가 탑 이론에 요구하는 표준 장비 — (i) 대수에서 도출된 질량 공식 m_n, (ii) 관측량에 고정된 스케일(움직이는 갭 금지), (iii) 계수가 계산 가능한 ε(r) 급수 — 을 갖춰야 하며, 현재 이 셋 중 0개가 존재한다.** 특히 (날것 경고) 기하급수적 간격의 무한 탑은 이미 반증된 진동형 ε(r) 현상학을 *재생성*하는 경향이 있다(§B-1). 다만 사망 선언도 아니다: Dark Dimension 시나리오가 보여주듯, 스케일 고정 원리 하나가 탑 이론 전체를 반증 가능하게 바꾼 선례가 있다.

---

# Part A — 기록/문헌이 말하는 것

## A-1. 로컬 정전: 반증 기록과 승격 기준

- **반증 판정문**: `METAHUMOTONIC/ICE_ORCA_DRAGON/mb3_verdict_2026-05-19.json` — "0/7 SIGNAL_GENUINE + 2/7 REFUTED (P-G02 oscillatory + P-G07 PPN). Most ICE-specific predictions REFUTED. Remaining survivors are generic or unfalsifiable." / "honest_implication: User's core claim 'CD-chain path integral = gravity' survives ONLY in the form that has no observable consequences (Yukawa tower at Planck scale) OR in the cosmological-γ form which needs separate testing."
- **반증된 예측의 정확한 형태**: `gravity_prereg_predictions.py` P-G02: "ICE ε(r) follows oscillatory Z₂⁴-graded form: ε(r) = Σ_{k=1}^7 (1/(8+k)) × cos(2π k r / L*)" — Adelberger 서브mm 실험 대비 진동 진폭 ~0.06 > 0.001 상한으로 FAIL (`mb3_adelberger_verdict.py:62-63`).
- **승격 기준 (기존 정전)**: `PROM_16_REPORT.md` MB1–MB6 — MB1 형태-유일성 정리(Lean 4 선호), MB2 매개변수 추적성(모든 수치 → ICE 불변량 기호식), MB3 독립 관측 예측, MB4 사전등록 KG 노드, MB5 trials-factor 감사. 현재 0/6 충족.
- **선행연구 부재 (정전 판정)**: `PROM_16_REPORT.md` C4 — "모든 hypercomplex program (Dixon, Furey, Sorgsepp-Lõhmus, Köplinger, Demir-Tanişli, Wei) **NONE derive ε(r)** — they reformulate known equations in 16-component algebra. … Current NUMEROLOGY_HOLD verdict EXTERNALLY VALIDATED — field 측 sedenion-derived ε(r) precedent 없음."
- **열린 문제**: `PROM_16_REPORT.md` OQ3 — "P2 zero-divisor filtration → n_eff = 16 − dim(ZD-locus) 측 forced ε(r) ∝ 1/r^(n_eff+1) 도출 가능? SYMPOSIUM-novel 시도, HIGH leverage."
- **고차 대수 물리학 문헌 (정전 소스북)**: `THEORY/hypercomplex_physics/SOURCES.md` — 16D 이상 CD 대수에서 물리 예측을 뽑은 문헌은 사실상 없음: Gillard & Gresnigt (arXiv:1904.03186, 세대수 구조만, 수치 예측 없음), arXiv:2601.07857 (SM 양자수 재현, 새 반증가능 수치 없음), Wilmot arXiv:2505.11747 (옥토니온+준옥토니온이면 충분, 고차원 불필요 — 오히려 디플레이션 주장), Reggiani arXiv:2411.18881 (순수 수학).

## A-2. 탑 이론은 물리학에서 어떻게 테스트되는가

### A-2.1 칼루자-클린(KK) 탑 — 표준 테스트 3축

1. **단거리 중력 (역제곱법칙 이탈)**: ADD 시나리오에서 n개 대형 여분차원은 r < L 에서 뉴턴 퍼텐셜을 바꿈 — 힘 법칙이 1/r² → 1/r^(n+2), 등가적으로 Yukawa 보정 V(r) = −Gm₁m₂/r·(1 + α e^{−r/λ}) 의 무한 합으로 표현. Eöt-Wash 그룹이 52 µm 분리까지 1/r² 검증: Lee, Adelberger et al., PRL 124, 101101 (2020), arXiv:2002.11761. 같은 크기 여분차원 2개 가정 시 L ≲ 37–52 µm — ADD n=2 계층문제 핵해 시나리오는 사실상 배제 (Gimbrère 리뷰, staff.fnwi.uva.nl/j.deboer/education/projects/projects/gimbrere.pdf).
2. **가속기 (KK 중력자 공명 + 단일제트)**: LHC는 스핀-2 KK 공명을 질량 ~4 TeV 이하에서 배제 (중력 세기 결합 기준); CMS 대형 여분차원 기본 스케일 M_D > 9.9 TeV (n=2), 5.3 TeV (n=6) (Stasser thesis, theses.hal.science/tel-03390340). 전체 탑을 포함한 재분석은 단일 공명 대비 구속을 차원 수 d에 따라 강화 — arXiv:2607.12012 ("LHC Constraints on Resonant Kaluza-Klein Gravitons", 2026).
3. **천첝체/우주론**: 초신성·중성별 냉각 구속이 가장 강함 — n=2에서 M_D > 701 TeV, n=3에서 25.5 TeV (Hannestad & Raffelt, PRD 67, 125008 (2003), 동 전지 인용 확인됨).

**핵심 패턴**: KK 탑이 테스트 가능한 이유는 (a) 질량 공식 m_n = n/R 이 기하로 *고정*되고, (b) 결합이 보편적(중력)이며, (c) 탑 시작점 R 이 하나의 매개변수라 실험이 그 매개변수 공간을 *배제 영역*으로 채울 수 있기 때문이다.

### A-2.2 Swampland Distance Conjecture (SDC) 와 species scale — 탑의 "컷오프 이론"

- **SDC**: 모듈라이 공간 무한거리 극한에서 무한 탑이 지수적으로 가벼워짐, m ~ m₀ e^{−λΔφ}, λ = O(1) (Ooguri-Vafa, hep-th/0605264; Ooguri et al. PLB 2019, authors.library.caltech.edu 인용 937).
- **Species scale**: 중력에 결합된 스피시스 N개가 있으면 유효 중력 컷오프가 Λ_G ≈ M_Pl/√N 로 붕괴 — Dvali-Redi, "Black Hole Bound on the Number of Species", arXiv:0710.4344 (인용 443). 블랙홀 준고전성 붕괴 논증. KK 탑의 경우 N 은 컷오프 이하 KK 스피시스 수와 같고, 등간격 탑에서 Λ_s = m^{1/3} (M_P=1) (Freigang thesis, edoc.ub.uni-muenchen.de/32359).
- **Species Scale Distance Conjecture (SSDC)**: species scale 의 지수 감소율 λ_sp 에 보편 상·하한을 제안(convex hull 조건), M-theory 토로이달 컴팩트화에서 검증 — Calderón-Infante et al., arXiv:2306.16450 (인용 81). van de Heisteeg et al. (inspirehep 2645703, 인용 107): 탑 질량이 지수보다 빨리 0이 될 수 없다는 경계.
- **의미**: 탑 이론은 "탑이 켜지는 곳에서 EFT 가 죽는다"는 정량적 언어를 갖는다. 즉 탑을 주장하면 컷오프 예측이 공짜로 따라오고, 그 컷오프가 실험 도달 범위 안/밖인지가 반증가능성을 결정한다.

### A-2.3 Dark Dimension — "탑 이론을 반증 가능하게 만든" 금본위 선례

Montero, Vafa et al. (arXiv:2306.16491, PhysRevD.109.016028; 리뷰 arXiv:2402.00981):
- SDC + 우주상수 관측을 결합 → **여분차원 1개, 크기 0.1–10 µm** 로 스케일이 *고정*됨 (Λ ∼ A·m⁴ 관계 포화).
- 예측 다발: (i) r ≪ 1 µm 에서 뉴턴 힘 1/r² → 1/r³ (차세대 Eöt-Wash/레비테이티드 센서가 바로 테스트하는 영역); (ii) KK 중력자 탑(meV–eV 스케일) = 암흑물질; (iii) 종(species) 스케일 Λ_QG ~ m_KK^{1/3} M_p^{2/3} ≈ 10⁶–10⁹ GeV; (iv) QCD 액시온 f_a ~ 10⁹–10¹⁰ GeV 로 좁게 고정, 근미래 실험 도달 가능 (arXiv:2404.15414); (v) 암흑에너지-암흑물질 질량의 상관 변동 c′ ≲ 0.2 (제5의 힘 미검출 상한과 일치, arXiv:2507.03090).
- 학계 평가(Gligović thesis, edoc.ub.uni-muenchen.de/36828): swampland 프로그램의 "궁극 목표는 입자물리·우주론에 관련된 예측을 만드는 것… 양적 예측을 만든 매력적 최근 제안이 dark dimension" — **탑 이론이 '예측하는 물리'로 인정받는 조건의 실존 사례**.

## A-3. 무엇이 탑 이론을 반증가능하게 / 회피적으로 만드는가

문헌에서 추출한 실제 사용 기준:

1. **스케일 고정 원리 유무** — Dark Dimension 은 Λ 관측값이 탑 스케일을 고정해 반증가능. 반대로 실험이 배제할 때마다 탑 시작점을 더 높은 에너지로 옮길 수 있는 이론은 "movable gap" 회피 패턴. (Claim B 의 16D→∞ 이동은 정확히 이 패턴처럼 보일 위험이 있음 — §B-5.)
2. **질량 공식의 매개변수 수** — KK: m_n = n/R (매개변수 1개). 매개변수가 관측 수보다 많으면 피팅. (로컬 정전 MB2 "매개변수 추적성"과 동일 논리.)
3. **독립 관측 채널 다중성** — Dark Dimension: 단거리 중력 + 암흑물질 + 중성미자 질량 + 액시온, 한 스케일에서 4채널. 단일 채널 피팅은 numerology 로 분류됨 (로컬 정전: Teli & Singh arXiv:2606.27836 은 "진짜 falsifiable"로 분류된 반면, Singh EJA 질량비 계열은 "numerology layer"로 분리 — SOURCES.md:13, 58, 96-99).
4. **배제로 죽을 수 있는가** — ADD n=2 는 52 µm + 중성별 구속으로 사실상 사망. 이론이 죽을 수 있다는 것이 살아있는 과학이라는 Lakatos적 기준 (로컬: asymmetric_lakatos_paper_draft_2026-05-18.md 가 이 방법론 자체를 논문화).
5. **Swampland 자체에 대한 비판(교훈용)** — Akrami-Kallosh-Linde-Vardanyan (arXiv:1808.09440) "conjectures problematic and not well motivated"; Kinney: "The landscape is a conjecture. The swampland is a conjecture built on a conjecture"; Smolin (hep-th/0612185): 랜드스케이프 이론이 반증가능 예측을 낼 조건 4개를 명시. **교훈: 추측 위의 추측으로는 안 되고, 관측값에 닻을 내린 정량 관계 하나가 있어야 반증가능성이 시작된다.**

## A-4. G 의 러닝 / 중력자 질량 / 우주론 구속치 (수치 장부)

| 채널 | 현재 구속 | 출처 |
|---|---|---|
| Ġ/G (시간 변화) | (2 ± 7) × 10⁻¹³ /yr (LLR, Müller et al. 2007); (4 ± 9) × 10⁻¹³ /yr (Williams et al. 2004, arXiv:gr-qc/0411113) | PMC5253913 리뷰 |
| PPN γ − 1 | (2.1 ± 2.3) × 10⁻⁵ (Cassini Shapiro) | PMC5253913 |
| PPN β − 1 | (1.2 ± 1.1) × 10⁻⁴ (LLR + Cassini 결합) | arXiv:gr-qc/0411113 |
| 역제곱법칙 | 52 µm ~ 10⁸ m, 20자릿수 스케일에서 Yukawa 배제; LLR 스케일에서 새 힘은 중력의 10⁻¹⁰ 이하 | PMC5253913; PRL 124 101101 |
| 등가원리 (SEP) | Δ(M_G/M_I) = (−2.0 ± 2.0) × 10⁻¹³ (LLR+Eöt-Wash) | PMC5253913 |
| 중력자 질량 m_g | ≲ 9.5 × 10⁻²² eV (GW170817); LVK 결합은 태양계 구속보다 강함 | arXiv:2403.07682 리뷰; ResearchGate GW170817 테스트 |
| GW-광 속도차 | |c_g − c|/c ≲ 수 × 10⁻¹⁵ (GW170817/GRB170817A) | mlsmawfield.com 리뷰 요약 |
| 스케일 의존 G_eff | RR 비국소 중력 모델: G_eff(t) 변화 ~ H₀ 예측 → LLR 구속 (0.99 ± 1.06) × 10⁻³ H₀ 에 의해 **모델 사망** (스크리닝 없는 러닝 G 는 태양계에서 바로 죽는다는 실례) | dmgw.space thesis (Genoud-Prachex) |

**교훈**: 태양계/실험실에서 GR 이 10⁻¹³ 수준으로 확인된 이상, "러닝 G" 판별자는 스크리닝 메커니즘 없이는 즉사한다. 스크리닝(chameleon/symmetron/Vainshtein)은 CD 대수에서 도출된 적이 없는 추가 재료다.

---

# Part B — 설계 제안 (⚠️ 전부 SECONDARY_AI 설계; 정전 아님, 사용자 판정 대기)

## B-1. 판별자 후보 (a): ε(r) = 계수가 계산 가능한 무한 급수

**템플릿 (문헌에 존재)**: KK 탑의 뉴턴 퍼텐셜 보정은 ε(r) = Σ_n α_n e^{−m_n r}. 등간격 m_n = n/R 이면 Σ e^{−nr/R} = 1/(e^{r/R}−1) 로 닫히고, r ≪ R 에서 멱법칙(1/r) 보정 = 고차원 법칙 회복. 즉 "무한 급수 + 닫힌 형태 + 계수 전부 기하에서 계산 가능"은 KK 에서 이미 실현된 구조다.

**Claim B 버전 설계**: 깨짐 층 n (dim A_n = 2^{n+1} … 차원은 2의 거듭제곱) 마다 Yukawa 항 하나, m_n 과 α_n 을 대수 불변량(층별 zero-divisor 궤적 차원, Aut 차원 등)에서 도출. 로컬 OQ3 (ZD 필터레이션 → n_eff) 가 α_n 의 첫 후보.

**⚠️ 날것 경고 — 이 판별자는 양날의 검**: 깨짐 층이 기하급수 간격(m_n ∝ ρⁿ, 예: 차원 배가마다 질량 배가)을 가지면 Σ_n α_n e^{−ρⁿ m₀ r} 은 **log r 의 주기함수(log-periodic 진동)** 를 갖는다. 즉 무한 기하 탑은 *일반적으로* 진동형 ε(r) 를 만든다 — **이미 반증된 P-G02 (진동형 Z₂⁴-graded ε(r), Adelberger 대비 60배 진폭) 의 현상학을 재생성할 위험**. 16D 판이 "진동 진폭 0.06 > 상한 0.001"로 죽었는데(로컬 기록), 무한 탑판이 같은 진동을 낸다면 반증의 계승이다. 탈출 조건(둘 중 하나를 *도출*해야 함, 선택 금지):
- (i) 비기하 간격(등간격 또는 초기하)이 대수에서 강제됨을 보이거나,
- (ii) α_n 이 n 과 함께 충분히 빨리 감소해 진동 진폭이 실험 상한 이하임을 계산으로 보이거나.

**실험**: Eöt-Wash 계열 (현재 52 µm), 레비테이티드 옵토메카닉스/원자 간섭계 (µm 이하 목표), Yukawa (α, λ) 면적 스캔. 민감도: α ~ 10⁻³ 수준 @ λ ~ 10–100 µm 가 현재 경계(Adelberger 상한이 P-G02 를 죽인 바로 그 상한).

**선행 게이트 (실험 이전)**: m_n 과 α_n 의 대수 도출 = 로컬 MB1/MB2. 현재 0개 존재 (A-1 C4: 문헌 전체에 선례 없음).

## B-2. 판별자 후보 (b): 스케일에 따른 G 의 러닝

**설계**: 무한 탑의 스피시스 카운팅이 G_eff(r) = G(1 + f(r/R₀)) 형태의 러닝을 유도. 스피시스 논리(A-2.2)로 G_eff 가 컷오프 근처에서 강해지는 방향은 자연스러움.

**현실 점검**: A-4 표 — 태양계에서 Ġ/G ~ 10⁻¹³/yr, PPN 10⁻⁴–10⁻⁵, LLR Yukawa 10⁻¹⁰ 이하. 스크리닝 없는 러닝은 RR 모델처럼 즉사. **따라서 이 판별자를 쓰려면 스크리닝 메커니즘의 대수적 유래가 먼저 필요하며, 그런 후보는 CD 문헌에 전혀 없다 (dead end 로 기록).** 잔여 가능 영역은 (i) 플랑크 스케일 근방에서만 켜지는 러닝(= 사실상 관측 불가 = 반증 불가 후퇴, 채택 불가), (ii) 우주론 스케일 러닝(→ 후보 c 의 γ=1/14 과 연결, 아래 B-4).

## B-3. 판별자 후보 (c): species-scale 형태의 컷오프 — 날것: 이건 실험 판별자 이전에 남용 일관성 게이트다

**설계 + 날것 경고**: Dvali 종 한계(A-2.2)를 Claim B 에 적용하면 — 탑 상태가 전부 중력에 결합하고 유한 간격으로 *가볍게* 쌓이면 N 이 커져 Λ_QG = M_Pl/√N 이 붕괴. **무한 탑 + 유한 질량갭 ⇒ N = ∞ ⇒ 컷오프 → 0 ⇒ EFT 가 모든 스케일에서 사망.** 이건 관측 문제가 아니라 이론 남용 일관성 문제다. 따라서:
- **강제 조건 (도출 과제)**: Claim B 의 탑은 KK 처럼 *질량이 n 과 함께 증가*해야 한다. 그러면 컷오프 Λ 아래 상태 수 N(Λ) 이 유한하고, Λ_QG 예측이 나온다.
- 이 조건 자체가 판별자: "대수가 증가하는 질량 공식 m_n 을 강제하는가?" 가 NO 이면 Claim B 는 실험 이전에 종-논증으로 낙제.
- m_n 을 얻으면 컷오프 예측 → 가속기/우주선입자(10⁶–10⁹ GeV 형태면 dark dimension 식) 또는 플랑크 스케일(= 반증 불가 판정)로 갈림.

**현재 상태**: m_n 미존재 → 이 게이트 **미통과/미판정**. dead end 아니지만, 통과 조건이 명확한 최우선 이론 과제.

## B-4. 판별자 후보 (d): 중력자/액시온 탑 스펙트럼

**설계**: 탑의 유한 간격이 meV–eV 영역이면 (dark dimension 유사) — (i) LIGO/Virgo/ET 수정 분산관계 (m_g ≲ 10⁻²² eV 현재, ET 목표 ~10⁻²⁰ eV 이상 개선, arXiv:2405.13314), (ii) 탑 = 암흑물질 후보, (iii) 액시온 유사 탑은 haloscope (dark dimension 액시온 선례: f_a ~ 10⁹–10¹⁰ GeV 고정 → 실험 도달).
**스케일 근거 부재**: Claim B 는 탑 간격을 정할 관측 앵커(dark dimension 의 Λ 에 해당)가 없다. 간격이 자유면 이 판별자는 피팅. **앵커 후보는 우주상수 Λ, γ=1/14 우주론 잔여 주장(P-G03), 또는 대수 상수 — 셋 다 미확립. P-G03 은 로컬 기록상 "escape lane NARROWED_NOT_CLOSED" 의 마지막 잔여 경로** (`mb3_verdict_2026-05-19.json`).

## B-5. 종합: "회피적 후퇴" 판정 체크리스트 (설계, 부모/사용자 판정용)

Claim B 를 A-3 기준에 대조:

| # | 기준 | Claim B 현재 상태 | 판정 |
|---|---|---|---|
| 1 | 관측값에 고정된 탑 스케일 | 없음 (16D→∞ 이동은 movable gap 패턴과 형태상 동일) | ✗ |
| 2 | 대수 도출 질량 공식 m_n | 없음 (C4: 문헌 선례 0건) | ✗ |
| 3 | 계수 계산 가능 ε(r) 급수 | 형태 후볼만 존재 (OQ3), 유일성 정리 없음 | ✗ |
| 4 | 독립 관측 채널 ≥2 | 잔여 채널: P-G03 우주론 1개 (미결) | △ |
| 5 | 남용 일관성 (species bound) | 증가 질량 공식 미증명 → 게이트 미통과 | ✗ |

**결론 (날것)**: 현재 형태의 Claim B 는 물리학 기준으로 *반증 불가*이며, 이는 16D 판 반증 직후 무한 탑으로의 이동이 "측정 불가능한 형태로만 생존"한다는 로컬 판정문(`mb3_verdict_2026-05-19.json` honest_implication)과 정확히 일치한다. **물리가 되기 위한 최소 경로는 하나로 수렴한다: 대수 불변량에서 증가하는 질량 공식 m_n 을 도출하는 것** (B-3 게이트). 그것이 나오면 B-1(ε(r) 급수, 단 log-periodic 함정 주의), B-3(컷오프), B-4(스펙트럼)이 연쇄적으로 열리고, 진동 재생성 문제(B-1 경고)가 그 자리에서 바로 검증 가능하다. 그것이 나오지 않으면 Claim B 는 수학 구조(direct limit A_∞ 의 정리들)로는 남되, 물리 주장으로는 반증가능성을 회복할 경로가 보이지 않는다.

## B-6. Dead ends / 빈 결과 명단 (정직 보고 의무)

1. **무한 CD 탑 물리 문헌**: 웹 + 로컬 소스북(`THEORY/hypercomplex_physics/SOURCES.md` 200+ 항목) 모두에서, 16D 를 넘는 CD 층에서 중력/ε(r)/스펙트럼을 도출한 문헌 **0건**. 가장 가까운 Wilmot (arXiv:2505.11747) 은 오히려 고차원 불필요론.
2. **스크리닝 메커니즘의 대수적 유래**: 검색 결과 없음 → B-2 판별자 사실상 봉쇄.
3. **SDC 의 대수 탑 버전**: SDC 문헌의 탑은 전부 모듈라이 공간 거리의 탑(KK/스트링). "대수 깨짐 층 n ↔ 필드 공간 거리" 매핑 문헌 없음 — 이 매핑은 SYMPOSIUM-novel 가설이며 선례 인용 불가.
4. **γ=1/14 우주론**: 로컬 기록상 미검증 잔여 경로. 이번 리서치에서 외부 검증/반증 문헌 발견 못 함 (별도 사이클 필요 — 로컬 `mb3_cosmology_check_PG03.py` 존재하나 외부 대조 미완).
