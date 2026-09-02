# Research areas

This directory holds the legacy flat-root computation corpus in stable, import-safe groups. Use
`./ice list`, `./ice info <name>`, and `./ice run <name>`; runnable names did not change when the files
moved.

| Area | Contents |
|---|---|
| [`hypercomplex/`](hypercomplex) | Cayley–Dickson helpers, sedenion/zero-divisor kernels, S-proof and queue diagnostics, plus adjacent result JSON |
| [`legacy_predictions/`](legacy_predictions) | dimensional estimates, preregistration controls, numerology diagnostics, and adjacent result JSON |
| [`reports/thothsaem/`](reports/thothsaem) | historical Thothsaem analysis reports |
| [`reports/furey/`](reports/furey) | historical Furey programme scaffold |
| [`intuition/`](intuition) | source-linked, non-authoritative question lenses federated to canonical open problems; never claims or execution authority |

The two kernel directories intentionally remain flat. Several scripts import `cd_core.py` or
`numerology_mc_judge.py` as a sibling module, and many write output beside `__file__`. Splitting them
further would require a real Python package/import migration rather than another file shuffle.

Other focused programmes remain at repository top-level directories, notably
[`../claimB_loop/`](../claimB_loop),
[`../cpt_temporal_folded_susy/`](../cpt_temporal_folded_susy), and the dated independent-test folders.
