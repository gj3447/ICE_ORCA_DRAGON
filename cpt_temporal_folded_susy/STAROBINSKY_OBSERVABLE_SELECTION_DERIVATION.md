# 실제 Weyl 제약의 1차 국소 강한 관측가능량 분류

2026-09-07 · SUPPORTING_METHOD · 해석적 유도 정본.

질문: 고정한 Starobinsky Weyl 제약, lapse 제약, repaired Neumann 시험공간에 대해
1차 국소 미분연산자 중 두 제약과 **강하게** 교환하는 것은 무엇인가?
출력: 이 정확한 클래스의 commutant가 항등원과 lapse 제약뿐이라는 분류.
비주장: 모든 고차·약한·BRST·관계론적 또는 비국소 관측가능량, 물리적 Hilbert 공간,
RAQ rigging map, full BFV/CPT 접합을 분류하거나 부정하지 않는다.

이것은 `open:starobinsky-seam-ward-boundary-state-limit`의 boundary-state 선택 문제를
좁히는 supporting 결과다. source-defined original relative cycle, global signed
intersections 또는 Gate 1의 typed input을 주지 않으므로 TOE core 진전은 아니다.

## 1. 정확한 범위와 규약

[state criterion audit](STAROBINSKY_BFV_STATE_CRITERION_AUDIT.md)와
[Neumann Cauchy dual construction](STAROBINSKY_DUAL_CAUCHY_DERIVATION.md)의
box, flat density, hbar=1 및 Weyl ordering을 그대로 쓴다.

\[
H=-\partial_a(f\partial_a)-b\partial_\phi^2+W,\qquad
f=-\frac1{24\pi^2a},\quad b=\frac1{4\pi^2a^3},\quad W=U-\frac{f''}{4},
\]
\[
U=-6\pi^2a+\frac32\pi^2a^3(1-e^{-\beta\phi})^2,
\qquad \beta=\sqrt{2/3},\qquad p_N=-i\partial_N.
\tag{1}
\]

특히 scaled constraint나 log-coordinate의 다른 ordering으로 교체하지 않는다.
분류할 연산자는 계수가 smooth이고 N에 의존하지 않는

\[
O=X+C+D\partial_N,\qquad
X=X^a(a,\phi)\partial_a+X^\phi(a,\phi)\partial_\phi,
\tag{2}
\]

이다. \([p_N,O]=0\)가 계수의 N 독립성을 요구한다. 아래에서 \([H,O]=0\)는
test function 위의 미분연산자 항등식이다. 제약을 오른쪽에 곱한
\([H,O]=R_HH+R_Np_N\) 같은 약한 normalizer 조건은 이 절에서 허용하지 않는다.

관심 있는 carrier는 r=0의 repaired space

\[
\Phi=\{u:\ \partial_a(H^kp_N^mu)|_{a=2}=0\ \text{for all }k,m\geq0,
\ \text{and }u\text{ vanishes in collars of the other faces}\}.
\tag{3}
\]

이다. 이는 smooth test space이지, 여기서 닫힌 연산자 domain이나 self-adjoint
closure를 이미 얻었다는 뜻은 아니다.

## 2. 실제 unscaled operator를 flat wedge operator로 바꾼다

다음을 둔다.

\[
r=k a^{3/2},\qquad k=\frac{4\pi\sqrt6}{3},\qquad
\theta=q\phi,\qquad q=\sqrt{\frac38},\qquad S=r^{2/3}.
\tag{4}
\]

직접 chain rule을 적용하면 kinetic part는

\[
-\partial_a(f\partial_a)-b\partial_\phi^2
=\partial_r^2-\frac1{3r}\partial_r-\frac1{r^2}\partial_\theta^2.
\tag{5}
\]

한편 Lorentzian polar wedge의 scalar wave operator는

\[
\Box=\partial_r^2+\frac1r\partial_r-\frac1{r^2}\partial_\theta^2.
\tag{6}
\]

이고

\[
S\Box S^{-1}=\partial_r^2-\frac1{3r}\partial_r
-\frac1{r^2}\partial_\theta^2+\frac4{9r^2}.
\tag{7}
\]

이다. \(f''=-1/(12\pi^2a^3)\) 및
\(4/(9r^2)=1/(24\pi^2a^3)\)이므로 정확히

\[
H=S(\Box+Q)S^{-1},\qquad
Q=U-\frac1{48\pi^2a^3}
=-A r^{2/3}+B r^2F(\theta)-C r^{-2},
\tag{8}
\]
\[
A=6\pi^2k^{-2/3}>0,\qquad B=\frac{3\pi^2}{2k^2}>0,
\qquad C=\frac{k^2}{48\pi^2}>0,
\qquad F(\theta)=(1-e^{-4\theta/3})^2.
\tag{9}
\]

여기서 \(\beta\phi=4\theta/3\)를 썼다. 식 (8)은 원래 H와의 similarity
변환일 뿐, inner product의 unitary equivalence나 다른 양자화 규약을 주장하지 않는다.

## 3. 1차 commutator의 계수 방정식

\(Y=S^{-1}(X+C)S=X+\gamma\)로 두면

\[
\gamma=C+\frac23\frac{X^r}{r}.
\tag{10}
\]

\([\Box+Q,Y]=0\)의 2차 계수를 직접 비교하면 wedge metric
\(ds^2=dr^2-r^2d\theta^2\)의 Killing equations가 나온다:

\[
\partial_rX^r=0,\qquad
\partial_\theta X^r-r^2\partial_rX^\theta=0,\qquad
X^r+r\partial_\theta X^\theta=0.
\tag{11}
\]

이는 외부 symmetry 정리를 가정한 단계가 아니다. 예를 들어 \(\Box\)를 식 (6)처럼
전개하여 \([\Box,X]\)의 \(\partial_r^2\), \(\partial_r\partial_\theta\),
\(\partial_\theta^2\) 계수를 각각 0으로 놓으면 식 (11)을 얻고, 그 세 식을
나머지 1차 계수에 대입하면 \([\Box,X]=0\)이다.

첫 식에서 \(X^r=G(\theta)\)이고, 둘째 식을 적분하면
\(X^\theta=-G'(\theta)/r+\delta(\theta)\)다. 셋째 식은
\(G-G''+r\delta'=0\)이므로 \(\delta\)는 상수이고 \(G''=G\)다. 따라서

\[
X^r=\alpha\cosh\theta+\zeta\sinh\theta,\qquad
X^\theta=-\frac{\alpha\sinh\theta+\zeta\cosh\theta}{r}+\delta.
\tag{12}
\]

이는 두 Minkowski translation과 boost의 일반 선형결합이다.

이제 multiplication commutator는

\[
[\Box,\gamma]
=2\gamma_r\partial_r-\frac2{r^2}\gamma_\theta\partial_\theta+\Box\gamma,
\qquad [Q,X]=-X(Q).
\tag{13}
\]

이다. 따라서 1차 계수는 \(\gamma_r=\gamma_\theta=0\), 즉 \(\gamma\)가 상수임을
강제하고, 남은 0차 계수는

\[
X(Q)=0.
\tag{14}
\]

을 준다.

## 4. 실제 Starobinsky potential은 모든 비영 Killing 장을 제거한다

식 (12)의 translation 부분을
\(G=\alpha\cosh\theta+\zeta\sinh\theta\)로 쓴다. 식 (8)의 직접 미분은

\[
X(Q)=2CG r^{-3}-\frac{2A}{3}G r^{-1/3}
+Br\{2FG-F'G'\}+\delta Br^2F'.
\tag{15}
\]

이다. 고정한 \(\theta\)에서 \(r^{-3},r^{-1/3},r,r^2\)는 임의의 연결된 열린
radial interval에서 선형독립이다. 따라서 식 (14)의 \(r^{-3}\) 계수는 \(G=0\)을
강제한다. \(\cosh\theta\)와 \(\sinh\theta\)의 독립성으로
\(\alpha=\zeta=0\)이다. 그 후 식 (15)는 \(\delta Br^2F'=0\)이고
\(F'\)가 항등적으로 0이 아니므로 \(\delta=0\)이다.

이 논증은 \(a\to0\)의 극한, large-field 근사 또는 potential의 수치 표본에 의존하지
않는다. finite box의 interior도 nonempty connected open radial interval을 가지므로 충분하다.
따라서 \(X=0\), \(\gamma\)는 상수이고 식 (10)에서 원래 multiplication coefficient
\(C\)도 상수다.

마지막으로 \([H,D\partial_N]=[H,D]\partial_N\)이다. 서로 다른 \(\partial_N\)
jet의 계수를 독립적으로 비교하면 \([H,D]=0\)이어야 하며, 그 1차 계수는
\(\partial_aD=\partial_\phi D=0\)을 준다. 결론은

\[
\boxed{\quad O=cI+d\partial_N=cI+i d\,p_N,\qquad c,d\in\mathbb C.\quad}
\tag{16}
\]

이다. 이는 선언한 1차 local strong class의 완전한 분류다.

## 5. repaired carrier, 쌍대 상태 및 formal adjoint에 대한 결과

식 (3)의 정의에서 H와 p_N은 각각 k 또는 m을 하나 증가시키므로 \(H\Phi\subset\Phi\),
\(p_N\Phi\subset\Phi\)다. 그러므로 식 (16)의 모든 O도 \(\Phi\)를 보존한다.
Flat pairing에서는 other-face collars와 a=2의 common Neumann trace로 Green boundary
form이 사라져 H는 이 test space에서 formally symmetric이다. N collars로 p_N도
formally symmetric이다. 따라서 formal star는

\[
(cI+d p_N)^*=\bar cI+\bar d p_N.
\tag{17}
\]

이며 real c,d의 조합이 formally symmetric이다. 이는 self-adjoint closure, spectrum 또는
positive physical product에 대한 결론이 아니다.

동일한 이유로 \(\mathbb C[H,p_N]\)의 모든 polynomial은 \(\Phi\)를 보존한다.
Neumann Cauchy dual states는
\(T_g\circ H=T_g\circ p_N=0\)이므로

\[
T_g[P(H,p_N)u]=P(0,0)T_g[u].
\tag{18}
\]

즉 이 constraint-generated extension algebra는 모든 \(T_g\)에 동일한 scalar로
작용한다. seed \(g\), rank-one normalization, positive form 또는 CPT sewing data를
선택하거나 서로 다른 \(T_g\)를 구별할 수 없다.

## 6. 남는 질문

식 (16)은 관측가능량 후보가 없다는 보편적 no-go가 아니다. 다음은 이 결과의 범위 밖이다.

- 고차 local strong commutant와 그 formal adjoint/domain 분석,
- \([H,O]\)가 H와 p_N의 조합인 weak observable 또는 BRST cohomological normalizer,
- clock을 포함한 relational observable과 integral kernel 같은 nonlocal observable,
- observable-* algebra, physical product, ghost/residual sector 및 양쪽 boundary orientation을
  포함하는 실제 BFV/CPT 접합.

따라서 이번 결과의 올바른 해석은 좁다. 가장 단순한 strong local algebra는 현재의
쌍대 해족과 비정준적 양의 form에서 선택 원리를 제공하지 못한다. 다음 단계는 그보다 넓은
관측가능량 클래스를 명시하고, 그 작용이 \(\ker T\)와 form을 보존하는지 검사하는 것이다.

## 7. 검증 경계

주된 false-signal은 scaled equation 또는 다른 ordering의 symmetry를 실제 H의 strong
commutant로 오인하는 것이다. 관련 control은 (i) 식 (5)–(9)의 actual Weyl coordinate 및
similarity identity, (ii) 식 (11)–(15)의 coefficient comparison과 finite-open-interval
independence, (iii) p_N mixed-jet와 repaired carrier/formal-adjoint checks다.

Runner는 위 유한한 미분·commutator coefficient identities만 검사한다.
Killing classification, functional domain, formal symmetry의 해석과 higher-order exclusion은
이 유도문에서 명시한 analytic scope를 따른다. 이 문서 자체는 실행 성공 기록이 아니다.

## 8. 선택한 kernel과 양의 form은 무엇을 통과하는가

T≠0인 복소 선형함수와 Φ 위 endomorphism O에 대해

\[
O(\ker T)\subseteq\ker T
\quad\Longleftrightarrow\quad
T\circ O=\lambda_O T.
\tag{19}
\]

왼쪽이면 O가 Φ/ker T≃C에 내려가므로 scalar λ_O로 작용한다. 반대 방향은 즉시
성립한다. 또는 T(w)≠0인 w를 골라 u−T(u)/T(w)·w에 O를 적용하면 같은 식을 얻는다.
F_T(u,v)=bar(Tu)Tv에 대해 F_T(Ou,v)=F_T(u,O* v)를 요구하면
λ_(O*)=bar(λ_O)가 필요하다. 식 (16)과 C[H,p_N]는 모든 T_g에서 이를 통과하지만
항상 같은 P(0,0)이므로 seed나 양의 정규화를 선택하지 않는다.

반면 두 operator가 같은 T의 kernel을 보존하면 T([O₁,O₂]u)=0이다.
실제 물리 관측가능량에서 [O₁,O₂]=zI, z≠0이 주어진다면 비영 rank-one quotient는
불가능하다. 이는 조건부 obstruction이며, 우리 모형에서 그런 물리 관측가능량을
이미 얻었다고 주장하지 않는다.

Seed label 공간 G=C_c^∞((-1,2))의 Qg=φg, Pg=−i g'는 [Q,P]=iI를 만족하고
Cauchy 사상 U로 운반하면 UQg,UPg도 Neumann 제약해다. 그러나 이는 해의 label
변환이다. 시험공간 위 O_A를 얻으려면 모든 g,u에 대해
T_g(O_Au)=T_(Ag)(u)가 필요하다. R(u)(g)=T_g(u)로 쓰면 R O_A=A' R이므로
A' Ran R⊂Ran R이 필요하다. 적절한 Φ 보존 연속 lift/right inverse도 현재 구성하지
않았다. 실제 국소 φ와 −i∂φ는 [H,φ]=−2b∂φ, [H,−i∂φ]=iW_φ로 이미 strong
commutation을 실패한다. 따라서 seed Q,P를 물리 관측가능량으로 승격하지 않는다.

만약 위 lift를 요구한다면, 고정한 bump g₀=E(1−4φ²)에 대해 Qg₀=φg₀는 g₀의
배수가 아니다. 기존 g↦T_g의 injectivity와 식 (19) 때문에 이 lift는 ker T_g₀를
보존할 수 없다. 한 해만 택한 rank-one 선택과 이 seed 작용은 함께 유지될 수 없다.
쌍대 transpose는 합성 순서를 뒤집으므로 seed의 [Q,P]=iI와 대응 test lift의
교환자 부호를 무심코 동일시하지 않는다.

## 9. 상보적인 bosonic 경계 pairing까지 실제로 구성한다

기존 Neumann 해 s_g에 더해, 같은 실제 H의 Dirichlet Cauchy 해 t_h를 정의한다.
상수 x₂=log 2에서 χ_D=0, ∂xχ_D=h인 compact smooth data를 주고 t_h=aχ_D로
둔다. 표준 Cauchy 정리로 Ht_h=0, t_h(2)=0, ∂a t_h(2)=h이다. p_N t_h=0이다.

반대편 시험공간은 Φ_D={u:(H^k p_N^m u)|₂=0 for all k,m, other-face collars}로
명시한다. H,p_N 아래 불변이며 interior compact tests를 포함한다. 같은 Green
계산으로 T^D_h[u]=∫_B t_hu는 Φ_D에서 H,p_N을 소거하고, h≠0이면 비영이다.
이것은 Φ_N과 다른 공간이며 두 편극의 물리적 동등성을 가정하지 않는다.

실수 계수 H의 bilinear Green 식에서 선택한 순서는 ∫[(Hs)t−s(Ht)]이다.
그 upper-face flux는 f(s t_a−s_a t)다. 따라서

\[
W_{N,D}(s_g,t_h)
=-\frac1{48\pi^2}\int_{\mathbb R}g(\phi)h(\phi)\,d\phi.
\tag{20}
\]

Full R_φ Cauchy evolution의 compact propagation으로 이 Wronskian은 a에 따라
보존된다. 유한 φ-box의 lateral flux를 버리지 않는다. g≠0이면 h=bar(g)를 택해
식 (20)이 비영임을 보이므로 N×D pairing은 양쪽에서 비퇴화다. N×N과 D×D는
각각 0이다. 이는 실제 H의 두 Cauchy 해족 사이 **복소 bilinear bosonic pairing**이며
양의 sesquilinear 물리 내적은 아니다. 전 계수 −1/(48π²)는 coordinate ∂a trace와
명시한 Green 순서에서 나온다; metric unit-normal convention을 몰래 대입하지 않는다.

K=complex conjugation은 Neumann과 Dirichlet을 각각 보존한다. 그러므로 현 K는
비영 Neumann 해를 Dirichlet 쪽으로 옮기는 CPT/polarization-exchange 사상이 아니다.
Full BFV/CPT 단계에는 oriented ghost state spaces, 실제 seam kernel과 그 BFV
intertwining, residual BV fields/Δ, mQME 및 BV pushforward가 여전히 없다.
On-shell에서 H,p_N이 0이라는 사실만으로 off-shell graded sewing identity가
증명됐다고 보고하지 않는다. Source-defined original joint cycle도 제공하지 않았다.

## 10. 문헌과 결론 경계

- [Giulini–Marolf §II](https://arxiv.org/html/gr-qc/9812024)는 시험공간·formal star와
  관측가능량 작용, rigging map의 intertwining/양성을 구별한다. 이 논문의 조건이
  우리 모형의 self-adjoint realization을 자동으로 주지는 않는다.
- [CMR §2.4.4, 식 (2.36), Remark 2.37](https://arxiv.org/html/1507.01221)은 transverse
  polarizations 사이 pairing과 residual BV pushforward를 사용하며, (2.22)의 mQME와
  양립하는 경계 BFV operator를 요구한다. 식 (20)은 그 전체 구조 중 bosonic
  boundary-pairing 후보까지만 제공한다.
- Cauchy 해 존재·전파는 기존에 직접 읽은 [Bär–Ginoux–Pfäffle Theorem 3.2.11](https://arxiv.org/pdf/0806.1036v1)을
  같은 열린 R² extension에 적용한다. 실제 PDE 존재와 pairing 비퇴화의 적분 논증은
  해석적이며 Lean에서는 유한 kernel·commutator·boundary-jet 대수만 검증한다.

Discovery: `./ice literature search "Dirac observables partial complete observables Hamiltonian constraints boundary quantization rigging map" --json`,
UTC 2026-09-07T07:54:10.829Z. 검색 결과를 승격 근거로 삼지 않고 위 primary 원문을 확인했다.
이 작업의 출력은 **현재 strong local 선택의 비선택 결과와 상보적인 bosonic pairing**이다.
물리적 상태 공간·CPT 접합의 완성 또는 새로운 물리 발견이라는 결론은 아니다.
