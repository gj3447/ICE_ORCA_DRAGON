# Starobinsky graded seam: coordinate polarization과 dual의 적대적 검토

2026-09-07 UTC · SUPPORTING_METHOD · source/polarization review.

질문은 현재 canonical BFV source를 coordinate-polarized quantum complex와 실제로 연결할
수 있는지다. 결론은 제한적이다. **현재 endpoint delta와 coefficient-algebraic-dual
계산만으로는 양자 seam state가 생기지 않는다.** 그러나 다음에 선언해야 할 최소 typed
object는 분명해졌다: 선택한 coordinate test pair, 그 graded dual polarization, half-density/
Berezin orientation, 두 BFV differential 사이의 chain pairing, 그리고 그 pairing을 구현하는
identity-cylinder kernel이다.

이는 original relative cycle, quantum CPT seam, physical Hilbert space, 또는 G1을 구성한
결과가 아니다.

## 1. 출발점과 이미 배제된 지름길

같은 finite canonical chart의 classical data는

\[
\alpha=p_a\delta a+p_\phi\delta\phi+\Pi\delta N
 +\bar\rho\delta c+\bar c\delta\rho,
\qquad \Omega=cH_L+\rho\Pi .
\]

coordinate polarization을 택하려면 먼저 `(a,phi,N;c,rho)`의 test state와 그 반대
polarization을 별도로 정해야 한다. flat measure와 formal Weyl convention만으로는
half-density, adjoint domain, 또는 ghost Berezin orientation이 정해지지 않는다.

특히 최근 endpoint 후보 `c rho D_{q0}`는 coefficient-degree algebraic dual에서
`Q-hat`-exact였다. 이는 선택한 primitive가 존재한다는 말이다. 그 dual은 original
complex의 usual graded dual도, quantum BFV state module도 아니다. 따라서 endpoint delta를
identity state, cap state, 또는 seam kernel이라고 부를 수 없다.

## 2. 최소한 필요한 두 cochain space

가장 작은 formal candidate는 다음처럼 두 공간을 구별한다.

\[
 C_+=\Phi_+\otimes\Lambda(c,\rho),\qquad
 Q_+=c\widehat H+\rho\widehat p_N,
\]

\[
 C_-=(\Phi_-)^{\vee}\otimes\Lambda(\partial_c,\partial_\rho),
\]

여기서 `vee`는 **graded continuous dual 또는 선언한 distributional dual**이어야 하며,
단순 algebraic transpose space라는 뜻이 아니다. 반대 polarization에서는 multiplication
by `c,rho`가 dual ghost derivatives로 옮겨간다. 따라서 `c H^t+rho p^t`를 같은 ghost degree에
다시 쓰는 coefficient-algebraic-dual complex는 이 목적의 편리한 대조일 뿐 seam의 right
state space가 아니다.

필요한 pairing은 total degree 규약을 포함하여

\[
 B(Q_+x,y)+(-1)^{|x|}B(x,Q_-y)=0. \tag{1}
\]

을 만족해야 한다. 이 식은 bosonic integration by parts, ghost Fourier/Berezin convention,
그리고 cutoff-face term을 모두 포함한 선언 뒤에야 의미가 있다. 현재 repaired compact-N
carrier는 finite translation group에 불변이 아니므로, 그것만으로 full lapse group pairing을
정의할 수 없다.

CMR은 polarization에서 state space를 functions가 아니라 appropriate half-densities로
두며, quantum BFV operator와 residual fields를 별도 data로 둔다 ([§2.3,
items 1--4 and eq. (2.22)](https://arxiv.org/html/1507.01221#S2.SS3)). 따라서 (1)의
형식적 ghost identity만으로 quantum state나 gluing theorem을 인용할 수 없다.

## 3. identity cylinder에 필요한 kernel

선언된 pair가 있으면 identity cylinder의 후보는 coordinate diagonal과 **dual ghost
Fourier kernel**의 tensor product다. schematic하게

\[
 I_{+-}(q_+,q_-;\theta_+,\theta_-)
 =\delta(q_+-q_-)\,K_{\rm gh}(\theta_+,\theta_-),
\]

이다. 여기서 `q=(a,phi,N)`이고 `K_gh`의 sign/order는 `dc d rho`의 orientation,
left/right odd derivatives, 그리고 어느 ghost variables가 dualized되는지로 정해야 한다.
`delta(c_2-c_1)delta(rho_2-rho_1)`를 고정 순서 없이 쓰는 것은 충분하지 않다. 그것은
coordinate-to-coordinate diagonal이며 coordinate-to-dual-polarization Fourier kernel과 다를
수 있다.

검증은 distributional intertwining

\[
 (Q_+\otimes 1+1\otimes Q_- )I_{+-}=0 \tag{2}
\]

와 gluing normalization이다. Bosonic diagonal은 boundary Green form을 만들므로, (2)에는
a=2, phi, N faces의 실제 domain condition이 들어가야 한다. Existing Gaussian kernel의
Ward defect와 box-face ledger는 precisely 이 입력을 생략할 수 없다는 scoped control이다.

CMR의 gluing은 polarization별 state pairing 후 residual BV pushforward를 요구한다
([§2.4.4, eq. (2.36) and Remark 2.37](https://arxiv.org/html/1507.01221#S2.SS4)).
또한 half-density/normalization은 independent data이며 determinant orientation을 지운
ordinary delta normalization이 아니다 ([§2.2.5](https://arxiv.org/html/1507.01221#S2.SS2)).

## 4. anti-linear seam의 부호 대조

실수 Weyl `H`와 `p_N=-i partial_N`에 대해 coordinate complex에서 anti-linear `K`는

\[
 KHK^{-1}=H,\qquad Kp_NK^{-1}=-p_N.
\]

따라서 **quantum coordinate convention의 한 후보**는

\[
 \Theta:(a,\phi,N;p_a,p_\phi,\Pi;c,\bar\rho,\rho,\bar c)
 \mapsto(a,\phi,N;-p_a,-p_\phi,-\Pi;
 c,-\bar\rho,-\rho,\bar c), \tag{3}
\]

with complex conjugation이다. 이 map은 `alpha -> -alpha`이고, `H_L`가 momentum-even인
chart에서 `Omega -> Omega`; equivalently `c` is even and `rho` is odd under the anti-linear
operator, so `rho p_N` is invariant. Coordinate differential에는
`Theta Q Theta^-1=Q`라는 covariance를 준다.

이것은 existing source-design memo의 anti-Poisson map
`c -> -c, bar-rho -> bar-rho, rho -> rho, bar-c -> -bar-c`, for which `Omega -> -Omega`,와
동일한 statement가 아니다. 후자는 classical boundary relation plus orientation convention이다.
(3)을 그것의 quantum lift라고 선언하려면 left/right orientation, whether the anti-Poisson
pullback is composed with complex conjugation, and the sign of the right differential을 함께
derive해야 한다. 이 선언 없이 두 sign tables을 섞으면 false Ward identity가 생긴다.

A sufficient anti-linear pairing requirement is

\[
 B(\Theta x,\Theta y)=\overline{B(x,y)}
\]

with the orientation-reversed right factor and the graded version of (1). It is not a proof that
`Theta` is spacetime CPT, Pin-compatible, or a physical antiunitary. Ghost Fourier transform,
Bosonic half-density conjugation and the chosen real/complex contour must all preserve (1)--(2).

## 5. state family가 남는 것은 그 자체로 실패가 아니다

CPT covariance is normally a symmetry constraint, not a uniqueness theorem. If a declared positive
Hilbert model and antiunitary Theta already exist, `rho -> (rho+Theta rho Theta^-1)/2` produces a
CPT-covariant state family; it does not choose a vacuum. A family is a legitimate construction if
its source, normalization, state space and observables are declared. It becomes a problem only when
one subsequently claims a source-selected state, a unique physical product, or a prediction without
an additional selection rule.

RAQ makes the same distinction: the dense invariant test space, observable star algebra, dual
solutions and physical inner product require separate input ([Giulini--Marolf §II.1--II.2](https://arxiv.org/html/gr-qc/9812024)).
The current finite-N collar construction has already shown why differential annihilation alone cannot
supply the missing group/domain input.

## 6. smallest useful construction, and its failure conditions

The next defensible object is not an endpoint delta. It is one explicitly declared finite
coordinate/dual-polarization **identity-cylinder datum**:

1. specify `Phi_+`, `Phi_-`, their topologies and the bosonic half-density;
2. specify ordered ghost Fourier pairing and left/right derivative convention;
3. write `Q_+`, `Q_-`, then prove (1) including every cutoff-face contribution;
4. give `I_{+-}` and prove (2) plus its identity/gluing normalization;
5. state the anti-linear map and test covariance with the chosen orientation.

A failure of any one of: common domain, nonzero face term, Berezin sign, half-density orientation,
or anti-linear covariance is a scoped rejection of that datum. Passing it would still not select an
original joint relative cycle, a regulator removal, a physical product, or G1 intersections.

The current compact top-ghost classes and the algebraic-dual endpoint exactness are useful
counterexamples to shortcut reasoning, not ingredients that already satisfy this list.
