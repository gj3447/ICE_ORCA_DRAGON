# Declared raw-\(C\) \(\Gamma_1\) left-boundary variation certificate

## 좁은 질문과 답

선언된 raw-\(C\) extension의 reference pair를 \(\lambda\)와 함께 바꾸지
않고 고정했을 때, 다음 두 질문에는 이제 제한된 의미에서 **예**라고 답할
수 있다.

1. \(\lambda\ne0\)에서 finite-\(Q_0\) Neumann 값이 빠뜨리는 minus-end
   correction functional을 전체 왼쪽 꼬리에서 엄밀히 bound할 수 있는가?
2. 정확히 \(\lambda=0\)인 zero-shell root에서 그 왼쪽 항을 포함한
   declared \(\partial_\lambda\Gamma_1\)를 다섯 inherited bracket 전체의
   outward ball로 감쌀 수 있는가?

번호 없는 bounded run은 exact 11/11, Arb-ball 60/60, theorem/scope guard
6개와 bracket 5/5를 통과했다. 다만 첫 질문의 출력은 실제
nonzero-\(\lambda\) Weyl solution이나 \(\Gamma_1\) 값이 아니라, 그 solution의
선언된 minus-tail \(L^2(f\,dQ)\) norm당 correction coefficient다. 두 번째
질문은 각 bracket 안의 **어떤 실제 root에도 조건부로 적용되는**
\(\lambda=0\) derivative enclosure이며 root uniqueness를 말하지 않는다.

## 고정된 boundary convention과 정확한 부호

선언된 reference field는 \(Q_0=-4\)에서

\[
c_p(Q_0)=1,\qquad c_{p,Q}(Q_0)=0
\]

이고 \(\lambda\)와 무관하게

\[
c_{p,QQ}=A_0c_p,
\qquad
A_0=36\pi^4e^{2Q}-\kappa^2
\]

를 푼다. 선택된 boundary map은

\[
\Gamma_{1,p}(u)=-\lim_{Q\to-\infty}W(u,c_p)
\]

이다. \(\hbar=1\)에서 generalized fiber equation을

\[
u_{\lambda,QQ}=(A_0+\lambda a)u_\lambda,
\qquad
a(Q)=6\pi^2e^{3Q/2}=\frac{f(Q)}2
\]

로 쓰면 repository convention \(W(u,c)=uc_Q-u_Qc\)에서

\[
W(u_\lambda,c_p)_Q=-\lambda a u_\lambda c_p.
\]

따라서 정확히

\[
\boxed{
\Gamma_{1,p}(u_\lambda)
=u_{\lambda,Q}(Q_0)
-\lambda\int_{-\infty}^{Q_0}a(Q)u_\lambda(Q)c_p(Q)\,dQ
}
\]

이다. \(\lambda\ne0\)에서 \(u_Q(Q_0)\)만 계산해 \(\Gamma_1\)라고 부르면
왼쪽 항을 누락한다. 또한 \(c_p\)를 \(\lambda\)에 따라 바꾸면 기존
extension이 아니라 다른 domain을 미분하게 된다.

## 실제 nonzero-\(\lambda\)에 대해 닫힌 연산자 bound

\(Q\le-4\)에서 \(V=36\pi^4e^{2Q}\)이고
\(y=(c_p,c_{p,Q}/\kappa)\)라 두면 free part는 skew rotation이며 perturbation
norm은 \(V/\kappa\) 이하이다. 따라서

\[
q(\kappa)
=\frac1\kappa\int_{-\infty}^{-4}V(Q)\,dQ
=\frac{18\pi^4e^{-8}}\kappa,
\]

\[
M_c(\kappa)
:=\|c_p\|_{L^2(a;(-\infty,-4])}
\le 2\pi e^{-3}e^{q(\kappa)}.
\]

그러므로 weighted Cauchy--Schwarz로

\[
\left|\Gamma_1(u_\lambda)-u_{\lambda,Q}(Q_0)\right|
\le
\frac{|\lambda|M_c(\kappa)}{\sqrt2}
\|u_\lambda\|_{L^2(f;(-\infty,Q_0])}.
\]

이 bound는 cutoff, ODE, quadrature 없이 minus end 전체에 적용된다. 입력은
명시적으로 0을 제외하는

\[
[-10^{-4},-10^{-8}],\qquad[10^{-8},10^{-4}]
\]

두 \(\lambda\) box를 사용했다. puncture는 nonzero bookkeeping을 위한 것이며
부등식 자체는 \(\lambda=0\)으로 연속적으로 이어진다.

| bracket | certified \(M_c\) envelope upper | \(|\lambda|\le10^{-4}\) correction coefficient per unit \(L^2(f)\) norm |
|---:|---:|---:|
| 1 | \(0.4184053357575944161\) | \(2.9585725025319610\times10^{-5}\) |
| 2 | \(0.3632266837280314677\) | \(2.5684005120396639\times10^{-5}\) |
| 3 | \(0.3487696575539799392\) | \(2.4661739005895727\times10^{-5}\) |
| 4 | \(0.3414655476104814086\) | \(2.4145260425703449\times10^{-5}\) |
| 5 | \(0.3369279141809626160\) | \(2.3824401292531938\times10^{-5}\) |

여기서 \(M_c\)는 exact norm이 아니라 certified envelope다. 실제
\(u_\lambda\)의 plus-recessive construction과 norm을 이번 계산은 만들지
않았으므로 actual nonzero-\(\lambda\) \(\Gamma_1\) 값은 계속 null이다.

## zero-shell root에서 새로 닫힌 left correction

\(C=6\pi^2\), \(x=Ce^Q\)이고

\[
u_0(Q;\kappa)=K_{i\kappa}(x),
\qquad a_0=u_0(Q_0)
\]

라 하자. bracket 안의 실제 characteristic root에서는
\(u_{0,Q}(Q_0)=0\)이고 \(a_0\ne0\)이므로 ODE uniqueness에 의해

\[
c_p(Q)=\frac{u_0(Q)}{a_0}.
\]

따라서

\[
I_{\rm tot}=\frac1{\sqrt C}
\int_0^\infty\sqrt{x}\,K_{i\kappa}(x)^2\,dx,
\]

\[
D_{\rm tot}:=\frac{I_{\rm tot}}{a_0^2},
\qquad
\frac{\partial_\lambda\Gamma_1|_0}{a_0}=-D_{\rm tot}.
\]

앞선 finite-\(Q_0\) Green result는 오른쪽 부분만 주므로

\[
\frac{\partial_\lambda u_{\lambda,Q}(Q_0)|_0}{a_0}
=-h(Q_0),
\]

\[
D_-=D_{\rm tot}-h(Q_0)
=\frac1{a_0^2\sqrt C}
\int_0^{x_0}\sqrt{x}\,K_{i\kappa}(x)^2\,dx>0.
\]

즉 기존 proxy derivative가 빠뜨린 항의 크기가 \(D_-\)다.

Mellin total은 Gradshteyn--Ryzhik 6.576(4)의

\[
\int_0^\infty x^{1/2}K_{i\kappa}(x)^2\,dx
=\frac{2^{-3/2}\Gamma(3/4)^2
\Gamma(3/4+i\kappa)\Gamma(3/4-i\kappa)}{\Gamma(3/2)}
\]

를 full parameter ball에서 평가했다. Bessel와 gamma는
`python-flint==0.9.0`의 acb/arb enclosure를 사용했고 80/120자리 두 tier는
같은 backend의 consistency check다.

아래는 두 tier intersection이다. \(\partial_\lambda\Gamma_1|_0\)의 마지막
열은 실제 nonzero-\(\lambda\) family를 수치 구성했다는 뜻이 아니라,
\(u_0=K_{i\kappa}\)로 고정한 zero-shell representative의 scale에서 나온
값이다.

| bracket | \(D_{\rm tot}\) | omitted left \(D_-\) | K-scaled \(\partial_\lambda\Gamma_1|_0\) |
|---:|---:|---:|---:|
| 1 | \([0.1985185739574058326792216314876977,\ 0.1985185739574058326792216314883373]\) | \([0.0556685344237028391546554952035663,\ 0.0556685344237028391546563221411658]\) | \([-0.0154696033434034823243758495132459,\ -0.0154696033434034823243758495131736]\) |
| 2 | \([0.5857454820323136731045051193122574,\ 0.5857454820323136731045051193156971]\) | \([0.0500564328219516633729008665362373,\ 0.0500564328219516633729462303215064]\) | \([0.00155336954225914637937871174945649,\ 0.00155336954225914637937871174946913]\) |
| 3 | \([0.9591509757722930860413514296885399,\ 0.9591509757722930860413514296960652]\) | \([0.0494306475010046762316664428415590,\ 0.0494306475010046762317736876093409]\) | \([-0.000213835974430145148933537237653486,\ -0.000213835974430145148933537237651221]\) |
| 4 | \([1.336298329948641626338723304959983,\ 1.336298329948641626338723304969565]\) | \([0.0492272982161382973359294026141920,\ 0.0492272982161382973406748814321856]\) | \([3.42410601578368099414329317037238\times10^{-5},\ 3.42410601578368099414329317040652\times10^{-5}]\) |
| 5 | \([1.719692699919683547560060917233493,\ 1.719692699919683547560060917244229]\) | \([0.0491326017514618566505381411970150,\ 0.0491326017514618568884854691387155]\) | \([-6.05388639006882465641232987345506\times10^{-6},\ -6.05388639006882465641232987340578\times10^{-6}]\) |

모든 \(D_-\) lower bound가 양수이고 모든 K-scaled derivative enclosure가
0을 배제한다. 과거 point-root/multiprecision conditional ledger의 다섯
\(F_\lambda\) 값은 모두 새 full-bracket ball 안에 들어왔다. 이는 독립적인
point comparison이지 root uniqueness나 global spectrum의 증명은 아니다.

## 실패를 숨기지 않은 실행 경로

첫 clean run은 exact 11/11과 각 precision tier의 절대 width gate를 모두
통과했지만, same-backend 120자리 enclosure 폭이 80자리보다 반드시 작아야
한다는 보조 조건 때문에 bracket당 한 개씩, ball 55/60에서
`NOT_CERTIFIED`가 됐다. 두 tier는 실제로 서로 겹쳤고 최대 폭은 사전 절대
상한보다 여러 자릿수 작았다. 첫 결과는 commit `ea8f31b`에 보존했다.

고정된 nonzero parameter band의 포함 폭은 arithmetic precision에 대해
단조일 필요가 없으므로, source commit `808479a`는 과학 질문이나 절대 폭
gate를 바꾸지 않고 기준을 "각 tier의 독립 절대 width 통과 + nonempty
intersection"으로 바로잡았다. 그 뒤 성공 result는 commit `e4a7871`에
고정됐다. 첫 실패는 가설의 반례가 아니라 invalid refinement criterion의
실패다.

## 과학적 의미와 아직 null인 것

이번 결과가 실제로 바꾼 것은 다음뿐이다.

- 선언된 고정 reference extension에서 nonzero-\(\lambda\) minus-tail
  correction functional이 stated weighted norm에 대해 bounded임;
- 다섯 full bracket에서 finite proxy가 빠뜨린 left correction이 엄밀히
  양수임;
- 각 bracket 안의 어떤 zero-shell root에서도 normalization-invariant
  declared \(\Gamma_1\) derivative ratio와 K-scaled derivative가 0이 아님.

다음은 계속 명시적 null이다.

- actual nonzero-\(\lambda\) plus-recessive solution과 그 \(\Gamma_1\) 값;
- constructed solution에 대한 minus-end remainder와 root continuation;
- finite-\(Q_0\) proxy \(F_\lambda\) amplitude, root velocity와 root
  uniqueness/completeness;
- nonreal resolvent, Weyl \(m\), spectral measure, rigging test space/map,
  physical product와 raw-\(C\) RAQ;
- \(C\leftrightarrow H=fC\) 양자동치, BFV, 관측 likelihood;
- 물리학, 양자중력 또는 TOE 주장.

따라서 다음 실제 P1 blocker는 validated plus-recessive
\(u_\lambda\)를 compact real \(\lambda\) box에서 구성하고, 그 **구체적
solution**에 대해 \(Q\to-\infty\) remainder를 outward enclosure로 닫는
것이다.

## 실행·재현·provenance

```text
./ice run raw_c_declared_gamma1_boundary_variation
./ice repro --only raw_c_declared_gamma1_boundary_variation
npm run check
```

- initial source commit: `7823ba8`;
- failed refinement result commit: `ea8f31b`;
- corrected source commit: `808479a`;
- certified result commit: `e4a7871`;
- input SHA-256:
  `d2d5ad19a36dff063b3bbbdaec55a5158931cd8eed4eca689b8399f6f70c5b32`;
- runner SHA-256:
  `f9cdf7a072bcef34abc732bf3ace329952996d696eb3bfc823e22deda82d3128`;
- result-file SHA-256:
  `4225653c8f5a7a39c24823de0994902c4c68afc33485b7bba35e4421dc964c87`;
- canonical result payload SHA-256, excluding its self field:
  `a112d2c9b0ba2409218c71e94afae16fd685e866e012c88b8694a1992919eebe`.

격리 재현은 `REPRO 1`, needs-attention 0이고 `npm run check`는 68/68 test
pass다. 이는 계산과 제어면의 재현성을 말하며 물리적 승격을 뜻하지 않는다.
