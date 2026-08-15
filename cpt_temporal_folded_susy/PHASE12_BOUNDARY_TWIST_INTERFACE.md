# Phase 12 — collar 경계-비틀림 정리와 rigid \(N=1\) SUSY interface witness

> 검증: `uv run --with sympy python3 phase12_boundary_twist_interface.py` →
> **38 exact PASS, 9 semantic mutants rejected, exit 0**.
>
> 판정 계약: `PHASE12_RESEARCH_CONTRACT.json` (`T2`, `POST_HOC`). Phase 7/11 결과와
> canonical-removability 관찰을 계약 작성 전에 이미 보았으므로 confirmation 라벨을 쓰지 않는다.

- cycle: `cpt-temporal-folded-susy-2026-08-15-phase12`
- baseline commit: `05c8fe09920cce39959eb18bc352c4ba9c73fd47`
- environment: Python 3.13.5, uv 0.12.3, SymPy locked through `uv run --with sympy`
- actor/date: Codex, 2026-08-15 UTC
- scientific verdict: `UNJUDGED` 유지 / programme appraisal: `UNAPPRAISED` 유지
- 식 번호: **E157–E162**

## 0. 결론부터

Phase 12는 서로 다른 세 문장을 분리한다.

1. **P12A — exact:** Phase 7/11의 strong 허용 항과, unrestricted lapse rescaling을 포함한
   weak dilation은 명시한 가정 아래 open
   interval의 새 bulk force가 아니라 Hamiltonian frame change로 정확히 제거된다. 남는 것은
   endpoint symplectic twist, 변환된 endpoint polarization, 그리고 \(D\ne0\)이면 boundary
   generating function이다. 따라서 Phase 7 회전 transfer를 그 자체로 관측 가능한 새 bulk
   동역학이라고 읽을 수 없다.
2. **P12B — exact but conditional:** 손으로 만든 정칙 4D rigid \(N=1\) Wess–Zumino
   모형에는 spatial half-BPS wall과 회전하는 spectator chiral doublet가 실제로 존재한다. 같은
   chiral multiplet에서 나온 scalar와 chiralino는 동일한 kinematic flavor connection을
   가진다. scalar differential expressions는 chiralino mass matrix에 대응하는 표준 first-order
   형식으로 정확히 factorize된다. 즉 **보손 collar만으로는 SUSY가 아니지만,
   whole-multiplet-compatible 유한 witness는 구성할 수 있다.**
3. **P12C — open:** 이 witness를 local \(N=1\) supergravity, rank-changing seam 또는
   pre-Big-Bang 시간가지로 올리는 유도는 하지 못했다. 한 Eto–Sakai형 matter-coupled 후보의
   holomorphic spectator Hessian이 common identity shift를 받는 것만 확인했으며 나머지
   local-SUSY gate는 `INCONCLUSIVE`다.

따라서 이번 결과는 “SUSY가 빅뱅 전 시간이다”의 증명이 아니다. 더 좁고 정확한 진전은
**collar를 bulk interaction이 아니라 conditional anchored reduced frame scalar로 재해석하고,
그 frame transport와 양립하는 진짜 rigid \(N=1\) parent를 하나 구성했다**는 것이다.

## 1. E157 — 유한 collar의 boundary-twist 정리

정확한 canonical chart에서

\[
S[q,p,N]=\int_{u_-}^{u_+}
\left[p_i\dot q^i-NC(q,p)-a(u)J(q,p)\right]du,
\qquad \vartheta=p_i\,dq^i
\tag{E157}
\]

를 잡는다. 부호 convention은

\[
X_J=(\partial_pJ,-\partial_qJ),\qquad
\iota_{X_J}(dq^i\wedge dp_i)=dJ
\]

이다. \(a\in L^1\)은 prescribed profile이고

\[
\theta(u)=\int_{u_-}^{u}a(s)ds,\qquad (q,p)=\Phi^J_{\theta(u)}(Q,P)
\]

로 둔다. \(J\)의 Hamiltonian flow가 필요한 구간에서 complete/invertible이고 다른 bulk 항도
\(J\)-invariant라고 가정한다. \(X_J\)와 canonical one-form에 대해

\[
\mathcal L_{X_J}\vartheta
=d\!\left[\vartheta(X_J)-J\right],\qquad
(\Phi_s^J)^*\vartheta=\vartheta+dF_s,
\]

\[
F_s(Q,P)=\int_0^s(\Phi_\tau^J)^*
\left[\vartheta(X_J)-J\right]d\tau
\]

이므로 time-dependent pullback은 정확히

\[
p_i\dot q^i=P_i\dot Q^i+a(u)J+\frac{d}{du}F_{\theta(u)}.
\]

따라서 \(\{C,J\}=0\)이면

\[
S=\int_{u_-}^{u_+}\left[P_i\dot Q^i-NC(Q,P)\right]du
+\left.F_{\theta}\right|_{u_-}^{u_+}.
\]

이는 **canonical equivalence**이지 자동으로 gauge equivalence라는 뜻은 아니다. 원래 endpoint
functional과 polarization도 함께 pullback해야 한다. 양쪽 endpoint frame이 독립적으로 자유롭고
anchor가 없으면 open holonomy는 좌표 선택으로 제거된다. 반대로 endpoint probe나 junction data가
frame을 고정하면 상대 twist는 남을 수 있다.

## 2. E158 — Phase 11 전체 동차 2차 class에 대한 닫힌식

Phase 11 E152의

\[
J=q^TMp+\frac12p^TDp,\qquad D=D^T
\]

에 대해 흐름은

\[
p_s=e^{-sM}P,\qquad
q_s=e^{sM^T}(Q+W_sP),\qquad
W_s=\int_0^s e^{-\tau M^T}De^{-\tau M}d\tau=W_s^T,
\]

\[
F_s=\frac12P^TW_sP.
\tag{E158}
\]

실행체는 일반 \(M\in\mathfrak{so}(1,2)\), 일반 symmetric \(D\), 그리고
\(M=M_0+cI\) weak extension을 exact matrix identity로 검사했다.

- Phase 7 \((\beta_+,\beta_-)\) 회전: \(D=0\), 따라서 \(F=0\). collar shape의 내부 frame은
  누적 \(\theta(u)\)에 의존하지만 endpoint twist는 오직
  \(\kappa=\int a\,du\)에 의존한다.
- \(p_+p_-\) shear: \(q=Q+\theta DP,\ p=P\)이며
  \(F_\theta=\theta P^TDP/2\)가 필수다. fixed old-\(q\)는
  \(\delta Q+\theta D\delta P=0\)로 운반되어야 한다.
- \(\alpha\leftrightarrow\beta\) boost: Lorentzian momentum form을 보존하는 cotangent lift로
  똑같이 bulk에서 제거된다.
- weak dilation \(J=q\cdot p\): \(\{C,J\}=-2C\)이므로 unrestricted lapse를 gauge fixing 전에
  변분하고 \(N_{\rm new}=Ne^{-2\theta}\)로 바꿀 때만 baseline bulk action이 복원된다.

두 negative fixture도 닫혔다. symmetric squeezer는
\(\{C,J\}=-2p_+p_-\)라 \(0\)도 \(\lambda C\)도 아니며, unequal-frequency potential은
회전 generator에 invariant하지 않다. 즉 “아무 collar나 **unchanged-baseline bulk에 대한
pure boundary twist**다”라는 문장은 거짓이다. 비불변 \(J\)도 kinetic term에서는 frame
change로 제거되지만, 그 대신 \(C\)가 time-dependent transformed constraint로 바뀐다.

projective 실패는 off-shell coefficient 비교만이 아니라 원래 Lorentzian constraint의 on-shell
witness로 고정했다. squeezer는
\((p_\alpha,p_+,p_-)=(5,3,4)\)에서 \(C=0\)이지만 bracket이 \(-24\)다. unequal-frequency
fixture는 \(q_+=q_-=1,\ p_+=p_-=0,\ \omega_+=1,\ \omega_-=2,\ p_\alpha=\sqrt5\)에서
\(C_\omega=0\)이지만 bracket이 \(3\)이다. 따라서 regular한 phase-space-dependent structure
function \(\lambda(q,p)\)를 허용해도 \(\{C,J\}=\lambda C\)일 수 없다.

범위 주의: E158의 실행체 완전성은 Phase 11의 **동차 2차 \(M,D\) class**에 대한 것이다.
E152가 별도로 언급한 \(p\)-선형, 상수, \(g(C)\) 전부를 exhaustive executable로 다시 분류했다고
주장하지 않는다.

## 3. E159 — 정칙 4D rigid \(N=1\) parent

4D는 \(3+1\)차원 spacetime을 뜻한다. 여기서 사용하는 것은 중력을 포함한 “M-theory”가 아니라
전역 초대칭을 가진 가장 작은 4D \(N=1\) chiral-superfield 모형이다:

\[
K=\Phi^\dagger\Phi+Z^\dagger Z,
\]

\[
W=\lambda\left(v^2\Phi-\frac{\Phi^3}{3}\right)
+\frac12 Z^TM(\Phi)Z,
\]

\[
M(\Phi)=R(\Theta)\begin{pmatrix}m_1&0\\0&m_2\end{pmatrix}R(\Theta)^T,
\quad
\Theta(\Phi)=\frac{\kappa(\Phi+v)}{2v},
\quad m_1,m_2\in\mathbb R\setminus\{0\},\ m_1\ne m_2.
\tag{E159}
\]

\(R(\Theta)\)는 복소 \(\Phi\) 공간에서는 \(SO(2,\mathbb C)\)이고, 아래 real wall slice에서는
\(SO(2)\)다. \(M^T=M\), canonical Kähler metric은 positive이고, \(Z=0\)에서는 spectator가
background 식에 기여하지 않으며 \(W_{\Phi Z_i}|_{Z=0}=0\)라 active/spectator linear block도
분리된다. \(m_1\ne m_2\)이므로 이 \(SO(2)\)는 unbroken flavor symmetry가 아니라
\(\Phi\)-dependent flavor-frame transport다. \(z\)를 **공간** 좌표로 잡으면

\[
\Phi'(z)=\lambda(v^2-\Phi^2),\qquad
\Phi(z)=v\tanh(\lambda vz),\qquad Z=0
\]

은 \(-v\to+v\)의 exact half-BPS wall이다. 양 endpoint는 F-flat이다. \(\kappa=\pi/2\)이면
coordinate mass axes가 서로 바뀌지만 이 각도는 action에서 유일하게 유도된 수가 아니라 **선택한
model datum**이다.

## 4. E160 — scalar의 formal factorization과 multiplet 공통 frame

real wall에서 \(Z=(x+iy)/\sqrt2\), \(M=M^T\in\mathbb R^{2\times2}\)로 쓰고

\[
\mathcal D=\partial_z+M(z),\qquad
\mathcal D^\sharp=-\partial_z+M(z)
\]

를 정의하면 같은 superpotential의 quadratic scalar operator는

\[
H_x=\mathcal D\mathcal D^\sharp
=-\partial_z^2+M^2+M',
\qquad
H_y=\mathcal D^\sharp\mathcal D
=-\partial_z^2+M^2-M',
\]

\[
\mathcal D H_y=H_x\mathcal D,qquad
\mathcal D^\sharp H_x=H_y\mathcal D^\sharp.
\tag{E160}
\]

여기서 \(M'=\partial_zM\), \(\mathcal D^\sharp\)는 아직 Hilbert domain과 boundary
condition을 주지 않은 **formal differential adjoint**다. 실행체가 임의의 real symmetric
\(M(z)\)와 test field에 대해 위 differential-expression 식을 exact로 확인했다. 이는
self-adjointness, spectrum, Fredholm pairing 또는 normalizable mode의 증명이 아니다.

표준 rigid Wess–Zumino component action의 quadratic fermion 항은

\[
\mathcal L_{\psi}^{(2)}
=-i\bar\psi_i\bar\sigma^\mu\partial_\mu\psi_i
-\frac12\left(M_{ij}\psi_i\psi_j+\mathrm{h.c.}\right).
\]

static, tangential-momentum-zero reduction에서 고정한 spinor convention을 택하면 그
first-order spatial expressions가 \(\mathcal D,\mathcal D^\sharp\)로 나타난다. 이 표준 component
관계와 달리, 실행체는 4D Weyl spinor/gamma reduction 자체를 구현하지 않았다. 실행체가 직접
검사한 fermionic 내용은 common flavor-frame covariance와 endpoint flavor identity다.

\(Z=R(\Theta)\zeta\), \(\psi_Z=R(\Theta)\psi_\zeta\)로 같은 chiral multiplet frame을
바꾸면

\[
A_z=R^T\partial_zR=\Theta'(z)
\begin{pmatrix}0&-1\\1&0\end{pmatrix}
\]

가 scalar와 chiralino flavor index에 동일하게 생긴다. \(Z=0\), fermion-free background의
linear spectator order에서는 field-dependent chiral redefinition의 추가 component 항도
사라진다. real slice에서 \(A_z^\dagger=-A_z\)다.

이것이 이번에 증명한 “multiplet-compatible transport”의 정확한 뜻이다. 전체 spatial transfer가
unitary라는 뜻은 아니다. \(M\)은 attenuation/scattering을 만들며, full Green function,
normalizable zero mode,
adiabaticity와 boundary domain은 아직 계산하지 않았다.

endpoint의 선택된 homogeneous flavor symbol
\(S(M)=[\,iM,\ I_2\,]\)에 대해서도

\[
M_+=UM_-U^T,\qquad
S(M_+)\operatorname{diag}(U,U)=US(M_-)
\]

을 exact로 확인했다. 이는 4D super-Poincaré algebra 전체의 대체물이 아니라 endpoint flavor
covariance 점검이다. 보손만 \(U\)로 돌리거나 boson/fermion angle을 다르게 하는 mutant는 이
identity를 깨뜨린다. 반면 whole-multiplet transport는 fermion parity와 commute한다. 즉 이
구성은 보손을 페르미온으로 바꾸지 않는다.

## 5. E161 — open twist는 anchor 없이는 observable이 아니다

고정-frame endpoint map을

\[
U=R_+R_-^{-1}=R(\kappa)
\]

로 정의한다. co-moving equation의 Wilson line
\(\mathcal P\exp(-\int A_zdz)\)는 반대 convention인 \(U^{-1}\)이다. 독립 endpoint basis
\(g_\pm\) 아래

\[
U\mapsto g_+Ug_-^{-1},\qquad n_\pm\mapsto g_\pm n_\pm
\]

이고, oriented external endpoint data가 조건부로 주어질 때만

\[
\mathcal A_{\rm frame}=n_+^TUn_-
\tag{E161}
\]

이 invariant다. 다음 chiral term은 그런 oriented vectors를 넣는 **formal bulk generating
spurion**의 예일 뿐이다:

\[
\Delta W_{\rm src}
=j_-h_-(\Phi)n_-^TZ+j_+h_+(\Phi)n_+^TZ,
\qquad h_\pm=\frac{1\pm\Phi/v}{2}
\]

source derivative를 취한 뒤 \(j_\pm=0\)으로 두면 wall background는 그대로고,
\(h_-\)와 \(h_+\)는 반대 endpoint에서 complementary limit을 가진다. 그러나 이들은 wall
전체에 걸친 smooth bulk function이고 한쪽 점근영역에서 1로 가므로 localized probe가 아니다.
\(j_\pm\ne0\)이면 \(F_Z\)와 asymptotic
vacuum을 바꿀 수 있다. 따라서 이것은 physical endpoint anchor를 **구성하지 않는다**.
그 구성에는 localized boundary/defect action, preserved boundary SUSY, smearing 및 variational
principle을 별도로 검사해야 한다.

\(\mathcal A_{\rm frame}\)은 external oriented data를 가정한 **reduced parallel-transport
scalar**다. full 4D source-to-source
amplitude나 flavor conversion probability가 아니다. 그것을 얻으려면 E160의 mass/potential을
포함한 Green function을 별도로 풀어야 한다. anchor가 없으면
\(g_+=U^{-1},g_-=I\)를 골라 \(U\mapsto I\)로 만들 수 있다.

## 6. E162 — matter-coupled \(N=1\) SUGRA 후보의 holomorphic gate

minimal Kähler

\[
K=\Phi^\dagger\Phi+Z^\dagger Z
\]

를 택하고, 오직 \(\Phi\) 하나가 active real scalar이며 \(Z=0\)인 slice에 한정한
Eto–Sakai형 후보

\[
W_{\rm lc}=e^{-\kappa_g^2(\Phi^2+Z^TZ)/2}
\left[W_{\rm rigid}+a\right]
\]

의 \(Z=0\) spectator holomorphic Hessian은

\[
\left.\partial_{Z_i}\partial_{Z_j}W_{\rm lc}\right|_{Z=0}
=e^{-\kappa_g^2\Phi^2/2}
\left[M(\Phi)-\kappa_g^2(W_{\rm wall}+a)I_2\right]_{ij}.
\tag{E162}
\]

따라서 이 **후보의 이 holomorphic Hessian gate에서만** gravitational deformation은 common
identity shift다. 이것은 물리적 SUGRA fermion mass
\(e^{K/2}D_iD_jW\), compensator/auxiliary system 또는 gravitino–goldstino mixing을 계산한
결과가 아니므로 physical flavor eigenframe transport는 여전히 OPEN이다. warped wall의 전체
bosonic 식,
gravitino–chiralino mixing, local-SUSY constraints, boundary conditions, positive regular domain 및
양자 anomaly는 검사하지 않았다. P12C 판정은 `INCONCLUSIVE`다.

관련 1차 문헌의 regular local-SUGRA BV/BV-BFV construction은 **이 chiral matter가 없는
pure first-order Palatini–Cartan supergravity**이고 nondegenerate coframe을 가정한다. 따라서
rank-changing Big-Bang seam이나 이번 matter parent에 그대로 적용할 수 없다. spatial BPS wall을 시간 방향으로 단순
analytic continuation하면 표준 Hermitian SUSY가 아니라 pseudo-supersymmetry로 가는 문제도 남는다.

## 7. 의미 변형 반박자 9개

실행체는 다음 잘못된 독해가 통과하지 못하도록 exact fixture를 함께 둔다.

1. shear의 \(F_\theta\) boundary term 생략
2. endpoint polarization을 변환하지 않음
3. forbidden symmetric squeezer를 strong/projective 허용으로 오인
4. unequal-frequency bulk potential을 회전-invariant로 오인
5. weak dilation에서 lapse rescaling 생략
6. \(m_1=m_2\)인데 물리적 mass eigenframe twist가 있다고 주장
7. endpoint에서 보손만 회전
8. scalar/chiralino에 서로 다른 회전각 사용
9. basis change 때 조건부 external endpoint vector를 함께 변환하지 않음

전부 exact하게 reject됐다. 이는 물리적 참의 확률을 뜻하지 않고, 명시한 유한 명제의 의미적
회귀를 막는 검사다.

## 8. T2 분류

| target claim | fiber / layer | inference | novelty | registration | fitting risk |
|---|---|---|---|---|---|
| P12A strong boundary-twist theorem | ALGEBRA / ALGEBRAIC | SUPPORTS | REPRODUCTION | POST_HOC | NOT_APPLICABLE |
| P12A weak dilation + lapse theorem | ALGEBRA / ALGEBRAIC | SUPPORTS | REPRODUCTION | POST_HOC | NOT_APPLICABLE |
| P12B engineered rigid \(N=1\) wall witness | PHYSICS / PHYSICS_MAPPING | SUPPORTS (조건부·고전) | REPRODUCTION | POST_HOC | NOT_APPLICABLE |
| original boson-only collar is an \(N=1\) completion | PHYSICS / PHYSICS_MAPPING | CONTRADICTS | REPRODUCTION | POST_HOC | NOT_APPLICABLE |
| P12C specified matter-coupled local-SUGRA uplift | PHYSICS / PHYSICS_MAPPING | INCONCLUSIVE | REPRODUCTION | POST_HOC | NOT_APPLICABLE |
| opposite time branch = superpartner sector | PHYSICS / PHYSICS_MAPPING | INCONCLUSIVE | REPRODUCTION | POST_HOC | NOT_APPLICABLE |

- reproduction policy: 모든 식/행렬 exact simplification; float tolerance 없음.
- Bayes: `NOT_ESTIMABLE` — prior와 \(P(E|H),P(E|\neg H)\)를 사전 정의하지 않았다.
- Lakatos: `UNDETERMINED` — belt를 boundary-frame reinterpretation + regular wall로 바꿨지만 독립 경험적
  corroboration이나 novel excess prediction이 아직 없다.
- KG action: `NONE`; ratification request: `none`.
- scientific verdict와 programme appraisal은 각각 `UNJUDGED`, `UNAPPRAISED`로 유지한다.

공학/회귀 receipt:

- `./ice run phase12_boundary_twist_interface` → 38 exact PASS / 9 mutants rejected / exit 0.
- `./ice run phase11_collar_admissibility` → 기존 E152–E156 exact 회귀 PASS / exit 0.
- `./ice doctor` → locked Node/Python/SymPy runtime `READY`.
- `npm run check` → strict TypeScript PASS, Vitest 12/12 PASS.
- `./ice info phase12_boundary_twist_interface` → runnable catalog 등록 확인; mapped legacy output은
  없으므로 `./ice repro --only ...` 비교 gate는 적용하지 않는다.
- contract JSON parse, Python byte-compile, `git diff --check` → PASS.

## 9. 이제 갈 방향

이번 pivot 뒤의 순서는 명확하다.

1. **bulk collar 관측량 추적을 잠시 멈추고 physical boundary data부터 구성한다.** unanchored
   \(U\)는 observable이 아니다. localized boundary/defect action과 preserved boundary SUSY,
   variational principle을 먼저 닫아야 한다.
2. 그 뒤 P12B의 full quadratic Green function을 풀어 localized probes 사이의 실제 response를
   계산한다. mass gap, nonadiabatic mixing, normalizable modes를 여기서 판정한다.
3. 그 결과가 nontrivial일 때만 E162 후보의 warped background와 gravitino/chiralino constraints를
   풀어 P12C local-SUGRA uplift를 시험한다.
4. spatial flavor wall과 cosmological anisotropy/curvature mode 사이의 별도 embedding map이
   나오기 전에는 이를 temporal fold 또는 Big Bang으로 부르지 않는다.
5. 정말 nonsingular temporal bounce를 유지하려면 standard two-derivative wall의 단순 회전이
   아니라 higher-derivative/NEC-violating dynamics 또는 다른 well-posed temporal completion을
   별도 계약으로 검토해야 한다.

즉 현재 가장 생산적인 경로는 **“시간가지=SUSY”를 먼저 선언하는 것**이 아니라
**regular \(N=1\) parent → localized SUSY boundary/defect probes → full response → local SUGRA → 마지막에
cosmological embedding** 순서다.

## 10. 출처와 파일

- 실행체: [`phase12_boundary_twist_interface.py`](phase12_boundary_twist_interface.py)
- 판정 계약: [`PHASE12_RESEARCH_CONTRACT.json`](PHASE12_RESEARCH_CONTRACT.json)
- 선행 분류: [`PHASE11_COLLAR_ADMISSIBILITY.md`](PHASE11_COLLAR_ADMISSIBILITY.md)
- 4D \(N=1\) SUGRA BPS wall: Cvetič–Griffies–Rey,
  [hep-th/9201007](https://arxiv.org/abs/hep-th/9201007)
- rigid wall profile을 보존하는 SUGRA deformation: Eto–Sakai,
  “Solvable Models of Domain Walls in N=1 Supergravity,”
  [hep-th/0307276](https://arxiv.org/abs/hep-th/0307276)
- Cattaneo–Fila-Robattino, “BV description of N=1, D=4 Supergravity in the first order formalism”
  (pure first-order theory; no chiral matter):
  [arXiv:2503.07373](https://arxiv.org/abs/2503.07373)
- Cattaneo–Fila-Robattino, “The Reduced Phase Space of N=1, D=4 Supergravity in the BV-BFV
  formalism” (pure first-order theory; nondegenerate boundary geometry):
  [arXiv:2601.13025](https://arxiv.org/abs/2601.13025)
- domain-wall/cosmology continuation과 pseudo-supersymmetry:
  [hep-th/0610253](https://arxiv.org/abs/hep-th/0610253)
