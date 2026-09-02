# Repository-local graph engineering completion profile

Date: 2026-09-02

Status: accepted

Profile: `ICE-REPOSITORY-GRAPH/1.0`

## Outcome

The finite graph-engineering target for this repository is complete when one
committed revision passes `npm run graph:release-check`. This is a completion
claim about the repository-local computational workbench, not about a theory of
everything, a physical discovery, or every file ever created around the
project.

The profile deliberately chooses a single authoritative authored graph—the
strict native JSON collection and registered graph documents—and builds
validation, deterministic retrieval, interoperability and release controls
around it. Generated RDF, JSON-LD, reports and crates are downstream views and
cannot be merged back as a second source of truth.

## Required stack

| Layer | Required closure |
| --- | --- |
| Native model | Strict collection/graph decoding, semantic validation, artifact hashes, evidence snapshots and explicit relation vocabulary |
| Schema lifecycle | Machine-readable current/supported versions; unknown future input fails until a real migration is implemented and registered |
| Corpus accountability | Every ordinary file below every declared research corpus root receives a longest-prefix coverage-ledger status; missing roots, unmapped files, symlinks, escapes and traversal-limit breaches fail |
| Stable interchange | JSON-LD 1.1, RDF 1.1, explicit RDFC-1.0 canonicalization, SHACL 1.0 Core and bounded local SPARQL 1.1 |
| Portable package | Non-overwriting RO-Crate 1.3 package with offline emitted-base-record validation, PROV-O lineage, hashes and no copied raw results |
| Retrieval quality | Deterministic canonical locators, bounded graph expansion, positive rank bounds, forbidden boundary locators and explicit no-anchor abstention |
| Human workflow | Read-only MCP and graph-aware planning/audit surfaces; no automatic graph mutation, successor generation or numerical execution authority |
| Supply chain | Node 24 and lockfile-pinned dependencies, SHA-pinned least-privilege CI actions, pull-request dependency review, high/critical production advisory gate and CycloneDX SBOM generation |

The single local acceptance command is:

```bash
npm run graph:release-check
```

It runs strict TypeScript and the complete test suite, native ontology and
artifact validation, SHACL, fixed GraphRAG retrieval/boundary/abstention cases,
architecture competency questions, agent-routing controls, declared-root
coverage, the current npm production advisory check, and an in-memory
lockfile-only CycloneDX 1.5 SBOM check. The release workflow generates the same
inventory as a retained artifact; its timestamp and serial number mean byte
identity is not claimed.

## Standards policy

Conformance targets are stable published specifications: JSON-LD 1.1, RDF
1.1, RDFC-1.0, SHACL 1.0, SPARQL 1.1, PROV-O and RO-Crate 1.3. RDF 1.2, SHACL
1.2 and SPARQL 1.2 remain monitored drafts rather than claimed conformance
targets. The local RO-Crate check validates the base records this generator
emits without remote-context dereferencing; it is not a universal third-party
RO-Crate certification.

Runtime graph packages remain exact lockfile pins. Patch updates may be taken
after the full gate. Node type declarations stay on the Node 24 line, while
TypeScript and Vitest major upgrades require a separate compatibility change;
an `npm outdated` major-version number is not itself evidence that changing the
project toolchain is safe.

The repository's direct SPARQL syntax dependency is the maintained Traqula
SPARQL 1.1 parser rather than the archived SPARQL.js package. SPARQL.js remains
in the current latest Comunica dependency closure, while `rdf-dataset-ext` and
`node-domexception` remain below the current latest SHACL and RDF packages.
These are recorded upstream transitive deprecation debts, not direct runtime
choices or known production advisories; the audit gate must continue to expose
any registry security finding rather than hiding it with lockfile overrides.
This follows the SPARQL.js repository's own archive notice and migration
direction:
https://github.com/RubenVerborgh/SPARQL.js/ and
https://github.com/comunica/traqula/blob/master/docs/sparqlJSMigration.md .

## Deliberate non-goals

Completion of this profile does not claim any of the following:

- a hosted multi-user triplestore, remote SPARQL endpoint, external KG write or
  bidirectional synchronization;
- unreviewed bulk ingestion, entity resolution, automatic deduplication or
  complete indexing of archives, generated output, narrative, and undeclared
  directories;
- learned embeddings, a Microsoft GraphRAG implementation, semantic synonym
  recall, citation entailment, or answer-generation quality;
- production identity, authorization, service telemetry, backups, disaster
  recovery, signed provenance or a public release;
- scientific truth, physical likelihood, Gate 1 closure, TOE completion, or a
  newly discovered physical phenomenon.

Those are separate products or research outcomes. Adding one requires its own
source of authority, threat/operations model, benchmark and explicit user
scope; it must not be inferred from this profile.

## Reopening rule

Reopen `ICE-REPOSITORY-GRAPH/1.0` only when its own contract regresses: a
supported schema cannot be decoded, a declared-root file becomes unclassified,
an interchange/package invariant fails, retrieval crosses a fixed boundary or
stops abstaining, a workflow gains unintended authority, or clean CI/SBOM
generation fails. New physics questions and additional calculations do not
reopen graph infrastructure by default; they use it.
