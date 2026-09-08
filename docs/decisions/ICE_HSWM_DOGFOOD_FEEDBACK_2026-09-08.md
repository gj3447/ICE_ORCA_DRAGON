# HSWM을 사용하면서 구현·검증·피드백하기

2026-09-08 · `SUPPORTING_METHOD` / 구현 검증.

사용자 요청은 완성된 HSWM을 기다리는 것이 아니라, ICE 연구를 실제 소비자로 삼아
부족한 구현을 찾아 고치고 관측한 결과를 돌려주는 것이다. 이번 작업은 native
TypeScript/Effect runtime으로 연구를 연결하고, 실제 실패 두 건의 수정과 검증을
수행한다. 연구 유용성, 실행 품질, 과학적 참은 별도로 기록한다.

## 실사용에서 확인한 결함과 수정

| 관측 | 원인 | 적용한 수정과 검증 |
| --- | --- | --- |
| 기존 이력 조회는 성공하지만 학습한 root route로 실행하면 `adaptive model`, exit 2 | native 학습기가 여섯 문맥 field에서 1054자 attempt key를 만들고 검증기는 256자 제한으로 거부 | 생성 가능한 feature 계약에서 유도한 attempt-key 상한으로 수정. 원본 실패, 수정 후 반복 update/predict, 짧은 문맥 parity와 상한 초과 거절 확인 |
| 다음 실제 실행의 references cell이 `/dev/stdin`의 `ENXIO`, exit 1 | ICE가 Node child의 socket stdin을 파일로 다시 열려고 함 | 실제 `process.stdin` stream을 제한된 크기로 읽도록 수정. spawned Node Socket 입력과 초과 입력 거절 검사 |

첫 실패 episode는 `4a9a7b51-d6e6-4698-8c84-daeac8a790ca`, 두 번째는
`2299a1da-8ca6-4014-9c39-45feba775093`이다. 각 `.ice/hswm-research/episodes/<id>/`
디렉토리에 invocation과 원래 stdout/stderr를 보존했다. 첫 오류는 episode가 native
DB에 만들어지기 전 발생했다. 두 번째 오류는 실제 references/root 실패 trajectory를
남겼다. 이 실패에 연구 유용성 true/false를 꾸며 넣지 않았다.

HSWM 원본 checkout에는 다른 작업의 변경이 진행 중이었다. 그 변경을 보존하면서
[upstream patch와 피드백](../../research/hswm/upstream/README.md)을 ICE에 추적하고,
무시되는 `.ice/hswm-research/native/`에 만든 검증본으로 실제 연구를 진행했다.
**수정본은 로컬 적용 상태이며 HSWM upstream에 merge한 상태가 아니다.**

## 실행본과 재현

ICE `research run/plan/state/graph/feedback/intuition`은 이제 Node로 native
`hswm-live-process.js`를 호출한다. v1/v2 SQLite 경로를 유지해 기존 연구 이력을
보존했다. Python은 USL adapter와 과거 비교 도구에 남는다. 이력 조회의 성공만으로
전체 호환성이 검증됐다고 쓰지 않는다.

검증본을 다시 만드는 명령은 다음과 같다. output은 아직 존재하지 않는 디렉토리여야 한다.

```bash
node scripts/qualify-hswm-context-key.mjs \
  --hswm-root ../HSWM --output .ice/hswm-research/native/context-key-qualification
node scripts/check-hswm-context-key.mjs \
  --original-js ../HSWM/src/hswm/effect-runtime/dist/adaptive-domain.js \
  --patched-js .ice/hswm-research/native/context-key-qualification/dist/adaptive-domain.js
# PASS를 검토한 뒤 이 로컬 실행본을 선택한다.
cp .ice/hswm-research/native/context-key-qualification/native-entry.candidate.json \
  .ice/hswm-research/native-entry.json
./ice research status --json
```

qualification은 검토한 patch hash와 원본의 patch 문맥을 요구하며 불일치하면 중단한다.
생성한 candidate는 원본/수정 source·compiled hash, patch hash, TypeScript 버전과
실행에 관련된 JS 8개 pin을 보존한다. 수정한 `adaptive-domain.ts`를 strict 옵션으로
컴파일하고 의존 declaration 검사는 `skipLibCheck`를 사용한다. 다른 native 파일은
설치된 dist에서 복사하므로 전체 HSWM source-build 동등성 검증이 아니다.

실제 사용한 검증본은 `context-key-qualification-20260908-r2`다. 수정한 domain JS
SHA-256은 `b2f5dbfcffeb007a02dcc92a672096364aaadc22e7763d8019c8a3e83b35a8c6`이다.
`research status`와 episode invocation은 실행 entry, 원본 interface hash와 로컬 pin을
기록한다. pin 불일치는 실행 전에 거부한다. 명시적 `ICE_HSWM_NATIVE_ENTRY` override는
별도로 표시하며 동일한 qualification을 받았다고 추정하지 않는다. DB·복사한 dist·
node_modules·cache는 Git에 넣지 않는다.

## 피드백이 실제로 도달하는 범위

현재 native `feedback --episode`는 root trajectory만 찾아 해당 relation을 갱신한다.
실제 snapshot에서 `--trajectory`를 전달하면 unknown option, exit 2다. 따라서 root의
좋은 결과를 내부 모든 분기의 학습으로 해석할 수 없다.

새 `./ice research review <review-file> --json`은 검토자가 지정한 episode·stage·
trajectory를 관측한 runtime과 대조하고, 실제 출력 bytes SHA-256을 검사한다.
동일 ID의 같은 기록은 멱등적이고 충돌한 기록은 거부한다. 영수증은
`LOCAL_STAGE_REVIEW_RECORDED` / `NOT_SUBMITTED`로 남아 native 내부 분기에 아직
전달하지 않았음을 드러낸다. agent 평가는 `author=agent`, `source=codex`다.

기존 P(N0) 회차의 domain과 synthesize 출력을 다시 검토해
[단계별 기록](../../research/hswm/reviews/) 두 개를 실제 artifact와 대조해 저장했다.
native root feedback의 source에도 `agent(codex)`를 명시한다. 이러한 유용성 label은
proposal의 과학적 참, 새로운 관계 의미의 학습 또는 KG 대비 성능 우위가 아니다.

반영할 upstream 기능은 실제 nested trajectory에 대한 명시적 평가를 그 출력 hash와
함께 받는 것이다. 필요한 입력·거부 조건·회귀 범위는 upstream 메모에 적었다.
관계 분화를 보이려고 합성 문맥이나 성공·실패를 실제 연구 label로 제출하지 않는다.
합성 입력은 context-key 구현 회귀에만 쓰며 실제 연구 DB를 학습시키지 않는다.

## 실제 boundary 연구 소비자

이번 supporting 질문은 M의 고전적 `Π = bar c = 0`을 특정 연산자 표현의 공동 kernel로
옮기는 후보다. compact-N collar, 적분 contraction의 차수 이동, named graded dual의
검출기를 함께 보며 후보가 실패할 조건을 구체화한다. source에서 양자 tuple이
도출됐거나 물리 CPT 접합이 완성됐다는 주장을 하지 않는다.

```bash
./ice research run 'M:Pi=bar c=0 고전적 경계축약을 p=-i d_N, bar c=i d_rho의 공동 kernel로 구현하는 후보를 공격하라. compact-N collar에서 그 kernel이 자명한지 확인하고, 기존 적분 contraction의 차수 이동과 비교하라. named graded-dual carrier로 옮길 때 같은 top detector와 BFV 사상을 보존한다고 말하려면 정확히 어떤 추가 입력이 필요한가? 하나의 판별식과 실패 증인을 제안하되 source-derived 양자화나 물리 CPT를 주장하지 말라.' \
  --target cpt::open:starobinsky-seam-ward-boundary-state-limit \
  --state-file research/hswm/primary-boundary-state.v1.json \
  --reference cpt_temporal_folded_susy/STAROBINSKY_RELATIVE_PRIMARY_BOUNDARY.md \
  --reference cpt_temporal_folded_susy/STAROBINSKY_PRIMARY_REDUCTION_DERIVATION.md \
  --reference cpt_temporal_folded_susy/STAROBINSKY_GRADED_DUAL_SEWING_DERIVATION.md \
  --mode review --tier supporting --budget 600 --json
```

Episode `15218ec9-ad22-4e48-9f57-056158ef70ae`는 exit 0, `SUCCEEDED`다.
native root duration은 255.378초, ICE에서 관측한 외부 wall time은
255.79390636600002초였다. 실행한 leaf 3개는 `references`, `domain`, `synthesize`이고
router 포함 trajectory는 5개다. root 선택은 `relation:research-with-state`, 내부는
`relation:declare-domain`이었다. 실행 결과의 `success`는 null로 유지됐다.

[최종 모델 제안 원문](../../research/hswm/primary-boundary-m-pilot-proposal.v1.json)의
SHA-256은 `1efb0e0cd26896016940c60d903e043ce5961506aa9b32739fcad8f68e3c531e`다.
raw prompt, 참조 준비, 개별 stage와 실패는 해당 로컬 episode에 보존한다.
이 원문은 LLM 제안이며 과학 계산 RESULT나 재현 가능한 seed 평가가 아니다.

기존 유도와 별도로 대조한 판단은 다음과 같다.

- 이 공간의 `pψ=0`은 각 계수를 N-상수로 만든다. 끝 근방의 소멸 조건이 그 상수를
  0으로 강제하므로 `ker p=0`, 따라서 공동 kernel도 0이다. 이 뒤 bar c 조건은 중복이다.
- `R_N p=0`, `Kχp=1`, `pKχ=1−JχR_N`인 적분 contraction은 kernel 대신 cokernel을
  남긴다. 축소 복합체는 차수 1,2에 놓인다. 고전적 coisotropic quotient를 이 두 양자
  후보 중 하나와 식별하려면 별도 source 대응이 필요하다.
- 연속 detector `t_g H=0`과 실제 허용 `v`의 `t_g(v)=1`을 확보하면, top **상태**
  `cρ Jχv`의 detector 결함은 적분 비교에서 0, 영공간 target에서 −1이다. 모델의
  `z=Jχv`는 top 계수를 나타내는 표기로 읽는다. 임의의 bump가 검출되는 것은 아니다.
  이번에는 seed를 평가한 새 계산을 실행하지 않았으므로 이 값들은 조건부 예상값이다.
- 차수를 반전한 연속 dual의 `Fᵗt_g=T_g`는 dual 사이 전달이다. primal과 dual의
  동일시, 양의 내적 또는 물리 CPT를 제공하지 않는다. synthesize의 반복은 domain의
  독립적인 수학 증거로 세지 않는다.

domain과 synthesize 모두 이 제한된 질문을 구체화하므로 agent 유용성은 `useful`로
평가했다. 두 [실제 단계별 검토 파일](../../research/hswm/reviews/)을 `research review`로
대조해 저장했고, 다음 root feedback을 실제 native DB에 전달했다.

```bash
./ice research feedback 15218ec9-ad22-4e48-9f57-056158ef70ae --useful true \
  --source '선언한 collar에서 공동 kernel 소실과 적분 cokernel을 구별하고 차수·detector 비교 조건을 명시해 유용함. 원문 대조한 조건부 제안이며 seed 계산·물리 CPT 검증은 아님.' --json
./ice research graph --profile v2 --json
```

native 응답은 `FEEDBACK_RECORDED`, `WEIGHTS_UPDATED`였다. 여기의 weights는 로컬
route estimate다. `research-with-state`의 관측 수는 1→2, revision은 2→3이 됐다.
내부 `declare-domain`은 관측 수 0, revision 1 그대로다. 같은 여섯 field로 native
root `plan --cell researcher`를 다시 조회해 exit 0과 observations 2를 확인했다.
수정한 모델로 **연구 실행→실제 평가→갱신된 모델의 다음 조회**까지 통과했다.
상호 배타적인 guard의 선택이므로 이 사실은 학습이 경로 선택을 개선했다는 비교 검증이 아니다.

## 검증과 완료 범위

`npm run graph:release-check`가 통과했다: strict typecheck, 37개 파일의 192개 테스트,
graph·SHACL·competency·GraphRAG·agent 검사, coverage, production dependency audit와
SBOM 검사다. synthetic context-key 회귀는 별도로 원본 실패와 수정본 통과를 확인했다.
`ontology review --graph all --base HEAD`는 정책 hash/시각 외 과학 graph 변경이 없음을
보였고, `graphrag diff --base HEAD --limit 12`의 15개 사례에서 순위·판정은 바뀌지 않았다.
`harness check`는 hash 544/544, 오류 0이며 기존 경고 75개를 보고했다.

이 작업은 지원 연구를 사용하는 인터페이스와 피드백을 검증했다. G1 지위나 과학적
claim·scope를 바꾸지 않았으므로 새 ontology evidence나 repro manifest를 만들지 않았다.
HSWM 관계 발명이나 새 물리의 완료는 이 실행과 구분한다.
