# ICE 양자중력 계산 워크벤치 실행 DAG

> 작성일: 2026-08-28
> 지위: 새 계산을 위한 설계 문서. 이 문서는 물리학 결론, 양자중력 이론, 관측 예측 또는 TOE 주장이 아니다.

## 목적과 경계

이 문서는 현재 워크벤치에서 남아 있는 여섯 연구 연결부를 **작고 독립적인 계산 단위**로 나눈다.
각 단위는 결과가 참이든 거짓이든 다음 단위를 자동으로 승인하지 않는다. 결과가 특정 장애물을
직접 줄였을 때에만 사람이 다음 단위를 선택한다.

현재 적용 중인 운영 경계는 다음과 같다.

- 새 계산기는 번호 없는 이름을 사용하고, committed clean source에서만 `./ice run`으로 실행한다.
- 공통 상한은 실행 시간 120초, stdout/stderr 각각 262,144 bytes, 변경 산출물 12개와 총 1,000,000 bytes다.
- 과거의 소진된 one-shot 계산기, 재구성 launch/replay 경로, 그리고 그 후손을 재실행·복제·개명하지 않는다.
- 직접 Python 실행, 자동 후속 실행, 결과를 근거로 한 물리학/TOE 승격은 허용되지 않는다.
- 외부 자료와 대형 likelihood 파일은 일반 Git에 넣지 않는다. URL, version, licence, checksum,
  fetch 방법만 추적하고, 실제 내려받기와 실행은 별도 승인된 환경에서 한다.

여기서 `완료`는 워크벤치가 좁게 선언한 계산을 마쳤다는 뜻이며, 물리적 해석의 완성이 아니다.
`오픈`은 아직 직접 계산할 수 있는 질문, `차단`은 현재 입력이나 선행 결과가 부족하여 계산해도
주장 범위를 넘게 되는 질문이다.

## 현재 기준선

| 상태 | 이미 있는 좁은 근거 | 아직 말할 수 없는 것 |
|---|---|---|
| 완료 | `gate1_v0_improved_static_bfv_source`: 한 Darboux 성분의 Abelian BFV zero-mode source algebra | full trajectory, absolute BFV measure, physical state |
| 완료 | `gate1_v0_bfv_m2_spectral_trajectory`: 한 formal nonzero mode의 상대 determinant/Pfaffian 대조 | zero-mode completion의 유일성, continuum measure |
| 완료 | `gate1_v0_bfv_zero_mode_elimination_ward`: determinant-weighted zero-ghost elimination 대 단순 삭제 구분 | lapse contour, modulus, BRST cohomology |
| 완료 | `gate1_v0_bfv_finite_pfaffian_orientation_transport`: finite odd block의 상대 orientation transport | bosonic contour, absolute Pfaffian line, gluing |
| 완료 | `gate1_v0_closed_s3_scalar_harmonic_projection_ledger`: zonal scalar (S^3), (L=2)의 projection remainder | ADM/HDA, Jacobi, anomaly 또는 BFV charge |
| 완료 | 역사적 closed-inflation background control: 두 (V\ne0) potential의 closed-FRW 해 존재성 | initial state 선택, perturbation, reheating, observational prediction |
| 완료 | 역사적 toy clock/rigging calibration | 실제 closed-inflation operator의 relational quantum theory |
| 오픈 | raw constraint의 전역 domain/RAQ, full (S^3) ADM/HDA, classical/quantum BFV, amplitude gluing, relational observables, BO/decoherence | 이들을 하나의 물리 이론으로 결합한 결론 |
| 차단 | 현재 (V=0) massless-scalar local model에서 CMB likelihood 직접 평가 | inflation/reheating/primordial spectrum이 정의되지 않음 |

역사적 실행체의 이름은 provenance 참조일 뿐 새 계산 이름의 템플릿이 아니다.

## 2026-08-28 실행 갱신

이번 작업에서 아래의 번호 없는 계산을 clean committed source로 실행했다. 표의 `완료`는
각 행의 좁은 계산 범위만 뜻한다.

| 연결부 | 실제로 계산된 것 | 관측 결과 | 남은 필수 단계 |
|---|---|---|---|
| 1 raw-\(C\) domain | `raw_c_constant_boundary_direct_integral` | 선언한 \(\Gamma_{1,p}=0\) line이 하나의 measurable, \(p\)-보존 decomposable 자기수반 확장을 이룸; exact 6/6, numerical 2/2 | 일반 \(p\)-mixing 분류와 물리적 boundary 선택 |
| 1 raw-\(C\) zero shell | `raw_c_zero_shell_characteristic_census` | \(\kappa\in[0,8]\) sign-changing root 5개; \(F(0)<0\); exact 4/4, numerical 4/4 | \(\lambda_j(p)\) branch와 transversality, spectral normalization, test space, rigging form |
| 2 closed \(S^3\) convention | `closed_s3_adm_linear_scalar_convention_audit` | homogeneous ADM/raw-\(C\) convention과 제한된 linear-zonal identities; exact 43/43 | complete SVT 및 실제 linear constraint brackets |
| 2 harmonic derivative ledger | `closed_s3_scalar_derived_harmonic_ledger` | scalar-derived norm, \(n=0,1\) degeneracy와 derivative identities; exact 26/26 | transverse bases와 full Gaunt/Clebsch--Gordan data |
| 2 nonlinear cutoff control | `closed_s3_zonal_scalar_convolution_cutoff_ledger` | cubic pairing projection 차이는 정확히 0이지만, 세 packet의 quadratic leakage와 iterated-convolution residual은 nonzero; exact 284/284 | full cubic ADM constraint, lapse/shift brackets, HDA/Jacobi scaling |
| 4 finite BFV amplitude control | `bfv_parametrized_particle_gluing_calibration` | affine toy에서 full-real lapse distribution, endpoint kernel, ordered Pfaffian, \(+i0\), short-time limit과 two-slab glue를 함께 고정; exact 8/8, numerical 1/1 | gravity contour, Gribov census, continuum determinant line과 absolute/glued amplitude |
| 5 two clocks | `v0_two_clock_relational_observable_comparison` | \(V=0\)의 \(\phi\)-clock과 \(P\)-clock은 공통 classical chart에서 역관계; \(Q\)-clock은 \(P=0\)에서 FP zero; exact 17/17 | quantum clock map, physical product, \(V\ne0\) turning-point chart |
| 6 \(V\ne0\) background | `closed_starobinsky_background_export_audit` | 선언한 \(M=1.3\times10^{-5}\), \(N_*=50,55,60\) leading slow-roll 표; exact 6/6, residual 9/9 | closed-mode evolution, initial state/reheating, BO/decoherence, spectrum adapter와 likelihood |

따라서 3의 중력 BFV charge는 아직 실행 가능한 입력을 갖지 못한다. 4의 finite toy 성공은 3의
structure functions를 대신하지 않으며, 6의 background 표도 primordial spectrum을 대신하지 않는다.
각 후속 runner는 바로 앞 결과가 아니라 위 표의 “남은 필수 단계”를 직접 겨냥해야 한다.

## 2026-08-29 실행 갱신

세 개의 새 번호 없는 계산을 각각 clean definition commit 뒤 `./ice run`으로 실행하고, committed
result를 별도 임시 사본에서 `./ice repro --only ...`로 재현했다. 세 재현 모두 `REPRO`,
`needs-attention 0`이었다.

| 연결부 | 실제로 계산된 것 | 관측 결과 | 줄어든 장애물 | 그대로 남은 장애물 |
|---|---|---|---|---|
| 1 raw-\(C\) zero shell | `raw_c_zero_shell_transversality_jacobian` | 5개 root에서 \(F_\kappa\ne0\), weighted Mellin norm과 5회 quadrature 일치, 조건부 \(1/|\lambda'|\approx0.0641\)–\(0.0747\); boolean 9/9, numerical 3/3 | 선언한 5개 root의 local simplicity와 local weight 후보를 수치로 고정 | \(F_\lambda\)는 moving-boundary Lagrange identity에 조건부다. nonzero-\(\lambda\) Weyl solve, global spectral measure, test space, rigging map과 RAQ는 null |
| 2 closed \(S^3\) all-sector bookkeeping | `closed_s3_full_svt_spectral_ledger` | source-pinned scalar/transverse-vector/TT low-mode transport와 cutoff count; exact 37/37, theorem guard 5; \(N=8\) 총 1,341 modes | 세 sector의 rough/Hodge/명시적 Lichnerowicz convention, 저차 예외와 count 범위를 한 packet에 고정 | `FULL_SVT`는 세 sector를 모두 기록했다는 뜻뿐이다. explicit basis, chirality resolution, Gaunt/Clebsch--Gordan, ADM/HDA는 null |
| 5–6 \(V\ne0\) two-clock domain | `homogeneous_closed_frw_starobinsky_two_clock_fp_domain_audit` | \(C_V=0=P\)에서 real-\(p\) domain \(y=e^QV\le3\), scalar-clock zero \(y=3\), \(P\)-clock FP zero \(y=2\), \(Q\)-clock factor zero; exact 12/12 | 이전의 잘못된 informal \(y=3/2\) 값을 제거하고 두 clock chart의 서로 다른 고전 경계를 고정 | 실제 trajectory가 어느 locus를 통과하는지, complete observable, quantum clock map, physical product, BO/decoherence와 likelihood는 null |

이 갱신은 세 갈래를 완성하지 않았다. 다음 독립 질문은 각각 (a) nonzero-\(\lambda\) plus-end
Weyl solution으로 \(F_\lambda\)를 직접 대조하는가, (b) 명시적 저차 SVT representative와 Gaunt
data를 구성해 source convention을 실제 ADM coefficient 입력으로 바꾸는가, (c) 고정된
Starobinsky closed-FRW initial data로 trajectory와 두 FP locus의 crossing 여부를 적분하는가이다.
어느 결과도 다른 질문의 실행 또는 물리적 승격을 자동 승인하지 않는다.

## 의존성 지도

```text
1 raw-C global operator / RAQ
  └─► 1.4 rescaling-equivalence comparison

2 ADM + S3 harmonic constraints
  └─► 2.4 cubic HDA/Jacobi + cutoff remainder
        └─► 3.1 classical BFV charge
              └─► 3.2 quantum BFV common-core audit

4 boundary/contour/Pfaffian/gluing
  ├─► 4.2 fixed-lapse superdeterminant
  ├─► 4.3 gauge-slice/Gribov census
  └─► 4.4 relative contour and 4.5 two-slab gluing

5 two-clock relational observables
  ├─► 5.2 quantum clock comparison
  └─► 5.3 perturbative relational variable             ◄── 2.3

6 V!=0 BO/decoherence/likelihood
  ├─► 6.2 closed-inflation mode equation
  ├─► 6.3 BO consistency                                  ◄── 5.1, 5.2
  ├─► 6.4 decoherence influence calculation               ◄── 6.2
  └─► 6.5 spectrum adapter ─► 6.6 likelihood smoke        ◄── 6.2, 6.3, 6.4
```

화살표는 논리적 의존성이다. 병렬 가지의 실행 권한이나 자동 실행 순서를 뜻하지 않는다.

## 1. raw constraint: direct-integral 자기수반 확장과 RAQ

### 1.1 `raw_c_fiber_boundary_data`

| 항목 | 내용 |
|---|---|
| 입력 | raw (C)의 정확한 differential expression, kinematical measure, fixed-(p) fiber, endpoint convention |
| 계산 | 각 fiber의 minimal/maximal domain, boundary form, deficiency index, candidate boundary maps를 symbolic 또는 certified numerical ledger로 검사 |
| 출력 | fiber별 limit-point/limit-circle 표, deficiency data, boundary-map convention, `UNRESOLVED` fiber 목록 |
| 성공 의미 | 지정한 fiber family에 대해 어떤 self-adjoint extension 자료가 필요한지 명확해진다 |
| 실패 의미 | expression 또는 measure에서 domain이 닫히지 않거나 data가 부족함을 기록한다. 선택된 (H)와의 비동치는 아직 판단하지 않는다 |
| 의존성 | 없음 |

### 1.2 `raw_c_direct_integral_measurability`

| 항목 | 내용 |
|---|---|
| 입력 | 1.1의 fiber boundary data, (p)-measure, candidate extension family `theta(p)` 또는 `U_p` |
| 계산 | measurable graph/resolvent 조건, direct-integral domain, decomposability와 symmetry covariance를 검사 |
| 출력 | global operator/domain의 정확한 정의 또는 measurable-family obstruction |
| 성공 의미 | 선언한 family 하나가 전역 self-adjoint operator를 정의한다는 operator-theoretic 결과 |
| 실패 의미 | 그 family가 전역 operator를 정의하지 못함. 다른 family의 부재를 뜻하지 않는다 |
| 의존성 | 1.1 |

### 1.3 `raw_c_raq_zero_fiber`

| 항목 | 내용 |
|---|---|
| 입력 | 1.2 operator, dense test space, lapse/group-average regularization, physical sesquilinear-form convention |
| 계산 | spectral/distributional zero fiber, rigging form positivity, null quotient와 candidate observable action을 검사 |
| 출력 | RAQ form, its null space, regularization dependence ledger |
| 성공 의미 | 선언한 operator와 test space에 대한 physical-form 후보가 정의된다 |
| 실패 의미 | zero fiber가 singular하거나 form이 positive/finite가 아님을 기록한다 |
| 의존성 | 1.2 |

### 1.4 `constraint_rescaling_quantum_comparison`

| 항목 | 내용 |
|---|---|
| 입력 | 1.3 raw-(C) RAQ data, 비교 대상 (H=fC)의 domain/RAQ data, 허용 intertwiner와 observable class |
| 계산 | spectral multiplicity, zero-fiber measure, domain map, selected observable intertwining을 비교 |
| 출력 | `EQUIVALENT_IN_DECLARED_CLASS`, `INEQUIVALENT_WITNESS`, 또는 `OPEN` |
| 성공 의미 | 명시한 class 안에서만 양자 동치 또는 반례가 나온다 |
| 실패 의미 | 비교에 필요한 domain/observable이 정의되지 않았음을 뜻한다 |
| 의존성 | 1.3 및 비교 대상의 독립 domain audit |

## 2. closed (S^3) ADM constraint와 cutoff remainder

### 2.1 `s3_adm_constraint_convention_audit`

| 항목 | 내용 |
|---|---|
| 입력 | closed-FRW+scalar ADM action, metric signature, lapse/shift, Poisson bracket, harmonic normalization |
| 계산 | homogeneous (H,D), variation, sign, density weight, background constraint를 exact check |
| 출력 | machine-readable convention ledger와 identity checks |
| 성공 의미 | 이후 mode calculation이 공유할 하나의 ADM convention을 고정한다 |
| 실패 의미 | 출처 또는 convention이 충돌함을 드러내며 후속 bracket 계산을 막는다 |
| 의존성 | 없음 |

### 2.2 `s3_svt_harmonic_gaunt_ledger`

| 항목 | 내용 |
|---|---|
| 입력 | 2.1 convention, complete scalar/vector/tensor harmonic basis, 작은 cutoff (L) |
| 계산 | orthonormality, Laplacian eigenvalue, parity, derivative identities, Gaunt selection rules와 product tails |
| 출력 | SVT normalization/Gaunt ledger와 retained/discarded mode map |
| 성공 의미 | zonal-only 기준선을 full SVT bookkeeping으로 확장한다 |
| 실패 의미 | chosen basis가 complete하거나 compatible하지 않음을 기록한다 |
| 의존성 | 2.1 |

### 2.3 `s3_adm_linear_constraint_modes`

| 항목 | 내용 |
|---|---|
| 입력 | 2.1–2.2, first-order perturbative constraints, declared mode cutoff |
| 계산 | (C^{(1)},D^{(1)}) coefficient와 (DD,DH,HH) bracket을 full-before-project 방식으로 비교 |
| 출력 | modewise bracket ledger, exact equality/remainder 분리 |
| 성공 의미 | 지정한 선형 차수에서 HDA의 구현을 확인한다 |
| 실패 의미 | convention/sign/missing mode 또는 finite projection remainder를 구분해 남긴다 |
| 의존성 | 2.1, 2.2 |

### 2.4 `s3_adm_cubic_hda_remainder`

| 항목 | 내용 |
|---|---|
| 입력 | 2.3와 cubic order까지의 constraint expansion, cutoffs (L,L+1,L+2) |
| 계산 | quadratic-order bracket에는 필요한 cubic contributions를 포함하고, Jacobiator와 cutoff scaling을 검사 |
| 출력 | continuum identity check, projected remainder, cutoff-scaling table, unclassified term ledger |
| 성공 의미 | truncation remainder와 algebraic inconsistency를 분리할 근거가 생긴다 |
| 실패 의미 | exact finite closure 실패 자체는 anomaly 판정이 아니다. scaling과 origin을 추가 기록한다 |
| 의존성 | 2.3 |

## 3. BFV charge와 quantum anomaly audit

### 3.1 `s3_classical_bfv_charge_nilpotency`

| 항목 | 내용 |
|---|---|
| 입력 | 2.4의 verified classical structure functions, ghost canonical pairs, grading/sign convention |
| 계산 | (Omega=C_Ac^A-\tfrac12U^C{}_{AB}c^Ac^B\mathcal P_C+\cdots)와 ({\Omega,\Omega})를 declared truncation까지 계산 |
| 출력 | classical BFV charge, nilpotency ledger, inherited projection remainder |
| 성공 의미 | 지정한 고전 truncation에서 BFV encoding이 HDA와 맞는다 |
| 실패 의미 | source algebra 또는 truncation이 BFV charge를 지지하지 못한다. 양자 anomaly 주장은 없다 |
| 의존성 | 2.4 |

### 3.2 `s3_quantum_bfv_common_core_audit`

| 항목 | 내용 |
|---|---|
| 입력 | 3.1, ordering, regulator, finite Fock/Schwartz-type core, adjoint/inner-product convention |
| 계산 | common invariant core, operator products, matrix elements of (widehat\Omega^2), regulator/cutoff dependence |
| 출력 | domain inclusion table, nilpotency defect decomposition, scaling data |
| 성공 의미 | 선언한 regulated representation에서만 (widehat\Omega^2=0) 또는 명시된 defect가 확인된다 |
| 실패 의미 | defect를 ordering/domain/regulator/truncation 중 가능한 원인으로 분해한다. 전체 양자중력 no-go가 아니다 |
| 의존성 | 3.1 |

## 4. boundary·contour·Pfaffian·gluing BFV amplitude

이 가지는 3의 inhomogeneous BFV charge와 궁극적으로 만나야 하지만, 아래 finite boundary controls는
독립적으로 먼저 수행할 수 있다. 어떤 finite control도 absolute measure를 산출하지 않는다.

### 4.1 `bfv_boundary_polarization_pairing`

| 항목 | 내용 |
|---|---|
| 입력 | finite constrained model, two endpoint polarizations, boundary symplectic potential, gauge fermion |
| 계산 | gauge-fermion variation의 boundary term, BFV pairing, endpoint ideal compatibility |
| 출력 | polarization-pairing identity 또는 mismatch ledger |
| 성공 의미 | 선언한 finite model에서 boundary convention이 내부 BFV algebra와 양립함 |
| 실패 의미 | amplitude construction 전에 endpoint prescription을 수정해야 함 |
| 의존성 | 없음 |

### 4.2 `bfv_fixed_lapse_superdeterminant`

| 항목 | 내용 |
|---|---|
| 입력 | 4.1, finite time lattice, same-regulator boson/ghost blocks, zero-mode rule |
| 계산 | fixed-lapse Hessian, zero-mode extraction, determinant/Pfaffian ratio와 regulator matching |
| 출력 | relative superdeterminant table와 zero-mode conditions |
| 성공 의미 | 지정한 regulator에서 상대 cancellation의 정확한 범위를 정한다 |
| 실패 의미 | cancellation이 없거나 regulator 의존임을 보인다. contour/absolute sign은 여전히 미결 |
| 의존성 | 4.1 |

### 4.3 `bfv_gauge_slice_orbit_coverage`

| 항목 | 내용 |
|---|---|
| 입력 | declared finite gauge family, gauge slice, gauge-orbit parameter domain |
| 계산 | FP determinant zero, copy, orbit coverage와 boundary crossing census |
| 출력 | admissible/inadmissible slice 판정과 Gribov ledger |
| 성공 의미 | finite model에서 gauge-fixing이 무엇을 덮는지 명확해진다 |
| 실패 의미 | 그 slice를 measure에 사용하지 못한다; absolute obstruction의 증명은 아니다 |
| 의존성 | 4.1 |

### 4.4 `bfv_relative_lapse_contour_audit`

| 항목 | 내용 |
|---|---|
| 입력 | explicit lapse contour, endpoints, singular divisor, Stokes chamber, asymptotic convergence criterion |
| 계산 | relative-cycle admissibility, convergence, deformation/Stokes crossing table |
| 출력 | contour class ledger와 unclassified ends |
| 성공 의미 | 선언한 finite/integrable model에서 contour 후보가 typed relative class를 이룬다 |
| 실패 의미 | contour가 수렴하지 않거나 endpoint data가 부족함을 보인다 |
| 의존성 | 4.2, 4.3 |

### 4.5 `bfv_two_slab_gluing_identity`

| 항목 | 내용 |
|---|---|
| 입력 | 4.1–4.4, 같은 regulator/polarization의 two-slab kernels와 interface measure |
| 계산 | (K_{02}=\int K_{01}K_{12})의 interface pairing, ghost orientation, zero-mode compatibility |
| 출력 | gluing identity error/remainder 및 orientation dependence |
| 성공 의미 | 선언한 finite regulated model의 composition law를 확인한다 |
| 실패 의미 | gluing defect의 위치를 interface, zero mode, contour, regulator 중 하나로 남긴다 |
| 의존성 | 4.2, 4.3, 4.4 |

## 5. 두 clock의 relational observable 비교

### 5.1 `relational_two_clock_classical`

| 항목 | 내용 |
|---|---|
| 입력 | 하나의 fixed (V\ne0) background, scalar clock (phi), geometric clock (alpha=\log a), gauge flow |
| 계산 | complete observable (O_f(\tau)), gauge invariance, FP determinant와 monotonic branch를 비교 |
| 출력 | clock chart domains, turning-point/FP-zero flags, classical observable comparison |
| 성공 의미 | 각 clock이 적용되는 branch와 겹치는 영역을 명시한다 |
| 실패 의미 | bounce에서 전역 단일 clock을 쓸 수 없음을 드러낸다; dynamics의 반증은 아니다 |
| 의존성 | 6.1의 background convention ledger |

### 5.2 `relational_two_clock_quantum_toy`

| 항목 | 내용 |
|---|---|
| 입력 | finite spectral constrained model, group averaging, 두 deparametrization clock, physical inner-product convention |
| 계산 | rigging map, branch projector, conditional evolution, clock-change map과 unitarity |
| 출력 | clock별 physical Hilbert-space/form과 equivalence/mismatch witness |
| 성공 의미 | 선언한 toy model에서 clock dependence를 검증 가능한 형태로 보인다 |
| 실패 의미 | clock-change map이 domain/unitarity에서 막힘을 기록한다 |
| 의존성 | 없음; 5.1의 실제 background와는 별도 calibration |

### 5.3 `relational_s3_perturbation_observable`

| 항목 | 내용 |
|---|---|
| 입력 | 2.3, 5.1, linear scalar perturbations, gauge-invariant variable convention |
| 계산 | clock-conditional Dirac observable과 reduced gauge-invariant variable의 equality를 linear order에서 검사 |
| 출력 | relational mode observable, gauge/clock comparison ledger |
| 성공 의미 | 지정한 branch와 linear order에서 observable map을 얻는다 |
| 실패 의미 | gauge choice, clock degeneracy 또는 missing constraint term을 분리해 기록한다 |
| 의존성 | 2.3, 5.1 |

## 6. (V\ne0) BO·decoherence·CLASS/Cobaya 연결

### 6.1 `closed_inflation_background_export_audit`

| 항목 | 내용 |
|---|---|
| 입력 | 선택한 (V(\phi)), units, closed-FRW initial-data convention, reheating parameterization |
| 계산 | background equations, constraint residual, slow-roll/end-of-inflation markers, input/output unit audit |
| 출력 | reproducible background table와 explicit free parameters |
| 성공 의미 | perturbation 계산의 정확한 background input을 고정한다 |
| 실패 의미 | potential/initial data가 desired branch를 만들지 못함을 보인다 |
| 의존성 | 없음. 과거 witness를 재실행하지 않고 source/convention을 새로 고정한다 |

### 6.2 `closed_inflation_mode_equation`

| 항목 | 내용 |
|---|---|
| 입력 | 6.1, discrete (S^3) scalar/tensor modes, vacuum/initial-state choice, normalization |
| 계산 | mode evolution, Wronskian conservation, scalar/tensor primordial spectrum table |
| 출력 | (mathcal P_{\mathcal R}(n)), (mathcal P_T(n)), numerical error and initial-state sensitivity |
| 성공 의미 | declared model의 primordial input을 생성한다 |
| 실패 의미 | vacuum/turning point/numerical stiffness dependence를 공개하며 likelihood 연결을 막는다 |
| 의존성 | 6.1 |

### 6.3 `bo_correction_consistency`

| 항목 | 내용 |
|---|---|
| 입력 | 5.1–5.2의 clock/inner-product decision, 6.1–6.2, WDW factor ordering, stated (M_{\rm Pl}^{-2}) expansion order |
| 계산 | BO hierarchy, corrected Schrödinger equation, norm/current conservation, clock/gauge dependence |
| 출력 | correction terms, retained-order error, inner-product consistency ledger |
| 성공 의미 | 선언한 semiclassical order에서 BO correction의 범위가 명확해진다 |
| 실패 의미 | nonunitarity 또는 clock dependence가 approximation/domain 어디서 오는지 기록한다 |
| 의존성 | 5.1, 5.2, 6.1, 6.2 |

### 6.4 `decoherence_influence_kernel`

| 항목 | 내용 |
|---|---|
| 입력 | 6.2 또는 6.3, system/environment split, initial environment state, coarse graining, regulator |
| 계산 | reduced density matrix 또는 influence functional, off-diagonal suppression, regulator/environment sensitivity |
| 출력 | decoherence functional, suppression regime, dependence ledger |
| 성공 의미 | 선택한 environment에서만 branch interference가 얼마나 줄어드는지 계산한다 |
| 실패 의미 | suppression이 없거나 cutoff dependent임을 보인다. WKB만으로 고전성이 증명되지 않는다 |
| 의존성 | 6.2; BO-corrected variant는 6.3 추가 필요 |

### 6.5 `primordial_to_class_adapter`

| 항목 | 내용 |
|---|---|
| 입력 | 6.2의 spectrum, curvature convention, interpolation/extrapolation rule, fiducial non-flat benchmark |
| 계산 | discrete closed-(S^3) spectrum을 Boltzmann-code primordial input convention으로 변환하고 unit/normalization regression |
| 출력 | versioned small spectrum adapter, benchmark residual, unsupported-scale flags |
| 성공 의미 | external Boltzmann solver에 전달 가능한 명시적 theory interface를 만든다 |
| 실패 의미 | spectrum convention/coverage가 solver interface와 맞지 않음을 보인다 |
| 의존성 | 6.2 |

### 6.6 `cosmology_likelihood_smoke`

| 항목 | 내용 |
|---|---|
| 입력 | 6.5 adapter, exact CLASS/classy and Cobaya versions, official likelihood/data URL·licence·checksum, declared cosmological/nuisance parameters |
| 계산 | fiducial regression과 한 개의 declared model point likelihood evaluation; sampling은 별도 후속 작업 |
| 출력 | environment lock metadata, input checksums, fiducial/model log-likelihood, failure diagnostics |
| 성공 의미 | 한 제한된 model point가 특정 공개 likelihood에 전달됨을 확인한다 |
| 실패 의미 | installation, data convention, prior, theory-domain 중 무엇이 맞지 않는지 분리한다 |
| 의존성 | 6.5; BO/decoherence 결과는 theory choice에 포함할 수 있으나 likelihood 자체의 전제는 아님 |

## 실행 전 공통 계약

각 계산기는 구현 전에 다음을 파일 인접 문서 또는 입력 JSON에 고정한다.

1. primary source와 채택한 식 번호, 모든 sign/measure/boundary convention
2. 입력의 provenance와 hash, cutoff·regulator·test space·domain
3. 성공, 반례, `OPEN`의 각각의 정확한 출력 조건
4. null로 유지할 큰 주장: absolute measure, continuum limit, physical state, physical prediction 중 해당하지 않는 것
5. 120초/1MB 공통 상한 안의 가장 작은 exact 또는 numerical check

`cosmology_likelihood_smoke`만 외부 의존성을 요구한다. 이 계산 이전에는 package 설치,
대형 data download, likelihood 실행을 하지 않는다. 그 전 단계의 모든 계산은 현재의
NumPy/SciPy/SymPy 환경으로 시작할 수 있어야 한다.

## 완료 판정의 해석

이 DAG에서 가능한 좋은 결과에는 null 또는 부정적 결과도 포함된다. 예를 들어 raw-(C)의
extension family가 measurable하지 않음, finite cutoff remainder가 사라지지 않음, 특정 gauge slice가
Gribov copy를 가짐, 두 clock의 unitary map이 없음, 혹은 spectrum이 solver convention을 만족하지
않음은 모두 다음 가정을 좁히는 정상적인 워크벤치 산출물이다.

반대로 어느 한 runner의 `PASS`도 다음을 뜻하지 않는다.

- full quantum-gravity path integral의 존재
- absolute BFV measure 또는 global contour의 선택
- anomaly-free continuum gravity의 증명
- 관측 자료가 ICE를 지지한다는 결론
- 물리학 또는 TOE 주장

그 경계는 결과 JSON, 인접 보고서, 그리고 repository-local ontology가 실제로 claim/evidence
scope를 바꾸는 경우에만 갱신한다.
