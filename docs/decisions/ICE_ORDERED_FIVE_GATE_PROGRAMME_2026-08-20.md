# ICE 양자중력 후보의 순차적 다섯 관문

> **상태:** ACTIVE programme workflow
> **기원:** 2026-08-20 사용자 지정 연구 순서
> **권한:** CPT × Temporal-Folded SUSY core route의 claim 승격 순서를 정한다.
> **비권한:** 과학적 evidence, preregistration, 완성된 양자중력 이론의 선언, 또는 각
> 관문의 성공을 미리 보증하는 문서가 아니다.

## 1. 결정

ICE_ORCA_DRAGON의 현재 local-fold 결과를 물리적 SUSY spectrum 주장으로 승격하려면 다음
다섯 typed gate를 순서대로 닫는다.

1. **원래 cycle과 signed global intersection**
   원래 lapse relative cycle을 fold 전체로 운반하여 signed intersection과 global contour를
   고정한다.
2. **Hard CFU 계수**
   선택된 cycle에 대한 regular hard quotient와 Airy/Airy-prime 계수를 계산한다.
3. **Full BFV/Pfaffian line과 Pin holonomy**
   선택된 saddle 조합 위에서 boson--fermion--ghost 전체 BFV/Pfaffian line과 Pin holonomy를
   계산한다.
4. **Spinorial charge와 common domain**
   그 holonomy가 conserved spinorial charge와 하나의 공통 physical domain을 보존하고 전체
   constraint algebra와 anomaly 없이 닫히는지 검사한다.
5. **Persistent order와 pole splitting**
   마지막으로 지속적 order parameter와 interacting boson/fermion retarded-pole splitting을
   계산한다.

Gate 번호는 Phase 번호와 일대일로 고정하지 않는다. 한 gate가 여러 Phase를 요구할 수 있고,
한 Phase가 한 gate의 obstruction만 발견할 수도 있다.

## 2. Phase 37에서 물려받은 경계

Phase 37은 세 유한 enclosing loop에서 local BVP root-cover의 비자명한 \(\mathbb Z_2\)
monodromy와, 표본 사이에 미해결 zero 또는 alias winding이 없다는 조건 아래 reduced bosonic
half-form의 order-four conjugacy class를 기록했다. 동시에 다음을 구별했다.

\[
\text{root cover}
\ne\text{Airy solution space}
\ne\text{relative-cycle Gauss--Manin map}
\ne\text{fermion Pfaffian/Pin line}
\ne Q_{\rm SUSY}.
\]

따라서 Phase 37의 holonomy를 Gate 1--4의 결과로 재명명하지 않는다. Bare root swap은
Phase-17 local/exchange charge의 parity-controlled basis equivalence도 깨지 않는다.

## 3. Gate 1 — original **joint** cycle과 signed intersections

사용자 문구의 “lapse relative cycle”은 출발점이지만, 현재 fold는 field boundary-value
solutions의 soft mode가 합쳐지는 곳이다. 그러므로 completion object는 다음처럼 강화한다.

\[
\Gamma_{\rm original}^{\rm joint}
\in H_{\rm rel}(\mathcal X_{\rm lapse}\times\mathcal X_{\rm fields}
\times\mathcal X_{\rm gauge};\mathcal X_{\rm bad}) .
\]

즉 lapse projection만이 아니라 field/momentum contour, endpoint polarization, gauge/BFV body와
orientation line을 함께 명시해야 한다. 이는 새 결론을 추가하는 것이 아니라 고차원
intersection의 type를 맞추는 보강이다.

입력:

- 결과를 보기 전에 명시한 original lapse--field relative class와 orientation;
- singular divisor, endpoint prescription, regulator와 Stokes chamber;
- 모든 관련 saddle, upward cycle, complex sheet와 asymptotic end의 census.

성공 출력:

\[
n_\sigma=\langle\Gamma_{\rm original}^{\rm joint},K_\sigma\rangle\in\mathbb Z
\]

의 완전한 oriented vector, 그리고 허용된 homotopy, gauge choice, regulator refinement에서의
안정성이다. 아래-origin/위-origin contour가 둘 다 허용되면 둘을 독립 가설로 계산한다.

실패·중단 조건:

- projected lapse crossing이 full joint space에서 비횡단이거나 field fibers가 만나지 않음;
- 추가 crossings의 signed cancellation;
- 누락 sheet, unclassified box exit, singular end 또는 Stokes jump;
- cutoff나 작은 contour deformation에 따른 crossing 수·부호 변화;
- original cycle이 수렴 relative class 또는 BRST-closed object가 아님.

한 local crossing이나 bounded arm은 Gate 1을 닫지 않는다. \(n_\sigma=0\)이 완전한 계산에서
나오면 그것도 유효한 negative resolution이며, 계산 실패가 아니다.

## 4. Gate 2 — hard CFU Airy/Airy-prime coefficients

Gate 1이 고정한 cycle vector를 canonical fold chart로 옮겨

\[
\mathcal K(\zeta)
=A(\zeta)\operatorname{Ai}(\lambda^{2/3}\zeta)
+\lambda^{-1/3}B(\zeta)\operatorname{Ai}'(\lambda^{2/3}\zeta)
\]

의 regular even/odd hard coefficients를 유도한다.

성공 조건:

- regular hard determinant quotient가 fold에서 nonzero이고 orientation을 가짐;
- \(A,B\)가 두 outer saddle amplitudes에서 유도되고 overlap 영역에서 다시 일치함;
- soft \(\zeta^{-1/4}\) factor를 CFU kernel과 이중 계수하지 않음;
- remainder/error 또는 명시한 asymptotic scope가 있음;
- Gate-1 cycle/Stokes coefficient와 absolute phase convention이 일관됨.

Airy ODE의 regularity, root permutation, 또는 separate-saddle determinant만으로는 Gate 2가
닫히지 않는다.

## 5. Gate 3 — full BFV/Pfaffian line과 Pin holonomy

Gate 1--2가 정한 saddle combination 위에서 metric, matter, chiralino, gravitino, Goldstino,
lapse/shift, multiplier와 ghost를 같은 regulator와 boundary condition으로 양자화한다.

성공 조건:

- constraint reduction, zero-mode/collective-coordinate 처리와 renormalization;
- bosonic determinant와 fermion/ghost Pfaffian의 실제 line bundle 및 common orientation;
- gauge-fermion과 regulator 변화에 대한 physical ratio/holonomy의 독립성;
- spectral flow, anomaly, Clifford reflection cocycle와 spacetime Pin lift;
- closed physical loop의 basis-independent holonomy.

Reduced endpoint-Jacobi \(d^{-1/2}\), finite bosonic sign, 또는 determinant만으로 추정한
Pfaffian sign은 Gate 3 evidence가 아니다.

## 6. Gate 4 — conserved spinorial charge, domain, constraint closure

Gate 3의 line과 holonomy 위에 fermion-odd Lorentz-spinor charge \(Q_\alpha\) 또는 local-SUGRA
constraint를 정의한다.

성공 조건:

- 하나의 양의 physical inner product와 common self-adjoint domain;
- time evolution/interface와의 conservation 또는 정확한 constraint intertwining;
- Hamiltonian, momentum, Lorentz, gauge, local-SUSY/BFV constraints와 anomaly-free closure;
- source/local observable algebra와 compatible한 action;
- basis change로 제거되지 않는 global consistency 또는 obstruction.

여기에는 두 갈래가 있다.

1. **Preserved-law branch:** 전역 \(Q\)가 존재하고 법칙을 보존한다. Gate 5의 breaking은
   vacuum/state의 spontaneous breaking이어야 한다.
2. **Obstructed-charge branch:** holonomy/domain/anomaly가 전역 \(Q\)를 막는다. 이는 conserved
   temporal supercharge가 아니라 explicit/global SUSY obstruction으로 이름을 바꾼다.

두 설명을 동시에 사용하지 않는다. Finite \(2\times2\) sheet intertwiner의 존재나 nullity는
Gate 4를 닫지 않는다.

## 7. Gate 5 — persistent order parameter와 interacting poles

Gate 4와 compatible한 branch에서 finite-energy persistent carrier를 유도한다. 후보가
\(F\), \(D\), flux sector, memory kernel 또는 vacuum order라면 그 동역학과 mediation을 action에서
계산한다.

성공 조건:

- seam/fold 이후 long-time limit에도 남는 gauge-invariant order parameter;
- interacting retarded self-energies \(\Sigma^R_B,\Sigma^R_F\)와 renormalized complex poles;
- matched trivial-holonomy, zero-order-parameter와 seam-off ablation;
- transient occupation 차이와 asymptotic pole 차이의 분리;
- FRW dilution/backreaction, vacuum lifetime와 visible-sector mediation의 통제.

Free equal-mass bulk에서 state occupation만 달라지는 것은 Gate 5 성공이 아니다. Preserved-law
branch라면 Ward identity, Goldstino와 spontaneous-breaking 조건도 함께 만족해야 한다.

## 8. 승격 순서와 탐색 허용 범위

Core claim promotion 순서는 엄격하다.

```text
Gate 1 typed cycle vector
→ Gate 2 absolute uniform kernel
→ Gate 3 physical determinant/Pfaffian/Pin line
→ Gate 4 physical Q/domain 또는 obstruction
→ Gate 5 persistent interacting spectrum
```

Downstream 탐색 계산을 미리 실행하는 것은 허용한다. 그러나 앞 gate의 typed output을 가정한
조건부 계산은 그 앞 gate가 evidence로 닫히기 전에는 programme의 물리적 진전으로 승격하지
않고 `CONDITIONAL`로 표시한다. 순서는 계산 금지가 아니라 claim 의존성이다.

Gate 4의 trivial 또는 obstructed 결과처럼, 질문을 완전히 답했지만 선호 경로에는 불리한
결과도 epistemic resolution이다. 다만 다음 gate를 unlock하려면 단순 `RESOLVED`가 아니라 그
gate가 요구하는 compatible typed output이 필요하다.

## 9. 실패, no-go와 상태 규칙

- 한 solver·ansatz·candidate의 실패: 해당 scoped claim만 `CONTRADICTED`; gate는 `OPEN`.
- scope 전체의 완전한 obstruction/no-go: 별도 evidence-backed negative claim으로 gate를 닫고
  해당 core route를 중단한다.
- positive construction: `SUPPORTED` claim, evidence, scope, report와 mutation controls를 붙인다.
- underdetermination: `INCONCLUSIVE` 또는 `BRANCH`; 선호 branch를 임의 선택하지 않는다.
- basis/gauge equivalence: `EQUIVALENCE`; 새 ontology를 만들지 않는다.

`PASS` check는 그 check statement가 계산됐다는 뜻이지, gate 전체가 성공했다는 뜻이 아니다.

## 10. 기존 open ledger와의 연결

| Gate | 기존 연구 채무 |
|---|---|
| 1 | `open:p28-global-relative-homology-and-intersection`, `open:p33-airy-cycle-amplitude-and-global-continuation`, `open:p37-global-cycle-hard-cfu-full-bfv-pfaffian-gate` |
| 2 | `open:p33-airy-cycle-amplitude-and-global-continuation`, `open:p36-original-cycle-hard-determinant-and-global-bfv-state` |
| 3 | `open:p28-full-gauge-reduced-superdeterminant`, `open:p17-pin-clifford-lift`, `open:p32-cpt-pin-lapse-class-selection` |
| 4 | `open:p17-conserved-charge`, `open:p17-gluing-domain`, `open:p17-projector-charge-compatibility`, `open:p17-reality-positivity-junction`, `open:full-4d-sugra-interface` |
| 5 | `open:p18-persistent-order-parameter`, `open:p18-interacting-wigner-self-energies`, `open:p18-frw-backreaction`, `open:p18-higgs-power-sensitivity` |

새 gate nodes는 이 채무를 지우거나 복제하지 않고, 필요한 출력의 순서를 명시한다.

## 11. 순서 자체의 재귀 감사

이 다섯 단계는 사용자 지정 core workflow이지 자연법칙이 아니다. 더 직접적인 formulation이
hard CFU를 우회하거나, Gate 3 계산이 Gate 1의 contour class를 추가로 제한할 수 있다. 그런
경우 계산은 병렬로 수행하되 최종 joint fixed point가 모든 typed consistency를 만족하는지
검사하고 이 문서를 개정한다.

각 gate는 원하는 결론을 보호하는 면책이 아니다. 특히 다음 질문을 순서 자체에도 적용한다.

- Gate를 제거해도 같은 observable이 유도되는가?
- 다른 formulation에서 같은 invariant로 수렴하는가?
- downstream 결과를 보고 upstream contour를 역설계하지 않았는가?
- 각 단계가 추가한 자유도보다 더 많은 가능한 결과를 실제로 배제하는가?

## 12. 허용되는 언어

다섯 gate가 현재 homogeneous/one-loop scope에서 모두 성공해도 우선 허용되는 명칭은
`globally selected gauge-consistent quantum-cosmology/SUGRA sector with a derived SUSY-breaking mechanism`
이다. 완성된 양자중력 이론을 주장하려면 full 3+1 dimensional local modes, arbitrary-background
constraint algebra, regulator-independent continuum or UV completion, positive physical state,
unitarity/causality, GR+QFT low-energy recovery와 독립 관측 discriminator가 추가로 필요하다.

## 13. Phase evidence 통합 규칙

각 후속 Phase는 최소한 다음을 기록한다.

- 어느 gate의 어떤 typed input/output을 시험했는가;
- 계산 전 고정한 contour/domain/regulator와 결과 의존 선택의 분리;
- exact/numerical checks와 최소 mutation 또는 negative control;
- `computed`와 `not_computed` scope;
- positive, negative, branch, equivalence 또는 open 판정;
- 다음 gate를 unlock했는지, 아니면 한 candidate만 닫았는지.

첫 후속 계산인 Phase 38은 Gate 1 전체의 성공을 전제하지 않는다. 먼저 Phase-32의 projected
crossing과 Phase-34--37의 local fold data가 original **joint** relative cycle 및 global integer
vector를 유일하게 정하는지 공격한다.
