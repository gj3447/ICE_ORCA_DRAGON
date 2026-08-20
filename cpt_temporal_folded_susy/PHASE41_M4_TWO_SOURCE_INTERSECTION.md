# Phase 41 — m=4 two-source local joint intersections

## Outcome

Phase 41 evaluates the frozen four-segment, two-source workflow in
`PHASE41_M4_TWO_SOURCE_INTERSECTION_INPUTS.json`.  The production run
completed with

```text
exact contracts:     7 / 7 PASS
numerical contracts: 8 / 9 PASS
run_status:           VALID_TYPED_RUN
process exit:         0
Gate 1:               OPEN_PARTIAL_PROGRESS
```

The one failed numerical contract is the full finite-difference tangent
control.  It failed the frozen adjacent-step plateau threshold at the same
chart column at all three audited points.  The finite-difference determinant
signs and the finite-difference-to-variational operator errors passed their
separate tests.  The failure is retained as
`TANGENT_CONTROL_FAILED`; no later step was selected after seeing the result.

All five primary full-\(\mathbb R^{14}\) local cap candidates were found and passed the
frozen residual, rank, transversality, parameter-window, reflection, direct
orientation, root-parity, ambient mode-basis, and strict overlap-chart
checks.  The radius and launch-shape controls and all five first-cap/path
ledgers also passed.  Nevertheless, the tangent plateau failure means that
the source-scoped local robustness claims remain **inconclusive**.

The two-source, anchor-subtracted saddle response passes the frozen stable
numerical rank-two rule.  This is a finite-precision statement in one
declared normalization, not a proof of exact algebraic rank.

No bounded-chain or global Picard–Lefschetz integer is emitted:

```text
bounded_chain_signed_sum = null
complete_global_signed_intersection_vector = null
global_n_sigma = null
cutoff_limit = null
continuum_limit = null
quantum_gravity_explanation = null
```

## 1. Frozen provenance and actual execution

The input manifest was introduced in commit
`58181447b558fa204406b732badd5c2fd541bb47` and has SHA-256

```text
dc17f4d25e758946fe00fec0bb209462294d4d982b1f86b59c099b8de064c92e
```

It is explicitly a post-feasibility workflow freeze, not a preregistration
or scientific-evidence artifact.  In particular, no reproducible pre-freeze
m=4 \(\mathbb R^{14}\) cap solution or local-orientation sign was retained.  The desired
direct sign, root sign, response rank, cutoff verdict, and global
intersection coefficient are all absent from the frozen inputs.

The final executable has SHA-256

```text
377506ed838b88e2c88c33bbb7c4bb7829fbdd8ae0329635b0587a2b8425d530
```

The actual zero-exit command was

```bash
.venv/bin/python cpt_temporal_folded_susy/phase41_m4_two_source_intersection.py
```

The executable writes no result file.  It emitted one typed `RESULT_JSON=`
record to standard output, followed by

```text
Completed 7/7 exact and 8/9 numerical contracts; Gate 1 remains OPEN_PARTIAL_PROGRESS.
```

This Markdown file is a human-readable summary of that frozen stdout run,
not a byte-for-byte archive of the full JSON.  Exact recovery of the full
payload requires rerunning the command with the same manifest, executable,
locked Python environment, and committed Phase-39 direction artifacts.  The
calculation is CPU-bound and the production run took on the order of tens of
minutes; no cross-process numerical cache or saved root artifact is assumed.

## 2. Model, sources, and one fixed flow geometry

The configuration space is

\[
X_4=\mathbb C^6_{a_1,\phi_1,a_2,\phi_2,a_3,\phi_3}
\times\mathbb C_T^*.
\]

With \(h=1/4\), one scalar midpoint action generates the complete
seven-component gradient and \(7\times7\) Hessian:

\[
S_4=2\pi^2\sum_{e=0}^{3}\left[
\frac{-6a_{e+1/2}(\Delta a_e)^2
+a_{e+1/2}^3(\Delta\phi_e)^2}{2Th}
+Th\left(-3a_{e+1/2}+a_{e+1/2}^3V(\phi_{e+1/2})\right)
\right],
\]

\[
V(\phi)=\frac34\left(1-e^{-\sqrt{2/3}\phi}\right)^2.
\]

The two real endpoint probes are

\[
a_L=a_b(1-\delta_a/2),\qquad
a_R=a_b(1+\delta_a/2),
\]

\[
\phi_L=\phi_b-\delta_\phi/2,\qquad
\phi_R=\phi_b+\delta_\phi/2.
\]

The `a_only` and `phi_only` axes are each solved at
\(-10^{-3},-5\times10^{-4},0,5\times10^{-4},10^{-3}\).  Positive and
negative saddle arms separately start from the one common zero-source root
and proceed from half step to full step.  The looser-tolerance solver-control
repeat obeys the same arm rule; target roots from the primary grid are not
used as warm starts.

At the shared saddle, the real Hessian inertia is

\[
(4\text{ negative},3\text{ positive},0\text{ zero}).
\]

Its eigenvalues begin

\[
-1.0179812891\times10^5,
-5.9514218194\times10^4,
-1.7311348622\times10^4,
-4.1974473011,
\]

and the positive eigenvalues are approximately

\[
3029.250775,\quad 10360.303503,\quad 17741.257197.
\]

One zero-source whitening map \(L_{4,0}\), mobility
\(M_{4,0}=L_{4,0}L_{4,0}^{T}\), and metric
\(g_{4,0}=M_{4,0}^{-1}\) are held fixed for every source, sign, launch shape,
and trajectory.  No source rewhitening or flow-metric mutation occurs.

The main fixed-geometry diagnostics are

| diagnostic | maximum/result |
|---|---:|
| mobility reflection relative error | \(5.38\times10^{-16}\) |
| \(Q\) orthogonality residual | \(5.25\times10^{-14}\) |
| \(Q^2-I\) residual | \(5.90\times10^{-16}\) |
| signed-projector reflection relative error | \(9.88\times10^{-13}\) |
| block-Procrustes frame error | \(9.87\times10^{-13}\) |
| \(J^T H_\xi J+I\), \(\lambda=1\) | \(1.08\times10^{-12}\) |

These pass the frozen \(2\times10^{-7}\) geometry tolerances.  They are
finite-cutoff numerical identities, not a metric-homotopy theorem.

## 3. Exact identities and the nonnesting negative control

The seven exact contracts verify:

1. one four-element scalar action generates every derivative;
2. the action is holomorphic off \(T=0\), with nonidentically-zero pole
   residue;
3. action, gradient, and Hessian obey the joint signed-source reflection;
4. the declared DST and nested bases have determinant \(+1\), reflection
   parity `+++--++`, and positive transition determinant;
5. the m=2 affine grid/cap embedding and retraction are exact, while the
   nonlinear midpoint actions are not identical;
6. \(\Gamma\) and \(K\) are both seven-real-dimensional in \(\mathbb R^{14}\),
   so replacing \(V_K\) by \(-V_K\) changes the determinant sign;
7. incomplete chain, census, Stokes, end, and physical-cycle data force all
   promoted outputs to remain false, null, or open.

The exact nonnesting witness is

\[
-\frac{63\pi^2}{32}e^{-\sqrt6/3}
+\frac{63\pi^2}{64}e^{-2\sqrt6/3}
+\frac{63\pi^2}{64}\ne0.
\]

Thus the m=2 and m=4 grids have an exact affine relation, but their
nonlinear actions, Hessians, upward cycles, and determinant lines are not
identified.

## 4. Two-source anchor-subtracted response

Define

\[
a_{\rm odd}=\frac{a_3-a_1}{\sqrt2},\qquad
\phi_{\rm odd}=\frac{\phi_3-\phi_1}{\sqrt2},
\]

subtract the linear endpoint-anchor contribution, and normalize the output
and source as frozen in the manifest.  In row order
`(a_odd/a_b, phi_odd/phi_b)` and column order
`(delta_a, delta_phi/phi_b)`, the reported half-step matrix is

\[
\chi_{1/2}\simeq
\begin{pmatrix}
4.641563772\times10^{-4} & 1.789434943\times10^{-3}\\
5.176662239\times10^{-3} & -1.063148730\times10^{-3}
\end{pmatrix}.
\]

The pre-freeze feasibility matrix is numerically the full-step matrix, not
the production output.  The script explicitly reports \(\chi_{1/2}\) and
separately retains \(\chi_1\).

The half-step singular values are approximately

\[
(5.28567\times10^{-3},\ 1.84589\times10^{-3}).
\]

The frozen error ledger gives

\[
E_{\rm step}\simeq6.52667\times10^{-6},\qquad
E_{\rm solver}\simeq2.43\times10^{-12},
\]

and therefore

\[
\frac{\sigma_{\min}(\chi_{1/2})}{10(E_{\rm step}+E_{\rm solver})}
\simeq28.2823>1.
\]

The maximum source-reversal residual is \(1.76\times10^{-16}\), and the
independently continued control grid also passes the saddle residual,
inertia, nondegeneracy, and reflection checks.  Consequently the frozen rule
supports **stable numerical rank two**.  It does not prove exact rank two,
exclude a smaller singular value outside the tested scale, or make either
endpoint probe a physical arrow of time.

## 5. Five primary local intersections and orientation

The five primary points are

```text
shared_zero
phi_minus   (delta_a=0,      delta_phi=-0.001)
phi_plus    (delta_a=0,      delta_phi=+0.001)
a_minus     (delta_a=-0.001, delta_phi=0)
a_plus      (delta_a=+0.001, delta_phi=0)
```

The positive half steps are continuation points.  Each negative full point
is independently solved from the shared zero seed; it is not manufactured
by reflecting the positive endpoint.

All five full \(\mathbb R^{14}\) candidates pass.  Their direct declared
signs are \(+1\), and their assembled nonlinear-root Jacobian signs are
\(-1\), as required when seven \(K\) columns are negated.  Reversing one
declared \(\Gamma\) parameter or one declared \(K\) parameter also reverses
the direct sign.

The signed endpoint candidates reflect into one another with physical
maximum residuals

| source | physical reflection max |
|---|---:|
| phi-only | \(1.385\times10^{-12}\) |
| a-only | \(6.058\times10^{-12}\) |

The DST and nested transformations act on the ambient realified **rows** of
the tangent matrix.  They are not applied to the cap/chart parameter
columns.  Both coordinate descriptions preserve the reported direct sign.

At every primary candidate, a second overlapping chart is constructed and
strictly re-integrated with its transported tangent.  Its transition
orientation, transition singular gap, chart margin, cap-state match, and
corrected sign pass.  This is a genuine overlap control rather than an
algebraic relabeling of the primary tangent.

The observed within-m=4 signs agree descriptively with the separately
audited m=3 declared-coordinate sign.  The m=3 and m=4 grids are nonnested,
and no common determinant line has been constructed, so this is not a
canonical cross-cutoff equality or convergence result.

## 6. The retained tangent-control failure

The root-parameter order is

```text
y_a1, y_phi1, y_a2, y_phi2, y_a3, y_phi3, psi,
u1, u2, u3, u4, u5, u6, flow_time
```

At `shared_zero`, `phi_plus`, and `a_plus`, the full residual is evaluated
with the strict DOP853 state map.  For every column, the implementation uses
the first adjacent pair of surviving finite-difference steps in the frozen
descending ladder.  It does not skip an unfavorable plateau.

All three finite-difference determinants have root sign \(-1\), agreeing
with the expected odd-seven-column parity.  The full operator errors also
pass:

| point | FD-to-variational relative operator error |
|---|---:|
| shared_zero | \(1.64506\times10^{-3}\) |
| phi_plus | \(7.73922\times10^{-4}\) |
| a_plus | \(1.35951\times10^{-3}\) |

Each is below the frozen two-percent threshold.  However, zero-based column
8, the `u2` chart column, fails its first-adjacent-pair plateau test:

| point | steps used | `u2` adjacent-step relative change |
|---|---:|---:|
| shared_zero | \(2\times10^{-6},5\times10^{-7}\) | 0.2988500 |
| phi_plus | \(2\times10^{-6},5\times10^{-7}\) | 0.2219933 |
| a_plus | \(2\times10^{-6},5\times10^{-7}\) | 0.7952717 |

All exceed 0.02.  A small aggregate operator error does not override an
unstable individual column, because the operator norm is dominated by other
columns.  Nor may a smaller later pair be selected after observing this
failure.  The correct Phase-41 result is therefore

```text
P41.tangent.three_full_FD_controls = TANGENT_CONTROL_FAILED
```

This failure makes the transported-frame trust and both source-scoped local
robustness claims inconclusive.  It does not erase the computed local roots,
and it is not a proof that no stable tangent discretization exists.

## 7. Launch and path controls

The frozen launch-control aggregate passes:

- radii \(5\times10^{-5}\), \(10^{-4}\), and \(2\times10^{-4}\) are tracked
  at `shared_zero`, `phi_plus`, and `a_plus`;
- the \(\lambda=1\) Morse-normalized ellipsoid is compared with the
  \(\lambda=0\) aligned orthonormal launch at `phi_plus` and `a_plus`;
- a repeated sign counts only when the normalized ambient cap state matches
  within \(5\times10^{-5}\);
- changing \(\lambda\) changes the finite launch surface, never the fixed
  flow mobility.

All five primary flow ledgers pass sampled nonincrease of
\(\operatorname{Re}S\), drift control for \(\operatorname{Im}S\), the
\(\xi\)-norm box, field/chart/phase/time margins, and an independent first
\(|T|=0.3\) event whose state matches the reported cap endpoint.

These checks support a finite-launch local cap-piece calculation.  They do
not classify the straight arms, later cap reintersections, all directions,
all roots, or the complete nonlinear upward manifold.

## 8. Contract ledger and claim boundary

| numerical contract | result |
|---|---|
| signed two-source saddle grids | PASS |
| anchor-subtracted response matrix | PASS; stable numerical rank two |
| one fixed mobility for both sources | PASS |
| five primary full-\(\mathbb R^{14}\) candidates | PASS |
| direct/root/basis/overlap orientation | PASS |
| three full finite-difference tangent controls | `TANGENT_CONTROL_FAILED` |
| radius and launch-shape controls | PASS |
| first-cap and flow-box ledgers | PASS |
| no-global-integer guard | PASS |

The typed interpretation is therefore:

```text
phi_only_local_m4_robustness = INCONCLUSIVE_WITHIN_FROZEN_LOCAL_PROTOCOL
a_only_local_m4_robustness   = INCONCLUSIVE_WITHIN_FROZEN_LOCAL_PROTOCOL
two_source_stable_numerical_rank = RANK_TWO_SUPPORTED_WITHIN_FROZEN_NORMALIZATION
exact_algebraic_response_rank = NOT_PROVED
m3_m4_sign_relation = DESCRIPTIVE_SEPARATELY_AUDITED_COMPARISON_ONLY
common_cross_cutoff_determinant_line = NOT_CONSTRUCTED
global_Picard_Lefschetz_promotion = PROHIBITED
Gate_1 = OPEN_PARTIAL_PROGRESS
SUSY_quantum_gravity_or_cosmology_claim = NOT_LICENSED
```

All sixteen incomplete-data booleans remain `false`.  In particular, no
action/upward-cycle identification across m=2 and m=4, no canonical m=3/m=4
sign equality, no straight-arm or reintersection census, no continuous
direction coverage, no root exhaustion, no nonlinear-manifold certificate,
no non-Stokes chamber, no relative-good-end classification, no physical
original cycle, no metric homotopy, and no BFV/Pfaffian/Pin orientation line
has been established.

## 9. Implementation-audit repairs after the input freeze

The manifest bytes, physical action, endpoints, source grids, fixed metric,
cap, launch radii and shapes, parameter boxes, solver tolerances, finite-
difference ladders, acceptance thresholds, and promotion boundary were not
changed during implementation.  The following repairs made the executable
obey those already-frozen inputs:

- the aligned-frame orientation repair flips one column, rather than two
  columns whose determinant effect would cancel;
- the production response reports the half-step matrix, while the disclosed
  pre-freeze spot remains labeled as a full-step observation;
- the Phase-39 prolongated seed keeps the actual cap `psi` distinct from its
  equatorial chart coordinate;
- BDF is seed-only; strict DOP853 determines the reported root even if the
  coarse solver's status flag is false;
- DST/nested mode changes act on realified ambient rows rather than on
  \(\Gamma/K\) parameter columns;
- the overlap chart strictly re-integrates both state and tangent before its
  corrected sign is accepted;
- the Phase-39 artifact paths resolve relative to the repository rather than
  the caller's working directory;
- the solver-tolerance response repeat follows independent signed
  zero-to-half-to-full arms and receives the same saddle diagnostics;
- nonfinite numerical payloads and numerical-stage exceptions emit a typed
  invalid-run JSON before nonzero exit, while ordinary scientific negative
  or inconclusive outcomes retain zero-exit typed results;
- local and rank claims are gated by all applicable numerical prerequisites,
  and every bounded/global/continuum/quantum-gravity output remains null.

These were implementation and audit-semantic corrections, not amendments to
the scientific input manifest and not post-result tuning of a desired sign,
rank, or root.

## 10. Reproduction limits and next calculation

This run establishes a local finite-cutoff computational ledger only.  Its
reproduction depends on the exact manifest and script hashes above, the
locked NumPy/SciPy/SymPy environment, and the byte-pinned Phase-39 source
artifacts used to derive the chart center.  The executable does not archive
its long JSON output or numerical roots, and it does not prove platform-
independent bitwise equality.  Reproduction should compare typed structure,
signs, inequalities, and toleranced numerical invariants rather than stdout
bytes.

The immediate next calculation is not global promotion.  It is to diagnose
the `u2` finite-difference plateau without changing the frozen Phase-41
outcome: separate integration noise, chart conditioning, and true local
nonlinearity using a newly declared control.  Any new step ladder, chart,
tolerance, or higher-precision map must be frozen as a new input rather than
retroactively substituted into this run.  Only after the tangent control is
resolved should the original cap-plus-arm chain, reintersections,
direction/root census, Stokes data, relative ends, and physical original
cycle be completed for a possible Gate-1 global coefficient.
