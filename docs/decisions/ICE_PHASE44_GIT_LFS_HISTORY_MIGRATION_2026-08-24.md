# Phase 44 result — Git LFS history migration

Date: 2026-08-24 UTC

Status: `LFS_MIGRATED_PUSH_PENDING`

Scope: repository transport and historical provenance only

## Decision

The user explicitly authorized history rewriting and Git LFS externalization on 2026-08-24. The
unpublished `main` tail was rewritten only from the commit that introduced the oversized Phase-44 result
through the then-current head. No remote commit was replaced and no force-push is authorized or needed.

This migration is not a calculation, a scientific reclassification, a reopening of the killed
Phase-51→56 route, or evidence for a physics/TOE claim.

## Migrated object

| Field | Value |
|---|---|
| path | `cpt_temporal_folded_susy/PHASE44_M4_NUMPY64_LOCAL_RHS_ERROR_DECOMPOSITION_RESULT.json` |
| bytes | `529,370,671` |
| content SHA-256 / LFS OID | `bcbebb6cbf64c91107ce72a699436206b91d4f65bcc5037729768fb23fbc9b75` |
| pre-migration Git blob | `b7d32b0547967d39ee69decb4e186fc8b9244c8a` |
| LFS pointer Git blob | `d8372d861b7e7de6419c9d32d178ba716320dc1e` |
| pre-migration introducing commit | `4e75a4fe9ce909fa62794f5a550a3409f6e0fc9f` |
| migrated introducing commit | `18a17b643874e74f7486fe9e009066eba8a467cb` |

The working-tree bytes and SHA-256 are unchanged. The Git tree stores this pointer:

```text
version https://git-lfs.github.com/spec/v1
oid sha256:bcbebb6cbf64c91107ce72a699436206b91d4f65bcc5037729768fb23fbc9b75
size 529370671
```

The exact `.gitattributes` rule is:

```gitattributes
cpt_temporal_folded_susy/PHASE44_M4_NUMPY64_LOCAL_RHS_ERROR_DECOMPOSITION_RESULT.json filter=lfs diff=lfs merge=lfs -text
```

## Rewrite boundary and recovery

| Field | Value |
|---|---|
| remote base | `dde2ff928e1a2019119e45b70148da9e19fbb3b4` |
| preserved Phase-44 parent | `d13af382fe65cc50f74fbc83861e41c0e7236341` |
| pre-migration head | `42c3e92b0519c99783777a4da41346192005dbb2` |
| migrated head before this attestation | `f36e84c6be3471d8202c9ccf4925f3830bd5d310` |
| unpublished commits still above remote | `116` |
| preserved local commits before boundary | `40` |
| rewritten commits | `76` |

The generated [old/new object map](ICE_PHASE44_GIT_LFS_OBJECT_MAP_2026-08-24.csv) has 76 rows and
SHA-256 `1882806fe40f0e4858d5e985f52a12b765e9d90781ce170ba5c21c9d43c58a31`.

The original DAG remains locally recoverable through:

- ref `backup/pre-lfs-main-20260824` → `42c3e92b0519c99783777a4da41346192005dbb2`;
- bundle `.git/migration-backups/pre-lfs-main-42c3e92-20260824.bundle`;
- bundle bytes `136,996,036`;
- bundle SHA-256 `6c8c7e4aefb71ccf74b7a3da1b15758ca16bc558817c9570f4c7fe9902c7a990`;
- bundle prerequisite `dde2ff928e1a2019119e45b70148da9e19fbb3b4`.

The backup ref is intentionally local and must never be included in `git push --all` or a mirror push,
because it still reaches the oversized ordinary-Git blob.

## Command and tool provenance

Git LFS `3.7.1` for Linux amd64 was installed under the user's local tool directory. The official
archive SHA-256 was verified as
`1c0b6ee5200ca708c5cebebb18fdeb0e1c98f1af5c1a9cba205a4c0ab5a5ec08` before use.

The mutation was bounded by a clean-tree check, exact old/remote heads, the verified bundle, one path,
one included ref, and the Phase-44 parent exclusion:

```bash
git lfs install --local
git lfs migrate import \
  --include-ref=refs/heads/main \
  --exclude-ref=d13af382fe65cc50f74fbc83861e41c0e7236341 \
  --include=cpt_temporal_folded_susy/PHASE44_M4_NUMPY64_LOCAL_RHS_ERROR_DECOMPOSITION_RESULT.json \
  --object-map=.git/migration-backups/phase44-lfs-object-map-20260824.csv \
  --yes
git lfs checkout -- \
  cpt_temporal_folded_susy/PHASE44_M4_NUMPY64_LOCAL_RHS_ERROR_DECOMPOSITION_RESULT.json
```

The same command was first exercised in an isolated scratch clone. Its migrated head was exactly
`f36e84c6be3471d8202c9ccf4925f3830bd5d310`, matching the real migration.

## Provenance boundary

The rewrite changes commit identities but not the captured research bytes. Sixty-six current files
contain 395 references to 59 rewritten pre-LFS commit IDs. Those strings are deliberately retained:
many are inside self-digested result and receipt artifacts, and replacing them would destroy the
historical evidence they describe. Interpret them in the pre-LFS namespace using the object map and
local bundle.

Fresh rewritten-history clones do not contain those old commit objects. Phase-52→56 frozen runners that
directly resolve old commits therefore require the bundle for archival exact-Git verification. They are
already on the Ragnarok-killed route and are not patched or rerun as part of this transport migration.
Content SHA-256 checks and the hydrated current artifacts remain unchanged.

## Validation before remote push

- isolated minimal-range trial: 76/76 commits rewritten;
- trial after old objects were pruned: strict TypeScript and Vitest `39/39` passed;
- trial ontology: 760 nodes, 2,249 edges, 166/166 hashes, zero errors;
- actual working file: 529,370,671 bytes with the original SHA-256;
- `git lfs fsck`: `OK`;
- ordinary Git blobs above the remote base: none over 100 MB; largest is 50,974,375 bytes;
- new `main` remains a descendant of the unchanged remote base with 116 commits above it;
- Ragnarok state and scientific classifications are unchanged.

## Remote receipt

At this attestation commit, the Git LFS object upload and remote `main` verification remain pending.
The active status is fail-closed as `LFS_MIGRATED_PUSH_PENDING`. A follow-up receipt may change it only
after both the LFS object and the ordinary Git ref are read back from GitHub.

## Sources

- [Git LFS migration reference](https://github.com/git-lfs/git-lfs/blob/main/docs/man/git-lfs-migrate.adoc)
- [Git LFS 3.7.1 release and checksums](https://github.com/git-lfs/git-lfs/releases/tag/v3.7.1)
- [GitHub large-file limits](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage)
- [GitHub LFS billing and quota](https://docs.github.com/en/billing/concepts/product-billing/git-lfs)
