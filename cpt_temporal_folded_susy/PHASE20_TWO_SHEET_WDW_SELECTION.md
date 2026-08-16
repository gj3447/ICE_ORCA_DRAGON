# Phase 20 — two-sheet WDW selection control

## Result first

The supplied calculation has a correct core result, but its strongest wording
and one factor-of-two convention need correction:

\[
\boxed{
\text{the leading de Sitter/WDW envelope does not select }
\varphi_*=5.442969458
}
\]

This is **not** an exact no-go for a CPT two-sheet supergravity wavefunction.
The exponent used here is the constant-field de Sitter hemisphere action. At
the benchmark \(V'\ne0\), no exact complex scalar-gravity saddle, WDW current,
sheet inner product, or local-SUGRA wavefunction has been solved.

The two probability conventions are

\[
P_{\rm WDW}\propto e^{2sI},
\qquad
P_{\rm independent\ pair}\propto e^{4sI},
\qquad s=\begin{cases}+1&\text{HH}\\-1&\text{tunneling.}\end{cases}
\tag{E200}
\]

The first is the standard semiclassical history weight. The second requires
an extra assumption: treat the two sheet histories as independent
tensor-product outcomes, so their history probabilities multiply. CPT sewing
alone does not establish that rule. The factor changes the slope by two but
does not change the no-finite-peak result.

The executable reproduces this separation with **18 exact PASS and 14
numerical PASS** checks:

~~~bash
uv run --locked python3 \
  cpt_temporal_folded_susy/phase20_two_sheet_wdw_selection.py
~~~

## 1. Leading de Sitter exponent

Use reduced Planck units and define

\[
\varphi=\frac{\phi}{M_{\rm Pl}},
\qquad
\lambda=\frac{M_s}{M_{\rm Pl}},
\qquad
b=\sqrt{\frac23},
\]

\[
\frac{V}{M_{\rm Pl}^4}
=\frac34\lambda^2(1-e^{-b\varphi})^2.
\tag{E201}
\]

For a constant scalar on a de Sitter hemisphere,

\[
I(\varphi)
=\frac{12\pi^2M_{\rm Pl}^4}{V}
=\frac{16\pi^2}
{\lambda^2(1-e^{-b\varphi})^2}.
\tag{E202}
\]

The normalization follows from
\(I_E(S^4)=-24\pi^2M_{\rm Pl}^4/V\); a hemisphere contributes half.
This is the conventional semiclassical control behind the
[Hartle–Hawking proposal](https://doi.org/10.1103/PhysRevD.28.2960).

Its exact symbolic derivative is

\[
I'(\varphi)=
-\frac{32\pi^2b\,e^{-b\varphi}}
{\lambda^2(1-e^{-b\varphi})^3}.
\tag{E203}
\]

For every finite \(\varphi>0\), this has no zero. It approaches zero only
asymptotically on the plateau. Consequently both signs in (E200) are
monotone: the HH envelope decreases with \(\varphi\), while the tunneling
envelope increases toward its large-field plateau.

The no-boundary literature uses a semiclassical history probability
proportional to \(\exp(-2I_R)\), not a universal two-sheet
\(\exp(4sI)\) rule. It also treats the exact saddle as generally complex;
see [Hartle, Hawking, and Hertog, arXiv:0711.4630](https://arxiv.org/abs/0711.4630).
Boyle and Turok motivate an analytic two-sheet spacetime and preferred QFT
vacuum, but do not derive the independent WDW product probability used in the
second expression of (E200); see
[arXiv:2109.06204](https://arxiv.org/abs/2109.06204).

## 2. The benchmark slopes

At

\[
\varphi_*=5.442969458
\]

the standard history convention gives

\[
\left.
\frac{d\ln P_{\rm WDW}}{d\varphi}
\right|_{\varphi_*}
=-s\frac{6.277009460746}{\lambda^2}.
\tag{E204}
\]

Under the additional independent-pair convention,

\[
\left.
\frac{d\ln P_{\rm independent\ pair}}{d\varphi}
\right|_{\varphi_*}
=-s\frac{12.554018921492}{\lambda^2}.
\tag{E205}
\]

For \(\lambda=1.3\times10^{-5}\),

| convention | HH slope | tunneling slope |
| --- | ---: | ---: |
| standard history | \(-3.7142068\times10^{10}\) | \(+3.7142068\times10^{10}\) |
| independent pair | \(-7.4284136\times10^{10}\) | \(+7.4284136\times10^{10}\) |

An \(h=10^{-7}\) high-precision central difference reproduces both analytic
derivatives. Thus the supplied \(12.55401892/\lambda^2\) number is
arithmetically correct under its extra pair assumption; it is not the unique
standard WDW normalization. Either way, the slope is emphatically nonzero.

There is a second qualification. At the same point,

\[
\frac{V'}V=0.0194106210,
\qquad
\epsilon_V=\frac12\left(\frac{V'}V\right)^2
=1.8838610\times10^{-4}.
\tag{E206}
\]

The de Sitter approximation is good in the slow-roll sense, but the scalar is
not constant. Calling (E202) the **exact Starobinsky WDW saddle action**
would therefore be too strong.

## 3. Symmetrization and interference

A coherent conjugate-saddle sum has the form

\[
\Psi_{\rm real}
=\mathcal N e^{sI}(e^{iS}+e^{-iS}),
\]

and hence

\[
|\Psi_{\rm real}|^2
=4|\mathcal N|^2e^{2sI}\cos^2S.
\tag{E207}
\]

This corrects two claims in the supplied text:

- a universal \(P_{\rm sym}=2e^{4sI}\) does not follow without specifying
  normalization, overlap, and whether the sheets are independent systems;
- coherent \(\cos^2S\) interference is order one, not automatically a
  “small fringe.”

If the sheets decohere, the cross term disappears. If they remain coherent,
the varying phase can create local nodes and extrema. A
\(\varphi\)-independent normalization alone cannot move the envelope peak,
but a \(\varphi\)-dependent overlap or phase can. WDW probabilities require
a current or decoherent-histories construction, and ordinary WKB itself
fails at a turning point. Halliwell derives approximate decoherence only for
suitably coarse WKB histories and regions; see
[arXiv:0909.2597](https://arxiv.org/abs/0909.2597).

## 4. What the Cecotti SUSY condition says

For

\[
K=-3\log\left[
T+\bar T-S\bar S+\frac{\zeta}{3}(S\bar S)^2
\right],
\qquad
W=3M S(T-1),
\]

the \(S=0,\ T=\bar T>0\) trajectory gives

\[
D_SW=3M(T-1),
\qquad
K^{S\bar S}=\frac{2T}{3},
\]

\[
F^S=-\frac{M(T-1)}{\sqrt{2T}},
\qquad
V=\frac{3M^2(T-1)^2}{4T^2}.
\tag{E208}
\]

At the benchmark,

\[
T_*=e^{b\varphi_*}=85.1288467223,
\qquad
\frac{F^S}{M}=-6.4475031455\ne0.
\tag{E209}
\]

Thus this classical inflationary background is not F-flat. The positive-real
static F-flat point on the displayed trajectory is \(T=1,\varphi=0\), not
\(\varphi_*\).

This does **not** prove that a quantum local-SUSY constraint forbids support at
\(\varphi_*\). In supersymmetric minisuperspace those constraints become
coupled first-order PDEs for wavefunction components and depend on the
Kähler geometry; see
[Cheng, D'Eath, and Moniz, arXiv:gr-qc/9406048](https://arxiv.org/abs/gr-qc/9406048).
They have not been solved here for the Cecotti \(K,W\), gravitino sector,
factor ordering, and CPT/Pin boundary condition.

## 5. Conditional curvature–reheating conversion

The independent closed-FRW integration from Phase 19 gives, at the
\(N_{\rm acc}=60\) acceleration endpoint,

\[
M_s a_b=2.0237730586,
\qquad
\frac{\rho_{\rm end}}{M_s^2M_{\rm Pl}^2}
=0.1751668051.
\tag{E210}
\]

The redundant Friedmann constraint at that endpoint is also checked to
better than \(2\times10^{-12}\) in relative error.

For constant reheating equation of state \(w_{\rm reh}\), entropy conservation,
and instantaneous thermalization at \(T_{\rm reh}\),

\[
a_{\rm today}
=a_b e^N
\left(\frac{\rho_{\rm end}}{\rho_{\rm reh}}\right)^{
1/[3(1+w_{\rm reh})]}
\frac{T_{\rm reh}}{T_0}
\left(\frac{g_{s,\rm reh}}{g_{s0}}\right)^{1/3},
\]

\[
\Omega_{K0}=-\frac1{(a_{\rm today}H_0)^2}
\quad (k=+1).
\tag{E211}
\]

Using the explicit benchmark inputs

\[
\begin{gathered}
M_s=1.22\times10^{-5}M_{\rm Pl},\quad
M_{\rm Pl}=2.435\times10^{18}\ {\rm GeV},\quad
w_{\rm reh}=0,\\
T_0=2.7255\ {\rm K},\quad
g_{\rm reh}=g_{s,\rm reh}=106.75,\quad
g_{s0}=3.909,\quad
H_0=67.4\ {\rm km\,s^{-1}Mpc^{-1}},
\end{gathered}
\]

with SI-to-GeV conversions taken from SciPy's CODATA-2022 constants, gives

\[
\boxed{
\Omega_{K0}
=-5.5258\times10^{-4}
\left(\frac{T_{\rm reh}}{10^9\ {\rm GeV}}\right)^{2/3}
}
\tag{E212}
\]

and

\[
|\Omega_{K0}|=10^{-3}
\quad\Longleftrightarrow\quad
T_{\rm reh}=2.4345\times10^9\ {\rm GeV}.
\tag{E213}
\]

The supplied rounded values \(5.526\times10^{-4}\) and
\(2.435\times10^9\ {\rm GeV}\) are therefore reproducible. They are not a
seam prediction:

\[
\frac{\partial\ln|\Omega_{K0}|}{\partial N}=-2,
\qquad
|\Omega_{K0}|\propto
M_s^{2/3}H_0^{-2}
T_{\rm reh}^{-2+8/[3(1+w_{\rm reh})]}.
\tag{E214}
\]

A one-e-fold change multiplies the magnitude by \(e^{-2}\). Changing the
reheating history changes even the temperature exponent. The sign is also
important: a closed \(k=+1\) model predicts negative \(\Omega_K\), whereas the
quoted \(0.001\) was only an absolute-value target.

Current curvature fits are model and data-set dependent. DESI DR2 reports
that its BAO results are well described by flat \(\Lambda\)CDM, while also
highlighting tensions among restricted cosmological fits; see the
[DESI DR2 cosmology analysis, arXiv:2503.14738](https://arxiv.org/abs/2503.14738).
No curvature detection is inserted into (E212).

## 6. One-loop peak condition

If a probability-level correction is defined by

\[
P=\exp\left(2sI-\Gamma_{\rm seam}^{(P)}\right),
\]

then a stationary point at \(\varphi_*\) requires

\[
\left.\Gamma_{\rm seam}^{(P)\prime}\right|_{\varphi_*}
=-s\frac{6.277009460746}{\lambda^2}.
\tag{E215}
\]

Here the prime is \(d/d\varphi\). A derivative with respect to the
dimensionful field \(\phi\) carries an additional \(M_{\rm Pl}^{-1}\).

Under the independent-pair convention \(2sI\to4sI\), the right-hand side
doubles to

\[
-s\frac{12.554018921492}{\lambda^2}.
\tag{E216}
\]

If \(\Gamma^{(1)}\) is instead defined in the **amplitude**, the probability
contains \(2\operatorname{Re}\Gamma^{(1)}\); its convention must be fixed
before comparing coefficients. A one-loop sharp peak has been found in a
large-nonminimal-coupling inflation model by
[Barvinsky, Kamenshchik, and Mishakov, arXiv:gr-qc/9612004](https://arxiv.org/abs/gr-qc/9612004).
That is a proof of principle in a different model, not a computed
boson–fermion–gravitino determinant for this two-sheet Cecotti theory.

## 7. Bounded verdict

### Established

- the displayed de Sitter exponent and both slope conventions are reproduced;
- neither leading envelope has a finite stationary point at \(5.442969458\);
- \(e^{4sI}\) is an additional independent-pair assumption, not an automatic
  consequence of CPT;
- the Cecotti inflationary point has \(F^S\ne0\);
- the rounded conditional \(\Omega_K\)–\(T_{\rm reh}\) numbers are reproduced
  with their sign and unit conventions exposed.

### Still open

- the exact complex Starobinsky saddle and its real action \(I_R\);
- a WDW current, measure, normalization, and factor ordering;
- the CPT/Pin Hilbert-space sewing and sheet overlap;
- the local-SUGRA wavefunction including gravitino and ghost sectors;
- the one-loop boson–fermion–gravitino determinant;
- a quantized four-form spectrum that selects \(\varphi_*\);
- a seam-derived \(T_{\rm reh}\) or present-day curvature prediction.

The correct research statement is therefore

\[
\boxed{
\text{the naive leading WDW envelope does not select }5.44,
\quad
\text{but an exact two-sheet SUGRA WDW no-go has not been proved.}
}
\]
