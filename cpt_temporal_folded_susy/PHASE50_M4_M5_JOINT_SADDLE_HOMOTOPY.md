# Phase 50 — sampled stabilized m=4→m=5 joint-saddle and local-plane transport

## Outcome

Phase 50 constructs one explicit common-ambient bridge from the retained
Phase-41 four-segment joint saddles to five-segment midpoint-action saddles.
All five frozen source-labelled branches complete the declared action path,
both positive metric paths, the forward/reverse and mesh controls, and the
half/double stabilizer mutations.

The guarded run completed with

```text
run_status:       VALID_RUN
exact checks:     6 / 6 PASS
numerical checks: 8 / 8 PASS
classification:  LOCAL_STABILIZED_M4_M5_SADDLE_UPWARD_PLANE_TRANSPORT_SUPPORTED_ON_FROZEN_PATHS
Gate 1:           OPEN_PARTIAL_PROGRESS
```

This is a sampled, explicitly stabilized local calculation in a declared
finite-dimensional workbench.  It is not a cutoff theorem, a continuation of
the Phase-41 Gamma–K intersections, a common physical determinant line, or a
physics claim.

## 1. Frozen inputs and execution provenance

The post-feasibility manifest first froze the branches, embedding,
stabilizers, paths, mutations, tolerances, and fail-closed outputs in commit
`f5fab2284517a3ac3fd1a41b82e2eb1322de84a8`.  Before any committed runner or
authoritative result, commit
`5e6f04ed7ce40672169c4b6e0cfad8180ec985af` clarified that the λ=0 mobility is
the Phase-42 m=4 mobility pushed into the common ambient space.  It changed no
branch, mesh, stabilizer, threshold, pilot observation, or desired result.

Authoritative artifacts are:

| artifact | commit | SHA-256 |
|---|---|---|
| effective input manifest | `5e6f04ed7ce40672169c4b6e0cfad8180ec985af` | `24706b3b44c1ff426c7b593370acdb324cd39b7998c05ef52e3ba5b88d1e6444` |
| runner | `f00b3e16b1cbb52302f097b2ae0360ec8b140224` | `77290311ad58198ace94f36e919a59fe19a330c5f49bb8c1ed8b6d15af697d90` |
| raw result | `4305c77f264bbe5fb62ea9d333129998e04d37c7` | `22594a5d7c513625384fbdb466101c073f3896a2be597704fa216c9643adbb44` |

The successful command was equivalent to

```bash
proxmox-scratch run p50a --timeout 300 -- bash -lc \
  './ice run phase50_m4_m5_joint_saddle_homotopy \
    > /tmp/ice-p50a.stdout 2> /tmp/ice-p50a.stderr'
```

The 1,159,794-byte raw result uses schema
`ice-phase50-m4-m5-joint-saddle-homotopy/v1`.  Its self-excluding canonical
digest is
`7300500ac7643301f593e720faaae858ea4ccf57b163fd99996b07a2758abc94`.
A strict standard-library parse rejected duplicate/nonfinite tokens, reproduced
that digest, matched the embedded runner hash to the committed source, and
counted every required record.

One preceding wrapper attempt used the longer label
`ice-phase50-authoritative`.  It failed before Python startup with
`listen EINVAL` because the TSX Unix-socket pathname exceeded the platform
limit.  No Phase-50 calculation ran in that attempt.  The failure scratch is
retained under `/var/tmp/orca-failures`; shortening only the wrapper label
resolved the infrastructure failure.

## 2. Common ambient action bridge

For one field, centered m=4 nodal deviations are prolonged to the four m=5
interior nodes by

\[
P=\begin{pmatrix}
4/5&0&0\\
2/5&3/5&0\\
0&3/5&2/5\\
0&0&4/5
\end{pmatrix},
\qquad
q=\frac{1}{\sqrt{10}}(-1,2,-2,1)^T.
\]

The calculation verifies exactly that

\[
(P^TP)^{-1}P^TP=I_3,\qquad P^Tq=0,
\qquad \mathcal R_5P=P\mathcal R_4,
\qquad \mathcal R_5q=-q.
\]

Interleaving the `a` and `phi` copies, copying `T`, and appending the two
added modes gives a real nine-by-nine basis `B` with

\[
\det B=\frac{1152}{3125}>0.
\]

The source-dependent linear endpoint anchor is subtracted before this map is
applied.  For common coordinates

\[
c=B^{-1}(w_5-\bar w_5),
\]

the stabilized endpoint action is

\[
S_0(w_5)=S_4(\bar w_4+c_{0:7})
 +\frac{\kappa_a}{2}c_7^2
 +\frac{\kappa_\phi}{2}c_8^2,
\]

with

\[
\kappa_a=-1.4\times10^5,\qquad
\kappa_\phi=2.4\times10^4,
\]

and

\[
S_\lambda=(1-\lambda)S_0+\lambda S_5.
\]

The gradient and Hessian use the chain rule

\[
\nabla_{w_5}S_0=B^{-T}\nabla_cS_0,
\qquad
H_{w_5}=B^{-T}H_cB^{-1}.
\]

The stabilization is a declared regulator choice, not an identification of
the two discrete actions.  The exact frozen nonnesting witness is

\[
S_5\circ P-S_4=54\pi^2\ne0
\]

at the manifest's rational witness configuration.

## 3. Saddle paths and tangent controls

Each Phase-42 m=4 root is embedded at λ=0, then solved on a 17-node mesh from
0 to 1.  A nine-node mesh and a full reverse 17-node path are separately
solved branch controls.  Every sampled Hessian has inertia `(5-,4+,0)`.

| branch | physical m=5 `T` | m=5 action | max `|∇S|` on path | min `|eig H|` on path | max coarse/fine distance | max forward/reverse distance | max implicit/FD tangent relative |
|---|---:|---:|---:|---:|---:|---:|---:|
| `shared_zero` | `0.7152637783` | `1.4367311437` | `7.671e-10` | `4.19606` | `5.138e-12` | `5.578e-12` | `2.377e-6` |
| `phi_minus` | `0.7151640887` | `1.4373621474` | `7.599e-10` | `4.19425` | `4.274e-12` | `3.639e-12` | `1.152e-6` |
| `phi_plus` | `0.7151640887` | `1.4373621473` | `7.635e-10` | `4.19425` | `2.672e-12` | `3.601e-12` | `2.081e-6` |
| `a_minus` | `0.7158730250` | `1.4330249483` | `7.746e-10` | `4.20698` | `4.291e-12` | `3.317e-12` | `1.918e-6` |
| `a_plus` | `0.7158730250` | `1.4330249483` | `7.584e-10` | `4.20698` | `4.120e-12` | `4.354e-12` | `9.949e-7` |

The frozen limits are `2e-8` for the gradient, `0.1` for the Hessian gap,
and `1e-8` for the mesh and reverse distances.  The largest λ=0 displacement
from the immutable embedded Phase-42 root is `1.711e-12`.

At λ=`0.25`, `0.5`, and `0.75`, the implicit saddle tangent

\[
\frac{dw}{d\lambda}=-H_\lambda^{-1}
(\nabla S_5-\nabla S_0)
\]

is compared with independently re-solved central differences at steps
`2e-4` and `5e-5`.  All thirty columns pass.  The worst implicit/finite-
difference relative discrepancy is `2.377e-6` against `0.005`; the worst
adjacent-step change is `2.281e-6` against `0.02`.

The reflected branch pairs also close at every fine node.  Their worst root
distance is `3.330e-12` and worst action difference is `2.751e-11`, below the
frozen `1e-8` limits.

## 4. Positive metric paths and local upward planes

The λ=0 mobility is

\[
M_0=B\,\operatorname{diag}
(M_{4,0},|\kappa_a|^{-1},|\kappa_\phi|^{-1})B^T,
\]

where `M_4,0` is byte-pinned in the Phase-42 checkpoint.  `M_1` is the native
m=5 zero-source mobility `O |Λ|^-1 O.T`.  The primary affine-invariant SPD
geodesic is

\[
M_\mu=M_0^{1/2}
(M_0^{-1/2}M_1M_0^{-1/2})^\mu M_0^{1/2};
\]

the affine segment `(1-μ)M0+μM1` is the metric-path mutation.

Both are checked at the union of all metric and diagonal-path samples:

| diagnostic | observed worst | frozen limit |
|---|---:|---:|
| minimum mobility eigenvalue | `4.116e-6` | at least `1e-10` |
| maximum mobility condition number | `5.790e4` | at most `1e8` |
| maximum reflection relative error | `6.691e-16` | at most `1e-9` |

For each saddle and mobility, a positive-diagonal Cholesky factor `L` is used
to diagonalize `L.T H L`.  Negative modes receive the frozen negative-real
phase and positive modes the positive-imaginary phase.  Signed blocks are
transported by orthogonal Procrustes alignment along three two-parameter
paths:

1. action first, then metric;
2. metric first, then action;
3. the diagonal `(λ,μ)=(t,t)`.

Across all five sources and both metric choices, the minimum consecutive
upward-plane principal overlap is `0.991143`, above `0.8`.  The minimum
endpoint overlap between the three paths is `0.9999999999999993`, above
`0.999999`, and every endpoint orientation comparison has sign `+1`.

This is a local nine-plane transport.  No Gamma tangent, K-flow
intersection, absolute determinant line, or nonlinear manifold is present.

## 5. Stabilizer and basis mutations

Multiplying both stabilizers by `0.5` or `2` preserves all five complete
forward/reverse paths, the `(5-,4+)` inertia, and the common m=5 endpoints.

| stabilizer scale | max distance to nominal m=5 endpoint | max reverse distance to embedded m=4 root |
|---:|---:|---:|
| `0.5` | `3.823e-12` | `1.632e-12` |
| `2` | `4.451e-12` | `1.952e-12` |

Negating the added-`a` coordinate column changes the raw augmented-basis sign
from `+1` to `-1` and the inverse-transition sign from `+1` to `-1`; the
corrected sign remains `+1`.  The lifted action, gradient, and Hessian are
unchanged to the recorded precision.

Descriptively, the m=5 Hessian restricted to the two normalized complement
directions at the embedded zero-source m=4 root has eigenvalues approximately
`-1.34147e5` and `2.33804e4`.  This `(1-,1+)` observation is retained but was
not introduced after the freeze as a pass criterion.

## 6. Independent validation

An independent 80-digit `mpmath` backend evaluated the frozen SymPy m=5
gradient and Hessian at all five serialized λ=1 endpoints.  It reproduced
inertia `(5-,4+,0)` at every point.  The largest gradient component was
`2.361e-11`; the largest difference between the 80-digit and recorded
minimum absolute Hessian eigenvalues was `3.094e-11`.

This check changes no authoritative output.  It is an arithmetic/backend
cross-check of the committed JSON.

## 7. Interpretation and boundary

### Calculated facts

- One declared stabilized action bridge retains all five sampled real saddle
  branches on both meshes and in reverse.
- No sampled Hessian zero, inertia change, source-reflection failure, or
  frozen state-box exit occurs.
- Two positive metric paths and three action/metric orderings transport the
  same oriented local upward nine-plane at the m=5 endpoint.
- The endpoint and orientation results survive both declared stabilizer-scale
  mutations and the added-basis sign mutation.

### Scoped inference

These controls support the existence of one numerically stable, explicitly
constructed local route from the retained m=4 saddle family to m=5 saddles.
They also supply a concrete common-ambient orientation convention for the next
local intersection calculation.

They do not establish regulator independence.  The action bridge contains an
artificial holomorphic stabilizer, λ is sampled rather than enclosed by a
formal no-zero theorem, and the metric calculation transports only tangent
planes.  Other stabilizations, action paths, or unsampled events remain open.

### Still open

- Continue an actual frozen m=5 Gamma–K candidate over this action/metric
  bridge and re-run the full residual, transversality, path, and tangent
  controls in `R18`.
- Search straight arms and cap reintersections, exhaust saddles and upward
  components, and classify Stokes data and all relative good ends.
- Specify and transport a physical original joint relative cycle and its
  BFV/Pfaffian/Pin orientation before emitting any global integer.
- The Phase-49 formal endpoint-error transport and portable-flow-adapter debt
  remains a separate local numerical follow-up.

Accordingly,

```text
bounded_chain_signed_sum                  = null
complete_global_signed_intersection_vector = null
global_n_sigma                            = null
cutoff_limit                              = null
continuum_limit                           = null
physical_original_cycle                   = null
global_promotion                          = PROHIBITED
Gate 1                                    = OPEN_PARTIAL_PROGRESS
```

## Bottom line

Phase 50 crosses the next finite-cutoff construction boundary: the five
retained m=4 joint saddles and their local oriented upward tangent planes can
be carried to m=5 on the frozen stabilized action/SPD-metric paths without a
sampled degeneracy.  That is a useful local workbench result, not the global
cycle, cutoff limit, or physical conclusion that Gate 1 still requires.
