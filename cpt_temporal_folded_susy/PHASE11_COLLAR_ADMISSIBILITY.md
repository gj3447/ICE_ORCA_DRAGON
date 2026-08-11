# Phase 11 — collar 변형의 제약-수준 허용/금지 분류 (G43–G46 예비)

> **공정 주석**: 패러다임 전환(사용자 verdict 2026-08-10) 공정 유지 — 검증 명령 하나.
> **v2 (2026-08-11)**: 5-반박자 적대 감사 반영 — v1의 exact 계산은 전부 재현됐으나
> 해석 6건이 교정됐고, 교정 내용 자체가 새 정리가 됐다. 감사 체크는 실행체에 흡수됨.
>
> 검증: `uv run --with sympy python3 phase11_collar_admissibility.py` → exit 0.

- cycle: `cpt-temporal-folded-susy-2026-08-09-phase11`
- scientific verdict: `UNJUDGED` (유지) / programme appraisal: `UNAPPRAISED` (유지)
- **식 번호 E152–E156** (v1의 E147–E151은 PHASE8_REPORT.md의 `\tag{E147}`/`\tag{E148}` 및
  원장 등록과 **실충돌**이라 재번호. Phase 9/10의 E136–E146도 Phase 8 계보 E136–E148과
  겹친다 — 상속된 충돌로 **표기만 하고 수리하지 않는다**.)

## 0. 질문

Phase 9·10의 다음 관문(여럿 중 관측-map 유효성의 관문): 관측을 만드는 collar
변형들은 **허용되는가, 강제되는가?** 판정 기준은 Phase 7이 스스로 쓴 제약 보존
\(\{C,H_\Sigma\}=0\) (E130) — strong 독해를 1차 기준으로 선언하고, weak(Dirac
1급) 대안은 **계산하되 판정하지 않는다**.

## 1. E152 — 분류 정리 (strong, 동차 2차, 전체 6차원)

\[
\{C,H\}\equiv0
\iff
H=q^TMp+\tfrac12p^TDp,\quad \eta M^T+M\eta=0\ (M\in\mathfrak{so}(1,2)),\quad D\ \text{자유};
\qquad A\equiv0\ \text{강제}.
\tag{E152}
\]

- 합법 \(q\)-\(p\) 블록 = 쌍 회전 1 + 혼합부호 α↔β **부스트 2** (부호 반전 덕에 대칭
  조합이 합법). 부스트 관측 map은 ω-함정(PHASE9_NULL §2.1)이라 유보.
- **Phase 9 대칭 squeezer는 쌍 블록에서 strong·weak 모두 사망**:
  \(\{C,q_+p_-+q_-p_+\}=-2p_+p_-\) (on-shell witness \(-24\), \(\lambda C\) 꼴 아님).
- 차수 ≤1: \(q\)-선형 금지, \(p\)-선형(변위)·상수·\(g(C)\) 합법 — 행렬의 범위는
  **동차 2차**로 한정 선언.

## 2. E153 — 기준 의존성: dilation이 squeezer map을 부활시킨다

전체 공간에서 weak 기준 \(\{C,H\}=\lambda C\)는 정확히 **한 방향**을 추가한다:
dilation \(H_{\rm dil}=q\!\cdot\!p\), \(\{C,q\!\cdot\!p\}=-2C\) (제약면 \(C=0\) 정확 보존).
그 흐름은 모든 모드의 단일모드 squeezer(\(\alpha=\cosh s,\beta=\sinh s\))이고

\[
r_{\rm obs}=r_{\rm vac}\left(1+2\sinh^2 s\right)
\tag{E153}
\]

— **Phase 9 E139 map 그대로다**. 따라서 v1의 "E139–E140 강등"은 기준-의존이다:
strong(E130의 조작적 독해)에선 도달 불가, weak에선 \(C\)를 건드리지 않고 도달
가능. (쌍 블록만 보면 weak는 \(\lambda=0\)이 강제라 아무것도 추가하지 않는다 —
v1 §1b는 그 범위에선 옳았다.)

## 3. E154 — 두-종: 회전-형은 강제, 퇴화는 관례

종 운동항 \(\tfrac12(c_1p_\zeta^2+c_2p_S^2)\) 확장에서 일반 종-혼합자의 합법 조건:

\[
n_{11}=n_{22}=0,\qquad c_1n_{12}+c_2n_{21}=0.
\tag{E154}
\]

- **회전-형 혼합만 합법** (\(n_{12}n_{21}<0\) 항상 — squeezer-형 불가): Phase 10
  E144 표의 빈 칸(대칭×두-종)은 **모든 \(c_1,c_2\)에서 FORBIDDEN**으로 닫힌다.
- 그러나 임의 \(c_1\ne c_2\)에서도 기울어진 합법 혼합자
  \(H'=q_\zeta p_S-(c_1/c_2)q_Sp_\zeta\)가 존재하고, 정준 재척도가 \(c_1/c_2\)를
  완전히 제거한다: **퇴화 \(c_1=c_2\)는 유도된 필연이 아니라 정규화 관례다**
  (v1의 "A4′ 필연 승격"은 철회). 살아남는 정확한 진술: 물리 변수에서 파워-보존
  등가중 map \(\beta_{\rm iso}=\sin^2\theta_c\)(E143)를 원하면 \(c_1=c_2\);
  기울어진 혼합자는 \(c_1/c_2\) 진폭 인자가 붙은 CDI를 만든다. A4′의 물리적
  내용(실제 (CDM, radiation) 쌍의 퇴화)은 **여전히 가정**이며, ω-판 동형 결과는
  PHASE9_NULL §2.3이 이미 유도했었다.
- 두-종 **shear** \(p_\zeta p_S\)는 모든 \(c_1,c_2\)에서 합법 (퇴화 불요).

## 4. E155 — 운동량 shear: 조건부 tensor 채널 (긴장 선언)

합법 \(D\)-클래스는 관측적으로 공집합이 아니다. Bogoliubov (exact):
\(\beta=i\sigma D/2\), \(\langle N_j\rangle=\tfrac{\sigma^2}4(D^2)_{jj}\)
(\(\sigma=s\omega\)). 교차-shear \(p_+p_-\): 위상평균 \(F=1+\sigma^2/2\);
단일모드 \(p_+^2/2\): \(F=1+\sigma^2/4\), **편광 비대칭** 신호. 결맞음 범위
\(F\in[1,\,1+\sigma^2]\) — shear는 **절대 억제하지 않는다** (squeezer의 ×0.043
분지와 구별되는 서명).

**선언된 긴장 (미해소)**: 신호가 사는 ω-레벨에서 PHASE9_NULL §2.2/2.3 게이트가
**둘 다 실패**한다 — \(\{C_\omega,p_+p_-\}=\omega^2(q_+p_-+q_-p_+)\ne0\) (위반
방향이 정확히 금지된 squeezer)이고 \([A_\omega,K_{\rm shear}]\ne0\). 회전은 두
게이트를 통과했고 shear는 통과하지 못한다. **shear는 신호가 0이 되는 곳(ω=0,
모델의 실제 제약 E122)에서만 합법이다** — map의 지위는 A1 k-확장이 이 긴장을
살아넘길 때만 유효한 조건부.

BK18 표는 **ILLUSTRATIVE**로 강등: k-독립 \(s\)면 증폭이 \(\propto k^2\) blue라
near-scale-invariant 카드 도메인 밖 — Phase 8/10의 도메인 기준을 적용하면 카드
대조의 정직한 판정은 **ABSTAIN** (스펙트럼-도메인 처리 전까지). pivot 독해 참고값:
\(r_{\rm vac}=10^{-3}\Rightarrow\sigma<8.37\) / \(3\times10^{-3}\Rightarrow4.69\) /
\(10^{-2}\Rightarrow2.28\) / \(3\times10^{-2}\Rightarrow0.63\).

\tag{E155}

## 5. E156 — 성분 × 채널 행렬 (완결 범위: 동차 2차, 상태 관례 선언 하)

**A5 (신규 선언, Phase 10 상속 아님)**: tensor 칸은 양자 진공(Phase 9 관례),
CDI 칸은 frozen 고전 진폭 \(p\to0\) — 채널별 상태 배정은 **비대칭 관례**다
(super-horizon 텐서도 얼며, 균일 취급 시 shear tensor 칸도 null이 된다).
frozen null은 exact-limit 진술이다 (잔여 \(p\)가 있으면 \(O(\sigma p)\) 잔류).

| 성분 | tensor | CDI |
|---|---|---|
| 회전 (반대칭 qp) | null (E137, 상태 무관) | \(\sin^2\theta_c\) (E143; 등가중 형태는 \(c_1{=}c_2\)) |
| 기울어진 종-혼합자 | — | \(c_1/c_2\) 인자 붙은 CDI (모든 \(c_1{\ne}c_2\) 합법) |
| shear 교차 \(p_+p_-\) | \(1+\sigma^2/2\) **조건부** (ω-긴장) | frozen null (A5) |
| shear 단일 \(p_\pm^2\) | \(1+\sigma^2/4\), 편광 비대칭 | frozen null (A5) |
| 부스트 (α↔β) | 유보 (ω 함정) | 유보 |
| dilation \(q{\cdot}p\) (**weak만**) | \(1+2\sinh^2 s\) — E139 부활 | frozen null (A5) |
| squeezer (대칭 qp) | **FORBIDDEN** (strong+weak, E152) | **FORBIDDEN** (모든 \(c_1,c_2\), E154) |
| qq / q-선형 | **FORBIDDEN** | 동일 |
| p-선형 변위 | 합법·미유도 | 합법·미유도 |

\tag{E156}

**E138 광의 독해의 supersession**: Phase 9 §2의 "관측 텐서 신호 ⟹ 대칭 성분
필요"는 **qp-클래스 안에서만** 참이다 — shear(strong 합법)와 dilation(weak
합법)이 반례다. E139–E140의 지위는 §2 참조 (기준-의존).

## 6. 선언된 가정 / 정직성

- **유한-정준 필요조건**이다: 4D N=1 SUGRA action·supermultiplet·junction·
  BFV/BRST·페르미온 교환은 유도하지 않았고 **G43–G46은 전부 OPEN**. "허용"
  클래스는 확립, "강제"는 없음 (\(\kappa,\sigma,s\) 자유). v1의 "유한 절반을
  닫음" 표현은 철회 — 이건 completion의 reduction이 만족해야 할 예비 정리다.
- A1·A2 (Phase 9), A3′ (Phase 10) 상속; **A5는 신규**; 인용 tensor map은 전부
  위상평균 (결맞음 범위 병기).
- 감사 provenance: 5-반박자 독립 sympy 재계산 (2026-08-11, 세션 07261f3d,
  workflow wf_593e6df8) — v1 exact 전부 재현 + material 6건 교정 반영.

## 7. 무엇이 닫혔고 무엇이 열렸나

닫힘:
- 동차 2차 collar의 허용/금지 **완전 분류** (strong: E152; weak 증분: E153).
- E144 빈 칸 = FORBIDDEN (모든 \(c_1,c_2\), E154). squeezer-형 종-혼합 불가 정리.
- 합법 클래스의 관측 map 일람 (E155–E156) + 회전/shear/dilation의 서명 구별
  (shear는 억제 불가·편광 비대칭 가능·k²-blue; dilation은 E139 재현).

열림:
- G43–G46 본체 (4D 유도 — \(\mathfrak{so}(1,2)\)⊕D⊕dilation 중 무엇이 실제로
  나오는가; 나오면 그때 "강제" 질문이 산다).
- strong vs weak 기준의 물리적 판정 (dilation 채널의 생사가 여기 걸림).
- shear의 ω-레벨 긴장 해소 여부, 부스트 map, k²-blue 스펙트럼-도메인 처리,
  p-선형 변위 map, G49–G51.

## 8. 파일

- 유도·검증 실행체: [`phase11_collar_admissibility.py`](phase11_collar_admissibility.py)
  (단일 검증 명령, exact sympy — 반박자 체크 흡수분 포함, exit 0 = 전부 통과)
