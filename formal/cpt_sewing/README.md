# ICE CPT boundary sewing — Lean 4

This project formalizes the **real bosonic boundary algebra** of the
[source construction design](../../docs/research/ICE_CPT_SEWING_ORIGINAL_CYCLE_CONSTRUCTION_DESIGN_2026-09-06.md).
It uses Lean `4.33.0` and mathlib commit
`db584cd6d46c92f209a44c0f1c829460d327499d`; all dependency revisions are in
[`lake-manifest.json`](lake-manifest.json).

Prepare the pinned dependencies in this directory with `lake update`. Lake's
mathlib hook downloads its official compiled dependency cache. If necessary,
`lake exe cache get` restores it. `.lake/` and generated binaries are local caches.
No sibling checkout is required.

From the repository root, perform the recorded proof verification with:

```sh
./ice run cpt_boundary_sewing_lean
```

The committed runner reads the actual [`Boundary.lean`](CptSewing/Boundary.lean)
source and appends `#check` and `#print axioms` for every theorem named in
[`proof-index.json`](proof-index.json). It re-elaborates that complete source in
one fresh Lean invocation. It does not accept an old project `.olean` as proof
of a changed source. The result includes compiler diagnostics, exact theorem
types, transitive axiom sets, source hashes and dependency revisions.

The accepted axiom set is limited to `propext`, `Classical.choice`, and
`Quot.sound`. Compilation warnings and errors fail. Separate temporary
negative controls check rejection of an admitted proof and of a custom axiom
that the compiler itself accepts. They are not project theorems.
The official basis for this audit is the
[Lean proof-validation reference](https://lean-lang.org/doc/reference/latest/ValidatingProofs/).

The theorem interface has three parts:

- Real momentum reflection is involutive, preserves the positive-scale chart
  and the declared Starobinsky Hamiltonian, and negates the evaluated canonical
  one-form and coordinate symplectic pairing.
- The sum primitive vanishes in every configuration direction exactly when
  the momenta are opposite. The difference primitive requires equal momenta.
- Explicit witnesses inside `a > 0` show that the two incorrect combinations
  of orientation and matching have residual `2`, rather than zero.

The source defines the coordinate expression of `d alpha`; it does not build
manifold differential forms. Lean's real division is total at zero, whereas
the physical source chart requires `a > 0`; this domain is recorded separately.
No theorem proves the bulk variation/GHY reduction, full quantum CPT,
ghost/BFV compatibility, boundary state, original integration cycle,
global intersection vector or physical discovery. Those objects remain open.
