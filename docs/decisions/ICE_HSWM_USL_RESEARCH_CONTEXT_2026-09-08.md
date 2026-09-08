# HSWM route로 수행하는 ICE 연구와 USL 문맥

2026-09-08 · 사용자 승인으로 활성화한 로컬 연구 route.

이 결정은 HSWM을 ICE 연구의 **참조 preview**가 아니라 실제 질문을 전개하고
검토하거나 제한된 계산으로 연결하는 route runtime으로 쓴다. 다만 HSWM의 출력과
feedback은 연구 제안·경로 선택의 기록일 뿐, 물리적 사실·evidence·TOE 진전의 판정은
아니다. ICE의 raw result, 인접 보고서, ontology의 사람 검토 경계와 `./ice run`의
실행 한도는 그대로 정본이다.

## 선언된 프로그램과 상태

이 문서의 기본 route는 v1이다. 검토한 연구 상태를 `--state-file`로 넘기는 v2는
[역할 관계·직관 확장 기록](ICE_HSWM_RESEARCH_STATE_INTUITION_2026-09-08.md)을 따른다.
v2는 별도 manifest와 SQLite를 사용하고, 실제 domain/map/obstruction 상태에 따라
중첩된 검토 셀을 선택한다. 아래 v1의 두 경쟁 경로와 v2의 상호 배타적 조건 경로를
같은 학습 검증으로 해석하지 않는다.

ICE program manifest는 `config/hswm-research.v1.json`이며, HSWM의 선언 schema는
`hswm-adaptive-program/v1`이다. 실행 상태는 저장소 밖의 전역 상태가 아니라
`.ice/hswm-research/runtime.sqlite3`에만 지속한다. 이 SQLite 기록은 episode, 선택한
route, 비용·성공/유용성 feedback을 보존한다. Git evidence artifact나 외부 KG write가
아니다.

실제 runtime 호출은 sibling checkout을 project로 지정한다.

```bash
# HSWM runtime의 직접 호출 형태. CONTEXT_JSON/TASK_JSON은 CLI가 만든 JSON 입력이다.
uv run --locked --no-sync --project "$ICE_HSWM_ROOT" hswm-live \
  --program config/hswm-research.v1.json \
  --state .ice/hswm-research/runtime.sqlite3 \
  --workspace . run \
  --context "$CONTEXT_JSON" --task "$TASK_JSON" --budget 600
```

기본 sibling root는 `../HSWM`이다. 위치가 다르면 `ICE_HSWM_ROOT`를 지정한다.
HSWM checkout을 수정하거나 ICE의 package dependency로 복사하지 않는다.

## ICE 연구 인터페이스

질문과 대상·참조는 ICE CLI가 고정하고, manifest command cell은 인증된 Codex CLI를
비대화식으로 호출해 formulation, adversarial reading, synthesis를 수행한다. Codex의
비대화식 호출 방식은 [official Codex noninteractive documentation](https://developers.openai.com/codex/noninteractive)를
따른다. credential은 manifest나 result에 쓰지 않는다.

```bash
./ice research plan "QUESTION" \
  --target cpt::node-id \
  --reference relative/path [--reference relative/path ...] \
  --mode investigate|review|compute \
  --tier supporting|core \
  [--runner runner-name] --budget 600 --json

./ice research run "QUESTION" \
  --target cpt::node-id \
  --reference relative/path [--reference relative/path ...] \
  --mode investigate|review|compute \
  --tier supporting|core \
  [--runner runner-name] --budget 600 --json

./ice research state --json
./ice research graph --json
./ice research feedback EPISODE --useful true|false --source "rationale" --json

# 선언적 supporting pilot: 실행 성공이나 과학적 결론을 뜻하지 않는다.
./ice research run "relative primary boundary reduction의 quantum boundary-state 입력을 반증 우선으로 검토한다" \
  --target cpt::open:starobinsky-seam-ward-boundary-state-limit \
  --reference cpt_temporal_folded_susy/STAROBINSKY_RELATIVE_PRIMARY_BOUNDARY.md \
  --mode investigate --tier supporting --budget 600 --json
```

`--source`는 ICE prefix를 제외한 228자 이내의 검토 근거다. USL에서 관측한 참조 파일의
내용 hash는 LLM 셀에서 다시 비교하며, 변경된 입력은 거부한다.

`--runner`는 `compute` mode에서만 허용한다. compute cell은 이름이 지정된 clean,
committed ICE runner를 명시적으로 `./ice run <runner>`로 호출한다. HSWM의 600초
route budget은 과학 runner의 기존 공통 실행 상한을 넓히지 않는다. core tier는
기존 `./ice agent plan`의 blocker·typed-object 검토와 모든 ICE governance를 우회하지
않는다.

`investigate`에는 같은 references에서 출발하는 두 route가 있다.

- **proposal-first**: `references → formulate → adversary → synthesize`
- **falsifier-first**: `references → adversary → formulate → synthesize`

`review`는 이미 선언된 질문·입력·주장을 읽어 반례와 scope를 검토하는 route다.
`compute`는 review 가능한 proposal을 runner 입력으로 구체화한 뒤에만 위의 명시적
실행 cell을 사용한다. 어느 route도 다음 질문, 계산, claim 승격을 자동 승인하지 않는다.

LLM cell의 문장은 제안이다. command exit, route score, 또는 `--useful`은 scientific
truth label이 아니다. [실제 4-cell 회차와 피드백 검증](ICE_HSWM_RESEARCH_PILOT_2026-09-08.md)에
실행 결과, 실제 연구 제안, 초기 연결 실패와 수정의 범위를 기록했다.

## Feedback의 한계

HSWM feedback은 선택한 context에서 relation/route의 유용성·비용 추정을 갱신한다.
이는 local adaptive relation estimate이지 neural weight training, full world model,
인과 검증, 혹은 HSWM의 대형 정체성 검증이 아니다. 모델의 유용성이나 full-world-model
성립은 이 feedback만으로 검증되지 않는다. `--useful`의 source rationale은 사용자 또는
agent review가 기록한 routing 판단의 provenance다. output이 유용했다는 label은 해당 proposal의
물리적 참이나 target claim의 evidence가 되지 않는다.

실행된 과학 계산의 정본은 여전히 해당 raw `RESULT.json`의 command·환경·checks와
인접 보고서다. HSWM SQLite state는 workflow provenance이고, ontology evidence edge를
대체하지 않는다. G1 original-cycle, CPT seam, physical state, G1–G5 또는 TOE의 지위를
이 설정만으로 바꾸지 않는다.

## USL의 남는 역할

USL은 HSWM을 대신해 연구를 수행하지 않는다. 기존 `./ice research prepare` reference helper와
`./ice research status`는 target, role-bearing reference, source locator와 가용성을 읽는
문맥 인터페이스로 유지한다. `../USL` 위치가 다르면 `ICE_USL_ROOT`를 지정한다.

USL observation·digest는 입력 파일과 로컬 node 표현이 그 시점에 읽혔음을 나타낼
뿐이다. 외부 resolver, 외부 KG 등록, semantic truth 판정, 실행 허가를 만들지 않는다.
USL v2 adapter/status는 선택적인 context helper이며 HSWM feedback이나 ICE claim을
자동으로 갱신하지 않는다.

## 구현 출처와 적용 범위

- HSWM runtime schema·routing·SQLite feedback: sibling
  `HSWM/src/hswm/cells/adaptive_runtime.py`와
  `HSWM/src/hswm/infrastructure/adaptive_cli.py`.
- command-cell 실행 및 bounded output: sibling
  `HSWM/src/hswm/cells/adaptive_executor.py`.
- HSWM의 현재 구현과 검증 범위: sibling
  `HSWM/README.md`, `HSWM/docs/canon/HSWM_CONSTITUTION_2026-08-20.md`.
- USL reference/status adapter: sibling
  `HSWM/docs/operations/HSWM_USL_ADAPTER_V2_2026-09-08.md`,
  `HSWM/src/hswm/infrastructure/usl_cli.py`,
  `HSWM/src/hswm/infrastructure/usl_adapter.py`.
- Codex noninteractive command use:
  [developers.openai.com/codex/noninteractive](https://developers.openai.com/codex/noninteractive).

이 문서는 local research routing의 적용 범위만 선언한다. source-defined joint relative
class, quantum cycle, analytic domain, physical Hilbert space, full 3+1 closure와 외부
과학 검토는 각각 남아 있는 별도 문제다.
