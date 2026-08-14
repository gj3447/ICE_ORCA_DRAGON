# Contributing

Thanks for your interest in contributing!

## Contributor License Agreement (required)

This project is **dual-licensed** — AGPL-3.0-or-later **and** a separate commercial
license (see [`LICENSING.md`](./LICENSING.md)). To keep that model viable, **100% of
the copyright must stay with the owner**, so every contribution requires agreement to
the CLA.

**Before your pull request can be merged**, read [`CLA.md`](./CLA.md) and include this
exact line in your PR description:

```
I have read and agree to the Contributor License Agreement (CLA.md).
```

Pull requests without this sign-off will not be merged. By contributing you agree your
contribution may also be distributed under the owner's commercial license (per CLA.md).

Contact: Ra Gyeongjun (라경준) — gj3447@gmail.com

## Development and validation

The control plane and numerical kernels have separate exact locks:

```bash
npm ci
uv sync --locked
./ice doctor
npm run check
```

For a changed numerical kernel, confirm its live name and run the directly relevant checks:

```bash
./ice list
./ice info <name>
./ice run <name>
# Only if <name> appears in ./ice repro --list:
./ice repro --only <mapped-script-name>
```

`npm run check` protects the TypeScript/Effect control-plane contract; it is not a
physics oracle. Choose the highest applicable tier before execution:

- T0 engineering: run directly relevant Node/Python/lock checks.
- T1 reproduction: record frozen inputs, environment, baseline, comparator, and diff; do not change
  claim confidence.
- T2 claim-impact work: run the full evidence gate in
  [`.claude/skills/science-feedback-loop.md`](.claude/skills/science-feedback-loop.md), including
  preregistration and null/multiplicity analysis only when applicable.

Lakatos is a programme/fiber checkpoint, not a mandatory label on every scientific code change. A T2
code change still needs its ordinary T0 engineering checks.

Do not relax the global comparator to make a drift green. Register a field-level
semantic invariant with evidence, or classify the artifact as nonportable. In
particular, the legacy queue03 metric is intentionally `NONPORTABLE_FAIL`.

Material/reusable T2 results may produce `PENDING` evidence. Direct confidence, status, Contract, Span,
or supersession changes require separate authorized ratification.
