# Claim B Overnight Loop Protocol (2026-07-24)

루프 목적: Claim B(무한 CD tower 경로적분 = 중력)의 계산 측 open status를
어느 브랜치로든 **봉인**한다. 반전이 목적이 아니라 판정이 목적이다.

근거 스펙: [`CLAIMB_COMPUTATIONAL_FRONTIER_DESIGN_2026-07-21.md`](CLAIMB_COMPUTATIONAL_FRONTIER_DESIGN_2026-07-21.md)
정전 제약: [`ICE_WORKBENCH_REFRAME_2026-05-18.md`](../docs/decisions/ICE_WORKBENCH_REFRAME_2026-05-18.md) (3-layer 공시),
MB4 sha256 사전등록 프로토콜, numerology_mc_judge 게이트.

## 절대 규칙

1. 한 실행(run)은 정확히 한 stage만 수행한다. STATE.md를 읽고 갱신한다.
2. 결정 계산(decisive computation)은 **실행 전에** 임계값·판정기준을 sha256으로
   사전등록한다. 사후 피팅 절대 금지. 결과가 기준과 다륵나 그대로 기록한다.
3. 어떤 결과도 "ICE가 물리를 예측한다"로 서술하지 않는다 (3-layer 공시).
   L1 대수 / L2-L3 물리벨트 / 신화층을 명시 분리한다.
4. PROGRESSIVE 브랜치가 나와도 avenue3 장벽(연속 관측량 창발 메커니즘 부재)은
   별도 breakthrough가 필요하다는 caveat를 항상 동반한다.
5. 재현: 각 계산은 2회 실행해 byte-identical 여부를 기록한다.

## Stages

- S_setup: 디자인 스펙 확인, C1/C2/C3 임계값·판정기준을 PREREG JSON으로 작성,
  sha256 커밋 (`prereg_claimB_loop_20260724.json` + `.sha256`).
- S_c2: 결합자 분포 측정 (`claimB_associator_distribution.py` 작성·실행).
  레벨 4–7, M=10^4 랜덤 단위 삼중쌍, r=‖[x,y,z]‖/‖x‖‖y‖‖z‖ 분포.
  판정: 포화+분포 수렴=PROGRESSIVE / 성장=KILL-A / r→0=KILL-B / 형 재편(KS)=KILL-C.
  결과: `results_c2_associator_distribution.json`.
- S_c1: ZD nullity 스펙트럼 (`claimB_zd_nullity_spectrum.py` 작성·실행).
  레벨 6,7 simple-ZD 쌍 영공간 차수 분포, 레벨 간 TV-distance.
  판정: TV 단조감소+형 수렴=극한 분포 후보 / 정체·증가=KILL.
  결과: `results_c1_zd_nullity_spectrum.json`.
- S_c3: 절단 안정화 (`claimB_truncation_stability.py` 작성·실행).
  사전등록된 예측족 P_n을 레벨 5,6,7에서 계산, 코시 수렴 판정.
  판정: CONVERGED / DRIFTING(극한 물리 부재) / INSUFFICIENT_LEVELS.
  결과: `results_c3_truncation_stability.json`.
- S_s0: S0 falsifiability scaffold — `∫D[γ]e^{iS[γ]}` 1쪽 LaTeX 문서
  (`S0_FALSIFIABILITY_SCAFFOLD_2026-07-24.md`). 측도 부재·associator obstruction이
  정확히 어느 항에서 터지는지 명시. "정확히 무엇이 죽었는지"의 정전화.
- S_report: 종합 판정 보고 (`CLAIMB_LOOP_FINAL_REPORT_2026-07-24.md`).
  C1/C2/C3 verdict 통합, 전체 브랜치(PROGRESSIVE_SEALED / KILL_SEALED) 선언,
  다음 게이트(진전 시: m_n 강제 도출 시도 / 봉인 시: math-only archival 권고).
- S_done: 아무것도 하지 않고 즉시 종료.

## STATE.md 형식

```
stage: S_setup | S_c2 | S_c1 | S_c3 | S_s0 | S_report | S_done
history: (각 실행 1줄: 시각, stage, 결과 요약, 산출물 경로)
```
