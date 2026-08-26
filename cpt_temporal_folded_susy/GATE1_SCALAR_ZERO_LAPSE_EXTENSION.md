# Gate 1 scalar zero-lapse extension 실패 종결

> **실행 상태:** `INVALID_RUN`
> **window 상태:** `CONSUMED_FAILED_EXACT_CHECK`
> **과학 판정:** `null` — 유효한 result가 생성되지 않음
> **Gate 1:** `OPEN_PARTIAL_PROGRESS`
> **전역 승격:** `PROHIBITED`

## 기술 요약

승인된 `GATE1_ZERO_LAPSE_20260826_01` one-shot은 정확히 한 번 시작됐고, 두 번째 exact
check `G1.zero.global_lower_offset`에서 exit code 1로 끝났다. exclusive receipt가 실행 전에
생성됐으므로 성공 여부와 무관하게 window는 소진됐다. result JSON은 생성되지 않았으며,
따라서 canonical boundary, scaling degree 또는 point-supported ambiguity에 대한 새 과학 판정은
없다.

실패는 동결된 수학 명제의 반례가 아니다. runner가 이미

```text
u_square = -lower_offset + square_coefficient * square
```

로 구성한 항등식을 확인하면서 왼쪽만 `simplify`한 뒤 SymPy 구조 동등성 `==`로 비교해 false를
낸 harness false negative다. 직전의 full Starobinsky square identity check는 통과했다. 이 실행에서
사용할 수 있는 과학 출력은 없으며, 기존 zero-lapse 상태 `OPEN`을 그대로 유지한다.

## 동결 provenance와 실제 실행

| 항목 | 관측값 |
| --- | --- |
| authorization | `GATE1_ZERO_LAPSE_20260826_01` |
| authorization commit | `1f0fc7d17cc704577db601071e46563a37db24f0` |
| command | `./ice run cpt_temporal_folded_susy/gate1_scalar_zero_lapse_extension` |
| args | none |
| start / observed | `2026-08-26T05:42:12Z` |
| receipt | `.git/ice-launches/GATE1_ZERO_LAPSE_20260826_01` |
| receipt birth | `2026-08-26T05:42:14.025056895Z` |
| receipt contents | empty directory, 0 children |
| exit code | `1` |
| wall time | `2.349 s` from Bash `time` with `TIMEFORMAT='WALL_SECONDS=%3R'` |
| result | absent |
| retry / repro | not authorized |
| automatic next | `null` |

동일 실행에 대해 unified-exec 외부 계측이 더 짧은 `2.203881327 s`를 표시했지만, 명령과 함께
명시적으로 수집한 Bash `2.349 s`를 정본으로 사용한다. 두 값 모두 30초 상한 안이다.

동결 byte는 승인 commit과 실행 시점 checkout에서 일치했다.

| 동결 대상 | SHA-256 |
| --- | --- |
| input | `5667cb42bbc7eb72ae50de05cc1b0abfbc12bf22c8036f6c59c6f5427644cd0e` |
| runner | `f7a7135f5d17ce283ef3dfe444b052499f85b9b3b6956be93a81d34ed106c58e` |
| upstream source-link result | `ad7c7f9ccf79047d0994eea3667b07c1fbb9795e7187c9730c5c6d819956f243` |
| authorization decision | `afad6e26b8445db8a7e1e04e31397768662c0ea6b1a2ecf0210bdd84fece6e61` |

## 실행된 check ledger

| 순서 | check | 상태 | 해석 |
| --- | --- | --- | --- |
| 1 | `G1.zero.starobinsky_global_square` | `PASS` | original rate와 square form의 exact identity가 통과함 |
| 2 | `G1.zero.global_lower_offset` | `FAIL` | 비대칭 단순화 뒤 구조 비교가 false를 내어 실행 중단 |

관측된 stderr의 종결 exception은 다음과 같다.

```text
AssertionError: [EXACT FAIL] G1.zero.global_lower_offset: u(q)+6*pi^2*a/hbar is exactly a positive coefficient times a real square for a,hbar>0
```

실패는 `exact_calculation` 안에서 result 조립·직렬화보다 먼저 발생했다. 따라서 통과한 exact
check는 1개, 실패한 exact check는 1개이며 theorem guard 0개, numerical check 0개다. root,
ODE, evaluator reconciliation과 automatic descendant도 실행되지 않았다.

## 결과 부재와 판정 경계

`GATE1_SCALAR_ZERO_LAPSE_EXTENSION_RESULT.json`은 존재하지 않는다. 따라서 다음 값은 모두
의도적으로 `null`이다.

- result SHA-256, self-digest와 byte count
- `run_status=VALID_RUN`에 속하는 classification과 verdict
- decision-table matched row와 programme impact
- canonical boundary, scaling degree와 point-support 결론

운영 분류만 `INVALID_RUN`이다. 이는 `NO_DISTRIBUTIONAL_EXTENSION`이나 `INCONCLUSIVE` 같은
과학 판정표 행과 동일시하지 않는다. 실패한 harness가 frozen question을 판정하지 못했으므로
기존 source-link 결과의 `zero_lapse_distribution=OPEN`을 그대로 상속한다.

## 보존되는 scope와 null 출력

- 비영 lapse arm의 declared fixed-\(a\), \(m=2\) scalar source link `KEEP`은 그대로다.
- zero-including full \(q\)-paired distribution은 `OPEN`이다.
- Gate 1은 `OPEN_PARTIAL_PROGRESS`, global promotion은 `PROHIBITED`다.
- `physical_original_cycle`, `full_joint_orientation`,
  `complete_global_signed_intersection_vector`, `global_n_sigma`, `physics_claim`과 `TOE_claim`은
  모두 `null`이다.
- `automatic_next=null`이며 Phase 57, replay, retry, reproduction 또는 이름을 바꾼 후손은
  승인되지 않았다.

exclusive receipt는 [동결 결정](../docs/decisions/ICE_GATE1_SCALAR_ZERO_LAPSE_BOUNDED_RESUME_2026-08-26.md)의
성공·실패·timeout 공통 소진 규칙에 따라 이 window를 닫는다. 다른 실행은 새롭고 명시적인
사용자 승인 없이는 허용되지 않는다.

## 동결 source 경계

- [입력 manifest](GATE1_SCALAR_ZERO_LAPSE_EXTENSION_INPUTS.json)
- [실패한 exact runner](gate1_scalar_zero_lapse_extension.py)
- [상속한 source-link result](GATE1_SCALAR_SOURCE_LINK_RESULT.json)
- Chakrabarti–Shafikov, [arXiv:1505.01230](https://arxiv.org/abs/1505.01230)
- Brunetti–Fredenhagen, [arXiv:math-ph/9903028](https://arxiv.org/abs/math-ph/9903028)

두 analytic source의 theorem guard는 이번 실행에서 도달하지 않았다. 이 보고서는 해당 정리를
새로 적용하거나 그 결론을 과학 evidence로 승격하지 않는다.
