# Phase 13A — Lorentzian local-SUGRA branch-Q kill test

> 검증: `./ice run phase13a_lorentzian_branch_supercharge` →
> **21 exact PASS, 8 semantic mutants rejected, exit 0**.
>
> 사전등록: `PHASE13A_RESEARCH_CONTRACT.json`, commit `c41b6a6`
> (실행체 작성 전). 최초 실행의 단일 `CONTRADICTS` 문구는 물리 mapping 범위를 넘었고,
> 독립 적대검토 뒤 `PHASE13A_ADVERSARIAL_ERRATUM.json`에
> `POST_HOC_CORRECTED`로 보존·정정했다. 원 사전등록 파일은 바꾸지 않았다.

- cycle: `cpt-temporal-folded-susy-2026-08-16-phase13a`
- corrected executable commit: `46551e6f1f32c1f2b4dc4dcd33f1d93e228997f8`
- executable SHA-256: `3fc9c66cd5010833e98544194b1b5410479c9e6daae0fc714255a468a5eedf05`
- environment: Node 24.13.0, Python 3.13.5, SymPy 1.14.0, uv 0.12.3
- actor/date: Codex, 2026-08-16 UTC
- scientific verdict: `UNJUDGED` 유지 / programme appraisal: `UNAPPRAISED` 유지
- 식 번호: **E163–E166**

## 0. 결론부터

Phase 13A의 정확한 결론은 다음 네 줄이다.

1. **formal WKB control — INCONCLUSIVE:** Moniz의 matter-coupled 4D \(N=1\) FRW
   제약 중 \(\partial_a,\partial_\phi\) principal term은 임의의
   \(e^{\pm i\lambda W}\)에 작용해 입력 위상을 유지한다. 그러나 \(W\)는 그 source의 물리적
   Hamilton–Jacobi 해가 아니고, 코드의 \(\pm\) projector도 관계적 팽창/수축 observable이
   아니라 손으로 만든 direct-sum 라벨이다.
2. **finite positive-kernel class — CONTRADICTS:** branch와 fermion parity를 모두 뒤집는
   유한 \(Q\)를 일부러 만들어도, 양의
   \(C=\{Q,Q^\dagger\}\)의 kernel에서는 유도된 \(Q\) map이 정확히 0이다. 이는 정확한
   유한 정리지만 4D SUGRA physical inner product나 constraint에 매핑되지 않았다.
3. **closure \(\Rightarrow\) exchange — CONTRADICTS:** generic CAR odd operator가 even symbol에
   정확히 닫히면서도 \(\pm\) cross block은 모두 0인 countercontrol이 존재한다. 따라서
   closure만으로 시간가지 교환은 따라오지 않는다.
4. **원래 핵심 주장 — INCONCLUSIVE/UNCONSTRUCTED:** gauge-independent relational branch
   projector, 공통 physical domain/inner product, 그리고 local gauge constraint와 구별되는
   nonzero fermionic charge를 하나의 모형에서 구성하지 못했다.

따라서 **“반대 시간가지가 superpartner다”를 증명하지도, 보편적으로 반증하지도 못했다.**
이번에 닫힌 것은 그 주장을 local constraint closure나 양의 finite square-root toy만으로
증명하려는 두 지름길이다.

## 1. 사전등록과 적대검토 정정

사전등록 계약은 실행체보다 먼저 commit `c41b6a6`에 독립적으로 고정됐다. 계약의 exact gate는
그대로 실행됐지만, 원 계약에는 다음 두 조건의 판정 우선순위가 명시되지 않았다.

- formal cross block 또는 finite kernel map이 0이면 scoped `CONTRADICTS`
- 관계적 projector/domain/charge가 미구성이면 core `INCONCLUSIVE`

최초 실행체는 전자만 최종 출력에 사용하여 전체 core를 `CONTRADICTS`로 과장했다. 두 독립
적대검토가 다음을 지적했다.

- formal \(P_\pm\)는 relational spectral projector가 아니다.
- finite positive-kernel 행렬은 Moniz/Eder constraint의 truncation이 아니다.
- generic CAR closure는 Eder–Sahlmann quantum operator의 재현이 아니다.
- G4가 OPEN인 이상 core verdict는 `INCONCLUSIVE/UNCONSTRUCTED`여야 한다.

원 계약을 소급 수정하지 않고 별도 erratum에 최초 실행 SHA, 지적, corrected independent
classification을 기록했다. 최초 untracked 실행체 snapshot은 저장되지 않았으므로 그 SHA는
정보성이고, release-grade provenance는 corrected executable commit부터다.

## 2. E163 — formal Moniz-principal WKB control

Moniz의 \(k=+1\), complex scalar chiral multiplet을 포함한 4D \(N=1\) FRW reduction에서
한 spinor component의 SUSY constraint principal part는

\[
S_A^{\rm prin}
=-\frac{i}{\sqrt2}(1+\phi\bar\phi)\chi_A\partial_\phi
-\frac{a}{2\sqrt6}\psi_A\partial_a .
\tag{E163}
\]

formal phase

\[
\Psi_s=e^{is\lambda W(a,\phi,\bar\phi)},\qquad s=\pm1
\]

에 대해

\[
S_A^{\rm prin}\Psi_s
=\Psi_s\,s\lambda
\left[
\frac{1+\phi\bar\phi}{\sqrt2}\chi_A\partial_\phi W
-\frac{ia}{2\sqrt6}\psi_A\partial_a W
\right].
\]

즉 differential principal term은 \(s\)를 coefficient에 넣지만 \(e^{is\lambda W}\)를
\(e^{-is\lambda W}\)로 바꾸지 않는다. multiplicative lower-order term도 위상을 바꾸지 않는다.
반대 위상을 직접 교환하려면 reflection/Fourier-integral canonical relation 또는 anti-linear
conjugation 같은 추가 구조가 필요하다. 실행체는 conjugation이
\(K(i\Psi)=-iK(\Psi)\)라 complex-linear fermionic \(Q\)와 다름도 exact witness로 확인한다.

그러나 이것은 물리 branch 판정이 아니다.

- 코드의 \(W\)는 real Lorentzian Hamilton–Jacobi 식을 푼 source solution이 아니다.
- Moniz가 실제로 전개한 coefficient 해에는 \(e^{\pm3\sigma^2a^2}\) 같은 실지수 sector가 있다.
- 코드의 \(P_\pm=(I\pm\sigma_3)/2\)는 formal phase direct sum을 정의하므로 cross block 0은
  그 정의에 포함된다.
- clock 방향을 고정한 관계적 팽창/수축은 전체 covector \(dW\to-dW\)와 같다고 가정할 수 없다.
- Lorentz constraint, 허용된 full wavefunction sector, Hermitian-conjugate constraint와 physical
  inner product는 실행체에 없다.

따라서 E163의 inference는 `INCONCLUSIVE / FORMAL_WKB_SYMBOL`이다.

## 3. E164 — positive finite-kernel obstruction

Phase 5의 finite cochain differential을

\[
d=\begin{pmatrix}0&0&0\\0&0&0\\1&-1&0\end{pmatrix},
\qquad d^2=0
\]

로 두고

\[
\mathcal H
=\mathbb C^2_{\rm formal\ sheet}\otimes
\mathbb C^3_{\rm cochain}\otimes
\mathbb C^2_F,
\]

\[
Q=\sigma_1\otimes d\otimes\sigma_1,
\qquad
Q^\dagger=\sigma_1\otimes d^\dagger\otimes\sigma_1
\]

를 택했다. 이 \(Q\)는 off shell에서 formal sheet와 fermion parity를 모두 실제로 뒤집고

\[
Q^2=(Q^\dagger)^2=0,
\qquad
C=\{Q,Q^\dagger\}
=I_2\otimes\{d,d^\dagger\}\otimes I_2.
\tag{E164}
\]

exact spectrum은

\[
\operatorname{spec}C=\{0^{\times4},2^{\times8}\}.
\]

\(h=(1,1,0)^T\)로 toy kernel projector를

\[
P_0=I_2\otimes\frac{hh^\dagger}{h^\dagger h}\otimes I_2
\]

라 하면 네 formal-sheet/parity cell이 각각 rank 1로 실제 존재한다. off-shell 교차 block은
nonzero지만

\[
QP_0=Q^\dagger P_0=0,
\qquad
P_0P_-F_-QP_+F_+P_0=0
\tag{E165}
\]

이다. 이는 일반적인 양의 finite Hilbert space에서도

\[
0=\langle\Psi,C\Psi\rangle
=\|Q\Psi\|^2+\|Q^\dagger\Psi\|^2
\]

이므로 \(\ker C\subseteq\ker Q\cap\ker Q^\dagger\)라는 정리다.

하지만 이 유한 정리를 실제 Lorentzian local SUGRA에 바로 적용할 수는 없다. Moniz/Eder의
left/right constraint가 이 toy의 Hilbert adjoint pair라는 유도, 양의 physical inner product,
공통 self-adjoint domain, 그리고 \(C\)와 실제 gravitational constraint의 동일시가 전부 없다.
따라서 `CONTRADICTS`는 **positive finite-kernel class 내부**에만 해당한다.

## 4. E166 — closure는 sheet exchange를 선택하지 않는다

두 CAR mode \(a_A,a_A^\dagger\)와 formal sheet symbol
\(K=\operatorname{diag}(k,-k)\)에 대해

\[
S_A^L=K\otimes a_A,
\qquad
S_B^R=K\otimes a_B^\dagger
\]

를 잡으면

\[
\{S_A^L,S_B^R\}=\delta_{AB}K^2\otimes I,
\qquad
[S_A^{L/R},\sigma_3\otimes I]=0.
\tag{E166}
\]

따라서 odd closure가 nonzero여도 sheet 교차 block은 전부 0일 수 있다. 이는
“local-SUSY closure면 자동으로 branch exchange”라는 논리적 함의를 반박하는 generic
countercontrol이다.

이 계산은 Eder–Sahlmann의 source operator를 재현하지 않는다. 그 논문의 exact quantum
closure는 \(k=0,L\to\infty\) self-dual homogeneous-isotropic subclass에서 volume shift,
fermion \(\Theta\) term, reality inner product, ordering과 residual \(S^R\) structure term을 포함한다.
실행체는 이를 모두 생략했으므로 Eder source evidence로 세지 않는다. 그 문헌이 주는 정확한
교훈은 **actual 4D-derived minisuperspace에서도 local SUSY constraint closure 자체는 가능하다**는
것이지, expanding/contracting branch를 superpartner로 묶는다는 것이 아니다.

## 5. 결정적 G4가 아직 OPEN인 이유

핵심 주장을 판정하려면 같은 모형에서 최소한 다음을 구성해야 한다.

1. chiral clock을 포함한 4D \(N=1\) action에서 유도된 Lorentzian reduced constraint
2. self-adjoint relational expansion observable \(\Omega_T\)와 spectral projector
   \(P_\pm=\mathbf1_{\mathbb R_\pm}(\Omega_T)\)
3. constraint solution space를 보존하는 공통 domain과 conserved/positive physical product
4. local gauge constraint와 구별되는 nonzero reduced·residual·boundary fermionic charge
   \(Q_{\rm phys}\)
5. basis/gauge invariant한
   \(P_-Q_{\rm phys}P_+\ne0\) 및 반대 방향 map

현재 source들은 이 conjunction을 제공하지 않는다. Moniz 모형은 chiral matter와 explicit
first-order constraint를 주지만 일반적인 conserved current/physical inner product가 닫히지 않았다.
Eder–Sahlmann 모형은 일부 exact quantum closure와 kinematical Hilbert space를 주지만 ordinary
scalar clock을 그냥 붙일 수 없고, \(v>0/v<0\)는 triad orientation이지 팽창/수축 branch가 아니다.

따라서 G4는 `UNCONSTRUCTED`이고 core inference는 `INCONCLUSIVE`다.

## 6. T2 독립 분류

| target claim | fiber / layer | inference | novelty | registration | fitting risk |
|---|---|---|---|---|---|
| formal Moniz-principal phase retention | ALGEBRA / FORMAL_WKB_SYMBOL | INCONCLUSIVE | REPRODUCTION | PREREGISTERED + POST_HOC_CORRECTED | NOT_APPLICABLE |
| positive finite-kernel \(Q\) gives nonzero kernel map | ALGEBRA / ALGEBRAIC | CONTRADICTS | REPRODUCTION | PREREGISTERED + POST_HOC_CORRECTED | NOT_APPLICABLE |
| odd CAR closure forces sheet exchange | ALGEBRA / ALGEBRAIC | CONTRADICTS | REPRODUCTION | PREREGISTERED + POST_HOC_CORRECTED | NOT_APPLICABLE |
| opposite relational WKB branch = superpartner | PHYSICS / PHYSICS_MAPPING | INCONCLUSIVE / UNCONSTRUCTED | REPRODUCTION | PREREGISTERED + POST_HOC_CORRECTED | NOT_APPLICABLE |

- reproduction: corrected committed executable에서 exact matrix/symbol comparison, float tolerance 없음;
  21 PASS / 8 mutants rejected / exit 0.
- Bayes: `NOT_ESTIMABLE` — prior와 양쪽 likelihood가 없고 exact obstruction에 수치 posterior를
  붙이지 않는다.
- Lakatos: `UNDETERMINED` — 새 경험적 예측이나 독립 corroboration이 없고, 이번 cycle은
  ontology 승격보다 잘못된 지름길 두 개의 범위를 닫았다.
- KG action: `NONE`; ratification request: `none`.
- scientific verdict/programme appraisal: 각각 `UNJUDGED` / `UNAPPRAISED` 유지.

## 7. 순서 게이트의 실제 효과

사전등록한 Phase 13A support 조건에는 G4의 실제 구성이 필수였다. G4가 `UNCONSTRUCTED`이므로
core 연구 순서는 여기서 멈춘다.

- Phase 13B full spatial wall S-matrix는 수행할 수 있지만 **별도 auxiliary interface project**다.
- 그것이 non-null이어도 literal cosmological branch claim의 evidence weight는 0이다.
- 따라서 이번 core cycle에서는 Phase 13B, 이산/anomaly-fixed wall, higher-derivative bounce로
  자동 진입하지 않았다.
- pre-Big-Bang branch 자체를 유지하고 싶다면 CPT-symmetric cosmology가 별도 fork이지만,
  CPT를 fermionic \(Q\)로 부르지 않는다.

이는 실패를 피한 것이 아니라 사전등록된 stop rule을 지킨 것이다.

## 8. 재현·공학 receipt

- `python3 -m json.tool cpt_temporal_folded_susy/PHASE13A_RESEARCH_CONTRACT.json` → PASS.
- `python3 -m json.tool cpt_temporal_folded_susy/PHASE13A_ADVERSARIAL_ERRATUM.json` → PASS.
- `python3 -m py_compile cpt_temporal_folded_susy/phase13a_lorentzian_branch_supercharge.py` → PASS.
- `./ice doctor` → locked Node/Python/SymPy runtime `READY`.
- `./ice info phase13a_lorentzian_branch_supercharge` → catalog 등록, mapped legacy output 없음.
- `./ice run phase13a_lorentzian_branch_supercharge` at commit `46551e6` →
  21 exact PASS / 8 mutants rejected / exit 0.
- 두 독립 read-only adversarial replay → 같은 count/exit 및 corrected scope `PASS`.
- `git diff --check` → PASS.

## 9. 출처와 범위

- P. V. Moniz, “Conserved Currents in Supersymmetric Quantum Cosmology?” — matter-coupled
  \(k=+1\) FRW의 explicit first-order SUSY constraint와 conserved-current 한계:
  [arXiv:gr-qc/9606047](https://arxiv.org/abs/gr-qc/9606047)
- K. Eder, H. Sahlmann, “Supersymmetric minisuperspace models in self-dual loop quantum
  cosmology” — 4D \(N=1\) 유도 homogeneous-isotropic model의 source-scoped exact closure:
  [arXiv:2010.15629](https://arxiv.org/abs/2010.15629)
- R. Capovilla, J. Guven, “Super-Minisuperspace and New Variables” — Bianchi A에서의 classical
  constraint-algebra 보존과 formal inner-product 한계:
  [arXiv:gr-qc/9402025](https://arxiv.org/abs/gr-qc/9402025)
- M. Wulf, “Non-closure of constraint algebra in N=1 supergravity” — full-theory ordering
  nonclosure 경고와 unregularized 범위:
  [arXiv:gr-qc/9606046](https://arxiv.org/abs/gr-qc/9606046)
- 역사적 중복 경계: Phase 3의 local constraint/global charge 구분
  (`PHASE3_REPORT.md`, SHA-256 `2265a158...`)과 Phase 5의
  `FINITE_ANALOGY_NOT_SUGRA` cochain (`PHASE5_REPORT.md`, SHA-256 `bc9959e0...`).

## 10. 파일

- 실행체: [`phase13a_lorentzian_branch_supercharge.py`](phase13a_lorentzian_branch_supercharge.py)
- 원 사전등록: [`PHASE13A_RESEARCH_CONTRACT.json`](PHASE13A_RESEARCH_CONTRACT.json)
- 적대검토 정정: [`PHASE13A_ADVERSARIAL_ERRATUM.json`](PHASE13A_ADVERSARIAL_ERRATUM.json)
- 선행 Phase 12: [`PHASE12_BOUNDARY_TWIST_INTERFACE.md`](PHASE12_BOUNDARY_TWIST_INTERFACE.md)
- 후속 charge-first audit:
  [`PHASE14A_CHIRAL_CLOCK_CHARGE_FIRST.md`](PHASE14A_CHIRAL_CLOCK_CHARGE_FIRST.md) — residual,
  spatial-boundary, bulk channels을 분해했지만 canonical bridge 미구성으로 literal-core 판정은 유지
