# Research ontology memory

> This directory is a human-readable memory and index over repository evidence. It is **not** a preregistration, research contract, scientific verdict, or knowledge-graph (KG) ratification. The machine-readable graph and run snapshots remain the traceable records; the prose pages are navigation aids.

## Current collection

| Programme | Human entry point | Machine record | Evidence and sources |
| --- | --- | --- | --- |
| CPT × Temporal-Folded SUSY | [Programme guide](./cpt-temporal-folded-susy/README.md) | [Research graph](./cpt-temporal-folded-susy/graph.json) | [Evidence guide](./cpt-temporal-folded-susy/references/evidence.md) · [Source inventory](./cpt-temporal-folded-susy/references/source-inventory.md) |

The graph uses [`research-graph/v1`](./schema/research-graph-v1.schema.json). The Phase 16–34 snapshots use [`research-run-evidence/v1`](./schema/research-run-evidence-v1.schema.json).

At the recorded `2026-08-17T18:31:54.008Z` graph update, the collection has 478 nodes and
1224 edges. Validation verifies 62/62 stored hashes (60 artifacts and 2 policies). The
Phase 16–34 run snapshots contain 328 named exact checks, 159 typed numerical-ledger checks, and one
legacy separately recorded Phase 18 numerical control (160 numerical controls in all). These
counts describe repository records, not independent replications or global scientific
confidence.

## Read and validate it

```bash
./ice ontology validate
./ice ontology summary
./ice ontology show claim:P16_BGG_BOSONIC_KINETIC_PARENT
./ice ontology trace claim:P17_FUNDAMENTAL_DOUBLED_SHEET_EXCHANGE_ALGEBRA --depth 2
./ice ontology trace claim:P20_LEADING_DE_SITTER_WDW_ENVELOPE_SELECTS_5P44 --depth 2
./ice ontology trace claim:P23_IMPOSED_BRIDGE_DEFINES_POSITIVE_TRACE_CLASS_REGULATED_DENSITY --depth 2
./ice ontology trace claim:P24_CONSTRAINT_PRESERVING_MIXED_HESSIAN_HAS_RANK_ONE --depth 2
./ice ontology trace claim:P28_DIRICHLET_BFV_GHOST_REMOVES_PROPER_LENGTH_ZERO_MODE --depth 2
./ice ontology trace claim:P29_FROZEN_QUADRATIC_KERNEL_HAS_DELTA_FLAT_IDENTITY_LIMIT --depth 2
./ice ontology trace claim:P30_FINITE_CUTOFF_LOCAL_COUPLED_FIELD_LAPSE_CYCLE_EXISTS --depth 2
./ice ontology trace claim:P31_PROPER_TIME_CANONICAL_DETERMINANT_SIGN_IS_STABLE --depth 2
./ice ontology trace claim:P32_SPECIFIED_BELOW_ORIGIN_FULL_LINE_HAS_RECORDED_PROJECTED_BASE_CROSSING --depth 2
./ice ontology trace claim:P33_RECORDED_DIRICHLET_CAUSTIC_HAS_SIMPLE_FOLD_AIRY_SCALE --depth 2
./ice ontology trace claim:P34_BOUNDED_DIRECTED_CONSTANT_PHASE_PAIR_EXISTS_BEYOND_FOLD --depth 2
```

Every command also accepts `--json`. `show` accepts either a full node ID or a bare stable `claim_id`;
`trace` walks incoming and outgoing relations to the requested bounded depth.

## How to read a claim

Follow a claim in this order:

1. Read the claim's `state`, `summary`, and `VALID_WITHIN` scope.
2. Follow `HAS_EVIDENCE` from the claim to an evidence node and inspect the edge's `polarity`. `SUPPORTS` and `CONTRADICTS` carry the scientific direction.
3. Follow `DEFINED_IN` and `RECORDED_IN` to the executable and observed run snapshot.
4. Follow `DERIVED_FROM` for a calculation source or `CITES` for literature framing and boundary conditions.
5. Follow `BLOCKED_BY` before promoting a finite witness into a physical construction. Follow
   `MOTIVATES` for a distinct next problem suggested by a terminal result; solving it does not reverse
   that result.

A check marked `PASS` means that the named exact test passed. It does **not** mean that the associated scientific claim is true. For example, a passing counterexample check can attach to a claim with `polarity: CONTRADICTS`.

## Identifier families

| Prefix | Meaning |
| --- | --- |
| `programme:` | Overall research question |
| `phase:` | Bounded calculation cycle |
| `concept:` | Reusable definition or distinction |
| `claim:` | Scoped, falsifiable statement |
| `evidence:` | Verified check group |
| `scope:` | Assumptions and exclusions |
| `open:` | Missing construction or unresolved question |
| `source:` | Primary or technical literature source |
| `artifact:` | Repository file |
| `policy:` | Repository workflow rule; never scientific evidence |
| `edge:` | Directed graph relation |
| `result:` | Observed executable-run snapshot |

Edges are read exactly in their stored `from → relation → to` direction. The current graph has no `SUPERSEDES` relation: `EXTENDS`, `FOLLOW_UP_TO`, and `CONTRASTS_WITH` preserve narrower cross-phase meanings without silently replacing earlier claims.

## KG bridges

`kg_bridges` are lookup memory between local IDs and live external UIDs. `EXACT` means the programme identity was matched; `RELATED` means topical overlap, not claim identity. `RESOLVED` means the UID lookup succeeded, not that the external KG accepted, reviewed, or ratified this repository's evidence. `UNRESOLVED` preserves a lookup key without inventing a UID.

For the programme's claims, scopes, blockers, and bridge list, continue to the [CPT × Temporal-Folded SUSY guide](./cpt-temporal-folded-susy/README.md).
