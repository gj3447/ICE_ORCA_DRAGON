# External comparator protocols

This directory holds strict, source-pinned method DAGs used to design bounded comparisons without
placing them in the canonical research ontology.

[`ice-comparator-protocol.v1.json`](ice-comparator-protocol.v1.json) records the initial
`DESIGN_ONLY` route:

```text
JBD calibration -> Hu–Sawicki n=1 audit -> locked background/scalar/tensor check -> ICE admission review

folded Wess–Zumino seam classification -- independent parallel context only
```

Inspect it with:

```bash
./ice comparator validate --json
./ice comparator summary --json
./ice comparator show route-step:hu-sawicki-n1-cross-domain --json
./ice comparator trace route-step:geometry-ice-admission-decision --json
```

Every input and output is `PLANNED` and `not_a_result`; both external solver pins are
`NOT_INSTALLED`. This directory supplies no physics claim, canonical evidence, likelihood, automatic
successor task, or execution authority. See the
[protocol decision](../../docs/decisions/ICE_EXTERNAL_COMPARATOR_PROTOCOL_2026-09-03.md).
