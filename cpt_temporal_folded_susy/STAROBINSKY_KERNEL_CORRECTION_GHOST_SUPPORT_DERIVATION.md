# Kernel 보정과 top-ghost class의 지지·계수 공간 판별

2026-09-07 · SUPPORTING_METHOD · SCOPED analytic derivation.

질문: 현재 Φ에 유한 rank 수반 호환 보정을 추가하고 고전 끝점을 분포로 옮기는
직접적인 보완이, 비자명한 관측가능량·양자 경계 class를 제공하는가?
출력: 실제 kernel-active 보정의 구성과 finite-rank 비선택 정리, compact 시험복합체와
coefficient-algebraic-dual 복합체의 top-ghost 판별.
비주장: 물리적 ghost-number-zero 상태·선택된 내적·원래 BFV/CPT 접합을 완성하지 않는다.

기준 commit은 `ee5f339cad206dcf151fd6b3d11ebb1fbbc61702`이다.
[앞선 실제 lift·canonical endpoint](STAROBINSKY_QUOTIENT_LIFT_BFV_BOUNDARY_DERIVATION.md),
[Cauchy 쌍대 해](STAROBINSKY_DUAL_CAUCHY_DERIVATION.md),
[degree-zero 시험복합체](STAROBINSKY_BFV_STATE_CRITERION_AUDIT.md)를 유지한다.
K=L²(B,flat), B=[1/2,2]×[-1,2]×[1/4,2], hbar=1, p=p_N=−i∂_N이다.
H는 앞선 unscaled Weyl 연산자, Φ는 모든 다른 face에 collar를 갖고
∂_a(H^k p^m u)|₂=0인 repaired Neumann 공간이다.

## 1. 실제로 작동하는 kernel 보정은 만들 수 있다

독립 Cauchy 해의 bounded 복소 선형 함수 T_i(u)=∫_B s_i u로
R:K→C^n을 정의한다. 앞선 compact-bump Gram section J는 R J=I를 만족하며,
R H=R p=0 on Φ다. 어떤 smooth real 비영 interior product bump
f(a,φ,N)=F(a,φ)χ(N)에 대해 w=∂_N f로 둔다. 그러면

\[
w\in C_c^\infty(B^\circ)\subset\Phi,\quad w\ne0,\quad Rw=0,
\qquad K_w u=\langle w,u\rangle_{L^2}w.
\tag{1}
\]

χ가 비영 compact bump이므로 χ'가 항등적으로 0일 수 없다. Rw=0은 N 적분과
χ의 양쪽 collar에서 따른다. K_w는 K 위 bounded rank-one self-adjoint이고
K_wΦ⊂Φ, K_w†Φ⊂Φ, R K_w=0이다. 따라서 O=λI+K_w는

\[
O=J(\lambda I)R+B,\qquad B=\lambda(I-JR)+K_w,\qquad RB=0
\tag{2}
\]

라는 실제 kernel 방향 보정을 포함한다.

p는 Φ에서 symmetric·injective이므로 pw≠0이며

\[
K_w p(pw)=\langle w,p^2w\rangle w=\|pw\|^2w\ne0.
\tag{3}
\]

이는 앞선 O_A p=0인 quotient-only lift와 다른 연산자다. 그러나 물리 observable은
아니다. w가 real이고 N collars를 가지므로
⟨w,pw⟩=−i∫w∂_Nw=0이고,

\[
[p,K_w]w=\|w\|^2pw\ne0.
\tag{4}
\]

즉 필요한 kernel 작용을 추가했다는 것만으로 constraint commutant 조건이
성립하지 않는다. H와의 commutator는 여기서 따로 분류하지 않는다.

## 2. 모든 bounded finite-rank 수반 호환 보정의 비선택 정리

K_0를 K 위 bounded finite-rank 연산자라 하고 K_0Φ⊂Φ 및 K_0†Φ⊂Φ를 요구한다.
추가로 R K_0=A R를 만족하는 유한 label 행렬 A가 있다고 하자. 그러면 **A=0**이다.

증명: Φ가 dense이고 K_0†가 continuous이므로 K_0†Φ는 ran K_0†에 dense다.
K_0†Φ는 finite-dimensional linear subspace이므로 K에서 closed이다.
따라서 ran K_0†=K_0†Φ⊂Φ다. 한편 S=ran R†는 N-independent Cauchy 대표들의
span이고, N-collar 조건에 의해 S∩Φ={0}이다. R J=I에서 R†가 injective임도 따른다.
수반을 취하면

\[
K_0^\dagger R^\dagger=R^\dagger A^\dagger.
\tag{5}
\]

왼쪽은 Φ, 오른쪽은 S에 들어가므로 둘 다 0이다. 따라서 A†=A=0이다.
R K_0=A R가 Φ에서만 주어졌더라도 양쪽이 bounded이고 Φ가 dense이므로 K로 연장된다.

따라서 O=λI+K_0에 R O=A R를 요구하면 반드시 A=λI다. 유한 rank 수반 호환 보정은
kernel 안에서 비영으로 작용할 수 있지만, 이 유한 Cauchy quotient에 새로운 작용을
줄 수 없다. 제약과의 strong commutation을 추가하기 전부터 성립하는 필요조건이다.

Finite rank가 핵심이다. Infinite-rank image의 dense subspace는 closed일 필요가
없으므로 위 논증을 모든 bounded observable로 확장하지 않는다. 모든 관측가능량이나
모든 상태공간의 부재도 아니다. 현재 w 내적 자유도를 이 유한 보정으로 선택하지 못한다.
[Giulini–Marolf §II.1](https://arxiv.org/html/gr-qc/9812024)의 observable-* 공통 정의역
조건을 판별 기준으로 사용했으며, 그 논문이 우리 모형의 결론을 증명해 주는 것은 아니다.

## 3. 실제 시험복합체에는 비영 top-ghost class가 존재한다

기존 coordinate ghosts c,ρ의 degree는 +1이고 순서는 cρ다. C^j=Φ⊗Λ^j(c,ρ)에 대해

\[
q_0u=(Hu,pu),\qquad q_1(x,y)=Hy-px,\qquad q_2=0.
\tag{6}
\]

여기서 (x,y)는 xc+yρ의 계수다. [H,p]=0으로 q_1q_0=0이고,

\[
H^2(C)=\Phi/(H\Phi+p\Phi)\;c\rho.
\tag{7}
\]

모든 T_i는 HΦ+pΦ를 소거한다. 따라서 앞선 실제 Gram section의 v_j=Je_j에 대해

\[
\sum_jz_j[c\rho v_j]=0\quad\Longrightarrow\quad
T_i\left(\sum_jz_jv_j\right)=z_i=0\quad\text{for every }i.
\tag{8}
\]

임의의 유한 n에 대해 독립 compact seeds를 고를 수 있으므로 **현재 C의 H²는
무한차원**이다. 이는 실제 Cauchy 함수와 interior bump 적분으로 검출한 class다.
PDE 또는 Gram 적분의 수치 array를 계산했다는 뜻은 아니다.

기존 H⁰(C)=0과 모순되지 않는다. 그 결론은 p의 injectivity에서 나왔고 그대로다.
이번 class의 degree는 2이며, 물리적 ghost number를 재지정하거나 physical H⁰로
이동시킨 것이 아니다. H¹ 전체를 계산하지 않았다. 양의 물리 내적도 선택되지 않았다.

## 4. 계수만 algebraic dual로 바꾼 복합체에서는 top class가 사라진다

별도 복합체를 명시한다:

\[
\widehat C^j=\Phi^*_{\rm alg}\otimes\Lambda^j(c,\rho),\qquad
H^tT=T\circ H,\quad p^tT=T\circ p,\quad
\widehat Q=cH^t+\rho p^t.
\tag{9}
\]

이는 **계수 공간만 dual로 바꾸고 ghost degree를 유지한 복합체**다. 전체 C의
graded dual은 degree를 반전시키므로 (9)와 다르다. (9)를 원래 quantum BFV state
space나 RAQ의 observable dual representation으로 동일시하지 않는다.

p가 Φ에서 injective이므로 p^t는 algebraic dual에서 surjective다. 임의 T에 대해
ran p 위 U(pu)=T(u)로 두고, 이 선형 함수를 Φ 전체로 연장하면 p^tU=T이다.
따라서

\[
c\rho T=\widehat Q(-cU),\qquad H^2(\widehat C)=0.
\tag{10}
\]

여기서 선형 연장은 algebraic choice이며 특정 continuous dual에서의 연속성을
주장하지 않는다. 반대로 시험공간 Φ의 top class에 이 surjectivity를 적용하지 않는다.

두 복합체의 비교에는 부호도 필요하다. Bilinear inclusion ιz[u]=∫_B zu는 shared
Neumann Green 조건과 N collars로

\[
H^t\iota z=\iota Hz,\qquad p^t\iota z=-\iota pz
\tag{11}
\]

를 만족한다. 따라서 ι와 함께 c→c, ρ→−ρ를 보내는 사상이 chain map이다.
Top 성분 cρz는 −cριz로 간다. 이 사상은 injective이지만, (8)의 class들은 (10)에서
exact가 되므로 quasi-isomorphism이 아니다. Injection과 cohomology equivalence를
혼동하지 않는다. 이 부호는 bilinear transpose convention에 따른 것이며,
sesquilinear Riesz inclusion이나 ket의 분포 미분과 섞지 않는다.

## 5. 고전 endpoint의 직접적인 분포 후보는 명시적으로 exact다

앞선 L_q0에서 a₀=2, φ₀∈(−1,2), N₀∈(1/4,2)를 고른다. Selected coordinate ghost
편극에서 δ(c)δ(ρ)=cρ라는 후보를 쓰면 endpoint trace

\[
D_{q_0}[u]=u(2,\phi_0,N_0),\qquad \Psi_{q_0}=c\rho D_{q_0}
\tag{12}
\]

를 얻는다. a=2는 B의 경계이므로 이를 D'(B°)의 내부 Dirac으로 쓰지 않는다.
Φ에 ambient smooth restriction의 C∞ seminorm topology를 주면 이 trace는 연속이다.
상응하는 scalar function space·half-density와 ghost-number shift는 물리적으로
선택되지 않았고, (12)는 검사용 coordinate 분포 후보일 뿐이다.

명시적 연속 functional

\[
S[u]=\int_{N_0}^{2}u(2,\phi_0,N)\,dN,\qquad V=-iS
\tag{13}
\]

에 대해 upper-N collar를 쓰면

\[
p^tS[u]=-i\,[u(2,\phi_0,N)]_{N_0}^{2}=iD_{q_0}[u],\qquad
p^tV=D_{q_0},\qquad \Psi_{q_0}=\widehat Q(-cV).
\tag{14}
\]

따라서 이 endpoint 후보는 closed이면서 exact다. S는 끝점까지 이어지는 지지를
가지므로 compact-N 제한을 보존하는 primitive가 아니다. S와 D는 이 C∞ topology에
연속이지만 L²-bounded functional로 취급하지 않는다. 임의의 다른 completion에서는
(13)의 허용 여부를 먼저 확인해야 한다.

동일 endpoint에 ghost-free D만 쓰면 p^tD[u]=−i∂_Nu(q₀)가 일반적으로 비영이다.
Ghost top factor에 의한 자동 closure와 비자명한 cohomology는 다르다.
D와 p^tD의 비영 witness는 φ₀에서 비영인 기존 Neumann Cauchy seed 해를 상단의
작은 a-collar에서 유지하고 그 아래와 φ 밖에서 cutoff한 뒤, N₀의 값/도함수를
독립 조절하는 interior N bump를 곱해 얻는다. 모든 H^k Neumann jets와 다른 face
collars를 함께 만족시킬 수 있다. 단순 polynomial을 실제 Φ witness로 쓰지 않는다.

[CMR §2.3, 식 (2.22), Remark 2.24](https://arxiv.org/html/1507.01221#S2.SS3)는
편극·half-density·양자 BFV 연산자·residual BV 자료와 cohomology equivalence를 구별한다.
우리 (9)의 chain injection은 그 equivalence 조건을 충족하지 않는다. 양자 경계에서
실제로 허용하는 exact representatives를 정하고 graded pairing과 residual pushforward를
구성해야 CPT/sewing으로 갈 수 있다. 원래 적분 경로나 규제 제거는 여기서 정하지 않았다.

## 6. 검증 범위와 재현 입력

주된 실패 분류는 `inference`다. Controls는 (i) 실제 kernel-active correction과
finite-rank range 분리, (ii) ghost degree·transpose/Green 부호,
(iii) compact class detector와 endpoint primitive의 지지 조건 세 묶음이다.
새 state domain이 같은 물리 이론의 허용 선택군이라는 가정은 하지 않는다.

Runner `./ice run starobinsky_kernel_correction_ghost_support`는 실제 Weyl/primary
Green 계수, 두 ghost 대수, chain-map 부호와 endpoint primitive를 기호 검산하고
두 Lean module을 검증한다. Lean은 finite-rank range의 analytic 적용, smooth/PDE
해 존재, 적분·trace의 연속성 또는 전체 BV–BFV 양자화를 증명하지 않는다.
실제 출력·실패·환경·입력 hash의 정본은 인접 raw result다.

Discovery 명령은 `./ice literature search "refined algebraic quantization observable
adjoint invariant test space boundary BFV polarization cohomology" --json`,
UTC `2026-09-07T09:23:21.590Z`다. Discovery metadata를 evidence로 쓰지 않고 위
Giulini–Marolf와 CMR primary 원문을 직접 대조했다. Bär–Ginoux–Pfäffle
Theorem 3.2.11의 적용과 실제 Cauchy data는 pinned 기존 유도를 사용한다.

Planner는 질문의 upstream 용어로 `CURRENT_BLOCKER_CANDIDATE`를 반환했다.
사람의 typed-object 검토에서는 원래 regulated joint class·signed intersection vector를
전혀 공급하지 않으므로 G1 후보로 채택하지 않았다. 본 작업은
`open:starobinsky-seam-ward-boundary-state-limit`의 supporting 결과다.
G1→G2 kernel→G3 gluing→G4 state/domain→G5 interaction→full-theory/empirical review의
미충족 upstream dependency와 물리 승격 금지는 그대로다.
