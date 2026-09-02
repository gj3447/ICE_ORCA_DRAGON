# Clean CI and release-readiness boundary

Date: 2026-09-02

Status: accepted

## Decision

Three least-privilege GitHub Actions workflows give this repository a clean
revision check, dependency-change review, and lockfile-based package inventory.
They do not ingest external knowledge, write the research ontology, publish an
artifact outside GitHub Actions, deploy a service, or authorize research work.

`graph-control-plane.yml` runs on pull requests and `main` pushes. It uses
Node 24, `npm ci`, hydrates exactly the tracked Phase 44 LFS object, and runs
`npm run graph:check`. The latter remains the repository's combined TypeScript,
test, ontology, SHACL, retrieval, competency, and agent-routing check.

`dependency-review.yml` runs only for pull requests with read-only repository
and pull-request permissions. It reviews dependency diffs and does not receive
write or package-publishing permissions.

`release-readiness.yml` runs on `main`, version-tag pushes, or manual dispatch.
It independently re-runs `graph:check`, fails on a registry-reported high or
critical production dependency advisory, then produces a `package-lock.json`-
based CycloneDX SBOM through npm's built-in `npm sbom` command. It verifies the
SBOM JSON marker and retains it as a 30-day GitHub Actions artifact. The audit
is time-dependent registry evidence and the SBOM is an inventory of the Node
dependency closure; neither is an attestation, a scientific result, or a
release publication. npm includes a generation timestamp and serial number, so
the SBOM is reconstructible from the pinned lockfile and npm toolchain but is
not claimed to be byte-for-byte reproducible.

## Pinned action sources

Every action is pinned to a full commit SHA, with its human-readable release
tag in the workflow comment. The values were resolved from the upstream GitHub
REST tag/ref endpoints on 2026-09-02:

| Action | Pinned commit | Release label | Upstream ref |
| --- | --- | --- | --- |
| `actions/checkout` | `11d5960a326750d5838078e36cf38b85af677262` | v4 | https://github.com/actions/checkout/tree/v4 |
| `actions/setup-node` | `49933ea5288caeca8642d1e84afbd3f7d6820020` | v4 | https://github.com/actions/setup-node/tree/v4 |
| `actions/dependency-review-action` | `a1d282b36b6f3519aa1f3fc636f609c47dddb294` | v5.0.0 | https://github.com/actions/dependency-review-action/tree/v5.0.0 |
| `actions/upload-artifact` | `ea165f8d65b6e75b540449e92b4886f43607fa02` | v4 | https://github.com/actions/upload-artifact/tree/v4 |

Refreshing a pin is a reviewed dependency change: inspect the upstream release
and commit, update the SHA and the label together, then run the local graph
check before merging.

This follows GitHub's secure-use guidance that a full commit SHA is the
immutable way to pin an action:
https://docs.github.com/en/actions/reference/security/secure-use . The SBOM
command and CycloneDX selection follow the npm CLI documentation:
https://docs.npmjs.com/cli/v11/commands/npm-sbom/ .

## Operational boundary

The workflows use only `contents: read`, except that dependency review also
needs `pull-requests: read`. They use per-workflow/ref concurrency cancellation
and bounded job timeouts on the explicit `ubuntu-24.04` runner label. Checkout
does not persist GitHub credentials and intentionally disables broad LFS
hydration; the checks download only the one LFS path required by the repository
rules.

This is CI and release readiness for a repository-local workbench. It is not a
claim of a hosted triplestore, production MCP service, external graph-KG sync,
security certification, archival completeness, or physics validation.
