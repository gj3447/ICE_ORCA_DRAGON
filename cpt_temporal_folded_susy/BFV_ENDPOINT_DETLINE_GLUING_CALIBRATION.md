# Finite BFV endpoint / determinant-line / gluing calibration

This unnumbered runner is a deliberately finite parametrized-free-particle
calibration for the P6 method lane.  It checks one compatible package only:

1. a fixed- `x` endpoint polarization and same- `x` interface pairing;
2. two ordered, nondegenerate finite ghost blocks and their relative Pfaffian
   reference orientation; and
3. the two-slab phase and squared-prefactor identities, with the remaining
   square-root sign fixed by the same declared `+i0` continuation on both slabs.

The lapse relative cycle is not an output selected by this calculation.  It is
an input with `status: OPEN`, `selected_contour: null`, and
`picard_lefschetz_selection: null`.  Consequently, the calibration supplies no
V=0 or gravitational absolute BFV measure, continuum determinant/Pfaffian
line, global thimble coefficient, or physical cycle.

The runner is fail-closed: a degenerate ghost block, non-antisymmetric block,
orientation mismatch, or gluing mismatch yields `FAIL_CLOSED` and exit status
1.  It writes its result only when explicitly run.

Primary method references are Cattaneo--Mnev--Reshetikhin,
[*Classical and quantum Lagrangian field theories with boundary*](https://arxiv.org/abs/1207.0239),
and Cattaneo--Mnev,
[*A note on gluing via fiber products in the (classical) BV-BFV formalism*](https://arxiv.org/abs/2208.11211).

## Intended bounded invocation

```bash
./ice run bfv_endpoint_detline_gluing_calibration
```

No execution is recorded by this document.  A successful toy calibration must
not be read as selecting a lapse contour or as promoting an absolute measure.
