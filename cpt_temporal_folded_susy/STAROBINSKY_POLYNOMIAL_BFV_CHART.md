# Starobinsky homogeneous BFV의 다항식 좌표 표현

2026-09-06 · **SUPPORTING_METHOD**.

같은 Lorentzian Starobinsky Hamiltonian과 선언한 homogeneous BFV convention을,
lapse·primary momentum·ghost까지 포함해 다항식 charge와 gauge fermion으로 표현했다.
정확한 항등식 검산은 **22/22 통과**했다. ghost가 운동량에 주는 보정항을 일부러 빼면
nilpotency가 깨지는 대조군도 예상한 비영 식을 반환했다.

이 결과는 source를 구성할 때 사용할 수 있는 **정확한 내부 좌표 변환**이다.
원래 relative cycle, 경계에서의 Ward identity, quantum measure, global intersection 또는
새 물리 발견을 구성한 결과는 아니다. 다항식으로 쓸 수 있다는 사실과 그 다항식의 적분
영역을 정했다는 사실은 서로 다르다.

## 1. 질문과 기존 입력

질문: Starobinsky 지수 potential을 다항식으로 바꾸는 변환이, lapse와 ghost를 포함한
extended canonical one-form 및 nilpotent BFV charge도 정확히 보존하는가?

원래의 bosonic constraint는 [Phase 24](PHASE24_CONNECTED_STAROBINSKY_INTERVAL.md)의
Dirichlet-reduced action을 \(T=iN\)으로 계속한

\[
H_L=-\frac{p_a^2}{24\pi^2a}+\frac{p_\phi^2}{4\pi^2a^3}
-6\pi^2a+2\pi^2a^3V,\qquad
V=\frac34(1-e^{-\beta\phi})^2,\quad\beta^2=\frac23.
\]

\(H_L(q,ip_E)=-H_E(q,p_E)\)를 별도로 검산했다. Euclidean constraint의 potential
부호를 그대로 Lorentzian으로 옮기지 않았다.

고전 homogeneous BFV extension은 \(\Omega=cH_L+\rho\Pi\)다.
[Phase 28 §7](PHASE28_THIMBLE_BFV_INTERSECTION.md)의
\(\Psi=-N\bar\rho\) convention을 **채택**한다. 이 선택을 물리적으로 선택된
Lorentzian source라고 부르지 않는다. even bracket은 antisymmetric, odd canonical
bracket은 symmetric \(+1\), gauge-fixed Hamiltonian은 \(-\{\Omega,\Psi\}\)다.

## 2. 먼저 bosonic 지수항을 없앤다

실수 \(a>0\), \(\phi\in\mathbb R\)에서

\[
u=a^2>0,\qquad v=a^2e^{-\beta\phi}>0,
\]

\[
p_u=\frac{p_a}{2a}+\frac{p_\phi}{\beta u},\qquad
p_v=-\frac{p_\phi}{\beta v}
\]

로 두면 \(p_a da+p_\phi d\phi=p_u du+p_v dv\)다. 양의 함수
\(f=24\pi^2u^{3/2}\)를 쓰면

\[
fH_L=-4u^2p_u^2-8uvp_up_v-144\pi^4u^2+36\pi^4u(u-v)^2.
\]

\(p_v^2\) 항의 소거에는 정확히 \(6\beta^2=4\)가 쓰인다. 이는 선택된 potential과
field normalization의 구조이지, 다른 모델에서 독립적으로 관측한 효과가 아니다.

## 3. lapse와 ghost까지 같이 옮기는 핵심 보정

\[
N=fn,\quad\pi_n=f\Pi,\quad
C=c/f,\quad B=f\bar\rho,\quad R=\rho/f,\quad D=f\bar c.
\]

이때 단순히 \(P_u=p_u\)로 놓을 수 없다. 다음 보정이 필요하다.

\[
G=BC+DR,\qquad
P_u=p_u+\frac{3}{2u}(n\pi_n+G),\qquad P_v=p_v.
\]

그 결과 전체 one-form은 정확히

\[
p_a da+p_\phi d\phi+\Pi dN+\bar\rho dc+\bar c d\rho
=P_u du+P_v dv+\pi_n dn+B\,dC+D\,dR.
\]

boundary total derivative를 버려 얻은 등식이 아니다. 좌표 변화에 따른 lapse와 odd
one-form의 \(du\) 성분이 운동량 보정항을 만든다.

\[
k=uP_u-\frac32(n\pi_n+G),\qquad
h(k)=-4k^2-8vkP_v-144\pi^4u^2+36\pi^4u(u-v)^2
\]

로 쓰면 원래 charge와 gauge fermion의 canonical image는

\[
\boxed{\Omega_{\rm poly}=C h(k)+R\pi_n},\qquad
\boxed{\Psi_{\rm poly}=-nB},
\]

\[
\{\Omega_{\rm poly},\Omega_{\rm poly}\}=0,\qquad
-\{\Omega_{\rm poly},\Psi_{\rm poly}\}=n h(k)+BR.
\]

각 Grassmann monomial의 even-variable 계수는 실제 다항식이다. charge, gauge fermion,
gauge-fixed Hamiltonian의 최대 even degree는 각각 **4, 1, 5**다.
\(h,\pi_n\)를 새 Abelian constraint pair라고 단정한 것이 아니다. 숨은 ghost 보정항을
포함한 **전체 charge**가 nilpotent라는 결과다.

## 4. 일부러 보정을 빼면 무엇이 틀리는가

\(A=uP_u-3n\pi_n/2\)로 두면 독립적인 손 전개는

\[
\Omega_{\rm poly}=C h(A)+R\pi_n-12CRD(A+vP_v).
\]

마지막 ghost 항을 지운 \(\Omega_{\rm bad}=C h(A)+R\pi_n\)에는

\[
\boxed{\{\Omega_{\rm bad},\Omega_{\rm bad}\}
=24CR\pi_n(A+vP_v)\ne0}
\]

라는 off-shell defect가 생긴다. \(\pi_n=0\)을 먼저 대입하면 이 오류를 숨기므로
primary constraint 밖의 항등식으로 검사했다. 이 대조군은 구현이 언제나 0을 반환하는
방식으로 nilpotency를 확인하지 않았음을 보여 준다.

## 5. 적분 경로가 자동으로 정해지지 않는 이유

실수 내부 chart의 역변환은 \(a=\sqrt u\),
\(\phi=\beta^{-1}\log(u/v)\)다. 복소화하면 square-root와 logarithm의 lift가 필요하다.
다항식 \(\Omega\)의 대수적 정의역에 \(u=0\)을 추가하는 것은 원래 source의 canonical
확장이 아니다. 그곳에서 \(f=0\)이고 좌표·ghost 역변환이 실패한다.

또한 원래 cutoff와 contour는 변수별 독립 box가 되지 않는다.

- \(\phi_{\min}\leq\phi\leq\phi_{\max}\)는
  \(ue^{-\beta\phi_{\max}}\leq v\leq ue^{-\beta\phi_{\min}}\)로 옮겨진다.
- lapse cap \(N=re^{i\theta}\)의 image는
  \(n=re^{i\theta}/(24\pi^2u^{3/2})\)다. 실수 \(u>0\)에서도 반경은 field에 의존한다.
- 고정 \(N\ne0\)에서 \(u\downarrow0\)이면 \(|n|\to\infty\)다. 반대로
  \(u\to\infty\)이면 \(n\to0\)이다. 원래 scale end가 mixed scale/lapse end로 이동한다.
- proper-time 조건 \(\dot N=0\)은 \(d(fn)/ds=0\)이지 일반적인 \(\dot n=0\)이 아니다.

따라서 이 표현의 named consumer는 **같은 source의 복소 chart lift와 correlated
relative-end를 구성하는 작업**이다. 그 소비자에게 action과 BRST algebra의 정확한
입력은 제공하지만, original class 자체나 regulator removal은 제공하지 않는다.
full current blocker를 바꾸지 않으므로 supporting method로 기록한다.

## 6. 실제 검산과 provenance

source 선행 commit: `9e446a19cf71ba443d926df18544d36f84fdc605`.

```text
./ice run starobinsky_polynomial_bfv_chart
FINITE_CANONICAL_POLYNOMIAL_BFV_CHART
exact controls: 22/22
polynomial even degrees: [4, 1, 5]
```

실제 exit code는 0이었다. Python `3.13.5`, SymPy `1.14.0`에서 실행했고,
[raw result](STAROBINSKY_POLYNOMIAL_BFV_CHART_RESULT.json)는 5,618 bytes다.
SHA-256은 `fce261a77bcdf1b6283d37425890550c7d67833c4c8164816d73b45a71b5d823`다.
runner와 algebra helper hash, 전체 check ledger는 raw result에만 보존한다.

principal failure는 `gauge`다. control은 (1) one-form와 같은 모델 부호,
(2) 독립 graded bracket·nilpotency·gauge density, (3) wrong-shift와 손 전개 대조 세 묶음이다.
독립 read-only 검토가 실행 전 수식·부호를 확인했고, 실행 뒤 raw hash·degree·대조군과
보고서의 domain/scope도 대조했다. 수치 정밀도 sweep이나 다른 모델의
spectral 결과를 evidence로 사용하지 않았다.

helper는 기존 V=0 runner 안의 순수 exterior multiplication/graded differentiation
정의만 hash-pinned import했다. V=0 constraint, 입력·결과, 실행 함수는 사용하지 않았다.
이는 algebra 코드 재사용이며 모델 사이 evidence 이전이 아니다.

초기 log-scale source 질문의 planner는 `CURRENT_BLOCKER_CANDIDATE`였으나, 실제 bounded
polynomial-charge 질문은 `INSUFFICIENT_ROUTE_EVIDENCE`였다. 후자를 키워드로 재포장하지 않고
계산을 supporting으로 수행했다. 새 original cycle이나 G1 진전으로 표시하지 않는다.
canonical graph와 repro manifest는 이 중간 방법 계산으로 변경하지 않았다.

## 7. 문헌과 발견 지위

Starobinsky의 auxiliary-field/frame rewrite는 알려진 방법이다.
[Franken et al. v2 §5.1](https://arxiv.org/html/2512.23656v2)와
[supersymmetric higher-derivative minisuperspace 연구](https://link.springer.com/article/10.1140/epjc/s10052-023-12160-z)는
그 배경을 제공한다. 이 문헌들이 위 polynomial BFV chart나 ICE의 source cycle을 제공했다고
주장하지 않는다. 첫 문헌의 source 처방은 [별도 적대적 검토](../docs/research/ICE_STAROBINSKY_SOURCE_LITERATURE_ADVERSARIAL_AUDIT_2026-09-06.md)에
따라 조건을 제한했다.

[Louko–Martínez-Pascual](https://arxiv.org/abs/1107.1092)의 constraint-rescaling 예는
고전적 재표현이 quantum domain/rigging-map 동치를 자동 보장하지 않는다는 방법 경계다.
그 toy result를 Starobinsky의 양자 판정으로 이식하지 않는다.
[Witten §3](https://arxiv.org/html/1001.2933)의 relative-cycle 방법도 변환된 action뿐 아니라
원래 cycle과 good ends가 있어야 적용된다.

신규성·양자 동치·관측 효과는 아직 확인되지 않았다. 이번에 얻은 것은 새로운 물리 법칙이
아니라, 기존 model의 source 문제를 다룰 수 있는 검산된 다항식 좌표 표현이다.
