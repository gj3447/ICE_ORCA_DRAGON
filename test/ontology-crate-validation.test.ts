import { expect, it } from "vitest"
import {
  RO_CRATE_13_CONTEXT,
  RO_CRATE_13_SPECIFICATION,
  validateRoCrate13BaseProfile
} from "../src/ontology/crate-validation.ts"

const validMetadata = () => ({
  "@context": [RO_CRATE_13_CONTEXT],
  "@graph": [
    {
      "@id": "ro-crate-metadata.json",
      "@type": "CreativeWork",
      conformsTo: { "@id": RO_CRATE_13_SPECIFICATION },
      about: { "@id": "./" }
    },
    {
      "@id": "./",
      "@type": "Dataset",
      name: "Demo crate",
      description: "A base-profile fixture",
      hasPart: [{ "@id": "data.json" }]
    },
    { "@id": "data.json", "@type": "File", name: "data.json" }
  ]
})

it("validates the RO-Crate 1.3 base-profile records emitted by the package", () => {
  expect(validateRoCrate13BaseProfile(validMetadata())).toEqual({
    schema: "ice-ro-crate-1.3-base-profile-report/v1",
    conforms: true,
    violations: []
  })
})

it("rejects a dangling root member and a malformed metadata descriptor", () => {
  const metadata: any = validMetadata()
  metadata["@graph"][0] = {
    "@id": "ro-crate-metadata.json",
    "@type": "CreativeWork",
    conformsTo: { "@id": "https://example.invalid/profile" },
    about: { "@id": "missing-root" }
  }
  metadata["@graph"][1] = {
    "@id": "./",
    "@type": "Dataset",
    name: "Demo crate",
    description: "A base-profile fixture",
    hasPart: [{ "@id": "missing.json" }]
  }
  const report = validateRoCrate13BaseProfile(metadata)
  expect(report.conforms).toBe(false)
  expect(report.violations.map(({ code }) => code)).toEqual(
    expect.arrayContaining([
      "METADATA_DESCRIPTOR_CONFORMS_TO",
      "METADATA_DESCRIPTOR_ABOUT",
      "ROOT_HAS_PART_DANGLING"
    ])
  )
})
