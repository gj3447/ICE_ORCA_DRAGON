# ICE_ORCA_DRAGON — 작업 규칙

> 이 저장소의 규칙은 여기 있다. 상위 규약(단일 writer 토큰, 세션 핸드오프, KG 정본)은
> 부모 저장소 SYMPOSIUM 의 `AGENTS.md` 를 따른다.
> **이 저장소는 submodule 이다.** 여기서 커밋하면 부모의 gitlink 가 바뀐다. submodule
> 커밋은 부모 writer token을 직접 보유하고 write-set에 이 gitlink를 포함한 세션만 한다.
> 다른 세션은 token이 HELD인 동안 read-only다.

## 먼저 알아야 할 것 — 여기는 물리학이 아니라 **계산 워크벤치**다

`ICE_WORKBENCH_REFRAME_2026-05-18.md` 가 영구 승격시킨 지위다
(선행: `ICE_PHYSICS_PARTIAL_RETREAT_2026-05-17.md`).

- 산출물을 **물리학 주장으로 서술하지 않는다.** 수치 일치는 그 자체로 물리가 아니다.
- 동시에 사용자 원문 spec(12사도 #2, `MIND/metahumotonic/나는야_ice_orca_dragon.md`)은
  **erase 금지**다 (narrative-feedback-loop, Eilu va-Eilu). 격하가 아니라 층 분리다.
- 이 둘을 동시에 지키는 것이 이 저장소에서 가장 자주 틀리는 지점이다.

## Commands

제어면은 **Node 24 + strict TypeScript + Effect 3**이며 `package-lock.json`으로 고정한다.
계산면은 기존 NumPy/SciPy/SymPy Python 커널이며 **Python 3.13 + `uv.lock`**으로
고정한다. 호스트 전역에 설치하지 말고 최초 1회 두 lock을 설치한다.

```bash
npm ci
uv sync --locked
```

- 환경 진단: `./ice doctor` (동일 명령: `npm run ice -- doctor`)
- 실행 가능한 스크립트 열거: `./ice list` (`--json` 지원)
- 스크립트 실행: `./ice run <name|relpath> [-- args...]`
  (해당 스크립트의 *자기 디렉토리*에서 실행되고 exit code 를 그대로 전파한다)
- 재현 검사: `./ice repro [--list]`
  (Effect scoped 임시 사본에서 실행하므로 committed JSON 불변)
- 단일 재현 검사: `./ice repro --only <name>`
- 스크립트 정보: `./ice info <name>` (경로 / 독스트링 / 산출 result JSON)
- 사전등록 게이트: `python3 ice_prereg_check.py`
  (P01–P15 pre-registered prediction vs 동결 PDG observable, MC null `P(E|~H)`,
  Bonferroni look-elsewhere 보정)

`name` 은 stem 또는 relpath, unique-prefix 매칭이 된다.

`test/`에는 Effect/Vitest 제어면 계약 검사가 있다 (`npm run check` = strict typecheck +
12 tests). 자동 GitHub Actions CI는 아직 없다.
이 검사는 도구 회귀만 막는다. 물리 오라클은 사전등록 + MC null 게이트이며,
"단위검사가 통과했다"는 물리 연구 완료 근거가 아니다.

재현 정책은 전역 epsilon이 아니다. 구조/키/배열/범주는 exact, 일반 float는 tight
semantic compare, queue04 optimizer angle 경로만 `atol=1e-6`이다. queue03 legacy는
basis-dependent metric 때문에 `NONPORTABLE_FAIL`이며 tolerance로 숨기지 않는다.

## Definition of Done

먼저 작업 tier를 고른다. 높은 tier의 의례를 낮은 tier에 소급 적용하지 않는다.
여러 tier가 겹치면 가장 높은 tier를 결과 관측 전에 적용한다. T0/T1에서 T2로 승격할 수는
있지만 결과가 불리하거나 null이라는 이유로 T2를 낮추지 않는다.

- **T0 일반 공학** — 문서, CLI, 리팩터링, 의존성, 타입/단위검사, 재현 하네스.
  Node/TS 제어면은 `npm run check`, Python 커널·`uv.lock`은 `./ice doctor`와 대상
  run/repro, 문서는 관련 형식/링크 검사처럼 변경한 plane에 직접 관련된 최소 검증이 통과하고
  결과 JSON을 뜻하지 않게 바꾸지 않으면 완료다. 과학 분류, Bayes, Lakatos,
  science-evidence KG 기록은 필요 없다.
- **T1 동결 계산 재현** — 기존 방법·observable·해석을 바꾸지 않는 재실행.
  `./ice doctor`, 정확한 명령/환경, semantic diff를 기록한다. 기대 결과와 일치했다는 이유만으로
  이론 confidence를 올리지 않는다. 유의한 drift나 과학 주장에 영향을 주는 방법 결함이 나오면
  T2로 승격한다.
- **T2 과학 주장 영향** — 새/변경 observable, 가설 지지·반박, null/multiplicity 결과,
  Contract confidence/status 또는 Span grade에 영향을 주는 작업. 이때만
  `.claude/skills/science-feedback-loop.md`의 전체 게이트를 적용한다. 코드도 바꿨다면 T0의
  관련 공학 검사도 함께 통과해야 한다.

T2에서도 사전등록 여부와 적용 가능한 null model을 결과 분류보다 먼저 고정한다. 수치 Bayes는 prior와
`P(E|H)`, `P(E|~H)`가 사전에 정의된 경우에만 한다. fitting/numerology 의심은 MC null과
look-elsewhere 검증 전에는 승격 근거가 아니다. 여러 세션에서 재사용할 결과만 provenance가
붙은 `PENDING` evidence로 KG에 기록한다. Contract/Span 변경은 기존 evidence ID와 명시된
ratifier 권한을 확인한 별도 ratification 뒤에 한다. discovery는 후속 작업으로 등록하고,
현재 판단을 막거나 사용자가 명시한 경우에만 재귀 진입한다.

## 결과 파일 규율

`*_results.json` / `RESULT.json` 은 산출물이며 실행하면 바뀐다.

- 남의 dirty result JSON 을 자기 커밋에 끌어넣지 않는다. 커밋 전 `git status` 를 본다.
- 결과를 갱신했으면 **어떤 스크립트를 어떤 인자로 돌려서 나온 것인지** 커밋 메시지에 쓴다.
  재현 불가능한 결과 파일은 결과가 아니다.

## Workflow

1. 관련 기존 산출물을 먼저 본다. 계산 작업일 때만 `./ice list`로 가장 비슷한 스크립트를 찾는다.
2. T0/T1/T2를 먼저 선언한다. T2라면 무엇을 예측하고 어떤 기준으로 판정할지 실행 전에 쓴다.
3. 가장 작은 변경을 만든다.
4. 변경에 맞는 최소 검증을 실행한다. 계산을 바꿨다면 `./ice run <name>`, 재현이면
   `./ice repro --only <name>`, T2면 필요에 따라 `python3 ice_prereg_check.py`를 사용한다.
5. 선택한 tier의 완료 조건까지만 수행한다. T0/T1에 T2 의례를 얹지 않는다.
6. 실행한 명령과 실제 출력을 보고한다. 관측하지 않은 그린을 보고하지 않는다.
