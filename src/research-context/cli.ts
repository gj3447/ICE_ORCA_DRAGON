import { Args, Command, Options } from "@effect/cli"
import { Console } from "effect"
import { researchPrepareCommand, researchStatusCommand } from "./commands.ts"
import { researchEpisodeCommand, researchFeedbackCommand, researchStateCommand, researchIntuitionCommand } from "../research-engine/commands.ts"
import { researchCellCommand } from "../research-engine/cell.ts"

const json = Options.boolean("json")
const status = Command.make("status", { json }, ({ json }) => researchStatusCommand(json)).pipe(
  Command.withDescription("inspect installed HSWM/USL research interfaces and source fingerprints")
)
const prepare = Command.make("prepare", {
  question: Args.text({ name: "question" }),
  target: Options.text("target").pipe(Options.withDefault("cpt::open:gate1-original-cycle-signed-global-intersections")),
  references: Options.text("reference").pipe(Options.repeated),
  json
}, ({ question, target, references, json }) => researchPrepareCommand(question, target, references, json)).pipe(
  Command.withDescription("observe local USL references and obtain a non-executing HSWM research proposal")
)

const episodeOptions = {
  question: Args.text({ name: "question" }),
  target: Options.text("target").pipe(Options.withDefault("cpt::open:gate1-original-cycle-signed-global-intersections")),
  references: Options.text("reference").pipe(Options.repeated),
  mode: Options.choice("mode", ["investigate", "review", "compute"]).pipe(Options.withDefault("investigate")),
  tier: Options.choice("tier", ["supporting", "core"]).pipe(Options.withDefault("supporting")),
  runner: Options.text("runner").pipe(Options.withDefault("")),
  budget: Options.integer("budget").pipe(Options.withDefault(600)),
  stateFile: Options.text("state-file").pipe(Options.withDefault("")),
  json
} as const
const run = Command.make("run", episodeOptions, (options) => researchEpisodeCommand("run", options, options.json)).pipe(
  Command.withDescription("execute a bounded HSWM research episode with USL context and actual LLM cells"))
const plan = Command.make("plan", episodeOptions, (options) => researchEpisodeCommand("plan", options, options.json)).pipe(
  Command.withDescription("inspect HSWM research route selection without invoking cells"))
const profile = Options.choice("profile", ["v1", "v2"]).pipe(Options.withDefault("v1"))
const state = Command.make("state", { json, profile }, ({ json, profile }) => researchStateCommand("status", json, profile))
const graph = Command.make("graph", { json, profile }, ({ json, profile }) => researchStateCommand("graph", json, profile))
const intuition = Command.make("intuition", {
  stateFile: Args.text({ name: "state-file" }), without: Options.text("without").pipe(Options.repeated), json
}, ({ stateFile, without, json }) => researchIntuitionCommand(stateFile, without, json)).pipe(
  Command.withDescription("explain source-bound research dependencies and inspect the actual HSWM route, including hypothetical input removal"))
const feedback = Command.make("feedback", {
  episode: Args.text({ name: "episode" }),
  useful: Options.choice("useful", ["true", "false"]),
  source: Options.text("source"), json
}, ({ episode, useful, source, json }) => researchFeedbackCommand(episode, useful, source, json)).pipe(
  Command.withDescription("update HSWM route estimates using an explicit research usefulness review"))
const cell = Command.make("cell", {
  stage: Args.choice([
    ["references", "references"], ["formulate", "formulate"], ["adversary", "adversary"],
    ["synthesize", "synthesize"], ["compute", "compute"], ["domain", "domain"],
    ["comparison", "comparison"], ["obstruction", "obstruction"], ["connections", "connections"]
  ] as const, { name: "stage" })
}, ({ stage }) => researchCellCommand(stage)).pipe(Command.withDescription("internal HSWM JSON-stdin research cell adapter"))

export const researchContextCommand = Command.make("research", {}, () =>
  Console.log("Use `ice research run <question>`, `intuition <state-file>`, `plan`, `state`, `graph`, or `feedback <episode>`."))
  .pipe(Command.withDescription("HSWM research execution and USL reference context"),
    Command.withSubcommands([run, plan, intuition, state, graph, feedback, status, prepare, cell]))
