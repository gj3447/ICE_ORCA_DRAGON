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

## TOE 북극성과 삼천포 차단 — ACTIVE

`docs/decisions/ICE_TOE_CRITICAL_PATH_ROUTING_2026-09-01.md`가 core 연구의 현재 navigation
정본이다. 사용자 목표는 evidence-backed TOE를 향한 선언된 CPT candidate route의 구성·해소 또는
반증이지만, 이는 목표이지 성립한 물리 claim이 아니다. scoped negative result는 해당 route만 닫으며
모든 가능한 TOE를 반증하지 않는다.

- 현재 첫 병목은 `open:gate1-original-cycle-signed-global-intersections`다. 기본 core 연구는
  source-defined regulated joint relative class, 완전한 saddle/sheet/singular·Stokes/good-end census,
  oriented global intersection vector, homotopy·gauge·regulator 안정성 중 하나를 직접 줄여야 한다.
  완전하고 안정적인 zero vector도 유효한 negative resolution이다.
- CPT core 작업을 설계하기 전에 `./ice agent plan "<한 질문>" --graph cpt --json`을 실행한다. 질문은
  canonical open-problem node, 아직 없는 typed object, bounded falsifiable output, 다음 gate에서 TOE
  종료조건까지의 dependency path를 명시해야 한다. planner의 `CURRENT_BLOCKER_CANDIDATE`는 검토
  후보일 뿐 승인이나 evidence가 아니며, 사람이 같은 네 항목을 확인해야 한다.
- G1→G2→G3→G4→G5→full-theory/empirical review는 claim dependency다. upstream compatible typed
  input 없이 수행한 downstream 계산은 허용되더라도 `CONDITIONAL`/`SUPPORTING_METHOD`이며 core TOE
  진전으로 세지 않는다. P1--P7은 기본 supporting이며, 사람이 정확한 G1--G5 missing object와 바뀔
  evidence edge를 확인한 경우에만 core-routing 후보가 된다.
- blocker/path가 없거나, 이미 충분한 local lemma를 반복하거나, named consumer 없는 tooling을 만들거나,
  backend·dtype·solver·tolerance만 바꾸거나, 다른 독립 ontology graph를 근거 없이 합치면
  `STOP_OR_REFRAME`, `MAINTENANCE`, 또는 `ARCHIVE`로 격리한다. 한 결과가 후속 작업을 자동 생성하지
  않는다.
- 저장소 내부의 최종 허용 표시는 `TOE_CANDIDATE_READY_FOR_EXTERNAL_REVIEW`다. G1--G5뿐 아니라 full
  3+1 local modes, arbitrary-background closure, regulator-independent continuum/UV completion, positive
  physical state, unitarity/causality, GR+QFT low-energy recovery, normalized discriminator, data likelihood와
  독립 재현 검토가 모두 필요하다. 이는 TOE 발견 선언이 아니며 과학적 수용은 외부 검토 사항이다.

## 실행 차단기 — ACTIVE (Ragnarok 역사 경로에 한정)

`docs/decisions/ICE_RAGNAROK_CIRCUIT_BREAKER_2026-08-23.md`는 killed route의 실행 경계만
정한다. 새 연구 방법은 `docs/decisions/ICE_LEAN_RESEARCH_RULES_2026-08-31.md`가 정본이다.
`./ice status`는 현재 운영 경계만, `./ice status --history`는 동결된 receipt·이관 이력을 보인다.
역사 상세는 provenance이지 새 작업의 절차가 아니다.

- Phase 51→56의 saved-backend/reconstructed-launch reconciliation 경로는 **KILL**이고 Phase 56
  terminal closeout은 소진됐다. Phase 57 이상, full replay, 번호를 낮춰 재사용한 후속 Phase와 같은
  evaluator/dtype/solver/residual/provenance 채무의 자동 offspring는 실행하지 않는다. 직접 Python
  실행으로 제어면을 우회하지 않는다.
- 정확히 동결된 Phase 11–50 runner는 hash-pinned 역사 검산 allowlist다. Phase 51–56과 과거 세
  Gate-1 one-shot runner는 결과 provenance로 보존하되 재실행·rename·retry하지 않는다.
- **새 연구는 번호 없는 core 계산으로 열려 있다.** clean committed runner만 `./ice run`을 통해
  실행하며 공통 상한은 120초, stdout/stderr 각 262,144 bytes, 변경 artifact 12개/1,000,000
  bytes다. per-window authorization이나 launch receipt를 새 작업의 재귀 계약으로 만들지 않는다.
  Phase 토큰을 붙인 새 descendant, traversal/absolute path, dirty·untracked core tree는 계속
  차단한다.
- generic bounded 계산 하나의 결과는 다음 계산을 자동 생성하거나 승인하지 않는다. 새 질문은 이전
  evidence가 실질적으로 남긴 과학적 장애물을 직접 겨냥하고, 입력·소스·가정과 실제로 관련된
  제외 범위만 고정한 독립 작업 단위여야 한다. 중앙 runtime 상한, `Gate 1`, `global_promotion`,
  `numbered_phase`, `automatic_next`와 무관한 일반 계산은 이 governance 필드를 결과에 복제하지 않는다.
- **규칙 부채 차단기도 active다.** 과거 one-shot authorization, receipt, 재개 조건, 대형 null matrix,
  전 check-ID 복제, 계산마다의 수동 repro/KG 등록을 새 번호 없는 계산의 기본 형식으로 이식하지
  않는다. false-signal map은 순차 gate가 아니라 실패 원인별 선택 메뉴이며 관련 control만 사용한다.
- 2026-08-30은 더 이상 서로 다른 번호 없는 계산의 대기 조건이 아니며, numbered route를 자동으로
  다시 여는 날짜도 아니다.
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
- 현재 연구 상태: `./ice status` (`--json` 지원)
- 동결된 상세 이력: `./ice status --history` (`--json`과 병용 가능)
- 실행 가능한 스크립트 열거: `./ice list` (`--json` 지원)
- 스크립트 실행: `./ice run <name|relpath> [-- args...]`
  (해당 스크립트의 *자기 디렉토리*에서 실행되고 exit code 를 그대로 전파한다)
- 재현 검사: `./ice repro [--list]`
  (Effect scoped 임시 사본에서 실행하므로 committed JSON 불변)
- 단일 재현 검사: `./ice repro --only <name>`
- 스크립트 정보: `./ice info <name>` (경로 / 독스트링 / 산출 result JSON)
- 연구 그래프 검사·조회: `./ice ontology validate`, `./ice ontology summary`,
  `./ice ontology show <node-id>`, `./ice ontology trace <node-id>`
- 현재 core/support 탐색: `./ice ontology guide --graph cpt --path toe-current-critical-path`,
  `./ice ontology guide --graph cpt --path v0-supporting-bridge-portfolio`
- graph+collection 변경 검토: `./ice ontology review --graph all --base HEAD`
- core 경로 사전검토: `./ice agent plan "<question>" --graph cpt --json`
- evidence 문맥·영향·무결성: `./ice harness context <node-id>`, `./ice harness impact <path>`,
  `./ice harness check`
- bounded graph retrieval: `./ice graphrag search "<question>" --graph cpt --depth 0..3`
- 기존 numerology 검산(선택): `./ice run ice_prereg_check`
  (과거 P01–P15 산출물 재현용이며 새 연구의 필수 게이트가 아니다)

`name` 은 stem 또는 relpath, unique-prefix 매칭이 된다.

`repro` manifest는 장기 회귀 기준으로 승격한 결과만 등록한다. 일반 bounded 계산마다 manifest와
전용 테스트를 추가하지 않는다. 새 계산의 1차 재현 기록은 raw result의 command·hash와 인접 보고서다.

`test/`에는 Effect/Vitest 제어면 계약 검사가 있다 (`npm run check` = strict typecheck +
Vitest suite). 자동 GitHub Actions CI는 아직 없다.
이 검사는 도구 회귀만 막는다. "단위검사가 통과했다"는 물리 연구 완료 근거가 아니며,
계산 결과와 물리적 해석은 분리해서 보고한다.

재현 정책은 전역 epsilon이 아니다. 구조/키/배열/범주는 exact, 일반 float는 tight
semantic compare, queue04 optimizer angle 경로만 `atol=1e-6`이다. queue03 legacy는
basis-dependent metric 때문에 `NONPORTABLE_FAIL`이며 tolerance로 숨기지 않는다.

## Definition of Done

새 번호 없는 계산의 방법 정본은
`docs/decisions/ICE_LEAN_RESEARCH_RULES_2026-08-31.md`다. 의무적인 연구 계약, tier 선언,
전면 사전등록, Bayes/Lakatos/KG ratification을 요구하지 않는다. 다음 여섯 규칙으로 끝낸다.

1. 질문 하나, 출력 하나, 그리고 그 결과만으로는 하지 않는 주장 하나를 짧게 고정한다.
2. primary source·방정식·convention·가정·입력·명령·환경·실제 출력과 실패를 raw result 또는
   인접 메모 한 곳에 남긴다.
3. `algebra`, `sign/unit`, `discretization`, `truncation`, `solver`, `spectrum`, `gauge`,
   `inference` 중 주된 실패원인을 하나 고르고 관련 control 1--3개만 수행한다.
4. 변경 위험과 주장 강도에 비례해 독립 검산한다. 같은 runner 재실행은 repeatability이지
   독립 evidence가 아니다.
5. finite 계산 사실, numerical error, model/continuum 해석, physical/empirical hypothesis를
   분리한다.
6. 결과는 다음 작업을 자동 승인하지 않는다. ontology는 claim/evidence/scope/open problem이
   실질적으로 바뀔 때만, repro manifest는 장기 회귀 기준이 필요할 때만 쓴다.

외부 자료를 쓰는 confirmatory empirical claim에만 observable, scan/cut/nuisance 범위와 stopping
rule의 사전 고정 및 적절한 multiplicity/global calibration을 요구한다. 결정론적 탐색 계산은
허용하되 탐색으로 표시한다. null, basis dependence, 단위/부호 오류도 그대로 결과로 보고하며
원하는 결론에 맞춰 숨기지 않는다.

과거 `*_RESEARCH_CONTRACT.json`, run receipt, replay receipt는 당시 결과의 재현 provenance일 뿐
새 작업을 지배하지 않는다. 기존 실행기가 그것을 읽는 경우 역사적 재현을 위해 보존한다.

## 연구 온톨로지

- 계산이 기존 claim의 지위, 직접 evidence, 적용 scope, 또는 다음 open problem을 실질적으로
  바꾸면 `ontology/`의 repository-local research graph를 갱신하고 `./ice ontology validate`로
  검증한다. 문구 수정, 방법 메모, 중간 실험, 단순 verifier 결과마다 의례적으로 갱신하지 않는다.
- 온톨로지는 연구 내용을 찾고 추적하기 위한 **기억·색인 계층**이다. 연구 계약, 사전등록,
  물리적 ratification, 또는 외부 KG 승격을 뜻하지 않는다. 외부 KG에 쓸 권한이나 정확한 대응
  노드가 없으면 local graph에 `UNRESOLVED` bridge로 남기고 임의로 새 UID를 만들지 않는다.
- raw `RESULT.json`을 실행 check ledger의 단일 정본으로 둔다. 온톨로지는 그 artifact hash와 결론을
  찾는 데 필요한 핵심 check locator만 보존하며, 전체 check 배열을 evidence snapshot과 graph에
  복제하지 않는다. 별도 snapshot은 raw result가 안정된 정본이 될 수 없는 경우에만 둔다.
- collection의 기본 graph는 CPT다. G1--G5 core path와 P1--P7 supporting path를 별도로 읽고,
  hypercomplex·legacy·IG-RUEQFT를 CPT evidence로 합치지 않는다. 새 node 묶음은 실제 의미를 가진
  typed edge로 programme component에 연결해야 하며, `ontology validate`의 component 오류를
  reading path만 추가해서 숨기지 않는다.

## 커밋 규율

- 사용자 요청의 완료된 작업 단위마다 관련 검증을 끝낸 뒤 **같은 턴에서 로컬 Git commit까지**
  만든다. 완료된 source·test·문서 변경을 handoff 시 unstaged/uncommitted로 남기지 않는다.
- 한 요청 안에 독립 deliverable이 여러 개면 의미 단위별로 커밋을 나눈다. 사소한 중간 patch마다
  커밋하지 말고, 검증 가능한 coherent unit이 완성되는 시점을 경계로 삼는다. clean runner를 위한
  실행 전 source/input commit 뒤에는 result·report와 실제로 필요한 색인 변경을 한 completion
  commit으로 묶으며, repro 등록과 ontology 등록만을 각각 별도 commit으로 만들지 않는다.
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

1. CPT core 연구면 `./ice agent plan "<question>" --graph cpt --json`으로 현재 blocker와 TOE dependency
   path를 먼저 검토한다. `CURRENT_BLOCKER_CANDIDATE`가 아니면 core 계산을 설계하지 않고 질문을
   재구성하거나 supporting/maintenance로 분류한다.
2. 관련 기존 산출물을 먼저 본다. 계산 작업일 때만 `./ice list`로 가장 비슷한 스크립트를 찾는다.
3. source/convention을 확인하고 가장 작은 계산 또는 변경을 만든다.
4. 변경에 맞는 최소 검증을 실행한다. 계산을 바꿨다면 `./ice run <name>`, 기존 산출물의
   재현이면 `./ice repro --only <name>`을 사용한다.
5. 실행한 명령과 실제 출력을 보고한다. 관측하지 않은 그린을 보고하지 않는다.
