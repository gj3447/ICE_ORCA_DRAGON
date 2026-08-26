# ICE_ORCA_DRAGON — 작업 규칙

> 이 파일이 독립 저장소의 활성 규칙이다. dev-01 정본 checkout은
> `/home/lagyeongjun/CD/ICE_ORCA_DRAGON`, 원격 정본은 `gj3447/ICE_ORCA_DRAGON`의
> `main`이다. 이 저장소는 submodule이 아니며 sibling 저장소의 writer token이나 규칙을
> 암묵적으로 상속하지 않는다. 기존 dirty 변경을 보존하고 변경 경로만 정확히 stage한 뒤,
> 이 저장소 안에서 직접 검증·commit한다. 원격 push는 사용자가 요청한 경우에만 한다.

## 먼저 알아야 할 것 — 여기는 물리학이 아니라 **계산 워크벤치**다

`docs/decisions/ICE_WORKBENCH_REFRAME_2026-05-18.md` 가 영구 승격시킨 지위다
(선행: `docs/decisions/ICE_PHYSICS_PARTIAL_RETREAT_2026-05-17.md`).

- 산출물을 **물리학 주장으로 서술하지 않는다.** 수치 일치는 그 자체로 물리가 아니다.
- 동시에 사용자 원문 spec(12사도 #2, `MIND/metahumotonic/나는야_ice_orca_dragon.md`)은
  **erase 금지**다 (narrative-feedback-loop, Eilu va-Eilu). 격하가 아니라 층 분리다.
- 이 둘을 동시에 지키는 것이 이 저장소에서 가장 자주 틀리는 지점이다.

## Ragnarok 회로 차단기 — ACTIVE

`docs/decisions/ICE_RAGNAROK_CIRCUIT_BREAKER_2026-08-23.md`가 현재 core 연구의 실행 경계를
정한다. `./ice status`가 기계 판독 가능한 정본이다.

- Phase 51→56의 saved-backend/reconstructed-launch reconciliation 경로는 **KILL**이다.
- Phase 56 terminal-closeout 예외는 동결된 질문의 실행·독립 재현을 마쳐 소진됐다. 그 결과와
  무관하게 Phase 57 이상, full replay, 같은 evaluator/dtype/solver/residual/provenance 채무의
  자동 offspring를 만들거나 실행하지 않는다. 직접 Python 실행으로 제어면을 우회하지 않는다.
- 제어면은 동결된 Phase 11–50 역사 실행체와 아래에 명시한 현재의 단일 bounded window만 허용한다.
  2026-08-25 사용자가 즉시
  승인한 `GATE1_DIRECT_20260825_01` exact hash-pinned runner는 Phase-39 straight field-ray end
  admissibility 계산을 정상 완료해 **소진됐으며 재실행하지 않는다**. 결과는 straight completion과
  declared slice의 constant-straight-line model class만 `KILL`, Gate 1은
  `OPEN_PARTIAL_PROGRESS`다. 완료된 Phase 56을 포함한 Phase 51+, 낮은 번호 재사용과 그 밖의
  Phase 토큰 없는 새 core 실행체도 모두 차단한다. 단, 2026-08-26 사용자가 별도 승인한
  `GATE1_SOURCE_LINK_20260826_01`은 새로 선언한 fixed-\(a\), \(m=2\) scalar \((q,p)\) control의
  source link만 검사하는 번호 없는 exact-hash runner 한 번이었다. `VALID_RUN`으로 끝나
  **소진됐으며 재실행하지 않는다**. 비영 lapse arm의 reduced scalar link와 orientation \(+1\)은
  `KEEP`, zero-including full \(q\)-paired distribution은 `OPEN`이고 Gate 1은 계속
  `OPEN_PARTIAL_PROGRESS`다. 직전 결과가 남긴 바로 그 장애물에 한해 사용자의 계속 연구 지시가
  `GATE1_ZERO_LAPSE_20260826_01`을 승인했다. 이는 같은 fixed-\(a\), \(m=2\) control의 full
  \(q\)-paired canonical boundary와 scaling-degree-preserving contact ambiguity만 검사하는 번호 없는
  exact-hash runner **한 번**이다. 현재 `AUTHORIZED_NOT_YET_RUN`이며 exact name, 무인자,
  clean core, runner/input/upstream hash, private exclusive receipt와 30초/250,000-byte 상한을 지킨다.
  이는 physical original joint cycle 복원, Phase 51–56 route 재개, Phase 57/full replay 또는 자동
  후손 권한이 아니다. `repro`도 같은 경계를 적용한다.
- 허용 경로도 runner SHA-256과 clean `cpt_temporal_folded_susy/` provenance가 일치해야 한다.
  traversal/absolute path, dirty·untracked core 파일, 허용 이름에 다른 bytes 덮어쓰기는 실행하지
  않는다.
- 2026-08-30은 일반 새 core Phase의 재검토 자격일일 뿐 자동 재개일이 아니다. 사용자의
  2026-08-25 및 2026-08-26 지시는 그 예정 대기만 각 exact Gate-1 계산에 한해 면제했으며,
  일반 재개나 새 numbered Phase 권한이 아니다. 상세 범위는
  `docs/decisions/ICE_GATE1_BOUNDED_RESUME_2026-08-25.md`와
  `docs/decisions/ICE_GATE1_SCALAR_SOURCE_LINK_BOUNDED_RESUME_2026-08-26.md`,
  `docs/decisions/ICE_GATE1_SCALAR_ZERO_LAPSE_BOUNDED_RESUME_2026-08-26.md`를 따른다.
- 이는 과학적 Gate 1 KILL이 아니다. Gate 1은 `OPEN_PARTIAL_PROGRESS`, global promotion은
  `PROHIBITED`, scientific route는 `OPEN`이다.
- Phase 44의 529,370,671-byte 결과는 2026-08-24 사용자 승인 아래 exact-path Git LFS로
  이관됐다. pre-LFS backup ref는 로컬 복구용이므로 `git push --all`/mirror 대상에 넣지 않는다.
  이후에도 100 MB 초과 산출물을 ordinary Git에 넣거나 별도 승인 없이 추가 이력 재작성을 하지
  않는다. 전송 상태와 provenance map은 `./ice status`와
  `docs/decisions/ICE_PHASE44_GIT_LFS_HISTORY_MIGRATION_2026-08-24.md`를 따른다.

## Commands

제어면은 **Node 24 + strict TypeScript + Effect 3**이며 `package-lock.json`으로 고정한다.
계산면은 기존 NumPy/SciPy/SymPy Python 커널이며 **Python 3.13 + `uv.lock`**으로
고정한다. Phase-44 원문 수화에는 Git LFS가 필요하다. 호스트 전역 Python/Node에 설치하지 말고
최초 1회 LFS와 두 lock을 준비한다.

```bash
git lfs install --local
git lfs pull --include="cpt_temporal_folded_susy/PHASE44_M4_NUMPY64_LOCAL_RHS_ERROR_DECOMPOSITION_RESULT.json"
npm ci
uv sync --locked
```

- 환경 진단: `./ice doctor` (동일 명령: `npm run ice -- doctor`)
- 연구 중단 상태: `./ice status` (`--json` 지원)
- 실행 가능한 스크립트 열거: `./ice list` (`--json` 지원)
- 스크립트 실행: `./ice run <name|relpath> [-- args...]`
  (해당 스크립트의 *자기 디렉토리*에서 실행되고 exit code 를 그대로 전파한다)
- 재현 검사: `./ice repro [--list]`
  (Effect scoped 임시 사본에서 실행하므로 committed JSON 불변)
- 단일 재현 검사: `./ice repro --only <name>`
- 스크립트 정보: `./ice info <name>` (경로 / 독스트링 / 산출 result JSON)
- 연구 그래프 검사·조회: `./ice ontology validate`, `./ice ontology summary`,
  `./ice ontology show <node-id>`, `./ice ontology trace <node-id>`
- 기존 numerology 검산(선택): `./ice run ice_prereg_check`
  (과거 P01–P15 산출물 재현용이며 새 연구의 필수 게이트가 아니다)

`name` 은 stem 또는 relpath, unique-prefix 매칭이 된다.

`test/`에는 Effect/Vitest 제어면 계약 검사가 있다 (`npm run check` = strict typecheck +
Vitest suite). 자동 GitHub Actions CI는 아직 없다.
이 검사는 도구 회귀만 막는다. "단위검사가 통과했다"는 물리 연구 완료 근거가 아니며,
계산 결과와 물리적 해석은 분리해서 보고한다.

재현 정책은 전역 epsilon이 아니다. 구조/키/배열/범주는 exact, 일반 float는 tight
semantic compare, queue04 optimizer angle 경로만 `atol=1e-6`이다. queue03 legacy는
basis-dependent metric 때문에 `NONPORTABLE_FAIL`이며 tolerance로 숨기지 않는다.

## Definition of Done

이 저장소는 의무적인 연구 계약, tier 선언, 사전등록, Bayes/Lakatos/KG ratification을 요구하지
않는다. 새 계산은 다음의 짧은 기준으로 끝낸다.

- 사용한 primary source, 방정식, convention과 가정을 코드나 인접 메모에 남긴다.
- 가장 작은 exact 또는 numerical calculation을 먼저 실행한다.
- 명령, 환경, 입력, 실제 출력을 남기고 변경 위험에 비례한 독립 검산을 한다.
- 계산으로 확인된 사실, 해석, 아직 열린 물리 가설을 명확히 분리한다.
- null, basis dependence, 단위/부호 오류도 그대로 결과로 보고하며 원하는 결론에 맞춰 숨기지 않는다.

과거 `*_RESEARCH_CONTRACT.json`, run receipt, replay receipt는 당시 결과의 재현 provenance일 뿐
새 작업을 지배하지 않는다. 기존 실행기가 그것을 읽는 경우 역사적 재현을 위해 보존한다.

## 연구 온톨로지

- 계산이 기존 claim의 지위, 직접 evidence, 적용 scope, 또는 다음 open problem을 실질적으로
  바꾸면 `ontology/`의 repository-local research graph와 evidence snapshot을 함께 갱신하고
  `./ice ontology validate`로 검증한다. 문구 수정이나 중간 실험마다 의례적으로 갱신하지 않는다.
- 온톨로지는 연구 내용을 찾고 추적하기 위한 **기억·색인 계층**이다. 연구 계약, 사전등록,
  물리적 ratification, 또는 외부 KG 승격을 뜻하지 않는다. 외부 KG에 쓸 권한이나 정확한 대응
  노드가 없으면 local graph에 `UNRESOLVED` bridge로 남기고 임의로 새 UID를 만들지 않는다.
- claim은 계산된 사실, 해석, 열린 가설을 구분하고, evidence는 재현 명령·script hash·개별 check
  ID를 보존한다. 사람이 먼저 읽을 수 있는 개념 지도와 기계가 검사하는 JSON을 함께 유지한다.

## 커밋 규율

- 사용자 요청의 완료된 작업 단위마다 관련 검증을 끝낸 뒤 **같은 턴에서 로컬 Git commit까지**
  만든다. 완료된 source·test·문서 변경을 handoff 시 unstaged/uncommitted로 남기지 않는다.
- 한 요청 안에 독립 deliverable이 여러 개면 의미 단위별로 커밋을 나눈다. 사소한 중간 patch마다
  커밋하지 말고, 검증 가능한 coherent unit이 완성되는 시점을 경계로 삼는다.
- 작업 시작과 커밋 직전에 `git status`를 확인한다. 기존 dirty 변경은 사용자 소유로 간주하고
  보존하며, 이번 작업에서 만든 정확한 경로만 stage한다. 다른 사람의 변경을 몰래 섞지 않는다.
- 커밋 메시지는 무엇을 계산·수정했는지 드러내고, 산출 결과를 포함하면 실행 명령이나 핵심
  검증을 본문에 기록한다. 실패한 검증을 숨긴 채 커밋하지 않는다.
- generated cache, 가상환경, 대용량 다운로드 binary는 사용자가 versioning까지 요청하지 않은
  한 커밋하지 않는다. 대신 재구성 가능한 source URL, version, checksum, 생성 명령을 추적한다.
- 기존 commit을 amend/rebase/reset으로 다시 쓰지 않는다. push, PR, release는 로컬 commit과
  별도 외부 변경이므로 사용자가 요청한 경우에만 수행한다.

## 결과 파일 규율

`*_results.json` / `RESULT.json` 은 산출물이며 실행하면 바뀐다.

- 남의 dirty result JSON 을 자기 커밋에 끌어넣지 않는다. 커밋 전 `git status` 를 본다.
- 결과를 갱신했으면 **어떤 스크립트를 어떤 인자로 돌려서 나온 것인지** 커밋 메시지에 쓴다.
  재현 불가능한 결과 파일은 결과가 아니다.

## Workflow

1. 관련 기존 산출물을 먼저 본다. 계산 작업일 때만 `./ice list`로 가장 비슷한 스크립트를 찾는다.
2. source/convention을 확인하고 가장 작은 계산 또는 변경을 만든다.
3. 변경에 맞는 최소 검증을 실행한다. 계산을 바꿨다면 `./ice run <name>`, 기존 산출물의
   재현이면 `./ice repro --only <name>`을 사용한다.
4. 실행한 명령과 실제 출력을 보고한다. 관측하지 않은 그린을 보고하지 않는다.
