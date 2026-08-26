# Gate 1 — affine phase band and reduced relative-class selection

## 결론

앞선 phase-locked construction은 한 점짜리 우연한 contour가 아니다. 같은 fixed-
\(a\), finite-regulator, \(m=2\) scalar fiber에서 일반 수평 affine tail을

\[
T=\rho e^{i\psi},\qquad
\delta=x+i b(\psi),\qquad
-\frac\pi2\leq\psi\leq\frac\pi2
\]

로 쓰자. Starobinsky full-rate exponential의 실수 계수가 엄격히 양수인 robust
tail들은 모두 하나의 principal phase band

\[
\boxed{\left|\psi-\kappa b(\psi)\right|<\frac\pi2}
\]

에 있고, 이 band 안에서

\[
b_s(\psi)=(1-s)b(\psi)+s\frac\psi\kappa,qquad 0\leq s\leq1
\]

로 phase-locked representative \(b_*(\psi)=\psi/\kappa\)에 수축된다. 이 homotopy는
양쪽 field end를 good region에 유지하고 Phase-39 중앙 window를 고정할 수 있다. 따라서
robust horizontal-affine model class 안의 연속적인 tail 선택 채무는 **하나의 reduced scalar-
fiber relative class**로 줄었다.

그러나 수렴성만으로 phase-locked representative 자체가 선택되지는 않는다. 예를 들어

\[
b_\lambda(\psi)=\frac{\lambda\psi}{\kappa},\qquad 0<\lambda<2
\]

전체가 admissible하고 같은 class에 있다. \(\lambda=1\)은 full-rate 위상을 정확히 상쇄하여
decay coefficient를 pointwise 최대로 만드는 유일한 representative다. 기존 Lorentzian real-
field source가 직접 고정하는 것은 real-lapse 두 arm의 literal real-line restriction이다. 이
restriction은 affine ansatz에서 \(\lambda=0\)이고 두 arm의 열린 good band 경계에 놓인다.
\(b=0\)을 복소 bypass cap 전체로 잇는 것은 source-selected cycle이 아니라 candidate lift다.
따라서 현재 기록만으로 phase-locked class를 physical original cycle의 deformation이라고 부를
수 없다.

```text
analytic_status          = EXACT_DERIVATION_INDEPENDENTLY_REVIEWED
robust_affine_tail_class = NARROW_TO_ONE_PRINCIPAL_REDUCED_RELATIVE_CLASS
phase_lock               = UNIQUE_EXACT_CANCELLATION_REPRESENTATIVE
source_selection         = OPEN
real_arm_limit           = OSCILLATORY_GOOD_BAND_BOUNDARY_ON_BOTH_ARMS
Gate 1                   = OPEN_PARTIAL_PROGRESS
physical_original_cycle  = null
global_n_sigma           = null
physics_claim            = null
TOE_claim                = null
automatic_next           = null
```

이는 numbered Phase, run receipt, 새 Python/SymPy 계산이 아니다. 활성 Ragnarok containment
아래 기존 exact action과 source provenance를 실행 없이 재분석한 결과다.

## 1. Inherited action과 범위

사용한 action과 convention은 앞선 보고서와 같다.

\[
S_2(\delta,T)
=\frac{4\pi^2a^3\delta^2}{T}
+2\pi^2T\left[-3a+\frac34a^3
\left(1-e^{-\kappa(\phi+\delta/2)}\right)^2\right],
\qquad \kappa=\sqrt{\frac23}.
\]

\(a>0\), real boundary \(\phi\), \(0<r\leq\rho\leq R<\infty\)를 고정한다. 적분
convention은 \(e^{-S_2}\)다. 이번 분류는 다음으로 한정된다.

- one-complex-dimensional interior \(\phi_1\) fiber;
- continuous bounded \(b:[-\pi/2,\pi/2]\to\mathbb R\)를 갖는 horizontal affine tails;
- full-rate Starobinsky coefficient가 zero가 아닌 **strict robust sector**;
- fixed finite lapse regulator와 Phase-39 중앙 field window를 보존하는 compact connector.

Full-rate coefficient가 정확히 zero인 boundary tail의 half-rate/polynomial case split, varying
\(a_1\), mixed joint infinity, \(r\to0\), \(R\to\infty\), BFV body와 full original cycle은
분류하지 않는다. 따라서 아래 phase-band 정리를 모든 가능한 nonlinear good end의 exhaustion으로
읽으면 안 된다.

Relative-cycle 언어는
[Witten, *Analytic Continuation Of Chern-Simons Theory*, §3.1.1](https://arxiv.org/abs/1001.2933)
의 일반 틀을 사용한다. 그 source는 이 중력 action이나 original cycle을 주지 않는다.
[Banihashemi–Jacobson, *On the lapse contour in the gravitational path integral*](https://arxiv.org/abs/2405.10307)은
그 논문이 명시한 full-real-lapse construction과 momenta-first integration order에서 below-origin
lapse를 지지하지만, finite Phase-39 bypass, 이 scalar tail 또는 그 orientation을 선택하지 않는다.

## 2. Exact full-rate phase band

\(E=e^{-\kappa\phi}\)라 두면 \(x\to-\infty\)의 full-rate 항은

\[
S_{\rm full}
=\frac32\pi^2a^3\rho E^2e^{-\kappa x}
e^{i(\psi-\kappa b(\psi))}.
\]

따라서 phase defect

\[
d(\psi)=\psi-\kappa b(\psi)
\]

에 대해

\[
\boxed{
\lim_{x\to-\infty}e^{\kappa x}\operatorname{Re}S_2
=\frac32\pi^2a^3\rho E^2\cos d(\psi)}.
\]

Strict full-rate goodness는 \(\cos d(\psi)>0\)다. \(d\)가 연속이므로 cap 전체에서는 어떤
하나의 정수 \(n\)에 대해

\[
-\frac\pi2+2\pi n<d(\psi)<\frac\pi2+2\pi n
\]

인 한 connected band 안에 머문다. Compactness 때문에 strict inequality는
\(\cos d\geq c_->0\)인 uniform bound를 준다. \(\rho\geq r>0\)이고 half-rate 항은
\(O(e^{-\kappa x/2})\), kinetic은 \(O(x^2)\)이므로 negative end는 \(\psi,\rho\)에 대해
균일하게 good하다.

## 3. 두 positive arm end가 principal band를 고른다

\(x\to+\infty\)에서는 exponential이 사라지고 kinetic real part가

\[
\frac{4\pi^2a^3}{\rho}
\left[(x^2-b^2)\cos\psi+2xb\sin\psi\right]
\]

로 지배한다. Interior \(|\psi|<\pi/2\)에서는 positive quadratic가 있다. 두 arm에서는

\[
\begin{aligned}
\psi=+\frac\pi2:&\quad
\operatorname{Re}S_2\sim\frac{8\pi^2a^3}{\rho}b(+\pi/2)x,\\
\psi=-\frac\pi2:&\quad
\operatorname{Re}S_2\sim-\frac{8\pi^2a^3}{\rho}b(-\pi/2)x.
\end{aligned}
\]

따라서 positive-\(x\) end가 둘 다 good하려면

\[
b(+\pi/2)>0,\qquad b(-\pi/2)<0
\]

이어야 한다. \(n\geq1\)인 full-rate band는 positive arm에서 첫 부호를 만족할 수 없고,
\(n\leq-1\)인 band는 negative arm에서 둘째 부호를 만족할 수 없다. 그러므로

\[
\boxed{n=0},\qquad
\boxed{|d(\psi)|<\pi/2}.
\]

Principal band에서는 endpoint 부호가 반대로 자동으로 따라온다. \(b\)의 boundedness와 endpoint
부호의 strictness를 이용해 phase interval을 중앙과 두 endpoint neighborhood로 나누면,
positive-\(x\) goodness도 \(\psi,\rho\) 전체에 균일하다.

## 4. Principal band의 contractibility

임의의 admissible \(b\)에 대해

\[
b_s=(1-s)b+s\frac\psi\kappa,
\qquad
d_s=\psi-\kappa b_s=(1-s)d
\]

를 둔다. \(|d|\leq D<\pi/2\)이므로 모든 \(s\)에 대해

\[
\cos d_s\geq\cos D>0.
\]

두 endpoint의 \(b_s\)는 같은 strict sign을 유지한다. 따라서 이 homotopy 전체에서 양 field
end가 uniform-good하다. Conjugation-compatible cycle에 \(b(-\psi)=-b(\psi)\)를 요구하면
\(b_s\)도 같은 조건을 보존한다.

Phase-39 중앙 window를 정확히 고정하려면 앞선 smooth cutoff \(\chi_\psi(x)\)를 재사용하여

\[
h_{\psi,s}(x)
=(1-\chi_\psi(x))x\tan\frac\psi2+\chi_\psi(x)b_s(\psi),
\qquad
\delta_{\psi,s}(x)=x+ih_{\psi,s}(x)
\]

로 둔다. 중앙에서는 모든 \(s\)에서 기존 half-angle line과 같고, 바깥에서는 \(b_s\) tail이다.
\(\operatorname{Re}\delta=x\)라 contour는 injective/immersed이며, \(T\neq0\)에서 action은
\(\delta\)에 entire이므로 connector singularity도 없다.

따라서 다음 scoped statement가 성립한다.

\[
\boxed{
\text{strict full-rate-good continuous horizontal affine tails}
\text{ form one fixed-}a\text{ scalar-fiber relative-homotopy class}.}
\]

이는 varying \(a\)와 \(T\)까지 함께 움직이는 full joint relative homology의 rank 또는 uniqueness
정리가 아니다.

## 5. Exact phase cancellation은 대표를 고르지만 source는 아니다

Full-rate 항을 단지 positive하게 만드는 대신 정확히 positive real로 만들면

\[
T e^{-\kappa\delta}=\rho e^{-\kappa x}>0,
\qquad d(\psi)\in2\pi\mathbb Z.
\]

Continuity 때문에 integer는 cap 전체에서 상수다. 두 positive arm end 또는 conjugation pairing을
같이 요구하면 principal value만 남아

\[
\boxed{b_*(\psi)=\frac\psi\kappa}
\]

가 된다. 더 일반적인 affine parameterization에서 imaginary \(x\)-slope가 있으면 full-rate 위상이
\(x\)에 따라 회전하므로 exact cancellation은 그 slope도 zero로 강제한다.

그러나 goodness는 exact cancellation보다 약하다. 명시적으로

\[
b_\lambda(\psi)=\frac{\lambda\psi}{\kappa},\qquad0<\lambda<2
\]

이면

\[
d_\lambda=(1-\lambda)\psi,qquad
\cos d_\lambda\geq
\cos\left(\frac{|1-\lambda|\pi}{2}\right)>0.
\]

모든 \(\lambda\)가 두 uniform-good ends와 conjugation pairing을 갖는다. \(\lambda=1\)만
\(d=0\)이므로 leading negative-end coefficient를 허용 가능한 최대값 \(1\)로 만든다. 이것은
**canonical maximum-damping representative**를 주지만, Lorentzian source가 maximum damping을
요구한다는 물리 원리는 아니다.

## 6. Literal real-field arm restriction과의 경계

Phase 30이 직접 기록한 것은 real nonzero lapse에서 scalar 방향의 literal real line, 즉 이
bypass의 두 arm restriction이다. Affine ansatz에서 이 restrictions은 \(\lambda=0\), 즉 arm에서
\(b=0\)에 해당한다. \(b=0\)을 복소 cap 전체로 연장한 것은 비교에 쓸 수 있는 candidate lift일
뿐 source-derived cycle이 아니다. 두 arms \(\psi=\pm\pi/2\)에서

\[
\operatorname{Re}S_2(x,T)=0
\]

가 real \(x\) 전체에서 성립한다: kinetic과 potential 모두 pure imaginary다. 따라서 recorded
arm restriction은 이 tail test의 oscillatory/good-band boundary이고 relative-good arm이 아니다.
각 고정 \(\lambda>0\)은 good하지만

\[
\inf_{\psi}\cos((1-\lambda)\psi)
=\sin\frac{\lambda\pi}{2}\longrightarrow0
\qquad(\lambda\to0^+)
\]

이므로 이 특정 \(b_\lambda=\lambda\psi/\kappa\) family를 통해 recorded real arm restrictions까지
포함하는 uniform convergent homotopy는 얻지 못한다. 이를 full Stokes-chamber 정리나 class 자체의
유일한 distributional boundary value로 부르지는 않는다; 단지 현재 scalar-tail family의 수렴
경계에 대한 exact 판정이다.

Affine bend는 interior \(\phi_1\)만 움직이고 fixed Dirichlet endpoint \(\phi_0=\phi_2=\phi_\partial\)
를 바꾸지 않으므로 boundary condition과 충돌하지 않는다. 하지만 arm에서 complex shift를 가지므로
recorded literal real-field arm restriction과 동일하지 않다. 그것의 regulated deformation이라는
주장은 별도 distributional/orientation 증명이 필요하다.

## 7. Source provenance 판정

기존 기록을 역추적하면 다음 경계가 명확하다.

- Phase 24는 real equal Dirichlet endpoints와 solved lapse modulus를 고정하지만 bulk contour를
  선택하지 않는다.
- Phase 27은 Wick map과 below-origin lateral의 local \(T=0\) side만 고정한다.
  Banihashemi--Jacobson은 그 논문의 full-real-lapse, momenta-first construction에서 below-origin
  prescription을 주며, Phase 32는 이를 저장소의 finite full-line bypass 후보로 별도 선언한다.
  어느 것도 finite Phase-39 field-history lift, large-lapse goodness 또는 global coefficient를
  고정하지 않는다.
- Phase 30의 half-angle configuration rays는 local kinetic Gaussian normalization이다. 같은 문서는
  nonlinear contour의 good ends와 original Lorentzian homology를 미증명으로 남긴다.
- Phase 32의 momentum/configuration lift와 projected sign은 declared local Gaussian data이고 full
  BFV orientation 또는 physical below-versus-above selection이 아니다.
- Phase 38은 original field/momentum history cycle, endpoint polarization, regulator/good ends,
  Stokes chamber와 full census가 필요하다고 명시한다.
- Phase-39 input은 자신의 finite-window chain을 `not a derived physical original relative cycle`로
  직렬화했고 `relative_homology_class_proved=false`, `uniform_good_end_decay_proved=false`를 남겼다.

따라서 phase-band theorem은 asymptotic scalar-tail ambiguity를 실질적으로 줄이지만, 기존 source
provenance를 source-selection evidence로 바꾸지는 않는다.

## 8. 다음 최소 discriminator

남은 가장 작은 source-link 문제는 새 root/ODE/full replay가 아니다. 먼저 한 \(m=2\) scalar
phase-space Gaussian에서 다음을 하나의 typed object로 고정해야 한다.

1. literal real \((q,p)\) cycle과 explicit \(N-i0\) prescription;
2. momentum을 먼저 적분한 configuration kernel과 Jacobian/Maslov orientation;
3. \(\Gamma_\lambda:\ b_\lambda=\lambda\psi/\kappa\)와 \(\lambda\to0^+\), field-cutoff
   removal, lapse \(i0\)/cap limit의 순서, measure와 orientation;
4. 그렇게 완전히 지정된 \(\Gamma_\lambda\) limiting distribution과 real phase-space kernel의
   equality, path/side/regulator dependence 또는 mismatch.

Equality면 이 reduced scalar class에 source link가 생기고, side/regulator dependence면 `BRANCH`,
mismatch면 그 link는 `KILL`이다. 어느 경우도 varying-\(a\), full joint census, determinant/BFV line과
global \(n_\sigma\)를 자동으로 계산하지 않는다. 활성 circuit breaker 아래 이 실행은 승인되지
않았으며 여기서는 사양만 기록한다.

> **후속 상태 (2026-08-26):** 위 문장은 이 보고서 작성 시점의 실행 상태다. 사용자가 이후
> 별도 번호 없는 exact one-shot을 승인했고, 그 계산은
> [`GATE1_SCALAR_SOURCE_LINK.md`](GATE1_SCALAR_SOURCE_LINK.md)의
> `NONZERO_ARM_MATCH_ZERO_LAPSE_OPEN`으로 완료·소진됐다. 비영 lapse-arm reduced scalar link는
> orientation \(+1\)로 `KEEP`됐지만 zero-including full \(q\)-paired distribution과 physical joint
> cycle은 여전히 열려 있다.

## 9. 검토와 최종 범위

세 독립 read-only 검토가 action 전개, phase-band inequality, winding-band endpoint sign,
contracting homotopy, \(0<\lambda<2\) counterfamily, exact-cancellation uniqueness와 source provenance를
대조했다. 새 Python/SymPy runner, root, ODE, evaluator 또는 numerical sample은 실행하지 않았다.

계산으로 확인된 사실:

- strict full-rate-good continuous horizontal affine tails는 principal band 하나로 제한된다;
- 그 band는 phase-locked representative로 admissibly contractible하다;
- exact phase cancellation과 두 arm goodness는 phase-locked representative를 유일하게 고른다;
- uniform goodness만으로 representative는 유일하지 않다;
- literal real-field arm은 good band의 oscillatory boundary다.

해석:

- fixed-\(a\) scalar fiber 안에서는 연속적인 affine-tail ambiguity가 relative-class ambiguity가
  아니다;
- phase lock은 최적 damping representative지만 아직 physical source selection은 아니다.

계속 열린 것:

- full-rate coefficient-zero boundary sectors와 non-horizontal/nonlinear asymptotic classes의 exhaustion;
- source-derived distributional/Maslov comparison;
- varying \(a_1\), mixed ends, regulator removal, connector intersections와 complete census;
- Stokes chamber, determinant/Pfaffian/Pin orientation, BFV body와 physical original cycle.

따라서 Gate 1은 `OPEN_PARTIAL_PROGRESS`, global promotion은 `PROHIBITED`이며
`physical_original_cycle`, `global_n_sigma`, physics/TOE claim은 계속 `null`이다.
