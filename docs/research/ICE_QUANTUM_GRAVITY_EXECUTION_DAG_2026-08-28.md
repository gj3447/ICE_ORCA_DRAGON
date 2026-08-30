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

열 개의 새 번호 없는 계산을 각각 clean definition commit 뒤 `./ice run`으로 실행하고, committed
result를 별도 임시 사본에서 `./ice repro --only ...`로 재현했다. 열 재현 모두 `REPRO`,
`needs-attention 0`이었다.

| 연결부 | 실제로 계산된 것 | 관측 결과 | 줄어든 장애물 | 그대로 남은 장애물 |
|---|---|---|---|---|
| 1 raw-\(C\) zero shell | `raw_c_zero_shell_transversality_jacobian` | 5개 root에서 \(F_\kappa\ne0\), weighted Mellin norm과 5회 quadrature 일치, 조건부 \(1/|\lambda'|\approx0.0641\)–\(0.0747\); boolean 9/9, numerical 3/3 | 선언한 5개 root의 local simplicity와 local weight 후보를 수치로 고정 | \(F_\lambda\)는 moving-boundary Lagrange identity에 조건부다. nonzero-\(\lambda\) Weyl solve, global spectral measure, test space, rigging map과 RAQ는 null |
| 1 raw-\(C\) nonzero-\(\lambda\) local check | `raw_c_nonzero_lambda_weyl_flambda_check` | 두 \(Q_+\), 두 \(Q_-\), 세 차분 간격에서 직접 ODE를 풀어 조건부 정규화 \(F_\lambda\)와 최대 상대오차 \(2.66\times10^{-8}\); exact 4/4, numerical 40/40, ODE 4,305/4,500 | 이전의 conditional identity에 독립적인 finite-cutoff 수치 대조를 추가하고 Wronskian·cutoff 안정성을 고정 | 유한 WKB datum의 exact endpoint limit, 전역 spectral measure, direct-integral test space, rigging map, positivity와 RAQ는 여전히 null |
| 1 raw-\(C\) real plus-tail control | `raw_c_plus_endpoint_liouville_green_tail_bound` | \(Q\ge4\), \(|\lambda|\le10^{-4}\), \(0\le\kappa\le8\)에서 exact 22/22, guard 3/3; \(V_{\rm analytic}=7.73285\times10^{-5}<V_{\rm bar}=9.44889\times10^{-5}\), \(E_{\rm bar}=4.72455\times10^{-5}\) | 무한대 recessive 조건을 \(Q_+=4\) datum으로 바꾸는 실수축 Liouville--Green tail 오차에 처음으로 명시적 균일 예산을 부여 | \(Q=4\to Q_0=-4\) validated transport, endpoint \(F/F_\lambda\), nonreal resolvent/Weyl \(m\), spectral measure, test space와 RAQ는 모두 null |
| 1 raw-\(C\) \(\lambda=0\) differentiated plus-tail | `raw_c_lambda_zero_differentiated_plus_tail` | 다섯 certified root bracket 전체에서 \(h(4)=\partial_\lambda[-u_Q/u]_{0}>0\); exact 9/9, Arb-ball 70/70, guard 6, 개별 폭 \(<4.62\times10^{-26}\), analytic tail \(<6.02\times10^{-28}\) | exact Bessel Green identity와 rigorous finite quadrature/analytic tail로 normalization-invariant \(h(4)\) datum을 좁게 인증 | node-safe \(Q=4\to-4\) sensitivity transport, nonzero-\(\lambda\) tail, normalized \(F_\lambda\), nonreal spectral data, RAQ는 null |
| 1 raw-\(C\) \(\lambda=0\) direct Green endpoint | `raw_c_lambda_zero_node_safe_green_transport` | pole-prone \(h\)를 interior에서 전개하지 않고 smooth \(J=-W=u^2h\)의 direct Bessel Green 적분으로 다섯 bracket의 \(J(-4)>0\), endpoint \(h(-4)>0\); exact 7/7, Arb-ball 61/61, guard 6, REPRO | \(\lambda=0\) five-bracket node-safe endpoint construction을 좁게 닫음 | 기존 \(h(4)\)의 numerical propagation/decomposition, nonzero-\(\lambda\) minus-end \(\Gamma_1\), declared \(F_\lambda\)/root velocity, spectral/RAQ는 null |
| 1 raw-\(C\) declared \(\Gamma_1\) boundary variation | `raw_c_declared_gamma1_boundary_variation` | selected fixed-reference \(\Gamma_1\) identity, zero-shell normalized/K-scaled derivative와 explicit left correction을 다섯 bracket에서 ball-certify; two punctured \(\lambda\) boxes에서는 per-unit declared minus-tail norm correction bound만 기록; exact 11/11, Arb-ball 60/60, guard 6 | \(\lambda=0\) declared-boundary derivative와 omitted left term을 좁게 닫음 | actual nonzero-\(\lambda\) plus-recessive solution, \(\Gamma_1\) value/remainder, continuation/root velocity, uniqueness, spectral/RAQ는 null |
| 1 raw-\(C\) actual nonzero-\(\lambda\) coarse enclosure | `raw_c_actual_nonzero_lambda_gamma1_coarse_enclosure` | root bracket 1과 두 punctured \(\lambda\) box에서 LG-selected actual recessive family를 \(u_\lambda(4)=A_\lambda(4)^{-1/4}\)로 고정하고, \(x\ge3\) Riccati barrier, compact two-state Grönwall, \(Q<-4\) rotating-frame Volterra bound를 결합; exact 14/14, Arb-ball 29/29, guard 6, REPRO | actual family의 존재·유한 endpoint rectangle·완전한 minus-tail remainder와 유한 \(\Gamma_1\) outward interval을 처음 구성 | 두 interval 반경이 약 \(1.1141\times10^{1410}\)이고 모두 0을 포함한다. numerical validated ODE, sharp value/sign, root continuation, spectrum/RAQ는 null |
| 2 closed \(S^3\) all-sector bookkeeping | `closed_s3_full_svt_spectral_ledger` | source-pinned scalar/transverse-vector/TT low-mode transport와 cutoff count; exact 37/37, theorem guard 5; \(N=8\) 총 1,341 modes | 세 sector의 rough/Hodge/명시적 Lichnerowicz convention, 저차 예외와 count 범위를 한 packet에 고정 | `FULL_SVT`는 세 sector를 모두 기록했다는 뜻뿐이다. explicit basis, chirality resolution, Gaunt/Clebsch--Gordan, ADM/HDA는 null |
| 2 closed \(S^3\) cubic curvature packet | `closed_s3_zonal_conformal_curvature_cubic_vertex_ledger` | \(Q_2\) 및 \(Q_1+Q_2\) conformal packet의 \(\sqrt qR\)를 cubic까지 exact 전개; exact 52/52. 두 packet 모두 \(N=2\) 밖 quadratic·cubic tail이 nonzero | 하나의 spatial-curvature subvertex와 비선형 hard-cutoff leakage를 정확한 계수로 고정 | zonal conformal sector 하나뿐이다. full kinetic/shear, matter, lapse/shift, nonzonal/SVT Gaunt, full ADM constraint와 HDA/Jacobi는 null |
| 2 closed \(S^3\) restricted kinetic packet | `closed_s3_zonal_conformal_trace_kinetic_cubic_vertex_ledger` | fixed-\(a\) trace cotangent ansatz에서 canonical \(\Pi\)와 DeWitt factor \(-2\pi G/(3a^3)\)를 고정하고 두 packet을 cubic까지 전개; exact 42/42, 두 \(N=2\) tail 모두 nonzero | curvature packet과 별개인 pure-trace kinetic subvertex 및 cutoff leakage를 정확한 계수로 고정 | \((a,p_a)\), tracefree/shear, matter, lapse/shift와 nonzonal/SVT가 빠진 restricted submanifold다. 두 packet을 합쳐도 full ADM/HDA가 아니다 |
| 2 closed \(S^3\) restricted \(V=0\) scalar-matter packet | `closed_s3_zonal_conformal_v0_scalar_matter_cubic_vertex_ledger` | fixed-\(a\) conformal metric과 scalar cotangent ansatz에서 normal-constraint matter density를 cubic까지 전개; exact 39/39, guard 3/3. aligned \(Q_2\) packet의 \(Q_4\) cubic tail은 항상 nonzero이고 \(Q_6\) tail도 일반적으로 nonzero | curvature·trace-kinetic과 구분된 한 \(V=0\) scalar-matter normal subvertex와 hard-cutoff leakage를 exact coefficient로 고정 | matter shift/momentum constraint, \((a,p_a)\), shear, lapse/shift, nonzonal SVT와 실제 ADM/HDA/Jacobi는 null |
| 2 closed \(S^3\) fixed-background matter \(HH\) packet | `closed_s3_zonal_v0_scalar_matter_hh_bracket_cutoff_ledger` | \(N=Q_1,M=Q_2,\xi=Q_1,\theta=Q_2\)에서 ambient \(HH\)=matter momentum target=\(5/(\pi^2a^2)\); \(L=2\) projected bracket는 0이고 omitted \(k=3\) channel이 전 remainder를 공급, \(L=3,4\)에서는 remainder=0; exact 39/39, guard 3, REPRO | 처음으로 nontrivial fixed-background zonal matter \(HH\) identity와 finite projection defect의 source channel을 exact 분리 | gravity/metric variation, nonzonal SVT, \(DD/DH\), cubic full ADM, Jacobi와 BFV anomaly는 모두 null |
| 5–6 \(V\ne0\) two-clock domain | `homogeneous_closed_frw_starobinsky_two_clock_fp_domain_audit` | \(C_V=0=P\)에서 real-\(p\) domain \(y=e^QV\le3\), scalar-clock zero \(y=3\), \(P\)-clock FP zero \(y=2\), \(Q\)-clock factor zero; exact 12/12 | 이전의 잘못된 informal \(y=3/2\) 값을 제거하고 두 clock chart의 서로 다른 고전 경계를 고정 | 실제 trajectory가 어느 locus를 통과하는지, complete observable, quantum clock map, physical product, BO/decoherence와 likelihood는 null |
| 5–6 \(V\ne0\) local clock-boundary field | `homogeneous_closed_frw_starobinsky_time_symmetric_clock_boundary_local_ledger` | 세 pinned \(\phi_*\) decimal representative에서 \(y=2\)의 두 \(p\) branch는 반대 부호의 \(|\dot y|\approx(5.08,4.65,4.28)\times10^{-7}\), \(y=3,P=p=0\)은 \(\dot y=0\); exact 10/10, numerical 36/36 | \(P=0\) 제약면의 국소 transversality/tangency와 Hamilton vector field를 고정 | 대표점은 초기조건이 아니다. trajectory selection·integration·crossing, complete observable, quantum clock, BO/decoherence와 likelihood는 null |

이 갱신은 세 갈래를 완성하지 않았다. 다음 독립 질문은 각각 (a) coarse actual
nonzero-\(\lambda\) \(\Gamma_1\) envelope를 Bessel/LG-preconditioned validated interval
transport로 좁혀 sign/continuation을 판별하고 nonreal resolvent·전역 spectral/test-space 자료를 닫을 수 있는가,
(b) fixed-background zonal matter \(HH\) control 위에 명시적 저차 nonzonal SVT representative와
Gaunt data, scale/shear·gravity·lapse/shift 항을 합쳐
실제 off-shell ADM coefficient를 구성하는가, (c) 물리적
해석과 분리된 명시적 seed protocol을 먼저 선언한 뒤에만 Starobinsky trajectory crossing을 적분할 것인가이다.
어느 결과도 다른 질문의 실행 또는 물리적 승격을 자동 승인하지 않는다.

### 2026-08-29 P1 exact-Bessel 추가 갱신

`python-flint==0.9.0`을 lock한 뒤 번호 없는
`raw_c_lambda_zero_bessel_ball_transport`를 clean committed source에서 실행하고
격리 재현했다. 정확히 \(\lambda=0\)에서 modified-Bessel \(K_{i\kappa}\)가
recessive 해이므로 \(+\infty\to Q_0=-4\)의 실수 direction을 수치 fundamental
matrix 없이 고정했다. exact 4/4, Arb ball 35/35, theorem/scope guard 5개가
통과했고, 다섯 disjoint bracket 각각에서 at-least-one real sign-changing zero를
인증했다. `./ice repro --only raw_c_lambda_zero_bessel_ball_transport`는 `REPRO`,
needs-attention 0이었다.

그 뒤 `raw_c_lambda_zero_differentiated_plus_tail`을 별도 clean committed
runner로 실행했다. exact Bessel Green identity, rigorous finite `acb.integral`과
analytic improper-tail bound가 exact 9/9, Arb-ball 70/70, guard 6개를 통과했고,
다섯 bracket 전체의 scale-invariant \(h(4)\)를 인증했다. 격리 재현은 `REPRO`,
needs-attention 0이다.

그 다음 `raw_c_lambda_zero_node_safe_green_transport`는 smooth
\(J=-W(u,\partial_\lambda u)=u^2h\)를 exact Bessel Green integral로 직접
\(Q_0=-4\)에 구성했다. 여섯 finite subsegment와 analytic \(x\ge32\) tail을
결합한 run은 exact 7/7, Arb-ball 61/61, guard 6개와 다섯 bracket 5/5를
통과했고 격리 재현도 `REPRO`였다. 이는 \(h(4)\) state propagation이 아니라
direct node-safe endpoint construction이다.

따라서 1.3의 \(\lambda=0\) anchor, 다섯 bracket의 differentiated plus-tail과
direct \(J(-4),h(-4)\) endpoint까지 완료됐다. 각 root의
uniqueness/completeness, nonzero-\(\lambda\) minus-end \(\Gamma_1\), declared
\(F_\lambda\), nonreal Weyl \(m\), spectral measure, test space와 RAQ는 여전히
null이다. P1부터 P7까지의 가정·실패조건·문헌 역할과 연결은
[`ICE_SIX_BRIDGE_METACOGNITIVE_PRIORITY_ONTOLOGY_2026-08-29.md`](ICE_SIX_BRIDGE_METACOGNITIVE_PRIORITY_ONTOLOGY_2026-08-29.md)에
분리했다.

raw-\(C\)의 정확한 남은 인증 순서와 현재 nonzero-\(\lambda\) minus-end boundary 공백은
[`RAW_C_ENDPOINT_CERTIFICATION_REQUIREMENTS_2026-08-29.md`](RAW_C_ENDPOINT_CERTIFICATION_REQUIREMENTS_2026-08-29.md)에
분리했다.

### 2026-08-30 P1 declared-\(\Gamma_1\) scoped update

`raw_c_declared_gamma1_boundary_variation`은 selected \(\Gamma_{1,p}=0\)
reference domain을 그대로 둔 번호 없는 bounded run이다. exact 11/11,
Arb-ball 60/60, theorem/scope guard 6개가 통과했다. 다섯 inherited full
\(\kappa\) bracket에서 zero-shell normalized/K-scaled declared
\(\partial_\lambda\Gamma_1\)와 omitted left correction을 인증했고, 두
punctured real \(\lambda\) box에서는 declared minus-tail \(L^2(f\,dQ)\) norm
per unit correction-functional operator bound만 기록했다.

이것은 actual nonzero-\(\lambda\) plus-recessive solution이나
\(\Gamma_1(u_\lambda)\) value/remainder를 만든 결과가 아니다. 따라서 root
continuation/velocity, uniqueness/completeness, nonreal Weyl data, spectral
measure, raw-\(C\) RAQ, \(C/H\) equivalence와 모든 physics/quantum-gravity/TOE
출력은 null이다. P1의 다음 독립 공백은 같은 fixed domain에서 actual
\(u_\lambda\)와 minus-end remainder를 validated하게 구성하는 일이다.

### 2026-08-30 P1 actual-family coarse-enclosure update

`raw_c_actual_nonzero_lambda_gamma1_coarse_enclosure`는 위 공백을 sharp
validated ODE 없이도 한 단계 좁혔다. 기존 DLMF/LG bound가 선택한 실제
recessive direction을 \(Q=4\)에서 명시적으로 renormalize하고, \(x\ge3\)에서
\(\rho=-u_Q/u-x-1/2\in[-1,1]\)의 inward barrier를 인증했다. 그 아래에서는
node를 허용하는 2성분 Grönwall rectangle을 \(Q=-4\)까지 운반했고, free-rotation
Volterra comparison으로 \(( -\infty,-4]\)의 remainder를 직접 봉입했다.

root bracket 1의 negative/positive \(\lambda\) box 모두에서 finite
\(\Gamma_1\) interval이 나왔고, 80/120-digit same-backend tiers와 exact
\(\lambda=0\) Bessel containment가 통과했다. 그러나 interval은 대략
\([-1.1141\times10^{1410},1.1141\times10^{1410}]\)라서 0을 포함한다. 이는
actual-family existence/boundedness 진전이지 eigenvalue 또는 spectral 발견이
아니다. 다음 P1 계산은 이 폭의 주원인인 compact Grönwall step을
Bessel/LG-preconditioned interval Taylor/transfer enclosure로 교체해야 한다.

### 2026-08-30 P2 scoped matter-\(HH\) update

`closed_s3_zonal_v0_scalar_matter_hh_bracket_cutoff_ledger`는 fixed background,
zonal, \(V=0\) matter 범위에서 처음으로 nonzero \(HH\) packet을 계산했다.
\(N=Q_1,M=Q_2,\xi=Q_1,\theta=Q_2\)에서 continuum/full-before-project 값과
matter momentum target은 모두 \(5/(\pi^2a^2)\)이다. \(L=2\) projection은
필요한 \(k=3\) canonical derivative channel을 잘라 bracket을 0으로 만들고,
그 차이 전체가 exact projection remainder다. \(L=3,4\)에서는 그 channel이
복구되어 remainder가 정확히 0이 된다.

따라서 이 finite defect는 anomaly가 아니라 누락 mode의 provenance가 명시된
cutoff artifact다. 동시에 이것은 gravity를 포함한 off-shell ADM/HDA closure가
아니다. 다음 P2 단위는 gravitational Hamiltonian/momentum contributions와
metric variation을 같은 packet에 추가한 뒤 \(DD,DH,HH\)를 비교하는 것이다.

Starobinsky local ledger의 최초 `..._p0_...` 경로는 제어면의 numbered-phase token 검사에 의해 Python
실행 전에 차단됐다. 이를 무번호 의미가 명백한 `..._time_symmetric_...`로 rename·commit한 뒤 실행했으며,
차단된 시도에서는 result artifact나 과학적 출력이 생기지 않았다.

## 의존성 지도

```text
1 raw-C global operator
  └─► 1.3 endpoint/spectral certification ─► 1.4 RAQ
        └─► 1.5 rescaling-equivalence comparison

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

### 1.3 `raw_c_endpoint_spectral_certification`

| 항목 | 내용 |
|---|---|
| 입력 | 1.2 operator, real plus-tail bound, selected boundary condition, real/complex spectral-parameter boxes |
| 계산 | validated \(Q_+\to Q_0\) transport와 endpoint \(F/F_\lambda\) enclosure를 먼저 만들고, 별도 nonreal resolvent에서 Weyl \(m\)-함수·spectral transform 자료를 검사 |
| 출력 | real endpoint enclosure, unresolved subboxes, nonreal resolvent/\(m\)-function ledger와 선언한 extension의 spectral measure 후보 |
| 성공 의미 | 선택한 extension과 parameter scope 안에서 RAQ가 참조할 spectral data가 인증됨 |
| 실패 의미 | tail, compact transport, complex resolvent 또는 boundary-value 단계 중 닫히지 않는 위치를 기록함. 실수 root 표만으로 spectral measure를 선언하지 않음 |
| 의존성 | 1.2; 상세 순서는 `RAW_C_ENDPOINT_CERTIFICATION_REQUIREMENTS_2026-08-29.md` |

### 1.4 `raw_c_raq_zero_fiber`

| 항목 | 내용 |
|---|---|
| 입력 | 1.2 operator, 1.3 spectral data, dense test space, lapse/group-average regularization, physical sesquilinear-form convention |
| 계산 | spectral/distributional zero fiber, rigging form positivity, null quotient와 candidate observable action을 검사 |
| 출력 | RAQ form, its null space, regularization dependence ledger |
| 성공 의미 | 선언한 operator와 test space에 대한 physical-form 후보가 정의된다 |
| 실패 의미 | zero fiber가 singular하거나 form이 positive/finite가 아님을 기록한다 |
| 의존성 | 1.2, 1.3 |

### 1.5 `constraint_rescaling_quantum_comparison`

| 항목 | 내용 |
|---|---|
| 입력 | 1.4 raw-(C) RAQ data, 비교 대상 (H=fC)의 domain/RAQ data, 허용 intertwiner와 observable class |
| 계산 | spectral multiplicity, zero-fiber measure, domain map, selected observable intertwining을 비교 |
| 출력 | `EQUIVALENT_IN_DECLARED_CLASS`, `INEQUIVALENT_WITNESS`, 또는 `OPEN` |
| 성공 의미 | 명시한 class 안에서만 양자 동치 또는 반례가 나온다 |
| 실패 의미 | 비교에 필요한 domain/observable이 정의되지 않았음을 뜻한다 |
| 의존성 | 1.4 및 비교 대상의 독립 domain audit |

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
