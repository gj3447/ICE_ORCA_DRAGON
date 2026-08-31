# Raw-\(C\) fixed-box nonreal endpoint interval certificate: blocker and design

## Decision

**Do not create or run an endpoint-certification runner yet.**  The repository
does contain the locked complex-ball arithmetic required to evaluate a WKB
datum outwardly (`python-flint==0.9.0`, `acb`), but it does not contain a
validated complex-tail theorem or a validated complex ODE transport routine
that turns that datum into an enclosure of the *actual* recessive solution.
Writing an `acb` WKB ball and attaching the real-axis error estimate to it
would therefore be a proxy relabelled as a certificate.

This is a narrow blocker for one prospective fixed box.  It makes no claim
about a singular Weyl--Titchmarsh function, a spectral measure, Stieltjes
inversion, a rigging map, RAQ, or a physical inner product.

## Reused material and exact point of failure

The existing
[`raw_c_plus_endpoint_liouville_green_tail_bound.py`](raw_c_plus_endpoint_liouville_green_tail_bound.py)
proves a real-tail Liouville--Green budget only after checking that
\(A(Q)\) is real and positive.  Its cited DLMF guard is explicitly scoped to
that hypothesis.  The existing
[`raw_c_nonreal_weyl_proxy.py`](raw_c_nonreal_weyl_proxy.py) uses a finite WKB
seed and adaptive double-precision integration, and calls itself a proxy for
exactly this reason.  The complex-ball use in the existing raw-\(C\) runners
is for elementary/Bessel/integral enclosures; it is not a validated complex
initial-value solver.

For a concrete next unit, fix

\[
p=0,\qquad Q_+=4,\qquad
 \operatorname{Re}z\in[-1/16,1/16],\quad
 \operatorname{Im}z\in[15/16,17/16].
\]

Then the fiber coefficient can be factored on \(Q\ge4\) as

\[
A(Q,z)=36\pi^4e^{2Q}(1+\delta(Q,z)),\qquad
\delta(Q,z)=\frac{z e^{-Q/2}}{6\pi^2}.
\]

An `acb` calculation can outwardly establish a strict bound
\( |\delta|\le\eta<1\) on this box, so the disc \(1+\delta\) excludes the
nonpositive real axis and the principal branch \(\sqrt A\) is well-defined
with positive real part.  It can also outwardly evaluate the WKB pair

\[
w(Q_+)=A(Q_+)^{-1/4},\qquad
w'(Q_+)=-\left(\sqrt{A(Q_+)}+
\frac{A'(Q_+)}{4A(Q_+)}\right)w(Q_+),
\]

and bound the algebraic residual

\[
r=\frac{5(A')^2}{16A^2}-\frac{A''}{4A}.
\]

Those three statements are useful *preconditions*, but they do not give an
outward ball for the actual recessive \((u(Q_+),u'(Q_+))\).  In particular,
the real result's conversion of an integral of \(r/\sqrt A\) into simultaneous
value and derivative errors depends on a real positive coefficient.  Replacing
positivity by the branch condition above without a complex progressive-path
argument would be an unproved theorem substitution.

## Minimum theorem-and-computation contract before a runner exists

The next independent unit must supply all of the following in code and in an
adjacent input manifest, for only the fixed box above.

1. **Complex-tail lemma.**  State and prove (or pin a source whose hypotheses
   are checked in full) a first-order/Volterra formulation for the selected
   principal \(\sqrt A\) branch.  It must bound both the value and derivative
   corrections at \(Q_+=4\), not merely a formal WKB residual.  Its kernel
   bound must use a verified monotone lower bound for
   \(\operatorname{Re}\sqrt{A(Q,z)}\) on the entire half-line.
2. **Tail-to-endpoint normalization.**  Fix a normalization for the
   recessive solution at infinity and show that the Volterra fixed point is
   unique in the stated ball norm.  A finite-cutoff numerical decay condition
   is insufficient.
3. **Outward complex arithmetic.**  Evaluate the WKB pair, the correction
   radii, every branch-separation lower bound, and the contraction constant
   with `acb` at two precision tiers.  Each displayed complex component must
   be an outward rectangle; no midpoint rounding or NumPy complex value may
   enter the certified path.
4. **Explicit fail-closed gates.**  Reject the box if the branch disc touches
   the cut, the real-part lower bound is nonpositive, the contraction constant
   is not strictly below one, or either endpoint enclosure is non-finite.
   A failed gate must emit `UNRESOLVED_FIXED_BOX`, never a proxy value.
5. **Scope firewall.**  The resulting output, if all gates pass, may say only
   `FINITE_FIXED_BOX_RECESSIVE_ENDPOINT_DATA_ENCLOSED`.  It must leave
   `singular_endpoint_nonreal_weyl_function`, spectral measure, spectral
   multiplicity, RAQ test space/map/product, and all physics claims null.
   Compact transport to \(Q_0=-4\) is a separate later question.

## Why this is not solved by the locked dependency alone

`python-flint` supplies outward elementary complex balls, not a theorem that
the proposed complex Liouville--Green error integral encloses the selected
solution.  No existing runner implements the required tail Volterra
contraction or a validated complex interval-Taylor flow.  The available
real-tail DLMF audit cannot be reused across this change of hypotheses.

The operator-theoretic reference, Eckhardt--Gesztesy--Nichols--Teschl,
[arXiv:1208.4677](https://arxiv.org/abs/1208.4677), remains the definition and
scope baseline for singular Weyl--Titchmarsh work.  It is not a substitute for
the model-specific complex endpoint lemma above.

## Implementation handoff

Once item 1 has a source-checked theorem or a self-contained proof, add only
these three files as one clean, unnumbered unit:

- `raw_c_fixed_box_nonreal_endpoint_enclosure.py`
- `RAW_C_FIXED_BOX_NONREAL_ENDPOINT_ENCLOSURE_INPUTS.json`
- `RAW_C_FIXED_BOX_NONREAL_ENDPOINT_ENCLOSURE.md`

The input must pin the selected extension result and this nonreal-proxy result
only as provenance, not as a proof.  Resource limits should keep one box, two
precision tiers, no SciPy ODE calls, no root search, and no sampling grid.
The runner should be executed only through `./ice run` after it is clean and
committed.
