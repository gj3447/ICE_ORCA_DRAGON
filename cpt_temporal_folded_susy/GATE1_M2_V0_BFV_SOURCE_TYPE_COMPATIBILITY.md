# Gate-1 Starobinsky \(m=2\) / \(V=0\) BFV source-type compatibility audit

## Outcome

The bounded result is

```text
KILL_DIRECT_V0_BFV_TO_STAROBINSKY_M2_SOURCE_IDENTIFICATION
```

This is a scoped negative result.  The existing local \(V=0\),
\(U_+\) improved-static BFV zero-mode algebra does **not** inhabit the source
type of the frozen Starobinsky finite-\(m=2\) joint action.  It therefore cannot
be relabelled or directly transplanted as the missing Gate-1 source.

The result does not kill either valid object in its own scope.  It keeps the
local \(V=0\) BFV algebra and the Starobinsky bosonic \(m=2\) action, and it
does not rule out a newly derived Starobinsky-compatible BFV source.

## Exact target action

For the two-element midpoint model, set

```math
A=a_b+\frac{x}{2},\qquad
\Phi=\phi_b+\frac{q}{2},\qquad
V(\Phi)=\frac{3}{4}\left(1-e^{-\sqrt{2/3}\,\Phi}\right)^2 .
```

The named frozen bosonic target is

```math
S_2(x,q,T_{\mathrm{prop}})
=-\frac{24\pi^2 A x^2}{T_{\mathrm{prop}}}
+\frac{4\pi^2 A^3q^2}{T_{\mathrm{prop}}}
+2\pi^2T_{\mathrm{prop}}\left[-3A+A^3V(\Phi)\right]
```

on

```math
X_2=\mathbb C_{a_1}\times\mathbb C_{\phi_1}\times
\mathbb C_{T_{\mathrm{prop}}}^{\ast}.
```

The independently reconstructed canonical form uses

```math
\mu_g=12\pi^2A,\qquad \mu_s=2\pi^2A^3,
```

```math
I_2=x(p_{a,0}-p_{a,1})+q(p_{\phi,0}-p_{\phi,1})
+\frac{z(p_{a,0}^2+p_{a,1}^2)}{4\mu_g}
-\frac{z(p_{\phi,0}^2+p_{\phi,1}^2)}{4\mu_s}
-zU(A,\Phi),
```

where \(U=2\pi^2[-3A+A^3V(\Phi)]\).  Stationary momentum elimination gives

```math
I_2^\star=-\frac{2\mu_gx^2}{z}+\frac{2\mu_sq^2}{z}-zU,
\qquad T_{\mathrm{prop}}=iz,
```

and the exact audit verifies \(iI_2^\star=-S_2\) in the declared Wick
convention.  This fixes the bosonic target; it is not yet a full FP/BFV source
or measure.

## Why the direct BFV transplant fails

With \(P=ap_a/2\), the two constraints differ by a bulk term:

```math
C_{\mathrm{Star}}-C_{V=0}=2\pi^2a^3V(\phi).
```

For the Starobinsky model,

```math
\{p_\phi,C_{\mathrm{Star}}\}
=-\partial_\phi C_{\mathrm{Star}}
=-2\pi^2a^3V'(\phi),
```

so the old \(p_\phi\) is not conserved and cannot be used as the cyclic
\(V=0\) invariant without a new Starobinsky canonical transformation.  The
constraint-root correction is

```math
F_{\mathrm{Star}}-F_{V=0}=-24\pi^4a^6V(\phi),
```

and the finite-action correction is

```math
S_{2,\mathrm{Star}}-S_{2,V=0}
=2\pi^2T_{\mathrm{prop}}A^3V(\Phi).
```

The last expression depends on the interior variable \(q\) and on
\(T_{\mathrm{prop}}\); it is not a fixed-endpoint constant.

The source-type comparison is therefore:

| Field | Frozen Starobinsky \(m=2\) target | Existing improved-static BFV object | Verdict |
|---|---|---|---|
| Model | \(V(\phi)\ne0\) | \(V=0\) | mismatch |
| Bulk action | includes \(2\pi^2T_{\mathrm{prop}}A^3V(\Phi)\) | absent | mismatch |
| Scalar momentum | old \(p_\phi\) is nonconserved | cyclic \(V=0\) invariant | new transform required |
| Time/lapse objects | proper-time modulus \(T_{\mathrm{prop}}\) | Darboux clock \(T_{\mathrm{clock}}\), plus BFV multiplier \(N\) | distinct types |
| Endpoint polarization | fixed old \((a,\phi)\) | endpoint-improved \((T_{\mathrm{clock}},\Phi)\) | no exact transform supplied |
| Finite \(m=2\) BFV lattice | required | absent | missing |
| Source equality/deformation | required | unproved | missing |
| Absolute determinant/Pfaffian line | required | unproved | missing |

The reported `mismatch_witness_count=7` counts values beginning with
`MISMATCH` plus values exactly equal to `MISSING`.  The separately typed
`MISSING_IN_CANDIDATE_SOURCE` finite-lattice field is an eighth compatibility
field, not a hidden positive result.

The positive-real-\(\phi\) theorem guard in the raw result is conditional on
the frozen endpoint or a positive-real neighborhood.  No complex source
corridor is inferred from it.  The symbolic bulk mismatch itself does not
depend on claiming such a corridor.

## Named chain theory and end model

The working chain **type** is the Pham--Witten relative singular-chain lane,
not a completed production chain:

```math
h=\mathrm{Re}(S_2/\hbar),\qquad
X_{\mathrm{good},M}=\{x\in X_2\mid h(x)\ge M\},
```

```math
\mathrm{RC}_{M,3}
=C_3\!\left(X_2,X_{\mathrm{good},M};
\mathbb Z\otimes\mathcal L_{G1}\right).
```

Its status is

```text
SELECTED_TYPE_HYPOTHESES_OPEN
```

Here \(M\) is a regulator, degree three is the bosonic complex dimension, and
\(\mathcal L_{G1}\) is a placeholder for one common source/chain/FP-BFV
orientation local system.  The notation does not assert that the source
relative class, tameness, a finite Morse basis, regulator stability, or the
orientation line exists.

The Hien rapid-decay lane remains an alternative, not a rejected theorem.  It
cannot be instantiated until a suitable meromorphic connection, compactification
with controlled divisor, real-oriented blow-up, directional decay condition,
and comparison to the source coefficient line are supplied.  Witten's
Picard--Lefschetz framework and Hien's rapid-decay homology provide mathematical
frameworks only; neither source selects the ICE cycle or its integer.

## Required construction order

The audit changes the execution order because every later object must live in
one common source type.

| Requested construction | Current exact status | Admission condition |
|---|---|---|
| Named chain/end model and exact joint \(m=2\) action | bosonic action fixed; relative singular-chain type selected conditionally | same-model BFV source plus chain hypotheses |
| Replacement-gauge FP/BFV source | direct \(V=0\) transplant retired | derive or falsify one Starobinsky constraint-adapted or time-dependent source |
| Source and limit order through \(N=0\) | open | first distinguish BFV multiplier \(N=0\) from the excluded proper-time pole \(T_{\mathrm{prop}}=0\), then prove the regulated distributional order |
| \(U_1/U'_1\), overlaps, orientation transport | open | common \(X_{\mathrm{gf}}\), source equality/deformation and \(\mathcal L_{G1}\) |
| End/divisor census and candidate completeness | partial end records only | all-end/divisor/Stokes census and either a tame Morse basis or a proved finite chain complex/quasi-isomorphism |
| `UNIQUE_LATERAL` / `STOKES_SPLIT` / `NO_ADMISSIBLE_LIFT` | unevaluated | all preceding typed inputs and independent mathematical review |

No zero-lapse, cover, orientation, census, or final trichotomy field is filled
with zero.  They remain null.

## Outcome-bound research transition

- Unexpected outcome: the most developed replacement source is locally valid
  for \(V=0\), but is the wrong type for the Starobinsky finite-\(m=2\)
  target.
- Competing mechanisms: `DIRECT_V0_TRANSPLANT` is retired only in the exact
  cross-scope-identification lane; `STAROBINSKY_CONSTRAINT_ADAPTED_IMPROVED_STATIC_SOURCE`
  and `STAROBINSKY_TIME_DEPENDENT_TRACE_SOURCE` remain live and unconstructed.
- Discriminating question: can one regular \(V(\phi)\ne0\) component derive
  its own endpoint-improved FP/BFV finite-\(m=2\) trajectory source and a typed
  comparison to the proper-time kernel?
- Changed future selection: construct or falsify that same-model replacement
  source before work on \(N=0\), \(U_1/U'_1\), the complete end census, or
  source-to-fold transport.

This is an invention-carrying candidate transition in the ICE workbench.  It
is not an HSWM learning admission, a Gate-1 closure, a physical state, a
quantum-gravity result, or a TOE claim.

## Execution and independent review

- Runner-definition commit: `e27e0f0017d93c6ff76e7ad10541c4db97a25b8a`
- Command: `./ice run gate1_m2_v0_bfv_source_type_compatibility`
- Result: `VALID_RUN`, 17/17 exact checks and 3/3 conditional theorem guards
- Raw result SHA-256: `38ae973ae85c380913cb038a6c495a7db78f331e9eec38bb2ab5e34f3d7c028e`
- Canonical payload SHA-256 excluding its self field:
  `5411e04686348f4f18fa5a3c8261955b317cfa9f4ac24f35ca229ce75285017d`
- Automatic descendants: zero

A separate read-only mathematical audit recomputed the file hashes and payload
digest and checked the constraint, Poisson-bracket, trace-bracket,
constraint-root, finite-action and canonical-pushforward identities.  It found
no verdict-blocking algebraic, sign, hash, or scope error.  This is independent
AI review of the recorded mathematics, not independent human custody or the
human mathematical sign-off required before preregistration.

## Sources and artifacts

- [Raw result](GATE1_M2_V0_BFV_SOURCE_TYPE_COMPATIBILITY_RESULT.json)
- [Input manifest](GATE1_M2_V0_BFV_SOURCE_TYPE_COMPATIBILITY_INPUTS.json)
- [Bounded runner](gate1_m2_v0_bfv_source_type_compatibility.py)
- [Witten, *Analytic Continuation Of Chern--Simons Theory*](https://arxiv.org/abs/1001.2933)
- [Hien, *Periods for flat algebraic connections*](https://arxiv.org/abs/0803.3463)
- [Matsubara-Heo, *On the rapid decay homology of F. Pham*](https://arxiv.org/abs/1705.06052)
