# ICE Ragnarok 회로 차단기

> **상태:** ACTIVE operational containment
> **발효:** 2026-08-23
> **재검토 가능일:** 2026-08-30 — 재검토 자격일일 뿐 자동 재개일이 아니다.
> **비권한:** 이 문서는 과학적 evidence, Gate 1 no-go, 물리학 주장 또는 TOE 판정이 아니다.

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

- 운영 상태는 `BOUNDED_PAUSE`다.
- Phase 56은 이미 동결된 질문을 닫고 결과를 보고하기 위한 유일한 terminal-closeout 예외다.
- 정확히 동결된 Phase 11–50 실행체만 역사 검산용 allowlist로 허용한다. KILL 범위인 Phase
  51–55 재실행, Phase 56 변종, Phase 토큰이 없거나 이름을 바꾼 새 core 실행체, Phase 57 이상은
  `./ice run`과 `./ice repro`에서 `RESEARCH_PHASE_PAUSED`로 거부한다.
- Phase 56 예외는
  `cpt_temporal_folded_susy/phase56_lambda_half_launch_provenance_residual_conditioning.py`
  하나와 정확히 일치해야 한다. 복합 파일명이나 낮은 Phase 번호 재사용으로 우회할 수 없다.
- 허용된 41개 역사 runner와 Phase 56 runner는 SHA-256까지 고정한다. core 디렉터리에 tracked
  수정이나 untracked 파일이 하나라도 있으면 실행 전에 `RESEARCH_CORE_DIRTY`, 허용 경로의 bytes가
  다르면 `RESEARCH_RUNNER_HASH_MISMATCH`로 닫는다. `./`, `..`, 역슬래시, absolute path로 core
  판정을 우회할 수 없고 workspace 밖으로 나가는 경로는 거부한다.
- 직접 `python ...` 실행이나 다른 실행기를 사용한 우회도 승인되지 않는다. 코드 차단기는
  협력적 제어면이므로 이 규칙이 그 나머지 표면을 닫는다.
- Phase 56 결과와 무관하게 `next_phase = null`이다. full replay, Phase 57, threshold 완화 또는
  같은 reconciliation의 새 이름 붙이기는 자동으로 열리지 않는다.

정본 상태는 `./ice status`와 `./ice status --json`으로 읽는다. 7일 pause는 Phase 56 실행
시각이 아니라 이 containment의 2026-08-23 발효일부터 계산한다.

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

2026-08-30 이후에도 다음 조건을 **모두** 만족하고 사용자가 명시적으로 승인해야 새 core Phase를
검토할 수 있다.

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

## 원격 전송 차단과 비파괴 수습

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

이력 수습은 파괴적·협업 조정 작업이므로 별도 사용자 승인 뒤에만 수행한다. 승인 시에는
안전 사본 작성 → artifact backend와 checksum 확정 → 명시한 refs만 filter/LFS migration → 새
checkout에서 tree·재현·ontology 검증 → force-push와 collaborator re-clone 조정 순서로 한다.
현재 결정은 어떤 amend, rebase, reset, filter 또는 push도 승인하지 않는다.

## 구현 한계

`./ice run`/`./ice repro` 차단기는 canonical relative path, frozen runner hash와 clean core tree를
검사하지만 이미 실행 중인 프로세스를 종료하지 않고 직접 Python 호출을 기술적으로
봉쇄하지도 않는다. 발효 시점의 프로세스 검사에서는 Phase 56/57 연구 프로세스가 남아 있지
않았고, 이후의 직접 우회는 이 결정과 `AGENTS.md` 위반이다. 자격증명 값이나 인증 로그는 이
문서의 evidence가 아니며 저장소에 복사하지 않는다.
