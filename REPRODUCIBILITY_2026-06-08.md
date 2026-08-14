# ICE_ORCA_DRAGON L1 재현성 attestation (2026-06-08)

## 2026-08-14 portability erratum — current contract

The historical body below is preserved as the record of the 2026-06-08
same-environment run. Its `byte-identical` language must **not** be read as a
cross-platform guarantee: BLAS/LAPACK, optimizer, and null-space basis choices were
not pinned by that run.

The current control plane is strict TypeScript + Effect 3 on Node 24
(`package-lock.json`). Numerical kernels remain Python 3.13 with NumPy 2.5.2,
SciPy 1.18.0, and SymPy 1.14.0 (`uv.lock`). `./ice repro` copies the candidate tree
into an Effect-scoped temporary directory, deletes each mapped output before its
kernel runs, drains stdout/stderr concurrently, kills the process group on timeout,
and reads baselines from `git show HEAD:./<output>`. It never restores files with
`git checkout`, so a user's dirty result cannot be erased.

Current mapped legacy-output ledger:

| Status | Count | Meaning |
|---|---:|---|
| `REPRO` | 12 | Keys/shapes/types and categorical values reproduce; registered numeric semantics pass |
| `NONPORTABLE_FAIL` | 1 | `queue_03_threshold_sensitivity_scan` uses a basis-dependent entrywise commutator maximum |
| `SUPERSEDED` | 1 | `queue_06_cooperative_vacuum` is not the generator of its committed repaired output |

The overall command intentionally exits 1 while queue03 is quarantined. This is an
honest needs-attention gate, not a failed attempt to manufacture a green badge.

Comparison policy is field-aware:

- object keys, array lengths, booleans, strings, and integer-valued JSON numbers are exact;
- curated verdict/timestamp/MC-overlay fields are excluded explicitly at the top level;
- ordinary floating-point leaves use `rtol=1e-12`, `atol=1e-15`;
- the S5.4 master residual is the semantic invariant `abs(residual) <= 1e-12`;
- only `$.case3_realistic.best_theta[*]` (circular distance) and
  `$.case3_realistic.theta_spread` in queue04 use `atol=1e-6`;
- NaN/Inf are failures, and queue03 is never tolerance-masked.

Queue03 changes categorical pass/fail counts across valid SciPy null-space bases,
so its old threshold story is method-invalid. See
[`QUEUE03_PORTABILITY_AUDIT_2026-08-14.md`](QUEUE03_PORTABILITY_AUDIT_2026-08-14.md).
A basis-invariant v2 would require a new preregistration, script, result, and verdict;
it must not overwrite the legacy JSON.

Current commands:

```bash
npm ci
uv sync --locked
./ice doctor
npm run check
./ice repro --only prove_s5_bv_ainfty
./ice repro --only queue_04_hosotani_toy
./ice repro  # 12 REPRO + 1 NONPORTABLE + 1 SUPERSEDED; exit 1
```

---

> PROM 16 remediation A1 산출. harness: `repro_check.py`. 정전 lesson: `lesson-ice-L1-repro-stale-output-path-exit0-not-reproduced-2026-06-05` + `lesson-ice-naive-remediation-reintroduces-drift-2026-06-08`.
>
> **이건 REPRODUCIBILITY attestation이지 correctness/물리진리 주장이 아니다.** green = "스크립트 재실행이 committed JSON의 *computed* 키를 byte-identical 재생성한다"(= exit 0이 기록된 수를 실제로 썼다). L2/L3 물리는 여전히 STAGNANT, 신화는 USER_PRIMARY.

## 한 일
1. **14 스크립트 stale 절대경로 제거**: `open("/Users/lagyeongjun/CD/AGENT/X.json")` → `open(Path(__file__).resolve().parent / "X.json")`. 결정론적 1:1 치환, 어느 cwd에서도 자기 디렉터리에 write. → 스크립트가 portable + 실제로 in-repo JSON을 생성.
2. **비파괴 재현 검증** (`repro_check.py`): committed JSON을 git-HEAD에서 baseline으로 잡고, 스크립트 실행 후 computed 키만 비교, committed 원본은 복원. **hand-curated verdict는 절대 덮어쓰지 않음**(`_verdict_auto_emit.py` "NEVER overwrites pre-existing verdict" 계약 준수, Eilu va-Eilu).

## 결과 (`python3 repro_check.py`, exit 0)

| 분류 | 수 | 스크립트 |
|---|---|---|
| **REPRO ✓** (computed bit-identical, verdict/timestamp 제외, curated 보존) | 12 | derive_{Lstar,dimensionless,mass_ratios}, prove_{higgs,s3,s5}, queue_{01,04,05,10,11}, verify_mp_mW |
| **NEW_ARTIFACT** | 1 | `queue_03_threshold_sensitivity_scan` — committed `queue_03_rep_results.json`은 아카이브된 *다른* 스크립트(`queue_03_rep_decomposition.py`) 출력. named script 출력은 부재했음 → 이번에 `queue_03_threshold_sensitivity_results.json` 신규 생성(1:1 매핑 복구) |
| **SUPERSEDED** | 1 | `queue_06_cooperative_vacuum` — committed JSON source = `inconclusive_redo.py`(n_trials supersede + method_fix). named script(`gamma_critical=null`)와 다름. **committed가 canonical**(보정 method), 덮어쓰지 않음 |

## 적대검증이 적발한 함정 (회피됨)
- **naive "재실행→커밋"은 파괴적**: 첫 시도에서 `derive_*` 3개의 curated verdict 라벨(`REFUTED`/`NUMEROLOGY_CONFIRMED`)이 스크립트 raw prose로 덮였고, queue_06의 보정 method 결과가 옛 스크립트 출력으로 덮임 → git diff 눈검증으로 적발 → 전량 복원. harness는 verdict-family + timestamp를 비교에서 제외해 재발 차단.
- adversarial 하위주장 정정: "verify_mp_mW 미실행"은 부정확 — 실제로 computed 키 bit-identical 재현됨.

## 남은 (OPTIONAL)
- queue_03 신규 출력에 `researchedAt` 타임스탬프 → bit-reproduction 비교에서 제외 처리됨. 완전 결정론 원하면 타임스탬프 제거 고려.
- `pyproject.toml` + `uv.lock`(sympy 1.14.0 / numpy 1.26.4, 현 환경) pin은 미생성 — 환경 재현성 강화 시 추가.
- CI 배선(`uv run python X.py && python3 repro_check.py`)은 GitHub Actions에 미등록 — 자동 gate 원하면 추가.

## 재현
```
python3 repro_check.py          # 12 REPRO + 1 NEW + 1 SUPERSEDED, exit 0
python3 repro_check.py --list   # 스크립트↔출력 매핑
```
