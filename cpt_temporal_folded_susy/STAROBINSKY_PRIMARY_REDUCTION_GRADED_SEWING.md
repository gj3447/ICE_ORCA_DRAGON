# Primary 축소·graded pairing·실제 구간 source 경계항

2026-09-07 · SUPPORTING_METHOD · 완료된 계산/해석 결과.

**현재 compact 시험복합체의 상태를 보존하는 실제 축소를 구성했고, 올바른 graded
dual에서 기존 비영 detector pairing이 유지됨을 확인했다.** 동시에 full-primary 구간
source를 bulk에서 분리해도 두 종류의 endpoint 자료가 남는다는 것을 명시했다.
양의 물리 내적이나 완성된 quantum BFV/CPT amplitude는 이 결과에 포함되지 않는다.

## 결과와 직관

| 대상 | 이번에 판별한 내용 | 남는 경계 |
| --- | --- | --- |
| 실제 compact-N 시험복합체 | 적분 R_N, normalized bump Jχ, 보정 primitive Kχ로 FI=id, id−IF=qh+hq | Self-adjoint domain이나 lapse gauge-group average가 아님 |
| 상태가 남는 차수 | H⁰=H¹=0, H²≅Ψ/HΨ는 무한차원 | Physical ghost degree를 재지정하지 않음 |
| 반대쪽 graded dual | 실제 T_g[z]=t_g[R_Nz]가 exact 대표에 무관하고 비영 | Complex-bilinear pairing이며 양의 내적/quantum kernel이 아님 |
| 차수를 유지한 continuous coefficient dual | 명시한 C∞ topology에서 pᵗ(T∘K)=T, 따라서 top cohomology=0 | 임의의 distributional completion에 적용하지 않음 |
| 실제 CMW 구간 source의 primary 분리 | 최소 bulk 작용과 auxiliary sector로 분리하되 −[σ⁺ρ], [σ⁺δN]이 남음 | Boundary-state equivalence, BV integral와 original cycle은 별도 |

직관은 보정 primitive에서 보인다. N 방향으로 그냥 적분하면 상단 경계에 누적값이
남는다. 적분 전에 χR_Nu를 빼면 전체 적분이 0이 되어 양쪽 N collar를 보존한다.
이 보정은 원래 top 상태를 지우지 않고 축소 공간으로 옮긴다. 서로 다른 normalized
χ는 같은 cohomology class의 대표를 고를 뿐이다.

반면 dualization에서 ghost 차수를 그대로 두면 다른 복합체가 된다. 이번 K는 그
복합체에서 모든 top coefficient의 **연속적인 primitive**까지 만들어 준다. 올바른
degree-reversed dual에서는 같은 T_g가 degree −2의 비영 class로 남는다. 따라서
“더 큰 공간으로 옮겼다”와 “상태를 보존하며 옮겼다”는 구별해야 한다.

Source 쪽에서는 σ=e²−Ndot, N⁺new=N⁺−dot σ⁺라는 local jet 변수변환으로

\[
 S_{\rm BV}=S_{\rm min}(E,c)+\int(-\Pi\sigma+\rho N^+_{\rm new})
 -[\sigma^+\rho],
\]

를 얻는다. BV cotangent primitive에도 [σ⁺δN]이 남는다. 두 항의 소거 조건은
같지 않으며, σ⁺=0은 둘을 함께 소거하는 한 충분한 끝점 제한이다. 그 제한이 원하는
상태와 complex cycle에 적합하다는 증명은 없다. 이 항들은 symmetry anomaly나
우주론적 에너지를 발견했다는 뜻이 아니다.

R_N은 **경계 configuration lapse 좌표**를 적분하는 시험공간 사상이다. Source의
좌표시간 s 경로 적분이나 full lapse gauge average를 실행한 것이 아니다. Local bulk
doublet의 분리와 compact 경계 상태의 cohomology는 연결 사상을 확인해야 이어진다.

## 근거와 독립 검토

- [실제 적분/PDE 유도](STAROBINSKY_PRIMARY_REDUCTION_DERIVATION.md): support와 모든 Neumann
  jets, homotopy, H¹의 Cauchy uniqueness, continuous-dual primitive.
- [graded dual 유도](STAROBINSKY_GRADED_DUAL_SEWING_DERIVATION.md): 반전된 degree, Hom differential과의
  부호 대응, dual-left Berezin order, 실제 T_g evaluation.
- [CMW component source 유도](../docs/research/ICE_STAROBINSKY_SOURCE_INDUCED_INTERVAL_BVBFV_2026-09-07.md):
  actual H_L/Π, 최소 source와의 body equality, incoming-minus-outgoing BFV primitive,
  두 relative endpoint 항.
- [적대적 seam 검토](../docs/research/ICE_STAROBINSKY_GRADED_SEAM_ADVERSARIAL_REVIEW_2026-09-07.md):
  anti-linear ghost 부호와 고전 anti-Poisson 부호의 차이, state family와 uniqueness 구별.

서로 독립적으로 support/zero-Cauchy argument와 전체 chain homotopy/Berezin 부호를
검토했다. 원문 대조에서 AKSZ multiplier를 target N과 자동 동일시하는 오류와,
ordinary variation의 경계항을 mCME의 상쇄항과 같은 부호로 쓰는 오류를 고쳤다.
기본 source 규약은 [CMW §8–9.1](https://arxiv.org/html/2012.13270#S8), quantum
pairing/pushforward의 경계는 [CMR §2.3–2.4](https://arxiv.org/html/1507.01221#S2.SS3)에 따른다.

이것은 원문 framework를 실제 homogeneous convention에 적용한 scoped 유도다.
PDE 존재·적분의 연속성·BV 경로 적분을 Lean이 모두 증명했다는 뜻은 아니다.

## 실행 기록

```text
./ice run starobinsky_primary_reduction_graded_sewing
SCOPED_PRIMARY_CHAIN_EQUIVALENCE_AND_NONZERO_GRADED_PAIRING
exact controls: 28/28
CptSewing/PrimaryReduction.lean: accepted=True; expected=11
CptSewing/GradedDualSewing.lean: accepted=True; expected=7
Lean theorems: 18
```

- Source commit: `c6923b7d3f3338f60ded489f90ebd2e257f1ecd1`.
- 실제 runtime: `15.45730352634564` seconds.
- Python `3.13.5`, SymPy `1.14.0`, Lean `4.33.0`.
- Mathlib: `db584cd6d46c92f209a44c0f1c829460d327499d`.
- Raw 정본: [STAROBINSKY_PRIMARY_REDUCTION_GRADED_SEWING_RESULT.json](STAROBINSKY_PRIMARY_REDUCTION_GRADED_SEWING_RESULT.json),
  SHA-256 `fecbb49e6c188259414de60083776f914151d0bff010ab0eb012b718b00a841b`.

두 Lean 파일의 모든 theorem을 inventory와 대조하고 warning-as-error로 elaboration했다.
각 정리의 axiom audit은 propext, Classical.choice, Quot.sound만 허용했다. 실제 함수공간의
support/PDE 가정은 해석적 입력이고, Lean은 주어진 선형 사상들의 함의와 Ward 항등식을
검증했다. 기호 검사도 유한 numerical PDE solution이나 global cycle census가 아니다.

첫 source `daa1e5f` 실행은 기호 검사 25/25와 graded-dual 7개가 통과했지만,
PrimaryReduction의 unused simp arguments와 product-zero 표현 때문에 실패했다.
이 실패를 고친 뒤 continuous-dual와 relative-source controls를 추가했다. 최초 재시도는
자신의 untracked 실패 raw 때문에 clean-core 검사에서 차단됐으며 계산은 실행되지 않았다.
그 실패 raw를 `/tmp/ice-primary-graded-daa1e5f-failure.json`에 보존하고 clean source로
실행하여 위 결과를 얻었다. 임시 실패 파일은 재현 입력이 아니며, 실패 원인은 이 문서에
남긴다. 성공한 raw의 command·source·input hashes가 재현 정본이다.

## 현재 남은 질문

이 결과는 `open:starobinsky-seam-ward-boundary-state-limit`를 좁힌다. 다음 판별 대상은
**위 endpoint 자료와 양립하는 boundary quantization map·half-density module·실제 interval
kernel이 존재하며, 비영 class와 접합 pairing을 함께 보존하는가**다. Positive product는
구성된 관측가능량과 domain에서 검토해야 하며, state family의 비유일성만으로 이론 실패라고
판정하지 않는다.

G1의 source-defined original joint relative class와 signed global intersections는 이번에
공급하지 않았다. G1→G2→G3→G4→G5→full-theory/empirical review의 upstream dependency,
workbench 지위와 물리/TOE 승격 경계는 유지된다.
