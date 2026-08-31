# ICE killed-route 실행 차단기 — Ragnarok 역사 기록

> **현재 권한:** `EXECUTION_CONTAINMENT_ONLY`
> **운영 상태:** `BOUNDED_SCIENCE_OPEN_KILLED_RECONCILIATION_CLOSED`
> **발효:** 2026-08-23
> **연구 방법 정본:** [`ICE_LEAN_RESEARCH_RULES_2026-08-31.md`](ICE_LEAN_RESEARCH_RULES_2026-08-31.md)
> **비권한:** 이 문서는 새 연구 계약, 재개 절차, 과학적 evidence, Gate 1 no-go, 물리학 주장 또는
> TOE 판정이 아니다.

이 문서가 현재 강제하는 것은 좁은 실행 안전 경계뿐이다.

- Phase 51--56 saved-backend/reconstructed-launch reconciliation과 그 이름 바꾼 후손은 닫는다.
- 새 numbered core Phase와 이미 소진된 세 Gate-1 runner 계보는 닫는다.
- 새 번호 없는 core 계산은 clean committed runner를 `./ice run`으로 실행하며 120초,
  stdout/stderr 각 262,144 bytes, 변경 artifact 12개·합계 1,000,000 bytes의 공통 상한을 쓴다.
- path traversal, absolute path, dirty·untracked core와 직접 Python 우회는 허용하지 않는다.

과거 one-shot authorization, receipt, consumed window, 2026-08-30 검토일, 재개 checklist와 이관
상세는 모두 **비운영 역사 provenance**다. 새 계산은 이를 복제하지 않으며 per-window receipt,
대형 null matrix, 전 check-ID snapshot, 수동 repro/KG 등록을 요구하지 않는다. 현재 상태는
`./ice status`, 원문 이력은 `./ice status --history`로 읽는다. 세 과거 window의 정본은 다음과
같다.

- [`ICE_GATE1_BOUNDED_RESUME_2026-08-25.md`](ICE_GATE1_BOUNDED_RESUME_2026-08-25.md)
- [`ICE_GATE1_SCALAR_SOURCE_LINK_BOUNDED_RESUME_2026-08-26.md`](ICE_GATE1_SCALAR_SOURCE_LINK_BOUNDED_RESUME_2026-08-26.md)
- [`ICE_GATE1_SCALAR_ZERO_LAPSE_BOUNDED_RESUME_2026-08-26.md`](ICE_GATE1_SCALAR_ZERO_LAPSE_BOUNDED_RESUME_2026-08-26.md)

## 활성 실행 결정

현재 판정은 다음 세 문장을 동시에 보존한다.

```text
RAGNAROK_PATTERN_PRESENT
SCIENTIFIC_PROGRESS_PARTIAL
CORE_GATE_NOT_CLOSED
```

Phase 51의 CSE/non-CSE RHS mismatch에서 Phase 52 dtype/evaluator repair, Phase 53 repaired
replay, Phase 54 schedule attribution, Phase 55 reconstructed trajectory, Phase 56
launch/provenance conditioning으로 이어진 **저장 backend 및 재구성 launch reconciliation 경로**는
Phase 56 종결 진단과 함께 `KILL`한다. 실패 원인을 더 작은 evaluator·dtype·solver·residual·provenance
Phase로 다시 낳는 자동 연장은 허용하지 않는다.

- 운영 상태는 `BOUNDED_SCIENCE_OPEN_KILLED_RECONCILIATION_CLOSED`다. 새 번호 없는 계산은
  공통 bounded runtime에서 열리고, killed reconciliation containment는 계속 active다.
- Phase 56 terminal closeout과 세 과거 Gate-1 one-shot root 및 이름 붙인 후손은 소진된 역사
  경로로 분류해 재실행하지 않는다. hash, receipt, 결과와 실패 상세는 `--history`와 위 전용
  결정문에만 둔다.
- 정확히 동결된 Phase 11–50 실행체는 역사 검산용 allowlist로 허용한다. KILL 범위인 Phase
  51–55 재실행, Phase 56 변종과 모든 새 numbered descendant는 `./ice run`과 `./ice repro`에서
  `RESEARCH_PHASE_PAUSED`로 거부한다. 새 번호 없는 core 실행체는 위 공통 상한 아래 허용한다.
- Phase 56 runner와 결과 identity는 종결 provenance로 보존하지만 더는 실행 allowlist가 아니다.
  복합 파일명이나 낮은 Phase 번호 재사용으로 우회할 수 없다.
- 허용된 41개 역사 runner는 SHA-256까지 고정한다. core 디렉터리에 tracked
  수정이나 untracked 파일이 하나라도 있으면 실행 전에 `RESEARCH_CORE_DIRTY`, 허용 경로의 bytes가
  다르면 `RESEARCH_RUNNER_HASH_MISMATCH`로 닫는다. `./`, `..`, 역슬래시, absolute path로 core
  판정을 우회할 수 없고 workspace 밖으로 나가는 경로는 거부한다.
- 직접 `python ...` 실행이나 다른 실행기 우회는 사용하지 않는다. 새 연구도 `./ice run`의
  Effect-scoped timeout, output 및 artifact 검사를 통과한다.
- Phase 56 결과와 무관하게 `next_phase = null`이다. full replay, Phase 57, threshold 완화 또는
  같은 reconciliation의 새 이름 붙이기는 자동으로 열리지 않는다.

현재 정본 상태는 `./ice status`와 `./ice status --json`으로 읽는다. 아래 역사 상세와 기존 v3
machine record는 `./ice status --history` 및 `./ice status --history --json`으로 읽는다. 과거
2026-08-30 검토일은 만료된 provenance이며 현재 계산을 기다리게 하거나 route를 다시 열지 않는다.

## 역사적 closeout — 운영 규칙 아님

### Phase 56 terminal closeout

2026-08-23T19:32:42Z authoritative run과 19:36:16Z 독립 재현은 모두 exit `0`이었고 stdout
321,195 bytes가 byte-identical했다. canonical result는 321,183 bytes, SHA-256
`c9163319405ed4ec696076f7516c32fa8af290794a2e1cc4762090812f693d27`, self-excluding digest
`56c567bf60fde04b7d68ab9a5c394faaf08e73e43fe1db36b082ba58e3c010b2`다.

```text
run_status = VALID_RUN
classification = P56_FRESH_PHASE53_ALGORITHM_LAUNCH_RECOVERS_SAVED_LAMBDA_HALF_TARGET
root calls = 1
solve_ivp calls = 8
forbidden root/replay calls = 0
next_phase = null
```

두 solver profile에서 P50-center 두 corner는 residual gate NONPASS를 유지했고 fresh-center 두
corner는 저장 endpoint/residual target을 회복했다. 이 분류는 single-root bounded diagnostic의
과학적 기록일 뿐 실행 권한이 아니다. `full_replay_authorized=false`, `phase57_authorized=false`,
`continuation_route=KILL`은 그대로다. Gate 1은 `OPEN_PARTIAL_PROGRESS`, global promotion은
`PROHIBITED`, physics/TOE claim은 `null`이다.

### Gate-1 scalar source-link terminal result

2026-08-26T04:12:08Z exact command는 2.791651251초에 exit `0`으로 끝났다. canonical result는
11,117 bytes, SHA-256
`ad7c7f9ccf79047d0994eea3667b07c1fbb9795e7187c9730c5c6d819956f243`, self-field 제외 digest는
`a3e9f17e7a5d0838cd295427bd161aabb2260b9d15f32b3364b1794ad997d04b`다.

```text
run_status                 = VALID_RUN
classification             = GATE1_NONZERO_LAPSE_SCALAR_SOURCE_LINK_MATCHES_ZERO_LAPSE_DISTRIBUTION_OPEN
exact checks               = 16/16 PASS
analytic theorem guards    = 3/3 separately reviewed
numerical/root/ODE calls   = 0/0/0
nonzero-arm scalar link    = KEEP, orientation +1
zero-lapse full q pairing  = OPEN
phase-lock selected        = false
Gate 1                     = OPEN_PARTIAL_PROGRESS
global promotion           = PROHIBITED
automatic_next             = null
```

이는 새로 선언한 fixed-\(a\), \(m=2\) scalar control의 비영 lapse-arm source link만 지지한다.
\(N=0\)을 포함한 full \(q\)-paired distribution, physical original/full joint/BFV cycle, global
coefficient와 physics/TOE claim은 얻지 않았다. 독립 읽기 전용 감사가 payload digest, momentum
prefactor와 두 arm 위상, end coefficients, 16개 executable exact result entry와 세 analytic guard를 재검산했고 결론을
바꾸지 않았다. runner는 재실행하지 않았다.

## 과학적 경계

KILL의 적용 대상은 위의 방법 경로이며 Gate 1이나 CPT × Temporal-Folded SUSY 전체가 아니다.

- Gate 1은 계속 `OPEN_PARTIAL_PROGRESS`다.
- `global_n_sigma`, `physical_original_cycle`, `physics_claim` 등 미계산 출력은 계속 `null`이다.
- `global_promotion = PROHIBITED`다.
- Phase 39–41의 bounded local intersection, Phase 49의 pinned-platform evaluator, Phase 50의
  sampled \(m=4\to5\) saddle bridge와 각 실패·`INCONCLUSIVE`·`NONPASS` 기록을 재분류하지 않는다.
- 사용자 원문 spec과 서사 층을 지우지 않는다. 계산 워크벤치의 증거 층과 분리해 보존한다.

따라서 운영상의 `continuation_route = KILL`과 과학상의 `scientific_route = OPEN`은 모순이
아니다. 현재 증거가 core를 닫지 못했다는 사실과, 같은 채무 하네스가 계속 Phase를 생성하지
못하게 하는 결정은 서로 다른 타입이다.

## Numbered route 재개 절차 없음

이 문서는 새 numbered Phase나 과거 one-shot 계보를 위한 재개 checklist를 제공하지 않는다.
2026-08-30 날짜, 사전 serialization, full census, 결과별 decision table과 대형 null matrix는 새
작업의 대기 조건이 아니다. 미래에 전혀 다른 numbered programme가 필요해지면 사용자가 그때
별도 범위와 권한을 정해야 하며, 이 문서나 한 계산의 출력이 그 결정을 자동 생성하지 않는다.

Phase 53이 저장하지 않은 authoritative saddle·factor·launch·initial-state bytes가 독립 출처에서
hash 인증된 형태로 회수되는 경우에도 검토 가능한 것은 별도 승인된 **비번호 archival
reproduction audit**뿐이다. 그것은 killed route, 다음 Phase 또는 물리 승격을 다시 열지 않는다.

## 역사적 원격 전송 차단과 승인된 수습

읽기 전용 검사에서 다음 사실을 확인했다.

| 항목 | 값 |
|---|---|
| tracked path | `cpt_temporal_folded_susy/PHASE44_M4_NUMPY64_LOCAL_RHS_ERROR_DECOMPOSITION_RESULT.json` |
| Git blob | `b7d32b0547967d39ee69decb4e186fc8b9244c8a` |
| blob bytes | `529,370,671` |
| introducing commit | `4e75a4fe9ce909fa62794f5a550a3409f6e0fc9f` |
| audit-start local branch | `main`, `origin/main`보다 112 commits ahead |

GitHub는 일반 Git에서 100 MB를 넘는 단일 객체를 차단하므로 현재 이력을 그대로 push할 수 없다.
최신 working-tree 파일만 삭제해도 과거 blob은 사라지지 않는다. 근거는
[GitHub repository limits](https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits)다.

즉시 적용하는 containment는 다음과 같다.

- 원격 push는 `BLOCKED_OVERSIZED_GIT_OBJECT`다.
- 새 100 MB 초과 산출물을 ordinary Git에 추가하지 않는다.
- 기존 blob을 조용히 삭제하거나 이력을 다시 쓰지 않는다.
- 재구성 가능한 산출물은 source, input, version, checksum, 생성 명령만 Git에 남기고 payload는
  승인된 외부 artifact storage 또는 Git LFS로 옮긴다.

이 단락은 2026-08-23 최초 차단 시점의 상태를 보존한다. 사용자는 2026-08-24 이력 재작성과
Git LFS 외부화를 명시적으로 승인했다. 승인된 수습은 정확한 Phase-44 결과 경로 하나와
`4e75a4f...`부터의 미공개 76커밋에만 적용되었고, `origin/main`과 그 뒤 첫 40개 로컬 커밋은
그대로 보존되었다. 일반 Git의 529,370,671-byte blob은 동일 내용 SHA-256의 LFS pointer로
교체되었으며 force-push는 필요하지 않다.

과거 결과·manifest·runner에 기록된 pre-LFS commit SHA는 실행 당시 provenance이므로 치환하지
않는다. old/new 76행 map과 원 DAG bundle이 두 namespace를 연결한다. 정확한 객체, 명령,
검증, backup과 remote receipt는
[`ICE_PHASE44_GIT_LFS_HISTORY_MIGRATION_2026-08-24.md`](ICE_PHASE44_GIT_LFS_HISTORY_MIGRATION_2026-08-24.md)에
기록한다. 이 transport 수습은 Ragnarok pause, route `KILL`, Gate 1 또는 어떤 과학 분류도 바꾸지
않는다.

## 구현 한계

`./ice run`/`./ice repro` 차단기는 canonical relative path, frozen runner hash와 clean core tree를
검사하지만 이미 실행 중인 프로세스를 종료하지 않고 직접 Python 호출을 기술적으로
봉쇄하지도 않는다. terminal closeout 뒤 제어면은 Phase 56도 `RESEARCH_PHASE_PAUSED`로 거부한다.
이후의 직접 우회는 이 결정과 `AGENTS.md` 위반이다. 자격증명 값이나 인증 로그는 이
문서의 evidence가 아니며 저장소에 복사하지 않는다.
