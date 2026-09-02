# Schema lifecycle and research coverage audit

Date: 2026-09-02

Native `ontology/*.json` remains the research-graph system of record.  The
machine-readable lifecycle at `ontology/schema/research-schema-lifecycle.json`
declares the only currently supported collection and graph schemas: v1.  Its
migration registry is deliberately empty: no fictional v0 input or migration
is accepted.  An input declaring an unregistered future version fails before
schema decoding; a real future migration must be registered explicitly.

`./ice ontology coverage [--json]` inventories only the corpus roots declared
by `ontology/collection.json`.  It uses the longest matching coverage-ledger
prefix for every ordinary file.  An unmapped file, unreadable declared root,
symlink, workspace escape, or traversal bound breach makes the audit invalid.
Traversal is sorted and bounded (depth 64, 20,000 directories, 100,000 files),
and symlinks are rejected rather than followed.

This is an indexing and scope-completeness control, not evidence, a physics
claim, a promotion mechanism, or authority to run a calculation.  `output/`,
archives, and any undeclared directory are not discovered implicitly.
