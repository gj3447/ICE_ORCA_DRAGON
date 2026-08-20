# ICE 무특권 재귀 검증 정책

> **상태:** ACTIVE methodology policy
> **기원:** 2026-08-20 사용자 제공 교훈. Greg Egan의 *Permutation City*를 읽는 방식에서
> 영감을 받았으나, 작품 해석이나 작품 속 이론을 과학적 근거로 채택하는 문서가 아니다.
> **적용 범위:** ICE_ORCA_DRAGON에서 새로 제안되는 철학적 원리, 수학적 대응, 물리적
> bridge, 상태 선택 규칙과 관측 해석.

## 1. 정책 명제

> **발견했다고 생각한 원리를 그 원리 자신, 그것을 발견한 이론, 상위·하위 층위와 반대
> 방향에 다시 적용한다. 최초 직관, 선호하는 해, 관찰자의 세계, 선택한 contour에는 예외를
> 주지 않는다.**

이를 `무특권 재귀 원칙`이라고 부른다.

이 정책의 목표는 아이디어를 계속 복잡하게 만드는 것이 아니다. 접합에서 생긴 직관을
필요조건, 반례, 불변량, 관측량과 자기일관성에 끝까지 노출하여 다음 가운데 하나로
종료시키는 것이다.

- 더 강하고 정확한 명제로 살아남는다.
- 적용 범위가 줄어든다.
- 서로 구별되지 않는 여러 branch로 남는다.
- 반례 또는 obstruction에 의해 폐쇄된다.

## 2. 필수 일곱 질문

새 원리 `R: A → B`를 제안하면 다음 질문을 순서대로 기록한다.

1. **조건:** 정확히 어떤 공리, domain, convention, scale과 regularization에서 성립하는가?
2. **반례:** 가장 작은 counterexample 또는 semantic mutant는 무엇인가?
3. **제거:** `A`를 제거하거나 약화해도 `B`가 성립하는가? 그렇다면 `A`는 설명 원인이
   아니라 장식일 수 있다.
4. **역방향:** `B → A` 또는 conjugate/reversed construction은 성립하는가? 성립하지 않으면
   방향을 만드는 추가 구조는 무엇인가?
5. **자기적용:** `R`을 `R` 자체, `R`을 선택한 규칙, 연구자가 선호한 branch에 적용하면
   최초 정의나 결론이 유지되는가?
6. **관측:** basis와 서술을 바꾸어도 남는 invariant와 parameter-independent discriminator는
   무엇인가?
7. **정의 안정성:** 계산 결과가 최초의 `A`, `B`, identity, reality, probability 정의를
   파괴하거나 몰래 바꾸지는 않는가?

한 질문을 아직 계산하지 못했다면 `OPEN`으로 남긴다. 유추나 명칭의 유사성으로 `PASS`를
대체하지 않는다.

## 3. 실행 루프

```text
접합 아이디어
→ 정의·가정 동결
→ 최소 계산
→ 반례·제거·역방향 검사
→ 원리와 선택 규칙에 자기적용
→ 불변량과 관측 사상 요구
→ 최초 정의 재검사
→ KEEP / NARROW / BRANCH / KILL
```

각 회전은 새로운 용어보다 새로운 위험을 추가해야 한다. 즉 다음 회전은 앞 회전의 결론을
보호하는 보조서사가 아니라, 그 결론이 실패할 수 있는 더 강한 검사를 만들어야 한다.

## 4. ICE 중심 철학에 즉시 적용한 결과

### 4.1 “전역 선택이 현실을 정한다”의 자기적용

현재 중심 철학은 국소 해 공간만으로 물리적 현실이 정해지지 않으며 global cycle, measure,
state가 필요하다고 말한다. 무특권 재귀를 적용하면 곧바로 다음 질문이 생긴다.

> **그 global cycle과 measure 자체는 무엇이 정하는가?**

따라서 임의로 고른 lapse bypass, 편리한 Airy contour, 원하는 sector prior를 “전역 선택”이라
이름 붙이는 것으로 연구를 종료할 수 없다. original Lorentzian problem, gauge reduction,
boundary condition 또는 더 상위의 물리 원리에서 그 선택을 유도하거나, 선택의 비유일성을
정직하게 결과로 남겨야 한다.

이 자기적용은 Phase 36의 다음 gate를 철학적으로 강화한다. 목표는 upper/lower 중 하나를
고르는 계산이 아니라, **왜 그 선택 규칙이 다른 규칙보다 특권을 갖는지 함께 유도하는
계산**이다.

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

## 5. 무한퇴행을 막는 종료 조건

자기적용은 모든 근거에 다시 근거를 요구하는 무한회의주의가 아니다. 한 branch의 굴착은
다음 가운데 하나에 도달하면 정당하게 멈출 수 있다.

1. 선언한 공리계 안의 exact theorem 또는 독립된 계산이 invariant를 고정한다.
2. 더 근본적인 action/constraint와 boundary data에서 해당 구조가 유도된다.
3. 서로 다른 formulation이 같은 observable 또는 universality class로 수렴한다.
4. parameter-independent discriminator가 외부 측정과 비교된다.
5. underdetermination, non-uniqueness 또는 obstruction이 증명되어 그 branch가 `BRANCH`,
   `INCONCLUSIVE` 또는 `KILL`로 명시된다.

`OPEN`을 정확히 선언하는 것도 종료다. 근거 없이 하나를 선택해 닫는 것보다 엄밀하다.

## 6. 기록 규칙

중심 주장이나 새 bridge를 추가할 때 보고서에는 최소한 다음을 남긴다.

- 원리와 적용 domain
- 최소 반례 또는 mutant
- 제거 및 역방향 결과
- 자기적용 대상과 결과
- 살아남은 invariant
- 관측 사상 또는 그것이 아직 없는 이유
- 최초 정의의 유지/수정 여부
- 최종 `KEEP / NARROW / BRANCH / KILL / OPEN` 판정

이 정책은 연구 계약이나 과학적 evidence가 아니다. 계산과 해석의 누락을 발견하기 위한
repository workflow rule이며, 원하는 결론을 보존할 권한을 부여하지 않는다.

## 7. 한 줄 교훈

> **접합이 아이디어를 만들고, 예외 없는 자기적용이 그 아이디어를 철학으로 만들며,
> 반례와 관측이 그 철학에 물리적 권리를 부여하거나 박탈한다.**
