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

SYMPOSIUM측 원본 커밋: `c1f10f6` (2026-08-11, 5-반박자 적대감사 경유 v2).

## 현재 경계 (Phase 13A)

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

## 순서 게이트와 다음 관문

Phase 13A의 사전등록 support 조건은 실제 relational \(Q_{\rm phys}\) 구성을 요구했다. 이 gate가
열리지 않았으므로 core 순서는 여기서 멈춘다.

1. literal core를 다시 열려면 chiral clock을 포함한 4D \(N=1\) Lorentzian reduction에서
   self-adjoint relational expansion projector, 공통 physical product/domain, nonzero residual 또는
   boundary fermionic charge를 먼저 구성해야 한다.
2. P12B full Green function/S-matrix는 별도 **spatial-interface auxiliary** 연구로만 수행할 수
   있으며, Phase 13A gate 전에는 cosmological branch 주장에 대한 evidence weight가 0이다.
3. 이산/anomaly-fixed wall과 higher-derivative bounce는 auxiliary response가 non-null이고 각각의
   독립 preregistration이 있을 때만 연다. spatial wall의 시간 analytic continuation은 증거로 쓰지 않는다.
