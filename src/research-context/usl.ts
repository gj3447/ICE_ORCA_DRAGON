import { pathToFileURL } from "node:url";

import { asJsonObject, type JsonObject } from "./core.ts";

export interface ResearchReferenceResource {
  readonly name: string;
  readonly role: string;
  readonly kind: "kg" | "filesystem";
  readonly locator: string;
  /** A caller-pinned comparison value. It is never used as an observation. */
  readonly contentHash: string;
}

export type ReadSnapshot = (locator: string) => Promise<{ readonly contentHash: string }>;

type UnknownRecord = Readonly<Record<string, unknown>>;
type ExternalEffect = unknown;

type ExternalEffectModule = {
  readonly Effect: {
    readonly fail: (error: unknown) => ExternalEffect;
    readonly provide: (effect: ExternalEffect, layer: unknown) => ExternalEffect;
    readonly runPromise: (effect: ExternalEffect) => Promise<unknown>;
    readonly tryPromise: <A>(options: {
      readonly try: () => Promise<A>;
      readonly catch: (cause: unknown) => unknown;
    }) => ExternalEffect;
  };
  readonly Either: {
    readonly isLeft: (value: unknown) => boolean;
  };
  readonly Layer: {
    readonly succeed: (tag: unknown, service: unknown) => unknown;
  };
};

type ExternalLanguageModule = {
  readonly compileSource: (source: string) => unknown;
  readonly observeProgram: (plan: unknown, options: {
    readonly links: readonly string[];
    readonly allowedLocators: readonly string[];
    readonly maxResources: number;
    readonly sourceText: string;
  }) => ExternalEffect;
};

type ExternalResolveModule = {
  readonly Resolvers: unknown;
  readonly ResolveError: new (input: {
    readonly kind: string;
    readonly locator: string;
    readonly reason: "ORPHAN" | "DENIED";
    readonly detail: string;
  }) => unknown;
};

type ExternalLocatorModule = {
  readonly formatLocator: (locator: unknown) => string;
};

type PlanResource = {
  readonly name: string;
  readonly locator: { readonly kind: string };
};

type PlanParticipant = {
  readonly role: string;
  readonly resource: string;
};

type PlanLink = {
  readonly name: string;
  readonly participants: readonly PlanParticipant[];
};

type PlanLike = {
  readonly resources: readonly PlanResource[];
  readonly links: readonly PlanLink[];
};

const SHA256_HEX = /^(?:sha256:)?[a-f0-9]{64}$/i;

const isRecord = (value: unknown): value is UnknownRecord =>
  typeof value === "object" && value !== null && !Array.isArray(value);

const valueDescription = (value: unknown): string => {
  if (value instanceof Error) return value.message;
  if (typeof value === "string") return value;
  return JSON.stringify(value) ?? String(value);
};

const requirePlan = (value: unknown): PlanLike => {
  if (!isRecord(value) || !Array.isArray(value.resources) || !Array.isArray(value.links)) {
    throw new Error("external USL compiler returned an invalid semantic plan");
  }
  const resources: PlanResource[] = value.resources.map((resource) => {
    if (!isRecord(resource) || typeof resource.name !== "string" || !isRecord(resource.locator) || typeof resource.locator.kind !== "string") {
      throw new Error("external USL plan has an invalid resource declaration");
    }
    return { name: resource.name, locator: { kind: resource.locator.kind } };
  });
  const links: PlanLink[] = value.links.map((link) => {
    if (!isRecord(link) || typeof link.name !== "string" || !Array.isArray(link.participants)) {
      throw new Error("external USL plan has an invalid link declaration");
    }
    const participants = link.participants.map((participant) => {
      if (!isRecord(participant) || typeof participant.role !== "string" || typeof participant.resource !== "string") {
        throw new Error("external USL plan has an invalid link participant");
      }
      return { role: participant.role, resource: participant.resource };
    });
    return { name: link.name, participants };
  });
  return { resources, links };
};

const unique = (values: readonly string[], label: string): void => {
  if (new Set(values).size !== values.length) throw new Error(`duplicate ${label} in caller resource declarations`);
};

const checkedResources = (resources: readonly ResearchReferenceResource[]): void => {
  unique(resources.map((resource) => resource.name), "name");
  unique(resources.map((resource) => resource.role), "role");
  unique(resources.map((resource) => resource.locator), "locator");
  for (const resource of resources) {
    if (!resource.name || !resource.role || !resource.locator || !SHA256_HEX.test(resource.contentHash)) {
      throw new Error("caller resource declarations require nonempty name, role, locator, and SHA-256 contentHash");
    }
  }
};

const validateSelectedLink = (
  plan: PlanLike,
  resources: readonly ResearchReferenceResource[],
  formatLocator: (locator: unknown) => string,
  rawPlan: unknown,
): void => {
  const selected = plan.links.filter((link) => link.name === "research");
  if (selected.length !== 1) throw new Error('USL source must declare exactly one selected link named "research"');
  const rawResources = isRecord(rawPlan) && Array.isArray(rawPlan.resources) ? rawPlan.resources : [];
  if (rawResources.length !== plan.resources.length) throw new Error("external USL plan resource declarations changed during validation");

  const declarations = new Map<string, { readonly kind: string; readonly locator: string }>();
  for (let index = 0; index < plan.resources.length; index += 1) {
    const resource = plan.resources[index]!;
    const raw = rawResources[index];
    if (!isRecord(raw) || !isRecord(raw.locator)) throw new Error("external USL plan resource locator is unavailable");
    declarations.set(resource.name, { kind: resource.locator.kind, locator: formatLocator(raw.locator) });
  }

  const participants = selected[0]!.participants;
  if (participants.length !== resources.length) throw new Error("research link participant count must equal caller resource count");
  const byRole = new Map(participants.map((participant) => [participant.role, participant.resource]));
  if (byRole.size !== participants.length) throw new Error("research link has duplicate participant roles");

  for (const resource of resources) {
    const name = byRole.get(resource.role);
    if (name !== resource.name) throw new Error(`research link role ${resource.role} must select caller resource ${resource.name}`);
    const declaration = declarations.get(resource.name);
    if (!declaration || declaration.kind !== resource.kind || declaration.locator !== resource.locator) {
      throw new Error(`USL declaration for ${resource.name} does not match its caller allowlist entry`);
    }
  }
};

const externalModuleUrl = (uslRoot: string, relativePath: string): string =>
  pathToFileURL(`${uslRoot.replace(/\/$/, "")}/${relativePath}`).href;

const requiredJsonObject = (value: unknown, label: string): JsonObject => {
  const object = asJsonObject(value);
  if (object === undefined) throw new Error(`${label} is not JSON object data`);
  return object;
};

/**
 * Read-only USL observation adapter. It loads the supplied USL checkout at
 * runtime, limits it to the caller's exact resource declarations, and obtains
 * every observed content hash from `readSnapshot` at observation time.
 */
export const observeResearchReferences = async (
  uslRoot: string,
  source: string,
  resources: readonly ResearchReferenceResource[],
  readSnapshot: ReadSnapshot,
): Promise<{ readonly plan: JsonObject; readonly report: JsonObject }> => {
  checkedResources(resources);

  const [languageModule, resolveModule, locatorModule, effectModule] = await Promise.all([
    import(externalModuleUrl(uslRoot, "src/language/index.ts")) as Promise<ExternalLanguageModule>,
    import(externalModuleUrl(uslRoot, "src/resolve.ts")) as Promise<ExternalResolveModule>,
    import(externalModuleUrl(uslRoot, "src/locator.ts")) as Promise<ExternalLocatorModule>,
    import(externalModuleUrl(uslRoot, "node_modules/effect/dist/esm/index.js")) as Promise<ExternalEffectModule>,
  ]);

  const compiled = languageModule.compileSource(source);
  if (effectModule.Either.isLeft(compiled)) {
    const detail = isRecord(compiled) ? valueDescription(compiled.left) : valueDescription(compiled);
    throw new Error(`USL source compilation failed: ${detail}`);
  }
  if (!isRecord(compiled) || !("right" in compiled)) throw new Error("external USL compiler returned an invalid Either result");
  const plan = compiled.right;
  const checkedPlan = requirePlan(plan);
  validateSelectedLink(checkedPlan, resources, locatorModule.formatLocator, plan);

  const declaredByLocator = new Map(resources.map((resource) => [resource.locator, resource]));
  const resolver = {
    resolve: (locator: unknown): ExternalEffect => {
      const formatted = locatorModule.formatLocator(locator);
      const declared = declaredByLocator.get(formatted);
      const kind = isRecord(locator) && typeof locator.kind === "string" ? locator.kind : "unknown";
      if (!declared || kind !== declared.kind) {
        return effectModule.Effect.fail(new resolveModule.ResolveError({
          kind,
          locator: formatted,
          reason: "DENIED",
          detail: "locator is outside the caller's exact resource allowlist",
        }));
      }
      return effectModule.Effect.tryPromise({
        try: async () => {
          const snapshot = await readSnapshot(formatted);
          if (!SHA256_HEX.test(snapshot.contentHash)) throw new Error("readSnapshot did not return a SHA-256 content hash");
          return {
            locator,
            resolvedLocator: formatted,
            contentHash: snapshot.contentHash,
            resolvedAt: new Date().toISOString(),
            guaranteeLevel: "trust_host" as const,
            matchCount: 1,
          };
        },
        catch: (cause) => new resolveModule.ResolveError({
          kind,
          locator: formatted,
          reason: "ORPHAN",
          detail: `fresh snapshot is unavailable: ${valueDescription(cause)}`,
        }),
      });
    },
  };
  const layer = effectModule.Layer.succeed(resolveModule.Resolvers, resolver);
  const observation = languageModule.observeProgram(plan, {
    links: ["research"],
    allowedLocators: resources.map((resource) => resource.locator),
    maxResources: resources.length,
    sourceText: source,
  });
  const report = await effectModule.Effect.runPromise(effectModule.Effect.provide(observation, layer));
  return { plan: requiredJsonObject(plan, "USL plan"), report: requiredJsonObject(report, "USL observation report") };
};
