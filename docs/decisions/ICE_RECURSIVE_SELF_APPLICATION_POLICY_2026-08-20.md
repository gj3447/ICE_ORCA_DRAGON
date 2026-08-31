# ICE 무특권 재귀 감사 — 역사적 선택 지도

> **상태:** HISTORICAL OPTIONAL ANALYSIS MAP; self-audit verdict `NARROW`
> **기원:** 2026-08-20 사용자 제공 교훈. Greg Egan의 *Permutation City*를 읽는 방식에서
> 영감을 받았으나, 작품 해석이나 작품 속 이론을 과학적 근거로 채택하는 문서가 아니다.
> **현재 적용:** 새 번호 없는 계산의 기본 절차는
> [`ICE_LEAN_RESEARCH_RULES_2026-08-31.md`](ICE_LEAN_RESEARCH_RULES_2026-08-31.md)다. 이 문서는
> 철학적 원리, 상태 선택 규칙 또는 관측 해석의 특권적 비대칭을 분석할 때 선택할 수 있는
> historical map이며, 새 계산의 순차 gate·계약·사전등록 요구가 아니다.

## 1. 보존된 분석 명제

> **물리적으로 동등해 보이는 후보들 사이에 서로 다른 허용성, 진폭, 실재성 또는 설명력을
> 부여하는 순간, 그 차이를 만든 규칙에도 같은 수준의 출처·불변성·경쟁대안·관측 민감성
> 검사를 적용한다. 최초 직관, 선호하는 해, 관찰자의 세계, 선택한 contour에는 면책을 주지
> 않는다.**

이를 `무특권 재귀 원칙`이라고 부른다. 여기서 **특권**은 차이나 비대칭 자체가 아니다.
경쟁 후보에 요구한 증거 부담을 특정 후보에만 면제하면서 그 차이를 물리적 필연성으로
선언하는 것이 특권이다. 실제 구조와 자료가 비대칭을 만든다면 서로 다르게 취급하는 것이
오히려 정확하다.

자기적용도 항상 문자 그대로의 `R(R)`을 뜻하지 않는다. 물리 상태에 작용하는 연산자가
자기 자신을 입력으로 받지 않는다면 그것은 type error다. 먼저 자기적용이 의미론적으로
같은 domain에 속하는지 검사하고, 그렇지 않을 때에는 `R`의 사용조건과 정당화에 같은 증거
부담을 부과하는 **메타 감사**로 바꾼다. 경계를 긋는다면 그 경계가 결론을 보호하기 위한
사후 예외가 아님을 밝혀야 한다.

이 정책의 목표는 아이디어를 계속 복잡하게 만드는 것이 아니다. 접합에서 생긴 직관을
필요조건, 반례, 불변량, 관측량과 자기일관성에 끝까지 노출하여 다음 가운데 하나로
종료시키는 것이다.

- 더 강하고 정확한 명제로 살아남는다.
- 적용 범위가 줄어든다.
- 서로 구별되지만 가중치가 정해지지 않는 여러 branch로 남는다.
- 표현만 다르고 관측적으로 같은 동치류로 소거된다.
- 반례 또는 obstruction에 의해 폐쇄된다.

## 2. 선택 가능한 여덟 질문

새 원리 `R: A → B`의 철학적 또는 선택-rule 분석에 이 지도를 쓰기로 했을 때 다음 질문을
참조할 수 있다. 새 계산마다 모두 기록하거나 순서대로 통과할 의무는 없다.

1. **종류와 구별:** `A`, `B`, `R`은 물리 법칙, gauge quotient, 경계 상태, 표현 convention,
   관측 사상, 연구자의 추론 규칙 중 무엇인가? 중복을 몫낸 뒤에도 `A`와 `B`가 다른가?
2. **조건:** 정확히 어떤 공리, domain, convention, scale과 regularization에서 성립하는가?
3. **반례:** 가장 작은 counterexample 또는 semantic mutant는 무엇인가?
4. **제거:** `A`를 제거하거나 약화해도 `B`가 성립하는가? 그렇다면 `A`는 설명 원인이
   아니라 장식일 수 있다.
5. **역방향:** `B → A` 또는 conjugate/reversed construction은 성립하는가? 성립하지 않으면
   방향을 만드는 추가 구조는 무엇인가?
6. **자기·메타 감사:** type-correct하면 `R`을 재적용한다. 그렇지 않으면 `R`을 선택한 규칙과
   연구자가 선호한 branch가 경쟁 후보와 같은 증거 부담을 지는지 검사한다.
7. **불변량과 관측:** 정당한 재서술에도 남는 invariant는 무엇이며, 독립적으로 고정되거나
   식별 가능한 매개변수 아래 어떤 observable이 경쟁 설명을 구별하는가?
8. **정의 안정성:** 계산 결과가 최초의 `A`, `B`, identity, reality, probability 정의를
   파괴하거나 몰래 바꾸지는 않는가?

한 질문을 아직 계산하지 못했다면 `OPEN`으로 남긴다. 유추나 명칭의 유사성으로 `PASS`를
대체하지 않는다.

## 3. 선택적 분석 루프

```text
접합 아이디어
→ 정의·가정 동결
→ gauge·basis 중복을 몫내고 실제 구별인지 검사
→ 최소 계산
→ 반례·제거·역방향 검사
→ type-correct한 자기적용 또는 선택 규칙의 메타 감사
→ 불변량과 관측 사상 요구
→ 최초 정의 재검사
→ KEEP / NARROW / BRANCH / EQUIVALENCE / KILL / OPEN
```

각 회전을 사용할 때에는 새로운 용어보다 새로운 위험을 추가한다. 즉 다음 회전은 앞 회전의 결론을
보호하는 보조서사가 아니라, 그 결론이 실패할 수 있는 더 강한 검사를 만든다.
좋은 재귀는 같은 자리를 도는 원이 아니라 나선이다. 한 회전 안에서는 정의를 얼리지만,
회전 사이에서는 새 반례와 계산을 가지고 정의와 원칙 자신도 다시 연다.

## 4. ICE 중심 철학에 즉시 적용한 결과

### 4.0 “두 sheet가 다르다”의 구별 검사

Phase 17에서는 `local` charge와 `sheet-exchanging` charge가 한 finite witness 안에서 unitary
basis change로 연결된다. 따라서 먼저 물어야 할 것은 “무엇이 sheet를 교환하는가?”가 아니라
“무엇이 두 sheet의 정체성을 basis-independent하게 고정하는가?”다. 전체 action, source
algebra, common domain과 observable이 그 unitary를 물리적 동치로 허용한다면 exchange는
현상이 아니라 서술이다. 허용하지 않을 때만 그 차이를 만드는 구조가 물리 후보가 된다.

### 4.1 “전역 선택이 현실을 정한다”의 자기적용

현재 중심 철학은 국소 해 공간만으로 물리 진폭이 정해지지 않으며 global cycle, measure,
state가 필요하다고 말한다. 무특권 재귀를 적용하면 곧바로 다음 질문이 생긴다.

> **그 global cycle과 measure 자체는 무엇이 정하는가?**

따라서 임의로 고른 lapse bypass, 편리한 Airy contour, 원하는 sector prior를 “전역 선택”이라
이름 붙이는 것으로 연구를 종료할 수 없다. original Lorentzian problem, gauge reduction,
boundary condition 또는 더 상위의 물리 원리에서 그 선택을 유도하거나, 선택의 비유일성을
정직하게 결과로 남겨야 한다.

이 자기적용은 Phase 36의 다음 gate를 철학적으로 강화한다. 그러나 upper/lower 중 하나를
반드시 골라야 한다는 전제도 면제하지 않는다. 목표는 original problem이 허용하는 상대계수,
CPT-real 중첩과 물리적 동치류를 유도하고, 유도되지 않는 자유도는 독립 경계 입력으로
노출하며, 그 민감도를 관측 진폭에서 계산하는 것이다.

### 4.2 “수학적 가능성은 물리적 실재가 아니다”의 자기적용

이 원리는 ICE가 만든 seam 철학에도 똑같이 적용된다. 철학적으로 일관된 seam 개념이 있다는
사실은 seam이 물리적으로 실재한다는 증거가 아니다. 중심 철학 자체도 action, common domain,
positive inner product, full cycle, persistent carrier와 observable gate를 면제받지 않는다.

따라서 철학 문서는 물리 가설을 정당화하는 마지막 전제가 아니라, 물리 가설이 통과해야 할
검사를 더 엄격하게 만드는 장치다.

### 4.3 “두 층을 연결한다”의 역방향·제거 검사

Hypercomplex algebra와 temporal-folded SUSY가 하나의 워크벤치를 공유한다고 해서 둘 사이의
물리적 derivation이 존재하는 것은 아니다.

- hypercomplex 구조를 제거해도 temporal seam 계산이 그대로 성립한다면, 현재 seam 이론은
  hypercomplex 설명을 필요로 하지 않는다.
- temporal seam을 제거해도 대수적 항등식이 그대로 성립한다면, 그 항등식은 seam의 증거가
  아니다.
- 두 방향 가운데 어느 쪽에도 정의된 map이 없다면 두 연구선은 병렬 프로그램으로 남긴다.

“둘 다 ICE에 속한다”는 서사적 소속은 물리적 bridge를 대신하지 않는다.

### 4.4 “상태 비대칭”의 제거·지속성 검사

Seam을 제거한 뒤에도 같은 pole spectrum이 나오거나, seam이 있어도 persistent carrier가
없어 late-time pole이 변하지 않는다면 seam은 현재 SUSY spectrum의 설명 원인이 아니다.
Phase 18의 null result가 이 검사의 첫 사례다. 이후 모든 breaking 제안은 seam 직후의 상태
차이뿐 아니라 carrier 제거, long-time limit, interacting pole과 backreaction을 검사해야 한다.

추가로 seam을 시간의 화살표 원인이라고 부르려면 한쪽 `incoming vacuum`, retarded
prescription과 post-seam observer를 이미 입력하지 않았는지 역방향으로 감사한다. 동일 sewing의
역과정도 허용된다면 seam geometry만으로 화살표는 나오지 않는다. 장기 원인성의 한 진단은

\[
\lim_{t\to\infty}
\frac{\delta\langle O(t)\rangle}{\delta\lambda_\Sigma}\ne0
\]

가 적어도 하나의 물리 observable에서 남는지 묻는 것이다. 모든 물리 관측량에서 0이면 그
seam은 과거 excitation의 기술일 수 있어도 현재 spectrum의 설명 원인은 아니다.

### 4.5 “measure가 초기상태를 고른다”의 자기감사

Phase 20의 HH/tunneling 부호, standard-history와 independent-pair weight, coherent/decoherent
합은 서로 다른 물리 입력이다. 초기값을 선택한다고 말하려면 measure와 probability 개념을
action, physical inner product 또는 WDW current에서 target-blind하게 유도해야 한다. 원하는
peak를 본 뒤 determinant나 prior를 조정하면 선택 규칙이 목표를 재입력한 것이다. 허용되는
factor ordering과 convention 변화에도 discriminator가 남아야 한다.

## 5. 선택적 감사의 종료 예시와 남는 전제

근거를 끝까지 요구하면 질문을 무한히 계속하거나, 근거들이 서로를 지지하는 원을 만들거나,
어느 지점에서 더 이상 유도되지 않는 전제를 선언하는 길이 남는다. 이 정책은 그 난점을
해결했다고 주장하지 않는다. 어디서 어떤 종류의 근거 위에 멈췄는지 숨기지 않게 할 뿐이다.

정리의 증명은 공리로부터의 귀결을 고정하지만 공리의 물리성을 증명하지 않는다. action에서의
유도는 임의성을 한 층 위로 옮길 수 있고, 여러 formulation의 수렴은 강건성을 주지만 유일한
실재를 확정하지 않는다. 관측은 외부 마찰을 주지만 시험된 범위만큼의 권리만 부여한다.

이 지도를 선택한 branch 분석은 다음 가운데 하나에 도달하면 닫을 수 있다.

1. 선언한 공리계 안의 exact theorem 또는 독립된 계산이 invariant를 고정한다. 남은 공리는
   명시적 전제다.
2. 더 근본적인 action/constraint와 boundary data에서 해당 구조가 유도된다. 상위 action의
   지위는 별도 문제다.
3. 서로 다른 formulation이 같은 observable 또는 universality class로 수렴한다. 이것은
   강건성이지 형이상학적 유일성은 아니다.
4. 독립적으로 고정되거나 식별 가능한 매개변수 아래 discriminator가 외부 측정과 비교된다.
   권리는 시험 범위에 한정된다.
5. 남은 차이가 모든 physical observable에서 사라져 `EQUIVALENCE`로 몫내어진다.
6. observable 차이는 남지만 현 이론이 가중치를 정하지 못해 `BRANCH`로 닫힌다.
7. underdetermination, non-uniqueness 또는 obstruction이 확인되어 `NARROW`, `INCONCLUSIVE`나
   `KILL`로 명시된다.

`OPEN`을 정확히 선언하는 것도 종료다. 다만 다음 결정 계산과 결과별 판정표를 붙인다. 새
계산 없이 서사만 더해 같은 branch를 다시 여는 것은 재귀가 아니라 면역화다. 독립 경계상태나
primitive가 남을 수도 있다. 우연적 입력은 설명 실패와 같지 않지만, 우연을 필연으로
판매해서도 안 된다.

## 6. 선택해서 사용할 때의 기록 예시

중심 주장이나 새 bridge에 이 지도를 적용하기로 한 경우 아래에서 실제 질문과 관련된 항목만
남긴다. 새 계산마다 이 목록 전체를 작성할 의무는 없다.

- 원리와 적용 domain
- 최소 반례 또는 mutant
- 제거 및 역방향 결과
- 자기적용 또는 메타 감사 대상과 결과
- 살아남은 invariant
- 관측 사상 또는 그것이 아직 없는 이유
- 최초 정의의 유지/수정 여부
- 최종 `KEEP / NARROW / BRANCH / EQUIVALENCE / KILL / OPEN` 판정

이 지도는 연구 계약, active repository workflow 또는 과학적 evidence가 아니다. 선택적으로
계산과 해석의 누락을 찾는 도구이며, 원하는 결론을 보존할 권한을 부여하지 않는다.

새 구조가 기존 null을 구하기 위해 추가되면 **예측 임대료**를 내야 한다. 원하는 수치를 보고
parameter를 맞추지 않고, 실패한 observable 정의를 바꾸지 않으며, 추가한 자유도보다 더 많은
가능한 결과를 배제하고 독립적인 새 예측을 만들어야 한다. `persistent F`, `preferred contour`,
`one-loop peak`라는 이름은 각각 vacuum dynamics, original-cycle derivation, target-blind
determinant 계산을 대신하지 않는다.

## 7. 보존된 자기감사

무특권 재귀 원칙에 무특권 재귀를 적용한 판정은 `NARROW`다.

- 이 원칙은 모든 대상에 문자 그대로 무한 재귀하는 우주 법칙이 아니다.
- 적용 대상은 동일성, 선택, 가중치, 인과성, 확률 또는 설명적 우위를 부여하는
  `privilege-bearing edge`다.
- type-correct하지 않은 자기적용은 금지하고 정당화의 메타 감사로 바꾼다.
- 이 정책을 제거해도 기존 계산 결과는 바뀌지 않는다. 정책은 evidence가 아니라 오류를 찾는
  도구다.
- 분석적 유용성은 숨은 가정을 실제로 드러내고 새 반증조건을 만드는 동안에만 유지된다.
- 새 가정, 반례, invariant, observable 차이 또는 model class 축소 없이 같은 의문만 복제하면
  재귀를 종료한다.
- 더 나은 감사법이 나오거나 이 정책이 유의미한 구별을 지우면 정책 자체를 수정하거나
  폐기한다.

무특권은 모든 사실에 충분한 이유가 반드시 존재한다는 형이상학적 명제가 아니다. 설명되지
않은 차이를 설명된 필연성으로 판매하지 말라는 제한된 연구 규율이다. 자기일관성은 모순을
거르는 체이지 세계와의 대응을 보증하는 봉인이 아니다.

## 8. 한 줄 교훈

> **접합이 아이디어를 만들고, 면책 없는 재귀 감사가 그 아이디어를 철학으로 만들며,
> 반례와 관측이 그 철학에 물리적 권리를 부여하거나 박탈한다.**

직관적 동반 명상은
[`../ICE_RECURSIVE_TRUTH_MEDITATION_2026-08-20.md`](../ICE_RECURSIVE_TRUTH_MEDITATION_2026-08-20.md)에
분리한다. 그 이미지는 사유 도구이지 이 정책이나 물리 가설의 evidence가 아니다.
