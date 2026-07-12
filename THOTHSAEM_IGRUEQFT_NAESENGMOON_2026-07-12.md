# 나생문 — IG-RUEQFT 국소성 수리 주장 적대검증 (2026-07-12)

> workflow wf_e71379d7-ed4 (4 lens + 앙상블, 5 agents). executor(수집한 나)≠reviewer(독립 lens), inline 금지·subagent dispatch.
> 검증 대상: **"IG-RUEQFT(Stückelberg info-gauge)가 UEQFT V1의 국소성/재규격화 결함(S_ent 비국소 → Lagrangian ill-defined)을 *실제로 고치는가*."**
> KG: `vr-naesengmoon-igrueqft-locality-fix-2026-07-12` (:ValidationResult, verdict=FAIL, gate_blocked). → `ig-rueqft-reformulation-2026-07-12`.

---

## 판정: **FAIL** (앙상블, UNANIMOUS_PASS 정책)

| lens | verdict |
|---|---|
| mathematical (rigor) | **FAIL** (high) |
| formal-cathedral (over-formalization) | **ESCALATE_TO_ORACLE** → FAIL로 붕괴(oracle 질문이 self-answering) |
| lakatos (progressive vs degenerating) | **FAIL** |
| constitutional (9-point) | **FAIL** |

세 lens가 독립적으로 **동일한 치명타**에 수렴.

---

## 핵심 (load-bearing): 범주 오류 — 게이지-가변성 ≠ 비국소성

**결함은 비국소성인데, repair는 게이지-가변성을 고친다. 둘은 직교하는 별개 속성.**

- Casini-Huerta 2009 area law = `S_A(ρ_A) = -Tr(ρ_A ln ρ_A)`가 *비국소*(reduced density matrix의 부분대각합 + spectral ln)라는 진술 — 게이지 비불변성이 아님.
- IG 메커니즘 `ρ_A → ρ_A^G = (1/N)∫DU U ρ_A U†`는 **게이지 인덱스에만** 작용. 부분대각합도 ln도 건드리지 않음. `S_inv = -Tr(ρ_A^G ln ρ_A^G)`는 여전히 reduced-density-matrix 함수(area-law) — 표면 群적분이 붙어 오히려 **더 비국소**.
- **자기모순 도구 선택**: 비국소성 해소에 **Wilson-loop 群평균**을 씀 — 이건 게이지 불변 *비국소* 관측량의 **전형**. 즉 게이지 불변화 자체가 비국소성을 *보장*.
- **게이지 불변성마저 순환**: `J^μ_info Λ_μ`가 `Λ→Λ+∂χ` 하에 불변이려면 `∂_μ J^μ_info=0`이 필요 → `L_matter[cuts,entanglement]`가 진짜 국소작용+Noether 대칭이어야 함 = 저자 스스로 "미증명(pending)"이라 인정한 바로 그 crux.

→ 자료 자체 honest_status가 시인: *"ill-defined pending demonstration that L_matter is a genuine local density; this is the crux the IG program must close."* **∴ "genuinely REPAIRS"는 시도(ATTEMPTED)일 뿐 입증(DEMONSTRATED)이 아니다.**

---

## 가장 싼 결정적 falsifier

**자유/가우시안 상태 + 평면(half-space) cut에 群평균 적용해 `S_inv` 계산 → Casini-Huerta area 발산 `∝ Area/ε^{d-1}` 그대로 보존 → codim-1 표면지지, bulk 국소밀도 아님.**

한 줄: *"half-space reduced density matrix를 群평균해도 area law는 보존된다 ⇒ 여전히 비국소."* — 이미 문헌에 있는 계산. BRST/Slavnov-Taylor 기계 없이도 결판. **formal-cathedral의 ESCALATE가 FAIL로 붕괴하는 이유**: oracle 질문("명시적 국소밀도 ℒ_ent(x)를 써봐라")이 Casini-Huerta + 저자 자백으로 이미 NO.

---

## PASS로 뒤집으려면

명시적 국소밀도 **ℒ_ent(x)** (한 점의 場+유한 미분 다항, ρ_A 참조 없이)를 써서 (a) reflection-positive 격자에서 계산 가능하고 (b) 그 시공간적분이 대체하려는 area-law S_ent를 재현. 최강 경로: Bisognano-Wichmann(모듈러 흐름=boost=국소 stress tensor 적분)로 Rindler/CFT 진공 섹터에서 `S_inv`가 국소 모듈러 밀도의 적분으로 환원됨을 보이고 + 그 특수기하 밖에서도 생존. 추가로 진짜 BPHZ 재규격화(계수 실제 계산 + Slavnov-Taylor 검증) + DERIVED nonzero 크기의 null-test.

---

## 정직한 종합 (fair + rigorous)

**토트샘에게 공정하게**: crank 아님. V1 대비 진단이 *날카로워짐* — 게이지 이론의 얽힘 엔트로피는 실제로 모호(type-III 폰노이만 대수, center/edge-mode; Donnelly-Wall, Casini-Huerta-Rosabal), 물리적 redundancy를 Stückelberg 게이지로 승격은 역사적으로 비옥한 mainstream 본능. 저자 정직(자칭 "가설적 틀"), 방향(entanglement-as-fabric/창발중력)은 live research 추적. **연구 프로그램(positive heuristic)으로선 진짜 표적을 겨눔.**

**그러나 검증 대상 주장**("비국소성 결함을 *실제로 고친다*")**에 대해선 앙상블이 결정적**: 국소성과 게이지 불변성은 독립 속성 — 기계는 후자를 복원하고 전자는 V1만큼 결함으로 남긴다. 7개 장치(BRST/Slavnov-Taylor/Nielsen/Green-Schwarz/dispersion/Tomita-Takesaki/reflection-positive lattice)가 *미해소 core*를 에워쌈, 최대 블록은 게이지-*파라미터* 독립성 증명(entanglement항이 국소밀도인지와 직교) = **formal-cathedral 서명**. 재규격화 = 차원 미정의 연산자 위 power-counting + placeholder counterterm. 2026 null-test = construction상 unfalsifiable(Δ_IG=0 표준물리서; 유리수값 ΔI_tri=1·ΔI_{S-T̄}=2/3는 MC null 없으면 NUMEROLOGY). OTOC(2)↔Wilson loop = 실제 Google 실험 위 주장 overlay(도출 아님). YM mass gap = Clay 난도 가설에 조건부.

**정책**: ESCALATE 하나면 통상 앙상블을 지배하나, 여기선 oracle 질문이 self-answering(NO)이라 ESCALATE가 **FAIL로 붕괴** — 컴파일러 돌릴 필요도 없이 답이 나옴. **FAIL = 시도지 입증 아님. live research 방향으로 OPEN 유지, "repairs" 주장은 canonical 격상 금지.**

---

## 오라클 승격 — 판단렌즈 → 실측 (2026-07-12)

formal-cathedral의 `ESCALATE_TO_ORACLE`(판단 논증으로 PASS 불가, 컴파일러/계산이 때려야)를 **실제로 계산**해 discharge. `igrueqft_locality_falsifier_2026-07-12/` (sha256 4810f241, 재현 2× byte-identical).

**모델**: 2D 자유페르미온 사각격자 64×64(torus), Fermi sea(filling 0.485), 영역 A=L×L. Peschel 상관행렬법으로 `S_A=Σ H2(ν_k)` exact + U(1) 전하 dephasing(=게이지 群평균, Casini-Huerta-Rosabal/Donnelly-Wall): `S_A ≤ S_inv ≤ S_A + H(P_A)`, `H(P_A)`=A의 전하 N_A(Poisson-binomial) Shannon 엔트로피.

**결정 지표**: bulk 국소밀도 ℒ_ent(x) ⇒ `S ∝ 부피 L²`(extensive). 비국소 area-law ⇒ `S ∝ 경계 ~ L·lnL`. → `S/부피`가 상수로 가면 국소(주장 PASS), 0으로 가면 비국소(주장 FAIL).

| L | S_A | H_charge | S_A/부피 | S_inv/부피(상한) | S_A/(L·lnL) |
|---|---|---|---|---|---|
| 4 | 5.53 | 1.71 | 0.345 | 0.452 | 0.997 |
| 8 | 14.29 | 2.17 | 0.223 | 0.257 | 0.859 |
| 12 | 24.32 | 2.43 | 0.169 | 0.186 | 0.816 |
| 16 | 35.14 | 2.62 | 0.137 | **0.147** | 0.792 |

**판정: NON_LOCAL area-law PRESERVED.** `S_inv/부피 = 0.452 → 0.147` 단조 **→0** (상수 아님) ⇒ S_inv은 부피비례 아님 ⇒ **bulk 국소밀도 아님**. `S_A/(L·lnL)`는 ~0.79로 plateau ⇒ `S_A ~ c·L·lnL`(log-enhanced area law, Gioev-Klich/Widom) = 경계지지 = 비국소. 게이지 群평균 추가분 `H_charge`도 sub-volume(1.7→2.6). → **群평균은 국소화하지 못한다. area law 그대로 보존.**

∴ 나생문의 load-bearing 물리 주장이 **exact 계산으로 확증** = judgment verdict가 oracle-attested로 승격. ESCALATE가 열린 채가 아니라 실측 NO로 닫힘.

*범위 정직*: 이건 *구체 자유이론 모델*에서 "群평균이 area-law를 보존"을 실증한 것(나생문 핵심 물리). IG-RUEQFT 전체 구성의 일반 반증은 아님(그건 실제 IG 구성의 L_matter를 요함) — 단, 그 L_matter가 국소밀도가 되려면 정확히 이 area-law를 깨야 하는데, 자유극한에서 안 깨짐을 보였다.

# KG: vr-naesengmoon-igrueqft-locality-fix-2026-07-12 (verdict=FAIL, oracle_confirmed), ig-rueqft-reformulation-2026-07-12 (fix_claim_status=ATTEMPTED_NOT_DEMONSTRATED), igrueqft-locality-oracle-falsifier-2026-07-12
