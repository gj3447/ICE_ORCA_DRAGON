import * as Command from "@effect/platform/Command"
import type { CommandExecutor } from "@effect/platform/CommandExecutor"
import type { PlatformError } from "@effect/platform/Error"
import { Effect, Stream } from "effect"
import type { Stream as EffectStream } from "effect/Stream"
import { iceError, type IceError } from "./errors.ts"

export interface ProcessSpec {
  readonly command: string
  readonly args?: ReadonlyArray<string>
  readonly cwd?: string
  readonly captureLimitCharacters?: number
}

export interface ProcessResult {
  readonly exitCode: number
  readonly stdout: string
  readonly stderr: string
}

const defaultCaptureLimitCharacters = 4 * 1024 * 1024
const maximumCaptureLimitCharacters = 32 * 1024 * 1024

const makeCommand = (spec: ProcessSpec): Command.Command => {
  const command = Command.make(spec.command, ...(spec.args ?? []))
  return spec.cwd === undefined
    ? command
    : command.pipe(Command.workingDirectory(spec.cwd))
}

const collectText = (
  stream: EffectStream<Uint8Array, PlatformError>,
  captureLimitCharacters: number
): Effect.Effect<string, PlatformError> =>
  Effect.suspend(() => {
    const decoder = new TextDecoder("utf-8")
    return stream.pipe(
      Stream.runFold("", (text, bytes) =>
        (text + decoder.decode(bytes, { stream: true })).slice(
          -captureLimitCharacters
        )
      ),
      Effect.map((text) =>
        (text + decoder.decode()).slice(-captureLimitCharacters)
      )
    )
  })

const mapPlatformError = (operation: string) =>
  Effect.mapError((error: PlatformError) =>
    iceError("PROCESS_PLATFORM_ERROR", `${operation}: ${String(error)}`)
  )

export const capture = (
  spec: ProcessSpec,
  timeoutSeconds?: number
): Effect.Effect<ProcessResult, IceError, CommandExecutor> => {
  const operation = [spec.command, ...(spec.args ?? [])].join(" ")
  return Effect.scoped(
    Effect.gen(function* () {
      const captureLimitCharacters =
        spec.captureLimitCharacters ?? defaultCaptureLimitCharacters
      if (
        !Number.isSafeInteger(captureLimitCharacters) ||
        captureLimitCharacters < 1 ||
        captureLimitCharacters > maximumCaptureLimitCharacters
      ) {
        return yield* Effect.fail(
          iceError(
            "PROCESS_CAPTURE_LIMIT_INVALID",
            `${operation}: captureLimitCharacters must be a positive safe integer no greater than ${maximumCaptureLimitCharacters}`
          )
        )
      }
      const child = yield* Command.start(makeCommand(spec)).pipe(
        mapPlatformError(operation)
      )

      // @effect/platform normally releases a live process with SIGTERM and
      // waits for it. Register a later (therefore earlier-running) finalizer so
      // interruption cannot hang forever on a SIGTERM-resistant process.
      yield* Effect.addFinalizer(() =>
        child.isRunning.pipe(
          Effect.flatMap((running) =>
            running ? child.kill("SIGKILL") : Effect.void
          ),
          Effect.ignore
        )
      )

      const collect = Effect.all(
        [
          collectText(child.stdout, captureLimitCharacters),
          collectText(child.stderr, captureLimitCharacters),
          child.exitCode
        ],
        { concurrency: "unbounded" }
      ).pipe(
        Effect.map(([stdout, stderr, exitCode]) => ({
          exitCode: Number(exitCode),
          stdout,
          stderr
        })),
        mapPlatformError(operation)
      )

      if (timeoutSeconds === undefined) {
        return yield* collect
      }

      return yield* collect.pipe(
        Effect.timeoutFail({
          duration: `${timeoutSeconds} seconds`,
          onTimeout: () =>
            iceError(
              "PROCESS_TIMEOUT",
              `${operation} exceeded ${timeoutSeconds}s`
            )
        }),
        Effect.catchTag("IceError", (error) =>
          error.code === "PROCESS_TIMEOUT"
            ? child.kill("SIGKILL").pipe(
                mapPlatformError(`${operation} SIGKILL`),
                Effect.zipRight(Effect.fail(error))
              )
            : Effect.fail(error)
        )
      )
    })
  )
}

export const inherit = (
  spec: ProcessSpec
): Effect.Effect<number, IceError, CommandExecutor> => {
  const operation = [spec.command, ...(spec.args ?? [])].join(" ")
  return makeCommand(spec).pipe(
    Command.stdin("inherit"),
    Command.stdout("inherit"),
    Command.stderr("inherit"),
    Command.exitCode,
    Effect.map(Number),
    mapPlatformError(operation)
  )
}
