import { expect, it, layer } from "@effect/vitest"
import { NodeContext } from "@effect/platform-node"
import { Effect, Fiber } from "effect"
import { capture } from "../src/process.ts"

layer(NodeContext.layer)("scoped process runner", (it) => {
  it.effect("captures stdout, stderr, and the real exit code concurrently", () =>
    Effect.gen(function* () {
      const result = yield* capture({
        command: process.execPath,
        args: [
          "-e",
          "process.stdout.write('out'); process.stderr.write('err'); process.exitCode = 7"
        ]
      })
      expect(result).toEqual({ exitCode: 7, stdout: "out", stderr: "err" })
    })
  )
})

it.live("hard-kills a SIGTERM-resistant process group on timeout", () => {
  const started = Date.now()
  return capture(
    {
      command: process.execPath,
      args: [
        "-e",
        "process.on('SIGTERM', () => {}); setInterval(() => {}, 1000)"
      ]
    },
    0.1
  ).pipe(
    Effect.either,
    Effect.tap((result) =>
      Effect.sync(() => {
        expect(result._tag).toBe("Left")
        if (result._tag === "Left") {
          expect(result.left.code).toBe("PROCESS_TIMEOUT")
        }
        expect(Date.now() - started).toBeLessThan(2_000)
      })
    ),
    Effect.provide(NodeContext.layer)
  )
})

it.live("hard-kills a SIGTERM-resistant process group on interruption", () =>
  Effect.gen(function* () {
    const started = Date.now()
    const fiber = yield* capture({
      command: process.execPath,
      args: [
        "-e",
        "process.on('SIGTERM', () => {}); setInterval(() => {}, 1000)"
      ]
    }).pipe(Effect.provide(NodeContext.layer), Effect.fork)

    yield* Effect.sleep("100 millis")
    yield* Fiber.interrupt(fiber)
    expect(Date.now() - started).toBeLessThan(2_000)
  })
)
