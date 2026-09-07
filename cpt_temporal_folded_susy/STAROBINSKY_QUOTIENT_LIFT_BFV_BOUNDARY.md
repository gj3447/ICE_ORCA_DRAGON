# 실제 쌍대 lift의 수반 장애물과 canonical BFV 경계조건

2026-09-07 · SUPPORTING_METHOD · SCOPED.

**현재 해의 유한 성분을 바꾸는 실제 연산자를 구성했지만, 그 비영 연산자는
현재 시험공간에서 수반 조건을 만족하지 못한다.** 별도로 같은 고전 BFV charge를
검사하여, 정확한 a=2 경계에서 constraint ghost를 자유롭게 두는 후보를 배제하고
ghost와 configuration을 고정하는 유한 canonical endpoint 후보를 구성했다.
물리 관측가능량·선택된 내적·원래 bulk 유도 BFV/CPT 접합은 여전히 OPEN이다.

| 대상 | 이번에 확인한 사실 | 남은 범위 |
|---|---|---|
| 실제 쌍대 성분의 작용 | Cauchy 해와 compact bumps의 Gram inverse로 O_A=JAR를 구성. R J=I, R O_A=A R, A≠0이면 O_A≠0 | O_A는 L²에서 bounded이고 Φ를 보존하지만, p_N strong commutation과 같은 Φ를 보존하는 수반 조건은 실패 |
| 일반적인 observable 보완 | R O=A R이면 O=JAR+B, R B=0. 비영이고 수반 조건을 만족하려면 B p_N≠0이 필요 | 적절한 B나 전체 observable-* 대수를 구성한 것은 아님. 기존 w 자유도는 미선택 |
| 정확한 fixed-a/free-ghost 경계 | a=2, 실수 H_L=0 body, 독립 free c, 기존 charge의 범위에서는 완전히 Q-tangent인 locus가 없음 | ghost 제한·변형된 경계식·추가 장·다른 경계조건 전체의 no-go는 아님 |
| ghost-fixed endpoint | a,φ,N 및 c=ρ=0을 끝점에서 고정하면 α와 Ω의 pullback이 0인 Q-tangent finite canonical Lagrangian을 구성 가능 | 원래 bulk의 boundary reduction, quantum N/D 편극과의 대응, graded pairing·CPT kernel은 미구성 |

한 질문은 현재 시험공간의 quotient-only lift와 a=2 cut을 실제 observable 및
canonical BFV 경계로 사용할 수 있는가였다. 출력은 그 두 후보의 domain/접성 판별이다.
Planner는 `INSUFFICIENT_ROUTE_EVIDENCE / NOT_ELIGIBLE`이었다. 원래 regulated joint
relative class와 signed global intersections를 제공하지 않으므로 G1 진전이나
물리 발견으로 세지 않는다. 정확한 가정과 증명은
[유도문](STAROBINSKY_QUOTIENT_LIFT_BFV_BOUNDARY_DERIVATION.md)에 있다.

## 1. 실제 연산자의 구성과 실패 이유

기존 repaired Neumann Φ와 B=[1/2,2]×[-1,2]×[1/4,2], flat density를 유지했다.
독립적인 실제 Cauchy 해 s_i에 대해 T_i(u)=∫_B s_i u, R=(T_1,…,T_n)로 둔다.
적절한 ζ∈C_c^∞(B°), ζ≥0를 선택하면

\[
G_{ij}=\int_B\zeta s_i\overline{s_j},\qquad
v_j=\sum_k\zeta\overline{s_k}(G^{-1})_{kj},\qquad
Jz=\sum_j z_jv_j
\]

가 R J=I를 준다. 따라서 O_A=JAR는 실제 해와 적분으로 정의된 유한 rank
연산자다. 이 존재 논증은 유도문의 해석적 증명이며 Gram 적분의 수치 평가나
PDE 전체의 Lean 형식화를 수행한 것은 아니다.

그러나 R p_N=0이므로 O_A p_N=0이다. 현재 Φ에서 p_N은 symmetric이고
injective다. O와 O*가 모두 Φ를 보존하면서 O p_N=0이면

\[
0=\langle O p_Nu,v\rangle
=\langle u,p_NO^*v\rangle
\quad\Longrightarrow\quad O^*=O=0.
\]

즉 비영 O_A는 같은 carrier를 보존하는 수반을 가질 수 없다. 실제 L² 수반의
image는 N-independent인 해들의 span에 놓여 N-collar 조건과 충돌한다.
이는 [RAQ의 공통 정의역·observable-* 조건](https://arxiv.org/html/gr-qc/9812024)에
대한 실패이며, 전체 물리 observable의 부재를 뜻하지 않는다.

직관적으로 R은 제약 방향의 정보를 지운다. JAR만 쓰면 그 정보를 지운 상태로
시험공간에 돌아오므로 수반 조건에 필요한 작용을 잃는다. 보완 후보는
O=JAR+B, RB=0의 **kernel 방향 작용**까지 제공해야 한다. B p_N≠0은 필요조건이며
그것만으로 충분하지 않다. 따라서 이번 O_A로 내적의 w 자유도를 제한하지 않는다.

## 2. 고전 BFV 경계에서도 ghost 선택이 실제 차이를 만든다

양자 Weyl H와 구별하여 원래 고전 H_L 및
Ω=cH_L+ρΠ, α=p_aδa+p_φδφ+ΠδN+barρδc+barcδρ를 썼다.
고정한 helper의 {q,p}=+1과 source proposal의 QF={Ω,F}에서

\[
Qa=\frac{c p_a}{12\pi^2a},\qquad QN=-\rho,\qquad
Qp_a=cH_{L,a},\qquad Q\bar\rho=H_L,\qquad Q\bar c=\Pi.
\]

a=2를 정확히 고정하고 c를 독립 free ghost로 두면 Q-접성은 p_a=0과
H_{L,a}=0을 차례로 요구한다. 실수 H_L=0 위에서 이들은 F=(1−e^{-βφ})²=2/3,
p_φ²=128π⁴를 요구하지만, 다음 계수

\[
\{H_L,H_{L,a}\}_{p_a=0}=-\frac9{2a}p_\phi F'(\phi)
\]

는 이 예외점에서도 0이 아니다. 따라서 이 fixed-a/free-c ansatz는 닫히지 않는다.
단순 witness는 (a,φ,p_a,p_φ,Π)=(2,0,0,8√6π²,0)이고,
H_L=0인데 Qp_a=−24π²c≠0이다. Ghost를 포함한 변형 경계식까지 배제하지 않았다.

반면

\[
L_{q_0}=\{a=a_0,\phi=\phi_0,N=N_0,c=\rho=0\}
\]

에서 p_a,p_φ,Π,barρ,barc를 자유롭게 두면 α|L=Ω|L=0이고 Q가 접한다.
Half even/odd canonical dimensions와 primitive pullback으로 Lagrangian임을
확인했다. 이는 선언한 유한 canonical 모형에서
[CMR adapted 경계조건 §3.7](https://arxiv.org/pdf/1201.0290)의 대응 조건을 만족하는
후보다. 원래 covariant bulk에서 유도한 BV–BFV 자료를 구성한 것은 아니다.

Quantum Neumann/Dirichlet Cauchy data와 이 고전 endpoint는 별개 객체다.
파동함수의 ∂_a s를 고전 p_a와 동일시하지 않았다. 두 객체의 양자화·편극 대응을
제공해야 실제 state module, graded pairing, residual BV pushforward와
[quantum BFV/CPT 접합 조건](https://arxiv.org/html/1507.01221)을 검사할 수 있다.

## 3. 실제 실행과 검증 경계

주된 실패 분류는 `inference`다. 정의역 보존이나 고전 endpoint를 물리 observable·
quantum 경계로 동일시하는 오류를 겨냥했다. Controls는 수반/domain obstruction,
실제 bracket 부호와 constrained tangency, ghost-fixed endpoint 대조의 세 묶음이다.

- 명령: `./ice run starobinsky_quotient_lift_bfv_boundary`.
- 최종 source commit: `64ed777d472ed1efbbb3b8b2119a40ec190bcef9`.
- 최종 status: `SCOPED_QUOTIENT_LIFT_ADJOINT_OBSTRUCTION_AND_CANONICAL_ENDPOINT`.
- 실제 graded bracket·Q table·constraint witness·정규화·endpoint 기호 검산 **35/35**.
- Lean **11/11**: QuotientLift **8/8**, CanonicalBoundary **3/3**.
- Lean 4.33.0, pinned mathlib, Python 3.13.5, SymPy 1.14.0; 실행 약 **24.03초**.
- `sorry`/`admit`/local axiom 없음. 허용 axioms는 `propext`, `Classical.choice`,
  `Quot.sound`이며 모든 정리의 출력·signature·axiom 검사는 raw result에 있다.

첫 source `e1c269c`에서는 기호 검산 35개와 CanonicalBoundary 3개가 통과했지만,
QuotientLift 마지막 정리의 `inner_self_eq_zero`에서 scalar type inference가 실패했다.
복소수 scalar를 명시한 `64ed777` 뒤 같은 정식 명령으로 전부 통과했다.
이는 증명 구문의 수정이며 실패를 수치 오차나 tolerance로 숨긴 것이 아니다.
첫 실행의 자체 생성 JSON은 임시 보존했고, 위 실패 내용은 이 보고서에 남겼다.

[raw result](STAROBINSKY_QUOTIENT_LIFT_BFV_BOUNDARY_RESULT.json)가 유일한 전체 check
ledger이며 [runner](starobinsky_quotient_lift_bfv_boundary.py),
[proof index](../formal/cpt_sewing/quotient-lift-bfv-boundary-proof-index.json)와 입력 hashes를
고정한다. Lean은 abstract linear/inner-product obstruction 및 정규화된 유한 실수
polynomial 모순을 검증한다. 실제 PDE·Gram section 존재, Φ의 domain 성질, 고전
primitive의 pullback 및 Lagrangian 해석은 유도문의 해석적 증명이다.

독립 정적 검토에서 Gram inverse의 지표·수반 범위, 원래 bracket 부호와 예외근의
추가 접성, ghost-fixed endpoint와 CMR 전체 구조의 차이를 대조했다. 이 검토는
외부 독립 재현이나 실험적 검증이 아니다. Scope는 그대로 supporting이며,
전체 self-adjoint H+p_N, 물리적 observable·내적, 실제 BFV/CPT 및 G1은 OPEN이다.
