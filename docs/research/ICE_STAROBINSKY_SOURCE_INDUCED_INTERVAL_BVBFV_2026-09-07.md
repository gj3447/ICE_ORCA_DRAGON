# 동차 Starobinsky source에서의 interval BV--BFV 후보

2026-09-07 · `SUPPORTING_METHOD` · 고전적, reviewable construction.

여기서 ``source-induced''는 **이미 고정한 동차 Lorentzian phase-space action
\(S_L\)와 그 canonical BFV extension으로부터** 1차원 AKSZ/BV--BFV 자료를
만든다는 좁은 뜻이다. 4차원 covariant Starobinsky gravity, GHY 항, 혹은 원래
complex integration cycle에서 이 자료를 유도했다는 뜻이 아니다.

질문은 하나다. 실제 homogeneous Starobinsky constraint와 primary lapse
constraint를 쓴다면, interval의 bulk--boundary identity를 만족하는 명시적
classical BV--BFV **extended-system 후보**를 적을 수 있는가? 아래의 출력은 그
후보와 부호다. 이 후보가 실제 \(S_L\)의 BV gauge fixing이라는 bridge는 별도의
조건이며, 이 문서에서 자동으로 성립한다고 하지 않는다. 비주장은 양자 state,
determinant, positive metric, CPT kernel, original relative class 및 G1의 global
intersection이다.

## 1. 고정한 실제 source와 convention

좌표시간 interval을 \(I=[s_-,s_+]\), \(\dot{}=d/ds\)로 둔다. 실제
homogeneous Lorentzian source는

\[
 S_L=\int_I\!ds\,[p_a\dot a+p_\phi\dot\phi-NH_L],
 \tag{1}
\]

\[
 H_L=-\frac{p_a^2}{24\pi^2a}+\frac{p_\phi^2}{4\pi^2a^3}
 -6\pi^2a+\frac32\pi^2a^3(1-e^{-\sqrt{2/3}\phi})^2,\qquad a>0 .
 \tag{2}
\]

식 (1)은 [기존 source convention](ICE_STAROBINSKY_BFV_BOUNDARY_IDEAL_METHOD_2026-09-06.md#3-부호와-constraint를-먼저-고정한다)과
[polynomial BFV chart](../../cpt_temporal_folded_susy/STAROBINSKY_POLYNOMIAL_BFV_CHART.md)의
Lorentzian convention을 그대로 쓴다. \(N\)은 configuration lapse이고 \(\Pi\)
는 그 primary momentum이다.

경계 BFV target \(\mathcal B\)는 even coordinates

\[
 (a,\phi,N;p_a,p_\phi,\Pi)
\]

와 odd canonical pairs \((c,\bar\rho)\), \((\rho,\bar c)\)로 둔다. Ghost
numbers는 \(c,\rho=+1\), \(\bar\rho,\bar c=-1\)이다. 고정한 one-form,
symplectic form, BFV Hamiltonian은

\[
 \alpha_{\rm BFV}=p_a\delta a+p_\phi\delta\phi+\Pi\delta N
       +\bar\rho\delta c+\bar c\delta\rho,
 \qquad \omega_{\rm BFV}=\delta\alpha_{\rm BFV},
 \qquad \Omega=cH_L+\rho\Pi .
 \tag{3}
\]

Even bracket에는 \(\{q,p\}=+1\), odd canonical bracket에는 symmetric \(+1\)
convention을 쓴다. 이 convention에서 \(Q_\partial F=\{\Omega,F\}\)이고

\[
 \begin{aligned}
 Qa&=\frac{cp_a}{12\pi^2a},& Q\phi&=-\frac{cp_\phi}{2\pi^2a^3},& QN&=-\rho,\\
 Qp_a&=c\partial_aH_L,& Qp_\phi&=c\partial_\phi H_L,& Q\Pi&=Qc=Q\rho=0,\\
 Q\bar\rho&=H_L,&Q\bar c&=\Pi .
\end{aligned}
\tag{4}
\]

For the even canonical pairs, \(\omega=\delta p\wedge\delta q\) and this
choice gives \(\iota_{Q_\partial}\omega_{\rm BFV}=\delta\Omega\). Hence the
order \(QF=\{\Omega,F\}\) fixes the target cohomological vector field. The
bulk component/Koszul signs are fixed separately by the CMW replacement in
§2, rather than by an unexpanded \(\pm\Omega\) superfield shorthand. The odd
part uses the same pinned right/left-derivative convention as the existing
graded helper.

\(H_L\)은 \(N\)에 독립이고 constraints \(H_L,\Pi\)는 Abelian이므로
\(\{\Omega,\Omega\}=0\). 이 한 항등식이 아래 AKSZ lift가 요구하는 target
Hamiltonian condition이다.

## 2. CMW의 명시적 Abelian interval BV component construction

이 절의 부호는 [CMW §8--§9.1, eqs. (79)--(80)](https://arxiv.org/html/2012.13270#S8)에서
직접 따른다. Generic superfield action을 추측하지 않는다. \(q^i=(a,\phi,N)\),
\(p_i=(p_a,p_\phi,\Pi)\), 두 constraints

\[
 H_1=H_L,\qquad H_2=\Pi,
 \qquad c^1=c,\quad c^2=\rho,
 \qquad b_1=\bar\rho,\quad b_2=\bar c
 \tag{5}
\]

를 CMW의 Abelian construction에 넣는다. Bulk BV field는
\((p,q,e^\alpha,c^\alpha;p_+ ,q^+,e^+_\alpha,c^+_\alpha)\)이고, CMW의
component replacement는

\[
 p_i\mapsto p_i+q^+_i,\quad q^i\mapsto q^i-p_+^i,
 \quad c^\alpha\mapsto c^\alpha-e^\alpha,
 \quad b_\alpha\mapsto-e^+_\alpha+c^+_\alpha .
 \tag{6}
\]

따라서 structure function이 0인 현재 경우의 BV action은

\[
 S_{\rm BV}=\int_I\!\left[
 p_i\,dq^i-e^+_\alpha\,dc^\alpha-e^\alpha H_\alpha(p,q)
 +c^\alpha\left(q_i^+\partial_{p_i}H_\alpha
 -p_+^i\partial_{q^i}H_\alpha\right)\right].
 \tag{7}
\]

This is an exact CMW component convention, including its deliberate signs.
The degree-zero 1-form components \(e^1,e^2\) are new multipliers; they are
not automatically the target coordinate \(N\). At vanishing BV partners and
ghosts, (7) becomes

\[
 S^{\rm cl}_{\rm ext}=\int_I ds\,[p_a\dot a+p_\phi\dot\phi+\Pi\dot N
 -e^1H_L-e^2\Pi].
 \tag{8}
\]

The full-primary component bridge that reproduces (1) is therefore

\[
 e^1=N,\qquad e^2=\dot N,
 \quad\Longrightarrow\quad
 S^{\rm cl}_{\rm ext}=S_L .
 \tag{9}
\]

The \(e^2\Pi\) term cancels the canonical \(\Pi\dot N\) term. Choosing
\(e^2=0\) would recover (1) only on a static-lapse or \(\Pi=0\) slice.
Equation (9) is a component-level equality, not yet a proved BV
gauge-fixing Lagrangian: the corresponding conditions on all plus fields,
their Lagrangian property, and their compatibility with a complex integration
cycle still have to be constructed. The reduced one-constraint system simply
uses \(e^1=N\) and has no primary-pair issue.

## 3. Exact oriented endpoint BFV data

Let ``in'' mean \(s_-\) and ``out'' mean \(s_+\). The ordinary variation of
the kinetic part of (7) is \(\alpha_{\rm BFV,out}-\alpha_{\rm BFV,in}\).
CMW's mCME cancels this with the **oppositely ordered** endpoint primitive:

\[
 \alpha_{\partial I}=\alpha_{\rm BFV,in}-\alpha_{\rm BFV,out},\qquad
 \omega_{\partial I}=\omega_{\rm BFV,in}-\omega_{\rm BFV,out},\qquad
 S_{\partial I}=\Omega_{\rm in}-\Omega_{\rm out}.
 \tag{10}
\]

With the CMW boundary map \(b_\alpha=-e^+_\alpha\) at both endpoints, the
exact classical identities are

\[
 \iota_{Q_{\rm BV}}\omega_{\rm BV}=\delta S_{\rm BV}
 +\pi^*\alpha_{\partial I},\qquad
 \frac12\iota_{Q_{\rm BV}}\iota_{Q_{\rm BV}}\omega_{\rm BV}
 =\pi^*S_{\partial I},\qquad d\pi(Q_{\rm BV})=Q_{\partial I}.
 \tag{11}
\]

These signs follow from CMW's component/Koszul convention. The actual target data in
(3)--(4) make (5)--(11) an explicit homogeneous Starobinsky extended-system
candidate; this does not derive them from covariant gravity plus GHY.

### 3.1 Primary pair를 분리할 때 남는 relative boundary 자료

식 (7)의 primary sector가 (1)에 맞추어지는 방식을, 경계 항까지 포함하여
local jet algebra에서 직접 쓸 수 있다. 다음은 bulk의 형식적 변수변환이지
경계 상태공간의 quasi-isomorphism 주장이 아니다. (E=e^1) 및

\[
 \sigma=e^2-\dot N,\qquad \sigma^+=e^+_2,\qquad
 N^+_{\rm new}=N^+-\dot e^+_2
 \tag{12}
\]

로 둔다. (7)을 현재 Abelian constraints에 전개하면 relevant terms are

\[
 \begin{split}
 S_{\rm BV}=\int_I ds\,[&p_a\dot a+p_\phi\dot\phi+\Pi\dot N
 -E H_L-e^2\Pi-e^+_1\dot c-e^+_2\dot\rho\\
 &+c(q_i^+\partial_{p_i}H_L-p_+^i\partial_{q^i}H_L)+\rho N^+] .
 \end{split}
 \tag{13}
\]

여기서 \(H_L\)은 \(N\)에 독립이므로 \(c\)-항에는 \(N\)-antifield
derivative가 없다. 적분 부분적분과 odd coefficient 순서를 포함하면

\[
 \begin{split}
 \int_I(\Pi\dot N-e^2\Pi)&=-\int_I\Pi\sigma,\\
 -\int_I\sigma^+\dot\rho+\int_I\rho N^+
 &=\int_I\rho N^+_{\rm new}-[\sigma^+\rho]_{s_-}^{s_+}.
 \end{split}
 \tag{14}
\]

두 번째 줄의 마지막 적분에서는 \(\rho\dot\sigma^+=-\dot\sigma^+\rho\)를
썼다. 따라서 exact bulk rewriting은

\[
 S_{\rm BV}=S_{\rm min}(E,c)
 +\int_I ds\,[-\Pi\sigma+\rho N^+_{\rm new}]
 -[\sigma^+\rho]_{s_-}^{s_+},
 \tag{15}
\]

이다. 여기서 \(S_{\rm min}(E,c)\)는 (13)에서 \(\Pi,e^2,\rho,N^+\)와
그 plus partners를 뺀 one-constraint \(H_L\) CMW action이다. 동시에 BV
cotangent one-form의 해당 부분은

\[
 \int_I(N^+\delta N+e^+_2\delta e^2)
 =\int_I(N^+_{\rm new}\delta N+\sigma^+\delta\sigma)
   +[\sigma^+\delta N]_{s_-}^{s_+}.
 \tag{16}
\]

즉 unrestricted local jet algebra 또는 compactly supported variations에서는
\((\Pi,\sigma;\Pi^+,\sigma^+)\)가 algebraic auxiliary quartet이고
\((N^+_{\rm new},\rho;N,\rho^+)\)는 formal contractible jet sector라는
유용한 bulk bookkeeping을 얻는다. 하지만 interval endpoint jets를 보존하면
(15)의 \(-[\sigma^+\rho]\)와 (16)의 \([\sigma^+\delta N]\)를 함께 유지해야
한다. \(\rho=0\) 또는 \(\sigma^+=0\)가 action boundary term을 없앨 수 있어도,
BV primitive는 allowed variations에서 따로 0이어야 한다; \(\sigma^+=0\)는
그 두 조건을 함께 충족하는 한 충분한 endpoint restriction이다.

따라서 \(E=N,\sigma=0\), 곧 (9)의 \(e^1=N,e^2=\dot N\),는 bosonic
component bridge를 다시 준다. 이것만으로 full BV Lagrangian, endpoint
polarization, 또는 허용된 full path-integration cycle이 정해지지는 않는다.
특히 compact-\(N\) boundary carrier에서 발견된 nontrivial top-ghost
cohomology를 이 local/compact-support bulk contraction으로 없앴다고 결론낼 수
없다.

## 4. The separate declared BFV gauge-fixed phase-space source

The CMW BV action (7) and the following gauge-fixed BFV component action are distinct.
For the already declared gauge fermion

\[
 \Psi=-N\bar\rho,
 \qquad H_\Psi=-\{\Omega,\Psi\}=NH_L+\bar\rho\rho,
 \tag{17}
\]

the declared BFV gauge-fixed trajectory action is

\[
 S^{(0)}_\Psi=\int_I ds\,[p_a\dot a+p_\phi\dot\phi+\Pi\dot N
 +\bar\rho\dot c+\bar c\dot\rho-NH_L-\bar\rho\rho].
 \tag{18}
\]

On the bosonic slice \(\Pi=c=\rho=\bar\rho=\bar c=0\), this **separate
Hamiltonian BFV construction** is precisely (1). Eliminating \(p_a,p_\phi\)
there gives the configuration form

\[
 S_L=\int_I ds\left[-\frac{6\pi^2a\dot a^2}{N}
 +\frac{\pi^2a^3\dot\phi^2}{N}+6\pi^2aN
 -\frac32\pi^2a^3N(1-e^{-\sqrt{2/3}\phi})^2\right].
 \tag{19}
\]

This verifies the actual \(S_L\) relation for the declared Hamiltonian BFV
action, not for (7) without the component bridge (9). It does **not** select a
path-integral measure or establish that either gauge-fixing Lagrangian is
admissible on the desired complex cycle. In particular, the positive-lapse
ray, a full-real group average, and a finite \(\Pi\) Fourier integral are
different source choices; none follows from (6) or (18).

The previously constructed finite canonical endpoint

\[
 L_{q_0}=\{a=a_0,\phi=\phi_0,N=N_0,c=\rho=0\}
 \tag{20}
\]

has \(\alpha_{\rm BFV}|_{L_{q_0}}=0\) and \(\Omega|_{L_{q_0}}=0\), and is
\(Q_\partial\)-tangent in the finite canonical model because the unconstrained
momenta and antighost momenta remain free. Hence it is a possible classical
adapted endpoint condition for the BFV target (3). It is not a proof that a
covariant bulk selects (20), nor an identification with the Weyl Cauchy jet condition at
\(a=2\).

## 5. What classical gluing now means

For two intervals with a common endpoint, identify the outgoing copy of
\(\mathcal B\) from the first interval with the incoming copy from the second.
The terms \(+\alpha_{\rm BFV}\) and \(-\alpha_{\rm BFV}\), and likewise
\(+\Omega\) and \(-\Omega\), cancel on this diagonal relation. This is the
classical source-level reason that the oriented seam is compatible with
(10)--(11).
It supplies neither a delta kernel nor a measure.

CMR quantum gluing instead pairs states in chosen transversal polarizations
and then performs a residual-field BV pushforward; see [CMR §2.4.4,
eqs. (2.36)--(2.37)](https://arxiv.org/html/1507.01221#S2.SS4.SSS4). CMR also
requires a quantum BFV operator on a polarized state/half-density space and
a bulk state obeying the mQME
\((\hbar^2\Delta_{\rm res}+\widehat\Omega)\widehat\psi=0\)
([CMR §2.3](https://arxiv.org/html/1507.01221#S2.SS3)). None of those objects
is furnished by the classical diagonal cancellation.

CMW's constrained-mechanics analysis is relevant because it explicitly
places finite-dimensional constrained interval systems in BV bulk/BFV
endpoint language. Its quantization results are not imported wholesale:
the current \(H_L\) is nonlinear and quadratic in endpoint momenta, while
the applicability conditions of any chosen CMW polarization theorem must be
checked separately.

## 6. Falsifiable handoff and exclusions

This construction reduces one ambiguity: an extended interval source using
(2) and the declared full BFV target must reproduce the CMW component action
(7), the incoming-minus-outgoing endpoint data (10)--(11), and the new
multipliers \(e^1,e^2\). A candidate which claims equivalence to the actual
\(S_L\) must additionally exhibit bridge (9), including all BV-partner
conditions. A proposed source that instead
has only \(H_L\), omits \(\rho\Pi\), or identifies \(\partial_a\) of a WDW
state with \(p_a\), is a different construction and cannot inherit this
result.

The next concrete object is a finite polarized boundary kernel/half-density
whose quantized BFV operator intertwines the two oriented endpoint copies,
together with an explicit regulator and its cutoff-face Ward terms. Its
failure to exist for a declared polarization is a valid negative result.
Before that object is supplied, the following remain open:

- a covariant Starobinsky plus GHY reduction to this finite target;
- the full-primary-pair BV gauge-fixing Lagrangian proving \(e^1=N\),
  \(e^2=\dot N\), its BV partners, and its ghost-sector boundary conditions;
- a specified bulk BV gauge-fixing Lagrangian and determinant/Berezin
  orientation;
- quantum mQME, residual fields, a CPT anti-linear lift, and a positive
  physical product;
- the source-defined regulated joint relative class, good ends, and oriented
  global saddle intersections required at G1.

This note is a source derivation, not an execution receipt. No new runner,
raw result, ontology status, physical discovery, or TOE claim is created.
