# External KG bridge resolution audit — 2026-09-03

`research/benchmarks/ice-kg-bridge-resolution-audit.v1.json` is a read-only
audit sidecar for the current canonical `kg_bridges` entries whose status is
`UNRESOLVED`. It is not a fifth ontology graph and has no authority to change a
bridge, claim, source, evidence status, or external registry.

The sidecar freezes the exact 75-key unresolved set as a SHA-256 digest of
sorted `(graph path, local id, system, lookup key)` records. `./ice bridges
validate` fails closed if a canonical graph's unresolved key set drifts, if a
local lookup key differs, if an audit rule names a non-current bridge, or if a
rule would classify a bridge as resolved. The command reads all four canonical
collection graphs, including the zero-unresolved legacy graph.

The audit result is zero resolved matches. Twenty-three CPT phase-number
collisions are explicitly recorded as `ID_COLLISION`: older SYMPOSIUM elements
have the same P-number but different definitions. Their GitHub permalinks are
nonidentity-audit locators only, never `external_uid` values and not even safe
`RELATED` bridges. The remaining entries are `NO_MATCH`, except the
hypercomplex external-registry entry, which is `REGISTRY_UNAVAILABLE` because
this audit has no verified readable registry surface.

The SYMPOSIUM source is pinned to commit
`5434d26348312dbed8d084c3a63a775dd0fc6547` and blob
`46195f1ccf400828a4531e03cffc994b24d44317`. On 2026-09-03, both `git ls-remote`
and authenticated GitHub API lookup confirmed that the commit and manifest exist in the remote
repository. This proves only the identity of the negative-collision source; it does not prove an ICE
bridge match.

The read-only lookup pass extracted 75 unique canonical `lookup_key` values and ran one literal
multi-pattern search over the sibling SYMPOSIUM checkout, excluding VCS, dependency, environment, and
bytecode directories. It returned zero exact-key hits. Broader inspection found only the 23 old
same-number phase records above; their definitions differ from the current ICE phase nodes. The
programme-level `external-research-kg` target had no verified registry surface. Consequently no
collision-free `EXACT` or `RELATED` UID exists in the audited sources, and all canonical bridges remain
`UNRESOLVED`.

Useful read-only commands:

```bash
./ice bridges validate --json
./ice bridges summary --json
./ice bridges show phase:p24 --json
```

`show` exposes the current canonical lookup key plus the audit outcome. It
never writes a bridge or converts an unresolved value into a zero or match.
