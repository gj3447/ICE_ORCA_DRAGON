# Gate 1 — Starobinsky \(m=2\) midpoint fixed-time HJ identity audit

## Outcome

The bounded one-shot result is

```text
KILL_FROZEN_MIDPOINT_AS_EXACT_FIXED_TIME_HJ_ELEMENT
```

The sealed frozen midpoint formula is not pointwise equal to the exact
fixed-time Euclidean Hamilton principal function of the declared
Hamiltonian.  On the equal-endpoint diagonal its Hamilton--Jacobi residual is
nonzero at both an exact algebraic Starobinsky witness and the frozen Phase-39
boundary witness.

This retires only
`FROZEN_MIDPOINT_AS_EXACT_FIXED_TIME_HJ_ELEMENT`.  It is not a no-go for a
different perfect or improved action, a lapse-extremized constrained principal
function, a controlled deformation of the midpoint formula, or a BFV source.
Gate 1 remains `OPEN_PARTIAL_PROGRESS`.

## 1. Frozen fixed-time candidate

Use the Euclidean configuration action

```math
I_E=2\pi^2\int d\tau\left[
\frac12G_{AB}(q)\dot q^A\dot q^B+U(q)
\right],
```

with

```math
q=(a,\phi),\qquad
G_{AB}=\mathrm{diag}(-6a,a^3),
```

```math
U(a,\phi)=-3a+a^3V(\phi),\qquad
V(\phi)=\frac34\left(1-e^{-\sqrt{2/3}\,\phi}\right)^2.
```

The resulting fixed-time Hamiltonian is

```math
H_E=
-\frac{p_a^2}{24\pi^2a}
+\frac{p_\phi^2}{4\pi^2a^3}
+6\pi^2a-2\pi^2a^3V(\phi).
```

For endpoints \(q_0,q_1\), duration \(t\), midpoint
\(q_m=(q_0+q_1)/2\), and increment \(\Delta q=q_1-q_0\), the tested element is

```math
S_{\mathrm{mid}}(q_0,q_1;t)
=2\pi^2\left[
\frac{G_{AB}(q_m)\Delta q^A\Delta q^B}{2t}
+tU(q_m)
\right].
```

Setting \(t=T/2\) and taking two algebraic copies with the same full endpoint
increment reconstructs the frozen equal-endpoint \(m=2\) convention exactly:

```math
2S_{\mathrm{mid}}\big|_{t=T/2}
=\frac{4\pi^2K}{T}+2\pi^2TU=S_2.
```

This is an algebraic two-copy factorization.  It is not a constructed
sequential continuum trajectory, composition law, or phase-space lift.

## 2. Exact diagonal discriminator

An exact fixed-time principal function for the displayed Hamiltonian must obey

```math
\partial_tW(q_0,q_1;t)
+H_E\!\left(q_1,\partial_{q_1}W\right)=0.
```

On the diagonal \(q_0=q_1=q\), exact differentiation of the midpoint element
gives

```math
\partial_tS_{\mathrm{mid}}=2\pi^2U,
\qquad
\partial_{q_1^A}S_{\mathrm{mid}}=\pi^2tU_A.
```

Therefore

```math
R_{\mathrm{HJ}}
:=\partial_tS_{\mathrm{mid}}
+H_E\!\left(q_1,\partial_{q_1}S_{\mathrm{mid}}\right)
=\frac{\pi^2t^2}{4}D(a,\phi),
```

where

```math
D(a,\phi)=G^{AB}U_AU_B
=-\frac{U_a^2}{6a}+\frac{U_\phi^2}{a^3}.
```

One admissible point with \(R_{\mathrm{HJ}}\ne0\) is enough to contradict
only the declared pointwise equality map.

### Exact witness

At

```math
a=2,\qquad
\phi=\sqrt{\frac32}\log2,\qquad
t=\frac12,
```

the symbolic audit obtains

```math
V=\frac3{16},\qquad
U_a=-\frac34,\qquad
U_\phi=\sqrt6,
```

```math
D=\frac{45}{64},
\qquad
R_{\mathrm{HJ}}=\frac{45\pi^2}{1024}>0.
```

### Frozen-boundary certificate

The second witness uses the exact decimal boundary values

```math
a=3.5668031935672753,qquad
\phi=1.0185809464006637,qquad
t=\frac25.
```

At 300-bit precision, python-flint/Arb outward-rounded ball arithmetic
certifies

| quantity | enclosing midpoint | certified sign |
|---|---:|:---:|
| \(D\) | \(2.358628592398597038799101768790179109\ldots\) | positive |
| \(R_{\mathrm{HJ}}\) | \(0.931149245442895690948698433641264018\ldots\) | positive |

The direct endpoint-Hamiltonian evaluation and the reduced residual formula
differ by a ball of radius about \(3.86\times10^{-87}\) containing zero.  The
raw result preserves the complete lower and upper bounds.

### Sign and normalization control

For constant \(G=1\) and constant \(U_0\),

```math
S_{\mathrm{flat}}
=\frac{\pi^2(q_1-q_0)^2}{t}+2\pi^2tU_0,
\qquad
H_{\mathrm{flat}}=\frac{p^2}{4\pi^2}-2\pi^2U_0,
```

the same symbolic pipeline returns an exactly zero HJ residual.  This checks
the signs and normalization without supplying evidence for the Starobinsky
candidate.

## 3. Deformation hint, not a construction

The audit records the formal off-diagonal ansatz

```math
\Delta S(q_0,q_1;t)
=-\frac{\pi^2t^3}{12}D(q_m).
```

On the diagonal, its explicit time derivative cancels the displayed
order-\(t^2\) defect.  Its endpoint contribution is

```math
\partial_{q_1^A}\Delta S
=-\frac{\pi^2t^3}{24}\partial_AD,
```

so the first cross contribution with the order-\(t\) base momentum enters the
Hamiltonian at order \(t^4\).  No off-diagonal HJ residual, neighborhood,
uniform remainder, convergence, equality, or source-deformation bound was
proved.  Its status is therefore only
`LEADING_DIAGONAL_COUNTERTERM_CANDIDATE_NO_UNIFORM_BOUND`.

## 4. What changed in the construction sequence

| Requested construction | Status after this audit |
|---|---|
| Named chain/end model and joint \(m=2\) action | The frozen bosonic action and hypotheses-open relative-chain type remain recorded; no production chain is admitted. |
| Replacement-gauge FP/BFV source | The direct \(V=0\) transplant, naive two-local-lapse unfixing, and frozen-midpoint fixed-time-HJ equality map are retired in separate scopes. No replacement source exists yet. |
| Source and limit order including \(N=0\) | Still blocked by the missing same-model first-order source and controlled map. |
| \(U_1/U'_1\), overlaps, basis and orientation | Not constructed or tested. |
| End/divisor census and candidate completeness | Not constructed or tested. |
| Lateral verdict | `UNIQUE_LATERAL`, `STOKES_SPLIT`, and `NO_ADMISSIBLE_LIFT` remain unevaluated. |
| Independent review and preregistration | Three post-run AI audits passed. Human mathematical sign-off and independent custody are absent, so preregistration remains closed. |

Missing values remain null, not zero.  In particular, no first-order
constraint lattice, local branch or flow, composition law, internal-vertex
gauge-null mode, BFV charge or gauge fermion, endpoint state, \(N=0\)
prescription, atlas, orientation, end census, relative cycle, global signed
intersection vector, physics result, or TOE result was constructed or
rejected.

## 5. Outcome-bound route change

- Unexpected outcome: the frozen formula reconstructs the existing \(m=2\)
  convention exactly but fails its proposed exact fixed-time HJ identity at
  two independently checked diagonal witnesses.
- Retired mechanism:
  `FROZEN_MIDPOINT_AS_EXACT_FIXED_TIME_HJ_ELEMENT`, in this exact scope only.
- Live competitors: `CONTROLLED_HJ_DEFORMATION_OR_PERFECT_ACTION`,
  `CONTINUUM_FIRST_CONSTRAINED_PRINCIPAL_FUNCTION`, and
  `STAROBINSKY_CONSTRAINT_ADAPTED_IMPROVED_STATIC_SOURCE`.
- Next discriminating question: for one named Starobinsky continuum branch,
  can a local constrained principal function be constructed with an exact
  composition law, one internal-vertex gauge-null mode, and a controlled
  projection or deformation bound to the frozen kernel?
- Changed selection: do not derive BFV data from the frozen midpoint formula
  by equality.  First construct that local continuum/HJ object or a controlled
  deformation.

The next question asserts no existence result and grants no automatic
execution authority.

## 6. Execution and independent review

- Planner checkpoint: `research-agent:81450cde454365a52f6a`
- Input/runner commit before execution:
  `6ed8ce69e50adace61f2fe673dc20647bac256a9`
- Command executed exactly once:
  `./ice run gate1_m2_starobinsky_midpoint_hj_identity_audit`
- Result: `VALID_RUN`; 16/16 exact checks, 4/4 Arb certificates, and 5/5
  theorem/scope guards
- Input SHA-256:
  `6c2ab273fd8d3c95e4b85337cf7f55c84eb961117c3db5982d65a260e4ba0696`
- Runner SHA-256:
  `287c142e1221ec8289f73be7e7054044773e47d6096c769c514db91f53c658ae`
- Raw-result SHA-256:
  `8defcaaccc03dc88251758815003592016b4b4cedb538d5426289c97f4d99325`
- Canonical payload SHA-256 excluding its self field:
  `7eca45eb80add06c27eef2578049e657bba2f106dd5f5b10b1f2b42f341d0550`
- Root calls, ODE calls, numerical samples, and automatic descendants: zero

Three post-run read-only audits independently checked the exact derivation,
recomputed both witnesses, verified the raw and canonical hashes, inspected
the Arb lower bounds, and reviewed the source and claim ceilings.  They found
no blocker.  This is independent AI review, not human mathematical review or
independent custody.

## Primary sources and artifacts

- [Raw result](GATE1_M2_STAROBINSKY_MIDPOINT_HJ_IDENTITY_AUDIT_RESULT.json)
- [Input manifest](GATE1_M2_STAROBINSKY_MIDPOINT_HJ_IDENTITY_AUDIT_INPUTS.json)
- [Bounded runner](gate1_m2_starobinsky_midpoint_hj_identity_audit.py)
- [Bahr, Dittrich, and Steinhaus, *Perfect discretization of reparametrization invariant path integrals*, arXiv:1101.4775v1](https://arxiv.org/abs/1101.4775v1)
- [Dittrich and Höhn, *Constraint analysis for variational discrete systems*, arXiv:1303.4294v3](https://arxiv.org/abs/1303.4294v3)
- [Dittrich, *From the discrete to the continuous: Towards a cylindrically consistent dynamics*, arXiv:1205.6127v1](https://arxiv.org/abs/1205.6127v1)
- [Johansson, *Arb: efficient arbitrary-precision midpoint-radius interval arithmetic*, arXiv:1611.02831v1](https://arxiv.org/abs/1611.02831v1)

The papers motivate the distinctions among ordinary discretization,
perfect/HJ constructions, and certified arithmetic.  None supplies this
Starobinsky residual, a replacement perfect action, or a BFV source.
