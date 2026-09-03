import { Console, Effect } from "effect"
import { iceError } from "../errors.ts"
import { loadValidOntologyCollectionStructure } from "../ontology/repository.ts"
import { auditBridgeResolution } from "./core.ts"
import { loadBridgeResolutionAudit } from "./repository.ts"

const inputs = Effect.all({
  audit: loadBridgeResolutionAudit,
  ontology: loadValidOntologyCollectionStructure
})

const report = inputs.pipe(
  Effect.map(({ audit, ontology }) =>
    auditBridgeResolution(audit, ontology.graphs)
  )
)

const validated = inputs.pipe(
  Effect.flatMap(({ audit, ontology }) => {
    const value = auditBridgeResolution(audit, ontology.graphs)
    return value.valid
      ? Effect.succeed({ audit, value })
      : Effect.fail(
          iceError(
            "BRIDGE_RESOLUTION_AUDIT_INVALID",
            value.errors.join(", ")
          )
        )
  })
)

const print = (value: unknown) => Console.log(JSON.stringify(value, null, 2))

export const bridgeAuditValidateData = report

export const bridgeAuditValidateCommand = (json: boolean) =>
  report.pipe(
    Effect.tap((value) =>
      json
        ? print(value)
        : Console.log(
            value.valid
              ? `valid: ${value.unresolved_bridges} unresolved bridges; 0 resolved matches`
              : `invalid: ${value.errors.join(", ")}`
          )
    )
  )

export const bridgeAuditSummaryData = validated.pipe(
  Effect.map(({ audit, value }) => ({
    schema: "ice-kg-bridge-resolution-audit-summary/v1" as const,
    audit_id: audit.audit_id,
    checked_at_utc: audit.checked_at_utc,
    valid: value.valid,
    unresolved_bridges: value.unresolved_bridges,
    resolved_matches: value.resolved_matches,
    counts: value.counts,
    actual_digest: value.actual_digest,
    does_not_alter_canonical_bridge_status:
      value.does_not_alter_canonical_bridge_status,
    non_claim: audit.non_claim
  }))
)

export const bridgeAuditSummaryCommand = (json: boolean) =>
  bridgeAuditSummaryData.pipe(
    Effect.tap((summary) =>
      json
        ? print(summary)
        : Console.log(
            `unresolved=${summary.unresolved_bridges} resolved=${summary.resolved_matches} NO_MATCH=${summary.counts.NO_MATCH} ID_COLLISION=${summary.counts.ID_COLLISION} REGISTRY_UNAVAILABLE=${summary.counts.REGISTRY_UNAVAILABLE}`
          )
    )
  )

export const bridgeAuditShowData = (localNodeId: string) =>
  validated.pipe(
    Effect.flatMap(({ audit, value }) => {
      const matches = value.bridges.filter(
        (bridge) => bridge.local_node_id === localNodeId
      )
      return matches.length === 0
        ? Effect.fail(
            iceError(
              "BRIDGE_AUDIT_TARGET_NOT_FOUND",
              `unresolved bridge '${localNodeId}' was not found`,
              2
            )
          )
        : Effect.succeed({
            schema: "ice-kg-bridge-resolution-audit-show/v1" as const,
            valid: value.valid,
            bridges: matches,
            resolved_matches: 0 as const,
            does_not_alter_canonical_bridge_status: true as const,
            boundary: audit.non_claim
          })
    })
  )

export const bridgeAuditShowCommand = (
  localNodeId: string,
  json: boolean
) =>
  bridgeAuditShowData(localNodeId).pipe(
    Effect.tap((value) =>
      json
        ? print(value)
        : Console.log(
            value.bridges
              .map(
                (bridge) =>
                  `${bridge.graph} ${bridge.local_node_id}: ${bridge.outcome}`
              )
              .join("\n")
          )
    )
  )
