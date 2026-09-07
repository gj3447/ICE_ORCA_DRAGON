# 실제 kernel 보정과 경계 class를 보존하는 공간의 조건

2026-09-07 · SUPPORTING_METHOD · SCOPED.

**Kernel 안에서 비영으로 작용하는 수반 호환 보정을 구성했다. 그러나 유한 rank
보정만으로는 현재 유한 해 quotient에 새로운 작용을 줄 수 없다.** 경계상태 쪽에서는
현재 compact 시험복합체의 비영 top-ghost class를 구성했고, 계수 공간을 algebraic
dual로 바꾸면 그 top class가 exact가 된다는 차이를 확인했다.

| 남은 문제 | 이번에 구성·판별한 결과 | 아직 성립하지 않는 결론 |
|---|---|---|
| 실제 kernel-active 보정 | Real interior bump f에서 w=∂_Nf, K_wu=⟨w,u⟩w를 구성. Bounded·self-adjoint·Φ 보존·RK_w=0·K_wp_N≠0 | [p_N,K_w]≠0이므로 이것 자체는 strong observable이 아님 |
| 보정으로 해·내적을 선택할 수 있는가 | 모든 bounded finite-rank K_0가 K_0,K_0†로 Φ를 보존하고 RK_0=AR를 만족하면 A=0. λI+K_0는 quotient에서 λI뿐 | Infinite-rank·unbounded·다른 정당화된 domain의 observable 전체를 배제하지 않음 |
| 실제 비영 BRST class | C=Φ⊗Λ(c,ρ)의 H²에 임의의 유한 개수만큼 독립 class를 구성하므로 H²는 무한차원 | H⁰(C)=0은 그대로. Degree 2를 물리적 degree 0으로 재지정하지 않음 |
| 분포 공간으로 옮긴 endpoint | 계수만 algebraic dual로 바꾼 복합체의 H²는 0. a=2 endpoint trace의 top-ghost 후보에는 명시적인 Heaviside primitive가 있음 | 이 복합체를 원래 quantum BFV state space나 전체 graded dual로 동일시하지 않음 |

이 결과는 “어떤 class가 비영인가?”에 **“어떤 지지·위상·ghost degree와 허용
primitive 아래에서 비영인가?”**를 추가한다. 두 공간 사이의 injection은 만들어도
cohomology를 보존하는 equivalence는 아닐 수 있다. 임의로 작은 공간을 택해 비영
class를 남기는 것만으로 물리적 상태를 선택했다고 할 수도 없다.

정확한 가정·증명·문헌과 입력은
[유도문](STAROBINSKY_KERNEL_CORRECTION_GHOST_SUPPORT_DERIVATION.md)에 있다.

## 1. 필요한 kernel 보정을 만들었지만 충분하지 않았다

기존 R=(T_1,…,T_n), R J=I의 실제 Cauchy/Gram 구성을 유지했다.
w=∂_N(F(a,φ)χ(N))를 real interior bump의 N 도함수로 택하면 Rw=0이다.
K_w의 range은 span{w}⊂Φ이고 수반도 같다. 실제로

\[
K_w p_N(p_Nw)=\|p_Nw\|^2w\ne0.
\]

따라서 앞선 quotient-only lift의 O_Ap_N=0 조건을 벗어나는 보정을 얻었다.
그러나 real w와 N collars 때문에 ⟨w,p_Nw⟩=0이고

\[
[p_N,K_w]w=\|w\|^2p_Nw\ne0.
\]

수반 조건과 kernel 작용을 확보하는 것, 제약과 양립하는 observable을 확보하는 것은
별개다. [RAQ 공통 정의역 조건](https://arxiv.org/html/gr-qc/9812024#S2.SS1)도 이 둘을 구별한다.

한 단계 넓혀 bounded finite-rank K_0 전체를 검사했다. Φ가 dense이고 K_0†가
finite-rank이므로 K_0†Φ⊂Φ이면 전체 ran K_0†⊂Φ다. 반면 R†의 image는
N-independent인 Cauchy 해의 span으로서 Φ와의 교집합이 0이다. 따라서

\[
R K_0=A R\quad\Longrightarrow\quad
K_0^\dagger R^\dagger=R^\dagger A^\dagger=0
\quad\Longrightarrow\quad A=0.
\]

이는 앞선 Op_N=0 정리의 반복이 아니다. 이번에는 kernel-active 연산자도 허용하지만
finite rank와 수반의 range 조건으로 label 작용을 제한한다. 기존 가중 내적 w의
자유도는 이 보정으로 선택되지 않는다.

## 2. 비영 class는 존재하지만 그 degree와 지지가 중요하다

같은 Φ의 coordinate-ghost differential은

\[
q_0u=(Hu,p_Nu),\qquad q_1(x,y)=Hy-p_Nx.
\]

Top class는 Φ/(HΦ+p_NΦ)에 해당한다. 모든 T_i가 분모를 소거하고 T_i(Je_j)=δ_ij이므로
서로 다른 [cρJe_j]는 독립이다. 임의의 n에 대해 이 구성이 가능하다.
따라서 **현재 시험복합체에 비영 cohomology가 전혀 없다는 결론은 틀리다.**
기존 결과는 정확히 H⁰=0이었고, 이번에 추가된 결과는 H²의 무한차원성이다.

계수만 Φ*alg로 바꾸고 H^tT=T∘H, p_N^tT=T∘p_N를 사용하는 별도 복합체에서는
p_N의 injectivity가 p_N^t의 surjectivity를 준다. 따라서 모든 top 계수 T에 대해

\[
p_N^tU=T\quad\Longrightarrow\quad c\rho T=\widehat Q(-cU).
\]

이 공간의 H²는 0이다. 이는 연속쌍대 전체에 대한 정리가 아니며, degree를 반전시키는
전체 graded dual의 결론도 아니다. 기존 T_g가 두 제약을 소거하는 비영 쌍대 해라는
결과는 유지된다. “모든 쌍대 상태가 사라진다”고 해석하지 않는다.

Bilinear inclusion ιz[u]=∫zu에는 p_N의 transpose 부호가 뒤집히므로
c→c, ρ→−ρ를 함께 적용해야 chain map이 된다. 그 사상은 injective이지만,
위 top class들은 exact가 되므로 quasi-isomorphism이 아니다.

## 3. 고전 endpoint의 직접적인 양자 분포 후보를 검사했다

앞서 구성한 ghost-fixed canonical endpoint를 선택한 coordinate-ghost 편극에서
표현하는 후보는 Ψ=cρD, D[u]=u(2,φ₀,N₀)다. a=2는 경계이므로 D를 열린 B° 내부의
Dirac 분포로 취급하지 않았다.

현재 C∞ test topology에서 연속인

\[
S[u]=\int_{N_0}^{2}u(2,\phi_0,N)\,dN
\]

를 사용하면 upper N-collar에 의해 p_N^tS=iD이고

\[
\Psi=c\rho D=\widehat Q\bigl(-c(-iS)\bigr).
\]

즉 이 후보는 closed이면서 exact다. S가 끝점까지 이어지는 지지를 허용하기 때문에
가능한 primitive이며, compact-N 조건이나 L² boundedness를 만족한다고 하지 않는다.

[CMR §2.3](https://arxiv.org/html/1507.01221#S2.SS3)는 편극과 half-density 상태공간,
양자 BFV 연산자, residual BV 자료 및 mQME를 함께 요구한다. 이번 분포 후보에는
그 전체 구성이 없다. 따라서 필요한 다음 입력은 **원래 source가 허용하는 상태와
primitive의 공간을 정하고, 그 공간에서 class 및 pairing이 잘 정의되는지 증명하는 것**이다.
실제 BFV/CPT kernel과 원래 적분 경로는 여전히 미구성이다.

## 4. 실행 기록과 검증 범위

- 명령: `./ice run starobinsky_kernel_correction_ghost_support`.
- 최종 source: `c0372db`.
- Status: `SCOPED_KERNEL_CORRECTION_NONSELECTION_AND_TOP_GHOST_SUPPORT_CONTRAST`.
- 기호 검산 **23/23**: 실제 Weyl/primary Green 부호, rank-one moment의 boundary 항,
  두 ghost 순서, coefficient-dual chain-map 부호 및 endpoint primitive.
- Lean **17/17**: FiniteRankCorrection **7**, TopGhostSupport **10**.
- Lean 4.33.0와 pinned mathlib, Python 3.13.5, SymPy 1.14.0.
- Strict warnings 유지. Source의 `sorry`/`admit`/local axiom 금지와 모든 정리의
  `propext`, `Classical.choice`, `Quot.sound` 허용 axiom 검사를 통과했다.

첫 source `1fb1c50`에서는 기호 검산 23개가 통과했지만 Lean이 rank-one scalar map의
`RingHom.id` 잔여 goal과 top-ghost 정리의 불필요한 section variable을 거부했다.
수정 `b188a76`에서는 finite-rank 정리 7개가 통과했고, `omit ... in` 앞의 doc comment
위치 때문에 나머지 모듈에 parse error가 남았다. `c0372db`에서 위치를 수정한 뒤
전체가 통과했다. 자체 생성 실패 JSON은 임시 보존했고 실패 사유는 이 보고서에 기록했다.

[raw result](STAROBINSKY_KERNEL_CORRECTION_GHOST_SUPPORT_RESULT.json)가 실제 환경·시간·
source hashes와 전체 check ledger의 정본이다.
[Runner](starobinsky_kernel_correction_ghost_support.py)와
[proof index](../formal/cpt_sewing/kernel-correction-ghost-support-proof-index.json)를 고정했다.

Actual Cauchy/PDE·compact bump 존재, finite-rank range와 dense carrier의 관계,
trace/primitive의 연속성, 무한차원성의 적용 및 실제 상태공간 해석은 유도문의
해석적 증명이다. Lean은 abstract adjoint/range, detector와 algebraic-dual exactness를
검증한다. 독립 정적 검토에서 이 적용 조건과 부호를 대조했다.

주된 실패 분류는 `inference`이며, 새 물리적 선택군이나 실험적 evidence를 만들지 않았다.
G1의 원래 joint relative class·signed intersections를 주지 않으므로 supporting으로 남는다.
물리적 내적·전체 BFV/CPT 접합·TOE 완성의 근거가 아니다.
