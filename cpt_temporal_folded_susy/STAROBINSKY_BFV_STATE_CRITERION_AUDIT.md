# 보완한 시험공간, 물리적 상태, CPT 접합은 별도로 확인해야 한다

2026-09-07 · SUPPORTING_METHOD / SCOPED_ANALYTIC_AUDIT.

사용자가 확인을 요청한 기준은 방향은 맞지만, **시험공간 안에서 비영 물리적 상태까지
찾으라는 요구로 읽으면 현재 구성에서는 실패한다.** 정확한 판정은 다음과 같다.

| 항목 | 현재 확인되는 범위 |
| --- | --- |
| 보완한 시험공간에서 BFV 연산이 잘 정의되는가? | 공통 불변 smooth 공간의 대수적 differential로는 그렇다. Closed operator/graph core는 미해결이다. |
| 그 minimal 시험복합체에 ghost 수 0의 비자명한 상태가 있는가? | 없다. 양 N 경계에서 떨어진 지지 조건과 primary constraint 때문에 H^0=0이다. |
| 별도의 물리적 상태공간이 존재하는가? | 미해결이다. 시험공간의 자명성은 쌍대 제약해나 rigging construction을 배제하지 않는다. |
| CPT 접합까지 구현되는가? | 미해결이다. Quantum lift, 상태·측도·pairing·kernel을 구성하지 않았다. |

질문 하나: 현재 보완한 시험공간이 비자명한 물리 상태와 CPT 접합까지 동시에
확인해 주는가? 출력 하나: 위 분리 판정과 아래의 정확한 degree-zero 소거 증명.
비주장 하나: full BFV theory 또는 물리적 상태 일반의 부재를 주장하지 않는다.
주된 실패원인은 `inference` — 시험함수와 물리적 상태를 같은 공간으로 식별하는 오류다.

## 1. 고정한 입력

[Ward-domain 유도](STAROBINSKY_WARD_DOMAIN_DERIVATION.md)의 H, p_N=−i∂_N,
B=[1/2,2]×[-1,2]×[1/4,2], B_r=(∂_a−r(φ,N))|₂를 그대로 쓴다.
Φ₀는 complex smooth ambient 함수의 B 제한 중 a=2 이외의 모든 face 근방에서
0인 함수다. 고정된 smooth r에 대해 보완 공간은

\[
\Phi=\{u\in\Phi_0:B_rH^k p_N^m u=0\text{ for all }k,m\ge0\}.
\]

Ghost 좌표는 c,ρ 두 개이고 모두 degree +1이다. 검사 대상은
C^j=Φ⊗Λ^j(c,ρ), j=0,1,2이며 C^{-1}=0이다. Negative-degree antighost 좌표를
추가한 다른 polarization이나 full nonminimal BFV complex는 검사 대상이 아니다.

## 2. 대수적 BFV differential은 확보된다

H의 계수는 N과 무관하여 [H,p_N]=0이다. 이는 앞선 raw result의
`symbolic.checks.formal_H_primary_commutator`가 정확히 검사한 항등식이다.
정의의 모든 k,m 조건을 한 칸 이동하면 HΦ⊂Φ, p_NΦ⊂Φ이고, 국소 미분은
다른 face의 지지를 확대하지 않는다. 따라서 Ω=cH+ρp_N은 C^j→C^{j+1}로 작용한다.

\[
\Omega^2=c\rho(Hp_N-p_NH)=0,
\]

c²=ρ²=0, cρ=−ρc를 썼다. Φ는 interior C_c^∞(B°)를 포함하여 보조 L²(B,flat)에서
조밀하다. 그러나 조밀성, 대수적 불변성, nilpotency는 closed realization의 graph-core
성질이나 physical inner product를 대신하지 않는다.

## 3. 현재 minimal 시험복합체의 H^0는 0이다

u∈C⁰=Φ에 Ωu=0을 가정하자. c와 ρ의 선형 독립성으로 Hu=0과 p_Nu=0이다.
후자로부터 각 (a,φ)에 대해

\[
\partial_Nu(a,\phi,N)=0\quad\Longrightarrow\quad
u(a,\phi,N)=g(a,\phi),\qquad N\in(1/4,2).
\]

그런데 u는 N=1/4와 N=2의 collar에서 0이다. N 방향 상수함수가 한 collar에서
0이면 전체 구간에서 0이므로 g=0이고 u=0이다. 따라서

\[
\boxed{\ker(\Omega:C^0\to C^1)=\{0\},\qquad H^0(C^\bullet,\Omega)=0.}
\]

이 결론에는 H의 스펙트럼, potential 또는 Robin 계수를 풀 필요조차 없다.
한쪽 N collar만으로도 충분하다. Φ가 비영이고 조밀하다는 §2와 모순되지 않는다:
시험공간에 함수가 많다는 것과 제약을 만족하는 함수가 있다는 것은 다르다.
이 증명은 다른 ghost degree의 cohomology를 계산하지 않는다.

## 4. 시험함수의 쌍대에서 보는 primary 제약은 다르다

g(a,φ)를 내부에 지지된 비영 smooth 함수로 택하고

\[
T_g[u]=\int_B g(a,\phi)u(a,\phi,N)\,da\,d\phi\,dN
\]

를 Φ 위의 복소 선형 함수로 둔다. N 경계에서 u가 0이므로

\[
T_g[p_Nu]=-i\int g(a,\phi)[u]_{N=1/4}^{2}\,da\,d\phi=0.
\]

T_g는 비영이다: u=bar(g)χ(N), χ가 양의 적분을 갖는 내부 smooth bump이면
u∈C_c^∞(B°)⊂Φ이고 T_g[u]>0이다. 이는 **primary 제약의 쌍대 해**만을 보인다.
일반적인 g는 T_g[Hu]=0을 만족하지 않으므로 full constrained state는 아니다.
이 유한 N 구간에서는 T_g에 L² 대표가 있지만 그 대표는 현재 Φ의 N-collar 조건을
만족하지 않는다. 그러므로 여기서 모든 쌍대 상태가 nonnormalizable이라고 주장하지 않는다.

물리적 상태를 찾는 한 방법은 적절한 auxiliary realization과 시험공간 Φ를 고정하고,
Φ*에서 제약을 풀며 rigging map과 양의 physical product를 구성하는 것이다.
[Giulini–Marolf, §II](https://arxiv.org/html/gr-qc/9812024)는 이 구별을 명시한다.
그 논문은 algebraic dual을 사용하며, continuous dual을 선택할 경우 시험공간의
위상도 따로 정해야 한다. 논문의 자기수반 제약 등 가정을 이 WDW 문제에서 확인한
것은 아니다. η 또는 group average가 존재하거나 유일하다고 여기서 주장하지 않는다.

따라서 더 정확한 판단 기준은 다음과 같다.

> 선택한 시험복합체에서 BFV differential을 정의한 뒤, 명시한 상태 공간 또는
> 쌍대·완비화에서 비자명한 제약해/BRST class와 적절한 물리 내적을 구성할 수 있는가?
> 그 자료와 호환되는 quantum CPT 작용 및 실제 접합 pairing을 함께 정의할 수 있는가?

## 5. CPT 접합에는 추가 객체가 필요하다

K:u→bar(u)의 kinematic conjugation만으로 quantum CPT lift가 결정되지는 않는다.
Ghost 작용, 양쪽 면 방향, polarization, domain 및 half-density/Berezin convention을
지정해야 한다. 특히 유효한 BRST class가 exact representative의 선택에 의존하지 않게
접합 pairing이 내려가는지와 실제 bulk/seam kernel의 호환성을 확인해야 한다.

BV-BFV의 boundary state와 양의 physical Hilbert state도 자동으로 같은 객체가 아니다.
[CMR §2.3, 식 (2.22)](https://arxiv.org/html/1507.01221#S2.SS3)의 bulk state는
residual-field BV Laplacian까지 포함한
(ℏ²Δ+Ω)Z=0을 만족한다. [§2.4.4, 식 (2.36)](https://arxiv.org/html/1507.01221#S2.SS4.SSS4)의
gluing에는 boundary pairing과 residual fields의 BV pushforward가 함께 들어간다.
이는 섭동적 BV-BFV의 방법 문맥이며, 현재의 a=2 field-coordinate cutoff를 그 논문의
시공간 경계와 동일시하거나 ICE의 original cycle을 공급하는 정리가 아니다.

## 6. 검토와 provenance

이번 산출물은 해석적 검토이며 새 scientific runner나 Lean 실행을 보고하지 않는다.
§2는 이전 실행이 검산한 commutator와 ghost 대수의 손 전개, §3은 N 방향 상수함수와
support의 직접 증명, §4는 독립적인 쌍대 pairing 대조다. 독립 수학 읽기 감사에서
§2–3의 결론과 minimal ghost-degree 범위를 대조했고, 문헌 검토에서 시험공간/쌍대와
BFV state/mQME/gluing의 구별을 확인했다. 기존 raw check ledger는 변경하지 않았다.

입력은 commit `4b574379742d6d94f50275cf119b7edb60221b8d`의
`STAROBINSKY_WARD_DOMAIN_DERIVATION.md` (SHA-256
`a7a62e4084554eba5f1dd5b9100903f1ea689c448c9952062d69686daa2f098f`)와
`STAROBINSKY_WARD_DOMAIN_RESULT.json` (SHA-256
`929bc9d5acdf583e7335efa57255a2cca48665dced009b3fe4f6e35c9305c5e9`)이다.
문헌 discovery 명령은
`./ice literature search "refined algebraic quantization rigging map Phi Phi star distributional constraint solutions positive physical inner product" --json`이고,
UTC 2026-09-07T06:34:08.574Z에 `works: []`였으며 위 primary 원문을 직접 읽었다.

사전 planner는 `INSUFFICIENT_ROUTE_EVIDENCE`였다. 이 검토는 기존
`open:starobinsky-seam-ward-boundary-state-limit`의 scope를 좁힐 뿐, source-defined original
relative class 또는 signed global intersections를 공급하지 않는다. G1→G2→G3→G4→G5와
full-theory/empirical review의 미충족 dependency는 유지한다. 안정적인 여기의 zero 결과는
다른 상태공간, full BFV, 물리 CPT, original cycle 또는 모든 TOE의 반증이 아니다.
