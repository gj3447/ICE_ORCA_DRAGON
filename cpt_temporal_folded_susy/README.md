# CPT × Temporal-Folded SUSY — ICE ORCA DRAGON 물리 연구 둥지

> **정책 (사용자 지시 2026-08-11)**: 물리학 연구는 ICE_ORCA_DRAGON(사도 #2, 물리학
> 대통합 — 자연법칙 축) 기반으로 간다. 이 디렉터리가 CPT×TFSUSY 프로그램의 ICE측
> 정본 둥지이며, Phase 12+ 신규 물리 산출물은 여기서 태어난다.

## 역사적 코퍼스

Phase 1–10 전체(102+ 파일: 검증기·manifest·LakatoTree receipt 포함)는
`SYMPOSIUM/FINDINGS/cpt-temporal-folded-susy-2026-08-09/`에 있다. Phase 7/8
manifest·receipt가 그 경로들을 sha-바인딩하므로 **이동하지 않는다** (Longinus
바인딩 보존). 이 둥지는 Phase 11부터의 정본 + 역사 코퍼스로의 포인터다.

## 수록

| 파일 | 내용 |
|---|---|
| `phase11_collar_admissibility.py` | Phase 11 v2 유도·검증 실행체 (단일 명령: `uv run --with sympy python3 phase11_collar_admissibility.py` → exit 0) |
| `PHASE11_COLLAR_ADMISSIBILITY.md` | Phase 11 v2 보고서 — E152–E156 (collar 허용/금지 분류, dilation 부활, 종-혼합 회전-형 강제, shear 조건부 채널) |
| `PHASE12_RESEARCH_CONTRACT.json` | Phase 12 T2 판정 계약 (`POST_HOC`; P12A boundary twist / P12B rigid \(N=1\) witness / P12C local-SUGRA gate 분리) |
| `phase12_boundary_twist_interface.py` | Phase 12 exact 실행체 — collar canonical-removability, rigid BPS wall, scalar formal factorization, multiplet 공통 flavor frame, conditional endpoint covariance 및 의미 변형 검사 |
| `PHASE12_BOUNDARY_TWIST_INTERFACE.md` | Phase 12 보고서 — E157–E162. 보손 collar는 bulk SUSY가 아니며, whole-multiplet rigid \(N=1\) spatial interface witness는 구성; local SUGRA/시간 fold는 OPEN |
| `PHASE13A_RESEARCH_CONTRACT.json` | Phase 13A T2 사전등록 계약 — Lorentzian local-SUGRA branch-\(Q\)의 formal symbol, positive-kernel, closure, physical-domain gate를 실행 전 고정 |
| `phase13a_lorentzian_branch_supercharge.py` | Phase 13A exact 실행체 — Moniz principal-symbol control, finite positive-kernel obstruction, CAR closure countercontrol 및 의미 변형 검사 |
| `PHASE13A_ADVERSARIAL_ERRATUM.json` | 최초 실행의 과도한 core 판정을 원 계약을 수정하지 않고 정정한 `POST_HOC_CORRECTED` 적대검토 기록 |
| `PHASE13A_LORENTZIAN_BRANCH_SUPERCHARGE.md` | Phase 13A 보고서 — E163–E166. 두 algebraic 지름길은 닫혔고 literal branch=superpartner core는 `INCONCLUSIVE/UNCONSTRUCTED` |
| `PHASE14A_RESEARCH_CONTRACT.json` | Phase 14A T2 사전등록 계약 — compact chiral-clock route의 goldstino residual, RT spatial boundary, proper-bulk quotient gate를 결과 전에 고정 |
| `PHASE14A_SOURCE_PACKET.json` | Kallosh·Henneaux·Martínez-Pérez–Ramírez source version/hash/scope와 정규화 bridge의 frozen packet |
| `PHASE14A_CHARGE_LEDGER.json` | 실행 전 동결한 immutable candidate ledger; observed status는 별도 result receipt에 기록 |
| `phase14a_chiral_clock_charge_first.py` | Phase 14A exact 실행체 — bosonic clock, goldstino residual, compact topology, formal quotient와 verdict precedence 검사 |
| `PHASE14A_RUN_RESULT.json` | 최초 실행 및 두 independent replay, observed gates, T2 classification을 담은 post-run receipt |
| `PHASE14A_CHIRAL_CLOCK_CHARGE_FIRST.md` | Phase 14A 보고서 — E167–E170. G2/G3은 닫혔지만 canonical bridge 미구성으로 selected target은 `INCONCLUSIVE/UNCONSTRUCTED` |
| `PHASE15A_RESEARCH_CONTRACT.json` / `PHASE15A_SOURCE_PACKET.json` / `PHASE15A_CONVENTION_MAP.json` / `PHASE15A_MODE_COMPENSATOR_LEDGER.json` | Phase 15A off-shell tangency 입력. 완성 executable commit 전 K1 sign을 관측해 cycle은 실행하지 않고 sequence-invalid로 봉인 |
| `PHASE15A_SEQUENCE_BREACH.json` | Phase 15A의 `INVALID / INCONCLUSIVE / PREREG_OR_PROVENANCE_INVALID` 기록과 K2 방화벽 |
| `PHASE15R_RESEARCH_CONTRACT.json` / `PHASE15R_SOURCE_CONVENTION_PACKET.json` | Known prior를 공개한 fresh T2 reproduction contract와 Hohl/Kallosh 두-source census |
| `phase15r_parent_sign_reproduction.py` | Phase 15R source-native curvature/action/scalar/Legendre/inertia 및 full-offshell coverage 실행체 |
| `PHASE15R_RUN_RESULT.json` / `PHASE15R_REPLAY_RECEIPT.json` | 최초 실행과 독립 replay 영수증. 47 PASS, 17 mutant categories / 18 fixtures, 4 guards |
| `PHASE15R_PARENT_SIGN_REPAIR.md` | Phase 15R 보고서 — E171–E176. Kallosh는 bosonic parent only, frozen census에는 full same-source parent가 없음 |
| `PHASE16_BGG_SOURCE_NOTES.md` | BGG `hep-th/0005225v1` source hash·식·convention 메모; 계약이나 실행 게이트가 아님 |
| `phase16_bgg_single_source.py` | BGG-only curvature/action/Hessian/Hamiltonian과 두 off-shell FLRW tangency witness의 exact 실행체 |
| `PHASE16_BGG_SINGLE_SOURCE.md` | Phase 16 보고서 — E177–E185. bosonic parent PASS, specified strict auxiliary-retaining FLRW tangency FAIL |
| `phase17_time_line_fold_algebra.py` | 스칼라 clock 없이 coordinate time-line 자체를 쓰는 local/reflection/doubled-sheet/SK algebra exact 실행체 |
| `PHASE17_TIME_LINE_FOLD_ALGEBRA.md` | Phase 17 보고서 — E186–E192. literal local half-exchange는 실패; fixed-fiber exchange와 별도 doubled-real projector witness는 성공 |
| `phase18_gaussian_seam_spectrum.py` | free equal-mass Wess–Zumino mode에서 instantaneous canonical seam의 pole·occupation·UV 비용을 가르는 exact 실행체 |
| `PHASE18_GAUSSIAN_SEAM_SPECTRUM.md` | Phase 18 보고서 — 47 exact checks + 1 numerical control. free seam-only pole splitting은 0; interacting/order-parameter route는 OPEN |
| `phase19_closed_sugra_bounce.py` | shift-symmetric/Cecotti SUGRA reduction과 closed \(k=+1\) time-symmetric bounce shooting을 검증하는 exact+numerical 실행체 |
| `PHASE19_CLOSED_SUGRA_BOUNCE.md` | Phase 19 보고서 — 17 exact + 30 numerical checks. 50–60 accelerated-e-fold background는 존재하지만 \(\phi_0\)는 역산 입력이며 CPT/Pin 선택값이 아님 |
| `phase20_two_sheet_wdw_selection.py` | 표준 WDW history와 추가 independent-pair 확률 convention, benchmark slope, F-flatness 및 조건부 curvature–reheating 변환 실행체 |
| `PHASE20_TWO_SHEET_WDW_SELECTION.md` | Phase 20 보고서 — 18 exact + 14 numerical checks. leading envelope는 \(5.442969458\)을 선택하지 않지만 exact two-sheet SUGRA WDW no-go는 아님 |
| `phase21_connected_seam_gaussian.py` | normalized two-sheet Gaussian에서 \(R\), \(R-1\), \(\log R\), flux tail과 sector-prior 의존성을 가르는 exact+numerical 실행체 |
| `PHASE21_CONNECTED_SEAM_GAUSSIAN.md` | Phase 21 보고서 — 27 exact + 7 numerical checks. no-seam baseline은 식별되지만 subtraction과 물리적 flux 확률은 자동 유도되지 않음 |
| `phase22_finite_mode_seam_density.py` | 한 free SUSY oscillator의 TFD-like seam density, graded anti-linear involution, DtN 상관, SK trace identity와 \(\omega\to0\) obstruction을 가르는 exact 실행체 |
| `PHASE22_FINITE_MODE_SEAM_DENSITY.md` | Phase 22 보고서 — 31 exact checks. \(\omega,\beta>0\) finite mode는 양의 정규화 상태를 갖지만 noncompact free zero mode는 trace class가 아님 |
| `phase23_homogeneous_minisuperspace_density.py` | full-real-lapse rigging, KG current, compact spectral density, quadratic zero root와 decompactification을 가르는 exact+numerical 실행체 |
| `PHASE23_HOMOGENEOUS_MINISUPERSPACE_DENSITY.md` | Phase 23 보고서 — 32 exact + 4 numerical checks. supplied \(B_L\)은 regulated density를 만들지만 constraint/CPT-like pairing만으로 그 가중치는 선택되지 않음 |
| `phase24_connected_starobinsky_interval.py` | real connected Starobinsky \(S^3\times I\) saddle, Hamilton-principal Hessian, constraint-null mixed block, fixed-length mutant와 contour obstruction을 가르는 실행체 |
| `PHASE24_CONNECTED_STAROBINSKY_INTERVAL.md` | Phase 24 보고서 — 6 exact + 14 numerical checks. connected response와 rank-one constrained channel은 지지되지만 positive density·physical entropy·thimble 선택은 미유도 |
| `phase25_connected_lapse_scan.py` | full off-shell lapse flow, Hamilton–Jacobi time identity, Schur reduction, Jacobi map, complex constant-phase segment와 real simple fold를 검증하는 실행체 |
| `PHASE25_CONNECTED_LAPSE_SCAN.md` | Phase 25 보고서 — 5 exact + 12 numerical checks. base lapse saddle과 local descent는 계산됐지만 global intersection number와 positive quantum state는 미유도 |
| `phase26_global_lapse_flow.py` | bounded constant-phase complex-lapse continuation, plateau control과 real-fold Airy scaling을 검증하는 실행체 |
| `PHASE26_GLOBAL_LAPSE_FLOW.md` | Phase 26 보고서 — 4 exact + 9 numerical checks. bounded arm과 fold uniformization은 계산됐지만 global endpoint·intersection·state는 미유도 |
| `phase27_lorentzian_lapse_endpoint.py` | Lorentzian--Euclidean Wick map, positive-half-line resolvent와 zero-duration Jacobi/Van Vleck scaling을 검증하는 실행체 |
| `PHASE27_LORENTZIAN_LAPSE_ENDPOINT.md` | Phase 27 보고서 — 13 exact + 8 numerical checks. raw fixed-\(T\) endpoint singularity는 확인됐지만 global PL coefficient와 full gauge-reduced kernel은 미유도 |
| `phase28_thimble_bfv_intersection.py` | bounded branch/dual-cycle crossing과 homogeneous Euclidean-continued BFV--BRST reduction을 검증하는 실행체 |
| `PHASE28_THIMBLE_BFV_INTERSECTION.md` | Phase 28 보고서 — 10 exact + 9 numerical checks. reduced ghost sector 뒤에도 proper length가 남지만 global coefficient·full determinant·physical state는 미유도 |
| `phase29_zero_lapse_uniform_kernel.py` | frozen quadratic short-time kernel의 distributional identity limit, BFV modulus measure와 indefinite-sign obstruction을 검증하는 실행체 |
| `PHASE29_ZERO_LAPSE_UNIFORM_KERNEL.md` | Phase 29 보고서 — 18 exact + 7 numerical checks. local flat endpoint measure에서 raw \(1/N\)은 delta-kernel normalization이지만 physical WDW measure·all-orders kernel·global PL coefficient는 미유도 |
| `../ontology/cpt-temporal-folded-susy/graph.json` | Phase 15R–29의 concept→claim→evidence→scope→open-problem 연결을 담은 기계 판독 정본 |
| `../ontology/cpt-temporal-folded-susy/README.md` | 위 그래프를 결과 중심으로 읽는 개념 지도와 추적 명령 |

SYMPOSIUM측 원본 커밋: `c1f10f6` (2026-08-11, 5-반박자 적대감사 경유 v2).

## 현재 경계 (Phase 29)

- Phase 11 strong 허용 class와 unrestricted-lapse rescaling을 포함한 weak dilation은 명시한
  가정 아래 open-interval bulk에서 canonical frame change로 제거되며 endpoint
  twist/polarization/boundary generator로 이동한다.
- 정칙 4D rigid \(N=1\) spatial BPS wall에서 scalar/chiralino에 같은 kinematic internal-flavor
  connection이 생기고 scalar differential expressions가 formal factorize되는 witness를 구성했다.
  이것은 physical endpoint detector, pre-Big-Bang branch나 local SUGRA completion의 증명이 아니다.
- Phase 13A의 generic CAR countercontrol은 closure만으로 branch exchange가 따라오지 않음을
  보였고, 양의 finite square-root toy의 physical-kernel map도 정확히 0이었다.
- gauge-independent relational branch projector, 공통 physical domain/inner product, local gauge
  constraint와 구별되는 nonzero \(Q_{\rm phys}\)의 결합은 아직 `UNCONSTRUCTED`다. 따라서 literal
  core는 증명·보편 반증 어느 쪽도 아니며 `INCONCLUSIVE`다.
- Phase 14A는 \(C_B=-p_X^2+p_T^2+p_Y^2\), 양·음 \(p_T\ne0\) clock patch와
  \(\alpha=(p_T^2+p_Y^2)/(2V_0^2a^6)>0\)를 exact하게 재현했다. 그 결과
  goldstino-gauge residual kernel은 0이다.
- Smooth compact \(T^3\)에서 RT spatial-boundary channel은
  `NOT_APPLICABLE_IN_THIS_ROUTE`다. 그러나 differentiable graded matter-SUGRA Dirac generator는
  유도되지 않아 template completeness와 equivalence-class deduplication은 보류됐고 selected
  charge target은 `INCONCLUSIVE_UNCONSTRUCTED`다.
- Phase 15A는 complete executable commit 전에 Hohl parent-sign 결과가 관측되어
  `INVALID / INCONCLUSIVE / PREREG_OR_PROVENANCE_INVALID`로 봉인됐다. 그 cycle의 K2 tangency와
  projector는 평가하지 않았다.
- Fresh Phase 15R은 Hohl/Kallosh source를 섞지 않고 재현했다. Hohl은 first-order kinetic
  inertia \((0,0,3)\)으로 bosonic sign gate를 통과하지 못하고, Kallosh는 \((1,0,2)\)를
  통과하지만 target old-minimal auxiliary/transform coverage가 없다.
- 따라서 frozen two-source census에서는 bosonic target이 `VALID/SUPPORTS`, full same-source
  target이 `VALID/CONTRADICTS/NO_VALID_SINGLE_PARENT_IN_FROZEN_CENSUS`다. 이는 문헌 전체 no-go나
  Temporal-Folded SUSY core 판정이 아니다.
- Phase 16의 BGG 단일-source 계산은 \(\mathcal R=-6Q\), inertia \((1,0,2)\),
  \(H=N(-p_X^2+p_T^2+p_Y^2)/(2V_0a^3)\)를 exact하게 재현해 bosonic parent gap을 닫았다.
- 그러나 같은 BGG 변환식은 source auxiliary \(b_a\)의 constructed spatial projection \(b_i\)와
  spatial spin-3/2 discarded mode에 각각 비영 잔차를 만든다. 따라서 arbitrary homogeneous \(F,\chi\)를 유지하면서 gravity를 strict
  FLRW/gamma-trace sector로 자르는 off-shell truncation은 local SUSY에 tangent하지 않는다.

- Phase 17은 scalar clock과 rolling background를 완전히 제거하고 coordinate \(t\in\mathbb R\) 자체를 계산했다.
  표준 support-local \(Q\)의 \(t<0\leftrightarrow t>0\) cross block은 정확히 0이지만,
  fundamental doubled sheet에서는 \(Q^X_\alpha=X_s\otimes q_\alpha\)가 표준 fixed-energy
  \(N=1\) closure와 양방향 rank-two exchange를 동시에 만족한다.
- 이 algebraic success를 원래 한 실수선의 \(t\mapsto-t\)로 unfold하면 연산자가 비국소적이고
  signed \(P_t\)와 commute하지 않는다. 또한 fixed \(t=0\) seam의 ordinary Lorentzian-real
  closure vector는 \(v^0=|\zeta_1|^2+|\zeta_2|^2\)이므로 비영 보존 parameter가 없다.
- 반면 두 sheet에 각각 제곱이 \(-1\)인 실수구조를 결합한 rank-four real fold projector는
  exact하게 존재한다. 따라서 leading open route는 doubled real sheet-mixing fold candidate +
  각 sheet 내부의 standard SUSY다. Pin/Clifford lift, 두 witness의 common-domain 결합,
  action/conserved charge/physical sheet anchor는 아직 OPEN이다.
- Phase 18은 standard instantaneous Cauchy-data map, unchanged free \(t>0\) bulk와 retarded-pole
  mass 정의 아래 \(m_{B,\mathrm{pole}}^2=m_{F,\mathrm{pole}}^2=m^2\)를 exact하게 보였다.
  Temporal seam은 occupation과 anomalous correlator를 바꾸어 non-SUSY state를 만들 수 있지만
  그 사실만으로 permanent soft mass를 만들지는 않는다.
- 명시적 scalar kick은 \(n_B(k)=\kappa^2/[4(k^2+m^2)]\)를 주지만 sharp limit의 energy density는
  \(\kappa^2\Lambda^2/(16\pi^2)\)로 발산한다. Gaussian finite-duration control은 UV를 누르지만
  strict \(t=0\) theorem 밖의 Born/quench control이다.
- 따라서 full Pin lift와 common variational domain은 여전히 OPEN이고, interacting Wigner
  self-energy, FRW dilution, persistent \(F/D\)-order parameter와 Higgs UV sensitivity도 아직
  계산되지 않았다. 현재 parameter-free pole prediction은 \(\Delta m_{\mathrm{pole}}^2=0\)뿐이다.
- Phase 19는 shift-symmetric quadratic 및 improved Cecotti/no-scale 궤적을 exact하게 축약하고,
  closed \(k=+1\) bosonic 방정식에서 각 potential의 50, 55, 60 accelerated-e-fold bounce를
  독립 shooting으로 재현했다. bounce에서 실제 \(H(0)=0\)이고 안정화 질량식의
  \(H_V^2=V/3\)과는 다르다.
- Phase 19의 각 \(\phi_0\)는 요청한 \(N_{\rm acc}\)에서 역산했다. 따라서
  \(\phi_0=5.44296946\ldots\)은 60-e-fold Starobinsky existence witness이지 CPT/Pin seam의
  초기값 예측이 아니다. fermionic sewing, perturbation, reheating 및 late-time soft scale도
  아직 유도하지 않았다.
- Phase 20의 leading de Sitter/WDW control에서 표준 history weight는 \(e^{2sI}\)이고
  \(e^{4sI}\)는 추가 independent-pair 가정이다. 둘 다 유한 \(\varphi>0\)에서 단조로워
  \(5.442969458\)에 peak가 없다. 다만 exact complex saddle, WDW current/measure, sheet overlap과
  local-SUGRA wavefunction을 풀지 않았으므로 exact two-sheet WDW no-go는 아니다.
- 동일 Phase 20의 \(\Omega_{K0}\)–\(T_{\rm reh}\) 식은 Phase 19 endpoint와 명시적 reheating,
  entropy, \(H_0\) 입력에서 얻는 조건부 변환이다. closed \(k=+1\)에서는 \(\Omega_{K0}<0\)이고,
  이 수식은 curvature 검출이나 seam-derived reheating 예측이 아니다.
- Phase 21은 positive Euclidean Gaussian에서 decoupled-sheet normalization이
  \(R(C=0)=1\)을 exact하게 식별함을 보였다. 하지만 그 항을 제외해 \(R-1\)을 쓰는 것은
  별도 weighting 선택이고, connected vacuum generator는 \(\log R\)이다.
- 단일 flux toy \(A_n=a_0+q^2n^2,\ C_n=\kappa\)에서는 \(R_n-1\)과 \(\log R_n\)이
  \(n^{-4}\)로 감쇠해 합이 유한하다. 그러나 실제 sector difference는
  \(Z_n(0)(R_n-1)\)이고, 이를 보존하면 정규화된 toy \(n=0\) weight가
  \(0.484950\ldots\)에서 \(0.626161\ldots\)로 바뀐다.
- 따라서 finite determinant나 Ramanujan/Abel/zeta finite part만으로 WDW 확률은 생기지 않는다.
  three-form SUGRA가 주는 실제 kernel, flux-sector measure, physical inner product/current 또는
  decoherence functional과 joint \((n,\phi)\) peak는 아직 OPEN이다.
- Phase 22는 한 positive-frequency free SUSY oscillator에 대해 정규화된 TFD-like purification,
  양의 reduced Gibbs density, exact fixed-energy \(\{Q,Q^\dagger\}=2H\), graded anti-linear sheet
  involution과 \(Z_{\rm SK}[J,J]=1\)을 동시에 구성했다.
- 이 결과는 thermal vacuum SUSY가 아니다. \([\rho_+,Q]=0\)이지만
  \(\langle H\rangle=2\omega r/(1-r^2)>0\)이고, \(\Theta_{\rm toy}\)는 spacetime Clifford/Pin lift가
  아닌 occupation-basis real structure다.
- 같은 ansatz의 noncompact \(\omega\to0^+\) limit에서는
  \(Z_B\sim(\beta\omega)^{-1}\), \(\langle x^2\rangle\sim(\beta\omega^2)^{-1}\)로 발산한다.
  이는 interacting inflaton minisuperspace의 no-go가 아니라 free zero-mode completion gate다.
- Phase 23은 \(C=p_T^2-h\)의 full-real-lapse average가 distributional rigging map을 주지만,
  half-lapse는 resolvent이고 \(\delta(C)\) 자체는 bounded density가 아님을 exact하게 분리했다.
- 명시적인 clock/positive-frequency 선택 뒤 compact Dirichlet control에서
  \(B_L=e^{-L\sqrt h}\)를 **입력하면** \(\rho_+=Z_L^{-1}e^{-2L\sqrt h}\)는 positive trace class다.
  그러나 \(L\), regulator와 toy pairing은 cap/CPT/Pin에서 유도되지 않았다.
- equal branch의 signed KG current는 0이어도 induced norm은 양수이고, positive-frequency
  superposition의 local current도 점별 양수가 아니다. 정확 반례는
  \(j_T=-55/(768\pi)\)를 준다.
- quadratic \(E=0\) root에서는 rigging integral이 \(1/\sqrt{2\epsilon}\)로 발산하고 clock FP가
  0이다. 실제 symmetric closed-FRW neck에는 extrinsic/two-patch clock 또는
  deparametrization-free RAQ가 필요하다.
- 이 경계의 claim, exact check, primary source, 적용 범위와 OPEN 항목은
  `../ontology/cpt-temporal-folded-susy/graph.json`에 stable ID로 연결했다. `./ice ontology validate`
  는 그 연결과 artifact hash를 검사하며, 그래프 자체는 연구 계약이나 외부 KG 승격이 아니다.
- Phase 24는 supplied \(\phi_{\rm center}=1\), base proper length \(T_0=0.7\)에서 real connected
  Starobinsky \(S^3\times I\) saddle을 재현하고, endpoint variation에서 proper length를 함께 풀어
  constraint를 유지할 때 \(K_{+-}\)에 한 개의 nonzero homogeneous direction이 남음을 보였다.
- 같은 endpoint를 고정하되 \(T=0.7\)을 모든 variation에서 고정하면 mixed block은 full rank다.
  따라서 rank one은 connectedness만이 아니라 Hamiltonian-constraint reduction의 결과다.
- full boundary Hessian과 real-contour scalar Schur complement는 indefinite다. fixed-\(a_\pm\)
  scalar subblock에서 precision coupling \(\kappa_K=+0.25632\)는 position correlation
  \(\rho_\phi=-0.25632\)에 해당한다. \(0.08756\)-nat 값은 flat-measure pure-two-mode Gaussian diagnostic일 뿐,
  physical seam entropy나 positive WDW density가 아니다. Phase 24의 claim, scope, evidence snapshot과
  OPEN gate는 ontology에 색인되어 artifact hash까지 검증된다.
- Phase 25는 fixed-boundary principal function이 \(T_*=0.7\)에서
  \(W_T=0\), \(W_{TT}=-8.923143\)인 nondegenerate lapse saddle임을 확인했다. 실수 \(T\)는
  \(e^{-W}\)의 local ascent이고, 기록된 constant-phase descent는 허수 방향으로 출발한다.
- augmented \((q,T)\) Hessian의 lapse Schur complement가 Phase 24 constrained Hessian을
  \(10^{-10}\) 이하 상대오차로 재현한다. 따라서 base rank one은 caustic이 아니라 lapse 제거 결과다.
- 같은 real symmetric branch는 \(T_c=9.788625568\)에서 simple Dirichlet fold에 도달한다.
  이는 global single-saddle 해석의 반례지만, global thimble·intersection number·physical Morse index를
  아직 정하지 않는다. Phase 25–29의 claim, scope, evidence snapshot과 OPEN gate는
  현재 ontology에 색인되어 artifact hash와 check ledger까지 검증된다.
- Phase 26은 upper constant-phase lapse arm을 projected \(\operatorname{Im}T\) turn 너머까지
  bounded하게 이어가고, real Dirichlet fold의 square-root/Airy scaling을 확인했다. 그러나 그 arm의
  global endpoint, original contour와의 intersection coefficient와 state normalization은 정하지 않는다.
- Phase 27은 \(N_L=-iT_E\) convention에서 positive Lorentzian lapse가
  \(T_E\in i\mathbb R_+\)로 감을 고정했다. Positive half-line object는 sourced resolvent이고,
  raw fixed-\(T\) two-coordinate Van Vleck magnitude는 \(T\to0\)에서 \(1/|T|\)로 발산한다.
  따라서 zero-lapse contact를 ordinary transverse interior intersection으로 세지 않는다.
- Phase 28의 Euclidean-continued homogeneous BFV--BRST control에서는 Dirichlet ghost reduction 뒤에도
  proper length \(T\)가 global modulus로 남고 \(W_{TT}<0\) 방향은 ghost-cancelled gauge zero mode가 아니다.
  기록한 vertical two-sided segments의 crossings와 local Gaussian factor는 **bounded/conditional**
  diagnostic이며, physical positive-lapse contour의 global coefficient는 아니다.
- string/SUGRA 보강의 현재 설계 경로는
  \(\text{BFV-reduced seam candidate}\to\text{CPT/Pin completion}\to
  \text{double-three-form }N=1\text{ SUGRA}\to
  \text{flux selection}\to F\ne0\to\text{soft terms}\)이다. \(D\)-term branch에는 별도의
  vector/gauging sector가 필요하다. String theory는 flux quantization,
  charged-membrane transition, soft-term map과 modular UV constraint를 제공할 후보지만 temporal seam,
  sector prior 또는 saddle survival을 자동으로 유도하지 않는다.
- Phase 29는 frozen leading real-lapse quadratic kernel을 local flat \(da\,d\phi\) endpoint measure에
  분포로 작용시키면 \(K_{N\to0}=\delta^{(2)}_{\rm flat}\)임을 확인했다. Pointwise \(1/N\)은
  이 범위에서 identity-kernel normalization이지 그 자체로 probability divergence가 아니다.
- 같은 fixed-\(s\) reduced BFV normalization에서 Dirichlet ghost와 coordinate Jacobian을 함께
  처리하면 proper-length modulus measure는 overall constant를 제외하고 \(dT\)다. Ghost가 pole을
  지우지 않으며, 임의로 \(N\)을 곱하면 sourced resolvent가 double pole로, group average가
  \(\delta(H)\)에서 \(\delta'(H)\)로 바뀌므로 같은 이론의 재규격화가 아니다.
- Homogeneous kinetic form은 한 양·한 음의 eigenvalue를 가져 하나의 imaginary-lapse sign으로 두
  방향을 동시에 감쇠할 수 없다. 따라서 physical WDW endpoint measure, all-orders uniform kernel,
  conformal-field/lapse cycle, full determinant와 global PL coefficient는 여전히 OPEN이다.

## 다음 계산

고정된 \(t=0\) boundary를 억지로 half-BPS wall처럼 취급하지 않고 다음 해석을 병렬로 유지한다.

- **PL/BFV global gate:** Phase 29의 local-flat leading delta parametrix를 physical WDW endpoint
  measure와 interacting all-orders uniform kernel로 확장한다. Indefinite kinetic form의 conformal-field
  cycle과 lapse cycle, endpoint/lateral prescription과 complete dual cycles를 함께 정해 global
  intersection coefficient를 계산한다. Homogeneous reduced ghost control을 inhomogeneous
  graviton·matter·gravitino·ghost superdeterminant와 BFV/BV Ward identity로 확장해 cutoff와
  gauge-fixing independence를 검사하며, 결과를 바꾸는 ad hoc \(N\) measure insertion은 쓰지 않는다.
- **Three-form seam-kernel gate:** compact three-form SUGRA boundary state 또는 charged-membrane
  saddle에서 실제 \(C_{n\ell}\), charge/tension, boundary ensemble과 determinant prefactor를
  유도한다. 그 뒤에만 regulated determinant와 joint \((n,\phi)\) measure의 내부 peak를 검사한다.
- **Background-state follow-up:** closed \(S^3\)에서 exact complex Starobinsky/SUGRA saddle,
  WDW current/inner product와 CPT/Pin sheet overlap을 함께 정하고, one-loop
  boson–fermion–gravitino determinant가 유한 initial-amplitude peak를 만드는지 계산한다.
- **Regulated-to-cosmological density gate:** Phase 23의 supplied \(B_L\) control을 실제 closed
  Starobinsky complex-cap constraint로 교체한다. Extrinsic/two-patch clock 또는 RAQ, factor
  ordering, primed determinant, collective-coordinate Jacobian과 physical WDW current에서
  \(B_L\) 또는 그 대체 kernel이 유도되는지 먼저 검사한다. 그 뒤 같은 cap에서
  gravitino–Goldstino–ghost boundary operator와 Pfaffian phase를 계산한다.
- **Foundational construction:** 두 complete free Wess–Zumino multiplet을 folded half-line에 놓고,
  Phase 17의 doubled real structure를 쓰는 quadratic bulk-plus-seam action을 직접 변분한다.
  Positive inner product, self-adjoint domain, conserved complex-linear \(Q\), sheet observable을
  한꺼번에 통과해야 한다.
- **Future interacting follow-up:** UV-admissible smooth seam state에서 \(4d\) interacting
  Wess–Zumino Schwinger–Keldysh \(\Pi_B^R(T,p)\)와 \(\Sigma_F^R(T,p)\)를 계산한다. Medium
  quasiparticle shift, boundary transient와 vacuum pole을 분리하고 FRW late-time limit을 취한다.
- **Persistent-breaking gate:** seam이 metastable \(F/D\)-order parameter를 실제로 선택하는지,
  생성된 visible operator가 soft class인지, bulk power sensitivity가 상쇄되는지 검사한다.
- **String-completion gate:** double-three-form \(N=1\) compactification의 실제 flux lattice, membrane
  charge/tension, moduli stabilization과 visible-sector mediation을 고정한 뒤 Phase 24--29 전체를
  재실행한다. Worldsheet BRST/crosscap을 temporal BFV seam과 동일시하지 않고, full modular-invariant
  spectrum이 필요한 UV cancellation은 별도 gate로 둔다.
- **Conservative physical interpretation:** 두 half-history는 CPT/Pin sewing으로 연결하고,
  ordinary SUSY는 각 history 안에서만 작용하게 한다. CPT sewing 자체를 supercharge라 부르지 않는다.
- **Real-time alternative:** Schwinger–Keldysh doubling을 쓰면 정확한 BRST supersymmetry를 얻지만,
  이는 particle superpartner algebra가 아니라 contour unitarity 구조로 분리한다.
- Phase 16 Bianchi-I/full-spin-\(3/2\) reduction은 local-SUGRA auxiliary route로 남기되,
  Phase 17의 coordinate-time fold와 scalar-clock/rolling-background 분석을 다시 섞지 않는다.
