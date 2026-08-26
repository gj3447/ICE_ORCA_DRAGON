# ICE Ragnarok 회로 차단기

> **상태:** ACTIVE operational containment — Phase 56 및 두 bounded Gate-1 window consumed,
> scalar zero-lapse one-shot authorized, `GATE1_ZERO_LAPSE_AUTHORIZED`
> **발효:** 2026-08-23
> **재검토 가능일:** 2026-08-30 — 재검토 자격일일 뿐 자동 재개일이 아니다.
> **비권한:** 이 문서는 과학적 evidence, Gate 1 no-go, 물리학 주장 또는 TOE 판정이 아니다.

> **2026-08-25 국소 개정:** 사용자가 즉시 연구 재개를 명시 승인하여 예정 대기만 정확히
> hash-pin된 번호 없는 Gate-1 end-admissibility 계산 한 개에 한해 면제했다. 그 계산은
> `VALID_RUN`으로 끝나 window가 소진됐고, straight completion 및 declared slice의
> constant-straight-line class만 `KILL`했다. Gate 1은 `OPEN_PARTIAL_PROGRESS`다. Phase 51--56
> route `KILL`, Phase 57 차단과 `next_phase=null`은 바뀌지 않는다. 정본 범위·상한·receipt는
> [`ICE_GATE1_BOUNDED_RESUME_2026-08-25.md`](ICE_GATE1_BOUNDED_RESUME_2026-08-25.md)다.

> **2026-08-26 국소 개정:** 사용자가 다음 연구 진행을 명시하여 예정 대기만 새로 선언한
> fixed-\(a\), \(m=2\) scalar phase-space/source-link exact 계산 한 개에 한해 면제했다. 이 계산은
> physical original cycle을 회수하지 않고 `NEW_BOUNDED_SCALAR_CONTROL`을 검사했다. `VALID_RUN`으로
> 끝나 window가 소진됐으며, Phase 51--56 route `KILL`,
> Phase 57/full replay 차단, `next_phase=null`은 바뀌지 않는다. 정본은
> [`ICE_GATE1_SCALAR_SOURCE_LINK_BOUNDED_RESUME_2026-08-26.md`](ICE_GATE1_SCALAR_SOURCE_LINK_BOUNDED_RESUME_2026-08-26.md)다.

> **2026-08-26 zero-lapse 국소 개정:** 사용자의 계속 연구 지시는 직전 결과가 명시한 다음
> 장애물, 즉 같은 fixed-\(a\), \(m=2\) scalar control의 full \(q\)-paired \(N=0\) canonical
> boundary/contact 문제 한 개에 한해 예정 대기를 면제한다. exact-hash, one-shot, no-argument,
> private receipt와 fail-closed null 경계는
> [`ICE_GATE1_SCALAR_ZERO_LAPSE_BOUNDED_RESUME_2026-08-26.md`](ICE_GATE1_SCALAR_ZERO_LAPSE_BOUNDED_RESUME_2026-08-26.md)에
> 동결했다. 이것은 Phase 57, full replay, retry, 자동 후손 또는 TOE 권한이 아니다.

## 결정

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

- 운영 상태는 exact scalar zero-lapse one-shot만 연 `GATE1_ZERO_LAPSE_AUTHORIZED`이며
  containment는 계속 active다.
- Phase 56의 유일한 terminal-closeout 예외는 실행·독립 재현을 완료해 소진됐다.
- 2026-08-25의 번호 없는 Gate-1 exact window도 한 번의 `VALID_RUN` 뒤 소진됐으며 retry나
  자동 후손을 허용하지 않는다.
- 2026-08-26의 번호 없는 `gate1_scalar_source_link`는 runner/input SHA-256, exact basename 또는
  relpath, 무인자, clean core, 30초/250,000-byte 상한 아래 한 번 실행되어 소진됐다. `.git` 내부
  exclusive launch receipt가 재실행을 차단하며 retry/repro/rename은 허용하지 않는다.
- `gate1_scalar_zero_lapse_extension`만 새 runner/input SHA-256과 upstream result hash에 묶여
  `AUTHORIZED_NOT_YET_RUN`이다. exact 이름·무인자 `ice run` 한 번 외에는 실행할 수 없고,
  receipt가 생기는 즉시 성공/실패/timeout과 무관하게 소진된다. `repro`는 허용하지 않는다.
- 정확히 동결된 Phase 11–50 실행체는 역사 검산용 allowlist로 허용한다. KILL 범위인 Phase
  51–55 재실행, Phase 56 변종, Phase 토큰이 없거나 이름을 바꾼 새 core 실행체, Phase 57 이상은
  `./ice run`과 `./ice repro`에서 `RESEARCH_PHASE_PAUSED`로 거부한다.
- Phase 56 runner와 결과 identity는 종결 provenance로 보존하지만 더는 실행 allowlist가 아니다.
  복합 파일명이나 낮은 Phase 번호 재사용으로 우회할 수 없다.
- 허용된 41개 역사 runner는 SHA-256까지 고정한다. core 디렉터리에 tracked
  수정이나 untracked 파일이 하나라도 있으면 실행 전에 `RESEARCH_CORE_DIRTY`, 허용 경로의 bytes가
  다르면 `RESEARCH_RUNNER_HASH_MISMATCH`로 닫는다. `./`, `..`, 역슬래시, absolute path로 core
  판정을 우회할 수 없고 workspace 밖으로 나가는 경로는 거부한다.
- 직접 `python ...` 실행이나 다른 실행기를 사용한 우회도 승인되지 않는다. 코드 차단기는
  협력적 제어면이므로 이 규칙이 그 나머지 표면을 닫는다.
- Phase 56 결과와 무관하게 `next_phase = null`이다. full replay, Phase 57, threshold 완화 또는
  같은 reconciliation의 새 이름 붙이기는 자동으로 열리지 않는다.

정본 상태는 `./ice status`와 `./ice status --json`으로 읽는다. 7일 pause는 Phase 56 실행
시각이 아니라 이 containment의 2026-08-23 발효일부터 계산한다.

## Phase 56 terminal closeout

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

## Gate-1 scalar source-link terminal result

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

## 재개 조건

일반 새 core Phase에는 2026-08-30 이후에도 다음 조건을 **모두** 만족하고 사용자가 명시적으로
승인해야 한다. 2026-08-25 국소 개정은 새 core Phase가 아니라, saddle/intersection 계산보다
앞선 necessary end-admissibility model-class reduction 한 개이므로 그 날짜 대기만 정확한
runner/input hash와 fail-closed null 출력 아래 면제했다. 그 일회성 예외는 이미 소진됐다.
2026-08-26 국소 개정 역시 일반 재개 조건을 충족했다고 주장하지 않는다. full cycle보다 앞선
reduced scalar source-link discriminator 한 개만 같은 방식으로 면제하며 자동 후손은 없다.

1. 같은 reconciliation이 아니라 Gate 1의 typed object를 직접 계산한다.
2. original joint cycle, orientation, singular divisor, endpoint prescription, regulator, Stokes
   chamber와 relative-end 입력을 실행 전에 완전히 serialize하고 hash-pin한다.
3. 모든 saddle, upward cycle, complex sheet와 asymptotic end의 census를 실행 전에 고정한다.
4. 새 counterexample, invariant, observable discriminator 또는 model-class reduction을 제시한다.
5. 결과별 `KEEP / NARROW / BRANCH / EQUIVALENCE / KILL / OPEN` 표와 단일 Phase의 runtime·artifact
   상한을 실행 전에 고정한다.
6. 아래 ordinary-Git 대용량 객체 문제를 외부화하거나 해결한다.

위 조건은 같은 reconciliation 경로의 재개 조건이 아니다. 그 경로는 새 numbered Phase로 다시
열지 않는다. Phase 53이 저장하지 않은 authoritative saddle, factor, launch와 initial-state bytes가
나중에 독립 출처에서 hash 인증된 형태로 회수되면, 사용자의 별도 승인 아래 **비번호 archival
reproduction audit**만 검토할 수 있다. 그 감사는 route 재개, 다음 Phase 또는 승격 권한이 아니다.

## 원격 전송 차단과 승인된 수습

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
