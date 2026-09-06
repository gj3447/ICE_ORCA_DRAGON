# Starobinsky 연속 constrained endpoint map: 국소 해 인증

2026-09-06. 지위: **SUPPORTED / SUPPORTING_METHOD**.
소스 실행 기준: `1d2c63c0f3fdb0a0a02ca99f04e44bb67058bb75`.

**결론:** 선언한 정확한 경계값과 작은 3차원 shooting box 안에 연속 constrained
endpoint map의 **유일한 regular 실수 root가 존재한다**. CAPD의 validated C1 flow로
함수와 미분을 감싼 뒤, 엄격한 Krawczyk inclusion과 weighted defect norm `<1`을
확인했다. 이는 이전의 근사 shooting root를 국소 인증으로 보완한 결과다.
exact discrete action, gauge-preserving element, quantum measure 또는 original
integration cycle을 구성한 결과는 아니다.

## 질문·입력·출력

질문은 [앞선 문헌 보완 설계](ICE_CONTINUUM_CERTIFICATE_LITERATURE_SUPPLEMENT_2026-09-06.md)의
고정 boundary constrained shooting map 하나다. 양끝에 동일하게 부여하는 값은

```math
a_b=3.5668031935672753,\qquad \phi_b=1.0185809464006637.
```

이 두 **십진수 자체를 정확한 입력**으로 정의했다. Phase 24의 연속 참 경계값이
이 십진수와 정확히 같다는 주장은 하지 않는다. 입력 seed는
[Phase 24의 full Euler–Lagrange RHS와 shooting 구성](../../cpt_temporal_folded_susy/phase24_connected_starobinsky_interval.py)을
따른다. Phase 24의 DOP853/HYBR 근사 출력을 enclosure라고 취급하지 않았다.

미지수 `y=(u_-,v_-,T)`의 중심은 아래의 정확한 binary64 dyadic 값이다.
괄호의 십진수는 중심을 선택한 seed 문자열이며 물리적 참값이 아니다.

| 성분 | 정확한 중심 hex | 반지름 |
|---|---|---|
| `u_-` (`0.09984512855`) | `0x1.98f7349c983b4p-4` | `2^-24` |
| `v_-` (`-0.10663777161`) | `-0x1.b4c9ced955101p-4` | `2^-24` |
| `T` (`0.7`) | `0x1.6666666666666p-1` | `2^-20` |

정확한 box는 `X=c+[-r,r]`다. 입력 정본은
[INPUTS.json](../../cpt_temporal_folded_susy/STAROBINSKY_CONTINUUM_ENDPOINT_CERTIFICATE_INPUTS.json),
실제 enclosure·certificate 정본은
[RESULT.json](../../cpt_temporal_folded_susy/STAROBINSKY_CONTINUUM_ENDPOINT_CERTIFICATE_RESULT.json)이다.
후자의 `certificate.declared_box_exact_rational`과 `validated_flow.box`가 정확한
`X`를 기록한다. `constraint_gradient_arb_outer_enclosure`는 제약식 미분을 감쌀 때만
쓴 조금 더 넓은 보조 구간이다. 그 넓은 구간 전체의 flow derivative를 인증했다고
읽으면 안 된다.

## 연속 방정식과 인증 논리

`u=a'`, `v=phi'`, prime은 proper-time `tau` 미분이다.

```math
V(\phi)=\frac34(1-e^{-b\phi})^2,\quad b=\sqrt{2/3},
\qquad
f(a,u,\phi,v)=\left(u,\frac{1-u^2}{2a}-\frac{av^2}{4}-\frac{aV}{2},
v,V'-\frac{3uv}{a}\right).
```

`C=0`에서만 동치인 reduced scale acceleration으로 교체하지 않았다. 초기 box의
대부분은 off-constraint이므로 그 교체는 `DF`까지 다른 endpoint map을 만든다.
`s=tau/T ∈ [0,1]`, `z=(a,u,phi,v,T)`를 사용하여
`z_s=(T f,0)`와 `M_s=Dg M`, `M(0)=I_5`를 함께 감쌌다.

```math
C=u^2-1-\frac{a^2}{3}\left(\frac{v^2}{2}-V\right),\qquad
F(y)=\bigl(a(1;y)-a_b,\ \phi(1;y)-\phi_b,\ C(0;y)\bigr).
```

`[DF(X)]`의 첫 두 행은 box C1 flow의 rows `(0,2)`, columns `(1,3,4)`이며,
셋째 행은 `(2u_-,-a_b^2 v_-/3,0)`이다. 시간 미분을 빠뜨리지 않았다.
full RHS를 `C`에 대입해 미분하면 `C'=-(u/a)C`이고
canonical energy `E=-6 pi^2 a C`는 보존된다. 아래의 전 구간 `a>0`와 초기 `C=0`을 함께 쓰면
인증된 root의 연속 trajectory에서 제약이 유지된다. 이것은 이 방정식의 해석적
항등식이며 별도의 gauge/BRST 구조 인증이 아니다.

중심 함수값의 enclosure `[F_c]`, box 미분 enclosure `[J]`에 대해 고정 실수
점행렬 `B`를 선택했다. NumPy 역행렬은 `B`의 dyadic 원소 선택에만 쓰였고,
그 역행렬 계산의 정확성을 가정해 결론을 내리지 않았다.

```math
[K]=c-B[F_c]+(I-B[J])[-r,r]\subset\operatorname{int}X,
\qquad q=\|D^{-1}(I-B[J])D\|_\infty<1,\quad D=\operatorname{diag}(r).
```

이는 `y -> y-BF(y)`가 `X` 안으로 들어가는 수축임을 보인다. `q<1`은 `[J]`의
모든 행렬의 비특이성도 보장하므로, 존재와 box 안의 유일성에 더해 endpoint root의
regularity를 얻는다. full action Hessian의 비퇴화나 gauge-null mode 판정은 아니다.
사용한 방법의 1차 근거는
[CAPD 논문 §4.1–4.2](https://arxiv.org/html/2010.07097)와
[Rump Theorem 13.3](https://www.tuhh.de/ti3/rump/intlab/ActaNumerica2010.pdf)다.
이 논문들이 ICE-specific 결과를 제공하는 것은 아니다.

## 실제 certificate

아래 십진수 범위는 읽기 편하도록 raw exact rational K enclosure를 바깥으로
넓혀 쓴 값이다. 판정에는 이 표시값을 사용하지 않았다.

| root 성분 | 인증된 root를 포함하는 범위 |
|---|---|
| `u_-` | `[0.0998451285467, 0.0998451285511]` |
| `v_-` | `[-0.1066377716110, -0.1066377716089]` |
| `T` | `[0.6999999999894, 0.7000000000106]` |

- weighted defect norm 상한은 약 `0.00003633666835704215 < 1`이다.
- strict inclusion 여유/원래 반지름은 각각 약 `0.9999449997`, `0.9999824095`,
  `0.9999889557`이다. 포함 판정이 경계의 수치 오차에 가까운 경우는 아니다.
- 초기 box 전체의 trajectory tube에서 `a > 3.56680305`다. endpoint만의 양성
  검사가 아니라 모든 validated time piece의 hull이다. `T>0`도 성립한다.
- 중심의 endpoint residual은 대략 `(7.59e-13,-1.85e-14)`, 초기 constraint는
  `2.03e-13`이다. 이 작은 residual 자체가 인증 근거는 아니며 `[F_c]` 전체를
  포함 판정에 사용했다.
- Taylor order `20`, 각 flow 최대 `128` step을 고정했다. 실제 point/box flow는
  각각 `3` step, exact free-flow control은 `1` step으로 `s=1`에 도달했다.

raw 결과의 verdict는
`CERTIFIED_UNIQUE_REGULAR_REAL_CONSTRAINED_ENDPOINT_ROOT_IN_DECLARED_BOX`다.
실패 시 `INCONCLUSIVE`로 끝내도록 작성했으며, 결과를 보고 seed·box·precision을
바꾼 검색은 하지 않았다.

## 주된 실패원인과 사용한 control

주된 실패원인은 `solver`로 잡았다. 필요한 control은 세 묶음으로 제한했다.

1. **방정식·시간 미분 대조:** 해석적으로 쓴 초기 `Dg`의 25 entries와 CAPD AD
   enclosure의 overlap, point/box 두 flow에서 첫 네 성분의
   `partial_T Phi_T=f(Phi_T)` overlap을 확인했다. 후자는 8 entries다.
   overlap은 consistency check이며 넓은 구간에서 항등식을 독립 증명하는 검사는 아니다.
2. **정확한 C1 대조 문제:** `g=(Tu,0,Tv,0,0)`의 dyadic initial data를 사용했다.
   해석적 endpoint 5개와 전체 `5x5` sensitivity matrix 25개가 모두 enclosure
   안에 있다. `T` column을 포함한 30개 값이 통과했다.
3. **certificate 산술 재검산:** Arb 192-bit 연산의 strict inclusion을 Python
   `Fraction`의 정확한 유리수 구간 연산으로 다시 계산했다. 두 검산 모두 통과했다.
   이들은 같은 CAPD flow enclosure를 공유하므로 독립 ODE 구현 두 개의 재현은 아니다.

입력 일치, 모든 flow의 최종 시간, 전 구간 domain 조건도 실제 출력에서 통과했다.
CAPD의 `SolutionCurve<CurveT,true>`가 모든 겹치는 step을 hull한다는 API 의미는
고정한 공식 소스에서 확인했다. 검토 위치와 재구성 명령은
[CAPD build 기록](ICE_CAPD_CONTINUUM_BACKEND_BUILD_2026-09-06.md)에 남겼다.
binary64 interval C1 적분이며 CAPD multiprecision 적분이라고 서술하지 않는다.

## 실행·provenance·검토

```bash
ICE_CAPD_BVP_BINARY=/home/lagyeongjun/.cache/ice-capd/693998cd6d73a0c4e1b141bfb79fcad1c40c3cbe/ice-helper/starobinsky_continuum_endpoint_certificate \
  ./ice run starobinsky_continuum_endpoint_certificate
```

- 소스·입력·build pin을 `57f0f3e`로 먼저 commit하고 첫 계산을 실행했다.
  첫 실행도 certificate를 통과했다. 결과 검토에서 exact box와 Arb 보조 구간을
  구별하지 않은 field naming을 발견했다. `1d2c63c`에서 출력 schema만 바로잡은 뒤
  **동일 입력·동일 방정식·동일 box**를 위 명령으로 다시 기록했다.
- 두 실행의 `validated_flow`, exact rational `K`, exact rational `q`가 각각 완전히
  같음을 확인했다. 이 재기록은 repeatability이며 새로운 독립 evidence가 아니다.
  첫 출력 hash는 `a86e6ea9c454231488761496e86d65f37ccc6d7784a936f9b5d989de4dc5af9e`;
  첫 출력은 superseded 중간 산출물이며 최종 raw 파일을 단일 정본으로 둔다.
- 최종 raw SHA-256:
  `e007401f24694a2371ecd82231f5216e0d13ae88cd2c3c3a2ebe2fead4b9b75c`.
  runner/input/helper/binary/lock hash와 실제 backend argv는 raw provenance에 있다.
- Python `3.13.5`, NumPy `2.5.2`, python-flint `0.9.0`; CAPD official `v6.0.0`
  revision과 compiler/link flags는 input/build 기록에 고정했다. 캐시의 외부 binary와
  source hash가 맞지 않으면 실행기는 certificate를 내지 않는다.
- 최종 계산 본체의 기록 시간은 약 `0.044 s`, CAPD child는 약 `0.0093 s`다.
  이는 CLI 시작 시간과 dependency build 시간을 포함하지 않는다. child stdout
  `9,548 bytes`, stderr `0 bytes`, raw result `31,416 bytes`, exit code `0`을 관측했다.
- C++ compile, Python compile, 수식·C1 API·실제 출력의 별도 읽기 검토를 수행했다.
  이 검토는 외부 연구팀의 독립 구현·재현 심사를 대신하지 않는다.
- `./ice ontology validate`는 오류 없이 통과했고, `./ice harness check`는
  `470/470` artifact hash를 확인했다. 기존 외부 bridge 경고 75개는 남아 있다.
  `./ice ontology review --graph all --base HEAD`에서 새 CPT node 8개와 edge 12개만
  추가됐고 다른 graph의 의미 변경은 없었다.
- `./ice graphrag eval --limit 12 --json`은 `15/15`, `./ice agent eval --json`은
  `6/6` 통과했다. `./ice graphrag diff --base HEAD --limit 12 --json`에서 한 검색의
  부수 hit 목록이 바뀌었지만 expected locator의 1위, pass 및 boundary 상태는 같았다.
  `./ice ontology coverage --json`은 `746/746` files mapped, issue `0`이었다.
  이 검사들은 도구·검색 회귀 검사이며 위 수학적 certificate의 증명 근거가 아니다.

## G1에 남는 경계

사전 planner는 `INSUFFICIENT_ROUTE_EVIDENCE`였고 이 작업을 core-labelled 계산으로
승격하지 않았다. choice-invariance/cross-domain 경계도 먼저 읽었다. 여기서 바꾼
evidence는 `open:gate1-starobinsky-exact-gauge-preserving-element-source`를 검토할 때
사용할 수 있는 **한 국소 연속 branch와 regular endpoint map의 witness**뿐이다.

양끝값이 같다는 이유로 midpoint reflection symmetry를 인증하지 않는다. 좌표 시계,
FP determinant, exact composition, gauge-null mode, BFV kernel은 여전히 없다.
이전의 naive local-lapse 및 midpoint-HJ 반례를 뒤집지 않는다.

original cycle, 전역 saddle/sheet/singular·Stokes/good-end census, oriented global
intersection vector와 그 안정성도 여전히 필요하다. 실수 box의 유일성을 전역 유일성이나
복소 continuation으로 확대하지 않는다. `open:gate1-original-cycle-signed-global-intersections`
및 refined source open의 지위를 그대로 두고, ontology에는 이번 scoped claim/evidence만
연결한다. `G1 OPEN_PARTIAL_PROGRESS`, global promotion 금지 경계는 유지된다.

이번 결과만으로 다른 계산을 자동 시작하지 않는다. 후속 후보를 정할 때 확인할 과학적
장애물은 이 branch로부터 필요한 source object를 실제 정의할 수 있는지이며,
동일 shooting box를 더 좁히는 작업 자체는 그 장애물을 해소하지 않는다.
