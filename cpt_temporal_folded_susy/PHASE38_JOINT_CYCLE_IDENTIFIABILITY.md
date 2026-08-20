# Phase 38 — Gate-1 joint-cycle identifiability and bounded end ledger

## Result

Phase 38 starts the first item of the ordered five-gate programme:

> transport one original joint lapse--field relative cycle through the fold,
> classify all signed intersections, and fix the global contour vector.

The gate is **not closed**. The calculation establishes the information still
needed to close it, fixes the correct conditional local cycle law, and extends
the bounded numerical census.

The strongest exact conclusion is

\[
\boxed{
\text{the recorded projected crossing and local root data do not establish}
\quad
\Gamma_{\rm original}^{\rm joint}\text{ or }n_\sigma .
}
\]

Phase 38 does not prove that the physical projection map on gravitational
relative homology is noninjective. Instead, a declared finite surrogate shows
why inverse reconstruction is not licensed without either:

1. an injectivity theorem for the actual physical projection; or
2. explicit admissible joint-cycle completions.

The exact local cycle law inherited from Phase 36 is

\[
\boldsymbol\Gamma_{\rm in}=G\boldsymbol\Gamma_{\rm out},
\qquad
G=\begin{pmatrix}-1&-1\\0&1\end{pmatrix},
\]

so coefficients and dual bases transform as

\[
\boxed{c_{\rm out}=G^T c_{\rm in}},
\qquad
\boxed{\boldsymbol K_{\rm in}=G^{-T}\boldsymbol K_{\rm out}}.
\]

This map must not be replaced by the root permutation

\[
P=\begin{pmatrix}0&1\\1&0\end{pmatrix}.
\]

For the explicitly conditional input \(c_{\rm in}=(1,0)^T\), which would mean
that a separately derived original cycle equals the declared local
\(\Gamma_0\), the correct cycle map gives

\[
G^T\binom10=\binom{-1}{-1}.
\]

This is a representation in the declared local cycle basis, not a computed
physical thimble vector or global intersection coefficient. The forbidden
root-swap substitution would instead give \((0,1)^T\), fabricating a
single-arm answer.

Numerically, the known upper/lower reflection-symmetric stationary-family
arms have been extended from the Phase-34 bound

\[
\operatorname{Re}T=13
\]

to

\[
\operatorname{Re}T=16.
\]

Two continuation step sizes reach the same endpoint root/basin to

\[
3.65\times10^{-14}
\]

in the five nonlinear unknowns. This is a continuation-seed control, not an
integration-mesh convergence theorem. No sampled endpoint-Jacobi zero or
sampled projected crossing with the Phase-32 full-line candidate's
imaginary-\(T\) lapse base appears on this bounded extension.

The two endpoints at \(\operatorname{Re}T=16\) are only numerical box exits,
not classified relative good ends. The origin-side arm likewise approaches
the singular \(N=T=0\) endpoint. The result API therefore returns

```json
{
  "full_joint_local_sign": null,
  "complete_global_signed_vector": null,
  "global_n_sigma": null
}
```

The executable passes **15 exact and 6 numerical checks**.

## 1. What Gate 1 actually asks for

The coefficient of a saddle is not an intersection of two curves after both
have been projected onto the lapse plane. It is an oriented intersection of
middle-dimensional relative cycles in the full gauge-fixed integration space:

\[
n_\sigma
=\left\langle
\Gamma_{\rm original}^{\rm joint},K_\sigma
\right\rangle
=\sum_{x\in\Gamma_{\rm original}^{\rm joint}\cap K_\sigma}
\operatorname{sgn}
\det_{\mathbb R}
\begin{bmatrix}
V_\Gamma(x)&V_K(x)
\end{bmatrix}.
\]

The completion object must include at least:

- the lapse contour and its orientation;
- the original field/momentum history cycle and endpoint polarization;
- a gauge/BFV embedding and orientation line;
- the singular divisor, regulator, and relative good-end condition;
- a non-Stokes chamber or specified \(i\epsilon\) lateral limit;
- every relevant saddle, sheet, upward component, crossing, and Stokes jump.

Phase 32 supplied the projection of an independently declared below-origin
full-line candidate and a locally decaying principal momentum lift around its
regulated bypass. It explicitly left field-history matching and the full BFV
orientation open. Phases 34--37 supplied bounded stationary roots, local cycle
algebra, and root/determinant local systems. None supplied the missing complete
joint cycle.

The distinction matters. A lapse projection can only determine a joint cycle
if the physical projection is proved injective on the admissible class. No
such theorem or explicit enumeration has yet been supplied.

## 2. Exact finite surrogate

Phase 38 encodes a small type-level warning. Use surrogate coordinates

\[
j=(\ell,c_U,c_L)^T,
\]

where \(\ell\) is the recorded lapse coordinate and \(c_U,c_L\) label two
otherwise unrecorded slots. The surrogate projection is

\[
\pi=\begin{pmatrix}1&0&0\end{pmatrix}.
\]

It has

\[
\operatorname{rank}\pi=1,
\qquad
\operatorname{nullity}\pi=2.
\]

In particular,

\[
\pi(1,1,0)^T=1,
\qquad
\pi(1,0,1)^T=1,
\]

although the two surrogate labels are distinct.

This is exact algebra inside the declared finite surrogate. It is **not** a
construction of two admissible gravitational cycles, a computation of the
physical projection map, or a determination of the physical
relative-homology rank. Its legitimate role is narrower: it catches any code
or prose that tries to invert an information-losing record without first
proving that the physical problem has no omitted fiber directions.

The orientation ledger has the same open slots. Schematically,

\[
\epsilon_{\rm joint}
=\epsilon_T\epsilon_{\mathrm{omitted\ cycle}}.
\]

Phase 32 fixed \(\epsilon_T=+1\) under its declared coordinate orientations.
Until the omitted full-cycle tangent and orientation are constructed, either
full-joint local sign remains
compatible with the record:

\[
\epsilon_{\rm joint}\in\{-1,+1\}.
\]

This does not say that the physical sign is arbitrary. It says the current
evidence has not defined enough oriented structure to calculate it.
No fermion Pfaffian phase is multiplied into this Picard--Lefschetz integer;
that separate saddle-weight line belongs to Gate 3.

## 3. Cycle map, dual map, and the root-swap mutation

In the Phase-36 Airy chart the three oriented decay-ray cycles satisfy

\[
\Gamma_0+\Gamma_L+\Gamma_U=0.
\]

For the clockwise ordered bases,

\[
(\Gamma_0,\Gamma_L)_{\rm in}
=G(\Gamma_U,\Gamma_L)_{\rm out},
\qquad
G=\begin{pmatrix}-1&-1\\0&1\end{pmatrix}.
\]

If a chain is represented by coefficients \(c_{\rm in}\) before the basis
change and \(c_{\rm out}\) after it, equality of the chain gives

\[
c_{\rm out}=G^Tc_{\rm in}.
\]

Thus

\[
\binom{c_U}{c_L}_{\rm out}
=
\binom{-c_0}{-c_0+c_L}_{\rm in}.
\]

The dual basis transforms by the inverse transpose,

\[
G^{-T}
=\begin{pmatrix}-1&0\\-1&1\end{pmatrix},
\qquad
G\left(G^{-T}\right)^T=I,
\]

which preserves the declared row-basis cycle--dual pairing.

The Phase-37 root permutation \(P\) happens to be conjugate to \(G\) as an
abstract \(2\times2\) matrix. That does not make the objects interchangeable:

```text
P : local BVP root fiber -> local BVP root fiber
G : ordered relative-cycle basis -> ordered relative-cycle basis
```

The mutation test substitutes \(P\) for \(G^T\). It fails on the conditional
\(\Gamma_0\) input by changing a two-component local cycle representation
into a one-component representation. This kills a specific type error; it is
not a refutation of every temporal-fold or temporal-SUSY hypothesis.

## 4. What the local arm vector would fix

For arm integrals \(J_U,J_L\), the exact Phase-36 convention gives

\[
\begin{pmatrix}J_U\\J_L\end{pmatrix}
=\frac12
\begin{pmatrix}-1&-i\\-1&i\end{pmatrix}
\begin{pmatrix}\operatorname{Ai}\\\operatorname{Bi}\end{pmatrix}.
\]

Therefore an eventual Gate-1 arm vector obeys

\[
c_UJ_U+c_LJ_L
=-\frac{c_U+c_L}{2}\operatorname{Ai}
+\frac{i(c_L-c_U)}{2}\operatorname{Bi}.
\]

This is a cycle/Stokes combination. It does not compute the regular hard
even/odd functions multiplying \(\operatorname{Ai}\) and
\(\operatorname{Ai}'\) in the CFU uniform kernel.

The executable's finite output-schema check simply records that the Gate-1
payload has arm slots but no hard-CFU slots. It is bookkeeping, not a theorem
that the physical hard functions are mathematically independent. Those hard
functions may be computed conditionally in parallel. What must wait for both
gates is promotion to one selected physical uniform kernel.

## 5. Numerical real-dual ledger

The inherited connected saddle is

\[
T_*=0.7,
\qquad
W_*=1.40669054283425,
\]

with the Phase-25 boundary

\[
q_\partial
=(3.56680319356728,1.01858094640066;
  3.56680319356728,1.01858094640066).
\]

Seven regulated origin-side points cover

\[
0.0015625\le T\le0.1.
\]

They all have \(W_T>0\) and

\[
\frac{\sigma_{\min}(B_v)}{T}>0.9995.
\]

Six bridge points then cover \(0.2\le T\le0.7\). Their \(W_T\) decreases to

\[
W_T(0.7)=7.03\times10^{-14},
\]

consistent with the recorded joint lapse saddle. Forty-seven post-saddle
points continue from \(T\simeq0.893\) to

\[
T_c-2\times10^{-4}
=9.78842556808124,
\]

and all have \(W_T<0\). This stitches the sampled **reduced stationary
family** on both sides of \(T_*\). It does not integrate the full joint
gradient-flow manifold.

## 6. Bounded outgoing extension

The Phase-34 upper complex arm was re-solved from its last recorded point at

\[
T=13+2.89138959974i
\]

using steps \(0.25\) and \(0.125\) in \(\operatorname{Re}T\). Both seed chains
reach the same endpoint root/basin at \(\operatorname{Re}T=16\) within

\[
3.65\times10^{-14}.
\]

Three new sampled checkpoints are:

| \(\operatorname{Re}T\) | \(\operatorname{Im}T\) | \(\sigma_{\min}(B_v)\) | independently reintegrated full-endpoint residual |
|---:|---:|---:|---:|
| 14 | 4.06177474506 | 8.30017 | \(2.43\times10^{-7}\) |
| 15 | 5.25529902765 | 9.55216 | \(3.32\times10^{-7}\) |
| 16 | 6.45658625611 | 10.81266 | \(5.39\times10^{-7}\) |

Real coefficients permit a conjugation control with opposite imaginary
parts. This is a symmetry construction and reintegration check, not an
independently discovered lower branch. The largest nonlinear root residual
on either continuation step sequence is

\[
4.40\times10^{-9}.
\]

The independent full integration becomes more ill-conditioned along this
extension: its endpoint residual grows from the Phase-34 \(10^{-9}\) scale to
the displayed \(10^{-7}\) scale. Phase 38 therefore stops at 16 and records
the surface as a numerical box boundary. It does not extrapolate the branch
to infinity or infer its asymptotic end from the apparent trend.

At the three new checkpoints and inherited bounded records,

\[
\operatorname{Re}T>T_c,
\qquad |T|>9.
\]

Their sampled lapse projections therefore do not cross the Phase-32
full-line candidate's imaginary-\(T\) base or its origin caps with
\(r\le0.1\). This is not a continuous no-crossing theorem, a census of other
sheets, or a statement about the full joint cycles.

## 7. End ledger and fail-closed integer

The known components currently end as follows:

| component | current status | why it is not closed |
|---|---|---|
| origin-side real arm | `SINGULAR_ENDPOINT_UNRESOLVED` | the regulated crossing approaches \(N=T=0\) |
| upper outgoing arm | `BOX_EXIT_UNRESOLVED` | calculation stops at \(\operatorname{Re}T=16\) |
| conjugate outgoing control | `BOX_EXIT_UNRESOLVED` | calculation stops at the same box |

A box boundary is not an asymptotic decay sector. A tracked BVP branch is not
automatically a complete upward thimble. A root sheet is not automatically a
relative cycle.

The executable therefore implements a hard output guard:

```text
if original joint cycle is incomplete
or any upward end is unclassified
or the bosonic/gauge-reduced cycle orientation is unfixed:
    global_n_sigma = null
```

These three booleans are necessary API guards, not a theorem that they are
sufficient for a physical Picard--Lefschetz coefficient. Completeness,
transversality, Stokes control, and regulator/cutoff stability would still
need independent evidence.

For the same reason, the positive lapse half-line endpoint contact remains
`null`; the code does not assign it \(0\), \(1/2\), or \(+1\).

## 8. Relation to the finite BFV result

Phase 31 found that the nonzero-mode bosonic gauge-pair determinant sign is

\[
(-1)^{m-1}
\]

at segment cutoff \(m\). On the recorded cutoffs

\[
m=(5,9,10,11,20,40)
\]

this gives

\[
(+,+,-,+,-,-).
\]

That cutoff-parity alternation is reproduced exactly as a guard. It shows why
a finite bosonic block cannot be borrowed as the missing absolute continuum
orientation. The relative boson/ghost cancellation of Phase 31 and an
oriented full BFV/Pfaffian line are different claims.

## 9. What was learned conceptually

Gate 1 is not mainly a problem of tracing one preferred trajectory. It is a
problem of closing a global accounting system.

A trajectory says where one stationary solution can be continued. A relative
cycle says which complete family of histories defines the integral, how it
ends, how it is oriented, and how it pairs with every relevant dual. The
latter includes counterfactual structure: arms that can cancel, crossings
that can appear in \(+/-\) pairs, and sheets that may contribute even when
they are not the branch first followed.

Local continuity is real information, but global amplitude is relational
information. The physical invariant is not the name of one sheet or the
visual persistence of one branch. It is the completed pairing that survives
relabeling, orientation bookkeeping, homotopy, Stokes continuation, and
regulator changes.

The present negative result is therefore productive:

\[
\boxed{
\text{root holonomy cannot substitute for an uncomputed original cycle.}
}
\]

## 10. Gate status after Phase 38

| Gate | promotion status | present typed output |
|---|---|---|
| 1. original joint cycle and global intersections | `OPEN_PARTIAL_PROGRESS` | finite inverse-reconstruction warning, conditional local cycle law, bounded end ledger |
| 2. hard CFU coefficients | `PHYSICAL_PROMOTION_DEPENDS_ON_GATE_1` | hard data may be explored conditionally; no selected kernel |
| 3. full BFV/Pfaffian/Pin line | `PHYSICAL_PROMOTION_DEPENDS_ON_GATE_2` | not computed |
| 4. spinorial charge/common domain | `PHYSICAL_PROMOTION_DEPENDS_ON_GATE_3` | not computed |
| 5. persistent order/pole splitting | `PHYSICAL_PROMOTION_DEPENDS_ON_GATE_4` | not computed |

The dependencies regulate claim promotion, not exploratory computation.

## 11. Next calculation

The next Gate-1 implementation should no longer continue only continuum BVP
roots. It should:

1. define one explicit finite-cutoff holomorphic joint action in field and
   lapse variables;
2. solve its exact discrete joint critical point rather than sample the
   continuum saddle;
3. locate its discrete fiber fold;
4. embed separately declared lower- and upper-bypass original field--lapse
   candidates, including orientations, \(i\epsilon\) chamber, and regulated
   boundary caps;
5. start the upward cycle from the joint Hessian/Takagi frame and transport
   its full tangent frame;
6. solve for isolated full-space intersections and compute
   \(\operatorname{sgn}\det_{\mathbb R}[V_\Gamma,V_K]\);
7. classify every encountered boundary as `GOOD_END`, `BAD_SINGULARITY`,
   `NEW_FOLD`, or `BOX_EXIT_UNRESOLVED`;
8. keep the global integer null until completeness and regulator/cutoff
   stability are demonstrated.

Gate 2 may compute hard CFU data in parallel. A physical uniform kernel
requires both the Gate-1 cycle vector and Gate-2 analytic-amplitude data.

## 12. Reproduction

From the repository root:

```bash
uv run --locked python3 \
  cpt_temporal_folded_susy/phase38_joint_cycle_identifiability.py
```

The program prints every exact and numerical check and ends with a single
machine-readable `PHASE38_RESULT=...` payload. It writes no files and uses no
target intersection sign, initial-value peak, or SUSY scale as input.

## References and scope

- [Witten](https://arxiv.org/abs/1001.2933) supplies the relative-cycle and
  Picard--Lefschetz framework. It does not supply this repository's original
  gravitational cycle, intersections, or good-end census.
- [Chester--Friedman--Ursell](https://doi.org/10.1017/S0305004100032655)
  supplies the coalescing-saddle uniform-asymptotic framework. It does not
  determine the hard coefficients or select this model's cycle.
- [Teitelboim](https://doi.org/10.1103/PhysRevLett.50.705) frames the
  causal-positive-time versus gauge-invariant lapse distinction.
- [Banihashemi--Jacobson](https://doi.org/10.1103/PhysRevD.111.066014)
  analyzes a below-origin lapse prescription for its stated integration
  order. It does not choose that class by CPT/Pin or compute the joint
  field--lapse coefficient used here.

All new numerical statements above are repository calculations. The cited
works frame the mathematical boundary; they do not evidence the Phase-38
numbers or close Gate 1.
