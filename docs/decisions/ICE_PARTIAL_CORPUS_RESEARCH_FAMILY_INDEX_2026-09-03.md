# PARTIAL-corpus research family index

Date: 2026-09-03

## Decision

The six corpus roots labelled `PARTIAL` are indexed by research family and decisive-result unit in
`ontology/research-family-index.v1.json`. The file is a hash-audited navigation and provenance artifact;
it is linked from the hypercomplex and legacy programme nodes but is not itself scientific evidence.

The 190 files observed below those roots split into 140 ordinary tracked research files and 50 generated
`__pycache__/*.pyc` files. Python bytecode remains visible in the observed total but is excluded from the
normalized research inventory. The normalized digest for each family is SHA-256 over sorted lines of
`repository-relative-path<TAB>file-sha256<LF>`.

The six families are:

- finite hypercomplex core;
- Avenue-3 finite automorphism/S3 tests;
- Claim B sealed finite-level loop;
- direct S3 action on the reconstructed derivation space;
- Wilmot theta lifecycle;
- legacy prediction, null-control, and provenance records.

Each decisive unit names its source/result bundle, an existing canonical evidence node, and the scope
boundary. Files outside those units are explicitly archival or producer support, not additional
corroboration. A duplicate result therefore cannot increase evidence weight merely because it is a
second file.

## Enforcement

`./ice ontology families [--json]` fails if:

- the family roots no longer equal the collection's complete PARTIAL-root set;
- a root is assigned twice or to the wrong graph;
- an ordinary file count or normalized tree hash changes;
- a decisive path is missing, generated, outside its root, or assigned to two units;
- a named evidence reference is absent from the owning graph; or
- a symlink or workspace escape is encountered.

`npm run graph:check` includes this audit. The canonical graph continues to hash-check the family-index
artifact itself.

## Boundary

Coverage stays `PARTIAL`. The index deliberately avoids 140 low-value file nodes and adds no claim,
evidence node, evidence polarity, physical interpretation, execution authority, or external KG UID.
Generated caches are not research. Unassigned ordinary files remain discoverable through the family
digest but are not treated as decisive results.
