# HSWM 실제 연구 회차 연결 검증

2026-09-08 · 로컬 연구 런타임의 공학적 검증 · 과학적 claim 변경 없음.

HSWM이 USL 참조 셀과 실제 Codex LLM 셀 세 개를 호출하고, 선택한 연구 경로에 대한
명시적 검토 피드백으로 relation 모델을 갱신했다. 아래 원문은 모델이 만든 연구 제안이며
새로운 양자 연산자나 과학적 증명을 구성한 산출물로 승격하지 않는다.

## 실제 실행

```bash
./ice research run "고전적 두 primary 경계 축약을 실제 양자 경계 연산자로 연결하기 위해 먼저 검증할 하나의 반증 가능한 조건을 정하고, 두 축약이 동등하다는 가정의 반례를 검토하라." \
  --target cpt::open:starobinsky-seam-ward-boundary-state-limit \
  --reference cpt_temporal_folded_susy/STAROBINSKY_RELATIVE_PRIMARY_BOUNDARY.md \
  --mode investigate --tier supporting --budget 600 --json
```

- Episode: `5bd65732-76bd-417b-84db-93b6ec1431b2`.
- 선택 경로: `relation:falsifier-first`; references → adversary → formulate → synthesize.
- 실제 leaf call: 4; 실행 결과 `SUCCEEDED`, 229.747초.
- 실행 직후 연구 유용성 값: `success: null`. Exit 0으로 route에 자동 보상을 주지 않았다.
- USL: 선언·관측 자원 3개, resolver call 3회, 거부 0개; HSWM reference adapter `READY`.
- 모델 포트: 설치된 Codex CLI 0.153.4, 실제 로그에서 gpt-6-astra / low / read-only 확인.
  모델·reasoning 옵션을 이 프로그램이 별도로 덮어쓰지 않는다.
- Manifest SHA-256: `02e5477532f8ed16ec1b8c02827260bc89fb67aab551fa40cd745b70741a6a79`.
- 참조 문서 SHA-256: `a3120fbebe45bfa862c5aa6f6e7c718ab12b2b3e68d86296641f0562af0ff726`.
- 아래 synthesis 원문 SHA-256: `53769049e6f3d7404cef5b16c92d2ab9a9c9cfd9893ff0ac3d1ae955abe97d2d`.

로컬 raw 기록은 `.ice/hswm-research/episodes/5bd65732-76bd-417b-84db-93b6ec1431b2/`의 invocation, references, 각 셀 JSON/Markdown과 runtime.json에
있다. HSWM SQLite는 `.ice/hswm-research/runtime.sqlite3`다. 이 로컬 상태·인증·캐시는
Git에 넣지 않으며, 다른 checkout은 manifest로 새 상태를 만든다. LLM 출력은 결정론적 재현을
약속하지 않는다. 이 문서는 공유 가능한 실행 요약과 실제 종합 원문을 보존한다.

## 검토와 실제 피드백

원문과 고전적 축약 보고서를 대조한 별도 agent 검토는 정의역을 포함한 chain-map 조건을
선명하게 만들었다는 점에서 유용하다고 판단했다. 반례는 C∞/Cc∞ primary toy complex이며,
실제 M/P 양자화의 비동등성이나 기존 finite/compact-N carrier의 no-go가 아니다. 실제 검사는
측도·topology·잔여 sector와 구체적 U_M/U_P를 선언해야 한다.

```bash
./ice research feedback 5bd65732-76bd-417b-84db-93b6ec1431b2 --useful true \
  --source "Agent review: useful domain-aware chain-map falsifier and missing U_M/U_P; compact-support example stays a toy countermodel. No actual quantum reduction or G1 evidence." --json
./ice research state --json
```

실제 응답은 `FEEDBACK_RECORDED`와 `WEIGHTS_UPDATED`다. 여기의 weights는
HSWM relation 선택 모델의 추정 계수이며 LLM 신경망 가중치가 아니다.
`relation:falsifier-first`는 revision 1 → 2, observations 0 → 1로 바뀌었다.
같은 mode/graph/tier에서 다시 plan을 조회하자 선택은 `relation:proposal-first`로 바뀌었다.
이 조회는 다음 회차를 실행하지 않았다. 한 번의 feedback으로 얻은 모델 점수는
보정된 과학적 확률이나 연구 성능 개선의 측정값이 아니다.
현재 runtime에는 21개 event, 실패 회차 1개와 feedback 기록 회차 1개가 있다.
유용성 피드백은 성능 향상이나 독립적인 인과 효과의 검증이 아니다.

## 관측한 실패와 검증 범위

- 첫 참조 시험은 초 단위 시각 절삭 때문에 같은 초의 밀리초 관측을 FUTURE_TIMESTAMP로
  오판했다. 소수초를 보존한 뒤 실제 adapter READY와 시각 회귀 테스트를 확인했다.
- 첫 episode `e6f710c0-fb51-4351-a623-c8ab67e88b42`는 LLM 포트가 열린 stdin의 EOF를
  기다려 180초 timeout으로 실패했다. 명시적 빈 입력으로 EOF를 보낸 뒤 짧은 실제 호출과
  위 4-cell 회차가 완료됐다. 첫 실패는 SQLite에 남기고 과학적 실패 보상을 주지 않았다.
- 긴 feedback source는 HSWM의 256자 계약에 걸려 거부됐다. ICE prefix를 포함하도록
  입력 상한을 맞춘 뒤 위 feedback이 실제로 기록됐다.
- USL 관측 후 파일 내용이 달라지는 경우의 거부 control은 잘못된 hash를 넣은 로컬 fixture로
  검사했다. 실제 셀이 LLM 호출 전에 exit 1과 `reference changed since USL observation`을
  반환했다. 이 guard와 문맥 status의 선두 배치는 별도 최종 패치이며 위 LLM 회차 원문을
  재생성하지 않았다.
- `npm run graph:release-check`: 통과(32개 test file, 170개 test; graph·coverage·advisory·SBOM).
  마지막 입력 guard·feedback 상한 패치 뒤 `npm run check`도 32개 file/170개 test를 통과했다.
- `./ice ontology review --graph all --base HEAD --json`: warning 0; 기존 정책 hash와 날짜만 변경.
  `./ice graphrag diff --base HEAD --limit 12 --json`: retrieval/routing 이동 0.
  `./ice harness check --json`: valid, hash 544개 확인.

과학 runner를 이 연결 시험에서 실행하지 않았다. compute mode의 실제 과학 결과,
Lean 증명, 양자 접합, Gate 1과 TOE의 진전은 이 검증 범위 밖이다. 이 실행은 준비한
context에서 연구 문장을 만들고 검토 피드백을 기록하는 로컬 기능을 검증했다.

## 실제 synthesis 셀 원문 — 검토용 제안

먼저 검증할 조건은 **두 고전적 축약에서 유도한 양자 후보 사상이, 선언된 정의역에서 BFV 미분과 호환되는가**이다. 이는 양자 경계 연산자로 연결하기 위한 필요조건이며, 두 축약의 양자적 동등성을 보장하는 충분조건은 아니다.

대상은 `cpt::open:starobinsky-seam-ward-boundary-state-limit`이고 범위는 `SUPPORTING_METHOD`다. 제공된 참조·packet·이전 출력은 문맥으로만 사용한다. 기재된 실행, 검사 및 증명 상태는 독립적으로 확인하지 않았다. 이 메모에서는 도구 실행이나 파일 수정·커밋·푸시를 하지 않았다.

**확정된 입력과 조건부 출발점**

이번 요청에서 확정된 것은 대상 질문과 supporting 범위다. 고전적 계산에 관해서는 참조가 다음 자료를 제시한다.

\[
M:\Pi=\bar c=0,\qquad P(N_0):N=N_0,\rho=0,
\]
\[
\Omega_{\rm ext}=cH_L+\rho\Pi,\qquad
QN=-\rho,\quad Q\bar c=\Pi.
\]

참조는 두 관계가 각각 허용 변분, 상대 경계항 소거, \(Q\)-접선성을 만족하며, 특성 방향을 몫내면 공통 자료
\[
(\mathcal B_{\rm red},\alpha_{\rm red},\Omega_{\rm red}),
\qquad \Omega_{\rm red}=cH_L
\]
를 얻는다고 보고한다. 여기서는 이를 **후보 구성의 조건부 고전적 입력**으로 둔다. 고전적 몫의 일치는 양자 상태 공간, 측도, 연산자 정의역 또는 내적의 일치를 뜻하지 않는다. Matter 제약도 제거된 것으로 취급하지 않는다.

제공된 그래프 상태 문자열은 관련 문제의 위치를 알려주는 색인이다. 특히 문맥의 evidence 목록이 비어 있고 일부가 잘렸으므로, 이를 완전한 근거 목록이나 추가 검증으로 사용할 수 없다.

**검증할 가설 하나**

가설은 다음과 같다.

> 고정된 양자화 자료에서 각 고전적 축약 관계를 구현하는 비자명한 degree-zero 사상 \(U_M,U_P\)를 구성할 수 있으며, 두 사상 모두 정의역을 포함한 BFV chain-map 조건을 만족한다.

이를 검증하려면 먼저 다음 typed object가 필요하다.

| 구분 | 필요한 객체 |
| --- | --- |
| 원천과 목표 | Graded 상태 공간 및 불변 정의역 \(D_X^\bullet,D_{\rm red}^\bullet\), \(X=M,P\) |
| 양자 미분 | 정의역을 보존하고 그 위에서 제곱이 영인 \(\widehat\Omega_X,\widehat\Omega_{\rm red}\) |
| 축약 후보 | 고전적 관계와 kernel 또는 작용 규칙의 대응을 명시한 \(U_X\) |
| 해석학적 자료 | Polarization, 측도·half-density, ghost convention, 연산자 순서, 잔여장·gauge-fixing, 끝점 조건과 topology |
| 결함 검출 | 목표 공간의 비영 원소를 구별하는 시험 쌍대공간과 pairing |

양자 미분의 nilpotence와 불변 정의역은 이 질문을 복합체 사이의 사상 문제로 만들기 위한 전제다. 영사상이나 고전적 관계와 무관하게 선택한 사상은 가설의 후보가 아니다.

첫 검증 조건은
\[
U_XD_X^k\subseteq D_{\rm red}^k,\qquad
\Delta_X\psi
:=\widehat\Omega_{\rm red}U_X\psi
-U_X\widehat\Omega_X\psi=0
\quad(\psi\in D_X^\bullet)
\]
이다. \(U_X\)의 degree가 0이므로 위 부호를 쓴다.

**반증자와 판정**

허용 상태 \(\psi\) 하나에서 정의역 포함이 실패하거나, 허용 시험 원소 \(\eta\)에 대해
\[
\langle\eta,\Delta_X\psi\rangle\ne0
\]
이면 해당 후보와 정의역의 조합은 반증된다. 분포값 사상이라면 분포 목표 공간과 미분, pairing을 처음부터 선언해야 한다.

권고하는 출력은 후보별 근거를 담은 **비교 기록 하나**다.

- `FAIL`: 명시적 정의역 이탈 또는 비영 결함을 제시한다.
- `PASS_ON_DECLARED_DOMAIN`: 전체 선언 정의역에서 조건이 성립하는 근거를 제시한다.
- `UNRESOLVED`: 객체가 빠졌거나 전체 정의역을 판정할 근거가 부족하다.

유한한 시험 상태에서 결함을 찾지 못한 결과는 전체 정의역의 통과가 아니다. Regulator가 필요하면 제거 극한의 topology와 합성 연산자의 극한 존재도 명시해야 한다. 또한 \(\Delta_X\)를 대상 노드의 Gaussian seam Ward 결함과 동일시하려면 실제 연산자·pairing 사이의 연결식이 필요하다.

**자동 동등성 가정에 대한 반례**

양의 lapse 구간 \(I=(0,\infty)\)에서 \(\deg\rho=1\)이고
\[
qf=-\rho f',\qquad q(\rho g)=0
\]
인 두 항 복합체를 생각하자. 이는 실제 \(M,P\)의 양자 연산자를 구성한 결과가 아니라, primary 방향이 자동으로 제거된다는 추론을 시험하는 모형이다.

모든 매끄러운 계수를 허용하면
\[
C^\infty(I)\xrightarrow{q}\rho C^\infty(I)
\]
에서 \(H^0\simeq\mathbb C,\ H^1=0\)이다. 상수는 닫혀 있고 모든 매끄러운 함수는 이 구간에서 매끄러운 원시함수를 갖는다.

반면 두 degree 모두 compact support를 요구하면
\[
C_c^\infty(I)\xrightarrow{q}\rho C_c^\infty(I)
\]
에서 \(H^0=0,\ H^1\simeq\mathbb C\)이다. 적분이 1인 compact-support bump \(g\)를 택하면 \(\rho g\)는 닫혀 있지만 exact하지 않다. 실제로 \(\rho g=qf\)인 compact-support \(f\)가 있다면
\[
1=\int_Ig\,dN=-\int_If'\,dN=0
\]
이라는 모순이 생긴다. 적분이 영인 compact-support 함수에는 compact-support 원시함수가 있으므로 \(H^1\)은 정확히 한 차원이다.

목표를 degree 0의 \(\mathbb C\), 미분 0으로 놓은 점 평가
\[
E_{N_0}(f)=f(N_0),\qquad E_{N_0}(\rho g)=0
\]
는 두 경우 모두 chain map이다. 그러나 compact-support 경우에는 비영 \(H^1\)을 소실시키고 \(H^0\)에서도 동형을 만들지 못하므로 quasi-isomorphism이 아니다.

따라서 **chain-map 조건을 통과해도 동등성은 실패할 수 있다.** 이 반례는 지지 조건이 다른 복합체를 비교한다. 실제 \(M,P\)가 각각 이 공간을 택한다는 근거는 없으므로 실제 두 축약의 비동등성을 확정하지 않는다. 반박되는 것은 고전적 축약만으로 양자 동등성이 자동으로 따라온다는 일반 추론이다.

**권고하는 다음 작업과 남는 경계**

다음 작업은 선언된 고전적 관계에 대응하는 **실제 양자 축약 사상 한 쌍과 그 정의역을 명세하고, 위 조건의 반증자를 찾는 것**으로 한정한다. 주 실패 원인은 `inference`이며 통제는 세 가지에 집중한다.

- 점 평가는 일반 \(L^2(I,dN)\) 동치류에서 정의되지 않는다. 평가 가능한 정의역과 BFV 불변성을 함께 확인한다.
- 적분형 후보는 적분과 끝점 극한이 존재할 때의
  \[
  \int_0^\infty -f'\,dN=f(0^+)-f(\infty)
  \]
  를 포함해 검사한다. 비상수 측도와 ghost 부호도 반영한다.
- Chain-map 성립과 cohomology 동형을 구분한다. 기존 \(R_N,J_\chi,K_\chi\)나 compact-\(N\) 결과를 이전하려면 실제 비교사상이 필요하다.

현재 제공 자료만으로는 필요한 양자 사상·정의역이 확보되지 않아 판정은 `UNRESOLVED`다. 이후 첫 조건을 통과해도 cohomology 동등성, 내적·관측가능량 보존, 허용 경계 상태에서의 Ward 극한 및 CPT 접합은 남는다.

이 권고는 source-defined joint relative class, 완전한 saddle/sheet/singular·Stokes/good-end census, oriented global intersection vector와 안정성을 제공하지 않는다. 따라서 G1/core 병목과 종료 조건은 유지된다. 실패의 범위도 선언한 양자 후보와 정의역에 한정하며, 결과 자체가 후속 계산이나 범위 확대를 자동 승인하지 않는다.
