# Ward 소거 조건에서 BRST 공통 시험공간으로 가는 데 필요한 추가 조건

2026-09-07 · SUPPORTING_METHOD · 해석적 유도 정본.

질문: a=2의 local Robin/Dirichlet 조건 하나로, 모든 ghost 계수에 같은
smooth 시험공간을 사용하는 BFV 연산의 불변 공간을 얻는가?
출력: 이 특정 ansatz의 불변성 판별식과 smooth 반례.
비주장: 자기수반 Robin 확장의 부재, BRST anomaly 또는 물리적 CPT 위반을 주장하지 않는다.

현재 질문은 `open:starobinsky-seam-ward-boundary-state-limit`을 직접 좁힌다.
사전 planner는 `INSUFFICIENT_ROUTE_EVIDENCE`였다. G1의 original relative cycle과
signed global intersections를 공급하지 않으므로 G1→G2→G3→G4→G5→full-theory/empirical
review에 대한 core 진전으로 세지 않는다. Choice-invariance path도 읽었다.
아래 서로 다른 boundary domains가 같은 물리 내용을 나타낸다고 가정하지 않는다.

## 1. 이전 극한 결과와 이번 domain ansatz

[앞선 유도](STAROBINSKY_WARD_FACE_LIMIT_DERIVATION.md)의 box, Weyl ordering,
hbar=1, flat density를 유지한다. a=0은 포함하지 않는다.

\[
H=-\partial_a(f\partial_a)-b\partial_\phi^2+W,\qquad
f=-\frac1{24\pi^2a},\quad b=\frac1{4\pi^2a^3},\quad W=U-f''/4,
\]
\[
U=-6\pi^2a+\frac32\pi^2a^3(1-e^{-\sqrt{2/3}\phi})^2,
\qquad p_N=-i\partial_N,\qquad\Omega=cH+\rho p_N.
\]

M=(0,∞)×R², B=[1/2,2]×[-1,2]×[1/4,2]. 이번 시험공간은
complex C_c^∞(M)의 B 제한이며 a=2 이외의 모든 면 근방에서 0이다.
r=r(φ,N)는 a와 무관하게 연장한 매끄러운 복소 함수다. 국소 경계 연산자는
B_r u=(∂_a u-r u)|₂, D_r^sm={u: B_r u=0}로 둔다.
이것은 smooth test space이며 closed operator domain이나 Hilbert graph core라고
이미 증명한 대상이 아니다.

검사하는 구체적 ansatz는 D_r^sm⊗Λ(c,ρ)이다. 모든 ghost 계수가 같은
D_r^sm에 속하고 Ω가 이 공간 자체로 되돌아온다고 요구한다.
Ghost-free u에 Ω를 작용시키면 독립 계수 Hu와 p_Nu가 생기므로
H D_r^sm⊂D_r^sm, p_N D_r^sm⊂D_r^sm가 이 ansatz에 필요하다.
이는 모든 가능한 BRST graded domain에 대한 필요조건이라는 뜻이 아니다.

## 2. 복소 boundary flux의 소거와 비선택

이전 분포 pairing에서 첫 시험함수를 bar(u)로 바꾸면, H의 계수가 실수이므로
같은 Green 계산으로 다음 sesquilinear boundary functional을 얻는다.
선택한 순서는 (Hu,v)−(u,Hv), (u,v)=∫bar(u)v다.

\[
\beta(u,v)=f(2)\int[\bar u\,v_a-\overline{u_a}\,v]_2\,d\phi dN.
\]

Common Robin 조건에서는 integrand=f(2)(r−bar(r))bar(u)v다.
따라서 자유롭게 국소화할 수 있는 모든 smooth boundary traces에 대해 β=0일
필요충분조건은 r가 실수라는 것이다. 필요성은 Im(r)가 0이 아닌 한 점 주변에서
부호가 일정한 작은 bump u=v를 택해 보인다. Complex r=i는 반례다.
Dirichlet은 값 trace가 0인 별도 경우다.

K u=bar(u)는 D_r^sm을 D_bar(r)^sm으로 보내므로 모든 real r가 K에 보존된다.
이 조건만으로 r=0 또는 특정 r가 선택되지 않는다. K는 실수 계수 H와 교환하고
p_N의 부호를 뒤집는 kinematic conjugation이며 full CPT/BFV lift가 아니다.
고전 (q,p)→(q,−p)의 부호를 ∂a trace에 또 삽입하지 않는다. Quantum lift,
양쪽 면의 방향, ghost/half-density 작용이 없으면 그 삽입은 정당화되지 않는다.

## 3. Primary lapse constraint가 드러내는 조건

Product rule과 B_r u=0의 N 미분으로

\[
B_r(p_Nu)=-i(\partial_N r)u|_2.
\tag{1}
\]

그러므로 boundary trace가 자유로운 전체 D_r^sm에서 p_N 보존은 r_N=0일 때만
가능하다. 충분성도 식 (1)에서 즉시 나온다. r=N은 real이고 K/Green 조건은
통과하지만 p_N 조건을 실패한다. u=η(a)e^{N(a−2)}ψ(φ,N)를 쓰면
B_Nu=0, B_Np_Nu=−iψ다. ψ는 face interior의 임의의 비영 smooth compact bump이고
η는 앞선 유도의 cutoff로 a=2 근방에서 1이다. 따라서 이 예시는 실제 smooth
함수이며 형식적 독립 jet 대입에만 의존하지 않는다.

## 4. r를 실수 상수로 제한해도 H 보존은 자동으로 생기지 않는다

아래 계수와 jets는 모두 a=2에서 평가한다. B_r u=0와 그 φ 미분을 이용하면

\[
\begin{split}
B_r(Hu)={}&-f u_{aaa}+(rf-2f')u_{aa}-b'u_{\phi\phi}
-2b r_\phi u_\phi\\
&+(W_a-rf''+r^2f'-b r_{\phi\phi})u.
\end{split}
\tag{2}
\]

r가 real/N-independent이어도 자유로운 세 번째 normal derivative는 남는다.
v₃=(a−2)³η(a)ψ(φ,N)는 모든 smooth r에 대해 B_rv₃=0이다. 그러나
v₃=v₃,a=v₃,aa=0, v₃,aaa=6ψ라서

\[
(Hv_3)|_2=0,\qquad
\boxed{B_r(Hv_3)=\frac{\psi}{8\pi^2}\ne0.}
\tag{3}
\]

횡방향 미분과 potential 항은 이 예시에서 face의 zero jets 때문에 없어지며
W를 버린 toy operator로 계산한 것이 아니다. Dirichlet로 바꾸어도
v₂=(a−2)²ηψ에 대해

\[
v_2|_2=0,\qquad (Hv_2)|_2=\frac{\psi}{24\pi^2}\ne0.
\tag{4}
\]

그러므로 D_r^sm⊗Λ(c,ρ)와 같은 Dirichlet ansatz는 Ω 아래 불변이 아니다.
식 (3)–(4)의 수치는 boundary-condition residual이며 이전 Ward weak-limit
값이나 anomaly 크기, 에너지 또는 관측량이 아니다.

## 5. 무엇을 보완해야 하는가

자기수반성은 H D(H)⊂D(H)를 요구하지 않는다. 그러므로 위 반례로 자기수반
Robin/Dirichlet extension을 부정하면 오류다. BFV의 모든 ghost sector에 같은
smooth 공간을 쓰려는 이번 ansatz가 부족하다는 것만 결론낸다.

이 ansatz를 유지하려면 같은 미분식으로

\[
\mathcal D_{r,\infty}^{sm}=
\{u:B_rH^k p_N^m u=0\ \text{for every }k,m\ge0\}
\]

같은 공통 불변 시험공간을 검토할 수 있다. [H,p_N]=0이고 support가 국소 미분으로
확대되지 않으므로 이 집합은 H,p_N 아래 대수적으로 불변이다. Interior compact
tests를 포함하므로 L²(B,flat)에서 조밀한 부분집합을 갖는다. 그러나 이것만으로
선택한 closed operator의 graph core, nonzero face trace, physical cohomology,
positive physical product 또는 sewing state를 얻지 않는다. 예컨대 r가 N에 의존하면
첫 식 (1)이 이미 허용 face traces를 줄인다.

다른 가능성은 ghost degree별로 다른 domains를 명시하는 것이다. 어느 것을 채택할지
이번 계산은 선택하지 않는다. 필요한 다음 입력은 실제 closed realizations 또는
graded domains와 quantum CPT trace action이다. 결과가 새 계산을 자동 생성하지 않는다.

## 6. 출처와 검증의 역할

- [Bonneau–Faraut–Valent, quant-ph/0103153](https://arxiv.org/html/quant-ph/0103153),
  §2는 Hψ와 H²ψ의 domain 혼동을, §4는 operator 정의와 결손지수·자기수반 확장을,
  §7.1은 conjugation이 boundary domain에도 적용되어야 함을 설명한다.
- [Asorey–Ibort–Marmo, hep-th/0403048](https://arxiv.org/html/hep-th/0403048),
  §2의 maximal-isotropic/Cayley parametrization은 domain 선택의 방법 문맥이다.
  그 regular Riemannian elliptic operator 정리를 여기의 indefinite WDW 식에
  그대로 적용하지 않는다. 새 식 (1)–(4)의 직접 증거는 위 유도와 runner다.

Discovery 명령은 `./ice literature search "complex sesquilinear Green boundary form maximal isotropic unitary parametrization antiunitary symmetry self-adjoint extensions" --json`이며,
UTC 2026-09-07T06:03:05.779Z의 OpenAlex 결과는 `works: []`였다.
위 원문을 웹으로 직접 읽었다. 주된 실패원인은 algebra/domain inference다. 관련 control은
(i) complex conjugation과 primary product rule, (ii) actual H의 full jet formula와
smooth counterexamples, (iii) 독립 finite Lean jet algebra의 세 묶음이다.

Lean은 finite complex/real jet identities만 검증한다. Smooth realization, 함수공간
범위와 해석은 이 문서에 있으며 독립 수학 읽기 검토로 대조한다. 실제 실행 성공과
환경·입력 hashes는 `STAROBINSKY_WARD_DOMAIN_RESULT.json`에만 기록한다.
