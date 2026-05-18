# 사용자 등록 walkthrough — 5분 안에 끝내기 (2026-05-19)

> AI 측 외부 web form 입력 불가 (browser + 비밀번호 + email verification + 개인정보). 사용자 직접 작업 필수.
> 본 문서 측 5분 절차 + 등록 완료 후 AI inject 자동화 ready.

---

## STEP 1 — ORCID 등록 (~2분)

### 1.1 접속
https://orcid.org/register

### 1.2 form 입력
| 필드 | 값 |
|---|---|
| **First name** | 라경준 (또는 Lagyeongjun) |
| **Last name** | (한국 이름 측 전체 합쳐 First에 넣어도 OK; 별도 Last 안 써도 됨) |
| **Primary email** | gj3447@gmail.com |
| **Confirm primary email** | gj3447@gmail.com |
| **Password** | 사용자 측 결정 (8자 이상, 숫자+문자) |
| **Confirm password** | 동일 |
| **Visibility** | "Everyone" 추천 (publish 측 paper 측 cite 위해) |

### 1.3 reCAPTCHA + agree to terms

### 1.4 이메일 verification
- gj3447@gmail.com inbox 측 ORCID 측 verify link 측 도착 (~1분 내)
- 클릭 → 등록 완료

### 1.5 ORCID ID 확인
완료 시 16-digit ID 부여 (예: `0000-0001-2345-6789`).
ID 측 본 작업 영역 측 사용자 직접 paste 측 알려주시면 AI 측 자동 inject:
- `papers/asymmetric_lakatos_paper_draft_2026-05-18.md` frontmatter ⟨pending registration⟩ → 실제 ID
- `papers/prereg_lakatos_methodology_paper_draft_2026-05-18.md` 동일
- `papers/COVER_LETTER_EJPS_asymmetric_lakatos.md` ⟨pending⟩ → 실제 ID
- `papers/COVER_LETTER_Synthese_prereg_lakatos.md` 동일

---

## STEP 2 — EJPS Editorial Manager 계정 (~2분)

### 2.1 접속
https://www.editorialmanager.com/euij

### 2.2 "Register Now" → 계정 생성
| 필드 | 값 |
|---|---|
| First name | 라경준 |
| Last name | (한국 이름 측 전체 First) |
| Username | 사용자 측 결정 (gj3447 추천) |
| Email | gj3447@gmail.com |
| Password | 사용자 측 결정 |
| ORCID | STEP 1 측 ID paste |
| Institution | "Independent Researcher" (소속 없음) |
| Country | South Korea (Republic of Korea) |
| Personal Classifications | Philosophy of Science / History and Philosophy of Physics / Logic |
| Personal Keywords | Lakatos / hypercomplex algebra / pre-registration / category theory |

### 2.3 이메일 verification 동일

### 2.4 로그인 확인
대시보드 측 진입 시 등록 완료.

---

## STEP 3 — Synthese Editorial Manager 계정 (~2분)

### 3.1 접속
https://www.editorialmanager.com/synt

### 3.2 "Register Now" — STEP 2 측 동일 절차

(주의: ORCID 측 EJPS 등록 시 측 자동 sync 측 가능 — Editorial Manager 시스템 측 ORCID 측 연동 후 같은 ID 인식)

---

## STEP 4 — arXiv 측 endorsement OR PhilSci-Archive (~5분)

### Option A: arXiv 측 endorsement 필요 (philsci.PS 카테고리)
- 첫 submit 측 endorser 1명 필요 (해당 category 측 prior arXiv submission 있는 author)
- 후보: Niels Gresnigt (Cl(8) 측 cited reference, suggested referee)
- 또는 Deborah Mayo (philosophy of science Lakatos lineage)
- 별도 email로 endorsement 요청 측 정중하게

### Option B: PhilSci-Archive 측 endorsement 없이 즉시 submit (추천)
- https://philsci-archive.pitt.edu/cgi/users/register
- 등록 → cover letter + paper PDF upload → 즉시 public
- EJPS / Synthese 측 "pre-print proof" 측 인정 OK

---

## STEP 5 — AI 측 ORCID ID inject 자동화

사용자 측 STEP 1-3 완료 + ORCID ID (예: `0000-0001-2345-6789`) 측 본 채팅 측 paste 시:

AI 측 자동으로 다음 4 파일 측 inject:
1. `papers/asymmetric_lakatos_paper_draft_2026-05-18.md` frontmatter
2. `papers/prereg_lakatos_methodology_paper_draft_2026-05-18.md` frontmatter
3. `papers/COVER_LETTER_EJPS_asymmetric_lakatos.md`
4. `papers/COVER_LETTER_Synthese_prereg_lakatos.md`

+ commit `feat(orcid-inject): bind real ORCID ID to all paper drafts and cover letters`

---

## STEP 6 — submit 직전 final checklist (사용자 직접)

| 체크 | done? |
|---|---|
| ORCID ID papers + cover letters 측 inject 됨 (AI 측 STEP 5) | ⬜ |
| 사용자 측 cover letters 측 본인 검토 (suggested referee 확인, 정정 가능) | ⬜ |
| AI tool use disclosure 측 본인 확정 (현재 wording: "Manuscript preparation assisted by Claude Code v* under sole-author direction; all theorem statements, proofs, and empirical procedures verified by author.") | ⬜ |
| Pandoc 측 markdown → LaTeX 변환 (선택: 사용자 직접 OR AI 자동) | ⬜ |
| EJPS submission portal 측 upload (paper PDF + cover letter + 4 suggested referees) | ⬜ |
| Synthese submission portal 측 upload (별도) | ⬜ |
| PhilSci-Archive 측 simultaneous deposit (옵션) | ⬜ |

---

## 사용자 측 5분 안 완료 시 — AI 측 즉시 할 수 있는 것

1. ORCID ID inject (4 파일, ~30초)
2. Pandoc LaTeX 변환 (사용자 측 pandoc install 권한 부여 시, ~1분)
3. arXiv LaTeX 측 sn-jnl.cls download + compile (사용자 측 인터넷 OK 시)
4. final proofread + 측 수정
5. AI 측 simultaneous PhilSci-Archive submit guide (사용자 측 계정 OK 시)

---

## 정확한 ETA

- 사용자 직접 작업: **10-15분 총** (ORCID 2 + EJPS 2 + Synthese 2 + verification 5 + final checklist 5)
- AI inject + LaTeX 변환: **~5분**
- 사용자 측 portal upload (EJPS + Synthese): **~10분 each**

→ **이번 주말 안 측 2 paper 측 submit 가능.**

---

## 한 줄

ORCID 측 사용자 직접 등록 5분 → ID 측 paste → AI 측 자동 inject + Pandoc 변환 + submit guide → 사용자 측 portal upload → done.

# KG: user-registration-walkthrough-2026-05-19, orcid-defer-with-specific-blocker
