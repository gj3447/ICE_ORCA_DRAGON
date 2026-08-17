# Claim B Computational Frontier — 3개 최저비용 결정 계산 설계 스펙 (2026-07-21)
> **성격**: DESIGN ONLY (실행 없음). 작성: computational-frontier 리서치 에이전트.
> **대상**: `oq-infinite-CD-tower-path-integral-gravity-untested-2026-05-19`.
> **방법론 고지**: §1-§3은 기록/문헌(검증 가능한 사실), §4-§6은 본 에이전트의 설계안【설계안】.

---

## 1. 기록: workbench 현재 역량 (파일 증거)

- **`cd_embedding.py`** (`ICE_ORCA_DRAGON/cd_embedding.py`): 재귀 CD 곱 `cd_multiply(a,b,n)` + 완전 곱셈표 `build_mult_table(n)` (float 텐서, n≤5 실용) + SVD 영공간 + 32D→16D 이중항 임베딩 분류기 (inherited/mixed/new). L.21-43, L.45-71.
- **`zd64_analysis.py`**: 64D를 **부호/인덱스 정수 표**(sign:int8, idx:int32, `cayley_dickson_mult_table(6)`)로 구성 — 밀집 float 표보다 훨씬 가벼움. C(63,2)=1953 쌍 SVD 스캔 구조 (L.17-83, L.250-277). 결과 JSON 없음(stdout만) — **64D ZD 카운트의 로컬 재현 산출물 부재**가 확인됨.
- **`queue_03_threshold_sensitivity_scan.py`**: n=4 고정, 7개 임계값 스윕 → decision tree → verdict JSON 프로토콜 (findingId/rootCause/caveats/confidence 필드). 레벨 일반화 없음 — `find_ZD_and_null(n=4)` 하드코딩 기본값.
- **`numerology_hidden_scan_v2_target_categories_2026-05-20.py`**: `ICE_PRIMITIVES`에 **ZD 카운트 n=4..8 (42/294/1518/6942/29886)이 이미 상수로 박혀 있음** (L.31-32). MC null + look-elsewhere Bonferroni + 3단 verdict(SIGNAL_GENUINE/WEAK/NUMEROLOGY_CONFIRMED) 프로토콜 확립.
- **`claimB_associator_growth_falsifier.py`**: **이미 실행됨**. 결합자 노름 = flat 2.0 (level 3/4/5, dim 8/16/32), 비영 결합자 수 168/1848/15960. KG `associator_mass_verification_result`(2026-02-02, 기각)와 독립 일치 (PROM_16_CLAIMB_PROOF_PATH_REPORT §4).

## 2. 기록/문헌: 세 후보 계산의 사전 상태 — 정직한 평가

**(a) ZD-count 점근 — 사실상 해결 완료(문헌). 신규 계산 불필요.**
OEIS A167654에 **닫힌 점화식이 존재**: v[4]=42, v[k]=2·v[k−1]+(2^{k−1}−1)(2^{k−1}−2) (Arndt, FXTbook 39.14절; oeis.org/A167654). 레벨 6,7,8 값 1518/6942/29886은 이미 OEIS + `ICE_PRIMITIVES` 양쪽에 존재. 확장(n=9..14): 124542, 509694, 2064894, 8317950, 33400830, 133885950.
점근: v_k ~ 2^{2k−1} (점화식 풀이: 특수해 계수 1/2). 전체 기저쌍 C(2^n−1,2) ~ 2^{2n−1} 대비 **ZD 밀도 → 1** (n=4: 42/105=0.400, n=5: 0.632, n=6: 0.777, n=7: 0.868, n=8: 0.923). 단, 이 카운트는 e_i+e_j형 "simple ZD"뿐 — 일반 ZD 다양체는 Moreno 1997 (arXiv:q-alg/9710013)이 모든 n≥4에 대해 대수적으로 기술.
→ **데드엔드 고지**: "스케일링 법칙이 나오는가?"라는 질문은 이미 답이 나온 질문이다. 나온 법칙(ZD 밀도 포화 → 1)은 PROM16 판독상 물리 내용에 대한 **부정 방향** 증거(ZD 폭발 = 노름 비곱셈성 악화, avenue3 메커니즘 유전). 새 계산을 설계할 여지는 카운트가 아니라 **null-dim 스펙트럼**(아래 C1)에만 있다.

**(b) 결합자 노름/조건수 점근 — 기저-노름 부분은 이미 반증. 잔여는 '분포' 통계뿐.**
`claimB_associator_growth_falsifier.py` 실행 기록: 기저 삼중쌍 노름 flat 2.0 — 사용자 직관의 정량 동력("무한히 심해지는 붕괴")에 NEGATIVE. **미측정 잔여**: (i) 임의 단위벡터 삼중쌍에 대한 ‖[x,y,z]‖/‖x‖‖y‖‖z‖ **분포**의 레벨 의존성, (ii) L_{e_i+e_j}의 영공간 차수(nullity) 분포의 레벨별 정규화 수렴 여부. Schafer 1954: flexibility+power-assoc은 ∀n 생존 → 발산하는 defect 계열이 아님.

**(c) 유한절단 예측의 안정화 — 프로토타입은 있으나 방법론 오염.**
`zd64_analysis.py`가 질량공식 재적합(32D α=5.75 → 64D 재피팅)의 프로토타입을 담고 있으나, (i) 결과 JSON 미저장, (ii) 베스트 트리플릿 탐색이 사후 탐색(post-hoc search) — `numerology_mc_judge` 계열 게이트 통과 불가 구조. Wilmot 2025(arXiv 2505.11747, 로컬 인용: PROM16 §1, scope-correction §1) 안정화 정리: n≥4에서 질적 포화 — 새 법칙붕괴 없음, 세는 양만 폭발. 즉 "예측이 안정화된다"는 것의 문헌상 예상 형태는 **'새 관측량 후보가 안 생긴다'는 쪽의 안정화**이지, 예측값 수렴이 아님.

## 3. 기록: 총괄 선행 verdict (재정리 금지, 인용만)

PROM_16_CLAIMB_PROOF_PATH_REPORT_2026-06-08.md: P(증명)≈0, P(2026-2031 falsifiable 진입)≈0.02-0.05; FATAL 장애 4건(측도 비존재, associator obstruction, 전제 오류, ε(r) 유전 실패). 아래 설계안들은 이 verdict를 뒤집기 위한 것이 아니라, **"무한 tower에 잔여 계산 가능한 구별 신호가 있는가"를 최저비용으로 봉인(seal)하기 위한 것**이다. 어느 브랜치가 나와도 연구 프로그램이 종결되도록 결정 기준을 사전 고정한다.

---

## 4. 【설계안 C1】 ZD nullity 스펙트럼 스캔 — 레벨 6,7(,8)

**질문**: simple ZD의 *개수*는 문헌 해결이지만, 각 쌍의 영공간 차수(nullity) **분포**는 레벨이 오를수록 정규화 후 수렴하는가, 계속 재편되는가. 수렴하면 극한 대상 A_∞에 "분포형 관측량 후보"가 존재. 계속 재편되면 극한 물리 부재의 구조적 증거 추가.

**스크립트 개요** (`claimB_zd_nullity_spectrum.py` 신규, `zd64_analysis.py` 표 구조 재사용):
```
1. sign,idx = cayley_dickson_mult_table(n)          # zd64_analysis.py L.17 재사용, n∈{6,7} (,8)
2. for (i,j) in combinations(range(1,2^n),2):
     L = build_left_mult_matrix(sign,idx,2^n, e_i+e_j)   # L.85 재사용 (열당 ±1 두 개 — 희소)
     nd = nullity via SVD (n≤7) 또는 희소/그래프 랭크 (n=8)
3. 출력: {n: {nullity: count}}, 정규화 분포 p_n(k)=count/C(2^n-1,2),
   쌍별 TV-distance TV(p_n, p_{n-1}) (공통 support로 임베딩 후)
4. decision tree + verdict JSON (queue_03의 findingId 프로토콜 상속)
```
**입력**: n 목록만. 외부 데이터 없음.
**결정 기준**:
- PROGRESSIVE 신호: TV(p_n,p_{n+1})가 n=5→6→7에서 단조감소 + nullity 분포 형(예: 최빈 nullity/2^n)이 수렴 → "극한 분포 존재" 후보, A_∞ 관측량 정식화 연구 착수 정당화.
- KILL: TV가 정체/증가, 또는 분포 형이 레벨마다 재편 → 극한에 안정 분포 부재, '빈 형식주의' 방향 추가 봉인.
- **사전등록 필요**: "수렴"의 임계(예: TV<0.05)와 분포 요약 통계를 sha256 커밋 후 실행 (MB4 프로토콜 상속).
**런타임 추정**: n=6: 1953 SVD(64×64) ≈ 수 초. n=7: 8128 SVD(128×128) ≈ 수 분. n=8: 32385 SVD(256×256) 밀집 ≈ 수 시간 — L이 열당 2비대각 희소이므로 희소 랭크(또는 LᵀL 블록 구조 이용)로 분 단위 가능. **총: 수 분~1시간 (n=8 제외 시).**
**정직성 경고**: nullity 분포 수렴이 나와도 그것은 "물리 관측량"이 아니라 "수학적 극한 통계"다. 물리 연결은 avenue3 verdict(연속 관측량 창발 메커니즘 부재, `avenue3_decisive_test_2026-06-05/RESULTS.md`)가 이미 구조적으로 차단 — C1의 PROGRESSIVE 브랜치는 수학 결과로만 가치가 있음.

## 5. 【설계안 C2】 랜덤 삼중쌍 결합자 분포 + defect 계열 측정 — 레벨 4-7

**질문**: 기저 노름은 flat 2.0으로 확정(기록). 그러나 **연속 원소**에 대한 결합자 비율 r(x,y,z)=‖[x,y,z]‖/(‖x‖‖y‖‖z‖)의 분포는 레벨 함수로서 어떻게 거동하는가 — 평균/분산이 수렴(포화)하는가, 단조 성장하는가. 이것이 "붕괴가 심화되는가"의 마지막 미측정 정량 잔여.

**스크립트 개요** (`claimB_associator_distribution.py` 신규):
```
1. sign/idx 표 (C1과 공유). 밀집 벡터 곱은 표 조회 기반 배치 곱셈 (numpy take/부호 곱).
2. for n in {4,5,6,7}: 시드 고정 (random.seed(42) 관례 상속)
     M=10000 삼중쌍: x,y,z ~ 단위구 (정규화 가우시안)
     r_k = ‖[x,y,z]‖/(‖x‖‖y‖‖z‖)  # 결합자 2회 곱셈
     추가 defect: flexibility 결함 ‖(xy)x−x(yx)‖, power-assoc 결함 ‖(xx)x−x(xx)‖
     (Schafer 생존 항등식 — 이론상 정확히 0이어야 함 → 부동소수 검증기로도 사용)
3. 출력: 레벨별 r의 평균/중앙/95백분위/최대 + KS-검정(분포 형 비교) + JSON
```
**입력**: n 목록, M, 시드.
**결정 기준** (사전등록 필수):
- PROGRESSIVE: 평균 r이 레벨에 대해 **단조 감소하지 않고 유의미한 양의 값으로 포화**하며 분포 형이 수렴 → "극한에서 비자명 결합자 통계 존재" = A_∞가 빈 대수가 아니라는 첫 계산 신호.
- KILL-A (성장): 평균 r이 지수/멱급수 성장 → path-integral 가중 수렴에 자유 파라미터 강제 (PROM16 §1 논리 재현, 기존 기록과 다른 경로로 kill).
- KILL-B (붕괴): 평균 r→0 급감 → 높은 레벨이 "거의 결합적"으로 퇴화, 무한 history 기여 소멸.
- KILL-C (재편): 평균은 비슷한데 분포 형(KS)이 레벨마다 유의하게 변함 → 안정 극한 통계 부재.
**런타임 추정**: 곱셈 1회 비용 ~ O(4^n) MAC. n=7, M=10⁴, 결합자당 곱 2회: 2·16384·10⁴ ≈ 3.3×10⁸ MAC ×(4레벨 누적) — numpy 배치화 시 **수 분~30분**. 가장 싼 결정 계산 후보 1순위.
**검증 내장**: flexibility/power-assoc defect가 1e-12 이하로 나오지 않으면 구현 버그로 판정 (Schafer 정리를 부동소수 오라클로 사용 — 결과 신뢰도의 자기 검증).

## 6. 【설계안 C3】 유한절단 예측 안정성 프로토콜 — 사전등록형

**질문**: 레벨-n 절단에서 정의되는 **사전등록된** 예측 족(family)이 n=5→6→7에서 코시 수렴하는가, 계속 바뀌는가. 이것이 "극한 물리 존재 여부"의 직접 시험.

**스크립트 개요** (`claimB_truncation_stability.py` 신규 + prereg JSON):
```
1. 사전등록 (sha256, MB4 프로토콜): 예측 족 P_n = {관측량 후보들}을 '레벨에 무관한 정의'로 고정.
   허용 정의 예: (i) ZD 쌍의 inherited/mixed/new 비율 (cd_embedding.py L.514-537 분류기의 레벨 일반화),
   (ii) 최빈 nullity 값, (iii) C2의 r 평균, (iv) queue_03 임계 스윕의 성공률 곡선 형상.
   금지: 사후 베스트피팅(zd64 질량공식식) — numerology_mc_judge 통과 불가로 기록상 반증됨.
2. 각 n∈{5,6,7}에 대해 P_n 계산 (C1/C2 산출물 재사용, 신규 계산 최소).
3. 수렴 판정: |P_7−P_6| vs |P_6−P_5| 비교 + 외삽(리처드슨)으로 P_∞ 추정, 불확도 산출.
4. verdict JSON: CONVERGED(극한 예측 존재) / DRIFTING(극한 물리 부재) / INSUFFICIENT_LEVELS.
```
**입력**: 사전등록 JSON + C1/C2 산출물.
**결정 기준**:
- PROGRESSIVE: 차분이 감소(코시 거동)하고 외삽 P_∞가 수치적으로 안정 → Claim B 최초의 *계산 가능한* 극한 예측. 단, 그 예측이 중력 관측량과 연결되려면 별도 도출 경로 필요(avenue3 장벽 그대로).
- KILL: 차분 정체/증가(DRIFTING) → "유한 절단 예측이 계속 바뀐다 = 극한 물리 없음"을 사전등록 하에 확정.
**런타임 추정**: C1/C2 산출 재사용 시 **수 분**. inherited/new 분류기 일반화는 임베딩 프로젝터 계산이 O(쌍수 × 차원³) — n=7에서 수십 분 가능.
**방법론 필수 조항**: C3의 모든 출력은 `numerology_mc_judge_v3_abc.py` 게이트를 통과해야 SIGNAL 인정 (Claim A가 Koide Q=2/3 P=1.000으로 전락한 전철 — PROM16 §4 명시).

---

## 7. 우선순위와 총비용【설계안】

| 순위 | 스펙 | 비용 | 결정력 | 비고 |
|---|---|---|---|---|
| 1 | C2 결합자 분포 | 수 분~30분 | 높음 | 마지막 미측정 정량 잔여; self-validating 내장 |
| 2 | C1 nullity 스펙트럼 | 수 분~1시간 | 중간 | 카운트는 문헌 해결; 분포만 신규 |
| 3 | C3 안정성 프로토콜 | 수 분(+재사용) | 최고(정의상) | 사전등록 게이트가 진짜 작업; 계산은 부산물 |

권고 순서: **C2 → C1 → C3**. C2가 KILL-A/B/C 어느 쪽이든 C3의 예측 족에서 r 항목이 즉시 확정되므로 순차 비용이 최소.

## 8. 정직한 종합 (기록 기반 전망)

- (a)는 **신규 계산 불필요**(점화식 + 밀도→1 포화 이미 확정) — 후보로서 데드엔드.
- (b)의 기저 부분은 **이미 반증됨**(flat 2.0, 2026-06-08 + 2026-02-02 독립 일치). C2는 연속 분포라는 좁은 잔여만 시험.
- 세 계산의 PROGRESSIVE 브랜치가 나올 사전 확률은 낮음(PROM16: 0.02-0.05). 그러나 그것이 이 설계의 목적이다: **어느 브랜치든 Claim B의 계산 측 open-status를 봉인**할 수 있다.
- 가장 큰 실질 장벽은 계산이 아니라 **avenue3 verdict**(CD doubling은 강제 정수 {2,3,7,14}만, 연속 관측량 메커니즘 부재) — 어떤 스펙트럼/분포 수렴이 나와도 중력 연속 관측량으로의 연결은 별도 breakthrough 필요. 이 점을 PROGRESSIVE 판독의 caveat로 모든 verdict JSON에 명시해야 함.
