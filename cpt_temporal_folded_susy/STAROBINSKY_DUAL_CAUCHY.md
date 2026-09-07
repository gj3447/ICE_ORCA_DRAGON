# 실제 두 제약을 만족하는 쌍대 해족 구성과 물리 내적의 남은 선택

2026-09-07 · SUPPORTING_METHOD · SCOPED.

**이번에는 실제 Weyl H와 p_N을 동시에 소거하는 비영 쌍대 상태를 구성했다.**
Neumann 경계조건을 선택한 repaired 시험공간에서 무한차원 해족을 얻는다.
그러나 이 해족의 통상적인 Klein–Gordon(KG) form은 모든 쌍에서 0이다.
선택한 한 해로 양의 1차원 quotient는 만들 수 있지만, 그것이 물리적 선택이라는
결론이나 full BFV/CPT 접합은 아직 얻지 않았다.

| 판단 | 이번 결과 | 근거의 범위 |
|---|---|---|
| repaired 시험공간의 minimal degree-zero cohomology | 기존의 0 결론 유지 | N-collar 조건과 p_N 제약; 쌍대 해를 배제하지 않음 |
| 같은 공간의 쌍대에서 H와 p_N을 함께 만족하는 비영 해 | Neumann 선택에서 구성됨; seed에 대해 injective | 실제 operator 변환 + 표준 Cauchy 정리 + Green identity |
| 해족 위 자연 KG form | 모든 쌍에서 0 | 전체 R_φ current와 공통 terminal 조건 |
| 명시한 양의 form과 conjugation | 선택한 rank-one quotient에서 성립 | 특정 실수 seed를 고른 비정준적 구성 |
| 관측가능량과 양립하는 물리 내적·full CPT 접합 | OPEN | observable-* intertwining, ghost/BV kernel 등이 없음 |

## 해를 실제로 정의한 방법

이전 [criterion audit](STAROBINSKY_BFV_STATE_CRITERION_AUDIT.md)의 flat density,
hbar=1, 실제 Starobinsky Weyl operator를 그대로 썼다. r=0은 이번에 명시적으로
택한 조건이며 물리적 유일성을 주장하지 않는다.

x=log a, s=aχ로 바꾸면 정확히

\[
24\pi^2a^2H[a\chi(\log a,\phi)]
=\chi_{xx}-6\chi_{\phi\phi}
+\left[-\frac12-144\pi^4e^{4x}
+36\pi^4e^{6x}(1-e^{-\sqrt{2/3}\phi})^2\right]\chi.
\]

임의의 g∈C_c^∞((-1,2))에 대해 a=2에서 s=g, s_a=0을 주는 Cauchy data
χ=g/2, χ_x=−g/2를 택한다. 열린 R_x×R_φ에서 풀고 a∈[1/2,2]에 제한한다.
Smooth 실수 potential을 가진 normally hyperbolic equation이므로 compact Cauchy
data의 유일 smooth 해와 finite propagation을 얻는다.
[Bär–Ginoux–Pfäffle, Theorems 3.2.11–12](https://arxiv.org/pdf/0806.1036v1).

해 s_g를 N과 무관하게 연장하면

\[
T_g[u]=\int_B s_g u,qquad T_g[Hu]=T_g[p_Nu]=0.
\]

시험함수의 collar 조건과 upper Neumann 조건이 적분 경계항을 소거한다.
g≠0이면 내부 bump로 T_g≠0을 확인할 수 있으며 g↦T_g는 injective다.
완전한 논증은 [유도문 §§1–3](STAROBINSKY_DUAL_CAUCHY_DERIVATION.md)에 있다.
이는 Cauchy 문제로 해를 정의한 해석적 구성이다. 특수함수 닫힌꼴이나 수치 PDE
solution array를 계산한 결과가 아니다. a=0 극한도 다루지 않는다.

## 왜 비영 해가 있어도 물리 내적은 별도 문제인가

공통 terminal 조건 χ_x=−χ 때문에 KG current의 terminal 값이 0이고,
전체 R_φ에서 보존되므로 해족의 모든 쌍에서 KG form이 0이다. 해는 φ-box 밖으로
전파될 수 있으므로 유한 φ-box의 lateral flux를 0으로 놓지 않았다.
이 결과는 이 해족과 이 form에 한정된다.

실수 비영 seed 하나를 택하면 F_T(u,v)=bar(T[u])T[v]는 positive semidefinite이며,
Φ/ker T에서는 양의 1차원 내적이다. K:u↦bar(u)는 이 quotient에 antiunitary
involution으로 내려간다. 하지만 다른 독립 seed를 고르면 kernel이 달라지고,
임의의 양의 rescaling도 가능하다. 따라서 positivity와 K만으로는 선택이 결정되지 않는다.

K는 kinematic conjugation이다. Ghost와 boundary orientation을 포함한 CPT 작용,
관측가능량의 *-구조와 intertwining, constraint self-adjoint realizations나 group
averaging은 구성하지 않았다. 그러므로 이 form을 RAQ rigging map이나 선택된 물리
Hilbert 공간이라고 부르지 않는다.
[Giulini–Marolf §II](https://arxiv.org/html/gr-qc/9812024).
기존 [CMR modified QME와 gluing](https://arxiv.org/html/1507.01221)의 bulk/seam
kernel 문제와 original integration cycle도 그대로 남는다.

이 결과가 정확하게 만든 질문은 다음과 같다: **명시한 관측가능량의 *-대수와 실제
접합 구조가 해족·내적·정규화를 함께 선택하며, 그 선택 뒤에도 비영 상태가 남는가?**
이는 열린 질문의 정밀화이며 후속 계산의 자동 승인은 아니다. G1 original class나
signed global intersection을 제공하지 않았으므로 core TOE 진전으로 세지 않는다.

## 실행과 검증 경계

- 명령: `./ice run starobinsky_dual_cauchy`.
- Source commit: `bba3ed8702d5c4e929cd65f2a531bf1147f004ec`.
- UTC 시작: 2026-09-07T06:59:18.886413+00:00; runner elapsed 3.026 s; exit 0.
- 실제 출력: `SCOPED_NEUMANN_CAUCHY_DUAL_FAMILY_WITH_DEGENERATE_KG_FORM`.
- SymPy 1.14.0 / Python 3.13.5: exact identity controls **16/16**.
- Lean 4.33.0: finite complex coefficient theorems **4/4**; 허용 axioms
  `propext`, `Classical.choice`, `Quot.sound`; warning/error 없음.

[Raw result](STAROBINSKY_DUAL_CAUCHY_RESULT.json)가 실제 check ledger와 입력 hash의
정본이다. [Runner](starobinsky_dual_cauchy.py)와
[Lean source](../formal/cpt_sewing/CptSewing/DualState.lean)는 재현 가능한 범위만 검사한다.
PDE 존재·유일성, 쌍대 injectivity와 quotient 구성은 유도문의 해석적 증명이며
Lean으로 증명한 것으로 보고하지 않는다. 별도 수학 검토에서 변환·경계·KG·quotient
논증을 대조했다. 유도문 끝의 미실행 표시는 source commit 당시의 상태이며 실제
실행 결과는 이 보고서와 raw result에 기록했다.

주된 실패원인은 `inference`다. Control은 실제 Weyl 변환, Green/current/primary,
rank-one form 범위의 세 묶음이다. 계산적·해석적 사실과 물리적 선택을 분리했으며,
KG의 zero 결과를 숨기거나 원하는 내적으로 대체해 물리 주장으로 승격하지 않았다.
