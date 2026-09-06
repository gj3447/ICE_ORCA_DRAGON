# Starobinsky 면적 seam 후보: 접합 운동량의 부호 검사

2026-09-06 · **SUPPORTING_METHOD / DECLARED_CANDIDATE_OBSTRUCTION**.

## 질문과 결과

> 기존의 실수 equal-endpoint Starobinsky 구간을, 비음수 면적 계수
> \(\sigma(\phi)\)를 가진 seam 하나로 stationary하게 닫을 수 있는가?

아래에서 선언한 작용과 접합 기하에서는 **불가능하다**. 필요한 중력 운동량 보상은
\(\sigma(\phi_b)<0\)를 요구한다. scalar 조건은 추가로
\(\sigma'(\phi_b)<0\)를 요구한다. 이 결과는 새로 선언한 후보의 배제이며,
[원문 감사](ICE_STAROBINSKY_ORIGINAL_SOURCE_SELECTION_AUDIT_2026-09-06.md)가 미정으로
남긴 실제 CPT 접합 작용을 도출하거나 반증한 것이 아니다.

직관은 경계 **값**과 경계 **운동량**의 차이에 있다. 현재 구간은 같은 크기로 돌아와도
진행 방향의 기울기가 감소한다. 양끝을 닫으려면 그 기울기를 되돌리는 seam이 필요하다.
선언한 양의 면적항은 그 보상을 주지 않는다. 다른 기하인 두 작은 de Sitter cap에서는
양의 면적항으로 접합할 수 있음을 직접 대조한다.

## 새 후보의 정확한 정의

[Phase 24 §1–2](../../cpt_temporal_folded_susy/PHASE24_CONNECTED_STAROBINSKY_INTERVAL.md)의
\(8\pi G=1\), proper-time Euclidean convention을 사용한다. 공간 단면은 \(S^3\)이고,
이미 Dirichlet gravitational boundary reduction을 한 작용은

\[
 I_{\rm bulk}=2\pi^2\int_L^R
 \left[-3a(a'^2+1)+a^3\left(\frac12\phi'^2+V\right)\right]d\tau,
 \qquad V=\frac34(1-e^{-\sqrt{2/3}\phi})^2.
\tag{1}
\]

실수 \(C^2\) bulk 해, \(T=R-L>0\), \(a>0\), 정확한 constraint
\(\mathcal C=a'^2-1-a^2(\phi'^2/2-V)/3=0\)를 가정한다.
두 endpoint는 \((a_b,\phi_b)\)로 같고 \(a_b,\phi_b>0\)다.
[기존 continuum seed](ICE_STAROBINSKY_CONTINUUM_ENDPOINT_CERTIFICATE_2026-09-06.md)가
이 범위에 있다. 아래 부호 증명에는 그 seed의 소수 근삿값이나 reflection symmetry를 쓰지 않는다.

한 구간의 \(L\to R\) orientation을 유지하여 양끝을 식별하고 다음 항을 **한 번** 더한다.

\[
 I_{\Sigma}=+\int_{\Sigma}\sqrt h\,\sigma(\phi_b)
 =+2\pi^2a_b^3\sigma(\phi_b),\qquad
 \sigma\in C^1(\mathbb R,[0,\infty)).
\tag{2}
\]

\(\sigma\)에는 별도의 \(a_b\) 의존성이 없고 추가 seam 자유도도 없다. (1)에 이미
반영한 gravitational boundary term을 다시 더하지 않는다. 추가 Legendre·corner·charge
작용이나 CPT conjugation 처방은 이 후보의 정의에 없다. 이는 기존 original source에서
유도한 처방이 아니라, 원문 감사 후 명시적으로 시험하는 모델링 가정이다.

## 두 접합식과 중력 쪽 모순

(1)의 canonical momenta와 on-shell endpoint variation은

\[
 p_a=-12\pi^2aa',\qquad p_\phi=2\pi^2a^3\phi',\qquad
 \delta I_{\rm bulk}=-p_L\delta q_L+p_R\delta q_R-H_E\delta T.
\tag{3}
\]

이제 두 경계값을 **함께 자유롭게** 변분한다. fixed-Dirichlet kernel 자체에는 이
stationarity를 요구하지 않는다. constrained principal branch에서 \(T\)가 함께 변할 때는
\(\partial_T I=-H_E=0\)인 실제 constraint saddle이므로 envelope 항이 사라진다.
[국소 principal-action 구성](../../cpt_temporal_folded_susy/STAROBINSKY_PRINCIPAL_BRANCH.md)과
fixed-time kernel을 이 과정에서 동일시하지 않는다.

\(\Delta p=p_R-p_L\)라 두면 (2)–(3)은

\[
 \Delta p_a+6\pi^2a_b^2\sigma(\phi_b)=0,\qquad
 \Delta p_\phi+2\pi^2a_b^3\sigma'(\phi_b)=0
\tag{4}
\]

를 준다. **Constraint 위에서만** bulk scale equation은

\[
 a''=-\frac a3(V+\phi'^2),\qquad
 \Delta p_a=4\pi^2a_b\int_L^R a(V+\phi'^2)d\tau>0.
\tag{5}
\]

적분의 strict positivity는 \(\phi_b>0\), \(V(\phi_b)>0\), endpoint 연속성에서
따른다. 따라서 (4)의 첫 식은 모든 \(\sigma\geq0\)에서 왼쪽이 양수다. 이것으로
선언한 후보 전체가 배제된다. (5)를 off-constraint flow나 Hessian의 방정식으로
대체해 쓰지는 않는다.

scalar 쪽도 [기존 경계 항등식](ICE_STAROBINSKY_REAL_COMPACT_CLOSURE_OBSTRUCTION_2026-09-06.md)에서

\[
 B=[a^3\phi\phi']_L^R
 =\int_L^R a^3(\phi'^2+\phi V_{,\phi})d\tau>0,
 \qquad \Delta p_\phi=\frac{2\pi^2}{\phi_b}B>0
\tag{6}
\]

를 얻는다. 비음수 제한을 풀었을 때 필요한 값과 미분은

\[
 \sigma(\phi_b)=-\frac{\Delta p_a}{6\pi^2a_b^2}<0,
 \qquad \sigma'(\phi_b)=-\frac{\Delta p_\phi}{2\pi^2a_b^3}<0.
\tag{7}
\]

\(\sigma'<0\)만으로 \(\sigma\geq0\)와 모순이라고 할 수는 없다. 배제의 결정적인
식은 중력 조건이다. (7)의 음수 계수를 곧바로 physical ghost나 음의 에너지의 증거로
부르지도 않는다. 한 경계점에 (7)을 맞춘 함수를 만드는 일은 original source,
stability 또는 positive quantum state의 유도가 아니다.

## 부호 대조: 두 작은 de Sitter cap

부호를 임의로 뒤집는 대신, 다른 기하의 작용을 독립적으로 변분한다. 이 대조 모델은
**상수 potential** \(V=3H^2>0\), 상수 scalar이며 각 cap은

\[
 a(\tau)=H^{-1}\sin(H\tau),\quad 0\leq\tau\leq T_b<\frac{\pi}{2H},
 \qquad c=\cos(HT_b)=\sqrt{1-H^2a_b^2}>0.
\tag{8}
\]

\(T_b>0\)로 둔다. (1)의 Dirichlet-reduced cap action을 직접 적분하면

\[
 I_{\rm cap}=-\frac{4\pi^2}{H^2}(1-c^3),\qquad
 \frac{dI_{\rm cap}}{da_b}=-12\pi^2a_bc.
\tag{9}
\]

regular pole의 boundary variation은 0이다. \(T_b(a_b)\)는 constraint를 만족하는 cap
family에서 함께 정해지며, 여기서도 \(H_E=0\)이다. 두 cap의 **final boundary끼리**
붙이면 bulk variation은 차가 아니라 합이다. 상수 \(\sigma\)의 seam을 한 번 넣어

\[
 \frac{d}{da_b}(I_{\rm cap,1}+I_{\rm cap,2}+2\pi^2a_b^3\sigma)
 =-24\pi^2a_bc+6\pi^2a_b^2\sigma=0
 \quad\Longleftrightarrow\quad \sigma=\frac{4c}{a_b}>0.
\tag{10}
\]

scalar junction도 0이다. \(c\to0\)의 equator limit는 \(\sigma\to0\)으로, 두
hemisphere의 smooth gluing과 맞는다. 이 식은 classical junction의 대조이며 decay
rate, fluctuation stability 또는 적분 cycle의 기여를 주장하지 않는다.

| 변분할 기하 | common boundary의 bulk 항 | 면적항의 결과 |
| --- | --- | --- |
| 현재 Starobinsky 한 구간의 양끝 식별 | \(p_R-p_L\), 중력 성분 양수 | 선언한 \(\sigma\geq0\)로 불가능 |
| 상수 potential의 두 작은 cap | \(p_1+p_2\), 중력 성분 음수 | (10)의 양의 \(\sigma\)로 가능 |

두 경우는 좌표 이름만 바꾼 동일한 물리가 아니다. 기하·potential·boundary prescription이
다르므로 이 대조를 같은 Starobinsky graph의 독립 physical consumer로 세지 않는다.

## primary source 대조와 판정의 지위

[Eckerle, arXiv:2003.04365](https://arxiv.org/html/2003.04365)의 §1.2,
eqs. (1.24)–(1.27)은 같은 Euclidean Einstein–scalar 부호를 쓰며 \(\kappa=8\pi G\)다.
§2의 cap-to-cap derivative, eq. (2.17)은 두 cap 기여의 합과 양의 wall term을 포함한다.
두 vacuum energy를 같게 놓고 \(\kappa=1\)로 옮기면 (10)과 일치한다. 이는 문헌의
thin-wall bounce의 action-difference 규약과, (9)에서 독립 적분한 Dirichlet cap action의
기하별 junction 부호를 대조한 것이다. 문헌의 smooth-wall 해나 decay 해석을 현재
Starobinsky seam에 이식하지 않으며, 이 부호 관찰의 신규성도 주장하지 않는다.

- 문헌 검색: `./ice literature search "Euclidean gravity scalar domain wall membrane tension junction action" --json`,
  `2026-09-06T14:52:05.881Z`. 검색 metadata와 별도로 위 primary text를 읽었다.
- 사전 planner: `INSUFFICIENT_ROUTE_EVIDENCE`. 실제 산출도 local candidate의
  analytic supporting 검사이며 G1의 class/vector를 구성하거나 해소하지 않는다.
- `./ice harness check`: 473/473 hash 확인, 오류 0, 기존 경고 75.
- 주된 위험은 `sign/unit`. 독립 읽기 검토로 (3)–(7)의 orientation·계수·constraint 범위,
  (8)–(10)의 직접 cap 적분, seam을 한 번 세는 경계항 처리를 대조했다.
  새 numerical runner나 관측 분석은 실행하지 않았다.

남는 미정 객체는 같은 모델의 실제 seam generating relation과 original joint relative
class다. 이 메모는 비음수 면적항 후보 하나를 제외하며, 다른 seam 작용·복소 saddle·CPT
접합 전체를 배제하지 않는다. 방법 메모와 직관 지도의 연결만 갱신하고 canonical
evidence edge·repro manifest·자동 후속 작업을 만들지 않는다.
