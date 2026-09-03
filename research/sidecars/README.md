# Non-authoritative sidecars

`collection.v1.json` is a fixed-path, SHA-256 integrity registry for the repository's research
intuition and comparator-method documents. It is deliberately outside `ontology/collection.json`.

Use `./ice sidecars validate`, `./ice sidecars summary`, and
`./ice sidecars show <sidecar-id>` to inspect it. These commands do not create canonical ontology
nodes or evidence edges, do not feed GraphRAG/planner/MCP, and never authorize execution.
