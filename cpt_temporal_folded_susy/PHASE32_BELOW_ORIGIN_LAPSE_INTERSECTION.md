# Phase 32 — below-origin lapse bypass and recorded intersection gate

## Outcome

Two lapse prescriptions that had previously been conflated now give sharply
different answers.

For the causal positive half-line with proper-time damping,

\[
N=x,\qquad x\geq0,
\]

the Wick map $T=iN$ places the contour on the positive imaginary $T$ ray.
Its closure meets the recorded positive-real upward dual only at the singular
origin.  A separately declared lower-lateral endpoint regulator,
$N=x-i\epsilon$, shifts this contact to $T=\epsilon$ but leaves it at the
contour endpoint rather than making it an interior transverse crossing.
Therefore no ordinary Picard--Lefschetz integer is assigned:

\[
\boxed{
N>0\text{ half-line}:\quad n_\sigma\text{ remains OPEN.}
}
\]

If instead the **full real lapse contour** is declared to bypass $N=0$ from
below,

\[
\Gamma_r^-
=(-\infty,-r]\cup
\{N=re^{i\theta}\mid-\pi\leq\theta\leq0\}
\cup[r,\infty),
\]

then the small lower $N$ semicircle maps to a right $T$ semicircle,

\[
-ir\longrightarrow r\longrightarrow ir.
\]

At $T=r$, the contour tangent points upward and the recorded dual tangent
points left.  With columns ordered as $(\Gamma_r^-,\mathcal K_\sigma)$,

\[
v_{\Gamma}=(0,1),\qquad v_{\mathcal K}=(-1,0),
\qquad
\det(v_\Gamma,v_\mathcal K)=+1.
\]

The actual complex fixed-boundary solution was solved at five recorded angles
on each of four such semicircles.  No sampled Jacobi zero was encountered.
With ambient orientation $(\operatorname{Re}T,\operatorname{Im}T)$, columns
ordered as $(\Gamma_r^-,\mathcal K_\sigma)$, a stipulated flow-outward
orientation on the left dual, and the declared positive-$N$-normalized
Gaussian lift, this gives

\[
\boxed{
\begin{gathered}
\text{specified below-origin full-line contour}\cr
{}+\text{declared positive-}N\text{-normalized coupled Gaussian lift}
\end{gathered}
\quad\Longrightarrow\quad
\text{one projected lapse-base crossing with coordinate sign }+1.
}
\]

This is deliberately **not** called either a signed local intersection of the
full joint BFV/PL cycles or the global coefficient $n_\sigma=+1$.  The full
$\mathcal K_\sigma$ tangent, ghost/superdeterminant orientation, and
determinant-line trivialization have not been constructed.
As $r\to0$, the crossing moves into the singular identity-kernel endpoint.
Other upward-cycle components, other complex BVP sheets, good ends, the full
oriented superdeterminant line, and all possible additional intersections
have not been enumerated.  Ordinary complex conjugation exchanges the upper
and lower lateral lapse loci.  Identifying that conjugation with a complete
CPT/Pin bra--ket map, and choosing which relative lapse class defines the ket,
remain open.

The executable passes 14 exact and 7 numerical checks.  No target value such
as $\phi=5.44$, $N_e=60$, a desired rank, or a SUSY scale enters the input.

## 1. Frozen connected saddle

The connected homogeneous Starobinsky interval is inherited without
retuning from Phases 24--31:

\[
q_\partial=
(3.56680319357,1.01858094640;
 3.56680319357,1.01858094640),
\]

\[
T_*=0.7,\qquad
W_*=1.40669054283434,\qquad
W_{TT}=-8.92314303834.
\]

The fixed-endpoint, fixed-$T$ branch has Hamilton--Jacobi derivative

\[
W_T=-H_E=6\pi^2a\mathcal C.
\]

On the short positive-real branch it approaches

\[
\lim_{T\to0^+}W_T
=2\pi^2[-3a_\partial+a_\partial^3V(\phi_\partial)]
=2.98719256735>0.
\]

Therefore its flow direction on the recorded upward dual points toward the
origin along the positive real $T$ axis.  The orientation of that dual is an
additional convention, stipulated below rather than fixed by $W_T>0$ alone.

## 2. Half-line versus full-line objects

The positive half-line is a Green object.  With $\eta>0$,

\[
G_\eta(H)
=\int_0^\infty dN\,e^{-iN(H-i\eta)}
=-\frac{i}{H-i\eta},
\]

so

\[
(H-i\eta)G_\eta=-i\mathbf 1.
\]

It is not the full constraint-supported distribution.  The full real lapse
instead formally gives

\[
\int_{-\infty}^{\infty}dN\,e^{-iNH}=2\pi\delta(H).
\]

The distinction between positive proper time and unrestricted lapse is the
old causality-versus-gauge-invariance split emphasized by
[Teitelboim](https://doi.org/10.1103/PhysRevLett.50.705) and in the
composition analysis of
[Halliwell--Ortiz](https://doi.org/10.1103/PhysRevD.48.748).

For the lower lateral half-line,

\[
N=x-i\epsilon,\quad x\geq0
\quad\Longrightarrow\quad
T=\epsilon+ix.
\]

For $0<\epsilon<T_*$, at $x=0$, $T=\epsilon$ lies on the recorded real dual,
but this point is the
boundary of the half-line contour.  In the $\epsilon\to0^+$ limit it also
approaches the singular zero-lapse endpoint.  An endpoint contact is not an
ordinary interior intersection number.

The full-line below-origin prescription supplies more data.  Its finite
semicircle has an honest interior crossing at $T=r$.  A below-origin contour
for the full real lapse, with momenta integrated before the lapse, is the
independent prescription analyzed by
[Banihashemi--Jacobson](https://doi.org/10.1103/PhysRevD.111.066014).
That prescription is not derived from the causal half-line and is not
selected here by CPT/Pin.

## 3. Coupled momentum cycle and local orientation

Freeze the principal homogeneous Hamiltonian form as

\[
H_{\rm kin}
=-\frac{p_g^2}{2\mu_g}+\frac{p_s^2}{2\mu_s},
\qquad \mu_g,\mu_s>0,
\]

and let $N=re^{i\theta}$ on the lower semicircle.  The declared decaying
momentum rays are

\[
p_g=e^{i(\pi/4-\theta/2)}y_g,\qquad
p_s=e^{i(-\pi/4-\theta/2)}y_s,\qquad y_g,y_s\in\mathbb R.
\]

They give the exact exponent

\[
-iNH_{\rm kin}
=-r\left(\frac{y_g^2}{2\mu_g}
          +\frac{y_s^2}{2\mu_s}\right).
\]

At the crossing $\theta=-\pi/2$,

\[
(p_g,p_s)\in(i\mathbb R,\mathbb R).
\]

The dual configuration rays are

\[
(\delta a,\delta\phi)\in(-i\mathbb R,\mathbb R).
\]

Their local Jacobians are $J_p=i$ and $J_q=-i$, so $J_pJ_q=+1$.
The explicitly declared principal Gaussian lift therefore adds no sign to the
stipulated projected crossing.  This calculation does not orient the full
BFV determinant line.

At the negative-real end of the lower turn, however, analytic transport of
the momentum integral already includes its Jacobian and gives $C/N=-C/r$.
The independently identity-normalized real kernel requires $C/|N|=C/r$.
Relating those two separately normalized cycles therefore needs an
**additional** orientation-line comparison or gluing transition $m_-=-1$:

\[
\left(-\frac Cr\right)m_-=\frac Cr,
\qquad m_-=-1.
\]

The $-1$ here is not a second copy of the already included momentum Jacobian;
it is extra comparison data between the analytically transported thimble and
the separately normalized negative-real Fresnel cycle.  The executable proves
that such a transition is required by these two conventions, but does not
derive it as a Maslov index, from CPT/Pin, or from the local equations.  In
particular,
Banihashemi--Jacobson remove the negative gravitational trace momentum before
their positive Gaussian argument; the retained signature-$(-,+)$ extension
above is our finite-mode control, not a theorem imported from that paper.

## 4. Regulated real-dual scan

The lower bypass crosses the recorded real dual at $T=r$.  The numerical
continuation gives:

| $r$ | $W_T$ | $\det B_v/r^2$ | $\sigma_{\min}(B_v)/r$ | $r\,|K_{\rm VV}|$ |
|---:|---:|---:|---:|---:|
| 0.1000000 | 2.92893947 | 0.99937433 | 0.99956745 | 97.93088889 |
| 0.0500000 | 2.97263984 | 0.99984348 | 0.99989182 | 97.90791044 |
| 0.0250000 | 2.98355505 | 0.99996086 | 0.99997295 | 97.90216368 |
| 0.0125000 | 2.98628323 | 0.99999022 | 0.99999324 | 97.90072686 |
| 0.0062500 | 2.98696524 | 0.99999755 | 0.99999831 | 97.90036764 |
| 0.0031250 | 2.98713573 | 0.99999939 | 0.99999958 | 97.90027784 |
| 0.0015625 | 2.98717836 | 0.99999985 | 0.99999989 | 97.90025539 |

The limiting endpoint coefficient is

\[
\frac{\sqrt{|M_gM_s|}}{2\pi}=97.9002479029.
\]

Thus the crossing remains transverse at every finite recorded $r$, while
the Van Vleck factor itself diverges as $1/r$.  This is precisely why the
limit is an endpoint problem rather than a finite ordinary crossing.

The scan is not a proof over the entire interval $0<T<T_*$.  It is a bounded
continuation from $r=.1$ down to $r=.0015625$, combined with the previously
tracked real dual from the saddle toward the origin.

## 5. Actual complex BVP around the lower bypass

For each

\[
r\in\{.1,.05,.025,.0125\}
\]

the complex fixed-boundary equations were solved at

\[
\theta\in
\{-\pi,-3\pi/4,-\pi/2,-\pi/4,0\}.
\]

This is 20 distinct sampled points, five on each of four lower semicircles.
It is not a proof of continuous sheet tracking between the samples.  The
maximum endpoint residual is

\[
8.89\times10^{-16},
\]

and the minimum recorded scaled Jacobi singular value obeys

\[
\min\frac{\sigma_{\min}}r>0.9995.
\]

Therefore the finite-$r$ local crossing is realized by the actual complex
connected boundary-value branch; it is not merely a drawing in the lapse
plane.  This still does not show that the entire nonlinear joint thimble has
been found.

## 6. Endpoint pairing and nonuniform limits

Two different limits coexist at $N=0$.

For a test-function-paired operator kernel, the arc length of the lower
semicircle is $O(r)$, so a bounded paired integrand has

\[
\int_{\Gamma_r^-}dN=2r\longrightarrow0.
\]

Pointwise, a scalar $1/N$ factor instead gives

\[
\int_{\Gamma_r^-}\frac{dN}{N}=i\pi.
\]

The two statements are compatible: exchanging the momentum/test-function
pairing with the zero-radius limit is not uniform.

Likewise, an endpoint displacement $N=x\mp i\epsilon$ multiplies a spectral
mode by $e^{\mp\epsilon\lambda}$.  At fixed $|\lambda|\leq M$,

\[
|e^{-\epsilon\lambda}-e^{+\epsilon\lambda}|
\leq2\sinh(\epsilon M)\longrightarrow0.
\]

But for $M=1/\epsilon$ the bound is

\[
2\sinh1=2.35040238729.
\]

Thus choosing the lateral class and removing the unbounded spectral cutoff
need not commute.  Feynman damping in the proper-time parameter does not, by
itself, fix this zero-lapse side choice.

## 7. Reduced BFV and CPT/Pin scope

In the declared reduced open-interval proper-time gauge,

\[
\delta\!\int_0^1N\,ds=c(1)-c(0)=0
\]

for Dirichlet ghosts, and the fixed-$s$ Dirichlet determinant is independent
of $T$.  Hence this reduced ghost control does not select the upper or lower
endpoint cap.  Phase 31 separately verifies the nonzero finite-cutoff BFV
quartets; neither calculation constructs the absolute nonlinear BFV/BV
measure.

Lapse conjugation maps

\[
x-i\epsilon\longleftrightarrow x+i\epsilon.
\]

Under $T=iN$ it induces $T\mapsto-\bar T$.  This pairs only the two lapse
loci.  A full CPT operation additionally requires boundary exchange plus the
field, spin/Pin, and measure-orientation actions.  Identifying the loci as
ket/bra prescriptions requires the conjugated field action, measure, and
determinant orientation;
that identification, selection of a ket contour, a four-dimensional Pin
lift, and a positive seam density matrix all remain open.

## 8. What is established and what remains open

Established within the frozen homogeneous model:

- the causal positive half-line, and its separately declared lower-lateral
  endpoint regulator, give only endpoint contact with the recorded dual;
- the specified full-line lower bypass maps to a right $T$ semicircle;
- its finite-$r$ cap has one projected lapse-base crossing with coordinate
  sign $+1$ under the declared orientations;
- the declared signature-$(-,+)$ momentum lift is locally convergent and
  preserves that local sign;
- the actual connected complex BVP was solved at five recorded angles on each
  of four lower bypasses without a sampled Jacobi zero;
- the $r\to0$ limit is nonuniform because the endpoint Van Vleck factor grows
  as $1/r$.

Still open:

- the complete global integer $n_\sigma$;
- every other upward-cycle component and every complex BVP sheet;
- the signed full-joint local intersection, global determinant/Maslov data,
  and BFV superdeterminant orientation;
- the physical reason, if any, for choosing below rather than above;
- the inhomogeneous SUGRA, gravitino, Goldstino, and ghost sectors;
- a trace-class WDW projector or full quantum seam state;
- selection of $(n,\phi_0,a_0)$ or a SUSY-breaking scale.

In relative Picard--Lefschetz theory the coefficient is an intersection of a
fully specified relative cycle with a complete dual thimble.  Local Morse
data do not supply that relative class; see
[Witten](https://arxiv.org/abs/1001.2933).  The current finite-$r$ result is
therefore a real advance—it resolves the recorded local crossing after a
specific contour choice—but it is not the final global selection theorem.

## Reproduction

```bash
uv run --locked python3 \
  cpt_temporal_folded_susy/phase32_below_origin_lapse_intersection.py

./ice run phase32_below_origin_lapse_intersection
```

The final JSON payload contains:

```json
{"exact_checks": 14, "numerical_checks": 7}
```

The script writes no files.  Its result payload records the contour class,
all check IDs, the real-dual scan, the complex-bypass BVP table, and the
remaining open gates.

## Primary-source boundaries

- [Banihashemi--Jacobson](https://doi.org/10.1103/PhysRevD.111.066014):
  full real lapse with a below-origin prescription after momentum-first
  convergence analysis; not a positive-half-line rule and not this model's
  computed PL intersection matrix.
- [Teitelboim](https://doi.org/10.1103/PhysRevLett.50.705): causal versus
  gauge-invariant proper-time range distinction; not a selection of the
  present relative cycle.
- [Halliwell 1988](https://doi.org/10.1103/PhysRevD.38.2468):
  minisuperspace/WDW path-integral and lapse-measure setting; not the present
  complex BVP calculation.
- [Halliwell--Ortiz](https://doi.org/10.1103/PhysRevD.48.748): proper-time
  ranges, Green functions, and composition laws; not a proof of the projected
  coordinate $+1$ sign or a full-cycle orientation.
- [Witten](https://arxiv.org/abs/1001.2933): relative Picard--Lefschetz
  cycles and intersection coefficients; not a derivation of the original
  cosmological integration cycle.
- [Feldbrugge--Lehners--Turok](https://arxiv.org/abs/1703.02076): a concrete
  Lorentzian cosmology contour/thimble analysis illustrating why the lapse
  contour is physical data; not a substitute for the missing global
  determinant line here.
