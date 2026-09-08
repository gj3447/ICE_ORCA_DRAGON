import assert from "node:assert/strict"
import { pathToFileURL } from "node:url"
import { resolve } from "node:path"

const args = process.argv.slice(2), value = (flag) => { const i = args.indexOf(flag); return i < 0 ? undefined : args[i + 1] }
const originalPath = value("--original-js"), patchedPath = value("--patched-js")
if (!originalPath || !patchedPath || args.length !== 4) throw new Error("Usage: node scripts/check-hswm-context-key.mjs --original-js PATH --patched-js PATH")
const original = await import(pathToFileURL(resolve(originalPath)).href), patched = await import(pathToFileURL(resolve(patchedPath)).href)
const right = (value) => { assert.equal(value._tag, "Right"); return value.right }
const six = Object.freeze({ mode: "investigate", graph: "cpt", tier: "supporting", domain: "missing", map: "missing", obstruction: "present" })
const generated = right(original.updateModel(original.initialModel(), six, { success: true, cost: 1 }))
const attemptLength = Object.keys(generated.context_attempts)[0].length
assert.ok(attemptLength > 256); assert.equal(original.predict(generated, six)._tag, "Left")
assert.equal(patched.predict(generated, six)._tag, "Right")
let repeated = generated
for (let i = 0; i < 3; i += 1) { repeated = right(patched.updateModel(repeated, six, { success: i % 2 === 0, cost: i + 1 })); assert.equal(patched.predict(repeated, six)._tag, "Right") }
const fast = Object.freeze({ route: "fast", state: "ready" }), slow = Object.freeze({ route: "slow", state: "ready" })
let oldModel = original.initialModel(), patchedModel = patched.initialModel()
for (let i = 0; i < 8; i += 1) { oldModel = right(original.updateModel(oldModel, fast, { success: true, cost: 1 })); oldModel = right(original.updateModel(oldModel, slow, { success: false, cost: 3 })); patchedModel = right(patched.updateModel(patchedModel, fast, { success: true, cost: 1 })); patchedModel = right(patched.updateModel(patchedModel, slow, { success: false, cost: 3 })) }
assert.deepEqual(patchedModel, oldModel); assert.equal(patched.predict(patchedModel, fast).right, original.predict(oldModel, fast).right)
const overbound = { ...patched.initialModel(), context_attempts: { ["x".repeat(129_096)]: 1 } }
assert.equal(patched.predict(overbound, fast)._tag, "Left")
console.log(JSON.stringify({ schema: "ice-hswm-context-key-regression/v1", status: "PASS", scope: "synthetic engineering regression", generated_attempt_key_length: attemptLength, repeated_observations: repeated.n }, null, 2))
