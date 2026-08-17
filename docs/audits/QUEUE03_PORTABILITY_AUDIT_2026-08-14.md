# Queue03 legacy portability audit — 2026-08-14

Status: **POST_HOC METHOD AUDIT**
Legacy disposition: **NONPORTABLE / INVALID_METHOD**
Physics disposition: **no new physics verdict**

This audit explains why `queue_03_threshold_sensitivity_scan.py` is quarantined by
the reproduction control plane. The legacy script and its JSON remain historical
artifacts; neither is silently rewritten.

## Failure mechanism

For a null-space basis matrix `Q`, queue03 projects a generator `L` as
`M = QᵀLQ`. SciPy may return any equally valid basis `Q' = QO` for orthogonal `O`.
The projected operator and commutator then transform by orthogonal similarity:

```text
M' = Oᵀ M O
C' = [M'_L, M'_R] = Oᵀ [M_L, M_R] O
```

Spectral and Frobenius norms are invariant under this transformation. The legacy
quantity `max(abs(C_ij))` is not. Therefore its threshold crossings are coordinate
artifacts, not portable properties of the projected operators.

## Adversarial measurements

Temporary-copy audit environment:

- base commit: `5bbc780376b26c3b9cc0cb4d50849e8801c7df78`
- Python 3.13.5
- NumPy 2.5.2
- SciPy 1.18.0
- orthogonal-rotation seed: `0x1CE03`

Observed structure:

- 42 zero-divisor candidates; every null space has dimension 4;
- 35 ambient triples; exactly two legacy “invariant” triples per candidate;
- the two triples share a generator in 42/42 cases;
- the combined numerical rank of all six projected generators is 3 in 42/42
  cases, not the rank 6 required for independent `su(2)_L ⊕ su(2)_R`;
- the legacy closure gate is structurally failed in 42/42 cases, consistent with
  queue02.

Across 64 random orthogonal basis changes per candidate (2,688 trials):

| Quantity | Observation |
|---|---:|
| legacy entrywise maximum | relative change up to 30.77%; median 7.27% |
| worst observed range, candidate `(5,12)` | 1.3706617 … 1.9996583 |
| Frobenius invariance error | ≤ 4.89e-15 |
| spectral invariance error | ≤ 2.44e-15 |
| normalized spectral invariance error | ≤ 9.99e-16 |

The invariant cross-commutator diagnostics are essentially constant:

- Frobenius norm: `4 ± 6e-15`;
- spectral norm: `2 ± 4e-15`;
- normalized spectral score
  `||[A,B]||₂ / (2 ||A||₂ ||B||₂) = 1 ± 7e-16` (maximally noncommuting).

This is not an epsilon-scale disagreement. In the legacy output, 863 numeric leaves
and 12 categorical leaves changed across valid environments; 800 numeric changes
still failed at `1e-6`. Success counts changed at thresholds 1.5 and 2.0.

## Performance finding

The legacy implementation recomputes the same generator matrices, projections, and
commutators for each of seven thresholds and previously triggered a large analysis
while importing `cd_embedding.py`.

- legacy end-to-end: about 180.6 s;
- cached generator matrices + one metric pass: about 1.36 s;
- measured speedup: about 132×.

The import-side-effect portion is removed by the pure `cd_core.py` numerical-kernel
boundary. A future diagnostic must compute operator scores once and derive threshold
labels from stored scores.

## Method verdict and future gate

Classification: **refutation of the legacy measurement method**, not confirmation or
refutation of a physical model. Fitting detection: **post-hoc**. Lakatos mechanism:
the quarantine is a progressive methodological correction because it removes a
basis artifact instead of adding an accommodating tolerance.

No v2 physics result is promoted here. A separate exploratory v2 must preregister:

1. closure and nondegeneracy gates for each projected triple;
2. rank 6 for the combined left/right generator span;
3. triple-selection and null-space `rcond` rules;
4. normalized spectral cross-commutator aggregation over all nine pairs;
5. a numerical-zero threshold and strict/non-strict comparison rule;
6. recursive NumPy-scalar JSON normalization;
7. an operator-level Hosotani transformation, replacing the legacy scalar `×0.85` toy.

It must use a new script/result name and an explicit `POST_HOC_EXPLORATORY` label.
The current canonical action is exactly what `./ice repro` reports:
`NONPORTABLE_FAIL` with a nonzero overall exit status.
