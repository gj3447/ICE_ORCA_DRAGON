import { Schema } from "effect"

export class IceError extends Schema.TaggedError<IceError>()("IceError", {
  code: Schema.String,
  message: Schema.String,
  exitCode: Schema.Number
}) {}

export const iceError = (
  code: string,
  message: string,
  exitCode = 1
): IceError => new IceError({ code, message, exitCode })
