import { Effect, Schema } from "effect"
import { iceError, type IceError } from "../errors.ts"
import {
  excludedTopLevelKeys,
  type ComparePolicy,
  type PathNumericRule
} from "./manifest.ts"

export type JsonObject = Readonly<Record<string, unknown>>

export interface Difference {
  readonly path: string
  readonly message: string
}

const JsonDocumentFromString = Schema.parseJson(Schema.Unknown)

const isObject = (value: unknown): value is JsonObject =>
  typeof value === "object" && value !== null && !Array.isArray(value)

export const decodeJsonObject = (
  source: string,
  label: string
): Effect.Effect<JsonObject, IceError> =>
  Schema.decodeUnknown(JsonDocumentFromString)(source).pipe(
    Effect.mapError((error) =>
      iceError("INVALID_JSON", `${label}: ${String(error)}`)
    ),
    Effect.flatMap((document) =>
      isObject(document)
        ? Effect.succeed(document)
        : Effect.fail(
            iceError("INVALID_JSON_SHAPE", `${label}: top-level value is not an object`)
          )
    )
  )

const render = (value: unknown): string => {
  const encoded = JSON.stringify(value)
  const text = encoded === undefined ? String(value) : encoded
  return text.length <= 180 ? text : `${text.slice(0, 177)}...`
}

const pathPattern = (pattern: string): RegExp => {
  const escaped = pattern.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")
  return new RegExp(`^${escaped.replace(/\\\[\\\*\\\]/g, "\\[\\d+\\]")}$`)
}

const ruleForPath = (
  rules: ReadonlyArray<PathNumericRule> | undefined,
  path: string
): PathNumericRule | undefined =>
  rules?.find((rule) => pathPattern(rule.path).test(path))

const close = (
  expected: number,
  actual: number,
  relativeTolerance: number,
  absoluteTolerance: number
): boolean =>
  Math.abs(expected - actual) <=
  Math.max(
    absoluteTolerance,
    relativeTolerance * Math.max(Math.abs(expected), Math.abs(actual))
  )

const circularDistance = (
  expected: number,
  actual: number,
  period: number
): number => {
  const half = period / 2
  return Math.abs((((actual - expected + half) % period) + period) % period - half)
}

const compareNumber = (
  expected: number,
  actual: number,
  path: string,
  policy: ComparePolicy
): ReadonlyArray<Difference> => {
  if (!Number.isFinite(expected) || !Number.isFinite(actual)) {
    return [
      {
        path,
        message: `non-finite numeric value is not reproducible (${expected} vs ${actual})`
      }
    ]
  }

  const pathRule = ruleForPath(policy.pathRules, path)
  if (pathRule?.kind === "near-zero") {
    return Math.abs(expected) <= pathRule.absoluteTolerance &&
      Math.abs(actual) <= pathRule.absoluteTolerance
      ? []
      : [
          {
            path,
            message: `${expected} vs ${actual}; both must be <= ${pathRule.absoluteTolerance}`
          }
        ]
  }
  if (pathRule?.kind === "circular") {
    const distance = circularDistance(expected, actual, pathRule.period)
    return distance <= pathRule.absoluteTolerance
      ? []
      : [
          {
            path,
            message: `circular distance ${distance} exceeds ${pathRule.absoluteTolerance}`
          }
        ]
  }

  if (Number.isInteger(expected) || Number.isInteger(actual)) {
    return expected === actual
      ? []
      : [{ path, message: `integer ${expected} != ${actual}` }]
  }

  const numericRule = pathRule?.kind === "close" ? pathRule : policy.defaultNumeric
  return close(
    expected,
    actual,
    numericRule.relativeTolerance,
    numericRule.absoluteTolerance
  )
    ? []
    : [
        {
          path,
          message:
            `${expected} != ${actual} ` +
            `(rtol=${numericRule.relativeTolerance}, atol=${numericRule.absoluteTolerance})`
        }
      ]
}

const compareValue = (
  expected: unknown,
  actual: unknown,
  path: string,
  policy: ComparePolicy
): ReadonlyArray<Difference> => {
  if (typeof expected !== typeof actual) {
    return [
      {
        path,
        message: `type ${typeof expected} != ${typeof actual}`
      }
    ]
  }

  if (typeof expected === "number" && typeof actual === "number") {
    return compareNumber(expected, actual, path, policy)
  }

  if (Array.isArray(expected) || Array.isArray(actual)) {
    if (!Array.isArray(expected) || !Array.isArray(actual)) {
      return [{ path, message: "array/non-array mismatch" }]
    }
    if (expected.length !== actual.length) {
      return [
        {
          path,
          message: `array length ${expected.length} != ${actual.length}`
        }
      ]
    }
    return expected.flatMap((expectedValue, index) =>
      compareValue(expectedValue, actual[index], `${path}[${index}]`, policy)
    )
  }

  if (isObject(expected) || isObject(actual)) {
    if (!isObject(expected) || !isObject(actual)) {
      return [{ path, message: "object/non-object mismatch" }]
    }
    const expectedKeys = Object.keys(expected).filter(
      (key) => path !== "$" || !excludedTopLevelKeys.has(key)
    ).sort()
    const actualKeys = Object.keys(actual).filter(
      (key) => path !== "$" || !excludedTopLevelKeys.has(key)
    ).sort()
    const expectedSet = new Set(expectedKeys)
    const actualSet = new Set(actualKeys)
    const missing = expectedKeys
      .filter((key) => !actualSet.has(key))
      .map((key): Difference => ({ path: `${path}.${key}`, message: "missing" }))
    const unexpected = actualKeys
      .filter((key) => !expectedSet.has(key))
      .map((key): Difference => ({ path: `${path}.${key}`, message: "unexpected" }))
    const shared = expectedKeys
      .filter((key) => actualSet.has(key))
      .flatMap((key) =>
        compareValue(expected[key], actual[key], `${path}.${key}`, policy)
      )
    return [...missing, ...unexpected, ...shared]
  }

  return Object.is(expected, actual)
    ? []
    : [{ path, message: `${render(expected)} != ${render(actual)}` }]
}

export const compareComputed = (
  expected: JsonObject,
  actual: JsonObject,
  policy: ComparePolicy
): ReadonlyArray<Difference> => compareValue(expected, actual, "$", policy)
