# P7 closed-cosmology likelihood readiness preflight

This is a bounded provenance and readiness classifier, not a primordial-mode
generator or likelihood calculation.  It pins four local results:

- the V0 classical two-clock overlap comparison;
- the closed unit- `S3` SVT spectral ledger;
- selected- `H` full- `p` regular-shell RAQ; and
- the finite parametrized-particle BFV gluing calibration.

It reports the closed- `S3` scalar and TT index convention only as supported
by the SVT ledger: scalar `n>=0`, `lambda_n=n(n+2)`, degeneracy `(n+1)^2`; TT
`n>=2`, with the stated rough/Lichnerowicz eigenvalue conventions and combined
degeneracy.  This is not an explicit basis, mode evolution, initial-state
selection, spectrum, or solver input convention.

The preflight is intentionally pinned to `BLOCKED`: there is no common raw-
`C` physical product, quantum clock map, `V!=0` generation model, initial
state, reheating convention, primordial normalization, or discrete- `n` to
CLASS adapter.  It imports and invokes neither CLASS/classy nor Cobaya; the
official release pins in the input manifest (CLASS `v3.3.4`/`e858083`, Cobaya
`v3.6.2`/`899f30a`, checked 2026-08-31) are navigation only.

## Intended bounded invocation

```bash
./ice run p7_closed_cosmology_likelihood_readiness_preflight
```

The expected successful execution status is `VALID_RUN` with verdict
`BLOCKED_P7_CLOSED_COSMOLOGY_LIKELIHOOD_NOT_READY_PREREQUISITES_ABSENT`; it is
not a likelihood result and authorizes no follow-on calculation.
