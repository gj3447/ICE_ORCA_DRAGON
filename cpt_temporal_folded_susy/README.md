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

SYMPOSIUM측 원본 커밋: `c1f10f6` (2026-08-11, 5-반박자 적대감사 경유 v2).

## 현재 경계 (Phase 12)

- Phase 11 strong 허용 class와 unrestricted-lapse rescaling을 포함한 weak dilation은 명시한
  가정 아래 open-interval bulk에서 canonical frame change로 제거되며 endpoint
  twist/polarization/boundary generator로 이동한다.
- 정칙 4D rigid \(N=1\) spatial BPS wall에서 scalar/chiralino에 같은 kinematic internal-flavor
  connection이 생기고 scalar differential expressions가 formal factorize되는 witness를 구성했다.
  이것은 physical endpoint detector, pre-Big-Bang branch나 local SUGRA completion의 증명이 아니다.

## 다음 관문 (Phase 13 후보)

1. P12B full quadratic Green function / normalizable mode / nonadiabatic mixing — reduced
   frame component가 실제 anchored response로 살아남는가
2. P12C specified matter-coupled 4D local-SUGRA uplift — warped background, gravitino/chiralino,
   boundary domain, positivity와 constraint closure
3. internal flavor와 cosmological anisotropy/curvature mode 사이의 독립 embedding map
4. strong vs weak 기준의 물리 판정 및 기존 shear/boost 스펙트럼-도메인 문제
