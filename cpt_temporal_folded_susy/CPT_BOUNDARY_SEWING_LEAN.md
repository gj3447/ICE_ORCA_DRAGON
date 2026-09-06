# CPT 실수 경계 접합: Lean 4 형식화

2026-09-06 · **SUPPORTING_METHOD / KERNEL_CHECKED_REAL_BOUNDARY_ALGEBRA**.

## 결과

[CPT source 구성 설계 §2](../docs/research/ICE_CPT_SEWING_ORIGINAL_CYCLE_CONSTRUCTION_DESIGN_2026-09-06.md)의
실수 bosonic 경계 관계를 Lean 4로 구현했다. 현재 소스를 새로 읽어 실행한 검증에서
**정리 14개가 모두 통과**했고, 각 정리의 전이적 공리 의존성은
`propext`, `Classical.choice`, `Quot.sound`에만 속했다.

질문은 하나다: **선언한 momentum reflection에서 sum boundary primitive가 사라지며,
다른 orientation을 섞는 오류를 정확히 구별할 수 있는가?** 답은 아래 좌표형 범위에서
그렇다는 것이다. 물리적 CPT source나 원래 적분 cycle의 구성이라는 주장은 하지 않는다.

## 실제로 증명한 객체

[Lean source](../formal/cpt_sewing/CptSewing/Boundary.lean)는 실수 좌표
\(z=(a,\phi,p_a,p_\phi)\)와 tangent \(v=(\delta a,\delta\phi,\delta p_a,\delta p_\phi)\)를
각각 `Phase`, `Tangent`로 둔다. Floating-point 숫자가 아니라 mathlib의 \(\mathbb R\)다.

\[
 T(a,\phi,p_a,p_\phi)=(a,\phi,-p_a,-p_\phi),\qquad
 \alpha_z(v)=p_a\delta a+p_\phi\delta\phi.
\]

| 정리 묶음 | 핵심 Lean 선언 | 보장 범위 |
| --- | --- | --- |
| 반사와 좌표형 canonical pairing | `momentumReflection_involutive`, `alpha_momentumReflection`, `omega_momentumReflection` | 반사를 두 번 하면 원래 점이고, 선언한 tangent 반사에서 \(\alpha\)와 \(\omega\)의 값이 부호를 바꿈 |
| 올바른 접합 | `sum_seam_zero`, `identity_difference_seam_zero` | Graph \(T\)의 plus primitive, identity graph의 minus primitive가 0 |
| 모든 공유 configuration 변분의 검사 | `sumPrimitive_forall_iff`, `differencePrimitive_forall_iff` | plus는 반대 momentum, minus는 같은 momentum과 필요충분 |
| 방향 오류 반례 | `wrong_orientation_sum_identity`, `wrong_orientation_difference_reflection` | \((a,\phi,p_a,p_\phi)=(1,1,1,0)\), \(\delta a=1\)에서 잘못된 두 조합은 residual 2 |
| 같은 모델의 Hamiltonian | `starobinskyHL_momentumReflection_onPhysicalChart` | \(a>0\) 보존과 코드화한 Starobinsky \(H_L(Tz)=H_L(z)\) |

전체 선언 목록은 [proof index](../formal/cpt_sewing/proof-index.json), 실제 정리 type과
공리 출력은 [raw result](CPT_BOUNDARY_SEWING_LEAN_RESULT.json)의 `elaboration.messages`와
`theorems`가 정본이다. 표가 모든 check 배열을 복제하지는 않는다.

여기서 iff 정리는 양쪽이 **공유하는 configuration tangent**를 변화시키는 검사다.
그 자체가 \(q_1=q_2\)인 전체 product graph를 구성하거나 독립적인 두 momentum tangent를
식별하지 않는다. 실제 reflection graph의 \(q\) 식별과 tangent 반사는 따로 정의돼 있다.

`omega`는 \(dp_a\wedge da+dp_\phi\wedge d\phi\)의 좌표 평가식으로 정의했다.
Manifold exterior calculus로 \(\omega=d\alpha\)를 유도한 정리는 아니다.
또한 \(H_L\)의 physical convention은 [기존 모델](STAROBINSKY_POLYNOMIAL_BFV_CHART.md)에서
가져온 입력이다. Lean은 그 식을 코드화한 뒤 momentum 반사 항등식을 확인한다.
Bulk/GHY 변분에서 이 식을 유도한 것까지 검증한 것으로 읽지 않는다.

실수 나눗셈은 Lean에서 0에도 값이 정의된다. Hamiltonian의 momentum parity는 그
대수적 확장에서도 성립하지만, physical chart는 별도로 \(a>0\)를 요구한다.
이 정리로 \(a=0\)을 original source에 추가하지 않는다.

## 검증 경로와 실제 출력

프로젝트는 Lean `4.33.0`과 mathlib
`db584cd6d46c92f209a44c0f1c829460d327499d`를 고정한다. Transitive dependency revision은
[Lake manifest](../formal/cpt_sewing/lake-manifest.json)에 있다.
공식 mathlib compiled cache를 준비했고, 그 cache와 가상환경은 버전 관리하지 않았다.

Source 선행 commit은 `b0e20b0`이며, 첫 실행은 import deprecation과 불필요한 tactic
사용을 strict warning/error 정책이 차단하여 exit 1이었다. 실패 raw result를 보존한
수정 commit `6ee232b16e22c2c5b6966bac2d4d1658512e49c6`에서 다시 실행했다.
실제 결과는 다음과 같다.

```text
./ice run cpt_boundary_sewing_lean
LEAN_KERNEL_ACCEPTED_SCOPED_REAL_BOUNDARY_SEWING
kernel-checked theorems: 14
transitive axiom audit: standard axioms only
acceptance controls: custom axiom and admitted proof rejected
```

Exit code **0**, runner elapsed **4.830409268382937 s**였다. Lean compiler는
`4.33.0`, commit `d8b18978322de05a8f3dba51ef03cf5461676c17`였다.
현재 proof source SHA-256은
`b5bbb07693be9362045fe9cf14026f57fbd58e3f161a2290a0c2688ba656d42a`다.

[실행기](cpt_boundary_sewing_lean.py)는 committed source/input bytes와 dependency revisions를
확인한다. Source 원문 뒤에 모든 theorem의 `#check`와 `#print axioms`를 붙이고,
이를 한 번의 `lake env lean --json -DwarningAsError=true`에 넘긴다. 현재 proof를
import하는 stale project `.olean`을 증거로 사용하지 않는다.

주된 실패 위험은 `sign/unit`이며 관련 대조는 세 묶음이다.

- 공유 configuration variation의 두 basis 방향에서 접합 조건을 역으로 유도하고,
  잘못된 orientation에는 physical-chart 내부의 정확한 residual 2 반례를 둔다.
- production theorem의 compiler diagnostics와 공리 의존성을 전부 검사한다.
- 별도 temporary payload에서 compiler가 허용하는 custom axiom을 감사기가 거부하고,
  미완성 `sorry` proof를 strict compiler가 거부하는지 확인한다. 두 대조 모두 통과했다.

마지막 두 payload는 production theorem이 아니다. Raw에 등장하는 `sorryAx`나
`controlAssumption`을 production proof의 의존성으로 세면 안 된다.
검증 의미는 [공식 Lean proof-validation 문서](https://lean-lang.org/doc/reference/latest/ValidatingProofs/)를
따른다. Imported Lean/mathlib compiled cache는 이번 실행에서 독립적으로 재빌드하거나
다른 kernel로 교차 검증하지 않은 신뢰 기반이다. 이 한계와 표준 공리 의존성을 숨기지 않는다.

## 그래프 연결과 남는 연구

Canonical CPT graph에는 선언된 실수 boundary identity의 claim/scope/evidence와
Lean source·runner·raw result·report artifact를 연결한다. 정리의 적용 경계는 CPT/Pin
sewing concept에 붙이고, 이후 source 해석은 기존
`open:gate1-starobinsky-exact-gauge-preserving-element-source`가 맡는다.
정리가 맞다는 사실과 그 정리만으로 BFV source가 만들어진다는 주장을 구별한다.

현재 source는 full ghost/lapse boundary pair, BRST-compatible sewing, quantum
antiunitary CPT, boundary state/polarization/measure, regulated original joint cycle,
saddle/sheet census 또는 signed global intersection vector를 만들지 않는다.
따라서 G1은 그대로 열려 있다. 사전 planner도 `INSUFFICIENT_ROUTE_EVIDENCE`였으며
이번 구현은 사용자 요청에 따른 **supporting formalization**이다.

다음 source 설계가 재사용할 것은 검증된 real 경계 부호와 all-direction momentum 조건이다.
미정인 객체를 Lean의 `axiom`이나 `sorry`로 선언해 완료된 것처럼 넣지 않았다.
독립 읽기 검토는 Lean type과 원래 설계의 대응, physical chart, shared tangent 범위,
raw hash 및 검증기의 실제 거부 동작을 대조했다. 새 물리·TOE 또는 신규성은 주장하지 않는다.
