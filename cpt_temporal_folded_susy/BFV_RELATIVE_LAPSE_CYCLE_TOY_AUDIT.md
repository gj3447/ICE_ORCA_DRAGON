# Open rapid-decay lapse-ray toy audit

This is the smallest separate method-lane work unit after the finite endpoint/
determinant-line/gluing calibration. It does **not** repair that result's open
lapse-cycle field, and it does not select an initial cycle for gravity.

It instead fixes an independent, finite analytic toy on
\(\mathbb C^*=\mathbb C\setminus\{0\}\):

\[
  e^{-(a/N+bN)},\qquad a,b>0,
\]

with the declared open rapid-decay ray \(\Gamma_+:(0,\infty)\). No relative-
homology group or class is specified. The runner checks
only that this ray decays at its two stated ends, that the forward and inverse
maps \((r_1,r_2)\leftrightarrow(T,s)\) preserve the positive two-slab domain,
that their orientation sign is recorded, and that the principal square-root
convention is compatible there. These are exact analytic bookkeeping checks,
not a contour integral, homology classification, pushforward, or saddle count.

The two supplied BV--BFV references motivate keeping boundary data compatible:
Cattaneo--Schiavina's ADM treatment induces compatible boundary BFV data, and
Cattaneo--Mnev describe classical gluing through a homotopy fiber product.
Neither result supplies the present toy ray's global relative-homology class,
a quantum pushforward, or an absolute gravity measure.

## Fail-closed scope

Even a passing result leaves null: the physical initial lapse relative cycle,
relative-homology class for the declared ray, global relative-homology basis
and Picard--Lefschetz coefficients, quantum
BV--BFV pushforward, V=0/gravity absolute BFV measure, continuum
determinant/Pfaffian line, and a gravity two-slab gluing theorem.

The controlled execution passed 3/3 derived exact checks and four declared
convention/scope guards. It records
`dr_1_wedge_dr_2 = -T*dT_wedge_ds = T*ds_wedge_dT`; this is orientation
bookkeeping, not a pushforward theorem. The result SHA-256 is
`96aff2e2040ae0085c27ecf7a55ef1de9b1cca107f435e3fc71fd22fb766132e`.
The reproduction command is `./ice run bfv_relative_lapse_cycle_toy_audit`.
