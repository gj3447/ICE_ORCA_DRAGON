import { Context, Layer } from "effect"
import { fileURLToPath } from "node:url"

export interface Workspace {
  readonly root: string
  readonly python: string
  readonly runtime: {
    readonly nodeMajor: 24
    readonly controlPackages: Readonly<
      Record<
        | "effect"
        | "@effect/cli"
        | "@effect/platform"
        | "@effect/platform-node"
        | "@effect/printer"
        | "@effect/printer-ansi"
        | "tsx",
        string
      >
    >
    readonly pythonMajorMinor: "3.13"
    readonly packages: Readonly<Record<"numpy" | "scipy" | "sympy", string>>
  }
}

export const Workspace = Context.GenericTag<Workspace>(
  "ice-orca-dragon/Workspace"
)

export const workspaceFromRoot = (root: string): Workspace => ({
  root,
  python: `${root}/.venv/bin/python`,
  runtime: {
    nodeMajor: 24,
    controlPackages: {
      effect: "3.22.1",
      "@effect/cli": "0.77.0",
      "@effect/platform": "0.97.1",
      "@effect/platform-node": "0.108.1",
      "@effect/printer": "0.51.0",
      "@effect/printer-ansi": "0.51.0",
      tsx: "4.23.12"
    },
    pythonMajorMinor: "3.13",
    packages: {
      numpy: "2.5.2",
      scipy: "1.18.0",
      sympy: "1.14.0"
    }
  }
})

const root = fileURLToPath(new URL("..", import.meta.url)).replace(/\/$/, "")

export const WorkspaceLive = Layer.succeed(Workspace, workspaceFromRoot(root))
