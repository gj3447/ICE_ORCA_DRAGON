# External comparator protocol

Date: 2026-09-03

Status: **DESIGN_ONLY / NO EXECUTION AUTHORITY**.

## Decision

External theories, codes, and data may be used as explicit comparators for a
bounded ICE question, but never as evidence that ICE is physically correct. A
comparator must make its action, matter coupling, conventions, source version,
tool revision, and failure criterion inspectable. It cannot create a canonical
claim, an ontology evidence edge, a CPT-gate dependency, or an automatic next
calculation.

The initial human-facing application is the geometry–energy route in
[the minimal verification design](../research/ICE_GEOMETRY_ENERGY_MINIMAL_VERIFICATION_ROUTE_2026-09-03.md).
It is intentionally outside the canonical CPT route until an explicit ICE action
and a matching typed open problem exist.

The strict sidecar is
[`research/benchmarks/ice-comparator-protocol.v1.json`](../../research/benchmarks/ice-comparator-protocol.v1.json),
validated by `./ice comparator validate`. It is intentionally not registered in
`ontology/collection.json`, GraphRAG, MCP, or the research-agent planner.

## Required comparator packet

Before a bounded implementation, record in one packet:

1. the full covariant action, matter metric/coupling, boundary functional,
   variational domain, and finite parameter vector;
2. the source equation locator and the distinction between a primary-source
   fact, a derived calculation, and a comparator-only assumption;
3. the allowed selection family: gauge, frame/field redefinition, boundary and
   initial data, regulator/EFT scale, sampling and output convention;
4. a mechanism-carrying typed output, an explicit null/kill condition, and the
   two independently defined downstream consumers using the same parameters;
5. full source revisions for all external code, including repository URL,
   immutable 40-character commit, release/patch provenance, compiler, and
   dependency locks; and
6. whether the result is a scoped comparator fact, an implementation check, or
   still only a design.

No floating branch, release name without commit, or unrecorded local patch is a
reproducible solver input.

## Initial source and tool pins

The following literature links are primary sources or official collaboration
comparators. They constrain model design; none is an ICE source of evidence.

| Role | Source | Boundary |
| --- | --- | --- |
| \(f(R)\) n=1 calibration | [Hu–Sawicki](https://arxiv.org/abs/0705.1158) | A finite-parameter modified-gravity comparator, not an ICE derivation |
| EFT mapping | [Gubitosi–Piazza–Vernizzi](https://arxiv.org/abs/1210.0201) | Framework for single-field EFT bookkeeping, not a physical-selection rule |
| linear observable organization | [Bellini–Sawicki](https://arxiv.org/abs/1404.3713) | Scalar–tensor observable parameterization, not an ICE model |
| EFTCAMB implementation | [Hu et al.](https://arxiv.org/abs/1312.5742) | Numerical method and stability checks, not independent physics evidence |
| hi_class implementation | [Zumalacárregui et al.](https://arxiv.org/abs/1605.06102) | Independent numerical method for Horndeski-class models |
| tensor-speed control | [GW170817 official multi-messenger analysis](https://arxiv.org/abs/1710.05834) | Empirical exclusion/control for applicable late-time models |
| background and scalar/lensing consumer context | [DESI DR2](https://arxiv.org/abs/2503.14738); [DES Y3](https://arxiv.org/abs/2105.13549) | Observational comparators only; no modified-gravity or ICE selection follows |

The following externally observed revisions are pinned for a future comparator
packet. The tools are not installed here. License review, compiler details,
dependency locks, and any local-patch hash are still required before use:

| Tool | Required immutable revision | Execution state |
| --- | --- | --- |
| H-EFTCAMB/EFTCAMB | <https://github.com/EFTCAMB/EFTCAMB> at `16d9c4e9f85751e30efd0a53b177941713078904` (observed 2026-09-03), plus dependency lock and local-patch hash | `NOT_INSTALLED—LICENSE REVIEW REQUIRED—DO NOT EXECUTE` |
| hi_class | <https://github.com/hiclass-code/hi_class_public> at `0009f51d89e6465c79e570b496c66fc90058fa77` (observed 2026-09-03), plus dependency lock and local-patch hash | `NOT_INSTALLED—LICENSE REVIEW REQUIRED—DO NOT EXECUTE` |

This is not a request to fetch, install, or run either tool.

## Equivalence and consumer rule

A field/frame quotient is accepted only if the action map is invertible on the
declared domain and matter couplings, normalization conventions, boundary data,
and initial data are transformed with it. Moving a term across the field
equation’s equals sign is bookkeeping, not new physics.

The same predeclared finite coupling vector must produce the background,
scalar-structure/lensing, and tensor outputs. Background-only agreement,
parameter retuning by consumer, a raw gauge-variable match, or a single solver
run cannot support a common-mechanism interpretation.

The associated required controls are:

| Control | Failure condition |
| --- | --- |
| Gauge/basis | an effect is absent in a gauge-invariant/operational observable or changes under an equivalent basis |
| Frame/field redefinition | transformed matter/boundary observables disagree |
| Cutoff/regulator | the effect requires \(k\) beyond the declared EFT validity scale or changes under allowed refinement |
| Boundary/initial data | a result is selected by an unacknowledged boundary condition or a physically distinct state is mislabeled an equivalent choice |
| Dual solver | convention-matched EFTCAMB and hi_class results disagree |
| Same coupling | a consumer needs a separately chosen parameter or nuisance function |

The repository-wide [choice-invariance and cross-domain policy](ICE_CHOICE_INVARIANCE_CROSS_DOMAIN_PROMOTION_2026-09-02.md)
remains the promotion boundary. This protocol operationalizes neither a new
physical claim nor an exception to that policy.

## CPT separation

The folded Wess–Zumino work remains an independent, scoped CPT context.
Phase 17’s doubled-sheet algebra witness and Phase 18’s free-seam pole null do
not validate an external geometry comparator. Conversely, even a fully checked
comparator cannot construct the physical fermion-odd charge, positive common
domain, Pin lift, or persistent interacting pole splitting required at CPT Gate
4–5. No cross-graph or cross-lane evidence edge is created by this protocol.
