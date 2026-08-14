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

`.claude/skills/science-feedback-loop.md` 의 루프를 끝까지 돌았을 때만 완료다.

```
계산 → 분류(confirmation / refutation / discovery / numerology)
     → Fitting Detection → Lakatos(progressive / degenerating)
     → Bayesian Update → KG 기록
```

1. **사전예측인지 사후피팅인지 판별을 강제한다.** 이 판별 없이 결과를 보고하지 않는다.
   사전등록 목록에 없던 예측을 사후에 맞췄다면 그렇게 쓴다.
2. **numerology 로 분류되면 `NUMEROLOGY_HOLD` 태깅 + Possibility 강등.** 승격하지 않는다.
3. 수비학 판별은 인상이 아니라 **MC null 정량화**로 한다. 같은 ICE primitive 에서 뽑은
   랜덤 비율이 얼마나 자주 그만큼 맞는지를 세고, look-elsewhere 를 보정한다.
4. **discovery 는 재귀 진입**이다 (PH2 재진입, `/apt-sp` 로 새 span 분해). 닫지 않는다.
5. KG 기록에는 provenance(증거 경로 + 날짜 + actor)를 붙인다. 새 `:Lesson` 은
   `lakatos_mechanism` 이 없으면 write 가 차단된다.

## 결과 파일 규율

`*_results.json` / `RESULT.json` 은 산출물이며 실행하면 바뀐다.

- 남의 dirty result JSON 을 자기 커밋에 끌어넣지 않는다. 커밋 전 `git status` 를 본다.
- 결과를 갱신했으면 **어떤 스크립트를 어떤 인자로 돌려서 나온 것인지** 커밋 메시지에 쓴다.
  재현 불가능한 결과 파일은 결과가 아니다.

## Workflow

1. `./ice list` 로 이미 있는 스크립트를 먼저 본다. 가장 비슷한 것을 읽는다.
2. 무엇을 예측하는지 **먼저** 쓴다. 돌리고 나서 정하지 않는다.
3. 가장 작은 변경을 만든다.
4. `./ice run <name>` 으로 돌리고, 필요하면
   `python3 ice_prereg_check.py` 로 게이트를 건다.
5. 분류 → Lakatos → KG 까지 간 뒤에 완료라고 말한다.
6. 돌린 명령과 실제 출력을 보고한다. 관측하지 않은 그린을 보고하지 않는다.
